#!/usr/bin/env python3
"""Find cost anomalies and unit-cost drift in a FOCUS export.

For each group (ServiceName by default) and day, compares EffectiveCost with
the median of the previous --window days. A day is an anomaly when it is
above median + k * 1.4826 * MAD (a robust z-score, not swayed by earlier
spikes) AND at least --min-rel above the median AND at least --min-abs in
money. All three are needed: a z-score alone flags cents on a quiet service,
a percentage alone flags noise, a money floor alone misses small services
that tripled.

With --units (CSV: date,units, e.g. orders or active users per day) it also
reports cost per unit for the first and second half of the period, because a
total that grows with the business is not a problem and a unit cost that
grows is.

Findings
  ANOMALY          group-day above all three thresholds                     FINDING
  UNIT_COST_UP     cost per unit up more than --min-rel half over half     FINDING
  SHORT_HISTORY    fewer than --window days before the first judged day    INFO

Refuses (exit 3) with fewer than 14 days of data: there is no baseline.
Exit codes: 0 none, 2 findings, 3 bad input.
Deterministic, stdlib only, no network.
"""
import argparse
import csv
import datetime as dt
import io
import json
import os
import statistics
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from focus_common import RULES_VERIFIED, load, read_input, sample_csv  # noqa: E402

EXIT = {"OK": 0, "FINDINGS": 2, "BAD_INPUT": 3}
MIN_DAYS = 14


def series(rows, by):
    s = defaultdict(lambda: defaultdict(float))
    for r in rows:
        if r.get("ChargeCategory") == "Tax":
            continue
        s[r.get(by) or "(none)"][r["_day"]] += r["EffectiveCost"]
    return s


def analyse(rows, by, window, k, min_rel, min_abs, units):
    days = sorted({r["_day"] for r in rows})
    span = (days[-1] - days[0]).days + 1
    if span < MIN_DAYS:
        raise ValueError(f"only {span} days of data; need at least {MIN_DAYS} for a baseline")
    all_days = [days[0] + dt.timedelta(days=i) for i in range(span)]
    findings, info = [], []
    for grp, s in sorted(series(rows, by).items()):
        vals = [s.get(d, 0.0) for d in all_days]
        for i in range(max(7, 1), len(vals)):
            hist = vals[max(0, i - window):i]
            if len(hist) < 7:
                continue
            med = statistics.median(hist)
            mad = statistics.median([abs(x - med) for x in hist])
            thr = med + k * 1.4826 * mad
            v = vals[i]
            if v > thr and v >= med * (1 + min_rel) and v - med >= min_abs:
                z = (v - med) / (1.4826 * mad) if mad > 0 else float("inf")
                findings.append({"code": "ANOMALY", "group": grp, "date": str(all_days[i]),
                                 "cost": round(v, 2), "baseline_median": round(med, 2),
                                 "excess": round(v - med, 2), "robust_z": None if z == float("inf") else round(z, 1),
                                 "message": f"{grp} on {all_days[i]}: {v:,.2f} vs median {med:,.2f} (+{v - med:,.2f})"})
    if span < window + 7:
        info.append({"code": "SHORT_HISTORY", "message": f"{span} days of data; the first judged days use a baseline shorter than --window {window}"})
    unit = None
    if units:
        total = defaultdict(float)
        for r in rows:
            if r.get("ChargeCategory") != "Tax":
                total[r["_day"]] += r["EffectiveCost"]
        common = [d for d in all_days if units.get(d)]
        if len(common) < MIN_DAYS:
            raise ValueError(f"--units covers {len(common)} days of the period; need {MIN_DAYS}")
        half = len(common) // 2
        a, b = common[:half], common[half:]
        ua = sum(total[d] for d in a) / sum(units[d] for d in a)
        ub = sum(total[d] for d in b) / sum(units[d] for d in b)
        unit = {"first_half": round(ua, 6), "second_half": round(ub, 6), "change": round((ub - ua) / ua, 4) if ua else None}
        if ua and (ub - ua) / ua > min_rel:
            findings.append({"code": "UNIT_COST_UP", "message": f"cost per unit {ua:.4f} -> {ub:.4f} ({(ub - ua) / ua:+.1%}) half over half"})
    return {"verdict": "OK" if not findings else "FINDINGS", "rules_verified": RULES_VERIFIED,
            "currency": rows[0].get("BillingCurrency"), "period": [str(days[0]), str(days[-1])],
            "grouped_by": by, "thresholds": {"window": window, "k": k, "min_rel": min_rel, "min_abs": min_abs},
            "unit_cost": unit, "findings": findings, "info": info}


def load_units(path):
    with open(path, encoding="utf-8-sig") as fh:
        rdr = csv.DictReader(fh)
        if not rdr.fieldnames or not {"date", "units"} <= set(rdr.fieldnames):
            raise ValueError("--units CSV needs columns date,units")
        out = {}
        for r in rdr:
            out[dt.date.fromisoformat(r["date"][:10])] = float(r["units"])
        return out


def sample_units():
    start = dt.date(2026, 10, 1)
    return {start + dt.timedelta(days=i): 5200.0 - (i * 20 if i > 14 else 0) for i in range(28)}


def render(res):
    t = res["thresholds"]
    out = [f"Cost anomalies: {res['verdict']}  ({res['period'][0]} to {res['period'][1]}, {res['currency']}, by {res['grouped_by']})",
           f"Rule: above median of previous {t['window']} days + {t['k']} robust SD, and +{t['min_rel']:.0%}, and +{t['min_abs']:,.0f}", ""]
    for f in res["findings"]:
        out.append(f"[FINDING] {f['code']}: {f['message']}")
    if not res["findings"]:
        out.append("No anomalies.")
    if res["unit_cost"]:
        u = res["unit_cost"]
        out.append(f"Unit cost: {u['first_half']:.4f} -> {u['second_half']:.4f}")
    out += [f"[INFO] {i['code']}: {i['message']}" for i in res["info"]]
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0], epilog="Exit codes: 0 none, 2 findings, 3 bad input.")
    ap.add_argument("--input", help="FOCUS cost-and-usage CSV export, daily granularity or finer")
    ap.add_argument("--by", default="ServiceName", help="column to group by (default ServiceName; e.g. SubAccountName)")
    ap.add_argument("--window", type=int, default=14, help="baseline days (default 14)")
    ap.add_argument("-k", type=float, default=3.0, help="robust SDs above the median (default 3)")
    ap.add_argument("--min-rel", type=float, default=0.3, help="minimum relative excess (default 0.3 = 30%%)")
    ap.add_argument("--min-abs", type=float, default=50.0, help="minimum excess in billing currency (default 50)")
    ap.add_argument("--units", help="CSV with date,units for unit cost (orders, users, requests)")
    ap.add_argument("--sample", action="store_true", help="run on a built-in synthetic export with one spike")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    a = ap.parse_args(argv)
    try:
        if a.window < 7 or a.k <= 0 or a.min_rel < 0 or a.min_abs < 0:
            raise ValueError("--window >= 7, -k > 0, --min-rel and --min-abs >= 0")
        text = sample_csv() if a.sample else (read_input(a.input) if a.input else None)
        if text is None:
            raise ValueError("give --input FILE or --sample")
        units = sample_units() if a.sample else (load_units(a.units) if a.units else None)
        rows = load(text)
        if a.by not in rows[0]:
            raise ValueError(f"column {a.by} not in the export")
        res = analyse(rows, a.by, a.window, a.k, a.min_rel, a.min_abs, units)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT["BAD_INPUT"]
    print(json.dumps(res, indent=2) if a.output == "json" else render(res))
    return EXIT[res["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
