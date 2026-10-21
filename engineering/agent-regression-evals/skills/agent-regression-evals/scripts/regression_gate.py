#!/usr/bin/env python3
"""Block a merge when the candidate agent is measurably worse than baseline.

"The pass rate went from 82% to 79%" is not a finding until you know whether
three points is outside the noise. This gate compares a candidate run to a
baseline run on the SAME cases and answers with statistics, not vibes:

  * per-case pass rates (mean over repeated trials), so a case run 5 times
    counts as one observation, not five (trials within a case are correlated;
    treating them as independent overstates confidence)
  * paired differences d_i = candidate_i - baseline_i, with a t-based 95% CI
    on the mean difference (pairing removes case difficulty from the noise)
  * an exact one-sided McNemar test on the cases whose majority outcome flipped
  * the sample size you would need to detect the observed drop, when the run
    is too small to tell

It BLOCKS on any of:
  - a statistically significant drop (upper end of the 95% CI below zero)
  - significantly more pass->fail than fail->pass flips (McNemar p < 0.05)
  - a critical case that passed every baseline trial and failed any candidate trial
  - cases present in the baseline but missing from the candidate (a dropped case
    is the cheapest way to "fix" a regression)
  - a quarantine entry with no owner, no expiry, or covering a critical case

It WARNS when the drop exceeds --tolerance but the run is underpowered, or when
mean cost per case rises more than --max-cost-increase.

Results files: JSONL, one trial per line:
  {"case_id": "...", "trial": 1, "passed": true, "critical": false, "cost_usd": 0.012}

Deterministic, stdlib only, no network, no LLM calls.

Exit codes:
    0  PASS (no regression detected)
    2  WARN (underpowered drop or cost increase; a human decides)
    3  invalid input
    4  BLOCK (merge must not proceed)
"""

import argparse
import datetime as dt
import json
import math
import sys
from collections import defaultdict

# Two-sided 95% t critical values by degrees of freedom; z beyond 30.
T95 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306,
       9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131,
       16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086, 21: 2.080, 22: 2.074,
       23: 2.069, 24: 2.064, 25: 2.060, 26: 2.056, 27: 2.052, 28: 2.048, 29: 2.045, 30: 2.042}


def _sample():
    base, cand = [], []
    outcomes = {  # case: (baseline passes of 5, candidate passes of 5, critical)
        "refund-lookup": (5, 5, True), "faq-shipping": (5, 4, False),
        "cancel-subscription": (5, 3, True), "address-change": (4, 4, False),
        "invoice-copy": (5, 5, False), "plan-upgrade": (4, 2, False),
        "password-reset": (5, 5, False), "order-status": (3, 3, False),
    }
    for cid, (bp, cp, crit) in outcomes.items():
        for t in range(1, 6):
            base.append({"case_id": cid, "trial": t, "passed": t <= bp, "critical": crit, "cost_usd": 0.010})
            cand.append({"case_id": cid, "trial": t, "passed": t <= cp, "critical": crit, "cost_usd": 0.013})
    return base, cand


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


def per_case(rows, label):
    acc = defaultdict(lambda: {"n": 0, "c": 0, "cost": 0.0, "cost_n": 0, "critical": False})
    for row in rows:
        cid = row.get("case_id")
        if cid is None or not isinstance(row.get("passed"), bool):
            _fail(f"{label}: every row needs case_id and boolean passed")
        a = acc[cid]
        a["n"] += 1
        a["c"] += row["passed"]
        a["critical"] = a["critical"] or bool(row.get("critical"))
        if isinstance(row.get("cost_usd"), (int, float)):
            a["cost"] += row["cost_usd"]
            a["cost_n"] += 1
    if not acc:
        _fail(f"{label}: no trials")
    return acc


def mcnemar_one_sided(b, c):
    """Exact one-sided McNemar: P(X >= b) for X ~ Binomial(b + c, 0.5).

    b = cases that flipped pass->fail, c = fail->pass. One-sided because the
    gate only asks "did it get worse?", not "did it change?".
    """
    n = b + c
    if n == 0:
        return 1.0
    return sum(math.comb(n, i) for i in range(b, n + 1)) / 2 ** n


