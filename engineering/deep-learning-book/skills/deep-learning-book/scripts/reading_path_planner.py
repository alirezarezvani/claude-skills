#!/usr/bin/env python3
"""reading_path_planner.py — turn a goal into an ordered, prerequisite-closed reading path.

The book's part order is not its dependency order. Read front-to-back and you spend
weeks in Chapters 2-4 before touching a network; skip Part I entirely and Chapter 8
becomes unreadable. This tool takes a goal and a background, resolves the *hard*
prerequisites of the chapters that goal needs, orders them, and prices the result
in weeks at your stated pace.

It refuses two things rather than guessing:
  * a goal whose subject the 2016 book does not cover at all (exit 3) — it names what
    covers it instead, rather than inventing the book's position on RLHF;
  * a goal too vague to route (exit 4) — it prints the questions that would fix it.

Deterministic keyword scoring. Standard library only. No network calls.

Exit codes:
    0  a path was produced
    2  usage error (argparse)
    3  goal is outside the book's scope
    4  goal could not be routed — forcing questions printed
"""

from __future__ import annotations

import argparse
import json
import re
import sys

# --------------------------------------------------------------------------- data

# Hard prerequisites only: skipping one makes the target unreadable, not merely
# harder. Soft prerequisites live in references/prerequisite_map.md and are
# deliberately not enforced here.
PREREQS: dict[int, tuple[int, ...]] = {
    1: (),
    2: (),
    3: (),
    4: (2,),
    5: (3,),
    6: (3,),
    7: (4, 5),
    8: (2, 4),
    9: (6,),
    10: (6,),
    11: (5,),
    12: (6,),
    13: (5,),
    14: (13,),
    15: (14,),
    16: (3,),
    17: (16,),
    18: (16, 17),
    19: (3,),
    20: (13, 19),
}

TITLES: dict[int, str] = {
    1: "Introduction",
    2: "Linear Algebra",
    3: "Probability and Information Theory",
    4: "Numerical Computation",
    5: "Machine Learning Basics",
    6: "Deep Feedforward Networks",
    7: "Regularization for Deep Learning",
    8: "Optimization for Training Deep Models",
    9: "Convolutional Networks",
    10: "Sequence Modeling: Recurrent and Recursive Nets",
    11: "Practical Methodology",
    12: "Applications",
    13: "Linear Factor Models",
    14: "Autoencoders",
    15: "Representation Learning",
    16: "Structured Probabilistic Models for Deep Learning",
    17: "Monte Carlo Methods",
    18: "Confronting the Partition Function",
    19: "Approximate Inference",
    20: "Deep Generative Models",
}

# Planning assumptions, not measurements. Part I and Part III chapters carry higher
# derivation density per page, which is why they cost more than their length suggests.
# Exposed in --output json so a reader can recalibrate against their own first chapter.
BASE_HOURS: dict[int, float] = {
    1: 1.5, 2: 5.0, 3: 6.0, 4: 4.5, 5: 9.0,
    6: 6.0, 7: 6.0, 8: 8.0, 9: 6.0, 10: 7.0, 11: 4.0, 12: 5.0,
    13: 4.0, 14: 4.5, 15: 5.0, 16: 6.0, 17: 5.0, 18: 7.0, 19: 6.0, 20: 8.0,
}

# Background multipliers on the hour estimate.
BACKGROUNDS: dict[str, tuple[float, str]] = {
    "none": (1.6, "little linear algebra or probability — Part I is real work, not review"),
    "math": (0.8, "comfortable with linear algebra and probability, new to ML"),
    "applied": (1.0, "ships models, wants the theory underneath"),
    "research": (0.7, "reads papers in the field; the book is filling gaps"),
}

