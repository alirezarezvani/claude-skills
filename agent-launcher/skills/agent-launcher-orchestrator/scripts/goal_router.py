#!/usr/bin/env python3
"""goal_router.py — deterministic router: session goal -> phase lane.

Reads the goal string (or ./my-agent/goal.json) and decides which phase skill
should run. Uses keyword scoring plus the recorded phase. Exit codes let the
orchestrator act without re-parsing prose:

  0  ROUTE  — a clear lane won; prints the lane and why.
  3  ASK    — ambiguous; prints the top candidates + one forcing question.
  4  REFUSE — goal is empty/too vague to route; prints what's missing.

Lanes: interview, stage-launch, grade-iterate, run-without-you, wrap-up.
Stdlib-only; no network calls.

Examples:
  goal_router.py --goal "grade my agent until the rubric passes"
  goal_router.py --out-dir ./my-agent --json
  goal_router.py --sample
"""
import argparse
import json
import sys
from pathlib import Path

LANES = ["interview", "stage-launch", "grade-iterate", "run-without-you", "wrap-up"]

# keyword -> lane weight
SIGNALS = {
    "interview": [
        ("what should", 2), ("scope", 2), ("plan", 2), ("requirements", 2), ("idea", 1),
        ("build sheet", 3), ("not sure what", 2), ("design the agent", 2), ("interview", 3),
    ],
    "stage-launch": [
        ("launch", 3), ("deploy it now", 2), ("stage", 2), ("payload", 3), ("create the agent", 2),
        ("first run", 2), ("kick it off", 2), ("environment", 1), ("api call", 2),
    ],
    "grade-iterate": [
        ("grade", 3), ("rubric", 3), ("iterate", 3), ("improve", 2), ("until it passes", 3),
        ("eval", 2), ("make it good", 2), ("success criteria", 2), ("outcome", 2), ("quality", 1),
    ],
    "run-without-you": [
        ("every morning", 3), ("every day", 3), ("weekly", 3), ("nightly", 3), ("schedule", 3),
        ("cron", 3), ("recurring", 3), ("without me", 2), ("run without you", 3), ("automate", 2),
        ("on a cadence", 2), ("at 9am", 2),
    ],
    "wrap-up": [
        ("wrap up", 3), ("close out", 3), ("recap", 2), ("what do i own", 2), ("summary", 1),
        ("done", 1), ("overview page", 2), ("hand off", 1),
    ],
}


def score(goal: str) -> dict:
    g = goal.lower()
    scores = {lane: 0 for lane in LANES}
    hits = {lane: [] for lane in LANES}
    for lane, kws in SIGNALS.items():
        for kw, w in kws:
            if kw in g:
                scores[lane] += w
                hits[lane].append(kw)
    return {"scores": scores, "hits": hits}


def load_goal(out_dir: Path):
    p = out_dir / "goal.json"
    if not p.exists():
        return None, None
    try:
        st = json.loads(p.read_text())
        return st.get("goal", ""), st.get("phase")
    except (json.JSONDecodeError, OSError):
        return None, None


def route(goal: str, recorded_phase):
    goal = (goal or "").strip()
    if len(goal.split()) < 3:
        return {
            "decision": "REFUSE",
            "exit": 4,
            "reason": "Goal is empty or under 3 words — too vague to route.",
            "need": "One sentence: what one job should the agent do end-to-end?",
        }
    sc = score(goal)
    scores = sc["scores"]
    ordered = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    top_lane, top = ordered[0]
    runner_lane, runner = ordered[1]

    # If nothing scored, fall back to the recorded phase, else default to interview.
    if top == 0:
        lane = recorded_phase if recorded_phase in LANES else "interview"
        return {
            "decision": "ROUTE", "exit": 0, "lane": lane,
            "reason": f"No lane keywords matched; using recorded phase '{recorded_phase}' (default interview).",
            "scores": scores,
        }

    clear = top >= 3 and (runner == 0 or top >= 2 * runner)
    if clear:
        return {
            "decision": "ROUTE", "exit": 0, "lane": top_lane,
            "reason": f"'{top_lane}' won ({top} vs {runner}) on: {', '.join(sc['hits'][top_lane])}.",
            "scores": scores,
        }
    return {
        "decision": "ASK", "exit": 3,
        "candidates": [top_lane, runner_lane],
        "reason": f"Ambiguous: {top_lane} ({top}) vs {runner_lane} ({runner}).",
        "question": f"Is this about {top_lane.replace('-', ' ')} or {runner_lane.replace('-', ' ')}?",
        "scores": scores,
    }


def _emit(result: dict, as_json: bool):
    if as_json:
        print(json.dumps(result, indent=2))
        return
    d = result["decision"]
    print(f"{d}: {result['reason']}")
    if d == "ROUTE":
        print(f"  -> lane: {result['lane']}")
    elif d == "ASK":
        print(f"  candidates: {', '.join(result['candidates'])}")
        print(f"  ask: {result['question']}")
    elif d == "REFUSE":
        print(f"  need: {result['need']}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Route a session goal to a phase lane (exit 0=route, 3=ask, 4=refuse).")
    ap.add_argument("--goal", default=None, help="Goal string. If omitted, read from goal.json.")
    ap.add_argument("--out-dir", default="./my-agent", help="Folder holding goal.json.")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--sample", action="store_true", help="Run a deterministic demo and exit.")
    args = ap.parse_args()

    if args.sample:
        for g in [
            "grade my agent until the rubric passes",
            "run the report every morning at 9am",
            "I have an idea but not sure what to build",
            "launch it now with the payloads",
            "make it better",  # ambiguous-ish
            "go",  # refuse
        ]:
            r = route(g, None)
            print(f"[{r['decision']:6}] {g!r} -> {r.get('lane') or r.get('candidates') or r.get('need')}")
        return 0

    goal = args.goal
    recorded_phase = None
    if goal is None:
        goal, recorded_phase = load_goal(Path(args.out_dir))
        if goal is None:
            print("No --goal given and no goal.json found.", file=sys.stderr)
            return 4
    result = route(goal, recorded_phase)
    _emit(result, args.json)
    return result["exit"]


if __name__ == "__main__":
    raise SystemExit(main())
