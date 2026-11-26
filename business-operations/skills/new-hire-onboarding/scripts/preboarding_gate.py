#!/usr/bin/env python3
"""Check whether a new hire's first day is ready, task by task, against the start date.

Input: a JSON file describing one hire:

  {
    "hire": "A. Rivera", "role": "Backend Engineer", "start_date": "2026-12-07",
    "jurisdiction": "US",            # US | UK | other (right-to-work rule used)
    "remote": true,                  # remote hires need equipment shipped earlier
    "manager": "J. Chen", "buddy": "P. Okafor",
    "tasks": [
      {"task": "Laptop shipped", "category": "equipment", "owner": "IT",
       "lead_days": 7, "status": "done"},
      ...
    ]
  }

Each task is due `lead_days` business days before the start date (Mon-Fri).
Status is done | in_progress | not_started | blocked. A task that is not done is

  LATE      its due date has passed
  AT_RISK   it is due within --risk-days business days, or it is blocked
  OPEN      it has time left

Required categories (one task each must exist): contract (signed offer or
contract), right_to_work, equipment, accounts (email/SSO and the systems the
role needs on day one), payroll, day_one_agenda. Spaces and hyphens in a
category are read as underscores; any other category is bad input (exit 3).
An optional "holidays" list of YYYY-MM-DD dates is skipped like a weekend. A named manager and a named
buddy (not the manager) are required too.

Right to work, per --jurisdiction or the file's jurisdiction:
  US     Form I-9 Section 1 by the first day of employment, Section 2 within
         3 business days after it (USCIS). The script prints the Section 2
         deadline; the right_to_work task covers Section 1.
  UK     the check must be done before employment starts (GOV.UK), so the
         right_to_work task is due at least one business day before the start
         and is blocking: a check left for day one shows LATE.
  other  no rule built in: the task must exist and the output says to confirm
         the local rule with HR or counsel.

Verdict:
  READY      every required item exists and nothing is LATE or AT_RISK
  AT_RISK    something is AT_RISK or LATE but no blocking item is late
  NOT_READY  a required category, the manager or the buddy is missing, or a
             blocking item (contract, right_to_work, equipment, accounts) is
             LATE or blocked (a blocked blocking item shows AT_RISK in its row
             but makes the verdict NOT_READY however much time is left: nothing
             moves it until someone unblocks it)
             -> move the start date or fix the item; do not start the hire
                on a day they cannot work

Exit codes: 0 READY, 2 AT_RISK, 3 bad input, 4 NOT_READY.
Deterministic, stdlib only, no network. The script never contacts an HR
system; it reads the file you give it.
"""
import argparse
import datetime as dt
import json
import re
import sys

EXIT = {"READY": 0, "AT_RISK": 2, "BAD_INPUT": 3, "NOT_READY": 4}
REQUIRED = ["contract", "right_to_work", "equipment", "accounts", "payroll", "day_one_agenda"]
BLOCKING = {"contract", "right_to_work", "equipment", "accounts"}
STATUSES = {"done", "in_progress", "not_started", "blocked"}
DEFAULT_LEAD = {"contract": 10, "right_to_work": 1, "equipment": 3, "accounts": 2,
                "payroll": 5, "day_one_agenda": 2}
REMOTE_EQUIPMENT_LEAD = 7

SAMPLE = {
    "hire": "A. Rivera", "role": "Backend Engineer", "start_date": "2026-12-07",
    "jurisdiction": "US", "remote": True, "manager": "J. Chen", "buddy": "",
    "tasks": [
        {"task": "Offer letter signed", "category": "contract", "owner": "Recruiting", "status": "done"},
        {"task": "I-9 Section 1 link sent", "category": "right_to_work", "owner": "People Ops", "status": "in_progress"},
        {"task": "Laptop shipped", "category": "equipment", "owner": "IT", "lead_days": 7, "status": "not_started"},
        {"task": "Email, SSO, GitHub, AWS read-only", "category": "accounts", "owner": "IT", "status": "in_progress"},
        {"task": "Payroll and tax forms", "category": "payroll", "owner": "Finance", "status": "not_started"},
        {"task": "Day-one agenda shared", "category": "day_one_agenda", "owner": "J. Chen", "status": "not_started"},
    ],
}


def parse_date(s, field):
    try:
        return dt.date.fromisoformat(str(s))
    except ValueError:
        raise ValueError(f"{field} must be YYYY-MM-DD, got {s!r}")


def is_business_day(d, holidays):
    return d.weekday() < 5 and d not in holidays


def business_days_before(d, n, holidays=frozenset()):
    while n > 0:
        d -= dt.timedelta(days=1)
        if is_business_day(d, holidays):
            n -= 1
    return d


