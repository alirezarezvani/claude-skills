#!/usr/bin/env python3
"""meeting_cost_calculator.py — Price a meeting in real dollars and gate whether it should exist.

The `meetings` skill's first discipline: a meeting is a purchase. This script prices it
(attendees x minutes x hourly rate, optionally + a 23-minute refocus overhead per attendee,
per Gloria Mark's interruption-recovery research) and then applies the should-this-exist gate:

  1. Is there a DECISION to make?      (--has-decision)  -> without one, it's a status update
  2. Is there an AGENDA?               (--has-agenda)    -> without one, nobody can prepare
  3. Is there a named meeting OWNER?   (--has-owner)     -> without one, nobody is accountable

Verdicts:
  ASYNC      — no decision needed. Send a memo/thread instead. The cheapest meeting is no meeting.
  NOT-READY  — a decision exists but the agenda and/or owner is missing (named explicitly).
  MEET       — decision + agenda + owner all present. Cost printed, plus a cost-per-minute line
               so agenda timeboxes get budgeted like money.

NO LLM CALLS. Pure arithmetic + thresholds. Stdlib only. Never sends or schedules anything.

Usage:
    python meeting_cost_calculator.py --attendees 6 --minutes 60 --avg-rate 90 \
        --include-refocus --has-decision --has-agenda --has-owner
    python meeting_cost_calculator.py --attendees 8 --minutes 30            # no decision -> ASYNC
    python meeting_cost_calculator.py --sample
    python meeting_cost_calculator.py --sample --json
"""

import argparse
import json
import sys
from typing import Any, Dict, List

REFOCUS_MINUTES = 23  # avg time to refocus after a context switch (Gloria Mark, UC Irvine)

EPILOG = """\
exit codes:
  0   MEET      — decision + agenda + owner present; cost printed
  1   usage error — bad or missing flags (never a verdict)
  2   ASYNC     — no decision needed; recommend a memo/thread instead of a meeting
  3   NOT-READY — decision exists but agenda and/or owner missing (named in output)

--help and --sample always exit per the verdict rules above (--sample is a MEET scenario, exit 0).
"""


def evaluate(attendees: int, minutes: int, avg_rate: float, include_refocus: bool,
             has_decision: bool, has_agenda: bool, has_owner: bool) -> Dict[str, Any]:
    direct_cost = round(attendees * (minutes / 60.0) * avg_rate, 2)
    refocus_cost = round(attendees * (REFOCUS_MINUTES / 60.0) * avg_rate, 2) if include_refocus else 0.0
    total_cost = round(direct_cost + refocus_cost, 2)
    cost_per_minute = round(total_cost / minutes, 2) if minutes else 0.0

    missing: List[str] = []
    if not has_agenda:
        missing.append("agenda")
    if not has_owner:
        missing.append("meeting owner")

    if not has_decision:
        verdict, exit_code = "ASYNC", 2
        headline = (
            "No decision to make -> this is a status update, not a meeting. "
            f"Send it as a memo/thread and save the ${total_cost:,.2f}. "
            "The cheapest meeting is the one you don't hold."
        )
    elif missing:
        verdict, exit_code = "NOT-READY", 3
        headline = (
            "A decision exists, but the meeting is not ready to be called. "
            f"Missing: {' and '.join(missing)}. "
            "Fix that, re-run the gate, and only then send the invite."
        )
    else:
        verdict, exit_code = "MEET", 0
        headline = (
            "Gate passed: decision + agenda + owner. This meeting has earned its slot. "
            f"It costs ${total_cost:,.2f} — budget the agenda timeboxes like money."
        )

    return {
        "inputs": {
            "attendees": attendees,
            "minutes": minutes,
            "avg_rate_per_hour": avg_rate,
            "include_refocus": include_refocus,
            "has_decision": has_decision,
            "has_agenda": has_agenda,
            "has_owner": has_owner,
        },
        "direct_cost": direct_cost,
        "refocus_cost": refocus_cost,
        "refocus_minutes_per_attendee": REFOCUS_MINUTES if include_refocus else 0,
        "total_cost": total_cost,
        "cost_per_minute": cost_per_minute,
        "missing": missing,
        "verdict": verdict,
        "exit_code": exit_code,
        "headline": headline,
    }


