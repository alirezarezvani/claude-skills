#!/usr/bin/env python3
"""Compare a private deal's net-to-LP IRR to its risk-matched public benchmark.

The forcing function from `references/05-benchmark-returns.md`: a private deal
must clear a liquid, net-of-fee public comparator *plus* an illiquidity premium,
or the LP is locking up capital for no compensated reason. Given a deal type, the
net-to-LP IRR, and the hold, this estimates:

  * the comparator's trailing 10yr return (the liquid hurdle),
  * the premium the deal implies over that comparator, and
  * whether that premium clears the illiquidity hurdle for the lock-up.

Comparator figures are hardcoded from `references/data/` snapshots (see
LAST_UPDATED) - the stdlib-only constraint rules out a live data pull, and the
snapshots are the versioned source of truth. Supply `--benchmark-return` to
override the hardcoded figure with a current one.

Screening heuristic, not underwriting. Clearing the hurdle is *necessary, not
sufficient*: private-market dispersion (`05` / Preqin) means the median fund of a
type underperforms its marketed top-quartile figure, so a single deal beating the
spread still carries idiosyncratic and below-median risk the index diversifies
away. stdlib-only by design (no pip installs).
"""

import argparse
import json
import math
import os
import re
import sys


# --------------------------------------------------------------------------- #
# Data (config only - no logic). Source: references/data/ snapshots.
# --------------------------------------------------------------------------- #

# ETF returns to the 2026-06-30 quarter-end; Treasury daily closes 2026-09-24.
# Source: references/data/etf-comparators-snapshot.md and
# references/data/fred-10yr-snapshot.md. Refresh both, then bump this stamp.
LAST_UPDATED = "2026-09-27"

# Trailing 10yr total return, net of expense ratio (%).
COMPARATORS = {
    "VNQ": {"name": "Vanguard Real Estate / REITs", "ten_yr": 4.92},
    "HYG": {"name": "iShares iBoxx High-Yield Corp", "ten_yr": 4.83},
    "PFF": {"name": "iShares Preferred & Income", "ten_yr": 3.00},
    "LQD": {"name": "iShares iBoxx IG Corp Bond", "ten_yr": 2.36},
    "SPY": {"name": "SPDR S&P 500 (equity anchor)", "ten_yr": 15.39},
    "VTI": {"name": "Vanguard Total Market (equity anchor)", "ten_yr": 15.04},
}

# Risk-free curve points (%), for duration-matched debt floors.
TREASURY = {"3mo": 4.24, "2yr": 4.87, "10yr": 5.18}

# Private deal type -> risk-matched comparator (per `05` spread table). Debt types
# also carry a duration-matched Treasury point for the credit+illiquidity spread.
DEAL_TYPES = {
    "multifamily-value-add": {"comparator": "VNQ"},
    "multifamily-core": {"comparator": "VNQ"},
    "multifamily-equity": {"comparator": "VNQ"},
    "industrial": {"comparator": "VNQ"},
    "retail-necessity": {"comparator": "VNQ"},
    "sfr": {"comparator": "VNQ"},
    "development": {"comparator": "VNQ"},
    "hard-money": {"comparator": "HYG", "treasury": "3mo"},
    "private-credit": {"comparator": "HYG", "treasury": "2yr"},
    "preferred-equity": {"comparator": "PFF"},
}

# `01`/`05` "variable" classes get no category comparator - they benchmark against
# the deal's own underwriting, not a category default.
VARIABLE_TYPES = {"office", "experiential-retail", "str", "mixed-use"}

# Omitted inputs fall back to the `05` demo deal so a bare run is a live demo.
# Every fallback used is reported as ASSUMED - never silently compared.
DEFAULTS = {"deal_type": "multifamily-equity", "net_irr": 11.2, "hold_years": 5.0}


# --------------------------------------------------------------------------- #
# Pure calculation core (same input -> same output, no side effects)
# --------------------------------------------------------------------------- #

def normalize_deal_type(raw):
    """Lowercase and hyphenate a deal-type string."""
    return raw.strip().lower().replace("_", "-").replace(" ", "-")


