#!/usr/bin/env python3
"""check_command_refs.py — reject slash-command references that Claude Code cannot run.

Claude Code names a plugin command `/<plugin>:<name>` and also accepts the bare
`/<name>` when nothing else claims it. This repo's commands are named `cs-<name>`,
so they run as `/cs-<name>`. The old `/cs:<name>` spelling looks like a namespace
but matches nothing, so a user who copies it from our docs gets "unknown command".

Scans the canonical tree (mirrors, CHANGELOG.md and the audit/ record excluded,
since those preserve history) and fails on any `/cs:<name>` reference.

Exit codes: 0 = clean, 1 = stale references found.

Usage:
  python3 scripts/check_command_refs.py
  python3 scripts/check_command_refs.py --json
"""

import argparse
import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDED_TOP_LEVEL = {
    ".git", ".codex", ".gemini", ".hermes", ".vibe", "audit", "node_modules",
    "documentation", "megaprompts", "eval-workspace", "site",
}
EXCLUDED_FILES = {"CHANGELOG.md", "check_command_refs.py"}
EXTENSIONS = (".md", ".json", ".py", ".sh", ".yml", ".yaml", ".txt")
STALE = re.compile(r"/cs:[a-z0-9][a-z0-9-]*")


def scan(root):
    findings = []
    for dirpath, dirnames, filenames in os.walk(root):
        if dirpath == root:
            dirnames[:] = [d for d in dirnames if d not in EXCLUDED_TOP_LEVEL]
        for fn in filenames:
            if fn in EXCLUDED_FILES or not fn.endswith(EXTENSIONS):
                continue
            path = os.path.join(dirpath, fn)
            if os.path.islink(path):
                continue
            try:
                with open(path, encoding="utf-8") as fh:
                    for lineno, line in enumerate(fh, 1):
                        for m in STALE.finditer(line):
                            findings.append((os.path.relpath(path, root), lineno, m.group(0)))
            except (OSError, UnicodeDecodeError):
                continue
    return findings


def main():
    ap = argparse.ArgumentParser(description="Fail on /cs:<name> command references, which Claude Code cannot run.")
    ap.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable output")
    ap.add_argument("--root", default=REPO_ROOT, help="Repo root (default: parent of this script)")
    args = ap.parse_args()

    findings = scan(os.path.abspath(args.root))
    if args.json:
        print(json.dumps([{"file": f, "line": n, "ref": r} for f, n, r in findings], indent=2))
    else:
        for f, n, r in findings:
            print(f"{f}:{n}: {r}  ->  use /cs-{r[4:]} (or /<plugin>:{r[4:]} for a skill)")
        print(f"\n{len(findings)} stale /cs: reference(s).")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
