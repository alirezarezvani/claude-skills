#!/usr/bin/env python3
"""Lint an SLA policy before it is promised to customers or fed to sla_check.py.

sla_check.py measures tickets against the policy it is given; it cannot tell you the
policy itself is wrong. Policies fail in a few repeatable ways: a field left out so a
default silently applies (UTC, Mon-Fri 9-5), a lower priority promised faster than a
higher one, an urgent target on a business clock (a Friday-evening outage waits until
Monday), a holiday calendar that ran out last year, or ticket priorities the policy does
not name, so those tickets drop out of every SLA report. This catches them.

Findings
  NO_TARGETS            no targets at all                                         BLOCKER
  MISSING_TARGET        a priority lacks first_response_h or resolution_h          BLOCKER
  BAD_VALUE             a target is not a positive number, or the clock is not
                        business / calendar, or business hours do not parse        BLOCKER
  RESOLUTION_BEFORE_FRT resolution_h shorter than first_response_h                 BLOCKER
  INVERTED_PRIORITY     a lower priority is promised faster than a higher one      BLOCKER
  UNMAPPED_PRIORITY     tickets (--tickets) carry a priority the policy lacks      BLOCKER
  URGENT_BUSINESS_CLOCK the top priority runs on the business clock                HIGH
  NO_TIMEZONE           timezone_offset missing: sla_check falls back to UTC       HIGH
  NO_BUSINESS_HOURS     business clock used but business_hours missing (defaults
                        to Mon-Fri 09:00-17:00 silently)                           HIGH
  TARGET_SPANS_WEEKS    a business-clock target longer than 2 working weeks        WARN
  HOLIDAYS_STALE        no holiday in the next 365 days (calendar not maintained)  WARN
  UNUSED_PRIORITY       a policy priority no ticket in --tickets uses             INFO

Priority order: --order (comma list, most urgent first), else the policy's "order" key,
else the known names urgent/critical/p1 > high/p2 > normal/medium/p3 > low/p4.
Exit codes: 0 clean, 2 findings, 3 bad input, 4 blocked. Deterministic, stdlib only.
"""
import argparse
import csv
import datetime as dt
import json
import re
import sys

EXIT = {"CLEAN": 0, "FINDINGS": 2, "BAD_INPUT": 3, "BLOCKED": 4}
SEV_ORDER = {"BLOCKER": 0, "HIGH": 1, "WARN": 2, "INFO": 3}
RANK = {"urgent": 0, "critical": 0, "p1": 0, "sev1": 0, "high": 1, "p2": 1, "sev2": 1,
        "normal": 2, "medium": 2, "p3": 2, "sev3": 2, "low": 3, "p4": 3, "sev4": 3}

SAMPLE = {
    "business_hours": {"days": [0, 1, 2, 3, 4], "start": "09:00", "end": "17:00", "holidays": ["2025-12-25"]},
    "targets": {
        "urgent": {"first_response_h": 1, "resolution_h": 8, "clock": "business"},
        "high": {"first_response_h": 4, "resolution_h": 3, "clock": "business"},
        "normal": {"first_response_h": 2, "resolution_h": 40, "clock": "business"},
        "low": {"first_response_h": 16, "resolution_h": 120, "clock": "business"}}}
SAMPLE_PRIORITIES = ["urgent", "high", "normal", "low", "p1", "normal"]


