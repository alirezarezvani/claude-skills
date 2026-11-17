#!/usr/bin/env python3
"""Classify ICT-related incidents as major under DORA and run the reporting clock.

A financial entity reports every major ICT-related incident to its competent
authority (Regulation (EU) 2022/2554 Art 19). Whether an incident is major is
set by Commission Delegated Regulation (EU) 2024/1772; the deadlines by
Commission Delegated Regulation (EU) 2025/301. This script reads an incident
log, applies the classification exactly as Art 8 of 2024/1772 states it,
checks recurring incidents, and says which report is due when.

Major (2024/1772 Art 8(1)): the incident affected CRITICAL SERVICES (Art 6: ICT services supporting critical
or important functions, authorised or supervised financial services, or a successful malicious unauthorised
access) AND either
  (a) a successful, malicious, unauthorised access that may result in data losses (Art 9(5)(b)), or
  (b) two or more of the other materiality thresholds of Art 9:
      clients     > 10% of clients using the service, > 100 000 clients, > 30% of financial counterparts,
                  > 10% of daily transactions (number or value), or relevant clients affected     Art 9(1)
      reputation  media, repeated complaints, regulatory requirements missed, client loss          Art 9(2)
      duration    > 24 h, or downtime > 2 h of a service supporting a critical or important function Art 9(3)
      geography   impact in two or more Member States                                               Art 9(4)
      data        adverse impact on availability, authenticity, integrity or confidentiality       Art 9(5)(a)
      economic    costs and losses > EUR 100 000                                                    Art 9(6)
Recurring (Art 8(2)): incidents not major on their own, same apparent root cause, at least twice in six months,
  jointly meeting Art 8(1): treated as one major incident. Checked monthly; not for microenterprises or Art 16 entities.

Deadlines (2025/301 Art 5)
  initial         4 h after classification as major, and no later than 24 h after awareness; if classified
                  later than 24 h after awareness, 4 h after classification                 Art 5(1)(a), 5(2)
  intermediate    72 h after the initial notification, and again when regular activities are recovered  Art 5(1)(b)
  final           1 month after the latest intermediate report                               Art 5(1)(c)
  weekends/bank holidays: by noon of the next working day, except initial and intermediate reports of credit
  institutions, CCPs, trading venues and NIS2-identified entities                           Art 5(4)-(5)
  late: tell the authority before the deadline, with reasons                                Art 5(3)
  clients: inform affected clients without undue delay when their financial interests are hit  DORA Art 19(3)

Incident CSV columns (timestamps ISO 8601 with offset):
  id, aware_at, classified_at, critical_services (yes|no: yes if ANY Art 6 condition holds, incl. a successful
  malicious unauthorised access), malicious_access (yes|no), clients_pct, clients,
  counterparts_pct, transactions_pct, transaction_value_pct, relevant_clients (yes|no), reputational
  (semicolon list: media;complaints;regulatory;client_loss or blank), duration_h, cif_downtime_h,
  member_states (count), data_impact (yes|no), economic_eur, root_cause_id, initial_at, intermediate_at,
  intermediate_updated_at, recovered_at, final_at, clients_informed_at

Deterministic, stdlib only, no network; submits nothing.

Exit codes:
    0  nothing major, or every due report on time
    2  reports pending, or findings below BLOCKER
    3  invalid input
    4  an overdue report, or an incident still unclassified more than 24 h after awareness
"""

import argparse
import calendar
import csv
import datetime as dt
import io
import json
import sys

UTC = dt.timezone.utc
H = dt.timedelta(hours=1)
YES = {"yes", "y", "true", "1"}
NO = {"no", "n", "false", "0"}
REPUTATION = {"media": "reflected in the media", "complaints": "repeated complaints from different clients",
              "regulatory": "regulatory requirements not met", "client_loss": "likely loss of clients with material impact"}
NO_RELIEF = {"credit-institution", "ccp", "trading-venue", "nis2-identified"}
SEVERITY_ORDER = ["BLOCKER", "HIGH", "MEDIUM", "INFO"]

