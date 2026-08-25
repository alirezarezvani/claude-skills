#!/usr/bin/env python3
"""check_model_freshness.py — retired-model-identifier linter (gate G7).

Proposed by audit/newgen-2026-06/00-MASTER.md and never built, which is why
retired model IDs and 2024 price tables kept drifting past two later audits.

Flags references to model identifiers that no longer exist, are no longer
current, or are presented as current when they are not. The point is not to
chase whatever is newest: it is to catch the cases that mislead a reader or
break on execution, namely

  - script defaults and config values naming a retired model
  - cost/pricing tables keyed on a retired model
  - copy-pasteable CLI examples pinning a retired versioned ID

Dated citations are legitimate and must NOT be flagged. A reference is treated
as a citation when the same line carries a year, an arXiv ID, the words
"paper"/"technical report"/"model card"/"as of"/"historical", or a
"snapshot"/"deprecated"/"retired" marker. Anything else needs an entry in
scripts/check_model_freshness_allowlist.txt with a reason.

Exit codes: 0 = clean, 1 = at least one unexplained retired identifier.

Usage:
  python3 scripts/check_model_freshness.py --all
  python3 scripts/check_model_freshness.py FILE [FILE ...]
  python3 scripts/check_model_freshness.py --all --json
  python3 scripts/check_model_freshness.py --list-patterns
"""

import argparse
import fnmatch
import json
import os
import re
import sys

# Excludes both directory names (pruned during walk) and individual filenames
# (e.g. CHANGELOG.md) — membership is checked against dirnames AND filenames.
EXCLUDED_NAMES = {
    ".git", ".codex", ".gemini", ".hermes", ".vibe", "node_modules",
    "docs",   # generated mirror; fix the source instead
    "audit",  # audit records quote stale IDs on purpose, that is their job
    "CHANGELOG.md",
}

SCAN_EXTENSIONS = (".md", ".py", ".json", ".yaml", ".yml", ".sh", ".txt")

# This linter and its allowlist necessarily name retired models; scanning them
# would just require self-referential allowlist entries.
SELF_FILES = {"check_model_freshness.py", "check_model_freshness_allowlist.txt"}

# Retired or superseded identifiers, as (regex, label) pairs. Word-ish bounded
# so `claude-3` does not match `claude-3x-something` unintentionally.
RETIRED_PATTERNS = [
    (r"\bclaude-instant\b", "claude-instant (retired)"),
    (r"\bclaude-2(?:\.\d+)?\b", "Claude 2 family (retired)"),
    (r"\bclaude-3(?:[.-]\d+)?(?:-(?:opus|sonnet|haiku))?(?:-\d{8})?\b",
     "Claude 3 family (retired)"),
    (r"\bClaude\s+3(?:\.\d+)?\s+(?:Opus|Sonnet|Haiku)\b", "Claude 3 family (retired)"),
    # Haiku 4.5 (claude-haiku-4-5-20251001) is still current, so it is
    # excluded from the Claude 4 sweep rather than allowlisted per-file.
    (r"\bclaude-(?:opus|sonnet)-4(?:[.-]\d+)?(?:-\d{8})?\b",
     "Claude 4 family (superseded by Claude 5)"),
    (r"\bclaude-haiku-4(?!\W*5)(?:[.-]\d+)?(?:-\d{8})?\b",
     "Claude 4 family (superseded by Claude 5)"),
    (r"\bClaude\s+(?:Opus|Sonnet)\s+4(?:\.\d+)?\b",
     "Claude 4 family (superseded by Claude 5)"),
    (r"\bClaude\s+Haiku\s+4(?!\.5)(?:\.\d+)?\b",
     "Claude 4 family (superseded by Claude 5)"),
    (r"\banthropic/claude-[a-z]+-4[.-]\d+\b", "Claude 4 family (superseded by Claude 5)"),
    (r"\bgpt-3\.5(?:-turbo)?\b", "gpt-3.5 (retired)"),
    # Longer variants first: alternation is ordered, so `o-mini` must precede `o`
    # or `gpt-4o-mini` reports as `gpt-4o`.
    (r"\bgpt-4(?:-32k|o-mini|o)?\b", "gpt-4 family (superseded)"),
    (r"\bGPT-4(?:o|-32k)?\b", "gpt-4 family (superseded)"),
    (r"\btext-embedding-ada-002\b", "ada-002 embeddings (superseded)"),
    (r"\bgemini-1\.5(?:-[a-z]+)?\b", "Gemini 1.5 (superseded)"),
]

