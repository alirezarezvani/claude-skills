#!/usr/bin/env python3
"""
extract_nuggets.py — from a finished mapping (.md), assemble nugget stubs for synthesis (S5).

Saves the manual gluing of nuggets.json. Pulls a nugget stub for each quote:
  {interview, role, cell, observation, quote, line, verified:null, severity:null, valence:null, cluster:null}
The severity/valence/cluster fields are left null — the model MUST fill them in (it's judgment, not parsing).
verified is filled in by verify_quotes.py.

CLI: python extract_nuggets.py mapping.md --interview "Daria" --role "operations" [--out nuggets.json]
        [--output {human,json}]
     python extract_nuggets.py --sample
"""

import argparse
import json
import re
import sys

# Catches codes: С3.2, С2.П (VMDI), as well as К5/К10, А1, J1, C1, E1
CELL_RE = re.compile(
    r"\*\*\s*([A-Za-zА-Яа-я]{1,2}\d{1,2}(?:\.[\wА-Яа-я]+)?)\s*[|｜]\s*([^*]+)\*\*"
)
QUOTE_RE = re.compile(r"«([^»]{4,})»")
LINE_RE = re.compile(r"\(L?(\d{1,4})\)")

SAMPLE_MAPPING = (
    "**K1 | Job to be done**\n"
    "Needs to reconcile the monthly budget without losing trust in the export.\n"
    "_«I opened three tabs and gave up after twenty minutes» (L2)_\n\n"
    "**A1 | Friction**\n"
    "The export didn't match what was on screen.\n"
    "_«The export didn't match what I saw on screen, so I stopped trusting it» (L4)_\n"
)


def _read_text(path):
    """Read a text file, or exit with a clear error."""
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError as e:
        sys.exit(f"error: {path}: {e.strerror or e}")
    except UnicodeDecodeError as e:
        sys.exit(f"error: {path}: not UTF-8 ({e.reason})")


def main():
    """CLI: assembles nugget stubs from an .md mapping for synthesis (S5)."""
    ap = argparse.ArgumentParser(
        description="Assemble nugget stubs from a finished mapping for synthesis (S5)."
    )
    ap.add_argument("mapping", nargs="?", help="Path to the finished mapping (.md)")
    ap.add_argument(
        "--interview", default=None, help="Required unless --sample is given"
    )
    ap.add_argument("--role", default=None, help="Required unless --sample is given")
    ap.add_argument("--out", default=None)
    ap.add_argument(
        "--sample",
        action="store_true",
        help="Run on a built-in sample mapping, no file needed",
    )
    ap.add_argument(
        "--output", choices=["human", "json"], default="human", help="Output format"
    )
    a = ap.parse_args()

    if a.sample:
        text, label = SAMPLE_MAPPING, "<sample>"
        a.interview = a.interview or "Sample-Respondent"
        a.role = a.role or "customer"
    else:
        if not a.mapping:
            sys.exit("error: mapping is required unless --sample is given")
        if not a.interview or not a.role:
            sys.exit(
                "error: --interview and --role are required unless --sample is given"
            )
        text, label = _read_text(a.mapping), a.mapping
    cur_cell, cur_title, obs = None, None, ""
    nuggets, idx = [], 0
    for ln in text.splitlines():
        m = CELL_RE.search(ln)
        if m:
            cur_cell, cur_title = m.group(1).strip(), m.group(2).strip()
            obs = ""
            continue
        if (
            cur_cell
            and "«" not in ln
            and ln.strip()
            and not ln.startswith(("#", "---", "**", "_", ">"))
        ):
            if len(obs) < 140:
                obs = (obs + " " + ln.strip()).strip()
        for mq in QUOTE_RE.finditer(ln):
            idx += 1
            mline = LINE_RE.search(ln)
            nuggets.append(
                {
                    "id": f"{a.interview[:4]}-{idx}",
                    "interview": a.interview,
                    "role": a.role,
                    "cell": cur_cell or "?",
                    "observation": (cur_title + " — " + obs)[:180]
                    if obs
                    else (cur_title or ""),
                    "quote": mq.group(1).strip(),
                    "line": int(mline.group(1)) if mline else None,
                    "verified": None,  # ← verify_quotes.py
                    "severity": None,  # ← model (1..5, with rationale)
                    "valence": None,  # ← model (+/-/0)
                    "cluster": None,  # ← model (S6)
                }
            )

    out_path = None
    if a.out or not a.sample:
        out_path = a.out or (re.sub(r"\.md$", "", label) + "_nuggets.json")
        open(out_path, "w", encoding="utf-8").write(
            json.dumps(nuggets, ensure_ascii=False, indent=2)
        )

    if a.output == "json":
        print(
            json.dumps(
                {
                    "mapping": label,
                    "out": out_path,
                    "nugget_count": len(nuggets),
                    "nuggets": nuggets,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(
            f"Nugget stubs: {len(nuggets)} → {out_path or '(sample, no --out given)'}"
        )
        print(
            "Next: verify_quotes fills in verified; the model fills in severity/valence/cluster."
        )


if __name__ == "__main__":
    main()
