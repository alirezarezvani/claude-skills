#!/usr/bin/env python3
"""Check a DORA register of information and its ICT contracts for missing terms.

Every financial entity keeps a register of all contractual arrangements on the
use of ICT services provided by ICT third-party service providers (Regulation
(EU) 2022/2554 Art 28(3)), in the templates of Implementing Regulation (EU)
2024/2956, and reports it to its competent authority on request. Art 30 lists
what every contract must contain, and more for contracts supporting critical
or important functions. This script reads the register as a CSV, one row per
contract, and finds the gaps a supervisor will find first.

Checks
  identity       provider legal entity identifier (LEI) or EUID present        ITS 2024/2956
  function       critical_or_important assessed (yes|no)                      Art 28(3), Art 3(22)
  all contracts  Art 30(2) terms (a)-(i) present                              Art 30(2)
  CIF contracts  Art 30(3) terms (a)-(f) present                              Art 30(3)
                 tested exit plan                                             Art 28(8)
                 pre-contract risk assessment and due diligence               Art 28(4)
                 subcontracting chain known                                   Art 30(2)(a), Art 29(2)
  concentration  one provider supporting several CIFs, or a CIF with no substitute   Art 29(1)
  third country  provider outside the EU supporting a CIF                     Art 29(2)

Register CSV columns:
  contract_id, provider, provider_lei, provider_country, service, critical_or_important (yes|no),
  function, art30_2 (semicolon list of present terms a..i), art30_3 (list of a..f),
  exit_plan (tested|documented|none), risk_assessment (yes|no), subcontractors (yes|no|unknown),
  substitutable (yes|no|unknown), last_review (YYYY-MM-DD)

Deterministic, stdlib only, no network; submits nothing.

Exit codes:
    0  clean
    2  findings below BLOCKER
    3  invalid input
    4  a BLOCKER: a CIF contract missing Art 30(3) terms or an exit plan, or an unassessed contract
"""

import argparse
import csv
import datetime as dt
import io
import json
import sys

ART30_2 = {
    "a": "clear description of all functions and ICT services, incl. whether subcontracting is permitted and on what conditions",
    "b": "locations (regions or countries) of service and data processing, and notice before they change",
    "c": "data protection: availability, authenticity, integrity, confidentiality, incl. personal data",
    "d": "access, recovery and return of data in an easily accessible format on insolvency, resolution, discontinuation or termination",
    "e": "service level descriptions, incl. updates and revisions",
    "f": "provider assistance in an ICT incident related to the service, at no extra cost or a cost set ex ante",
    "g": "provider cooperation with competent and resolution authorities",
    "h": "termination rights and minimum notice periods, per competent-authority expectations",
    "i": "provider participation in the entity's ICT security awareness and resilience training",
}
ART30_3 = {
    "a": "full service level descriptions with precise quantitative and qualitative performance targets",
    "b": "notice periods and reporting obligations to the entity, incl. developments that may affect service",
    "c": "provider implements and tests business contingency plans and has appropriate ICT security measures",
    "d": "provider participates and cooperates fully in the entity's TLPT (Arts 26-27)",
    "e": "unrestricted rights of access, inspection and audit by the entity, its auditor and the competent authority",
    "f": "exit strategies, in particular a mandatory adequate transition period",
}
EEA = set("AT BE BG HR CY CZ DK EE FI FR DE GR EL HU IE IT LV LT LU MT NL PL PT RO SK SI ES SE IS LI NO".split())
SEVERITY_ORDER = ["BLOCKER", "HIGH", "MEDIUM", "INFO"]

SAMPLE = """contract_id,provider,provider_lei,provider_country,service,critical_or_important,function,art30_2,art30_3,exit_plan,risk_assessment,subcontractors,substitutable,last_review
C-001,Cloudhost SE,529900ABCDEFGHIJ1234,DE,IaaS core banking,yes,payments;core-ledger,a;b;c;d;e;f;g;h;i,a;b;c;e;f,documented,yes,yes,no,2026-03-01
C-002,Cloudhost SE,529900ABCDEFGHIJ1234,DE,managed backup,yes,core-ledger,a;b;c;d;e;f;g;h;i,a;b;c;d;e;f,tested,yes,yes,yes,2026-06-12
C-003,CardSwitch Inc,,US,card processing,yes,card-issuing,a;b;c;e;g;h,a;b;e,none,no,unknown,unknown,2024-02-10
C-004,OfficeSuite BV,724500ZYXWVUTSRQ9876,NL,email and office,no,,a;b;c;d;e;g;h,,none,yes,yes,yes,2026-01-15
C-005,HR Payroll GmbH,391200QWERTYUIOP5555,DE,payroll SaaS,,,a;b;c,,none,,unknown,,
"""


