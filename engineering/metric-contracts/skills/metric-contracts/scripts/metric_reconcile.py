#!/usr/bin/env python3
"""Two places report the same metric with different numbers. Find out why.

Give two CSVs of one metric by period (warehouse vs BI tool, finance vs
product dashboard, old vs new definition). Each needs a key column (period,
or any join key) and a value column. Rows are matched on the key, compared
with a relative tolerance, and the pattern of the differences is matched to
the cause that usually produces it.

Patterns (first match is reported as most likely; all matches are listed)
  COVERAGE    keys present on one side only (late load, different history start)
  BUCKETING   totals agree, periods do not: same records, different period
              assignment (time zone, or order date vs ship date)
  SCALE       one side is a constant multiple of the other (cents vs units,
              percent vs fraction, tax included, currency conversion)
  OFFSET      constant absolute gap (a manual adjustment row, one-off record)
  STEP        agree until one period, disagree from then on (definition or
              pipeline change at that point)
  TAIL        only the latest periods disagree (freshness, restatement)
  SUBSET      one side always lower by a varying share (it excludes refunds,
              cancellations, test or internal accounts, a region); always
              higher suggests a join fan-out double counting
  MIXED       none of the above: compare the definitions (metric_diff.py)

Exit codes: 0 every matched key within tolerance and no coverage gap,
2 mismatch, 3 bad input. Deterministic, stdlib only, no network.
"""
import argparse
import csv
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from metric_common import VERIFIED, asset, emit  # noqa: E402

KNOWN_FACTORS = [(100, "cents vs units, or percent vs fraction"), (1000, "thousands, or ms vs s"),
                 (1.19, "19% VAT included on one side"), (1.2, "20% VAT included on one side"),
                 (1.07, "7% tax included on one side"), (1.1, "10% tax included on one side"),
                 (24, "hours vs days"), (60, "minutes vs hours"), (7, "weekly vs daily")]


class Bad(Exception):
    pass


