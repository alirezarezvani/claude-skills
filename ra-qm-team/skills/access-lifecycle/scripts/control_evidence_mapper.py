#!/usr/bin/env python3
"""Turn access_diff.py and access_review_campaign.py results into a per-control view.

An auditor does not ask "how many findings did the script produce". They ask,
control by control, what was tested, what exceptions were found, and what
evidence is kept. This script reads the --output json of the two sibling tools
and answers that for the frameworks you name.

Status per control
  FAIL                at least one BLOCKER finding maps to it
  EXCEPTIONS          findings map to it, none of them blockers
  NO_EXCEPTIONS       every input that tests it was supplied and found nothing
  PARTLY_TESTED       no exceptions, but one of the inputs that tests it was not supplied
  NOT_TESTED          none of the inputs that test it was supplied
  NOT_COVERED         these tools do not test it at all (named so nobody assumes they do)

There is no PASS. A script finding nothing is not an operating-effectiveness
conclusion; that is the auditor's call, made on the evidence listed here.

Control titles and wording are paraphrased from the public texts (AICPA TSC 2017
rev. 2022 points of focus, NIST SP 800-53 Rev 5, PCI DSS v4.0.1, 45 CFR 164.308,
PCAOB AS 1105). ISO/IEC 27001:2022 Annex A titles only: check the requirement
text against your licensed copy.

Deterministic, stdlib only, no network.

Exit codes:
    0  no exceptions in any tested control
    2  exceptions, no failures
    3  invalid input
    4  at least one control FAIL
"""

import argparse
import json
import os
import sys

FRAMEWORKS = {"iso27001": "ISO27001", "soc2": "SOC2", "nist80053": "NIST", "pci": "PCI",
              "hipaa": "HIPAA", "sox": "PCAOB"}

# control id -> (title, inputs that test it, what an auditor tests, evidence to keep)
CATALOGUE = {
    "ISO27001:A.5.15": ("Access control", [],
                        "An approved access control policy exists and is applied.",
                        "The policy, its approval record and review date."),
    "ISO27001:A.5.16": ("Identity management", ["diff"],
                        "Every identity maps to a person or an owned non-human use; the full lifecycle is managed.",
                        "Roster and account exports with pull dates, the access_diff report, orphan remediation tickets."),
    "ISO27001:A.5.18": ("Access rights", ["diff", "campaign"],
                        "Access is provisioned, reviewed at planned intervals and removed or adjusted on change or exit.",
                        "Campaign decisions with reviewer and timestamp, removal tickets, re-export showing removal."),
    "ISO27001:A.6.5": ("Responsibilities after termination or change of employment", ["diff"],
                       "Leavers and movers lose the access their old role needed.",
                       "HR termination list, account export after the exit date, disable timestamps."),
    "ISO27001:A.8.2": ("Privileged access rights", ["diff", "campaign"],
                       "Privileged access is restricted, owned and reviewed more often than standard access.",
                       "Privileged account list, last-review dates, campaign decisions for privileged lines."),
    "ISO27001:A.5.3": ("Segregation of duties", ["campaign"],
                       "Conflicting duties, including approving your own access, are separated.",
                       "Reviewer assignment rules and the campaign file showing no self-review."),
    "SOC2:CC6.1": ("Logical access security software, infrastructure and architectures", [],
                   "Access security architecture: authentication, network segmentation, encryption of credentials.",
                   "System configuration evidence; out of scope for these tools."),
    "SOC2:CC6.2": ("Registration, authorization and removal of users", ["diff", "campaign"],
                   "Users are authorized before access is issued, and credentials are removed when access is no longer authorized.",
                   "Joiner approvals (not tested here), leaver disable evidence, the access_diff report."),
    "SOC2:CC6.3": ("Authorize, modify or remove access based on roles, least privilege, SoD", ["diff", "campaign"],
                   "Access changes follow role changes, and periodic review removes what is no longer needed.",
                   "Mover tickets, campaign decisions, removal evidence."),
    "NIST:AC-2": ("Account management", ["diff", "campaign"],
                  "Accounts are authorized, monitored, reviewed at the defined frequency and removed when no longer needed (AC-2 a-j).",
                  "Account inventory, review records at the ODP frequency, disable records."),
    "NIST:AC-2(3)": ("Disable accounts", ["diff"],
                     "Expired, unassociated, policy-violating and inactive accounts are disabled within the defined period.",
                     "Inactivity report against the ODP period, disable timestamps."),
    "NIST:AC-5": ("Separation of duties", ["campaign"],
                  "Duties are separated, including review of one's own access.",
                  "Reviewer assignment and the campaign file."),
    "PCI:7.2.4": ("Review of all user accounts and access privileges", ["diff", "campaign"],
                  "All accounts, including third-party, reviewed at least every six months; inappropriate access addressed; management acknowledges.",
                  "Campaign file, management acknowledgement, removal evidence."),
    "PCI:7.2.5.1": ("Review of application and system account access", ["diff"],
                    "System and application accounts reviewed at the frequency set by the targeted risk analysis (12.3.1).",
                    "Service account inventory with owners, the targeted risk analysis, review records."),
    "PCI:8.2.5": ("Access for terminated users is immediately revoked", ["diff"],
                  "Terminated users have no active access.",
                  "Termination list, account export, disable timestamps."),
    "PCI:8.2.6": ("Inactive accounts removed or disabled within 90 days", ["diff"],
                  "No user account is inactive for more than 90 days and still enabled.",
                  "Last-login export and the access_diff inactive findings."),
    "HIPAA:164.308(a)(3)(ii)(C)": ("Termination procedures (addressable)", ["diff"],
                                    "ePHI access ends when employment ends, or a documented equivalent is in place.",
                                    "Termination procedure, disable evidence for ePHI systems, decision record if addressed differently."),
    "PCAOB:AS1105.10": ("Information produced by the entity", ["campaign"],
                        "The report the review was run on is complete and accurate, or the controls over producing it were tested.",
                        "The export query or parameters, pull timestamp, the population check in this report."),
}
SEVERITY_RANK = {"BLOCKER": 0, "HIGH": 1, "MEDIUM": 2}