def norm(v):
    return (v or "").strip()


def flags(row, col):
    return {x.strip().lower() for x in norm(row.get(col)).replace(",", ";").split(";") if x.strip()}


def yn(row, col, line, allow_unknown=False):
    v = norm(row.get(col)).lower()
    ok = {"yes", "no"} | ({"unknown"} if allow_unknown else set())
    if v and v not in ok:
        raise ValueError(f"row {line} {col}: '{v}' must be one of {', '.join(sorted(ok))}")
    return v or None


def run(text, today, review_months):
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise ValueError("register has no rows")
    missing_cols = {"contract_id", "provider", "critical_or_important", "art30_2"} - set(rows[0].keys())
    if missing_cols:
        raise ValueError("register is missing columns: " + ", ".join(sorted(missing_cols)))
    out, cif_by_provider, nonsub = [], {}, []
    for i, r in enumerate(rows):
        line = i + 2
        cid = norm(r.get("contract_id")) or f"row {line}"
        fs = []

        def add(sev, code, msg, ref):
            fs.append({"severity": sev, "code": code, "message": msg, "ref": ref})

        t2, t3 = flags(r, "art30_2"), flags(r, "art30_3")
        bad = (t2 - set(ART30_2)) | (t3 - set(ART30_3))
        if bad:
            raise ValueError(f"row {line} ({cid}): unknown term letters {', '.join(sorted(bad))}")
        cif = yn(r, "critical_or_important", line)
        ra = yn(r, "risk_assessment", line)
        sub = yn(r, "subcontractors", line, True)
        subst = yn(r, "substitutable", line, True)
        exitp = norm(r.get("exit_plan")).lower() or "none"
        if exitp not in {"tested", "documented", "none"}:
            raise ValueError(f"row {line} exit_plan: '{exitp}' must be tested, documented or none")
        country = norm(r.get("provider_country")).upper()
        prov = norm(r.get("provider"))

        if not norm(r.get("provider_lei")):
            add("HIGH", "NO_LEI", "provider has no LEI or EUID: the register templates identify every provider by it", "ITS 2024/2956")
        if cif is None:
            add("BLOCKER", "CIF_NOT_ASSESSED", "critical_or_important not assessed: you cannot tell which Art 30 terms apply", "DORA Art 28(3), Art 3(22)")
        miss2 = sorted(set(ART30_2) - t2)
        if miss2:
            add("HIGH", "ART30_2_MISSING", "missing " + "; ".join(f"({k}) {ART30_2[k]}" for k in miss2), "DORA Art 30(2)")
        if cif == "yes":
            miss3 = sorted(set(ART30_3) - t3)
            if miss3:
                add("BLOCKER", "ART30_3_MISSING", "contract supports a critical or important function but lacks " + "; ".join(f"({k}) {ART30_3[k]}" for k in miss3), "DORA Art 30(3)")
            if exitp == "none":
                add("BLOCKER", "NO_EXIT_PLAN", "no exit strategy for a critical or important function", "DORA Art 28(8)")
            elif exitp == "documented":
                add("MEDIUM", "EXIT_NOT_TESTED", "exit plan documented but not tested; Art 28(8) requires it be realistic, feasible and adequately tested", "DORA Art 28(8)")
            if ra != "yes":
                add("HIGH", "NO_RISK_ASSESSMENT", "no recorded pre-contract risk assessment and due diligence", "DORA Art 28(4)")
            if sub in (None, "unknown"):
                add("HIGH", "SUBCONTRACTING_UNKNOWN", "subcontracting chain unknown for a critical or important function", "DORA Art 29(2), Art 30(2)(a)")
            if country and country not in EEA:
                add("MEDIUM", "THIRD_COUNTRY", f"provider in {country} supports a critical or important function: assess insolvency law, data recovery and supervisory access", "DORA Art 29(2)")
            if subst in ("no", "unknown"):
                nonsub.append(cid)
            cif_by_provider.setdefault(prov, []).append(cid)
        rev = norm(r.get("last_review"))
        if rev:
            try:
                d = dt.date.fromisoformat(rev)
            except ValueError:
                raise ValueError(f"row {line} last_review: '{rev}' is not YYYY-MM-DD")
            if (today - d).days > review_months * 30.4:
                add("MEDIUM", "REVIEW_STALE", f"last reviewed {rev}, more than {review_months} months ago; the register is kept up to date", "DORA Art 28(3)")
        else:
            add("MEDIUM", "NO_REVIEW_DATE", "no last_review date", "DORA Art 28(3)")
        out.append({"contract_id": cid, "provider": prov, "critical_or_important": cif, "findings": fs})

    portfolio = []
    for prov, cids in cif_by_provider.items():
        if len(cids) >= 2:
            portfolio.append({"severity": "MEDIUM", "code": "CONCENTRATION",
                              "message": f"{prov} supports critical or important functions under {len(cids)} contracts ({', '.join(cids)}): assess ICT concentration risk",
                              "ref": "DORA Art 29(1)"})
    if nonsub:
        portfolio.append({"severity": "MEDIUM", "code": "NOT_SUBSTITUTABLE",
                          "message": f"no confirmed substitute for {', '.join(nonsub)}: weigh this in the concentration assessment and the exit plan",
                          "ref": "DORA Art 29(1)(a)"})
    counts = {s: 0 for s in SEVERITY_ORDER}
    for f in [f for c in out for f in c["findings"]] + portfolio:
        counts[f["severity"]] += 1
    verdict = "BLOCKED" if counts["BLOCKER"] else "GAPS" if counts["HIGH"] or counts["MEDIUM"] else "CLEAN"
    return {"verdict": verdict, "as_of": today.isoformat(),
            "summary": {"contracts": len(out), "critical_or_important": sum(1 for c in out if c["critical_or_important"] == "yes"), "findings": counts},
            "contracts": out, "portfolio": portfolio}


