#!/usr/bin/env python3
"""check_command_refs.py — reject slash-command references that Claude Code cannot run.

Claude Code names a plugin command `/<plugin>:<name>` and also accepts the bare
`/<name>` when nothing else claims it. This repo's commands are named `cs-<name>`,
so they run as `/cs-<name>`. The old `/cs-<name>` spelling looks like a namespace
but matches nothing, so a user who copies it from our docs gets "unknown command".

Scans the canonical tree (mirrors, CHANGELOG.md and the audit/ record excluded,
since those preserve history) and fails on any `/cs-<name>` reference or any `/<prefix>:<name>` whose prefix
is not a plugin.json name.

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
    ".git", ".codex", ".gemini", ".hermes", ".vibe", ".claude", "audit", "node_modules",
    "documentation", "megaprompts", "eval-workspace", "site",
}
EXCLUDED_FILES = {"CHANGELOG.md", "check_command_refs.py"}
EXTENSIONS = (".md", ".json", ".py", ".sh", ".yml", ".yaml", ".txt")
STALE = re.compile(r"/cs:[a-z0-9*<{][a-z0-9-}>]*")
# Any other `/<prefix>:<name>` must use a real plugin namespace, which Claude Code
# takes from plugin.json `name`. Docs once used shorthand prefixes (`/ar:`,
# `/hub:`, `/em:`, `/docker:`) that never existed. `</ns:tag>` XML and URLs are
# skipped by the lookbehind; placeholder namespaces are allowed.
NAMESPACED = re.compile(r"(?<![\w./:<-])/([a-z][a-z0-9-]*):([a-z0-9*<{][a-z0-9-}>*]*)")
PLACEHOLDER_NAMESPACES = {"my-plugin", "plugin"}


def plugin_namespaces(root):
    names = set()
    for dirpath, dirnames, filenames in os.walk(root):
        if dirpath == root:
            dirnames[:] = [d for d in dirnames if d not in EXCLUDED_TOP_LEVEL]
        if os.path.basename(dirpath) == ".claude-plugin" and "plugin.json" in filenames:
            try:
                with open(os.path.join(dirpath, "plugin.json"), encoding="utf-8") as fh:
                    names.add(json.load(fh)["name"])
            except (OSError, ValueError, KeyError):
                continue
    return names


def scan(root):
    findings = []
    known = plugin_namespaces(root) | PLACEHOLDER_NAMESPACES
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
                        for m in NAMESPACED.finditer(line):
                            if m.group(1) != "cs" and m.group(1) not in known and not line[m.end():].startswith("://"):
                                findings.append((os.path.relpath(path, root), lineno, m.group(0)))
            except (OSError, UnicodeDecodeError):
                continue
    return findings


def main():
    ap = argparse.ArgumentParser(description="Fail on /cs-<name> command references, which Claude Code cannot run.")
    ap.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable output")
    ap.add_argument("--root", default=REPO_ROOT, help="Repo root (default: parent of this script)")
    args = ap.parse_args()

    findings = scan(os.path.abspath(args.root))
    if args.json:
        print(json.dumps([{"file": f, "line": n, "ref": r} for f, n, r in findings], indent=2))
    else:
        for f, n, r in findings:
            if r.startswith("/cs:"):
                print(f"{f}:{n}: {r}  ->  use /cs-{r[4:]} (or /<plugin>:{r[4:]} for a skill)")
            else:
                print(f"{f}:{n}: {r}  ->  no plugin is named {r[1:].split(':')[0]!r}; use /<plugin.json name>:<skill> or the bare /<skill>")
        print(f"\n{len(findings)} command reference(s) with no matching plugin namespace.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
