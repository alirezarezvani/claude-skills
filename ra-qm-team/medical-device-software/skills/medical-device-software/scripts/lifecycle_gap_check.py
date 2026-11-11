#!/usr/bin/env python3
"""Gap-check a medical device software lifecycle against IEC 62304 (by safety class) and IEC 81001-5-1.

Give the software safety class and an assessment CSV with one row per
requirement. The script works out which IEC 62304:2006+A1:2015 subclauses the
class requires, optionally adds the IEC 81001-5-1:2021 security activities,
refuses an assessment that skips a required id, and says what blocks a
release or a submission.

Requirement ids
  62304 subclauses, e.g. 5.1.1, 5.3.5, 9.8     (--list --class C prints those required for C)
  81001-5-1 activities prefixed S, e.g. S5.7.4  (added with --security)

Class applicability follows the class markers of IEC 62304:2006+A1:2015 as
reproduced by two independent secondary sources (Al Cohen's "IEC 62304 Items
by Class"; SimQ's class summary); the markers in your licensed copy prevail.
81001-5-1 headings are taken from the public IEC FDIS 81001-5-1 sample and
apply to all health software regardless of 62304 class.

Findings
  NOT_MET_REQUIRED     a required requirement NOT_MET                                   BLOCKER
  NA_NOT_ALLOWED       NA on a requirement that cannot be scoped out                     BLOCKER
  PARTIAL              partly met                                                       HIGH
  MET_NO_EVIDENCE      MET with no evidence reference                                    HIGH
  NA_NO_REASON         NA without a written justification                                HIGH
  LEGACY_NOT_ASSESSED  4.4 marked NA while the release note says legacy software is used  HIGH
  EXTRA_ROWS           ids that the class does not require (ignored, listed)             INFO

CSV columns: id, status (MET | PARTIAL | NOT_MET | NA), evidence, justification, owner

Deterministic, stdlib only, no network. It checks completeness and internal
consistency; whether the evidence is adequate is for the manufacturer's
reviewers and the notified body or FDA.

Exit codes:
    0  READY
    2  GAPS
    3  invalid input (unknown id, missing required ids, bad status)
    4  BLOCKED
"""

import argparse
import csv
import io
import json
import sys

ABC, BC, C = "ABC", "BC", "C"

