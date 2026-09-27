#!/usr/bin/env python3
"""Estimate net-to-LP IRR and total fee drag from a private deal's fee stack.

Screening tool, not underwriting. Given a gross deal IRR, the fee stack, the
hold period, and the promote terms, it estimates the LP's net IRR and decomposes
the gross-to-net drag into recurring fees, one-time fees, and promote.

The model mirrors `references/02-fee-stack-library.md` (the "Total-drag
framework"), which treats drag *additively* in annual basis points:

    net LP IRR  ~=  gross IRR
                  - recurring fees   (annual %, paid every year)
                  - one-time fees    (% spread across the hold: fee / hold_years)
                  - promote          (waterfall on profit, annualized below)

Two deliberate simplifications, consistent with `02`'s screening stance:
  * Drag is additive. Fees and promote are each computed against the gross
    return rather than compounding on one another's residual. This is how `02`'s
    worked examples are built; it slightly overstates total drag versus a full
    sequential waterfall, which is the conservative direction for screening.
  * Promote uses a single bullet distribution at exit (no J-curve / interim
    distribution schedule). Distribution timing is a separate LP risk surfaced
    by the skill (`03` -> GEN-11), not a fee-drag input.

For the precise per-deal answer, replace the inputs with the real fee schedule
and waterfall from the PPM. Omitted inputs fall back to the `02` worked example
and are reported as ASSUMED, so pass 0 for any fee or carry the deal doesn't
charge. stdlib-only by design (no pip installs).
"""

import argparse
import json
import math
import sys


# --------------------------------------------------------------------------- #
# Data (config only - no logic)
# --------------------------------------------------------------------------- #

# Inputs the caller omits fall back to these, which reproduce the `02` worked
# example so a bare run is a live demo. A non-zero fallback is a number the deal
# never disclosed, so every one used is reported as ASSUMED - never silently
# folded into the drag. Omitted zero-default fees are simply not charged.
DEFAULTS = {
    "gross_irr": 15.0,
    "hold_years": 7.0,
    "carry": 20.0,
    "hurdle": 8.0,
    "catch_up": 100.0,
    "acquisition_fee": 2.0,
    "disposition_fee": 1.0,
    "loan_placement_fee": 0.0,
    "refinance_fee": 0.0,
    "mgmt_fee": 1.5,
    "admin_fee": 0.3,
    "servicing_fee": 0.0,
    "fund_mgmt_fee": 0.0,
}


# --------------------------------------------------------------------------- #
# Pure calculation core (same input -> same output, no side effects)
# --------------------------------------------------------------------------- #

def recurring_drag_bps(annual_fee_pct):
    """Annual drag in bps from recurring fees. A fee charged every year drags
    the IRR by its own rate: 1.5%/yr == 150 bps/yr."""
    return annual_fee_pct * 100.0


def one_time_drag_bps(one_time_fee_pct, hold_years):
    """Annual drag in bps from one-time fees, spread across the hold. A 2%
    one-time fee over 7 years is ~28.6 bps/yr; over 3 years, ~66.7 bps/yr."""
    if hold_years <= 0:
        return 0.0
    return (one_time_fee_pct / hold_years) * 100.0


