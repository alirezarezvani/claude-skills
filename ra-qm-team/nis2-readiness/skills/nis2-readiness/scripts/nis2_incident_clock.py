#!/usr/bin/env python3
"""Decide whether a NIS2 incident is significant and run the Article 23 reporting clock.

Essential and important entities notify their CSIRT or competent authority of
every significant incident (Directive (EU) 2022/2555 Art 23). The clock runs
from the moment the entity becomes aware of the significant incident. This
script reads an incident log and says, per incident, whether it is
significant, which report is due when, which is late, and what each report
must contain. It never decides "not significant" on missing data.

Significance
  general test (Art 23(3)): severe operational disruption of services or financial loss for the
    entity, or considerable material or non-material damage to other persons (actual or capable of)
  digital infrastructure and digital providers (Implementing Regulation (EU) 2024/2690 Art 3, applies to
    DNS, TLD, cloud, data centre, CDN, MSP, MSSP, marketplaces, search engines, social networks,
    trust services): any of
      direct financial loss > EUR 500 000 or 5% of last year's turnover, whichever is lower   Art 3(1)(a)
      exfiltration of trade secrets (caused or capable of)                                    Art 3(1)(b)
      death of a natural person (caused or capable of)                                        Art 3(1)(c)
      considerable damage to a natural person's health (caused or capable of)                 Art 3(1)(d)
      successful, suspected malicious, unauthorised access capable of severe disruption       Art 3(1)(e)
      recurring: same apparent root cause at least twice in six months, jointly meeting (a)   Art 3(1)(f), Art 4
        (the script cannot aggregate: answer yes only after checking the joint financial-loss test yourself)
      a service-specific threshold of Arts 5-14 (column sector_threshold_met)                 Art 3(1)(g)
  Scheduled maintenance and planned interruptions are not significant (Art 3(2)).

Deadlines (Art 23(4))
  early warning      24 h after awareness; say whether unlawful/malicious acts are suspected and
                     whether cross-border impact is possible                                 (a)
  notification       72 h after awareness (24 h for trust service providers on trust-service
                     incidents); update, initial severity and impact assessment, IoCs        (b), 2nd subpara
  intermediate       only on request of the CSIRT or authority                              (c)
  final report       one month after the notification: description, severity, impact, root
                     cause, mitigation, cross-border impact                                  (d)
  progress report    if handling is still ongoing when the final report is due; the final
                     report then follows within one month after handling ends               (e)
  recipients         notify service recipients without undue delay where the incident is
                     likely to adversely affect their services (Art 23(1)); communicate
                     protective measures for significant cyber threats (Art 23(2))

Incident CSV columns (timestamps ISO 8601 with offset):
  id, entity, category (essential|important), digital_provider (yes|no), trust_service (yes|no),
  detected_at, aware_at, significant (yes|no|blank to compute), severe_disruption, damage_to_others,
  financial_loss_eur, annual_turnover_eur, trade_secret_exfiltration, death, health_damage,
  malicious_access_severe, recurring, sector_threshold_met, scheduled_maintenance,
  early_warning_at, notification_at, final_report_at, progress_report_at, handling_concluded_at,
  recipients_informed_at, malicious_suspected (yes|no|unknown), cross_border (yes|no|unknown),
  severity_impact, root_cause, mitigation

Deterministic, stdlib only, no network; submits nothing. National transpositions can add detail
(Germany: BSIG section 32, report via the BSI portal).

Exit codes:
    0  every due report sent on time, nothing open
    2  reports pending or findings below BLOCKER
    3  invalid input
    4  overdue report, awareness not recorded, or significance undetermined after 24 h
"""

import argparse
import calendar
import csv
import datetime as dt
import io
import json
import sys

