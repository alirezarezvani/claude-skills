#!/usr/bin/env python3
"""training_diagnostics.py — Chapter 11's triage as an executable decision tree.

Chapter 11 argues that knowing many algorithms matters less than knowing which one a
measurement calls for, and gives the rule most teams get backwards: *read training
error first*. High training error means the model or the optimizer is the bottleneck,
and collecting more data will not help.

This tool takes the measurements you already have from a run and returns a ranked
diagnosis, the specific next action, and the chapter that justifies it. Rules fire in
priority order, so a NaN is never diagnosed as overfitting.

The thresholds are documented defaults, not physics — every one is overridable, and
--output json prints the values actually used.

Standard library only. No network calls, no model loading.

Exit codes:
    0  a diagnosis was produced and training looks healthy
    1  a diagnosis was produced and something needs fixing
    2  usage error (argparse)
    4  not enough measurements to diagnose — the missing ones are named
"""

from __future__ import annotations

import argparse
import json
import math
import sys

# Documented defaults. Every one is overridable from the command line.
DEFAULTS = {
    # Relative gap = (val - train) / max(train, floor). Above this, overfitting.
    "overfit_rel_gap": 0.30,
    # Below this relative gap, the run is not overfitting in any actionable sense.
    "healthy_rel_gap": 0.10,
    # Gradient norm above this is a cliff (ch08); clip before anything else.
    "grad_explode": 100.0,
    # Gradient norm below this with non-trivial loss means saturation or dead units.
    "grad_vanish": 1e-6,
    # Divisor floor so a near-zero training loss does not produce an infinite ratio.
    "loss_floor": 1e-6,
    # Training loss above target * this multiple counts as underfitting.
    "underfit_multiple": 1.15,
}


class Finding:
    def __init__(self, rank: int, code: str, verdict: str, evidence: str,
                 action: str, chapter: str) -> None:
        self.rank = rank
        self.code = code
        self.verdict = verdict
        self.evidence = evidence
        self.action = action
        self.chapter = chapter

    def as_dict(self) -> dict:
        return {
            "rank": self.rank,
            "code": self.code,
            "verdict": self.verdict,
            "evidence": self.evidence,
            "action": self.action,
            "chapter": self.chapter,
        }


