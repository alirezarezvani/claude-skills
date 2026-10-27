#!/usr/bin/env python3
"""Diff an HR roster against an account export and find the access that should not exist.

An access review that starts from the account list asks "is this access
appropriate?" for accounts nobody can explain. This script starts from the
people: who has left, who changed role, which accounts belong to nobody, and
which privileged accounts nobody has looked at. Those are the samples an
auditor pulls first (ISO/IEC 27001:2022 A.5.18 and A.6.5, SOC 2 CC6.2 and
CC6.3, NIST SP 800-53 Rev. 5 AC-2, PCI DSS v4.0.1 8.2.5 and 8.2.6).

Findings
  LEAVER_ENABLED            terminated in HR, account still enabled after the grace period  BLOCKER
  LEAVER_USED_AFTER_EXIT    a login after the termination date (treat as a possible incident) BLOCKER
  ORPHAN_ACCOUNT            enabled human account that matches nobody in HR    BLOCKER if privileged, else HIGH
  SERVICE_OWNER_MISSING     enabled service account with no owner, or an owner who is not active
                                                                               BLOCKER if privileged, else HIGH
  MOVER_NOT_REVIEWED        role changed after the account's last review       HIGH
  PRIVILEGED_REVIEW_OVERDUE privileged account not reviewed within --privileged-review-days  HIGH
  INACTIVE                  enabled, no activity within --inactive-days        MEDIUM

Thresholds are policy. --inactive-days has no default because the right value
is yours (PCI DSS 8.2.6 uses 90; NIST AC-2(3) leaves it organization-defined).
The leaver grace period defaults to 0 days: PCI DSS 8.2.5 says "immediately".

Roster CSV columns:   employee_id, email, name, status (active|terminated|leave),
                      termination_date, role_changed_date (optional), manager_email (optional)
Accounts CSV columns: system, account_id, email, employee_id (optional),
                      account_type (human|service), enabled (true|false),
                      privileged (true|false), last_login, created, owner_email,
                      last_reviewed
Dates are YYYY-MM-DD; a datetime is truncated to its date. Accounts are joined
to people on employee_id when both sides have it, otherwise on email
(case-insensitive).

Deterministic, stdlib only, no network. Not an identity system: it reads
exports you produce, so the result is only as complete as those exports, and
an auditor will test that (PCAOB AS 1105.10). Keep the exports and the
parameters used to pull them.

Exit codes:
    0  CLEAN
    2  FINDINGS (no blockers)
    3  invalid input
    4  BLOCKED (at least one BLOCKER)
"""

import argparse
import csv
import datetime as dt
import io
import json
import sys

CONTROLS = {
    "LEAVER_ENABLED": ["ISO27001:A.5.18", "ISO27001:A.6.5", "SOC2:CC6.2", "NIST:AC-2", "PCI:8.2.5", "HIPAA:164.308(a)(3)(ii)(C)"],
    "LEAVER_USED_AFTER_EXIT": ["ISO27001:A.5.18", "ISO27001:A.6.5", "SOC2:CC6.2", "NIST:AC-2", "PCI:8.2.5", "HIPAA:164.308(a)(3)(ii)(C)"],
    "ORPHAN_ACCOUNT": ["ISO27001:A.5.16", "ISO27001:A.5.18", "SOC2:CC6.2", "NIST:AC-2(3)", "PCI:7.2.4"],
    "SERVICE_OWNER_MISSING": ["ISO27001:A.5.16", "SOC2:CC6.2", "NIST:AC-2", "PCI:7.2.5.1"],
    "MOVER_NOT_REVIEWED": ["ISO27001:A.5.18", "ISO27001:A.6.5", "SOC2:CC6.3", "NIST:AC-2"],
    "PRIVILEGED_REVIEW_OVERDUE": ["ISO27001:A.8.2", "ISO27001:A.5.18", "SOC2:CC6.3", "NIST:AC-2", "PCI:7.2.4"],
    "INACTIVE": ["ISO27001:A.5.18", "NIST:AC-2(3)", "PCI:8.2.6"],
}
ACTION = {
    "LEAVER_ENABLED": "Disable now; confirm by re-exporting the account list and keep both exports.",
    "LEAVER_USED_AFTER_EXIT": "Disable now and open a security incident: someone used a leaver's account after exit.",
    "ORPHAN_ACCOUNT": "Find the owner or disable it; an account nobody claims is nobody's to review.",
    "SERVICE_OWNER_MISSING": "Assign an active owner or disable it; rotate its credentials if the owner left.",
    "MOVER_NOT_REVIEWED": "Review this account against the new role and remove what the old role needed.",
    "PRIVILEGED_REVIEW_OVERDUE": "Review this privileged account now and record who reviewed it and when.",
    "INACTIVE": "Disable it, or record why an unused account must stay enabled.",
}
SEVERITY_ORDER = {"BLOCKER": 0, "HIGH": 1, "MEDIUM": 2}

