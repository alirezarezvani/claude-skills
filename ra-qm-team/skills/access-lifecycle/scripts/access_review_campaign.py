#!/usr/bin/env python3
"""Check a periodic access-review campaign the way an auditor will test it.

A finished campaign is not "every line has a tick". The test is whether the
review covered the whole population, whether the right people decided, whether
anything was decided at all, and whether every revoke actually happened. This
script checks the campaign's decision file against those four questions and,
when given the account export the campaign was built from, against the
population itself.

Findings
  POPULATION_GAP        an enabled account in the export is missing from the campaign   BLOCKER
  NOT_IN_POPULATION     a campaign line matches no account in the export (wrong export?) HIGH
  UNDECIDED             no decision recorded                                             BLOCKER
  SELF_REVIEW           the reviewer is the account's own user                           BLOCKER
  REVOKE_NOT_REMOVED    revoke/modify decided, no removal recorded past --remediation-days BLOCKER
  REVOKE_PENDING        revoke/modify decided, removal still inside the remediation window HIGH
  LATE_DECISION         decided after --close-date                                       HIGH
  NO_REVIEWER           decision recorded with no reviewer named                         BLOCKER
  RUBBER_STAMP          a reviewer kept every line of a large batch at machine speed     HIGH (a signal, not proof)

Rubber-stamp signal: a reviewer with at least --rubber-min decisions (default 20),
every one "keep", and a median gap between consecutive decisions of at most
--rubber-seconds (default 10). It needs decided_at with a time of day; it says
nothing about whether the reviewer was right, only that the evidence of
review is thin.

Decisions CSV columns: system, account_id, user_email, reviewer_email, decision
(keep|revoke|modify, blank = undecided), decided_at (ISO date or datetime),
removed_at (date the revoke/modify was carried out), privileged (true|false).
Population CSV: the access_diff.py accounts format (system, account_id, enabled, ...).

The remediation window is policy and has no default. "Any inappropriate access
is addressed" (PCI DSS v4.0.1 7.2.4) does not give a number; yours should.

Deterministic, stdlib only, no network.

Exit codes:
    0  COMPLETE
    2  COMPLETE_WITH_FINDINGS (no blockers)
    3  invalid input
    4  INCOMPLETE (at least one BLOCKER)
"""

import argparse
import csv
import datetime as dt
import io
import json
import statistics
import sys

CONTROLS = {
    "POPULATION_GAP": ["ISO27001:A.5.18", "SOC2:CC6.2", "NIST:AC-2", "PCI:7.2.4", "PCAOB:AS1105.10"],
    "NOT_IN_POPULATION": ["SOC2:CC6.2", "PCAOB:AS1105.10"],
    "UNDECIDED": ["ISO27001:A.5.18", "SOC2:CC6.3", "NIST:AC-2", "PCI:7.2.4"],
    "SELF_REVIEW": ["ISO27001:A.5.3", "SOC2:CC6.3", "NIST:AC-5"],
    "NO_REVIEWER": ["ISO27001:A.5.18", "SOC2:CC6.3", "NIST:AC-2", "PCI:7.2.4"],
    "REVOKE_NOT_REMOVED": ["ISO27001:A.5.18", "SOC2:CC6.2", "SOC2:CC6.3", "NIST:AC-2", "PCI:7.2.4"],
    "REVOKE_PENDING": ["ISO27001:A.5.18", "SOC2:CC6.2", "SOC2:CC6.3", "NIST:AC-2", "PCI:7.2.4"],
    "LATE_DECISION": ["ISO27001:A.5.18", "SOC2:CC6.3", "NIST:AC-2", "PCI:7.2.4"],
    "RUBBER_STAMP": ["ISO27001:A.5.18", "SOC2:CC6.3", "PCI:7.2.4"],
}
ACTION = {
    "POPULATION_GAP": "Add it to the campaign and get a decision; a review that skips accounts did not review the population.",
    "NOT_IN_POPULATION": "Check which export the campaign was built from; the two must be the same pull.",
    "UNDECIDED": "Get a decision from the reviewer or escalate to their manager.",
    "SELF_REVIEW": "Reassign to the user's manager or the system owner and re-decide.",
    "NO_REVIEWER": "Record who decided; an anonymous decision is not evidence of review.",
    "REVOKE_NOT_REMOVED": "Remove the access, then re-export to prove it is gone.",
    "REVOKE_PENDING": "Track it to removal before the window closes.",
    "LATE_DECISION": "Record why it was late; repeated lateness means the campaign window is too short or unowned.",
    "RUBBER_STAMP": "Ask the reviewer to re-review a sample and record what they checked for each line.",
}
SEVERITY_ORDER = {"BLOCKER": 0, "HIGH": 1}

