#!/usr/bin/env python3
"""verdict_reader.py — read a grader result and decide the next move.

Reads a CMA outcome result (from a saved SSE event or a JSON file you paste) and
tables the rubric outcome, then recommends the next move:
  satisfied            -> SHIP (or promote to schedule)
  needs_revision       -> SHARPEN (prompt/tools) then RE-RUN
  max_iterations_reached / failed -> ESCALATE to the founder
  interrupted          -> RESUME
Stdlib-only; no network calls.

Result JSON shape (minimal):
  {"status": "needs_revision", "iteration": 2, "max_iterations": 5,
   "rubric_results": [{"criterion": "...", "pass": true, "note": "..."}],
   "explanation": "..."}

Examples:
  verdict_reader.py --result ./my-agent/last-verdict.json
  verdict_reader.py --sample
"""
import argparse
import json
import sys
from pathlib import Path

NEXT_MOVE = {
    "satisfied": ("SHIP", "Rubric satisfied. Ship v0, or promote to a scheduled deployment (Phase 4)."),
    "needs_revision": ("SHARPEN", "Fix the failing rubric lines (prompt/tools/inputs), then re-run."),
    "max_iterations_reached": ("ESCALATE", "Cap hit without convergence. Escalate to the founder; re-scope the rubric or the tools."),
    "failed": ("ESCALATE", "Run failed. Read the explanation; likely a tool/permission/setup issue to fix before re-run."),
    "interrupted": ("RESUME", "Send a user.message to resume; checkpoints last 30 days."),
}


def read(result: dict):
    status = result.get("status", "unknown")
    move, why = NEXT_MOVE.get(status, ("INVESTIGATE", f"Unknown status '{status}'. Inspect the raw event."))
    rr = result.get("rubric_results", []) or []
    passed = [r for r in rr if r.get("pass")]
    failed = [r for r in rr if not r.get("pass")]
    it = result.get("iteration")
    mx = result.get("max_iterations")
    budget_note = None
    if it is not None and mx:
        remaining = mx - it
        budget_note = f"{it}/{mx} iterations used, {remaining} left"
        if status == "needs_revision" and remaining <= 1:
            move = "SHARPEN-OR-ESCALATE"
            why = "One iteration left — make the single highest-value fix, or escalate now rather than waste the cap."
    return {
        "status": status,
        "next_move": move,
        "why": why,
        "passed": [r.get("criterion", "?") for r in passed],
        "failed": [{"criterion": r.get("criterion", "?"), "note": r.get("note", "")} for r in failed],
        "budget": budget_note,
        "explanation": result.get("explanation", ""),
    }


def _emit(v, as_json):
    if as_json:
        print(json.dumps(v, indent=2))
        return
    print(f"STATUS: {v['status']}   NEXT MOVE: {v['next_move']}")
    print(f"  {v['why']}")
    if v.get("budget"):
        print(f"  budget: {v['budget']}")
    if v["passed"]:
        print(f"  passed ({len(v['passed'])}): " + "; ".join(v["passed"]))
    if v["failed"]:
        print(f"  FAILED ({len(v['failed'])}):")
        for f in v["failed"]:
            note = f" — {f['note']}" if f["note"] else ""
            print(f"    - {f['criterion']}{note}")
    if v["explanation"]:
        print(f"  grader: {v['explanation']}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Read a grader verdict and recommend the next move.")
    ap.add_argument("--result", help="Path to a grader result JSON.")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--sample", action="store_true")
    args = ap.parse_args()

    if args.sample:
        sample = {
            "status": "needs_revision", "iteration": 4, "max_iterations": 5,
            "rubric_results": [
                {"criterion": "Every email labeled", "pass": True},
                {"criterion": "No invented facts", "pass": False, "note": "row 7 invented an SLA"},
                {"criterion": "Urgent precision", "pass": True},
            ],
            "explanation": "Close, but one reason wasn't grounded in the email text.",
        }
        _emit(read(sample), False)
        return 0

    if not args.result:
        print("Provide --result path.", file=sys.stderr)
        return 2
    result = json.loads(Path(args.result).read_text())
    _emit(read(result), args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
