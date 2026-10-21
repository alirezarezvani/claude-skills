#!/usr/bin/env python3
"""
extract_claims.py — pull quotes from a finished mapping (.md) into claims.json.

Removes manual gluing: parses our mapping format and collects a list of quotes for verify_quotes.py.
Recognizes:
  - cell headers: **К5 | Системы...**, **А1 | eNPS...**, ### СЛОЙ ...
  - quotes in guillemets: «...» (on any lines, most often in _italic_ «Цитата: «...»» or _«...» (L61)_)
  - optional line number in the quote: (L61) / (61)

The line number is NOT required — verify_quotes finds it itself (see --emit-enriched).

CLI: python extract_claims.py mapping.md [--interview "Daria"] [--role "operations"] [--out claims.json]
        [--output {human,json}]
     python extract_claims.py --sample
"""

import argparse
import json
import re
import sys
from collections import Counter

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
    """CLI: parses an .md mapping and extracts a list of quotes into claims.json."""
    ap = argparse.ArgumentParser(
        description="Extract quotes from a finished mapping into claims.json."
    )
    ap.add_argument("mapping", nargs="?", help="Path to the finished mapping (.md)")
    ap.add_argument("--interview", default=None)
    ap.add_argument("--role", default=None)
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
    else:
        if not a.mapping:
            sys.exit("error: mapping is required unless --sample is given")
        text, label = _read_text(a.mapping), a.mapping
    lines = text.splitlines()
    cur_cell, cur_title, cur_claimtext = None, None, ""
    claims = []
    for ln in lines:
        mcell = CELL_RE.search(ln)
        if mcell:
            cur_cell = mcell.group(1).strip()
            cur_title = mcell.group(2).strip()
            cur_claimtext = ""
            continue
        # accumulate the cell text as a «claim» (without quote lines)
        if (
            cur_cell
            and "«" not in ln
            and ln.strip()
            and not ln.startswith(("#", "---", "**", "_Цитата"))
        ):
            if len(cur_claimtext) < 160:
                cur_claimtext = (cur_claimtext + " " + ln.strip()).strip()
        for mq in QUOTE_RE.finditer(ln):
            quote = mq.group(1).strip()
            mline = LINE_RE.search(ln)
            claim = {
                "cell": cur_cell or "?",
                "title": cur_title or "",
                "claim": cur_claimtext[:160],
                "quote": quote,
            }
            if mline:
                claim["line"] = int(mline.group(1))
            if a.interview:
                claim["interview"] = a.interview
            if a.role:
                claim["role"] = a.role
            claims.append(claim)

    out_path = None
    if a.out or not a.sample:
        out_path = a.out or (re.sub(r"\.md$", "", label) + "_claims.json")
        open(out_path, "w", encoding="utf-8").write(
            json.dumps(claims, ensure_ascii=False, indent=2)
        )
    c = Counter(x["cell"] for x in claims)

    if a.output == "json":
        print(
            json.dumps(
                {
                    "mapping": label,
                    "out": out_path,
                    "claim_count": len(claims),
                    "by_cell": dict(c),
                    "claims": claims,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(
            f"Quotes extracted: {len(claims)} from {label} → {out_path or '(sample, no --out given)'}"
        )
        print("by cell:", dict(c))


if __name__ == "__main__":
    main()