def _fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(3)


def _load(path, label):
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        _fail(f"{label}: {exc}")
    if not isinstance(data, dict) or not isinstance(data.get("findings"), list):
        _fail(f"{label}: not a --output json report (no findings list)")
    return data


def map_controls(frameworks, diff=None, campaign=None):
    supplied = {k for k, v in (("diff", diff), ("campaign", campaign)) if v is not None}
    if not supplied:
        _fail("give at least one of --diff or --campaign")
    prefixes = {FRAMEWORKS[f] for f in frameworks}
    hits = {}
    for source, report in (("diff", diff), ("campaign", campaign)):
        for f in (report or {}).get("findings", []):
            for cid in f.get("controls", []):
                hits.setdefault(cid, []).append({"source": source, "code": f.get("code"), "severity": f.get("severity"),
                                                 "system": f.get("system"), "account_id": f.get("account_id")})
    controls = []
    for cid, (title, tested_by, tests, evidence) in CATALOGUE.items():
        if cid.split(":")[0] not in prefixes:
            continue
        found = sorted(hits.get(cid, []), key=lambda h: (SEVERITY_RANK.get(h["severity"], 9), h["code"] or ""))
        if not tested_by:
            status = "NOT_COVERED"
        elif not supplied & set(tested_by):
            status = "NOT_TESTED"
        elif any(h["severity"] == "BLOCKER" for h in found):
            status = "FAIL"
        elif found:
            status = "EXCEPTIONS"
        elif set(tested_by) <= supplied:
            status = "NO_EXCEPTIONS"
        else:
            status = "PARTLY_TESTED"
        controls.append({"control": cid, "title": title, "status": status, "tested_by": tested_by,
                         "auditor_tests": tests, "evidence_to_keep": evidence,
                         "exceptions": len(found), "findings": found})
    order = ["FAIL", "EXCEPTIONS", "PARTLY_TESTED", "NO_EXCEPTIONS", "NOT_TESTED", "NOT_COVERED"]
    controls.sort(key=lambda c: (order.index(c["status"]), c["control"]))
    caveats = []
    for label, report in (("access_diff", diff), ("access_review_campaign", campaign)):
        if report is not None:
            caveats += [f"{label}: {n}" for n in report.get("not_checked", []) + report.get("notes", [])]
            caveats += [f"{label}: data quality: {q}" for q in report.get("data_quality", [])]
    summary = {s: sum(c["status"] == s for c in controls) for s in order}
    return {"frameworks": sorted(frameworks), "inputs": sorted(supplied), "summary": summary,
            "controls": controls, "caveats": caveats}


