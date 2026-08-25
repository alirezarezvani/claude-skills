#!/usr/bin/env python3
"""loop_compiler.py — compile a goal + phase into an execution shape (plan.v1).

Turns "what are we doing and where are we" into exactly one of three shapes:

  single-pass  — interview -> plan -> stage -> launch (Phases 1-2)
  grade-iterate — CMA user.define_outcome self-grading, BOUNDED by max_iterations
  cron-loop    — recurring scheduled deployment ("run without you")

A grade-iterate loop is NEVER emitted without a max_iterations cap (1..20). A
cron-loop may nest an outcome so each firing self-grades. Stdlib-only.

Examples:
  loop_compiler.py --phase grade-iterate --max-iterations 5
  loop_compiler.py --phase run-without-you --cron "0 9 * * *" --timezone Europe/Berlin --nest-outcome
  loop_compiler.py --out-dir ./my-agent          # read phase from goal.json
  loop_compiler.py --sample
"""
import argparse
import json
import sys
from pathlib import Path

MAX_ITER_CEILING = 20
MAX_ITER_DEFAULT = 3

PHASE_TO_SHAPE = {
    "interview": "single-pass",
    "stage-launch": "single-pass",
    "grade-iterate": "grade-iterate",
    "run-without-you": "cron-loop",
    "wrap-up": "single-pass",
    "done": "single-pass",
}

SINGLE_PASS_STEPS = ["interview", "plan", "validate", "stage", "launch"]


def clamp_iters(n) -> int:
    try:
        n = int(n)
    except (TypeError, ValueError):
        n = MAX_ITER_DEFAULT
    return max(1, min(MAX_ITER_CEILING, n))


def compile_plan(phase, max_iterations, cron, timezone, event, nest_outcome):
    shape = PHASE_TO_SHAPE.get(phase, "single-pass")

    # run-without-you can be recurring (cron), event-driven, or on-demand.
    if phase == "run-without-you":
        if cron:
            shape = "cron-loop"
        elif event:
            shape = "event-driven"
        else:
            shape = "on-demand"

    plan = {"plan_version": "plan.v1", "phase": phase, "shape": shape}

    if shape == "single-pass":
        plan["terminal_state"] = "a live session produced its first output"
        plan["steps"] = SINGLE_PASS_STEPS
        plan["repeats"] = False
    elif shape == "grade-iterate":
        cap = clamp_iters(max_iterations)
        plan["repeats"] = True
        plan["bounded"] = True
        plan["max_iterations"] = cap
        plan["mechanism"] = "user.define_outcome (isolated grader) -> verdict -> next attempt"
        plan["terminal_states"] = ["satisfied", "max_iterations_reached", "failed", "interrupted"]
        plan["loop_invariant"] = "each iteration moves >=1 rubric line fail->pass or the run halts"
        plan["next_moves"] = ["sharpen prompt/tools", "re-run as-is", "promote to schedule"]
    elif shape == "cron-loop":
        plan["repeats"] = True
        plan["bounded"] = False
        plan["mechanism"] = "POST /v1/deployments schedule.cron -> a session per firing (drun_)"
        plan["schedule"] = {"expression": cron, "timezone": timezone or "UTC"}
        plan["safety"] = ["always_ask MCP", "limited networking", "read_only memory where possible",
                          "max_iterations per firing", "workspace spend limit", "test with manual run first"]
        plan["terminal_state"] = "none by design; runs until paused/archived"
        if nest_outcome:
            plan["nested_outcome"] = {"bounded": True, "max_iterations": clamp_iters(max_iterations),
                                      "note": "each firing self-grades before finishing"}
    elif shape == "event-driven":
        plan["repeats"] = True
        plan["bounded"] = False
        plan["mechanism"] = "documented curl to send user.message on your event (not scheduled)"
        plan["event"] = event
    elif shape == "on-demand":
        plan["repeats"] = False
        plan["mechanism"] = "no deployment; send user.message when you ask"

    # warnings
    warnings = []
    if shape == "cron-loop" and not cron:
        warnings.append("cron-loop selected but no --cron expression given; schedule is a placeholder")
    if shape == "grade-iterate" and max_iterations and int_or_none(max_iterations) and int(max_iterations) > MAX_ITER_CEILING:
        warnings.append(f"max_iterations clamped to {MAX_ITER_CEILING} (CMA ceiling)")
    plan["warnings"] = warnings
    return plan


def int_or_none(v):
    try:
        int(v)
        return True
    except (TypeError, ValueError):
        return False


def load_phase(out_dir: Path):
    p = out_dir / "goal.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text()).get("phase")
    except (json.JSONDecodeError, OSError):
        return None


def _emit(plan: dict, as_json: bool):
    if as_json:
        print(json.dumps(plan, indent=2))
        return
    print(f"shape: {plan['shape']}  (phase={plan['phase']})")
    if plan.get("bounded") is True:
        print(f"  bounded loop, max_iterations={plan.get('max_iterations')}")
    if plan.get("bounded") is False:
        print("  unbounded (safety rails required)")
    if "schedule" in plan:
        print(f"  schedule: {plan['schedule']['expression']} [{plan['schedule']['timezone']}]")
    if "nested_outcome" in plan:
        print(f"  nested outcome: each firing self-grades (max_iterations={plan['nested_outcome']['max_iterations']})")
    if plan.get("steps"):
        print(f"  steps: {' -> '.join(plan['steps'])}")
    print(f"  mechanism: {plan.get('mechanism','-')}")
    for w in plan.get("warnings", []):
        print(f"  WARN: {w}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Compile a goal+phase into an execution shape (single-pass / grade-iterate / cron-loop).")
    ap.add_argument("--phase", default=None, help="One of interview, stage-launch, grade-iterate, run-without-you, wrap-up.")
    ap.add_argument("--out-dir", default="./my-agent", help="Read phase from goal.json when --phase omitted.")
    ap.add_argument("--max-iterations", default=MAX_ITER_DEFAULT, help="Grade-loop cap (clamped 1..20).")
    ap.add_argument("--cron", default=None, help="5-field POSIX cron expression (run-without-you).")
    ap.add_argument("--timezone", default=None, help="IANA timezone for the schedule.")
    ap.add_argument("--event", default=None, help="Event description for an event-driven trigger.")
    ap.add_argument("--nest-outcome", action="store_true", help="Nest a self-grading outcome inside each cron firing.")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--sample", action="store_true", help="Run a deterministic demo and exit.")
    args = ap.parse_args()

    if args.sample:
        for kw in [
            dict(phase="interview"),
            dict(phase="grade-iterate", max_iterations=99),
            dict(phase="run-without-you", cron="0 9 * * *", timezone="Europe/Berlin", nest_outcome=True),
            dict(phase="run-without-you"),
        ]:
            plan = compile_plan(kw.get("phase"), kw.get("max_iterations", 3), kw.get("cron"),
                                kw.get("timezone"), kw.get("event"), kw.get("nest_outcome", False))
            print(f"--- {kw} ---")
            _emit(plan, False)
        return 0

    phase = args.phase or load_phase(Path(args.out_dir))
    if not phase:
        print("No --phase given and no goal.json phase found.", file=sys.stderr)
        return 2
    plan = compile_plan(phase, args.max_iterations, args.cron, args.timezone, args.event, args.nest_outcome)
    _emit(plan, args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
