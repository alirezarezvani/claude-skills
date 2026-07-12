#!/usr/bin/env python3
"""Single-file HTML dashboard generator for the gold-scalper fleet.

Reads the engine journal (logs/journal.jsonl), the fleet switchboard
(config/enabled.json), optional realized-deal history (logs/deals.json,
exported from MT5: list of {magic, profit, time}) and optional
config/settings.json, and renders one self-contained HTML file:

    python dashboard.py [--journal logs/journal.jsonl]
                        [--deals logs/deals.json]
                        [--enabled config/enabled.json]
                        [--out logs/dashboard.html]
                        [--refresh 10]

Discipline (markdown-html rules): single file, zero framework runtimes,
inline CSS custom-property design tokens, Google Fonts is the only external,
WCAG AA >= 4.5:1 contrast, prefers-reduced-motion honored. Stdlib only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import pathlib
import sys

BASE_DIR = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Reuse the supervisor's aggregation if importable; otherwise carry a
# faithful stdlib copy so this file also works extracted on its own.
try:
    from supervisor import STRATEGY_ORDER, build_scorecard  # type: ignore
except Exception:                                            # pragma: no cover
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

    def _pnl_metrics(profits):
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

    def build_scorecard(events, deals):
        per = {}

        def row(name):
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
            row(name)["pnl_metrics"] = _pnl_metrics(profits)

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
                "events_total": len(events), "halts": halts, "strategies": per}


# Fleet taxonomy — canonical order groups of five (mirrors strategies/__init__).
CATEGORY_SLICES = [("breakout", 0, 5), ("reversion", 5, 10),
                   ("event", 10, 15), ("trend", 15, 20)]
CATEGORY_OF = {name: cat for cat, lo, hi in CATEGORY_SLICES
               for name in STRATEGY_ORDER[lo:hi]}

KIND_CLASS = {
    "engine_start": "neutral", "engine_stop": "neutral",
    "signal": "gold", "order": "info", "close": "up", "sl_move": "neutral",
    "strategy_error": "down", "disabled": "warn", "halt": "down",
    "supervisor_apply": "info",
}

esc = html.escape


# ---------------------------------------------------------------- loading ---
def load_journal_counted(path: pathlib.Path):
    """Journal events + count of malformed/torn lines that were skipped."""
    if not path.exists():
        return [], 0
    events, skipped = [], 0
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
            if isinstance(ev, dict):
                events.append(ev)
            else:
                skipped += 1
        except json.JSONDecodeError:
            skipped += 1
    return events, skipped


def load_deals(path: pathlib.Path, magic_base: int):
    """Returns (name -> [profits] in time order, chronological deal list)."""
    if not path.exists():
        return {}, []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}, []
    deals = []
    for d in raw if isinstance(raw, list) else []:
        if not isinstance(d, dict):
            continue
        idx = int(d.get("magic", -1)) - magic_base
        if 0 <= idx < len(STRATEGY_ORDER):
            deals.append({"strategy": STRATEGY_ORDER[idx],
                          "profit": float(d.get("profit", 0.0)),
                          "time": str(d.get("time", ""))})
    deals.sort(key=lambda d: d["time"])
    per: dict[str, list[float]] = {}
    for d in deals:
        per.setdefault(d["strategy"], []).append(d["profit"])
    return per, deals


def load_json_or(path: pathlib.Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def fleet_state(events):
    """Last engine_start / engine_stop / halt wins."""
    state, reason, last_ts = "NO DATA", "", None
    for ev in events:
        k = ev.get("kind")
        if k == "engine_start":
            state, reason = "RUNNING", ""
        elif k == "engine_stop":
            state, reason = "STOPPED", ""
        elif k == "halt":
            state, reason = "HALTED", str(ev.get("reason", ""))
        ts = ev.get("ts")
        if ts:
            last_ts = str(ts)
    return state, reason, last_ts


def parse_ts(ts: str):
    try:
        d = dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=dt.timezone.utc)
    except (ValueError, AttributeError):
        return None


# ------------------------------------------------------------- formatting ---
def money(v: float) -> str:
    return f"{v:+,.2f}"


def ts_html(ts: str, long_fmt: bool = False) -> str:
    d = parse_ts(ts)
    if d is None:
        return esc(ts)
    utc = d.astimezone(dt.timezone.utc)
    label = utc.strftime("%b %d %H:%M:%S" if long_fmt else "%H:%M:%S")
    extra = ' data-long="1"' if long_fmt else ""
    return (f'<time datetime="{esc(ts)}">{label} UTC</time>'
            f' <span class="local" data-ts="{esc(ts)}"{extra}></span>')


# ------------------------------------------------------------- SVG charts ---
def _yticks(lo: float, hi: float, n: int = 4):
    if hi <= lo:
        hi = lo + 1.0
    step = (hi - lo) / n
    return [lo + i * step for i in range(n + 1)]


def equity_svg(deals: list) -> str:
    """Cumulative realized P&L line + shared-x underwater drawdown area."""
    W, PL, PR = 960, 66, 14
    T, H_EQ, GAP, H_DD, B = 16, 208, 34, 92, 24
    H = T + H_EQ + GAP + H_DD + B
    plot_w = W - PL - PR
    n = len(deals)
    cum, run = [], 0.0
    for d in deals:
        run += d["profit"]
        cum.append(run)
    peaks, peak = [], float("-inf")
    for c in cum:
        peak = max(peak, c)
        peaks.append(peak)
    dds = [c - p for c, p in zip(cum, peaks)]          # <= 0
    lo, hi = min(0.0, min(cum)), max(0.0, max(cum))
    dd_lo = min(dds) if dds else 0.0
    if dd_lo == 0.0:
        dd_lo = -1.0

    def x(i):
        return PL + (plot_w * i / (n - 1) if n > 1 else plot_w / 2)

    def y_eq(v):
        return T + H_EQ * (1 - (v - lo) / (hi - lo or 1))

    def y_dd(v):
        return T + H_EQ + GAP + H_DD * (v / dd_lo)

    parts = []
    # equity gridlines + labels
    for tv in _yticks(lo, hi):
        yy = y_eq(tv)
        parts.append(f'<line class="grid" x1="{PL}" y1="{yy:.1f}" x2="{W - PR}" y2="{yy:.1f}"/>')
        parts.append(f'<text class="ax" x="{PL - 8}" y="{yy + 4:.1f}" text-anchor="end">{money(tv)}</text>')
    zy = y_eq(0)
    parts.append(f'<line class="zero" x1="{PL}" y1="{zy:.1f}" x2="{W - PR}" y2="{zy:.1f}"/>')
    # equity line, gold; soft fill down to zero line
    pts = " ".join(f"{x(i):.1f},{y_eq(c):.1f}" for i, c in enumerate(cum))
    area = f"M{x(0):.1f},{zy:.1f} L" + " L".join(
        f"{x(i):.1f},{y_eq(c):.1f}" for i, c in enumerate(cum)) + f" L{x(n - 1):.1f},{zy:.1f} Z"
    parts.append(f'<path class="eq-fill" d="{area}"/>')
    parts.append(f'<polyline class="eq-line" points="{pts}"/>')
    for i, d in enumerate(deals):
        cls = "pt up" if d["profit"] >= 0 else "pt down"
        tip = (f"{d['strategy']}  {d['time']}\n"
               f"deal {money(d['profit'])}   cumulative {money(cum[i])}")
        parts.append(f'<circle class="{cls}" cx="{x(i):.1f}" cy="{y_eq(cum[i]):.1f}" r="3">'
                     f'<title>{esc(tip)}</title></circle>')
    # drawdown pane
    dz = T + H_EQ + GAP
    parts.append(f'<line class="zero" x1="{PL}" y1="{dz}" x2="{W - PR}" y2="{dz}"/>')
    for tv in (dd_lo / 2, dd_lo):
        yy = y_dd(tv)
        parts.append(f'<line class="grid" x1="{PL}" y1="{yy:.1f}" x2="{W - PR}" y2="{yy:.1f}"/>')
        parts.append(f'<text class="ax" x="{PL - 8}" y="{yy + 4:.1f}" text-anchor="end">{money(tv)}</text>')
    dd_area = f"M{x(0):.1f},{dz} L" + " L".join(
        f"{x(i):.1f},{y_dd(v):.1f}" for i, v in enumerate(dds)) + f" L{x(n - 1):.1f},{dz} Z"
    parts.append(f'<path class="dd-fill" d="{dd_area}"/>')
    for i, v in enumerate(dds):
        if v < 0:
            parts.append(f'<circle class="pt dd" cx="{x(i):.1f}" cy="{y_dd(v):.1f}" r="2.5">'
                         f'<title>{esc(deals[i]["time"])}\ndrawdown {money(v)}</title></circle>')
    parts.append(f'<text class="ax lbl" x="{PL}" y="{T - 4}">cumulative realized P&amp;L</text>')
    parts.append(f'<text class="ax lbl" x="{PL}" y="{dz - 6}">underwater drawdown</text>')
    if deals:
        parts.append(f'<text class="ax" x="{PL}" y="{H - 6}">{esc(deals[0]["time"][:16])}</text>')
        parts.append(f'<text class="ax" x="{W - PR}" y="{H - 6}" text-anchor="end">{esc(deals[-1]["time"][:16])}</text>')
    label = f"Equity curve: {n} deals, net {money(cum[-1])}, max drawdown {money(min(dds))}"
    return (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{esc(label)}" '
            f'preserveAspectRatio="xMidYMid meet">{"".join(parts)}</svg>')


def activity_svg(events: list) -> str:
    """Fallback sparkline: journal events bucketed per hour."""
    buckets: dict[str, int] = {}
    for ev in events:
        ts = str(ev.get("ts", ""))
        if len(ts) >= 13:
            buckets[ts[:13]] = buckets.get(ts[:13], 0) + 1
    keys = sorted(buckets)
    W, H, PL, T, B = 960, 180, 66, 16, 24
    plot_w, plot_h = W - PL - 14, H - T - B
    n, mx = len(keys), max(buckets.values(), default=1)
    parts = []
    bw = max(4.0, min(38.0, plot_w / max(n, 1) - 4))
    for i, k in enumerate(keys):
        v = buckets[k]
        bh = plot_h * v / mx
        bx = PL + (plot_w * i / max(n - 1, 1)) - bw / 2 if n > 1 else PL + plot_w / 2 - bw / 2
        parts.append(f'<rect class="bar" x="{bx:.1f}" y="{T + plot_h - bh:.1f}" '
                     f'width="{bw:.1f}" height="{bh:.1f}" rx="2">'
                     f'<title>{esc(k)}:00 UTC — {v} events</title></rect>')
    parts.append(f'<line class="zero" x1="{PL}" y1="{T + plot_h}" x2="{W - 14}" y2="{T + plot_h}"/>')
    parts.append(f'<text class="ax" x="{PL - 8}" y="{T + 8}" text-anchor="end">{mx}</text>')
    parts.append(f'<text class="ax lbl" x="{PL}" y="{T - 4}">journal events per hour</text>')
    if keys:
        parts.append(f'<text class="ax" x="{PL}" y="{H - 6}">{esc(keys[0])}:00</text>')
        parts.append(f'<text class="ax" x="{W - 14}" y="{H - 6}" text-anchor="end">{esc(keys[-1])}:00</text>')
    return (f'<svg viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="Journal activity per hour, peak {mx} events">{"".join(parts)}</svg>')


# ------------------------------------------------------------- HTML parts ---
def close_bucket(reason: str) -> str:
    r = reason.lower()
    if "tp" in r or "take" in r:
        return "tp"
    if r == "sl" or "stop_loss" in r or ("sl" in r and "move" not in r and "trail" not in r):
        return "sl"
    if "time" in r:
        return "time"
    return "other"


def fleet_table(per: dict, enabled: dict, deals_present: bool) -> str:
    head_cells = [
        ("strategy", "s", "Strategy"), ("cat", "s", "Category"),
        ("state", "s", "State"), ("signals", "n", "Signals"),
        ("veto", "n", "Veto rate"), ("orders", "n", "Orders"),
        ("closes", "n", "Closes tp/sl/time/other"), ("errors", "n", "Errors"),
    ]
    if deals_present:
        head_cells += [("pnl", "n", "P&amp;L"), ("pf", "n", "PF")]
    ths = "".join(
        f'<th data-k="{k}" data-t="{t}" scope="col" aria-sort="none">{lbl}'
        f'<span class="arrow" aria-hidden="true"></span></th>'
        for k, t, lbl in head_cells)

    rows = []
    for name in STRATEGY_ORDER:
        r = per.get(name, {"signals": 0, "vetoed": 0, "orders_filled": 0,
                           "orders_failed": 0, "closes": {}, "errors": 0,
                           "sl_moves": 0, "flags": [], "disable_candidate": False})
        cat = CATEGORY_OF.get(name, "other")
        is_on = bool(enabled.get(name, True))
        sig, veto = r["signals"], r["vetoed"]
        veto_pct = 100.0 * veto / sig if sig else 0.0
        orders = r["orders_filled"] + r["orders_failed"]
        buckets = {"tp": 0, "sl": 0, "time": 0, "other": 0}
        for reason, cnt in r.get("closes", {}).items():
            buckets[close_bucket(str(reason))] += cnt
        closes_total = sum(buckets.values())
        flags = r.get("flags", [])
        flagged = bool(r.get("disable_candidate"))
        row_cls = ' class="flagged"' if flagged else ""
        flag_note = (f'<div class="flagnote">&#9888; DISABLE-CANDIDATE: '
                     f'{esc("; ".join(flags))}</div>') if flagged else ""
        state_txt = "on" if is_on else "off"
        state = (f'<span class="dot {"on" if is_on else "off"}" aria-hidden="true"></span>'
                 f'<span class="statetxt">{state_txt}</span>')
        veto_bar = (f'<div class="micro" role="img" aria-label="veto rate {veto_pct:.0f} percent">'
                    f'<div class="micro-fill" style="width:{veto_pct:.0f}%"></div></div>'
                    f'<span class="num">{veto_pct:.0f}%</span>' if sig else
                    '<span class="num muted">&mdash;</span>')
        if closes_total:
            segs = "".join(
                f'<div class="seg {b}" style="width:{100 * buckets[b] / closes_total:.1f}%"></div>'
                for b in ("tp", "sl", "time", "other") if buckets[b])
            closes_tip = " / ".join(f"{b}:{buckets[b]}" for b in ("tp", "sl", "time", "other"))
            closes_cell = (f'<div class="stack" title="{esc(closes_tip)}" role="img" '
                           f'aria-label="closes {esc(closes_tip)}">{segs}</div>'
                           f'<span class="num">{closes_total}</span>')
        else:
            closes_cell = '<span class="num muted">&mdash;</span>'
        cells = [
            f'<td data-v="{esc(name)}"><span class="sname">{esc(name)}</span>{flag_note}</td>',
            f'<td data-v="{cat}"><span class="badge cat-{cat}">{cat}</span></td>',
            f'<td data-v="{state_txt}">{state}</td>',
            f'<td class="num" data-v="{sig}">{sig}</td>',
            f'<td data-v="{veto_pct:.1f}">{veto_bar}</td>',
            f'<td class="num" data-v="{orders}">{orders}'
            + (f'<span class="muted"> ({r["orders_failed"]}&#10007;)</span>' if r["orders_failed"] else "")
            + '</td>',
            f'<td data-v="{closes_total}">{closes_cell}</td>',
            f'<td class="num{" bad" if r["errors"] >= 3 else ""}" data-v="{r["errors"]}">{r["errors"]}</td>',
        ]
        if deals_present:
            pm = r.get("pnl_metrics")
            if pm:
                pnl, pf = pm["pnl"], pm["profit_factor"]
                pf_v = 999999 if pf == float("inf") else pf
                pf_s = "&#8734;" if pf == float("inf") else f"{pf:.2f}"
                pcls = "up" if pnl >= 0 else "down"
                cells.append(f'<td class="num {pcls}" data-v="{pnl}">{money(pnl)}</td>')
                cells.append(f'<td class="num" data-v="{pf_v}" '
                             f'title="{pm["trades"]} trades, win {pm["win_pct"]}%, '
                             f'expectancy {money(pm["expectancy"])}">{pf_s}</td>')
            else:
                cells.append('<td class="num muted" data-v="-1e18">&mdash;</td>')
                cells.append('<td class="num muted" data-v="-1e18">&mdash;</td>')
        title = f' title="{esc("; ".join(flags))}"' if flagged else ""
        rows.append(f"<tr{row_cls} data-name=\"{esc(name)}\"{title}>{''.join(cells)}</tr>")

    return (f'<table id="fleet" aria-label="Strategy fleet scorecard">'
            f'<thead><tr>{ths}</tr></thead><tbody>{"".join(rows)}</tbody></table>')


def event_detail(ev: dict) -> str:
    skip = {"ts", "kind", "strategy"}
    bits = []
    for k, v in ev.items():
        if k in skip:
            continue
        if isinstance(v, float):
            v = f"{v:g}"
        bits.append(f'<span class="kv"><span class="k">{esc(str(k))}</span>={esc(str(v))}</span>')
    return " ".join(bits)


def event_stream(events: list) -> str:
    last = list(reversed(events[-100:]))
    kinds = sorted({str(ev.get("kind", "?")) for ev in last})
    btns = ['<button type="button" data-kind="all" class="on" aria-pressed="true">all</button>']
    btns += [f'<button type="button" data-kind="{esc(k)}" aria-pressed="false">{esc(k)}</button>'
             for k in kinds]
    rows = []
    for ev in last:
        kind = str(ev.get("kind", "?"))
        cls = KIND_CLASS.get(kind, "neutral")
        strat = ev.get("strategy")
        strat_html = f'<span class="estrat">{esc(str(strat))}</span>' if strat else ""
        rows.append(
            f'<tr data-kind="{esc(kind)}">'
            f'<td class="ets">{ts_html(str(ev.get("ts", "")))}</td>'
            f'<td><span class="badge kb-{cls}">{esc(kind)}</span></td>'
            f'<td>{strat_html}</td>'
            f'<td class="edetail">{event_detail(ev)}</td></tr>')
    if not rows:
        rows.append('<tr><td colspan="4" class="empty">No journal events yet.</td></tr>')
    return (f'<div class="efilter" role="group" aria-label="Filter events by kind">{"".join(btns)}</div>'
            f'<div class="escroll"><table id="events" aria-label="Last 100 journal events, newest first">'
            f'<thead><tr><th scope="col">time</th><th scope="col">kind</th>'
            f'<th scope="col">strategy</th><th scope="col">detail</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')


def risk_panel(settings, events: list, halts: int) -> str:
    risk = (settings or {}).get("risk", {}) if isinstance(settings, dict) else {}
    labels = [
        ("max_risk_per_trade_pct", "risk / trade", "%"),
        ("max_daily_loss_pct", "max daily loss", "%"),
        ("max_weekly_loss_pct", "max weekly loss", "%"),
        ("max_open_positions", "max open positions", ""),
        ("max_same_direction", "max same direction", ""),
        ("max_total_volume_lots", "max total volume", " lots"),
        ("min_equity", "min equity", ""),
        ("news_blackout", "news blackout", ""),
    ]
    items = []
    for key, lbl, unit in labels:
        v = risk.get(key)
        if v is None:
            continue
        if isinstance(v, bool):
            v = "on" if v else "off"
        items.append(f'<div class="riskrow"><dt>{esc(lbl)}</dt>'
                     f'<dd class="num">{esc(str(v))}{unit}</dd></div>')
    body = (f'<dl class="risklist">{"".join(items)}</dl>' if items else
            '<p class="empty">config/settings.json not readable &mdash; '
            'circuit-breaker limits unknown.</p>')
    recent_halts = [ev for ev in events if ev.get("kind") == "halt"][-3:]
    hrows = "".join(
        f'<li>{ts_html(str(ev.get("ts", "")), long_fmt=True)} &mdash; '
        f'{esc(str(ev.get("reason", "")))}</li>' for ev in reversed(recent_halts))
    halt_html = (f'<div class="halts"><h3>{halts} halt{"s" if halts != 1 else ""} in journal</h3>'
                 f'<ul>{hrows}</ul></div>' if halts else
                 '<p class="okline"><span class="dot on" aria-hidden="true"></span>'
                 'No circuit-breaker halts in journal.</p>')
    return body + halt_html


# ------------------------------------------------------------ CSS + JS -----
CSS = """
:root{
  --bg:#0b0e14; --surface:#121722; --surface-2:#1a2130; --border:#252e40;
  --text:#e7eaf1; --muted:#9aa3b5;
  --gold:#d4af37; --gold-soft:rgba(212,175,55,.13);
  --up:#63c97e; --down:#f0716f; --warn:#e5b567; --info:#72b9ee;
  --shadow:0 1px 0 rgba(0,0,0,.4);
}
@media (prefers-color-scheme: light){
  :root{
    --bg:#f6f5f1; --surface:#ffffff; --surface-2:#efede6; --border:#d9d5c9;
    --text:#1d222c; --muted:#59627a;
    --gold:#7c5f10; --gold-soft:rgba(124,95,16,.10);
    --up:#1e7c3d; --down:#c22f2c; --warn:#8a5a00; --info:#175f9e;
    --shadow:0 1px 2px rgba(0,0,0,.06);
  }
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--bg); color:var(--text);
  font:14px/1.5 'Inter',system-ui,sans-serif;
  font-variant-numeric:tabular-nums;
}
.num,td.num,time,.local,.ets,.edetail,.kv,.riskrow dd,.big{
  font-family:'JetBrains Mono',ui-monospace,monospace;
}
a{color:var(--gold)}
:focus-visible{outline:2px solid var(--gold); outline-offset:2px; border-radius:3px}
.wrap{max-width:1240px; margin:0 auto; padding:20px 22px 40px}
.grid{display:grid; grid-template-columns:minmax(0,2.1fr) minmax(0,1fr); gap:16px}
.full{grid-column:1/-1}
@media (max-width:900px){ .grid{grid-template-columns:minmax(0,1fr)} }
section.panel{
  background:var(--surface); border:1px solid var(--border); border-radius:10px;
  padding:16px 18px; box-shadow:var(--shadow); min-width:0;
}
h1{font-size:19px; font-weight:600; letter-spacing:.02em; margin:0}
h1 .sym{color:var(--gold)}
h2{font-size:12px; font-weight:600; letter-spacing:.14em; text-transform:uppercase;
   color:var(--muted); margin:0 0 12px; border-bottom:1px solid var(--border);
   padding-bottom:8px}