def render_human(r: Dict[str, Any]) -> str:
    i = r["inputs"]
    out: List[str] = []
    out.append("Meeting Cost Gate (should this meeting exist?)")
    out.append("=" * 64)
    out.append(f"  Attendees: {i['attendees']}   Length: {i['minutes']} min   "
               f"Rate: ${i['avg_rate_per_hour']:,.0f}/hr")
    out.append(f"  Direct cost:  ${r['direct_cost']:>10,.2f}   "
               f"({i['attendees']} x {i['minutes']} min x ${i['avg_rate_per_hour']:,.0f}/hr)")
    if i["include_refocus"]:
        out.append(f"  Refocus cost: ${r['refocus_cost']:>10,.2f}   "
                   f"({REFOCUS_MINUTES} min refocus overhead per attendee)")
    out.append(f"  TOTAL COST:   ${r['total_cost']:>10,.2f}")
    out.append("")
    out.append(f"  Gate: decision={'yes' if i['has_decision'] else 'NO'} | "
               f"agenda={'yes' if i['has_agenda'] else 'NO'} | "
               f"owner={'yes' if i['has_owner'] else 'NO'}")
    out.append("")
    out.append(f"  VERDICT: {r['verdict']}")
    out.append(f"  {r['headline']}")
    if r["verdict"] == "MEET":
        out.append("")
        out.append(f"  Every minute of this meeting costs ${r['cost_per_minute']:,.2f} — "
                   "price each agenda topic's timebox against that.")
    return "\n".join(out)


SAMPLE = dict(attendees=6, minutes=60, avg_rate=90.0, include_refocus=True,
              has_decision=True, has_agenda=True, has_owner=True)


def main(argv: List[str]) -> int:
    p = argparse.ArgumentParser(
        description="Price a meeting and gate whether it should exist (ASYNC / NOT-READY / MEET).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=EPILOG,
    )
    p.add_argument("--attendees", type=int, help="Number of attendees")
    p.add_argument("--minutes", type=int, help="Scheduled meeting length in minutes")
    p.add_argument("--avg-rate", type=float, default=90.0,
                   help="Average fully-loaded hourly rate per attendee in dollars (default: 90)")
    p.add_argument("--include-refocus", action="store_true",
                   help=f"Add a {REFOCUS_MINUTES}-minute refocus overhead per attendee to the cost")
    p.add_argument("--has-decision", action="store_true",
                   help="A specific decision will be made in this meeting")
    p.add_argument("--has-agenda", action="store_true",
                   help="A timeboxed agenda with desired outcomes exists")
    p.add_argument("--has-owner", action="store_true",
                   help="A named meeting owner is accountable for outcome + follow-through")
    p.add_argument("--sample", action="store_true", help="Run the embedded sample (a MEET scenario)")
    p.add_argument("--json", action="store_true", help="Emit machine-readable JSON instead of text")
    args = p.parse_args(argv)

    if args.sample:
        vals = dict(SAMPLE)
    elif args.attendees is not None and args.minutes is not None:
        if args.attendees < 1 or args.minutes < 1:
            print("error: --attendees and --minutes must both be >= 1", file=sys.stderr)
            return 1
        vals = dict(attendees=args.attendees, minutes=args.minutes, avg_rate=args.avg_rate,
                    include_refocus=args.include_refocus, has_decision=args.has_decision,
                    has_agenda=args.has_agenda, has_owner=args.has_owner)
    else:
        p.print_help()
        print("\nerror: provide --attendees and --minutes, or --sample", file=sys.stderr)
        return 1

    result = evaluate(**vals)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render_human(result))
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
