"""Simulated broker for backtesting — same public surface as core.broker_mt5.MT5Broker.

Replays a historical M1 OHLCV DataFrame bar by bar. The engine-side contract
is identical to MT5Broker: tick(), bars(), spread_points(), equity(),
magic_for(), open_positions(), position_for_magic(), market_order(),
close_position(), modify_sl(), shutdown(), plus .symbol and .info — so the
same strategy executors run unchanged against history.

Fill model (deliberately conservative):
  * longs enter at ask (+ slippage), exit on the bid side of each bar;
  * shorts enter at bid (- slippage), exit on the ask side (bar high/low
    shifted up by the spread) so the spread is paid once per round trip;
  * if both SL and TP fall inside one bar's range, the SL is assumed hit first.
"""
from __future__ import annotations

import dataclasses
import pathlib
import sys
import types
from typing import Optional

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from core.strategy_base import PositionState, Side, Signal  # noqa: E402

TF_RULES = {"M1": "1min", "M5": "5min", "M15": "15min", "M30": "30min",
            "H1": "1h", "H4": "4h", "D1": "1D"}
TF_DELTAS = {tf: pd.Timedelta(rule) for tf, rule in TF_RULES.items()}

_AGG = {"open": "first", "high": "max", "low": "min",
        "close": "last", "tick_volume": "sum"}


@dataclasses.dataclass
class _SimPosition:
    ticket: int
    magic: int
    side: Side
    entry: float
    sl: float
    tp: Optional[float]
    volume: float
    open_time: pd.Timestamp
    comment: str = ""


