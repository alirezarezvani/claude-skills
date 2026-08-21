#!/usr/bin/env python3
"""check_frontmatter.py — YAML frontmatter validator for skills, agents, and commands.

Every other gate in this repo extracts frontmatter with a regex or a line scan
(see generate-docs.py and sync-codex-skills.py), so a block that is not valid
YAML sails through CI unnoticed. Claude Code parses it properly: when the YAML
is malformed it loads the body with EMPTY metadata, which silently removes the
skill's `description` from the skill listing and makes it invisible to
model invocation. Agents, where `name` and `description` are required, may fail
to load entirely.

This gate parses each block with yaml.safe_load and enforces the fields Claude
Code actually reads.

Errors (exit 1):
  - frontmatter block present but not parseable, or not a YAML mapping
  - missing `description` (skills/commands) or `name`/`description` (agents)
  - an agent `name` containing ':' (rejected by Claude Code >= 2.1.218)
  - no frontmatter block at all in a file that should have one

Warnings (exit 0 unless --strict):
  - keys outside the current Claude Code frontmatter spec
  - combined description + when_to_use over the 1536-char skill-listing cap

Exit codes: 0 = clean, 1 = at least one error (or a warning under --strict).
Intended as CI gate G10.

Usage:
  python3 scripts/check_frontmatter.py --all             # scan canonical dirs repo-wide
  python3 scripts/check_frontmatter.py FILE [FILE ...]   # scan specific files
  python3 scripts/check_frontmatter.py --all --json      # machine-readable output
  python3 scripts/check_frontmatter.py --all --strict    # warnings become errors
"""

import argparse
import fnmatch
import json
import os
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover - CI installs yamllint, which vendors PyYAML
    sys.stderr.write(
        "check_frontmatter.py needs PyYAML (pip install pyyaml). "
        "Parsing frontmatter with a regex is what this gate exists to prevent.\n"
    )
    sys.exit(2)

EXCLUDED_DIRS = {
    ".git", ".codex", ".gemini", ".hermes", ".vibe", "docs", "audit",
    "node_modules", ".github", ".claude-plugin",
}

FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)

# Files that legitimately carry no frontmatter: documentation that happens to
# live inside a canonical dir, and the skill-tester's deliberate bare fixture.
DOC_BASENAMES = {"README.md", "CLAUDE.md", "TEMPLATE.md"}
NO_FRONTMATTER_OK = ("*/assets/sample-skill/SKILL.md",)

# Claude Code skill frontmatter. Commands are skills, so they share this set.
# https://code.claude.com/docs/en/skills#frontmatter-reference
SKILL_SPEC_KEYS = {
    "name", "description", "when_to_use", "argument-hint", "arguments",
    "disable-model-invocation", "user-invocable", "allowed-tools",
    "disallowed-tools", "model", "effort", "context", "agent", "background",
    "hooks", "paths", "shell",
}

# Claude Code subagent frontmatter.
# https://code.claude.com/docs/en/sub-agents#write-subagent-files
AGENT_SPEC_KEYS = {
    "name", "description", "tools", "disallowedTools", "model",
    "permissionMode", "maxTurns", "skills", "mcpServers", "hooks", "memory",
    "background", "effort", "isolation", "color", "initialPrompt",
}

# Pre-existing repo conventions that no runtime reads. Reported separately from
# genuine typos so the migration in the v5 plan has a worklist rather than noise.
KNOWN_REPO_EXTRAS = {
    "license", "metadata", "version", "author", "tags", "compatible_tools",
    "triggers", "command", "domain", "title", "emoji", "vibe", "tier",
    "category", "dependencies", "not_for", "agents", "source", "attribution",
}

# Combined description + when_to_use budget per entry in the skill listing.
DESC_CAP = 1536


def kind_for(rel_path):
    """skill | agent | command, based on where the file lives."""
    if os.path.basename(rel_path) == "SKILL.md":
        return "skill"
    parts = rel_path.split(os.sep)
    if "agents" in parts:
        return "agent"
    return "command"


