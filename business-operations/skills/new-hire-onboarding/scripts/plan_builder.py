#!/usr/bin/env python3
"""Build a new hire's 30/60/90-day plan and refuse milestones nobody could check.

Input: a JSON file:

  {
    "hire": "A. Rivera", "role": "Backend Engineer", "start_date": "2026-12-07",
    "manager": "J. Chen", "buddy": "P. Okafor", "profile": "engineering",
    "milestones": [
      {"phase": 30, "outcome": "Ship a small bug fix to production",
       "done_when": "PR merged and deployed", "early_win": true},
      {"phase": 60, "outcome": "Own the billing-export service on-call shadow",
       "done_when": "Shadowed 1 on-call week, handled 2 pages with the primary"},
      ...
    ]
  }

Rules (the plan is refused, exit 4, on any BLOCK):
  P1 BLOCK  every phase (30, 60, 90; 120 for the executive profile) has at least
            one milestone. WARN above 5 in a phase: too many to focus on.
  P2 BLOCK  every milestone has a `done_when` someone other than the hire could
            check. An outcome that starts with learn / understand / get familiar /
            get to know / explore / absorb / settle in / ramp up and has no
            `done_when` is a hope, not a milestone.
  P3 WARN   the 30-day phase has an early win (`early_win: true`): a small,
            visible result that builds credibility early (Watkins).
  P4 BLOCK  a named manager and a named buddy who is not the manager.

Schedule (business days; a date that lands on a weekend moves to Monday):
  day 1: welcome, manager 1:1, buddy intro, access check
  end of week 1: manager check-in on role clarity
  weekly manager 1:1 through the horizon
  buddy meetings weekly (every two weeks for executive): 13 in 90 days, above
  the "more than 8 in 90 days" bracket in Microsoft's buddy pilot
  checkpoints on day 30, 60, 90 (and 120): milestones reviewed, plan adjusted

--profile picks the horizon and the example milestones printed when a phase
is empty: standard, engineering, sales, support, executive.

Exit codes: 0 plan built, 2 built with warnings, 3 bad input, 4 refused.
Deterministic, stdlib only, no network.
"""
import argparse
import datetime as dt
import json
import re
import sys

EXIT = {"OK": 0, "WARN": 2, "BAD_INPUT": 3, "REFUSED": 4}
VAGUE = re.compile(r"^\s*(learn|understand|get (familiar|to know|up to speed|acquainted)|familiari[sz]e|explore|"
                   r"absorb|settle in|ramp( up)?|onboard|meet (the|everyone)|shadow(?! .*\d)|observe|be comfortable)\b", re.I)
PROFILES = {
    "standard": {"horizon": 90, "buddy_every_days": 7, "examples": {
        30: ["Run the team's weekly report end to end (done when: report sent on time, manager signs off)"],
        60: ["Own one recurring process (done when: ran it twice with no handoff back)"],
        90: ["Deliver one improvement the team asked for (done when: change live, owner of the old process agrees)"]}},
    "engineering": {"horizon": 90, "buddy_every_days": 7, "examples": {
        30: ["Ship a small fix to production (done when: PR merged and deployed)"],
        60: ["Own a component's on-call shadow week (done when: handled 2 pages with the primary)"],
        90: ["Lead a scoped feature from design to release (done when: design doc approved, feature live)"]}},
    "sales": {"horizon": 90, "buddy_every_days": 7, "examples": {
        30: ["Run a full discovery call with the manager listening (done when: call scored on the team rubric)"],
        60: ["Build own pipeline (done when: N qualified opportunities in the CRM, N set by the manager)"],
        90: ["Close first deal or reach ramp quota (done when: closed-won in the CRM)"]}},
    "support": {"horizon": 90, "buddy_every_days": 7, "examples": {
        30: ["Resolve tickets from the starter queue (done when: N solved with QA score above the team bar)"],
        60: ["Take the full queue for one shift (done when: SLA met for the shift)"],
        90: ["Write or fix two help-center articles (done when: published, reviewed by the KB owner)"]}},
    "executive": {"horizon": 120, "buddy_every_days": 14, "examples": {
        30: ["Present a listening-tour diagnosis (done when: written diagnosis reviewed with the CEO)"],
        60: ["Agree priorities with peers (done when: written top-3 priorities signed off by the leadership team)"],
        90: ["Deliver one early win in the org (done when: named result live, announced)"],
        120: ["Present the org plan (done when: plan approved with owners and dates)"]}},
}