UTC = dt.timezone.utc
H24, H72 = dt.timedelta(hours=24), dt.timedelta(hours=72)
YES = {"yes", "y", "true", "1"}
NO = {"no", "n", "false", "0"}
SEVERITY_ORDER = ["BLOCKER", "HIGH", "MEDIUM", "INFO"]
REQUIRED = {
    "early_warning": [("malicious_suspected", "whether unlawful or malicious acts are suspected (Art 23(4)(a))"),
                      ("cross_border", "whether a cross-border impact is possible (Art 23(4)(a))")],
    "notification": [("severity_impact", "initial assessment of severity and impact, IoCs where available (Art 23(4)(b))")],
    "final_report": [("severity_impact", "detailed description, severity and impact (Art 23(4)(d)(i))"),
                     ("root_cause", "type of threat or root cause (Art 23(4)(d)(ii))"),
                     ("mitigation", "applied and ongoing mitigation measures (Art 23(4)(d)(iii))")],
}

SAMPLE = """id,entity,category,digital_provider,trust_service,detected_at,aware_at,significant,severe_disruption,damage_to_others,financial_loss_eur,annual_turnover_eur,trade_secret_exfiltration,death,health_damage,malicious_access_severe,recurring,sector_threshold_met,scheduled_maintenance,early_warning_at,notification_at,final_report_at,progress_report_at,handling_concluded_at,recipients_informed_at,malicious_suspected,cross_border,severity_impact,root_cause,mitigation
INC-41,CloudNest SaaS GmbH,important,yes,no,2026-11-14T02:10:00+01:00,2026-11-14T07:30:00+01:00,,,,40000,14000000,no,no,no,yes,no,no,no,2026-11-14T18:00:00+01:00,,,,,,yes,unknown,,,
INC-42,Stadtwerke Nord GmbH,essential,no,no,2026-11-16T21:00:00+01:00,2026-11-16T23:15:00+01:00,,yes,,,,,,,,,,,,,,,,,,,,,
INC-43,OrthoParts Manufacturing,important,no,no,2026-11-15T09:00:00+01:00,,,,,,,,,,,,,,,,,,,,,,,,
INC-44,TrustSign QTSP,essential,yes,yes,2026-10-01T10:00:00+02:00,2026-10-01T12:00:00+02:00,yes,,,,,,,,,,,,2026-10-01T20:00:00+02:00,2026-10-02T09:00:00+02:00,2026-10-30T16:00:00+01:00,,2026-10-05T12:00:00+02:00,2026-10-01T15:00:00+02:00,no,no,certificate issuance halted 3 h,HSM firmware fault,firmware rollback; vendor fix
INC-45,CloudNest SaaS GmbH,important,yes,no,2026-11-12T08:00:00+01:00,2026-11-12T09:00:00+01:00,,,,,,,,,,,,yes,,,,,,,,,,,
"""

RULES_VERIFIED = "2026-11-17"  # bump after re-checking the cited articles


def norm(v):
    return (v or "").strip()


def flag(row, col):
    v = norm(row.get(col)).lower()
    if not v:
        return None
    if v in YES:
        return True
    if v in NO:
        return False
    raise ValueError(f"{col}: '{row.get(col)}' is not yes/no (leave it blank if not assessed)")


