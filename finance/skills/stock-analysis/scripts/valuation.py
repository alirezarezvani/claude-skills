#!/usr/bin/env python3
"""valuation.py -- Stage-6 valuation calculator for the stock-analysis skill.

Purpose
-------
`references/06-valuation.md` calls the reverse-DCF "the most useful single
output" of a valuation, yet Stage 6 was the one place the skill still did all
its arithmetic by hand -- EV bridges, trailing multiples, the reverse-DCF
implied-growth solve, a forward DCF, and a probability-weighted scenario table.
Hand arithmetic is where false precision and slips creep in. This script does
the mechanical parts consistently, the same way `ratios.py` and `score.py` do,
so the analyst spends judgement on the *inputs and interpretation*, not on
compounding a cash-flow series in their head.

It computes nothing it was not given and asserts nothing about whether the
inputs are right. It is a calculator with guard-rails, not an oracle: every
output is only as good as the assumptions fed in, and the reverse-DCF is
deliberately framed as "what growth does today's price imply?" -- a testable
question, not a target price.

Standard library only. Python 3.8+. No network, no third-party packages.

--------------------------------------------------------------------------------
WHAT IT PRODUCES
--------------------------------------------------------------------------------
Each section runs only if its input block is present.

  ev_bridge   Enterprise value from the bridge: market cap + debt + minority
              + preferred - cash (+ leases / - associate investments if given).
  multiples   Trailing valuation multiples from EV / market cap and the P&L:
              P/E, EV/EBITDA, EV/EBIT, EV/Sales, P/B, P/FCF, FCF yield,
              earnings yield, dividend yield.
  reverse_dcf The market-implied stage-1 growth: the constant FCF growth rate,
              held for N years then fading to terminal growth, that a 2-stage
              FCFF model needs to reproduce today's EV. The headline question.
  dcf         A forward 2-stage FCFF value per share from your own growth,
              fade, terminal-growth, WACC and net-debt assumptions.
  scenarios   A probability-weighted value per share across bear/base/bull rows,
              each priced by whatever inputs it carries (value, EPS x exit P/E,
              EBITDA x EV/EBITDA, or a small DCF), plus upside vs the price.

--------------------------------------------------------------------------------
INPUT SCHEMA (JSON object; every block optional)
--------------------------------------------------------------------------------
  company, ticker, as_of, currency, units   -- labels only.
  market:     {price, shares_out, market_cap, as_of}
              market_cap is used if given, else price * shares_out.
  ev_bridge:  {market_cap, total_debt, cash, minority_interest, preferred,
               lease_liabilities (added), associate_investments (subtracted)}
  financials: {ebitda, ebit, pat, sales, book_value_equity, fcf, dividends}
              trailing figures for the multiples panel.
  reverse_dcf:{base_fcf, wacc, stage1_years, terminal_growth, ev (optional -
               defaults to the ev_bridge result)}
  dcf:        {base_fcf, stage1_growth, stage1_years, fade_years,
               terminal_growth, wacc, net_debt, minority, shares_out}
  scenarios:  [{label, prob, ...pricing inputs...}, ...]
              pricing inputs, first match wins:
                value_per_share
                eps + exit_pe
                ebitda + ev_ebitda (+ net_debt, minority, shares_out)
                base_fcf + stage1_growth (+ the dcf fields; unstated fields fall
                  back to the top-level dcf block)

RATES.  wacc, growth and terminal_growth may be given as decimals (0.12) or as
percents (12); any magnitude above 1.5 is read as a percent and divided by 100.
A Gordon terminal requires wacc > terminal_growth -- otherwise the model is
infinite/negative and the run FAILS with a clear message.

--------------------------------------------------------------------------------
USAGE
--------------------------------------------------------------------------------
    python valuation.py inputs.json            # readable report
    python valuation.py inputs.json --json      # machine-readable
    python valuation.py --template              # annotated blank input
    python valuation.py --example               # run the built-in example
    python valuation.py --example --json

Exit code: 0 on a clean run, 1 on an invalid assumption (e.g. terminal growth
>= WACC), 2 on unusable input (bad path / bad JSON).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any, Dict, List, Optional, Sequence, Tuple

SCRIPT = "valuation.py"

# A rate given as a percent (12) rather than a decimal (0.12) is a common slip;
# anything larger than this is interpreted as a percent and divided by 100.
_RATE_AS_PERCENT_ABOVE = 1.5

# Interpretive guard-rails (warnings only -- judgement, not hard rules).
_TERMINAL_GROWTH_HIGH = 0.05      # terminal growth above ~nominal long-run GDP.
_WACC_LOW = 0.06                  # a suspiciously low discount rate.
_WACC_HIGH = 0.20                 # a suspiciously high one.
_IMPLIED_GROWTH_DEMANDING = 0.15  # implied stage-1 growth the market rarely sustains.


# --------------------------------------------------------------------------- #
# Loading and coercion
# --------------------------------------------------------------------------- #
def strip_line_comments(text: str) -> str:
    """Drop whole-line `//` comments so an annotated template loads as JSON."""
    return "\n".join(
        line for line in text.splitlines() if not line.lstrip().startswith("//")
    )


def load_input(path: str) -> Dict[str, Any]:
    """Read and parse the input file, raising ValueError with a clear message."""
    try:
        with open(path, "r", encoding="utf-8-sig") as handle:
            raw = handle.read()
    except FileNotFoundError:
        raise ValueError("cannot read %r: no such file" % path)
    except OSError as err:
        raise ValueError("cannot read %r: %s" % (path, err.strerror or err))
    try:
        doc = json.loads(strip_line_comments(raw))
    except json.JSONDecodeError as err:
        raise ValueError(
            "%s is not valid JSON: %s (line %d, column %d)"
            % (path, err.msg, err.lineno, err.colno)
        )
    if not isinstance(doc, dict):
        raise ValueError(
            "%s must contain a JSON object at the top level, got %s"
            % (path, type(doc).__name__)
        )
    return doc


def num(value: Any) -> Optional[float]:
    """Coerce a value to float, or return None. Accepts '1,23,456' and '₹ 59,500'."""
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = re.sub(r"[,\s₹$£€¥%]", "", value)
        try:
            return float(cleaned)
        except ValueError:
            return None
    return None


def rate(value: Any) -> Optional[float]:
    """Coerce to a decimal rate; a magnitude above 1.5 is read as a percent."""
    n = num(value)
    if n is None:
        return None
    return n / 100.0 if abs(n) > _RATE_AS_PERCENT_ABOVE else n


def get(block: Any, key: str) -> Optional[float]:
    """Fetch and numify block[key], tolerating a missing block."""
    if not isinstance(block, dict):
        return None
    return num(block.get(key))


# --------------------------------------------------------------------------- #
# Formatting
# --------------------------------------------------------------------------- #
def fmt_money(x: Optional[float]) -> str:
    """Format a currency amount with thousands separators, or n/a."""
    if x is None:
        return "n/a"
    if x == int(x):
        return "{:,}".format(int(x))
    return "{:,.1f}".format(x)


def fmt_x(x: Optional[float]) -> str:
    """Format a multiple like 21.7x, or n/a."""
    return "n/a" if x is None else "%.1fx" % x


def fmt_pct(x: Optional[float]) -> str:
    """Format a decimal rate as a percentage, or n/a."""
    return "n/a" if x is None else "%.1f%%" % (x * 100.0)


def _div(a: Optional[float], b: Optional[float]) -> Optional[float]:
    """Safe division: None if either side is missing or the denominator is ~0."""
    if a is None or b is None or abs(b) < 1e-12:
        return None
    return a / b


# --------------------------------------------------------------------------- #
# Result / finding model
# --------------------------------------------------------------------------- #
class Note:
    """A warning or error surfaced during a valuation run."""

    def __init__(self, severity: str, message: str) -> None:
        self.severity = severity  # "error" | "warn"
        self.message = message

    def to_dict(self) -> Dict[str, str]:
        return {"severity": self.severity, "message": self.message}


# --------------------------------------------------------------------------- #
# Market cap resolution
# --------------------------------------------------------------------------- #
def resolve_market_cap(doc: Dict[str, Any]) -> Optional[float]:
    """Market cap from ev_bridge, else market.market_cap, else price*shares."""
    mc = get(doc.get("ev_bridge"), "market_cap")
    if mc is not None:
        return mc
    market = doc.get("market")
    mc = get(market, "market_cap")
    if mc is not None:
        return mc
    price = get(market, "price")
    shares = get(market, "shares_out")
    if price is not None and shares is not None:
        return price * shares
    return None


def resolve_price(doc: Dict[str, Any]) -> Optional[float]:
    """Current price per share, if given."""
    return get(doc.get("market"), "price")


# --------------------------------------------------------------------------- #
# EV bridge
# --------------------------------------------------------------------------- #
def compute_ev_bridge(doc: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Enterprise value from its components, returning the bridge and the total."""
    block = doc.get("ev_bridge")
    if not isinstance(block, dict):
        return None
    mc = resolve_market_cap(doc)
    if mc is None:
        return None
    debt = get(block, "total_debt") or 0.0
    minority = get(block, "minority_interest") or 0.0
    preferred = get(block, "preferred") or 0.0
    cash = get(block, "cash") or 0.0
    leases = get(block, "lease_liabilities") or 0.0
    assoc = get(block, "associate_investments") or 0.0
    ev = mc + debt + minority + preferred + leases - cash - assoc
    net_debt = debt + leases - cash
    rows = [
        ("Market cap", mc),
        ("+ Total debt", debt),
        ("+ Lease liabilities", leases) if leases else None,
        ("+ Minority interest", minority) if minority else None,
        ("+ Preferred", preferred) if preferred else None,
        ("- Cash & equivalents", -cash),
        ("- Investments in associates", -assoc) if assoc else None,
        ("= Enterprise value", ev),
    ]
    return {
        "market_cap": mc,
        "enterprise_value": ev,
        "net_debt": net_debt,
        "rows": [r for r in rows if r is not None],
    }