def parse_date(s, field):
    try:
        return dt.date.fromisoformat(str(s))
    except ValueError:
        raise ValueError(f"{field} must be YYYY-MM-DD, got {s!r}")


def on_business_day(d):
    while d.weekday() >= 5:
        d += dt.timedelta(days=1)
    return d


def build(spec, profile_override=None):
    if not isinstance(spec, dict):
        raise ValueError("input must be a JSON object")
    start = parse_date(spec.get("start_date"), "start_date")
    if start.weekday() >= 5:
        raise ValueError(f"start_date {start} is a weekend day")
    profile = (profile_override or spec.get("profile") or "standard").lower()
    if profile not in PROFILES:
        raise ValueError(f"profile must be one of {sorted(PROFILES)}")
    prof = PROFILES[profile]
    horizon = prof["horizon"]
    phases = list(range(30, horizon + 1, 30))
    ms = spec.get("milestones") or []
    if not isinstance(ms, list):
        raise ValueError("milestones must be a list")

    findings, by_phase = [], {p: [] for p in phases}
    for i, m in enumerate(ms):
        if not isinstance(m, dict) or not m.get("outcome"):
            raise ValueError(f"milestone {i}: needs 'phase' and 'outcome'")
        try:
            ph = int(m.get("phase"))
        except (TypeError, ValueError):
            raise ValueError(f"milestone {i}: phase must be one of {phases}")
        if ph not in by_phase:
            raise ValueError(f"milestone {i}: phase must be one of {phases}, got {ph}")
        outcome = str(m["outcome"]).strip()
        done_when = str(m.get("done_when") or "").strip()
        item = {"phase": ph, "outcome": outcome, "done_when": done_when or None,
                "early_win": bool(m.get("early_win")), "owner": (m.get("owner") or spec.get("hire") or "hire")}
        if not done_when:
            kind = "vague outcome" if VAGUE.search(outcome) else "no check"
            findings.append({"rule": "P2", "level": "BLOCK",
                             "msg": f"Day {ph}: '{outcome}' has no done_when ({kind}). Say what someone else could see when it is done."})
        by_phase[ph].append(item)

    for ph in phases:
        n = len(by_phase[ph])
        if n == 0:
            ex = "; ".join(prof["examples"].get(ph, []))
            findings.append({"rule": "P1", "level": "BLOCK", "msg": f"Day {ph}: no milestone. Example for {profile}: {ex}"})
        elif n > 5:
            findings.append({"rule": "P1", "level": "WARN", "msg": f"Day {ph}: {n} milestones; keep 3 to 5 so the hire can focus."})
    if by_phase[30] and not any(m["early_win"] for m in by_phase[30]):
        findings.append({"rule": "P3", "level": "WARN",
                         "msg": "Day 30: no early win marked. Pick one small, visible result and set early_win: true."})
    manager = spec.get("manager") or ""
    if not isinstance(manager, str):
        raise ValueError("manager must be a string")
    manager = manager.strip()
    buddy = spec.get("buddy") or ""
    if not isinstance(buddy, str):
        raise ValueError("buddy must be a string")
    buddy = buddy.strip()
    if not manager:
        findings.append({"rule": "P4", "level": "BLOCK", "msg": "No named manager."})
    if not buddy:
        findings.append({"rule": "P4", "level": "BLOCK", "msg": "No named buddy. Pick a peer, not the manager."})
    elif manager and buddy.lower() == manager.lower():
        findings.append({"rule": "P4", "level": "BLOCK", "msg": "The buddy is the manager. A buddy is a peer the hire can ask anything."})

    sched = [{"date": start.isoformat(), "day": 1, "event": "Welcome, manager 1:1, buddy intro, access check"},
             {"date": on_business_day(start + dt.timedelta(days=4)).isoformat(), "day": 5,
              "event": "Manager check-in: role clarity, what the first 30 days are for"}]
    for ph in phases:
        d = on_business_day(start + dt.timedelta(days=ph - 1))
        sched.append({"date": d.isoformat(), "day": ph,
                      "event": f"Day-{ph} checkpoint with manager: review milestones, adjust the next phase"})
    sched.sort(key=lambda e: e["date"])
    end = dt.date.fromisoformat(sched[-1]["date"])
    buddy_n = len(range(0, horizon, prof["buddy_every_days"]))
    mgr_n = len(range(0, horizon, 7))

    blocks = [f for f in findings if f["level"] == "BLOCK"]
    status = "REFUSED" if blocks else ("WARN" if findings else "OK")
    return {"hire": spec.get("hire", ""), "role": spec.get("role", ""), "profile": profile, "start_date": start.isoformat(),
            "end_date": end.isoformat(), "horizon_days": horizon, "manager": manager or None, "buddy": buddy or None,
            "milestones": {str(p): by_phase[p] for p in phases}, "schedule": sched,
            "cadence": {"manager_1on1s": mgr_n, "buddy_meetings": buddy_n,
                        "buddy_every_days": prof["buddy_every_days"]},
            "findings": findings, "status": status}


