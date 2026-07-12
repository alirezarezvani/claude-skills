"""Out-of-band supervisor — reads the journal, scores each strategy, and
prepares/applies fleet decisions. Stdlib only; no MT5 or pandas dependency,
so it runs anywhere (including the Linux box the terminal isn't on).

  python supervisor.py score  [--journal logs/journal.jsonl] [--json]
  python supervisor.py review [--journal logs/journal.jsonl]
  python supervisor.py apply  --disable name1,name2 --enable name3

`score`  — activity + (if logs/deals.json is present) realized-pnl metrics
           per strategy, with mechanical DISABLE-CANDIDATE flags.
`review` — prints a ready-to-paste Claude Fable 5 review prompt embedding the
           scorecard and recent journal tail. It only prints; a human (or a
           Claude Code session) runs it and applies verdicts via `apply`.
`apply`  — flips strategies in config/enabled.json and journals the change.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import sys

BASE_DIR = pathlib.Path(__file__).resolve().parent

# Canonical fleet order — must match strategies/__init__.py ALL_STRATEGIES.
# Index = magic-number offset from magic_base; used to join logs/deals.json.
STRATEGY_ORDER = [
    "london_breakout", "ny_open_momentum", "orb_ny",
    "asian_range_break", "vol_expansion",
    "vwap_reversion", "bollinger_fade", "rsi_extreme_fade",
    "round_number_bounce", "pivot_reversion",
    "news_spike_fade", "tick_velocity_ignition", "spread_aware_liquidity",
    "dxy_divergence", "liquidity_sweep_reversal",
    "ema_ribbon_pullback", "stoch_trend_scalp", "macd_zero_cross",
    "keltner_supertrend_ride", "heikin_ashi_atr",
]


# ---------- loading ----------
def load_journal(path: pathlib.Path) -> list[dict]:
    if not path.exists():
        return []
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue                      # tolerate a torn write at the tail
    return events


def load_deals(base: pathlib.Path) -> dict[str, list[float]]:
    """logs/deals.json: list of {magic, profit} exported from MT5 history.
    Returns strategy_name -> chronological list of realized profits."""
    p = base / "logs" / "deals.json"
    if not p.exists():
        return {}
    try:
        deals = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    magic_base = 770000
    settings = base / "config" / "settings.json"
    if settings.exists():
        try:
            magic_base = json.loads(settings.read_text(encoding="utf-8")).get(
                "magic_base", magic_base)
        except (OSError, json.JSONDecodeError):
            pass
    out: dict[str, list[float]] = {}
    for d in deals:
        idx = d.get("magic", -1) - magic_base
        if 0 <= idx < len(STRATEGY_ORDER):
            out.setdefault(STRATEGY_ORDER[idx], []).append(float(d.get("profit", 0.0)))
    return out


# ---------- scoring ----------
def pnl_metrics(profits: list[float]) -> dict:
    wins = [p for p in profits if p > 0]
    losses = [p for p in profits if p < 0]
    gross_win, gross_loss = sum(wins), -sum(losses)
    peak = run = max_dd = 0.0
    for p in profits:
        run += p
        peak = max(peak, run)
        max_dd = max(max_dd, peak - run)
    return {
        "trades": len(profits),
        "pnl": round(sum(profits), 2),
        "win_pct": round(100 * len(wins) / len(profits), 1) if profits else 0.0,
        "profit_factor": (round(gross_win / gross_loss, 2) if gross_loss > 0
                          else (float("inf") if gross_win > 0 else 0.0)),
        "expectancy": round(sum(profits) / len(profits), 2) if profits else 0.0,
        "max_drawdown": round(max_dd, 2),
    }


def build_scorecard(events: list[dict], deals: dict[str, list[float]]) -> dict:
    per: dict[str, dict] = {}

    def row(name: str) -> dict:
        return per.setdefault(name, {
            "signals": 0, "vetoed": 0, "orders_filled": 0, "orders_failed": 0,
            "closes": {}, "errors": 0, "disabled_events": 0, "sl_moves": 0,
        })

    for ev in events:
        name = ev.get("strategy")
        if not name:
            continue
        kind = ev.get("kind")
        r = row(name)
        if kind == "signal":
            r["signals"] += 1
            if ev.get("vetoed"):
                r["vetoed"] += 1
        elif kind == "order":
            r["orders_filled" if ev.get("filled") else "orders_failed"] += 1
        elif kind == "close":
            reason = ev.get("reason", "unknown")
            r["closes"][reason] = r["closes"].get(reason, 0) + 1
        elif kind == "strategy_error":
            r["errors"] += 1
        elif kind == "disabled":
            r["disabled_events"] += 1
        elif kind == "sl_move":
            r["sl_moves"] += 1

    for name, profits in deals.items():
        row(name)["pnl_metrics"] = pnl_metrics(profits)

    # mechanical disable-candidate rules
    for name, r in per.items():
        flags = []
        pm = r.get("pnl_metrics")
        if pm and pm["trades"] >= 30 and pm["profit_factor"] < 0.8:
            flags.append(f"profit factor {pm['profit_factor']} < 0.8 over {pm['trades']} trades")
        if r["errors"] >= 3:
            flags.append(f"{r['errors']} errors")
        if r["signals"] >= 20:
            veto_rate = 100 * r["vetoed"] / r["signals"]
            if veto_rate > 80:
                flags.append(f"veto rate {veto_rate:.0f}% over {r['signals']} signals")
        r["disable_candidate"] = bool(flags)
        r["flags"] = flags

    halts = sum(1 for ev in events if ev.get("kind") == "halt")
    return {"generated": dt.datetime.now(dt.timezone.utc).isoformat(),
            "events_total": len(events), "halts": halts,
            "strategies": per}


def print_table(card: dict) -> None:
    per = card["strategies"]
    header = (f"{'strategy':<26}{'sig':>5}{'veto':>6}{'fill':>6}{'close':>7}"
              f"{'err':>5}{'pnl':>10}{'pf':>7}{'win%':>7}  flags")
    print(header)
    print("-" * len(header))
    for name in sorted(per):
        r = per[name]
        pm = r.get("pnl_metrics", {})
        pf = pm.get("profit_factor", "")
        print(f"{name:<26}{r['signals']:>5}{r['vetoed']:>6}{r['orders_filled']:>6}"
              f"{sum(r['closes'].values()):>7}{r['errors']:>5}"
              f"{pm.get('pnl', ''):>10}{pf if pf != '' else '':>7}"
              f"{pm.get('win_pct', ''):>7}  "
              f"{'DISABLE-CANDIDATE: ' + '; '.join(r['flags']) if r['disable_candidate'] else ''}")
    print(f"\n{card['events_total']} journal events, {card['halts']} halts, "
          f"{sum(1 for r in per.values() if r['disable_candidate'])} disable candidate(s)")


# ---------- subcommands ----------
def cmd_score(args) -> int:
    events = load_journal(args.journal)
    if not events:
        print("no data yet")
        return 0
    card = build_scorecard(events, load_deals(BASE_DIR))
    if args.json:
        print(json.dumps(card, indent=2))
    else:
        print_table(card)
    return 0


REVIEW_INSTRUCTIONS = """\
You are the supervisor of a 20-strategy gold scalping fleet running on one
MT5 account. Below are the fleet scorecard (aggregated from the trade
journal, with realized-pnl metrics where MT5 deal history was exported) and
the last 50 raw journal events.