# --------------------------------------------------------------------------- #
# Trailing multiples
# --------------------------------------------------------------------------- #
def compute_multiples(doc: Dict[str, Any], ev: Optional[float],
                      market_cap: Optional[float]) -> Optional[Dict[str, Any]]:
    """Trailing valuation multiples from EV / market cap and the P&L block."""
    fin = doc.get("financials")
    if not isinstance(fin, dict) or (ev is None and market_cap is None):
        return None
    ebitda = get(fin, "ebitda")
    ebit = get(fin, "ebit")
    pat = get(fin, "pat")
    sales = get(fin, "sales")
    book = get(fin, "book_value_equity")
    fcf = get(fin, "fcf")
    dividends = get(fin, "dividends")
    out = {
        "pe": _div(market_cap, pat),
        "ev_ebitda": _div(ev, ebitda),
        "ev_ebit": _div(ev, ebit),
        "ev_sales": _div(ev, sales),
        "pb": _div(market_cap, book),
        "p_fcf": _div(market_cap, fcf),
        "fcf_yield": _div(fcf, market_cap),
        "earnings_yield": _div(pat, market_cap),
        "dividend_yield": _div(dividends, market_cap),
    }
    return out


# --------------------------------------------------------------------------- #
# DCF core (shared by forward DCF and scenarios)
# --------------------------------------------------------------------------- #
def _ev_from_growth(base: float, g: float, wacc: float, years: int,
                    term_g: float) -> float:
    """PV of a constant-growth stage plus Gordon terminal (FCFF), for one g."""
    pv = 0.0
    fcf = base
    for t in range(1, years + 1):
        fcf = base * (1.0 + g) ** t
        pv += fcf / (1.0 + wacc) ** t
    fcf_n = base * (1.0 + g) ** years
    tv = fcf_n * (1.0 + term_g) / (wacc - term_g)
    pv += tv / (1.0 + wacc) ** years
    return pv


