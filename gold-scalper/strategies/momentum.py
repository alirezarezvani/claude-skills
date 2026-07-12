"""Momentum / breakout executors (strategies 1-5).

Shared edge family: gold concentrates volatility at session opens; range
breaks in those windows continue more often than they revert. Each executor
differs in which range it measures and which window it trades.
"""
from __future__ import annotations

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from core.strategy_base import StrategyBase, Signal, Side, ExitReason, MarketContext
from core.indicators import atr, ema, adx, session_range


class LondonBreakout(StrategyBase):
    """#1 — Break of the Asian-session range in the first two London hours."""
    name = "london_breakout"
    category = "momentum"
    primary_timeframe = "M5"
    sessions_utc = ((7.0, 10.0),)          # London 07:00-10:00 UTC
    lookback_bars = 300
    default_risk_pct = 0.3

    RANGE_START, RANGE_END = 0, 7          # Asian range 00:00-07:00 UTC
    BUFFER_ATR = 0.25                      # break must clear range by this many ATRs
    RR = 1.5

    def on_bar(self, ctx: MarketContext):
        df = ctx.bars_for("M5")
        rng = session_range(df, self.RANGE_START, self.RANGE_END, ctx.now)
        if rng is None:
            return None
        hi, lo = rng
        if (hi - lo) < 2.0:                # dead Asian session — range too small to matter
            return None
        a = float(atr(df, 14).iloc[-1])
        buf = self.BUFFER_ATR * a
        close = float(df["close"].iloc[-1])
        if close > hi + buf:
            sl = hi - 0.5 * a              # back inside the range invalidates the break
            return Signal(Side.LONG, ctx.ask, sl,
                          ctx.ask + self.RR * (ctx.ask - sl),
                          comment=self.name, time_stop_bars=24)
        if close < lo - buf:
            sl = lo + 0.5 * a
            return Signal(Side.SHORT, ctx.bid, sl,
                          ctx.bid - self.RR * (sl - ctx.bid),
                          comment=self.name, time_stop_bars=24)
        return None


class NYOpenMomentum(StrategyBase):
    """#2 — Ride the impulse in the first NY hour when it agrees with M15 trend."""
    name = "ny_open_momentum"
    category = "momentum"
    primary_timeframe = "M5"
    extra_timeframes = ("M15",)
    sessions_utc = ((13.5, 15.5),)         # 13:30-15:30 UTC (NY equity open window)
    default_risk_pct = 0.3

    IMPULSE_ATR = 1.2                      # last bar range must exceed this x ATR
    RR = 1.2

    def on_bar(self, ctx: MarketContext):
        m5, m15 = ctx.bars_for("M5"), ctx.bars_for("M15")
        a = float(atr(m5, 14).iloc[-1])
        bar = m5.iloc[-1]
        bar_range = bar["high"] - bar["low"]
        if bar_range < self.IMPULSE_ATR * a:
            return None
        trend_up = float(ema(m15["close"], 20).iloc[-1]) > float(ema(m15["close"], 50).iloc[-1])
        body_up = bar["close"] > bar["open"]
        if body_up and trend_up and bar["close"] > (bar["low"] + 0.7 * bar_range):
            sl = float(bar["low"])
            return Signal(Side.LONG, ctx.ask, sl, ctx.ask + self.RR * (ctx.ask - sl),
                          comment=self.name, time_stop_bars=12)
        if not body_up and not trend_up and bar["close"] < (bar["low"] + 0.3 * bar_range):
            sl = float(bar["high"])
            return Signal(Side.SHORT, ctx.bid, sl, ctx.bid - self.RR * (sl - ctx.bid),
                          comment=self.name, time_stop_bars=12)
        return None


