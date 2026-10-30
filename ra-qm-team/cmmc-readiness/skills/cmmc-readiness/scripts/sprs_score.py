#!/usr/bin/env python3
"""Score a CMMC Level 2 self-assessment and say whether it can reach Conditional or Final status.

Scoring follows 32 CFR 170.24(c)(2): start at 110 (one per NIST SP 800-171
Rev 2 requirement) and subtract 5, 3 or 1 for each requirement NOT MET. Two
requirements take partial credit: IA.L2-3.5.3 (MFA) and SC.L2-3.13.11
(FIPS-validated encryption) each cost 3 when PARTIAL and 5 when NOT MET.
CA.L2-3.12.4 (the System Security Plan) carries no points: without a current
SSP the assessment cannot be completed at all. The same score is what a Basic
self-assessment reports to SPRS under DFARS 252.204-7019/7020.

Conditional status (32 CFR 170.21(a)(2)) needs score/110 >= 0.8 (88 or more)
and every NOT MET requirement POA&M-eligible: worth 1 point, not one of the
six that can never be deferred (AC.L2-3.1.20, AC.L2-3.1.22, CA.L2-3.12.4,
PE.L2-3.10.3, PE.L2-3.10.4, PE.L2-3.10.5), with one exception: SC.L2-3.13.11
PARTIAL (encryption used, not FIPS-validated) may go on the POA&M at 3 points.

Verdicts
  FINAL_ELIGIBLE        110 of 110, nothing to defer                      exit 0
  CONDITIONAL_ELIGIBLE  88+ and every gap POA&M-eligible; 180 days to close exit 2
  NOT_ELIGIBLE          under 88, or a gap that cannot be deferred        exit 4
  BLOCKED_NO_SSP        CA.L2-3.12.4 not met: no assessment can finish    exit 4

Input CSV columns: requirement_id, status, justification (optional), evidence (optional)
  requirement_id  AC.L2-3.1.1 or 3.1.1
  status          MET | NOT_MET | NA | PARTIAL  (PARTIAL only for 3.5.3 and 3.13.11)
  justification   required for NA; an NA the assessor rejects becomes NOT MET
Every one of the 110 requirements must appear exactly once. A requirement you
have not assessed is not MET: the script refuses to guess it.

Deterministic, stdlib only, no network. Not an assessment: a C3PAO or DIBCAC
assessor decides MET, and only the Affirming Official affirms in SPRS.

Exit codes:
    0  FINAL_ELIGIBLE
    2  CONDITIONAL_ELIGIBLE
    3  invalid input
    4  NOT_ELIGIBLE or BLOCKED_NO_SSP
"""

import argparse
import csv
import io
import json
import sys

