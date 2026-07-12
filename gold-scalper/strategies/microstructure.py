"""Microstructure executors (strategies 11-15).

Shared edge family: gold's order flow leaves fingerprints on the tape — news
spikes overshoot and retrace, tick bursts ignite continuation, tight-spread
regimes mean-revert, the dollar leash snaps back, and resting stops get swept
right before reversals. Each executor reads one of those fingerprints.
"""
from __future__ import annotations

import datetime as dt
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from core.strategy_base import StrategyBase, Signal, Side, ExitReason, MarketContext
from core.indicators import atr, sma, rsi, session_range


class NewsSpikeFade(StrategyBase):
    """#11 — Fade the overreaction bar 3-10 minutes after a high-impact release."""
    name = "news_spike_fade"
    category = "microstructure"
    primary_timeframe = "M1"
    aux_feeds = ("calendar",)
    default_risk_pct = 0.15                # dangerous strategy — smallest risk
    max_spread_points = 600.0              # spreads are wide post-news

    MIN_LAG_MIN, MAX_LAG_MIN = 3.0, 10.0   # engine blackout is ±5 min; we trade after
    SPIKE_ATR = 3.0                        # 3-bar spike must exceed this x ATR
    SL_BUF = 0.3                           # SL beyond the spike extreme, in ATRs
    RETRACE = 0.38                         # TP = 38% retrace of the spike leg

    def _recent_high_impact(self, ctx: MarketContext):
        now = ctx.now.replace(tzinfo=None) if ctx.now.tzinfo else ctx.now
        for ev in ctx.aux.get("calendar") or []:
            if not isinstance(ev, dict) or ev.get("impact") != "high":
                continue
            try:
                t = dt.datetime.fromisoformat(str(ev.get("time")))
            except ValueError:
                continue
            if t.tzinfo is not None:
                t = t.astimezone(dt.timezone.utc).replace(tzinfo=None)
            age_min = (now - t).total_seconds() / 60.0
            if self.MIN_LAG_MIN <= age_min <= self.MAX_LAG_MIN:
                return t
        return None

    def on_bar(self, ctx: MarketContext):
        df = ctx.bars_for("M1")
        if len(df) < 20:
            return None
        event_time = self._recent_high_impact(ctx)
        if event_time is None:
            return None
        try:
            after = df[df.index >= event_time]
        except TypeError:                  # tz-aware index vs naive event time
            return None
        if len(after) < 4:                 # 3 spike bars + the pullback bar
            return None
        spike = after.iloc[:3]
        a = float(atr(df, 14).iloc[-1])
        if not a > 0:
            return None
        move = float(spike["close"].iloc[-1]) - float(spike["open"].iloc[0])
        if abs(move) < self.SPIKE_ATR * a:
            return None
        bar = df.iloc[-1]
        if move > 0 and bar["close"] < bar["open"]:   # up-spike, first bearish bar
            extreme = float(spike["high"].max())
            leg = extreme - float(spike["low"].min())
            if leg <= 0:
                return None
            sl = extreme + self.SL_BUF * a
            tp = extreme - self.RETRACE * leg
            return Signal(Side.SHORT, ctx.bid, sl, tp,
                          comment=self.name, time_stop_bars=20)
        if move < 0 and bar["close"] > bar["open"]:   # down-spike, first bullish bar
            extreme = float(spike["low"].min())
            leg = float(spike["high"].max()) - extreme
            if leg <= 0:
                return None
            sl = extreme - self.SL_BUF * a
            tp = extreme + self.RETRACE * leg
            return Signal(Side.LONG, ctx.ask, sl, tp,
                          comment=self.name, time_stop_bars=20)
        return None