# (id, title, classes, na_allowed)
R62304 = [
    ("4.1", "Quality management system", ABC, False),
    ("4.2", "Risk management (ISO 14971)", ABC, False),
    ("4.3", "Software safety classification", ABC, False),
    ("4.4", "Legacy software (NA only if no legacy software is used)", ABC, True),
    ("5.1.1", "Software development plan", ABC, False),
    ("5.1.2", "Keep software development plan updated", ABC, False),
    ("5.1.3", "Software development plan reference to system design and development", ABC, False),
    ("5.1.4", "Software development standards, methods and tools planning", C, False),
    ("5.1.5", "Software integration and integration testing planning", BC, False),
    ("5.1.6", "Software verification planning", ABC, False),
    ("5.1.7", "Software risk management planning", ABC, False),
    ("5.1.8", "Documentation planning", ABC, False),
    ("5.1.9", "Software configuration management planning", ABC, False),
    ("5.1.10", "Supporting items to be controlled", BC, False),
    ("5.1.11", "Software configuration item control before verification", BC, False),
    ("5.1.12", "Identification and avoidance of common software defects", BC, False),
    ("5.2.1", "Define and document software requirements from system requirements", ABC, False),
    ("5.2.2", "Software requirements content", ABC, False),
    ("5.2.3", "Include risk control measures in software requirements", BC, False),
    ("5.2.4", "Re-evaluate medical device risk analysis", ABC, False),
    ("5.2.5", "Update requirements", ABC, False),
    ("5.2.6", "Verify software requirements", ABC, False),
    ("5.3.1", "Transform software requirements into an architecture", BC, False),
    ("5.3.2", "Develop an architecture for the interfaces of software items", BC, False),
    ("5.3.3", "Specify functional and performance requirements of SOUP items", BC, True),
    ("5.3.4", "Specify system hardware and software required by SOUP items", BC, True),
    ("5.3.5", "Identify segregation necessary for risk control", C, True),
    ("5.3.6", "Verify software architecture", BC, False),
    ("5.4.1", "Subdivide software into software units", BC, False),
    ("5.4.2", "Develop detailed design for each software unit", C, False),
    ("5.4.3", "Develop detailed design for interfaces", C, False),
    ("5.4.4", "Verify detailed design", C, False),
    ("5.5.1", "Implement each software unit", ABC, False),
    ("5.5.2", "Establish software unit verification process", BC, False),
    ("5.5.3", "Software unit acceptance criteria", BC, False),
    ("5.5.4", "Additional software unit acceptance criteria", C, False),
    ("5.5.5", "Software unit verification", BC, False),
    ("5.6.1", "Integrate software units", BC, False),
    ("5.6.2", "Verify software integration", BC, False),
    ("5.6.3", "Software integration testing", BC, False),
    ("5.6.4", "Software integration testing content", BC, False),
    ("5.6.5", "Evaluate software integration test procedures", BC, False),
    ("5.6.6", "Conduct regression tests", BC, False),
    ("5.6.7", "Integration test record contents", BC, False),
    ("5.6.8", "Use software problem resolution process", BC, False),
    ("5.7.1", "Establish tests for software requirements", ABC, False),
    ("5.7.2", "Use software problem resolution process", ABC, False),
    ("5.7.3", "Retest after changes", ABC, False),
    ("5.7.4", "Evaluate software system testing", ABC, False),
    ("5.7.5", "Software system test record contents", ABC, False),
    ("5.8.1", "Ensure software verification is complete", ABC, False),
    ("5.8.2", "Document known residual anomalies", ABC, False),
    ("5.8.3", "Evaluate known residual anomalies", BC, False),
    ("5.8.4", "Document released versions", ABC, False),
    ("5.8.5", "Document how released software was created", BC, False),
    ("5.8.6", "Ensure activities and tasks are complete", BC, False),
    ("5.8.7", "Archive software", ABC, False),
    ("5.8.8", "Assure reliable delivery of released software", ABC, False),
    ("6.1", "Establish software maintenance plan", ABC, False),
    ("6.2.1", "Document and evaluate feedback (incl. effect of problem reports on safety)", ABC, False),
    ("6.2.2", "Use software problem resolution process", ABC, False),
    ("6.2.3", "Analyse change requests", ABC, False),
    ("6.2.4", "Change request approval", ABC, False),
    ("6.2.5", "Communicate to users and regulators", ABC, False),
    ("6.3.1", "Use established process to implement modification", ABC, False),
    ("6.3.2", "Re-release modified software system", ABC, False),
    ("7.1.1", "Identify software items that could contribute to a hazardous situation", BC, False),
    ("7.1.2", "Identify potential causes of contribution to a hazardous situation", BC, False),
    ("7.1.3", "Evaluate published SOUP anomaly lists", BC, True),
    ("7.1.4", "Document potential causes", BC, False),
    ("7.2.1", "Define risk control measures", BC, False),
    ("7.2.2", "Risk control measures implemented in software", BC, False),
    ("7.3.1", "Verify risk control measures", BC, False),
    ("7.3.3", "Document traceability", BC, False),
    ("7.4.1", "Analyse changes to medical device software with respect to safety", ABC, False),
    ("7.4.2", "Analyse impact of software changes on existing risk control measures", BC, False),
    ("7.4.3", "Perform risk management activities based on analyses", BC, False),
    ("8.1.1", "Establish means to identify configuration items", ABC, False),
    ("8.1.2", "Identify SOUP", ABC, True),
    ("8.1.3", "Identify system configuration documentation", ABC, False),
    ("8.2.1", "Approve change requests", ABC, False),
    ("8.2.2", "Implement changes", ABC, False),
    ("8.2.3", "Verify changes", ABC, False),
    ("8.2.4", "Provide means for traceability of change", ABC, False),
    ("8.3", "Configuration status accounting", ABC, False),
    ("9.1", "Prepare problem reports", ABC, False),
    ("9.2", "Investigate the problem", ABC, False),
    ("9.3", "Advise relevant parties", ABC, False),
    ("9.4", "Use change control process", ABC, False),
    ("9.5", "Maintain records", ABC, False),
    ("9.6", "Analyse problems for trends", ABC, False),
    ("9.7", "Verify software problem resolution", ABC, False),
    ("9.8", "Test documentation contents", ABC, False),
]

