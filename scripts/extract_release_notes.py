#!/usr/bin/env python3
"""Extract release notes for a specific version (or the latest) from CHANGELOG.md.

CHANGELOG.md must follow the Keep-a-Changelog header format:
    ## [X.Y.Z] - YYYY-MM-DD - optional subtitle

Outputs JSON by default:
    {"version": "2.8.0", "date": "2026-05-19", "subtitle": "...", "body": "..."}

Or use --format=plain to print just the body, or --format=github-release to
print a release body suitable for `gh release create --notes-file -`.

Examples:
    python3 scripts/extract_release_notes.py
    python3 scripts/extract_release_notes.py --version 2.7.3
    python3 scripts/extract_release_notes.py --format plain
    python3 scripts/extract_release_notes.py --format github-release
"""
import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHANGELOG = REPO / "CHANGELOG.md"

# Matches: ## [2.8.0] - 2026-05-19 - optional subtitle text
# Subtitle separator can be "-", "—", or absent.
HEADER = re.compile(
    r"^##\s+\[(?P<version>\d+\.\d+\.\d+(?:-[\w.]+)?)\]\s*-\s*"
    r"(?P<date>\d{4}-\d{2}-\d{2})"
    r"(?:\s*[-—]\s*(?P<subtitle>.+))?\s*$"
)


def parse_changelog(text):
    """Return list of {version, date, subtitle, body} dicts in file order."""
    lines = text.splitlines()
    entries = []
    current = None
    body_lines = []
    for line in lines:
        m = HEADER.match(line)
        if m:
            if current:
                current["body"] = "\n".join(body_lines).strip()
                entries.append(current)
            current = {
                "version": m.group("version"),
                "date": m.group("date"),
                "subtitle": (m.group("subtitle") or "").strip(),
            }
            body_lines = []
        elif current is not None:
            body_lines.append(line)
    if current:
        current["body"] = "\n".join(body_lines).strip()
        entries.append(current)
    return entries


def select_entry(entries, version):
    if version is None:
        if not entries:
            return None
        return entries[0]
    for e in entries:
        if e["version"] == version:
            return e
    return None


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--version", help="Specific version to extract (default: latest)")
    ap.add_argument("--changelog", default=str(CHANGELOG), help="Path to CHANGELOG.md")
    ap.add_argument(
        "--format",
        choices=["json", "plain", "github-release"],
        default="json",
        help="Output format (default: json)",
    )
    args = ap.parse_args()

    path = Path(args.changelog)
    if not path.exists():
        print(f"CHANGELOG not found: {path}", file=sys.stderr)
        return 2

    entries = parse_changelog(path.read_text())
    entry = select_entry(entries, args.version)
    if not entry:
        if args.version:
            print(f"Version {args.version} not found in {path}", file=sys.stderr)
        else:
            print(f"No version entries found in {path}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(entry, indent=2))
    elif args.format == "plain":
        print(entry["body"])
    elif args.format == "github-release":
        title_line = f"# {entry['version']} — {entry['subtitle']}" if entry["subtitle"] else f"# {entry['version']}"
        print(title_line)
        print(f"_Released {entry['date']}_")
        print()
        print(entry["body"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