# Destination lanes. Each is (label, target chapters, note). Scored by keyword hits.
LANES: dict[str, dict] = {
    "practitioner": {
        "label": "Applied practitioner — train models that work",
        "targets": (5, 6, 7, 8, 11),
        "keywords": ("train", "training", "practical", "ship", "production", "apply",
                     "applied", "practitioner", "debug", "tune", "tuning", "improve",
                     "overfit", "underfit", "hyperparameter", "baseline", "workflow"),
        "note": "Chapters 5 and 11 first; they pay off before you finish Part I.",
    },
    "vision": {
        "label": "Computer vision — convolutional models",
        "targets": (6, 7, 8, 9, 12),
        "keywords": ("vision", "image", "convolution", "convolutional", "cnn", "conv",
                     "segmentation", "detection", "pooling", "receptive"),
        "note": "Ch 9's prior-vs-data argument is what explains ViT's data hunger later.",
    },
    "sequence": {
        "label": "Sequence modelling — recurrence, gradients through time, attention",
        "targets": (6, 8, 10, 12),
        "keywords": ("sequence", "rnn", "lstm", "gru", "recurrent", "time series",
                     "timeseries", "nlp", "language", "text", "speech", "translation",
                     "transformer", "attention"),
        "note": "Read Ch 10 for the gradient analysis, not the architecture advice — "
                "see references/book_to_2026_delta.md before applying it.",
    },
    "generative": {
        "label": "Generative modelling — the Part III chain",
        "targets": (13, 14, 16, 17, 18, 19, 20),
        "keywords": ("generative", "vae", "gan", "diffusion", "autoencoder", "sampling",
                     "mcmc", "boltzmann", "latent", "variational", "elbo", "density",
                     "score matching", "partition"),
        "note": "Ch 18 is the chapter whose ideas became diffusion. Do not skip it to "
                "reach Ch 20.",
    },
    "representation": {
        "label": "Representation and self-supervised learning",
        "targets": (5, 13, 14, 15),
        "keywords": ("representation", "embedding", "feature", "features", "transfer",
                     "pretrain", "pretraining", "self-supervised", "unsupervised",
                     "disentangle", "disentangled", "probe"),
        "note": "The bet in Ch 15 was right; every method it lists was replaced. "
                "Read it with the delta reference open.",
    },
    "foundations": {
        "label": "Mathematical foundations — the machinery under everything else",
        "targets": (2, 3, 4, 5),
        "keywords": ("math", "mathematics", "foundation", "foundations", "linear algebra",
                     "probability", "statistics", "theory", "fundamentals", "basics",
                     "prerequisite", "prerequisites", "refresher", "interview"),
        "note": "Pair with a dedicated linear algebra text; Part I is reference "
                "material, not pedagogy.",
    },
    "optimization": {
        "label": "Optimization — why training stalls, diverges, or crawls",
        "targets": (2, 4, 8, 11),
        "keywords": ("optimization", "optimizer", "sgd", "adam", "momentum", "gradient",
                     "converge", "convergence", "diverge", "learning rate", "saddle",
                     "initialization", "batch norm", "normalization", "clipping"),
        "note": "Ch 8 is unreadable without Ch 2 and 4. This is the one place the "
                "prerequisite is genuinely hard.",
    },
    "complete": {
        "label": "Complete read — all twenty chapters",
        "targets": tuple(range(1, 21)),
        "keywords": ("everything", "whole book", "entire book", "all chapters",
                     "cover to cover", "complete", "full read", "read the book",
                     "start to finish"),
        "note": "Even here, read Ch 5 and Ch 11 early rather than in numeric order.",
    },
}

# Subjects the 2016 book does not cover. Naming these beats improvising its position.
OUT_OF_SCOPE: dict[str, str] = {
    "rlhf": "RLHF / preference tuning — published 2017+; nothing in this book covers it.",
    "dpo": "Direct preference optimization — 2023; outside the book entirely.",
    "llm": "Large language model training and serving — the book predates it; see "
           "engineering/llm-cost-optimizer and references/book_to_2026_delta.md.",
    "prompt": "Prompting and in-context learning — post-dates the book.",
    "agent": "Agentic systems — outside the book; see engineering/agent-harness.",
    "mlops": "MLOps tooling and deployment — see engineering-team/senior-ml-engineer.",
    "fine-tun": "Fine-tuning of pretrained foundation models — the book's transfer "
                "learning section (ch15) is the nearest thing, and it is not the same.",
    "lora": "Parameter-efficient fine-tuning (LoRA and relatives) — 2021+.",
    "rag": "Retrieval-augmented generation — outside the book.",
    "mamba": "State-space models — 2021+; ch10's gradient analysis is the relevant "
             "background the book does provide.",
    "fairness": "Fairness, bias auditing and model governance — not treated.",
    "reinforcement": "Reinforcement learning — mentioned only in passing (ch12).",
}

# Tokens whose real surface forms a word-boundary match would otherwise miss.
# Everything else matches itself, optionally pluralized.
SURFACE_FORMS: dict[str, tuple[str, ...]] = {
    "fine-tun": ("fine-tuning", "fine-tune", "fine-tuned", "finetuning", "finetune"),
    "prompt": ("prompt", "prompting", "prompts"),
    "agent": ("agent", "agents", "agentic"),
}


def _matches(token: str, text: str) -> bool:
    """True when token appears in text as a whole word (optionally pluralized).

    Substring matching is wrong here and was a real defect: "rag" appears inside
    "storage", "lora" inside "exploratory", "conv" inside "converge", and "text"
    inside "context" — each one producing a confident false refusal or a wrong lane.
    """
    for form in SURFACE_FORMS.get(token, (token,)):
        # Plain -s only. An -es branch collided with unrelated words: "rag" + "es"
        # matches the standalone word "rages", so a goal about overfitting was
        # refused as out-of-scope RAG work. No token here needs an -es plural —
        # every one ending in s/x/z/ch/sh is already plural or non-count — so any
        # irregular form belongs in SURFACE_FORMS, spelled out.
        if re.search(rf"\b{re.escape(form)}s?\b", text):
            return True
    return False