def required_premium_bps(hold_years):
    """Illiquidity hurdle band (low, high) in bps for a lock-up, per `05`'s
    heuristic tiering: ~200bps at <=1yr, ~300-400 at 3-5yr, ~400-600 at 7-10yr.
    Scales the price of illiquidity with its duration; it is a heuristic, not a law."""
    if hold_years <= 1:
        return (200.0, 200.0)
    if hold_years <= 5:
        return (300.0, 400.0)
    return (400.0, 600.0)


def verdict_for(implied_bps, low, high):
    """Three-state read of the implied premium against the hurdle band."""
    if implied_bps < 0:
        return "FAILS - net IRR trails the liquid comparator outright"
    if implied_bps < low:
        return "THIN / FAILS - implied premium is below the illiquidity hurdle"
    if implied_bps < high:
        return "CLEARS (thin) - in the lower half of the hurdle band"
    return "CLEARS comfortably"


def compute_comparison(params, assumed=()):
    """Orchestrate the comparison from a params dict. Pure: returns a result
    dict, prints nothing. Raises ValueError on an unknown deal type. `assumed`
    names the params that fell back to DEFAULTS; they are carried into the result."""
    deal_type = normalize_deal_type(params["deal_type"])
    net_irr = params["net_irr"]
    hold = params["hold_years"]
    assumed_inputs = {k: params[k] for k in assumed}

    if deal_type in VARIABLE_TYPES:
        return {
            "deal_type": deal_type,
            "assumed_inputs": assumed_inputs,
            "variable": True,
            "guidance": ("This is a `variable` class (05): no category comparator. "
                         "Benchmark against the deal's own underwriting and the closest "
                         "stable analog - the absence of a category baseline is itself "
                         "informative."),
        }

    if deal_type not in DEAL_TYPES:
        valid = ", ".join(sorted(DEAL_TYPES) + sorted(VARIABLE_TYPES))
        raise ValueError(f"Unknown deal type '{deal_type}'. Valid types: {valid}")

    spec = DEAL_TYPES[deal_type]
    ticker = spec["comparator"]

    if params["benchmark_return"] is not None:
        comparator_return = params["benchmark_return"]
        comparator_label = f"user-supplied ({comparator_return:.2f}%)"
    else:
        comparator_return = COMPARATORS[ticker]["ten_yr"]
        comparator_label = f"{ticker} - {COMPARATORS[ticker]['name']} ({comparator_return:.2f}% 10yr)"

    implied_bps = (net_irr - comparator_return) * 100.0

    if params["illiquidity_premium_assumed"] is not None:
        req = params["illiquidity_premium_assumed"] * 100.0
        low, high = req, req
        hurdle_label = f"{req:.0f} bps (user-assumed)"
    else:
        low, high = required_premium_bps(hold)
        hurdle_label = (f"~{low:.0f} bps" if low == high
                        else f"~{low:.0f}-{high:.0f} bps")

    result = {
        "deal_type": deal_type,
        "assumed_inputs": assumed_inputs,
        "variable": False,
        "net_irr_pct": round(net_irr, 2),
        "comparator": comparator_label,
        "comparator_return_pct": round(comparator_return, 2),
        "implied_premium_bps": round(implied_bps, 1),
        "hold_years": hold,
        "illiquidity_hurdle_bps": [round(low, 1), round(high, 1)],
        "illiquidity_hurdle_label": hurdle_label,
        "verdict": verdict_for(implied_bps, low, high),
        "note": ("Beating the spread is necessary, not sufficient - dispersion means "
                 "the median fund underperforms the marketed top-quartile figure."),
    }

    # Debt types: also report the spread over the duration-matched Treasury (the
    # absolute credit + illiquidity premium, complementing the HYG credit spread).
    if "treasury" in spec:
        t_point = spec["treasury"]
        t_rate = TREASURY[t_point]
        result["treasury_floor"] = {
            "point": t_point,
            "rate_pct": t_rate,
            "spread_bps": round((net_irr - t_rate) * 100.0, 1),
            "note": (f"Net yield over the duration-matched {t_point} Treasury "
                     f"({t_rate:.2f}%) - the absolute credit + illiquidity spread."),
        }
    return result


