#!/usr/bin/env python3
"""Check a medical device software trace matrix: system requirement -> software requirement -> test, and hazard -> risk control -> verification.

Notified bodies and FDA reviewers ask for the trace matrix first and read raw
test data second. This script finds the breaks before they do: software
requirements with no parent, requirements no test covers, failed or unrun
tests at release with no recorded anomaly, and software risk control measures
that trace to no hazard or have no passing verification.

CSV columns (header required; one row per software requirement)
  req_id            software requirement id
  system_req        parent system requirement id(s), ';'-separated
  is_risk_control   yes | no   the requirement implements a risk control measure (5.2.3)
  hazard_ids        hazard / hazardous situation id(s) from the risk file, ';'-separated
  tests             test case id(s), ';'-separated
  results           result per test in the same order: pass | fail | not_run
  anomaly_ids       problem report / anomaly id(s) recorded for a fail or not_run, ';'-separated

Findings (IEC 62304:2006+A1:2015 references; class-dependent ones need --class)
  RC_NO_HAZARD       risk control with no hazard id (7.3.3, class B/C)              BLOCKER
  RC_UNVERIFIED      risk control without a passing test (7.3.1, class B/C)          BLOCKER
  UNTESTED           requirement with no test (5.7.1)            BLOCKER with --release, else HIGH
  OPEN_RESULT        fail or not_run with no anomaly id (5.8.1, 5.8.2)  BLOCKER with --release, else HIGH
  RESIDUAL_ANOMALY   fail or not_run with an anomaly id: evaluate it (5.8.2; 5.8.3 for B/C)  HIGH
  NO_SYSTEM_TRACE    software requirement with no parent system requirement (5.2.1) HIGH
  RESULT_MISMATCH    number of results differs from number of tests                 invalid input

Deterministic, stdlib only, no network. A link in the matrix is not proof the
test verifies the requirement; reviewers still read the test.

Exit codes:
    0  TRACED
    2  FINDINGS
    3  invalid input
    4  BLOCKED
"""

import argparse
import csv
import io
import json
import sys

COLUMNS = ["req_id", "system_req", "is_risk_control", "hazard_ids", "tests", "results", "anomaly_ids"]
RESULTS = {"pass", "fail", "not_run"}
SEV = {"BLOCKER": 4, "HIGH": 2}

SAMPLE = """req_id,system_req,is_risk_control,hazard_ids,tests,results,anomaly_ids
SWR-001,SYS-010,no,,TC-001;TC-002,pass;pass,
SWR-002,SYS-011,yes,HAZ-03,TC-003,pass,
SWR-003,SYS-011,yes,,TC-004,fail,
SWR-004,,no,,TC-005,pass,
SWR-005,SYS-012,no,,,,
SWR-006,SYS-013,no,,TC-006,fail,PR-117
SWR-007,SYS-014,yes,HAZ-07,TC-007,not_run,
"""


def split(v):
    return [x.strip() for x in (v or "").split(";") if x.strip()]


