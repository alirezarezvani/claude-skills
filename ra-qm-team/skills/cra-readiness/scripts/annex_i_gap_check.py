#!/usr/bin/env python3
"""Check a CRA readiness assessment against Annex I, Annex II and Annex VII before the EU declaration of conformity.

A manufacturer may sign the EU declaration of conformity and affix the CE
marking only once conformity with the essential cybersecurity requirements is
demonstrated (Art 13(12), Art 28). This script reads one row per requirement,
refuses an assessment that skips any, and says what stands between the product
and a signable declaration.

Requirement ids (all 39 must be present)
  P1-1, P1-2a .. P1-2m   Annex I Part I: cybersecurity properties of the product
  P2-1 .. P2-8           Annex I Part II: vulnerability handling (applies to every product)
  TD-1 .. TD-8           Annex VII: technical documentation
  UI-1 .. UI-9           Annex II: information and instructions to the user
  Run --list to print them with titles.

Findings
  NOT_MET_ESSENTIAL   an Annex I requirement NOT_MET: no declaration can be signed           BLOCKER
  NA_NOT_ALLOWED      NA on a requirement that applies to every product                       BLOCKER
  NOT_MET_DOC         Annex VII or Annex II item NOT_MET                                      HIGH
  PARTIAL             a requirement only partly met                                           HIGH
  MET_NO_EVIDENCE     MET with no evidence reference                                          HIGH
  NA_NO_REASON        NA without the written justification Art 13(4) requires                 HIGH
  SBOM_NOT_CHECKED    P2-1 marked MET without a passing sbom_check.py run noted in evidence    MEDIUM

CSV columns: id, status (MET | PARTIAL | NOT_MET | NA), evidence, justification, owner

Deterministic, stdlib only, no network. It checks completeness and internal
consistency; whether evidence actually demonstrates conformity is for the
manufacturer and, on routes B+C or H, the notified body.

Exit codes:
    0  READY_FOR_DECLARATION
    2  GAPS (HIGH or MEDIUM findings)
    3  invalid input (unknown id, missing ids, bad status)
    4  BLOCKED
"""

import argparse
import csv
import io
import json
import sys

REQS = [
    ("P1-1", "Designed, developed and produced to ensure a cybersecurity level appropriate to the risks", "Annex I Part I(1)", False),
    ("P1-2a", "Made available without known exploitable vulnerabilities", "Annex I Part I(2)(a)", False),
    ("P1-2b", "Secure by default configuration, with reset to the original state", "Annex I Part I(2)(b)", True),
    ("P1-2c", "Vulnerabilities addressable by security updates; automatic updates on by default with opt-out, notification, postponement", "Annex I Part I(2)(c)", True),
    ("P1-2d", "Protection from unauthorised access (authentication, identity or access management) and reporting of possible unauthorised access", "Annex I Part I(2)(d)", True),
    ("P1-2e", "Confidentiality of stored, transmitted or processed data (e.g. state-of-the-art encryption at rest and in transit)", "Annex I Part I(2)(e)", True),
    ("P1-2f", "Integrity of data, commands, programs and configuration; report corruption", "Annex I Part I(2)(f)", True),
    ("P1-2g", "Data minimisation: process only data adequate, relevant and limited to the intended purpose", "Annex I Part I(2)(g)", True),
    ("P1-2h", "Availability of essential and basic functions, incl. after an incident; resilience against denial-of-service", "Annex I Part I(2)(h)", True),
    ("P1-2i", "Minimise negative impact on the availability of services provided by other devices or networks", "Annex I Part I(2)(i)", True),
    ("P1-2j", "Limit attack surfaces, including external interfaces", "Annex I Part I(2)(j)", True),
    ("P1-2k", "Reduce incident impact with exploitation mitigation mechanisms and techniques", "Annex I Part I(2)(k)", True),
    ("P1-2l", "Record and monitor relevant internal activity (access to or modification of data, services, functions), with user opt-out", "Annex I Part I(2)(l)", True),
    ("P1-2m", "Users can securely and easily remove all data and settings permanently; secure transfer where data moves to other systems", "Annex I Part I(2)(m)", True),
    ("P2-1", "Identify and document vulnerabilities and components, incl. a machine-readable SBOM covering at least top-level dependencies", "Annex I Part II(1)", False),
    ("P2-2", "Address and remediate vulnerabilities without delay, incl. security updates; separate from functionality updates where technically feasible", "Annex I Part II(2)", False),
    ("P2-3", "Effective and regular tests and reviews of the product's security", "Annex I Part II(3)", False),
    ("P2-4", "Once an update is available, share and publicly disclose fixed vulnerabilities (description, products, impact, severity, remediation)", "Annex I Part II(4)", False),
    ("P2-5", "Put in place and enforce a coordinated vulnerability disclosure policy", "Annex I Part II(5)", False),
    ("P2-6", "Facilitate sharing of information on potential vulnerabilities, incl. a contact address for reports", "Annex I Part II(6)", False),
    ("P2-7", "Mechanisms to securely distribute updates, automatically where applicable for security updates", "Annex I Part II(7)", False),
    ("P2-8", "Disseminate security updates without delay and free of charge, with advisory messages", "Annex I Part II(8)", False),
    ("TD-1", "General description: intended purpose, software versions, hardware photos/layout, user information", "Annex VII(1)", False),
    ("TD-2", "Design, development, production and vulnerability handling (SBOM, CVD policy, contact address, update distribution)", "Annex VII(2)", False),
    ("TD-3", "Cybersecurity risk assessment (Art 13) and how Annex I Part I applies", "Annex VII(3)", False),
    ("TD-4", "Information taken into account to determine the support period (Art 13(8))", "Annex VII(4)", False),
    ("TD-5", "Harmonised standards, common specifications or certification schemes applied, or the solutions adopted instead", "Annex VII(5)", False),
    ("TD-6", "Reports of tests verifying conformity with Annex I Parts I and II", "Annex VII(6)", False),
    ("TD-7", "Copy of the EU declaration of conformity", "Annex VII(7)", False),
    ("TD-8", "SBOM, available on reasoned request of a market surveillance authority", "Annex VII(8)", True),
    ("UI-1", "Manufacturer name, postal address, email or other digital contact, website", "Annex II(1)", False),
    ("UI-2", "Single point of contact for vulnerability reports and where the CVD policy is found", "Annex II(2)", False),
    ("UI-3", "Name, type and information to uniquely identify the product", "Annex II(3)", False),
    ("UI-4", "Intended purpose, security environment, essential functionalities and security properties", "Annex II(4)", False),
    ("UI-5", "Known or foreseeable circumstances leading to significant cybersecurity risks", "Annex II(5)", False),
    ("UI-6", "Internet address of the EU declaration of conformity, where applicable", "Annex II(6)", True),
    ("UI-7", "Type of technical security support and the end date of the support period", "Annex II(7)", False),
    ("UI-8", "Detailed instructions: secure commissioning and use, effect of changes, installing updates, secure decommissioning, turning off automatic updates, integrator information", "Annex II(8)", False),
    ("UI-9", "Where the SBOM can be accessed, if the manufacturer makes it available to users", "Annex II(9)", True),
]
IDS = [r[0] for r in REQS]
INFO = {r[0]: {"title": r[1], "ref": r[2], "na_allowed": r[3]} for r in REQS}
CANON = {x.upper(): x for x in IDS}
STATUSES = {"MET", "PARTIAL", "NOT_MET", "NA"}
SEVERITY_ORDER = ["BLOCKER", "HIGH", "MEDIUM"]


