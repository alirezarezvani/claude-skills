#!/usr/bin/env python3
"""check_paths.py — phantom-path linter for skills, agents, and commands.

Scans SKILL.md files plus *.md files under any agents/ or commands/ directory
for path-like references (scripts/, references/, assets/, skills/, templates/
tokens, `python x.py` invocations, and ../ relative paths) and verifies each
candidate resolves against (a) the owning skill/plugin root, (b) the file's
own directory, or (c) the repo root. A candidate is OK if ANY base resolves.

Known dynamic patterns (containing { < $ ~ *) and URLs are skipped.

Exit codes: 0 = all paths resolve, 1 = at least one unresolvable path.
Intended as CI gate G1.

Usage:
  python3 scripts/check_paths.py --all            # scan canonical dirs repo-wide
  python3 scripts/check_paths.py FILE [FILE ...]  # scan specific files
  python3 scripts/check_paths.py --all --json     # machine-readable output
"""

import argparse
import fnmatch
import json
import os
import re
import sys

EXCLUDED_DIRS = {
    ".git", ".codex", ".gemini", ".hermes", ".vibe", "docs", "audit",
    "node_modules", ".github", ".claude", ".claude-plugin",
}

# Token-style paths anchored on a canonical content dir, with a known extension.
RE_MARKER_PATH = re.compile(
    r"[A-Za-z0-9_\-./]*\b(?:scripts|references|assets|skills|templates)/"
    r"[A-Za-z0-9_\-./]+\.(?:py|md|sh|json|yaml|yml)\b"
)
# Any multi-segment reference to a SKILL.md file.
RE_SKILLMD = re.compile(r"[A-Za-z0-9_\-./]+/SKILL\.md\b")
# python / python3 script invocations.
RE_PY_INVOKE = re.compile(r"\bpython3?\s+([A-Za-z0-9_\-./]+\.py)\b")
# Relative parent-dir paths.
RE_RELATIVE = re.compile(r"\.\./[A-Za-z0-9_\-./]+")

DYNAMIC_CHARS = set("{<$~*")
PLACEHOLDER_HINTS = ("path/to", "your-", "your_", "example.com", "...", "skill-name", "agent-name")
# Chars that, immediately before a match, signal a placeholder prefix was cut off
# (e.g. `{skill_path}/scripts/x.py`, `"$SKILL/scripts/x.py"`, `<plugin>/scripts/x.py`,
# `TC-001-.../tc_record.json` — a literal `.` before `../` means an `...` ellipsis).
PLACEHOLDER_PREFIX_CHARS = set("}$>*~.")
# Gitignored maintainer-local folders (see root CLAUDE.md): references into these
# are intentional dead links for cloners — not phantom paths.
MAINTAINER_LOCAL = ("megaprompts", "documentation", "eval-workspace", "tests", ".autoresearch")


def is_dynamic(token: str) -> bool:
    if any(c in DYNAMIC_CHARS for c in token):
        return True
    if "://" in token or token.startswith("http"):
        return True
    low = token.lower()
    return any(h in low for h in PLACEHOLDER_HINTS)


def clean(token: str) -> str:
    token = token.strip().strip("`'\"()[]<>,;:")
    while token.startswith("./"):
        token = token[2:]
    return token.rstrip(".")


def extract_candidates(text: str):
    """Yield normalized path candidates found in text."""
    seen = set()
    for regex, group in ((RE_MARKER_PATH, 0), (RE_SKILLMD, 0), (RE_PY_INVOKE, 1), (RE_RELATIVE, 0)):
        for m in regex.finditer(text):
            start = m.start(group)
            if start > 0 and text[start - 1] in PLACEHOLDER_PREFIX_CHARS:
                continue  # truncated placeholder like {skill_path}/scripts/x.py
            tok = clean(m.group(group))
            if not tok or "/" not in tok:
                continue
            if is_dynamic(tok):
                continue
            parts = [p for p in tok.split("/") if p and p != ".."]
            if parts and parts[0] in MAINTAINER_LOCAL:
                continue  # intentional gitignored maintainer-local link
            if tok not in seen:
                seen.add(tok)
                yield tok