def check_quarantine(entries, critical, today):
    valid, problems = set(), []
    for e in entries:
        cid = e.get("case_id", "?")
        if cid in critical:
            problems.append(f"{cid}: critical cases cannot be quarantined")
            continue
        if not str(e.get("owner", "")).strip() or not str(e.get("expires", "")).strip():
            problems.append(f"{cid}: quarantine needs an owner and an expiry date")
            continue
        try:
            expires = dt.date.fromisoformat(str(e["expires"]))
        except ValueError:
            problems.append(f"{cid}: expiry '{e['expires']}' is not YYYY-MM-DD")
            continue
        if expires < today:
            continue  # expired: the case re-enters the gate, which is the point of an expiry
        valid.add(cid)
    return valid, problems


def gate(base_rows, cand_rows, quarantine, tolerance, max_cost_increase, allow_missing, today):
    base, cand = per_case(base_rows, "baseline"), per_case(cand_rows, "candidate")
    critical = {c for c, v in base.items() if v["critical"]} | {c for c, v in cand.items() if v["critical"]}
    blocks, warns, notes = [], [], []

    missing = sorted(set(base) - set(cand))
    if missing and not allow_missing:
        blocks.append(f"{len(missing)} baseline case(s) missing from candidate: {', '.join(missing[:10])}")
    new_cases = sorted(set(cand) - set(base))
    if new_cases:
        notes.append(f"{len(new_cases)} new case(s) have no baseline and are not gated")

    quarantined, q_problems = check_quarantine(quarantine, critical, today)
    blocks.extend(f"invalid quarantine: {p}" for p in q_problems)

    gated = sorted((set(base) & set(cand)) - quarantined)
    if not gated:
        _fail("no overlapping, non-quarantined cases to compare")

    diffs, flips_bad, flips_good, critical_regressions, rows = [], 0, 0, [], []
    for cid in gated:
        b, c = base[cid], cand[cid]
        pb, pc = b["c"] / b["n"], c["c"] / c["n"]
        diffs.append(pc - pb)
        if pb >= 0.5 > pc:
            flips_bad += 1
        elif pc >= 0.5 > pb:
            flips_good += 1
        if cid in critical and pb == 1.0 and pc < 1.0:
            critical_regressions.append(f"{cid} ({b['c']}/{b['n']} -> {c['c']}/{c['n']})")
        rows.append({"case_id": cid, "baseline": round(pb, 3), "candidate": round(pc, 3),
                     "delta": round(pc - pb, 3), "critical": cid in critical})

    n = len(diffs)
    mean = sum(diffs) / n
    sd = math.sqrt(sum((d - mean) ** 2 for d in diffs) / (n - 1)) if n > 1 else 0.0
    se = sd / math.sqrt(n) if n else 0.0
    tcrit = T95.get(n - 1, 1.96) if n > 1 else float("inf")
    ci = (mean - tcrit * se, mean + tcrit * se) if n > 1 else (float("-inf"), float("inf"))
    mcnemar_p = mcnemar_one_sided(flips_bad, flips_good)

    if critical_regressions:
        blocks.append("critical case regressed: " + "; ".join(critical_regressions))
    if mcnemar_p < 0.05 and flips_bad > flips_good:
        blocks.append(f"significant flips: {flips_bad} cases pass->fail vs {flips_good} fail->pass (McNemar one-sided p={mcnemar_p:.3f})")
    if ci[1] < 0:
        blocks.append(f"significant drop: mean per-case delta {mean:+.3f}, 95% CI [{ci[0]:+.3f}, {ci[1]:+.3f}]")
    elif mean <= -tolerance:
        needed = math.ceil(((1.96 + 0.84) * sd / abs(mean)) ** 2) if sd > 0 else n
        warns.append(f"drop of {mean:+.3f} exceeds tolerance {tolerance} but CI [{ci[0]:+.3f}, {ci[1]:+.3f}] "
                     f"includes 0; about {needed} cases needed to detect it at 80% power")
    if ci[0] > 0:
        notes.append(f"significant improvement: mean delta {mean:+.3f}")
    if n < 10:
        notes.append(f"only {n} gated cases; small samples detect only large regressions")

    bc = [base[c]["cost"] / base[c]["cost_n"] for c in gated if base[c]["cost_n"]]
    cc = [cand[c]["cost"] / cand[c]["cost_n"] for c in gated if cand[c]["cost_n"]]
    cost = None
    if bc and cc and sum(bc) > 0:
        change = (sum(cc) / len(cc)) / (sum(bc) / len(bc)) - 1
        cost = round(change, 3)
        if change > max_cost_increase:
            warns.append(f"mean cost per case up {change:.1%} (limit {max_cost_increase:.0%})")

    verdict, code = ("BLOCK", 4) if blocks else (("WARN", 2) if warns else ("PASS", 0))
    return {
        "verdict": verdict, "gated_cases": n, "quarantined": sorted(quarantined),
        "mean_delta": round(mean, 4), "ci95": [round(ci[0], 4), round(ci[1], 4)] if n > 1 else None,
        "mcnemar": {"pass_to_fail": flips_bad, "fail_to_pass": flips_good, "p_value": round(mcnemar_p, 4)},
        "cost_change": cost, "blocks": blocks, "warnings": warns, "notes": notes,
        "cases": sorted(rows, key=lambda r: r["delta"]),
    }, code