SAMPLE_ROSTER = """employee_id,email,name,status,termination_date,role_changed_date,manager_email
E100,ana.ruiz@example.com,Ana Ruiz,active,,,lee.chan@example.com
E101,ben.okafor@example.com,Ben Okafor,terminated,2026-09-30,,lee.chan@example.com
E102,cara.lind@example.com,Cara Lind,active,,2026-10-01,lee.chan@example.com
E103,dev.shah@example.com,Dev Shah,terminated,2026-10-20,,lee.chan@example.com
E104,lee.chan@example.com,Lee Chan,active,,,
"""
SAMPLE_ACCOUNTS = """system,account_id,email,employee_id,account_type,enabled,privileged,last_login,created,owner_email,last_reviewed
okta,u-100,ana.ruiz@example.com,E100,human,true,false,2026-10-29,2024-02-01,,2026-07-15
okta,u-101,ben.okafor@example.com,E101,human,true,false,2026-09-29,2023-05-10,,2026-07-15
aws,arn-102,cara.lind@example.com,E102,human,true,true,2026-10-30,2025-01-12,,2026-08-01
aws,arn-103,dev.shah@example.com,E103,human,false,true,2026-10-24,2024-11-03,,2026-08-01
github,gh-ghost,old.contractor@example.com,,human,true,false,2026-05-02,2025-03-01,,2026-07-15
aws,svc-backup,,,service,true,true,2026-10-31,2023-01-01,ben.okafor@example.com,2026-01-10
okta,u-104,lee.chan@example.com,E104,human,true,true,2026-10-31,2022-06-01,,2026-09-01
"""
SAMPLE_ARGS = {"as_of": "2026-10-31", "inactive_days": 90, "privileged_review_days": 90}


def _fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(3)


def _date(value, field, where):
    value = (value or "").strip()
    if not value:
        return None
    try:
        return dt.date.fromisoformat(value[:10])
    except ValueError:
        _fail(f"{where}: {field} '{value}' is not a YYYY-MM-DD date")


def _bool(value):
    return (value or "").strip().lower() in ("true", "yes", "y", "1")


def _read(text, required, label):
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        _fail(f"{label}: empty file or missing header row")
    header = {h.strip().lower() for h in reader.fieldnames}
    missing = [c for c in required if c not in header]
    if missing:
        _fail(f"{label}: missing column(s) {', '.join(missing)}")
    return [{(k or "").strip().lower(): (v or "").strip() for k, v in row.items()} for row in reader]


def load_roster(text):
    rows = _read(text, ["employee_id", "email", "status"], "roster")
    people, by_id, by_email, quality = [], {}, {}, []
    for n, r in enumerate(rows, start=2):
        where = f"roster line {n}"
        status = r["status"].lower()
        if status not in ("active", "terminated", "leave"):
            _fail(f"{where}: status '{r['status']}' must be active, terminated or leave")
        p = {"employee_id": r["employee_id"], "email": r["email"].lower(), "name": r.get("name", ""),
             "status": status, "terminated": _date(r.get("termination_date"), "termination_date", where),
             "role_changed": _date(r.get("role_changed_date"), "role_changed_date", where)}
        if status == "terminated" and not p["terminated"]:
            _fail(f"{where}: terminated without a termination_date")
        for key, index in (("employee_id", by_id), ("email", by_email)):
            if p[key]:
                if p[key] in index:
                    quality.append(f"duplicate {key} '{p[key]}' in roster (lines with the same person cannot both be right)")
                index[p[key]] = p
        people.append(p)
    return people, by_id, by_email, quality