# --------------------------------------------------------------------------- #
# I/O boundary (argument parsing, formatting, printing)
# --------------------------------------------------------------------------- #

def parse_args(argv):
    p = argparse.ArgumentParser(
        description="Compare a private deal's net-to-LP IRR to its public benchmark + illiquidity hurdle.",
        epilog=("Comparator figures are hardcoded from references/data snapshots "
                f"(LAST_UPDATED {LAST_UPDATED}); pass --benchmark-return to override with a "
                "current figure. Run with no arguments for the 05-benchmark-returns demo."),
    )
    # Omitted inputs fall back to DEFAULTS (the `05` demo) and are reported as ASSUMED.
    p.add_argument("--deal-type", type=str, default=None,
                   help=f"Private deal type (default if omitted, reported as ASSUMED: "
                        f"{DEFAULTS['deal_type']}). See --list-types for the full set.")
    p.add_argument("--net-irr", type=float, default=None,
                   help=f"Deal's net-to-LP IRR, %% (default if omitted, reported as "
                        f"ASSUMED: {DEFAULTS['net_irr']:g})")
    p.add_argument("--hold-years", type=float, default=None,
                   help=f"Lock-up / hold period in years (default if omitted, reported "
                        f"as ASSUMED: {DEFAULTS['hold_years']:g})")
    p.add_argument("--illiquidity-premium-assumed", type=float, default=None,
                   help="Override the hold-based illiquidity hurdle, %% (e.g. 2 = 200 bps)")
    p.add_argument("--benchmark-return", type=float, default=None,
                   help="Override the hardcoded comparator's trailing return, %%")
    p.add_argument("--format", choices=("text", "json"), default="text",
                   help="Output format (default: text)")
    p.add_argument("--json", action="store_const", dest="format", const="json",
                   help="Shorthand for --format json")
    p.add_argument("--list-types", action="store_true", help="List valid deal types and exit")
    p.add_argument("--self-check", action="store_true", help="Run internal checks against `05` and exit")
    return p.parse_args(argv)


def args_to_params(args):
    """Returns (params, assumed): params with omitted inputs filled from
    DEFAULTS, and the keys whose default was used."""
    params = {
        "illiquidity_premium_assumed": args.illiquidity_premium_assumed,
        "benchmark_return": args.benchmark_return,
    }
    assumed = []
    for key, default in DEFAULTS.items():
        value = getattr(args, key)
        if value is None:
            value = default
            assumed.append(key)
        params[key] = value
    return params, assumed


def validate_params(params):
    """Boundary check on a params dict. Returns (errors, warnings): errors are
    structurally invalid inputs (reject, exit 2); warnings are runnable but
    suspect, usually a unit slip (emit result, exit 1). The unknown-deal-type
    case stays handled by compute_comparison (ValueError -> exit 2); this covers
    the numeric domain. Kept out of the pure core."""
    errors, warnings = [], []

    # NaN compares False against every bound below, so it must be caught first.
    numeric = ("net_irr", "hold_years", "illiquidity_premium_assumed", "benchmark_return")
    bad = [k for k in numeric if params[k] is not None and not math.isfinite(params[k])]
    if bad:
        return [f"{k.replace('_', '-')} must be a finite number" for k in bad], []

    if params["hold_years"] <= 0:
        errors.append("hold-years must be greater than 0")
    if params["net_irr"] < -100:
        errors.append("net-irr below -100% is impossible")
    prem = params["illiquidity_premium_assumed"]
    if prem is not None and prem < 0:
        errors.append("illiquidity-premium-assumed cannot be negative")
    bench = params["benchmark_return"]
    if bench is not None and bench < -100:
        errors.append("benchmark-return below -100% is impossible")

    if params["net_irr"] > 100:
        warnings.append(f"net-irr {params['net_irr']:g}% is implausibly high - "
                        "check units (11.2 means 11.2%, not 0.112)")

    return errors, warnings


