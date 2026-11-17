#!/usr/bin/env python3
"""Measure how much cloud spend can be allocated to an owner, from a FOCUS export.

Allocation coverage = EffectiveCost of rows carrying every required tag with a
non-empty value / allocatable EffectiveCost (all rows except Tax). Reports
spend by service category and sub account, the largest unallocated resources,
and tag-value hygiene problems that split one owner into several (Prod vs prod).

Findings
  BELOW_TARGET     coverage below --target                                  FINDING
  CASE_VARIANTS    one tag key has values differing only in case/spacing    FINDING
  EMPTY_VALUE      tag present with an empty value (counts as untagged)     FINDING
  NO_RESOURCE_ID   unallocated cost on rows with no ResourceId (shared or
                   commitment waste): needs a split rule, not a tag         INFO

EffectiveCost is used, not BilledCost, so prepaid commitments are spread over
the usage they covered (FOCUS sets EffectiveCost to 0 on purchase rows).

Exit codes: 0 at or above target, 2 findings, 3 bad input.
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


def norm(v):
    return " ".join(v.lower().replace("_", "-").split())


def analyse(rows, required, target, top):
    allocatable = [r for r in rows if r.get("ChargeCategory") != "Tax"]
    total = sum(r["EffectiveCost"] for r in allocatable)
    if total <= 0:
        raise ValueError("allocatable EffectiveCost is zero; is this a FOCUS cost export?")
    tagged = 0.0
    by_cat, by_acct = defaultdict(float), defaultdict(float)
    untagged_res = defaultdict(float)
    no_res_cost = 0.0
    values = defaultdict(lambda: defaultdict(float))
    empty = defaultdict(float)
    for r in allocatable:
        c = r["EffectiveCost"]
        by_cat[r.get("ServiceCategory") or "(none)"] += c
        by_acct[r.get("SubAccountName") or r.get("SubAccountId") or "(none)"] += c
        tags = r["_tags"]
        for k, v in tags.items():
            if v.strip():
                values[k][v] += c
            else:
                empty[k] += c
        if all(tags.get(k, "").strip() for k in required):
            tagged += c
        else:
            rid = (r.get("ResourceId") or "").strip()
            if rid:
                untagged_res[(rid, r.get("ServiceName", ""))] += c
            else:
                no_res_cost += c
    cov = tagged / total
    findings = []
    if cov < target:
        findings.append({"code": "BELOW_TARGET", "message": f"allocation coverage {cov:.1%} < target {target:.0%}"})
    for k in sorted(values):
        groups = defaultdict(list)
        for v in values[k]:
            groups[norm(v)].append(v)
        for vs in groups.values():
            if len(vs) > 1:
                findings.append({"code": "CASE_VARIANTS", "message": f"tag '{k}' has {sorted(vs)}: one owner counted as {len(vs)}; normalise in the tag policy"})
    for k, c in sorted(empty.items()):
        if c > 0:
            findings.append({"code": "EMPTY_VALUE", "message": f"tag '{k}' present but empty on {c:,.2f} of cost"})
    info = []
    if no_res_cost > 0:
        info.append({"code": "NO_RESOURCE_ID", "message": f"{no_res_cost:,.2f} unallocated cost has no ResourceId (shared charges or unused commitment): allocate it by a split rule (proportional, even or fixed), not by tagging"})
    near = []
    lower_req = {k.lower(): k for k in required}
    for k in values:
        if k not in required and k.lower() in lower_req:
            near.append(f"'{k}' (required key is '{lower_req[k.lower()]}')")
    if near:
        findings.append({"code": "CASE_VARIANTS", "message": "tag key spelled differently from the required key: " + ", ".join(near)})
    return {
        "verdict": "OK" if not findings else "FINDINGS",
        "rules_verified": RULES_VERIFIED,
        "currency": rows[0].get("BillingCurrency"),
        "period": [str(min(r["_day"] for r in rows)), str(max(r["_day"] for r in rows))],
        "required_tags": required,
        "allocatable_effective_cost": round(total, 2),
        "allocated_effective_cost": round(tagged, 2),
        "coverage": round(cov, 4),
        "target": target,
        "by_service_category": {k: round(v, 2) for k, v in sorted(by_cat.items(), key=lambda x: -x[1])},
        "by_sub_account": {k: round(v, 2) for k, v in sorted(by_acct.items(), key=lambda x: -x[1])},
        "top_unallocated_resources": [{"resource": rid, "service": svc, "effective_cost": round(c, 2)}
                                      for (rid, svc), c in sorted(untagged_res.items(), key=lambda x: -x[1])[:top]],
        "findings": findings,
        "info": info,
    }


def render(res):
    cur = res["currency"]
    out = [f"Allocation check: {res['verdict']}  ({res['period'][0]} to {res['period'][1]}, {cur})",
           f"Coverage {res['coverage']:.1%} of {res['allocatable_effective_cost']:,.2f} allocatable EffectiveCost "
           f"carries all of {', '.join(res['required_tags'])} (target {res['target']:.0%})", "",
           "By service category:"]
    out += [f"  {k:20s} {v:>12,.2f}" for k, v in res["by_service_category"].items()]
    out.append("Largest unallocated resources:")
    out += [f"  {x['resource']:20s} {x['service']:24s} {x['effective_cost']:>12,.2f}" for x in res["top_unallocated_resources"]] or ["  none"]
    out.append("")
    out += [f"[FINDING] {f['code']}: {f['message']}" for f in res["findings"]]
    out += [f"[INFO] {f['code']}: {f['message']}" for f in res["info"]]
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0], epilog="Exit codes: 0 at or above target, 2 findings, 3 bad input.")
    ap.add_argument("--input", help="FOCUS cost-and-usage CSV export")
    ap.add_argument("--required-tags", default="team,env,cost-center", help="comma-separated tag keys every row must carry (default team,env,cost-center)")
    ap.add_argument("--target", type=float, default=0.9, help="coverage target, 0-1 (default 0.9; set your own policy)")
    ap.add_argument("--top", type=int, default=10, help="unallocated resources to list (default 10)")
    ap.add_argument("--sample", action="store_true", help="run on a built-in synthetic export")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    a = ap.parse_args(argv)
    try:
        if not 0 < a.target <= 1:
            raise ValueError("--target must be in (0, 1]")
        text = sample_csv() if a.sample else (read_input(a.input) if a.input else None)
        if text is None:
            raise ValueError("give --input FILE or --sample")
        required = [t.strip() for t in a.required_tags.split(",") if t.strip()]
        if not required:
            raise ValueError("--required-tags is empty")
        res = analyse(load(text), required, a.target, a.top)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT["BAD_INPUT"]
    print(json.dumps(res, indent=2) if a.output == "json" else render(res))
    return EXIT[res["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
