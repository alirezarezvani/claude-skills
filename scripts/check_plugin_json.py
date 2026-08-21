#!/usr/bin/env python3
"""Validate plugin.json files against the ClawHub schema.

Required fields (exactly these 8):
  name, description, version, author{name,url}, homepage, repository, license, skills

Non-spec keys are hard failures. Claude Code's manifest validator rejects the
whole plugin.json on ANY unrecognized key (issue #954 — 37+ plugins were
uninstallable because of `source` / `attribution` keys). Authoring metadata
(Path-B provenance, upstream vendoring credit) now lives in a sibling
`.claude-plugin/authoring-notes.json` file, which Claude Code never reads.
This script also sanity-checks that file when present.

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
# Formerly tolerated in-manifest; Claude Code rejects any unrecognized key
# (issue #954), so these now belong in .claude-plugin/authoring-notes.json.
RELOCATED_TO_NOTES = {"source", "attribution"}
NOTES_ALLOWED = {"source", "attribution"}
STRING_FIELDS = ("name", "description", "homepage", "repository", "license")
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[\w.]+)?$")


def _check_keys(data):
    keys = set(data.keys())
    errors = []
    relocated = keys & RELOCATED_TO_NOTES
    extra = keys - ALLOWED - RELOCATED_TO_NOTES
    missing = ALLOWED - keys
    if relocated:
        errors.append(
            f"non-spec fields {sorted(relocated)}: Claude Code rejects the whole manifest "
            f"on any unrecognized key (issue #954) — move them to "
            f".claude-plugin/authoring-notes.json"
        )
    if extra:
        errors.append(f"extra fields: {sorted(extra)}")
    if missing:
        errors.append(f"missing fields: {sorted(missing)}")
    return errors


def _check_authoring_notes(path):
    """Sanity-check the sibling authoring-notes.json, if one exists."""
    notes_path = os.path.join(os.path.dirname(path), "authoring-notes.json")
    if not os.path.exists(notes_path):
        return []
    try:
        with open(notes_path) as f:
            notes = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        return [f"authoring-notes.json: unreadable JSON: {e}"]
    if not isinstance(notes, dict):
        return ["authoring-notes.json: must be a JSON object"]
    extra = set(notes.keys()) - NOTES_ALLOWED
    if extra:
        return [f"authoring-notes.json: unexpected keys {sorted(extra)} "
                f"(allowed: {sorted(NOTES_ALLOWED)})"]
    return []


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
            + _check_author(data) + _check_skills(data) + _check_authoring_notes(path))


def find_all():
    out = []
    for root, dirs, files in os.walk(REPO):
        if any(skip in root for skip in (".git", "node_modules", "eval-workspace", ".gemini")):
            dirs[:] = []
            continue
        if "plugin.json" in files and root.endswith(".claude-plugin"):
            out.append(os.path.join(root, "plugin.json"))
    return sorted(out)


def check_marketplace_descriptions():
    """GitHub Copilot CLI rejects the whole marketplace if any plugin
    description exceeds 1024 chars (see PR #964). Guard the cap here so a
    routine description tweak can't silently re-break external loaders."""
    path = os.path.join(REPO, ".claude-plugin", "marketplace.json")
    errors = []
    try:
        with open(path) as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        return [f"marketplace.json unreadable: {e}"]
    for p in data.get("plugins", []):
        n = len(p.get("description", ""))
        if n > 1024:
            errors.append(
                f"marketplace.json: '{p.get('name', '?')}' description is "
                f"{n} chars (max 1024 — breaks Copilot CLI marketplace load)")
    return errors


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
    if args.all:
        mp_errors = check_marketplace_descriptions()
        if mp_errors:
            failed += 1
            print("FAIL .claude-plugin/marketplace.json")
            for e in mp_errors:
                print(f"  - {e}")
        else:
            print("OK   .claude-plugin/marketplace.json (all plugin descriptions <= 1024 chars)")
    if warned:
        print(f"\n{warned} file(s) passed with warnings (legacy schema)", file=sys.stderr)
    if failed:
        print(f"\n{failed} file(s) failed validation", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
