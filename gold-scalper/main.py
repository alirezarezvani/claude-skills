"""Entrypoint — wires config, broker, risk, and the 20-strategy fleet.

Live:     python main.py
Dry run:  python main.py --dry-run          (reads live data, sends no orders)
Subset:   python main.py --strategies london_breakout,vwap_reversion

Requires Windows + a running MT5 terminal + `pip install MetaTrader5 pandas`.
"""
from __future__ import annotations

import argparse
import json
import logging
import pathlib
import sys

BASE_DIR = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from core.risk import RiskConfig, RiskManager       # noqa: E402
from core.engine import Engine                       # noqa: E402
from strategies import ALL_STRATEGIES                # noqa: E402

log = logging.getLogger("main")


class DryRunBroker:
    """Proxy around MT5Broker: all reads pass through to live data, all
    order-mutating calls only log what would happen and report fake success.
    Lets a full engine loop run against a live feed without sending orders."""

    def __init__(self, real):
        self._real = real

    def __getattr__(self, name):
        return getattr(self._real, name)

    def market_order(self, sig, lots, magic, deviation=20):
        log.info("[DRY-RUN] would OPEN %s %s %.2f lots entry=%.2f sl=%.2f tp=%s (magic=%d)",
                 sig.side.value, self._real.symbol, lots,
                 sig.entry, sig.stop_loss, sig.take_profit, magic)
        return -1

    def close_position(self, pos, reason=""):
        log.info("[DRY-RUN] would CLOSE ticket %s (%s)", pos.ticket, reason)
        return True

    def modify_sl(self, pos, new_sl):
        log.info("[DRY-RUN] would MOVE SL on ticket %s to %.2f", pos.ticket, new_sl)
        return True


def setup_logging(base: pathlib.Path) -> None:
    logs = base / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    fmt = "%(asctime)s %(name)s %(levelname)s %(message)s"
    logging.basicConfig(
        level=logging.INFO, format=fmt,
        handlers=[logging.StreamHandler(sys.stdout),
                  logging.FileHandler(logs / "harness.log", encoding="utf-8")])


def load_calendar(base: pathlib.Path, rel_path: str) -> list:
    p = pathlib.Path(rel_path)
    if not p.is_absolute():
        p = base / p
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            log.warning("calendar file %s unreadable — trading without it", p)
    return []


def build_strategies(name_filter: str | None) -> list:
    strategies = [cls() for cls in ALL_STRATEGIES]
    if not name_filter:
        return strategies
    wanted = {n.strip() for n in name_filter.split(",") if n.strip()}
    unknown = wanted - {s.name for s in strategies}
    if unknown:
        sys.exit(f"unknown strategy name(s): {', '.join(sorted(unknown))}\n"
                 f"available: {', '.join(s.name for s in strategies)}")
    return [s for s in strategies if s.name in wanted]


def main() -> None:
    ap = argparse.ArgumentParser(description="Gold scalper harness — 20-strategy MT5 fleet")
    ap.add_argument("--config", default=str(BASE_DIR / "config" / "settings.json"),
                    help="path to settings.json")
    ap.add_argument("--dry-run", action="store_true",
                    help="read live data but log orders instead of sending them")
    ap.add_argument("--strategies", default=None,
                    help="comma-separated strategy names to run (default: all 20)")
    args = ap.parse_args()

    setup_logging(BASE_DIR)

    cfg_path = pathlib.Path(args.config)
    try:
        settings = json.loads(cfg_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        sys.exit(f"cannot read config {cfg_path}: {e}")

    risk = RiskManager(RiskConfig(**settings.get("risk", {})),
                       state_path=BASE_DIR / "logs" / "risk_state.json")
    calendar = load_calendar(BASE_DIR, settings.get("calendar_path", "config/calendar.json"))
    strategies = build_strategies(args.strategies)

    try:
        from core.broker_mt5 import MT5Broker
        mt5_cfg = settings.get("mt5", {})
        broker = MT5Broker(symbol=settings.get("symbol", "XAUUSD"),
                           magic_base=settings.get("magic_base", 770000),
                           login=mt5_cfg.get("login"),
                           password=mt5_cfg.get("password", ""),
                           server=mt5_cfg.get("server", ""),
                           terminal_path=mt5_cfg.get("terminal_path"))
    except (ImportError, RuntimeError) as e:
        sys.exit(
            f"MT5 connection failed: {e}\n"
            "This harness needs:\n"
            "  1. Windows (the MetaTrader5 Python package is Windows-only)\n"
            "  2. A running MT5 terminal logged into your broker account\n"
            "  3. pip install MetaTrader5 pandas\n"
            "Check config/settings.json mt5.login/password/server/terminal_path.")

    if args.dry_run:
        log.info("DRY-RUN mode: no orders will be sent")
        broker = DryRunBroker(broker)
    else:
        acc = None
        try:
            import MetaTrader5 as mt5
            acc = mt5.account_info()
        except ImportError:
            pass
        is_demo = acc is not None and getattr(acc, "trade_mode", None) == 0
        if not is_demo and not settings.get("i_understand_this_is_real_money", False):
            broker.shutdown()
            sys.exit("REFUSED: this account is not a demo account.\n"
                     "Sending real orders requires  \"i_understand_this_is_real_money\": true\n"
                     "in settings.json — or use --dry-run / a demo account.")

    engine = Engine(broker, strategies, risk, base_dir=BASE_DIR, calendar=calendar)
    try:
        engine.run()
    finally:
        broker.shutdown()


if __name__ == "__main__":
    main()
