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

Tools that advertise JSON output but do NOT yet expose `--sample` are reported
as "uncovered" — a to-do list for backporting the convention, not a failure
(so the gate can be adopted incrementally without going red on day one).
Pass --strict to treat uncovered JSON tools as failures once coverage is high.

Exit codes:
  0  every --sample JSON tool produced valid JSON (and, with --strict, every
     JSON-advertising tool exposes --sample)
  1  one or more --sample JSON runs produced invalid JSON / errored
  2  harness error

Usage:
  python3 scripts/smoke_json_output.py            # human-readable report
  python3 scripts/smoke_json_output.py --json     # machine-readable report
  python3 scripts/smoke_json_output.py --strict   # uncovered JSON tools fail
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
    if rel_path in SELF_SKIP:
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
        }, indent=2))
    else:
        print(f"JSON-advertising tools:   {total_json}")
        print(f"Covered by --sample:      {covered}  ({coverage_pct}%)")
        print(f"Verified valid JSON:      {covered - len(failures)}")
        print(f"Failed:                   {len(failures)}")
        print(f"Uncovered (no --sample):  {len(uncovered)}")
        if failures:
            print("\nFAILURES:")
            for f in failures:
                print(f"  {f['file']}\n      {f['detail']}")
        if uncovered:
            print("\nUNCOVERED (advertise JSON but lack --sample — backport target):")
            for f in uncovered:
                print(f"  {f}")

    if failures:
        return 1
    if args.strict and uncovered:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
