"""Mean-reversion executors (strategies 6-10).

Shared edge family: outside news windows, gold on low timeframes oscillates
around liquidity anchors (VWAP, bands, round numbers, pivots). Extensions
away from those anchors driven by thin-book bursts tend to snap back. Every
executor here carries a regime filter or confirmation bar, because the one
way this family dies is fading a real breakout.
"""
from __future__ import annotations

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from core.strategy_base import StrategyBase, Signal, Side, MarketContext
from core.indicators import (
    atr, rsi, bollinger, adx, sma, vwap_session, round_levels,
)


class VWAPReversion(StrategyBase):
    """#6 — Fade 2-ATR extensions from session VWAP back to VWAP."""
    name = "vwap_reversion"
    category = "mean-reversion"
    primary_timeframe = "M1"
    sessions_utc = ((7.0, 20.0),)
    lookback_bars = 400
    default_risk_pct = 0.2

    K_ATR = 2.0
    RSI_LO, RSI_HI = 25, 75

    def on_bar(self, ctx: MarketContext):
        df = ctx.bars_for("M1")
        vwap = vwap_session(df)
        v = float(vwap.iloc[-1])
        if v != v:                          # NaN — first bars of the session
            return None
        a = float(atr(df, 14).iloc[-1])
        if a <= 0:
            return None
        close = float(df["close"].iloc[-1])
        r = float(rsi(df["close"], 7).iloc[-1])
        if close < v - self.K_ATR * a and r < self.RSI_LO:
            sl = ctx.ask - 1.2 * a
            return Signal(Side.LONG, ctx.ask, sl, v,
                          comment=self.name, time_stop_bars=30)
        if close > v + self.K_ATR * a and r > self.RSI_HI:
            sl = ctx.bid + 1.2 * a
            return Signal(Side.SHORT, ctx.bid, sl, v,
                          comment=self.name, time_stop_bars=30)
        return None


class BollingerFade(StrategyBase):
    """#7 — BB(20,2.5) band re-entry fade with ADX regime filter."""
    name = "bollinger_fade"
    category = "mean-reversion"
    primary_timeframe = "M5"
    default_risk_pct = 0.25

    ADX_MAX = 25

    def on_bar(self, ctx: MarketContext):
        df = ctx.bars_for("M5")
        lower, mid, upper = bollinger(df["close"], 20, 2.5)
        if float(adx(df, 14).iloc[-1]) > self.ADX_MAX:
            return None                     # trending — fades die
        a = float(atr(df, 14).iloc[-1])
        prev, cur = df.iloc[-2], df.iloc[-1]
        m = float(mid.iloc[-1])
        # re-entry confirmation: prev closed outside, current closed back inside
        if prev["close"] < float(lower.iloc[-2]) and cur["close"] > float(lower.iloc[-1]):
            sl = float(min(prev["low"], cur["low"])) - 0.3 * a
            return Signal(Side.LONG, ctx.ask, sl, m,
                          comment=self.name, time_stop_bars=20)
        if prev["close"] > float(upper.iloc[-2]) and cur["close"] < float(upper.iloc[-1]):
            sl = float(max(prev["high"], cur["high"])) + 0.3 * a
            return Signal(Side.SHORT, ctx.bid, sl, m,
                          comment=self.name, time_stop_bars=20)
        return None


class RSIExtremeFade(StrategyBase):
    """#8 — RSI(5) cross-back through 15/85; high win-rate, sub-1 RR by design."""
    name = "rsi_extreme_fade"
    category = "mean-reversion"
    primary_timeframe = "M1"
    sessions_utc = ((7.0, 20.0),)
    default_risk_pct = 0.2

    LO, HI = 15, 85

    def on_bar(self, ctx: MarketContext):
        df = ctx.bars_for("M1")
        r = rsi(df["close"], 5)
        prev_r, cur_r = float(r.iloc[-2]), float(r.iloc[-1])
        a = float(atr(df, 14).iloc[-1])
        if a <= 0:
            return None
        bar = df.iloc[-1]
        bullish = bar["close"] > bar["open"]
        if prev_r < self.LO <= cur_r and bullish:
            return Signal(Side.LONG, ctx.ask, ctx.ask - 1.5 * a, ctx.ask + 1.0 * a,
                          comment=self.name, time_stop_bars=15)
        if prev_r > self.HI >= cur_r and not bullish:
            return Signal(Side.SHORT, ctx.bid, ctx.bid + 1.5 * a, ctx.bid - 1.0 * a,
                          comment=self.name, time_stop_bars=15)
        return None


class RoundNumberBounce(StrategyBase):
    """#9 — Rejection wicks at $10 psychological levels within 1 ATR of price."""
    name = "round_number_bounce"
    category = "mean-reversion"
    primary_timeframe = "M5"
    default_risk_pct = 0.2

    STEP = 10.0
    WICK_MIN = 0.6                          # recovery must span 60% of bar range

    def on_bar(self, ctx: MarketContext):
        df = ctx.bars_for("M5")
        a = float(atr(df, 14).iloc[-1])
        if a <= 0:
            return None
        bar = df.iloc[-1]
        rng = float(bar["high"] - bar["low"])
        if rng <= 0:
            return None
        price = float(bar["close"])
        for level in round_levels(price, self.STEP):
            if abs(level - price) > a:
                continue
            # long: low pierced the level, close recovered above with a strong wick
            if bar["low"] < level < bar["close"] and (bar["close"] - bar["low"]) > self.WICK_MIN * rng:
                sl = level - 0.8 * a
                return Signal(Side.LONG, ctx.ask, sl, ctx.ask + 1.2 * a,
                              comment=self.name, time_stop_bars=24)
            if bar["high"] > level > bar["close"] and (bar["high"] - bar["close"]) > self.WICK_MIN * rng:
                sl = level + 0.8 * a
                return Signal(Side.SHORT, ctx.bid, sl, ctx.bid - 1.2 * a,
                              comment=self.name, time_stop_bars=24)
        return None


class PivotReversion(StrategyBase):
    """#10 — Classic daily-pivot S1/R1 rejections targeting the pivot."""
    name = "pivot_reversion"
    category = "mean-reversion"
    primary_timeframe = "M5"
    extra_timeframes = ("D1",)
    default_risk_pct = 0.25

    MIN_TP_ATR = 0.5

    def on_bar(self, ctx: MarketContext):
        m5, d1 = ctx.bars_for("M5"), ctx.bars_for("D1")
        if len(d1) < 2:
            return None
        y = d1.iloc[-2]                     # yesterday's completed daily bar
        p = float(y["high"] + y["low"] + y["close"]) / 3
        r1 = 2 * p - float(y["low"])
        s1 = 2 * p - float(y["high"])
        a = float(atr(m5, 14).iloc[-1])
        if a <= 0:
            return None
        bar = m5.iloc[-1]
        bullish = bar["close"] > bar["open"]
        if bar["low"] <= s1 and bar["close"] > s1 and bullish:
            if abs(p - ctx.ask) < self.MIN_TP_ATR * a:
                return None                 # pivot too close — no room to pay spread
            return Signal(Side.LONG, ctx.ask, s1 - 1.0 * a, p,
                          comment=self.name, time_stop_bars=36)
        if bar["high"] >= r1 and bar["close"] < r1 and not bullish:
            if abs(ctx.bid - p) < self.MIN_TP_ATR * a:
                return None
            return Signal(Side.SHORT, ctx.bid, r1 + 1.0 * a, p,
                          comment=self.name, time_stop_bars=36)
        return None