def skill_root(file_path: str, repo_root: str) -> str:
    """Walk up from the file's dir to the nearest skill/plugin root."""
    d = os.path.dirname(os.path.abspath(file_path))
    # If the file sits in an agents/ or commands/ dir, the plugin root is above it.
    while True:
        if (os.path.isfile(os.path.join(d, "SKILL.md"))
                or os.path.isdir(os.path.join(d, ".claude-plugin"))
                or os.path.isfile(os.path.join(d, "plugin.json"))):
            return d
        parent = os.path.dirname(d)
        if parent == d or os.path.abspath(d) == os.path.abspath(repo_root):
            return os.path.abspath(repo_root)
        d = parent


def resolves(candidate: str, bases) -> bool:
    for base in bases:
        p = os.path.normpath(os.path.join(base, candidate))
        if os.path.exists(p):
            return True
    return False


def load_allowlist(repo_root: str):
    """Read scripts/check_paths_allowlist.txt: `file-glob :: candidate-glob` per line.

    Each entry whitelists a known false positive (teaching examples, hypothetical
    user-project paths, example tool output). Keep entries narrow — one file glob
    plus one candidate glob — so real path contracts stay checked.
    """
    entries = []
    path = os.path.join(repo_root, "scripts", "check_paths_allowlist.txt")
    if not os.path.isfile(path):
        return entries
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.split("#", 1)[0].strip()
            if not line or "::" not in line:
                continue
            file_glob, cand_glob = (part.strip() for part in line.split("::", 1))
            if file_glob and cand_glob:
                entries.append((file_glob, cand_glob))
    return entries


def allowlisted(rel_file: str, candidate: str, allowlist) -> bool:
    return any(
        fnmatch.fnmatch(rel_file, fg) and fnmatch.fnmatch(candidate, cg)
        for fg, cg in allowlist
    )


def scan_file(path: str, repo_root: str, allowlist=()):
    """Return list of unresolvable path candidates in file."""
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError as exc:
        return [f"<unreadable: {exc}>"]
    file_dir = os.path.dirname(os.path.abspath(path))
    bases = (skill_root(path, repo_root), file_dir, os.path.abspath(repo_root))
    rel_file = os.path.relpath(os.path.abspath(path), repo_root)
    return [c for c in extract_candidates(text)
            if not resolves(c, bases) and not allowlisted(rel_file, c, allowlist)]


def collect_canonical(repo_root: str):
    """All SKILL.md + *.md under any agents/ or commands/ dir, excluding sync/doc trees."""
    targets = []
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
        parts = os.path.relpath(dirpath, repo_root).split(os.sep)
        in_canonical_dir = "agents" in parts or "commands" in parts
        for fn in filenames:
            if fn == "SKILL.md" or (in_canonical_dir and fn.endswith(".md")):
                targets.append(os.path.join(dirpath, fn))
    return sorted(targets)


def main():
    ap = argparse.ArgumentParser(
        description="Lint SKILL.md / agents / commands files for phantom (unresolvable) path references."
    )
    ap.add_argument("files", nargs="*", help="Specific markdown files to scan")
    ap.add_argument("--all", action="store_true",
                    help="Scan all SKILL.md + agents/*.md + commands/*.md in the repo")
    ap.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable output")
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    help="Repo root (default: parent of this script)")
    args = ap.parse_args()

    repo_root = os.path.abspath(args.root)
    if args.all:
        targets = collect_canonical(repo_root)
    elif args.files:
        targets = [os.path.abspath(f) for f in args.files]
    else:
        ap.print_help()
        return 0

    allowlist = load_allowlist(repo_root)
    findings = {}
    for f in targets:
        bad = scan_file(f, repo_root, allowlist)
        if bad:
            findings[os.path.relpath(f, repo_root)] = bad

    total = sum(len(v) for v in findings.values())
    if args.json:
        print(json.dumps({"files_scanned": len(targets), "files_with_findings": len(findings),
                          "total_unresolvable": total, "findings": findings}, indent=2))
    else:
        for f in sorted(findings):
            print(f"{f}:")
            for p in findings[f]:
                print(f"  UNRESOLVABLE: {p}")
        print(f"\nScanned {len(targets)} files; {len(findings)} files with findings; "
              f"{total} unresolvable path references.")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
