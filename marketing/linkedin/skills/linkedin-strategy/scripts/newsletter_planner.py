#!/usr/bin/env python3
"""newsletter_planner.py — gate a LinkedIn newsletter, then lay out its first arc.

A LinkedIn newsletter notifies every subscriber on every issue. That is a standing
promise about cadence and topic, and it is the reason most of them are abandoned
after four issues: the promise was made against a month the author happened to
have free.

This tool gates the promise before it is made:

  ELIGIBILITY  LinkedIn evaluates access for members and Pages with more than 150
               followers and/or connections, among other criteria it does not
               publish in full. Below that, the answer is "not yet".
  SUSTAINABILITY  Cadence x issue cost, checked against a six-month horizon rather
               than a good week. Six months is the horizon because that is roughly
               when a newsletter starts to have a returning readership.
  SHAPE        Issues mapped across the declared pillars with rotating issue types,
               so the arc is not twelve variations of the same essay.
  STOP RULE    The condition under which you slow down or end it, written before
               issue one, when it is still a decision rather than a defeat.

Exit codes:
  0  green — eligible, sustainable, arc emitted
  2  eligible but thin (named risks; proceed knowingly)
  3  refused — not eligible yet, or the cadence cannot be sustained

Stdlib only. No network. Deterministic.
"""

import argparse
import json
import sys

ELIGIBILITY_FLOOR = 150      # LinkedIn Help: newsletters evaluated above 150 followers/connections
THIN_AUDIENCE = 500
ISSUE_MINUTES_DEFAULT = 150
HORIZON_MONTHS = 6

CADENCES = {
    "weekly": {"issues_per_month": 4.3, "label": "Weekly"},
    "biweekly": {"issues_per_month": 2.15, "label": "Every two weeks"},
    "monthly": {"issues_per_month": 1.0, "label": "Monthly"},
}

# Rotating issue shapes so the arc does not become twelve identical essays.
ISSUE_TYPES = [
    ("framework", "A repeatable way to make one decision. The issue people forward."),
    ("teardown", "One real artifact examined in public — with permission, or anonymised."),
    ("field-note", "What you actually did this fortnight, including what failed."),
    ("counter-take", "The received wisdom in your field, and where it breaks."),
    ("reader-question", "One question a reader asked, answered at length."),
    ("roundup", "What you read and what changed your mind. Cheapest issue to produce — "
                "keep one in reserve for a bad month."),
]

SAMPLE = {
    "followers": 1800,
    "cadence": "biweekly",
    "minutes_per_month": 420,
    "issue_minutes": 150,
    "pillars": ["Trust debt in analytics", "dbt and modelling decisions",
                "Hiring the first analytics engineer"],
    "issues": 12,
}