# (family, requirement number, points, short title). Points per 32 CFR 170.24(c)(2)(i)(B);
# 3.5.3 and 3.13.11 are variable (3 partial / 5 not met), 3.12.4 is unscored.
REQUIREMENTS = [
    ("AC", "3.1.1", 5, "Limit system access to authorized users, processes and devices"),
    ("AC", "3.1.2", 5, "Limit access to permitted transactions and functions"),
    ("AC", "3.1.3", 1, "Control the flow of CUI per approved authorizations"),
    ("AC", "3.1.4", 1, "Separate duties to reduce collusion risk"),
    ("AC", "3.1.5", 3, "Least privilege, including for privileged accounts"),
    ("AC", "3.1.6", 1, "Use non-privileged accounts for non-security functions"),
    ("AC", "3.1.7", 1, "Prevent non-privileged users running privileged functions; audit them"),
    ("AC", "3.1.8", 1, "Limit unsuccessful logon attempts"),
    ("AC", "3.1.9", 1, "Privacy and security notices consistent with CUI rules"),
    ("AC", "3.1.10", 1, "Session lock with pattern-hiding display"),
    ("AC", "3.1.11", 1, "Terminate user sessions after a defined condition"),
    ("AC", "3.1.12", 5, "Monitor and control remote access sessions"),
    ("AC", "3.1.13", 5, "Cryptographic protection of remote access sessions"),
    ("AC", "3.1.14", 1, "Route remote access through managed access control points"),
    ("AC", "3.1.15", 1, "Authorize remote privileged commands and security information access"),
    ("AC", "3.1.16", 5, "Authorize wireless access before connection"),
    ("AC", "3.1.17", 5, "Protect wireless access with authentication and encryption"),
    ("AC", "3.1.18", 5, "Control connection of mobile devices"),
    ("AC", "3.1.19", 3, "Encrypt CUI on mobile devices and platforms"),
    ("AC", "3.1.20", 1, "Verify and control connections to external systems"),
    ("AC", "3.1.21", 1, "Limit portable storage use on external systems"),
    ("AC", "3.1.22", 1, "Control CUI posted on publicly accessible systems"),
    ("AT", "3.2.1", 5, "Security awareness of risks for managers, admins and users"),
    ("AT", "3.2.2", 5, "Train personnel for their security duties"),
    ("AT", "3.2.3", 1, "Insider threat awareness training"),
    ("AU", "3.3.1", 5, "Create and retain audit logs to monitor and investigate"),
    ("AU", "3.3.2", 3, "Trace actions to individual users"),
    ("AU", "3.3.3", 1, "Review and update logged events"),
    ("AU", "3.3.4", 1, "Alert on audit logging process failure"),
    ("AU", "3.3.5", 5, "Correlate audit review, analysis and reporting"),
    ("AU", "3.3.6", 1, "Audit record reduction and report generation"),
    ("AU", "3.3.7", 1, "Synchronize system clocks to an authoritative source"),
    ("AU", "3.3.8", 1, "Protect audit information and tools"),
    ("AU", "3.3.9", 1, "Limit audit logging management to a subset of privileged users"),
    ("CM", "3.4.1", 5, "Baseline configurations and inventories"),
    ("CM", "3.4.2", 5, "Enforce security configuration settings"),
    ("CM", "3.4.3", 1, "Track, review, approve and log changes"),
    ("CM", "3.4.4", 1, "Analyze security impact of changes"),
    ("CM", "3.4.5", 5, "Physical and logical access restrictions for changes"),
    ("CM", "3.4.6", 5, "Least functionality: essential capabilities only"),
    ("CM", "3.4.7", 5, "Restrict nonessential programs, ports, protocols and services"),
    ("CM", "3.4.8", 5, "Application blacklisting or whitelisting policy"),
    ("CM", "3.4.9", 1, "Control and monitor user-installed software"),
    ("IA", "3.5.1", 5, "Identify users, processes and devices"),
    ("IA", "3.5.2", 5, "Authenticate users, processes and devices"),
    ("IA", "3.5.3", 5, "Multifactor authentication for local/network privileged and network access"),
    ("IA", "3.5.4", 1, "Replay-resistant authentication for network access"),
    ("IA", "3.5.5", 1, "Prevent identifier reuse for a defined period"),
    ("IA", "3.5.6", 1, "Disable identifiers after a defined inactivity period"),
    ("IA", "3.5.7", 1, "Minimum password complexity and change of characters"),
    ("IA", "3.5.8", 1, "Prohibit password reuse for a number of generations"),
    ("IA", "3.5.9", 1, "Temporary passwords with immediate change"),
    ("IA", "3.5.10", 5, "Store and transmit only cryptographically protected passwords"),
    ("IA", "3.5.11", 1, "Obscure authentication feedback"),
    ("IR", "3.6.1", 5, "Operational incident-handling capability"),
    ("IR", "3.6.2", 5, "Track, document and report incidents"),
    ("IR", "3.6.3", 1, "Test the incident response capability"),
    ("MA", "3.7.1", 3, "Perform maintenance"),
    ("MA", "3.7.2", 5, "Control maintenance tools, techniques and personnel"),
    ("MA", "3.7.3", 1, "Sanitize equipment removed for off-site maintenance"),
    ("MA", "3.7.4", 3, "Check maintenance media for malicious code"),
    ("MA", "3.7.5", 5, "MFA for nonlocal maintenance; terminate when done"),
    ("MA", "3.7.6", 1, "Supervise maintenance personnel without access authorization"),
    ("MP", "3.8.1", 3, "Protect system media containing CUI"),
    ("MP", "3.8.2", 3, "Limit access to CUI on media to authorized users"),
    ("MP", "3.8.3", 5, "Sanitize or destroy media before disposal or reuse"),
    ("MP", "3.8.4", 1, "Mark media with CUI markings and distribution limits"),
    ("MP", "3.8.5", 1, "Control access to and accountability for media in transport"),
    ("MP", "3.8.6", 1, "Cryptographically protect CUI on digital media in transport"),
    ("MP", "3.8.7", 5, "Control removable media on system components"),
    ("MP", "3.8.8", 3, "Prohibit portable storage with no identifiable owner"),
    ("MP", "3.8.9", 1, "Protect confidentiality of backup CUI"),
    ("PS", "3.9.1", 3, "Screen individuals before authorizing access"),
    ("PS", "3.9.2", 5, "Protect CUI during terminations and transfers"),
    ("PE", "3.10.1", 5, "Limit physical access to authorized individuals"),
    ("PE", "3.10.2", 5, "Protect and monitor the physical facility"),
    ("PE", "3.10.3", 1, "Escort and monitor visitors"),
    ("PE", "3.10.4", 1, "Keep audit logs of physical access"),
    ("PE", "3.10.5", 1, "Control and manage physical access devices"),
    ("PE", "3.10.6", 1, "Safeguard CUI at alternate work sites"),
    ("RA", "3.11.1", 3, "Periodically assess risk"),
    ("RA", "3.11.2", 5, "Scan for vulnerabilities periodically and when new ones are identified"),
    ("RA", "3.11.3", 1, "Remediate vulnerabilities per risk assessments"),
    ("CA", "3.12.1", 5, "Periodically assess security controls"),
    ("CA", "3.12.2", 3, "Plans of action to correct deficiencies"),
    ("CA", "3.12.3", 5, "Monitor security controls on an ongoing basis"),
    ("CA", "3.12.4", 0, "Develop, document and update the System Security Plan"),
    ("SC", "3.13.1", 5, "Monitor, control and protect communications at boundaries"),
    ("SC", "3.13.2", 5, "Architectural designs and engineering principles for security"),
    ("SC", "3.13.3", 1, "Separate user functionality from system management"),
    ("SC", "3.13.4", 1, "Prevent unauthorized information transfer via shared resources"),
    ("SC", "3.13.5", 5, "Subnetworks for publicly accessible components"),
    ("SC", "3.13.6", 5, "Deny network traffic by default, permit by exception"),
    ("SC", "3.13.7", 1, "Prevent split tunneling for remote devices"),
    ("SC", "3.13.8", 3, "Cryptographic protection of CUI in transmission"),
    ("SC", "3.13.9", 1, "Terminate network connections at session end or inactivity"),
    ("SC", "3.13.10", 1, "Establish and manage cryptographic keys"),
    ("SC", "3.13.11", 5, "FIPS-validated cryptography protecting CUI"),
    ("SC", "3.13.12", 1, "Prohibit remote activation of collaborative computing devices"),
    ("SC", "3.13.13", 1, "Control and monitor mobile code"),
    ("SC", "3.13.14", 1, "Control and monitor VoIP"),
    ("SC", "3.13.15", 5, "Protect authenticity of communications sessions"),
    ("SC", "3.13.16", 1, "Protect CUI at rest"),
    ("SI", "3.14.1", 5, "Identify, report and correct system flaws in time"),
    ("SI", "3.14.2", 5, "Malicious code protection at designated locations"),
    ("SI", "3.14.3", 5, "Monitor security alerts and advisories and act on them"),
    ("SI", "3.14.4", 5, "Update malicious code protection when new releases are available"),
    ("SI", "3.14.5", 3, "Periodic and real-time scans of files from external sources"),
    ("SI", "3.14.6", 5, "Monitor systems and traffic to detect attacks"),
    ("SI", "3.14.7", 3, "Identify unauthorized use of systems"),
]
PARTIAL_POINTS = {"3.5.3": 3, "3.13.11": 3}
NEVER_ON_POAM = {"3.1.20", "3.1.22", "3.12.4", "3.10.3", "3.10.4", "3.10.5"}
SSP = "3.12.4"
MAX_SCORE = 110
CONDITIONAL_MIN = 88  # 0.8 x 110, 32 CFR 170.21(a)(2)(i)
STATUSES = {"MET", "NOT_MET", "NA", "PARTIAL"}