def solve_implied_growth(target_ev: float, base: float, wacc: float,
                         years: int, term_g: float) -> Tuple[str, float]:
    """Bisection-solve the stage-1 growth that reproduces target_ev.

    EV is monotone increasing in g, so bisection is exact and robust. Returns a
    status: 'ok' with the growth; 'below'/'above' if the target sits outside the
    range the model can produce between -95% and +200% growth (a signal the price
    is unreachable under these terminal/WACC assumptions, which is itself
    informative).
    """
    lo, hi = -0.95, 2.0
    f_lo = _ev_from_growth(base, lo, wacc, years, term_g) - target_ev
    f_hi = _ev_from_growth(base, hi, wacc, years, term_g) - target_ev
    if f_lo > 0:
        return "below", lo
    if f_hi < 0:
        return "above", hi
    for _ in range(200):
        mid = (lo + hi) / 2.0
        f_mid = _ev_from_growth(base, mid, wacc, years, term_g) - target_ev
        if abs(f_mid) < 1e-6 * max(1.0, abs(target_ev)):
            return "ok", mid
        if f_mid < 0:
            lo = mid
        else:
            hi = mid
    return "ok", (lo + hi) / 2.0


def forward_dcf(base: float, g1: float, n1: int, fade_years: int, term_g: float,
                wacc: float, net_debt: float, minority: float,
                shares: Optional[float]) -> Dict[str, Any]:
    """A 2-stage (constant then linear-fade) FCFF DCF -> EV, equity, per share."""
    pv_explicit = 0.0
    fcf = base
    year = 0
    for _ in range(max(0, n1)):
        year += 1
        fcf = fcf * (1.0 + g1)
        pv_explicit += fcf / (1.0 + wacc) ** year
    for k in range(1, max(0, fade_years) + 1):
        year += 1
        g = g1 + (term_g - g1) * (k / fade_years) if fade_years else term_g
        fcf = fcf * (1.0 + g)
        pv_explicit += fcf / (1.0 + wacc) ** year
    if year == 0:  # no explicit years: value the terminal off the base directly.
        year = 1
        fcf = base * (1.0 + term_g)
    tv = fcf * (1.0 + term_g) / (wacc - term_g)
    pv_terminal = tv / (1.0 + wacc) ** year
    ev = pv_explicit + pv_terminal
    equity = ev - net_debt - minority
    per_share = _div(equity, shares)
    return {
        "enterprise_value": ev,
        "equity_value": equity,
        "per_share": per_share,
        "pv_explicit": pv_explicit,
        "pv_terminal": pv_terminal,
        "terminal_pct_of_ev": _div(pv_terminal, ev),
    }


