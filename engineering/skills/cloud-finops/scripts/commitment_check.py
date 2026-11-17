#!/usr/bin/env python3
"""Commitment discounts (Savings Plans, Reserved Instances, CUDs) from a FOCUS export.

Computes, per FinOps Foundation definitions:
  utilization  share of commitment cost that covered usage
               = EffectiveCost(Used) / EffectiveCost(Used + Unused)
  coverage     share of eligible usage covered by commitments, on-demand
               equivalent = ListCost(committed usage) / ListCost(eligible usage)
  ESR          effective savings rate = savings / on-demand equivalent spend
               = (ListCost(eligible usage) - EffectiveCost(eligible usage)
                  - EffectiveCost(Unused)) / ListCost(eligible usage)

ListCost stands in for the on-demand equivalent; that is exact where the
provider's list price is its on-demand price, and an approximation otherwise.
"Eligible" usage is usage in the --eligible service categories (default
Compute) plus any row that already carries a CommitmentDiscountId.

It also gives the steady floor of uncovered eligible usage (the lowest daily
on-demand spend in the window), which is the most that a new commitment could
cover every day. Sizing above that floor bets on growth; say so if you do it.

Findings
  LOW_UTILIZATION   a commitment below --min-utilization (wasted spend)     FINDING
  UNUSED_COST       total Unused EffectiveCost > 0                           FINDING
  COVERAGE_GAP      coverage below --min-coverage while utilization is at or
                    above --min-utilization (buy more only now)             FINDING
  BUY_WHILE_WASTING coverage gap AND low utilization: fix utilization first  FINDING

Exit codes: 0 healthy, 2 findings, 3 bad input.
Deterministic, stdlib only, no network.
"""
import argparse
import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from focus_common import RULES_VERIFIED, load, read_input, sample_csv  # noqa: E402

EXIT = {"OK": 0, "FINDINGS": 2, "BAD_INPUT": 3}


def analyse(rows, eligible_cats, min_util, min_cov):
    if not any("CommitmentDiscountStatus" in r for r in rows):
        raise ValueError("no CommitmentDiscountStatus column: the provider export has no commitment data")
    usage = [r for r in rows if r.get("ChargeCategory") == "Usage"]
    used = [r for r in usage if (r.get("CommitmentDiscountStatus") or "") == "Used"]
    unused = [r for r in usage if (r.get("CommitmentDiscountStatus") or "") == "Unused"]
    per = defaultdict(lambda: {"used": 0.0, "unused": 0.0})
    for r in used:
        per[r.get("CommitmentDiscountId") or "(unnamed)"]["used"] += r["EffectiveCost"]
    for r in unused:
        per[r.get("CommitmentDiscountId") or "(unnamed)"]["unused"] += r["EffectiveCost"]
    used_c = sum(v["used"] for v in per.values())
    unused_c = sum(v["unused"] for v in per.values())
    util = used_c / (used_c + unused_c) if used_c + unused_c > 0 else None

    def eligible(r):
        return (r.get("ServiceCategory") in eligible_cats or (r.get("CommitmentDiscountId") or "").strip()) and r.get("CommitmentDiscountStatus") != "Unused"
    elig = [r for r in usage if eligible(r)]
    list_elig = sum(r["ListCost"] for r in elig)
    list_committed = sum(r["ListCost"] for r in elig if (r.get("CommitmentDiscountStatus") or "") == "Used")
    eff_elig = sum(r["EffectiveCost"] for r in elig)
    cov = list_committed / list_elig if list_elig > 0 else None
    esr = (list_elig - eff_elig - unused_c) / list_elig if list_elig > 0 else None

    daily_od = defaultdict(float)
    for r in elig:
        if (r.get("CommitmentDiscountStatus") or "") != "Used":
            daily_od[r["_day"]] += r["EffectiveCost"]
    days = sorted({r["_day"] for r in rows})
    floor = min(daily_od.get(d, 0.0) for d in days) if days else 0.0

    findings = []
    low = []
    for cid, v in sorted(per.items()):
        tot = v["used"] + v["unused"]
        u = v["used"] / tot if tot else None
        if u is not None and u < min_util:
            low.append(cid)
            findings.append({"code": "LOW_UTILIZATION", "message": f"{cid}: utilization {u:.1%} < {min_util:.0%}; {v['unused']:,.2f} unused"})
    if unused_c > 0:
        findings.append({"code": "UNUSED_COST", "message": f"{unused_c:,.2f} of commitment cost went unused in the period"})
    if cov is not None and cov < min_cov:
        if low:
            findings.append({"code": "BUY_WHILE_WASTING", "message": f"coverage {cov:.1%} < {min_cov:.0%} but commitments are under-used: move or reshape workloads onto the existing commitments before buying more"})
        else:
            findings.append({"code": "COVERAGE_GAP", "message": f"coverage {cov:.1%} < {min_cov:.0%}; uncovered eligible spend never fell below {floor:,.2f}/day in this window, which bounds a new commitment that would stay fully used"})
    return {
        "verdict": "OK" if not findings else "FINDINGS",
        "rules_verified": RULES_VERIFIED,
        "currency": rows[0].get("BillingCurrency"),
        "period": [str(days[0]), str(days[-1])],
        "eligible_service_categories": sorted(eligible_cats),
        "utilization": None if util is None else round(util, 4),
        "coverage": None if cov is None else round(cov, 4),
        "effective_savings_rate": None if esr is None else round(esr, 4),
        "on_demand_equivalent_eligible": round(list_elig, 2),
        "effective_cost_eligible": round(eff_elig, 2),
        "unused_commitment_cost": round(unused_c, 2),
        "uncovered_daily_floor": round(floor, 2),
        "commitments": {cid: {"used": round(v["used"], 2), "unused": round(v["unused"], 2),
                              "utilization": round(v["used"] / (v["used"] + v["unused"]), 4) if v["used"] + v["unused"] else None}
                        for cid, v in per.items()},
        "findings": findings,
    }