# --------------------------------------------------------------------------- logic


def close_prerequisites(targets: tuple[int, ...]) -> list[int]:
    """Return targets plus every hard prerequisite, in ascending chapter order."""
    needed: set[int] = set()
    stack = list(targets)
    while stack:
        chapter = stack.pop()
        if chapter in needed:
            continue
        needed.add(chapter)
        stack.extend(PREREQS.get(chapter, ()))
    return sorted(needed)


def order_path(chapters: list[int]) -> list[int]:
    """Order chapters so every hard prerequisite precedes its dependent.

    Among chapters whose prerequisites are already satisfied, the cheapest
    high-value chapter goes first: ch05 and ch11 are promoted because their
    vocabulary is reused everywhere and they are actionable immediately.
    """
    promoted = {5: -2, 11: -1}
    remaining = set(chapters)
    placed: list[int] = []
    while remaining:
        ready = [c for c in remaining if all(p in placed for p in PREREQS.get(c, ()))]
        if not ready:  # unreachable with the current acyclic table; fail loudly if it changes
            raise RuntimeError("prerequisite cycle in PREREQS")
        ready.sort(key=lambda c: (promoted.get(c, 0), c))
        nxt = ready[0]
        placed.append(nxt)
        remaining.discard(nxt)
    return placed


def score_lanes(goal: str) -> list[tuple[str, int]]:
    """Score every lane by keyword hits in the goal text, best first.

    Ties are broken by keyword specificity — the lane whose longest matched
    keyword is longest wins — because an equal hit count between a generic term
    and a discriminating one should not be settled by luck. "train a transformer"
    hits `practitioner` on "train" and `sequence` on "transformer", one each; the
    longer, more specific match is the one that names the subject. Lane key is the
    final tie-break so the ordering stays deterministic.
    """
    text = goal.lower()
    scored = []
    for key, lane in LANES.items():
        matched = [kw for kw in lane["keywords"] if _matches(kw, text)]
        if matched:
            scored.append((key, len(matched), max(len(kw) for kw in matched)))
    scored.sort(key=lambda row: (-row[1], -row[2], row[0]))
    return [(key, hits) for key, hits, _ in scored]


def out_of_scope_hits(goal: str) -> list[str]:
    text = goal.lower()
    return [note for token, note in OUT_OF_SCOPE.items() if _matches(token, text)]


def plan(goal: str, background: str, hours_per_week: float,
         include_intro: bool) -> dict:
    lane_key, _ = score_lanes(goal)[0]
    lane = LANES[lane_key]
    targets = lane["targets"]
    chapters = close_prerequisites(targets)
    if include_intro and 1 not in chapters:
        # ch01 is context, not a prerequisite of anything, so it never arrives via
        # closure — the flag is the only way to reach it outside the complete lane.
        # (An earlier form of this filtered ch01 *out*, which was inert: nothing
        # depends on ch01, and the one lane that targets it skipped the filter.)
        chapters.append(1)
    ordered = order_path(chapters)

    multiplier, background_note = BACKGROUNDS[background]
    entries = []
    for chapter in ordered:
        hours = round(BASE_HOURS[chapter] * multiplier, 1)
        entries.append({
            "chapter": chapter,
            "title": TITLES[chapter],
            "role": "target" if chapter in targets else "prerequisite",
            "hours": hours,
            "file": f"chapters/ch{chapter:02d}-*.md",
            "url": "https://www.deeplearningbook.org/",
        })

    total_hours = round(sum(e["hours"] for e in entries), 1)
    weeks = round(total_hours / hours_per_week, 1) if hours_per_week > 0 else None
    skipped = [c for c in range(1, 21) if c not in ordered]

    return {
        "goal": goal,
        "lane": lane_key,
        "lane_label": lane["label"],
        "background": background,
        "background_note": background_note,
        "hours_per_week": hours_per_week,
        "path": entries,
        "total_hours": total_hours,
        "estimated_weeks": weeks,
        "skipped_chapters": skipped,
        "note": lane["note"],
        "assumptions": {
            "base_hours_per_chapter": BASE_HOURS,
            "background_multiplier": multiplier,
            "basis": "planning heuristic, not measurement — recalibrate after chapter one",
        },
        "hard_prerequisites_applied": {
            str(c): list(PREREQS[c]) for c in ordered if PREREQS.get(c)
        },
    }


# --------------------------------------------------------------------------- output