class TickVelocityIgnition(StrategyBase):
    """#12 — Enter with a tick-volume burst bar that closes hard at its extreme."""
    name = "tick_velocity_ignition"
    category = "microstructure"
    primary_timeframe = "M1"
    sessions_utc = ((7.0, 20.0),)
    default_risk_pct = 0.2

    VOL_MULT = 2.5                         # tick_volume vs its SMA(20)
    RANGE_ATR = 1.5                        # bar range vs ATR(14)
    CLOSE_ZONE = 0.25                      # close within this fraction of the extreme
    RR = 1.2

    def on_bar(self, ctx: MarketContext):
        df = ctx.bars_for("M1")
        if len(df) < 22:
            return None
        vol = df["tick_volume"].astype(float)
        base = float(sma(vol, 20).iloc[-2])    # average of the bars before ignition
        if not base > 0:
            return None
        if float(vol.iloc[-1]) < self.VOL_MULT * base:
            return None
        a = float(atr(df, 14).iloc[-1])
        if not a > 0:
            return None
        bar = df.iloc[-1]
        rng = bar["high"] - bar["low"]
        if rng < self.RANGE_ATR * a or not rng > 0:
            return None
        if bar["close"] >= bar["high"] - self.CLOSE_ZONE * rng:
            sl = float(bar["low"])
            return Signal(Side.LONG, ctx.ask, sl, ctx.ask + self.RR * (ctx.ask - sl),
                          comment=self.name, time_stop_bars=10)
        if bar["close"] <= bar["low"] + self.CLOSE_ZONE * rng:
            sl = float(bar["high"])
            return Signal(Side.SHORT, ctx.bid, sl, ctx.bid - self.RR * (sl - ctx.bid),
                          comment=self.name, time_stop_bars=10)
        return None


class SpreadAwareLiquidity(StrategyBase):
    """#13 — Micro mean-reversion to SMA(30), taken only in tight-spread regimes."""
    name = "spread_aware_liquidity"
    category = "microstructure"
    primary_timeframe = "M1"
    sessions_utc = ((7.0, 17.0),)
    default_risk_pct = 0.2
    max_spread_points = 150.0              # only trade when liquidity is good

    Z_TRIGGER = 2.2
    RSI_LONG, RSI_SHORT = 20.0, 80.0

    def on_bar(self, ctx: MarketContext):
        if ctx.spread_points > self.max_spread_points:
            return None
        df = ctx.bars_for("M1")
        if len(df) < 32:
            return None
        close = df["close"]
        mid = float(sma(close, 30).iloc[-1])
        sd = float(close.rolling(30).std(ddof=0).iloc[-1])
        a = float(atr(df, 14).iloc[-1])
        if not sd > 0 or not a > 0 or not mid > 0:
            return None
        z = (float(close.iloc[-1]) - mid) / sd
        r = float(rsi(close, 3).iloc[-1])
        if z < -self.Z_TRIGGER and r < self.RSI_LONG:
            return Signal(Side.LONG, ctx.ask, ctx.ask - a, mid,
                          comment=self.name, time_stop_bars=12)
        if z > self.Z_TRIGGER and r > self.RSI_SHORT:
            return Signal(Side.SHORT, ctx.bid, ctx.bid + a, mid,
                          comment=self.name, time_stop_bars=12)
        return None


