#!/usr/bin/env python3
"""open_loop_scanner.py — Inventory the open loops hiding in a directory.

The GET CLEAR phase of a weekly review starts with evidence, not memory. This script scans a
directory for three kinds of open loop:

  1. checkbox    — unchecked markdown checkboxes:  - [ ] / * [ ]
  2. todo_fixme  — TODO / FIXME markers in text and source files
  3. stale_file  — files not modified in --stale-days days (default 14)

Output is an inventory grouped by kind, with counts and per-file locations, so the review walks
real loops instead of whatever the user happens to remember.

Deterministic logic. No LLM calls, no network. Stdlib only.

Usage:
    python open_loop_scanner.py --dir ~/notes
    python open_loop_scanner.py --dir . --stale-days 30 --json
    python open_loop_scanner.py --sample

Exit codes:
    0  scan complete (even if zero loops found) — also --sample / --help
    2  directory not found or not a directory
"""

import argparse
import json
import os
import re
import sys
import time
from typing import Any, Dict, List

SKIP_DIRS = {".git", ".hg", ".svn", "node_modules", "__pycache__", ".venv", "venv",
             "dist", "build", ".idea", ".vscode", ".cache"}
CHECKBOX_EXTS = {".md", ".markdown", ".txt"}
TEXT_EXTS = CHECKBOX_EXTS | {".py", ".js", ".ts", ".tsx", ".jsx", ".sh", ".rb", ".go",
                             ".rs", ".java", ".c", ".h", ".cpp", ".css", ".html",
                             ".yaml", ".yml", ".toml", ".ini", ".cfg", ".sql"}

CHECKBOX_RE = re.compile(r"^\s*[-*]\s+\[ \]\s+(.*)$")
TODO_RE = re.compile(r"\b(TODO|FIXME)\b[:\s]*(.*)", re.IGNORECASE)


def _snippet(text: str, limit: int = 80) -> str:
    text = text.strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


def scan(directory: str, stale_days: int) -> Dict[str, Any]:
    now = time.time()
    stale_cutoff = now - stale_days * 86400
    checkboxes: List[Dict[str, Any]] = []
    todos: List[Dict[str, Any]] = []
    stale: List[Dict[str, Any]] = []
    files_scanned = 0

    for root, dirs, files in os.walk(directory):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
        for fname in sorted(files):
            ext = os.path.splitext(fname)[1].lower()
            if ext not in TEXT_EXTS:
                continue
            path = os.path.join(root, fname)
            rel = os.path.relpath(path, directory)
            files_scanned += 1

            try:
                mtime = os.path.getmtime(path)
                if mtime < stale_cutoff:
                    stale.append({"file": rel,
                                  "days_since_modified": int((now - mtime) // 86400)})
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    for lineno, line in enumerate(f, 1):
                        if ext in CHECKBOX_EXTS:
                            m = CHECKBOX_RE.match(line)
                            if m:
                                checkboxes.append({"file": rel, "line": lineno,
                                                   "text": _snippet(m.group(1))})
                        m = TODO_RE.search(line)
                        if m:
                            todos.append({"file": rel, "line": lineno,
                                          "marker": m.group(1).upper(),
                                          "text": _snippet(m.group(2))})
            except OSError:
                continue

    total = len(checkboxes) + len(todos) + len(stale)
    return {
        "directory": os.path.abspath(directory),
        "stale_days_threshold": stale_days,
        "files_scanned": files_scanned,
        "total_open_loops": total,
        "loops": {
            "checkbox": {"count": len(checkboxes), "items": checkboxes},
            "todo_fixme": {"count": len(todos), "items": todos},
            "stale_file": {"count": len(stale), "items": stale},
        },
    }


SAMPLE_RESULT: Dict[str, Any] = {
    "directory": "/home/sample/notes",
    "stale_days_threshold": 14,
    "files_scanned": 12,
    "total_open_loops": 7,
    "loops": {
        "checkbox": {
            "count": 3,
            "items": [
                {"file": "projects/website-relaunch.md", "line": 14,
                 "text": "email designer about the hero image"},
                {"file": "projects/website-relaunch.md", "line": 15,
                 "text": "draft the pricing page copy"},
                {"file": "inbox.md", "line": 3, "text": "book dentist appointment"},
            ],
        },
        "todo_fixme": {
            "count": 2,
            "items": [
                {"file": "scripts/backup.sh", "line": 22, "marker": "TODO",
                 "text": "rotate old archives after 90 days"},
                {"file": "notes/tax-prep.md", "line": 8, "marker": "FIXME",
                 "text": "the mileage total is wrong, recount Q2"},
            ],
        },
        "stale_file": {
            "count": 2,
            "items": [
                {"file": "projects/learn-spanish.md", "days_since_modified": 41},
                {"file": "someday/write-a-novel.md", "days_since_modified": 63},
            ],
        },
    },
}

KIND_LABEL = {
    "checkbox": "Unchecked checkboxes (- [ ])",
    "todo_fixme": "TODO / FIXME markers",
    "stale_file": "Stale files (untouched past threshold)",
}


def render_human(r: Dict[str, Any]) -> str:
    out = ["Open Loop Scanner (evidence first, memory second)", "=" * 64]
    out.append(f"  Directory:     {r['directory']}")
    out.append(f"  Files scanned: {r['files_scanned']}   "
               f"Stale threshold: {r['stale_days_threshold']} days")
    out.append(f"  TOTAL OPEN LOOPS: {r['total_open_loops']}")
    for kind in ("checkbox", "todo_fixme", "stale_file"):
        bucket = r["loops"][kind]
        out.append(f"\n  {KIND_LABEL[kind]} — {bucket['count']}")
        for item in bucket["items"][:25]:
            if kind == "stale_file":
                out.append(f"    - {item['file']}  ({item['days_since_modified']} days untouched)")
            elif kind == "todo_fixme":
                out.append(f"    - {item['file']}:{item['line']}  [{item['marker']}] {item['text']}")
            else:
                out.append(f"    - {item['file']}:{item['line']}  {item['text']}")
        if bucket["count"] > 25:
            out.append(f"    … and {bucket['count'] - 25} more")
    out.append("")
    out.append("  Feed these into GET CLEAR: collect, clarify, and route every loop")
    out.append("  to a list — next action, waiting-for, someday/maybe, or trash.")
    return "\n".join(out)


def main(argv: List[str]) -> int:
    p = argparse.ArgumentParser(
        description="Scan a directory for open loops: unchecked checkboxes, TODO/FIXME, stale files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--dir", default=".", help="Directory to scan (default: current directory)")
    p.add_argument("--stale-days", type=int, default=14,
                   help="Flag files not modified in this many days (default: 14)")
    p.add_argument("--sample", action="store_true",
                   help="Print a canned deterministic scan result and exit 0")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    args = p.parse_args(argv)

    if args.sample:
        result = SAMPLE_RESULT
    else:
        if not os.path.isdir(args.dir):
            print(f"error: not a directory: {args.dir}", file=sys.stderr)
            return 2
        result = scan(args.dir, args.stale_days)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render_human(result))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
