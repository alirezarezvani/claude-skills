#!/usr/bin/env python3
"""Set plugin versions in plugin.json and marketplace.json together.

Companion to scripts/check_plugin_versions.py (gate G11). Use it at release
time, or when the gate reports an unbumped plugin:

  python3 scripts/bump_plugin_versions.py --to 2.14.1 --changed-since origin/dev
  python3 scripts/bump_plugin_versions.py --to 2.14.1 --all
  python3 scripts/bump_plugin_versions.py --to 2.14.1 --plugin finance-skills --dry-run

Only the `version` value is rewritten, in place, so manifest formatting and key
order survive. The marketplace `metadata.version` is left alone; it is the repo
release version and moves with the CHANGELOG.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_plugin_versions import MARKETPLACE, REPO_ROOT, SEMVER, git, payload  # noqa: E402

VERSION_VALUE = re.compile(r'("version"\s*:\s*")[^"]*(")')


def set_manifest(path, new, dry):
    text = open(path).read()
    out, n = VERSION_VALUE.subn(lambda m: m.group(1) + new + m.group(2), text, count=1)
    if n != 1:
        raise SystemExit(f"error: no version key in {path}")
    if not dry:
        open(path, "w").write(out)


def set_marketplace(names, new, dry):
    path = os.path.join(REPO_ROOT, MARKETPLACE)
    text = open(path).read()
    # Rewrite each plugin entry's version, located by its "name" key, so the
    # top-level metadata.version is never touched.
    for name in names:
        pat = re.compile(r'("name"\s*:\s*"' + re.escape(name) + r'"[^{}]*?"version"\s*:\s*")[^"]*(")', re.S)
        text, n = pat.subn(lambda m: m.group(1) + new + m.group(2), text, count=1)
        if n != 1:
            raise SystemExit(f"error: could not locate marketplace entry for {name}")
    if not dry:
        open(path, "w").write(text)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--to", required=True, help="new version, e.g. 2.14.1")
    sel = ap.add_mutually_exclusive_group(required=True)
    sel.add_argument("--all", action="store_true", help="every marketplace plugin")
    sel.add_argument("--changed-since", metavar="REF", help="plugins whose payload changed since REF")
    sel.add_argument("--plugin", action="append", help="plugin name (repeatable)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not SEMVER.match(args.to):
        raise SystemExit("error: --to must be semver")

    plugins = json.load(open(os.path.join(REPO_ROOT, MARKETPLACE)))["plugins"]
    if args.all:
        chosen = plugins
    elif args.plugin:
        chosen = [p for p in plugins if p["name"] in set(args.plugin)]
        missing = set(args.plugin) - {p["name"] for p in chosen}
        if missing:
            raise SystemExit(f"error: unknown plugin(s): {', '.join(sorted(missing))}")
    else:
        mb = git("merge-base", args.changed_since, "HEAD").strip()
        changed = set(git("diff", "--name-only", "--no-renames", mb).split())
        changed |= set(git("ls-files", "--others", "--exclude-standard").split())
        chosen = []
        for p in plugins:
            src = os.path.normpath(p["source"])
            prefix = "" if src == "." else src + "/"
            files = payload(src)
            if any(c.startswith(prefix) or c in files for c in changed):
                chosen.append(p)

    for p in chosen:
        set_manifest(os.path.join(REPO_ROOT, os.path.normpath(p["source"]), ".claude-plugin", "plugin.json"),
                     args.to, args.dry_run)
    set_marketplace([p["name"] for p in chosen], args.to, args.dry_run)
    verb = "would set" if args.dry_run else "set"
    print(f"{verb} {len(chosen)} plugin(s) to {args.to}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
