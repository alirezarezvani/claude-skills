#!/usr/bin/env python3
"""
consensus.py — a «reliability council» WITHOUT external APIs.

Takes N independent mapping runs of one interview and for EACH cell decides:
stable (all agree) or contested (needs human adjudication — flag).

Why this way: the evidence base (self-consistency ICLR'23; multi-agent debate ICML'24;
LLM-judge flip-rate up to 56%) says — correct conclusions converge across runs, errors are scattered;
a single auto-judge is unreliable. Hence: auto-consensus where there is agreement, and FLAG TO A HUMAN where
the runs diverge. The model does not pick a winner silently.

For cells with a label (eNPS: PROMOTER/NEUTRAL/DETRACTOR etc.) — voting by label.
For free text — stability via pairwise similarity (difflib, stdlib).
Run weight can be set by the share of valid quotes (from verify_quotes.py) — bad runs weigh less.

CLI:
  python consensus.py run1.json run2.json run3.json
       [--weights 1.0,0.8,1.0] [--stability 0.55] [--out consensus.json]

Run format (json):
  { "K1": {"label": null, "text": "..."},
    "A1": {"label": "NEUTRAL", "text": "..."}, ... }
  A flat form is also allowed { "K1": "text", ... } — then label=None.
"""

import argparse
import json
import re
import sys
from difflib import SequenceMatcher
from collections import Counter

LABELS = {  # known label dictionaries for vote normalization
    "enps": {"промоутер", "нейтрал", "детрактор", "promoter", "neutral", "detractor"},
}


