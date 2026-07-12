"""MT5 broker adapter.

The only module that imports MetaTrader5. Everything above it (engine,
strategies, risk) is broker-agnostic, which is what lets the same executors
run against the backtest broker in backtest/sim_broker.py unchanged.

Requires: pip install MetaTrader5 pandas  (Windows + running MT5 terminal).
"""
from __future__ import annotations

import datetime as dt
import logging
from typing import Optional

import pandas as pd

try:
    import MetaTrader5 as mt5
except ImportError:            # allows backtesting on non-Windows machines
    mt5 = None

from .strategy_base import PositionState, Side, Signal

log = logging.getLogger("broker")

TIMEFRAME_MAP = {}
if mt5:
    TIMEFRAME_MAP = {
        "M1": mt5.TIMEFRAME_M1, "M5": mt5.TIMEFRAME_M5,
        "M15": mt5.TIMEFRAME_M15, "M30": mt5.TIMEFRAME_M30,
        "H1": mt5.TIMEFRAME_H1, "H4": mt5.TIMEFRAME_H4, "D1": mt5.TIMEFRAME_D1,
    }

TF_SECONDS = {"M1": 60, "M5": 300, "M15": 900, "M30": 1800,
              "H1": 3600, "H4": 14400, "D1": 86400}


class MT5Broker:
    last_fill: Optional[dict] = None       # requested vs filled on the latest order

    def __init__(self, symbol: str, magic_base: int = 770000,
                 login: Optional[int] = None, password: str = "",
                 server: str = "", terminal_path: Optional[str] = None):
        if mt5 is None:
            raise RuntimeError("MetaTrader5 package not installed — live mode "
                               "needs Windows + `pip install MetaTrader5`")
        self.symbol = symbol
        self.magic_base = magic_base
        kwargs = {}
        if terminal_path:
            kwargs["path"] = terminal_path
        if login:
            kwargs.update(login=login, password=password, server=server)
        if not mt5.initialize(**kwargs):
            raise RuntimeError(f"mt5.initialize failed: {mt5.last_error()}")
        if not mt5.symbol_select(symbol, True):
            raise RuntimeError(f"symbol_select({symbol}) failed: {mt5.last_error()}")
        self.info = mt5.symbol_info(symbol)
        self.utc_offset_s = self._probe_server_offset()
        log.info("connected: %s, spread=%s pts, tick_value=%s, server offset %+dh",
                 symbol, self.info.spread, self.info.trade_tick_value,
                 self.utc_offset_s // 3600)

    def _probe_server_offset(self) -> int:
        """MT5 bar timestamps are broker-server time (usually UTC+2/+3, DST-shifting).
        Session logic runs in UTC, so all bars are normalized: compare the newest
        M1 bar's timestamp to actual UTC now, rounded to the nearest 30 minutes."""
        rates = mt5.copy_rates_from_pos(self.symbol, mt5.TIMEFRAME_M1, 0, 1)
        if rates is None or not len(rates):
            log.warning("server-offset probe failed — assuming server time == UTC")
            return 0
        now = dt.datetime.now(dt.timezone.utc).timestamp()
        raw = float(rates[0]["time"]) - now
        return int(round(raw / 1800.0)) * 1800

    # ---------- market data ----------
    def tick(self):
        return mt5.symbol_info_tick(self.symbol)

    def bars(self, timeframe: str, count: int, symbol: Optional[str] = None) -> pd.DataFrame:
        rates = mt5.copy_rates_from_pos(symbol or self.symbol,
                                        TIMEFRAME_MAP[timeframe], 0, count)
        if rates is None:
            raise RuntimeError(f"copy_rates failed: {mt5.last_error()}")
        df = pd.DataFrame(rates)
        # normalize broker-server timestamps to true UTC so session windows hold
        df["time"] = pd.to_datetime(df["time"] - self.utc_offset_s, unit="s", utc=True)
        return df.set_index("time")

    def spread_points(self) -> float:
        t = self.tick()
        return (t.ask - t.bid) / self.info.point

    # ---------- account ----------
    def equity(self) -> float:
        acc = mt5.account_info()
        return acc.equity if acc else 0.0

    # ---------- positions (one magic number per strategy) ----------
    def magic_for(self, strategy_index: int) -> int:
        return self.magic_base + strategy_index

    def open_positions(self) -> list[PositionState]:
        out = []
        for p in (mt5.positions_get(symbol=self.symbol) or []):
            if not (self.magic_base <= p.magic < self.magic_base + 1000):
                continue                      # not ours — never touch it
            out.append(PositionState(
                ticket=p.ticket,
                side=Side.LONG if p.type == mt5.POSITION_TYPE_BUY else Side.SHORT,
                entry_price=p.price_open, stop_loss=p.sl,
                take_profit=p.tp or None, volume=p.volume,
                opened_at=dt.datetime.fromtimestamp(p.time, dt.timezone.utc)))
        return out

    def position_for_magic(self, magic: int) -> Optional[PositionState]:
        for p in (mt5.positions_get(symbol=self.symbol) or []):
            if p.magic == magic:
                return PositionState(
                    ticket=p.ticket,
                    side=Side.LONG if p.type == mt5.POSITION_TYPE_BUY else Side.SHORT,
                    entry_price=p.price_open, stop_loss=p.sl,
                    take_profit=p.tp or None, volume=p.volume,
                    opened_at=dt.datetime.fromtimestamp(p.time, dt.timezone.utc))
        return None

    # ---------- orders ----------
    def market_order(self, sig: Signal, lots: float, magic: int,
                     deviation: int = 20) -> Optional[int]:
        t = self.tick()
        price = t.ask if sig.side == Side.LONG else t.bid
        req = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": lots,
            "type": mt5.ORDER_TYPE_BUY if sig.side == Side.LONG else mt5.ORDER_TYPE_SELL,
            "price": price,
            "sl": sig.stop_loss,
            "tp": sig.take_profit or 0.0,
            "deviation": deviation,
            "magic": magic,
            "comment": sig.comment[:31],
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": self._filling_mode(),
        }
        res = mt5.order_send(req)
        if res is None or res.retcode != mt5.TRADE_RETCODE_DONE:
            log.error("order_send failed for %s: %s", sig.comment,
                      res.retcode if res else mt5.last_error())
            self.last_fill = None
            return None
        slip = (res.price - price) / self.info.point
        if sig.side == Side.SHORT:
            slip = -slip                    # positive = adverse for either side
        self.last_fill = {"requested": price, "filled": res.price,
                          "slippage_points": round(slip, 1)}
        log.info("OPENED %s %s %.2f lots @ %.2f (slip %+.1f pts) sl=%.2f tp=%s (magic=%d)",
                 sig.side.value, self.symbol, lots, res.price, slip,
                 sig.stop_loss, sig.take_profit, magic)
        return res.order

    def close_position(self, pos: PositionState, reason: str = "") -> bool:
        t = self.tick()
        req = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": pos.volume,
            "type": mt5.ORDER_TYPE_SELL if pos.side == Side.LONG else mt5.ORDER_TYPE_BUY,
            "position": pos.ticket,
            "price": t.bid if pos.side == Side.LONG else t.ask,
            "deviation": 30,
            "comment": f"close:{reason}"[:31],
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": self._filling_mode(),
        }
        res = mt5.order_send(req)
        ok = res is not None and res.retcode == mt5.TRADE_RETCODE_DONE
        (log.info if ok else log.error)("close ticket %d (%s): %s",
                                        pos.ticket, reason,
                                        "done" if ok else (res.retcode if res else mt5.last_error()))
        return ok

    def modify_sl(self, pos: PositionState, new_sl: float) -> bool:
        req = {"action": mt5.TRADE_ACTION_SLTP, "symbol": self.symbol,
               "position": pos.ticket, "sl": new_sl, "tp": pos.take_profit or 0.0}
        res = mt5.order_send(req)
        return res is not None and res.retcode == mt5.TRADE_RETCODE_DONE

    def _filling_mode(self):
        fm = self.info.filling_mode
        if fm & 1:
            return mt5.ORDER_FILLING_FOK
        if fm & 2:
            return mt5.ORDER_FILLING_IOC
        return mt5.ORDER_FILLING_RETURN

    def shutdown(self):
        mt5.shutdown()
