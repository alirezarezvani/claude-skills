#!/usr/bin/env python3
"""eval_scaffold.py — generate a held-back eval scaffold + a parallel-run plan.

Once a version passes the in-loop rubric, run held-back cases (that the agent
never saw during iteration) to check it generalizes. This tool emits an eval
scaffold JSON (cases + expected + a per-case kickoff message) and a parallel-run
plan describing how to fan the cases across sessions. Stdlib-only; no network.

Examples:
  eval_scaffold.py --sheet ./my-agent/build-sheet.json --out ./my-agent/eval.json
  eval_scaffold.py --cases cases.json --concurrency 5
  eval_scaffold.py --sample
"""
import argparse
import json
import sys
from pathlib import Path


def scaffold(agent_name, goal, rubric, cases, concurrency):
    eval_cases = []
    for i, c in enumerate(cases):
        cid = c.get("id") or f"case-{i+1}"
        eval_cases.append({
            "id": cid,
            "input": c.get("input", ""),
            "expected": {k: v for k, v in c.items() if k not in ("id", "input")},
            "kickoff": {"events": [{"type": "user.message", "content": c.get("input", "")}]},
            "grade_against_rubric": True,
        })
    plan = {
        "eval_version": "eval.v1",
        "agent_name": agent_name,
        "goal": goal,
        "rubric": rubric,
        "cases": eval_cases,
        "run_plan": {
            "mode": "parallel",
            "concurrency": max(1, min(int(concurrency), 25)),  # CMA <=25 concurrent threads
            "note": "Each case is an independent session; grade each against the same rubric. "
                    "Cap concurrency at 25 (CMA thread ceiling). Run only AFTER a version passes the in-loop rubric.",
            "pass_condition": "All held-back cases satisfied (or an explicit, recorded exception).",
        },
    }
    return plan


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate a held-back eval scaffold + parallel-run plan.")
    ap.add_argument("--sheet", help="build-sheet.json (reads eval_plan.held_back_cases + rubric).")
    ap.add_argument("--cases", help="JSON file: a list of {id,input,...expected} objects.")
    ap.add_argument("--concurrency", default=5)
    ap.add_argument("--out", help="Write the eval scaffold here.")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--sample", action="store_true")
    args = ap.parse_args()

    if args.sample:
        sheet = json.loads((Path(__file__).resolve().parents[3] / "assets" / "example-build-sheet.json").read_text())
        cases = sheet.get("eval_plan", {}).get("held_back_cases", [])
        rubric = sheet.get("primitives", {}).get("outcome", {}).get("rubric", "")
        plan = scaffold(sheet["agent_name"], sheet["goal"], rubric, cases, 5)
        print(json.dumps(plan, indent=2))
        return 0

    agent_name, goal, rubric = "agent", "", ""
    cases = []
    if args.sheet:
        sheet = json.loads(Path(args.sheet).read_text())
        agent_name = sheet.get("agent_name", "agent")
        goal = sheet.get("goal", "")
        rubric = sheet.get("primitives", {}).get("outcome", {}).get("rubric", "")
        cases = sheet.get("eval_plan", {}).get("held_back_cases", [])
    if args.cases:
        cases = json.loads(Path(args.cases).read_text())
    if not cases:
        print("No held-back cases found (provide --cases or a sheet with eval_plan.held_back_cases).", file=sys.stderr)
        return 1

    plan = scaffold(agent_name, goal, rubric, cases, args.concurrency)
    text = json.dumps(plan, indent=2)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text + "\n")
        print(f"Wrote {args.out} ({len(cases)} cases, concurrency {plan['run_plan']['concurrency']})")
    if args.json or not args.out:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