# --------------------------------------------------------------------------- #
# Reverse DCF
# --------------------------------------------------------------------------- #
def compute_reverse_dcf(doc: Dict[str, Any], ev_bridge: Optional[Dict[str, Any]],
                        notes: List[Note]) -> Optional[Dict[str, Any]]:
    """Solve for the market-implied stage-1 growth, given price-derived EV."""
    block = doc.get("reverse_dcf")
    if not isinstance(block, dict):
        return None
    base = get(block, "base_fcf")
    wacc = rate(block.get("wacc"))
    years = get(block, "stage1_years")
    term_g = rate(block.get("terminal_growth"))
    target_ev = get(block, "ev")
    if target_ev is None and ev_bridge is not None:
        target_ev = ev_bridge.get("enterprise_value")
    missing = [k for k, v in (("base_fcf", base), ("wacc", wacc),
                              ("stage1_years", years), ("terminal_growth", term_g),
                              ("ev", target_ev)) if v is None]
    if missing:
        notes.append(Note("warn", "reverse_dcf skipped: missing %s."
                          % ", ".join(missing)))
        return None
    years = int(years)
    if wacc <= term_g:
        notes.append(Note("error",
                          "reverse_dcf: WACC (%.1f%%) must exceed terminal growth "
                          "(%.1f%%); the Gordon terminal is otherwise infinite."
                          % (wacc * 100, term_g * 100)))
        return None
    if base <= 0:
        notes.append(Note("warn",
                          "reverse_dcf skipped: base FCF is non-positive, so an "
                          "implied-growth solve is not meaningful. Anchor on "
                          "EV/EBITDA or normalise FCF first."))
        return None
    status, g = solve_implied_growth(target_ev, base, wacc, years, term_g)
    result = {
        "target_ev": target_ev, "base_fcf": base, "wacc": wacc,
        "stage1_years": years, "terminal_growth": term_g,
        "implied_growth": g, "status": status,
    }
    if status == "ok" and g >= _IMPLIED_GROWTH_DEMANDING:
        notes.append(Note("warn",
                          "Market implies ~%.1f%% FCF growth for %d years -- "
                          "demanding; check it against what this company (and its "
                          "industry) has actually delivered."
                          % (g * 100, years)))
    if status == "above":
        notes.append(Note("warn",
                          "Even 200%% growth for %d years cannot reproduce today's "
                          "EV under these WACC/terminal assumptions -- the price "
                          "embeds more than this model can express; revisit the "
                          "assumptions or the base FCF." % years))
    if status == "below":
        notes.append(Note("warn",
                          "Today's EV is below the model's value even at deeply "
                          "negative growth -- the market is pricing in decline or "
                          "distress relative to these assumptions."))
    return result


# --------------------------------------------------------------------------- #
# Forward DCF
# --------------------------------------------------------------------------- #
def compute_forward_dcf(doc: Dict[str, Any], notes: List[Note]
                        ) -> Optional[Dict[str, Any]]:
    """A forward 2-stage FCFF DCF from the analyst's own assumptions."""
    block = doc.get("dcf")
    if not isinstance(block, dict):
        return None
    base = get(block, "base_fcf")
    g1 = rate(block.get("stage1_growth"))
    n1 = get(block, "stage1_years")
    fade = get(block, "fade_years") or 0.0
    term_g = rate(block.get("terminal_growth"))
    wacc = rate(block.get("wacc"))
    net_debt = get(block, "net_debt") or 0.0
    minority = get(block, "minority") or 0.0
    shares = get(block, "shares_out")
    missing = [k for k, v in (("base_fcf", base), ("stage1_growth", g1),
                              ("stage1_years", n1), ("terminal_growth", term_g),
                              ("wacc", wacc)) if v is None]
    if missing:
        notes.append(Note("warn", "dcf skipped: missing %s." % ", ".join(missing)))
        return None
    if wacc <= term_g:
        notes.append(Note("error",
                          "dcf: WACC (%.1f%%) must exceed terminal growth (%.1f%%)."
                          % (wacc * 100, term_g * 100)))
        return None
    res = forward_dcf(base, g1, int(n1), int(fade), term_g, wacc,
                      net_debt, minority, shares)
    res.update({"base_fcf": base, "stage1_growth": g1, "stage1_years": int(n1),
                "fade_years": int(fade), "terminal_growth": term_g, "wacc": wacc,
                "net_debt": net_debt})
    price = resolve_price(doc)
    if price is not None and res.get("per_share"):
        res["upside_vs_price"] = _div(res["per_share"] - price, price)
    if res.get("terminal_pct_of_ev") and res["terminal_pct_of_ev"] > 0.75:
        notes.append(Note("warn",
                          "dcf: %.0f%% of value sits in the terminal -- the answer "
                          "is an assumption about perpetuity, not the explicit "
                          "forecast." % (res["terminal_pct_of_ev"] * 100)))
    return res


