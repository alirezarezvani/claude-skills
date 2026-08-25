#!/usr/bin/env python3
"""
number_lines.py — number a transcript line by line for quote traceability.

Every quote in a mapping must reference a line number; verify_quotes.py then
checks the match. LLMs handle line numbers poorly «in their head» — so we number by script.

Supports .txt and .docx (stdlib parsing, no external dependencies).

CLI:  python number_lines.py input.txt [--out output.txt] [--output {human,json}]
      python number_lines.py --sample
Output: lines of the form 'L1: ...', 'L2: ...'
"""

import argparse
import json
import sys
import os
import zipfile
from xml.etree import ElementTree as ET

_W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

SAMPLE_TEXT = (
    "Interviewer: Tell me about the last time you tried to reconcile the budget.\n"
    "Respondent: Honestly, I opened three tabs and gave up after twenty minutes.\n"
    "Interviewer: What made you give up?\n"
    "Respondent: The export didn't match what I saw on screen, so I stopped trusting it.\n"
)


def read_docx(path):
    """Reads .docx text via stdlib (zipfile + XML): paragraphs from word/document.xml, text from <w:t>."""
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)
    paragraphs = []
    for p in root.iter(f"{_W_NS}p"):
        text = "".join(t.text or "" for t in p.iter(f"{_W_NS}t"))
        paragraphs.append(text)
    return "\n".join(paragraphs)


def read_text(path):
    """Reads .txt or .docx (stdlib parsing); errors → a clear message, exit 1."""
    if path.lower().endswith(".docx"):
        try:
            return read_docx(path)
        except (zipfile.BadZipFile, KeyError, ET.ParseError) as e:
            sys.exit(f"error: {path}: failed to read .docx ({e})")
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError as e:
        sys.exit(f"error: {path}: {e.strerror or e}")
    except UnicodeDecodeError as e:
        sys.exit(f"error: {path}: not UTF-8 ({e.reason})")


def main():
    """CLI: numbers the transcript's lines and writes the result to *_nl.txt."""
    ap = argparse.ArgumentParser(
        description="Number a transcript's lines for quote traceability."
    )
    ap.add_argument("input", nargs="?", help="Transcript file (.txt or .docx)")
    ap.add_argument("--out", default=None)
    ap.add_argument(
        "--sample",
        action="store_true",
        help="Run on a built-in sample transcript, no input file needed",
    )
    ap.add_argument(
        "--output", choices=["human", "json"], default="human", help="Output format"
    )
    a = ap.parse_args()

    if a.sample:
        text, label = SAMPLE_TEXT, "<sample>"
    else:
        if not a.input:
            sys.exit("error: input is required unless --sample is given")
        text, label = read_text(a.input), a.input

    lines = text.splitlines()
    numbered = "\n".join(f"L{i}: {ln}" for i, ln in enumerate(lines, 1))

    out_path = None
    if a.out or not a.sample:
        out_path = a.out or (os.path.splitext(label)[0] + "_nl.txt")
        open(out_path, "w", encoding="utf-8").write(numbered)

    if a.output == "json":
        print(
            json.dumps(
                {
                    "input": label,
                    "out": out_path,
                    "line_count": len(lines),
                    "numbered_preview": numbered.splitlines()[:5],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        if out_path:
            print(f"Lines numbered: {len(lines)} → {out_path}")
        else:
            print(f"Lines numbered: {len(lines)} (sample, no --out given)")
            print(numbered)


if __name__ == "__main__":
    main()
