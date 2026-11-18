#!/usr/bin/env python3
"""Extract cited links and their paragraph context from a Markdown draft.

Usage:
    python3 extract_claims.py draft.md
    python3 extract_claims.py draft.md --json -o claims.json
    python3 extract_claims.py --sample --json
    python3 extract_claims.py --selftest

Exit codes: 0 extracted links, 1 no links found, 2 input error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BARE_URL = re.compile(r"https?://[^\s)\]}，。；]+")
SAMPLE = """# Sample roundup

Orca is a desktop agent fleet manager, licensed MIT ([repo](https://github.com/stablyai/orca)).

It supports Windows and macOS, per the README: https://example.com/orca/readme
"""


def find_md_links(paragraph: str) -> list[tuple[str, str, int, int]]:
    """Return (text, url, start, end) for [text](url) links, pairing brackets."""
    found: list[tuple[str, str, int, int]] = []
    cursor = 0
    while True:
        start = paragraph.find("[", cursor)
        if start < 0:
            break
        middle = paragraph.find("](", start + 1)
        if middle < 0:
            break
        end = paragraph.find(")", middle + 2)
        if end < 0:
            break
        url = paragraph[middle + 2 : end]
        if url.startswith("http"):
            found.append((paragraph[start + 1 : middle], url, middle + 2, end))
        cursor = end + 1
    return found


def extract(text: str) -> list[dict[str, str]]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    items: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    def add(url: str, link_text: str, paragraph: str) -> None:
        key = (url, paragraph[:40])
        if key in seen:
            return
        seen.add(key)
        items.append({"url": url, "link_text": link_text, "context": paragraph})

    for paragraph in paragraphs:
        markdown_links = find_md_links(paragraph)
        spans = [(start, end) for _, _, start, end in markdown_links]
        for link_text, url, _, _ in markdown_links:
            add(url, link_text, paragraph)
        for match in BARE_URL.finditer(paragraph):
            if any(start <= match.start() < end for start, end in spans):
                continue
            add(match.group(0).rstrip(".,;、。"), "", paragraph)
    return items


def run(path: Path, as_json: bool, output: Path | None) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"error: cannot read {path}: {exc}", file=sys.stderr)
        return 2

    items = extract(text)
    payload = {"draft": str(path), "link_count": len(items), "links": items}
    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    if output is not None:
        output.write_text(rendered + "\n", encoding="utf-8")
    if as_json:
        print(rendered)
    else:
        for item in items:
            print(f"{item['url']}\t{item['link_text']}")
        print(f"links: {len(items)}")
    return 0 if items else 1


def selftest() -> int:
    text = (
        "A [repo](https://github.com/o/r) link and a bare https://example.com/x link.\n\n"
        "Same [repo](https://github.com/o/r) again in another paragraph."
    )
    items = extract(text)
    urls = [item["url"] for item in items]
    assert urls.count("https://github.com/o/r") == 2, urls
    assert "https://example.com/x" in urls, urls
    print(f"selftest ok: {len(items)} links")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract cited links and paragraph context from Markdown.")
    parser.add_argument("draft", nargs="?", type=Path, help="Markdown file to scan")
    parser.add_argument("--json", action="store_true", help="print the JSON payload")
    parser.add_argument("-o", "--output", type=Path, help="write the JSON payload to this file")
    parser.add_argument("--sample", action="store_true", help="run the embedded sample draft")
    parser.add_argument("--selftest", action="store_true", help="run the extractor self-test")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()
    if args.sample:
        items = extract(SAMPLE)
        payload = {"draft": "<sample>", "link_count": len(items), "links": items}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    if args.draft is None:
        parser.error("provide a Markdown draft, or use --sample / --selftest")
    return run(args.draft, args.json, args.output)


if __name__ == "__main__":
    raise SystemExit(main())
