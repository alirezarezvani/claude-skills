#!/usr/bin/env python3
"""Skill-listing budget guard (gate G12).

Claude Code puts the name and description of every model-invocable skill and
command into one listing, capped at about 1% of the context window (30,000
characters for Sonnet on Claude Code 2.1.314). Past the cap it drops
descriptions, starting with the least-used skills, and a skill listed by name
only rarely fires. The skill-doctor audit of 2026-10-30 measured the whole
marketplace at 7.8x that budget.

This gate measures what each marketplace plugin adds to the listing:

  - every SKILL.md the plugin's `skills` paths reach, counted as
    name + description (description capped at 1,536 characters, as Claude Code does);
  - every command under the plugin's `commands/` that the model can invoke
    (no `disable-model-invocation: true`).

Ratchet: a plugin may not grow past its line in scripts/listing_budget_baseline.txt,
and a plugin with no line may not exceed --new-plugin-cap. Shrinking is always
fine; regenerate the baseline after a reduction so it cannot grow back.

Exit codes:
  0  clean
  1  a plugin grew past its baseline or a new plugin is over the cap
  2  usage error

Usage:
  python3 scripts/check_listing_budget.py                     # check
  python3 scripts/check_listing_budget.py --report            # per-plugin table
  python3 scripts/check_listing_budget.py --update-baseline   # after shrinking
"""
import argparse
import glob
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE = os.path.join(REPO, "scripts", "listing_budget_baseline.txt")
MAX_DESC = 1536
LISTING_BUDGET = 30000

sys.path.insert(0, os.path.join(REPO, "engineering", "write-a-skill", "skills", "write-a-skill", "scripts"))
from _skill_frontmatter import extract_frontmatter  # noqa: E402


def _entry_chars(path):
    fm = extract_frontmatter(open(path, encoding="utf-8").read())
    name = fm.get("name", "").strip("\"'") or os.path.basename(os.path.dirname(path))
    desc = fm.get("description", "").strip("\"'")
    return len(name) + 2 + min(len(desc), MAX_DESC), fm


def plugin_listing(root, manifest):
    """(entries, chars) the plugin adds to the model's listing."""
    skills = manifest.get("skills", [])
    if isinstance(skills, str):
        skills = [skills]
    seen, entries, chars = set(), 0, 0
    for rel in skills:
        base = os.path.normpath(os.path.join(root, rel))
        for sm in sorted(glob.glob(os.path.join(base, "SKILL.md")) + glob.glob(os.path.join(base, "*", "SKILL.md"))):
            real = os.path.realpath(sm)
            if real in seen:
                continue
            seen.add(real)
            c, fm = _entry_chars(sm)
            if str(fm.get("disable-model-invocation", "")).lower() == "true":
                continue
            entries += 1
            chars += c
    for cmd in sorted(glob.glob(os.path.join(root, "commands", "*.md"))):
        c, fm = _entry_chars(cmd)
        if str(fm.get("disable-model-invocation", "")).lower() == "true":
            continue
        entries += 1
        chars += c
    return entries, chars


def measure():
    market = json.load(open(os.path.join(REPO, ".claude-plugin", "marketplace.json")))
    out = {}
    for p in market["plugins"]:
        root = os.path.normpath(os.path.join(REPO, p["source"]))
        manifest = json.load(open(os.path.join(root, ".claude-plugin", "plugin.json")))
        out[p["name"]] = plugin_listing(root, manifest)
    return out


def load_baseline():
    base = {}
    if os.path.exists(BASELINE):
        for line in open(BASELINE):
            if line.strip() and not line.startswith("#"):
                name, chars = line.split()
                base[name] = int(chars)
    return base


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--report", action="store_true", help="print a per-plugin table, largest first")
    ap.add_argument("--update-baseline", action="store_true", help="rewrite the baseline from the tree")
    ap.add_argument("--new-plugin-cap", type=int, default=6000, help="max chars for a plugin with no baseline line (default 6000)")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args()

    sizes = measure()
    total = sum(c for _, c in sizes.values())

    if args.update_baseline:
        with open(BASELINE, "w") as f:
            f.write("# Gate G12 ratchet: listing characters each plugin adds (skills + model-invocable commands).\n"
                    "# A plugin may shrink, never grow past its line. Regenerate after a reduction:\n"
                    "#   python3 scripts/check_listing_budget.py --update-baseline\n")
            for name in sorted(sizes):
                f.write(f"{name} {sizes[name][1]}\n")
        print(f"baseline written: {len(sizes)} plugins, {total} chars")
        return 0

    base = load_baseline()
    problems = []
    for name, (_, chars) in sorted(sizes.items()):
        if name in base and chars > base[name]:
            problems.append(f"{name}: {chars} chars, baseline {base[name]} (+{chars - base[name]})")
        elif name not in base and chars > args.new_plugin_cap:
            problems.append(f"{name}: new plugin adds {chars} chars, cap {args.new_plugin_cap}")

    if args.json:
        print(json.dumps({"total_chars": total, "budget": LISTING_BUDGET, "plugins": {k: {"entries": e, "chars": c} for k, (e, c) in sizes.items()}, "problems": problems}, indent=2))
    else:
        if args.report:
            print(f"{'plugin':40s} {'entries':>7s} {'chars':>7s}")
            for name, (e, c) in sorted(sizes.items(), key=lambda x: -x[1][1]):
                print(f"{name:40s} {e:7d} {c:7d}")
        print(f"G12: {len(sizes)} plugins add {total} listing chars ({total / LISTING_BUDGET:.1f}x the {LISTING_BUDGET} budget if all are installed)")
        for p in problems:
            print(f"  GREW  {p}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
