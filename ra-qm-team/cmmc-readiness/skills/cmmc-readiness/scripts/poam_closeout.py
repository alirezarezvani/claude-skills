#!/usr/bin/env python3
"""Track a CMMC Level 2 POA&M to closeout and keep the status dates honest.

Conditional CMMC status lasts 180 days. If every POA&M item is not closed and
confirmed by a closeout assessment inside that window, the Conditional status
expires (32 CFR 170.21(b)). This script reads the score from sprs_score.py and
the POA&M, then checks that the POA&M covers exactly the deferred gaps, that
each item may be deferred at all, and how many days are left.

Findings
  NOT_CONDITIONAL       the score is not Conditional-eligible: there is nothing to close out    BLOCKER
  POAM_INELIGIBLE       an item that may never be on a POA&M (170.21(a)(2))                     BLOCKER
  GAP_NOT_ON_POAM       a NOT MET or PARTIAL requirement with no POA&M item                     BLOCKER
  WINDOW_EXPIRED        open items after the 180-day closeout deadline: status has expired     BLOCKER
  AFFIRMATION_OVERDUE   no affirmation since the last anniversary of the Final status date      BLOCKER
  MILESTONE_AFTER_DEADLINE  an item planned to finish after the deadline                         HIGH
  NO_OWNER              an open item with nobody named                                          HIGH
  CLOSED_NO_EVIDENCE    marked closed with no evidence; the closeout assessment retests it      HIGH
  DEADLINE_NEAR         deadline inside --warn-days with items still open                       MEDIUM
  NOT_A_GAP             a POA&M item for a requirement the score shows as MET or NA             MEDIUM

Dates (32 CFR 170.4, 170.21(b), 170.22)
  closeout deadline     Conditional status date + 180 days
  status valid until    Conditional status date + 3 years (a Final status keeps that date)
  affirmations          at Conditional status, at closeout, then every year after the Final status date

POA&M CSV columns: requirement_id, status (OPEN|CLOSED), owner, milestone_date, closed_date, evidence

Deterministic, stdlib only, no network. The closeout assessment itself is done
by the OSA (Level 2 Self) or a C3PAO (Level 2 C3PAO); this script only says
whether you are ready for it.

Exit codes:
    0  READY_FOR_CLOSEOUT (every item closed with evidence) or FINAL (nothing deferred)
    2  ON_TRACK or AT_RISK (open items, deadline not passed)
    3  invalid input
    4  BLOCKED or EXPIRED
"""

import argparse
import csv
import datetime as dt
import io
import json
import sys

WINDOW_DAYS = 180

SAMPLE_SCORE = {
    "verdict": "CONDITIONAL_ELIGIBLE",
    "score": 105,
    "requirements": [
        {"id": "AU.L2-3.3.4", "status": "NOT_MET", "deduction": 1, "poam_eligible": True},
        {"id": "CM.L2-3.4.9", "status": "NOT_MET", "deduction": 1, "poam_eligible": True},
        {"id": "SC.L2-3.13.11", "status": "PARTIAL", "deduction": 3, "poam_eligible": True},
        {"id": "MP.L2-3.8.4", "status": "NOT_MET", "deduction": 1, "poam_eligible": True},
        {"id": "IA.L2-3.5.3", "status": "MET", "deduction": 0},
    ],
}
SAMPLE_POAM = """requirement_id,status,owner,milestone_date,closed_date,evidence
AU.L2-3.3.4,CLOSED,j.ortiz@example.com,2026-08-15,2026-08-10,SIEM rule LOG-PIPE-01 alert screenshot + test ticket SEC-311
CM.L2-3.4.9,OPEN,j.ortiz@example.com,2026-12-20,,
SC.L2-3.13.11,OPEN,,2026-11-30,,
IA.L2-3.5.3,CLOSED,m.kim@example.com,2026-07-01,2026-07-01,
"""
SEVERITY_ORDER = {"BLOCKER": 0, "HIGH": 1, "MEDIUM": 2}


def parse_date(s, field):
    s = (s or "").strip()
    if not s:
        return None
    try:
        return dt.date.fromisoformat(s[:10])
    except ValueError:
        raise ValueError(f"{field}: '{s}' is not a YYYY-MM-DD date")


def add_years(d, n):
    try:
        return d.replace(year=d.year + n)
    except ValueError:  # 29 February
        return d.replace(year=d.year + n, day=28)


def short_id(raw):
    raw = (raw or "").strip()
    return raw.split("-", 1)[1].strip() if "-" in raw else raw


