#!/usr/bin/env python3
"""build_sheet_builder.py — assemble/normalize a build-sheet.json for a CMA.

Takes an interview_planner.py plan (or a partial sheet) and produces a normalized
build-sheet.json under ./my-agent/. Fills defaults, orders keys, and strips the
planner's private _notes into a top-level "loop_hint". Stdlib-only.

Examples:
  interview_planner.py --sample > /tmp/plan.json
  build_sheet_builder.py --plan /tmp/plan.json --out-dir ./my-agent
  build_sheet_builder.py --sample
"""
import argparse
import json
import sys
from pathlib import Path

REQUIRED = ("agent_name", "goal", "primitives")


def build(plan: dict) -> dict:
    notes = plan.pop("_notes", {}) if isinstance(plan, dict) else {}
    sheet = {
        "agent_name": plan.get("agent_name", "agent"),
        "goal": plan.get("goal", ""),
        "primitives": plan.get("primitives", {}),
        "deferrals": plan.get("deferrals", []),
        "eval_plan": plan.get("eval_plan", {"success_criteria": [], "held_back_cases": []}),
    }
    # ensure agent + environment exist
    prim = sheet["primitives"]
    prim.setdefault("agent", {"model": "claude-opus-5", "tools": [{"type": "agent_toolset_20260401"}]})
    prim["agent"].setdefault("model", "claude-opus-5")
    prim.setdefault("environment", {"type": "cloud", "networking": "unrestricted", "packages": {}})
    if notes.get("loop_hint"):
        sheet["loop_hint"] = notes["loop_hint"]
    return sheet


def missing(sheet: dict):
    miss = [k for k in REQUIRED if not sheet.get(k)]
    if not sheet.get("goal"):
        miss.append("goal(empty)")
    if "agent" not in sheet.get("primitives", {}):
        miss.append("primitives.agent")
    return sorted(set(miss))


def main() -> int:
    ap = argparse.ArgumentParser(description="Assemble a normalized build-sheet.json from a planner plan.")
    ap.add_argument("--plan", help="Path to an interview_planner.py plan JSON.")
    ap.add_argument("--out-dir", default="./my-agent")
    ap.add_argument("--stdout", action="store_true", help="Print instead of writing to disk.")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--sample", action="store_true")
    args = ap.parse_args()

    if args.sample:
        sample_plan = {
            "agent_name": "support-triage",
            "goal": "Triage overnight support email.",
            "primitives": {"agent": {"model": "claude-opus-5", "tools": [{"type": "agent_toolset_20260401"}]},
                           "environment": {"type": "cloud", "networking": "unrestricted", "packages": {}}},
            "deferrals": [{"version": "v1", "item": "Real Gmail MCP", "reason": "no cred", "mechanism": "register vault"}],
            "eval_plan": {"success_criteria": ["all labeled"], "held_back_cases": []},
            "_notes": {"loop_hint": "cron-loop"},
        }
        sheet = build(sample_plan)
        print(json.dumps(sheet, indent=2))
        print(f"\nmissing: {missing(sheet) or 'none'}", file=sys.stderr)
        return 0

    if not args.plan:
        print("Provide --plan (an interview_planner.py plan).", file=sys.stderr)
        return 2
    plan = json.loads(Path(args.plan).read_text())
    sheet = build(plan)
    miss = missing(sheet)
    text = json.dumps(sheet, indent=2)
    if args.stdout or args.json:
        print(text)
    else:
        out_dir = Path(args.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        dest = out_dir / "build-sheet.json"
        dest.write_text(text + "\n")
        print(f"Wrote {dest}")
    if miss:
        print(f"WARN missing/empty: {', '.join(miss)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