def promote_drag(gross_irr_pct, hurdle_pct, carry_pct, hold_years, catch_up_pct=100.0):
    """Promote drag in bps via a bullet-exit waterfall on $1 of LP capital.

    Tiers: (1) return of capital + a simple preferred-return accrual to the LP,
    (2) a GP catch-up toward its carry share of distributed profit, scaled by
    `catch_up_pct`, (3) residual profit split (1-carry)/carry LP/GP.

    Returns (drag_bps, detail) where detail carries the LP/GP profit split and
    whether the deal clears the hurdle. Note: with a 100% catch-up the pref
    governs distribution *timing*, not the final split — the GP still ends with
    exactly `carry` of total profit. The pref only changes the LP's share when
    the catch-up is below 100%.

    "Clears the hurdle" is read off the waterfall itself: total profit exceeds
    the simple pref accrual. Comparing the compound gross IRR to the pref *rate*
    would disagree with the promote actually paid - at 8% gross over an 8% simple
    pref for 7 years, profit (71%) still exceeds the accrual (56%).
    """
    g = gross_irr_pct / 100.0
    pref = hurdle_pct / 100.0
    carry = carry_pct / 100.0
    catch_up = catch_up_pct / 100.0

    total_profit = (1.0 + g) ** hold_years - 1.0 if hold_years > 0 else 0.0
    pref_accrual = pref * hold_years            # simple pref on $1 (per `02`)
    clears = hold_years > 0 and total_profit > pref_accrual

    detail = {
        "clears_hurdle": clears,
        "gp_profit_share_pct": 0.0,
        "lp_profit_share_pct": 100.0,
        "note": "",
    }

    if not clears:
        detail["note"] = (f"Profit does not exceed the simple {hurdle_pct:g}% pref accrual - "
                          "no promote is earned, but the LP may not realize the full pref.")
        return 0.0, detail
    if carry <= 0.0:
        detail["note"] = "No carry - the LP keeps all profit."
        return 0.0, detail

    profit_above_pref = total_profit - pref_accrual

    # Full catch-up target: the GP take that makes GP == carry of (pref + take).
    if carry < 1.0:
        full_catch_up = carry * pref_accrual / (1.0 - carry)
    else:
        full_catch_up = profit_above_pref
    catch_up_target = catch_up * full_catch_up

    catch_up_taken = min(catch_up_target, profit_above_pref)
    residual = profit_above_pref - catch_up_taken
    gp_profit = catch_up_taken + carry * residual

    lp_terminal = 1.0 + (total_profit - gp_profit)
    lp_net_irr = lp_terminal ** (1.0 / hold_years) - 1.0
    drag_bps = max(0.0, (g - lp_net_irr) * 10000.0)  # promote drag is never negative

    detail["gp_profit_share_pct"] = round(gp_profit / total_profit * 100.0, 2)
    detail["lp_profit_share_pct"] = round((1.0 - gp_profit / total_profit) * 100.0, 2)
    if g <= pref:
        detail["note"] = (f"Gross IRR is at or below the {hurdle_pct:g}% pref rate, but the pref "
                          "is simple (non-compounding), so profit still exceeds the accrual "
                          "and promote is earned. A compounding pref would change this.")
    elif catch_up_pct >= 100.0:
        detail["note"] = (f"With a 100% catch-up, the {hurdle_pct:g}% pref governs "
                          "distribution timing, not the final split - the GP still "
                          f"takes {carry_pct:g}% of total profit.")
    else:
        detail["note"] = (f"Catch-up below 100% lets the {hurdle_pct:g}% pref lift the "
                          "LP's share above the residual split.")
    return drag_bps, detail


def compute_fee_drag(params, assumed=()):
    """Orchestrate the drag estimate from a params dict. Pure: returns a result
    dict, prints nothing. `assumed` names the params that fell back to DEFAULTS;
    they are carried into the result so no invented input goes unreported."""
    hold = params["hold_years"]

    recurring_pct = (params["mgmt_fee"] + params["admin_fee"]
                     + params["servicing_fee"] + params["fund_mgmt_fee"])
    one_time_pct = (params["acquisition_fee"] + params["disposition_fee"]
                    + params["loan_placement_fee"] + params["refinance_fee"])

    recurring_bps = recurring_drag_bps(recurring_pct)
    one_time_bps = one_time_drag_bps(one_time_pct, hold)
    promote_bps, carry_detail = promote_drag(
        params["gross_irr"], params["hurdle"], params["carry"], hold, params["catch_up"]
    )

    total_bps = recurring_bps + one_time_bps + promote_bps
    net_irr = params["gross_irr"] - total_bps / 100.0

    return {
        "inputs": params,
        "assumed_inputs": {k: params[k] for k in assumed},
        "gross_irr_pct": round(params["gross_irr"], 4),
        "net_irr_pct": round(net_irr, 2),
        "total_drag_bps": round(total_bps, 1),
        "total_drag_pct": round(total_bps / 100.0, 2),
        "drag_breakdown_bps": {
            "recurring_fees": round(recurring_bps, 1),
            "one_time_fees": round(one_time_bps, 1),
            "promote": round(promote_bps, 1),
        },
        "carry_analysis": carry_detail,
    }


# --------------------------------------------------------------------------- #
# I/O boundary (argument parsing, formatting, printing)
# --------------------------------------------------------------------------- #