SAMPLE = """id,aware_at,classified_at,critical_services,malicious_access,clients_pct,clients,counterparts_pct,transactions_pct,transaction_value_pct,relevant_clients,reputational,duration_h,cif_downtime_h,member_states,data_impact,economic_eur,root_cause_id,initial_at,intermediate_at,intermediate_updated_at,recovered_at,final_at,clients_informed_at
ICT-301,2026-11-13T19:10:00+01:00,2026-11-13T21:00:00+01:00,yes,no,14,42000,,,,no,media,6,4.5,1,no,60000,RC-DNS,2026-11-14T00:30:00+01:00,,,2026-11-14T03:00:00+01:00,,
ICT-302,2026-11-16T08:20:00+01:00,,yes,yes,,,,,,,,1,0.5,1,yes,,RC-PHISH,,,,,,
ICT-303,2026-09-02T10:00:00+02:00,2026-09-02T11:00:00+02:00,yes,no,3,9000,,,,no,,30,3,2,no,250000,RC-STOR,2026-09-02T14:30:00+02:00,2026-09-05T12:00:00+02:00,,2026-09-03T18:00:00+02:00,2026-10-03T12:00:00+02:00,2026-09-02T16:00:00+02:00
ICT-304,2026-10-20T09:00:00+02:00,,yes,no,2,800,,,,no,,3,1,1,no,30000,RC-BATCH,,,,,,
ICT-305,2026-11-10T09:00:00+01:00,,yes,no,4,1200,,,,no,complaints,4,1.5,1,no,40000,RC-BATCH,,,,,,
ICT-306,2026-11-15T22:00:00+01:00,,no,no,,,,,,,,2,,1,no,,,,,,,,
"""

RULES_VERIFIED = "2026-11-17"  # bump after re-checking the cited articles


def norm(v):
    return (v or "").strip()


def b(row, col):
    v = norm(row.get(col)).lower()
    if not v:
        return None
    if v in YES:
        return True
    if v in NO:
        return False
    raise ValueError(f"{col}: '{row.get(col)}' is not yes/no (leave it blank if not assessed)")


def f(row, col, line):
    v = norm(row.get(col))
    if not v:
        return None
    try:
        return float(v)
    except ValueError:
        raise ValueError(f"row {line} {col}: '{v}' is not a number")