BY_NUMBER = {num: (fam, num, pts, title) for fam, num, pts, title in REQUIREMENTS}

SAMPLE = """requirement_id,status,justification,evidence
""" + "".join(
    f"{fam}.L2-{num},{'MET'},,\n" for fam, num, _, _ in REQUIREMENTS
    if num not in {"3.1.20", "3.3.4", "3.5.3", "3.13.11", "3.10.6", "3.13.14", "3.4.9"}
) + """AC.L2-3.1.20,MET,,
AU.L2-3.3.4,NOT_MET,,SIEM alerting on log pipeline failure not configured
IA.L2-3.5.3,PARTIAL,,MFA on VPN and admin accounts only; not on general network logons
SC.L2-3.13.11,PARTIAL,,BitLocker in non-FIPS mode on engineering laptops
PE.L2-3.10.6,NA,No alternate work sites: remote work prohibited for CUI by policy SEC-04,
SC.L2-3.13.14,NA,,
CM.L2-3.4.9,NOT_MET,,No control over user-installed software on CAD workstations
"""


def ident(fam, num):
    return f"{fam}.L2-{num}"


def normalize_id(raw):
    raw = (raw or "").strip()
    num = raw.split("-", 1)[1] if "-" in raw else raw
    num = num.strip()
    return num if num in BY_NUMBER else None


