#!/usr/bin/env python3
"""Flag every material account fluctuation and refuse explanations that explain nothing.

Flux review is where a close either catches the misposting or rubber-stamps it.
The failure is rarely missing a variance; it is accepting "timing" or "in line
with expectations" as the reason. Auditing standards on analytical procedures
(PCAOB AS 2305) say the threshold for investigating a difference is driven by
materiality, and that management's explanation should ordinarily be
corroborated with other evidence. This script applies that to the close.

An account is MATERIAL when its change versus the comparison column passes the
threshold rule (both --pct and --abs by default; --rule or makes either one
enough), when it flips sign, or when it is new or gone and above --abs.
Thresholds are your policy; no standard prescribes a percentage or amount.

Every material line needs an explanation, and the explanation is linted:
  MISSING      empty
  BOILERPLATE  a stock phrase ("timing", "n/a", "in line with expectations",
               "business as usual", "various", "normal fluctuation") with no number
  NO_DRIVER    no quantified driver (no figure at all) - says that it moved, not why
  NO_EVIDENCE  explanation present but no evidence reference (a sign-off alone is
               not evidence of review) - warning only

With --reviewer, a material line whose owner is the reviewer is SELF_REVIEW and
blocks: nobody reviews their own explanation. Name a second reviewer for those lines.

CSV columns (header row required): account, name, current, prior, and optionally
budget, explanation, evidence, owner. --compare budget uses the budget column.

Deterministic, stdlib only, no network.

Exit codes:
    0  COMPLETE - every material line has a quantified, evidenced explanation
    2  NEEDS_EVIDENCE - explanations are adequate but some lack evidence references
    3  invalid input
    4  INCOMPLETE - material lines with missing, boilerplate or unquantified explanations,
                    or lines the reviewer owns
"""

import argparse
import csv
import io
import json
import re
import sys

BOILERPLATE = re.compile(r"^\s*(timing( difference)?|n/?a|none|tbd|see (above|below|prior)|in line with (expectations|budget|plan)"
                         r"|business as usual|bau|various|misc(ellaneous)?|normal (fluctuation|activity|course)|immaterial"
                         r"|as expected|no (issue|concern)s?|ok|fine|reviewed)\W*$", re.I)
HAS_NUMBER = re.compile(r"\d")

SAMPLE_CSV = """account,name,current,prior,explanation,evidence,owner
4000,Subscription revenue,1250000,1120000,"Net new ARR 140k from 6 enterprise deals closed Sep; churn -10k (2 SMB logos)",CRM export oct-arr.xlsx,Sam
5100,Hosting costs,182000,141000,timing,,Priya
6200,Contractors,64000,61000,,,Dana
6300,Travel,18500,9200,"Two offsites (Berlin 6.1k, Lisbon 3.4k) budgeted in Q4",TE report 10/2026,Dana
2100,Accrued liabilities,-96000,-150000,"Released 60k legal accrual after settlement signed 14 Oct; new 6k audit fee accrual",Settlement agreement,Lee
1500,Prepaid expenses,-4000,22000,Reclass error suspected,,Lee
6900,Bank charges,2400,1100,"Higher charges",,Sam
"""


def _fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(3)


def num(raw, where):
    s = str(raw).strip().replace(",", "")
    neg = s.startswith("(") and s.endswith(")")
    s = s.strip("()") or "0"
    try:
        v = float(s)
    except ValueError:
        _fail(f"{where}: not a number ({raw!r})")
    return -v if neg else v


def lint_explanation(text, evidence):
    t = (text or "").strip()
    if not t:
        return "MISSING"
    if BOILERPLATE.match(t):
        return "BOILERPLATE"
    if not HAS_NUMBER.search(t):
        return "NO_DRIVER"
    if not (evidence or "").strip():
        return "NO_EVIDENCE"
    return "OK"