def diagnose(train_loss: float | None, val_loss: float | None,
             grad_norm: float | None, target_loss: float | None,
             tiny_subset_fits: str, nan_seen: bool,
             epochs: int | None, thresholds: dict) -> tuple[list[Finding], dict]:
    """Return (findings, metrics). Rules fire in priority order; rank 1 acts first."""
    findings: list[Finding] = []
    metrics: dict = {}

    non_finite = (
        nan_seen
        or (train_loss is not None and not math.isfinite(train_loss))
        or (val_loss is not None and not math.isfinite(val_loss))
    )

    # --- Rule 1: numerics before modelling (ch04) -------------------------------
    if non_finite:
        findings.append(Finding(
            len(findings) + 1, "NUMERICS",
            "Loss is NaN or infinite — this is a numerics failure, not a modelling one",
            "a non-finite loss was reported",
            "Check in this order: log(0) or log of a negative, division by a near-zero "
            "denominator, exp of a large logit, then an exploding gradient. Use fused "
            "log_softmax / cross-entropy rather than hand-rolled exp-then-normalize, and "
            "work in log-space for probability products.",
            "ch04 (Numerical Computation)",
        ))
        # A non-finite loss makes every downstream ratio meaningless.
        return findings, metrics

    # --- Rule 2: is it a bug at all? (ch11) -------------------------------------
    if tiny_subset_fits == "no":
        findings.append(Finding(
            len(findings) + 1, "BUG",
            "The model cannot overfit a tiny subset — this is a bug, not a hard problem",
            "--tiny-subset-fits no",
            "Stop tuning. Check the data pipeline (labels aligned with inputs?), the loss "
            "reduction, whether gradients actually reach the parameters (a detached tensor "
            "or a frozen module), and the learning rate. Compare backprop against numerical "
            "derivatives on one layer if it is still unclear.",
            "ch11 (Practical Methodology — debugging strategies)",
        ))

    # --- Rule 3: gradient behaviour (ch08, ch10, ch06) --------------------------
    if grad_norm is not None:
        metrics["grad_norm"] = grad_norm
        if grad_norm > thresholds["grad_explode"]:
            findings.append(Finding(
                len(findings) + 1, "EXPLODING_GRADIENT",
                "Gradient norm is in cliff territory",
                f"grad_norm {grad_norm:g} > {thresholds['grad_explode']:g}",
                "Clip gradients by global norm before changing anything else. If a "
                "recurrence is in the graph, clipping is not optional. Then re-check the "
                "learning rate and the initialization scale.",
                "ch08 (Optimization — cliffs), ch10 (exploding gradients through time)",
            ))
        elif grad_norm < thresholds["grad_vanish"]:
            findings.append(Finding(
                len(findings) + 1, "VANISHING_GRADIENT",
                "Gradient norm is effectively zero — units are saturated or dead",
                f"grad_norm {grad_norm:g} < {thresholds['grad_vanish']:g}",
                "Check for saturating hidden units (sigmoid/tanh in a deep stack), dead "
                "ReLUs from a too-large learning rate, and initialization scale "
                "(He/Xavier). Add residual connections or normalization if the stack is "
                "deep.",
                "ch08 (initialization), ch06 (hidden units), ch10 (vanishing gradients)",
            ))

    # --- Rule 4/5: the fit verdict (ch05, ch07, ch11) ---------------------------
    if train_loss is not None and val_loss is not None:
        denom = max(abs(train_loss), thresholds["loss_floor"])
        gap = val_loss - train_loss
        rel_gap = gap / denom
        metrics.update({
            "train_loss": train_loss,
            "val_loss": val_loss,
            "gap": round(gap, 6),
            "relative_gap": round(rel_gap, 4),
        })

        underfitting = None
        if target_loss is not None:
            metrics["target_loss"] = target_loss
            underfitting = train_loss > target_loss * thresholds["underfit_multiple"]

        if underfitting:
            findings.append(Finding(
                len(findings) + 1, "UNDERFIT",
                "Training error is above target — the bottleneck is capacity or optimization",
                f"train_loss {train_loss:g} > target {target_loss:g} × "
                f"{thresholds['underfit_multiple']}",
                "Do NOT collect more data — it cannot help while training error is high. "
                "In order: tune learning rate and schedule, check initialization, add "
                "capacity, remove regularization you added earlier, train longer.",
                "ch11 (the data-vs-capacity rule), ch08 (Optimization), ch05 (capacity)",
            ))
        elif rel_gap > thresholds["overfit_rel_gap"]:
            findings.append(Finding(
                len(findings) + 1, "OVERFIT",
                "Validation error substantially exceeds training error",
                f"relative gap {rel_gap:.2f} > {thresholds['overfit_rel_gap']}",
                "Work the regularization ladder in cost order, one change at a time: more "
                "real data → label-preserving augmentation → early stopping → decoupled "
                "weight decay (AdamW, not Adam+L2) → label smoothing → dropout. Shrink the "
                "model LAST: past the interpolation threshold, double descent means a "
                "bigger model with more data can generalize better.",
                "ch07 (Regularization), ch05 (capacity and the U-curve's caveat)",
            ))
        elif rel_gap < thresholds["healthy_rel_gap"] and target_loss is None:
            findings.append(Finding(
                len(findings) + 1, "GAP_SMALL_TARGET_UNKNOWN",
                "The train/val gap is small — but without a target loss this cannot "
                "distinguish 'converged' from 'underfitting equally on both splits'",
                f"relative gap {rel_gap:.2f} < {thresholds['healthy_rel_gap']}, "
                "no --target-loss supplied",
                "Supply --target-loss (a human baseline, a published number, or the "
                "irreducible-error estimate for the task) and re-run. Chapter 11's first "
                "step is naming the metric and its target value, and this is why.",
                "ch11 (determine goals: error metric and target value)",
            ))

    if not findings:
        findings.append(Finding(
            1, "HEALTHY",
            "No rule fired — the measurements supplied look healthy",
            "; ".join(f"{k}={v}" for k, v in metrics.items()) or "measurements within thresholds",
            "Confirm the metric you are optimizing is the one you care about, then change "
            "one thing per experiment and keep the log.",
            "ch11 (Practical Methodology)",
        ))

    if epochs is not None:
        metrics["epochs"] = epochs
    return findings, metrics