SAMPLE_DECISIONS = """system,account_id,user_email,reviewer_email,decision,decided_at,removed_at,privileged
okta,u-100,ana.ruiz@example.com,lee.chan@example.com,keep,2026-10-10T09:00:00,,false
okta,u-101,ben.okafor@example.com,lee.chan@example.com,revoke,2026-10-10T09:01:00,,false
aws,arn-102,cara.lind@example.com,cara.lind@example.com,keep,2026-10-11T14:20:00,,true
github,gh-ghost,old.contractor@example.com,lee.chan@example.com,,,,false
okta,u-104,lee.chan@example.com,mia.berg@example.com,keep,2026-10-12T10:00:00,,true
aws,arn-103,dev.shah@example.com,lee.chan@example.com,modify,2026-10-28T16:00:00,,true
"""
SAMPLE_POPULATION = """system,account_id,email,employee_id,account_type,enabled,privileged,last_login,created,owner_email,last_reviewed
okta,u-100,ana.ruiz@example.com,E100,human,true,false,2026-10-29,2024-02-01,,2026-07-15
okta,u-101,ben.okafor@example.com,E101,human,true,false,2026-09-29,2023-05-10,,2026-07-15
aws,arn-102,cara.lind@example.com,E102,human,true,true,2026-10-30,2025-01-12,,2026-08-01
aws,arn-103,dev.shah@example.com,E103,human,false,true,2026-10-24,2024-11-03,,2026-08-01
github,gh-ghost,old.contractor@example.com,,human,true,false,2026-05-02,2025-03-01,,2026-07-15
aws,svc-backup,,,service,true,true,2026-10-31,2023-01-01,ben.okafor@example.com,2026-01-10
okta,u-104,lee.chan@example.com,E104,human,true,true,2026-10-31,2022-06-01,,2026-09-01
"""
SAMPLE_ARGS = {"as_of": "2026-10-31", "close_date": "2026-10-20", "remediation_days": 10}


def _fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(3)


def _when(value, field, where):
    value = (value or "").strip()
    if not value:
        return None
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None) if len(value) > 10 \
            else dt.datetime.combine(dt.date.fromisoformat(value), dt.time())
    except ValueError:
        _fail(f"{where}: {field} '{value}' is not an ISO date or datetime")


def _read(text, required, label):
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        _fail(f"{label}: empty file or missing header row")
    header = {h.strip().lower() for h in reader.fieldnames}
    missing = [c for c in required if c not in header]
    if missing:
        _fail(f"{label}: missing column(s) {', '.join(missing)}")
    return [{(k or "").strip().lower(): (v or "").strip() for k, v in row.items()} for row in reader]


def load_decisions(text):
    rows = _read(text, ["system", "account_id", "user_email", "reviewer_email", "decision"], "decisions")
    out = []
    for n, r in enumerate(rows, start=2):
        where = f"decisions line {n}"
        decision = r["decision"].lower()
        if decision not in ("", "keep", "revoke", "modify"):
            _fail(f"{where}: decision '{r['decision']}' must be keep, revoke, modify or blank")
        out.append({"system": r["system"], "account_id": r["account_id"], "user": r["user_email"].lower(),
                    "reviewer": r["reviewer_email"].lower(), "decision": decision,
                    "decided_at": _when(r.get("decided_at"), "decided_at", where),
                    "has_time": len(r.get("decided_at", "")) > 10,
                    "removed_at": _when(r.get("removed_at"), "removed_at", where),
                    "privileged": r.get("privileged", "").lower() in ("true", "yes", "y", "1")})
    return out