def format_human(r):
    lines = ["Benchmark comparison (screening, not underwriting)", "=" * 50]
    if r["assumed_inputs"]:
        assumed = ", ".join(f"{k.replace('_', '-')} {v:g}" if isinstance(v, float)
                            else f"{k.replace('_', '-')} {v}"
                            for k, v in r["assumed_inputs"].items())
        lines += [f"  ASSUMED (not supplied): {assumed}",
                  "  These are demo defaults, not the deal's terms - pass the deal's own values.",
                  ""]
    if r.get("variable"):
        lines += [f"  Deal type      {r['deal_type']}",
                  "  Comparator     none - variable class",
                  f"  Guidance       {r['guidance']}"]
        return "\n".join(lines)
    lines += [
        f"  Deal type            {r['deal_type']}",
        f"  Deal net IRR (LP)    {r['net_irr_pct']:>8.2f}%",
        f"  Comparator           {r['comparator']}",
        f"  Implied premium      {r['implied_premium_bps']:>8.0f} bps over comparator",
        f"  Lock-up              {r['hold_years']:g} yr  ->  illiquidity hurdle {r['illiquidity_hurdle_label']}",
        f"  Verdict              {r['verdict']}",
    ]
    if "treasury_floor" in r:
        t = r["treasury_floor"]
        lines.append(f"  Treasury floor       {t['spread_bps']:>8.0f} bps over the {t['point']} ({t['rate_pct']:.2f}%)")
    lines.append(f"  {r['note']}")
    return "\n".join(lines)


