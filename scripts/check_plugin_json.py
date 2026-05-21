#!/usr/bin/env python3
"""Validate plugin.json files against the strict ClawHub schema.

Required fields (exactly these 8):
  name, description, version, author{name,url}, homepage, repository, license, skills

Two approved extension fields (documented in CLAUDE.md, stripped at ClawHub-publish):
  source, attribution

skills layouts (Claude Code tightens its path validator regularly — be explicit):
  - Single-skill plugin (SKILL.md at root):       "skills": ["./"]      (array form)
  - Plugin with skills/ subdir (CC v2.1.107-v2.1.132):
                                                   "skills": "./skills"  (WITH "./" prefix)
  - Plugin with skills/ subdir (CC v2.1.133+):    "skills": "skills"    (NO "./" prefix)
  - Multi-skill domain plugin (subfolders at root):
                                                   "skills": ["./sub1", "./sub2", ...]

CURRENT INSTALLED VERSION: CC v2.1.119 → use "./skills" form (WITH "./" prefix).

REJECTED forms and why:
  - "skills": "./"     — Claude Code v2.1.107+ rejects ("Path escapes plugin directory")
  - "skills": "skills" — Claude Code v2.1.119 rejects (prefix-less form requires v2.1.133+)

When CC is upgraded past v2.1.133:
  - Change "./skills" → "skills" in all 47 string-format plugin.json files
  - Update this docstring and _check_skills_string() below
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


def _check_skills_string(s):
    if s in ("./", ""):
        return ['skills: bare "./" is rejected by Claude Code v2.1.107+; '
                'use ["./"] (array) for single-skill at root, or "./skills" for subdir layout']
    if s == "./skills":
        # Valid for CC v2.1.107–v2.1.132. When CC v2.1.133+ is installed, drop the "./" prefix.
        return []
    if s.startswith("./"):
        return [f'skills: {s!r} starts with "./" — only "./skills" is an approved string value. '
                f'Use "./skills" for subdir layout, ["./"] for single-skill at root, '
                f'or ["./sub1", "./sub2"] for multi-skill plugins.']
    # Bare string without "./" (e.g. "skills") requires CC v2.1.133+ — rejected on v2.1.119.
    return [f'skills: {s!r} has no "./" prefix — this form requires CC v2.1.133+. '
            f'Current installed CC is v2.1.119. Use "./skills" instead.']


def _check_skills_array(s):
    if not s:
        return ["skills: array is empty"]
    errors = []
    for entry in s:
        if not isinstance(entry, str):
            errors.append(f"skills: entries must be strings, got {entry!r}")
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
    for t in targets:
        errs = validate(t)
        rel = os.path.relpath(t, REPO)
        if errs:
            failed += 1
            print(f"FAIL {rel}")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"OK   {rel}")
    if failed:
        print(f"\n{failed} file(s) failed validation", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
