#!/usr/bin/env python3
"""capacity_planner.py — capacity, the generalization gap, and what to spend next.

Chapter 5 gives the bias-variance budget and the classical U-shaped capacity curve.
Chapter 7 gives the regularizers you spend from that budget. This tool combines them
into one recommendation: given a measured gap and a parameters-per-example ratio, what
is the cheapest next purchase?

It carries one correction the 2016 text predates. The classical advice "shrink the
model when it overfits" assumed the underparameterized side of the U-curve. Past the
interpolation threshold, test error can fall again (double descent; Belkin et al. 2019,
Nakkiran et al. 2020), so in the overparameterized regime this tool ranks *more data,
more regularization, longer training* above *smaller model* and says why.

Standard library only. No network calls.

Exit codes:
    0  a plan was produced and the fit looks balanced
    1  a plan was produced and an action is recommended
    2  usage error (argparse)
    4  inputs are inconsistent (e.g. validation error below training error by a wide
       margin, which usually means a leaky split rather than a good model)
"""

from __future__ import annotations

import argparse
import json
import sys

# Regularization ladder in cost order (ch07). Cost is effort+risk, not compute.
LADDER = [
    ("more-real-data", "Collect more real labelled data",
     "The only intervention that reduces variance without adding bias. Everything below "
     "is a substitute for it.", "ch05, ch07"),
    ("augmentation", "Label-preserving data augmentation",
     "Cheapest substitute for real data where a real invariance exists. Verify the "
     "transform preserves the label — a flip destroys the label on digits.", "ch07"),
    ("early-stopping", "Early stopping on a validation metric",
     "Approximately equivalent to L2 under a quadratic approximation, at near-zero cost. "
     "Usually the first thing to try.", "ch07"),
    ("weight-decay", "Decoupled weight decay (AdamW)",
     "Damps directions the data does not constrain. Use AdamW, not Adam with an L2 term "
     "in the loss — they are not equivalent under an adaptive optimizer.", "ch07, ch08"),
    ("label-smoothing", "Label smoothing",
     "Reduces over-confidence on the training targets; cheap and usually harmless.",
     "ch07 (noise injection on labels)"),
    ("dropout", "Dropout",
     "Approximate ensembling. Note the interaction with batch norm, and that modern "
     "large stacks regularize far more lightly than 2016 practice.", "ch07"),
    ("parameter-sharing", "Structural parameter sharing",
     "The strongest regularizer: remove parameters rather than penalize them. Only valid "
     "when a real invariance exists (convolution, weight tying).", "ch07, ch09"),
    ("smaller-model", "Reduce model capacity",
     "Classical advice from the underparameterized side of the U-curve. In the "
     "overparameterized regime this is ranked last, not first.", "ch05"),
]

# Parameters-per-example ratio bands. Approximate regime markers, not a threshold
# theorem — the interpolation threshold depends on the task, the architecture and the
# label noise, and cannot be read off a parameter count alone.
UNDERPARAMETERIZED_MAX = 1.0
OVERPARAMETERIZED_MIN = 10.0


def classify_regime(params: int, examples: int,
                    under_max: float = UNDERPARAMETERIZED_MAX,
                    over_min: float = OVERPARAMETERIZED_MIN) -> tuple[str, float, str]:
    ratio = params / examples
    if ratio < under_max:
        regime = "underparameterized"
        note = ("Fewer parameters than training examples. The classical U-curve applies "
                "directly here: reducing capacity is a legitimate response to overfitting.")
    elif ratio < over_min:
        regime = "near-interpolation"
        note = ("Roughly at the interpolation threshold, where the classical curve peaks "
                "and double descent begins. This is the worst place to sit: both more "
                "capacity and less capacity can improve test error, so measure rather "
                "than reason.")
    else:
        regime = "overparameterized"
        note = ("Many more parameters than examples. The classical 'shrink the model' "
                "advice is not reliable here — double descent means a larger model with "
                "more data or stronger regularization often generalizes better.")
    return regime, ratio, note


