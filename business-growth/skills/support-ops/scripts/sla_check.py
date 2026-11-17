#!/usr/bin/env python3
"""Support SLA attainment, breach risk and backlog health from a ticket export.

Input: a tickets CSV from any helpdesk, with columns
  id, priority, created_at, first_response_at, resolved_at
and optionally reopened (0/1), channel. Timestamps are ISO 8601; blank means
"not yet". A policy JSON gives per-priority targets in hours and the clock
they run on (business or calendar hours):

  {"timezone_offset": "+01:00",
   "business_hours": {"days": [0,1,2,3,4], "start": "09:00", "end": "17:00", "holidays": ["2026-12-25"]},
   "targets": {"urgent": {"first_response_h": 1, "resolution_h": 8, "clock": "calendar"},
               "normal": {"first_response_h": 8, "resolution_h": 40, "clock": "business"}}}

Reports per priority: first-response and resolution attainment, median and
90th percentile, open tickets already breached or due within --risk-hours,
backlog age buckets and reopen rate. A ticket that was resolved and reopened
counts as a resolution breach if --reopen-breaches is set, because the
customer's problem was not solved in time.

Exit codes: 0 all targets met and nothing at risk, 2 attainment below
--target or tickets at risk, 3 bad input, 4 open tickets already breached.
Deterministic (pass --now for a fixed clock), stdlib only, no network.
"""
import argparse
import csv
import datetime as dt
import io
import json
import statistics
import sys
from collections import defaultdict

EXIT = {"OK": 0, "AT_RISK": 2, "BAD_INPUT": 3, "BREACHED": 4}

SAMPLE_POLICY = {
    "timezone_offset": "+01:00",
    "business_hours": {"days": [0, 1, 2, 3, 4], "start": "09:00", "end": "17:00", "holidays": ["2026-11-11"]},
    "targets": {
        "urgent": {"first_response_h": 1, "resolution_h": 8, "clock": "calendar"},
        "high": {"first_response_h": 4, "resolution_h": 16, "clock": "business"},
        "normal": {"first_response_h": 8, "resolution_h": 40, "clock": "business"},
    },
}
SAMPLE_TICKETS = """id,priority,created_at,first_response_at,resolved_at,reopened,channel
T-101,urgent,2026-11-13T22:10:00+01:00,2026-11-13T22:40:00+01:00,2026-11-14T04:05:00+01:00,0,chat
T-102,urgent,2026-11-14T10:00:00+01:00,2026-11-14T11:25:00+01:00,2026-11-14T15:00:00+01:00,0,phone
T-103,high,2026-11-13T16:30:00+01:00,2026-11-16T09:45:00+01:00,2026-11-16T15:00:00+01:00,0,email
T-104,high,2026-11-14T09:05:00+01:00,2026-11-14T10:00:00+01:00,,0,email
T-105,normal,2026-11-10T14:00:00+01:00,2026-11-12T10:00:00+01:00,2026-11-14T12:00:00+01:00,1,email
T-106,normal,2026-11-12T09:30:00+01:00,2026-11-12T13:00:00+01:00,2026-11-13T11:00:00+01:00,0,email
T-107,normal,2026-11-16T15:00:00+01:00,,,0,email
T-108,normal,2026-11-09T11:00:00+01:00,2026-11-09T12:00:00+01:00,,0,email
T-109,high,2026-11-16T14:00:00+01:00,,,0,chat
"""
SAMPLE_NOW = "2026-11-17T11:00:00+01:00"


def parse_ts(raw, tz):
    raw = (raw or "").strip()
    if not raw:
        return None
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    t = dt.datetime.fromisoformat(raw)
    if t.tzinfo is None:
        t = t.replace(tzinfo=tz)
    return t.astimezone(tz)


def parse_offset(s):
    sign = -1 if s.startswith("-") else 1
    h, m = s.lstrip("+-").split(":")
    return dt.timezone(sign * dt.timedelta(hours=int(h), minutes=int(m)))