class OpeningRangeBreakout(StrategyBase):
    """#3 — Classic ORB: first 30 min of NY session defines the range; trade the break."""
    name = "orb_ny"
    category = "momentum"
    primary_timeframe = "M5"
    sessions_utc = ((14.0, 17.0),)         # trade breaks 14:00-17:00 UTC
    default_risk_pct = 0.25

    OR_START, OR_END = 13.5, 14.0          # opening range 13:30-14:00 UTC
    RR = 2.0
    _traded_today: str = ""

    def on_bar(self, ctx: MarketContext):
        day = ctx.now.strftime("%Y-%m-%d")
        if self._traded_today == day:      # one break per day, first signal only
            return None
        df = ctx.bars_for("M5")
        orb = df[(df.index.date == ctx.now.date())
                 & (df.index.hour * 60 + df.index.minute >= self.OR_START * 60)
                 & (df.index.hour * 60 + df.index.minute < self.OR_END * 60)]
        if len(orb) < 5:
            return None
        hi, lo = float(orb["high"].max()), float(orb["low"].min())
        close = float(df["close"].iloc[-1])
        if close > hi:
            self._traded_today = day
            return Signal(Side.LONG, ctx.ask, lo, ctx.ask + self.RR * (ctx.ask - lo),
                          comment=self.name, time_stop_bars=36)
        if close < lo:
            self._traded_today = day
            return Signal(Side.SHORT, ctx.bid, hi, ctx.bid - self.RR * (hi - ctx.bid),
                          comment=self.name, time_stop_bars=36)
        return None


class AsianRangeBreakout(StrategyBase):
    """#4 — Fakeout-filtered break of the overnight consolidation during late Asia,
    anticipating the pre-London push. Requires a retest hold, unlike #1."""
    name = "asian_range_break"
    category = "momentum"
    primary_timeframe = "M15"
    sessions_utc = ((4.0, 7.0),)
    default_risk_pct = 0.2

    RANGE_START, RANGE_END = 0, 4
    RR = 1.5

    def on_bar(self, ctx: MarketContext):
        df = ctx.bars_for("M15")
        rng = session_range(df, self.RANGE_START, self.RANGE_END, ctx.now)
        if rng is None:
            return None
        hi, lo = rng
        a = float(atr(df, 14).iloc[-1])
        prev, cur = df.iloc[-2], df.iloc[-1]
        # break bar followed by a hold bar that does NOT re-enter the range
        if prev["close"] > hi and cur["low"] > hi:
            sl = hi - 0.3 * a
            return Signal(Side.LONG, ctx.ask, sl, ctx.ask + self.RR * (ctx.ask - sl),
                          comment=self.name, time_stop_bars=16)
        if prev["close"] < lo and cur["high"] < lo:
            sl = lo + 0.3 * a
            return Signal(Side.SHORT, ctx.bid, sl, ctx.bid - self.RR * (sl - ctx.bid),
                          comment=self.name, time_stop_bars=16)
        return None


class VolatilityExpansion(StrategyBase):
    """#5 — Squeeze-then-burst: trade the direction of the first expansion bar
    after ATR compresses well below its own average. Session-agnostic."""
    name = "vol_expansion"
    category = "momentum"
    primary_timeframe = "M5"
    default_risk_pct = 0.25

    SQUEEZE = 0.7                          # ATR(7) < 0.7 x ATR(48) = compression
    BURST = 1.8                            # bar range > 1.8 x ATR(7) = ignition
    RR = 1.5

    def on_bar(self, ctx: MarketContext):
        df = ctx.bars_for("M5")
        a_fast = atr(df, 7)
        a_slow = atr(df, 48)
        # compression measured on the bars BEFORE the burst bar
        if float(a_fast.iloc[-2]) > self.SQUEEZE * float(a_slow.iloc[-2]):
            return None
        bar = df.iloc[-1]
        rng = bar["high"] - bar["low"]
        if rng < self.BURST * float(a_fast.iloc[-2]):
            return None
        if float(adx(df, 14).iloc[-1]) < 15:   # ignition needs directional energy
            return None
        if bar["close"] > bar["open"]:
            sl = float(bar["low"])
            return Signal(Side.LONG, ctx.ask, sl, ctx.ask + self.RR * (ctx.ask - sl),
                          comment=self.name, time_stop_bars=18)
        sl = float(bar["high"])
        return Signal(Side.SHORT, ctx.bid, sl, ctx.bid - self.RR * (sl - ctx.bid),
                      comment=self.name, time_stop_bars=18)
