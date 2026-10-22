#!/usr/bin/env python3
"""Plugin version-bump guard (gate G11).

Claude Code caches an installed plugin under its version. When a plugin's files
change but its version does not, `claude plugin update` reports "already at the
latest version" and every existing install keeps the old files forever. The
v2.14.0 audit found 70 of 104 plugins in that state (73 still at 2.9.0), so the
v2.13 and v2.14 fixes never reached anyone who had installed earlier.

This gate compares the working tree with a base ref:

  1. Every marketplace entry's `version` must equal its plugin.json `version`.
  2. Every plugin whose installed payload changed since the base must carry a
     strictly higher version than it had at the base. The payload is the whole
     `source` directory as Claude Code copies it, including files reached
     through symlinks (c-level-agents/vendor/...), so a change to a symlink
     target counts against every plugin that links to it.

New plugins (absent at the base) only need check 1.

Exit codes:
  0  clean
  1  violations (listed on stdout)
  2  usage or git error

Usage:
  python3 scripts/check_plugin_versions.py --base origin/dev
  python3 scripts/check_plugin_versions.py --base v2.14.0 --json
  python3 scripts/check_plugin_versions.py            # check 1 only (no base)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKETPLACE = ".claude-plugin/marketplace.json"
SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)")


def git(*args):
    out = subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {out.stderr.strip()}")
    return out.stdout


def parse_version(v):
    m = SEMVER.match(v or "")
    return tuple(int(x) for x in m.groups()) if m else None


def norm(source):
    return os.path.normpath(source)


def payload(source):
    """Repo-relative real paths of every file Claude Code would copy for `source`."""
    root = os.path.join(REPO_ROOT, source)
    files, seen = set(), set()
    for dirpath, dirnames, filenames in os.walk(root, followlinks=True):
        real = os.path.realpath(dirpath)
        if real in seen:
            dirnames[:] = []
            continue
        seen.add(real)
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
        for f in filenames:
            p = os.path.join(dirpath, f)
            files.add(os.path.relpath(p, REPO_ROOT))
            files.add(os.path.relpath(os.path.realpath(p), REPO_ROOT))
    return files


def base_json(base, path):
    try:
        return json.loads(git("show", f"{base}:{path}"))
    except (RuntimeError, ValueError):
        return None


def check(base):
    problems = []
    market = json.load(open(os.path.join(REPO_ROOT, MARKETPLACE)))
    plugins = market["plugins"]

    for p in plugins:
        pj = os.path.join(norm(p["source"]), ".claude-plugin", "plugin.json")
        try:
            v = json.load(open(os.path.join(REPO_ROOT, pj)))["version"]
        except (OSError, ValueError, KeyError) as exc:
            problems.append({"plugin": p["name"], "rule": "manifest", "detail": f"{pj}: {exc}"})
            continue
        if p.get("version") != v:
            problems.append({"plugin": p["name"], "rule": "sync",
                             "detail": f"marketplace.json says {p.get('version')}, {pj} says {v}"})

    if not base:
        return problems

    merge_base = git("merge-base", base, "HEAD").strip()
    changed = set(git("diff", "--name-only", "--no-renames", merge_base).split())
    changed |= set(git("ls-files", "--others", "--exclude-standard").split())
    old_market = base_json(merge_base, MARKETPLACE) or {"plugins": []}
    old_versions = {p["name"]: p.get("version") for p in old_market["plugins"]}

    for p in plugins:
        name = p["name"]
        if name not in old_versions:
            continue
        src = norm(p["source"])
        prefix = "" if src == "." else src + "/"
        files = payload(src)
        hits = sorted(c for c in changed if (c.startswith(prefix) or c in files))
        if not hits:
            continue
        old, new = parse_version(old_versions[name]), parse_version(p.get("version"))
        if old is None or new is None or new <= old:
            problems.append({
                "plugin": name, "rule": "bump",
                "detail": (f"{len(hits)} file(s) changed (e.g. {hits[0]}) but version "
                           f"{p.get('version')} is not above {old_versions[name]} at the base"),
            })
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--base", help="git ref to compare against (e.g. origin/dev); omit to check sync only")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()
    try:
        problems = check(args.base)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({"base": args.base, "problems": problems}, indent=2))
    else:
        for pr in problems:
            print(f"[{pr['rule']}] {pr['plugin']}: {pr['detail']}")
        print(f"{len(problems)} problem(s)" if problems else "plugin versions OK")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