def analyse(decisions_text, as_of, remediation_days, close_date=None, population_text=None,
            rubber_min=20, rubber_seconds=10):
    items = load_decisions(decisions_text)
    findings, notes = [], []

    def add(code, severity, item, detail):
        findings.append({"code": code, "severity": severity, "system": item["system"], "account_id": item["account_id"],
                         "user": item.get("user", ""), "reviewer": item.get("reviewer", ""), "detail": detail,
                         "action": ACTION[code], "controls": CONTROLS[code]})

    keys = {(i["system"], i["account_id"]) for i in items}
    if population_text is not None:
        pop = _read(population_text, ["system", "account_id", "enabled"], "population")
        pop_keys = set()
        for r in pop:
            pop_keys.add((r["system"], r["account_id"]))
            if r["enabled"].lower() in ("true", "yes", "y", "1") and (r["system"], r["account_id"]) not in keys:
                add("POPULATION_GAP", "BLOCKER", {"system": r["system"], "account_id": r["account_id"],
                                                  "user": r.get("email", "").lower() or r.get("owner_email", "").lower()},
                    "enabled in the export, absent from the campaign")
        for i in items:
            if (i["system"], i["account_id"]) not in pop_keys:
                add("NOT_IN_POPULATION", "HIGH", i, "campaign line matches no account in the export")
    else:
        notes.append("population completeness not checked (pass --population with the export the campaign was built from)")

    for i in items:
        if not i["decision"]:
            add("UNDECIDED", "BLOCKER", i, "no decision recorded")
            continue
        if not i["reviewer"]:
            add("NO_REVIEWER", "BLOCKER", i, f"'{i['decision']}' recorded with no reviewer")
        elif i["user"] and i["reviewer"] == i["user"]:
            add("SELF_REVIEW", "BLOCKER", i, f"{i['reviewer']} reviewed their own access" + (" (privileged)" if i["privileged"] else ""))
        if close_date and i["decided_at"] and i["decided_at"].date() > close_date:
            add("LATE_DECISION", "HIGH", i, f"decided {i['decided_at'].date()}, campaign closed {close_date}")
        if i["decision"] in ("revoke", "modify") and not i["removed_at"]:
            if not i["decided_at"]:
                add("REVOKE_NOT_REMOVED", "BLOCKER", i, f"{i['decision']} with no decision date and no removal recorded")
            else:
                age = (as_of - i["decided_at"].date()).days
                if age > remediation_days:
                    add("REVOKE_NOT_REMOVED", "BLOCKER", i, f"{i['decision']} decided {age} days ago, no removal recorded (policy {remediation_days})")
                else:
                    add("REVOKE_PENDING", "HIGH", i, f"{i['decision']} decided {age} days ago, {remediation_days - age} day(s) left")

    by_reviewer = {}
    for i in items:
        if i["decision"] and i["reviewer"]:
            by_reviewer.setdefault(i["reviewer"], []).append(i)
    for reviewer, batch in sorted(by_reviewer.items()):
        if len(batch) < rubber_min or any(i["decision"] != "keep" for i in batch):
            continue
        times = sorted(i["decided_at"] for i in batch if i["decided_at"] and i["has_time"])
        if len(times) < rubber_min:
            notes.append(f"{reviewer}: {len(batch)} keeps, but decided_at has no time of day; rubber-stamp signal not checked")
            continue
        gap = statistics.median((b - a).total_seconds() for a, b in zip(times, times[1:]))
        if gap <= rubber_seconds:
            add("RUBBER_STAMP", "HIGH", {"system": "*", "account_id": f"{len(batch)} lines", "user": "", "reviewer": reviewer},
                f"{len(batch)} decisions, all keep, median {gap:.0f}s between decisions")

    findings.sort(key=lambda f: (SEVERITY_ORDER[f["severity"]], f["code"], f["system"], f["account_id"]))
    counts = {s: sum(f["severity"] == s for f in findings) for s in SEVERITY_ORDER}
    decided = sum(1 for i in items if i["decision"])
    verdict = "INCOMPLETE" if counts["BLOCKER"] else "COMPLETE_WITH_FINDINGS" if findings else "COMPLETE"
    return {
        "verdict": verdict, "as_of": as_of.isoformat(),
        "policy": {"remediation_days": remediation_days, "close_date": close_date.isoformat() if close_date else None,
                   "rubber_min": rubber_min, "rubber_seconds": rubber_seconds},
        "campaign": {"lines": len(items), "decided": decided,
                     "revoked_or_modified": sum(1 for i in items if i["decision"] in ("revoke", "modify")),
                     "reviewers": len(by_reviewer)},
        "counts": counts, "findings": findings, "notes": notes,
    }


