#!/usr/bin/env python3
"""
export_marp.py — Render a wiki page (or subtree) as a Marp slide deck.

Marp is a Markdown-based slide format supported by an Obsidian plugin. This
script adds Marp frontmatter and converts `## H2` headings into slide breaks,
so any wiki page with H2 sections becomes a usable slide deck with zero
manual formatting.

Usage:
    python export_marp.py --vault . --page wiki/synthesis/interpretability-overview.md
    python export_marp.py --vault . --page wiki/concepts/ --theme gaia --out slides/
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

MARP_HEADER = """---
marp: true
theme: {theme}
paginate: true
---

"""


def strip_frontmatter(text: str) -> str:
    return FRONTMATTER_RE.sub("", text, count=1)


def to_marp(text: str, theme: str) -> str:
    body = strip_frontmatter(text).strip()
    # Turn each "## " into a new slide separator.
    # First H1 → title slide. Subsequent H2 → slide breaks.
    lines = body.splitlines()
    out: list[str] = []
    seen_h1 = False
    for line in lines:
        if line.startswith("# ") and not seen_h1:
            out.append(line)
            out.append("")
            seen_h1 = True
            continue
        if line.startswith("## "):
            out.append("\n---\n")
            out.append(line)
            continue
        out.append(line)
    return MARP_HEADER.format(theme=theme) + "\n".join(out).strip() + "\n"


def render_one(src: Path, out_path: Path, theme: str) -> None:
    text = src.read_text(encoding="utf-8", errors="replace")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(to_marp(text, theme), encoding="utf-8")
    print(f"[ok] {src.name} -> {out_path}")


def main() -> None:
    p = argparse.ArgumentParser(description="Render a wiki page (or subtree) to Marp")
    p.add_argument("--vault", required=True)
    p.add_argument("--page", required=True, help="Page or directory (relative to vault)")
    p.add_argument("--theme", default="default", choices=["default", "gaia", "uncover"])
    p.add_argument("--out", default="slides", help="Output directory (relative to vault)")
    args = p.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    src = (vault / args.page).resolve()
    if not src.exists():
        print(f"[error] not found: {src}", file=sys.stderr)
        sys.exit(1)

    out_root = vault / args.out
    if src.is_file():
        render_one(src, out_root / src.name.replace(".md", ".marp.md"), args.theme)
    else:
        for md in sorted(src.rglob("*.md")):
            rel = md.relative_to(src)
            dest = out_root / rel.with_suffix(".marp.md")
            render_one(md, dest, args.theme)


if __name__ == "__main__":
    main()
