#!/usr/bin/env python3
"""Deterministic gate for the readme-polish skill.

Stdlib only, no network, no LLM. The skill states mechanical rules (explicit
anchors, honest badges, mermaid size, table width, no placeholder assets).
This script makes the statically checkable ones enforceable. Rendering and
human fact-checking are still required -- see SKILL.md, step 4.

Rules
  R001  dead local link            relative link target does not exist
  R002  broken / placeholder badge image src is an HTML page, or a shields.io
                                    URL still carries OWNER/REPO placeholders
  R003  placeholder asset          image alt/path advertises a placeholder
  R004  non-ASCII anchor           #中文 / emoji link without an explicit <a id>
  R005  broken anchor              #target matches no explicit id / heading slug
  R006  mermaid too large          more node definitions than the configured max
  R007  wide table                 more columns than the configured max
  R008  badge overload             more shields.io badges than the configured max
  R009  install below fold         no install command in the first N lines (warn)

Exit codes: 0 = clean, 1 = warnings only, 2 = errors (or warnings under
--strict), 3 = a file is missing or unreadable. Bad flags exit 2 via argparse,
with a usage message on stderr and no findings. --json for CI consumption.

Examples
  python scripts/check_readme.py README.md
  python scripts/check_readme.py --strict --json README.md README.zh-CN.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

try:  # keep output readable on Windows consoles
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SEVERITY = {"error": "ERROR", "warning": "WARN "}

LINK_RE = re.compile(
    r"(?<!!)\[[^\]]*\]\(\s*<?([^)>\s]+)>?(?:\s+[\"'][^\"']*[\"'])?\s*\)"
)
IMG_RE = re.compile(
    r"!\[([^\]]*)\]\(\s*<?([^)>\s]+)>?(?:\s+[\"'][^\"']*[\"'])?\s*\)"
)
HTML_IMG_RE = re.compile(r"<img\b[^>]*?\bsrc\s*=\s*[\"']([^\"']+)[\"']", re.I)
EXPLICIT_ID_RE = re.compile(r"<a\s+(?:id|name)\s*=\s*[\"']([^\"']+)[\"']", re.I)
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})\s*(.*)$")
NODE_DEF_RE = re.compile(
    r"(?:^|[\s>\-])([A-Za-z_][A-Za-z0-9_]*)\s*[\[\{\(]"
)
INSTALL_RE = re.compile(
    r"\b(npx|npm\s+(?:i|install)|pnpm\s+add|yarn\s+add|pip\s+install|"
    r"uv\s+(?:run|pip|tool)|git\s+clone|cargo\s+install|go\s+install|"
    r"composer\s+require|brew\s+install)\b",
    re.I,
)
PLACEHOLDER_RE = re.compile(
    r"(\b(?:placeholder|todo|tbd|coming\s+soon)\b|待补|占位|示例截图|假图)", re.I
)
INLINE_CODE_RE = re.compile(r"`+[^`]*`+")
GITHUB_PAGE_IMG_RE = re.compile(r"github\.com/[^)\s\"']+/(?:blob|tree)/", re.I)
IMAGE_EXT_RE = re.compile(r"\.(?:png|jpe?g|gif|webp|svg|avif|bmp)(?:\?|$)", re.I)
TABLE_SEP_RE = re.compile(r"^:?-{2,}:?$")


@dataclass
class Finding:
    file: str
    rule: str
    severity: str
    line: int
    message: str


@dataclass
class Config:
    max_mermaid_nodes: int = 7
    max_table_cols: int = 5
    max_badges: int = 6
    first_screen_lines: int = 40


def slugify(text: str) -> str:
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    # GitHub keeps a leading hyphen left by a stripped emoji: "🚀 Install" -> "-install".
    return re.sub(r"\s", "-", text)


def has_non_ascii(text: str) -> bool:
    return any(ord(ch) > 127 for ch in text)


def strip_inline_code(line: str) -> str:
    """Blank out `code spans` so quoted examples are not treated as components.

    Skill docs quote broken snippets on purpose (e.g. the WattWatch anchor and
    the clipbrain License badge). Those are evidence, not README defects.
    """
    return INLINE_CODE_RE.sub(lambda m: " " * len(m.group(0)), line)


def is_external(target: str) -> bool:
    return bool(re.match(r"^(?:https?://|mailto:|data:|//)", target, re.I))


def suspicious_image_url(url: str) -> str | None:
    """Return a reason string when an image src cannot render as an image."""
    if not is_external(url):
        return None  # local paths are covered by R001
    if "OWNER/REPO" in url or "YOUR_REPO" in url or "<owner>" in url.lower():
        return "shields.io URL still contains a placeholder owner/repo"
    if GITHUB_PAGE_IMG_RE.search(url):
        return "image src points at a GitHub blob/tree HTML page (broken image)"
    bare = url.split("?", 1)[0].rstrip("/")
    if "github.com" in url and not IMAGE_EXT_RE.search(bare) and not bare.endswith("/badge"):
        return "image src points at a GitHub HTML page, not an image file"
    if url.lower().endswith(".html") or url.lower().endswith(".htm"):
        return "image src points at an HTML page"
    return None


def scan_file(path: Path, cfg: Config) -> list[Finding]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise RuntimeError(f"{path}: {exc}") from exc

    lines = text.splitlines()
    findings: list[Finding] = []
    name = str(path)

    def add(rule: str, severity: str, line: int, message: str) -> None:
        findings.append(Finding(name, rule, severity, line, message))

    # Pass 1: mark fenced code, collect mermaid blocks and heading slugs / ids.
    code_lines: set[int] = set()
    mermaid_blocks: list[tuple[int, list[str]]] = []
    fence_char: str | None = None
    fence_is_mermaid = False
    mermaid_start = 0
    mermaid_lines: list[str] = []
    explicit_ids: set[str] = set()
    heading_slugs: set[str] = set()
    slug_counts: dict[str, int] = {}

    for lineno, line in enumerate(lines, 1):
        match = FENCE_RE.match(line)
        if match:
            marker, info = match.group(1), match.group(2).strip()
            if fence_char is None:
                fence_char = marker[0]
                fence_is_mermaid = info.lower().startswith("mermaid")
                mermaid_start = lineno
                mermaid_lines = []
            elif marker[0] == fence_char:
                if fence_is_mermaid:
                    mermaid_blocks.append((mermaid_start, mermaid_lines))
                fence_char = None
                fence_is_mermaid = False
            code_lines.add(lineno)
            continue
        if fence_char is not None:
            code_lines.add(lineno)
            if fence_is_mermaid:
                mermaid_lines.append(line)
            continue

        for found in EXPLICIT_ID_RE.findall(line):
            explicit_ids.add(found)
        heading = HEADING_RE.match(line)
        if heading:
            # GitHub suffixes repeated slugs: usage, usage-1, usage-2 ...
            base = slugify(heading.group(1))
            seen = slug_counts.get(base, 0)
            slug_counts[base] = seen + 1
            heading_slugs.add(base if seen == 0 else f"{base}-{seen}")

    # Pass 2: line-level checks outside fenced code.
    badge_count = sum(
        len(re.findall(r"img\.shields\.io", strip_inline_code(line), re.I))
        for lineno, line in enumerate(lines, 1)
        if lineno not in code_lines
    )
    seen_images: set[tuple[int, str]] = set()
    # Install commands usually live inside fenced code, so scan raw lines.
    install_visible = any(
        INSTALL_RE.search(line) for line in lines[: cfg.first_screen_lines]
    )
    in_wide_table = False

    for lineno, line in enumerate(lines, 1):
        if lineno in code_lines:
            continue
        scan_line = strip_inline_code(line)

        for alt, url in IMG_RE.findall(scan_line):
            if (lineno, url) in seen_images:
                continue
            seen_images.add((lineno, url))
            _check_image(add, lineno, alt, url, path)
        for url in HTML_IMG_RE.findall(scan_line):
            if (lineno, url) in seen_images:
                continue
            seen_images.add((lineno, url))
            _check_image(add, lineno, "", url, path)

        for target in LINK_RE.findall(scan_line):
            _check_link(add, lineno, target, path, explicit_ids, heading_slugs)

        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = re.split(r"(?<!\\)\|", stripped[1:-1])
            if cells and all(TABLE_SEP_RE.match(c.strip()) for c in cells):
                continue  # separator row, keep the current table state
            if len(cells) > cfg.max_table_cols:
                if not in_wide_table:  # one finding per table, not per row
                    add(
                        "R007",
                        "warning",
                        lineno,
                        f"table has {len(cells)} columns (max {cfg.max_table_cols}); "
                        "it breaks on narrow screens, split it or use a list",
                    )
                in_wide_table = True
            else:
                in_wide_table = False
        else:
            in_wide_table = False

    for start, block_lines in mermaid_blocks:
        nodes: set[str] = set()
        for block_line in block_lines:
            nodes.update(NODE_DEF_RE.findall(block_line))
        if len(nodes) > cfg.max_mermaid_nodes:
            add(
                "R006",
                "warning",
                start,
                f"mermaid block defines {len(nodes)} nodes "
                f"(max {cfg.max_mermaid_nodes}); draw a flow, not an architecture map",
            )

    # Badge count and the 15-second install test only apply to README files,
    # not to this skill's own docs (which quote component examples).
    is_readme = path.name.lower().startswith("readme")

    if is_readme and badge_count > cfg.max_badges:
        add(
            "R008",
            "warning",
            0,
            f"{badge_count} shields.io badges found (max {cfg.max_badges}); "
            "each badge must earn its place",
        )

    if is_readme and not install_visible:
        add(
            "R009",
            "warning",
            0,
            f"no install command found in the first {cfg.first_screen_lines} lines; "
            "the 15-second test needs a working install path above the fold",
        )

    return findings


def _check_image(add, lineno: int, alt: str, url: str, readme: Path) -> None:
    filename = url.split("?", 1)[0].split("#", 1)[0].rstrip("/").rsplit("/", 1)[-1]
    if PLACEHOLDER_RE.search(alt) or PLACEHOLDER_RE.search(filename):
        add(
            "R003",
            "error",
            lineno,
            f"placeholder asset '{alt or url}' -- honesty rule: never advertise "
            "an entity that does not exist",
        )
    reason = suspicious_image_url(url)
    if reason:
        add("R002", "error", lineno, f"{reason}: {url}")
    if not is_external(url) and not url.startswith("#"):
        local = url.split("#", 1)[0]
        if local and not (readme.parent / local).exists():
            add("R001", "error", lineno, f"image target does not exist: {local}")


def _check_link(
    add,
    lineno: int,
    target: str,
    readme: Path,
    explicit_ids: set[str],
    heading_slugs: set[str],
) -> None:
    if target.startswith("#"):
        anchor = target[1:]
        if not anchor:
            return
        if has_non_ascii(anchor) and anchor not in explicit_ids:
            add(
                "R004",
                "error",
                lineno,
                f"non-ASCII anchor #{anchor} has no explicit <a id=\"...\">; "
                "GitHub auto-anchors for CJK/emoji headings are unreliable",
            )
            return
        if anchor not in explicit_ids and anchor.lower() not in heading_slugs:
            add(
                "R005",
                "error",
                lineno,
                f"anchor #{anchor} matches neither an explicit <a id> nor a heading slug",
            )
        return

    if is_external(target):
        return
    local = target.split("#", 1)[0]
    if local and not (readme.parent / local).exists():
        add("R001", "error", lineno, f"local link target does not exist: {local}")


def emit(findings: list[Finding], as_json: bool) -> None:
    errors = sum(f.severity == "error" for f in findings)
    warnings = sum(f.severity == "warning" for f in findings)
    if as_json:
        print(
            json.dumps(
                {
                    "errors": errors,
                    "warnings": warnings,
                    "findings": [asdict(f) for f in findings],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return
    files = sorted({f.file for f in findings})
    for name in files:
        print(f"readme-polish gate · {name}")
        for f in [x for x in findings if x.file == name]:
            where = f"L{f.line}" if f.line else "file"
            print(f"  {SEVERITY[f.severity]} {f.rule} {where:>6}  {f.message}")
    if not findings:
        print("readme-polish gate · clean (no findings)")
    print(f"summary: {errors} error(s), {warnings} warning(s)")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Deterministic README gate for the readme-polish skill."
    )
    parser.add_argument("files", nargs="*", type=Path, help="README files to check")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument(
        "--sample",
        action="store_true",
        help="run the embedded sample README (CI JSON-output gate)",
    )
    parser.add_argument(
        "--strict", action="store_true", help="treat warnings as errors (exit 2)"
    )
    parser.add_argument("--max-mermaid-nodes", type=int, default=7)
    parser.add_argument("--max-table-cols", type=int, default=5)
    parser.add_argument("--max-badges", type=int, default=6)
    parser.add_argument("--first-screen-lines", type=int, default=40)
    args = parser.parse_args(list(argv) if argv is not None else None)

    cfg = Config(
        max_mermaid_nodes=args.max_mermaid_nodes,
        max_table_cols=args.max_table_cols,
        max_badges=args.max_badges,
        first_screen_lines=args.first_screen_lines,
    )
    files = list(args.files)
    sample_dir: tempfile.TemporaryDirectory[str] | None = None
    if args.sample:
        sample_dir = tempfile.TemporaryDirectory()
        sample = Path(sample_dir.name) / "README.md"
        sample.write_text(
            "# Sample Project\n\n"
            "![License](https://img.shields.io/badge/license-MIT-blue)\n\n"
            "## Install\n\n"
            "```bash\npip install sample-project\n```\n",
            encoding="utf-8",
        )
        files.append(sample)
    if not files:
        parser.error("provide at least one README file, or --sample")

    findings: list[Finding] = []
    for path in files:
        if not path.is_file():
            print(f"error: not a file: {path}", file=sys.stderr)
            return 3
        try:
            findings.extend(scan_file(path, cfg))
        except RuntimeError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 3

    if sample_dir is not None:
        sample_dir.cleanup()

    emit(findings, args.json)
    errors = sum(f.severity == "error" for f in findings)
    warnings = sum(f.severity == "warning" for f in findings)
    # 0 = clean, 1 = warnings, 2 = errors (or warnings in --strict mode).
    if errors or (args.strict and warnings):
        return 2
    if warnings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