# --------------------------------------------------------------------------- #
# Scenarios
# --------------------------------------------------------------------------- #
def scenario_value(row: Dict[str, Any], doc: Dict[str, Any],
                   notes: List[Note]) -> Optional[float]:
    """Value one scenario row by the first pricing method whose inputs are present."""
    label = row.get("label", "(scenario)")
    # 1) value per share stated directly.
    v = get(row, "value_per_share")
    if v is not None:
        return v
    # 2) EPS x exit P/E.
    eps, pe = get(row, "eps"), get(row, "exit_pe")
    if eps is not None and pe is not None:
        return eps * pe
    # 3) EBITDA x EV/EBITDA -> equity -> per share.
    ebitda, mult = get(row, "ebitda"), get(row, "ev_ebitda")
    if ebitda is not None and mult is not None:
        ev = ebitda * mult
        net_debt = get(row, "net_debt")
        if net_debt is None:
            net_debt = get(doc.get("dcf"), "net_debt") or 0.0
        minority = get(row, "minority") or 0.0
        shares = get(row, "shares_out") or get(doc.get("dcf"), "shares_out") \
            or get(doc.get("market"), "shares_out")
        return _div(ev - net_debt - minority, shares)
    # 4) a small DCF, falling back to the top-level dcf block for unstated fields.
    base = get(row, "base_fcf")
    g1 = rate(row.get("stage1_growth"))
    if base is not None and g1 is not None:
        d = doc.get("dcf") if isinstance(doc.get("dcf"), dict) else {}
        n1 = get(row, "stage1_years") or get(d, "stage1_years") or 10
        fade = get(row, "fade_years") or get(d, "fade_years") or 0
        term_g = rate(row.get("terminal_growth")) or rate(d.get("terminal_growth"))
        wacc = rate(row.get("wacc")) or rate(d.get("wacc"))
        net_debt = get(row, "net_debt")
        if net_debt is None:
            net_debt = get(d, "net_debt") or 0.0
        minority = get(row, "minority") or 0.0
        shares = get(row, "shares_out") or get(d, "shares_out") \
            or get(doc.get("market"), "shares_out")
        if None in (term_g, wacc) or shares is None:
            notes.append(Note("warn", "scenario '%s': DCF inputs incomplete." % label))
            return None
        if wacc <= term_g:
            notes.append(Note("error", "scenario '%s': WACC must exceed terminal "
                              "growth." % label))
            return None
        res = forward_dcf(base, g1, int(n1), int(fade), term_g, wacc,
                          net_debt, minority, shares)
        return res.get("per_share")
    notes.append(Note("warn", "scenario '%s': no usable pricing inputs "
                      "(value_per_share, eps+exit_pe, ebitda+ev_ebitda, or "
                      "base_fcf+stage1_growth)." % label))
    return None


def compute_scenarios(doc: Dict[str, Any], notes: List[Note]
                      ) -> Optional[Dict[str, Any]]:
    """Value each scenario, weight by probability, compare to the current price."""
    rows = doc.get("scenarios")
    if not isinstance(rows, list) or not rows:
        return None
    price = resolve_price(doc)
    out_rows: List[Dict[str, Any]] = []
    weighted = 0.0
    prob_sum = 0.0
    have_all = True
    for row in rows:
        if not isinstance(row, dict):
            continue
        label = row.get("label", "(scenario)")
        prob = get(row, "prob")
        value = scenario_value(row, doc, notes)
        if prob is not None:
            prob_sum += prob
        if value is None or prob is None:
            have_all = False
        else:
            weighted += prob * value
        out_rows.append({
            "label": label, "prob": prob, "value_per_share": value,
            "upside_vs_price": _div(value - price, price)
            if (value is not None and price is not None) else None,
        })
    if abs(prob_sum - 1.0) > 0.02:
        notes.append(Note("warn", "scenario probabilities sum to %.2f, not 1.00."
                          % prob_sum))
    result = {
        "rows": out_rows,
        "prob_sum": prob_sum,
        "weighted_value": weighted if have_all else None,
        "weighted_upside": _div(weighted - price, price)
        if (have_all and price is not None) else None,
        "price": price,
    }
    return result


