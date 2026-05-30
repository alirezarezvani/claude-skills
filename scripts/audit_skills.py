#!/usr/bin/env python3
"""Run skill_review_checklist_runner on every SKILL.md in the repo + aggregate."""

import json
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNNER = os.path.join(
    REPO_ROOT,
    "engineering/write-a-skill/skills/write-a-skill/scripts/skill_review_checklist_runner.py"
)

EXCLUDE_PATTERNS = ("node_modules", "/.codex/", "/.gemini/", "/.cursor/", "/.cline/", "/site/", "/.git/", "/templates/", "assets/sample-skill")


def find_skills():
    skills = []
    for root, _, files in os.walk(REPO_ROOT):
        if any(p in root for p in EXCLUDE_PATTERNS):
            continue
        if "SKILL.md" in files:
            skills.append(root)
    return sorted(skills)


def audit_skill(skill_folder):
    """Run the runner; return parsed JSON result."""
    try:
        out = subprocess.run(
            ["python3", RUNNER, skill_folder, "--output", "json"],
            capture_output=True, text=True, timeout=10,
        )
        return json.loads(out.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError) as e:
        return {"error": str(e), "folder": skill_folder, "passed": 0, "total": 6, "overall": "ERROR"}


def main():
    skills = find_skills()
    print(f"Auditing {len(skills)} skills...\n", file=sys.stderr)

    results = []
    for i, folder in enumerate(skills, 1):
        if i % 50 == 0:
            print(f"  ... {i}/{len(skills)}", file=sys.stderr)
        results.append(audit_skill(folder))

    # Aggregate
    pass_count = sum(1 for r in results if r.get("overall") == "PASS")
    warn_count = sum(1 for r in results if r.get("overall") == "WARN")
    fail_count = sum(1 for r in results if r.get("overall") == "FAIL")
    error_count = sum(1 for r in results if r.get("overall") == "ERROR")

    # Count failures by rule
    rule_failures = {}
    for r in results:
        for check in r.get("checks", []):
            if not check.get("pass"):
                rule = check.get("rule", "unknown")
                rule_failures[rule] = rule_failures.get(rule, 0) + 1

    # Top-10 worst (most failed checks)
    worst = sorted(
        results,
        key=lambda r: (r.get("passed", 0), -len(r.get("folder", ""))),
    )[:10]

    print("=" * 72)
    print("REPO-WIDE SKILL AUDIT (write-a-skill review checklist)")
    print("=" * 72)
    print(f"\nTotal SKILL.md audited: {len(results)}")
    print(f"  PASS  (6/6): {pass_count} ({100*pass_count//max(len(results),1)}%)")
    print(f"  WARN  (5/6): {warn_count}")
    print(f"  FAIL  (≤4/6): {fail_count}")
    print(f"  ERROR (couldn't parse): {error_count}")

    print("\n" + "-" * 72)
    print("FAILURES BY RULE")
    print("-" * 72)
    for rule, count in sorted(rule_failures.items(), key=lambda x: -x[1]):
        pct = 100 * count // max(len(results), 1)
        print(f"  {count:>4d} ({pct:>3d}%)  {rule}")

    print("\n" + "-" * 72)
    print("TOP-10 WORST OFFENDERS")
    print("-" * 72)
    for w in worst:
        folder = w.get("folder", "?").replace(REPO_ROOT + "/", "")
        passed = w.get("passed", 0)
        failed_rules = [c["rule"] for c in w.get("checks", []) if not c.get("pass")]
        print(f"\n  [{passed}/6] {folder}")
        for fr in failed_rules:
            print(f"    - {fr}")


if __name__ == "__main__":
    main()