def plan(params: int, examples: int, train_error: float, val_error: float,
         applied: set[str], target_error: float | None,
         overfit_rel_gap: float,
         under_max: float = UNDERPARAMETERIZED_MAX,
         over_min: float = OVERPARAMETERIZED_MIN) -> dict:
    regime, ratio, regime_note = classify_regime(params, examples, under_max, over_min)
    denom = max(abs(train_error), 1e-6)
    gap = val_error - train_error
    rel_gap = gap / denom

    if target_error is not None and train_error > target_error * 1.15:
        verdict = "UNDERFIT"
        headline = ("Training error is above target — capacity or optimization is the "
                    "bottleneck. More data cannot help yet.")
        actions = [
            ("tune-lr-schedule", "Tune learning rate and schedule first",
             "Usually dominates the choice of optimizer family. Warmup plus cosine decay "
             "is the modern default for deep stacks.", "ch08"),
            ("check-init", "Check initialization scale (He / Xavier)",
             "Bad initialization is a common silent cause of a model that will not fit.",
             "ch08"),
            ("remove-regularization", "Remove regularization you already added",
             "Every regularizer you applied is buying variance reduction you cannot "
             "currently afford.", "ch07"),
            ("add-capacity", "Add capacity (width or depth)",
             "Only after the three above — an optimization problem does not respond to "
             "more parameters.", "ch05, ch06"),
        ]
    elif rel_gap > overfit_rel_gap:
        verdict = "OVERFIT"
        headline = (f"Validation error exceeds training error by {rel_gap:.0%} of the "
                    "training error — spend from the regularization budget.")
        ladder = [item for item in LADDER if item[0] not in applied]
        if regime == "underparameterized":
            actions = ladder
        else:
            # Push smaller-model to the end and say why.
            actions = ([item for item in ladder if item[0] != "smaller-model"]
                       + [item for item in ladder if item[0] == "smaller-model"])
    else:
        verdict = "BALANCED"
        headline = ("The gap is within tolerance. Neither more capacity nor more "
                    "regularization is indicated by these numbers.")
        actions = [
            ("verify-metric", "Verify the metric is the one you care about",
             "A balanced fit on the wrong proxy is still the wrong model.", "ch11"),
            ("check-splits", "Confirm the split is clean and the result holds across seeds",
             "A small dataset with one seed is not a measurement.", "ch05, ch11"),
        ]

    return {
        "verdict": verdict,
        "headline": headline,
        "regime": regime,
        "regime_note": regime_note,
        "params": params,
        "train_examples": examples,
        "params_per_example": round(ratio, 3),
        "train_error": train_error,
        "val_error": val_error,
        "gap": round(gap, 6),
        "relative_gap": round(rel_gap, 4),
        "target_error": target_error,
        "already_applied": sorted(applied),
        "actions": [
            {"id": a[0], "action": a[1], "why": a[2], "chapter": a[3]}
            for a in actions
        ],
        "thresholds": {
            "overfit_rel_gap": overfit_rel_gap,
            "underparameterized_max": under_max,
            "overparameterized_min": over_min,
        },
        "double_descent_caveat": (
            regime != "underparameterized" and verdict == "OVERFIT"
        ),
    }


