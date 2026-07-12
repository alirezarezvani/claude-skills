"""Strategy executor contract.

Every one of the 20 strategy executors subclasses StrategyBase. The harness
only ever talks to this interface — a strategy never touches MT5 directly,
never sizes its own position, and never bypasses the risk gate. It consumes
a MarketContext and emits Signals; everything else is the harness's job.
"""
from __future__ import annotations

import dataclasses
import datetime as dt
import enum
from typing import Optional


class Side(enum.Enum):
    LONG = "long"
    SHORT = "short"


class ExitReason(enum.Enum):
    TAKE_PROFIT = "take_profit"
    STOP_LOSS = "stop_loss"
    TIME_STOP = "time_stop"
    STRATEGY_EXIT = "strategy_exit"
    RISK_HALT = "risk_halt"
    SUPERVISOR = "supervisor"


@dataclasses.dataclass
class Signal:
    """An order intent. Prices are absolute; the harness converts SL distance
    into lot size via the risk manager. tp may be None when the strategy
    manages its own exit through on_bar/manage_position."""
    side: Side
    entry: float               # intended entry price (market orders fill at bid/ask)
    stop_loss: float           # absolute price, required — no SL, no trade
    take_profit: Optional[float]
    comment: str = ""
    time_stop_bars: Optional[int] = None   # force-close after N primary bars
    confidence: float = 1.0    # 0..1, scales risk down (never up)


@dataclasses.dataclass
class PositionState:
    ticket: int
    side: Side
    entry_price: float
    stop_loss: float
    take_profit: Optional[float]
    volume: float
    opened_at: dt.datetime
    bars_held: int = 0


@dataclasses.dataclass
class MarketContext:
    """Everything a strategy is allowed to see for one evaluation tick."""
    symbol: str
    now: dt.datetime            # broker/server time, UTC
    bid: float
    ask: float
    spread_points: float
    bars: dict                  # timeframe -> pandas.DataFrame (OHLCV, tick_volume), oldest->newest
    aux: dict                   # extra feeds keyed by name, e.g. {"DXY": DataFrame, "calendar": [...]}
    position: Optional[PositionState]  # this strategy's open position, if any

    def bars_for(self, timeframe: str):
        df = self.bars.get(timeframe)
        if df is None:
            raise KeyError(f"strategy requested timeframe {timeframe!r} "
                           f"not declared in required_data()")
        return df


class StrategyBase:
    # --- identity / declaration (override in subclass) ---
    name: str = "unnamed"
    category: str = "uncategorized"      # momentum | mean-reversion | microstructure | indicator-hybrid
    primary_timeframe: str = "M5"
    extra_timeframes: tuple = ()         # e.g. ("M15",)
    aux_feeds: tuple = ()                # e.g. ("DXY", "calendar")
    lookback_bars: int = 200
    # sessions the strategy may open trades in, as UTC (start_hour, end_hour) pairs;
    # empty tuple = any time. Exits are always allowed.
    sessions_utc: tuple = ()
    default_risk_pct: float = 0.25       # % of equity risked per trade
    max_spread_points: float = 350.0     # skip entries when spread wider than this

    def warmup(self, ctx: MarketContext) -> None:
        """Called once with full lookback history before the live loop starts."""

    def on_bar(self, ctx: MarketContext) -> Optional[Signal]:
        """Called on each closed primary-timeframe bar while flat.
        Return a Signal to request an entry, or None."""
        raise NotImplementedError

    def manage_position(self, ctx: MarketContext) -> Optional[ExitReason]:
        """Called on each closed primary bar while holding a position.
        Return an ExitReason to request a close, or None to hold.
        Trailing-stop moves go through ctx.position mutation requests via
        the returned None + self.pending_sl_move (see below)."""
        # default: honor time stop only
        pos = ctx.position
        if pos and self._time_stop_bars is not None and pos.bars_held >= self._time_stop_bars:
            return ExitReason.TIME_STOP
        return None

    # A strategy may set this inside manage_position to ask the harness to
    # move the stop (e.g. trail / break-even). Harness reads and clears it.
    pending_sl_move: Optional[float] = None
    _time_stop_bars: Optional[int] = None

    def in_session(self, now: dt.datetime) -> bool:
        if not self.sessions_utc:
            return True
        h = now.hour + now.minute / 60.0
        for start, end in self.sessions_utc:
            if start <= h < end:
                return True
        return False
