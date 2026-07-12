"""Indicator-hybrid executors (strategies 16-20).

Shared edge family: classic indicator setups sharpened with regime and
structure filters — pullbacks into stacked EMAs, oscillator turns with a
higher-timeframe trend gate, zero-line momentum ignition, and two managed
trend rides (Supertrend/Keltner and Heikin-Ashi) that trail instead of
taking a fixed target.
"""
from __future__ import annotations

import math
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from core.strategy_base import StrategyBase, Signal, Side, ExitReason, MarketContext
from core.indicators import atr, ema, stochastic, macd, keltner, supertrend, heikin_ashi


def _finite(*vals: float) -> bool:
    return all(math.isfinite(v) for v in vals)


class EMARibbonPullback(StrategyBase):
    """#16 — Pullback into a stacked 8/13/21 EMA ribbon that closes back out."""
    name = "ema_ribbon_pullback"
    category = "indicator-hybrid"
    primary_timeframe = "M5"
    sessions_utc = ((7.0, 20.0),)
    default_risk_pct = 0.25

    SL_ATR = 0.5
    RR = 1.5

    def on_bar(self, ctx: MarketContext):
        df = ctx.bars_for("M5")
        if len(df) < 30:
            return None
        c = df["close"]
        e8, e13, e21 = ema(c, 8), ema(c, 13), ema(c, 21)
        f8, f13, f21 = float(e8.iloc[-1]), float(e13.iloc[-1]), float(e21.iloc[-1])
        e21_prev = float(e21.iloc[-4])                # 3 bars ago
        a = float(atr(df, 14).iloc[-1])
        if not _finite(f8, f13, f21, e21_prev, a) or a <= 0:
            return None
        bar = df.iloc[-1]
        if f8 > f13 > f21 and f21 > e21_prev:         # bullish ribbon, rising base
            if bar["low"] <= f13 and bar["close"] > f8:
                sl = f21 - self.SL_ATR * a
                risk = ctx.ask - sl
                if risk <= 0:
                    return None
                return Signal(Side.LONG, ctx.ask, sl, ctx.ask + self.RR * risk,
                              comment=self.name, time_stop_bars=24)
        if f8 < f13 < f21 and f21 < e21_prev:         # bearish ribbon, falling base
            if bar["high"] >= f13 and bar["close"] < f8:
                sl = f21 + self.SL_ATR * a
                risk = sl - ctx.bid
                if risk <= 0:
                    return None
                return Signal(Side.SHORT, ctx.bid, sl, ctx.bid - self.RR * risk,
                              comment=self.name, time_stop_bars=24)
        return None


class StochTrendScalp(StrategyBase):
    """#17 — Stochastic turn out of an extreme, traded only with the M15 trend."""
    name = "stoch_trend_scalp"
    category = "indicator-hybrid"
    primary_timeframe = "M5"
    extra_timeframes = ("M15",)
    sessions_utc = ((7.0, 20.0),)
    default_risk_pct = 0.25

    SL_ATR = 1.2
    RR = 1.5

    def on_bar(self, ctx: MarketContext):
        m5, m15 = ctx.bars_for("M5"), ctx.bars_for("M15")
        if len(m5) < 30 or len(m15) < 60:
            return None
        k, d = stochastic(m5, 5, 3, 3)
        k1, k2 = float(k.iloc[-1]), float(k.iloc[-2])
        d1, d2 = float(d.iloc[-1]), float(d.iloc[-2])
        a = float(atr(m5, 14).iloc[-1])
        t_fast = float(ema(m15["close"], 20).iloc[-1])
        t_slow = float(ema(m15["close"], 50).iloc[-1])
        if not _finite(k1, k2, d1, d2, a, t_fast, t_slow) or a <= 0:
            return None
        if t_fast > t_slow and k1 > d1 and k2 <= d2 and k1 < 30 and d1 < 30:
            sl = ctx.ask - self.SL_ATR * a
            return Signal(Side.LONG, ctx.ask, sl,
                          ctx.ask + self.RR * (ctx.ask - sl),
                          comment=self.name, time_stop_bars=20)
        if t_fast < t_slow and k1 < d1 and k2 >= d2 and k1 > 70 and d1 > 70:
            sl = ctx.bid + self.SL_ATR * a
            return Signal(Side.SHORT, ctx.bid, sl,
                          ctx.bid - self.RR * (sl - ctx.bid),
                          comment=self.name, time_stop_bars=20)
        return None


class MACDZeroCross(StrategyBase):
    """#18 — MACD zero-line cross with an expanding histogram, dead markets skipped."""
    name = "macd_zero_cross"
    category = "indicator-hybrid"
    primary_timeframe = "M5"
    default_risk_pct = 0.25

    DEAD_RATIO = 0.6                       # ATR(14) below this x ATR(100) = no energy
    SL_ATR = 1.5
    RR = 2.0

    def on_bar(self, ctx: MarketContext):
        df = ctx.bars_for("M5")
        if len(df) < 120:
            return None
        line, _, hist = macd(df["close"], 12, 26, 9)
        l1, l2 = float(line.iloc[-1]), float(line.iloc[-2])
        h1, h2, h3 = float(hist.iloc[-1]), float(hist.iloc[-2]), float(hist.iloc[-3])
        a_fast = float(atr(df, 14).iloc[-1])
        a_slow = float(atr(df, 100).iloc[-1])
        if not _finite(l1, l2, h1, h2, h3, a_fast, a_slow) or a_fast <= 0:
            return None
        if a_fast < self.DEAD_RATIO * a_slow:
            return None
        if l1 > 0 and l2 <= 0 and h1 > h2 > h3:
            sl = ctx.ask - self.SL_ATR * a_fast
            return Signal(Side.LONG, ctx.ask, sl,
                          ctx.ask + self.RR * (ctx.ask - sl),
                          comment=self.name, time_stop_bars=30)
        if l1 < 0 and l2 >= 0 and h1 < h2 < h3:
            sl = ctx.bid + self.SL_ATR * a_fast
            return Signal(Side.SHORT, ctx.bid, sl,
                          ctx.bid - self.RR * (sl - ctx.bid),
                          comment=self.name, time_stop_bars=30)
        return None


