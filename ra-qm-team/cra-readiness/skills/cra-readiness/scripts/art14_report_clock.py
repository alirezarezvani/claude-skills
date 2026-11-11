#!/usr/bin/env python3
"""Run the Article 14 reporting clock for CRA vulnerabilities and severe incidents.

Since 11 September 2026 (Art 71(2)) a manufacturer must report every actively
exploited vulnerability and every severe incident affecting the security of a
product with digital elements to the CSIRT designated as coordinator and ENISA,
through the Single Reporting Platform. The clock starts when the manufacturer
becomes aware. This script reads an event log and says, per event, which
report is due when, which is late, and what the report must contain.

Deadlines (Regulation (EU) 2024/2847)
  actively exploited vulnerability (Art 14(2))
    early warning   24 hours after awareness            (a)
    notification    72 hours after awareness            (b)
    final report    14 days after a corrective or mitigating measure is available   (c)
  severe incident (Art 14(4))
    early warning   24 hours after awareness            (a)  must say if unlawful/malicious acts are suspected
    notification    72 hours after awareness            (b)
    final report    one month after the incident notification was submitted        (c)
  users (Art 14(8))  inform impacted users, and where appropriate all users, after awareness

Findings
  OVERDUE               a report whose deadline has passed and that was not sent              BLOCKER
  AWARENESS_NOT_RECORDED  no awareness timestamp: the clock runs from detection instead       BLOCKER
  LATE                  a report sent after its deadline: record why                          HIGH
  USERS_NOT_INFORMED    corrective measure available but users not informed (Art 14(8))       HIGH
  MISSING_CONTENT       a required field for a sent report is blank                           HIGH
  DUE_SOON              a report due inside --warn-hours                                       MEDIUM
  SLOW_ASSESSMENT       more than 24 hours from detection to awareness: document the triage    MEDIUM
  NOT_REPORTABLE        aware before 11 Sep 2026, or a component flaw not exploited in your product  INFO

Event CSV columns (timestamps ISO 8601 with offset, e.g. 2026-11-03T09:15:00+01:00):
  id, kind (vulnerability|incident), product, detected_at, aware_at, early_warning_at,
  notification_at, corrective_available_at, final_report_at, users_informed_at,
  exploited_in_product (yes|no), malicious_suspected (yes|no|unknown), member_states,
  corrective_measures, severity_impact, root_cause

"Aware" follows the Commission guidance C(2026) 5252: an initial assessment
has reached a reasonable degree of certainty. The Single Reporting Platform does
not record that moment, so your own log is the evidence.

Deterministic, stdlib only, no network; it does not submit anything.

Exit codes:
    0  every due report sent on time, nothing open
    2  reports pending or findings below BLOCKER
    3  invalid input
    4  OVERDUE or awareness not recorded
"""

import argparse
import calendar
import csv
import datetime as dt
import io
import json
import sys

UTC = dt.timezone.utc
IN_FORCE_DATE = dt.date(2026, 9, 11)  # Art 71(2), compared on the local date of awareness
H24, H72 = dt.timedelta(hours=24), dt.timedelta(hours=72)
D14 = dt.timedelta(days=14)
YES = {"yes", "y", "true", "1"}
NO = {"no", "n", "false", "0"}
SEVERITY_ORDER = ["BLOCKER", "HIGH", "MEDIUM", "INFO"]

REQUIRED_CONTENT = {
    ("vulnerability", "early_warning"): ["member_states"],
    ("vulnerability", "notification"): ["corrective_measures"],
    ("vulnerability", "final_report"): ["severity_impact", "corrective_measures"],
    ("incident", "early_warning"): ["malicious_suspected", "member_states"],
    ("incident", "notification"): ["corrective_measures"],
    ("incident", "final_report"): ["severity_impact", "root_cause", "corrective_measures"],
}
CONTENT_REF = {
    "member_states": "Member States where the product is made available (Art 14(2)(a), 14(4)(a))",
    "malicious_suspected": "whether unlawful or malicious acts are suspected (Art 14(4)(a))",
    "corrective_measures": "corrective or mitigating measures taken and those users can take (Art 14(2)(b), 14(4)(b))",
    "severity_impact": "severity and impact (Art 14(2)(c), 14(4)(c))",
    "root_cause": "type of threat or root cause (Art 14(4)(c)(ii))",
}