def _read_json(path):
    """Read a JSON file; broken JSON or a missing file → a clear error, exit 1."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except OSError as e:
        sys.exit(f"error: {path}: {e.strerror or e}")
    except UnicodeDecodeError as e:
        sys.exit(f"error: {path}: not UTF-8 ({e.reason})")
    except json.JSONDecodeError as e:
        sys.exit(
            f"error: {path}: invalid JSON — line {e.lineno}, column {e.colno} ({e.msg})"
        )


def norm_label(s):
    """Normalizes a label: lowercase, first word, punctuation stripped."""
    if not s:
        return None
    t = re.sub(r"[^\wа-яё]+", " ", str(s).lower()).strip()
    t = t.split()[0] if t else None
    return t


def load_run(path):
    """Loads one mapping run (json) into the shape {cell: {label, text}}."""
    d = _read_json(path)
    out = {}
    for cell, v in d.items():
        if isinstance(v, dict):
            out[cell] = {
                "label": norm_label(v.get("label")),
                "text": v.get("text", "") or "",
            }
        else:
            out[cell] = {"label": None, "text": str(v)}
    return out


def text_stability(texts):
    """Average pairwise similarity of texts (0..1). 1 = identical."""
    texts = [t for t in texts if t.strip()]
    if len(texts) < 2:
        return 1.0 if texts else 0.0
    sims, n = [], len(texts)
    for i in range(n):
        for j in range(i + 1, n):
            sims.append(SequenceMatcher(None, texts[i], texts[j]).ratio())
    return sum(sims) / len(sims) if sims else 1.0


def weighted_vote(labels, weights):
    """Weighted label vote: returns (winning label, agreement level, share)."""
    tally = Counter()
    for lab, w in zip(labels, weights):
        if lab:
            tally[lab] += w
    if not tally:
        return None, "n/a", 0.0
    top, top_w = tally.most_common(1)[0]
    total = sum(tally.values())
    share = top_w / total if total else 0.0
    distinct = len([l for l in labels if l])
    unique = len(set(l for l in labels if l))
    if unique <= 1:
        agree = "unanimous"
    elif share >= 0.5:
        agree = "majority"
    else:
        agree = "split"
    return top, agree, round(share, 2)


SAMPLE_RUNS = [
    {
        "K1": {
            "label": None,
            "text": "Wants to reconcile the budget without losing trust in the export.",
        },
        "A1": {
            "label": "PROMOTER",
            "text": "Would recommend it, cites the export fix.",
        },
    },
    {
        "K1": {"label": None, "text": "Wants to reconcile the monthly budget faster."},
        "A1": {
            "label": "DETRACTOR",
            "text": "Would not recommend, still distrusts the export.",
        },
    },
    {
        "K1": {
            "label": None,
            "text": "Wants a trustworthy budget reconciliation flow.",
        },
        "A1": {
            "label": "PROMOTER",
            "text": "Recommends it now that the export is fixed.",
        },
    },
]


def main():
    """CLI: compares N mapping runs and flags divergent cells for a human."""
    ap = argparse.ArgumentParser(
        description="Compare N independent mapping runs and flag divergent cells for a human."
    )
    ap.add_argument("runs", nargs="*", help="JSON run files (>=2)")
    ap.add_argument("--weights", default=None, help="comma-separated, one per run")
    ap.add_argument(
        "--text-floor",
        type=float,
        default=0.35,
        help="Hard floor of text similarity for LABEL-LESS cells: below = content "
        "diverged substantially → flag. Different wordings with the same meaning do NOT fall here.",
    )
    ap.add_argument(
        "--stability", type=float, default=None, help="deprecated alias of --text-floor"
    )
    ap.add_argument(
        "--grounding-floor",
        type=float,
        default=0.6,
        help="Below this mean run grounding, unanimity is suspicious",
    )
    ap.add_argument("--out", default=None)
    ap.add_argument(
        "--sample", action="store_true", help="Run on 3 built-in sample mapping runs"
    )
    ap.add_argument(
        "--output",
        choices=["human", "json"],
        default="json",
        help="Output format (default json — this script's stdout is machine-consumed by make_adjudication.py)",
    )
    a = ap.parse_args()

    if a.sample:
        runs = [dict(r) for r in SAMPLE_RUNS]
    else:
        if not a.runs:
            sys.exit("error: >=2 run files are required unless --sample is given")
        runs = [load_run(p) for p in a.runs]
    N = len(runs)
    if N < 2:
        print("Need >=2 runs for consensus.", file=sys.stderr)
        sys.exit(1)
    weights = [1.0] * N
    if a.weights:
        weights = [float(x) for x in a.weights.split(",")]
        assert len(weights) == N, "weights must match the number of runs"

    cells = []
    for r in runs:
        for c in r:
            if c not in cells:
                cells.append(c)

    text_floor = a.stability if a.stability is not None else a.text_floor
    report = {}
    flags = []
    low_stab = []
    ungrounded = []
    mean_weight = sum(weights) / len(weights) if weights else 1.0
    for cell in cells:
        entries = [r.get(cell, {"label": None, "text": ""}) for r in runs]
        labels = [e["label"] for e in entries]
        texts = [e["text"] for e in entries]
        has_labels = any(labels)
        stab = text_stability(texts)
        rec = {"stability": round(stab, 2)}
        flag = False
        if has_labels:
            lab, agree, share = weighted_vote(labels, weights)
            rec.update(
                {
                    "label_consensus": lab,
                    "agreement": agree,
                    "label_share": share,
                    "labels": labels,
                }
            )
            # An analytical label (eNPS etc.) is subjective and unstable across runs.
            # Any label disagreement → a human decides. Agreement in substance with different wording is not a flag.
            if agree != "unanimous":
                flag = True
            # Unanimity alone does NOT mean "correct": the runs may have converged
            # because they are biased the same way.
            elif mean_weight < a.grounding_floor:
                ungrounded.append(cell)
                rec["unanimous_but_ungrounded"] = True
        else:
            # no label: flag only on SUBSTANTIAL divergence in content
            if stab < text_floor:
                flag = True
                rec["reason_content_divergence"] = True
        if stab < 0.5:
            low_stab.append(cell)  # soft hint «wordings diverged», not a hard flag
        rec["flag_for_human"] = flag
        if flag:
            flags.append(cell)
        report[cell] = rec

    # Three independent analysis runs agreeing EVERYWHERE is not luck, it is a sign
    # that there was no independence.
    degenerate = N >= 3 and len(cells) >= 5 and not flags
    summary = {
        "runs": N,
        "weights": weights,
        "cells_total": len(cells),
        "cells_flagged": len(flags),
        "flagged": flags,
        "low_stability_hint": low_stab,
        "unanimous_but_ungrounded": ungrounded,
        "council_degenerate": degenerate,
        "note": "flagged = substantive disagreement → a human adjudicates blind. "
        "low_stability_hint = agreement in substance but different wordings (soft, can be ignored). "
        "unanimous_but_ungrounded = the runs agreed but are weakly grounded: that agreement "
        "does not confirm the conclusion, it may mean identical bias (needs --weights = the "
        "runs' verified_share). "
        "council_degenerate = not a single cell diverged: usually means the runs were not "
        "independent — chat history was fed instead of a fresh context (star-model, S3.1).",
    }
    out = {"summary": summary, "cells": report}
    js = json.dumps(out, ensure_ascii=False, indent=2)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(js)

    if a.output == "json":
        print(js)
    else:
        print(
            f"Cells: {summary['cells_total']} | flagged for human: {summary['cells_flagged']}"
        )
        if flags:
            print(f"  Flagged: {flags}")
        if low_stab:
            print(f"  Low-stability hint: {low_stab}")
        if a.out:
            print(f"  → {a.out}")


if __name__ == "__main__":
    main()