def render(result: dict) -> str:
    lines = [
        "CAPACITY & REGULARIZATION PLAN",
        "=" * 70,
        f"Verdict   : {result['verdict']}",
        f"            {result['headline']}",
        "",
        f"Regime    : {result['regime']} "
        f"({result['params_per_example']} params per training example)",
        f"            {result['regime_note']}",
        "",
        f"Train err : {result['train_error']}   Val err: {result['val_error']}   "
        f"gap: {result['gap']} ({result['relative_gap']:.0%} of train error)",
    ]
    if result["already_applied"]:
        lines.append(f"Applied   : {', '.join(result['already_applied'])} (excluded below)")
    lines += ["", "Do these in order:", "-" * 70]
    for index, action in enumerate(result["actions"], start=1):
        lines.append(f"{index}. {action['action']}  [{action['chapter']}]")
        lines.append(f"   {action['why']}")
    lines.append("-" * 70)
    if result["double_descent_caveat"]:
        lines.append(
            "Double-descent caveat: 'reduce capacity' is ranked LAST here because this "
            "model is at or past the interpolation threshold, where the classical "
            "U-curve advice is unreliable (Belkin 2019, Nakkiran 2020 — both post-date "
            "the book). See references/book_to_2026_delta.md."
        )
    lines.append("Change one thing per experiment and re-measure the gap. (ch11)")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Turn a measured generalization gap into an ordered action plan.",
        epilog="Exit codes: 0 balanced · 1 action recommended · 4 inconsistent inputs.",
    )
    parser.add_argument("--params", type=int, help="trainable parameter count")
    parser.add_argument("--train-examples", type=int, help="number of training examples")
    parser.add_argument("--train-error", type=float,
                        help="training error or loss (same units as --val-error)")
    parser.add_argument("--val-error", type=float, help="validation error or loss")
    parser.add_argument("--target-error", type=float,
                        help="the value that would count as success; without it, "
                             "underfitting cannot be distinguished from convergence")
    parser.add_argument("--applied", default="",
                        help="comma-separated regularizers already in use, from: "
                             + ",".join(item[0] for item in LADDER))
    parser.add_argument("--overfit-rel-gap", type=float, default=0.30,
                        help="relative gap above which the fit counts as overfitting "
                             "(default: 0.30)")
    parser.add_argument("--underparameterized-max", type=float,
                        default=UNDERPARAMETERIZED_MAX,
                        help="params-per-example below which the classical U-curve "
                             f"applies directly (default: {UNDERPARAMETERIZED_MAX})")
    parser.add_argument("--overparameterized-min", type=float,
                        default=OVERPARAMETERIZED_MIN,
                        help="params-per-example above which double descent makes "
                             "'shrink the model' unreliable "
                             f"(default: {OVERPARAMETERIZED_MIN}). These are heuristic "
                             "bands, not a threshold theorem — the interpolation point "
                             "depends on task, architecture and label noise.")
    parser.add_argument("--output", choices=("text", "json"), default="text")
    parser.add_argument("--sample", action="store_true",
                        help="run against a built-in overparameterized example")
    args = parser.parse_args(argv)

    if args.sample:
        args.params, args.train_examples = 12_000_000, 50_000
        args.train_error, args.val_error = 0.01, 0.22
        args.applied = "early-stopping"

    required = (args.params, args.train_examples, args.train_error, args.val_error)
    if any(value is None for value in required):
        parser.error("--params, --train-examples, --train-error and --val-error are all "
                     "required (or use --sample)")
    if args.params <= 0 or args.train_examples <= 0:
        parser.error("--params and --train-examples must be positive")
    if args.underparameterized_max >= args.overparameterized_min:
        # Overlapping bands silently mis-class the regime, and the cost is not
        # cosmetic: an overparameterized model reported as underparameterized ranks
        # "shrink the model" FIRST, inverting the double-descent correction this
        # tool exists to apply.
        parser.error(
            f"--underparameterized-max ({args.underparameterized_max}) must be less "
            f"than --overparameterized-min ({args.overparameterized_min}); the bands "
            "are ordered and must not overlap"
        )

    known = {item[0] for item in LADDER}
    applied = {token.strip() for token in args.applied.split(",") if token.strip()}
    unknown = applied - known
    if unknown:
        parser.error(f"unknown --applied value(s): {', '.join(sorted(unknown))}; "
                     f"choose from {', '.join(sorted(known))}")

    if args.val_error < args.train_error - 0.05 * max(abs(args.train_error), 1e-6):
        payload = {
            "status": "inconsistent_input",
            "reason": "validation error is materially below training error",
            "explanation": "This usually means a leaky split, a validation set that is "
                           "easier than the training set, or regularization active at "
                           "train time but not at eval (dropout, augmentation). Fix the "
                           "measurement before acting on it.",
            "chapter": "ch05, ch11",
        }
        if args.output == "json":
            print(json.dumps(payload, indent=2))
        else:
            print("INCONSISTENT INPUT — " + payload["reason"])
            print(payload["explanation"])
        return 4

    result = plan(args.params, args.train_examples, args.train_error, args.val_error,
                  applied, args.target_error, args.overfit_rel_gap,
                  args.underparameterized_max, args.overparameterized_min)

    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        print(render(result))
    return 0 if result["verdict"] == "BALANCED" else 1


if __name__ == "__main__":
    sys.exit(main())
