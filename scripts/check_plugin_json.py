#!/usr/bin/env python3
"""Validate plugin.json files against the ClawHub schema.

Required fields (exactly these 8):
  name, description, version, author{name,url}, homepage, repository, license, skills

Two approved extension fields (documented in CLAUDE.md, stripped at ClawHub-publish):
  source, attribution

skills layouts — per the live Claude Code plugin spec
(https://code.claude.com/docs/en/plugins-reference), "All paths must be
relative to the plugin root and start with ./". CC 2.1.145 returns
`Validation errors: skills: Invalid input` on a bare string without "./".
Legacy bare-string form is still accepted by this validator during the
migration window, but emits a WARN line.

  CANONICAL (post-CC 2.1.144):
    - Single-skill plugin (SKILL.md at root):      "skills": ["./"]
    - Plugin with skills/ subdir:                  "skills": "./skills"  (or ["./skills"])
    - Multi-skill domain plugin (subfolders):      "skills": ["./sub1", "./sub2", ...]

  LEGACY (pre-migration, still passes with WARN):
    - "skills": "skills"  (bare subdir name, no "./" prefix)

  REJECTED:
    - Empty string / empty array
    - Non-string array entries
    - Strings that are neither "skills"-style legacy nor "./"-prefixed
"""
import argparse
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED = {"name", "description", "version", "author", "homepage", "repository", "license", "skills"}
APPROVED_EXTENSIONS = {"source", "attribution"}
STRING_FIELDS = ("name", "description", "homepage", "repository", "license")
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[\w.]+)?$")


def _check_keys(data):
    keys = set(data.keys())
    errors = []
    extra = keys - ALLOWED - APPROVED_EXTENSIONS
    missing = ALLOWED - keys
    if extra:
        errors.append(f"extra fields: {sorted(extra)}")
    if missing:
        errors.append(f"missing fields: {sorted(missing)}")
    return errors


def _check_strings(data):
    return [f"{k}: must be string" for k in STRING_FIELDS if k in data and not isinstance(data[k], str)]


def _check_version(data):
    if "version" not in data:
        return []
    v = data["version"]
    if not isinstance(v, str) or not SEMVER.match(v):
        return [f"version: must match semver, got {v!r}"]
    return []


def _check_author(data):
    if "author" not in data:
        return []
    a = data["author"]
    if not isinstance(a, dict):
        return ["author: must be object {name, url}"]
    errors = []
    if not isinstance(a.get("name"), str):
        errors.append("author.name: must be string")
    if not isinstance(a.get("url"), str):
        errors.append("author.url: must be string")
    extra = set(a.keys()) - {"name", "url"}
    if extra:
        errors.append(f"author: extra fields {sorted(extra)}")
    return errors


_LEGACY_SKILLS_VALUES = {"skills"}


def _check_skills_string(s):
    if s == "":
        return ["skills: empty string"]
    if s == "./":
        return ['skills: bare "./" must be wrapped in an array — use ["./"] for single-skill plugins']
    if s.startswith("./"):
        return []
    if s in _LEGACY_SKILLS_VALUES:
        return [f'WARN skills: legacy bare {s!r} — Claude Code 2.1.144+ requires the "./" prefix '
                f'per the plugin spec. Migrate to "./{s}" or ["./{s}"].']
    return [f'skills: {s!r} must start with "./" (Claude Code plugin spec: "All paths must be '
            f'relative to the plugin root and start with ./")']


def _check_skills_array(s):
    if not s:
        return ["skills: array is empty"]
    errors = []
    for entry in s:
        if not isinstance(entry, str):
            errors.append(f"skills: entries must be strings, got {entry!r}")
            continue
        if entry == "":
            errors.append("skills: array contains empty string")
            continue
        if not entry.startswith("./"):
            errors.append(f'skills: array entry {entry!r} must start with "./" '
                          f'(Claude Code plugin spec)')
    return errors


def _check_skills(data):
    if "skills" not in data:
        return []
    s = data["skills"]
    if isinstance(s, str):
        return _check_skills_string(s)
    if isinstance(s, list):
        return _check_skills_array(s)
    return ["skills: must be string or array of strings"]


def validate(path):
    try:
        with open(path) as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        return [f"unreadable JSON: {e}"]
    return (_check_keys(data) + _check_strings(data) + _check_version(data)
            + _check_author(data) + _check_skills(data))


def find_all():
    out = []
    for root, dirs, files in os.walk(REPO):
        if any(skip in root for skip in (".git", "node_modules", "eval-workspace", ".gemini")):
            dirs[:] = []
            continue
        if "plugin.json" in files and root.endswith(".claude-plugin"):
            out.append(os.path.join(root, "plugin.json"))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("path", nargs="?", help="Path to a plugin.json file")
    g.add_argument("--all", action="store_true", help="Validate every plugin.json in the repo")
    args = ap.parse_args()

    targets = find_all() if args.all else [args.path]
    failed = 0
    warned = 0
    for t in targets:
        msgs = validate(t)
        rel = os.path.relpath(t, REPO)
        hard = [m for m in msgs if not m.startswith("WARN ")]
        soft = [m for m in msgs if m.startswith("WARN ")]
        if hard:
            failed += 1
            print(f"FAIL {rel}")
            for e in hard:
                print(f"  - {e}")
            for w in soft:
                print(f"  - {w[5:]}")
        elif soft:
            warned += 1
            print(f"WARN {rel}")
            for w in soft:
                print(f"  - {w[5:]}")
        else:
            print(f"OK   {rel}")
    if warned:
        print(f"\n{warned} file(s) passed with warnings (legacy schema)", file=sys.stderr)
    if failed:
        print(f"\n{failed} file(s) failed validation", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
