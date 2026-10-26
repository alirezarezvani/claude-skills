#!/usr/bin/env python3
"""JSON-output verification gate for Python tools (audit gate G9).

Companion to smoke_scripts.py (which only asserts `--help` exits 0). Many tools
advertise `--json` or `--format json` in their help text but require positional
or required arguments before they can emit anything — so a bare-flag smoke test
reports false failures (see issue #654).

This harness verifies JSON output the way the tools are actually meant to run:

  1. Discover every tool whose `--help` advertises JSON output AND an embedded
     `--sample` fixture (the chosen convention — issue #654 Option A).
  2. Run `<tool> --sample <json-flag>` and assert stdout parses as JSON.

Tools that advertise JSON output but do NOT yet expose `--sample` are
"uncovered". The gate is a ratchet: every uncovered tool must be listed in
scripts/smoke_json_baseline.txt (the legacy backlog as of Oct 2026). A NEW tool
that advertises JSON without `--sample` fails, and so does a baseline entry
whose tool now has `--sample` (or no longer exists) — delete that line, so the
backlog only ever shrinks. Pass --strict to fail on every uncovered tool,
baseline or not, once the backlog is cleared.

Exit codes:
  0  every --sample JSON tool produced valid JSON, no uncovered tool is missing
     from the baseline, and the baseline holds no stale entries
  1  invalid JSON / error from a --sample run, a new uncovered tool, a stale
     baseline entry, or (with --strict) any uncovered tool
  2  harness error

Usage:
  python3 scripts/smoke_json_output.py            # human-readable report
  python3 scripts/smoke_json_output.py --json     # machine-readable report
  python3 scripts/smoke_json_output.py --strict   # uncovered JSON tools fail
  python3 scripts/smoke_json_output.py --update-baseline   # rewrite the backlog
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIMEOUT_SECONDS = 20

# Reuse the same exclusion set + exceptions file as the --help gate.
EXCLUDE_DIRS = {
    ".git", ".codex", ".gemini", ".hermes", ".vibe", "docs", "audit",
    "node_modules", "integrations", "eval-workspace", "site",
    "__pycache__", ".venv", "venv",
}
EXCEPTIONS_FILE = os.path.join(REPO_ROOT, "scripts", "smoke_exceptions.txt")
BASELINE_FILE = os.path.join(REPO_ROOT, "scripts", "smoke_json_baseline.txt")

# The smoke harnesses describe `--sample`/`--json` in their own help text but
# are gate runners, not analysis tools — never classify them as JSON tools.
SELF_SKIP = {"scripts/smoke_json_output.py", "scripts/smoke_scripts.py"}

# `--format json` is only a valid invocation when help shows json as a choice,
# e.g. `--format {text,json}`. A bare mention of the word "format" elsewhere in
# help must not trigger it (that misfires on tools that only accept `--json`).
_FORMAT_JSON_RE = re.compile(r"--format[ =]?\{[^}]*\bjson\b[^}]*\}")


def load_exceptions(path):
    exceptions = {}
    if not os.path.isfile(path):
        return exceptions
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            rel = line.split("#", 1)[0].strip()
            if rel:
                exceptions[rel] = True
    return exceptions


def find_python_files(root):
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDE_DIRS)
        for name in sorted(filenames):
            if name.endswith(".py"):
                files.append(os.path.relpath(
                    os.path.join(dirpath, name), root).replace(os.sep, "/"))
    return files


def _help_text(abs_path):
    try:
        proc = subprocess.run(
            [sys.executable, abs_path, "--help"],
            stdin=subprocess.DEVNULL, capture_output=True, text=True,
            timeout=TIMEOUT_SECONDS, cwd=os.path.dirname(abs_path),
        )
    except (subprocess.TimeoutExpired, OSError):
        return ""
    return (proc.stdout or "") + (proc.stderr or "") if proc.returncode == 0 else ""


def classify(rel_path):
    """Return (advertises_json, json_flag, has_sample) for one tool."""
    # Top-level scripts/ holds repo tooling (gates, syncs), not skill tools.
    if rel_path in SELF_SKIP or rel_path.startswith("scripts/"):
        return False, None, False
    abs_path = os.path.join(REPO_ROOT, rel_path)
    help_text = _help_text(abs_path)
    if not help_text:
        return False, None, False
    low = help_text.lower()
    # Prefer `--format json` only when help shows json as an actual choice;
    # otherwise fall back to a plain `--json` flag.
    json_flag = None
    if _FORMAT_JSON_RE.search(low):
        json_flag = ["--format", "json"]
    elif re.search(r"(?<![\w-])--json(?![\w-])", low):
        json_flag = ["--json"]
    advertises_json = json_flag is not None
    has_sample = "--sample" in low
    return advertises_json, json_flag, has_sample


def verify_one(rel_path, json_flag):
    """Run `<tool> --sample <json_flag>` and check stdout parses as JSON."""
    abs_path = os.path.join(REPO_ROOT, rel_path)
    try:
        proc = subprocess.run(
            [sys.executable, abs_path, "--sample", *json_flag],
            stdin=subprocess.DEVNULL, capture_output=True, text=True,
            timeout=TIMEOUT_SECONDS, cwd=os.path.dirname(abs_path),
        )
    except subprocess.TimeoutExpired:
        return rel_path, False, f"timeout after {TIMEOUT_SECONDS}s"
    except OSError as exc:
        return rel_path, False, f"could not execute: {exc}"
    # A non-zero exit is acceptable only if the tool intentionally signals a
    # finding through its exit code (e.g. blast_radius RED) — but it must still
    # have emitted valid JSON on stdout.
    out = (proc.stdout or "").strip()
    if not out:
        tail = (proc.stderr or "").strip().splitlines()
        return rel_path, False, f"no stdout (exit {proc.returncode}): {tail[-1] if tail else ''}"[:200]
    try:
        json.loads(out)
    except json.JSONDecodeError as exc:
        return rel_path, False, f"stdout is not valid JSON: {exc}"
    return rel_path, True, ""


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="store_true",
                        help="emit a JSON report instead of human-readable output")
    parser.add_argument("--strict", action="store_true",
                        help="treat JSON-advertising tools without --sample as failures")
    parser.add_argument("--baseline", default=BASELINE_FILE,
                        help="legacy uncovered-tool backlog (default: scripts/smoke_json_baseline.txt)")
    parser.add_argument("--update-baseline", action="store_true",
                        help="rewrite the baseline to the current uncovered list and exit")
    parser.add_argument("--jobs", type=int, default=os.cpu_count() or 4,
                        help="parallel workers (default: CPU count)")
    parser.add_argument("--root", default=REPO_ROOT, help="repo root")
    args = parser.parse_args(argv)

    try:
        exceptions = load_exceptions(EXCEPTIONS_FILE)
    except OSError as exc:
        print(f"ERROR: cannot read exceptions file: {exc}", file=sys.stderr)
        return 2

    all_files = [f for f in find_python_files(args.root) if f not in exceptions]

    # Phase 1: classify in parallel.
    json_tools = {}   # rel_path -> json_flag
    uncovered = []    # advertises json but no --sample
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = pool.map(lambda f: (f, *classify(f)), all_files)
        for rel_path, advertises, json_flag, has_sample in results:
            if not advertises:
                continue
            if has_sample:
                json_tools[rel_path] = json_flag
            else:
                uncovered.append(rel_path)
    uncovered.sort()

    if args.update_baseline:
        with open(args.baseline, "w", encoding="utf-8") as f:
            f.write("# Gate G9 ratchet: tools that advertise JSON output but have no --sample yet.\n"
                    "# Only ever delete lines (after adding --sample). New tools may not be added here.\n"
                    "# Regenerate with: python3 scripts/smoke_json_output.py --update-baseline\n")
            f.writelines(p + "\n" for p in uncovered)
        print(f"Wrote {len(uncovered)} entries to {os.path.relpath(args.baseline, args.root)}")
        return 0

    try:
        baseline = set(load_exceptions(args.baseline))
    except OSError as exc:
        print(f"ERROR: cannot read baseline file: {exc}", file=sys.stderr)
        return 2
    new_uncovered = [p for p in uncovered if p not in baseline]
    stale_baseline = sorted(baseline - set(uncovered))

    # Phase 2: verify covered tools in parallel.
    failures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for rel_path, ok, detail in pool.map(
                lambda item: verify_one(item[0], item[1]), sorted(json_tools.items())):
            if not ok:
                failures.append({"file": rel_path, "detail": detail})
    failures.sort(key=lambda f: f["file"])

    covered = len(json_tools)
    total_json = covered + len(uncovered)
    coverage_pct = round(100 * covered / total_json, 1) if total_json else 100.0

    if args.json:
        print(json.dumps({
            "json_advertising_tools": total_json,
            "covered_by_sample": covered,
            "coverage_pct": coverage_pct,
            "verified_ok": covered - len(failures),
            "failed": failures,
            "uncovered": uncovered,
            "new_uncovered": new_uncovered,
            "stale_baseline": stale_baseline,
        }, indent=2))
    else:
        print(f"JSON-advertising tools:   {total_json}")
        print(f"Covered by --sample:      {covered}  ({coverage_pct}%)")
        print(f"Verified valid JSON:      {covered - len(failures)}")
        print(f"Failed:                   {len(failures)}")
        print(f"Uncovered (no --sample):  {len(uncovered)}")
        print(f"In legacy baseline:       {len(uncovered) - len(new_uncovered)}")
        if failures:
            print("\nFAILURES:")
            for f in failures:
                print(f"  {f['file']}\n      {f['detail']}")
        if new_uncovered:
            print("\nNEW TOOLS WITHOUT --sample (add an embedded --sample fixture; do not baseline them):")
            for f in new_uncovered:
                print(f"  {f}")
        if stale_baseline:
            print("\nSTALE BASELINE ENTRIES (now covered or removed; delete these lines from the baseline):")
            for f in stale_baseline:
                print(f"  {f}")

    if failures or new_uncovered or stale_baseline:
        return 1
    if args.strict and uncovered:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