SAMPLE = """id,kind,product,detected_at,aware_at,early_warning_at,notification_at,corrective_available_at,final_report_at,users_informed_at,exploited_in_product,malicious_suspected,member_states,corrective_measures,severity_impact,root_cause
VULN-2026-014,vulnerability,Clinic Gateway Router,2026-10-02T08:10:00+02:00,2026-10-02T15:40:00+02:00,2026-10-03T09:00:00+02:00,2026-10-04T17:30:00+02:00,2026-10-09T12:00:00+02:00,2026-10-20T10:00:00+02:00,2026-10-09T16:00:00+02:00,yes,,DE AT NL,firmware 4.2.1; disable remote admin,CVSS 9.8 RCE on WAN admin,
VULN-2026-019,vulnerability,GaitCam Home,2026-11-07T22:05:00+01:00,2026-11-09T11:00:00+01:00,2026-11-09T19:00:00+01:00,,,,,yes,,DE,,,
INC-2026-003,incident,GaitCam Home,2026-11-08T06:00:00+01:00,,,,,,,,unknown,DE,,,
VULN-2026-020,vulnerability,Sensor SDK v3,2026-11-05T10:00:00+01:00,2026-11-05T12:00:00+01:00,,,,,,no,,,,,
VULN-2026-007,vulnerability,Clinic Gateway Router,2026-08-20T09:00:00+02:00,2026-08-21T09:00:00+02:00,,,,,,yes,,DE,,,
"""


def norm(v):
    return (v or "").strip()