def parse_ts(v, field):
    v = norm(v)
    if not v:
        return None
    try:
        t = dt.datetime.fromisoformat(v.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError(f"{field}: '{v}' is not an ISO 8601 timestamp")
    if t.tzinfo is None:
        raise ValueError(f"{field}: '{v}' has no UTC offset; a 24-hour clock needs one")
    return t


def num(v, field):
    v = norm(v)
    if not v:
        return None
    try:
        return float(v)
    except ValueError:
        raise ValueError(f"{field}: '{v}' is not a number")


def add_month(t):
    y, m = (t.year + 1, 1) if t.month == 12 else (t.year, t.month + 1)
    return t.replace(year=y, month=m, day=min(t.day, calendar.monthrange(y, m)[1]))


def fmt(t):
    return t.astimezone(UTC).strftime("%Y-%m-%d %H:%M UTC") if t else "-"


def hours(d):
    return round(d.total_seconds() / 3600, 1)


def significance(row, line):
    """Return (True|False|None, reasons, basis)."""
    stated = norm(row.get("significant")).lower()
    if stated in YES:
        return True, ["stated significant"], "stated"
    if flag(row, "scheduled_maintenance"):
        return False, ["scheduled maintenance or planned interruption (2024/2690 Art 3(2))"], "2024/2690 Art 3(2)"
    reasons, unknown = [], 0
    if flag(row, "digital_provider"):
        loss = num(row.get("financial_loss_eur"), f"row {line} financial_loss_eur")
        turnover = num(row.get("annual_turnover_eur"), f"row {line} annual_turnover_eur")
        if loss is not None:
            cap = min(500000, 0.05 * turnover) if turnover else 500000
            if loss > cap:
                reasons.append(f"direct financial loss EUR {loss:,.0f} > EUR {cap:,.0f} (Art 3(1)(a))")
        else:
            unknown += 1
        for col, ref in (("trade_secret_exfiltration", "Art 3(1)(b)"), ("death", "Art 3(1)(c)"),
                         ("health_damage", "Art 3(1)(d)"), ("malicious_access_severe", "Art 3(1)(e)"),
                         ("recurring", "Art 3(1)(f), Art 4"), ("sector_threshold_met", "Art 3(1)(g), Arts 5-14")):
            f = flag(row, col)
            if f:
                reasons.append(f"{col.replace('_', ' ')} ({ref})")
            elif f is None:
                unknown += 1
        basis = "Implementing Regulation (EU) 2024/2690"
    else:
        for col, ref in (("severe_disruption", "severe operational disruption or financial loss (Art 23(3)(a))"),
                         ("damage_to_others", "considerable damage to other persons (Art 23(3)(b))")):
            f = flag(row, col)
            if f:
                reasons.append(ref)
            elif f is None:
                unknown += 1
        basis = "Directive (EU) 2022/2555 Art 23(3)"
    if reasons:
        return True, reasons, basis
    if stated in NO and unknown == 0:
        return False, ["no criterion met"], basis
    if unknown:
        return None, [f"{unknown} criteria not assessed"], basis
    return False, ["no criterion met"], basis


def evaluate(row, line, now, warn):
    iid = norm(row.get("id")) or f"row {line}"
    cat = norm(row.get("category")).lower()
    if cat not in {"essential", "important"}:
        raise ValueError(f"row {line} ({iid}): category must be essential or important (run nis2_scope_classifier.py first)")
    ts = {c: parse_ts(row.get(c), f"row {line} {c}") for c in
          ("detected_at", "aware_at", "early_warning_at", "notification_at", "final_report_at",
           "progress_report_at", "handling_concluded_at", "recipients_informed_at")}
    findings, reports = [], []

    def add(sev, code, msg, ref):
        findings.append({"severity": sev, "code": code, "message": msg, "ref": ref})

    sig, why, basis = significance(row, line)
    inc = {"id": iid, "entity": norm(row.get("entity")), "category": cat, "significant": sig,
           "significance_basis": basis, "significance_reasons": why, "clock_start": None,
           "clock_basis": None, "reports": reports, "findings": findings}

    start, cbasis = ts["aware_at"], "awareness"
    if start is None:
        if ts["detected_at"] is None:
            raise ValueError(f"row {line} ({iid}): needs aware_at or at least detected_at")
        start, cbasis = ts["detected_at"], "detection (awareness not recorded)"
    if ts["detected_at"] and ts["aware_at"] and ts["aware_at"] < ts["detected_at"]:
        raise ValueError(f"row {line} ({iid}): aware_at is before detected_at")
    for c in ("early_warning_at", "notification_at", "final_report_at", "progress_report_at",
              "handling_concluded_at", "recipients_informed_at"):
        if ts[c] and ts[c] < start:
            raise ValueError(f"row {line} ({iid}): {c} is before the clock start ({cbasis})")
    for a_, b_ in (("early_warning_at", "notification_at"), ("notification_at", "final_report_at"), ("notification_at", "progress_report_at")):
        if ts[a_] and ts[b_] and ts[b_] < ts[a_]:
            raise ValueError(f"row {line} ({iid}): {b_} is before {a_}")
    future = [c for c in ts if ts[c] and ts[c] > now]

    if sig is False:
        add("INFO", "NOT_SIGNIFICANT", f"not significant under {basis}: {'; '.join(why)}. Keep the assessment; a voluntary notification is possible (Art 30)", basis)
        return inc
    if sig is None:
        sev = "BLOCKER" if now - start > H24 else "HIGH"
        add(sev, "SIGNIFICANCE_UNDETERMINED", f"{'; '.join(why)}. The deadlines below are shown as if significant; decide now, because the 24-hour clock does not wait for the assessment", basis)
    if ts["aware_at"] is None:
        add("BLOCKER", "AWARENESS_NOT_RECORDED", "no awareness timestamp: the clock is run from detection. Record when you established, with reasonable certainty, that a significant incident occurred", "Art 23(4)")
    inc["clock_start"], inc["clock_basis"] = start.isoformat(), cbasis
    if future:
        add("MEDIUM", "FUTURE_TIMESTAMP", f"{', '.join(future)} after the evaluation time; check the log or --as-of", "data quality")

    trust = flag(row, "trust_service")
    notif_window = H24 if trust else H72
    plan = [("early_warning", start + H24, "Art 23(4)(a)"),
            ("notification", start + notif_window, "Art 23(4)(b)" + (", 2nd subpara (trust service: 24 h)" if trust else ""))]
    sent_n = ts["notification_at"]
    final_due = add_month(sent_n) if sent_n else None
    concluded = ts["handling_concluded_at"]
    if final_due and (concluded is None or concluded > final_due) and not ts["final_report_at"]:
        plan.append(("progress_report", final_due, "Art 23(4)(e)"))
        plan.append(("final_report", add_month(concluded) if concluded else None, "Art 23(4)(e)"))
    else:
        plan.append(("final_report", final_due, "Art 23(4)(d)"))

    for name, due, ref in plan:
        sent = ts.get(f"{name}_at")
        r = {"report": name, "due": due.isoformat() if due else None, "sent": sent.isoformat() if sent else None, "ref": ref}
        if sent and due and sent > due:
            r["status"] = "LATE"
            add("HIGH", "LATE", f"{name} sent {hours(sent - due)} h after the deadline; record why", ref)
        elif sent:
            r["status"] = "ON_TIME"
        elif due is None:
            r["status"] = "WAITING"
            r["waiting_for"] = "end of incident handling" if name == "final_report" and sent_n else "incident notification"
        elif now > due:
            r["status"] = "OVERDUE"
            add("BLOCKER", "OVERDUE", f"{name} was due {fmt(due)}, {hours(now - due)} h ago; send it now and say why it is late", ref)
        else:
            r["status"] = "DUE"
            r["hours_left"] = hours(due - now)
            if due - now <= warn:
                add("MEDIUM", "DUE_SOON", f"{name} due {fmt(due)} ({hours(due - now)} h left)", ref)
        if sent and name in REQUIRED:
            for col, desc in REQUIRED[name]:
                v = norm(row.get(col)).lower()
                if not v:
                    add("HIGH", "MISSING_CONTENT", f"{name}: no record of {desc}", ref)
        reports.append(r)

    if ts["recipients_informed_at"] is None:
        add("MEDIUM", "RECIPIENTS_NOT_INFORMED", "no record that service recipients likely to be adversely affected were told; decide and record it", "Art 23(1)")
    return inc


def run(text, now, warn):
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise ValueError("incident log has no rows")
    incs = [evaluate(r, i + 2, now, warn) for i, r in enumerate(rows)]
    counts = {s: 0 for s in SEVERITY_ORDER}
    pending = 0
    for x in incs:
        for f in x["findings"]:
            counts[f["severity"]] += 1
        pending += sum(1 for r in x["reports"] if r["status"] in {"DUE", "WAITING"})
    verdict = "OVERDUE" if counts["BLOCKER"] else "OPEN" if pending or counts["HIGH"] or counts["MEDIUM"] else "ON_TIME"
    return {"verdict": verdict, "as_of": now.isoformat(),
            "summary": {"incidents": len(incs), "significant": sum(1 for x in incs if x["significant"]),
                        "undetermined": sum(1 for x in incs if x["significant"] is None),
                        "pending_reports": pending, "findings": counts},
            "incidents": incs}


def render(out):
    lines = [f"NIS2 Article 23 clock: {out['verdict']}  (as of {fmt(dt.datetime.fromisoformat(out['as_of']))})", ""]
    for x in out["incidents"]:
        s = {True: "significant", False: "not significant", None: "UNDETERMINED"}[x["significant"]]
        lines.append(f"- {x['id']} {x['entity']} [{x['category']}]: {s} ({x['significance_basis']}: {'; '.join(x['significance_reasons'])})")
        if x["clock_start"]:
            lines.append(f"    clock from {x['clock_basis']}: {fmt(dt.datetime.fromisoformat(x['clock_start']))}")
        for r in x["reports"]:
            due = fmt(dt.datetime.fromisoformat(r["due"])) if r["due"] else f"after {r.get('waiting_for', '?')}"
            extra = f", {r['hours_left']} h left" if "hours_left" in r else ""
            lines.append(f"    {r['report']:<15} {r['status']:<8} due {due}{extra}  [{r['ref']}]")
        for f in sorted(x["findings"], key=lambda f: SEVERITY_ORDER.index(f["severity"])):
            lines.append(f"    {f['severity']:<7} {f['code']}: {f['message']} [{f['ref']}]")
    s = out["summary"]
    lines += ["", f"{s['incidents']} incidents, {s['significant']} significant, {s['undetermined']} undetermined, "
              f"{s['pending_reports']} reports pending. Findings: " + ", ".join(f"{k} {v}" for k, v in s["findings"].items()),
              "Send to the CSIRT or competent authority of the supervising Member State; intermediate reports only on request (Art 23(4)(c))."]
    lines += ["", f"Rules last verified {RULES_VERIFIED}. Not legal advice: confirm with counsel or the competent authority."]
    return "\n".join(lines)


EXIT = {"ON_TIME": 0, "OPEN": 2, "OVERDUE": 4}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog="Exit codes: 0 on time, 2 open (includes a report sent late: LATE is recorded, not blocking), 3 invalid input (also a report timestamp before the clock start), 4 overdue, awareness not recorded, or significance undetermined after 24 h.")
    p.add_argument("--incidents", help="incident log CSV (columns in the module docstring)")
    p.add_argument("--as-of", help="evaluation time, ISO 8601 with offset (default: now)")
    p.add_argument("--warn-hours", type=float, default=12, help="flag reports due within this many hours (default 12)")
    p.add_argument("--sample", action="store_true", help="run on a built-in example log")
    p.add_argument("--output", choices=["text", "json"], default="text")
    p.add_argument("--json", action="store_true", help="shorthand for --output json")
    a = p.parse_args(argv)
    if a.json:
        a.output = "json"
    try:
        if a.sample:
            text, now = SAMPLE, dt.datetime(2026, 11, 17, 8, 0, tzinfo=UTC)
        else:
            if not a.incidents:
                p.print_usage(sys.stderr)
                print("error: give --incidents or --sample", file=sys.stderr)
                return 3
            with open(a.incidents, newline="", encoding="utf-8-sig") as fh:
                text = fh.read()
            now = parse_ts(a.as_of, "--as-of") or dt.datetime.now(UTC)
        if a.warn_hours < 0:
            raise ValueError("--warn-hours must not be negative")
        out = run(text, now, dt.timedelta(hours=a.warn_hours))
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
