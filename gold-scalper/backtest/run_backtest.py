"""Backtest runner — replays M1 history through the strategy fleet.

Usage:
    python run_backtest.py --csv path/to/xauusd_m1.csv \
        [--strategies name1,name2] [--equity 10000] [--spread 300] [--json out.json]

Replicates core/engine.py's per-bar dispatch inline (the live engine has a
sleep/signal loop that makes no sense against replayed data): each SimBroker
step, every strategy whose primary-timeframe bar just closed gets on_bar()
while flat or manage_position() while holding, every Signal is sized through
the RiskManager, and pending_sl_move is honored exactly as in the engine.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import tempfile

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from core.risk import RiskConfig, RiskManager          # noqa: E402
from core.strategy_base import MarketContext, Side     # noqa: E402
from backtest.sim_broker import SimBroker              # noqa: E402

try:
    from strategies import ALL_STRATEGIES
except ImportError as e:
    print(f"ERROR: cannot import strategy registry: {e}\n"
          f"A module under strategies/ is missing or broken "
          f"(strategies/__init__.py imports momentum, mean_reversion, "
          f"microstructure, indicator_hybrid). Fix or stub it, then rerun.",
          file=sys.stderr)
    sys.exit(1)


def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "volume" in df.columns and "tick_volume" not in df.columns:
        df = df.rename(columns={"volume": "tick_volume"})
    need = {"time", "open", "high", "low", "close", "tick_volume"}
    missing = need - set(df.columns)
    if missing:
        print(f"ERROR: CSV missing columns: {sorted(missing)}", file=sys.stderr)
        sys.exit(1)
    df["time"] = pd.to_datetime(df["time"], utc=True)
    return df.set_index("time").sort_index()


def run(sim: SimBroker, strategies: list, risk: RiskManager) -> None:
    last_bar: dict[str, object] = {}
    errors: dict[str, int] = {}
    disabled: set[str] = set()
    bars_held: dict[int, tuple[int, int]] = {}      # magic -> (ticket, bars_held)

    while not sim.done:
        sim.step()                                   # advance bar, resolve SL/TP
        now = sim.now.to_pydatetime()
        equity = sim.equity()
        risk.roll(now, equity)
        allowed, why = risk.trading_allowed(now, equity)
        if not allowed:
            for pos in sim.open_positions():
                sim.close_position(pos, "risk_halt")
            continue

        for idx, strat in enumerate(strategies):
            if strat.name in disabled:
                continue
            tf = strat.primary_timeframe
            df = sim.bars(tf, strat.lookback_bars)
            if len(df) < strat.lookback_bars:
                continue                             # not enough history yet
            last = df.index[-1]
            if last_bar.get(strat.name) == last:
                continue                             # no new closed bar
            last_bar[strat.name] = last

            magic = sim.magic_for(idx)
            try:
                t = sim.tick()
                pos = sim.position_for_magic(magic)
                if pos is not None:                  # restore bars-held counter
                    tkt, held = bars_held.get(magic, (pos.ticket, 0))
                    held = held + 1 if tkt == pos.ticket else 1
                    bars_held[magic] = (pos.ticket, held)
                    pos.bars_held = held
                ctx = MarketContext(
                    symbol=sim.symbol, now=now, bid=t.bid, ask=t.ask,
                    spread_points=sim.spread_points(),
                    bars={f: sim.bars(f, strat.lookback_bars)
                          for f in (tf, *strat.extra_timeframes)},
                    aux={}, position=pos)

                if pos is not None:
                    strat.pending_sl_move = None
                    reason = strat.manage_position(ctx)
                    if reason is not None:
                        sim.close_position(pos, reason.value)
                        bars_held.pop(magic, None)
                    elif strat.pending_sl_move is not None:
                        sim.modify_sl(pos, strat.pending_sl_move)
                elif (strat.in_session(now)
                      and ctx.spread_points <= strat.max_spread_points):
                    sig = strat.on_bar(ctx)
                    if sig is not None:
                        sig.comment = sig.comment or strat.name
                        info = sim.info
                        lots = risk.size_signal(
                            sig, equity=equity,
                            requested_risk_pct=strat.default_risk_pct,
                            tick_value=info.trade_tick_value,
                            tick_size=info.trade_tick_size,
                            volume_min=info.volume_min,
                            volume_step=info.volume_step,
                            volume_max=info.volume_max,
                            open_positions=sim.open_positions())
                        if lots is not None:
                            strat._time_stop_bars = sig.time_stop_bars
                            sim.market_order(sig, lots, magic)
                            bars_held[magic] = (sim.position_for_magic(magic).ticket, 0)
                errors[strat.name] = 0
            except Exception as e:
                errors[strat.name] = errors.get(strat.name, 0) + 1
                print(f"[warn] {strat.name} error "
                      f"({errors[strat.name]}/3): {e}", file=sys.stderr)
                if errors[strat.name] >= 3:
                    disabled.add(strat.name)
                    print(f"[warn] DISABLED {strat.name}: 3 consecutive errors",
                          file=sys.stderr)

    for pos in sim.open_positions():                 # flatten at end of data
        sim.close_position(pos, "end_of_data")


def scorecard(sim: SimBroker, strategies: list) -> list[dict]:
    by_magic = {sim.magic_for(i): s.name for i, s in enumerate(strategies)}
    rows = []
    for magic, name in by_magic.items():
        trades = sorted((t for t in sim.trade_log if t["magic"] == magic),
                        key=lambda t: t["close_time"])
        rows.append(_score_row(name, trades))
    rows.append(_score_row("TOTAL", sorted(sim.trade_log,
                                           key=lambda t: t["close_time"])))
    return rows


def _score_row(name: str, trades: list[dict]) -> dict:
    wins = [t for t in trades if t["pnl"] > 0]
    gp = sum(t["pnl"] for t in wins)
    gl = sum(t["pnl"] for t in trades if t["pnl"] <= 0)
    cum = peak = max_dd = 0.0
    for t in trades:
        cum += t["pnl"]
        peak = max(peak, cum)
        max_dd = max(max_dd, peak - cum)
    n = len(trades)
    return {"strategy": name, "trades": n, "wins": len(wins),
            "win_pct": 100.0 * len(wins) / n if n else 0.0,
            "gross_profit": gp, "gross_loss": gl,
            "profit_factor": gp / abs(gl) if gl else (float("inf") if gp else 0.0),
            "expectancy": (gp + gl) / n if n else 0.0,
            "max_drawdown": max_dd}


def print_table(rows: list[dict]) -> None:
    hdr = f"{'strategy':<28}{'trades':>7}{'wins':>6}{'win%':>7}" \
          f"{'gross P':>11}{'gross L':>11}{'PF':>7}{'expect':>9}{'maxDD':>10}"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        pf = f"{r['profit_factor']:.2f}" if r["profit_factor"] != float("inf") else "inf"
        print(f"{r['strategy']:<28}{r['trades']:>7}{r['wins']:>6}"
              f"{r['win_pct']:>6.1f}%{r['gross_profit']:>11.2f}"
              f"{r['gross_loss']:>11.2f}{pf:>7}{r['expectancy']:>9.2f}"
              f"{r['max_drawdown']:>10.2f}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Replay M1 history through the fleet")
    ap.add_argument("--csv", required=True, help="M1 OHLCV CSV (time,open,high,low,close,tick_volume)")
    ap.add_argument("--strategies", default="", help="comma-separated strategy names to run (default: all)")
    ap.add_argument("--equity", type=float, default=10_000)
    ap.add_argument("--spread", type=float, default=300, help="spread in points")
    ap.add_argument("--json", default="", help="also dump scorecard + trade log to this file")
    args = ap.parse_args()

    m1 = load_csv(args.csv)
    strategies = [cls() for cls in ALL_STRATEGIES]
    if args.strategies:
        wanted = {n.strip() for n in args.strategies.split(",") if n.strip()}
        unknown = wanted - {s.name for s in strategies}
        if unknown:
            print(f"ERROR: unknown strategies: {sorted(unknown)}\n"
                  f"available: {sorted(s.name for s in strategies)}", file=sys.stderr)
            sys.exit(1)
        strategies = [s for s in strategies if s.name in wanted]

    sim = SimBroker("XAUUSD", m1, spread_points=args.spread,
                    initial_equity=args.equity)
    with tempfile.TemporaryDirectory() as td:
        risk = RiskManager(RiskConfig(),
                           pathlib.Path(td) / "risk_state.json")
        run(sim, strategies, risk)

    rows = scorecard(sim, strategies)
    print(f"\nBacktest {m1.index[0]} -> {m1.index[-1]} "
          f"({len(m1)} M1 bars), final equity {sim.equity():.2f}\n")
    print_table(rows)

    if args.json:
        payload = {"scorecard": rows,
                   "final_equity": sim.equity(),
                   "trades": [{**t, "open_time": str(t["open_time"]),
                               "close_time": str(t["close_time"])}
                              for t in sim.trade_log]}
        pathlib.Path(args.json).write_text(json.dumps(payload, indent=2, default=str))
        print(f"\nwrote {args.json}")


if __name__ == "__main__":
    main()