h3{font-size:13px; margin:14px 0 6px}
.muted{color:var(--muted)}
/* ---------- header ---------- */
header.top{display:flex; flex-wrap:wrap; gap:14px 22px; align-items:center; margin-bottom:14px}
.pill{
  display:inline-flex; align-items:center; gap:8px; padding:5px 14px;
  border-radius:999px; border:1px solid var(--border); font-weight:600;
  font-size:13px; letter-spacing:.06em; background:var(--surface);
}
.pill .dot{width:9px;height:9px;border-radius:50%}
.pill.run{color:var(--up); border-color:var(--up)}
.pill.halt{color:var(--down); border-color:var(--down); background:color-mix(in srgb,var(--down) 12%,var(--surface))}
.pill.stop,.pill.nodata{color:var(--muted)}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px;vertical-align:baseline}
.dot.on{background:var(--up)} .dot.off{background:var(--muted)}
.stats{display:flex; flex-wrap:wrap; gap:10px 26px; margin-left:auto}
.stat{min-width:72px}
.stat .lbl{font-size:10px; letter-spacing:.12em; text-transform:uppercase; color:var(--muted)}
.stat .big{font-size:17px; font-weight:600}
.stat .big.up{color:var(--up)} .stat .big.down{color:var(--down)}
#stale,.banner{
  border-radius:8px; padding:10px 16px; margin:0 0 14px; font-weight:600;
}
.banner.halt{
  background:color-mix(in srgb,var(--down) 16%,var(--surface));
  border:1px solid var(--down); color:var(--down); font-size:15px;
}
#stale{
  background:color-mix(in srgb,var(--warn) 14%,var(--surface));
  border:1px solid var(--warn); color:var(--warn);
}
/* ---------- charts ---------- */
svg{width:100%; height:auto; display:block}
.grid-l,.grid{stroke:var(--border)}
svg .grid{stroke:var(--border); stroke-width:1}
svg .zero{stroke:var(--muted); stroke-width:1; stroke-dasharray:4 3}
svg .ax{fill:var(--muted); font:10.5px 'JetBrains Mono',monospace}
svg .ax.lbl{letter-spacing:.1em; text-transform:uppercase; fill:var(--gold)}
svg .eq-line{fill:none; stroke:var(--gold); stroke-width:2; stroke-linejoin:round}
svg .eq-fill{fill:var(--gold-soft)}
svg .dd-fill{fill:color-mix(in srgb,var(--down) 30%,transparent); stroke:var(--down); stroke-width:1}
svg .pt{fill:var(--gold); stroke:var(--bg); stroke-width:1}
svg .pt.up{fill:var(--up)} svg .pt.down{fill:var(--down)} svg .pt.dd{fill:var(--down)}
svg .bar{fill:var(--gold)}
.chartnote{font-size:12px; color:var(--muted); margin:8px 0 0}
/* ---------- fleet table ---------- */
.tscroll,.escroll{overflow-x:auto}
table{border-collapse:collapse; width:100%; font-size:13px}
th,td{padding:7px 10px; text-align:left; border-bottom:1px solid var(--border); white-space:nowrap}
th{
  font-size:10.5px; letter-spacing:.1em; text-transform:uppercase; color:var(--muted);
  cursor:pointer; user-select:none; position:sticky; top:0; background:var(--surface);
}
th .arrow::after{content:''; margin-left:4px}
th[data-dir=asc] .arrow::after{content:'\\2191'}
th[data-dir=desc] .arrow::after{content:'\\2193'}
tbody tr:hover{background:var(--surface-2)}
td.num{text-align:right}
td .up{color:var(--up)} td .down{color:var(--down)}
td.num.up{color:var(--up)} td.num.down{color:var(--down)} td.num.bad{color:var(--down);font-weight:600}
tr.flagged td:first-child{box-shadow:inset 3px 0 0 var(--warn)}
.sname{font-family:'JetBrains Mono',monospace; font-size:12.5px}
.flagnote{font-size:11px; color:var(--warn); white-space:normal; max-width:340px}
.badge{
  display:inline-block; padding:1px 8px; border-radius:4px; font-size:10.5px;
  font-weight:600; letter-spacing:.08em; text-transform:uppercase;
  border:1px solid var(--border); color:var(--muted);
}
.cat-breakout{color:var(--gold); border-color:var(--gold)}
.cat-reversion{color:var(--info); border-color:var(--info)}
.cat-event{color:var(--warn); border-color:var(--warn)}
.cat-trend{color:var(--up); border-color:var(--up)}
.micro{
  display:inline-block; width:64px; height:7px; border-radius:4px;
  background:var(--surface-2); border:1px solid var(--border);
  vertical-align:middle; margin-right:7px; overflow:hidden;
}
.micro-fill{height:100%; background:var(--warn)}
.stack{
  display:inline-flex; width:72px; height:9px; border-radius:4px; overflow:hidden;
  border:1px solid var(--border); vertical-align:middle; margin-right:7px;
}
.seg.tp{background:var(--up)} .seg.sl{background:var(--down)}
.seg.time{background:var(--warn)} .seg.other{background:var(--muted)}
.legend{font-size:11px; color:var(--muted); margin-top:8px}
.legend .seg{display:inline-block; width:9px; height:9px; border-radius:2px;
  vertical-align:baseline; margin:0 4px 0 10px}