# --------------------------------------------------------------------------- #
# Assumption guard-rails (warnings)
# --------------------------------------------------------------------------- #
def check_assumptions(doc: Dict[str, Any], notes: List[Note]) -> None:
    """Flag aggressive or implausible discount-rate / terminal-growth inputs."""
    for block_name in ("reverse_dcf", "dcf"):
        block = doc.get(block_name)
        if not isinstance(block, dict):
            continue
        wacc = rate(block.get("wacc"))
        term_g = rate(block.get("terminal_growth"))
        if wacc is not None and not (_WACC_LOW <= wacc <= _WACC_HIGH):
            notes.append(Note("warn", "%s: WACC of %.1f%% is outside the usual "
                              "6-20%% band -- state how it was derived (risk-free "
                              "rate + its date, ERP, beta)."
                              % (block_name, wacc * 100)))
        if term_g is not None and term_g > _TERMINAL_GROWTH_HIGH:
            notes.append(Note("warn", "%s: terminal growth of %.1f%% exceeds "
                              "~nominal long-run GDP; a business cannot outgrow the "
                              "economy forever." % (block_name, term_g * 100)))


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #
def run(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Run every section whose inputs are present; collect results and notes."""
    notes: List[Note] = []
    check_assumptions(doc, notes)
    ev_bridge = compute_ev_bridge(doc)
    market_cap = resolve_market_cap(doc)
    ev = ev_bridge.get("enterprise_value") if ev_bridge else \
        get(doc.get("reverse_dcf"), "ev")
    multiples = compute_multiples(doc, ev, market_cap)
    reverse = compute_reverse_dcf(doc, ev_bridge, notes)
    dcf = compute_forward_dcf(doc, notes)
    scenarios = compute_scenarios(doc, notes)
    return {
        "company": doc.get("company"),
        "ticker": doc.get("ticker"),
        "as_of": doc.get("as_of"),
        "currency": doc.get("currency"),
        "units": doc.get("units"),
        "market_cap": market_cap,
        "ev_bridge": ev_bridge,
        "multiples": multiples,
        "reverse_dcf": reverse,
        "dcf": dcf,
        "scenarios": scenarios,
        "notes": notes,
    }


def has_error(notes: Sequence[Note]) -> bool:
    """True if any note is an error (invalid assumption)."""
    return any(n.severity == "error" for n in notes)


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #
def render_text(res: Dict[str, Any]) -> str:
    """Render the human-readable valuation report."""
    cur = res.get("currency") or ""
    units = res.get("units") or ""
    unit_tag = ("%s %s" % (cur, units)).strip() or "(units unstated)"
    lines: List[str] = []
    lines.append("=" * 72)
    lines.append("VALUATION  --  %s%s" % (
        res.get("company") or "(company not stated)",
        " [%s]" % res["ticker"] if res.get("ticker") else ""))
    lines.append("=" * 72)
    lines.append("As of : %s   Amounts in: %s   (multiples/rates are unitless)"
                 % (res.get("as_of") or "(not stated)", unit_tag))
    lines.append("Outputs are estimates -- only as sound as the assumptions below.")

    ev_bridge = res.get("ev_bridge")
    if ev_bridge:
        lines.append("")
        lines.append("-" * 72)
        lines.append("EV BRIDGE (%s)" % unit_tag)
        lines.append("-" * 72)
        for label, val in ev_bridge["rows"]:
            lines.append("  %-32s %14s" % (label, fmt_money(val)))
        lines.append("  %-32s %14s" % ("(net debt)", fmt_money(ev_bridge["net_debt"])))

    mult = res.get("multiples")
    if mult:
        lines.append("")
        lines.append("-" * 72)
        lines.append("TRAILING MULTIPLES")
        lines.append("-" * 72)
        pairs = [
            ("P/E", fmt_x(mult["pe"])), ("EV/EBITDA", fmt_x(mult["ev_ebitda"])),
            ("EV/EBIT", fmt_x(mult["ev_ebit"])), ("EV/Sales", fmt_x(mult["ev_sales"])),
            ("P/B", fmt_x(mult["pb"])), ("P/FCF", fmt_x(mult["p_fcf"])),
            ("FCF yield", fmt_pct(mult["fcf_yield"])),
            ("Earnings yield", fmt_pct(mult["earnings_yield"])),
            ("Dividend yield", fmt_pct(mult["dividend_yield"])),
        ]
        for i in range(0, len(pairs), 3):
            chunk = pairs[i:i + 3]
            lines.append("  " + "".join("%-14s %-9s" % (k, v) for k, v in chunk))

    rev = res.get("reverse_dcf")
    if rev:
        lines.append("")
        lines.append("-" * 72)
        lines.append("REVERSE DCF -- what growth is priced in?")
        lines.append("-" * 72)
        lines.append("  Anchor EV        : %s %s" % (fmt_money(rev["target_ev"]), unit_tag))
        lines.append("  Base FCF         : %s %s" % (fmt_money(rev["base_fcf"]), unit_tag))
        lines.append("  WACC / terminal g: %s / %s"
                     % (fmt_pct(rev["wacc"]), fmt_pct(rev["terminal_growth"])))
        lines.append("  Stage-1 horizon  : %d years" % rev["stage1_years"])
        if rev["status"] == "ok":
            lines.append("  => IMPLIED stage-1 FCF growth: %s per year" %
                         fmt_pct(rev["implied_growth"]))
            lines.append("     i.e. today's price already assumes ~%s FCF growth "
                         "for %d years, fading to %s."
                         % (fmt_pct(rev["implied_growth"]), rev["stage1_years"],
                            fmt_pct(rev["terminal_growth"])))
        elif rev["status"] == "above":
            lines.append("  => price implies MORE than +200%%/yr growth is needed "
                         "-- unreachable under these assumptions.")
        else:
            lines.append("  => price sits below the model even at deeply negative "
                         "growth -- decline/distress is priced in.")

    dcf = res.get("dcf")
    if dcf:
        lines.append("")
        lines.append("-" * 72)
        lines.append("FORWARD DCF (your assumptions)")
        lines.append("-" * 72)
        lines.append("  Base FCF %s | g1 %s for %dy | fade %dy | term g %s | WACC %s"
                     % (fmt_money(dcf["base_fcf"]), fmt_pct(dcf["stage1_growth"]),
                        dcf["stage1_years"], dcf["fade_years"],
                        fmt_pct(dcf["terminal_growth"]), fmt_pct(dcf["wacc"])))
        lines.append("  Enterprise value : %s %s" % (fmt_money(dcf["enterprise_value"]), unit_tag))
        lines.append("  Equity value     : %s %s" % (fmt_money(dcf["equity_value"]), unit_tag))
        lines.append("  Value per share  : %s" % fmt_money(dcf["per_share"]))
        lines.append("  Terminal %% of EV : %s" % fmt_pct(dcf["terminal_pct_of_ev"]))
        if dcf.get("upside_vs_price") is not None:
            lines.append("  Upside vs price  : %s" % fmt_pct(dcf["upside_vs_price"]))

    scen = res.get("scenarios")
    if scen:
        lines.append("")
        lines.append("-" * 72)
        lines.append("SCENARIOS")
        lines.append("-" * 72)
        lines.append("  %-14s %6s %16s %12s" % ("Scenario", "Prob", "Value/share", "vs price"))
        for row in scen["rows"]:
            lines.append("  %-14s %6s %16s %12s" % (
                row["label"],
                fmt_pct(row["prob"]) if row["prob"] is not None else "n/a",
                fmt_money(row["value_per_share"]),
                fmt_pct(row["upside_vs_price"]) if row["upside_vs_price"] is not None else "n/a"))
        if scen["weighted_value"] is not None:
            lines.append("  %-14s %6s %16s %12s" % (
                "Prob-weighted", fmt_pct(scen["prob_sum"]),
                fmt_money(scen["weighted_value"]),
                fmt_pct(scen["weighted_upside"]) if scen["weighted_upside"] is not None else "n/a"))

    notes = res.get("notes") or []
    errors = [n for n in notes if n.severity == "error"]
    warns = [n for n in notes if n.severity == "warn"]
    lines.append("")
    lines.append("-" * 72)
    if errors:
        lines.append("ERRORS -- %d (invalid assumptions; results above may be omitted)"
                     % len(errors))
        for n in errors:
            lines.append("  [error] %s" % n.message)
    if warns:
        lines.append("WARNINGS -- %d" % len(warns))
        for n in warns:
            lines.append("  [warn]  %s" % n.message)
    if not notes:
        lines.append("No assumption warnings.")
    return "\n".join(lines)


def render_json(res: Dict[str, Any]) -> str:
    """Render the machine-readable result."""
    payload = dict(res)
    payload["notes"] = [n.to_dict() for n in res.get("notes", [])]
    return json.dumps(payload, indent=2, ensure_ascii=False, default=str)


# --------------------------------------------------------------------------- #
# Template and example
# --------------------------------------------------------------------------- #
TEMPLATE = """\
// Valuation input template for the stock-analysis skill.
// Fill in only the blocks you need; each section runs if its block is present.
// Rates may be decimals (0.12) or percents (12). Whole-line // comments are
// stripped by the loader. Then run:  python valuation.py this_file.json
{
  "company": "",
  "ticker": "",
  "as_of": "YYYY-MM-DD",
  "currency": "INR",
  "units": "crore",
  "market": {"price": 0, "shares_out": 0, "market_cap": 0, "as_of": "YYYY-MM-DD"},
  "ev_bridge": {
    "market_cap": 0, "total_debt": 0, "cash": 0,
    "minority_interest": 0, "preferred": 0,
    "lease_liabilities": 0, "associate_investments": 0
  },
  "financials": {
    "ebitda": 0, "ebit": 0, "pat": 0, "sales": 0,
    "book_value_equity": 0, "fcf": 0, "dividends": 0
  },
  "reverse_dcf": {"base_fcf": 0, "wacc": 0.12, "stage1_years": 10, "terminal_growth": 0.04},
  "dcf": {
    "base_fcf": 0, "stage1_growth": 0.15, "stage1_years": 10, "fade_years": 5,
    "terminal_growth": 0.04, "wacc": 0.12, "net_debt": 0, "minority": 0, "shares_out": 0
  },
  "scenarios": [
    {"label": "Bear", "prob": 0.30, "eps": 0, "exit_pe": 0},
    {"label": "Base", "prob": 0.45, "eps": 0, "exit_pe": 0},
    {"label": "Bull", "prob": 0.25, "eps": 0, "exit_pe": 0}
  ]
}
"""


def example_document() -> Dict[str, Any]:
    """A filled example (a fictional distributor) exercising every section."""
    return {
        "company": "Illustrative Distribution Co (fictional)",
        "ticker": "NSE:ILLUSDEMO",
        "as_of": "2026-08-02",
        "currency": "INR", "units": "crore",
        "market": {"price": 1240.0, "shares_out": 4.36, "market_cap": 5406.0,
                   "as_of": "2026-07-15"},
        "ev_bridge": {"market_cap": 5406.0, "total_debt": 677.0, "cash": 327.0,
                      "minority_interest": 60.0, "preferred": 0.0},
        "financials": {"ebitda": 266.0, "ebit": 220.0, "pat": 115.0,
                       "sales": 6591.0, "book_value_equity": 1688.0,
                       "fcf": 60.0, "dividends": 0.0},
        "reverse_dcf": {"base_fcf": 90.0, "wacc": 0.125, "stage1_years": 10,
                        "terminal_growth": 0.04},
        "dcf": {"base_fcf": 90.0, "stage1_growth": 0.20, "stage1_years": 7,
                "fade_years": 5, "terminal_growth": 0.04, "wacc": 0.125,
                "net_debt": 410.0, "minority": 0.0, "shares_out": 4.36},
        "scenarios": [
            {"label": "Bear", "prob": 0.30, "eps": 31.0, "exit_pe": 25.0},
            {"label": "Base", "prob": 0.45, "eps": 34.0, "exit_pe": 33.0},
            {"label": "Bull", "prob": 0.25, "eps": 36.0, "exit_pe": 40.0},
        ],
    }


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    """Construct the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog=SCRIPT,
        description="Stage-6 valuation calculator: EV bridge, trailing multiples, "
                    "reverse-DCF implied growth, forward 2-stage DCF, and a "
                    "probability-weighted scenario table.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", nargs="?", help="path to the valuation input JSON")
    parser.add_argument("--json", dest="as_json", action="store_true",
                        help="emit results as JSON instead of a text report")
    parser.add_argument("--template", action="store_true",
                        help="print an annotated blank input file and exit")
    parser.add_argument("--example", action="store_true",
                        help="run the built-in fictional example")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Entry point. Returns 0 clean, 1 invalid assumption, 2 bad input."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.template:
        sys.stdout.write(TEMPLATE)
        return 0
    if args.example:
        doc = example_document()
    else:
        if not args.input:
            parser.error("a valuation JSON file is required (or --template / --example)")
        try:
            doc = load_input(args.input)
        except ValueError as err:
            sys.stderr.write("%s: %s\n" % (SCRIPT, err))
            return 2

    res = run(doc)
    if args.as_json:
        sys.stdout.write(render_json(res) + "\n")
    else:
        sys.stdout.write(render_text(res) + "\n")
    return 1 if has_error(res["notes"]) else 0


if __name__ == "__main__":
    sys.exit(main())
