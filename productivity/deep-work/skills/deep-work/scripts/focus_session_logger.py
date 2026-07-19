#!/usr/bin/env python3
"""focus_session_logger.py — JSON-backed focus-session log: deep hours this week, streaks, targets.

You cannot improve a deep-work practice you do not measure. This script keeps a tiny local
ledger of focus sessions and answers two questions:

  status  — how many deep hours this week (ISO week, Mon-Sun) vs --target (default 15)?
  streak  — how many consecutive days (ending today, with a one-day grace) have at least
            one logged session?

Subcommands:
  log     --minutes N --label X [--date YYYY-MM-DD]   append one focus session
  status  [--target HOURS] [--date YYYY-MM-DD]        this week's deep hours vs target
  streak  [--date YYYY-MM-DD]                         consecutive-day streak

State lives in a single JSON file (--state, default ~/.deep-work/sessions.json), created on
demand. Writes are atomic (tmp file + os.replace) so a crash never corrupts the ledger.
The top-level --sample flag prints a canned status report WITHOUT touching disk.

NO LLM CALLS. Stdlib only. Deterministic given the same state file and --date.

Exit codes:
  0  success (log appended / report printed)
  1  usage error, bad date, or unreadable/corrupt state file

Usage:
    python focus_session_logger.py log --minutes 90 --label "Write product spec"
    python focus_session_logger.py status --target 15
    python focus_session_logger.py streak
    python focus_session_logger.py --sample
"""

import argparse
import datetime as dt
import json
import os
import sys
import tempfile
from typing import Any, Dict, List, Tuple

DEFAULT_STATE = os.path.join(os.path.expanduser("~"), ".deep-work", "sessions.json")
DEFAULT_TARGET_HOURS = 15.0


def parse_date(value: str, flag: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"{flag} must be YYYY-MM-DD, got: {value!r}")


def load_state(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {"sessions": []}
    try:
        with open(path, "r", encoding="utf-8") as f:
            state = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read state file {path}: {exc}")
    if not isinstance(state, dict) or not isinstance(state.get("sessions"), list):
        raise ValueError(f"state file {path} is not a valid session ledger")
    return state


def save_state(path: str, state: Dict[str, Any]) -> None:
    """Atomic write: temp file in the same directory, then os.replace."""
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".sessions-", suffix=".tmp", dir=directory)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
            f.write("\n")
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def week_bounds(day: dt.date) -> Tuple[dt.date, dt.date]:
    monday = day - dt.timedelta(days=day.weekday())
    return monday, monday + dt.timedelta(days=6)


def cmd_log(state: Dict[str, Any], minutes: int, label: str, day: dt.date) -> Dict[str, Any]:
    state["sessions"].append({"date": day.isoformat(), "minutes": minutes, "label": label})
    total_today = sum(s["minutes"] for s in state["sessions"] if s["date"] == day.isoformat())
    return {"logged": {"date": day.isoformat(), "minutes": minutes, "label": label},
            "sessions_total": len(state["sessions"]),
            "minutes_today": total_today}


def cmd_status(state: Dict[str, Any], target_hours: float, day: dt.date) -> Dict[str, Any]:
    monday, sunday = week_bounds(day)
    week = [s for s in state["sessions"]
            if monday.isoformat() <= s["date"] <= sunday.isoformat()]
    minutes = sum(s["minutes"] for s in week)
    hours = round(minutes / 60.0, 2)
    by_day: Dict[str, int] = {}
    for s in week:
        by_day[s["date"]] = by_day.get(s["date"], 0) + s["minutes"]
    remaining = round(max(0.0, target_hours - hours), 2)
    on_track = hours >= target_hours
    return {
        "week": f"{monday.isoformat()} .. {sunday.isoformat()}",
        "as_of": day.isoformat(),
        "sessions_this_week": len(week),
        "deep_hours_this_week": hours,
        "target_hours": target_hours,
        "remaining_hours": remaining,
        "on_track": on_track,
        "by_day_minutes": dict(sorted(by_day.items())),
        "headline": (f"{hours}h of deep work this week vs a {target_hours:g}h target — "
                     + ("target met. Protect the streak."
                        if on_track else f"{remaining}h still to block.")),
    }


def cmd_streak(state: Dict[str, Any], day: dt.date) -> Dict[str, Any]:
    days = {s["date"] for s in state["sessions"]}
    cursor = day
    if cursor.isoformat() not in days:          # one-day grace: today not logged yet
        cursor = cursor - dt.timedelta(days=1)
    streak = 0
    while cursor.isoformat() in days:
        streak += 1
        cursor = cursor - dt.timedelta(days=1)
    return {
        "as_of": day.isoformat(),
        "streak_days": streak,
        "headline": (f"{streak} consecutive day(s) with at least one focus session."
                     if streak else "No active streak — one 90-minute block today starts it."),
    }


