#!/usr/bin/env python3
"""Check a new hire's first 90 days against their plan: missed checkpoints, overdue milestones, a lapsed buddy.

Input: a JSON ramp log (the plan's milestones plus what happened):

  {
    "hire": "A. Rivera", "start_date": "2026-12-07", "horizon_days": 90,
    "milestones": [
      {"phase": 30, "outcome": "Ship a small bug fix", "done_on": "2026-12-18"},
      {"phase": 60, "outcome": "On-call shadow week", "done_on": null}
    ],
    "meetings": [
      {"date": "2026-12-07", "type": "manager"},
      {"date": "2026-12-09", "type": "buddy"},
      {"date": "2027-01-06", "type": "checkpoint"}
    ]
  }

Meeting types: manager (1:1), buddy, checkpoint (the day-30/60/90 review).

Findings, judged on --today:
  CHECKPOINT_MISSED  a day-30/60/90 checkpoint is past due by more than
                     --grace days and no checkpoint meeting was held within
                     --grace days of it
  MILESTONE_OVERDUE  a milestone's phase has ended and it has no done_on
  BUDDY_LAPSED       fewer buddy meetings than half the weekly pace so far,
                     or none in the first 10 days
  MANAGER_GAP        more than 14 days between manager 1:1s (or since the
                     last one)
  NO_CHECKPOINT_BEFORE_OVERDUE  a milestone went overdue with no checkpoint
                     held in its phase: the plan was never reviewed, so ask
                     what blocked it before judging the hire

Verdict:
  ON_TRACK   no findings
  AT_RISK    one overdue milestone, or a missed checkpoint, a lapsed buddy or
             a manager gap
  OFF_TRACK  two or more overdue milestones, or an overdue milestone plus a
             missed checkpoint

The verdict is about the onboarding, not the person. It never says pass or
fail probation: that decision belongs to the manager and HR, with the
hire's own account of what got in the way.

Exit codes: 0 ON_TRACK, 2 AT_RISK, 3 bad input, 4 OFF_TRACK.
Deterministic, stdlib only, no network.
"""
import argparse
import datetime as dt
import json
import sys

EXIT = {"ON_TRACK": 0, "AT_RISK": 2, "BAD_INPUT": 3, "OFF_TRACK": 4}
TYPES = {"manager", "buddy", "checkpoint"}
NOTE = ("This reads the onboarding, not the person. A probation or performance decision belongs to the "
        "manager and HR, with the hire's own account of what got in the way.")

SAMPLE = {
    "hire": "A. Rivera", "start_date": "2026-12-07", "horizon_days": 90,
    "milestones": [
        {"phase": 30, "outcome": "Ship a small bug fix to production", "done_on": "2026-12-18"},
        {"phase": 30, "outcome": "Map the billing services in a one-page diagram", "done_on": None},
        {"phase": 60, "outcome": "Own the billing-export on-call shadow week", "done_on": None},
        {"phase": 90, "outcome": "Lead the invoice-retry feature", "done_on": None},
    ],
    "meetings": [
        {"date": "2026-12-07", "type": "manager"}, {"date": "2026-12-07", "type": "buddy"},
        {"date": "2026-12-14", "type": "manager"}, {"date": "2026-12-16", "type": "buddy"},
        {"date": "2026-12-21", "type": "manager"}, {"date": "2027-01-11", "type": "manager"},
        {"date": "2027-01-18", "type": "manager"},
    ],
}


def parse_date(s, field):
    try:
        return dt.date.fromisoformat(str(s))
    except ValueError:
        raise ValueError(f"{field} must be YYYY-MM-DD, got {s!r}")


