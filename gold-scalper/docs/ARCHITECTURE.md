# Gold Scalper — Multi-Strategy Agent Harness for MT5

One Python process runs **20 independent XAUUSD scalping executors** against a
single MT5 account, coordinated by a harness that owns everything strategies
must never own: order routing, position sizing, portfolio risk, news
blackouts, journaling, and kill switches. A supervisor loop (Claude Fable 5,
out-of-band) reads the journal, scores each strategy, and flips executors
on/off between sessions.

The design follows this repo's `engineering/agent-harness` discipline:
goal → decomposed tasks (strategies) → deterministic execution → machine
verification → bounded retries → escalate to human → refuse to run unverified.

```
┌─────────────────────────────────────────────────────────────┐
│  SUPERVISOR (supervisor.py + Claude Fable 5, out-of-band)    │
│  journal → scorecard → keep/disable verdicts → enabled.json  │
└──────────────────────────┬──────────────────────────────────┘
                           │ hot-reloaded every iteration
┌──────────────────────────▼──────────────────────────────────┐
│  ENGINE (core/engine.py) — one loop, all strategies          │
│  new-bar gate · news blackout · shared market snapshot       │
│  3-strike error trip → auto-disable · JSONL audit journal    │
├──────────────┬───────────────────────┬───────────────────────┤
│ RISK GATE    │ 20 STRATEGY EXECUTORS │ INDICATOR KIT         │
│ core/risk.py │ strategies/*.py       │ core/indicators.py    │
│ sizing, caps │ pure: Context→Signal  │ pandas-only,          │
│ circuit brkrs│ never touch broker    │ no-lookahead          │
└──────────────┴───────────┬───────────┴───────────────────────┘
                           │ single choke point
┌──────────────────────────▼──────────────────────────────────┐
│  BROKER ADAPTER — the ONLY module importing MetaTrader5      │
│  core/broker_mt5.py (live) / backtest/sim_broker.py (sim)    │
│  magic-number-per-strategy · restart-safe position adoption  │
└──────────────────────────────────────────────────────────────┘
```

## The contract

A strategy sees only a `MarketContext` (bid/ask, spread, closed bars for its
declared timeframes, declared aux feeds, its own position) and returns a
`Signal` (side, entry, **mandatory absolute SL**, TP, optional time-stop) or
an `ExitReason`. It declares its needs as class attributes
(`primary_timeframe`, `sessions_utc`, `default_risk_pct`,
`max_spread_points`, `aux_feeds`).

A strategy **cannot**: place orders, size positions, see other strategies'
positions, exceed the risk cap, or trade during a news blackout. One buggy
executor cannot hurt the account beyond its own risk slice.

**Attribution:** strategy *i* in `strategies/__init__.py:ALL_STRATEGIES` gets
MT5 magic `magic_base + i` (default 770000+i). This gives per-strategy P&L
from MT5 history, restart-safety (open positions re-adopted by magic on
boot), and zero interference with anything else on the account. The registry
is **append-only — never reorder**.

## Risk model (survival > preservation > growth)

| Control | Default | On breach |
|---|---|---|
| Per-trade risk | ≤ 0.5% equity (strategies ask 0.15–0.3%) | signal resized down |
| Daily loss | 2% from day-start equity | flatten all + 24 h halt |
| Weekly loss | 5% | flatten all + 7-day halt |
| Concurrent positions | 6 total, 4 same-direction | signal vetoed |
| Total volume | 3.0 lots | signal vetoed |
| News blackout | ±5 min around high-impact events | no entries fleet-wide |
| Strategy errors | 3 consecutive exceptions | strategy auto-disabled + journaled |

Sizing from SL distance:
`lots = equity × risk% / ((SL_dist / tick_size) × tick_value)`, snapped to
broker volume constraints. No SL, no trade. Halt state persists atomically in
`logs/risk_state.json`, so a crash-restart during a halt stays halted.

## The 20 executors