def deduction(num, status):
    pts = BY_NUMBER[num][2]
    if status in ("MET", "NA"):
        return 0
    if status == "PARTIAL":
        return PARTIAL_POINTS[num]
    return pts


def poam_eligible(num, status, ded):
    if num in NEVER_ON_POAM:
        return False, "never permitted on a POA&M (32 CFR 170.21(a)(2)(iii))"
    if num == "3.13.11" and status == "PARTIAL":
        return True, "encryption used but not FIPS-validated: the one 3-point exception (170.21(a)(2)(ii))"
    if ded <= 1:
        return True, "1-point requirement"
    return False, f"worth {ded} points: only 1-point requirements may be deferred (170.21(a)(2)(ii))"


def parse(text):
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames or "requirement_id" not in reader.fieldnames or "status" not in reader.fieldnames:
        raise ValueError("CSV needs columns requirement_id and status")
    rows, errors, seen = {}, [], {}
    for line, r in enumerate(reader, start=2):
        num = normalize_id(r.get("requirement_id"))
        status = (r.get("status") or "").strip().upper().replace(" ", "_").replace("NOTMET", "NOT_MET")
        if status == "N/A":
            status = "NA"
        if num is None:
            errors.append(f"line {line}: unknown requirement '{r.get('requirement_id')}' (not one of the 110 Level 2 requirements)")
            continue
        if num in seen:
            errors.append(f"line {line}: {ident(BY_NUMBER[num][0], num)} listed twice (first on line {seen[num]})")
            continue
        if status not in STATUSES:
            errors.append(f"line {line}: status '{r.get('status')}' must be MET, NOT_MET, NA or PARTIAL")
            continue
        if status == "PARTIAL" and num not in PARTIAL_POINTS:
            errors.append(f"line {line}: PARTIAL only exists for IA.L2-3.5.3 and SC.L2-3.13.11; "
                          f"{ident(BY_NUMBER[num][0], num)} is MET or NOT_MET")
            continue
        if status == "NA" and num == SSP:
            errors.append(f"line {line}: the System Security Plan (CA.L2-3.12.4) cannot be NA")
            continue
        seen[num] = line
        rows[num] = {"status": status, "justification": (r.get("justification") or "").strip(),
                     "evidence": (r.get("evidence") or "").strip()}
    missing = [ident(f, n) for f, n, _, _ in REQUIREMENTS if n not in rows and n not in seen]
    if missing and len(missing) < MAX_SCORE:
        errors.append(f"{len(missing)} requirement(s) missing; an unassessed requirement is not MET: "
                      + ", ".join(missing[:12]) + (" ..." if len(missing) > 12 else ""))
    return rows, errors


def score(rows):
    results, findings = [], []
    total = MAX_SCORE
    by_family = {}
    for fam, num, pts, title in REQUIREMENTS:
        r = rows[num]
        ded = deduction(num, r["status"])
        total -= ded
        fam_entry = by_family.setdefault(fam, {"requirements": 0, "not_met": 0, "deducted": 0})
        fam_entry["requirements"] += 1
        fam_entry["deducted"] += ded
        entry = {"id": ident(fam, num), "title": title, "status": r["status"],
                 "points": pts if num not in PARTIAL_POINTS else "3/5", "deduction": ded}
        if r["status"] in ("NOT_MET", "PARTIAL") or (num == SSP and r["status"] == "NOT_MET"):
            fam_entry["not_met"] += 1
            ok, why = poam_eligible(num, r["status"], ded)
            entry["poam_eligible"] = ok
            entry["poam_reason"] = why
            if r["evidence"]:
                entry["note"] = r["evidence"]
        if r["status"] == "NA" and not r["justification"]:
            findings.append({"severity": "HIGH", "code": "NA_WITHOUT_JUSTIFICATION", "id": entry["id"],
                             "detail": "NA counts as MET only if the assessor accepts the reason; write it in the SSP"})
        results.append(entry)
    return total, results, by_family, findings


def verdict(total, results):
    gaps = [r for r in results if r["status"] in ("NOT_MET", "PARTIAL")]
    ssp_missing = any(r["id"].endswith(SSP) and r["status"] == "NOT_MET" for r in results)
    blocking = [g for g in gaps if not g["poam_eligible"]]
    if ssp_missing:
        return "BLOCKED_NO_SSP", gaps, blocking
    if not gaps:
        return "FINAL_ELIGIBLE", gaps, blocking
    if total >= CONDITIONAL_MIN and not blocking:
        return "CONDITIONAL_ELIGIBLE", gaps, blocking
    return "NOT_ELIGIBLE", gaps, blocking