def render(findings: list[Finding], metrics: dict, thresholds: dict) -> str:
    lines = ["TRAINING DIAGNOSIS", "=" * 68]
    if metrics:
        lines.append("Measurements: " + "  ".join(f"{k}={v}" for k, v in metrics.items()))
        lines.append("")
    for finding in findings:
        lines.append(f"[{finding.rank}] {finding.code} — {finding.verdict}")
        lines.append(f"    evidence : {finding.evidence}")
        lines.append(f"    action   : {finding.action}")
        lines.append(f"    chapter  : {finding.chapter}")
        lines.append("")
    lines.append("Thresholds used: " + ", ".join(f"{k}={v}" for k, v in thresholds.items()))
    lines.append("Rules fire in priority order — act on [1] before anything below it.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Diagnose a training run against Chapter 11's decision tree.",
        epilog="Exit codes: 0 healthy · 1 something needs fixing · 4 not enough input.",
    )
    parser.add_argument("--train-loss", type=float, help="final or current training loss")
    parser.add_argument("--val-loss", type=float, help="matching validation loss")
    parser.add_argument("--target-loss", type=float,
                        help="the loss value that would count as success — a human "
                             "baseline, a published number, or an irreducible-error "
                             "estimate. Without it, underfitting cannot be detected.")
    parser.add_argument("--grad-norm", type=float, help="observed global gradient norm")
    parser.add_argument("--epochs", type=int, help="epochs trained so far (recorded only)")
    parser.add_argument("--nan", action="store_true",
                        help="the loss went NaN or inf at any point")
    parser.add_argument("--tiny-subset-fits", choices=("yes", "no", "unknown"),
                        default="unknown",
                        help="can the model drive training loss to ~0 on 10-50 examples? "
                             "(ch11's smoke test; default: unknown)")
    parser.add_argument("--overfit-rel-gap", type=float, default=DEFAULTS["overfit_rel_gap"])
    parser.add_argument("--healthy-rel-gap", type=float, default=DEFAULTS["healthy_rel_gap"])
    parser.add_argument("--grad-explode", type=float, default=DEFAULTS["grad_explode"])
    parser.add_argument("--grad-vanish", type=float, default=DEFAULTS["grad_vanish"])
    parser.add_argument("--underfit-multiple", type=float,
                        default=DEFAULTS["underfit_multiple"])
    parser.add_argument("--output", choices=("text", "json"), default="text")
    parser.add_argument("--sample", action="store_true",
                        help="run against a built-in overfitting example")
    args = parser.parse_args(argv)

    if args.sample:
        args.train_loss, args.val_loss = 0.02, 1.90
        args.grad_norm, args.epochs = 0.4, 30
        args.tiny_subset_fits = "yes"

    thresholds = {
        "overfit_rel_gap": args.overfit_rel_gap,
        "healthy_rel_gap": args.healthy_rel_gap,
        "grad_explode": args.grad_explode,
        "grad_vanish": args.grad_vanish,
        "loss_floor": DEFAULTS["loss_floor"],
        "underfit_multiple": args.underfit_multiple,
    }

    have_losses = args.train_loss is not None and args.val_loss is not None
    if not have_losses and not args.nan and args.grad_norm is None \
            and args.tiny_subset_fits == "unknown":
        missing = {
            "status": "insufficient_input",
            "need_at_least_one_of": [
                "--train-loss with --val-loss",
                "--grad-norm",
                "--nan",
                "--tiny-subset-fits yes|no",
            ],
            "note": "Chapter 11's first instruction is to instrument the run. This tool "
                    "reads instruments; it does not guess.",
        }
        if args.output == "json":
            print(json.dumps(missing, indent=2))
        else:
            print("NOT ENOUGH INPUT — supply at least one of:")
            for item in missing["need_at_least_one_of"]:
                print(f"  {item}")
            print(f"\n{missing['note']}")
        return 4

    findings, metrics = diagnose(
        args.train_loss, args.val_loss, args.grad_norm, args.target_loss,
        args.tiny_subset_fits, args.nan, args.epochs, thresholds,
    )

    if args.output == "json":
        print(json.dumps({
            "findings": [f.as_dict() for f in findings],
            "metrics": metrics,
            "thresholds": thresholds,
        }, indent=2))
    else:
        print(render(findings, metrics, thresholds))

    return 0 if findings[0].code == "HEALTHY" else 1


if __name__ == "__main__":
    sys.exit(main())