| # | Name | TF | Idea |
|---|---|---|---|
| 1 | london_breakout | M5 | Asian-range break in first London hours, ATR buffer |
| 2 | ny_open_momentum | M5/M15 | NY-open impulse bar aligned with M15 EMA trend |
| 3 | orb_ny | M5 | 30-min opening-range breakout, one trade/day |
| 4 | asian_range_break | M15 | Overnight range break with retest-hold filter |
| 5 | vol_expansion | M5 | ATR squeeze → burst-bar ignition, ADX filter |
| 6 | vwap_reversion | M1 | Fade 2-ATR extensions from session VWAP |
| 7 | bollinger_fade | M5 | BB(20,2.5) re-entry fade, ADX<25 regime filter |
| 8 | rsi_extreme_fade | M1 | RSI(5) cross-back through 15/85 |
| 9 | round_number_bounce | M5 | Rejection wicks at $10 psychological levels |
| 10 | pivot_reversion | M5/D1 | S1/R1 daily-pivot rejections targeting pivot |
| 11 | news_spike_fade | M1 | Fade the overreaction leg after high-impact prints |
| 12 | tick_velocity_ignition | M1 | Tick-volume + range burst momentum ignition |
| 13 | spread_aware_liquidity | M1 | Z-score micro-reversion, only in tight-spread regimes |
| 14 | dxy_divergence | M5+DXY | Gold/DXY inverse-correlation break snap |
| 15 | liquidity_sweep_reversal | M5 | Sweep of session extreme then rejection (SMC) |
| 16 | ema_ribbon_pullback | M5 | 8/13/21 ribbon trend, enter on ribbon pullback |
| 17 | stoch_trend_scalp | M5/M15 | Stoch(5,3,3) hooks in M15-trend direction only |
| 18 | macd_zero_cross | M5 | MACD zero-cross with expanding histogram |
| 19 | keltner_supertrend_ride | M5 | Supertrend + Keltner pullback, trailing exit |
| 20 | heikin_ashi_atr | M5 | HA color-flip entries, opposite-body exit |

Per-strategy spec sheets (edge hypothesis, exact rules, failure modes,
sources) live in `docs/STRATEGIES.md`.

## Engine iteration

1. Roll day/week equity anchors; check circuit breakers → tripped = flatten
   everything and halt.
2. Fetch bars **once per unique timeframe** (20 strategies share ~4 fetches)
   plus aux feeds (DXY bars, calendar).
3. Hot-reload `config/enabled.json` — the supervisor/human control surface.
4. Per strategy, gated on *its* new closed bar: holding →
   `manage_position()` (exit / trail via `pending_sl_move` / time-stop);
   flat and enabled and in-session and spread OK and no blackout →
   `on_bar()` → Signal → risk gate → `order_send`.
5. Every event (signal, veto+why, order, SL move, close, error, disable,
   halt) appended to `logs/journal.jsonl`.

Entries only happen on closed bars, so backtest and live evaluate identical
data — the indicator kit has no intra-bar lookahead anywhere.

## Supervisor — where Fable 5 sits

Deliberately out-of-band; analysis can never block or crash execution.

- **Deterministic layer** (`supervisor.py score`): journal + MT5 deal history
  per magic → per-strategy scorecard (trades, win%, profit factor,
  expectancy, max DD, veto rate, errors). Mechanical flags: PF < 0.8 over
  ≥ 30 trades, 3-strike error trips, veto rate > 80%.
- **Fable 5 layer** (`supervisor.py review`): packages scorecard + recent
  journal into a review prompt; Claude Fable 5 reasons about *why* a strategy
  bleeds (regime shift? spread widening? session drift?) and returns
  keep/disable/tune verdicts, applied via `supervisor.py apply` — a one-line,
  auditable, reversible edit to `enabled.json`. It never touches orders.
- **Escalation:** circuit-breaker halts and auto-disables notify the
  operator; re-enabling after a halt is always a human decision.

## Backtest parity

`backtest/sim_broker.py` implements the same interface as `MT5Broker`
replaying M1 history with configurable spread and slippage — the exact same
strategy code runs in sim. `backtest/run_backtest.py` emits the same
scorecard the supervisor uses.

**Promotion pipeline (non-negotiable):** each strategy must show positive
expectancy after spread on ≥ 6 months of M1 data → whole fleet on a **demo
account ≥ 2 weeks** → only then real money, at minimum size.

## Running

```bash
pip install MetaTrader5 pandas numpy   # live needs Windows + running MT5 terminal

python main.py --dry-run               # full pipeline, orders logged not sent
python main.py                         # live (demo account first!)
python backtest/run_backtest.py --csv xauusd_m1.csv
python supervisor.py score             # scorecard
python supervisor.py review            # generate Fable 5 review prompt
```

## Honest caveat

Retail gold scalping fights spread and slippage first and the market second —
a 25–35 cent spread against a 60-cent target eats most naive edges. That is
exactly why the harness enforces spread gates, per-strategy attribution, and
the backtest → demo → live pipeline: the point of running 20 executors is to
let the journal **kill** the majority that don't survive transaction costs
and keep the few that do. Expect to disable most of the fleet. That is the
system working, not failing.
