"""Portfolio-level risk gate.

Sits between every strategy Signal and the broker. Enforces the survival >
preservation > growth hierarchy: per-trade risk caps, daily/weekly loss
circuit breakers, max concurrent exposure across all 20 executors, and a
correlation guard so five momentum bots can't all pile into the same London
breakout at full size.

All strategies share ONE account; this module is the only thing standing
between an over-eager executor and a blown account. Nothing trades around it.
"""
from __future__ import annotations

import dataclasses
import datetime as dt
import json
import logging
import pathlib
from typing import Optional

from .strategy_base import Signal, Side

log = logging.getLogger("risk")


@dataclasses.dataclass
class RiskConfig:
    max_risk_per_trade_pct: float = 0.5      # hard cap regardless of strategy ask
    max_daily_loss_pct: float = 2.0          # halt all entries for the day
    max_weekly_loss_pct: float = 5.0         # halt all entries for the week
    max_open_positions: int = 6              # across all strategies
    max_same_direction: int = 4              # long OR short concurrently
    max_total_volume_lots: float = 3.0
    min_equity: float = 100.0                # stop trading below this
    news_blackout: bool = True               # honored by engine via calendar feed


class RiskManager:
    def __init__(self, cfg: RiskConfig, state_path: pathlib.Path):
        self.cfg = cfg
        self.state_path = state_path
        self._state = self._load()

    # ---------- persistence (atomic, survives restarts) ----------
    def _load(self) -> dict:
        if self.state_path.exists():
            try:
                return json.loads(self.state_path.read_text())
            except (json.JSONDecodeError, OSError):
                log.warning("risk state unreadable, starting fresh")
        return {"day": None, "day_start_equity": None,
                "week": None, "week_start_equity": None,
                "halted_until": None}

    def _save(self) -> None:
        tmp = self.state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self._state, indent=2, default=str))
        tmp.replace(self.state_path)

    # ---------- rollover ----------
    def roll(self, now: dt.datetime, equity: float) -> None:
        day = now.strftime("%Y-%m-%d")
        week = now.strftime("%G-W%V")
        if self._state["day"] != day:
            self._state.update(day=day, day_start_equity=equity)
        if self._state["week"] != week:
            self._state.update(week=week, week_start_equity=equity)
        self._save()

    # ---------- circuit breakers ----------
    def trading_allowed(self, now: dt.datetime, equity: float) -> tuple[bool, str]:
        if equity < self.cfg.min_equity:
            return False, f"equity {equity:.2f} below floor {self.cfg.min_equity}"
        halted = self._state.get("halted_until")
        if halted and now < dt.datetime.fromisoformat(halted):
            return False, f"halted until {halted}"
        d0 = self._state.get("day_start_equity")
        if d0:
            dd = (d0 - equity) / d0 * 100
            if dd >= self.cfg.max_daily_loss_pct:
                self.halt(now, hours=24, reason=f"daily loss {dd:.2f}%")
                return False, f"daily loss limit hit ({dd:.2f}%)"
        w0 = self._state.get("week_start_equity")
        if w0:
            dd = (w0 - equity) / w0 * 100
            if dd >= self.cfg.max_weekly_loss_pct:
                self.halt(now, hours=24 * 7, reason=f"weekly loss {dd:.2f}%")
                return False, f"weekly loss limit hit ({dd:.2f}%)"
        return True, "ok"

    def halt(self, now: dt.datetime, hours: float, reason: str) -> None:
        until = now + dt.timedelta(hours=hours)
        self._state["halted_until"] = until.isoformat()
        self._save()
        log.error("TRADING HALTED until %s: %s", until, reason)

    # ---------- per-signal gate ----------
    def size_signal(self, sig: Signal, *, equity: float, requested_risk_pct: float,
                    tick_value: float, tick_size: float,
                    volume_min: float, volume_step: float, volume_max: float,
                    open_positions: list) -> Optional[float]:
        """Return lot size for the signal, or None to veto it."""
        if len(open_positions) >= self.cfg.max_open_positions:
            log.info("veto %s: max open positions", sig.comment)
            return None
        same_dir = sum(1 for p in open_positions if p.side == sig.side)
        if same_dir >= self.cfg.max_same_direction:
            log.info("veto %s: %d positions already %s", sig.comment, same_dir, sig.side.value)
            return None

        sl_dist = abs(sig.entry - sig.stop_loss)
        if sl_dist <= 0 or tick_size <= 0 or tick_value <= 0:
            log.warning("veto %s: degenerate SL/contract params", sig.comment)
            return None

        risk_pct = min(requested_risk_pct, self.cfg.max_risk_per_trade_pct)
        risk_pct *= max(0.0, min(sig.confidence, 1.0))
        risk_amount = equity * risk_pct / 100.0
        loss_per_lot = (sl_dist / tick_size) * tick_value
        lots = risk_amount / loss_per_lot

        # broker constraints
        lots = max(volume_min, min(lots, volume_max))
        lots = round(lots / volume_step) * volume_step
        lots = round(lots, 2)
        if lots < volume_min:
            return None

        total_vol = sum(p.volume for p in open_positions) + lots
        if total_vol > self.cfg.max_total_volume_lots:
            log.info("veto %s: total volume %.2f > cap", sig.comment, total_vol)
            return None
        return lots
