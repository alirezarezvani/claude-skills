#!/usr/bin/env python3
"""Repo-wide `--help` smoke gate for Python tools (audit gate G8).

Contract: every `.py` file in the canonical tree must exit 0 on
`python3 <file> --help` within 15 seconds. Hook-style scripts that read
stdin and fixed-contract evaluators are listed (with a reason) in
scripts/smoke_exceptions.txt and skipped.

Excluded directories: derived sync copies (.codex/.gemini/.hermes/.vibe),
docs/, audit/, node_modules/, .git/, generated integrations/, gitignored
maintainer-local folders, and __pycache__.

Exit codes:
  0  every non-excepted script passed
  1  one or more non-excepted scripts failed (listed on stdout)
  2  harness error (e.g. exceptions file unreadable)

Usage:
  python3 scripts/smoke_scripts.py            # human-readable report
  python3 scripts/smoke_scripts.py --json     # machine-readable report
  python3 scripts/smoke_scripts.py --jobs 4   # control parallelism
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEPTIONS_FILE = os.path.join(REPO_ROOT, "scripts", "smoke_exceptions.txt")
TIMEOUT_SECONDS = 15

# Directory names pruned anywhere in the walk.
EXCLUDE_DIRS = {
    ".git", ".codex", ".gemini", ".hermes", ".vibe", "docs", "audit",
    "node_modules", "integrations", "eval-workspace", "site",
    "__pycache__", ".venv", "venv",
}


def load_exceptions(path):
    """Parse the by-design exceptions file: `<relpath>  # reason` per line."""
    exceptions = {}
    if not os.path.isfile(path):
        return exceptions
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "#" in line:
                rel, reason = line.split("#", 1)
                exceptions[rel.strip()] = reason.strip()
            else:
                exceptions[line] = "(no reason given)"
    return exceptions


def find_python_files(root):
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(
            d for d in dirnames if d not in EXCLUDE_DIRS)
        for name in sorted(filenames):
            if name.endswith(".py"):
                files.append(os.path.relpath(
                    os.path.join(dirpath, name), root).replace(os.sep, "/"))
    return files


def smoke_one(rel_path):
    """Run `python3 <file> --help`; return (rel_path, ok, detail)."""
    abs_path = os.path.join(REPO_ROOT, rel_path)
    try:
        proc = subprocess.run(
            [sys.executable, abs_path, "--help"],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            cwd=os.path.dirname(abs_path),
        )
    except subprocess.TimeoutExpired:
        return rel_path, False, f"timeout after {TIMEOUT_SECONDS}s"
    except OSError as exc:
        return rel_path, False, f"could not execute: {exc}"
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()
        detail = tail[-1] if tail else "(no output)"
        return rel_path, False, f"exit {proc.returncode}: {detail[:200]}"
    return rel_path, True, ""


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Run `python3 <file> --help` on every .py in the "
                    "canonical tree and assert exit 0 (gate G8).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Exit codes:\n"
               "  0  all scripts passed --help, no stale exceptions\n"
               "  1  one or more scripts failed the --help smoke test\n"
               "  3  smoke_exceptions.txt lists files that no longer exist")
    parser.add_argument("--json", action="store_true",
                        help="emit a JSON report instead of human-readable output")
    parser.add_argument("--jobs", type=int, default=os.cpu_count() or 4,
                        help="parallel workers (default: CPU count)")
    parser.add_argument("--root", default=REPO_ROOT,
                        help="repo root (default: parent of this script)")
    args = parser.parse_args(argv)

    try:
        exceptions = load_exceptions(EXCEPTIONS_FILE)
    except OSError as exc:
        print(f"ERROR: cannot read exceptions file: {exc}", file=sys.stderr)
        return 2

    all_files = find_python_files(args.root)
    to_check = [f for f in all_files if f not in exceptions]
    skipped = sorted(set(all_files) & set(exceptions))
    stale_exceptions = sorted(set(exceptions) - set(all_files))

    failures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for rel_path, ok, detail in pool.map(smoke_one, to_check):
            if not ok:
                failures.append({"file": rel_path, "detail": detail})
    failures.sort(key=lambda f: f["file"])

    if args.json:
        print(json.dumps({
            "total": len(all_files),
            "checked": len(to_check),
            "passed": len(to_check) - len(failures),
            "failed": failures,
            "skipped_by_exception": [
                {"file": f, "reason": exceptions[f]} for f in skipped],
            "stale_exceptions": stale_exceptions,
        }, indent=2))
    else:
        print(f"Scripts found:   {len(all_files)}")
        print(f"Checked:         {len(to_check)}")
        print(f"Passed:          {len(to_check) - len(failures)}")
        print(f"Failed:          {len(failures)}")
        print(f"Skipped (by-design exceptions): {len(skipped)}")
        if failures:
            print("\nFAILURES:")
            for f in failures:
                print(f"  {f['file']}")
                print(f"      {f['detail']}")
        if stale_exceptions:
            print("\nERROR: exceptions listing files that no longer exist")
            print("(remove them from scripts/smoke_exceptions.txt):")
            for f in stale_exceptions:
                print(f"  {f}")

    if failures:
        return 1
    # Only reached when no --help failures; a real failure (exit 1) takes
    # precedence over allowlist hygiene (exit 3).
    if stale_exceptions:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