# Signals that a line is quoting a source or explicitly labelling age.
CITATION_HINTS = (
    "paper", "technical report", "model card", "as of", "historical",
    "snapshot", "deprecated", "retired", "superseded", "arxiv", "et al",
    "changelog", "was ", "formerly", "legacy", "pre-", "no longer",
)
YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")

# Lines that are much more likely to be a live default than prose.
EXECUTABLE_HINTS = (
    "model=", "model =", '"model"', "'model'", "model:", "--model",
    "-m ", "default=", "MODEL", "input\":", "output\":",
)


def load_allowlist(repo_root):
    """<file-glob> :: <substring>  — one per line, '#' comments."""
    path = os.path.join(repo_root, "scripts", "check_model_freshness_allowlist.txt")
    entries = []
    if not os.path.exists(path):
        return entries
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "::" not in line:
                continue
            file_glob, needle = (part.strip() for part in line.split("::", 1))
            entries.append((file_glob, needle))
    return entries


def allowlisted(rel_file, line_text, allowlist):
    posix = rel_file.replace(os.sep, "/")
    return any(fnmatch.fnmatch(posix, glob) and needle in line_text
               for glob, needle in allowlist)


def is_citation(line_text):
    lowered = line_text.lower()
    if YEAR_RE.search(line_text):
        return True
    return any(hint in lowered for hint in CITATION_HINTS)


def looks_executable(line_text):
    return any(hint in line_text for hint in EXECUTABLE_HINTS)


def scan_file(path, repo_root, allowlist):
    rel = os.path.relpath(path, repo_root)
    findings = []
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return findings

    for lineno, line in enumerate(text.splitlines(), 1):
        if allowlisted(rel, line, allowlist):
            continue
        for pattern, label in RETIRED_PATTERNS:
            match = re.search(pattern, line)
            if not match:
                continue
            # An executable default outweighs a citation hint on the same line:
            # `model: str = "claude-3-opus"  # 2024 default` still breaks.
            if is_citation(line) and not looks_executable(line):
                continue
            findings.append({
                "line": lineno,
                "match": match.group(0),
                "label": label,
                "executable": looks_executable(line),
                "text": line.strip()[:160],
            })
            break
    return findings


def collect(repo_root):
    targets = []
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_NAMES]
        for fn in filenames:
            if fn in EXCLUDED_NAMES or fn in SELF_FILES:
                continue
            if fn.endswith(SCAN_EXTENSIONS):
                targets.append(os.path.join(dirpath, fn))
    return sorted(targets)


def main():
    ap = argparse.ArgumentParser(
        description="Flag retired model identifiers presented as current."
    )
    ap.add_argument("files", nargs="*", help="Specific files to scan")
    ap.add_argument("--all", action="store_true", help="Scan the canonical tree")
    ap.add_argument("--json", action="store_true", help="Emit JSON")
    ap.add_argument("--list-patterns", action="store_true",
                    help="Print the retired-identifier deny-list and exit")
    ap.add_argument("--executable-only", action="store_true",
                    help="Report only script defaults, config values and CLI examples")
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    help="Repo root (default: parent of this script)")
    args = ap.parse_args()

    if args.list_patterns:
        for pattern, label in RETIRED_PATTERNS:
            print(f"{label}\n    {pattern}")
        return 0

    repo_root = os.path.abspath(args.root)
    if args.all:
        targets = collect(repo_root)
    elif args.files:
        targets = [os.path.abspath(f) for f in args.files]
    else:
        ap.print_help()
        return 0

    allowlist = load_allowlist(repo_root)
    findings = {}
    for path in targets:
        hits = scan_file(path, repo_root, allowlist)
        if args.executable_only:
            hits = [h for h in hits if h["executable"]]
        if hits:
            findings[os.path.relpath(path, repo_root)] = hits

    total = sum(len(v) for v in findings.values())
    n_exec = sum(1 for v in findings.values() for h in v if h["executable"])

    if args.json:
        print(json.dumps({
            "files_scanned": len(targets),
            "total_findings": total,
            "executable_findings": n_exec,
            "findings": findings,
        }, indent=2))
    else:
        for rel in sorted(findings):
            print(f"{rel}:")
            for hit in findings[rel]:
                tag = "EXEC" if hit["executable"] else "PROSE"
                print(f"  {tag} L{hit['line']}: {hit['match']} — {hit['label']}")
                print(f"        {hit['text']}")
        print(f"\nScanned {len(targets)} files; {total} retired-identifier references "
              f"({n_exec} in executable positions).")
        if total:
            print("Fix the reference, or add an allowlist entry with a reason to "
                  "scripts/check_model_freshness_allowlist.txt")

    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