def lint(policy, now, order=None, ticket_priorities=None):
    f = []
    add = lambda code, sev, msg: f.append({"code": code, "severity": sev, "message": msg})
    targets = policy.get("targets") or {}
    if not isinstance(targets, dict) or not targets:
        add("NO_TARGETS", "BLOCKER", "policy has no targets")
        return f, []
    names = [p.lower() for p in targets]
    tg = {p.lower(): t for p, t in targets.items()}
    clean = {}
    for p, t in tg.items():
        ok = True
        for k in ("first_response_h", "resolution_h"):
            if k not in t:
                add("MISSING_TARGET", "BLOCKER", f"{p}: no {k}")
                ok = False
            elif not isinstance(t[k], (int, float)) or isinstance(t[k], bool) or t[k] <= 0:
                add("BAD_VALUE", "BLOCKER", f"{p}: {k} must be a positive number of hours, got {t[k]!r}")
                ok = False
        clock = t.get("clock", "business")
        if clock not in ("business", "calendar"):
            add("BAD_VALUE", "BLOCKER", f"{p}: clock must be business or calendar, got {clock!r}")
            ok = False
        if ok:
            clean[p] = (t["first_response_h"], t["resolution_h"], clock)
            if t["resolution_h"] < t["first_response_h"]:
                add("RESOLUTION_BEFORE_FRT", "BLOCKER",
                    f"{p}: resolution {t['resolution_h']}h is shorter than first response {t['first_response_h']}h")

    if order:
        ranked = [p for p in order if p in clean]
    elif isinstance(policy.get("order"), list):
        ranked = [p.lower() for p in policy["order"] if p.lower() in clean]
    else:
        ranked = sorted((p for p in clean if p in RANK), key=lambda p: RANK[p])
    for i, hi in enumerate(ranked):
        for lo in ranked[i + 1:]:
            for idx, label in ((0, "first response"), (1, "resolution")):
                if clean[lo][idx] < clean[hi][idx]:
                    add("INVERTED_PRIORITY", "BLOCKER",
                        f"{lo} promises {label} in {clean[lo][idx]}h, faster than {hi} ({clean[hi][idx]}h)")
    if ranked and clean[ranked[0]][2] == "business":
        add("URGENT_BUSINESS_CLOCK", "HIGH",
            f"top priority '{ranked[0]}' runs on the business clock: an outage reported Friday evening is not due "
            f"until Monday. Use the calendar clock, or state the on-call hours in the contract.")

    if "timezone_offset" not in policy:
        add("NO_TIMEZONE", "HIGH", "timezone_offset missing: sla_check.py measures in UTC, which shifts every business day")
    elif not re.match(r"^[+-]\d{2}:\d{2}$", str(policy["timezone_offset"])):
        add("BAD_VALUE", "BLOCKER", f"timezone_offset must look like +01:00, got {policy['timezone_offset']!r}")

    uses_business = any(c[2] == "business" for c in clean.values())
    bh = policy.get("business_hours")
    if uses_business and not bh:
        add("NO_BUSINESS_HOURS", "HIGH", "business clock in use but business_hours missing: Mon-Fri 09:00-17:00 applies silently")
    bh = bh or {}
    day_hours = 8.0
    days = bh.get("days", [0, 1, 2, 3, 4])
    try:
        start = dt.time.fromisoformat(bh.get("start", "09:00"))
        end = dt.time.fromisoformat(bh.get("end", "17:00"))
        if end <= start:
            raise ValueError("end must be after start (overnight shifts: use the calendar clock)")
        if not days or any(not isinstance(d, int) or d < 0 or d > 6 for d in days):
            raise ValueError("days must be weekday numbers 0 (Mon) to 6 (Sun)")
        day_hours = (dt.datetime.combine(dt.date.today(), end) - dt.datetime.combine(dt.date.today(), start)).seconds / 3600
        hol = [dt.date.fromisoformat(h) for h in bh.get("holidays", [])]
    except (ValueError, TypeError) as exc:
        add("BAD_VALUE", "BLOCKER", f"business_hours: {exc}")
        hol = []
    if uses_business:
        two_weeks = day_hours * len(set(days)) * 2
        for p, (frt, res, clock) in clean.items():
            if clock == "business" and res > two_weeks:
                add("TARGET_SPANS_WEEKS", "WARN",
                    f"{p}: resolution {res} business hours is over two working weeks ({two_weeks:g}h); "
                    f"customers read it as calendar time, so state it in days")
        today = now.date()
        if not any(today <= h <= today + dt.timedelta(days=365) for h in hol):
            add("HOLIDAYS_STALE", "WARN", "no holiday in the next 365 days: add this year's calendar, or business-hour "
                                          "clocks will count public holidays as working time")

    if ticket_priorities is not None:
        seen = {p.strip().lower() for p in ticket_priorities if p.strip()}
        for p in sorted(seen - set(names)):
            n = sum(1 for x in ticket_priorities if x.strip().lower() == p)
            add("UNMAPPED_PRIORITY", "BLOCKER", f"{n} ticket(s) have priority '{p}', which the policy does not define: "
                                                f"they drop out of SLA reporting. Map it or add a target.")
        for p in sorted(set(names) - seen):
            add("UNUSED_PRIORITY", "INFO", f"no ticket uses priority '{p}'")
    return f, ranked


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 epilog="Exit codes: 0 clean, 2 findings, 3 bad input, 4 blocked.")
    ap.add_argument("--policy", help="SLA policy JSON (the same file sla_check.py reads)")
    ap.add_argument("--tickets", help="tickets CSV with a priority column, to find unmapped priorities")
    ap.add_argument("--order", help="priorities most urgent first, comma-separated (default: known names)")
    ap.add_argument("--now", help="date for the holiday check, YYYY-MM-DD (default today)")
    ap.add_argument("--sample", action="store_true", help="run on a built-in example")
    ap.add_argument("--output", "--format", choices=["text", "json"], default="text")
    a = ap.parse_args(argv)
    try:
        now = dt.datetime.fromisoformat(a.now) if a.now else dt.datetime.now()
        order = [p.strip().lower() for p in a.order.split(",")] if a.order else None
        if a.sample:
            policy, prios = SAMPLE, SAMPLE_PRIORITIES
            now = dt.datetime(2026, 11, 26)
        else:
            if not a.policy:
                raise ValueError("--policy is required (or use --sample)")
            with open(a.policy, encoding="utf-8") as fh:
                policy = json.load(fh)
            if not isinstance(policy, dict):
                raise ValueError("policy must be a JSON object")
            prios = None
            if a.tickets:
                with open(a.tickets, encoding="utf-8", newline="") as fh:
                    rdr = csv.DictReader(fh)
                    if not rdr.fieldnames or "priority" not in rdr.fieldnames:
                        raise ValueError("tickets CSV needs a priority column")
                    prios = [r["priority"] or "" for r in rdr]
        findings, ranked = lint(policy, now, order, prios)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"verdict": "BAD_INPUT", "error": str(exc)}) if a.output == "json" else f"BAD_INPUT: {exc}")
        return EXIT["BAD_INPUT"]
    findings.sort(key=lambda x: SEV_ORDER[x["severity"]])
    sevs = {x["severity"] for x in findings}
    verdict = "BLOCKED" if "BLOCKER" in sevs else "FINDINGS" if sevs & {"HIGH", "WARN"} else "CLEAN"
    res = {"verdict": verdict, "priority_order": ranked,
           "counts": {s: sum(1 for x in findings if x["severity"] == s) for s in SEV_ORDER}, "findings": findings}
    if a.output == "json":
        print(json.dumps(res, indent=2))
    else:
        print(f"SLA policy lint: {verdict}  (priority order: {' > '.join(ranked) or 'unknown'})")
        for x in findings:
            print(f"  [{x['severity']}] {x['code']}: {x['message']}")
    return EXIT[verdict]


if __name__ == "__main__":
    sys.exit(main())