# IEC 81001-5-1:2021 activities (headings from the IEC FDIS public sample). Applies to all health software.
# na_allowed is this skill's policy, not a clause of the standard: 4.1.3 lets the manufacturer scope
# activities with a justification, but security risk management, vulnerability intake/handling and
# monitoring are never scoped out here, because FD&C Act 524B(b)(1) and MDCG 2019-16 expect them for any
# connected device.
R81001 = [
    ("S4.1.1", "Quality management system covers security activities", True),
    ("S4.1.2", "Identification of responsibilities", True),
    ("S4.1.3", "Identification of applicability (which activities apply to this product)", False),
    ("S4.1.4", "Security expertise of the people doing the activities", True),
    ("S4.1.5", "Software items from third-party suppliers", True),
    ("S4.1.6", "Continuous improvement", True),
    ("S4.1.7", "Disclosing security-related issues", False),
    ("S4.1.8", "Periodic review of security defect management", False),
    ("S4.1.9", "Accompanying documentation review", True),
    ("S4.2", "Security risk management", False),
    ("S4.3", "Software item classification relating to risk transfer (maintained / supported / required)", False),
    ("S5.1.1", "Activities in the life cycle process", True),
    ("S5.1.2", "Development environment security", True),
    ("S5.1.3", "Secure coding standards (planning)", True),
    ("S5.2.1", "Health software security requirements", False),
    ("S5.2.2", "Security requirements review", True),
    ("S5.2.3", "Security risks for required software", True),
    ("S5.3.1", "Defense-in-depth architecture/design", True),
    ("S5.3.2", "Secure design best practices", True),
    ("S5.3.3", "Security architectural design review", True),
    ("S5.4.1", "Software design best practices", True),
    ("S5.4.2", "Secure design", True),
    ("S5.4.3", "Secure health software interfaces", True),
    ("S5.4.4", "Detailed design verification for security", True),
    ("S5.5.1", "Secure coding standards (applied)", True),
    ("S5.5.2", "Security implementation review", True),
    ("S5.6", "Software integration testing", True),
    ("S5.7.1", "Security requirements testing", True),
    ("S5.7.2", "Threat mitigation testing", True),
    ("S5.7.3", "Vulnerability testing", True),
    ("S5.7.4", "Penetration testing", True),
    ("S5.7.5", "Managing conflicts of interest between testers and developers", True),
    ("S5.8.1", "Resolve findings prior to release", False),
    ("S5.8.2", "Release documentation", True),
    ("S5.8.3", "File integrity", True),
    ("S5.8.4", "Controls for private keys", True),
    ("S5.8.5", "Assessing and addressing security-related issues", True),
    ("S5.8.6", "Activity completion", True),
    ("S5.8.7", "Secure decommissioning guidelines for health software", True),
    ("S6.1.1", "Timely delivery of security updates", False),
    ("S6.2.1", "Monitoring public incident reports", False),
    ("S6.2.2", "Security update verification", True),
    ("S6.3.1", "Supported software security update documentation", True),
    ("S6.3.2", "Maintained software security update delivery", True),
    ("S6.3.3", "Maintained software security update integrity", True),
    ("S7.1.2", "Product security context", False),
    ("S7.2", "Identification of vulnerabilities, threats and associated adverse impacts", False),
    ("S7.3", "Estimation and evaluation of security risk", False),
    ("S7.4", "Controlling security risks", False),
    ("S7.5", "Monitoring the effectiveness of risk controls", False),
    ("S8", "Software configuration management (security)", True),
    ("S9.2", "Receiving notifications about vulnerabilities", False),
    ("S9.3", "Reviewing vulnerabilities", False),
    ("S9.4", "Analysing vulnerabilities", False),
    ("S9.5", "Addressing security-related issues", False),
]

