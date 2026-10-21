#!/usr/bin/env python3
"""Find eval cases whose outcome changes between identical trials.

An agent eval run once per case cannot tell a regression from a coin flip.
Run every case k times, then this script says which cases are stable and
which are flaky, and reports two numbers that answer different questions:

  pass@k  = 1 - C(n-c, k) / C(n, k)   "did it succeed at least once in k tries?"
                                      (unbiased estimator, Chen et al. 2021)
  pass^k  = C(c, k) / C(n, k)         "did it succeed on all k tries?"
                                      (tau-bench, Yao et al. 2024)

where n = trials run for the case and c = trials passed. pass@k is the number
a demo wants; pass^k is the number a user experiences, because a user meets
every trial, not the best one. A wide gap between them is the flakiness.

Classification per case (needs at least --min-trials trials):
  STABLE_PASS   c == n
  STABLE_FAIL   c == 0
  FLAKY         0 < c < n

A flaky case is not automatically noise. In an agent, run-to-run variance is
often the defect itself. Cases marked critical are never offered for
quarantine; every quarantine stub this script writes has an empty owner and
expiry that the regression gate refuses until a human fills them in.

Trial order is checked too: if every failure falls in the later half of the
trial numbers (and there are at least 3), the trials are probably not
independent - shared state, a warming cache, rate limits or session leakage -
and every pass rate and test in the suite is optimistic until that is fixed.
This is a heuristic warning; it does not change the verdict.

Results file: JSONL, one trial per line:
  {"case_id": "...", "trial": 1, "passed": true, "critical": false}

Deterministic, stdlib only, no network, no LLM calls.

Exit codes:
    0  no flaky cases
    2  flaky cases found (listed, with pass@k and pass^k)
    3  invalid input
    4  refused: some cases have fewer than --min-trials trials
"""

import argparse
import json
import math
import sys
from collections import defaultdict

SAMPLE_RESULTS = (
    [{"case_id": "refund-lookup", "trial": t, "passed": True, "critical": True} for t in range(1, 6)]
    + [{"case_id": "faq-shipping", "trial": t, "passed": t != 3} for t in range(1, 6)]
    + [{"case_id": "cancel-subscription", "trial": t, "passed": t in (1, 4), "critical": True} for t in range(1, 6)]
    + [{"case_id": "address-change", "trial": t, "passed": False} for t in range(1, 6)]
)


def _fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(3)


def load_jsonl(path):
    rows = []
    try:
        with open(path, encoding="utf-8") as fh:
            for n, line in enumerate(fh, 1):
                if line.strip():
                    try:
                        rows.append(json.loads(line))
                    except json.JSONDecodeError as exc:
                        _fail(f"{path}:{n}: not valid JSON ({exc.msg})")
    except OSError as exc:
        _fail(f"cannot read {path}: {exc.strerror}")
    return rows


def pass_at_k(n, c, k):
    if k > n:
        return None
    if n - c < k:
        return 1.0
    return 1.0 - math.comb(n - c, k) / math.comb(n, k)


def pass_hat_k(n, c, k):
    if k > n:
        return None
    return math.comb(c, k) / math.comb(n, k)