def build(text):
    rows, errors = parse(text)
    if errors:
        return None, errors
    total, results, by_family, findings = score(rows)
    v, gaps, blocking = verdict(total, results)
    # Fixing a blocking gap restores its deduction; the score after fixing all of them
    # is the best score reachable with only POA&M-eligible gaps left open.
    after_blockers = total + sum(g["deduction"] for g in blocking)
    out = {
        "verdict": v,
        "score": total,
        "max_score": MAX_SCORE,
        "conditional_minimum": CONDITIONAL_MIN,
        "counts": {s: sum(1 for r in results if r["status"] == s) for s in ("MET", "NOT_MET", "PARTIAL", "NA")},
        "fix_before_assessment": sorted(
            [{"id": g["id"], "title": g["title"], "deduction": g["deduction"], "reason": g["poam_reason"]} for g in blocking],
            key=lambda g: -g["deduction"]),
        "poam_candidates": [{"id": g["id"], "title": g["title"], "deduction": g["deduction"]}
                            for g in gaps if g["poam_eligible"]],
        "score_after_fixing_blockers": after_blockers,
        "points_short_of_conditional": max(0, CONDITIONAL_MIN - after_blockers),
        "families": by_family,
        "findings": findings,
        "requirements": results,
    }
    return out, []


def render(out):
    lines = [f"CMMC Level 2 score: {out['score']} / {out['max_score']}   verdict: {out['verdict']}",
             "  MET {MET} · NOT_MET {NOT_MET} · PARTIAL {PARTIAL} · NA {NA}".format(**out["counts"])]
    if out["verdict"] == "BLOCKED_NO_SSP":
        lines.append("  No current System Security Plan (CA.L2-3.12.4): the assessment cannot be completed (32 CFR 170.24(c)(2)(ii)).")
    if out["fix_before_assessment"]:
        lines.append("\nFix before any assessment (cannot be deferred to a POA&M):")
        for g in out["fix_before_assessment"]:
            lines.append(f"  -{g['deduction']:<2} {g['id']:<14} {g['title']}  [{g['reason']}]")
    if out["poam_candidates"]:
        lines.append("\nMay go on a POA&M (closeout within 180 days of the Conditional status date):")
        for g in out["poam_candidates"]:
            lines.append(f"  -{g['deduction']:<2} {g['id']:<14} {g['title']}")
    if out["verdict"] == "NOT_ELIGIBLE":
        lines.append(f"\nAfter fixing every blocker the score would be {out['score_after_fixing_blockers']}"
                     + (f", still {out['points_short_of_conditional']} short of {out['conditional_minimum']}."
                        if out["points_short_of_conditional"] else f", enough for Conditional status."))
    for f in out["findings"]:
        lines.append(f"\n[{f['severity']}] {f['code']} {f['id']}: {f['detail']}")
    lines.append("\nNot an assessment. An assessor decides MET; the Affirming Official affirms in SPRS.")
    return "\n".join(lines)


EXIT = {"FINAL_ELIGIBLE": 0, "CONDITIONAL_ELIGIBLE": 2, "NOT_ELIGIBLE": 4, "BLOCKED_NO_SSP": 4}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog="Exit codes: 0 final-eligible, 2 conditional-eligible, 3 invalid input, 4 not eligible or blocked.")
    p.add_argument("--assessment", help="CSV of all 110 requirements with status")
    p.add_argument("--sample", action="store_true", help="run on a built-in example")
    p.add_argument("--output", choices=["text", "json"], default="text")
    p.add_argument("--json", action="store_true", help="shorthand for --output json")
    a = p.parse_args(argv)
    if a.json:
        a.output = "json"
    if a.sample:
        text = SAMPLE
    elif a.assessment:
        try:
            with open(a.assessment, newline="", encoding="utf-8-sig") as fh:
                text = fh.read()
        except OSError as e:
            print(f"error: {e}", file=sys.stderr)
            return 3
    else:
        p.print_usage(sys.stderr)
        print("error: give --assessment FILE or --sample", file=sys.stderr)
        return 3
    try:
        out, errors = build(text)
    except ValueError as e:
        errors, out = [str(e)], None
    if errors:
        if a.output == "json":
            print(json.dumps({"verdict": "INVALID_INPUT", "errors": errors}, indent=2))
        else:
            print("Invalid input:\n  " + "\n  ".join(errors), file=sys.stderr)
        return 3
    print(json.dumps(out, indent=2) if a.output == "json" else render(out))
    return EXIT[out["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