def check(score, poam_text, conditional, as_of, warn_days, final=None, last_affirmation=None):
    findings = []

    def add(sev, code, rid, detail):
        findings.append({"severity": sev, "code": code, "id": rid, "detail": detail})

    verdict_in = score.get("verdict")
    gaps = {short_id(r["id"]): r for r in score.get("requirements", [])
            if r.get("status") in ("NOT_MET", "PARTIAL")}
    if verdict_in == "FINAL_ELIGIBLE" and not gaps:
        return {"verdict": "FINAL", "detail": "Score is 110: nothing is deferred, so there is no POA&M to close.",
                "findings": []}
    if verdict_in != "CONDITIONAL_ELIGIBLE":
        add("BLOCKER", "NOT_CONDITIONAL", "-",
            f"score verdict is {verdict_in}: fix the gaps that cannot be deferred before planning a closeout")

    reader = csv.DictReader(io.StringIO(poam_text))
    need = {"requirement_id", "status"}
    if not reader.fieldnames or not need <= set(reader.fieldnames):
        raise ValueError("POA&M CSV needs columns requirement_id and status (plus owner, milestone_date, closed_date, evidence)")
    deadline = conditional + dt.timedelta(days=WINDOW_DAYS)
    items, seen = [], set()
    for line, r in enumerate(reader, start=2):
        rid_raw = (r.get("requirement_id") or "").strip()
        rid = short_id(rid_raw)
        status = (r.get("status") or "").strip().upper()
        if status not in ("OPEN", "CLOSED"):
            raise ValueError(f"line {line}: status '{r.get('status')}' must be OPEN or CLOSED")
        if rid in seen:
            raise ValueError(f"line {line}: {rid_raw} listed twice")
        seen.add(rid)
        milestone = parse_date(r.get("milestone_date"), f"line {line} milestone_date")
        closed = parse_date(r.get("closed_date"), f"line {line} closed_date")
        owner = (r.get("owner") or "").strip()
        evidence = (r.get("evidence") or "").strip()
        items.append({"id": rid_raw, "status": status, "owner": owner, "milestone_date": str(milestone or ""),
                      "closed_date": str(closed or "")})
        gap = gaps.get(rid)
        if gap is None:
            add("MEDIUM", "NOT_A_GAP", rid_raw,
                "the score shows this requirement MET or NA; drop the item or correct the assessment")
            continue
        if not gap.get("poam_eligible", False):
            add("BLOCKER", "POAM_INELIGIBLE", rid_raw,
                gap.get("poam_reason", "this requirement may not be deferred") + "; implement it before the assessment")
        if status == "CLOSED":
            if not evidence:
                add("HIGH", "CLOSED_NO_EVIDENCE", rid_raw,
                    "record what proves it (config export, screenshot, ticket); the closeout assessment retests it")
            continue
        if not owner:
            add("HIGH", "NO_OWNER", rid_raw, "name the person who will close it")
        if milestone and milestone > deadline:
            add("HIGH", "MILESTONE_AFTER_DEADLINE", rid_raw,
                f"planned {milestone}, deadline {deadline}: finish earlier or the Conditional status expires")
    for rid, gap in gaps.items():
        if rid not in seen:
            add("BLOCKER", "GAP_NOT_ON_POAM", gap["id"],
                "every NOT MET requirement needs a POA&M item (32 CFR 170.24)")

    open_items = [i for i in items if i["status"] == "OPEN" and short_id(i["id"]) in gaps]
    days_left = (deadline - as_of).days
    if open_items and as_of > deadline:
        add("BLOCKER", "WINDOW_EXPIRED", "-",
            f"{len(open_items)} item(s) still open {-days_left} day(s) after the {deadline} deadline: "
            "the Conditional status has expired (32 CFR 170.21(b)); a new assessment is needed")
    elif open_items and days_left <= warn_days:
        add("MEDIUM", "DEADLINE_NEAR", "-",
            f"{days_left} day(s) to {deadline} with {len(open_items)} item(s) open; book the closeout assessment now")

    calendar = {
        "conditional_status_date": str(conditional),
        "closeout_deadline": str(deadline),
        "days_to_closeout_deadline": days_left,
        "status_valid_until": str(add_years(conditional, 3)),
        "affirmations": ["at Conditional status (" + str(conditional) + ")", "at POA&M closeout"],
    }
    if final:
        anniversaries = [add_years(final, n) for n in range(1, 4)]
        calendar["final_status_date"] = str(final)
        calendar["annual_affirmations_due"] = [str(d) for d in anniversaries if d <= add_years(conditional, 3)]
        past = [d for d in anniversaries if d <= as_of]
        if past and (last_affirmation is None or last_affirmation < past[-1]):
            add("BLOCKER", "AFFIRMATION_OVERDUE", "-",
                f"annual affirmation due {past[-1]} not recorded; without it the status lapses (32 CFR 170.22)")
    if any(f["severity"] == "BLOCKER" for f in findings):
        v = "EXPIRED" if any(f["code"] == "WINDOW_EXPIRED" for f in findings) else "BLOCKED"
    elif not open_items and not any(f["code"] == "CLOSED_NO_EVIDENCE" for f in findings):
        v = "READY_FOR_CLOSEOUT"
    elif any(f["severity"] == "HIGH" for f in findings) or any(f["code"] == "DEADLINE_NEAR" for f in findings):
        v = "AT_RISK"
    else:
        v = "ON_TRACK"
    findings.sort(key=lambda f: SEVERITY_ORDER[f["severity"]])
    return {"verdict": v, "as_of": str(as_of), "open_items": len(open_items),
            "deferred_gaps": len(gaps), "calendar": calendar, "findings": findings, "items": items}