def render_human(kind: str, r: Dict[str, Any]) -> str:
    out: List[str] = []
    if kind == "log":
        s = r["logged"]
        out.append(f"Logged: {s['minutes']} min — \"{s['label']}\" on {s['date']}")
        out.append(f"  Today so far: {r['minutes_today']} min · Ledger total: {r['sessions_total']} session(s)")
    elif kind == "status":
        out.append(f"Deep-Work Status — week {r['week']} (as of {r['as_of']})")
        out.append("=" * 64)
        tail = "ON TRACK" if r["on_track"] else f"{r['remaining_hours']}h remaining"
        out.append(f"  Deep hours: {r['deep_hours_this_week']}h / {r['target_hours']:g}h target   ({tail})")
        for d, m in r["by_day_minutes"].items():
            out.append(f"    {d}: {m} min")
        out.append(f"  {r['headline']}")
    else:  # streak
        out.append(f"Deep-Work Streak (as of {r['as_of']})")
        out.append("=" * 64)
        out.append(f"  {r['headline']}")
    return "\n".join(out)


SAMPLE_STATUS = {
    "kind": "status",
    "sample": True,
    "week": "2026-07-13 .. 2026-07-19",
    "as_of": "2026-07-16",
    "deep_hours_this_week": 8.5,
    "target_hours": 15.0,
    "on_track": False,
    "remaining_hours": 6.5,
    "by_day_minutes": {"2026-07-13": 120, "2026-07-14": 180,
                       "2026-07-15": 90, "2026-07-16": 120},
    "streak_days": 4,
    "headline": "8.5h of deep work this week vs a 15h target — 6.5h still to block.",
}

SAMPLE_REPORT = """Deep-Work Status — week 2026-07-13 .. 2026-07-19 (sample, no disk touched)
================================================================
  Deep hours: 8.5h / 15h target   (6.5h remaining)
    2026-07-13: 120 min
    2026-07-14: 180 min
    2026-07-15: 90 min
    2026-07-16: 120 min
  8.5h of deep work this week vs a 15h target — 6.5h still to block.
  Streak: 4 consecutive day(s) with at least one focus session."""


def main(argv: List[str]) -> int:
    p = argparse.ArgumentParser(
        description="JSON-backed focus-session log: deep hours this week, streaks, targets.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=("Exit codes:\n"
                "  0  success (log appended / report printed)\n"
                "  1  usage error, bad date, or unreadable/corrupt state file"),
    )
    p.add_argument("--state", default=DEFAULT_STATE,
                   help=f"Path to the JSON ledger (default {DEFAULT_STATE})")
    p.add_argument("--sample", action="store_true",
                   help="Print a canned status report without touching disk")
    p.add_argument("--json", action="store_true",
                   help="Emit JSON instead of the report (also honored with --sample)")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="Emit JSON instead of the report")
    sub = p.add_subparsers(dest="cmd")

    p_log = sub.add_parser("log", help="Append one focus session", parents=[common])
    p_log.add_argument("--minutes", type=int, required=True, help="Session length in minutes")
    p_log.add_argument("--label", default="deep work", help="What the session was spent on")
    p_log.add_argument("--date", help="Session date YYYY-MM-DD (default today)")

    p_status = sub.add_parser("status", help="This week's deep hours vs target", parents=[common])
    p_status.add_argument("--target", type=float, default=DEFAULT_TARGET_HOURS,
                          help=f"Weekly deep-hours target (default {DEFAULT_TARGET_HOURS:g})")
    p_status.add_argument("--date", help="As-of date YYYY-MM-DD (default today)")

    p_streak = sub.add_parser("streak", help="Consecutive days with at least one session", parents=[common])
    p_streak.add_argument("--date", help="As-of date YYYY-MM-DD (default today)")

    args = p.parse_args(argv)

    if args.sample:
        if args.json:
            print(json.dumps(SAMPLE_STATUS, indent=2))
        else:
            print(SAMPLE_REPORT)
        return 0
    if not args.cmd:
        p.print_help()
        print("\nerror: a subcommand is required (log / status / streak) or --sample",
              file=sys.stderr)
        return 1

    try:
        day = parse_date(args.date, "--date") if getattr(args, "date", None) else dt.date.today()
        state = load_state(args.state)
        if args.cmd == "log":
            if args.minutes <= 0:
                raise ValueError("--minutes must be a positive integer")
            result = cmd_log(state, args.minutes, args.label, day)
            save_state(args.state, state)
        elif args.cmd == "status":
            result = cmd_status(state, args.target, day)
        else:
            result = cmd_streak(state, day)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render_human(args.cmd, result))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
