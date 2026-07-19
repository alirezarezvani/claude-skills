#!/usr/bin/env python3
"""Dual-publish drift guard (audit gate G4).

Several skills are published twice on purpose:

  bundled:     <domain>/skills/<name>/...
  standalone:  <domain>/<name>/skills/<name>/...
            or <domain>/compliance-team-*/skills/<name>/...   (ra-qm-team pattern)

The two copies are kept in sync by scripts/sync_skill_bundles.py. This guard
discovers every such pair programmatically and recursively compares the two
trees (a `diff -rq` equivalent built on os.walk + filecmp with full content
comparison). Any file that exists on only one side, or whose content differs,
is drift.

Exit codes:
  0  all pairs identical
  1  drift detected (drifted files listed on stdout)
  2  unexpected error (e.g. repo root not found)

Usage:
  python3 scripts/check_dual_publish.py            # check all pairs
  python3 scripts/check_dual_publish.py --list     # show discovered pairs
  python3 scripts/check_dual_publish.py --json     # machine-readable report
"""
from __future__ import annotations

import argparse
import filecmp
import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Top-level directories that are never skill domains (sync copies, docs, VCS).
EXCLUDE_TOP_LEVEL = {
    ".git", ".github", ".codex", ".gemini", ".hermes", ".vibe", ".claude",
    ".claude-plugin", ".codex-plugin", "docs", "audit", "node_modules",
    "integrations", "eval-workspace", "templates", "standards", "assets",
    "scripts", "agents", "commands", "orchestration", "custom-gpt", "site",
}

# Directory names that may never appear inside a compared payload
# (none expected today; kept for future-proofing against editor litter).
IGNORE_NAMES = {"__pycache__", ".DS_Store"}


def is_skill_dir(path):
    return os.path.isfile(os.path.join(path, "SKILL.md"))


def discover_pairs(repo_root):
    """Return [(bundled_rel, standalone_rel)] for every dual-publish pair."""
    pairs = []
    for domain in sorted(os.listdir(repo_root)):
        domain_path = os.path.join(repo_root, domain)
        if domain in EXCLUDE_TOP_LEVEL or domain.startswith("."):
            continue
        if not os.path.isdir(domain_path):
            continue
        bundled_root = os.path.join(domain_path, "skills")
        if not os.path.isdir(bundled_root):
            continue
        for name in sorted(os.listdir(bundled_root)):
            bundled = os.path.join(bundled_root, name)
            if not is_skill_dir(bundled):
                continue
            candidates = [os.path.join(domain_path, name, "skills", name)]
            for entry in sorted(os.listdir(domain_path)):
                if entry.startswith("compliance-team-"):
                    candidates.append(
                        os.path.join(domain_path, entry, "skills", name))
            for cand in candidates:
                if is_skill_dir(cand):
                    pairs.append((
                        os.path.relpath(bundled, repo_root),
                        os.path.relpath(cand, repo_root),
                    ))
    return pairs


def _listdir(path):
    try:
        return sorted(e for e in os.listdir(path) if e not in IGNORE_NAMES)
    except OSError:
        return []


def compare_trees(left, right, rel=""):
    """Recursive diff -rq equivalent. Returns list of drift descriptions."""
    drift = []
    left_entries = set(_listdir(left))
    right_entries = set(_listdir(right))

    for entry in sorted(left_entries - right_entries):
        drift.append(f"only-in-bundled: {os.path.join(rel, entry)}")
    for entry in sorted(right_entries - left_entries):
        drift.append(f"only-in-standalone: {os.path.join(rel, entry)}")

    for entry in sorted(left_entries & right_entries):
        lp = os.path.join(left, entry)
        rp = os.path.join(right, entry)
        sub_rel = os.path.join(rel, entry)
        l_dir, r_dir = os.path.isdir(lp), os.path.isdir(rp)
        if l_dir != r_dir:
            drift.append(f"type-mismatch (file vs dir): {sub_rel}")
        elif l_dir:
            drift.extend(compare_trees(lp, rp, sub_rel))
        else:
            try:
                same = filecmp.cmp(lp, rp, shallow=False)
            except OSError as exc:
                drift.append(f"unreadable: {sub_rel} ({exc})")
                continue
            if not same:
                drift.append(f"differs: {sub_rel}")
    return drift


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Verify dual-published skill pairs are byte-identical "
                    "(gate G4).")
    parser.add_argument("--list", action="store_true",
                        help="list discovered pairs and exit")
    parser.add_argument("--json", action="store_true",
                        help="emit a JSON report instead of human-readable output")
    parser.add_argument("--root", default=REPO_ROOT,
                        help="repo root (default: parent of this script)")
    args = parser.parse_args(argv)

    if not os.path.isdir(args.root):
        print(f"ERROR: repo root not found: {args.root}", file=sys.stderr)
        return 2

    pairs = discover_pairs(args.root)

    if args.list:
        if args.json:
            print(json.dumps(
                [{"bundled": b, "standalone": s} for b, s in pairs], indent=2))
        else:
            for bundled, standalone in pairs:
                print(f"{bundled}  <->  {standalone}")
            print(f"\n{len(pairs)} dual-publish pair(s) discovered")
        return 0

    report = []
    drifted_pairs = 0
    for bundled, standalone in pairs:
        drift = compare_trees(
            os.path.join(args.root, bundled),
            os.path.join(args.root, standalone))
        report.append({"bundled": bundled, "standalone": standalone,
                       "drift": drift})
        if drift:
            drifted_pairs += 1

    if args.json:
        print(json.dumps({
            "pairs": len(pairs),
            "drifted": drifted_pairs,
            "results": report,
        }, indent=2))
    else:
        for item in report:
            status = "DRIFT" if item["drift"] else "OK"
            print(f"[{status}] {item['bundled']}  <->  {item['standalone']}")
            for line in item["drift"]:
                print(f"    {line}")
        print(f"\n{len(pairs)} pair(s) checked, {drifted_pairs} drifted")

    if not pairs:
        print("WARNING: no dual-publish pairs discovered — discovery logic "
              "may be stale", file=sys.stderr)

    return 1 if drifted_pairs else 0


if __name__ == "__main__":
    sys.exit(main())