class DXYDivergence(StrategyBase):
    """#14 — Trade gold back into inverse correlation when it and DXY move together."""
    name = "dxy_divergence"
    category = "microstructure"
    primary_timeframe = "M5"
    aux_feeds = ("DXY",)
    default_risk_pct = 0.2

    RET_BARS = 12                          # lookback for both return legs
    MIN_RET = 0.0015                       # each |return| must exceed 0.15%
    SL_ATR = 1.5
    RR = 1.5

    def on_bar(self, ctx: MarketContext):
        df = ctx.bars_for("M5")
        dxy = ctx.aux.get("DXY")
        if dxy is None or getattr(dxy, "empty", True) or "close" not in dxy:
            return None
        if len(df) < self.RET_BARS + 1 or len(dxy) < self.RET_BARS + 1:
            return None
        g0 = float(df["close"].iloc[-self.RET_BARS - 1])
        d0 = float(dxy["close"].iloc[-self.RET_BARS - 1])
        if not g0 > 0 or not d0 > 0:
            return None
        gold_ret = float(df["close"].iloc[-1]) / g0 - 1.0
        dxy_ret = float(dxy["close"].iloc[-1]) / d0 - 1.0
        if abs(gold_ret) < self.MIN_RET or abs(dxy_ret) < self.MIN_RET:
            return None
        a = float(atr(df, 14).iloc[-1])
        if not a > 0:
            return None
        if gold_ret > 0 and dxy_ret > 0:   # both rose — short gold to restore inverse
            sl = ctx.bid + self.SL_ATR * a
            return Signal(Side.SHORT, ctx.bid, sl, ctx.bid - self.RR * (sl - ctx.bid),
                          comment=self.name, time_stop_bars=24)
        if gold_ret < 0 and dxy_ret < 0:   # both fell — long gold
            sl = ctx.ask - self.SL_ATR * a
            return Signal(Side.LONG, ctx.ask, sl, ctx.ask + self.RR * (ctx.ask - sl),
                          comment=self.name, time_stop_bars=24)
        return None


class LiquiditySweepReversal(StrategyBase):
    """#15 — SMC stop hunt: wick through an aged session extreme, close back inside."""
    name = "liquidity_sweep_reversal"
    category = "microstructure"
    primary_timeframe = "M5"
    sessions_utc = ((7.0, 20.0),)
    default_risk_pct = 0.25

    MIN_AGE_HOURS = 2                      # extreme must be at least this old
    MIN_BARS_AGO = 8                       # ...and from an earlier bar than this
    SL_BUF = 0.5                           # SL beyond the sweep extreme, in ATRs
    REJECT_ZONE = 0.4                      # close within this fraction of the far extreme
    RR = 2.0

    def on_bar(self, ctx: MarketContext):
        df = ctx.bars_for("M5")
        hour = int(ctx.now.hour)
        if hour < self.MIN_AGE_HOURS or len(df) < self.MIN_BARS_AGO + 1:
            return None
        rng = session_range(df, 0, hour, ctx.now)
        if rng is None:
            return None
        hi, lo = rng
        today = df[(df.index.date == ctx.now.date()) & (df.index.hour < hour)]
        if today.empty:
            return None
        a = float(atr(df, 14).iloc[-1])
        if not a > 0:
            return None
        bar = df.iloc[-1]
        bar_rng = bar["high"] - bar["low"]
        if not bar_rng > 0:
            return None
        cutoff_time = ctx.now - dt.timedelta(hours=self.MIN_AGE_HOURS)
        cutoff_bar = df.index[-self.MIN_BARS_AGO]
        # long: wick below the aged session low, close back above with rejection
        t_lo = today["low"].idxmin()
        if (bar["low"] < lo and bar["close"] > lo
                and bar["close"] >= bar["high"] - self.REJECT_ZONE * bar_rng
                and t_lo <= cutoff_time and t_lo < cutoff_bar):
            sl = float(bar["low"]) - self.SL_BUF * a
            return Signal(Side.LONG, ctx.ask, sl, ctx.ask + self.RR * (ctx.ask - sl),
                          comment=self.name, time_stop_bars=30)
        # short: wick above the aged session high, close back below with rejection
        t_hi = today["high"].idxmax()
        if (bar["high"] > hi and bar["close"] < hi
                and bar["close"] <= bar["low"] + self.REJECT_ZONE * bar_rng
                and t_hi <= cutoff_time and t_hi < cutoff_bar):
            sl = float(bar["high"]) + self.SL_BUF * a
            return Signal(Side.SHORT, ctx.bid, sl, ctx.bid - self.RR * (sl - ctx.bid),
                          comment=self.name, time_stop_bars=30)
        return None
