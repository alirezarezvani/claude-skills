#!/usr/bin/env python3
"""
make_adjudication.py — cards for a human on contested cells (from consensus.py).

The council doesn't resolve contested cells itself — it flags them. This script prepares a convenient fork for the human:
for each flagged cell it shows the options from DIFFERENT runs side by side, so the human chooses blind.

Input: output of consensus.py + the same run*.json.
Output: adjudication.md (for the human) + adjudication.json.

CLI: python make_adjudication.py consensus.json run1.json run2.json [run3.json ...]
        [--out adjudication.md] [--output {human,json}]
     python make_adjudication.py --sample
"""

import argparse
import json
import re
import sys

SAMPLE_CONSENSUS = {
    "summary": {"flagged": ["A1"]},
    "cells": {"A1": {"labels": ["PROMOTER", "DETRACTOR"], "agreement": "split"}},
}
SAMPLE_RUNS = [
    {"A1": {"label": "PROMOTER", "text": "Recommends it, cites the export fix."}},
    {
        "A1": {
            "label": "DETRACTOR",
            "text": "Would not recommend, still distrusts the export.",
        }
    },
]


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


def load_run(path):
    """Loads one mapping run (json) into the shape {cell: {label, text}}."""
    d = _read_json(path)
    out = {}
    for cell, v in d.items():
        out[cell] = v if isinstance(v, dict) else {"label": None, "text": str(v)}
    return out


def main():
    """CLI: prepares adjudication cards for the cells flagged by consensus.py."""
    ap = argparse.ArgumentParser(
        description="Prepare human adjudication cards for cells flagged by consensus.py."
    )
    ap.add_argument("consensus", nargs="?", help="Output of consensus.py")
    ap.add_argument(
        "runs", nargs="*", help="The same run*.json files given to consensus.py"
    )
    ap.add_argument("--out", default=None)
    ap.add_argument(
        "--sample", action="store_true", help="Run on built-in sample consensus + runs"
    )
    ap.add_argument(
        "--output", choices=["human", "json"], default="human", help="Output format"
    )
    a = ap.parse_args()

    if a.sample:
        cons, runs = SAMPLE_CONSENSUS, [dict(r) for r in SAMPLE_RUNS]
    else:
        if not a.consensus or not a.runs:
            sys.exit(
                "error: consensus and >=1 run file are required unless --sample is given"
            )
        cons = _read_json(a.consensus)
        runs = [load_run(p) for p in a.runs]
    flagged = cons.get("summary", {}).get("flagged", [])

    md = [
        "# Adjudication of contested cells (decided by a human, blind)\n",
        f"Flagged by the council: {len(flagged)}. For each — the run options. Choose one or write your own.\n",
    ]
    cards = []
    for cell in flagged:
        md.append(f"\n## {cell}\n")
        info = cons.get("cells", {}).get(cell, {})
        if "labels" in info:
            md.append(
                f"_Run labels: {info.get('labels')} · agreement: {info.get('agreement')}_\n"
            )
        options = []
        for i, r in enumerate(runs, 1):
            e = r.get(cell, {})
            lab = e.get("label")
            txt = (e.get("text") or "").strip()
            md.append(f"- **Option {i}**" + (f" [{lab}]" if lab else "") + f": {txt}")
            options.append({"run": i, "label": lab, "text": txt})
        md.append("\n**Human decision:** _______  · **Why:** _______\n")
        cards.append(
            {"cell": cell, "options": options, "decision": None, "rationale": None}
        )

    out_path = None
    if a.out or not a.sample:
        out_path = a.out or "adjudication.md"
        open(out_path, "w", encoding="utf-8").write("\n".join(md))
        open(re.sub(r"\.md$", ".json", out_path), "w", encoding="utf-8").write(
            json.dumps({"cards": cards}, ensure_ascii=False, indent=2)
        )

    if a.output == "json":
        print(
            json.dumps(
                {"out": out_path, "card_count": len(cards), "cards": cards},
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(
            f"Adjudication cards: {len(cards)} → {out_path or '(sample, no --out given)'}"
        )


if __name__ == "__main__":
    main()
