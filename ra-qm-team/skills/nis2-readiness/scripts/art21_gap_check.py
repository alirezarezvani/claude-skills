#!/usr/bin/env python3
"""Check an entity's NIS2 Article 20/21/23 measures before an audit or supervisory request.

Essential and important entities must take appropriate and proportionate
technical, operational and organisational measures based on an all-hazards
approach, covering at least the ten areas of Art 21(2)(a)-(j); the management
body approves and oversees them and must be trained (Art 20). This script reads
a self-assessment (one row per requirement id), refuses a file that skips any
id, and reports what blocks, what is partial, and what has no evidence.

Statuses: MET, PARTIAL, NOT_MET, NA. NA is accepted only where the text itself
is conditional ("where appropriate"); everything else applies to every entity.
Unassessed is never MET.

For DNS, TLD, cloud, data centre, CDN, MSP, MSSP, marketplace, search engine,
social network and trust service providers, Implementing Regulation (EU)
2024/2690 Annex sets the technical and methodological requirements for each
area; use --digital-provider to have the report say so per area.

Assessment CSV columns: id, status, evidence, owner, notes   (use --template for a blank file)

Deterministic, stdlib only, no network. A gap list, not an audit opinion.

Exit codes:
    0  every requirement MET with evidence
    2  PARTIAL items or MET without evidence
    3  invalid input (unknown id, missing id, bad status, NA where not allowed)
    4  any NOT_MET
"""

import argparse
import csv
import io
import json
import sys

# id, requirement, reference, NA allowed
REQS = [
    ("GOV-1", "Management body approves the cybersecurity risk-management measures", "Art 20(1)", False),
    ("GOV-2", "Management body oversees implementation and can be held liable for infringements", "Art 20(1)", False),
    ("GOV-3", "Members of the management body follow cybersecurity training", "Art 20(2)", False),
    ("GOV-4", "Similar training offered to employees on a regular basis (Member States shall encourage)", "Art 20(2)", True),
    ("RSK-1", "Measures are proportionate and based on an all-hazards approach (risk exposure, size, likelihood, severity, cost) and documented", "Art 21(1)", False),
    ("A", "Policies on risk analysis and information system security", "Art 21(2)(a)", False),
    ("B", "Incident handling (prevention, detection, response, recovery)", "Art 21(2)(b)", False),
    ("C-1", "Business continuity: backup management", "Art 21(2)(c)", False),
    ("C-2", "Business continuity: disaster recovery", "Art 21(2)(c)", False),
    ("C-3", "Crisis management", "Art 21(2)(c)", False),
    ("D-1", "Supply chain security: security aspects of relationships with direct suppliers and service providers", "Art 21(2)(d)", False),
    ("D-2", "Supplier-specific vulnerabilities, product quality, secure development practices of suppliers considered", "Art 21(3)", False),
    ("D-3", "Results of Union coordinated supply-chain risk assessments taken into account", "Art 21(3), Art 22", False),
    ("E-1", "Security in acquisition, development and maintenance of network and information systems", "Art 21(2)(e)", False),
    ("E-2", "Vulnerability handling and disclosure", "Art 21(2)(e)", False),
    ("F", "Policies and procedures to assess the effectiveness of the measures", "Art 21(2)(f)", False),
    ("G-1", "Basic cyber hygiene practices", "Art 21(2)(g)", False),
    ("G-2", "Cybersecurity training", "Art 21(2)(g)", False),
    ("H", "Policies and procedures on cryptography and, where appropriate, encryption", "Art 21(2)(h)", False),
    ("I-1", "Human resources security", "Art 21(2)(i)", False),
    ("I-2", "Access control policies", "Art 21(2)(i)", False),
    ("I-3", "Asset management", "Art 21(2)(i)", False),
    ("P-1", "Environmental and physical security of network and information systems (all-hazards: power, fire, flood, physical access)", "Art 21(1)", False),
    ("J-1", "Multi-factor or continuous authentication solutions, where appropriate", "Art 21(2)(j)", True),
    ("J-2", "Secured voice, video and text communications, where appropriate", "Art 21(2)(j)", True),
    ("J-3", "Secured emergency communication systems within the entity, where appropriate", "Art 21(2)(j)", True),
    ("COR-1", "Necessary, appropriate and proportionate corrective measures taken without undue delay on non-compliance", "Art 21(4)", False),
    ("REP-1", "Process to classify significant incidents and send the 24 h early warning and 72 h notification, with named owners", "Art 23(3)-(4)", False),
    ("REP-2", "Process to inform service recipients of significant incidents and of significant cyber threats", "Art 23(1)-(2)", False),
    ("REG-1", "Registered with the competent authority; changes notified within two weeks", "Art 3(4), Art 27", False),
]
IDS = [r[0] for r in REQS]
BY_ID = {r[0]: r for r in REQS}
STATUSES = {"MET", "PARTIAL", "NOT_MET", "NA"}
# 2024/2690 Annex sections for digital providers
ANNEX_2690 = {"A": "Annex 1-2", "B": "Annex 3", "C-1": "Annex 4", "C-2": "Annex 4", "C-3": "Annex 4",
              "D-1": "Annex 5", "D-2": "Annex 5", "E-1": "Annex 6", "E-2": "Annex 6", "F": "Annex 7",
              "G-1": "Annex 8", "G-2": "Annex 8", "H": "Annex 9", "I-1": "Annex 10", "I-2": "Annex 11",
              "I-3": "Annex 12", "P-1": "Annex 13", "J-1": "Annex 11", "RSK-1": "Annex 2", "REP-1": "Annex 3"}
