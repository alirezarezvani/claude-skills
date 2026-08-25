#!/usr/bin/env python3
"""primitives_inventory.py — recap every CMA primitive the founder now owns.

Reads build-sheet.json (+ optional goal.json) and prints an inventory: agent
(model, tools, skills), environment, session resources, memory stores, vaults,
outcome, deployment schedule. The close-out "here's what you own" table.
Stdlib-only; no network calls.

Examples:
  primitives_inventory.py --sheet ./my-agent/build-sheet.json
  primitives_inventory.py --sheet ./my-agent/build-sheet.json --goal ./my-agent/goal.json --json
  primitives_inventory.py --sample
"""
import argparse
import json
import sys
from pathlib import Path


def inventory(sheet, goal_state):
    prim = sheet.get("primitives", {})
    agent = prim.get("agent", {})
    env = prim.get("environment", {})
    session = prim.get("session", {})
    inv = {
        "agent_name": sheet.get("agent_name", "agent"),
        "goal": sheet.get("goal", ""),
        "agent": {
            "model": agent.get("model"),
            "tools": [t.get("type", t.get("name", "?")) for t in agent.get("tools", [])],
            "mcp_servers": [s.get("name", s.get("url", "?")) for s in agent.get("mcp_servers", [])],
            "skills": agent.get("skills", []),
            "multiagent": bool(agent.get("multiagent")),
        },
        "environment": {"type": env.get("type"), "networking": env.get("networking")},
        "session": {
            "resources": [r.get("type", "?") for r in session.get("resources", [])],
            "memory_stores": len(session.get("memory_stores", [])),
            "vaults": len(session.get("vault_ids", [])),
        },
        "outcome": bool(prim.get("outcome")),
        "deployment": prim.get("deployment", {}).get("schedule") if prim.get("deployment") else None,
        "deferrals": len(sheet.get("deferrals", [])),
    }
    if goal_state:
        inv["phase"] = goal_state.get("phase")
        inv["phases_done"] = goal_state.get("phases_done", [])
    return inv


def _emit(inv, as_json):
    if as_json:
        print(json.dumps(inv, indent=2))
        return
    print(f"=== {inv['agent_name']} — primitives owned ===")
    print(f"goal: {inv['goal']}")
    a = inv["agent"]
    print(f"agent:        model={a['model']}  tools={a['tools']}  skills={a['skills'] or '[]'}"
          + (f"  mcp={a['mcp_servers']}" if a['mcp_servers'] else "")
          + ("  multiagent=yes" if a["multiagent"] else ""))
    print(f"environment:  {inv['environment']['type']} / {inv['environment']['networking']}")
    s = inv["session"]
    print(f"session:      resources={s['resources'] or '[]'}  memory_stores={s['memory_stores']}  vaults={s['vaults']}")
    print(f"outcome:      {'yes (self-grading)' if inv['outcome'] else 'no'}")
    print(f"deployment:   {inv['deployment'] if inv['deployment'] else 'none (on-demand)'}")
    print(f"deferrals:    {inv['deferrals']} recorded")
    if "phase" in inv:
        print(f"phase:        {inv['phase']}  (done: {', '.join(inv['phases_done']) or 'none'})")


def main() -> int:
    ap = argparse.ArgumentParser(description="Recap every CMA primitive the founder owns.")
    ap.add_argument("--sheet", help="build-sheet.json.")
    ap.add_argument("--goal", help="goal.json (optional, for phase context).")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--sample", action="store_true")
    args = ap.parse_args()

    if args.sample:
        sheet = json.loads((Path(__file__).resolve().parents[3] / "assets" / "example-build-sheet.json").read_text())
        _emit(inventory(sheet, {"phase": "wrap-up", "phases_done": ["interview", "stage-launch", "grade-iterate", "run-without-you"]}), False)
        return 0

    if not args.sheet:
        print("Provide --sheet path.", file=sys.stderr)
        return 2
    sheet = json.loads(Path(args.sheet).read_text())
    goal_state = json.loads(Path(args.goal).read_text()) if args.goal and Path(args.goal).exists() else None
    _emit(inventory(sheet, goal_state), args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