def no_frontmatter_ok(rel_path):
    if os.path.basename(rel_path) in DOC_BASENAMES:
        return True
    posix = rel_path.replace(os.sep, "/")
    return any(fnmatch.fnmatch(posix, pat) for pat in NO_FRONTMATTER_OK)


def check_file(path, repo_root):
    """Return (errors, warnings, offspec_keys) for one file."""
    rel = os.path.relpath(path, repo_root)
    kind = kind_for(rel)
    errors, warnings, offspec = [], [], []

    text = open(path, encoding="utf-8", errors="replace").read()
    match = FRONTMATTER_RE.match(text)
    if not match:
        if not no_frontmatter_ok(rel):
            errors.append("no YAML frontmatter block")
        return errors, warnings, offspec

    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        detail = str(exc).replace("\n", " ")
        errors.append(f"frontmatter is not valid YAML: {detail}")
        return errors, warnings, offspec

    if not isinstance(data, dict):
        errors.append(f"frontmatter is not a YAML mapping (parsed as {type(data).__name__})")
        return errors, warnings, offspec

    if not str(data.get("description") or "").strip():
        errors.append("missing `description` — Claude Code has nothing to match the skill against")

    if kind == "agent":
        name = str(data.get("name") or "").strip()
        if not name:
            errors.append("missing `name` — required for subagents")
        elif ":" in name:
            errors.append(f"`name: {name}` contains ':', which Claude Code >= 2.1.218 refuses to load")

    spec = AGENT_SPEC_KEYS if kind == "agent" else SKILL_SPEC_KEYS
    for key in data:
        if key in spec:
            continue
        if key in KNOWN_REPO_EXTRAS:
            offspec.append(key)
        else:
            warnings.append(f"unrecognized key `{key}` (not in the {kind} frontmatter spec)")

    listing = len(str(data.get("description") or "")) + len(str(data.get("when_to_use") or ""))
    if kind != "agent" and listing > DESC_CAP:
        warnings.append(
            f"description + when_to_use is {listing} chars; the skill listing truncates at {DESC_CAP}"
        )

    return errors, warnings, offspec


def collect_canonical(repo_root):
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
        description="Validate YAML frontmatter on SKILL.md / agents / commands files."
    )
    ap.add_argument("files", nargs="*", help="Specific markdown files to scan")
    ap.add_argument("--all", action="store_true",
                    help="Scan all SKILL.md + agents/*.md + commands/*.md in the repo")
    ap.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable output")
    ap.add_argument("--strict", action="store_true", help="Treat warnings as errors")
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

    errors, warnings = {}, {}
    offspec_counts = {}
    for path in targets:
        errs, warns, offspec = check_file(path, repo_root)
        rel = os.path.relpath(path, repo_root)
        if errs:
            errors[rel] = errs
        if warns:
            warnings[rel] = warns
        for key in offspec:
            offspec_counts[key] = offspec_counts.get(key, 0) + 1

    n_err = sum(len(v) for v in errors.values())
    n_warn = sum(len(v) for v in warnings.values())

    if args.json:
        print(json.dumps({
            "files_scanned": len(targets),
            "errors": errors,
            "warnings": warnings,
            "total_errors": n_err,
            "total_warnings": n_warn,
            "off_spec_key_counts": dict(sorted(offspec_counts.items(),
                                               key=lambda kv: -kv[1])),
        }, indent=2))
    else:
        for rel in sorted(errors):
            print(f"{rel}:")
            for msg in errors[rel]:
                print(f"  ERROR: {msg}")
        for rel in sorted(warnings):
            print(f"{rel}:")
            for msg in warnings[rel]:
                print(f"  WARN: {msg}")
        if offspec_counts:
            print("\nOff-spec keys still in use (no runtime reads these):")
            for key, count in sorted(offspec_counts.items(), key=lambda kv: -kv[1]):
                print(f"  {count:4d}  {key}")
        print(f"\nScanned {len(targets)} files; {n_err} errors, {n_warn} warnings.")

    if n_err:
        return 1
    return 1 if (args.strict and n_warn) else 0


if __name__ == "__main__":
    sys.exit(main())