def wilson(c, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = c / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def analyse(rows, k, min_trials):
    by_case = defaultdict(list)
    fails_by_trial = defaultdict(int)
    trial_numbers = set()
    critical = set()
    for row in rows:
        cid = row.get("case_id")
        if cid is None or not isinstance(row.get("passed"), bool):
            _fail(f"every row needs case_id and boolean passed (got {row})")
        by_case[cid].append(row["passed"])
        if isinstance(row.get("trial"), int):
            trial_numbers.add(row["trial"])
            if not row["passed"]:
                fails_by_trial[row["trial"]] += 1
        if row.get("critical"):
            critical.add(cid)
    if not by_case:
        _fail("no trials in results")

    cases = []
    for cid in sorted(by_case):
        outcomes = by_case[cid]
        n, c = len(outcomes), sum(outcomes)
        if n < min_trials:
            cls = "INSUFFICIENT_TRIALS"
        elif c == n:
            cls = "STABLE_PASS"
        elif c == 0:
            cls = "STABLE_FAIL"
        else:
            cls = "FLAKY"
        lo, hi = wilson(c, n)
        cases.append({
            "case_id": cid, "trials": n, "passed": c, "class": cls,
            "critical": cid in critical,
            "pass_rate": round(c / n, 3),
            "wilson_95": [round(lo, 3), round(hi, 3)],
            f"pass@{k}": None if pass_at_k(n, c, k) is None else round(pass_at_k(n, c, k), 3),
            f"pass^{k}": None if pass_hat_k(n, c, k) is None else round(pass_hat_k(n, c, k), 3),
        })

    classified = [c for c in cases if c["class"] != "INSUFFICIENT_TRIALS"]
    flaky = [c for c in classified if c["class"] == "FLAKY"]
    pk = [c[f"pass@{k}"] for c in classified if c[f"pass@{k}"] is not None]
    phk = [c[f"pass^{k}"] for c in classified if c[f"pass^{k}"] is not None]
    summary = {
        "cases": len(cases),
        "classified": len(classified),
        "stable_pass": sum(c["class"] == "STABLE_PASS" for c in cases),
        "stable_fail": sum(c["class"] == "STABLE_FAIL" for c in cases),
        "flaky": len(flaky),
        "insufficient": len(cases) - len(classified),
        "flake_rate": round(len(flaky) / len(classified), 3) if classified else None,
        f"mean_pass@{k}": round(sum(pk) / len(pk), 3) if pk else None,
        f"mean_pass^{k}": round(sum(phk) / len(phk), 3) if phk else None,
    }
    quarantine = [{
        "case_id": c["case_id"], "owner": "", "expires": "", "reason": "",
        "observed_pass_rate": c["pass_rate"],
    } for c in flaky if not c["critical"]]
    must_fix = [c["case_id"] for c in flaky if c["critical"]]

    if summary["insufficient"]:
        verdict, code = "REFUSED_INSUFFICIENT_TRIALS", 4
    elif flaky:
        verdict, code = "FLAKY_CASES", 2
    else:
        verdict, code = "STABLE", 0
    order_warning = None
    ordered = sorted(trial_numbers)
    if len(ordered) >= 3:
        early = ordered[:len(ordered) // 2]
        total = sum(fails_by_trial.values())
        if total >= 3 and not any(fails_by_trial[t] for t in early):
            order_warning = (f"all {total} failures are in trials {ordered[len(early)]}-{ordered[-1]}; "
                             "trials 1-{} never fail. Check for shared state between trials before trusting any rate."
                             .format(early[-1]))
    return {"verdict": verdict, "k": k, "min_trials": min_trials, "summary": summary,
            "failures_by_trial": {str(t): fails_by_trial[t] for t in ordered}, "trial_order_warning": order_warning,
            "critical_flaky_must_fix": must_fix, "quarantine_candidates": quarantine,
            "cases": cases}, code


def render(r):
    s, k = r["summary"], r["k"]
    out = [f"Flake detection: {r['verdict']}  (k={k}, min trials={r['min_trials']})",
           f"  cases {s['cases']}: stable-pass {s['stable_pass']}, stable-fail {s['stable_fail']}, "
           f"flaky {s['flaky']}, insufficient {s['insufficient']}"]
    if s["flake_rate"] is not None:
        out.append(f"  flake rate {s['flake_rate']:.1%}   mean pass@{k} {s[f'mean_pass@{k}']}   mean pass^{k} {s[f'mean_pass^{k}']}")
    for c in r["cases"]:
        if c["class"] in ("FLAKY", "INSUFFICIENT_TRIALS"):
            tag = " [critical]" if c["critical"] else ""
            out.append(f"  - {c['case_id']}{tag}: {c['class']} {c['passed']}/{c['trials']} "
                       f"(95% CI {c['wilson_95'][0]:.2f}-{c['wilson_95'][1]:.2f}) pass^{k}={c[f'pass^{k}']}")
    if r["critical_flaky_must_fix"]:
        out.append("  Critical and flaky (fix, never quarantine): " + ", ".join(r["critical_flaky_must_fix"]))
    if r["quarantine_candidates"]:
        out.append("  Quarantine candidates need an owner, an expiry and a reason before the gate accepts them.")
    if r["trial_order_warning"]:
        out.append("  Trial-order warning: " + r["trial_order_warning"])
    if r["verdict"] == "REFUSED_INSUFFICIENT_TRIALS":
        out.append(f"  Refused: stability cannot be judged from fewer than {r['min_trials']} trials. Re-run those cases.")
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description="Classify eval cases as stable or flaky from repeated trials; report pass@k and pass^k.")
    p.add_argument("--results", help="JSONL of trials: {case_id, trial, passed, critical?}")
    p.add_argument("--k", type=int, default=3, help="k for pass@k and pass^k (default 3)")
    p.add_argument("--min-trials", type=int, default=3, help="refuse to classify cases with fewer trials (default 3)")
    p.add_argument("--quarantine-out", help="write quarantine stubs (owner/expiry left blank) to this JSON file")
    p.add_argument("--sample", action="store_true", help="run on embedded sample results")
    p.add_argument("--output", choices=["text", "json"], default="text")
    a = p.parse_args()
    if a.k < 1 or a.min_trials < 2:
        p.error("--k must be >= 1 and --min-trials >= 2")
    if a.sample:
        rows = SAMPLE_RESULTS
    elif a.results:
        rows = load_jsonl(a.results)
    else:
        p.error("give --results or --sample")
    report, code = analyse(rows, a.k, a.min_trials)
    if a.quarantine_out:
        with open(a.quarantine_out, "w", encoding="utf-8") as fh:
            json.dump({"quarantine": report["quarantine_candidates"]}, fh, indent=2)
    print(json.dumps(report, indent=2) if a.output == "json" else render(report))
    return code


if __name__ == "__main__":
    sys.exit(main())