SEVERITY_ORDER = ["BLOCKER", "HIGH", "MEDIUM", "INFO"]


def sample():
    status = {"GOV-3": "NOT_MET", "D-2": "PARTIAL", "D-3": "PARTIAL", "E-2": "PARTIAL", "J-2": "NA",
              "J-3": "NA", "F": "PARTIAL", "REP-1": "NOT_MET", "GOV-4": "MET"}
    ev = {"GOV-1": "Board minutes 2026-03-12 item 4", "GOV-2": "Board minutes 2026-03-12; quarterly CISO report",
          "RSK-1": "Risk register v7", "A": "ISMS policy v3.2", "B": "IR plan v2", "C-1": "Backup SOP v4, restore test 2026-09",
          "C-2": "DR plan v2, failover test 2026-06", "C-3": "Crisis plan v1", "D-1": "Supplier policy v2",
          "E-1": "SDLC standard v5", "G-1": "Hygiene baseline v1", "G-2": "LMS completion 2026 Q3 92%", "H": "Crypto policy v1",
          "I-1": "HR security SOP", "I-2": "IAM policy v3", "I-3": "CMDB export 2026-10", "J-1": "",
          "COR-1": "CAPA log", "REP-2": "Customer comms SOP", "REG-1": "BSI registration receipt 2026-02-20", "GOV-4": "LMS"}
    rows = ["id,status,evidence,owner,notes"]
    for i in IDS:
        rows.append(f"{i},{status.get(i, 'MET')},{ev.get(i, '')},CISO,")
    return "\n".join(rows) + "\n"


