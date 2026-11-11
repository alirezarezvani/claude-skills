#!/usr/bin/env python3
"""Check the skill-router hooks shipped by plugins.

Every plugin that ships hooks/skill_router.py must:
  1. carry a byte-identical copy of the canonical script (engineering-team/hooks/skill_router.py),
  2. have a hooks/skill_routes.json whose "plugin" equals its plugin.json name,
  3. route only to skills that exist in that plugin, with regexes that compile,
  4. register the router under UserPromptSubmit in hooks/hooks.json.

With --cases FILE it also prints, per routed skill, how many of the file's positive
prompts get a hint and how many hints land on near-miss prompts (a measurement, not a gate).

Exit 0 when clean, 1 on any finding.
"""
from __future__ import annotations

import argparse
import filecmp
import glob
import importlib.util
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, "engineering-team", "hooks", "skill_router.py")


def plugin_skills(root, manifest):
    skills = manifest.get("skills", [])
    skills = [skills] if isinstance(skills, str) else skills
    names = set()
    for entry in skills:
        base = os.path.normpath(os.path.join(root, entry))
        for f in glob.glob(os.path.join(base, "**", "SKILL.md"), recursive=True):
            names.add(os.path.basename(os.path.dirname(f)))
    return names


def check(root, problems):
    rel = os.path.relpath(root, REPO)
    script = os.path.join(root, "hooks", "skill_router.py")
    routes_path = os.path.join(root, "hooks", "skill_routes.json")
    hooks_path = os.path.join(root, "hooks", "hooks.json")
    if not filecmp.cmp(script, CANON, shallow=False):
        problems.append(f"{rel}: hooks/skill_router.py differs from {os.path.relpath(CANON, REPO)}")
    try:
        manifest = json.load(open(os.path.join(root, ".claude-plugin", "plugin.json")))
        cfg = json.load(open(routes_path))
    except (OSError, ValueError) as e:
        problems.append(f"{rel}: {e}")
        return
    if cfg.get("plugin") != manifest.get("name"):
        problems.append(f"{rel}: skill_routes.json plugin {cfg.get('plugin')!r} != plugin.json name {manifest.get('name')!r}")
    have = plugin_skills(root, manifest)
    for r in cfg.get("routes", []):
        if r.get("skill") not in have:
            problems.append(f"{rel}: route to {r.get('skill')!r}, which this plugin does not ship")
        if not r.get("why"):
            problems.append(f"{rel}: route {r.get('skill')!r} has no 'why'")
        pats = list(r.get("any", [])) + list(r.get("not", []))
        for a, b in r.get("pairs", []):
            pats += list(a) + list(b)
        if not (r.get("any") or r.get("pairs")):
            problems.append(f"{rel}: route {r.get('skill')!r} has no patterns")
        for p in pats:
            try:
                re.compile(p, re.I)
            except re.error as e:
                problems.append(f"{rel}: route {r.get('skill')!r} bad regex {p!r}: {e}")
    try:
        hooks = json.load(open(hooks_path)).get("hooks", {})
    except (OSError, ValueError) as e:
        problems.append(f"{rel}: hooks/hooks.json: {e}")
        return
    cmds = [h.get("command", "") for m in hooks.get("UserPromptSubmit", []) for h in m.get("hooks", [])]
    if not any("${CLAUDE_PLUGIN_ROOT}/hooks/skill_router.py" in c for c in cmds):
        problems.append(f"{rel}: hooks.json does not register skill_router.py under UserPromptSubmit")


def measure(roots, cases_file):
    spec = importlib.util.spec_from_file_location("skill_router", CANON)
    sr = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sr)
    routers = [sr.load_routes(os.path.join(r, "hooks", "skill_routes.json")) for r in roots]
    targets = {r["skill"] for _, rs in routers for r in rs}
    cases = json.load(open(cases_file))

    def hints(p):
        return [r["skill"] for _, rs in routers for r in [sr.best_route(rs, p)] if r]

    hit = tot = near = 0
    for c in cases.values():
        if c["name"] in targets:
            for p in c["pos"]:
                tot += 1
                hit += c["name"] in hints(p)
            negs = c["neg"] if isinstance(c["neg"], list) else [c["neg"]]
            near += sum(1 for p in negs if c["name"] in hints(p))
    print(f"{cases_file}: hints on {hit}/{tot} positive prompts, {near} on the routed skills' own near misses")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cases", help="trigger cases JSON to measure the routes against")
    args = ap.parse_args()
    roots = sorted({os.path.dirname(os.path.dirname(p)) for p in
                    glob.glob(os.path.join(REPO, "**", "hooks", "skill_router.py"), recursive=True)
                    if "/." not in os.path.relpath(p, REPO)})
    problems = []
    for root in roots:
        check(root, problems)
    for p in problems:
        print("FAIL", p)
    print(f"skill router: {len(roots)} plugins checked, {len(problems)} problems")
    if args.cases:
        measure(roots, args.cases)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