def check(spec, today, grace):
    if not isinstance(spec, dict):
        raise ValueError("input must be a JSON object")
    start = parse_date(spec.get("start_date"), "start_date")
    horizon = spec.get("horizon_days", 90)
    if not isinstance(horizon, int) or horizon < 30:
        raise ValueError("horizon_days must be a whole number >= 30")
    if today < start:
        raise ValueError(f"--today {today} is before the start date {start}: run preboarding_gate.py instead")
    day = (today - start).days + 1
    phases = list(range(30, horizon + 1, 30))

    meetings = []
    for i, m in enumerate(spec.get("meetings") or []):
        if not isinstance(m, dict) or str(m.get("type", "")).lower() not in TYPES:
            raise ValueError(f"meeting {i}: type must be one of {sorted(TYPES)}")
        d = parse_date(m.get("date"), f"meeting {i} date")
        if d <= today:
            meetings.append((d, m["type"].lower()))
    meetings.sort()

    findings = []
    checkpoints = [d for d, t in meetings if t == "checkpoint"]
    cp_rows = []
    for ph in phases:
        due = start + dt.timedelta(days=ph - 1)
        held = next((d for d in checkpoints if abs((d - due).days) <= grace), None)
        if held:
            state = "HELD"
        elif (today - due).days > grace:
            state = "MISSED"
            findings.append({"code": "CHECKPOINT_MISSED", "msg": f"Day-{ph} checkpoint (due {due}) was not held."})
        else:
            state = "UPCOMING"
        cp_rows.append({"day": ph, "due": due.isoformat(), "state": state, "held_on": held.isoformat() if held else None})

    ms_rows, overdue = [], 0
    for i, m in enumerate(spec.get("milestones") or []):
        if not isinstance(m, dict) or not m.get("outcome"):
            raise ValueError(f"milestone {i}: needs 'phase' and 'outcome'")
        ph = m.get("phase")
        if ph not in phases:
            raise ValueError(f"milestone {i}: phase must be one of {phases}")
        due = start + dt.timedelta(days=ph - 1)
        done = parse_date(m["done_on"], f"milestone {i} done_on") if m.get("done_on") else None
        if done and done <= today:
            state = "DONE" if done <= due else "DONE_LATE"
        elif today > due:
            state = "OVERDUE"
            overdue += 1
            findings.append({"code": "MILESTONE_OVERDUE", "msg": f"Day {ph}: '{m['outcome']}' was due {due}, not done."})
            phase_start = start + dt.timedelta(days=ph - 30)
            if not any(phase_start <= d <= due + dt.timedelta(days=grace) for d in checkpoints):
                findings.append({"code": "NO_CHECKPOINT_BEFORE_OVERDUE",
                                 "msg": f"Day {ph}: no checkpoint was held in this phase, so nobody reviewed '{m['outcome']}' "
                                        "before it slipped. Ask what blocked it before judging the hire."})
        else:
            state = "OPEN"
        ms_rows.append({"phase": ph, "outcome": m["outcome"], "due": due.isoformat(),
                        "done_on": done.isoformat() if done else None, "state": state})

    buddy = [d for d, t in meetings if t == "buddy"]
    expected = max(1, min(day, horizon) // 7)
    if day > 10 and not any(d <= start + dt.timedelta(days=9) for d in buddy):
        findings.append({"code": "BUDDY_LAPSED", "msg": "No buddy meeting in the first 10 days."})
    elif len(buddy) < expected / 2:
        findings.append({"code": "BUDDY_LAPSED",
                         "msg": f"{len(buddy)} buddy meetings by day {day}; weekly pace is {expected}. "
                                "Microsoft's buddy pilot found the benefit rose with each meeting band up to more than 8 in 90 days."})

    mgr = [d for d, t in meetings if t == "manager"]
    gap_from = [start] + mgr
    gaps = [(b - a).days for a, b in zip(gap_from, mgr + [today])]
    worst = max(gaps) if gaps else (today - start).days
    if worst > 14:
        findings.append({"code": "MANAGER_GAP", "msg": f"Longest stretch without a manager 1:1: {worst} days (limit 14)."})

    missed = any(f["code"] == "CHECKPOINT_MISSED" for f in findings)
    if overdue >= 2 or (overdue and missed):
        verdict = "OFF_TRACK"
    elif findings:
        verdict = "AT_RISK"
    else:
        verdict = "ON_TRACK"
    return {"hire": spec.get("hire", ""), "start_date": start.isoformat(), "today": today.isoformat(), "day": day,
            "verdict": verdict, "checkpoints": cp_rows, "milestones": ms_rows,
            "meetings": {"manager": len(mgr), "buddy": len(buddy), "checkpoint": len(checkpoints)},
            "findings": findings, "note": NOTE, "defaults": {"grace_days": grace, "manager_gap_days": 14}}


def render(r):
    out = [f"Ramp check: {r['hire'] or 'new hire'}, day {r['day']} (started {r['start_date']}, judged {r['today']})",
           f"VERDICT: {r['verdict']}", "", "Checkpoints:"]
    out += [f"  day {c['day']:>3}  due {c['due']}  {c['state']}" + (f" ({c['held_on']})" if c["held_on"] else "")
            for c in r["checkpoints"]]
    out.append("Milestones:")
    out += [f"  {m['state']:9} day {m['phase']:>3}  {m['outcome']}" for m in r["milestones"]]
    mt = r["meetings"]
    out.append(f"Meetings so far: {mt['manager']} manager 1:1s, {mt['buddy']} buddy, {mt['checkpoint']} checkpoints")
    if r["findings"]:
        out.append("")
        out += [f"{f['code']}: {f['msg']}" for f in r["findings"]]
    out += ["", r["note"], f"Defaults: checkpoint grace {r['defaults']['grace_days']} days, manager gap limit 14 days."]
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 epilog="Exit codes: 0 ON_TRACK, 2 AT_RISK, 3 bad input, 4 OFF_TRACK.")
    ap.add_argument("--log", help="ramp log JSON (start_date, milestones with done_on, meetings)")
    ap.add_argument("--today", help="date to judge from, YYYY-MM-DD (default: today)")
    ap.add_argument("--grace", type=int, default=5, help="days a checkpoint may move and still count as held (default 5)")
    ap.add_argument("--sample", action="store_true", help="run on a built-in log (today = 2027-01-20)")
    ap.add_argument("--output", "--format", choices=["text", "json"], default="text")
    a = ap.parse_args(argv)
    try:
        if a.sample:
            spec, today = SAMPLE, dt.date(2027, 1, 20)
        elif a.log:
            with open(a.log, encoding="utf-8") as f:
                spec = json.load(f)
            today = dt.date.today()
        else:
            raise ValueError("give --log FILE or --sample")
        if a.today:
            today = parse_date(a.today, "--today")
        res = check(spec, today, a.grace)
    except (ValueError, OSError, json.JSONDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return EXIT["BAD_INPUT"]
    print(json.dumps(res, indent=2) if a.output == "json" else render(res))
    return EXIT[res["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