def _figures_in_05():
    """Read the figures this script hardcodes back out of `05`, so a refresh that
    updates one and not the other fails the self-check. Returns None when `05`
    isn't beside the script (e.g. the script was copied out on its own)."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        os.pardir, "references", "05-benchmark-returns.md")
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return None
    stamp = re.search(r"LAST_UPDATED: (\d{4}-\d{2}-\d{2})", text)
    ten_yr = {m.group(1): float(m.group(2)) for m in re.finditer(
        r"^\| ([A-Z]{2,5}) \| ~?(-?\d+(?:\.\d+)?)%", text, re.MULTILINE)}
    treasury = {m.group(1): float(m.group(2)) for m in re.finditer(
        r"(3mo|2yr|10yr) ≈ \*\*(\d+(?:\.\d+)?)%\*\*", text)}  # ≈ = approx-equal sign
    return {"last_updated": stamp.group(1) if stamp else None,
            "ten_yr": ten_yr, "treasury": treasury}


def _self_check():
    """Validate against `05-benchmark-returns.md` spread-table anchors."""
    ok = True

    def run(deal_type, net_irr, hold):
        return compute_comparison({
            "deal_type": deal_type, "net_irr": net_irr, "hold_years": hold,
            "illiquidity_premium_assumed": None, "benchmark_return": None,
        })

    # Multifamily value-add 13% net vs VNQ 4.92% -> ~808 bps, clears comfortably (7yr).
    r = run("multifamily-value-add", 13.0, 7.0)
    if not (800 <= r["implied_premium_bps"] <= 815 and "CLEARS comfortably" in r["verdict"]):
        ok = False
        print(f"FAIL mf value-add: {r['implied_premium_bps']} bps / {r['verdict']}")
    else:
        print(f"ok   mf value-add = {r['implied_premium_bps']:.0f} bps ({r['verdict']})")

    # Preferred equity 6% net vs PFF 3.00% -> ~300 bps, thin for a 5yr lock-up.
    r = run("preferred-equity", 6.0, 5.0)
    if not (295 <= r["implied_premium_bps"] <= 305 and "comfortably" not in r["verdict"]):
        ok = False
        print(f"FAIL pref equity: {r['implied_premium_bps']} bps / {r['verdict']}")
    else:
        print(f"ok   pref equity = {r['implied_premium_bps']:.0f} bps ({r['verdict']})")

    # Hard money 9% net: HYG spread ~417 bps and a duration-matched 3mo Treasury floor ~476 bps.
    r = run("hard-money", 9.0, 1.0)
    t = r.get("treasury_floor", {})
    if not (abs(r["implied_premium_bps"] - 417) <= 5 and abs(t.get("spread_bps", 0) - 476) <= 5):
        ok = False
        print(f"FAIL hard-money: {r['implied_premium_bps']} bps / treasury {t.get('spread_bps')}")
    else:
        print(f"ok   hard-money = {r['implied_premium_bps']:.0f} bps; treasury floor {t['spread_bps']:.0f} bps")

    # Variable class returns guidance, not a forced comparator.
    r = run("office", 12.0, 7.0)
    if not r.get("variable"):
        ok = False
        print("FAIL office should be a variable class")
    else:
        print("ok   office -> variable class (no forced comparator)")

    # Omitted inputs are reported as assumed; supplied ones are not.
    _, assumed = args_to_params(parse_args(["--deal-type", "hard-money"]))
    if set(assumed) != {"net_irr", "hold_years"}:
        ok = False
        print(f"FAIL assumed inputs: {sorted(assumed)}")
    else:
        print("ok   omitted net-irr / hold-years reported as assumed")

    # Input validation: a known-bad input must be rejected; a suspect one warned.
    base = {"deal_type": "multifamily-equity", "net_irr": 11.2, "hold_years": 5.0,
            "illiquidity_premium_assumed": None, "benchmark_return": None}
    for override, label in (({"hold_years": 0.0}, "hold-years 0"),
                            ({"net_irr": float("nan")}, "net-irr nan"),
                            ({"benchmark_return": float("inf")}, "benchmark-return inf")):
        if not validate_params({**base, **override})[0]:
            ok = False
            print(f"FAIL validator: {label} should error")
        else:
            print(f"ok   validator rejects {label}")
    if not validate_params({**base, "net_irr": 150.0})[1]:
        ok = False
        print("FAIL validator: net-irr 150 should warn")
    else:
        print("ok   validator warns on net-irr 150")

    # Drift guard: the hardcoded constants must match `05`, which is refreshed
    # from references/data/. A refresh that skips this file fails here.
    ref = _figures_in_05()
    if ref is None:
        print("skip drift guard - references/05-benchmark-returns.md not beside the script")
    else:
        mismatches = []
        if ref["last_updated"] != LAST_UPDATED:
            mismatches.append(f"LAST_UPDATED {LAST_UPDATED} vs 05 {ref['last_updated']}")
        for ticker, spec in COMPARATORS.items():
            if ref["ten_yr"].get(ticker) != spec["ten_yr"]:
                mismatches.append(f"{ticker} 10yr {spec['ten_yr']} vs 05 {ref['ten_yr'].get(ticker)}")
        for point, rate in TREASURY.items():
            if ref["treasury"].get(point) != rate:
                mismatches.append(f"Treasury {point} {rate} vs 05 {ref['treasury'].get(point)}")
        if mismatches:
            ok = False
            for m in mismatches:
                print(f"FAIL drift vs 05: {m}")
        else:
            print(f"ok   constants match 05 ({len(COMPARATORS)} comparators, "
                  f"{len(TREASURY)} Treasury points, LAST_UPDATED {LAST_UPDATED})")

    print("PASS" if ok else "FAILED")
    return 0 if ok else 1


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    args = parse_args(argv)
    if args.self_check:
        return _self_check()
    if args.list_types:
        print("Comparator-mapped types:")
        for dt in sorted(DEAL_TYPES):
            print(f"  {dt:<22} -> {DEAL_TYPES[dt]['comparator']}")
        print("Variable (no category comparator): " + ", ".join(sorted(VARIABLE_TYPES)))
        return 0
    params, assumed = args_to_params(args)
    errors, warnings = validate_params(params)
    if assumed:  # invented inputs deserve the same exit 1 as a suspected unit slip
        warnings.append("not supplied, demo defaults assumed: "
                        + ", ".join(k.replace("_", "-") for k in assumed))
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        return 2
    try:
        result = compute_comparison(params, assumed)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(format_human(result))
    return 1 if warnings else 0


if __name__ == "__main__":
    sys.exit(main())
