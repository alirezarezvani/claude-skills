#!/usr/bin/env python3
"""outreach_volume_guard.py — size manual outreach so it stays manual, and legal.

Three separate things restrict a LinkedIn account, and volume plans usually trip
at least one:

  1. LinkedIn enforces a weekly invitation limit (widely observed at about 100
     invitations per week; LinkedIn does not publish the exact figure and adjusts
     it per account). Pending invitations count.
  2. A low acceptance rate is itself a signal. Sustained low acceptance plus high
     volume is the pattern automated tools produce, and it is what gets reviewed.
  3. Anything that looks machine-paced — a constant per-day rate, hundreds of
     touches, identical wording — is prohibited outright by User Agreement §8.2,
     whether or not a machine actually sent it.

This tool prices the plan in minutes, checks it against the caps, and refuses the
volumes that cannot be produced by a person typing. It never sends anything.

Exit codes:
  0  SAFE       — plan fits the caps and the time budget
  2  TIGHT      — allowed, with named risks
  3  OVER       — over a cap or over the time budget; the overage is named
  4  REFUSED    — the volume is not humanly manual; this is an automation plan

Stdlib only. No network. Nothing is transmitted anywhere.
"""

import argparse
import json
import sys

WEEKLY_INVITE_LIMIT = 100      # observed LinkedIn cap; not published exactly
DAILY_MANUAL_CEILING = 25      # above this, per day, it stops being hand-written
REFUSE_DAILY = 40              # above this it is an automation plan, not a cadence
LOW_ACCEPTANCE = 0.20
MINUTES_PER_INVITE = 5         # read their work, write the specific line, send
MINUTES_PER_DM = 8


