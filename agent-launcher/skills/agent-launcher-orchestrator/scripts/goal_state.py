#!/usr/bin/env python3
"""goal_state.py — read/write/advance the per-session goal file (./my-agent/goal.json).

The goal is the through-line of a CMA launch that spans multiple sessions. This
tool owns goal.json: init a new goal, set fields, print status, or advance to the
next phase. Stdlib-only; no network calls.

Phases (in order): interview -> stage-launch -> grade-iterate -> run-without-you
-> wrap-up -> done.

Examples:
  goal_state.py init --goal "Triage my inbox every morning" --agent-name inbox-triage
  goal_state.py set --phase grade-iterate --note "v0 = triage only"
  goal_state.py status --json
  goal_state.py advance
  goal_state.py --sample
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

PHASES = ["interview", "stage-launch", "grade-iterate", "run-without-you", "wrap-up", "done"]
DEFAULT_DIR = Path("./my-agent")
FILENAME = "goal.json"


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def _path(out_dir: Path) -> Path:
    return out_dir / FILENAME


def _load(out_dir: Path) -> dict:
    p = _path(out_dir)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def _save(out_dir: Path, state: dict) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = _now()
    p = _path(out_dir)
    p.write_text(json.dumps(state, indent=2) + "\n")
    return p


def _new_state(goal: str, agent_name: str) -> dict:
    return {
        "goal": goal,
        "agent_name": agent_name,
        "phase": "interview",
        "phases_done": [],
        "loop": None,
        "artifacts": {},
        "notes": "",
        "updated_at": _now(),
    }


def cmd_init(args) -> int:
    out_dir = Path(args.out_dir)
    if _path(out_dir).exists() and not args.force:
        print(f"goal.json already exists at {_path(out_dir)} (use --force to overwrite)", file=sys.stderr)
        return 1
    state = _new_state(args.goal, args.agent_name or _slug(args.goal))
    p = _save(out_dir, state)
    _emit(state, args.json, f"Initialized goal at {p}")
    return 0


def cmd_set(args) -> int:
    out_dir = Path(args.out_dir)
    state = _load(out_dir)
    if not state:
        print("No goal.json found. Run `init` first.", file=sys.stderr)
        return 1
    if args.goal is not None:
        state["goal"] = args.goal
    if args.agent_name is not None:
        state["agent_name"] = args.agent_name
    if args.phase is not None:
        if args.phase not in PHASES:
            print(f"Unknown phase '{args.phase}'. One of: {', '.join(PHASES)}", file=sys.stderr)
            return 2
        state["phase"] = args.phase
    if args.note is not None:
        state["notes"] = args.note
    if args.artifact:
        state.setdefault("artifacts", {})
        for kv in args.artifact:
            if "=" not in kv:
                print(f"--artifact expects key=value, got '{kv}'", file=sys.stderr)
                return 2
            k, v = kv.split("=", 1)
            state["artifacts"][k] = v
    p = _save(out_dir, state)
    _emit(state, args.json, f"Updated {p}")
    return 0


def cmd_status(args) -> int:
    state = _load(Path(args.out_dir))
    if not state:
        print("No goal set. Run `goal_state.py init --goal \"...\"`.", file=sys.stderr)
        return 1
    _emit(state, args.json, None)
    return 0


def cmd_advance(args) -> int:
    out_dir = Path(args.out_dir)
    state = _load(out_dir)
    if not state:
        print("No goal.json found. Run `init` first.", file=sys.stderr)
        return 1
    cur = state.get("phase", "interview")
    if cur == "done":
        _emit(state, args.json, "Already at 'done'.")
        return 0
    idx = PHASES.index(cur) if cur in PHASES else 0
    state.setdefault("phases_done", [])
    if cur not in state["phases_done"] and cur != "done":
        state["phases_done"].append(cur)
    state["phase"] = PHASES[min(idx + 1, len(PHASES) - 1)]
    p = _save(out_dir, state)
    _emit(state, args.json, f"Advanced {cur} -> {state['phase']} ({p})")
    return 0


def _slug(text: str) -> str:
    s = "".join(c.lower() if c.isalnum() else "-" for c in text).strip("-")
    while "--" in s:
        s = s.replace("--", "-")
    return (s[:40] or "agent").strip("-")


def _emit(state: dict, as_json: bool, msg) -> None:
    if as_json:
        print(json.dumps(state, indent=2))
        return
    if msg:
        print(msg)
    print(f"  goal:        {state.get('goal','')}")
    print(f"  agent_name:  {state.get('agent_name','')}")
    print(f"  phase:       {state.get('phase','')}")
    done = state.get("phases_done") or []
    print(f"  phases_done: {', '.join(done) if done else '(none)'}")
    loop = state.get("loop")
    if loop:
        print(f"  loop:        {loop.get('shape','?')} (max_iterations={loop.get('max_iterations','-')})")
    if state.get("notes"):
        print(f"  notes:       {state['notes']}")


def _sample() -> int:
    import tempfile
    d = Path(tempfile.mkdtemp(prefix="al-goal-"))
    st = _new_state("Triage my support inbox every morning", "support-triage")
    _save(d, st)
    print("SAMPLE: initialized goal, then advanced twice")
    s = _load(d)
    _emit(s, False, None)
    # advance twice
    for _ in range(2):
        cur = s["phase"]
        s.setdefault("phases_done", [])
        if cur not in s["phases_done"]:
            s["phases_done"].append(cur)
        s["phase"] = PHASES[min(PHASES.index(cur) + 1, len(PHASES) - 1)]
    _save(d, s)
    print("\nafter two advances:")
    _emit(s, False, None)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Read/write/advance the per-session CMA launch goal (./my-agent/goal.json).")
    ap.add_argument("--sample", action="store_true", help="Run a deterministic demo and exit.")
    sub = ap.add_subparsers(dest="cmd")

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--out-dir", default=str(DEFAULT_DIR), help="Folder holding goal.json (default ./my-agent).")
    common.add_argument("--json", action="store_true", help="Emit the full state as JSON.")

    p_init = sub.add_parser("init", parents=[common], help="Create a new goal.json.")
    p_init.add_argument("--goal", required=True, help="One-sentence job the agent does.")
    p_init.add_argument("--agent-name", default=None, help="Short name (default: slug of the goal).")
    p_init.add_argument("--force", action="store_true", help="Overwrite an existing goal.json.")
    p_init.set_defaults(func=cmd_init)

    p_set = sub.add_parser("set", parents=[common], help="Update goal fields.")
    p_set.add_argument("--goal", default=None)
    p_set.add_argument("--agent-name", default=None)
    p_set.add_argument("--phase", default=None, help=f"One of: {', '.join(PHASES)}")
    p_set.add_argument("--note", default=None)
    p_set.add_argument("--artifact", action="append", help="key=value artifact path (repeatable).")
    p_set.set_defaults(func=cmd_set)

    p_status = sub.add_parser("status", parents=[common], help="Print the current goal + phase.")
    p_status.set_defaults(func=cmd_status)

    p_adv = sub.add_parser("advance", parents=[common], help="Move to the next phase.")
    p_adv.set_defaults(func=cmd_advance)

    args = ap.parse_args()
    if args.sample:
        return _sample()
    if not getattr(args, "cmd", None):
        ap.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