def pct(x):
    return "n/a" if x is None else f"{x:.1%}"


def render(res):
    out = [f"Commitment check: {res['verdict']}  ({res['period'][0]} to {res['period'][1]}, {res['currency']}; eligible = {', '.join(res['eligible_service_categories'])})",
           f"Utilization {pct(res['utilization'])} · Coverage {pct(res['coverage'])} · Effective savings rate {pct(res['effective_savings_rate'])}",
           f"On-demand equivalent {res['on_demand_equivalent_eligible']:,.2f}, paid {res['effective_cost_eligible']:,.2f} + unused {res['unused_commitment_cost']:,.2f}",
           f"Uncovered eligible spend floor: {res['uncovered_daily_floor']:,.2f}/day", ""]
    for cid, v in res["commitments"].items():
        out.append(f"  {cid}: used {v['used']:,.2f}, unused {v['unused']:,.2f}, utilization {pct(v['utilization'])}")
    out.append("")
    out += [f"[FINDING] {f['code']}: {f['message']}" for f in res["findings"]] or ["No findings."]
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0], epilog="Exit codes: 0 healthy, 2 findings, 3 bad input.")
    ap.add_argument("--input", help="FOCUS cost-and-usage CSV export")
    ap.add_argument("--eligible", default="Compute", help="ServiceCategory values commitments can cover, comma-separated (default Compute)")
    ap.add_argument("--min-utilization", type=float, default=0.95, help="utilization floor per commitment (default 0.95)")
    ap.add_argument("--min-coverage", type=float, default=0.7, help="coverage target (default 0.7; your policy)")
    ap.add_argument("--sample", action="store_true", help="run on a built-in synthetic export")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    a = ap.parse_args(argv)
    try:
        for v in (a.min_utilization, a.min_coverage):
            if not 0 <= v <= 1:
                raise ValueError("--min-utilization and --min-coverage must be in [0, 1]")
        text = sample_csv() if a.sample else (read_input(a.input) if a.input else None)
        if text is None:
            raise ValueError("give --input FILE or --sample")
        cats = {c.strip() for c in a.eligible.split(",") if c.strip()}
        res = analyse(load(text), cats, a.min_utilization, a.min_coverage)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT["BAD_INPUT"]
    print(json.dumps(res, indent=2) if a.output == "json" else render(res))
    return EXIT[res["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
