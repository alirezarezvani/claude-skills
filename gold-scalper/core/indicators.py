"""Shared indicator kit — pandas-only, no TA-Lib dependency.

Kept deliberately small: every function is a pure transform of an OHLCV
DataFrame so strategies stay deterministic and backtest-identical to live.
All functions use only closed-bar data (no lookahead).
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def ema(s: pd.Series, period: int) -> pd.Series:
    return s.ewm(span=period, adjust=False).mean()


def sma(s: pd.Series, period: int) -> pd.Series:
    return s.rolling(period).mean()


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    hl = df["high"] - df["low"]
    hc = (df["high"] - df["close"].shift()).abs()
    lc = (df["low"] - df["close"].shift()).abs()
    tr = pd.concat([hl, hc, lc], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / period, adjust=False).mean()


def rsi(s: pd.Series, period: int = 14) -> pd.Series:
    delta = s.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / period, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / period, adjust=False).mean()
    rs = gain / loss.replace(0, np.nan)
    return (100 - 100 / (1 + rs)).fillna(50)


def bollinger(s: pd.Series, period: int = 20, stds: float = 2.0):
    mid = sma(s, period)
    sd = s.rolling(period).std(ddof=0)
    return mid - stds * sd, mid, mid + stds * sd


def stochastic(df: pd.DataFrame, k: int = 5, smooth_k: int = 3, d: int = 3):
    lo = df["low"].rolling(k).min()
    hi = df["high"].rolling(k).max()
    raw = 100 * (df["close"] - lo) / (hi - lo).replace(0, np.nan)
    k_line = raw.rolling(smooth_k).mean()
    return k_line, k_line.rolling(d).mean()


def macd(s: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
    line = ema(s, fast) - ema(s, slow)
    sig = ema(line, signal)
    return line, sig, line - sig


def keltner(df: pd.DataFrame, period: int = 20, mult: float = 2.0, atr_period: int = 10):
    mid = ema(df["close"], period)
    rng = atr(df, atr_period) * mult
    return mid - rng, mid, mid + rng


def supertrend(df: pd.DataFrame, period: int = 10, mult: float = 3.0) -> pd.Series:
    """Returns +1 (uptrend) / -1 (downtrend) per bar."""
    a = atr(df, period)
    hl2 = (df["high"] + df["low"]) / 2
    upper = hl2 + mult * a
    lower = hl2 - mult * a
    trend = np.ones(len(df), dtype=int)
    ub = upper.to_numpy().copy()
    lb = lower.to_numpy().copy()
    close = df["close"].to_numpy()
    for i in range(1, len(df)):
        ub[i] = min(ub[i], ub[i - 1]) if close[i - 1] <= ub[i - 1] else ub[i]
        lb[i] = max(lb[i], lb[i - 1]) if close[i - 1] >= lb[i - 1] else lb[i]
        if close[i] > ub[i - 1]:
            trend[i] = 1
        elif close[i] < lb[i - 1]:
            trend[i] = -1
        else:
            trend[i] = trend[i - 1]
    return pd.Series(trend, index=df.index)


def heikin_ashi(df: pd.DataFrame) -> pd.DataFrame:
    ha = pd.DataFrame(index=df.index)
    ha["close"] = (df["open"] + df["high"] + df["low"] + df["close"]) / 4
    ha_open = [(df["open"].iloc[0] + df["close"].iloc[0]) / 2]
    for i in range(1, len(df)):
        ha_open.append((ha_open[-1] + ha["close"].iloc[i - 1]) / 2)
    ha["open"] = ha_open
    ha["high"] = pd.concat([df["high"], ha["open"], ha["close"]], axis=1).max(axis=1)
    ha["low"] = pd.concat([df["low"], ha["open"], ha["close"]], axis=1).min(axis=1)
    return ha


def vwap_session(df: pd.DataFrame) -> pd.Series:
    """Session VWAP resetting at UTC midnight; volume = tick_volume."""
    day = df.index.date
    tp = (df["high"] + df["low"] + df["close"]) / 3
    vol = df["tick_volume"].astype(float)
    pv = (tp * vol).groupby(day).cumsum()
    cv = vol.groupby(day).cumsum().replace(0, np.nan)
    return pv / cv


def adx(df: pd.DataFrame, period: int = 14) -> pd.Series:
    up = df["high"].diff()
    dn = -df["low"].diff()
    plus_dm = np.where((up > dn) & (up > 0), up, 0.0)
    minus_dm = np.where((dn > up) & (dn > 0), dn, 0.0)
    a = atr(df, period)
    plus_di = 100 * pd.Series(plus_dm, index=df.index).ewm(alpha=1/period, adjust=False).mean() / a
    minus_di = 100 * pd.Series(minus_dm, index=df.index).ewm(alpha=1/period, adjust=False).mean() / a
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)
    return dx.ewm(alpha=1/period, adjust=False).mean().fillna(0)


def session_range(df: pd.DataFrame, start_h: int, end_h: int, now) -> tuple[float, float] | None:
    """High/low of today's bars in [start_h, end_h) UTC. None if no bars yet."""
    today = df[(df.index.date == now.date())
               & (df.index.hour >= start_h) & (df.index.hour < end_h)]
    if today.empty:
        return None
    return float(today["high"].max()), float(today["low"].min())


def round_levels(price: float, step: float = 10.0, n: int = 3) -> list[float]:
    """Nearest n round-number levels each side (gold: $10 steps → 2360, 2370…)."""
    base = round(price / step) * step
    return [base + i * step for i in range(-n, n + 1)]