def render(out):
    if out["verdict"] == "FINAL":
        return out["detail"]
    c = out["calendar"]
    lines = [f"POA&M closeout: {out['verdict']}   ({out['open_items']} of {out['deferred_gaps']} deferred gap(s) open)",
             f"  Conditional status {c['conditional_status_date']} → closeout deadline {c['closeout_deadline']}"
             f" ({c['days_to_closeout_deadline']} day(s) from {out['as_of']})",
             f"  Status valid until {c['status_valid_until']}"]
    if c.get("annual_affirmations_due"):
        lines.append("  Annual affirmations due: " + ", ".join(c["annual_affirmations_due"]))
    for f in out["findings"]:
        lines.append(f"[{f['severity']}] {f['code']} {f['id']}: {f['detail']}")
    lines.append("Closeout is confirmed by the OSA (Level 2 Self) or a C3PAO (Level 2 C3PAO), not by this script.")
    return "\n".join(lines)


EXIT = {"FINAL": 0, "READY_FOR_CLOSEOUT": 0, "ON_TRACK": 2, "AT_RISK": 2, "BLOCKED": 4, "EXPIRED": 4}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog="Exit codes: 0 ready or final, 2 on track or at risk, 3 invalid input, 4 blocked or expired.")
    p.add_argument("--score", help="JSON written by sprs_score.py --output json")
    p.add_argument("--poam", help="POA&M CSV")
    p.add_argument("--conditional-date", help="Conditional CMMC Status Date, YYYY-MM-DD")
    p.add_argument("--final-date", help="Final CMMC Status Date, if reached (enables annual affirmation checks)")
    p.add_argument("--last-affirmation", help="date of the most recent SPRS affirmation")
    p.add_argument("--as-of", help="evaluation date (default: today)")
    p.add_argument("--warn-days", type=int, default=30, help="flag the deadline this many days ahead (default 30)")
    p.add_argument("--sample", action="store_true", help="run on a built-in example")
    p.add_argument("--output", choices=["text", "json"], default="text")
    p.add_argument("--json", action="store_true", help="shorthand for --output json")
    a = p.parse_args(argv)
    if a.json:
        a.output = "json"
    try:
        if a.sample:
            score, poam_text = SAMPLE_SCORE, SAMPLE_POAM
            conditional, as_of = dt.date(2026, 6, 15), dt.date(2026, 11, 20)
        else:
            if not (a.score and a.poam and a.conditional_date):
                p.print_usage(sys.stderr)
                print("error: give --score, --poam and --conditional-date, or --sample", file=sys.stderr)
                return 3
            with open(a.score, encoding="utf-8") as fh:
                score = json.load(fh)
            with open(a.poam, newline="", encoding="utf-8-sig") as fh:
                poam_text = fh.read()
            conditional = parse_date(a.conditional_date, "--conditional-date")
            as_of = parse_date(a.as_of, "--as-of") or dt.date.today()
        final = parse_date(a.final_date, "--final-date")
        last_aff = parse_date(a.last_affirmation, "--last-affirmation")
        if final and final < conditional:
            raise ValueError("--final-date is before --conditional-date")
        out = check(score, poam_text, conditional, as_of, a.warn_days, final, last_aff)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as e:
        if a.output == "json":
            print(json.dumps({"verdict": "INVALID_INPUT", "errors": [str(e)]}, indent=2))
        else:
            print(f"error: {e}", file=sys.stderr)
        return 3
    print(json.dumps(out, indent=2) if a.output == "json" else render(out))
    return EXIT[out["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