/* ---------- events ---------- */
.efilter{display:flex; flex-wrap:wrap; gap:6px; margin-bottom:10px}
.efilter button{
  background:var(--surface-2); color:var(--text); border:1px solid var(--border);
  border-radius:999px; padding:3px 12px; font:600 11.5px 'JetBrains Mono',monospace;
  cursor:pointer;
}
.efilter button.on{border-color:var(--gold); color:var(--gold); background:var(--gold-soft)}
#events{font-size:12.5px}
#events td{padding:4px 10px}
.edetail{white-space:normal; max-width:640px; color:var(--muted); word-break:break-word}
.kv .k{color:var(--gold)}
.estrat{font-family:'JetBrains Mono',monospace}
.kb-gold{color:var(--gold); border-color:var(--gold)}
.kb-info{color:var(--info); border-color:var(--info)}
.kb-up{color:var(--up); border-color:var(--up)}
.kb-down{color:var(--down); border-color:var(--down)}
.kb-warn{color:var(--warn); border-color:var(--warn)}
.escroll{max-height:520px; overflow-y:auto}
.local{color:var(--muted); font-size:11px}
/* ---------- risk ---------- */
.risklist{margin:0}
.riskrow{display:flex; justify-content:space-between; gap:12px;
  border-bottom:1px dotted var(--border); padding:5px 0}