STATUSES = {"MET", "PARTIAL", "NOT_MET", "NA"}
SEV = {"BLOCKER": 4, "HIGH": 2, "INFO": 0}


def catalogue(cls, security):
    reqs = [(i, t, f"IEC 62304 {i}", na) for i, t, classes, na in R62304 if cls in classes]
    if security:
        reqs += [(i, t, f"IEC 81001-5-1 {i[1:]}", na) for i, t, na in R81001]
    return reqs


SAMPLE_CLASS = "B"


def sample_text():
    rows = ["id,status,evidence,justification,owner"]
    for rid, _t, _r, _na in catalogue(SAMPLE_CLASS, True):
        status, ev, just = "MET", f"DHF/{rid}", ""
        if rid == "4.4":
            status, ev, just = "NA", "", "no legacy software: all items developed under this plan"
        elif rid == "5.6.3":
            status, ev = "PARTIAL", "ITP-002 draft"
        elif rid == "7.1.3":
            status, ev = "NOT_MET", ""
        elif rid == "S5.7.4":
            status, ev, just = "NA", "", "no network attack surface"
        elif rid == "S9.3":
            status, ev = "MET", ""
        rows.append(f"{rid},{status},{ev},{just},")
    return "\n".join(rows) + "\n"


def run(text, cls, security, legacy_used):
    reqs = catalogue(cls, security)
    known = {r[0]: r for r in reqs}
    all_ids = {i for i, *_ in R62304} | {i for i, *_ in R81001}
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise ValueError("no rows")
    for col in ("id", "status"):
        if col not in rows[0]:
            raise ValueError(f"missing column {col}")
    got, extra = {}, []
    for n, r in enumerate(rows, 2):
        rid = (r.get("id") or "").strip()
        st = (r.get("status") or "").strip().upper()
        if rid not in all_ids:
            raise ValueError(f"line {n}: unknown id {rid!r} (run --list)")
        if st not in STATUSES:
            raise ValueError(f"line {n}: status must be one of {sorted(STATUSES)}")
        if rid in got:
            raise ValueError(f"line {n}: duplicate id {rid}")
        if rid not in known:
            extra.append(rid)
            continue
        got[rid] = {"status": st, "evidence": (r.get("evidence") or "").strip(),
                    "justification": (r.get("justification") or "").strip(), "owner": (r.get("owner") or "").strip()}
    missing = [i for i in known if i not in got]
    if missing:
        raise ValueError(f"unassessed is not MET; {len(missing)} required ids missing for class {cls}: {', '.join(missing[:15])}"
                         + (" ..." if len(missing) > 15 else ""))
    findings = []
    for rid, (i, title, ref, na_ok) in known.items():
        g = got[rid]
        st = g["status"]
        if st == "NOT_MET":
            findings.append(("BLOCKER", "NOT_MET_REQUIRED", rid, f"{ref} {title}"))
        elif st == "NA":
            if not na_ok:
                findings.append(("BLOCKER", "NA_NOT_ALLOWED", rid, f"{ref} {title} cannot be scoped out for class {cls}"))
            elif not g["justification"]:
                findings.append(("HIGH", "NA_NO_REASON", rid, f"{ref} NA needs a written justification"))
            if rid == "4.4" and legacy_used:
                findings.append(("HIGH", "LEGACY_NOT_ASSESSED", rid, "legacy software declared but 4.4 gap analysis marked NA"))
        elif st == "PARTIAL":
            findings.append(("HIGH", "PARTIAL", rid, f"{ref} {title}"))
        elif st == "MET" and not g["evidence"]:
            findings.append(("HIGH", "MET_NO_EVIDENCE", rid, f"{ref} MET with no evidence reference"))
    if extra:
        findings.append(("INFO", "EXTRA_ROWS", ",".join(extra), f"not required for class {cls}; ignored"))
    worst = max([SEV[f[0]] for f in findings] or [0])
    verdict = {4: "BLOCKED", 2: "GAPS", 0: "READY"}[worst]
    order = {"BLOCKER": 0, "HIGH": 1, "INFO": 2}
    findings.sort(key=lambda f: order[f[0]])
    counts = {s: sum(1 for g in got.values() if g["status"] == s) for s in STATUSES}
    return {
        "verdict": verdict, "software_safety_class": cls, "security_81001_5_1": security,
        "required": len(known), "status_counts": counts,
        "findings": [{"severity": s, "code": c, "id": i, "detail": d} for s, c, i, d in findings],
        "note": "Class markers per IEC 62304:2006+A1:2015 via secondary sources; your licensed copy prevails. "
                "Evidence adequacy is for your reviewers and the notified body or FDA.",
    }