def guard(invites: int, pending: int, dms: int, minutes: int,
          acceptance: float, days_active: int) -> dict:
    findings = []
    per_day = invites / max(1, days_active)

    def add(sev, area, finding, fix):
        findings.append({"severity": sev, "area": area, "finding": finding, "fix": fix})

    verdict, code = "SAFE", 0

    if per_day > REFUSE_DAILY:
        add("refusal", "automation-pattern",
            f"{invites} invitations over {days_active} day(s) is {per_day:.0f}/day. Nobody reads "
            "that many profiles and writes that many specific lines. This is an automation plan.",
            "Cut to a volume you would actually type. If the number is the point rather than the "
            "people, the channel is wrong — that is what advertising is for.")
        verdict, code = "REFUSED", 4

    total_pipeline = invites + pending
    if total_pipeline > WEEKLY_INVITE_LIMIT:
        add("blocking", "invite-limit",
            f"{invites} new + {pending} pending = {total_pipeline} against a weekly limit observed "
            f"around {WEEKLY_INVITE_LIMIT}. LinkedIn counts pending invitations, and it does not "
            "publish the exact figure.",
            f"Withdraw invitations older than three weeks first, then send at most "
            f"{max(0, WEEKLY_INVITE_LIMIT - pending)} this week. Note that a withdrawn invitation "
            "cannot be re-sent to the same person for about three weeks.")
        if code < 3:
            verdict, code = "OVER", 3
    elif total_pipeline > WEEKLY_INVITE_LIMIT * 0.8:
        add("warning", "invite-limit",
            f"{total_pipeline} of ~{WEEKLY_INVITE_LIMIT} weekly capacity used, counting "
            f"{pending} pending.",
            "Clear stale pending invitations before the next batch.")
        if code == 0:
            verdict, code = "TIGHT", 2

    if per_day > DAILY_MANUAL_CEILING and code < 4:
        add("warning", "pacing",
            f"{per_day:.0f} invitations/day is above the {DAILY_MANUAL_CEILING} that a person "
            "can send with a genuinely specific line each.",
            "Spread it. Uneven, human pacing is also what a real person's activity looks like.")
        if code == 0:
            verdict, code = "TIGHT", 2

    if 0 < acceptance < LOW_ACCEPTANCE:
        add("blocking", "acceptance-rate",
            f"{acceptance:.0%} acceptance is below the {LOW_ACCEPTANCE:.0%} floor. Sustained low "
            "acceptance at volume is the signal LinkedIn reviews, and it also means the targeting "
            "is wrong.",
            "Stop sending. Fix who you are targeting and what the note says before resuming. "
            "Rebuild acceptance by warming up first — comment on their posts for two weeks, then "
            "send.")
        if code < 3:
            verdict, code = "OVER", 3

    time_needed = invites * MINUTES_PER_INVITE + dms * MINUTES_PER_DM
    if time_needed > minutes:
        add("blocking", "time-budget",
            f"{invites} invitations ({MINUTES_PER_INVITE} min each) plus {dms} DMs "
            f"({MINUTES_PER_DM} min each) needs {time_needed} min; the budget is {minutes} min.",
            f"Either cut to {max(0, (minutes - dms * MINUTES_PER_DM) // MINUTES_PER_INVITE)} "
            "invitations, or accept that the shortfall gets paid in generic messages — which is "
            "the same as not sending them.")
        if code < 3:
            verdict, code = "OVER", 3

    safe_weekly = min(WEEKLY_INVITE_LIMIT - pending,
                      DAILY_MANUAL_CEILING * days_active,
                      minutes // MINUTES_PER_INVITE if MINUTES_PER_INVITE else 0)
    return {
        "verdict": verdict,
        "exit_code": code,
        "plan": {"invites": invites, "pending": pending, "dms": dms,
                 "days_active": days_active, "per_day": round(per_day, 1),
                 "minutes_budget": minutes, "minutes_needed": time_needed,
                 "acceptance_rate": acceptance},
        "caps": {"weekly_invite_limit_observed": WEEKLY_INVITE_LIMIT,
                 "daily_manual_ceiling": DAILY_MANUAL_CEILING,
                 "refuse_above_per_day": REFUSE_DAILY,
                 "note": "LinkedIn does not publish the exact invitation limit and adjusts it "
                         "per account. These are conservative working numbers."},
        "safe_volume_this_week": max(0, int(safe_weekly)),
        "findings": findings,
        "standing_rules": [
            "Send by hand, one at a time. Automated sending is prohibited by User Agreement §8.2 "
            "and no volume target is worth a restricted account.",
            "Every message carries a line that could only have been written for that person.",
            "Track acceptance weekly. Falling acceptance means the targeting is wrong, not that "
            "the volume is too low.",
            "Warm before you ask: two weeks of genuine comments beats any note.",
        ],
    }


def render_human(r: dict) -> str:
    p, c = r["plan"], r["caps"]
    lines = [f"Outreach volume: {r['verdict']}", "=" * 52,
             f"Plan  : {p['invites']} invites (+{p['pending']} pending), {p['dms']} DMs over "
             f"{p['days_active']} day(s) = {p['per_day']}/day",
             f"Time  : {p['minutes_needed']} min needed / {p['minutes_budget']} min budget",
             f"Caps  : ~{c['weekly_invite_limit_observed']}/week, "
             f"{c['daily_manual_ceiling']}/day manual ceiling",
             f"Safe this week: {r['safe_volume_this_week']} invitations", ""]
    if r["findings"]:
        lines.append("Findings:")
        for f in r["findings"]:
            lines.append(f"  [{f['severity'].upper():<8}] {f['area']}: {f['finding']}")
            lines.append(f"             fix → {f['fix']}")
    else:
        lines.append("No findings.")
    lines.append("\nStanding rules:")
    for s in r["standing_rules"]:
        lines.append(f"  - {s}")
    lines.append(f"\n{c['note']}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Size manual LinkedIn outreach against the caps "
                    "(safe=0 / tight=2 / over=3 / refused=4). Nothing is sent.")
    ap.add_argument("--invites", type=int, default=0, help="New connection invitations planned.")
    ap.add_argument("--pending", type=int, default=0, help="Invitations already pending.")
    ap.add_argument("--dms", type=int, default=0, help="Direct messages planned.")
    ap.add_argument("--minutes", type=int, default=120, help="Minutes budgeted this week.")
    ap.add_argument("--acceptance", type=float, default=0.0,
                    help="Recent acceptance rate as a fraction, e.g. 0.34. 0 = unknown.")
    ap.add_argument("--days", type=int, default=5, help="Days you will spread this over.")
    ap.add_argument("--output", choices=["json", "human"], default="json")
    ap.add_argument("--sample", action="store_true", help="Run a built-in over-ambitious plan.")
    args = ap.parse_args()

    if args.sample:
        invites, pending, dms, minutes, acceptance, days = 150, 40, 20, 120, 0.14, 5
    else:
        invites, pending, dms = args.invites, args.pending, args.dms
        minutes, acceptance, days = args.minutes, args.acceptance, max(1, args.days)
        if invites == 0 and dms == 0:
            ap.error("provide --invites and/or --dms (or use --sample)")
    if not 0.0 <= acceptance <= 1.0:
        ap.error("--acceptance must be a fraction between 0 and 1")

    result = guard(invites, pending, dms, minutes, acceptance, max(1, days))
    print(json.dumps(result, indent=2) if args.output == "json" else render_human(result))
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
