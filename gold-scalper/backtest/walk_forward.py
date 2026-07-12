"""Walk-forward validation — rolling out-of-sample windows over the fleet.

Usage:
    python walk_forward.py --csv path/to/xauusd_m1.csv \
        [--window-days 30] [--step-days 7] [--min-windows 4] \
        [--equity 10000] [--spread 300] [--json out.json] \
        [--strategies name1,name2]

Our strategies have FIXED parameters — there is no optimization step — so
every window is pure out-of-sample: this is a consistency test, not an
optimize-then-validate walk-forward. Window k covers
[start + k*step, start + k*step + window). Each window gets a fresh
SimBroker, fresh strategy instances, and a fresh RiskManager state file in
its own tempdir, so no state bleeds between windows.

Reuses run_backtest.py's load_csv() and run() (the per-bar engine loop)
unchanged; only the slicing, aggregation, and verdict logic live here.

Verdicts per strategy:
  ROBUST            >= min-windows windows with trades AND >= 60% of those
                    profitable AND pooled PF > 1.1
  NEGATIVE          pooled PF < 0.9
  INCONSISTENT      traded, but fails the consistency bar
  INSUFFICIENT-DATA fewer than min-windows windows with >= 5 trades each
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import sys
import tempfile

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from core.risk import RiskConfig, RiskManager                    # noqa: E402
from backtest.sim_broker import SimBroker                        # noqa: E402
from backtest.run_backtest import load_csv, run, ALL_STRATEGIES  # noqa: E402

MIN_TRADES_PER_WINDOW = 5      # a window "counts" for the data gate at >= 5
VERDICT_RANK = {"NEGATIVE": 0, "INCONSISTENT": 1,
                "INSUFFICIENT-DATA": 2, "ROBUST": 3}


def make_windows(index: pd.DatetimeIndex, window_days: int,
                 step_days: int) -> list[tuple[pd.Timestamp, pd.Timestamp]]:
    """Rolling out-of-sample windows: [start + k*step, start + k*step + window)."""
    start, end = index[0], index[-1]
    window = pd.Timedelta(days=window_days)
    step = pd.Timedelta(days=step_days)
    out, k = [], 0
    while True:
        ws = start + k * step
        we = ws + window
        if we > end + pd.Timedelta(minutes=1):     # only full windows
            break
        out.append((ws, we))
        k += 1
    return out


def run_window(m1: pd.DataFrame, names: set[str], equity: float,
               spread: float) -> tuple[list, SimBroker]:
    """One fully isolated backtest: fresh broker, strategies, risk state."""
    strategies = [cls() for cls in ALL_STRATEGIES]
    if names:
        strategies = [s for s in strategies if s.name in names]
    sim = SimBroker("XAUUSD", m1, spread_points=spread, initial_equity=equity)
    with tempfile.TemporaryDirectory() as td:
        risk = RiskManager(RiskConfig(), pathlib.Path(td) / "risk_state.json")
        run(sim, strategies, risk)
    return strategies, sim


def window_rows(sim: SimBroker, strategies: list) -> dict[str, dict]:
    """Per-strategy stats for one window, keyed by strategy name."""
    rows = {}
    for idx, strat in enumerate(strategies):
        magic = sim.magic_for(idx)
        trades = [t for t in sim.trade_log if t["magic"] == magic]
        gp = sum(t["pnl"] for t in trades if t["pnl"] > 0)
        gl = sum(t["pnl"] for t in trades if t["pnl"] <= 0)
        rows[strat.name] = {"trades": len(trades),
                            "wins": sum(1 for t in trades if t["pnl"] > 0),
                            "pnl": gp + gl,
                            "gross_profit": gp, "gross_loss": gl}
    return rows


def aggregate(name: str, per_window: list[dict], min_windows: int) -> dict:
    """Roll one strategy's window rows up into stats + verdict."""
    traded = [w for w in per_window if w["trades"] > 0]
    pnls = [w["pnl"] for w in traded]
    profitable = sum(1 for p in pnls if p > 0)
    pct_profitable = 100.0 * profitable / len(traded) if traded else 0.0
    gp = sum(w["gross_profit"] for w in per_window)
    gl = sum(w["gross_loss"] for w in per_window)
    pooled_pf = gp / abs(gl) if gl else (float("inf") if gp else 0.0)
    windows_5plus = sum(1 for w in per_window
                        if w["trades"] >= MIN_TRADES_PER_WINDOW)

    if windows_5plus < min_windows:
        verdict = "INSUFFICIENT-DATA"
    elif pooled_pf < 0.9:
        verdict = "NEGATIVE"
    elif (len(traded) >= min_windows and pct_profitable >= 60.0
          and pooled_pf > 1.1):
        verdict = "ROBUST"
    else:
        verdict = "INCONSISTENT"

    return {"strategy": name,
            "windows_traded": len(traded),
            "windows_5plus_trades": windows_5plus,
            "pct_windows_profitable": pct_profitable,
            "mean_window_pnl": statistics.mean(pnls) if pnls else 0.0,
            "median_window_pnl": statistics.median(pnls) if pnls else 0.0,
            "worst_window_pnl": min(pnls) if pnls else 0.0,
            "stdev_window_pnl": statistics.stdev(pnls) if len(pnls) > 1 else 0.0,
            "total_trades": sum(w["trades"] for w in per_window),
            "pooled_pf": pooled_pf,
            "verdict": verdict}


