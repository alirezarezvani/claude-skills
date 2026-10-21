#!/usr/bin/env python3
"""
compare_to_gold.py — scaffolding for human-in-the-loop comparison "AI mapping vs gold.md".

NOT an automatic scorer. The script does not assign scores or judge divergences — it
prepares a blank where a human, BLIND, fills in the coverage score (1-5) and the
divergence code ([F]/[O]/[I]/[R], see references/rubric.md), comparing the wordings
without knowing in advance which source is which.

Parsing gold.md — by cell headers `### <code> — <title>` and blocks `Quote: ... (line N)`
inside each cell. The format is read "as is": gold.md stays plain markdown, it is not
rewritten into a separate JSON format.

The AI mapping is supplied the same way: a markdown file with the same cell headers
`### <code> — <title>`, obtained by an actual run of the skill's pipeline (S1→S4) on the
same transcript.txt the skill uses. This script does not call an LLM.

CLI:
  python compare_to_gold.py --gold gold.md --ai ai_mapping.md [--lens templates/candidate.md] [--out review.md]
"""

import argparse
import json
import re
import sys

CELL_HEADER_RE = re.compile(
    r"^###\s+(?P<code>\S+)\s+—\s+(?P<title>.+?)\s*$", re.MULTILINE
)
SECTION_HEADER_RE = re.compile(r"^##\s+(?!#).+$", re.MULTILINE)

SAMPLE_GOLD_MD = (
    "### K1 — Job to be done\n"
    "Needs to reconcile the monthly budget without losing trust in the export.\n\n"
    "### A1 — Friction\n"
    "The export didn't match what was on screen, so trust broke.\n"
)
SAMPLE_AI_MD = (
    "### K1 — Job to be done\n"
    "Wants to reconcile the budget quickly.\n\n"
    "### A1 — Friction\n"
    "The export was slow.\n"
)


def _read_text(path):
    """Reads a text file or exits with a clear error."""
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError as e:
        sys.exit(f"error: {path}: {e.strerror or e}")
    except UnicodeDecodeError as e:
        sys.exit(f"error: {path}: not UTF-8 ({e.reason})")


def parse_cells(text):
    """Splits a markdown mapping into cells by headers `### <code> — <title>`.

    Returns a list of (code, title, body) in the order they appear in the text.
    body is the raw text of the cell between its header and the next `###` (or the
    end of the file / the next `##` section).
    """
    headers = list(CELL_HEADER_RE.finditer(text))
    sections = [m.start() for m in SECTION_HEADER_RE.finditer(text)]
    cells = []
    for i, m in enumerate(headers):
        start = m.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        next_section = next((s for s in sections if s > start and s < end), None)
        if next_section is not None:
            end = next_section
        body = text[start:end].strip("\n")
        cells.append((m.group("code"), m.group("title").strip(), body))
    return cells


def lens_cell_order(lens_text):
    """Extracts cell order and titles from the lens template (templates/<lens>.md), if given.

    Template lines of the form `- **K1 Title** — description`. Used only for sorting /
    checking completeness of the cell set — not required to build the blank.
    """
    order = []
    for m in re.finditer(
        r"^\s*-\s+\*\*(?P<code>\S+)\s+(?P<title>[^*]+?)\*\*", lens_text, re.MULTILINE
    ):
        order.append((m.group("code"), m.group("title").strip()))
    return order


def render_review(gold_cells, ai_cells, lens_order=None):
    """Builds a markdown blank: for each cell, the gold version and the AI version side by side + empty fields for a human."""
    ai_by_code = {code: (title, body) for code, title, body in ai_cells}
    gold_codes = [code for code, _, _ in gold_cells]

    order = gold_codes
    if lens_order:
        lens_codes = [code for code, _ in lens_order]
        order = [c for c in lens_codes if c in gold_codes] + [
            c for c in gold_codes if c not in lens_codes
        ]

    gold_by_code = {code: (title, body) for code, title, body in gold_cells}

    lines = ["# Human↔AI review blank", ""]
    missing_in_ai = [c for c in order if c not in ai_by_code]
    if missing_in_ai:
        lines.append(
            f"**Warning:** missing from the AI mapping: {', '.join(missing_in_ai)}"
        )
        lines.append("")

    for code in order:
        gold_title, gold_body = gold_by_code[code]
        lines.append(f"## {code} — {gold_title}")
        lines.append("")
        lines.append("### Gold")
        lines.append(gold_body if gold_body else "_(empty)_")
        lines.append("")
        lines.append("### AI")
        if code in ai_by_code:
            _, ai_body = ai_by_code[code]
            lines.append(ai_body if ai_body else "_(empty)_")
        else:
            lines.append("_(cell missing from the AI mapping)_")
        lines.append("")
        lines.append("Coverage score (1-5): ___")
        lines.append("Divergence code (if any): ___")
        lines.append("")
        lines.append("---")
        lines.append("")

    extra_in_ai = [code for code, _, _ in ai_cells if code not in gold_by_code]
    if extra_in_ai:
        lines.append(f"**In AI, not in gold:** {', '.join(extra_in_ai)}")
        lines.append("")

    return "\n".join(lines)


def main():
    """CLI: builds a human↔AI review blank from gold.md and an AI mapping of the same lens."""
    ap = argparse.ArgumentParser(
        description="Build a human vs. AI review blank from gold.md and an AI mapping."
    )
    ap.add_argument(
        "--transcript",
        help="fixture's transcript.txt (for reference in the blank's header)",
    )
    ap.add_argument(
        "--gold",
        default=None,
        help="fixture's gold.md; required unless --sample is given",
    )
    ap.add_argument(
        "--ai",
        default=None,
        help="AI mapping, same cell headers; required unless --sample is given",
    )
    ap.add_argument("--lens", help="templates/<lens>.md — optional, for cell order")
    ap.add_argument("--out", default=None)
    ap.add_argument(
        "--sample",
        action="store_true",
        help="Run on a built-in sample gold.md + AI mapping",
    )
    ap.add_argument(
        "--output", choices=["human", "json"], default="human", help="Output format"
    )
    a = ap.parse_args()

    if a.sample:
        gold_text, ai_text = SAMPLE_GOLD_MD, SAMPLE_AI_MD
    else:
        if not a.gold or not a.ai:
            sys.exit("error: --gold and --ai are required unless --sample is given")
        gold_text = _read_text(a.gold)
        ai_text = _read_text(a.ai)
    lens_order = lens_cell_order(_read_text(a.lens)) if a.lens else None

    gold_cells = parse_cells(gold_text)
    ai_cells = parse_cells(ai_text)
    if not gold_cells:
        sys.exit("error: gold: no cell headers found (`### <code> — <title>`)")

    out = render_review(gold_cells, ai_cells, lens_order)
    if a.transcript:
        out = f"**Transcript:** {a.transcript}\n\n" + out

    out_path = a.out
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(out)

    if a.output == "json":
        ai_codes = {code for code, _, _ in ai_cells}
        gold_codes = [code for code, _, _ in gold_cells]
        print(
            json.dumps(
                {
                    "out": out_path,
                    "gold_cells": len(gold_cells),
                    "ai_cells": len(ai_cells),
                    "missing_in_ai": [c for c in gold_codes if c not in ai_codes],
                    "extra_in_ai": [c for c, _, _ in ai_cells if c not in gold_codes],
                    "blank_md": out if not out_path else None,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    elif out_path:
        print(f"Review blank: {len(gold_cells)} cells → {out_path}")
    else:
        print(out)


if __name__ == "__main__":
    main()