class KeltnerSupertrendRide(StrategyBase):
    """#19 — Supertrend-gated Keltner-midline reclaim, ridden with a trailing stop."""
    name = "keltner_supertrend_ride"
    category = "indicator-hybrid"
    primary_timeframe = "M5"
    sessions_utc = ((7.0, 20.0),)
    default_risk_pct = 0.3

    def on_bar(self, ctx: MarketContext):
        df = ctx.bars_for("M5")
        if len(df) < 40:
            return None
        lower, mid, upper = keltner(df, 20)
        st = int(supertrend(df, 10, 3.0).iloc[-1])
        m1, m2 = float(mid.iloc[-1]), float(mid.iloc[-2])
        lo_band, hi_band = float(lower.iloc[-1]), float(upper.iloc[-1])
        if not _finite(m1, m2, lo_band, hi_band):
            return None
        prev, cur = df.iloc[-2], df.iloc[-1]
        if st == 1 and prev["low"] <= m2 and cur["close"] > m1:
            if ctx.ask - lo_band <= 0:
                return None
            return Signal(Side.LONG, ctx.ask, lo_band, None,
                          comment=self.name, time_stop_bars=60)
        if st == -1 and prev["high"] >= m2 and cur["close"] < m1:
            if hi_band - ctx.bid <= 0:
                return None
            return Signal(Side.SHORT, ctx.bid, hi_band, None,
                          comment=self.name, time_stop_bars=60)
        return None

    def manage_position(self, ctx: MarketContext):
        pos = ctx.position
        if pos is None:
            return None
        if self._time_stop_bars is not None and pos.bars_held >= self._time_stop_bars:
            return ExitReason.TIME_STOP
        df = ctx.bars_for("M5")
        st = int(supertrend(df, 10, 3.0).iloc[-1])
        if (pos.side is Side.LONG and st == -1) or (pos.side is Side.SHORT and st == 1):
            return ExitReason.STRATEGY_EXIT
        mid = float(keltner(df, 20)[1].iloc[-1])
        if math.isfinite(mid):
            if pos.side is Side.LONG and mid > pos.stop_loss:
                self.pending_sl_move = mid
            elif pos.side is Side.SHORT and mid < pos.stop_loss:
                self.pending_sl_move = mid
        return None


class HeikinAshiATR(StrategyBase):
    """#20 — Heikin-Ashi color flip with a flat wick, ridden until the flip reverses."""
    name = "heikin_ashi_atr"
    category = "indicator-hybrid"
    primary_timeframe = "M5"
    sessions_utc = ((7.0, 20.0),)
    default_risk_pct = 0.25

    WICK_TOL = 0.9995                      # ha_low >= ha_open * this = near-flat bottom
    SL_ATR = 1.5
    EXIT_BODY_ATR = 0.5

    def on_bar(self, ctx: MarketContext):
        df = ctx.bars_for("M5")
        if len(df) < 30:
            return None
        ha = heikin_ashi(df)
        prev, cur = ha.iloc[-2], ha.iloc[-1]
        a = float(atr(df, 14).iloc[-1])
        if not _finite(float(cur["open"]), float(cur["close"]),
                       float(prev["open"]), float(prev["close"]), a) or a <= 0:
            return None
        prev_red = prev["close"] < prev["open"]
        prev_green = prev["close"] > prev["open"]
        cur_green = cur["close"] > cur["open"]
        cur_red = cur["close"] < cur["open"]
        if prev_red and cur_green and cur["low"] >= cur["open"] * self.WICK_TOL:
            sl = ctx.ask - self.SL_ATR * a
            return Signal(Side.LONG, ctx.ask, sl, None,
                          comment=self.name, time_stop_bars=40)
        if prev_green and cur_red and cur["high"] <= cur["open"] * (2 - self.WICK_TOL):
            sl = ctx.bid + self.SL_ATR * a
            return Signal(Side.SHORT, ctx.bid, sl, None,
                          comment=self.name, time_stop_bars=40)
        return None

    def manage_position(self, ctx: MarketContext):
        pos = ctx.position
        if pos is None:
            return None
        if self._time_stop_bars is not None and pos.bars_held >= self._time_stop_bars:
            return ExitReason.TIME_STOP
        df = ctx.bars_for("M5")
        ha = heikin_ashi(df)
        cur = ha.iloc[-1]
        a = float(atr(df, 14).iloc[-1])
        if not _finite(float(cur["open"]), float(cur["close"]), a) or a <= 0:
            return None
        body = abs(float(cur["close"]) - float(cur["open"]))
        opposite = (cur["close"] < cur["open"]) if pos.side is Side.LONG \
            else (cur["close"] > cur["open"])
        if opposite and body > self.EXIT_BODY_ATR * a:
            return ExitReason.STRATEGY_EXIT
        return None