def ts(row, col, line):
    v = norm(row.get(col))
    if not v:
        return None
    try:
        t = dt.datetime.fromisoformat(v.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError(f"row {line} {col}: '{v}' is not ISO 8601")
    if t.tzinfo is None:
        raise ValueError(f"row {line} {col}: '{v}' needs a UTC offset")
    return t


def add_month(t):
    y, m = (t.year + 1, 1) if t.month == 12 else (t.year, t.month + 1)
    return t.replace(year=y, month=m, day=min(t.day, calendar.monthrange(y, m)[1]))


def fmt(t):
    return t.astimezone(UTC).strftime("%Y-%m-%d %H:%M UTC") if t else "-"


def thresholds(m):
    """m: dict of measures. Returns (met list, unknown count)."""
    met, unknown = [], 0
    c = []
    for key, lim, label in (("clients_pct", 10, "> 10% of clients"), ("clients", 100000, "> 100 000 clients"),
                            ("counterparts_pct", 30, "> 30% of counterparts"), ("transactions_pct", 10, "> 10% of daily transactions"),
                            ("transaction_value_pct", 10, "> 10% of daily transaction value")):
        if m.get(key) is not None and m[key] > lim:
            c.append(label)
    if m.get("relevant_clients"):
        c.append("relevant clients or counterparts affected")
    if c:
        met.append(("clients", "Art 9(1)", ", ".join(c)))
    elif m.get("clients_pct") is None and m.get("clients") is None:
        unknown += 1
    if m.get("reputational"):
        met.append(("reputation", "Art 9(2)", ", ".join(REPUTATION[r] for r in m["reputational"])))
    d = []
    if m.get("duration_h") is not None and m["duration_h"] > 24:
        d.append(f"duration {m['duration_h']:g} h > 24 h")
    if m.get("cif_downtime_h") is not None and m["cif_downtime_h"] > 2:
        d.append(f"downtime {m['cif_downtime_h']:g} h > 2 h on a critical or important function")
    if d:
        met.append(("duration", "Art 9(3)", ", ".join(d)))
    elif m.get("duration_h") is None:
        unknown += 1
    if m.get("member_states") is not None and m["member_states"] >= 2:
        met.append(("geography", "Art 9(4)", f"{m['member_states']:g} Member States"))
    if m.get("data_impact"):
        met.append(("data", "Art 9(5)(a)", "adverse impact on data"))
    elif m.get("data_impact") is None:
        unknown += 1
    if m.get("economic_eur") is not None and m["economic_eur"] > 100000:
        met.append(("economic", "Art 9(6)", f"EUR {m['economic_eur']:,.0f} > EUR 100 000"))
    elif m.get("economic_eur") is None:
        unknown += 1
    return met, unknown


def measures(row, line):
    rep = [r.strip().lower() for r in norm(row.get("reputational")).replace(",", ";").split(";") if r.strip()]
    bad = [r for r in rep if r not in REPUTATION]
    if bad:
        raise ValueError(f"row {line} reputational: unknown '{', '.join(bad)}' (media, complaints, regulatory, client_loss)")
    return {"critical_services": b(row, "critical_services"), "malicious_access": b(row, "malicious_access"),
            "clients_pct": f(row, "clients_pct", line), "clients": f(row, "clients", line),
            "counterparts_pct": f(row, "counterparts_pct", line), "transactions_pct": f(row, "transactions_pct", line),
            "transaction_value_pct": f(row, "transaction_value_pct", line), "relevant_clients": b(row, "relevant_clients"),
            "reputational": rep, "duration_h": f(row, "duration_h", line), "cif_downtime_h": f(row, "cif_downtime_h", line),
            "member_states": f(row, "member_states", line), "data_impact": b(row, "data_impact"),
            "economic_eur": f(row, "economic_eur", line)}


def classify(m):
    if m["critical_services"] is None:
        return None, ["critical_services not assessed (Art 6)"], []
    if not m["critical_services"]:
        return False, ["critical services not affected: never major (Art 8(1))"], []
    if m["malicious_access"]:
        return True, ["critical services + successful malicious unauthorised access that may cause data loss (Art 8(1)(a), Art 9(5)(b))"], []
    met, unknown = thresholds(m)
    if len(met) >= 2:
        return True, ["critical services + " + "; ".join(f"{k} ({ref}: {d})" for k, ref, d in met)], met
    if m["malicious_access"] is None:
        return None, ["critical services affected but malicious_access not assessed; a successful malicious access alone makes it major (Art 8(1)(a))"], met
    if len(met) + unknown >= 2:
        return None, [f"critical services + {len(met)} threshold(s) met, {unknown} not assessed; two decide it"], met
    return False, [f"critical services but only {len(met)} other threshold met" + (f": {met[0][0]}" if met else "")], met


def next_working(t, holidays):
    """Noon of the next working day (local offset of t) if t falls on a weekend or holiday."""
    if t.weekday() < 5 and t.date() not in holidays:
        return t, False
    d = t
    while True:
        d = (d + dt.timedelta(days=1)).replace(hour=12, minute=0, second=0, microsecond=0)
        if d.weekday() < 5 and d.date() not in holidays:
            return d, True


def run(text, now, entity, micro, holidays, warn):
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise ValueError("incident log has no rows")
    incs = []
    for i, r in enumerate(rows):
        line = i + 2
        iid = norm(r.get("id")) or f"row {line}"
        t = {c: ts(r, c, line) for c in ("aware_at", "classified_at", "initial_at", "intermediate_at",
                                          "intermediate_updated_at", "recovered_at", "final_at", "clients_informed_at")}
        if t["aware_at"] is None:
            raise ValueError(f"row {line} ({iid}): aware_at is required")
        m = measures(r, line)
        major, why, met = classify(m)
        incs.append({"id": iid, "row": r, "t": t, "m": m, "major": major, "why": why, "met": met,
                     "root": norm(r.get("root_cause_id")), "recurring": False, "reports": [], "findings": []})

    if not micro and entity != "art16":
        groups = {}
        for x in incs:
            if x["major"] is not True and x["root"] and x["m"]["critical_services"]:
                groups.setdefault(x["root"], []).append(x)
        for root, xs in groups.items():
            xs.sort(key=lambda x: x["t"]["aware_at"])
            # Sliding window: the first incident that completes a qualifying set within 183 days
            # (Art 8(2) "at least twice within 6 months") becomes the reportable major incident.
            for anchor in xs[1:]:
                window = [x for x in xs if dt.timedelta(0) <= anchor["t"]["aware_at"] - x["t"]["aware_at"] <= dt.timedelta(days=183)]
                if len(window) < 2:
                    continue
                agg = {"critical_services": True, "malicious_access": any(x["m"]["malicious_access"] for x in window)}
                for k in ("clients", "economic_eur", "duration_h", "cif_downtime_h"):
                    vals = [x["m"][k] for x in window if x["m"][k] is not None]
                    agg[k] = sum(vals) if vals else None
                for k in ("clients_pct", "counterparts_pct", "transactions_pct", "transaction_value_pct", "member_states"):
                    vals = [x["m"][k] for x in window if x["m"][k] is not None]
                    agg[k] = max(vals) if vals else None
                agg["relevant_clients"] = any(x["m"]["relevant_clients"] for x in window)
                agg["reputational"] = sorted({r for x in window for r in x["m"]["reputational"]})
                agg["data_impact"] = any(x["m"]["data_impact"] for x in window)
                maj, why, _ = classify(agg)
                if maj:
                    last = anchor
                    last["major"], last["recurring"] = True, True
                    last["why"] = [f"RECURRING: {len(window)} incidents with root cause {root} within 6 months jointly meet Art 8(1): {why[0]} (Art 8(2)). Aggregation here sums clients, costs and durations and takes the widest share; confirm the method with your competent authority"]
                    break

    counts = {s: 0 for s in SEVERITY_ORDER}
    pending = 0
    relief_allowed = entity not in NO_RELIEF
    for x in incs:
        t, fs = x["t"], x["findings"]

        def add(sev, code, msg, ref):
            fs.append({"severity": sev, "code": code, "message": msg, "ref": ref})

        if x["major"] is None:
            sev = "BLOCKER" if now - t["aware_at"] > 24 * H else "HIGH"
            add(sev, "UNCLASSIFIED", f"{x['why'][0]}. Classify now: the initial notification is due no later than 24 h after awareness if it is major", "RTS 2024/1772 Arts 6-9; RTS 2025/301 Art 5(1)(a)")
        if x["major"] is not True:
            if x["major"] is False:
                add("INFO", "NOT_MAJOR", x["why"][0] + ". Keep the classification record; voluntary notification of significant cyber threats is possible (DORA Art 19(2))", "RTS 2024/1772 Art 8")
            x.pop("row")
            continue
        cls = t["classified_at"]
        if cls is None and x["recurring"]:
            add("HIGH", "RECURRING_MAJOR", "recurring incidents jointly meet the major criteria: classify now and record it; the initial notification is due 4 h after that classification", "RTS 2024/1772 Art 8(2); RTS 2025/301 Art 5(1)(a)")
            x["reports"].append({"report": "initial", "due": None, "sent": None, "status": "WAITING",
                                 "waiting_for": "classification (then 4 h)", "ref": "RTS 2025/301 Art 5(1)(a)"})
            x.pop("row")
            continue
        if cls is None:
            add("HIGH", "CLASSIFICATION_TIME_MISSING", "major on the data given but no classified_at; the initial clock is taken as 24 h after awareness. Record when you classified it", "RTS 2025/301 Art 5(1)(a)")
            due_init = t["aware_at"] + 24 * H
        elif cls - t["aware_at"] > 24 * H:
            due_init = cls + 4 * H
            add("MEDIUM", "LATE_CLASSIFICATION", "classified more than 24 h after awareness: initial is due 4 h after classification; keep the reasons", "RTS 2025/301 Art 5(2)")
        else:
            due_init = min(cls + 4 * H, t["aware_at"] + 24 * H)
        plan = [("initial", due_init, "RTS 2025/301 Art 5(1)(a)")]
        plan.append(("intermediate", t["initial_at"] + 72 * H if t["initial_at"] else None, "RTS 2025/301 Art 5(1)(b)"))
        last_inter = t["intermediate_updated_at"] or t["intermediate_at"]
        plan.append(("final", add_month(last_inter) if last_inter else None, "RTS 2025/301 Art 5(1)(c)"))
        for name, due, ref in plan:
            sent = t[f"{name}_at"]
            eff, moved = (due, False)
            if due and (relief_allowed or name == "final"):
                eff, moved = next_working(due, holidays)
            rep = {"report": name, "due": eff.isoformat() if eff else None, "sent": sent.isoformat() if sent else None, "ref": ref}
            if moved:
                rep["note"] = "deadline fell on a weekend or bank holiday: noon of the next working day (Art 5(4))"
            if sent and eff and sent > eff:
                rep["status"] = "LATE"
                add("HIGH", "LATE", f"{name} sent {round((sent - eff) / H, 1)} h after the deadline; Art 5(3) required telling the authority before it passed", ref)
            elif sent:
                rep["status"] = "ON_TIME"
            elif eff is None:
                rep["status"] = "WAITING"
                rep["waiting_for"] = "initial notification" if name == "intermediate" else "intermediate report"
            elif now > eff:
                rep["status"] = "OVERDUE"
                add("BLOCKER", "OVERDUE", f"{name} was due {fmt(eff)}, {round((now - eff) / H, 1)} h ago", ref)
            else:
                rep["status"] = "DUE"
                rep["hours_left"] = round((eff - now) / H, 1)
                if eff - now <= warn:
                    add("MEDIUM", "DUE_SOON", f"{name} due {fmt(eff)} ({rep['hours_left']} h left); if you cannot make it, tell the authority before it passes (Art 5(3))", ref)
            x["reports"].append(rep)
        if t["recovered_at"] and t["intermediate_at"] and not t["intermediate_updated_at"] and t["recovered_at"] > t["intermediate_at"]:
            add("MEDIUM", "UPDATE_ON_RECOVERY", "regular activities recovered after the intermediate report: send an updated intermediate report", "RTS 2025/301 Art 5(1)(b)")
        if (x["met"] and any(k == "clients" for k, _, _ in x["met"])) and not t["clients_informed_at"]:
            add("HIGH", "CLIENTS_NOT_INFORMED", "clients affected: if their financial interests are hit, inform them without undue delay of the incident and the mitigation", "DORA Art 19(3)")
        x.pop("row")

    for x in incs:
        for fnd in x["findings"]:
            counts[fnd["severity"]] += 1
        pending += sum(1 for r in x["reports"] if r["status"] in {"DUE", "WAITING"})
        x["aware_at"] = x["t"]["aware_at"].isoformat()
        del x["t"], x["m"]
        x["met"] = [{"criterion": k, "ref": ref, "detail": d} for k, ref, d in x["met"]]
    verdict = "OVERDUE" if counts["BLOCKER"] else "OPEN" if pending or counts["HIGH"] or counts["MEDIUM"] else "ON_TIME"
    notes = []
    if not holidays:
        notes.append("no --holidays given: bank holidays are treated as working days, so the Art 5(4) relief may be missed on them")
    return {"verdict": verdict, "as_of": now.isoformat(), "entity": entity, "weekend_relief": relief_allowed, "notes": notes,
            "summary": {"incidents": len(incs), "major": sum(1 for x in incs if x["major"]),
                        "unclassified": sum(1 for x in incs if x["major"] is None), "pending_reports": pending, "findings": counts},
            "incidents": incs}


def render(out):
    lines = [f"DORA major-incident clock: {out['verdict']}  (as of {fmt(dt.datetime.fromisoformat(out['as_of']))}; entity {out['entity']})", ""]
    for x in out["incidents"]:
        s = {True: "MAJOR", False: "not major", None: "UNCLASSIFIED"}[x["major"]]
        lines.append(f"- {x['id']}: {s}  ({x['why'][0]})")
        for r in x["reports"]:
            due = fmt(dt.datetime.fromisoformat(r["due"])) if r["due"] else f"after {r.get('waiting_for', '?')}"
            extra = f", {r['hours_left']} h left" if "hours_left" in r else ""
            note = f"  ({r['note']})" if r.get("note") else ""
            lines.append(f"    {r['report']:<13} {r['status']:<8} due {due}{extra}  [{r['ref']}]{note}")
        for f_ in sorted(x["findings"], key=lambda f_: SEVERITY_ORDER.index(f_["severity"])):
            lines.append(f"    {f_['severity']:<7} {f_['code']}: {f_['message']} [{f_['ref']}]")
    s = out["summary"]
    lines += ["", f"{s['incidents']} incidents, {s['major']} major, {s['unclassified']} unclassified, {s['pending_reports']} reports pending. "
              "Findings: " + ", ".join(f"{k} {v}" for k, v in s["findings"].items()),
              *[f"Note: {n}" for n in out["notes"]],
              "Report to the financial competent authority with the ITS templates (Implementing Regulation (EU) 2025/302)."]
    lines += ["", f"Rules last verified {RULES_VERIFIED}. Not legal advice: confirm with counsel or the competent authority."]
    return "\n".join(lines)


EXIT = {"ON_TIME": 0, "OPEN": 2, "OVERDUE": 4}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog="Exit codes: 0 on time, 2 open (includes reports not yet due, e.g. an intermediate report still waiting on the initial one), 3 invalid input, 4 overdue or unclassified after 24 h. "
                                       "Weekdays and noon are evaluated in each timestamp's own UTC offset: write timestamps in the Member State's local time.")
    p.add_argument("--incidents", help="incident log CSV (columns in the module docstring)")
    p.add_argument("--entity", default="other", choices=["credit-institution", "ccp", "trading-venue", "nis2-identified", "art16", "other"],
                   help="entity kind: decides weekend relief (Art 5(5)) and the recurring check (art16 = simplified framework)")
    p.add_argument("--microenterprise", action="store_true", help="skip the recurring-incident check (RTS 2024/1772 Art 8(2))")
    p.add_argument("--holidays", default="", help="comma-separated bank holidays YYYY-MM-DD in your Member State")
    p.add_argument("--as-of", help="evaluation time, ISO 8601 with offset (default: now)")
    p.add_argument("--warn-hours", type=float, default=4, help="flag reports due within this many hours (default 4)")
    p.add_argument("--sample", action="store_true", help="run on a built-in example log")
    p.add_argument("--output", choices=["text", "json"], default="text")
    p.add_argument("--json", action="store_true", help="shorthand for --output json")
    a = p.parse_args(argv)
    if a.json:
        a.output = "json"
    try:
        holidays = set()
        for d in [x.strip() for x in a.holidays.split(",") if x.strip()]:
            try:
                holidays.add(dt.date.fromisoformat(d))
            except ValueError:
                raise ValueError(f"--holidays: '{d}' is not YYYY-MM-DD")
        if a.sample:
            text, now = SAMPLE, dt.datetime(2026, 11, 17, 8, 0, tzinfo=UTC)
        else:
            if not a.incidents:
                p.print_usage(sys.stderr)
                print("error: give --incidents or --sample", file=sys.stderr)
                return 3
            with open(a.incidents, newline="", encoding="utf-8-sig") as fh:
                text = fh.read()
            now = ts({"x": a.as_of}, "x", 0) if a.as_of else dt.datetime.now(UTC)
        if a.warn_hours < 0:
            raise ValueError("--warn-hours must not be negative")
        out = run(text, now, a.entity, a.microenterprise, holidays, a.warn_hours * H)
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