def parse_args(argv):
    p = argparse.ArgumentParser(
        description="Estimate net-to-LP IRR and gross-to-net fee drag for a private deal.",
        epilog="Run with no arguments to reproduce the 02-fee-stack-library worked "
               "example (15 percent gross multifamily, 7-year hold, full stack, ~10.6 percent net).",
    )
    # Omitted inputs fall back to DEFAULTS (the `02` worked example) and are
    # reported as ASSUMED. Pass 0 explicitly for a fee or carry the deal lacks.
    def num(flag, help_text):
        d = DEFAULTS[flag.lstrip("-").replace("-", "_")]
        note = f"reported as ASSUMED: {d:g}" if d else "0, not charged"
        p.add_argument(flag, type=float, default=None,
                       help=f"{help_text} (default if omitted: {note})")
    num("--gross-irr", "Gross deal IRR, %%")
    num("--hold-years", "Hold period in years")
    num("--carry", "GP promote / carry, %%; 0 if the deal has none")
    num("--hurdle", "Preferred return / hurdle, %%")
    num("--catch-up", "GP catch-up, %% (100 = full catch-up to carry share; 0 = none)")
    # One-time fees
    num("--acquisition-fee", "One-time, %%")
    num("--disposition-fee", "One-time, %%")
    num("--loan-placement-fee", "One-time, %%")
    num("--refinance-fee", "One-time, %%")
    # Recurring (annual) fees
    num("--mgmt-fee", "Annual asset-mgmt fee, %%")
    num("--admin-fee", "Annual admin/IR fee, %%")
    num("--servicing-fee", "Annual servicing fee, %%")
    num("--fund-mgmt-fee", "Annual fund mgmt fee, %%")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of a human-readable summary")
    p.add_argument("--self-check", action="store_true", help="Run internal checks against `02` and exit")
    return p.parse_args(argv)


def args_to_params(args):
    """Returns (params, assumed): params with omitted inputs filled from
    DEFAULTS, and the keys whose non-zero default was used."""
    params, assumed = {}, []
    for key, default in DEFAULTS.items():
        value = getattr(args, key)
        if value is None:
            value = default
            if default != 0:
                assumed.append(key)
        params[key] = value
    return params, assumed


def validate_params(params):
    """Boundary check on a params dict. Returns (errors, warnings): errors are
    structurally invalid inputs the drag math can't represent (reject, exit 2);
    warnings are runnable but suspect, usually a unit slip (emit result, exit 1).
    Kept out of the pure core so the calculation stays side-effect-free.
    A screening tool that silently accepts a negative fee (LP 'earns' the fee) or
    a zero hold (no drag reported) is worse than one that refuses and says why."""
    errors, warnings = [], []

    fee_fields = ("mgmt_fee", "admin_fee", "servicing_fee", "fund_mgmt_fee",
                  "acquisition_fee", "disposition_fee", "loan_placement_fee",
                  "refinance_fee")

    # NaN compares False against every bound below, so it must be caught first.
    bad = [k for k, v in params.items() if not math.isfinite(v)]
    if bad:
        return [f"{k.replace('_', '-')} must be a finite number" for k in bad], []

    if params["hold_years"] <= 0:
        errors.append("hold-years must be greater than 0")
    for f in fee_fields:
        if params[f] < 0:
            errors.append(f"{f.replace('_', '-')} cannot be negative (fees are a % >= 0)")
    if not 0 <= params["carry"] <= 100:
        errors.append("carry must be between 0 and 100 (%)")
    if params["hurdle"] < 0:
        errors.append("hurdle cannot be negative")
    if not 0 <= params["catch_up"] <= 100:
        errors.append("catch-up must be between 0 and 100 (%)")
    if params["gross_irr"] < -100:
        errors.append("gross-irr below -100% is impossible (terminal value can't go below 0)")

    # Warnings: runnable, but the numbers look like a unit slip.
    if params["gross_irr"] > 100:
        warnings.append(f"gross-irr {params['gross_irr']:g}% is implausibly high - "
                        "check units (15 means 15%, not 0.15)")
    for f in ("mgmt_fee", "carry"):
        if 0 < params[f] < 0.1:
            warnings.append(f"{f.replace('_', '-')} {params[f]:g} looks like a fraction - "
                            "fees are in percent (1.5 means 1.5%)")
    total_fee = sum(params[f] for f in fee_fields)
    if total_fee > 50:
        warnings.append(f"total fee load {total_fee:g}% is very high - verify the fee inputs")

    return errors, warnings


