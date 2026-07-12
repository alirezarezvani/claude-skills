"""Harness engine — the loop controller that runs all 20 executors.

Design (mirrors this repo's engineering/agent-harness discipline):
  goal -> per-strategy executors -> every action verified -> bounded retries
  -> circuit breakers escalate to human -> journal is the audit trail.

One process, one account, N strategies. Each strategy gets its own MT5 magic
number so positions are attributable and restart-safe: on boot the engine
re-adopts any open position whose magic falls in our range.

Per iteration (each new closed primary bar, checked every POLL_SECONDS):
  1. roll risk day/week counters, check circuit breakers
  2. build one shared MarketContext snapshot (bars fetched once per TF)
  3. for each ENABLED strategy: flat -> on_bar() may emit a Signal;
     holding -> manage_position() may exit / trail
  4. every Signal passes the RiskManager gate before order_send
  5. everything is journaled to logs/journal.jsonl (one JSON per event)

The supervisor (supervisor.py) reads the journal and can flip strategies
on/off via config/enabled.json — the engine re-reads it every iteration, so
a human or a Claude Fable 5 review loop can intervene without a restart.
"""
from __future__ import annotations

import datetime as dt
import json
import logging
import pathlib
import signal as os_signal
import time
from typing import Optional

from .strategy_base import ExitReason, MarketContext, Signal, StrategyBase
from .risk import RiskConfig, RiskManager

log = logging.getLogger("engine")

POLL_SECONDS = 2.0
ROLLOVER_START, ROLLOVER_END = (21, 50), (22, 10)   # UTC swap window: spreads 5-10x
MAX_TRADES_PER_DAY = 5                              # per strategy — stops SL-loops


def in_rollover(now: dt.datetime) -> bool:
    hm = (now.hour, now.minute)
    return ROLLOVER_START <= hm < ROLLOVER_END


class Journal:
    def __init__(self, path: pathlib.Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, kind: str, **fields) -> None:
        rec = {"ts": dt.datetime.now(dt.timezone.utc).isoformat(), "kind": kind, **fields}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, default=str) + "\n")