def business_days_after(d, n, holidays=frozenset()):
    while n > 0:
        d += dt.timedelta(days=1)
        if is_business_day(d, holidays):
            n -= 1
    return d


def business_days_between(a, b, holidays=frozenset()):
    """Business days from a (exclusive) to b (inclusive); negative if b < a."""
    if b == a:
        return 0
    step = 1 if b > a else -1
    n, d = 0, a
    while d != b:
        d += dt.timedelta(days=step)
        if is_business_day(d, holidays):
            n += step
    return n


def text_field(value, field):
    if value is None:
        return ""
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string, got {type(value).__name__}")
    return value.strip()


def norm_category(value):
    return re.sub(r"[\s-]+", "_", str(value).strip().lower())


def evaluate(spec, today, risk_days, jurisdiction=None):
    if not isinstance(spec, dict):
        raise ValueError("input must be a JSON object")
    hol = spec.get("holidays") or []
    if not isinstance(hol, list):
        raise ValueError("holidays must be a list of YYYY-MM-DD dates")
    holidays_set = frozenset(parse_date(h, "holidays entry") for h in hol)
    start = parse_date(spec.get("start_date"), "start_date")
    if start.weekday() >= 5:
        raise ValueError(f"start_date {start} is a weekend day")
    if start < today:
        raise ValueError(f"start_date {start} is before {today}: the preboarding gate is for upcoming starts")
    if start in holidays_set:
        raise ValueError(f"start_date {start} is listed as a holiday")
    juris = (jurisdiction or text_field(spec.get("jurisdiction"), "jurisdiction") or "other").upper()
    if juris not in {"US", "UK", "OTHER"}:
        raise ValueError("jurisdiction must be US, UK or other")
    remote = bool(spec.get("remote", False))
    tasks = spec.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("tasks must be a non-empty list")

    rows, findings = [], []
    seen = set()
    for i, t in enumerate(tasks):
        if not isinstance(t, dict) or not t.get("task") or not t.get("category"):
            raise ValueError(f"task {i}: needs 'task' and 'category'")
        t = dict(t, task=text_field(t["task"], f"task {i} name"))
        cat = norm_category(t["category"])
        if cat not in DEFAULT_LEAD:
            raise ValueError(f"task {t['task']!r}: category {t['category']!r} is not one of {REQUIRED}")
        status = str(t.get("status", "not_started")).strip().lower()
        if status not in STATUSES:
            raise ValueError(f"task {t['task']!r}: status must be one of {sorted(STATUSES)}")
        lead = t.get("lead_days")
        if lead is None:
            lead = REMOTE_EQUIPMENT_LEAD if (cat == "equipment" and remote) else DEFAULT_LEAD[cat]
        if isinstance(lead, bool) or not isinstance(lead, int) or lead < 0:
            raise ValueError(f"task {t['task']!r}: lead_days must be a whole number >= 0")
        if cat == "right_to_work" and juris == "UK" and lead < 1:
            lead = 1  # UK check must be complete before the first day
        due = business_days_before(start, lead, holidays_set) if lead else start
        left = business_days_between(today, due, holidays_set)
        if status == "done":
            state = "DONE"
        elif left < 0:
            state = "LATE"
        elif status == "blocked" or left <= risk_days:
            state = "AT_RISK"
        else:
            state = "OPEN"
        owner = text_field(t.get("owner"), f"task {t['task']!r} owner")
        if not owner and state != "DONE":
            findings.append(f"NO_OWNER: '{t['task']}' has no owner; nobody will chase it.")
        seen.add(cat)
        rows.append({"task": t["task"], "category": cat, "owner": owner or "-", "status": status,
                     "due": due.isoformat(), "business_days_left": left, "state": state,
                     "blocking": cat in BLOCKING})

    missing = [c for c in REQUIRED if c not in seen]
    people = {k: text_field(spec.get(k), k) for k in ("manager", "buddy")}
    for c in missing:
        findings.append(f"MISSING: no '{c}' task. Add it with an owner and a due date.")
    for k, v in people.items():
        if not v:
            findings.append(f"MISSING: no named {k}. Name one person before the start date.")
    same = people["buddy"] and people["buddy"].lower() == people["manager"].lower()
    if same:
        findings.append("BUDDY_IS_MANAGER: the buddy must be a peer the hire can ask anything, not the manager.")

    blocking_late = [r for r in rows if r["blocking"] and (r["state"] == "LATE" or r["status"] == "blocked")]
    risky = [r for r in rows if r["state"] in ("LATE", "AT_RISK")]
    if missing or not all(people.values()) or same or blocking_late:
        verdict = "NOT_READY"
    elif risky:
        verdict = "AT_RISK"
    else:
        verdict = "READY"

    rtw = {}
    if juris == "US":
        rtw = {"rule": "Form I-9 Section 1 by the first day; Section 2 within 3 business days after it (USCIS). "
                       "Counted Mon-Fri minus listed holidays; if the employer is open other days, count those instead",
               "section_1_by": start.isoformat(),
               "section_2_by": business_days_after(start, 3, holidays_set).isoformat()}
    elif juris == "UK":
        rtw = {"rule": "Right to work check before employment starts (GOV.UK)", "check_by": business_days_before(start, 1, holidays_set).isoformat()}
    else:
        rtw = {"rule": "No rule built in for this jurisdiction: confirm the right-to-work deadline with HR or counsel"}

    order = {"LATE": 0, "AT_RISK": 1, "OPEN": 2, "DONE": 3}
    rows.sort(key=lambda r: (order[r["state"]], not r["blocking"], r["due"]))
    return {"hire": spec.get("hire", ""), "role": spec.get("role", ""), "start_date": start.isoformat(),
            "today": today.isoformat(), "business_days_to_start": business_days_between(today, start, holidays_set),
            "jurisdiction": juris, "remote": remote, "manager": people["manager"] or None,
            "buddy": people["buddy"] or None, "right_to_work": rtw, "verdict": verdict,
            "tasks": rows, "findings": findings,
            "defaults": {"risk_days": risk_days, "remote_equipment_lead_days": REMOTE_EQUIPMENT_LEAD,
                         "default_lead_days": DEFAULT_LEAD,
                         "holidays": sorted(h.isoformat() for h in holidays_set)}}