def format_human(r):
    b = r["drag_breakdown_bps"]
    c = r["carry_analysis"]
    lines = [
        "Fee-drag estimate (screening, not underwriting)",
        "=" * 48,
    ]
    if r["assumed_inputs"]:
        assumed = ", ".join(f"{k.replace('_', '-')} {v:g}" for k, v in r["assumed_inputs"].items())
        lines += [f"  ASSUMED (not supplied): {assumed}",
                  "  These are demo defaults, not disclosed terms - pass 0 for any the deal lacks.",
                  ""]
    lines += [
        f"  Gross deal IRR        {r['gross_irr_pct']:>8.2f}%",
        f"  Estimated net LP IRR  {r['net_irr_pct']:>8.2f}%",
        f"  Total fee drag        {r['total_drag_pct']:>8.2f}%  ({r['total_drag_bps']:.0f} bps/yr)",
        "",
        "  Drag breakdown (bps/yr)",
        f"    Recurring fees      {b['recurring_fees']:>8.1f}",
        f"    One-time fees       {b['one_time_fees']:>8.1f}",
        f"    Promote             {b['promote']:>8.1f}",
        "",
        "  Carry / waterfall",
        f"    Clears hurdle       {'yes' if c['clears_hurdle'] else 'no':>8}",
        f"    LP share of profit  {c['lp_profit_share_pct']:>7.1f}%",
        f"    GP share of profit  {c['gp_profit_share_pct']:>7.1f}%",
        f"    {c['note']}",
    ]
    return "\n".join(lines)


def _self_check():
    """Validate the model against `02-fee-stack-library.md` anchor points."""
    ok = True

    # Full worked example (total-drag section): ~10.5-11% net.
    full = compute_fee_drag(*args_to_params(parse_args([])))
    if not (10.4 <= full["net_irr_pct"] <= 11.0):
        ok = False
        print(f"FAIL worked example: net {full['net_irr_pct']}% not in 10.4-11.0%")
    else:
        print(f"ok   worked example net IRR = {full['net_irr_pct']}% (expected ~10.5-11%)")

    # Promote-only anchors from the waterfall example: ~150 bps @ 12%, ~200 bps @ 15%.
    for gross, lo, hi in ((12.0, 150.0, 220.0), (15.0, 180.0, 250.0)):
        bps, _ = promote_drag(gross, 8.0, 20.0, 7.0, 100.0)
        if not (lo <= bps <= hi):
            ok = False
            print(f"FAIL promote @ {gross:g}%: {bps:.0f} bps not in {lo:.0f}-{hi:.0f}")
        else:
            print(f"ok   promote @ {gross:g}% gross = {bps:.0f} bps")

    # Hurdle flag agrees with the promote actually paid, on both sides of the accrual.
    for gross, hurdle, hold, want_clear in ((8.0, 8.0, 7.0, True), (5.0, 8.0, 3.0, False)):
        bps, detail = promote_drag(gross, hurdle, 20.0, hold, 100.0)
        if detail["clears_hurdle"] != want_clear or (bps > 0) != want_clear:
            ok = False
            print(f"FAIL hurdle flag @ {gross:g}/{hurdle:g}/{hold:g}yr: "
                  f"clears={detail['clears_hurdle']} promote={bps:.0f} bps")
        else:
            print(f"ok   hurdle flag @ {gross:g}% gross / {hurdle:g}% pref / {hold:g}yr "
                  f"= clears {detail['clears_hurdle']}, promote {bps:.0f} bps")

    # A sparse call reports every non-zero default it used; explicit inputs are not assumed.
    _, assumed = args_to_params(parse_args(
        ["--gross-irr", "10", "--hold-years", "1", "--servicing-fee", "1"]))
    want = {"carry", "hurdle", "catch_up", "acquisition_fee", "disposition_fee",
            "mgmt_fee", "admin_fee"}
    if set(assumed) != want:
        ok = False
        print(f"FAIL assumed inputs: {sorted(assumed)}")
    else:
        print(f"ok   sparse call reports {len(assumed)} assumed inputs")

    # Input validation: a known-bad input must be rejected; a suspect one warned.
    for argv, label in ((["--hold-years", "0"], "hold-years 0"),
                        (["--gross-irr", "nan"], "gross-irr nan"),
                        (["--mgmt-fee", "inf"], "mgmt-fee inf")):
        if not validate_params(args_to_params(parse_args(argv))[0])[0]:
            ok = False
            print(f"FAIL validator: {label} should error")
        else:
            print(f"ok   validator rejects {label}")
    suspect, _ = args_to_params(parse_args(["--gross-irr", "150"]))
    if not validate_params(suspect)[1]:
        ok = False
        print("FAIL validator: gross-irr 150 should warn")
    else:
        print("ok   validator warns on gross-irr 150")

    print("PASS" if ok else "FAILED")
    return 0 if ok else 1


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    args = parse_args(argv)
    if args.self_check:
        return _self_check()
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
    result = compute_fee_drag(params, assumed)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_human(result))
    return 1 if warnings else 0


if __name__ == "__main__":
    sys.exit(main())