def _sample():
    rows = ["id,status,evidence,justification,owner"]
    special = {
        "P1-2b": ("PARTIAL", "default admin password rotated at first boot; reset tested on v4 only", "", "Firmware"),
        "P1-2g": ("NA", "", "", "Privacy"),
        "P1-2l": ("NOT_MET", "", "", "Platform"),
        "P1-2m": ("NA", "", "Device stores no user data; all telemetry is forwarded and not retained (risk assessment RA-7 s.4)", "Platform"),
        "P2-1": ("MET", "sbom/cyclonedx-1.6.json", "", "Release eng"),
        "P2-5": ("MET", "", "", "PSIRT"),
        "TD-4": ("NOT_MET", "", "", "Product"),
        "TD-8": ("NA", "", "", "Release eng"),
        "UI-9": ("NA", "", "SBOM is not shared with users", "Product"),
    }
    for rid in IDS:
        st, ev, ju, ow = special.get(rid, ("MET", f"evidence/{rid}.md", "", "Security"))
        rows.append(f"{rid},{st},{ev},\"{ju}\",{ow}")
    return "\n".join(rows) + "\n"


SAMPLE = _sample()


def run(text):
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows or "id" not in rows[0] or "status" not in rows[0]:
        raise ValueError("assessment CSV needs at least id and status columns")
    seen = {}
    for i, r in enumerate(rows, start=2):
        rid = CANON.get((r.get("id") or "").strip().upper(), (r.get("id") or "").strip())
        st = (r.get("status") or "").strip().upper().replace(" ", "_")
        if rid not in INFO:
            raise ValueError(f"row {i}: unknown id '{rid}' (run --list)")
        if rid in seen:
            raise ValueError(f"row {i}: duplicate id {rid}")
        if st not in STATUSES:
            raise ValueError(f"row {i} ({rid}): status '{st}' is not MET, PARTIAL, NOT_MET or NA")
        seen[rid] = {"status": st, "evidence": (r.get("evidence") or "").strip(),
                     "justification": (r.get("justification") or "").strip(), "owner": (r.get("owner") or "").strip()}
    missing = [x for x in IDS if x not in seen]
    if missing:
        raise ValueError(f"{len(missing)} requirements not assessed (unassessed is not MET): {', '.join(missing)}")

    findings = []

    def add(sev, code, rid, msg):
        findings.append({"severity": sev, "code": code, "id": rid, "ref": INFO[rid]["ref"],
                         "owner": seen[rid]["owner"], "message": msg})

    for rid in IDS:
        row, meta = seen[rid], INFO[rid]
        essential = rid.startswith("P")
        st = row["status"]
        if st == "NOT_MET":
            if essential:
                add("BLOCKER", "NOT_MET_ESSENTIAL", rid, f"{meta['title']}")
            else:
                add("HIGH", "NOT_MET_DOC", rid, f"{meta['title']}")
        elif st == "PARTIAL":
            add("HIGH", "PARTIAL", rid, f"{meta['title']}" + (f" ({row['evidence']})" if row["evidence"] else ""))
        elif st == "NA":
            if not meta["na_allowed"]:
                why = {"P2": "Annex I Part II has no 'where applicable': vulnerability handling applies to every product",
                       "P1-2a": "no product may be made available with known exploitable vulnerabilities, so this cannot be NA"}.get(
                          rid if rid == "P1-2a" else rid[:2], "this applies to every product")
                add("BLOCKER", "NA_NOT_ALLOWED", rid, f"{meta['title']}: {why}")
            elif not row["justification"]:
                why = ("an Annex I requirement marked not applicable needs a justification in the technical documentation (Art 13(4))"
                       if essential else "record why this item does not apply to the product")
                add("HIGH", "NA_NO_REASON", rid, why)
        elif st == "MET":
            if not row["evidence"]:
                add("HIGH", "MET_NO_EVIDENCE", rid, f"{meta['title']}: name the test report, document or artefact")
            elif rid == "P2-1" and "sbom_check" not in row["evidence"].lower():
                add("MEDIUM", "SBOM_NOT_CHECKED", rid, "run sbom_check.py on the SBOM and cite its PASS in the evidence column")

    counts = {s: sum(1 for f in findings if f["severity"] == s) for s in SEVERITY_ORDER}
    status_counts = {s: sum(1 for r in seen.values() if r["status"] == s) for s in sorted(STATUSES)}
    verdict = "BLOCKED" if counts["BLOCKER"] else "GAPS" if findings else "READY_FOR_DECLARATION"
    findings.sort(key=lambda f: (SEVERITY_ORDER.index(f["severity"]), IDS.index(f["id"])))
    return {"verdict": verdict, "summary": {"requirements": len(IDS), "status": status_counts, "findings": counts},
            "findings": findings}