For each strategy flagged DISABLE-CANDIDATE - and any other strategy whose
record concerns you - decide: keep, disable, or tune. Base the decision on
the evidence shown (profit factor, expectancy, drawdown, error counts, veto
rates, close reasons), not on priors about the strategy style. A high veto
rate may mean the risk gate is doing its job during a crowded regime, not
that the strategy is broken - reason about cause before disabling.

Output a JSON object mapping strategy name to verdict, e.g.
{"news_spike_fade": "disable", "vwap_reversion": "keep", "orb_ny": "tune: widen ORB window"}
with one short sentence of reasoning per entry. A human will apply verdicts
with: python supervisor.py apply --disable <names> --enable <names>
"""


def cmd_review(args) -> int:
    events = load_journal(args.journal)
    if not events:
        print("no data yet")
        return 0
    card = build_scorecard(events, load_deals(BASE_DIR))
    print(REVIEW_INSTRUCTIONS)
    print("=== SCORECARD ===")
    print(json.dumps(card, indent=2))
    print("\n=== LAST 50 JOURNAL EVENTS ===")
    for ev in events[-50:]:
        print(json.dumps(ev))
    return 0


def cmd_apply(args) -> int:
    disable = [n.strip() for n in (args.disable or "").split(",") if n.strip()]
    enable = [n.strip() for n in (args.enable or "").split(",") if n.strip()]
    if not disable and not enable:
        print("nothing to apply — pass --disable and/or --enable")
        return 1
    unknown = [n for n in disable + enable if n not in STRATEGY_ORDER]
    if unknown:
        print(f"unknown strategy name(s): {', '.join(unknown)}")
        return 1

    enabled_path = BASE_DIR / "config" / "enabled.json"
    enabled_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        current = json.loads(enabled_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        current = {}

    changes = {}
    for name in disable:
        if current.get(name, True) is not False:
            changes[name] = False
    for name in enable:
        if current.get(name, True) is not True:
            changes[name] = True

    if not changes:
        print("no changes — enabled.json already matches")
        return 0

    for name, value in changes.items():
        old = current.get(name, True)
        print(f"  {name}: {old} -> {value}")
        current[name] = value
    enabled_path.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {enabled_path}")

    journal_path = BASE_DIR / "logs" / "journal.jsonl"
    journal_path.parent.mkdir(parents=True, exist_ok=True)
    rec = {"ts": dt.datetime.now(dt.timezone.utc).isoformat(),
           "kind": "supervisor_apply", "changes": changes}
    with journal_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Journal analyzer / fleet supervisor")
    sub = ap.add_subparsers(dest="command", required=True)

    default_journal = BASE_DIR / "logs" / "journal.jsonl"
    p_score = sub.add_parser("score", help="per-strategy scorecard from the journal")
    p_score.add_argument("--journal", type=pathlib.Path, default=default_journal)
    p_score.add_argument("--json", action="store_true", help="machine-readable output")
    p_score.set_defaults(fn=cmd_score)

    p_review = sub.add_parser("review", help="print a Claude Fable 5 review prompt")
    p_review.add_argument("--journal", type=pathlib.Path, default=default_journal)
    p_review.set_defaults(fn=cmd_review)

    p_apply = sub.add_parser("apply", help="flip strategies in config/enabled.json")
    p_apply.add_argument("--disable", default="", help="comma-separated names to disable")
    p_apply.add_argument("--enable", default="", help="comma-separated names to enable")
    p_apply.set_defaults(fn=cmd_apply)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