def load_accounts(text):
    rows = _read(text, ["system", "account_id", "enabled"], "accounts")
    accounts = []
    for n, r in enumerate(rows, start=2):
        where = f"accounts line {n}"
        kind = (r.get("account_type") or "human").lower()
        if kind not in ("human", "service"):
            _fail(f"{where}: account_type '{kind}' must be human or service")
        accounts.append({
            "system": r["system"], "account_id": r["account_id"], "email": r.get("email", "").lower(),
            "employee_id": r.get("employee_id", ""), "type": kind, "enabled": _bool(r["enabled"]),
            "privileged": _bool(r.get("privileged")), "owner": r.get("owner_email", "").lower(),
            "last_login": _date(r.get("last_login"), "last_login", where),
            "created": _date(r.get("created"), "created", where),
            "last_reviewed": _date(r.get("last_reviewed"), "last_reviewed", where),
        })
    return accounts


def match(account, by_id, by_email):
    if account["employee_id"] and account["employee_id"] in by_id:
        return by_id[account["employee_id"]]
    if account["email"] and account["email"] in by_email:
        return by_email[account["email"]]
    return None


def analyse(roster_text, accounts_text, as_of, inactive_days, grace_days=0, privileged_review_days=None):
    people, by_id, by_email, quality = load_roster(roster_text)
    accounts = load_accounts(accounts_text)
    findings = []

    def add(code, severity, acct, detail, person=None):
        findings.append({"code": code, "severity": severity, "system": acct["system"],
                         "account_id": acct["account_id"], "user": acct["email"] or acct["owner"] or "",
                         "privileged": acct["privileged"], "detail": detail, "action": ACTION[code],
                         "controls": CONTROLS[code], "person": person["employee_id"] if person else ""})

    unmatchable = 0
    for a in accounts:
        person = match(a, by_id, by_email) if a["type"] == "human" else None
        if a["type"] == "human" and not a["email"] and not a["employee_id"]:
            unmatchable += 1
        if person and person["status"] == "terminated":
            exit_day = person["terminated"]
            if a["last_login"] and a["last_login"] > exit_day:
                add("LEAVER_USED_AFTER_EXIT", "BLOCKER", a,
                    f"terminated {exit_day}, last login {a['last_login']}", person)
            if a["enabled"] and (as_of - exit_day).days > grace_days:
                add("LEAVER_ENABLED", "BLOCKER", a,
                    f"terminated {exit_day}, still enabled {(as_of - exit_day).days} days later (grace {grace_days})", person)
        if not a["enabled"]:
            continue
        if a["type"] == "human" and person is None:
            add("ORPHAN_ACCOUNT", "BLOCKER" if a["privileged"] else "HIGH", a,
                "no HR record matches this account" + (" (privileged)" if a["privileged"] else ""))
        if a["type"] == "service":
            owner = by_email.get(a["owner"]) if a["owner"] else None
            if not a["owner"]:
                why = "no owner recorded"
            elif owner is None:
                why = f"owner {a['owner']} is not in HR"
            elif owner["status"] != "active":
                why = f"owner {a['owner']} is {owner['status']}"
            else:
                why = None
            if why:
                add("SERVICE_OWNER_MISSING", "BLOCKER" if a["privileged"] else "HIGH", a, why)
        if person and person["status"] != "terminated" and person["role_changed"]:
            if not a["last_reviewed"] or a["last_reviewed"] < person["role_changed"]:
                add("MOVER_NOT_REVIEWED", "HIGH", a,
                    f"role changed {person['role_changed']}, last review {a['last_reviewed'] or 'never'}", person)
        if a["privileged"] and privileged_review_days is not None:
            if not a["last_reviewed"] or (as_of - a["last_reviewed"]).days > privileged_review_days:
                add("PRIVILEGED_REVIEW_OVERDUE", "HIGH", a,
                    f"last review {a['last_reviewed'] or 'never'}, policy {privileged_review_days} days", person)
        last_activity = a["last_login"] or a["created"]
        if last_activity and (as_of - last_activity).days > inactive_days:
            what = "last login" if a["last_login"] else "never logged in; created"
            add("INACTIVE", "MEDIUM", a, f"{what} {last_activity}, {(as_of - last_activity).days} days ago (policy {inactive_days})", person)
        if not last_activity:
            quality.append(f"{a['system']}/{a['account_id']}: no last_login or created date, inactivity not checked")

    if unmatchable:
        quality.append(f"{unmatchable} human account(s) carry neither email nor employee_id and cannot be matched")
    findings.sort(key=lambda f: (SEVERITY_ORDER[f["severity"]], f["code"], f["system"], f["account_id"]))
    counts = {s: sum(f["severity"] == s for f in findings) for s in SEVERITY_ORDER}
    verdict = "BLOCKED" if counts["BLOCKER"] else "FINDINGS" if findings else "CLEAN"
    return {
        "verdict": verdict, "as_of": as_of.isoformat(),
        "policy": {"inactive_days": inactive_days, "leaver_grace_days": grace_days,
                   "privileged_review_days": privileged_review_days},
        "population": {"people": len(people), "accounts": len(accounts),
                       "enabled": sum(a["enabled"] for a in accounts),
                       "privileged_enabled": sum(a["enabled"] and a["privileged"] for a in accounts)},
        "counts": counts, "findings": findings, "data_quality": quality,
        "not_checked": [] if privileged_review_days is not None else
        ["privileged review age (pass --privileged-review-days to check it)"],
    }