def render(result):
    s = result["summary"]
    out = [f"CONTROL EVIDENCE MAP  frameworks: {', '.join(result['frameworks'])}  inputs: {', '.join(result['inputs'])}",
           " · ".join(f"{k} {v}" for k, v in s.items() if v), ""]
    for c in result["controls"]:
        out.append(f"{c['status']:<14} {c['control']:<28} {c['title']}")
        if c["findings"]:
            codes = {}
            for h in c["findings"]:
                codes[(h["severity"], h["code"])] = codes.get((h["severity"], h["code"]), 0) + 1
            out.append("               exceptions: " + ", ".join(f"{n}× {code} ({sev})" for (sev, code), n in codes.items()))
        if c["status"] != "NOT_COVERED":
            out.append(f"               auditor tests: {c['auditor_tests']}")
            out.append(f"               keep: {c['evidence_to_keep']}")
    for cav in result["caveats"]:
        out.append(f"CAVEAT  {cav}")
    out.append("")
    out.append("No status here is an audit opinion. ISO/IEC 27001 Annex A titles only; verify against your licensed copy.")
    return "\n".join(out)


def _sample():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import datetime as dt
    import access_diff
    import access_review_campaign as arc
    d = access_diff.analyse(access_diff.SAMPLE_ROSTER, access_diff.SAMPLE_ACCOUNTS,
                            dt.date.fromisoformat(access_diff.SAMPLE_ARGS["as_of"]),
                            access_diff.SAMPLE_ARGS["inactive_days"],
                            privileged_review_days=access_diff.SAMPLE_ARGS["privileged_review_days"])
    c = arc.analyse(arc.SAMPLE_DECISIONS, dt.date.fromisoformat(arc.SAMPLE_ARGS["as_of"]),
                    arc.SAMPLE_ARGS["remediation_days"], dt.date.fromisoformat(arc.SAMPLE_ARGS["close_date"]),
                    arc.SAMPLE_POPULATION)
    return d, c


def main():
    p = argparse.ArgumentParser(description="Map access_diff / access_review_campaign JSON findings to per-control status and evidence.")
    p.add_argument("--diff", help="access_diff.py --output json file")
    p.add_argument("--campaign", help="access_review_campaign.py --output json file")
    p.add_argument("--framework", default="iso27001,soc2",
                   help=f"comma list from {','.join(FRAMEWORKS)} (default iso27001,soc2)")
    p.add_argument("--sample", action="store_true", help="run both sibling tools on their samples and map the result")
    p.add_argument("--output", choices=["text", "json"], default="text")
    a = p.parse_args()
    frameworks = [f.strip().lower() for f in a.framework.split(",") if f.strip()]
    unknown = [f for f in frameworks if f not in FRAMEWORKS]
    if unknown or not frameworks:
        _fail(f"unknown framework(s) {', '.join(unknown) or '(none)'}; choose from {', '.join(FRAMEWORKS)}")
    if a.sample:
        diff, campaign = _sample()
    else:
        diff = _load(a.diff, "--diff") if a.diff else None
        campaign = _load(a.campaign, "--campaign") if a.campaign else None
    result = map_controls(frameworks, diff, campaign)
    print(json.dumps(result, indent=2) if a.output == "json" else render(result))
    s = result["summary"]
    return 4 if s["FAIL"] else 2 if s["EXCEPTIONS"] else 0


if __name__ == "__main__":
    sys.exit(main())