.riskrow dt{color:var(--muted)} .riskrow dd{margin:0; font-weight:600}
.halts ul{margin:4px 0 0; padding-left:18px}
.halts li{color:var(--down); font-size:12.5px; margin:3px 0}
.halts h3{color:var(--down)}
.okline{color:var(--up); font-size:13px}
.empty{color:var(--muted); font-style:italic; padding:14px 4px}
footer{margin-top:22px; font-size:12px; color:var(--muted);
  border-top:1px solid var(--border); padding-top:12px;
  display:flex; flex-wrap:wrap; gap:6px 24px}
@media (prefers-reduced-motion: no-preference){
  tbody tr,.efilter button{transition:background-color .15s ease, color .15s ease}
}
@media (prefers-reduced-motion: reduce){
  *,*::before,*::after{animation:none!important; transition:none!important; scroll-behavior:auto!important}
}
"""

JS = """
(function(){
'use strict';
function initSort(){
  var table=document.getElementById('fleet'); if(!table) return;
  var ths=table.querySelectorAll('th[data-k]');
  ths.forEach(function(th,i){
    th.tabIndex=0;
    function go(){
      var dir=th.dataset.dir==='asc'?'desc':'asc';
      ths.forEach(function(o){o.removeAttribute('data-dir');o.setAttribute('aria-sort','none');});
      th.dataset.dir=dir;
      th.setAttribute('aria-sort',dir==='asc'?'ascending':'descending');
      var tb=table.tBodies[0], rows=Array.prototype.slice.call(tb.rows);
      var numeric=th.dataset.t==='n';
      rows.sort(function(a,b){
        var av=a.cells[i].dataset.v, bv=b.cells[i].dataset.v, c;
        if(numeric){ c=(parseFloat(av)||0)-(parseFloat(bv)||0); }
        else{ c=String(av||'').localeCompare(String(bv||'')); }
        return dir==='asc'?c:-c;
      });
      rows.forEach(function(r){tb.appendChild(r);});
    }
    th.addEventListener('click',go);
    th.addEventListener('keydown',function(e){
      if(e.key==='Enter'||e.key===' '){e.preventDefault();go();}
    });
  });
}
function initFilter(){
  var btns=document.querySelectorAll('.efilter button');
  btns.forEach(function(b){
    b.addEventListener('click',function(){
      btns.forEach(function(o){o.classList.remove('on');o.setAttribute('aria-pressed','false');});
      b.classList.add('on'); b.setAttribute('aria-pressed','true');
      var k=b.dataset.kind;
      document.querySelectorAll('#events tbody tr').forEach(function(r){
        r.style.display=(k==='all'||r.dataset.kind===k)?'':'none';
      });
    });
  });
}
function initTimes(){
  var fShort=new Intl.DateTimeFormat(undefined,{hour:'2-digit',minute:'2-digit',second:'2-digit'});
  var fLong=new Intl.DateTimeFormat(undefined,{month:'short',day:'2-digit',hour:'2-digit',minute:'2-digit'});
  document.querySelectorAll('.local[data-ts]').forEach(function(el){
    var d=new Date(el.dataset.ts);
    if(!isNaN(d)) el.textContent='\\u00b7 '+(el.dataset.long?fLong:fShort).format(d)+' local';
  });
}
function initStale(){
  var ts=document.body.dataset.lastEvent, w=document.getElementById('stale');
  if(!ts||!w) return;
  var age=(Date.now()-new Date(ts).getTime())/60000;
  if(age>5){ w.hidden=false;
    var s=w.querySelector('[data-age]'); if(s) s.textContent=Math.round(age)+' min'; }
}
initSort(); initFilter(); initTimes(); initStale();
})();
"""


# --------------------------------------------------------------- assembly ---
def build_page(*, events, skipped, card, enabled, settings, deals_list,
               deals_present, refresh, journal_path, out_path) -> str:
    now = dt.datetime.now(dt.timezone.utc)
    state, halt_reason, last_ts = fleet_state(events)
    per = card["strategies"]

    n_enabled = sum(1 for n in STRATEGY_ORDER if enabled.get(n, True))
    n_disabled = len(STRATEGY_ORDER) - n_enabled
    n_tripped = sum(1 for n in STRATEGY_ORDER if per.get(n, {}).get("errors", 0) >= 3)

    pill_cls = {"RUNNING": "run", "HALTED": "halt", "STOPPED": "stop"}.get(state, "nodata")
    pill_txt = f"{state} — {esc(halt_reason)}" if state == "HALTED" and halt_reason else state
    pill = (f'<span class="pill {pill_cls}" role="status">'
            f'<span class="dot {"on" if state == "RUNNING" else "off"}" aria-hidden="true"></span>'
            f'{pill_txt}</span>')

    stats = []
    if deals_present:
        net = sum(d["profit"] for d in deals_list)
        cls = "up" if net >= 0 else "down"
        stats.append(('net realized P&amp;L', f'<span class="big {cls}">{money(net)}</span>'))
    stats += [
        ("enabled", f'<span class="big">{n_enabled}<span class="muted">/{len(STRATEGY_ORDER)}</span></span>'),
        ("disabled", f'<span class="big">{n_disabled}</span>'),
        ("error-tripped", f'<span class="big{" down" if n_tripped else ""}">{n_tripped}</span>'),
        ("events", f'<span class="big">{card["events_total"]}</span>'),
        ("last event", f'<span class="big" style="font-size:13px">{ts_html(last_ts, long_fmt=True) if last_ts else "&mdash;"}</span>'),
    ]
    stats_html = "".join(f'<div class="stat"><div class="lbl">{lbl}</div>{val}</div>'
                         for lbl, val in stats)

    stale_hidden = " hidden"
    last_dt = parse_ts(last_ts) if last_ts else None
    if last_dt and (now - last_dt).total_seconds() > 300:
        stale_hidden = ""
    stale = (f'<div id="stale" role="alert"{stale_hidden}>&#9888; Stale data &mdash; '
             f'last journal event is <span data-age>&gt;5 min</span> old. '
             f'The engine may not be writing.</div>')

    halt_banner = ""
    if state == "HALTED":
        halt_banner = (f'<div class="banner halt" role="alert">&#9632; TRADING HALTED &mdash; '
                       f'circuit breaker: {esc(halt_reason) or "reason not recorded"}. '
                       f'All positions flattened; human review required before restart.</div>')

    if deals_present and len(deals_list) >= 2:
        chart = equity_svg(deals_list)
        chart_note = (f'<p class="chartnote">{len(deals_list)} realized deals from deals.json '
                      f'&mdash; gold line: cumulative P&amp;L; red area: underwater drawdown '
                      f'(shared x-axis). Hover points for detail.</p>')
    elif events:
        chart = activity_svg(events)
        chart_note = ('<p class="chartnote">No deals.json found &mdash; showing journal '
                      'activity per hour instead. Export MT5 deal history to '
                      'logs/deals.json for the equity curve.</p>')
    else:
        chart = ('<p class="empty">No journal yet. Start the engine '
                 '(<code>python main.py</code>) and regenerate this dashboard.</p>')
        chart_note = ""

    table = fleet_table(per, enabled, deals_present)
    legend = ('<p class="legend">close reasons:'
              '<span class="seg tp" aria-hidden="true"></span>tp'
              '<span class="seg sl" aria-hidden="true"></span>sl'
              '<span class="seg time" aria-hidden="true"></span>time'
              '<span class="seg other" aria-hidden="true"></span>other'
              ' &mdash; click a column header to sort. &#9888; left border = DISABLE-CANDIDATE '
              '(PF&lt;0.8 over &ge;30 trades, errors&ge;3, or veto&gt;80% over &ge;20 signals).</p>')

    meta_refresh = (f'<meta http-equiv="refresh" content="{int(refresh)}">'
                    if refresh and refresh > 0 else "")
    refresh_note = (f"auto-reload every {int(refresh)}s" if refresh and refresh > 0
                    else "auto-reload off")
    skipped_note = (f' &middot; {skipped} malformed journal line{"s" if skipped != 1 else ""} skipped'
                    if skipped else "")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark light">
{meta_refresh}
<title>gold-scalper &middot; fleet dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body data-last-event="{esc(last_ts or '')}">
<div class="wrap">
<header class="top">
  <h1><span class="sym">XAUUSD</span> scalper fleet</h1>
  {pill}
  <div class="stats">{stats_html}</div>
</header>
{halt_banner}
{stale}
<div class="grid">
  <section class="panel" aria-labelledby="h-eq">
    <h2 id="h-eq">Equity &amp; drawdown</h2>
    {chart}
    {chart_note}
  </section>
  <section class="panel" aria-labelledby="h-risk">
    <h2 id="h-risk">Risk &amp; circuit breakers</h2>
    {risk_panel(settings, events, card["halts"])}
  </section>
  <section class="panel full" aria-labelledby="h-fleet">
    <h2 id="h-fleet">Strategy fleet &mdash; {len(STRATEGY_ORDER)} strategies</h2>
    <div class="tscroll">{table}</div>
    {legend}
  </section>
  <section class="panel full" aria-labelledby="h-ev">
    <h2 id="h-ev">Event stream &mdash; last 100, newest first</h2>
    {event_stream(events)}
  </section>
</div>
<footer>
  <span>generated {esc(now.strftime('%Y-%m-%d %H:%M:%S'))} UTC from {esc(str(journal_path))}{skipped_note}</span>
  <span>{refresh_note} &mdash; this is a static snapshot: re-run <code>python dashboard.py</code> for live data</span>
</footer>
</div>
<script>{JS}</script>
</body>
</html>
"""