def read(path, key, value):
    if not os.path.isfile(path):
        raise Bad(f"{path}: file not found")
    with open(path, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        raise Bad(f"{path}: no rows")
    cols = list(rows[0].keys())
    k = key or cols[0]
    v = value or (cols[1] if len(cols) > 1 else None)
    if k not in cols or v not in cols:
        raise Bad(f"{path}: needs columns {k!r} and {v!r}; has {cols}")
    out = {}
    for i, r in enumerate(rows, 2):
        raw = (r[v] or "").strip().replace(",", "")
        try:
            val = float(raw) if raw else 0.0
        except ValueError:
            raise Bad(f"{path} line {i}: {v}={r[v]!r} is not a number")
        if val != val or val in (float("inf"), float("-inf")):
            raise Bad(f"{path} line {i}: {v} is not finite")
        kk = r[k].strip()
        if kk in out:
            raise Bad(f"{path}: key {kk!r} appears twice; aggregate to one row per key first")
        out[kk] = val
    return out


def _near(x, y, rel):
    return abs(x - y) <= rel * max(abs(x), abs(y), 1e-12)


def diagnose(a, b, rel, abs_tol):
    keys = sorted(a.keys() | b.keys())
    only_a = [k for k in keys if k not in b]
    only_b = [k for k in keys if k not in a]
    both = [k for k in keys if k in a and k in b]
    rows, patterns = [], []
    for k in both:
        d = b[k] - a[k]
        ok = abs(d) <= abs_tol or _near(a[k], b[k], rel)
        rows.append({"key": k, "a": a[k], "b": b[k], "diff": d, "rel": d / a[k] if a[k] else None, "ok": ok})
    bad = [r for r in rows if not r["ok"]]
    if only_a or only_b:
        where = []
        for side, ks in (("a", only_a), ("b", only_b)):
            if ks:
                pos = "at the end" if ks[-1] == keys[-1] and len(ks) <= 3 else ("at the start" if ks[0] == keys[0] else "in the middle")
                where.append(f"{len(ks)} key(s) only in {side} {pos} ({', '.join(ks[:5])})")
        patterns.append(("COVERAGE", "; ".join(where) + ". End: one side not loaded yet. Start: different "
                         "history or backfill. Middle: a failed load or a filter on dates",
                         "check load times and the date filter on both sides"))
    if not bad:
        return rows, bad, patterns
    sa, sb = sum(r["a"] for r in rows), sum(r["b"] for r in rows)
    if len(bad) >= 2 and _near(sa, sb, rel):
        patterns.append(("BUCKETING", f"totals agree ({sa:,.2f} vs {sb:,.2f}) but {len(bad)} period(s) do not: "
                         "the same records land in different periods",
                         "compare the time zone and the date column each side groups by"))
    ratios = [r["b"] / r["a"] for r in bad if r["a"]]
    diffs = [r["diff"] for r in bad]
    every = len(bad) == len(rows) and len(bad) >= 2
    cv_ratio = statistics.pstdev(ratios) / abs(statistics.mean(ratios)) if len(ratios) >= 2 and statistics.mean(ratios) else 1
    cv_diff = statistics.pstdev(diffs) / abs(statistics.mean(diffs)) if len(diffs) >= 2 and statistics.mean(diffs) else 1
    constant = None  # whichever of ratio or gap is steadier explains it
    if every and min(cv_ratio, cv_diff) < 0.005:
        constant = "SCALE" if cv_ratio <= cv_diff else "OFFSET"
    if constant == "SCALE":
        f = statistics.mean(ratios)
        g = f if f >= 1 else 1 / f
        name = next((n for x, n in KNOWN_FACTORS if abs(g - x) / x < 0.01), "a unit, currency or FX difference")
        patterns.append(("SCALE", f"b is {f:.4g} x a on every period ({name})",
                         "compare the unit, currency and tax treatment of the two sources"))
    elif constant == "OFFSET":
        patterns.append(("OFFSET", f"constant gap of {statistics.mean(diffs):,.2f} on every period",
                         "look for a manual adjustment or a single record one side includes"))
    first = next(i for i, r in enumerate(rows) if not r["ok"])
    if 0 < first and all(not r["ok"] for r in rows[first:]) and len(rows) - first >= 2:
        if len(rows) - first <= 3 and first >= len(rows) / 2:
            patterns.append(("TAIL", f"only the last {len(rows) - first} period(s) differ, from {rows[first]['key']}",
                             "check freshness and late-arriving data; re-run after the next load"))
        patterns.append(("STEP", f"agree until {rows[first - 1]['key']}, differ from {rows[first]['key']} on",
                         f"find what changed on {rows[first]['key']}: a definition edit, deploy or new filter"))
    if not constant and len(bad) >= 2 and (all(r["diff"] < 0 for r in bad) or all(r["diff"] > 0 for r in bad)):
        lower = all(r["diff"] < 0 for r in bad)
        shares = [abs(r["rel"]) for r in bad if r["rel"] is not None]
        patterns.append(("SUBSET", f"b is {'lower' if lower else 'higher'} on all {len(bad)} differing periods, "
                         f"by {min(shares):.1%} to {max(shares):.1%}",
                         "one side excludes a subset (refunds, cancelled, test or internal accounts, a region)"
                         if lower else "b may double count through a join fan-out, or a looser filter"))
    if not [p for p in patterns if p[0] != "COVERAGE"]:
        patterns.append(("MIXED", "no single pattern fits", "diff the two definitions (metric_diff.py), "
                         "then split both sides by one dimension at a time"))
    return rows, bad, patterns


def render(res):
    lines = [f"Metric reconcile  a={res['a']}  b={res['b']}  tolerance {res['rel_tol']:.2%} (verified {VERIFIED})", "",
             f"  {res['matched']} matched keys, {res['breaches']} outside tolerance; "
             f"totals a={res['total_a']:,.2f} b={res['total_b']:,.2f}"]
    if res["worst"]:
        lines += ["", f"  {'key':<12} {'a':>14} {'b':>14} {'b-a':>12} {'rel':>8}"]
        for r in res["worst"]:
            rel = f"{r['rel']:+.2%}" if r["rel"] is not None else "n/a"
            lines.append(f"  {r['key']:<12} {r['a']:>14,.2f} {r['b']:>14,.2f} {r['diff']:>12,.2f} {rel:>8}")
    if res["patterns"]:
        lines.append("")
        for i, p in enumerate(res["patterns"]):
            lines.append(f"  {'MOST LIKELY' if i == 0 else 'also fits':<11} {p['pattern']}: {p['evidence']}")
            lines.append(f"              next: {p['next']}")
    lines += ["", f"Verdict: {res['verdict']}"]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--a", help="CSV from the first source (the one you trust more)")
    ap.add_argument("--b", help="CSV from the second source")
    ap.add_argument("--key", help="key column (default: first column)")
    ap.add_argument("--value", help="value column (default: second column)")
    ap.add_argument("--rel-tol", type=float, default=0.005, help="relative tolerance, default 0.005 (0.5%%)")
    ap.add_argument("--abs-tol", type=float, default=0.0, help="absolute tolerance, default 0")
    ap.add_argument("--top", type=int, default=10, help="rows to show, default 10")
    ap.add_argument("--sample", action="store_true", help="reconcile the bundled warehouse vs BI example")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    x = ap.parse_args()
    if x.sample:
        x.a, x.b = asset("revenue_warehouse.csv"), asset("revenue_bi_tool.csv")
    if not x.a or not x.b:
        ap.error("give --a FILE and --b FILE, or --sample")
    if not (0 <= x.rel_tol < 1) or x.abs_tol < 0:
        print("bad input: --rel-tol must be in [0, 1) and --abs-tol >= 0", file=sys.stderr)
        return 3
    try:
        a, b = read(x.a, x.key, x.value), read(x.b, x.key, x.value)
    except Bad as e:
        print(f"bad input: {e}", file=sys.stderr)
        return 3
    rows, bad, patterns = diagnose(a, b, x.rel_tol, x.abs_tol)
    if not rows:
        print("bad input: the two files share no keys", file=sys.stderr)
        return 3
    worst = sorted(bad, key=lambda r: -abs(r["diff"]))[:x.top]
    failed = bool(bad) or any(p[0] == "COVERAGE" for p in patterns)
    res = {"a": os.path.basename(x.a), "b": os.path.basename(x.b), "rel_tol": x.rel_tol, "matched": len(rows),
           "breaches": len(bad), "total_a": sum(r["a"] for r in rows), "total_b": sum(r["b"] for r in rows),
           "worst": sorted(worst, key=lambda r: r["key"]),
           "patterns": [{"pattern": p, "evidence": e, "next": n} for p, e, n in patterns],
           "verdict": "MISMATCH" if failed else "MATCH"}
    emit(res, x.output, render)
    return 2 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