def render(out):
    s = out["summary"]
    lines = [f"Annex I / II / VII readiness: {out['verdict']}",
             f"{s['requirements']} requirements: " + ", ".join(f"{k} {v}" for k, v in s["status"].items()), ""]
    for f in out["findings"]:
        owner = f" (owner: {f['owner']})" if f["owner"] else ""
        lines.append(f"{f['severity']:<7} {f['code']:<18} {f['id']:<6} {f['message']} [{f['ref']}]{owner}")
    if not out["findings"]:
        lines.append("No gaps recorded. The declaration is the manufacturer's: name who signs it (Art 28).")
    lines += ["", "Completeness check only: it does not judge whether the evidence demonstrates conformity."]
    return "\n".join(lines)


EXIT = {"READY_FOR_DECLARATION": 0, "GAPS": 2, "BLOCKED": 4}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog="Exit codes: 0 ready, 2 gaps, 3 invalid input, 4 blocked.")
    p.add_argument("--assessment", help="assessment CSV: id,status,evidence,justification,owner")
    p.add_argument("--list", action="store_true", help="print all requirement ids with titles and exit")
    p.add_argument("--template", action="store_true", help="print a blank assessment CSV with every id and exit")
    p.add_argument("--sample", action="store_true", help="run on a built-in example assessment")
    p.add_argument("--output", choices=["text", "json"], default="text")
    p.add_argument("--json", action="store_true", help="shorthand for --output json")
    a = p.parse_args(argv)
    if a.json:
        a.output = "json"
    if a.list:
        if a.output == "json":
            print(json.dumps(INFO, indent=2))
        else:
            for rid, title, ref, na in REQS:
                print(f"{rid:<6} {ref:<22} {'NA ok ' if na else 'always'}  {title}")
        return 0
    if a.template:
        print("id,status,evidence,justification,owner")
        for rid in IDS:
            print(f"{rid},NOT_MET,,,")
        return 0
    try:
        if a.sample:
            text = SAMPLE
        else:
            if not a.assessment:
                p.print_usage(sys.stderr)
                print("error: give --assessment, --list, --template or --sample", file=sys.stderr)
                return 3
            with open(a.assessment, newline="", encoding="utf-8-sig") as fh:
                text = fh.read()
        out = run(text)
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