def build(followers: int, cadence: str, minutes_per_month: int, issue_minutes: int,
          pillars: list, issues: int) -> dict:
    findings = []
    spec = CADENCES[cadence]

    if followers < ELIGIBILITY_FLOOR:
        return {
            "verdict": "NOT_ELIGIBLE",
            "exit_code": 3,
            "followers": followers,
            "floor": ELIGIBILITY_FLOOR,
            "finding": f"{followers} followers/connections. LinkedIn evaluates newsletter access "
                       f"above {ELIGIBILITY_FLOOR}, and applies further criteria it does not "
                       "publish in full.",
            "instead": "Publish the same material as regular posts on the same day each week. "
                       "It builds the audience the newsletter will need, and it costs less to "
                       "abandon if the topic turns out to be wrong.",
            "recheck_at": ELIGIBILITY_FLOOR,
        }

    if followers < THIN_AUDIENCE:
        findings.append({
            "severity": "warning", "area": "audience",
            "finding": f"{followers} followers. Eligible, but a newsletter to a small list has a "
                       "high abandonment rate — the feedback is too sparse to tell you whether "
                       "the topic is right.",
            "fix": "Consider running the format as posts for another quarter. The newsletter "
                   "converts better when there is already an audience asking for the next one.",
        })

    monthly_cost = spec["issues_per_month"] * issue_minutes
    sustainable = monthly_cost <= minutes_per_month
    if not sustainable:
        affordable = [c for c, s in CADENCES.items()
                      if s["issues_per_month"] * issue_minutes <= minutes_per_month]
        return {
            "verdict": "UNSUSTAINABLE",
            "exit_code": 3,
            "cadence": cadence,
            "monthly_cost_minutes": round(monthly_cost),
            "monthly_budget_minutes": minutes_per_month,
            "horizon_months": HORIZON_MONTHS,
            "finding": f"{spec['label']} at {issue_minutes} min/issue costs about "
                       f"{round(monthly_cost)} min/month against a {minutes_per_month}-min budget. "
                       f"Over {HORIZON_MONTHS} months that is a "
                       f"{round(monthly_cost * HORIZON_MONTHS)}-minute commitment you cannot pay.",
            "instead": (f"Drop to {', '.join(affordable)}." if affordable else
                        "Cut the issue cost — a 60-minute field-note format is a real newsletter; "
                        "a 150-minute essay you skip is not."),
            "rule": "Cadence is the promise. Missing it is more damaging than never having made it, "
                    "because subscribers opted in to a frequency.",
        }

    headroom = round((minutes_per_month - monthly_cost) / minutes_per_month * 100)
    if headroom < 20:
        findings.append({
            "severity": "warning", "area": "sustainability",
            "finding": f"Only {headroom}% headroom. One busy month breaks the cadence.",
            "fix": "Bank two issues before launching, and keep the roundup format in reserve as "
                   "the low-cost issue for a bad month.",
        })

    pillars = [p for p in pillars if str(p).strip()] or ["(no pillars declared)"]
    if pillars == ["(no pillars declared)"]:
        findings.append({
            "severity": "warning", "area": "shape",
            "finding": "No pillars declared, so the arc cannot be balanced against your positioning.",
            "fix": "Run positioning_brief.py first. A newsletter with no pillars drifts within "
                   "three issues.",
        })

    arc = []
    for i in range(issues):
        # Offset the pillar cycle by the type cycle so pillar/type pairs do not
        # repeat in lockstep every LCM(pillars, types) issues.
        pillar = pillars[(i + i // len(ISSUE_TYPES)) % len(pillars)]
        itype, why = ISSUE_TYPES[i % len(ISSUE_TYPES)]
        arc.append({"issue": i + 1, "pillar": pillar, "type": itype, "shape": why})

    verdict, code = ("THIN", 2) if findings else ("GREEN", 0)
    return {
        "verdict": verdict,
        "exit_code": code,
        "eligibility": {"followers": followers, "floor": ELIGIBILITY_FLOOR, "eligible": True,
                        "note": "LinkedIn also applies criteria it does not publish; eligibility "
                                "is evaluated by LinkedIn, not by this tool."},
        "cadence": {"choice": cadence, "label": spec["label"],
                    "issues_per_month": spec["issues_per_month"],
                    "monthly_cost_minutes": round(monthly_cost),
                    "monthly_budget_minutes": minutes_per_month,
                    "headroom_pct": headroom},
        "arc": arc,
        "findings": findings,
        "stop_rule": [
            "Write it now, before issue one.",
            "If three consecutive issues land below half the median engagement of your regular "
            "posts, the format is not earning its cost — move the material back to posts.",
            "If you miss two scheduled issues in a quarter, drop the cadence one step rather "
            "than trying to catch up. Subscribers notice frequency, not effort.",
            "Ending it deliberately with a final issue costs nothing. Letting it go quiet is "
            "the version people remember.",
        ],
        "naming_rule": "Name the newsletter after the problem it solves, not after yourself. "
                       "'The Analytics Trust Letter' tells a stranger whether to subscribe; "
                       "'Alex's Newsletter' does not.",
    }


def render_human(r: dict) -> str:
    if r["verdict"] in ("NOT_ELIGIBLE", "UNSUSTAINABLE"):
        lines = [f"Newsletter: {r['verdict']}", "=" * 52, r["finding"], "",
                 f"Instead: {r['instead']}"]
        if "rule" in r:
            lines += ["", r["rule"]]
        return "\n".join(lines)
    c = r["cadence"]
    lines = [f"Newsletter: {r['verdict']}", "=" * 52,
             f"Eligibility : {r['eligibility']['followers']} followers "
             f"(floor {r['eligibility']['floor']}) — {r['eligibility']['note']}",
             f"Cadence     : {c['label']} — {c['monthly_cost_minutes']} of "
             f"{c['monthly_budget_minutes']} min/month, {c['headroom_pct']}% headroom", ""]
    if r["findings"]:
        lines.append("Findings:")
        for f in r["findings"]:
            lines.append(f"  [{f['severity'].upper():<8}] {f['area']}: {f['finding']}")
            lines.append(f"             fix → {f['fix']}")
        lines.append("")
    lines.append("Arc:")
    for a in r["arc"]:
        lines.append(f"  #{a['issue']:<3} {a['type']:<15} {a['pillar']}")
    lines.append("\nStop rule:")
    for s in r["stop_rule"]:
        lines.append(f"  - {s}")
    lines.append(f"\n{r['naming_rule']}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Gate and plan a LinkedIn newsletter (green=0 / thin=2 / refused=3).")
    ap.add_argument("--followers", type=int, help="Followers and/or connections.")
    ap.add_argument("--cadence", choices=sorted(CADENCES), default="biweekly")
    ap.add_argument("--minutes-per-month", type=int, default=300,
                    help="Minutes per month you will protect for the newsletter.")
    ap.add_argument("--issue-minutes", type=int, default=ISSUE_MINUTES_DEFAULT,
                    help=f"Minutes one issue really takes (default {ISSUE_MINUTES_DEFAULT}).")
    ap.add_argument("--pillar", action="append", default=[],
                    help="A content pillar from the positioning brief. Repeatable.")
    ap.add_argument("--issues", type=int, default=12, help="Issues to lay out (default 12).")
    ap.add_argument("--output", choices=["json", "human"], default="json")
    ap.add_argument("--sample", action="store_true", help="Run a built-in example.")
    args = ap.parse_args()

    if args.sample:
        s = SAMPLE
        followers, cadence = s["followers"], s["cadence"]
        mpm, im, pillars, issues = (s["minutes_per_month"], s["issue_minutes"],
                                    s["pillars"], s["issues"])
    else:
        if args.followers is None:
            ap.error("--followers is required (or use --sample)")
        followers, cadence = args.followers, args.cadence
        mpm, im, pillars, issues = (args.minutes_per_month, args.issue_minutes,
                                    args.pillar, args.issues)
    if issues < 1 or issues > 52:
        ap.error("--issues must be between 1 and 52")

    result = build(followers, cadence, mpm, im, pillars, issues)
    print(json.dumps(result, indent=2) if args.output == "json" else render_human(result))
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