class SimBroker:
    def __init__(self, symbol: str, m1_df: pd.DataFrame,
                 spread_points: float = 300, initial_equity: float = 10_000,
                 point: float = 0.01, tick_value: float = 1.0,
                 tick_size: float = 0.01, volume_min: float = 0.01,
                 volume_step: float = 0.01, volume_max: float = 10.0,
                 slippage_points: float = 20, magic_base: int = 770000):
        df = m1_df.copy()
        if "tick_volume" not in df.columns and "volume" in df.columns:
            df = df.rename(columns={"volume": "tick_volume"})
        missing = [c for c in _AGG if c not in df.columns]
        if missing:
            raise ValueError(f"m1_df missing columns: {missing}")
        if not isinstance(df.index, pd.DatetimeIndex):
            raise ValueError("m1_df must have a DatetimeIndex")
        df = df[list(_AGG)].sort_index()
        df.index = (df.index.tz_localize("UTC") if df.index.tz is None
                    else df.index.tz_convert("UTC"))
        if df.empty:
            raise ValueError("m1_df is empty")
        self._m1 = df

        self.symbol = symbol
        self.magic_base = magic_base
        self._point = point
        self._spread_pts = float(spread_points)
        self._slippage_pts = float(slippage_points)
        self._tick_value = tick_value
        self._tick_size = tick_size
        self._initial_equity = float(initial_equity)
        self.info = types.SimpleNamespace(
            point=point, spread=spread_points,
            trade_tick_value=tick_value, trade_tick_size=tick_size,
            volume_min=volume_min, volume_step=volume_step,
            volume_max=volume_max, filling_mode=1)

        self._i = 0                          # index pointer into the M1 data
        self._next_ticket = 1
        self._realized = 0.0
        self._positions: list[_SimPosition] = []
        self.trade_log: list[dict] = []
        self._resampled: dict[str, tuple[pd.DataFrame, pd.DatetimeIndex]] = {}

    # ---------- clock ----------
    @property
    def now(self) -> pd.Timestamp:
        return self._m1.index[self._i]

    @property
    def done(self) -> bool:
        return self._i >= len(self._m1) - 1

    def step(self) -> None:
        """Advance one M1 bar, then mark open positions to the new bar."""
        if self.done:
            return
        self._i += 1
        self._check_exits(self._m1.iloc[self._i], self.now)

    # ---------- market data ----------
    def tick(self):
        close = float(self._m1["close"].iloc[self._i])
        return types.SimpleNamespace(bid=close,
                                     ask=close + self._spread_pts * self._point,
                                     time=self.now)

    def bars(self, timeframe: str, count: int,
             symbol: Optional[str] = None) -> pd.DataFrame:
        if symbol is not None and symbol != self.symbol:
            raise KeyError(f"sim broker has no data for symbol {symbol!r}")
        if timeframe not in TF_RULES:
            raise KeyError(f"unknown timeframe {timeframe!r}")
        if timeframe == "M1":
            # the engine acts on bar close, so the current M1 bar counts as closed
            return self._m1.iloc[:self._i + 1].tail(count)
        res, completion = self._get_resampled(timeframe)
        # a resampled bar is complete once its period end is covered by the
        # current (closed) M1 bar: bar_start + tf <= now + 1min
        cutoff = self.now + pd.Timedelta(minutes=1)
        pos = completion.searchsorted(cutoff, side="right")
        return res.iloc[:pos].tail(count)

    def _get_resampled(self, timeframe: str):
        cached = self._resampled.get(timeframe)
        if cached is None:
            res = (self._m1.resample(TF_RULES[timeframe],
                                     label="left", closed="left")
                   .agg(_AGG).dropna(subset=["open"]))
            cached = (res, res.index + TF_DELTAS[timeframe])
            self._resampled[timeframe] = cached
        return cached

    def spread_points(self) -> float:
        return self._spread_pts

    # ---------- account ----------
    def equity(self) -> float:
        close = float(self._m1["close"].iloc[self._i])
        unrealized = sum(self._pnl(p.side, p.entry, close, p.volume)
                         for p in self._positions)
        return self._initial_equity + self._realized + unrealized

    # ---------- positions ----------
    def magic_for(self, strategy_index: int) -> int:
        return self.magic_base + strategy_index

    def open_positions(self) -> list[PositionState]:
        return [self._to_state(p) for p in self._positions]

    def position_for_magic(self, magic: int) -> Optional[PositionState]:
        for p in self._positions:
            if p.magic == magic:
                return self._to_state(p)
        return None

    def _to_state(self, p: _SimPosition) -> PositionState:
        return PositionState(ticket=p.ticket, side=p.side, entry_price=p.entry,
                             stop_loss=p.sl, take_profit=p.tp, volume=p.volume,
                             opened_at=p.open_time.to_pydatetime())

    # ---------- orders ----------
    def market_order(self, sig: Signal, lots: float, magic: int,
                     deviation: int = 20) -> Optional[int]:
        t = self.tick()
        slip = self._slippage_pts * self._point       # adverse slippage
        price = t.ask + slip if sig.side == Side.LONG else t.bid - slip
        pos = _SimPosition(ticket=self._next_ticket, magic=magic, side=sig.side,
                           entry=price, sl=sig.stop_loss,
                           tp=sig.take_profit or None, volume=lots,
                           open_time=self.now, comment=sig.comment[:31])
        self._next_ticket += 1
        self._positions.append(pos)
        return pos.ticket

    def close_position(self, pos: PositionState, reason: str = "") -> bool:
        p = self._find(pos.ticket)
        if p is None:
            return False
        t = self.tick()
        exit_price = t.bid if p.side == Side.LONG else t.ask
        self._close(p, exit_price, reason or "strategy_exit", self.now)
        return True

    def modify_sl(self, pos: PositionState, new_sl: float) -> bool:
        p = self._find(pos.ticket)
        if p is None:
            return False
        p.sl = new_sl
        return True

    def shutdown(self) -> None:
        pass

    # ---------- internals ----------
    def _find(self, ticket: int) -> Optional[_SimPosition]:
        for p in self._positions:
            if p.ticket == ticket:
                return p
        return None

    def _pnl(self, side: Side, entry: float, exit_price: float,
             volume: float) -> float:
        diff = exit_price - entry if side == Side.LONG else entry - exit_price
        return diff / self._tick_size * self._tick_value * volume

    def _close(self, p: _SimPosition, exit_price: float, reason: str,
               close_time: pd.Timestamp) -> None:
        pnl = self._pnl(p.side, p.entry, exit_price, p.volume)
        self._realized += pnl
        self.trade_log.append({
            "magic": p.magic, "side": p.side.value, "entry": p.entry,
            "exit": exit_price, "volume": p.volume, "pnl": pnl,
            "open_time": p.open_time, "close_time": close_time,
            "reason": reason, "comment": p.comment})
        self._positions.remove(p)

    def _check_exits(self, bar, when: pd.Timestamp) -> None:
        spread = self._spread_pts * self._point
        hi, lo = float(bar["high"]), float(bar["low"])
        for p in list(self._positions):
            if p.side == Side.LONG:                    # exits on the bid side
                sl_hit = p.sl > 0 and lo <= p.sl
                tp_hit = p.tp is not None and hi >= p.tp
            else:                                      # exits on the ask side
                sl_hit = p.sl > 0 and hi + spread >= p.sl
                tp_hit = p.tp is not None and lo + spread <= p.tp
            if sl_hit:                # conservative: SL first when both inside bar
                self._close(p, p.sl, "stop_loss", when)
            elif tp_hit:
                self._close(p, p.tp, "take_profit", when)