def run(text, digital):
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise ValueError("assessment has no rows")
    if not {"id", "status"} <= set(rows[0].keys()):
        raise ValueError("assessment needs columns id,status (evidence, owner, notes optional)")
    seen, errors = {}, []
    for n, r in enumerate(rows, start=2):
        rid = (r.get("id") or "").strip().upper()
        st = (r.get("status") or "").strip().upper().replace(" ", "_")
        if rid not in BY_ID:
            errors.append(f"row {n}: unknown id '{rid}' (see --list)")
            continue
        if rid in seen:
            errors.append(f"row {n}: duplicate id {rid}")
        if st not in STATUSES:
            errors.append(f"row {n} {rid}: status '{st}' must be one of MET, PARTIAL, NOT_MET, NA")
        elif st == "NA" and not BY_ID[rid][3]:
            errors.append(f"row {n} {rid}: NA not allowed, {BY_ID[rid][2]} applies to every entity in scope")
        seen[rid] = {"status": st, "evidence": (r.get("evidence") or "").strip(), "owner": (r.get("owner") or "").strip()}
    missing = [i for i in IDS if i not in seen]
    if missing:
        errors.append(f"unassessed ids (unassessed is not MET): {', '.join(missing)}")
    if errors:
        raise ValueError("; ".join(errors))

    items, counts = [], {s: 0 for s in SEVERITY_ORDER}
    for rid, text_, ref, _ in REQS:
        s = seen[rid]
        sev = code = None
        if s["status"] == "NOT_MET":
            sev, code = "BLOCKER", "NOT_MET"
        elif s["status"] == "PARTIAL":
            sev, code = "HIGH", "PARTIAL"
        elif s["status"] == "MET" and not s["evidence"]:
            sev, code = "MEDIUM", "NO_EVIDENCE"
        elif s["status"] == "MET" and not s["owner"]:
            sev, code = "MEDIUM", "NO_OWNER"
        item = {"id": rid, "requirement": text_, "ref": ref, **s}
        if digital and rid in ANNEX_2690:
            item["detail"] = f"Implementing Regulation (EU) 2024/2690 {ANNEX_2690[rid]}"
        if sev:
            item["severity"], item["code"] = sev, code
            counts[sev] += 1
        items.append(item)
    verdict = "BLOCKED" if counts["BLOCKER"] else "GAPS" if counts["HIGH"] or counts["MEDIUM"] else "READY"
    return {"verdict": verdict, "digital_provider": digital,
            "summary": {"requirements": len(items), "met": sum(1 for i in items if i["status"] == "MET"),
                        "na": sum(1 for i in items if i["status"] == "NA"), "findings": counts},
            "items": items}


def render(out):
    lines = [f"NIS2 Art 20/21/23 gap check: {out['verdict']}", ""]
    flagged = sorted([i for i in out["items"] if i.get("severity")], key=lambda i: SEVERITY_ORDER.index(i["severity"]))
    for i in flagged:
        d = f"  -> {i['detail']}" if i.get("detail") else ""
        lines.append(f"  {i['severity']:<7} {i['id']:<6} {i['code']:<11} {i['requirement']} [{i['ref']}]{d}")
    if not flagged:
        lines.append("  no gaps")
    s = out["summary"]
    lines += ["", f"{s['met']}/{s['requirements']} MET, {s['na']} NA. Findings: " + ", ".join(f"{k} {v}" for k, v in s["findings"].items())]
    if out["digital_provider"]:
        lines.append("Digital provider: each area is specified in Implementing Regulation (EU) 2024/2690 Annex; audit against that text.")
    lines += ["", "Rules last verified 2026-11-17. Not legal advice: confirm with counsel or the competent authority."]
    return "\n".join(lines)


EXIT = {"READY": 0, "GAPS": 2, "BLOCKED": 4}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog="Exit codes: 0 ready, 2 gaps, 3 invalid input, 4 NOT_MET present.")
    p.add_argument("--assessment", help="assessment CSV: id,status,evidence,owner,notes")
    p.add_argument("--digital-provider", action="store_true", help="entity is covered by Implementing Regulation (EU) 2024/2690")
    p.add_argument("--list", action="store_true", help="print the requirement ids")
    p.add_argument("--template", action="store_true", help="print a blank assessment CSV")
    p.add_argument("--sample", action="store_true", help="run on a built-in example")
    p.add_argument("--output", choices=["text", "json"], default="text")
    p.add_argument("--json", action="store_true", help="shorthand for --output json")
    a = p.parse_args(argv)
    if a.json:
        a.output = "json"
    if a.list:
        for rid, t, ref, na in REQS:
            print(f"  {rid:<6} {t} [{ref}]{' (NA allowed)' if na else ''}")
        return 0
    if a.template:
        print("id,status,evidence,owner,notes")
        for rid in IDS:
            print(f"{rid},,,,")
        return 0
    try:
        if a.sample:
            text = sample()
        else:
            if not a.assessment:
                p.print_usage(sys.stderr)
                print("error: give --assessment, --template or --sample", file=sys.stderr)
                return 3
            with open(a.assessment, newline="", encoding="utf-8-sig") as fh:
                text = fh.read()
        out = run(text, a.digital_provider)
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