def render(r):
    out = [f"Regression gate: {r['verdict']}",
           f"  gated cases {r['gated_cases']}, quarantined {len(r['quarantined'])}",
           f"  mean per-case delta {r['mean_delta']:+.3f}" + (f", 95% CI [{r['ci95'][0]:+.3f}, {r['ci95'][1]:+.3f}]" if r["ci95"] else ""),
           f"  McNemar: {r['mcnemar']['pass_to_fail']} pass->fail, {r['mcnemar']['fail_to_pass']} fail->pass, one-sided p={r['mcnemar']['p_value']}"]
    if r["cost_change"] is not None:
        out.append(f"  cost per case change {r['cost_change']:+.1%}")
    for label, items in (("BLOCK", r["blocks"]), ("WARN", r["warnings"]), ("note", r["notes"])):
        out.extend(f"  {label}: {i}" for i in items)
    worst = [c for c in r["cases"] if c["delta"] < 0][:5]
    if worst:
        out.append("  largest per-case drops:")
        out.extend(f"    {c['case_id']}{' [critical]' if c['critical'] else ''}: {c['baseline']:.2f} -> {c['candidate']:.2f}" for c in worst)
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description="Paired statistical regression gate for agent evals: candidate vs baseline.")
    p.add_argument("--baseline", help="baseline JSONL of trials")
    p.add_argument("--candidate", help="candidate JSONL of trials")
    p.add_argument("--quarantine", help='JSON {"quarantine": [{case_id, owner, expires, reason}]}')
    p.add_argument("--tolerance", type=float, default=0.02, help="mean drop that triggers a WARN when not significant (default 0.02)")
    p.add_argument("--max-cost-increase", type=float, default=0.20, help="WARN above this relative cost rise (default 0.20)")
    p.add_argument("--allow-missing", action="store_true", help="do not block on baseline cases missing from the candidate")
    p.add_argument("--today", help="override today's date (YYYY-MM-DD) for quarantine expiry checks")
    p.add_argument("--sample", action="store_true", help="run on embedded sample runs")
    p.add_argument("--output", choices=["text", "json"], default="text")
    a = p.parse_args()

    today = dt.date.today()
    if a.today:
        try:
            today = dt.date.fromisoformat(a.today)
        except ValueError:
            p.error("--today must be YYYY-MM-DD")
    quarantine = []
    if a.quarantine:
        try:
            with open(a.quarantine, encoding="utf-8") as fh:
                quarantine = json.load(fh).get("quarantine", [])
        except (OSError, json.JSONDecodeError, AttributeError) as exc:
            _fail(f"cannot read quarantine file: {exc}")
    if a.sample:
        base, cand = _sample()
    elif a.baseline and a.candidate:
        base, cand = load_jsonl(a.baseline), load_jsonl(a.candidate)
    else:
        p.error("give --baseline and --candidate, or --sample")
    report, code = gate(base, cand, quarantine, a.tolerance, a.max_cost_increase, a.allow_missing, today)
    print(json.dumps(report, indent=2) if a.output == "json" else render(report))
    return code


if __name__ == "__main__":
    sys.exit(main())