def render(r):
    out = [f"Preboarding gate: {r['hire'] or 'new hire'} ({r['role'] or 'role not given'}), "
           f"starts {r['start_date']} ({r['business_days_to_start']} business days from {r['today']})",
           f"VERDICT: {r['verdict']}", ""]
    out.append(f"{'STATE':8} {'DUE':10} {'LEFT':>4}  {'OWNER':12} TASK")
    for t in r["tasks"]:
        flag = " [blocking]" if t["blocking"] and t["state"] != "DONE" else ""
        out.append(f"{t['state']:8} {t['due']:10} {t['business_days_left']:>4}  {t['owner'][:12]:12} {t['task']}{flag}")
    out.append("")
    rtw = r["right_to_work"]
    out.append(f"Right to work ({r['jurisdiction']}): {rtw['rule']}")
    for k in ("section_1_by", "section_2_by", "check_by"):
        if k in rtw:
            out.append(f"  {k.replace('_', ' ')}: {rtw[k]}")
    out.append(f"Manager: {r['manager'] or 'MISSING'} | Buddy: {r['buddy'] or 'MISSING'}")
    if r["findings"]:
        out.append("")
        out.extend(r["findings"])
    if r["verdict"] == "NOT_READY":
        out.append("")
        out.append("Do not start the hire on a day they cannot work: fix the items above or move the start date.")
    out.append("")
    out.append(f"Defaults: at risk = due within {r['defaults']['risk_days']} business days; "
               f"remote equipment lead {r['defaults']['remote_equipment_lead_days']} business days; weekends skipped, "
               f"{len(r['defaults']['holidays'])} listed holiday(s) skipped (add a \"holidays\" list to the hire file).")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 epilog="Exit codes: 0 READY, 2 AT_RISK, 3 bad input, 4 NOT_READY.")
    ap.add_argument("--hire", help="hire JSON (start_date, jurisdiction, remote, manager, buddy, tasks)")
    ap.add_argument("--today", help="date to judge from, YYYY-MM-DD (default: today)")
    ap.add_argument("--jurisdiction", choices=["US", "UK", "other"], help="override the file's jurisdiction")
    ap.add_argument("--risk-days", type=int, default=2, help="business days before due that count as at risk (default 2)")
    ap.add_argument("--sample", action="store_true", help="run on a built-in hire (today = 2026-11-30)")
    ap.add_argument("--output", "--format", choices=["text", "json"], default="text")
    a = ap.parse_args(argv)
    try:
        if a.sample:
            spec, today = SAMPLE, dt.date(2026, 11, 30)
        elif a.hire:
            with open(a.hire, encoding="utf-8") as f:
                spec = json.load(f)
            today = dt.date.today()
        else:
            raise ValueError("give --hire FILE or --sample")
        if a.today:
            today = parse_date(a.today, "--today")
        if a.risk_days < 0:
            raise ValueError("--risk-days must be 0 or more")
        res = evaluate(spec, today, a.risk_days, a.jurisdiction)
    except (ValueError, OSError, json.JSONDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return EXIT["BAD_INPUT"]
    print(json.dumps(res, indent=2) if a.output == "json" else render(res))
    return EXIT[res["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