def render_md(r):
    out = [f"# 30/60/90 plan: {r['hire'] or 'new hire'}, {r['role'] or 'role'}", "",
           f"Start {r['start_date']} · profile {r['profile']} · manager {r['manager'] or 'MISSING'} · "
           f"buddy {r['buddy'] or 'MISSING'} · status **{r['status']}**", ""]
    if r["findings"]:
        out.append("## Fix before sharing" if r["status"] == "REFUSED" else "## Warnings")
        out += [f"- {f['level']} {f['rule']}: {f['msg']}" for f in r["findings"]]
        out.append("")
    for ph, items in r["milestones"].items():
        out.append(f"## By day {ph}")
        if not items:
            out.append("- (none yet)")
        for m in items:
            win = " (early win)" if m["early_win"] else ""
            out.append(f"- [ ] {m['outcome']}{win}. Done when: {m['done_when'] or 'MISSING'}")
        out.append("")
    out.append("## Calendar")
    out.append("| Date | Day | What |")
    out.append("|---|---|---|")
    out += [f"| {e['date']} | {e['day']} | {e['event']} |" for e in r["schedule"]]
    c = r["cadence"]
    out += ["", f"Plus {c['manager_1on1s']} weekly manager 1:1s and {c['buddy_meetings']} buddy meetings "
                f"(every {c['buddy_every_days']} days) through {r['end_date']}."]
    return "\n".join(out)


SAMPLE = {
    "hire": "A. Rivera", "role": "Backend Engineer", "start_date": "2026-12-07",
    "manager": "J. Chen", "buddy": "P. Okafor", "profile": "engineering",
    "milestones": [
        {"phase": 30, "outcome": "Ship a small bug fix to production", "done_when": "PR merged and deployed", "early_win": True},
        {"phase": 30, "outcome": "Understand the billing architecture"},
        {"phase": 60, "outcome": "Own the billing-export on-call shadow week",
         "done_when": "Handled 2 pages with the primary, wrote one runbook fix"},
        {"phase": 90, "outcome": "Lead the invoice-retry feature", "done_when": "Design doc approved and feature live"},
    ],
}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 epilog="Exit codes: 0 built, 2 built with warnings, 3 bad input, 4 refused.")
    ap.add_argument("--plan", help="plan JSON (start_date, manager, buddy, profile, milestones)")
    ap.add_argument("--profile", choices=sorted(PROFILES), help="override the file's profile")
    ap.add_argument("--sample", action="store_true", help="run on a built-in plan")
    ap.add_argument("--output", "--format", choices=["text", "md", "json"], default="text",
                    help="text and md print the plan as markdown; json for tools")
    a = ap.parse_args(argv)
    try:
        if a.sample:
            spec = SAMPLE
        elif a.plan:
            with open(a.plan, encoding="utf-8") as f:
                spec = json.load(f)
        else:
            raise ValueError("give --plan FILE or --sample")
        res = build(spec, a.profile)
    except (ValueError, OSError, json.JSONDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return EXIT["BAD_INPUT"]
    print(json.dumps(res, indent=2) if a.output == "json" else render_md(res))
    return EXIT[res["status"]]


if __name__ == "__main__":
    sys.exit(main())