def render(result: dict) -> str:
    lines = [
        "READING PATH",
        "=" * 64,
        f"Goal        : {result['goal']}",
        f"Lane        : {result['lane_label']}",
        f"Background  : {result['background']} — {result['background_note']}",
        f"Budget      : {result['total_hours']} h at {result['hours_per_week']} h/week"
        f" ≈ {result['estimated_weeks']} weeks",
        "",
        f"{'#':>3}  {'ch':>4}  {'hrs':>5}  role          title",
        "-" * 64,
    ]
    for index, entry in enumerate(result["path"], start=1):
        lines.append(
            f"{index:>3}  ch{entry['chapter']:02d}  {entry['hours']:>5}  "
            f"{entry['role']:<12}  {entry['title']}"
        )
    lines.append("-" * 64)
    if result["hard_prerequisites_applied"]:
        lines.append("Hard prerequisites pulled in:")
        for chapter, prereqs in result["hard_prerequisites_applied"].items():
            names = ", ".join(f"ch{p:02d}" for p in prereqs)
            lines.append(f"  ch{int(chapter):02d} needs {names}")
    if result["skipped_chapters"]:
        skipped = ", ".join(f"ch{c:02d}" for c in result["skipped_chapters"])
        lines.append(f"Not in this path: {skipped}")
    lines.append("")
    lines.append(f"Note: {result['note']}")
    lines.append("Hours are a planning heuristic. Recalibrate after your first chapter.")
    lines.append("Read the chapters free at https://www.deeplearningbook.org/")
    return "\n".join(lines)


SAMPLE_GOAL = "I want to train convolutional models for image classification and debug them"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Plan a prerequisite-closed reading path through the Deep Learning book.",
        epilog="Exit codes: 0 ok · 3 goal outside the book · 4 goal too vague to route.",
    )
    parser.add_argument("--goal", help="what you want to be able to do afterwards")
    parser.add_argument("--background", default="applied", choices=sorted(BACKGROUNDS),
                        help="your starting point (default: applied)")
    parser.add_argument("--hours-per-week", type=float, default=5.0,
                        help="study hours available per week (default: 5)")
    parser.add_argument("--include-intro", action="store_true",
                        help="add ch01 to the path; it is context rather than content, "
                             "so no lane pulls it in on its own (the complete read "
                             "already includes it)")
    parser.add_argument("--output", choices=("text", "json"), default="text")
    parser.add_argument("--sample", action="store_true",
                        help="run against a built-in example goal")
    args = parser.parse_args(argv)

    goal = SAMPLE_GOAL if args.sample else args.goal
    if not goal:
        parser.error("--goal is required (or use --sample)")
    if args.hours_per_week <= 0:
        parser.error("--hours-per-week must be positive")

    scoped_out = out_of_scope_hits(goal)
    lane_scores = score_lanes(goal)
    top_score = lane_scores[0][1] if lane_scores else 0
    # An out-of-scope subject wins over a weak lane match: "LoRA fine-tuning" hits the
    # practitioner lane on the word "tuning" while being entirely outside the book.
    if scoped_out and (len(scoped_out) >= 2 or top_score < 2):
        payload = {
            "status": "out_of_scope",
            "goal": goal,
            "reasons": scoped_out,
            "pointer": "references/book_to_2026_delta.md",
        }
        if args.output == "json":
            print(json.dumps(payload, indent=2))
        else:
            print("OUT OF SCOPE — the 2016 book does not cover this goal.\n")
            for reason in scoped_out:
                print(f"  - {reason}")
            print("\nSee references/book_to_2026_delta.md for what replaced the book's "
                  "position, and route to the skills named above.")
        return 3

    if not lane_scores:
        payload = {
            "status": "unroutable",
            "goal": goal,
            "questions": [
                "What do you want to be able to DO afterwards — train, diagnose, "
                "derive, or evaluate?",
                "Which data type: images, sequences, tabular, or generative modelling?",
                "Is this a refresher over known material or a first pass?",
            ],
            "lanes": {key: lane["label"] for key, lane in LANES.items()},
        }
        if args.output == "json":
            print(json.dumps(payload, indent=2))
        else:
            print("CANNOT ROUTE — the goal does not name a subject in the book.\n")
            print("Answer one of these and re-run:")
            for question in payload["questions"]:
                print(f"  - {question}")
            print("\nOr name a lane directly:")
            for key, label in payload["lanes"].items():
                print(f"  {key:<15} {label}")
        return 4

    result = plan(goal, args.background, args.hours_per_week, args.include_intro)
    if scoped_out:
        result["scope_warnings"] = scoped_out
    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        print(render(result))
        if scoped_out:
            print("\nPartly outside the book — these parts are not covered:")
            for reason in scoped_out:
                print(f"  - {reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
