#!/usr/bin/env python3
"""upgrade_suggester.py — suggest the next 1-2 upgrades for a launched agent.

Ranks the build sheet's deferrals (v1 before v2, real-integration before
nice-to-have) and adds standing hardening suggestions (tighten networking, pin the
agent version in the deployment, nest an outcome if a schedule lacks one). Prints
the top 1-2 with the exact mechanism. Stdlib-only; no network calls.

Examples:
  upgrade_suggester.py --sheet ./my-agent/build-sheet.json
  upgrade_suggester.py --sheet ./my-agent/build-sheet.json --top 2 --json
  upgrade_suggester.py --sample
"""
import argparse
import json
import sys
from pathlib import Path


def suggest(sheet):
    prim = sheet.get("primitives", {})
    env = prim.get("environment", {})
    candidates = []

    # 1) recorded deferrals, v1 first
    for d in sorted(sheet.get("deferrals", []) or [], key=lambda x: x.get("version", "v9")):
        weight = 100 if d.get("version") == "v1" else 60
        if any(w in (d.get("item", "") + d.get("mechanism", "")).lower() for w in ("mcp", "real", "integration")):
            weight += 10
        candidates.append({"weight": weight, "title": f"{d.get('version','v?')} — {d.get('item','')}",
                           "why": d.get("reason", ""), "mechanism": d.get("mechanism", "")})

    # 2) standing hardening moves
    if env.get("networking", "unrestricted") == "unrestricted":
        candidates.append({"weight": 55, "title": "Harden networking to 'limited'",
                           "why": "unrestricted egress is broader than needed",
                           "mechanism": "Set environment networking to 'limited' with an explicit allowed_hosts list."})
    if prim.get("deployment") and not prim.get("outcome"):
        candidates.append({"weight": 70, "title": "Nest a self-grading outcome in the schedule",
                           "why": "each firing should self-grade",
                           "mechanism": "Add user.define_outcome to the deployment's initial_events (--nest-outcome)."})
    if prim.get("deployment"):
        candidates.append({"weight": 50, "title": "Pin the agent version in the deployment",
                           "why": "avoid a config change silently altering scheduled runs",
                           "mechanism": "Set agent {type:agent,id,version:N} in the deployment payload once a version passes."})
    if not prim.get("outcome"):
        candidates.append({"weight": 65, "title": "Add an outcome rubric (grade→iterate)",
                           "why": "no self-grading defined yet",
                           "mechanism": "Run grade-iterate/outcome_builder.py to add a rubric + max_iterations."})

    candidates.sort(key=lambda c: c["weight"], reverse=True)
    return candidates


def main() -> int:
    ap = argparse.ArgumentParser(description="Suggest the next 1-2 upgrades for a launched agent.")
    ap.add_argument("--sheet", help="build-sheet.json.")
    ap.add_argument("--top", type=int, default=2)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--sample", action="store_true")
    args = ap.parse_args()

    if args.sample:
        sheet = json.loads((Path(__file__).resolve().parents[3] / "assets" / "example-build-sheet.json").read_text())
        cands = suggest(sheet)[:2]
        for i, c in enumerate(cands, 1):
            print(f"{i}. {c['title']}\n   why: {c['why']}\n   how: {c['mechanism']}")
        return 0

    if not args.sheet:
        print("Provide --sheet path.", file=sys.stderr)
        return 2
    sheet = json.loads(Path(args.sheet).read_text())
    cands = suggest(sheet)[: max(1, args.top)]
    if args.json:
        print(json.dumps(cands, indent=2))
    else:
        for i, c in enumerate(cands, 1):
            print(f"{i}. {c['title']}\n   why: {c['why']}\n   how: {c['mechanism']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