def render(out):
    lines = [f"IEC 62304 class {out['software_safety_class']}"
             + (" + IEC 81001-5-1" if out["security_81001_5_1"] else "")
             + f" lifecycle gap check: {out['verdict']}",
             f"{out['required']} required ids; " + ", ".join(f"{k} {v}" for k, v in sorted(out["status_counts"].items())), ""]
    for f in out["findings"]:
        lines.append(f"[{f['severity']}] {f['code']} {f['id']}: {f['detail']}")
    lines += ["", out["note"]]
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                epilog="Exit codes: 0 ready, 2 gaps, 3 invalid input, 4 blocked.")
    p.add_argument("--assessment", help="assessment CSV: id,status,evidence,justification,owner")
    p.add_argument("--class", dest="cls", choices=["A", "B", "C"], help="IEC 62304 software safety class")
    p.add_argument("--security", action="store_true", help="add the IEC 81001-5-1 activities (S-prefixed ids)")
    p.add_argument("--legacy", action="store_true", help="legacy software (IEC 62304 4.4) is part of this release")
    p.add_argument("--list", action="store_true", help="print the ids required for --class (and --security) and exit")
    p.add_argument("--template", action="store_true", help="print a blank assessment CSV for --class and exit")
    p.add_argument("--sample", action="store_true", help="run on a built-in class B + security example")
    p.add_argument("--output", choices=["text", "json"], default="text")
    p.add_argument("--json", action="store_true", help="shorthand for --output json")
    a = p.parse_args(argv)
    if a.json:
        a.output = "json"
    if a.sample:
        a.cls, a.security = SAMPLE_CLASS, True
    if (a.list or a.template or a.assessment) and not a.cls:
        print("error: --class A|B|C is required (run software_safety_classifier.py first)", file=sys.stderr)
        return 3
    if a.list:
        reqs = catalogue(a.cls, a.security)
        if a.output == "json":
            print(json.dumps([{"id": i, "title": t, "ref": r, "na_allowed": na} for i, t, r, na in reqs], indent=2))
        else:
            for i, t, r, na in reqs:
                print(f"{i:<8} {'NA ok ' if na else 'always'}  {t}")
            print(f"\n{len(reqs)} ids for class {a.cls}" + (" with IEC 81001-5-1" if a.security else ""))
        return 0
    if a.template:
        print("id,status,evidence,justification,owner")
        for i, *_ in catalogue(a.cls, a.security):
            print(f"{i},NOT_MET,,,")
        return 0
    try:
        if a.sample:
            text = sample_text()
        else:
            if not a.assessment:
                p.print_usage(sys.stderr)
                print("error: give --assessment, --list, --template or --sample", file=sys.stderr)
                return 3
            with open(a.assessment, newline="", encoding="utf-8-sig") as fh:
                text = fh.read()
        out = run(text, a.cls, a.security, a.legacy)
    except (OSError, ValueError, csv.Error) as e:
        if a.output == "json":
            print(json.dumps({"verdict": "INVALID_INPUT", "errors": [str(e)]}, indent=2))
        else:
            print(f"error: {e}", file=sys.stderr)
        return 3
    print(json.dumps(out, indent=2) if a.output == "json" else render(out))
    return {"BLOCKED": 4, "GAPS": 2, "READY": 0}[out["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