def render(report):
    out = [f"ACCESS DIFF  {report['verdict']}  as of {report['as_of']}",
           f"People {report['population']['people']} · accounts {report['population']['accounts']} "
           f"({report['population']['enabled']} enabled, {report['population']['privileged_enabled']} privileged)",
           f"Policy: inactive > {report['policy']['inactive_days']} days · leaver grace {report['policy']['leaver_grace_days']} days"
           + (f" · privileged review every {report['policy']['privileged_review_days']} days"
              if report['policy']['privileged_review_days'] is not None else ""),
           f"Findings: {report['counts']['BLOCKER']} blocker · {report['counts']['HIGH']} high · {report['counts']['MEDIUM']} medium", ""]
    for f in report["findings"]:
        out.append(f"{f['severity']:<7} {f['code']:<26} {f['system']}/{f['account_id']}  {f['user']}")
        out.append(f"        {f['detail']}")
        out.append(f"        → {f['action']}  [{', '.join(f['controls'])}]")
    for q in report["data_quality"]:
        out.append(f"DATA    {q}")
    for n in report["not_checked"]:
        out.append(f"NOT CHECKED  {n}")
    out.append("")
    out.append("Keep both exports and the parameters used to pull them: the result is only as complete as they are.")
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description="Diff an HR roster against an account export: leavers, orphans, unowned service accounts, movers, stale privileged access, inactivity.")
    p.add_argument("--roster", help="HR roster CSV")
    p.add_argument("--accounts", help="account export CSV (one or many systems)")
    p.add_argument("--as-of", help="review date YYYY-MM-DD (default: today)")
    p.add_argument("--inactive-days", type=int, help="POLICY: days without activity before an enabled account is flagged (no default)")
    p.add_argument("--leaver-grace-days", type=int, default=0, help="POLICY: days after termination before an enabled leaver blocks (default 0)")
    p.add_argument("--privileged-review-days", type=int, help="POLICY: maximum days since a privileged account was last reviewed")
    p.add_argument("--sample", action="store_true", help="run on an embedded sample roster and account export")
    p.add_argument("--output", choices=["text", "json"], default="text")
    a = p.parse_args()
    if a.sample:
        roster, accounts = SAMPLE_ROSTER, SAMPLE_ACCOUNTS
        as_of = dt.date.fromisoformat(SAMPLE_ARGS["as_of"])
        inactive, review = SAMPLE_ARGS["inactive_days"], SAMPLE_ARGS["privileged_review_days"]
    else:
        if not (a.roster and a.accounts):
            _fail("give --roster and --accounts, or --sample")
        if a.inactive_days is None:
            _fail("--inactive-days is required: it is your policy, not a standard (PCI DSS 8.2.6 uses 90)")
        try:
            with open(a.roster, encoding="utf-8-sig") as fh:
                roster = fh.read()
            with open(a.accounts, encoding="utf-8-sig") as fh:
                accounts = fh.read()
        except OSError as exc:
            _fail(str(exc))
        try:
            as_of = dt.date.fromisoformat(a.as_of) if a.as_of else dt.date.today()
        except ValueError:
            _fail(f"--as-of '{a.as_of}' is not a YYYY-MM-DD date")
        inactive, review = a.inactive_days, a.privileged_review_days
    for name, value in (("inactive-days", inactive), ("leaver-grace-days", a.leaver_grace_days), ("privileged-review-days", review)):
        if value is not None and value < 0:
            _fail(f"--{name} must be 0 or more")
    report = analyse(roster, accounts, as_of, inactive, a.leaver_grace_days, review)
    print(json.dumps(report, indent=2) if a.output == "json" else render(report))
    return {"CLEAN": 0, "FINDINGS": 2, "BLOCKED": 4}[report["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