class Clock:
    def __init__(self, policy):
        bh = policy.get("business_hours") or {}
        self.days = set(bh.get("days", [0, 1, 2, 3, 4]))
        self.start = dt.time.fromisoformat(bh.get("start", "09:00"))
        self.end = dt.time.fromisoformat(bh.get("end", "17:00"))
        if self.end <= self.start:
            raise ValueError("business_hours end must be after start (overnight shifts: use the calendar clock)")
        self.holidays = {dt.date.fromisoformat(d) for d in bh.get("holidays", [])}

    def business_hours(self, a, b):
        """Business hours between datetimes a <= b (same tz)."""
        if b <= a:
            return 0.0
        total = 0.0
        d = a.date()
        while d <= b.date():
            if d.weekday() in self.days and d not in self.holidays:
                ws = dt.datetime.combine(d, self.start, a.tzinfo)
                we = dt.datetime.combine(d, self.end, a.tzinfo)
                lo, hi = max(a, ws), min(b, we)
                if hi > lo:
                    total += (hi - lo).total_seconds() / 3600
            d += dt.timedelta(days=1)
        return total

    def elapsed(self, a, b, clock):
        return self.business_hours(a, b) if clock == "business" else max(0.0, (b - a).total_seconds() / 3600)


def pct(xs, q):
    if not xs:
        return None
    xs = sorted(xs)
    k = (len(xs) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return round(xs[lo] + (xs[hi] - xs[lo]) * (k - lo), 2)


def analyse(text, policy, now, target, risk_h, reopen_breaches):
    tz = parse_offset(policy.get("timezone_offset", "+00:00"))
    clock = Clock(policy)
    targets = policy.get("targets") or {}
    if not targets:
        raise ValueError("policy has no targets")
    for p, t in targets.items():
        if t.get("clock", "business") not in ("business", "calendar"):
            raise ValueError(f"targets.{p}.clock must be business or calendar")
    rdr = csv.DictReader(io.StringIO(text))
    need = {"id", "priority", "created_at", "first_response_at", "resolved_at"}
    if not rdr.fieldnames or not need <= set(rdr.fieldnames):
        raise ValueError("tickets CSV needs columns: " + ", ".join(sorted(need)))
    now = now.astimezone(tz)
    stats = defaultdict(lambda: {"n": 0, "frt": [], "frt_met": 0, "frt_n": 0, "res": [], "res_met": 0, "res_n": 0, "reopened": 0})
    breached, at_risk, unknown = [], [], set()
    ages = {"<1d": 0, "1-3d": 0, "3-7d": 0, ">7d": 0}
    for i, r in enumerate(rdr, 2):
        pr = (r["priority"] or "").strip().lower()
        if pr not in targets:
            unknown.add(pr or "(blank)")
            continue
        t = targets[pr]
        ck = t.get("clock", "business")
        try:
            c = parse_ts(r["created_at"], tz)
            f = parse_ts(r["first_response_at"], tz)
            z = parse_ts(r["resolved_at"], tz)
        except ValueError as exc:
            raise ValueError(f"row {i} ({r['id']}): {exc}")
        if c is None:
            raise ValueError(f"row {i} ({r['id']}): created_at is empty")
        for label, x in (("first_response_at", f), ("resolved_at", z)):
            if x is not None and x < c:
                raise ValueError(f"row {i} ({r['id']}): {label} is before created_at")
        s = stats[pr]
        s["n"] += 1
        reopened = (r.get("reopened") or "0").strip() in ("1", "true", "yes")
        s["reopened"] += reopened
        for kind, end, goal in (("frt", f, t["first_response_h"]), ("res", z, t["resolution_h"])):
            if end is not None:
                e = clock.elapsed(c, end, ck)
                s[kind].append(e)
                s[kind + "_n"] += 1
                met = e <= goal and not (kind == "res" and reopened and reopen_breaches)
                s[kind + "_met"] += met
            else:
                e = clock.elapsed(c, now, ck)
                left = goal - e
                item = {"id": r["id"], "priority": pr, "stage": "first response" if kind == "frt" else "resolution",
                        "elapsed_h": round(e, 2), "target_h": goal, "clock": ck}
                if left < 0:
                    s[kind + "_n"] += 1  # counts as missed already
                    breached.append(item)
                elif left <= risk_h:
                    item["hours_left"] = round(left, 2)
                    at_risk.append(item)
        if z is None:
            age_d = (now - c).total_seconds() / 86400
            ages["<1d" if age_d < 1 else "1-3d" if age_d < 3 else "3-7d" if age_d < 7 else ">7d"] += 1
    if not stats:
        raise ValueError("no tickets with a priority named in the policy" + (f" (found {sorted(unknown)})" if unknown else ""))
    per = {}
    below = []
    for pr, s in stats.items():
        frt_att = s["frt_met"] / s["frt_n"] if s["frt_n"] else None
        res_att = s["res_met"] / s["res_n"] if s["res_n"] else None
        per[pr] = {"tickets": s["n"], "clock": targets[pr].get("clock", "business"),
                   "first_response": {"target_h": targets[pr]["first_response_h"], "attainment": None if frt_att is None else round(frt_att, 3),
                                      "p50_h": pct(s["frt"], .5), "p90_h": pct(s["frt"], .9)},
                   "resolution": {"target_h": targets[pr]["resolution_h"], "attainment": None if res_att is None else round(res_att, 3),
                                  "p50_h": pct(s["res"], .5), "p90_h": pct(s["res"], .9)},
                   "reopen_rate": round(s["reopened"] / s["n"], 3)}
        for k, v in (("first response", frt_att), ("resolution", res_att)):
            if v is not None and v < target:
                below.append(f"{pr} {k} attainment {v:.0%} < {target:.0%}")
    verdict = "BREACHED" if breached else ("AT_RISK" if (below or at_risk) else "OK")
    return {"verdict": verdict, "now": now.isoformat(), "target_attainment": target, "per_priority": per,
            "below_target": below, "open_breached": breached,
            "open_at_risk": sorted(at_risk, key=lambda x: x["hours_left"]), "backlog_age": ages,
            "ignored_priorities": sorted(unknown)}


def render(res):
    out = [f"SLA check: {res['verdict']}  (as of {res['now']}, attainment target {res['target_attainment']:.0%})", ""]
    out.append(f"{'priority':10s} {'n':>4s} {'clock':9s} {'FRT att':>8s} {'FRT p90':>8s} {'RES att':>8s} {'RES p90':>8s} {'reopen':>7s}")
    for pr, p in res["per_priority"].items():
        f, r = p["first_response"], p["resolution"]
        fa = "n/a" if f["attainment"] is None else f"{f['attainment']:.0%}"
        ra = "n/a" if r["attainment"] is None else f"{r['attainment']:.0%}"
        out.append(f"{pr:10s} {p['tickets']:>4d} {p['clock']:9s} {fa:>8s} {str(f['p90_h']):>8s} {ra:>8s} {str(r['p90_h']):>8s} {p['reopen_rate']:>7.0%}")
    out.append("")
    for b in res["open_breached"]:
        out.append(f"[BREACHED] {b['id']} ({b['priority']}) {b['stage']}: {b['elapsed_h']}h of {b['target_h']}h {b['clock']}")
    for a in res["open_at_risk"]:
        out.append(f"[AT RISK] {a['id']} ({a['priority']}) {a['stage']}: {a['hours_left']}h left ({a['clock']})")
    for b in res["below_target"]:
        out.append(f"[BELOW TARGET] {b}")
    out.append("Backlog age: " + ", ".join(f"{k} {v}" for k, v in res["backlog_age"].items()))
    if res["ignored_priorities"]:
        out.append(f"Ignored (no target in policy): {', '.join(res['ignored_priorities'])}")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0], epilog="Exit codes: 0 ok, 2 at risk or below target, 3 bad input, 4 open tickets breached.")
    ap.add_argument("--tickets", help="tickets CSV")
    ap.add_argument("--policy", help="SLA policy JSON (targets and business hours)")
    ap.add_argument("--now", help="ISO timestamp to evaluate at (default: current time)")
    ap.add_argument("--target", type=float, default=0.9, help="attainment target, 0-1 (default 0.9)")
    ap.add_argument("--risk-hours", type=float, default=2.0, help="flag open tickets due within this many clock hours (default 2)")
    ap.add_argument("--reopen-breaches", action="store_true", help="count reopened tickets as resolution breaches")
    ap.add_argument("--sample", action="store_true", help="run on built-in tickets and policy")
    ap.add_argument("--output", "--format", choices=["text", "json"], default="text")
    a = ap.parse_args(argv)
    try:
        if a.sample:
            text, policy, now_raw = SAMPLE_TICKETS, SAMPLE_POLICY, a.now or SAMPLE_NOW
        else:
            if not (a.tickets and a.policy):
                raise ValueError("give --tickets and --policy, or --sample")
            with open(a.tickets, encoding="utf-8-sig") as fh:
                text = fh.read()
            with open(a.policy, encoding="utf-8") as fh:
                policy = json.load(fh)
            now_raw = a.now
        if not 0 < a.target <= 1:
            raise ValueError("--target must be in (0, 1]")
        tz = parse_offset(policy.get("timezone_offset", "+00:00"))
        now = parse_ts(now_raw, tz) if now_raw else dt.datetime.now(tz)
        res = analyse(text, policy, now, a.target, a.risk_hours, a.reopen_breaches)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT["BAD_INPUT"]
    print(json.dumps(res, indent=2) if a.output == "json" else render(res))
    return EXIT[res["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