def analyse(text, pct, abs_thr, rule, compare, reviewer=None):
    reader = csv.DictReader(io.StringIO(text))
    cols = {c.strip().lower() for c in (reader.fieldnames or [])}
    need = {"account", "current", compare}
    if not need <= cols:
        _fail(f"CSV needs columns {sorted(need)}; has {sorted(cols)}")
    lines = []
    for n, raw in enumerate(reader, 2):
        r = {k.strip().lower(): (v or "").strip() for k, v in raw.items() if k}
        cur, base = num(r["current"], f"line {n} current"), num(r[compare], f"line {n} {compare}")
        delta = cur - base
        rel = abs(delta) / abs(base) if base else None
        reasons = []
        over_abs = abs(delta) >= abs_thr
        over_pct = rel is None or rel * 100 >= pct
        if (over_abs and over_pct) if rule == "and" else (over_abs or over_pct and abs(delta) > 0):
            reasons.append(f"{delta:+,.0f} ({'new' if rel is None else format(delta / abs(base), '+.0%')})")
        if base and cur and (base > 0) != (cur > 0):
            reasons.append("sign flip")
        if (base == 0) != (cur == 0) and abs(delta) >= abs_thr and "sign flip" not in reasons and not reasons:
            reasons.append("new or closed balance")
        material = bool(reasons)
        status = lint_explanation(r.get("explanation"), r.get("evidence")) if material else "NOT_MATERIAL"
        lines.append({"account": r["account"], "name": r.get("name", ""), "current": cur, compare: base,
                      "delta": round(delta, 2), "pct": None if rel is None else round(delta / abs(base) * 100, 1),
                      "material": material, "why_material": reasons, "explanation_status": status,
                      "owner": r.get("owner", ""), "explanation": r.get("explanation", "")})
    if not lines:
        _fail("no account rows")
    material = [l for l in lines if l["material"]]
    failing = [l for l in material if l["explanation_status"] in ("MISSING", "BOILERPLATE", "NO_DRIVER")]
    unevidenced = [l for l in material if l["explanation_status"] == "NO_EVIDENCE"]
    self_review = [l["account"] for l in material
                   if reviewer and l["owner"].strip().lower() == reviewer.strip().lower()]
    verdict, code = ("INCOMPLETE", 4) if failing or self_review else (("NEEDS_EVIDENCE", 2) if unevidenced else ("COMPLETE", 0))
    return {"verdict": verdict, "compare": compare, "threshold": {"pct": pct, "abs": abs_thr, "rule": rule},
            "accounts": len(lines), "material": len(material), "failing": len(failing), "unevidenced": len(unevidenced),
            "reviewer": reviewer, "self_review": self_review,
            "material_lines": sorted(material, key=lambda l: -abs(l["delta"])),
            "not_material": [l["account"] for l in lines if not l["material"]]}, code


def render(r):
    t = r["threshold"]
    out = [f"Flux review vs {r['compare']}: {r['verdict']}",
           f"  threshold: >= {t['pct']}% {t['rule'].upper()} >= {t['abs']:,.0f} (your policy); "
           f"{r['material']} of {r['accounts']} accounts material, {r['failing']} failing, {r['unevidenced']} without evidence"]
    for l in r["material_lines"]:
        mark = "ok " if l["explanation_status"] == "OK" else "!! "
        out.append(f"  {mark}{l['account']:<6} {l['name'][:24]:<24} {', '.join(l['why_material']):<22} "
                   f"{l['explanation_status']:<12} owner {l['owner'] or '-'}")
    if r["self_review"]:
        out.append(f"  !! {r['reviewer']} owns {', '.join(r['self_review'])} and cannot review them; name a second reviewer.")
    if r["failing"]:
        out.append("  Every '!!' line needs a quantified driver (what moved, by how much, why) before the close is signed.")
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description="Flux analysis: flag material account changes and lint their explanations.")
    p.add_argument("--input", help="trial balance comparison CSV (account, name, current, prior[, budget, explanation, evidence, owner])")
    p.add_argument("--pct", type=float, default=10.0, help="percentage threshold (default 10; policy, not a standard)")
    p.add_argument("--abs", dest="abs_thr", type=float, default=10000.0, help="absolute threshold (default 10000; policy, not a standard)")
    p.add_argument("--rule", choices=["and", "or"], default="and", help="material when both thresholds pass (and) or either (or)")
    p.add_argument("--compare", choices=["prior", "budget"], default="prior", help="comparison column (default prior)")
    p.add_argument("--reviewer", help="name of the flux reviewer; material lines they own block as self-review")
    p.add_argument("--sample", action="store_true", help="run on an embedded sample")
    p.add_argument("--output", choices=["text", "json"], default="text")
    a = p.parse_args()
    if a.sample:
        text = SAMPLE_CSV
    elif a.input:
        try:
            text = open(a.input, encoding="utf-8-sig").read()
        except OSError as exc:
            _fail(f"cannot read {a.input}: {exc.strerror}")
    else:
        p.error("give --input, or --sample")
    report, code = analyse(text, a.pct, a.abs_thr, a.rule, a.compare, a.reviewer)
    print(json.dumps(report, indent=2) if a.output == "json" else render(report))
    return code


if __name__ == "__main__":
    sys.exit(main())