class Engine:
    def __init__(self, broker, strategies: list[StrategyBase],
                 risk: RiskManager, base_dir: pathlib.Path,
                 calendar: Optional[list] = None):
        self.broker = broker
        self.strategies = strategies
        self.risk = risk
        self.base = base_dir
        self.journal = Journal(base_dir / "logs" / "journal.jsonl")
        self.enabled_path = base_dir / "config" / "enabled.json"
        self.calendar = calendar or []          # [{"time": iso, "impact": "high"}, ...]
        self._last_bar_time: dict[str, object] = {}
        self._trades_day: str = ""
        self._trades_today: dict[str, int] = {}
        self._adopted_bars: dict[int, int] = self._load_adopted()
        self._stop = False
        os_signal.signal(os_signal.SIGINT, self._sigint)
        os_signal.signal(os_signal.SIGTERM, self._sigint)

    def _sigint(self, *_):
        log.warning("shutdown requested — finishing iteration then stopping")
        self._stop = True

    # ---------- liveness + restart persistence ----------
    def _heartbeat(self, now: dt.datetime, equity: float) -> None:
        p = self.base / "logs" / "heartbeat.json"
        tmp = p.with_suffix(".tmp")
        try:
            tmp.write_text(json.dumps({
                "ts": now.isoformat(), "equity": equity,
                "open_positions": len(self.broker.open_positions())}))
            tmp.replace(p)
        except OSError:
            pass                                    # liveness is best-effort

    def _bars_path(self) -> pathlib.Path:
        return self.base / "logs" / "bars_held.json"

    def _load_adopted(self) -> dict[int, int]:
        try:
            return {int(k): v for k, v in
                    json.loads(self._bars_path().read_text()).items()}
        except (OSError, json.JSONDecodeError, ValueError):
            return {}

    def _save_adopted(self) -> None:
        tmp = self._bars_path().with_suffix(".tmp")
        try:
            tmp.write_text(json.dumps(self._adopted_bars))
            tmp.replace(self._bars_path())
        except OSError:
            pass

    # ---------- config hot-reload ----------
    def enabled_map(self) -> dict:
        try:
            return json.loads(self.enabled_path.read_text())
        except (OSError, json.JSONDecodeError):
            return {}

    # ---------- news blackout ----------
    def in_news_blackout(self, now: dt.datetime, minutes: int = 5) -> bool:
        for ev in self.calendar:
            if ev.get("impact") != "high":
                continue
            t = dt.datetime.fromisoformat(ev["time"])
            if abs((t - now).total_seconds()) <= minutes * 60:
                return True
        return False

    # ---------- context assembly (one snapshot shared by all strategies) ----------
    def build_context(self, strategy: StrategyBase, shared_bars: dict,
                      shared_aux: dict, now: dt.datetime) -> MarketContext:
        t = self.broker.tick()
        magic = self.broker.magic_for(self.strategies.index(strategy))
        return MarketContext(
            symbol=self.broker.symbol, now=now,
            bid=t.bid, ask=t.ask,
            spread_points=self.broker.spread_points(),
            bars={tf: shared_bars[tf] for tf in
                  (strategy.primary_timeframe, *strategy.extra_timeframes)},
            aux={k: shared_aux[k] for k in strategy.aux_feeds if k in shared_aux},
            position=self.broker.position_for_magic(magic))

    def fetch_shared(self) -> tuple[dict, dict]:
        tfs, aux_names = set(), set()
        for s in self.strategies:
            tfs.add(s.primary_timeframe)
            tfs.update(s.extra_timeframes)
            aux_names.update(s.aux_feeds)
        lookback = max(s.lookback_bars for s in self.strategies)
        bars = {tf: self.broker.bars(tf, lookback) for tf in tfs}
        aux = {}
        if "DXY" in aux_names:
            for sym in ("DXY", "USDX", "USDollar", "DX"):
                try:
                    aux["DXY"] = self.broker.bars("M5", lookback, symbol=sym)
                    break
                except Exception:
                    continue
        if "calendar" in aux_names:
            aux["calendar"] = self.calendar
        return bars, aux

    # ---------- main loop ----------
    def run(self) -> None:
        log.info("engine start: %d strategies on %s", len(self.strategies), self.broker.symbol)
        self.journal.write("engine_start",
                           strategies=[s.name for s in self.strategies])
        for s in self.strategies:
            try:
                bars, aux = self.fetch_shared()
                s.warmup(self.build_context(s, bars, aux,
                                            dt.datetime.now(dt.timezone.utc)))
            except Exception:
                log.exception("warmup failed for %s — disabling", s.name)
                self._disable(s.name, "warmup failure")

        errors: dict[str, int] = {}
        while not self._stop:
            try:
                self.iterate(errors)
            except Exception:
                log.exception("iteration error")
            time.sleep(POLL_SECONDS)
        self.journal.write("engine_stop")
        log.info("engine stopped")

    def iterate(self, errors: dict[str, int]) -> None:
        now = dt.datetime.now(dt.timezone.utc)
        equity = self.broker.equity()
        self._heartbeat(now, equity)
        if (self.base / "HALT").exists():          # manual kill switch: touch HALT
            log.error("HALT file present — flattening and stopping")
            self._flatten_all(ExitReason.SUPERVISOR, "manual HALT file")
            self._stop = True
            return
        self.risk.roll(now, equity)
        allowed, why = self.risk.trading_allowed(now, equity)
        if not allowed:
            self._flatten_all(ExitReason.RISK_HALT, why)
            return

        bars, aux = self.fetch_shared()
        enabled = self.enabled_map()
        blackout = ((self.risk.cfg.news_blackout and self.in_news_blackout(now))
                    or in_rollover(now))
        open_positions = self.broker.open_positions()
        day = now.strftime("%Y-%m-%d")
        if self._trades_day != day:
            self._trades_day, self._trades_today = day, {}

        for idx, strat in enumerate(self.strategies):
            if errors.get(strat.name, 0) >= 3:
                continue                                  # tripped — needs human/supervisor reset
            # new-bar gate per strategy timeframe
            tf = strat.primary_timeframe
            last = bars[tf].index[-1]
            key = f"{strat.name}:{tf}"
            if self._last_bar_time.get(key) == last:
                continue
            self._last_bar_time[key] = last

            try:
                ctx = self.build_context(strat, bars, aux, now)
                if ctx.position is not None:
                    self._manage(strat, ctx, idx)
                elif (enabled.get(strat.name, True) and not blackout
                      and strat.in_session(now)
                      and ctx.spread_points <= strat.max_spread_points):
                    self._maybe_enter(strat, ctx, idx, equity, open_positions)
                errors[strat.name] = 0
            except Exception as e:
                errors[strat.name] = errors.get(strat.name, 0) + 1
                log.exception("strategy %s error (%d/3)", strat.name, errors[strat.name])
                self.journal.write("strategy_error", strategy=strat.name,
                                   error=str(e), count=errors[strat.name])
                if errors[strat.name] >= 3:
                    self._disable(strat.name, "3 consecutive errors — escalated")

    def _maybe_enter(self, strat: StrategyBase, ctx: MarketContext, idx: int,
                     equity: float, open_positions: list) -> None:
        if self._trades_today.get(strat.name, 0) >= MAX_TRADES_PER_DAY:
            return                              # pathological signal-loop guard
        sig = strat.on_bar(ctx)
        if sig is None:
            return
        sig.comment = sig.comment or strat.name
        info = self.broker.info
        lots = self.risk.size_signal(
            sig, equity=equity, requested_risk_pct=strat.default_risk_pct,
            tick_value=info.trade_tick_value, tick_size=info.trade_tick_size,
            volume_min=info.volume_min, volume_step=info.volume_step,
            volume_max=info.volume_max, open_positions=open_positions)
        self.journal.write("signal", strategy=strat.name, side=sig.side.value,
                           entry=sig.entry, sl=sig.stop_loss, tp=sig.take_profit,
                           sized_lots=lots, vetoed=lots is None)
        if lots is None:
            return
        strat._time_stop_bars = sig.time_stop_bars
        ticket = self.broker.market_order(sig, lots, self.broker.magic_for(idx))
        fill = getattr(self.broker, "last_fill", None)
        self.journal.write("order", strategy=strat.name, ticket=ticket,
                           lots=lots, filled=ticket is not None,
                           slippage_points=fill["slippage_points"] if fill else None)
        if ticket is not None:
            self._trades_today[strat.name] = self._trades_today.get(strat.name, 0) + 1

    def _manage(self, strat: StrategyBase, ctx: MarketContext, idx: int) -> None:
        t = ctx.position.ticket
        # bars_held persists across restarts so adopted positions keep their
        # time-stop clock instead of resetting to zero
        ctx.position.bars_held = self._adopted_bars.get(t, 0) + 1
        self._adopted_bars[t] = ctx.position.bars_held
        self._save_adopted()
        strat.pending_sl_move = None
        reason = strat.manage_position(ctx)
        if reason is not None:
            ok = self.broker.close_position(ctx.position, reason.value)
            if ok:
                self._adopted_bars.pop(t, None)
                self._save_adopted()
            self.journal.write("close", strategy=strat.name,
                               ticket=t,
                               reason=reason.value, ok=ok)
        elif strat.pending_sl_move is not None:
            ok = self.broker.modify_sl(ctx.position, strat.pending_sl_move)
            self.journal.write("sl_move", strategy=strat.name,
                               ticket=ctx.position.ticket,
                               new_sl=strat.pending_sl_move, ok=ok)

    def _flatten_all(self, reason: ExitReason, why: str) -> None:
        for pos in self.broker.open_positions():
            self.broker.close_position(pos, reason.value)
        self.journal.write("halt", reason=why)

    def _disable(self, name: str, why: str) -> None:
        m = self.enabled_map()
        m[name] = False
        self.enabled_path.parent.mkdir(parents=True, exist_ok=True)
        self.enabled_path.write_text(json.dumps(m, indent=2))
        self.journal.write("disabled", strategy=name, reason=why)
        log.error("DISABLED %s: %s", name, why)