def parse_ts(v, field):
    v = norm(v)
    if not v:
        return None
    try:
        t = dt.datetime.fromisoformat(v.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError(f"{field}: '{v}' is not an ISO 8601 timestamp")
    if t.tzinfo is None:
        raise ValueError(f"{field}: '{v}' has no UTC offset; a 24-hour clock needs one (e.g. +01:00 or Z)")
    return t


def add_month(t):
    """Same day next month, clamped to the month's last day (Art 14(4)(c): 'within one month')."""
    y, m = (t.year + 1, 1) if t.month == 12 else (t.year, t.month + 1)
    return t.replace(year=y, month=m, day=min(t.day, calendar.monthrange(y, m)[1]))


def fmt(t):
    return t.astimezone(UTC).strftime("%Y-%m-%d %H:%M UTC") if t else "-"


def hours(delta):
    return round(delta.total_seconds() / 3600, 1)


def evaluate(row, line, now, warn, small):
    eid = norm(row.get("id")) or f"row {line}"
    kind = norm(row.get("kind")).lower()
    if kind not in {"vulnerability", "incident"}:
        raise ValueError(f"row {line} ({eid}): kind must be vulnerability or incident")
    ts = {c: parse_ts(row.get(c), f"row {line} {c}") for c in
          ("detected_at", "aware_at", "early_warning_at", "notification_at",
           "corrective_available_at", "final_report_at", "users_informed_at")}
    findings, reports = [], []

    def add(sev, code, msg, ref):
        findings.append({"severity": sev, "code": code, "message": msg, "ref": ref})

    ev = {"id": eid, "kind": kind, "product": norm(row.get("product")), "reportable": True,
          "clock_start": None, "clock_basis": None, "reports": reports, "findings": findings}

    if kind == "vulnerability" and norm(row.get("exploited_in_product")).lower() in NO:
        ev["reportable"] = False
        add("INFO", "NOT_REPORTABLE", "no reliable evidence that a malicious actor exploited it in your product, so it is not an actively exploited vulnerability: fix it under Annex I Part II, tell the component maintainer if it sits in a third-party component (Art 13(6)); a voluntary report is possible (Art 15)", "Art 3(42), Art 13(6), Art 15")
        return ev

    start, basis = ts["aware_at"], "awareness"
    if start is None:
        if ts["detected_at"] is None:
            raise ValueError(f"row {line} ({eid}): needs aware_at or at least detected_at")
        start, basis = ts["detected_at"], "detection (awareness not recorded)"
        add("BLOCKER", "AWARENESS_NOT_RECORDED", "no awareness timestamp; the clock is run from detection, the earliest moment an authority could argue. Record when the initial assessment reached reasonable certainty", "Art 14(2), 14(4); Commission guidance C(2026) 5252")
    elif ts["detected_at"] and start - ts["detected_at"] > H24:
        add("MEDIUM", "SLOW_ASSESSMENT", f"{hours(start - ts['detected_at'])} h from detection to awareness; keep the triage record that shows why", "Commission guidance C(2026) 5252")
    if ts["detected_at"] and start < ts["detected_at"]:
        raise ValueError(f"row {line} ({eid}): aware_at is before detected_at")
    ev["clock_start"], ev["clock_basis"] = start.isoformat(), basis

    if start.date() < IN_FORCE_DATE:
        ev["reportable"] = False
        add("INFO", "NOT_REPORTABLE", "awareness before 11 Sep 2026, when Article 14 did not yet apply. Exploitation that first becomes known on or after that date is reportable", "Art 71(2)")
        return ev

    para = "14(2)" if kind == "vulnerability" else "14(4)"
    plan = [("early_warning", start + H24, f"Art {para}(a)"), ("notification", start + H72, f"Art {para}(b)")]
    if kind == "vulnerability":
        fix = ts["corrective_available_at"]
        plan.append(("final_report", fix + D14 if fix else None, f"Art {para}(c)"))
    else:
        sent = ts["notification_at"]
        plan.append(("final_report", add_month(sent) if sent else None, f"Art {para}(c)"))

    for name, due, ref in plan:
        sent = ts[f"{name}_at"]
        r = {"report": name, "due": due.isoformat() if due else None, "sent": sent.isoformat() if sent else None, "ref": ref}
        if sent and due and sent > due:
            r["status"] = "LATE"
            note = " (micro or small enterprise: Art 64(10)(a) excludes fines for this 24-hour deadline, the duty itself stands)" if name == "early_warning" and small else ""
            add("HIGH", "LATE", f"{name} sent {hours(sent - due)} h after the deadline{note}", ref)
        elif sent:
            r["status"] = "ON_TIME"
        elif due is None:
            r["status"] = "WAITING"
            r["waiting_for"] = "corrective or mitigating measure" if kind == "vulnerability" else "incident notification"
        elif now > due:
            r["status"] = "OVERDUE"
            note = " Art 64(10)(a) excludes fines for micro and small enterprises on this 24-hour deadline; send it now anyway." if name == "early_warning" and small else ""
            add("BLOCKER", "OVERDUE", f"{name} was due {fmt(due)}, {hours(now - due)} h ago.{note}", ref)
        else:
            r["status"] = "DUE"
            r["hours_left"] = hours(due - now)
            if due - now <= warn:
                add("MEDIUM", "DUE_SOON", f"{name} due {fmt(due)} ({hours(due - now)} h left)", ref)
        if sent:
            for col in REQUIRED_CONTENT[(kind, name)]:
                val = norm(row.get(col)).lower()
                if not val or (col == "malicious_suspected" and val not in YES | NO | {"unknown"}):
                    add("HIGH", "MISSING_CONTENT", f"{name}: no record of {CONTENT_REF[col]}", ref)
        reports.append(r)

    if ts["users_informed_at"] is None and ts["corrective_available_at"] is not None:
        add("HIGH", "USERS_NOT_INFORMED", "a corrective or mitigating measure exists but impacted users have not been informed; use a structured, machine-readable advisory where appropriate", "Art 14(8)")
    return ev


def run(text, now, warn, small):
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise ValueError("event log has no rows")
    events = [evaluate(r, i + 2, now, warn, small) for i, r in enumerate(rows)]
    counts = {s: 0 for s in SEVERITY_ORDER}
    pending = 0
    for e in events:
        for f in e["findings"]:
            counts[f["severity"]] += 1
        pending += sum(1 for r in e["reports"] if r["status"] in {"DUE", "WAITING"})
    verdict = "OVERDUE" if counts["BLOCKER"] else "OPEN" if pending or counts["HIGH"] or counts["MEDIUM"] else "ON_TIME"
    return {"verdict": verdict, "as_of": now.isoformat(), "small_enterprise": small,
            "summary": {"events": len(events), "reportable": sum(e["reportable"] for e in events),
                        "pending_reports": pending, "findings": counts},
            "events": events}


def render(out):
    lines = [f"Article 14 clock: {out['verdict']}  (as of {fmt(dt.datetime.fromisoformat(out['as_of']))})", ""]
    for e in out["events"]:
        lines.append(f"- {e['id']} [{e['kind']}] {e['product']}" + ("" if e["reportable"] else "  (not reportable)"))
        if e["clock_start"]:
            lines.append(f"    clock from {e['clock_basis']}: {fmt(dt.datetime.fromisoformat(e['clock_start']))}")
        for r in e["reports"]:
            due = fmt(dt.datetime.fromisoformat(r["due"])) if r["due"] else f"after {r.get('waiting_for', '?')}"
            extra = f", {r['hours_left']} h left" if "hours_left" in r else ""
            lines.append(f"    {r['report']:<13} {r['status']:<8} due {due}{extra}  [{r['ref']}]")
        for f in sorted(e["findings"], key=lambda f: SEVERITY_ORDER.index(f["severity"])):
            lines.append(f"    {f['severity']:<7} {f['code']}: {f['message']} [{f['ref']}]")
    s = out["summary"]
    lines += ["", f"{s['events']} events, {s['reportable']} reportable, {s['pending_reports']} reports pending. "
              "Findings: " + ", ".join(f"{k} {v}" for k, v in s["findings"].items()),
              "Submit through the ENISA Single Reporting Platform to the CSIRT designated as coordinator (Art 14(7), Art 16)."]
    return "\n".join(lines)


EXIT = {"ON_TIME": 0, "OPEN": 2, "OVERDUE": 4}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog="Exit codes: 0 on time, 2 open, 3 invalid input, 4 overdue.")
    p.add_argument("--events", help="event log CSV (columns in the module docstring)")
    p.add_argument("--as-of", help="evaluation time, ISO 8601 with offset (default: now)")
    p.add_argument("--warn-hours", type=float, default=12, help="flag reports due within this many hours (default 12)")
    p.add_argument("--small-enterprise", action="store_true",
                   help="manufacturer is a micro or small enterprise (notes Art 64(10)(a) on the 24-hour deadline)")
    p.add_argument("--sample", action="store_true", help="run on a built-in example log")
    p.add_argument("--output", choices=["text", "json"], default="text")
    p.add_argument("--json", action="store_true", help="shorthand for --output json")
    a = p.parse_args(argv)
    if a.json:
        a.output = "json"
    try:
        if a.sample:
            text, now = SAMPLE, dt.datetime(2026, 11, 10, 9, 0, tzinfo=UTC)
        else:
            if not a.events:
                p.print_usage(sys.stderr)
                print("error: give --events or --sample", file=sys.stderr)
                return 3
            with open(a.events, newline="", encoding="utf-8-sig") as fh:
                text = fh.read()
            now = parse_ts(a.as_of, "--as-of") or dt.datetime.now(UTC)
        if a.warn_hours < 0:
            raise ValueError("--warn-hours must not be negative")
        out = run(text, now, dt.timedelta(hours=a.warn_hours), a.small_enterprise)
    except (OSError, ValueError, csv.Error) as e:
        if a.output == "json":
            print(json.dumps({"verdict": "INVALID_INPUT", "errors": [str(e)]}, indent=2))
        else:
            print(f"error: {e}", file=sys.stderr)
        return 3
    print(json.dumps(out, indent=2) if a.output == "json" else render(out))
    return EXIT[out["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