def render(o):
    lines = [f"DORA register of information: {o['verdict']}  (as of {o['as_of']})", ""]
    for c in o["contracts"]:
        tag = {"yes": "CIF", "no": "non-CIF", None: "UNASSESSED"}[c["critical_or_important"]]
        lines.append(f"- {c['contract_id']} {c['provider']} [{tag}]" + ("  ok" if not c["findings"] else ""))
        for f in sorted(c["findings"], key=lambda f: SEVERITY_ORDER.index(f["severity"])):
            lines.append(f"    {f['severity']:<7} {f['code']}: {f['message']} [{f['ref']}]")
    if o["portfolio"]:
        lines += ["", "Portfolio:"] + [f"    {f['severity']:<7} {f['code']}: {f['message']} [{f['ref']}]" for f in o["portfolio"]]
    s = o["summary"]
    lines += ["", f"{s['contracts']} contracts, {s['critical_or_important']} supporting critical or important functions. Findings: "
              + ", ".join(f"{k} {v}" for k, v in s["findings"].items())]
    lines += ["", "Rules last verified 2026-11-17. Not legal advice: confirm with counsel or the competent authority."]
    return "\n".join(lines)


EXIT = {"CLEAN": 0, "GAPS": 2, "BLOCKED": 4}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog="Exit codes: 0 clean, 2 gaps, 3 invalid input, 4 blocked.")
    p.add_argument("--register", help="register CSV (columns in the module docstring)")
    p.add_argument("--as-of", help="evaluation date YYYY-MM-DD (default: today)")
    p.add_argument("--review-months", type=int, default=12, help="flag contracts not reviewed within this many months (default 12)")
    p.add_argument("--list-terms", action="store_true", help="print the Art 30(2) and 30(3) term letters and exit")
    p.add_argument("--sample", action="store_true", help="run on a built-in example register")
    p.add_argument("--output", choices=["text", "json"], default="text")
    p.add_argument("--json", action="store_true", help="shorthand for --output json")
    a = p.parse_args(argv)
    if a.json:
        a.output = "json"
    if a.list_terms:
        print("Art 30(2), every contract:")
        print("\n".join(f"  {k}  {v}" for k, v in ART30_2.items()))
        print("Art 30(3), contracts supporting critical or important functions:")
        print("\n".join(f"  {k}  {v}" for k, v in ART30_3.items()))
        return 0
    try:
        if a.review_months < 1:
            raise ValueError("--review-months must be at least 1")
        if a.sample:
            text, today = SAMPLE, dt.date(2026, 11, 17)
        else:
            if not a.register:
                p.print_usage(sys.stderr)
                print("error: give --register or --sample", file=sys.stderr)
                return 3
            with open(a.register, newline="", encoding="utf-8-sig") as fh:
                text = fh.read()
            today = dt.date.fromisoformat(a.as_of) if a.as_of else dt.date.today()
        o = run(text, today, a.review_months)
    except (OSError, ValueError, csv.Error) as e:
        if a.output == "json":
            print(json.dumps({"verdict": "INVALID_INPUT", "errors": [str(e)]}, indent=2))
        else:
            print(f"error: {e}", file=sys.stderr)
        return 3
    print(json.dumps(o, indent=2) if a.output == "json" else render(o))
    return EXIT[o["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
