#!/usr/bin/env python3
"""Generate changelog sections from git log using conventional commit prefixes."""

import argparse
import subprocess
from collections import defaultdict


SECTIONS = {
    "feat": "Features",
    "fix": "Fixes",
    "docs": "Documentation",
    "refactor": "Refactors",
    "test": "Tests",
    "chore": "Chores",
    "perf": "Performance",
    "ci": "CI",
    "build": "Build",
    "style": "Style",
    "revert": "Reverts",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate changelog from git commits.")
    parser.add_argument("--from", dest="from_ref", default="HEAD~50")
    parser.add_argument("--to", dest="to_ref", default="HEAD")
    parser.add_argument("--format", choices=["markdown", "text"], default="markdown")
    return parser.parse_args()


def get_git_log(from_ref: str, to_ref: str) -> list[str]:
    commit_range = f"{from_ref}..{to_ref}"
    cmd = ["git", "log", "--pretty=format:%s", commit_range]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return lines


def group_commits(subjects: list[str]) -> dict[str, list[str]]:
    grouped = defaultdict(list)
    grouped["other"] = []

    for subject in subjects:
        commit_type = "other"
        for prefix in SECTIONS:
            if subject.startswith(f"{prefix}:"):
                commit_type = prefix
                break
        grouped[commit_type].append(subject)

    return grouped


def render_markdown(grouped: dict[str, list[str]]) -> str:
    out = ["# Changelog", ""]
    ordered_types = list(SECTIONS.keys()) + ["other"]
    for commit_type in ordered_types:
        commits = grouped.get(commit_type, [])
        if not commits:
            continue
        header = SECTIONS.get(commit_type, "Other")
        out.append(f"## {header}")
        for item in commits:
            out.append(f"- {item}")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def render_text(grouped: dict[str, list[str]]) -> str:
    out = []
    ordered_types = list(SECTIONS.keys()) + ["other"]
    for commit_type in ordered_types:
        commits = grouped.get(commit_type, [])
        if not commits:
            continue
        header = SECTIONS.get(commit_type, "Other")
        out.append(header.upper())
        for item in commits:
            out.append(f"* {item}")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    subjects = get_git_log(args.from_ref, args.to_ref)
    grouped = group_commits(subjects)

    if args.format == "markdown":
        print(render_markdown(grouped), end="")
    else:
        print(render_text(grouped), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