def run(text, cls, release):
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise ValueError("no rows")
    missing = [c for c in COLUMNS if c not in rows[0]]
    if missing:
        raise ValueError(f"missing columns: {', '.join(missing)}")
    bc = cls in ("B", "C")
    findings, seen = [], set()
    stats = {"requirements": 0, "risk_controls": 0, "tested": 0, "all_pass": 0}
    gate = "BLOCKER" if release else "HIGH"
    for n, r in enumerate(rows, 2):
        rid = (r["req_id"] or "").strip()
        if not rid:
            raise ValueError(f"line {n}: empty req_id")
        if rid in seen:
            raise ValueError(f"line {n}: duplicate req_id {rid}")
        seen.add(rid)
        tests, results = split(r["tests"]), [x.lower() for x in split(r["results"])]
        if len(tests) != len(results):
            raise ValueError(f"{rid}: {len(tests)} tests but {len(results)} results (RESULT_MISMATCH)")
        bad = [x for x in results if x not in RESULTS]
        if bad:
            raise ValueError(f"{rid}: results must be pass, fail or not_run, got {bad}")
        rc = (r["is_risk_control"] or "").strip().lower() in ("yes", "y", "true")
        anomalies = split(r["anomaly_ids"])
        stats["requirements"] += 1
        stats["risk_controls"] += rc
        if not split(r["system_req"]):
            findings.append(("HIGH", "NO_SYSTEM_TRACE", rid, "no parent system requirement (5.2.1)"))
        if not tests:
            findings.append((gate, "UNTESTED", rid, "no test covers this requirement (5.7.1)"))
        else:
            stats["tested"] += 1
            if all(x == "pass" for x in results):
                stats["all_pass"] += 1
        open_ = [t for t, x in zip(tests, results) if x != "pass"]
        if open_:
            if anomalies:
                findings.append(("HIGH", "RESIDUAL_ANOMALY", rid,
                                 f"{', '.join(open_)} not passing; anomaly {', '.join(anomalies)} must be documented"
                                 + (" and evaluated for safety (5.8.2, 5.8.3)" if bc else " (5.8.2)")))
            else:
                findings.append((gate, "OPEN_RESULT", rid,
                                 f"{', '.join(open_)} failed or not run and no anomaly recorded (5.8.1, 5.8.2)"))
        if rc and bc:
            if not split(r["hazard_ids"]):
                findings.append(("BLOCKER", "RC_NO_HAZARD", rid, "risk control measure traces to no hazard (7.3.3)"))
            if "pass" not in results:
                findings.append(("BLOCKER", "RC_UNVERIFIED", rid, "risk control measure has no passing verification (7.3.1)"))
    worst = max([SEV[f[0]] for f in findings] or [0])
    verdict = {4: "BLOCKED", 2: "FINDINGS", 0: "TRACED"}[worst]
    order = {"BLOCKER": 0, "HIGH": 1}
    findings.sort(key=lambda f: (order[f[0]], f[2]))
    req = stats["requirements"]
    stats["test_coverage_pct"] = round(100 * stats["tested"] / req, 1) if req else 0.0
    return {"verdict": verdict, "software_safety_class": cls, "release_gate": release, "stats": stats,
            "findings": [{"severity": s, "code": c, "id": i, "detail": d} for s, c, i, d in findings],
            "note": "A trace link is not proof of verification; reviewers read the test and its raw data."
                    + ("" if cls else " Pass --class to apply the class B/C risk-control checks.")}


def render(out):
    s = out["stats"]
    lines = [f"Trace matrix check: {out['verdict']}"
             + (f" (class {out['software_safety_class']})" if out["software_safety_class"] else "")
             + (" [release gate]" if out["release_gate"] else ""),
             f"{s['requirements']} requirements, {s['risk_controls']} risk controls, "
             f"{s['test_coverage_pct']}% with a test, {s['all_pass']} fully passing", ""]
    for f in out["findings"]:
        lines.append(f"[{f['severity']}] {f['code']} {f['id']}: {f['detail']}")
    lines += ["", out["note"]]
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                epilog="Exit codes: 0 traced, 2 findings, 3 invalid input, 4 blocked.")
    p.add_argument("--matrix", help="trace matrix CSV (columns in module docstring)")
    p.add_argument("--class", dest="cls", choices=["A", "B", "C"], help="IEC 62304 software safety class")
    p.add_argument("--release", action="store_true", help="release gate: untested requirements and open results block")
    p.add_argument("--template", action="store_true", help="print the CSV header and exit")
    p.add_argument("--sample", action="store_true", help="run on a built-in class C matrix with --release")
    p.add_argument("--output", choices=["text", "json"], default="text")
    p.add_argument("--json", action="store_true", help="shorthand for --output json")
    a = p.parse_args(argv)
    if a.json:
        a.output = "json"
    if a.template:
        print(",".join(COLUMNS))
        return 0
    try:
        if a.sample:
            text, a.cls, a.release = SAMPLE, "C", True
        else:
            if not a.matrix:
                p.print_usage(sys.stderr)
                print("error: give --matrix, --template or --sample", file=sys.stderr)
                return 3
            with open(a.matrix, newline="", encoding="utf-8-sig") as fh:
                text = fh.read()
        out = run(text, a.cls, a.release)
    except (OSError, ValueError, csv.Error) as e:
        if a.output == "json":
            print(json.dumps({"verdict": "INVALID_INPUT", "errors": [str(e)]}, indent=2))
        else:
            print(f"error: {e}", file=sys.stderr)
        return 3
    print(json.dumps(out, indent=2) if a.output == "json" else render(out))
    return {"BLOCKED": 4, "FINDINGS": 2, "TRACED": 0}[out["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