def print_table(rows: list[dict]) -> None:
    hdr = f"{'strategy':<28}{'wins':>5}{'w5+':>5}{'%prof':>7}{'meanPnL':>10}" \
          f"{'medPnL':>10}{'worst':>10}{'stdev':>10}{'trades':>8}" \
          f"{'PF':>7}  {'verdict':<17}"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        pf = "inf" if r["pooled_pf"] == float("inf") else f"{r['pooled_pf']:.2f}"
        print(f"{r['strategy']:<28}{r['windows_traded']:>5}"
              f"{r['windows_5plus_trades']:>5}"
              f"{r['pct_windows_profitable']:>6.0f}%"
              f"{r['mean_window_pnl']:>10.2f}{r['median_window_pnl']:>10.2f}"
              f"{r['worst_window_pnl']:>10.2f}{r['stdev_window_pnl']:>10.2f}"
              f"{r['total_trades']:>8}{pf:>7}  {r['verdict']:<17}")
    print("\n(wins = windows with >=1 trade, w5+ = windows with >=5 trades, "
          "%prof = of traded windows)")


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Walk-forward validation over rolling out-of-sample windows")
    ap.add_argument("--csv", required=True,
                    help="M1 OHLCV CSV (time,open,high,low,close,tick_volume)")
    ap.add_argument("--window-days", type=int, default=30)
    ap.add_argument("--step-days", type=int, default=7)
    ap.add_argument("--min-windows", type=int, default=4,
                    help="windows with >=5 trades required to escape "
                         "INSUFFICIENT-DATA; also the ROBUST floor")
    ap.add_argument("--equity", type=float, default=10_000)
    ap.add_argument("--spread", type=float, default=300, help="spread in points")
    ap.add_argument("--json", default="",
                    help="dump full per-window detail to this file")
    ap.add_argument("--strategies", default="",
                    help="comma-separated strategy names (default: all)")
    args = ap.parse_args()

    m1 = load_csv(args.csv)

    all_names = {cls.name for cls in ALL_STRATEGIES}
    wanted: set[str] = set()
    if args.strategies:
        wanted = {n.strip() for n in args.strategies.split(",") if n.strip()}
        unknown = wanted - all_names
        if unknown:
            print(f"ERROR: unknown strategies: {sorted(unknown)}\n"
                  f"available: {sorted(all_names)}", file=sys.stderr)
            sys.exit(1)
    strat_names = sorted(wanted) if wanted else sorted(all_names)

    windows = make_windows(m1.index, args.window_days, args.step_days)
    if not windows:
        print(f"ERROR: data span {m1.index[0]} -> {m1.index[-1]} is shorter "
              f"than one {args.window_days}-day window", file=sys.stderr)
        sys.exit(1)

    print(f"Walk-forward validation: {len(windows)} rolling windows of "
          f"{args.window_days}d, step {args.step_days}d, over "
          f"{m1.index[0]} -> {m1.index[-1]} ({len(m1)} M1 bars)")
    print("All strategy parameters are FIXED (no optimization step): every "
          "window is pure out-of-sample.\n")

    per_window_detail: list[dict] = []
    per_strategy: dict[str, list[dict]] = {n: [] for n in strat_names}

    for k, (ws, we) in enumerate(windows):
        chunk = m1[(m1.index >= ws) & (m1.index < we)]
        if len(chunk) < 10:                      # e.g. all-weekend window
            print(f"[window {k + 1}/{len(windows)}] {ws.date()} -> {we.date()}"
                  f"  SKIPPED ({len(chunk)} bars)")
            continue
        strategies, sim = run_window(chunk, wanted, args.equity, args.spread)
        rows = window_rows(sim, strategies)
        for name, row in rows.items():
            per_strategy[name].append(row)
        fleet_trades = sum(r["trades"] for r in rows.values())
        fleet_pnl = sum(r["pnl"] for r in rows.values())
        print(f"[window {k + 1}/{len(windows)}] {ws.date()} -> {we.date()}"
              f"  bars={len(chunk)}  fleet trades={fleet_trades}"
              f"  fleet pnl={fleet_pnl:+.2f}")
        per_window_detail.append({
            "window": k + 1, "start": str(ws), "end": str(we),
            "bars": len(chunk), "fleet_trades": fleet_trades,
            "fleet_pnl": fleet_pnl, "final_equity": sim.equity(),
            "strategies": rows})

    agg = [aggregate(n, per_strategy[n], args.min_windows)
           for n in strat_names]
    agg.sort(key=lambda r: (VERDICT_RANK[r["verdict"]],
                            r["pooled_pf"], r["mean_window_pnl"]))

    print()
    print_table(agg)
    robust = sum(1 for r in agg if r["verdict"] == "ROBUST")
    print(f"\n{robust} of {len(agg)} strategies clear the walk-forward gate")

    if args.json:
        payload = {"config": {"csv": args.csv,
                              "window_days": args.window_days,
                              "step_days": args.step_days,
                              "min_windows": args.min_windows,
                              "equity": args.equity, "spread": args.spread,
                              "strategies": strat_names},
                   "data_span": [str(m1.index[0]), str(m1.index[-1])],
                   "windows": per_window_detail,
                   "aggregate": agg,
                   "robust_count": robust}
        pathlib.Path(args.json).write_text(
            json.dumps(payload, indent=2, default=str))
        print(f"wrote {args.json}")


if __name__ == "__main__":
    main()