def render(report):
    c = report["campaign"]
    out = [f"ACCESS REVIEW CAMPAIGN  {report['verdict']}  as of {report['as_of']}",
           f"Lines {c['lines']} · decided {c['decided']} · revoke/modify {c['revoked_or_modified']} · reviewers {c['reviewers']}",
           f"Policy: removal within {report['policy']['remediation_days']} days"
           + (f" · campaign closed {report['policy']['close_date']}" if report['policy']['close_date'] else ""),
           f"Findings: {report['counts']['BLOCKER']} blocker · {report['counts']['HIGH']} high", ""]
    for f in report["findings"]:
        who = f"user {f['user']}" if f["user"] else ""
        who += f"  reviewer {f['reviewer']}" if f["reviewer"] else ""
        out.append(f"{f['severity']:<7} {f['code']:<19} {f['system']}/{f['account_id']}  {who.strip()}")
        out.append(f"        {f['detail']}")
        out.append(f"        → {f['action']}  [{', '.join(f['controls'])}]")
    for n in report["notes"]:
        out.append(f"NOTE    {n}")
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description="Check an access-review campaign: population completeness, decisions, self-review, removals, timeliness, rubber-stamping.")
    p.add_argument("--decisions", help="campaign decisions CSV")
    p.add_argument("--population", help="account export the campaign was built from (access_diff.py accounts format)")
    p.add_argument("--as-of", help="check date YYYY-MM-DD (default: today)")
    p.add_argument("--close-date", help="campaign deadline YYYY-MM-DD")
    p.add_argument("--remediation-days", type=int, help="POLICY: days allowed from a revoke decision to removal (no default)")
    p.add_argument("--rubber-min", type=int, default=20, help="minimum batch size for the rubber-stamp signal (default 20)")
    p.add_argument("--rubber-seconds", type=float, default=10, help="median seconds between decisions at or below which a batch is flagged (default 10)")
    p.add_argument("--sample", action="store_true", help="run on an embedded sample campaign")
    p.add_argument("--output", choices=["text", "json"], default="text")
    a = p.parse_args()
    if a.sample:
        decisions, population = SAMPLE_DECISIONS, SAMPLE_POPULATION
        as_of = dt.date.fromisoformat(SAMPLE_ARGS["as_of"])
        close = dt.date.fromisoformat(SAMPLE_ARGS["close_date"])
        remediation = SAMPLE_ARGS["remediation_days"]
    else:
        if not a.decisions:
            _fail("give --decisions, or --sample")
        if a.remediation_days is None:
            _fail("--remediation-days is required: it is your policy, not a standard")
        try:
            with open(a.decisions, encoding="utf-8-sig") as fh:
                decisions = fh.read()
            population = None
            if a.population:
                with open(a.population, encoding="utf-8-sig") as fh:
                    population = fh.read()
        except OSError as exc:
            _fail(str(exc))
        try:
            as_of = dt.date.fromisoformat(a.as_of) if a.as_of else dt.date.today()
            close = dt.date.fromisoformat(a.close_date) if a.close_date else None
        except ValueError as exc:
            _fail(f"bad date: {exc}")
        remediation = a.remediation_days
    if remediation < 0 or a.rubber_min < 2 or a.rubber_seconds < 0:
        _fail("--remediation-days must be 0 or more, --rubber-min at least 2, --rubber-seconds 0 or more")
    report = analyse(decisions, as_of, remediation, close, population, a.rubber_min, a.rubber_seconds)
    print(json.dumps(report, indent=2) if a.output == "json" else render(report))
    return {"COMPLETE": 0, "COMPLETE_WITH_FINDINGS": 2, "INCOMPLETE": 4}[report["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