# ------------------------------------------------------------------- main ---
def resolve(p: str) -> pathlib.Path:
    path = pathlib.Path(p)
    if path.is_absolute():
        return path
    return path if path.exists() else (BASE_DIR / p)


def main() -> int:
    ap = argparse.ArgumentParser(description="Render the fleet journal as a single-file HTML dashboard")
    ap.add_argument("--journal", default="logs/journal.jsonl")
    ap.add_argument("--deals", default="logs/deals.json")
    ap.add_argument("--enabled", default="config/enabled.json")
    ap.add_argument("--out", default="logs/dashboard.html")
    ap.add_argument("--refresh", type=int, default=10,
                    help="meta-refresh seconds; 0 disables auto-reload")
    args = ap.parse_args()

    journal_path = resolve(args.journal)
    deals_path = resolve(args.deals)
    enabled_path = resolve(args.enabled)
    out_path = pathlib.Path(args.out)
    if not out_path.is_absolute():
        out_path = BASE_DIR / args.out

    settings = load_json_or(BASE_DIR / "config" / "settings.json", {})
    magic_base = settings.get("magic_base", 770000) if isinstance(settings, dict) else 770000

    events, skipped = load_journal_counted(journal_path)
    deals_per, deals_list = load_deals(deals_path, magic_base)
    enabled = load_json_or(enabled_path, {})
    if not isinstance(enabled, dict):
        enabled = {}
    card = build_scorecard(events, deals_per)

    page = build_page(events=events, skipped=skipped, card=card, enabled=enabled,
                      settings=settings, deals_list=deals_list,
                      deals_present=bool(deals_list), refresh=args.refresh,
                      journal_path=journal_path, out_path=out_path)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(page, encoding="utf-8")
    size = out_path.stat().st_size
    print(f"wrote {out_path} ({size:,} bytes) — {len(events)} events"
          f"{f', {skipped} malformed lines skipped' if skipped else ''}, "
          f"{len(deals_list)} deals")
    return 0


if __name__ == "__main__":
    sys.exit(main())
