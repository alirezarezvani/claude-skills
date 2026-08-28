#!/usr/bin/env python3
"""ratios.py -- deterministic financial ratio engine for the stock-analysis skill.

Purpose
-------
Every analysis otherwise recomputes the same ratios by hand, which invites
arithmetic slips and silent inconsistency between sections of the same report.
This script takes raw financial line items for one company across several
periods and returns the full derived ratio set: growth, the margin ladder, the
return set, 3-step and 5-step DuPont, return on incremental invested capital,
leverage, liquidity, working capital, cash-flow quality, per-share figures, an
explicit enterprise-value bridge, valuation multiples, and automatic quality
warnings.

Python 3.8+. Standard library only. No network access, no third-party packages.

SECTOR GATE -- READ THIS FIRST
------------------------------
For **banks, NBFCs/HFCs, insurers and REITs/InvITs** most of the ratios below
are meaningless or actively misleading:

  * Banks and NBFCs -- debt is raw material, not financing. Invested capital,
    NOPAT, enterprise value, EV/EBITDA, net debt/EBITDA and ROIC are undefined.
    A bank is *supposed* to run 8-15x assets/equity, so the DuPont equity
    multiplier is not a warning, it is the business model. Use ROA and ROE read
    together with CET1/CAR, NIM, cost-to-income, credit cost and RoRWA.
  * Insurers -- new-business strain depresses reported ROE precisely when the
    company is writing profitable growth. Use ROEV, VNB margin, combined ratio.
  * REITs/InvITs -- assets are carried at fair value and the asset *is* the
    business, so ROIC collapses toward the cap rate by construction. Use AFFO
    yield, NOI yield on cost, cap rate vs cost of debt, LTV.

Pass ``--sector banks`` (or nbfc / insurance / reit / financials) and the script
prints this warning prominently and suppresses the enterprise-value multiples
for the sectors where EV has no meaning. Use the matching sector playbook in
``references/sectors/`` for the metric set that actually applies.

Usage
-----
    python ratios.py inputs.json
    python ratios.py inputs.json --json > ratios.json
    python ratios.py inputs.json --sector banks
    python ratios.py --example > inputs.json      # emit the worked example below
    python ratios.py --help

Input format
------------
A JSON object with:

  ``company``, ``currency``, ``basis``, ``sector``  -- free-text metadata.
  ``periods``      -- list of period objects, **ordered oldest first** (set
                      ``"periods_order": "newest_first"`` if yours are reversed).
  ``market``       -- optional. Price / share count / EV-bridge items used for
                      valuation. Applies to the latest period.

Every numeric field is optional. Anything that cannot be computed from what was
supplied is reported as ``n/a`` with the reason, never guessed. Line items that
can be derived unambiguously from others (gross profit from revenue and COGS,
EBIT from EBITDA and depreciation, and so on) are derived and the derivation is
listed under INPUT INTEGRITY.

Recognised period fields (all optional, all in one consistent currency unit):

  Income statement:
    label, revenue, cogs, gross_profit, ebitda, depreciation, ebit,
    other_income, interest, pbt, tax, cash_taxes_paid, minority_interest,
    associate_profit, exceptional_items, pat
  Balance sheet:
    equity, minority_interest_bs, total_assets, goodwill, intangibles,
    short_term_debt, long_term_debt, current_maturities, gross_debt,
    lease_liabilities, rou_assets, cash, current_investments,
    investments_in_associates, current_assets, current_liabilities,
    inventory, receivables, payables, net_ppe, cwip, pension_deficit,
    preference_capital, other_debt_like
  Cash flow:
    cfo, capex, acquisitions, dividends_paid, interest_paid, lease_expense,
    preference_dividends
  Shares:
    shares_outstanding, diluted_shares, dividend_per_share

Recognised ``market`` fields:
    price, as_of, market_cap, diluted_shares, surplus_cash, preference_capital,
    minority_interest, pension_deficit, other_debt_like,
    contingent_consideration, value_of_associates

Sign conventions: capex, acquisitions, dividends_paid, interest_paid and tax are
supplied as **positive outflows**. Revenue is net of indirect taxes (state the
basis in the report; peers must be on the same basis).

Worked example input
--------------------
A complete, runnable example (also available via ``--example``):

--- EXAMPLE INPUT (begin) ---
{
  "company": "Example Manufacturing Ltd",
  "currency": "INR crore",
  "basis": "consolidated",
  "sector": "manufacturing",
  "source": "FY22-FY25 annual reports, consolidated; price from NSE 2026-07-21",
  "periods_order": "oldest_first",
  "periods": [
    {
      "label": "FY22",
      "revenue": 4000, "cogs": 2400, "ebitda": 720, "depreciation": 180,
      "other_income": 40, "interest": 90, "tax": 125, "minority_interest": 10,
      "equity": 2100, "minority_interest_bs": 60, "total_assets": 3900,
      "goodwill": 150, "intangibles": 90,
      "short_term_debt": 250, "long_term_debt": 700, "current_maturities": 100,
      "lease_liabilities": 180, "rou_assets": 170,
      "cash": 260, "current_investments": 140, "investments_in_associates": 90,
      "current_assets": 1750, "current_liabilities": 1100,
      "inventory": 620, "receivables": 700, "payables": 560,
      "net_ppe": 1500, "cwip": 120,
      "cfo": 600, "capex": 260, "acquisitions": 0, "dividends_paid": 90,
      "interest_paid": 88, "cash_taxes_paid": 120, "lease_expense": 60,
      "shares_outstanding": 20.0, "diluted_shares": 20.05
    },
    {
      "label": "FY23",
      "revenue": 4560, "cogs": 2735, "ebitda": 830, "depreciation": 205,
      "other_income": 45, "interest": 95, "tax": 148, "minority_interest": 12,
      "equity": 2420, "minority_interest_bs": 68, "total_assets": 4350,
      "goodwill": 150, "intangibles": 85,
      "short_term_debt": 260, "long_term_debt": 720, "current_maturities": 110,
      "lease_liabilities": 195, "rou_assets": 185,
      "cash": 300, "current_investments": 150, "investments_in_associates": 95,
      "current_assets": 1950, "current_liabilities": 1180,
      "inventory": 700, "receivables": 820, "payables": 600,
      "net_ppe": 1620, "cwip": 160,
      "cfo": 640, "capex": 300, "acquisitions": 0, "dividends_paid": 100,
      "interest_paid": 93, "cash_taxes_paid": 140, "lease_expense": 66,
      "shares_outstanding": 20.0, "diluted_shares": 20.1
    },
    {
      "label": "FY24",
      "revenue": 5200, "cogs": 3120, "ebitda": 950, "depreciation": 235,
      "other_income": 52, "interest": 102, "tax": 172, "minority_interest": 14,
      "equity": 2790, "minority_interest_bs": 76, "total_assets": 4900,
      "goodwill": 150, "intangibles": 80,
      "short_term_debt": 280, "long_term_debt": 760, "current_maturities": 120,
      "lease_liabilities": 210, "rou_assets": 200,
      "cash": 330, "current_investments": 170, "investments_in_associates": 100,
      "current_assets": 2200, "current_liabilities": 1290,
      "inventory": 800, "receivables": 980, "payables": 640,
      "net_ppe": 1780, "cwip": 210,
      "cfo": 690, "capex": 340, "acquisitions": 0, "dividends_paid": 115,
      "interest_paid": 100, "cash_taxes_paid": 165, "lease_expense": 72,
      "shares_outstanding": 20.0, "diluted_shares": 20.15
    },
    {
      "label": "FY25",
      "revenue": 5950, "cogs": 3540, "ebitda": 1105, "depreciation": 268,
      "other_income": 58, "interest": 110, "tax": 200, "minority_interest": 16,
      "equity": 3230, "minority_interest_bs": 85, "total_assets": 5590,
      "goodwill": 150, "intangibles": 75,
      "short_term_debt": 300, "long_term_debt": 800, "current_maturities": 130,
      "lease_liabilities": 225, "rou_assets": 215,
      "cash": 380, "current_investments": 200, "investments_in_associates": 110,
      "current_assets": 2560, "current_liabilities": 1420,
      "inventory": 920, "receivables": 1220, "payables": 690,
      "net_ppe": 1960, "cwip": 260,
      "cfo": 760, "capex": 420, "acquisitions": 0, "dividends_paid": 130,
      "interest_paid": 108, "cash_taxes_paid": 190, "lease_expense": 78,
      "shares_outstanding": 20.0, "diluted_shares": 20.2
    }
  ],
  "market": {
    "as_of": "2026-07-21",
    "price": 620,
    "diluted_shares": 20.2,
    "pension_deficit": 30,
    "preference_capital": 0,
    "other_debt_like": 0,
    "contingent_consideration": 0,
    "value_of_associates": 110
  }
}
--- EXAMPLE INPUT (end) ---

Running that example produces, among much else, a 14.2% revenue CAGR, an 18.6%
FY25 EBITDA margin, FY25 ROCE of 21.5% against ROIC of 16.1%, an EV of 13,404
built component by component, and two quality warnings: receivables compounding
at 20.3% against revenue at 14.2%, and a DSO that rises in every single year.
That pair is the classic early signature of channel stuffing or weakening
customers -- and it is invisible in the headline growth and margin figures,
which look excellent throughout.

Method notes that matter
------------------------
  * Balance-sheet denominators use the **average** of opening and closing
    balances wherever a prior period exists; the earliest period necessarily
    uses closing balances and is marked as such.
  * NOPAT uses a **normalised** tax rate (aggregate tax / aggregate PBT across
    all supplied periods), not one year's effective rate. Override with
    ``--tax-rate``. India: a company that elected s.115BAA is not comparable to
    its own pre-FY20 history; hold the rate constant for cross-cycle work.
  * "OPM" is reported as the EBITDA margin (the Indian screener convention) and
    separately as the EBIT margin. They are different numbers; the label is
    always explicit here so the two are never mixed.
  * Invested capital is computed by both the financing route and the operating
    route and the two are reconciled. A gap means something is misclassified.
  * ROIIC lags the capital denominator by one year, per the standard
    construction, whenever enough periods are supplied.
  * A silently wrong EV corrupts every EV multiple, so the bridge is printed
    component by component, with every component that was *not* supplied listed
    explicitly.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

# --------------------------------------------------------------------------- #
# Types and constants
# --------------------------------------------------------------------------- #

Number = Optional[float]
# A computed cell is (value, reason_it_is_missing). Exactly one is not None.
Cell = Tuple[Number, Optional[str]]

DAYS_IN_YEAR = 365.0

#: Period fields the script understands. Anything else is reported as a typo
#: risk rather than silently ignored.
KNOWN_PERIOD_FIELDS = {
    # metadata
    "label", "years_from_prior", "note",
    # income statement
    "revenue", "cogs", "gross_profit", "ebitda", "depreciation", "ebit",
    "other_income", "interest", "pbt", "tax", "cash_taxes_paid",
    "minority_interest", "associate_profit", "exceptional_items", "pat",
    # balance sheet
    "equity", "minority_interest_bs", "total_assets", "goodwill", "intangibles",
    "short_term_debt", "long_term_debt", "current_maturities", "gross_debt",
    "lease_liabilities", "rou_assets", "cash", "current_investments",
    "investments_in_associates", "current_assets", "current_liabilities",
    "inventory", "receivables", "payables", "net_ppe", "cwip",
    "pension_deficit", "preference_capital", "other_debt_like",
    # cash flow
    "cfo", "capex", "acquisitions", "dividends_paid", "interest_paid",
    "lease_expense", "preference_dividends",
    # shares
    "shares_outstanding", "diluted_shares", "dividend_per_share",
}

KNOWN_MARKET_FIELDS = {
    "price", "as_of", "market_cap", "diluted_shares", "shares_outstanding",
    "surplus_cash", "preference_capital", "minority_interest",
    "pension_deficit", "other_debt_like", "contingent_consideration",
    "value_of_associates", "note",
}

#: Sectors where the standard ratio set is meaningless or inverted.
FINANCIAL_SECTOR_KEYS = {
    "bank", "banks", "banking", "nbfc", "nbfcs", "hfc", "hfcs", "lender",
    "financial", "financials", "finance", "insurance", "insurer", "insurers",
    "life-insurance", "general-insurance", "reit", "reits", "invit", "invits",
    "realestate-reit",
}

#: Subset of the above where enterprise value itself has no meaning, so every
#: EV multiple is suppressed rather than printed as a plausible-looking number.
EV_MEANINGLESS_SECTOR_KEYS = {
    "bank", "banks", "banking", "nbfc", "nbfcs", "hfc", "hfcs", "lender",
    "financial", "financials", "finance", "insurance", "insurer", "insurers",
    "life-insurance", "general-insurance",
}

SECTOR_GATE_MESSAGE = {
    "bank": (
        "BANK / LENDER. Debt is raw material, not financing. Invested capital, "
        "NOPAT, enterprise value, EV multiples, net debt/EBITDA, interest "
        "coverage and ROIC are undefined for a bank; a bank is supposed to run "
        "8-15x assets/equity, so the DuPont equity multiplier is the business "
        "model and not a warning. Use ROA and ROE together with CET1/CAR, NIM, "
        "cost-to-income, credit cost and RoRWA. See references/sectors/banks.md."
    ),
    "nbfc": (
        "NBFC / HFC. Leverage is the product. Use the lender form of DuPont: "
        "ROA decomposed into NIM + fees - opex - credit cost, times the equity "
        "multiplier, with leverage read against the regulatory ceiling. EV and "
        "ROIC are meaningless. See references/sectors/nbfc.md."
    ),
    "insurance": (
        "INSURER. New-business strain depresses reported ROE precisely when the "
        "company is writing profitable growth, and invested capital is not "
        "meaningful against float. Life: ROEV, VNB margin, operating variances. "
        "General: combined ratio, ROE ex-investment gains. "
        "See references/sectors/insurance.md."
    ),
    "reit": (
        "REIT / InvIT. Assets are carried at fair value and the asset is the "
        "business, so ROIC collapses toward the cap rate by construction and "
        "earnings-based multiples are distorted by depreciation. Use AFFO "
        "yield, NOI yield on cost, cap rate vs cost of debt and LTV. "
        "See references/sectors/realestate-reit.md."
    ),
}


# --------------------------------------------------------------------------- #
# Small numeric helpers -- every one of these is explicit about failure
# --------------------------------------------------------------------------- #

def to_number(value: Any, where: str, key: str) -> Number:
    """Coerce an input value to float, or None if it is absent.

    Empty strings, ``None`` and the strings "na"/"n/a"/"-" all mean "not
    supplied". Anything else that is not numeric raises ValueError naming the
    period and the key, because a silently dropped input is how a wrong number
    reaches a report.
    """
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError("%s: field '%s' is a boolean; expected a number" % (where, key))
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        text = value.strip().replace(",", "")
        if text == "" or text.lower() in {"na", "n/a", "-", "nil", "none"}:
            return None
        try:
            return float(text)
        except ValueError:
            raise ValueError(
                "%s: field '%s' has non-numeric value %r" % (where, key, value)
            )
    raise ValueError("%s: field '%s' has unsupported type %s" % (where, key, type(value).__name__))


def divide(
    numerator: Number,
    denominator: Number,
    num_label: str,
    den_label: str,
    scale: float = 1.0,
    require_positive_denominator: bool = False,
) -> Cell:
    """Divide with explicit None / zero / negative-denominator handling.

    Returns ``(value, None)`` on success and ``(None, reason)`` otherwise. The
    reason names the missing or offending input so the caller can print exactly
    why a metric could not be computed.

    ``require_positive_denominator`` is used for ratios that are not merely
    unusual but *uninterpretable* when the base is negative -- ROE on negative
    equity, ROIC on negative invested capital, a CAGR off a negative start.
    """
    if numerator is None:
        return None, "%s not available" % num_label
    if denominator is None:
        return None, "%s not available" % den_label
    if denominator == 0:
        return None, "%s is zero" % den_label
    if require_positive_denominator and denominator < 0:
        return None, "%s is negative (%s) - ratio is not meaningful" % (
            den_label, format_number(denominator),
        )
    return numerator / denominator * scale, None


def subtract(a: Number, b: Number) -> Number:
    """Subtract, propagating None (a missing input must not become zero)."""
    if a is None or b is None:
        return None
    return a - b


def add_optional(*values: Number) -> Number:
    """Sum values, returning None if every value is None; absent parts count 0.

    Used only where a component genuinely defaults to zero when a company does
    not have it (no leases, no minorities). Callers that must not default are
    expected to use ``subtract``/direct access instead.
    """
    present = [v for v in values if v is not None]
    if not present:
        return None
    return float(sum(present))


def sum_strict(*values: Number) -> Number:
    """Sum, returning None if any component is missing."""
    if any(v is None for v in values):
        return None
    return float(sum(v for v in values if v is not None))


def cagr(begin: Number, end: Number, years: float, label: str) -> Cell:
    """Compound annual growth rate in percent, with sign handling made explicit.

    A CAGR from a negative or zero base is arithmetically undefined, and a CAGR
    to a negative endpoint is meaningless; both are reported as such rather
    than returned as a number.
    """
    if begin is None or end is None:
        return None, "%s not available for both endpoints" % label
    if years <= 0:
        return None, "period span is zero"
    if begin <= 0:
        return None, "%s starts at %s - CAGR from a non-positive base is undefined" % (
            label, format_number(begin),
        )
    if end <= 0:
        return None, "%s ends at %s - CAGR to a non-positive value is undefined" % (
            label, format_number(end),
        )
    return ((end / begin) ** (1.0 / years) - 1.0) * 100.0, None


def yoy(prev: Number, cur: Number, label: str) -> Cell:
    """Year-on-year growth in percent, undefined off a non-positive base."""
    if prev is None or cur is None:
        return None, "%s not available for both periods" % label
    if prev == 0:
        return None, "prior-period %s is zero" % label
    if prev < 0:
        return None, "prior-period %s is negative (%s) - growth rate is not meaningful" % (
            label, format_number(prev),
        )
    return (cur / prev - 1.0) * 100.0, None


def format_number(value: Number, decimals: int = 1) -> str:
    """Format an absolute figure with thousands separators."""
    if value is None:
        return "n/a"
    return "{:,.{d}f}".format(value, d=decimals)


def format_cell(cell: Cell, unit: str) -> str:
    """Render a computed cell for the text table."""
    value, _reason = cell
    if value is None:
        return "n/a"
    if unit == "%":
        return "{:,.1f}%".format(value)
    if unit == "x":
        return "{:,.2f}x".format(value)
    if unit == "days":
        return "{:,.0f}d".format(value)
    if unit == "abs":
        return format_number(value, 1)
    if unit == "ps":
        return "{:,.2f}".format(value)
    if unit == "count":
        return "{:,.2f}".format(value)
    return "{:,.2f}".format(value)


# --------------------------------------------------------------------------- #
# Period model
# --------------------------------------------------------------------------- #

class Period:
    """One reporting period, with unambiguous line-item derivations applied.

    Only derivations that cannot change the meaning of the number are performed
    (gross profit from revenue less COGS, EBIT from EBITDA less depreciation,
    and so on). Every derivation is recorded in ``self.derivations`` and printed
    under INPUT INTEGRITY so a reader can see which figures came from the filing
    and which the script inferred.
    """

    def __init__(self, raw: Dict[str, Any], index: int) -> None:
        """Parse one raw period object and apply the safe derivations."""
        self.index = index
        self.label = str(raw.get("label") or "P%d" % (index + 1))
        where = "period '%s'" % self.label
        self.unknown_keys = sorted(k for k in raw if k not in KNOWN_PERIOD_FIELDS)
        self.data: Dict[str, Number] = {}
        for key, value in raw.items():
            if key in {"label", "note"}:
                continue
            if key not in KNOWN_PERIOD_FIELDS:
                continue
            self.data[key] = to_number(value, where, key)
        self.years_from_prior = self.data.pop("years_from_prior", None)
        self.derivations: List[str] = []
        self._derive()

    # -- access ------------------------------------------------------------ #

    def get(self, field: str) -> Number:
        """Return a line item, or None if it was neither supplied nor derived."""
        return self.data.get(field)

    def has(self, field: str) -> bool:
        """True when a line item is available."""
        return self.data.get(field) is not None

    def _set(self, field: str, value: Number, how: str) -> None:
        """Record a derived line item and how it was obtained."""
        if value is None or self.data.get(field) is not None:
            return
        self.data[field] = value
        self.derivations.append("%s: %s = %s" % (self.label, field, how))

    # -- derivation -------------------------------------------------------- #

    def _derive(self) -> None:
        """Fill in line items that follow unambiguously from those supplied."""
        d = self.data

        # Income statement ladder.
        if d.get("gross_profit") is None and d.get("revenue") is not None and d.get("cogs") is not None:
            self._set("gross_profit", d["revenue"] - d["cogs"], "revenue - COGS")
        if d.get("cogs") is None and d.get("revenue") is not None and d.get("gross_profit") is not None:
            self._set("cogs", d["revenue"] - d["gross_profit"], "revenue - gross profit")
        if d.get("ebitda") is None and d.get("ebit") is not None and d.get("depreciation") is not None:
            self._set("ebitda", d["ebit"] + d["depreciation"], "EBIT + depreciation & amortisation")
        if d.get("ebit") is None and d.get("ebitda") is not None and d.get("depreciation") is not None:
            self._set("ebit", d["ebitda"] - d["depreciation"], "EBITDA - depreciation & amortisation")
        if d.get("depreciation") is None and d.get("ebitda") is not None and d.get("ebit") is not None:
            self._set("depreciation", d["ebitda"] - d["ebit"], "EBITDA - EBIT")

        # PBT only where the bridge is unambiguous: no exceptional items, and
        # other income / interest both stated.
        if (
            d.get("pbt") is None
            and d.get("ebit") is not None
            and d.get("interest") is not None
            and not d.get("exceptional_items")
        ):
            other = d.get("other_income") or 0.0
            assoc = d.get("associate_profit") or 0.0
            self._set(
                "pbt",
                d["ebit"] + other + assoc - d["interest"],
                "EBIT + other income + associate profit - interest (no exceptional items supplied)",
            )
        if d.get("pat") is None and d.get("pbt") is not None and d.get("tax") is not None:
            minority = d.get("minority_interest") or 0.0
            self._set(
                "pat",
                d["pbt"] - d["tax"] - minority,
                "PBT - tax - minority interest",
            )
        if d.get("tax") is None and d.get("pbt") is not None and d.get("pat") is not None:
            minority = d.get("minority_interest") or 0.0
            self._set("tax", d["pbt"] - d["pat"] - minority, "PBT - PAT - minority interest")

        # Debt aggregation.
        if d.get("gross_debt") is None:
            parts = [d.get("short_term_debt"), d.get("long_term_debt"), d.get("current_maturities")]
            if any(p is not None for p in parts):
                self._set(
                    "gross_debt",
                    float(sum(p for p in parts if p is not None)),
                    "sum of supplied debt components (short-term + long-term + current maturities)",
                )

        # Cash-flow derivations.
        if d.get("capex") is not None and d.get("cfo") is not None:
            self._set("fcf", d["cfo"] - d["capex"], "CFO - capex")

    # -- composite balance-sheet quantities -------------------------------- #

    def debt_including_leases(self) -> Number:
        """Gross debt plus capitalised lease liabilities (leases default to 0)."""
        gross = self.get("gross_debt")
        if gross is None:
            return None
        return gross + (self.get("lease_liabilities") or 0.0)

    def liquid_assets(self) -> Number:
        """Cash and equivalents plus current investments / liquid funds.

        Indian filings park surplus treasury in "current investments" (liquid
        mutual funds) rather than in "cash and cash equivalents"; both lines
        must be read or net debt is overstated.
        """
        return add_optional(self.get("cash"), self.get("current_investments"))

    def net_debt(self) -> Number:
        """Gross debt + leases - cash - current investments."""
        debt = self.debt_including_leases()
        if debt is None:
            return None
        liquid = self.liquid_assets()
        if liquid is None:
            return None
        return debt - liquid

    def net_working_capital(self) -> Number:
        """Operating working capital: current assets and liabilities, ex-finance.

        Cash, current investments, short-term debt and current maturities are
        removed so that a change in the treasury or the revolver does not read
        as a change in operating working-capital intensity.
        """
        ca, cl = self.get("current_assets"), self.get("current_liabilities")
        if ca is None or cl is None:
            return None
        operating_ca = ca - (self.get("cash") or 0.0) - (self.get("current_investments") or 0.0)
        operating_cl = cl - (self.get("short_term_debt") or 0.0) - (self.get("current_maturities") or 0.0)
        return operating_ca - operating_cl

    def invested_capital_financing(self) -> Cell:
        """Invested capital, financing route.

        equity + minority interest + debt + leases - surplus cash and
        non-operating investments. Returns the standard (value, reason) cell.
        """
        equity = self.get("equity")
        if equity is None:
            return None, "shareholders' equity not available"
        debt = self.debt_including_leases()
        if debt is None:
            return None, "gross debt not available"
        liquid = self.liquid_assets()
        if liquid is None:
            return None, "cash / current investments not available"
        value = (
            equity
            + (self.get("minority_interest_bs") or 0.0)
            + debt
            - liquid
            - (self.get("investments_in_associates") or 0.0)
        )
        return value, None

    def invested_capital_operating(self) -> Cell:
        """Invested capital, operating route.

        net working capital + net PP&E + CWIP + right-of-use assets + goodwill
        and acquired intangibles. Computed independently of the financing route
        so the two can be reconciled; a material gap means something is
        misclassified.
        """
        nwc = self.net_working_capital()
        if nwc is None:
            return None, "current assets / current liabilities not available"
        ppe = self.get("net_ppe")
        if ppe is None:
            return None, "net PP&E not available"
        value = (
            nwc
            + ppe
            + (self.get("cwip") or 0.0)
            + (self.get("rou_assets") or self.get("lease_liabilities") or 0.0)
            + (self.get("goodwill") or 0.0)
            + (self.get("intangibles") or 0.0)
        )
        return value, None

    def capital_employed(self) -> Cell:
        """Capital employed for ROCE: total assets less current liabilities."""
        ta, cl = self.get("total_assets"), self.get("current_liabilities")
        if ta is not None and cl is not None:
            return ta - cl, None
        equity = self.get("equity")
        debt = self.debt_including_leases()
        if equity is not None and debt is not None:
            return equity + (self.get("minority_interest_bs") or 0.0) + debt, None
        return None, "total assets and current liabilities not available (nor equity + debt)"

    def tangible_equity(self) -> Number:
        """Equity less goodwill and acquired intangibles."""
        equity = self.get("equity")
        if equity is None:
            return None
        return equity - (self.get("goodwill") or 0.0) - (self.get("intangibles") or 0.0)

    def tangible_invested_capital(self) -> Cell:
        """Invested capital excluding goodwill and acquired intangibles.

        Excluding goodwill measures how well the *operations* use capital;
        including it measures capital allocation. Both are reported.
        """
        base, reason = self.invested_capital_financing()
        if base is None:
            return None, reason
        return base - (self.get("goodwill") or 0.0) - (self.get("intangibles") or 0.0), None


# --------------------------------------------------------------------------- #
# Output containers
# --------------------------------------------------------------------------- #

class Section:
    """A titled block of per-period rows plus whole-period scalar rows."""

    def __init__(self, title: str, period_labels: Sequence[str], note: Optional[str] = None) -> None:
        """Create an empty section with a title, column labels and an optional note."""
        self.title = title
        self.period_labels = list(period_labels)
        self.note = note
        self.rows: List[Dict[str, Any]] = []
        self.scalars: List[Dict[str, Any]] = []
        self.suppressed: Optional[str] = None

    def add(self, name: str, unit: str, cells: Sequence[Cell]) -> None:
        """Add a row with one cell per period."""
        self.rows.append({"name": name, "unit": unit, "cells": list(cells)})

    def add_scalar(self, name: str, unit: str, cell: Cell) -> None:
        """Add a single figure that spans the whole period set (a CAGR, ROIIC)."""
        self.scalars.append({"name": name, "unit": unit, "cell": cell})

    def suppress(self, reason: str) -> None:
        """Mark the whole section as not applicable, with the reason shown."""
        self.suppressed = reason


class Warning_:
    """One triggered quality test, carrying the values that triggered it."""

    def __init__(self, test: str, severity: str, detail: str, values: Dict[str, Any]) -> None:
        """Record a triggered test, its severity, the explanation and the inputs."""
        self.test = test
        self.severity = severity  # "high" | "medium"
        self.detail = detail
        self.values = values

    def to_dict(self) -> Dict[str, Any]:
        """Serialise for --json output."""
        return {
            "test": self.test,
            "severity": self.severity,
            "detail": self.detail,
            "values": self.values,
        }


# --------------------------------------------------------------------------- #
# The analysis engine
# --------------------------------------------------------------------------- #

class Analysis:
    """Computes the full ratio set from a parsed input document."""

    def __init__(self, doc: Dict[str, Any], options: argparse.Namespace) -> None:
        """Validate the input document, build the period list and fix the tax rate.

        Raises ValueError with a specific message on any structural problem, so
        a malformed input fails loudly rather than producing a partial report.
        """
        self.options = options
        self.company = str(doc.get("company") or "(unnamed company)")
        self.currency = str(doc.get("currency") or "units not stated")
        self.basis = str(doc.get("basis") or "basis not stated (consolidated vs standalone!)")
        self.source = doc.get("source")
        self.sector_raw = (options.sector or doc.get("sector") or "").strip()
        self.sector_key = self.sector_raw.lower().replace(" ", "-")

        raw_periods = doc.get("periods")
        if not isinstance(raw_periods, list) or not raw_periods:
            raise ValueError("input must contain a non-empty 'periods' list")
        if str(doc.get("periods_order", "oldest_first")).lower() in {"newest_first", "reverse", "desc"}:
            raw_periods = list(reversed(raw_periods))
        self.periods: List[Period] = [Period(p, i) for i, p in enumerate(raw_periods)]
        self.n = len(self.periods)
        self.labels = [p.label for p in self.periods]

        market = doc.get("market") or {}
        if not isinstance(market, dict):
            raise ValueError("'market' must be an object")
        self.market: Dict[str, Any] = {}
        self.unknown_market_keys = sorted(k for k in market if k not in KNOWN_MARKET_FIELDS)
        for key, value in market.items():
            if key in {"as_of", "note"} or key not in KNOWN_MARKET_FIELDS:
                self.market[key] = value
                continue
            self.market[key] = to_number(value, "market", key)

        self.cautions: List[str] = []
        self.method_notes: List[str] = []
        self.sections: List[Section] = []
        self.warnings: List[Warning_] = []
        self.ev_bridge: Dict[str, Any] = {}

        self.period_years = float(options.period_years)
        self.normalised_tax_rate: Number = None
        self.tax_rate_basis = ""

        self._collect_input_cautions()
        self._set_tax_rate()

    # -- setup ------------------------------------------------------------- #

    def _collect_input_cautions(self) -> None:
        """Record input-integrity issues: unknown keys, derivations, ordering."""
        for period in self.periods:
            for key in period.unknown_keys:
                self.cautions.append(
                    "period '%s': unrecognised field '%s' was ignored - check for a typo"
                    % (period.label, key)
                )
        for key in self.unknown_market_keys:
            self.cautions.append("market: unrecognised field '%s' was ignored" % key)
        if self.n < 2:
            self.cautions.append(
                "only one period supplied: growth, CAGR, ROIIC, average balances and "
                "trend-based quality tests cannot be computed"
            )
        if "consolidated" not in self.basis.lower() and "standalone" not in self.basis.lower():
            self.cautions.append(
                "'basis' does not state consolidated vs standalone - for any company with "
                "subsidiaries these differ materially and mixing them invalidates every ratio"
            )

    def _set_tax_rate(self) -> None:
        """Establish the normalised tax rate used for NOPAT.

        Aggregate tax over aggregate PBT across all supplied periods, which is
        more stable than any single year's effective rate. ``--tax-rate``
        overrides it; ``--use-cash-tax`` uses cash taxes paid instead of the
        book charge.
        """
        if self.options.tax_rate is not None:
            self.normalised_tax_rate = float(self.options.tax_rate) / 100.0
            self.tax_rate_basis = "supplied via --tax-rate"
            self.method_notes.append(
                "NOPAT uses a tax rate of %.1f%% supplied on the command line."
                % (self.normalised_tax_rate * 100.0)
            )
            return

        tax_field = "cash_taxes_paid" if self.options.use_cash_tax else "tax"
        taxes, pbts = 0.0, 0.0
        used = []
        for period in self.periods:
            tax, pbt = period.get(tax_field), period.get("pbt")
            if tax is None or pbt is None or pbt <= 0:
                continue
            taxes += tax
            pbts += pbt
            used.append(period.label)
        if pbts > 0:
            self.normalised_tax_rate = taxes / pbts
            self.tax_rate_basis = "aggregate %s / aggregate PBT over %s" % (
                "cash taxes paid" if self.options.use_cash_tax else "tax charge",
                ", ".join(used),
            )
            self.method_notes.append(
                "NOPAT uses a normalised tax rate of %.1f%% (%s), not any single year's "
                "effective rate. India: an entity that elected s.115BAA is not comparable "
                "to its own pre-FY20 history - hold the rate constant for cross-cycle work."
                % (self.normalised_tax_rate * 100.0, self.tax_rate_basis)
            )
        else:
            self.tax_rate_basis = "not derivable (tax and positive PBT not both available)"
            self.cautions.append(
                "normalised tax rate could not be derived, so NOPAT, ROIC, return on "
                "tangible capital and ROIIC are unavailable; supply tax and PBT, or pass "
                "--tax-rate"
            )

    # -- generic accessors ------------------------------------------------- #

    def value(self, i: int, field: str) -> Number:
        """Line item for period i."""
        return self.periods[i].get(field)

    def average_balance(self, i: int, field: str) -> Cell:
        """Average of opening and closing balance for period i, where possible.

        Falls back to the closing balance for the earliest period (or when the
        prior year's figure is missing) and says so, because pairing a full
        year of profit with a year-end balance after a mid-year acquisition is
        one of the standard ways an ROCE series lies.
        """
        current = self.value(i, field)
        if current is None:
            return None, "%s not available" % field.replace("_", " ")
        if i == 0:
            return current, None
        prior = self.value(i - 1, field)
        if prior is None:
            return current, None
        return (current + prior) / 2.0, None

    def average_of(self, i: int, getter: Callable[[int], Cell]) -> Cell:
        """Average a computed balance (e.g. invested capital) over the period."""
        current, reason = getter(i)
        if current is None:
            return None, reason
        if i == 0:
            return current, None
        prior, _ = getter(i - 1)
        if prior is None:
            return current, None
        return (current + prior) / 2.0, None

    def ic_financing(self, i: int) -> Cell:
        """Invested capital (financing route) for period i."""
        return self.periods[i].invested_capital_financing()

    def ic_operating(self, i: int) -> Cell:
        """Invested capital (operating route) for period i."""
        return self.periods[i].invested_capital_operating()

    def capital_employed(self, i: int) -> Cell:
        """Capital employed for period i."""
        return self.periods[i].capital_employed()

    def tangible_ic(self, i: int) -> Cell:
        """Tangible invested capital for period i."""
        return self.periods[i].tangible_invested_capital()

    def nopat(self, i: int) -> Cell:
        """NOPAT = EBIT x (1 - normalised tax rate)."""
        ebit = self.value(i, "ebit")
        if ebit is None:
            return None, "EBIT not available"
        if self.normalised_tax_rate is None:
            return None, "normalised tax rate not derivable (%s)" % self.tax_rate_basis
        return ebit * (1.0 - self.normalised_tax_rate), None

    def series(self, fn: Callable[[int], Cell]) -> List[Cell]:
        """Evaluate fn for every period, returning one cell per period."""
        return [fn(i) for i in range(self.n)]

    def blank_first(self) -> Cell:
        """The standard 'no prior period' cell for YoY-style rows."""
        return None, "no prior period"

    # ------------------------------------------------------------------ #
    # Sections
    # ------------------------------------------------------------------ #

    def build_all(self) -> None:
        """Compute every section, the EV bridge and the quality warnings."""
        self.method_notes.append(
            "Balance-sheet denominators use the average of opening and closing balances "
            "wherever a prior period exists; the earliest period necessarily uses closing "
            "balances."
        )
        self.method_notes.append(
            "Periods are assumed to be %.2f year(s) apart (change with --period-years)."
            % self.period_years
        )
        self.sections.append(self.section_growth())
        self.sections.append(self.section_margins())
        self.sections.append(self.section_returns())
        self.sections.append(self.section_dupont3())
        self.sections.append(self.section_dupont5())
        self.sections.append(self.section_incremental())
        self.sections.append(self.section_leverage())
        self.sections.append(self.section_liquidity())
        self.sections.append(self.section_working_capital())
        self.sections.append(self.section_cash_quality())
        self.sections.append(self.section_per_share())
        self.build_ev_bridge()
        self.sections.append(self.section_valuation())
        self.detect_quality_warnings()

    # -- growth ------------------------------------------------------------ #

    def section_growth(self) -> Section:
        """Year-on-year growth and full-period CAGRs for the top lines."""
        section = Section("GROWTH", self.labels)
        span = (self.n - 1) * self.period_years

        for field, name in (
            ("revenue", "Revenue"),
            ("gross_profit", "Gross profit"),
            ("ebitda", "EBITDA"),
            ("ebit", "EBIT"),
            ("pat", "PAT"),
        ):
            cells: List[Cell] = [self.blank_first()]
            for i in range(1, self.n):
                cells.append(yoy(self.value(i - 1, field), self.value(i, field), name.lower()))
            section.add("%s YoY" % name, "%", cells)

        for field, name in (
            ("revenue", "Revenue"),
            ("ebitda", "EBITDA"),
            ("pat", "PAT"),
            ("gross_profit", "Gross profit"),
        ):
            if self.n < 2:
                section.add_scalar("%s CAGR" % name, "%", (None, "needs at least two periods"))
                continue
            section.add_scalar(
                "%s CAGR (%s -> %s, %.1fy)" % (name, self.labels[0], self.labels[-1], span),
                "%",
                cagr(self.value(0, field), self.value(self.n - 1, field), span, name.lower()),
            )

        # A 3-year CAGR alongside the full span, where the history allows it.
        if self.n >= 4:
            span3 = 3 * self.period_years
            for field, name in (("revenue", "Revenue"), ("ebitda", "EBITDA"), ("pat", "PAT")):
                section.add_scalar(
                    "%s CAGR (last %.1fy)" % (name, span3),
                    "%",
                    cagr(self.value(self.n - 4, field), self.value(self.n - 1, field), span3, name.lower()),
                )
        return section

    # -- margins ----------------------------------------------------------- #

    def section_margins(self) -> Section:
        """The full margin ladder, from gross margin down to net margin."""
        section = Section(
            "MARGIN LADDER",
            self.labels,
            note=(
                "'OPM' in Indian screeners is the EBITDA margin; the EBIT margin is a "
                "different number. Both are labelled explicitly here so they are never mixed."
            ),
        )
        rev = lambda i: self.value(i, "revenue")  # noqa: E731 - local shorthand

        section.add("Revenue", "abs", self.series(lambda i: (rev(i), "revenue not available")
                                                  if rev(i) is None else (rev(i), None)))
        section.add("Gross margin", "%", self.series(
            lambda i: divide(self.value(i, "gross_profit"), rev(i), "gross profit", "revenue", 100.0)))
        section.add("EBITDA margin (OPM)", "%", self.series(
            lambda i: divide(self.value(i, "ebitda"), rev(i), "EBITDA", "revenue", 100.0)))
        section.add("EBIT margin", "%", self.series(
            lambda i: divide(self.value(i, "ebit"), rev(i), "EBIT", "revenue", 100.0)))
        section.add("PBT margin", "%", self.series(
            lambda i: divide(self.value(i, "pbt"), rev(i), "PBT", "revenue", 100.0)))
        section.add("Net (PAT) margin", "%", self.series(
            lambda i: divide(self.value(i, "pat"), rev(i), "PAT", "revenue", 100.0)))
        section.add("Depreciation % of sales", "%", self.series(
            lambda i: divide(self.value(i, "depreciation"), rev(i), "depreciation", "revenue", 100.0)))
        section.add("Interest % of sales", "%", self.series(
            lambda i: divide(self.value(i, "interest"), rev(i), "interest", "revenue", 100.0)))
        section.add("Effective tax rate", "%", self.series(
            lambda i: divide(self.value(i, "tax"), self.value(i, "pbt"), "tax charge", "PBT", 100.0,
                             require_positive_denominator=True)))
        section.add("Cash tax rate", "%", self.series(
            lambda i: divide(self.value(i, "cash_taxes_paid"), self.value(i, "pbt"),
                             "cash taxes paid", "PBT", 100.0, require_positive_denominator=True)))
        return section

    # -- returns ----------------------------------------------------------- #

    def section_returns(self) -> Section:
        """ROE, ROCE, ROIC, ROA and the tangible-capital variants."""
        section = Section(
            "RETURNS ON CAPITAL",
            self.labels,
            note=(
                "Return on capital, not margin, is what compounds. Invested capital is "
                "computed by both routes and reconciled; a material gap means something is "
                "misclassified. ROIC excluding goodwill measures the operations, ROIC "
                "including it measures capital allocation - both are shown."
            ),
        )
        section.add("NOPAT", "abs", self.series(self.nopat))
        section.add("Invested capital (financing route)", "abs", self.series(self.ic_financing))
        section.add("Invested capital (operating route)", "abs", self.series(self.ic_operating))

        def reconciliation(i: int) -> Cell:
            """Financing-route minus operating-route invested capital."""
            a, reason_a = self.ic_financing(i)
            b, reason_b = self.ic_operating(i)
            if a is None:
                return None, reason_a
            if b is None:
                return None, reason_b
            return a - b, None

        section.add("  reconciliation gap (fin - op)", "abs", self.series(reconciliation))
        section.add("Capital employed", "abs", self.series(self.capital_employed))

        section.add("ROE", "%", self.series(
            lambda i: divide(self.value(i, "pat"), self.average_balance(i, "equity")[0],
                             "PAT", "average shareholders' equity", 100.0,
                             require_positive_denominator=True)))
        section.add("ROCE (EBIT / avg capital employed)", "%", self.series(
            lambda i: divide(self.value(i, "ebit"), self.average_of(i, self.capital_employed)[0],
                             "EBIT", "average capital employed", 100.0,
                             require_positive_denominator=True)))
        section.add("ROIC (NOPAT / avg invested capital)", "%", self.series(
            lambda i: divide(self.nopat(i)[0], self.average_of(i, self.ic_financing)[0],
                             "NOPAT", "average invested capital", 100.0,
                             require_positive_denominator=True)))
        section.add("ROIC ex-goodwill (tangible capital)", "%", self.series(
            lambda i: divide(self.nopat(i)[0], self.average_of(i, self.tangible_ic)[0],
                             "NOPAT", "average tangible invested capital", 100.0,
                             require_positive_denominator=True)))
        section.add("Return on tangible equity", "%", self.series(
            lambda i: divide(self.value(i, "pat"),
                             self.average_of(i, lambda j: (self.periods[j].tangible_equity(),
                                                           "equity not available"))[0],
                             "PAT", "average tangible equity", 100.0,
                             require_positive_denominator=True)))
        section.add("ROA (PAT / avg total assets)", "%", self.series(
            lambda i: divide(self.value(i, "pat"), self.average_balance(i, "total_assets")[0],
                             "PAT", "average total assets", 100.0,
                             require_positive_denominator=True)))
        section.add("NOPAT margin", "%", self.series(
            lambda i: divide(self.nopat(i)[0], self.value(i, "revenue"), "NOPAT", "revenue", 100.0)))
        section.add("Capital turnover (sales / avg IC)", "x", self.series(
            lambda i: divide(self.value(i, "revenue"), self.average_of(i, self.ic_financing)[0],
                             "revenue", "average invested capital",
                             require_positive_denominator=True)))
        section.add("Fixed-asset turnover (sales / avg net PP&E)", "x", self.series(
            lambda i: divide(self.value(i, "revenue"), self.average_balance(i, "net_ppe")[0],
                             "revenue", "average net PP&E", require_positive_denominator=True)))
        return section

    # -- DuPont ------------------------------------------------------------ #

    def section_dupont3(self) -> Section:
        """3-step DuPont: what kind of business is this."""
        section = Section(
            "DUPONT - 3 STEP  (ROE = net margin x asset turnover x equity multiplier)",
            self.labels,
            note="Answers 'what kind of business is this'. Average balances are used, so "
                 "the product reconciles exactly to ROE.",
        )
        net_margin = self.series(
            lambda i: divide(self.value(i, "pat"), self.value(i, "revenue"), "PAT", "revenue"))
        asset_turnover = self.series(
            lambda i: divide(self.value(i, "revenue"), self.average_balance(i, "total_assets")[0],
                             "revenue", "average total assets", require_positive_denominator=True))
        equity_multiplier = self.series(
            lambda i: divide(self.average_balance(i, "total_assets")[0],
                             self.average_balance(i, "equity")[0],
                             "average total assets", "average equity",
                             require_positive_denominator=True))

        section.add("Net margin (PAT / sales)", "%", [
            (c[0] * 100.0 if c[0] is not None else None, c[1]) for c in net_margin])
        section.add("Asset turnover (sales / avg assets)", "x", asset_turnover)
        section.add("Equity multiplier (avg assets / avg equity)", "x", equity_multiplier)
        section.add("= ROE (product of the three)", "%", [
            self._product([net_margin[i], asset_turnover[i], equity_multiplier[i]], 100.0)
            for i in range(self.n)])
        section.add("ROE (direct: PAT / avg equity)", "%", self.series(
            lambda i: divide(self.value(i, "pat"), self.average_balance(i, "equity")[0],
                             "PAT", "average equity", 100.0, require_positive_denominator=True)))
        return section

    def section_dupont5(self) -> Section:
        """5-step DuPont: where the ROE is actually coming from."""
        section = Section(
            "DUPONT - 5 STEP  (ROE = tax burden x interest burden x EBIT margin x asset turnover x leverage)",
            self.labels,
            note=(
                "Separates operations-driven ROE (margin x turnover) from financing-driven "
                "ROE (tax burden, interest burden, leverage). Two firms with the same ROE "
                "and different decompositions are not comparable investments. Note that the "
                "interest burden can exceed 1.0 where other income is large, since PBT then "
                "sits above EBIT."
            ),
        )
        tax_burden = self.series(
            lambda i: divide(self.value(i, "pat"), self.value(i, "pbt"), "PAT", "PBT"))
        interest_burden = self.series(
            lambda i: divide(self.value(i, "pbt"), self.value(i, "ebit"), "PBT", "EBIT"))
        ebit_margin = self.series(
            lambda i: divide(self.value(i, "ebit"), self.value(i, "revenue"), "EBIT", "revenue"))
        asset_turnover = self.series(
            lambda i: divide(self.value(i, "revenue"), self.average_balance(i, "total_assets")[0],
                             "revenue", "average total assets", require_positive_denominator=True))
        leverage = self.series(
            lambda i: divide(self.average_balance(i, "total_assets")[0],
                             self.average_balance(i, "equity")[0],
                             "average total assets", "average equity",
                             require_positive_denominator=True))

        section.add("Tax burden (PAT / PBT)", "x", tax_burden)
        section.add("Interest burden (PBT / EBIT)", "x", interest_burden)
        section.add("EBIT margin (EBIT / sales)", "%", [
            (c[0] * 100.0 if c[0] is not None else None, c[1]) for c in ebit_margin])
        section.add("Asset turnover (sales / avg assets)", "x", asset_turnover)
        section.add("Equity multiplier (avg assets / avg equity)", "x", leverage)
        section.add("= ROE (product of the five)", "%", [
            self._product([tax_burden[i], interest_burden[i], ebit_margin[i],
                           asset_turnover[i], leverage[i]], 100.0)
            for i in range(self.n)])

        if self.n >= 2:
            section.add_scalar(
                "ROE driver over the full period",
                "text",
                self._dupont_attribution(tax_burden, interest_burden, ebit_margin,
                                         asset_turnover, leverage),
            )
        return section

    @staticmethod
    def _product(cells: Sequence[Cell], scale: float = 1.0) -> Cell:
        """Multiply cells, propagating the first missing-value reason."""
        total = scale
        for value, reason in cells:
            if value is None:
                return None, reason or "component not available"
            total *= value
        return total, None

    def _dupont_attribution(self, *term_series: Sequence[Cell]) -> Cell:
        """Name the DuPont term that moved most between first and last period.

        Uses the log-decomposition of a product: the term with the largest
        absolute change in log-value contributed most to the change in ROE.
        """
        names = ["tax burden", "interest burden", "EBIT margin", "asset turnover", "leverage"]
        contributions = []
        for name, cells in zip(names, term_series):
            first, last = cells[0][0], cells[-1][0]
            if first is None or last is None or first <= 0 or last <= 0:
                continue
            contributions.append((abs(math.log(last / first)), name, first, last))
        if not contributions:
            return None, "not enough positive terms in both endpoint periods"
        contributions.sort(reverse=True)
        _, name, first, last = contributions[0]
        operations = {"EBIT margin", "asset turnover"}
        character = "operations-driven" if name in operations else "financing/tax-driven"
        return (
            "largest move: %s, %.3f -> %.3f (%s)" % (name, first, last, character)
        ), None

    # -- incremental returns ----------------------------------------------- #

    def section_incremental(self) -> Section:
        """ROIIC, the reinvestment rate and the growth they jointly imply."""
        section = Section(
            "INCREMENTAL RETURNS",
            self.labels,
            note=(
                "Average ROIC is history; ROIIC is the forecast. The capital denominator is "
                "lagged one year because capital takes time to earn. Blended ROIC drifts "
                "toward ROIIC as new capital dominates the base - which is why a company can "
                "report record profits for years while every new rupee destroys value."
            ),
        )
        window = int(self.options.roiic_years)
        nopats = [self.nopat(i)[0] for i in range(self.n)]
        ics = [self.ic_financing(i)[0] for i in range(self.n)]
        last = self.n - 1
        roiic_cell: Cell = (None, "needs at least two periods")

        if self.n < 2:
            section.add_scalar("ROIIC", "%", roiic_cell)
        else:
            k = min(window, self.n - 1)
            lagged = self.n >= k + 2
            if lagged:
                num_hi, num_lo = last, last - k
                den_hi, den_lo = last - 1, last - k - 1
                basis = "%d-year, capital lagged one year (%s..%s vs capital %s..%s)" % (
                    k, self.labels[num_lo], self.labels[num_hi],
                    self.labels[den_lo], self.labels[den_hi])
            else:
                num_hi, num_lo = last, last - k
                den_hi, den_lo = last, last - k
                basis = "%d-year, capital NOT lagged (only %d periods supplied)" % (k, self.n)
            section.add_scalar("ROIIC basis", "text", (basis, None))
            roiic_cell = self._roiic(nopats, ics, num_lo, num_hi, den_lo, den_hi)
            section.add_scalar("ROIIC", "%", roiic_cell)
            section.add_scalar(
                "  change in NOPAT", "abs",
                (subtract(nopats[num_hi], nopats[num_lo]), "NOPAT not available for both endpoints")
                if nopats[num_hi] is not None and nopats[num_lo] is not None
                else (None, "NOPAT not available for both endpoints"))
            section.add_scalar(
                "  change in invested capital", "abs",
                (subtract(ics[den_hi], ics[den_lo]), None)
                if ics[den_hi] is not None and ics[den_lo] is not None
                else (None, "invested capital not available for both endpoints"))
            section.add_scalar(
                "ROIC at start of window", "%",
                divide(nopats[num_lo], ics[num_lo], "opening NOPAT", "opening invested capital",
                       100.0, require_positive_denominator=True))
            section.add_scalar(
                "ROIC at end of window", "%",
                divide(nopats[num_hi], ics[num_hi], "closing NOPAT", "closing invested capital",
                       100.0, require_positive_denominator=True))

        # Reinvestment rate, per period.
        def reinvestment(i: int) -> Cell:
            """(capex + acquisitions + change in NWC - depreciation) / NOPAT."""
            capex = self.value(i, "capex")
            if capex is None:
                return None, "capex not available"
            dep = self.value(i, "depreciation")
            if dep is None:
                return None, "depreciation not available"
            nopat_value, reason = self.nopat(i)
            if nopat_value is None:
                return None, reason
            if nopat_value <= 0:
                return None, "NOPAT is not positive - reinvestment rate is not meaningful"
            delta_nwc = 0.0
            if i > 0:
                cur = self.periods[i].net_working_capital()
                prev = self.periods[i - 1].net_working_capital()
                if cur is not None and prev is not None:
                    delta_nwc = cur - prev
            spend = capex + (self.value(i, "acquisitions") or 0.0) + delta_nwc - dep
            return spend / nopat_value * 100.0, None

        section.add("Reinvestment rate (% of NOPAT)", "%", self.series(reinvestment))
        section.add("Capex / depreciation", "x", self.series(
            lambda i: divide(self.value(i, "capex"), self.value(i, "depreciation"),
                             "capex", "depreciation")))

        if self.n >= 2:
            roiic_value, roiic_reason = roiic_cell
            reinvest_last, reinvest_reason = reinvestment(self.n - 1)
            if roiic_value is None or reinvest_last is None:
                section.add_scalar(
                    "Implied intrinsic growth (reinvestment x ROIIC)", "%",
                    (None, "needs both ROIIC and the latest reinvestment rate (%s)"
                     % (roiic_reason or reinvest_reason or "input missing")))
            else:
                section.add_scalar(
                    "Implied intrinsic growth (reinvestment x ROIIC)", "%",
                    (reinvest_last / 100.0 * roiic_value, None))
        return section

    @staticmethod
    def _roiic(nopats: Sequence[Number], ics: Sequence[Number],
               num_lo: int, num_hi: int, den_lo: int, den_hi: int) -> Cell:
        """Return on incremental invested capital over a window."""
        if nopats[num_hi] is None or nopats[num_lo] is None:
            return None, "NOPAT not available at both ends of the window"
        if ics[den_hi] is None or ics[den_lo] is None:
            return None, "invested capital not available at both ends of the window"
        delta_nopat = nopats[num_hi] - nopats[num_lo]
        delta_ic = ics[den_hi] - ics[den_lo]
        if delta_ic == 0:
            return None, "invested capital did not change over the window"
        if delta_ic < 0:
            return None, (
                "invested capital fell by %s over the window - ROIIC is not meaningful "
                "when the capital base shrinks (report the NOPAT change and the capital "
                "release separately)" % format_number(abs(delta_ic))
            )
        return delta_nopat / delta_ic * 100.0, None

    # -- leverage ---------------------------------------------------------- #

    def section_leverage(self) -> Section:
        """Debt levels and the coverage ratios that decide refinancing terms."""
        section = Section(
            "LEVERAGE AND COVERAGE",
            self.labels,
            note=(
                "Debt includes capitalised lease liabilities throughout. Net debt deducts "
                "cash and current investments (Indian filings park surplus treasury in "
                "current investments, not in cash). Every band is sector-dependent: 3x net "
                "debt/EBITDA is prudent for a contracted utility and reckless for a mid-cap "
                "with a 200-day cash cycle."
            ),
        )
        section.add("Gross debt (incl. leases)", "abs", self.series(
            lambda i: (self.periods[i].debt_including_leases(), "gross debt not available")
            if self.periods[i].debt_including_leases() is None
            else (self.periods[i].debt_including_leases(), None)))
        section.add("Net debt", "abs", self.series(
            lambda i: (self.periods[i].net_debt(), None)
            if self.periods[i].net_debt() is not None
            else (None, "gross debt or cash / current investments not available")))
        section.add("Debt / equity", "x", self.series(
            lambda i: divide(self.periods[i].debt_including_leases(), self.value(i, "equity"),
                             "gross debt incl. leases", "shareholders' equity",
                             require_positive_denominator=True)))
        section.add("Net debt / equity", "x", self.series(
            lambda i: divide(self.periods[i].net_debt(), self.value(i, "equity"),
                             "net debt", "shareholders' equity",
                             require_positive_denominator=True)))
        section.add("Net debt / EBITDA", "x", self.series(
            lambda i: divide(self.periods[i].net_debt(), self.value(i, "ebitda"),
                             "net debt", "EBITDA", require_positive_denominator=True)))
        section.add("Gross debt / EBITDA", "x", self.series(
            lambda i: divide(self.periods[i].debt_including_leases(), self.value(i, "ebitda"),
                             "gross debt", "EBITDA", require_positive_denominator=True)))

        def net_debt_over_ebitda_less_capex(i: int) -> Cell:
            """Leverage against the cash left after sustaining capital spend."""
            ebitda, capex = self.value(i, "ebitda"), self.value(i, "capex")
            if ebitda is None:
                return None, "EBITDA not available"
            if capex is None:
                return None, "capex not available"
            return divide(self.periods[i].net_debt(), ebitda - capex,
                          "net debt", "EBITDA less capex", require_positive_denominator=True)

        section.add("Net debt / (EBITDA - capex)", "x", self.series(net_debt_over_ebitda_less_capex))
        section.add("Interest coverage (EBIT / interest)", "x", self.series(
            lambda i: divide(self.value(i, "ebit"), self.value(i, "interest"),
                             "EBIT", "interest expense", require_positive_denominator=True)))
        section.add("EBITDA interest coverage", "x", self.series(
            lambda i: divide(self.value(i, "ebitda"), self.value(i, "interest"),
                             "EBITDA", "interest expense", require_positive_denominator=True)))

        def cash_interest_coverage(i: int) -> Cell:
            """(CFO before interest) / cash interest paid. Cash pays interest."""
            cfo, paid = self.value(i, "cfo"), self.value(i, "interest_paid")
            if cfo is None:
                return None, "CFO not available"
            if paid is None:
                return None, "interest paid (cash) not available"
            return divide(cfo + paid, paid, "CFO before interest", "cash interest paid",
                          require_positive_denominator=True)

        section.add("Cash interest coverage", "x", self.series(cash_interest_coverage))

        def fixed_charge_coverage(i: int) -> Cell:
            """(EBIT + lease expense) / (interest + lease expense + pref dividends).

            The only fair coverage measure where leases and preference capital
            are large -- retail, airlines, shipping, hotels.
            """
            ebit, interest = self.value(i, "ebit"), self.value(i, "interest")
            lease = self.value(i, "lease_expense")
            if ebit is None:
                return None, "EBIT not available"
            if interest is None:
                return None, "interest expense not available"
            if lease is None:
                return None, ("lease expense not available - without it this is just interest "
                              "coverage, which understates the fixed-charge burden of a "
                              "lease-heavy business")
            pref = self.value(i, "preference_dividends") or 0.0
            return divide(ebit + lease, interest + lease + pref,
                          "EBIT plus lease expense", "interest plus leases plus preference dividends",
                          require_positive_denominator=True)

        section.add("Fixed-charge coverage", "x", self.series(fixed_charge_coverage))
        return section

    # -- liquidity --------------------------------------------------------- #

    def section_liquidity(self) -> Section:
        """Current, quick and cash ratios."""
        section = Section("LIQUIDITY", self.labels)
        section.add("Current ratio", "x", self.series(
            lambda i: divide(self.value(i, "current_assets"), self.value(i, "current_liabilities"),
                             "current assets", "current liabilities",
                             require_positive_denominator=True)))

        def quick(i: int) -> Cell:
            """(Current assets - inventory) / current liabilities."""
            ca, inv = self.value(i, "current_assets"), self.value(i, "inventory")
            if ca is None:
                return None, "current assets not available"
            if inv is None:
                return None, "inventory not available"
            return divide(ca - inv, self.value(i, "current_liabilities"),
                          "current assets less inventory", "current liabilities",
                          require_positive_denominator=True)

        section.add("Quick ratio", "x", self.series(quick))
        section.add("Cash ratio", "x", self.series(
            lambda i: divide(self.periods[i].liquid_assets(), self.value(i, "current_liabilities"),
                             "cash and current investments", "current liabilities",
                             require_positive_denominator=True)))
        return section

    # -- working capital --------------------------------------------------- #

    def section_working_capital(self) -> Section:
        """DSO, DIO, DPO, the cash conversion cycle and working-capital intensity."""
        section = Section(
            "WORKING CAPITAL",
            self.labels,
            note=(
                "Days are computed on average balances. A CCC that improves because DPO "
                "jumped is supplier financing, and a CCC that improves because receivables "
                "were factored is a balance-sheet transaction - neither is an operating gain, "
                "and both reverse."
            ),
        )

        def dso(i: int) -> Cell:
            """Trade receivables / revenue x 365, on average balances."""
            avg, reason = self.average_balance(i, "receivables")
            if avg is None:
                return None, reason
            return divide(avg, self.value(i, "revenue"), "average receivables", "revenue",
                          DAYS_IN_YEAR, require_positive_denominator=True)

        def dio(i: int) -> Cell:
            """Inventory / COGS x 365, on average balances."""
            avg, reason = self.average_balance(i, "inventory")
            if avg is None:
                return None, reason
            return divide(avg, self.value(i, "cogs"), "average inventory", "COGS",
                          DAYS_IN_YEAR, require_positive_denominator=True)

        def dpo(i: int) -> Cell:
            """Trade payables / COGS x 365, on average balances."""
            avg, reason = self.average_balance(i, "payables")
            if avg is None:
                return None, reason
            return divide(avg, self.value(i, "cogs"), "average payables", "COGS",
                          DAYS_IN_YEAR, require_positive_denominator=True)

        dso_cells = self.series(dso)
        dio_cells = self.series(dio)
        dpo_cells = self.series(dpo)
        section.add("DSO (receivable days)", "days", dso_cells)
        section.add("DIO (inventory days)", "days", dio_cells)
        section.add("DPO (payable days)", "days", dpo_cells)

        ccc_cells: List[Cell] = []
        for i in range(self.n):
            parts = [dso_cells[i], dio_cells[i], dpo_cells[i]]
            missing = [c[1] for c in parts if c[0] is None]
            if missing:
                ccc_cells.append((None, "; ".join(sorted(set(m for m in missing if m)))))
            else:
                ccc_cells.append((dso_cells[i][0] + dio_cells[i][0] - dpo_cells[i][0], None))
        section.add("Cash conversion cycle (DSO + DIO - DPO)", "days", ccc_cells)

        section.add("Net working capital", "abs", self.series(
            lambda i: (self.periods[i].net_working_capital(), None)
            if self.periods[i].net_working_capital() is not None
            else (None, "current assets / current liabilities not available")))
        section.add("Net working capital / sales", "%", self.series(
            lambda i: divide(self.periods[i].net_working_capital(), self.value(i, "revenue"),
                             "net working capital", "revenue", 100.0)))

        def delta_nwc_over_delta_revenue(i: int) -> Cell:
            """Change in NWC divided by change in revenue: does growth eat cash?"""
            if i == 0:
                return None, "no prior period"
            cur, prev = self.periods[i].net_working_capital(), self.periods[i - 1].net_working_capital()
            if cur is None or prev is None:
                return None, "net working capital not available for both periods"
            rev_cur, rev_prev = self.value(i, "revenue"), self.value(i - 1, "revenue")
            if rev_cur is None or rev_prev is None:
                return None, "revenue not available for both periods"
            if rev_cur == rev_prev:
                return None, "revenue did not change"
            return (cur - prev) / (rev_cur - rev_prev) * 100.0, None

        section.add("Change in NWC / change in revenue", "%", self.series(delta_nwc_over_delta_revenue))
        return section

    # -- cash flow quality ------------------------------------------------- #

    def section_cash_quality(self) -> Section:
        """Whether the reported profit turns into cash."""
        section = Section(
            "CASH FLOW QUALITY",
            self.labels,
            note=(
                "The Sloan accrual ratio -- (net income - CFO) / average total assets -- is "
                "one of the most robust anomalies in the literature: above roughly 10% is a "
                "red flag for earnings reversal."
            ),
        )
        section.add("CFO", "abs", self.series(
            lambda i: (self.value(i, "cfo"), None) if self.value(i, "cfo") is not None
            else (None, "CFO not available")))
        section.add("Capex", "abs", self.series(
            lambda i: (self.value(i, "capex"), None) if self.value(i, "capex") is not None
            else (None, "capex not available")))
        section.add("Free cash flow (CFO - capex)", "abs", self.series(
            lambda i: (self.value(i, "fcf"), None) if self.value(i, "fcf") is not None
            else (None, "CFO or capex not available")))
        section.add("OCF / EBITDA", "x", self.series(
            lambda i: divide(self.value(i, "cfo"), self.value(i, "ebitda"), "CFO", "EBITDA",
                             require_positive_denominator=True)))
        section.add("OCF / net profit", "x", self.series(
            lambda i: divide(self.value(i, "cfo"), self.value(i, "pat"), "CFO", "PAT",
                             require_positive_denominator=True)))
        section.add("FCF / net profit", "x", self.series(
            lambda i: divide(self.value(i, "fcf"), self.value(i, "pat"), "FCF", "PAT",
                             require_positive_denominator=True)))
        section.add("FCF margin", "%", self.series(
            lambda i: divide(self.value(i, "fcf"), self.value(i, "revenue"), "FCF", "revenue", 100.0)))
        section.add("FCF / EBITDA (cash conversion)", "%", self.series(
            lambda i: divide(self.value(i, "fcf"), self.value(i, "ebitda"), "FCF", "EBITDA", 100.0,
                             require_positive_denominator=True)))

        def accrual_ratio(i: int) -> Cell:
            """Sloan accrual ratio: (PAT - CFO) / average total assets."""
            pat, cfo = self.value(i, "pat"), self.value(i, "cfo")
            if pat is None:
                return None, "PAT not available"
            if cfo is None:
                return None, "CFO not available"
            avg, reason = self.average_balance(i, "total_assets")
            if avg is None:
                return None, reason
            return divide(pat - cfo, avg, "PAT less CFO", "average total assets", 100.0,
                          require_positive_denominator=True)

        section.add("Accrual ratio (Sloan)", "%", self.series(accrual_ratio))
        section.add("Capex / sales", "%", self.series(
            lambda i: divide(self.value(i, "capex"), self.value(i, "revenue"), "capex", "revenue", 100.0)))
        section.add("Capex / depreciation", "x", self.series(
            lambda i: divide(self.value(i, "capex"), self.value(i, "depreciation"),
                             "capex", "depreciation", require_positive_denominator=True)))

        # Cumulative cash conversion over the whole period -- more informative
        # than any single year, and the form the literature uses.
        cfo_total = sum(p.get("cfo") for p in self.periods if p.get("cfo") is not None)
        pat_total = sum(p.get("pat") for p in self.periods if p.get("pat") is not None)
        have_all = all(p.has("cfo") and p.has("pat") for p in self.periods)
        if have_all:
            section.add_scalar("Cumulative CFO / cumulative PAT", "x",
                               divide(cfo_total, pat_total, "cumulative CFO", "cumulative PAT",
                                      require_positive_denominator=True))
        else:
            section.add_scalar("Cumulative CFO / cumulative PAT", "x",
                               (None, "CFO and PAT are not available for every period"))
        return section

    # -- per share --------------------------------------------------------- #

    def _diluted_shares(self, i: int) -> Cell:
        """Diluted share count for period i, falling back to the basic count."""
        diluted = self.value(i, "diluted_shares")
        if diluted is not None:
            return diluted, None
        basic = self.value(i, "shares_outstanding")
        if basic is not None:
            return basic, None
        return None, "no share count supplied"

    def section_per_share(self) -> Section:
        """Per-share figures on the diluted count."""
        section = Section(
            "PER SHARE",
            self.labels,
            note=(
                "Computed on the diluted count where supplied (basic count otherwise). A "
                "count lifted from the cover of a filing understates the claim on the "
                "business wherever options, RSUs, warrants, CCPS or convertibles exist."
            ),
        )
        section.add("Diluted shares", "count", self.series(self._diluted_shares))
        section.add("EPS (diluted)", "ps", self.series(
            lambda i: divide(self.value(i, "pat"), self._diluted_shares(i)[0],
                             "PAT", "diluted share count", require_positive_denominator=True)))
        section.add("Book value per share", "ps", self.series(
            lambda i: divide(self.value(i, "equity"), self._diluted_shares(i)[0],
                             "shareholders' equity", "diluted share count",
                             require_positive_denominator=True)))
        section.add("Tangible book value per share", "ps", self.series(
            lambda i: divide(self.periods[i].tangible_equity(), self._diluted_shares(i)[0],
                             "tangible equity", "diluted share count",
                             require_positive_denominator=True)))
        section.add("Revenue per share", "ps", self.series(
            lambda i: divide(self.value(i, "revenue"), self._diluted_shares(i)[0],
                             "revenue", "diluted share count", require_positive_denominator=True)))
        section.add("CFO per share", "ps", self.series(
            lambda i: divide(self.value(i, "cfo"), self._diluted_shares(i)[0],
                             "CFO", "diluted share count", require_positive_denominator=True)))
        section.add("FCF per share", "ps", self.series(
            lambda i: divide(self.value(i, "fcf"), self._diluted_shares(i)[0],
                             "FCF", "diluted share count", require_positive_denominator=True)))

        def dps(i: int) -> Cell:
            """Dividend per share, taken directly or from total dividends paid."""
            direct = self.value(i, "dividend_per_share")
            if direct is not None:
                return direct, None
            return divide(self.value(i, "dividends_paid"), self._diluted_shares(i)[0],
                          "dividends paid", "diluted share count",
                          require_positive_denominator=True)

        section.add("Dividend per share", "ps", self.series(dps))
        section.add("Dividend payout ratio", "%", self.series(
            lambda i: divide(self.value(i, "dividends_paid"), self.value(i, "pat"),
                             "dividends paid", "PAT", 100.0, require_positive_denominator=True)))
        return section

    # -- enterprise value bridge ------------------------------------------- #

    def build_ev_bridge(self) -> None:
        """Build the EV bridge component by component.

        Most "cheap on EV/EBITDA" findings are arithmetic errors in EV, so every
        component is shown, every component that was not supplied is named, and
        the surplus-cash assumption is stated rather than buried.
        """
        latest = self.periods[-1]
        market = self.market
        bridge: Dict[str, Any] = {
            "as_of": market.get("as_of"),
            "period": latest.label,
            "components": [],
            "not_supplied": [],
            "assumptions": [],
            "enterprise_value": None,
            "market_cap": None,
            "reason": None,
        }

        # 1. Fully diluted market capitalisation.
        market_cap = market.get("market_cap")
        cap_source = "supplied directly"
        if market_cap is None:
            price = market.get("price")
            shares = market.get("diluted_shares")
            if shares is None:
                shares = market.get("shares_outstanding")
            if shares is None:
                shares = self._diluted_shares(self.n - 1)[0]
            if price is not None and shares is not None:
                market_cap = price * shares
                cap_source = "price %s x diluted share count %s" % (
                    format_number(price, 2), format_number(shares, 2))
        if market_cap is not None and market_cap <= 0:
            bridge["reason"] = (
                "market capitalisation computed as %s - a non-positive market cap means the "
                "price or the share count is wrong; every multiple is suppressed rather than "
                "printed" % format_number(market_cap)
            )
            market_cap = None
        if market_cap is None:
            bridge.setdefault("reason", None)
            bridge["reason"] = bridge["reason"] or (
                "no market capitalisation: supply market.market_cap, or market.price with a "
                "diluted share count"
            )
            self.ev_bridge = bridge
            return
        bridge["market_cap"] = market_cap
        bridge["components"].append({
            "name": "Fully diluted market capitalisation",
            "sign": "+", "value": market_cap, "source": cap_source, "supplied": True,
        })

        def component(name: str, sign: str, market_key: Optional[str],
                      period_field: Optional[str], note: str = "") -> Number:
            """Add one bridge component, defaulting to zero but recording the gap."""
            value = market.get(market_key) if market_key else None
            source = "market input"
            if value is None and period_field:
                value = latest.get(period_field)
                source = "%s balance sheet" % latest.label
            if value is None:
                bridge["not_supplied"].append(name)
                value = 0.0
                source = "not supplied - treated as zero"
            bridge["components"].append({
                "name": name, "sign": sign, "value": value,
                "source": source + ((" (%s)" % note) if note else ""),
                "supplied": source != "not supplied - treated as zero",
            })
            return value

        gross_debt = latest.get("gross_debt")
        if gross_debt is None:
            bridge["not_supplied"].append("Gross debt")
            gross_debt = 0.0
            bridge["components"].append({
                "name": "Gross debt (short + long term + current maturities)",
                "sign": "+", "value": 0.0,
                "source": "not supplied - treated as zero", "supplied": False,
            })
        else:
            bridge["components"].append({
                "name": "Gross debt (short + long term + current maturities)",
                "sign": "+", "value": gross_debt,
                "source": "%s balance sheet" % latest.label, "supplied": True,
            })

        leases = component("Capitalised lease liabilities", "+", None, "lease_liabilities",
                           "IFRS 16 / Ind AS 116 / ASC 842")
        preference = component("Preference shares / CCPS", "+", "preference_capital", "preference_capital")
        minorities = component("Non-controlling (minority) interest", "+", "minority_interest",
                               "minority_interest_bs", "at book unless a market value was supplied")
        pension = component("Net pension / gratuity deficit", "+", "pension_deficit", "pension_deficit",
                            "net of plan assets, tax-effected")
        other_debt = component("Other debt-like items", "+", "other_debt_like", "other_debt_like",
                               "reverse factoring, ARO, earn-outs, related-party loans")
        contingent = component("Contingent consideration / earn-outs", "+", "contingent_consideration", None)

        # Surplus cash, with the operating-cash carve-out stated explicitly.
        surplus = market.get("surplus_cash")
        if surplus is None:
            liquid = latest.liquid_assets()
            if liquid is None:
                bridge["not_supplied"].append("Surplus cash and equivalents")
                surplus = 0.0
                cash_source = "not supplied - treated as zero (EV is overstated)"
            else:
                pct = float(self.options.operating_cash_pct)
                revenue = latest.get("revenue")
                carve_out = 0.0
                if pct > 0 and revenue is not None:
                    carve_out = revenue * pct / 100.0
                    bridge["assumptions"].append(
                        "operating cash requirement carved out at %.1f%% of revenue = %s; "
                        "only the remainder is treated as distributable surplus"
                        % (pct, format_number(carve_out))
                    )
                elif pct > 0:
                    bridge["assumptions"].append(
                        "--operating-cash-pct was set but revenue is unavailable, so no "
                        "operating-cash carve-out could be applied"
                    )
                else:
                    bridge["assumptions"].append(
                        "ALL cash and current investments treated as surplus (no operating-cash "
                        "carve-out). Use --operating-cash-pct to carve out operating cash "
                        "(typically 2-5% of revenue), and exclude trapped, escrow, margin and "
                        "customer-float balances, which are not distributable."
                    )
                surplus = max(liquid - carve_out, 0.0)
                cash_source = "cash + current investments less any carve-out"
            bridge["components"].append({
                "name": "Less: surplus cash and equivalents", "sign": "-",
                "value": surplus, "source": cash_source,
                "supplied": "not supplied" not in cash_source,
            })
        else:
            bridge["components"].append({
                "name": "Less: surplus cash and equivalents", "sign": "-",
                "value": surplus, "source": "market input", "supplied": True,
            })

        associates = market.get("value_of_associates")
        assoc_source = "market input (fair value)"
        if associates is None:
            associates = latest.get("investments_in_associates")
            assoc_source = "%s balance sheet (BOOK value - fair value is preferable)" % latest.label
        if associates is None:
            bridge["not_supplied"].append("Value of associates / JVs / listed stakes")
            associates = 0.0
            assoc_source = "not supplied - treated as zero"
        bridge["components"].append({
            "name": "Less: value of non-consolidated stakes (associates, JVs)", "sign": "-",
            "value": associates, "source": assoc_source,
            "supplied": assoc_source != "not supplied - treated as zero",
        })

        enterprise_value = (
            market_cap + gross_debt + leases + preference + minorities + pension
            + other_debt + contingent - surplus - associates
        )
        bridge["enterprise_value"] = enterprise_value
        bridge["assumptions"].append(
            "Pairing rule: minority interest is inside EV, so the earnings figure paired with "
            "an EV multiple must be pre-minority (EBITDA and EBIT are). P/E and P/B pair with "
            "the post-minority PAT and owners' equity."
        )
        if "Value of associates / JVs / listed stakes" not in bridge["not_supplied"] and associates:
            bridge["assumptions"].append(
                "Associates are deducted from EV, so any share of associate profit must also "
                "be stripped out of the earnings figure - doing one without the other is the "
                "commonest silent error in holdco and conglomerate analysis."
            )
        self.ev_bridge = bridge

    # -- valuation --------------------------------------------------------- #

    def section_valuation(self) -> Section:
        """Equity and enterprise multiples on the latest period."""
        latest_index = self.n - 1
        latest = self.periods[latest_index]
        as_of = self.market.get("as_of")
        title = "VALUATION (on %s%s)" % (latest.label, (", price as of %s" % as_of) if as_of else "")
        section = Section(
            title, [latest.label],
            note=(
                "Multiples are computed on the latest supplied period only. A multiple "
                "without an as-of date and a stated earnings basis is not usable."
            ),
        )
        market_cap = self.ev_bridge.get("market_cap")
        enterprise_value = self.ev_bridge.get("enterprise_value")

        if market_cap is None:
            section.suppress(self.ev_bridge.get("reason") or "no market data supplied")
            return section

        ev_suppressed_reason = None
        if self.sector_key in EV_MEANINGLESS_SECTOR_KEYS:
            ev_suppressed_reason = (
                "enterprise value has no meaning for a bank, NBFC or insurer - debt is raw "
                "material, not financing, so every EV multiple is suppressed. Use P/B, "
                "P/ABV, ROE vs cost of equity, P/EV."
            )

        def ev_cell(numerator_name: str, denominator: Number, den_label: str) -> Cell:
            """EV multiple, suppressed entirely where EV is meaningless."""
            if ev_suppressed_reason:
                return None, ev_suppressed_reason
            return divide(enterprise_value, denominator, numerator_name, den_label,
                          require_positive_denominator=True)

        section.add("Market capitalisation", "abs", [(market_cap, None)])
        section.add("Enterprise value", "abs", [
            (None, ev_suppressed_reason) if ev_suppressed_reason else (enterprise_value, None)])
        section.add("P/E (trailing)", "x", [
            divide(market_cap, latest.get("pat"), "market cap", "PAT",
                   require_positive_denominator=True)])
        section.add("P/B", "x", [
            divide(market_cap, latest.get("equity"), "market cap", "shareholders' equity",
                   require_positive_denominator=True)])
        section.add("P/B (tangible)", "x", [
            divide(market_cap, latest.tangible_equity(), "market cap", "tangible equity",
                   require_positive_denominator=True)])
        section.add("P/S", "x", [
            divide(market_cap, latest.get("revenue"), "market cap", "revenue",
                   require_positive_denominator=True)])
        section.add("EV/EBITDA", "x", [ev_cell("enterprise value", latest.get("ebitda"), "EBITDA")])
        section.add("EV/EBIT", "x", [ev_cell("enterprise value", latest.get("ebit"), "EBIT")])
        section.add("EV/Sales", "x", [ev_cell("enterprise value", latest.get("revenue"), "revenue")])
        section.add("EV/CFO", "x", [ev_cell("enterprise value", latest.get("cfo"), "CFO")])
        section.add("Earnings yield (PAT / market cap)", "%", [
            divide(latest.get("pat"), market_cap, "PAT", "market cap", 100.0,
                   require_positive_denominator=True)])
        section.add("FCF yield (FCF / market cap)", "%", [
            divide(latest.get("fcf"), market_cap, "FCF", "market cap", 100.0,
                   require_positive_denominator=True)])
        if ev_suppressed_reason:
            section.add("FCF yield (FCF / EV)", "%", [(None, ev_suppressed_reason)])
            section.add("EBIT / EV (earnings yield, enterprise)", "%", [(None, ev_suppressed_reason)])
        else:
            section.add("FCF yield (FCF / EV)", "%", [
                divide(latest.get("fcf"), enterprise_value, "FCF", "enterprise value", 100.0,
                       require_positive_denominator=True)])
            section.add("EBIT / EV (earnings yield, enterprise)", "%", [
                divide(latest.get("ebit"), enterprise_value, "EBIT", "enterprise value", 100.0,
                       require_positive_denominator=True)])
        section.add("Dividend yield", "%", [
            divide(latest.get("dividends_paid"), market_cap, "dividends paid", "market cap", 100.0,
                   require_positive_denominator=True)])
        return section

    # ------------------------------------------------------------------ #
    # Quality warnings
    # ------------------------------------------------------------------ #

    def detect_quality_warnings(self) -> None:
        """Run every automatic quality test and record the ones that trigger.

        Each warning names the test and carries the values that triggered it, so
        a reader can check the arithmetic rather than take the flag on trust.
        """
        self._warn_cash_vs_profit()
        self._warn_receivables_vs_sales()
        self._warn_inventory_vs_sales()
        self._warn_dso_trend()
        self._warn_interest_cover()
        self._warn_capex_vs_depreciation()
        self._warn_negative_fcf_with_profit()
        self._warn_tax_rate_anomalies()
        self._warn_accrual_ratio()
        self._warn_leverage()

    def _add_warning(self, test: str, severity: str, detail: str, values: Dict[str, Any]) -> None:
        """Register a triggered warning."""
        self.warnings.append(Warning_(test, severity, detail, values))

    def _warn_cash_vs_profit(self) -> None:
        """OCF below net profit across multiple years."""
        pairs = [(p.label, p.get("cfo"), p.get("pat")) for p in self.periods
                 if p.get("cfo") is not None and p.get("pat") is not None]
        if len(pairs) < 2:
            return
        shortfalls = [(label, cfo, pat) for label, cfo, pat in pairs if pat > 0 and cfo < pat]
        cfo_total = sum(cfo for _, cfo, _ in pairs)
        pat_total = sum(pat for _, _, pat in pairs)
        ratio = cfo_total / pat_total if pat_total > 0 else None
        if len(shortfalls) >= 2:
            severity = "high" if (ratio is not None and ratio < 0.8) else "medium"
            self._add_warning(
                "OCF below net profit in multiple years",
                severity,
                "Operating cash flow fell short of reported net profit in %d of %d periods%s. "
                "Profit that does not become cash is either sitting in working capital or is "
                "not real; bridge net income to CFO line by line before accepting the earnings."
                % (len(shortfalls), len(pairs),
                   "" if ratio is None else "; cumulative CFO/PAT = %.2fx" % ratio),
                {
                    "periods": [
                        {"period": label, "cfo": cfo, "pat": pat, "shortfall": pat - cfo}
                        for label, cfo, pat in shortfalls
                    ],
                    "cumulative_cfo": cfo_total,
                    "cumulative_pat": pat_total,
                    "cumulative_cfo_over_pat": ratio,
                },
            )
        elif ratio is not None and ratio < 0.8:
            self._add_warning(
                "Cumulative OCF well below cumulative net profit",
                "medium",
                "Cumulative CFO/PAT over the supplied history is %.2fx (below 0.80x), even "
                "though few individual years show a shortfall." % ratio,
                {"cumulative_cfo": cfo_total, "cumulative_pat": pat_total,
                 "cumulative_cfo_over_pat": ratio},
            )

    def _growth_gap_warning(self, field: str, label: str, threshold_pp: float,
                            detail_tail: str) -> None:
        """Shared test: a balance-sheet item compounding faster than sales."""
        if self.n < 2:
            return
        span = (self.n - 1) * self.period_years
        item_cagr, item_reason = cagr(self.value(0, field), self.value(self.n - 1, field), span, label)
        rev_cagr, rev_reason = cagr(self.value(0, "revenue"), self.value(self.n - 1, "revenue"),
                                    span, "revenue")
        if item_cagr is None or rev_cagr is None:
            return
        gap = item_cagr - rev_cagr
        if gap <= threshold_pp:
            return
        severity = "high" if gap > 2 * threshold_pp else "medium"
        self._add_warning(
            "%s growing faster than sales" % label.capitalize(),
            severity,
            "%s compounded at %.1f%% against revenue at %.1f%% over %s-%s, a gap of %.1f "
            "percentage points. %s"
            % (label.capitalize(), item_cagr, rev_cagr, self.labels[0], self.labels[-1],
               gap, detail_tail),
            {
                "metric_cagr_pct": item_cagr,
                "revenue_cagr_pct": rev_cagr,
                "gap_pp": gap,
                "opening": {"period": self.labels[0], label: self.value(0, field),
                            "revenue": self.value(0, "revenue")},
                "closing": {"period": self.labels[-1], label: self.value(self.n - 1, field),
                            "revenue": self.value(self.n - 1, "revenue")},
            },
        )

    def _warn_receivables_vs_sales(self) -> None:
        """Receivables growing materially faster than sales."""
        self._growth_gap_warning(
            "receivables", "receivables", self.options.growth_gap_pp,
            "That is the classic signature of pulled-forward revenue, channel stuffing or "
            "weakening customers. Read the Schedule III receivables ageing schedule and check "
            "the over-6-month bucket before accepting the headline DSO.",
        )

    def _warn_inventory_vs_sales(self) -> None:
        """Inventory growing faster than sales."""
        self._growth_gap_warning(
            "inventory", "inventory", self.options.growth_gap_pp,
            "Inventory built ahead of demand precedes write-downs. Check whether it is raw "
            "material (input-cost positioning) or finished goods (unsold product).",
        )

    def _warn_dso_trend(self) -> None:
        """A DSO that rises year after year.

        The earliest period's DSO is computed on a closing balance rather than
        an average, so it is excluded from the trend: comparing a closing-basis
        figure with average-basis figures manufactures a trend that is not there.
        """
        dso_values: List[Tuple[str, float]] = []
        first_comparable = 1 if self.n > 1 else 0
        for i in range(first_comparable, self.n):
            avg, _ = self.average_balance(i, "receivables")
            revenue = self.value(i, "revenue")
            if avg is None or revenue is None or revenue <= 0:
                continue
            dso_values.append((self.labels[i], avg / revenue * DAYS_IN_YEAR))
        if len(dso_values) < 3:
            return
        rising_every_year = all(
            dso_values[i][1] > dso_values[i - 1][1] for i in range(1, len(dso_values)))
        first, last = dso_values[0][1], dso_values[-1][1]
        pct_change = (last / first - 1.0) * 100.0 if first > 0 else None
        material = pct_change is not None and pct_change > 15.0
        if not (rising_every_year or material):
            return
        severity = "high" if (rising_every_year and material) else "medium"
        self._add_warning(
            "Rising DSO trend",
            severity,
            "Receivable days moved from %.0f (%s) to %.0f (%s)%s%s. Rising DSO is the "
            "earliest sign of channel stuffing, weakening customers or aggressive revenue "
            "recognition; distinguish it from a deliberate credit-terms change and check "
            "whether any apparent improvement came from factoring."
            % (first, dso_values[0][0], last, dso_values[-1][0],
               "" if pct_change is None else ", %+.1f%%" % pct_change,
               ", rising in every single year" if rising_every_year else ""),
            {"dso_by_period": [{"period": p, "dso_days": v} for p, v in dso_values],
             "change_pct": pct_change, "rose_every_year": rising_every_year},
        )

    def _warn_interest_cover(self) -> None:
        """Interest coverage below the threshold."""
        threshold = float(self.options.interest_cover_threshold)
        breaches = []
        for i in range(self.n):
            ebit, interest = self.value(i, "ebit"), self.value(i, "interest")
            if ebit is None or interest is None or interest <= 0:
                continue
            cover = ebit / interest
            if cover < threshold:
                breaches.append({"period": self.labels[i], "ebit": ebit,
                                 "interest": interest, "coverage_x": cover})
        if not breaches:
            return
        worst = min(b["coverage_x"] for b in breaches)
        latest_breach = breaches[-1]["period"] == self.labels[-1]
        severity = "high" if (worst < 1.5 or latest_breach) else "medium"
        self._add_warning(
            "Interest coverage below %.1fx" % threshold,
            severity,
            "EBIT/interest fell below %.1fx in %d period(s); the worst was %.2fx. Below "
            "roughly 2x a modest earnings dip breaches covenants, and the covenant test is "
            "usually run on a definition of EBITDA set in the credit agreement rather than "
            "the reported one - read it." % (threshold, len(breaches), worst),
            {"breaches": breaches, "threshold_x": threshold},
        )

    def _warn_capex_vs_depreciation(self) -> None:
        """Capex persistently below depreciation."""
        ratios = []
        for i in range(self.n):
            capex, dep = self.value(i, "capex"), self.value(i, "depreciation")
            if capex is None or dep is None or dep <= 0:
                continue
            ratios.append({"period": self.labels[i], "capex": capex,
                           "depreciation": dep, "capex_over_dep_x": capex / dep})
        if len(ratios) < 2:
            return
        below = [r for r in ratios if r["capex_over_dep_x"] < 0.9]
        if len(below) < 2 or len(below) < len(ratios) / 2.0:
            return
        self._add_warning(
            "Capex persistently below depreciation",
            "medium",
            "Capex was below 90%% of depreciation in %d of %d periods. Either the asset base "
            "is being run down (which flatters current margins and cash flow at the cost of "
            "future capacity) or depreciation is overstated relative to true economic life - "
            "and only one of those is good news. Check the useful-life assumptions and the "
            "age of the gross block." % (len(below), len(ratios)),
            {"periods": ratios, "below_threshold": [r["period"] for r in below]},
        )

    def _warn_negative_fcf_with_profit(self) -> None:
        """Negative free cash flow while reporting a profit."""
        hits = []
        for period in self.periods:
            fcf, pat = period.get("fcf"), period.get("pat")
            if fcf is None or pat is None:
                continue
            if fcf < 0 and pat > 0:
                hits.append({"period": period.label, "fcf": fcf, "pat": pat,
                             "cfo": period.get("cfo"), "capex": period.get("capex")})
        if not hits:
            return
        severity = "high" if len(hits) >= 2 else "medium"
        self._add_warning(
            "Negative FCF while reporting profit",
            severity,
            "Free cash flow was negative in %d period(s) despite positive reported profit: "
            "%s. Separate growth capex from maintenance capex before concluding this is a "
            "problem - a genuine build-out is negative by design - but a company that never "
            "generates cash is funding its dividend from borrowings."
            % (len(hits), ", ".join(h["period"] for h in hits)),
            {"periods": hits},
        )

    def _warn_tax_rate_anomalies(self) -> None:
        """Effective tax rates that are implausible, volatile, or off statutory."""
        rates = []
        for i in range(self.n):
            tax, pbt = self.value(i, "tax"), self.value(i, "pbt")
            if tax is None or pbt is None or pbt <= 0:
                continue
            rates.append({"period": self.labels[i], "tax": tax, "pbt": pbt,
                          "effective_rate_pct": tax / pbt * 100.0})
        if not rates:
            return
        values = [r["effective_rate_pct"] for r in rates]
        issues = []
        if min(values) < 10.0:
            issues.append("an effective rate below 10%")
        if max(values) > 50.0:
            issues.append("an effective rate above 50%")
        if len(values) >= 2 and (max(values) - min(values)) > 10.0:
            issues.append("a swing of %.1f percentage points across the period"
                          % (max(values) - min(values)))
        statutory = self.options.statutory_tax
        if statutory is not None:
            latest = values[-1]
            if abs(latest - float(statutory)) > 10.0:
                issues.append("the latest rate of %.1f%% is more than 10pp away from the "
                              "stated statutory rate of %.1f%%" % (latest, float(statutory)))
        # Book vs cash tax divergence is the other half of this test.
        cash_gap = None
        for i in range(self.n):
            book, cash, pbt = self.value(i, "tax"), self.value(i, "cash_taxes_paid"), self.value(i, "pbt")
            if book is None or cash is None or pbt is None or pbt <= 0:
                continue
            gap = (book - cash) / pbt * 100.0
            if abs(gap) > 8.0:
                cash_gap = {"period": self.labels[i], "book_tax": book, "cash_tax": cash,
                            "gap_pp_of_pbt": gap}
                issues.append("book tax and cash tax paid diverge by %.1fpp of PBT in %s"
                              % (gap, self.labels[i]))
                break
        if not issues:
            return
        self._add_warning(
            "Effective tax rate anomaly",
            "medium",
            "Tax tests flagged: %s. A tax rate that moves without a regime change usually "
            "signals one-off credits, MAT credit utilisation, an expiring tax holiday about "
            "to reverse, or aggressive positions under dispute - each of which makes the "
            "current post-tax earnings a poor guide to the next year's."
            % "; ".join(issues),
            {"effective_rates": rates, "statutory_rate_pct": statutory,
             "book_vs_cash_tax": cash_gap},
        )

    def _warn_accrual_ratio(self) -> None:
        """Sloan accrual ratio above the red-flag threshold."""
        hits = []
        for i in range(self.n):
            pat, cfo = self.value(i, "pat"), self.value(i, "cfo")
            avg, _ = self.average_balance(i, "total_assets")
            if pat is None or cfo is None or avg is None or avg <= 0:
                continue
            ratio = (pat - cfo) / avg * 100.0
            if ratio > 10.0:
                hits.append({"period": self.labels[i], "accrual_ratio_pct": ratio,
                             "pat": pat, "cfo": cfo, "avg_total_assets": avg})
        if not hits:
            return
        self._add_warning(
            "High accrual ratio (Sloan)",
            "high" if len(hits) >= 2 else "medium",
            "(Net income - CFO) / average total assets exceeded 10%% in %d period(s). High-"
            "accrual firms systematically underperform; this is one of the most robust "
            "anomalies in the accounting literature." % len(hits),
            {"periods": hits, "threshold_pct": 10.0},
        )

    def _warn_leverage(self) -> None:
        """Net debt/EBITDA above a broadly stretched level in the latest period."""
        latest = self.periods[-1]
        net_debt, ebitda = latest.net_debt(), latest.get("ebitda")
        if net_debt is None or ebitda is None or ebitda <= 0:
            return
        ratio = net_debt / ebitda
        if ratio <= 3.5:
            return
        self._add_warning(
            "Net debt / EBITDA above 3.5x",
            "high" if ratio > 4.5 else "medium",
            "Net debt/EBITDA is %.2fx in %s. That band is stretched outside utilities, REITs "
            "and contracted infrastructure - check the maturity ladder, the covenant "
            "definition of EBITDA, and whether leverage is being measured at a commodity or "
            "cycle peak." % (ratio, latest.label),
            {"period": latest.label, "net_debt": net_debt, "ebitda": ebitda,
             "net_debt_over_ebitda_x": ratio},
        )

    # ------------------------------------------------------------------ #
    # Sector gate
    # ------------------------------------------------------------------ #

    def sector_gate(self) -> Optional[str]:
        """Return the sector warning text when the sector is a financial one."""
        key = self.sector_key
        if key not in FINANCIAL_SECTOR_KEYS:
            return None
        if key in {"bank", "banks", "banking", "lender", "financial", "financials", "finance"}:
            body = SECTOR_GATE_MESSAGE["bank"]
        elif key in {"nbfc", "nbfcs", "hfc", "hfcs"}:
            body = SECTOR_GATE_MESSAGE["nbfc"]
        elif key in {"insurance", "insurer", "insurers", "life-insurance", "general-insurance"}:
            body = SECTOR_GATE_MESSAGE["insurance"]
        else:
            body = SECTOR_GATE_MESSAGE["reit"]
        return body

    # ------------------------------------------------------------------ #
    # Collecting what could not be computed
    # ------------------------------------------------------------------ #

    def not_computed(self) -> List[Dict[str, Any]]:
        """Aggregate every metric that could not be computed, with the reason.

        "No prior period" is excluded: the first period of any series has no
        year-on-year figure by construction, which is arithmetic rather than a
        gap in the data.
        """
        structural = {"no prior period"}
        collected: Dict[Tuple[str, str, str], List[str]] = {}
        for section in self.sections:
            if section.suppressed:
                collected.setdefault((section.title, "(whole section)", section.suppressed), [])
                continue
            for row in section.rows:
                for idx, (value, reason) in enumerate(row["cells"]):
                    if value is not None or reason in structural:
                        continue
                    label = (section.period_labels[idx]
                             if idx < len(section.period_labels) else "?")
                    key = (section.title, row["name"], reason or "reason not recorded")
                    collected.setdefault(key, []).append(label)
            for scalar in section.scalars:
                value, reason = scalar["cell"]
                if value is None:
                    key = (section.title, scalar["name"], reason or "reason not recorded")
                    collected.setdefault(key, [])
        return [
            {"section": section, "metric": metric, "reason": reason, "periods": periods}
            for (section, metric, reason), periods in collected.items()
        ]


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #

LABEL_WIDTH = 46
COL_WIDTH = 13


def wrap(text: str, width: int = 96, indent: str = "  ") -> List[str]:
    """Wrap text to a width, returning indented lines (no textwrap import games)."""
    words, lines, current = text.split(), [], ""
    for word in words:
        candidate = word if not current else current + " " + word
        if len(candidate) + len(indent) > width:
            lines.append(indent + current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(indent + current)
    return lines


def render_section(section: Section) -> List[str]:
    """Render one section as fixed-width text."""
    out: List[str] = []
    out.append("")
    out.append(section.title)
    out.append("-" * max(len(section.title), 60))
    if section.suppressed:
        out.extend(wrap("NOT APPLICABLE: " + section.suppressed))
        return out
    if section.note:
        out.extend(wrap("Note: " + section.note))
        out.append("")
    if section.rows:
        header = " " * LABEL_WIDTH + "".join(
            label.rjust(COL_WIDTH) for label in section.period_labels)
        out.append(header)
        for row in section.rows:
            name = row["name"]
            if len(name) > LABEL_WIDTH - 1:
                name = name[: LABEL_WIDTH - 2] + "."
            line = name.ljust(LABEL_WIDTH)
            line += "".join(format_cell(cell, row["unit"]).rjust(COL_WIDTH)
                            for cell in row["cells"])
            out.append(line)
    for scalar in section.scalars:
        value, _reason = scalar["cell"]
        if scalar["unit"] == "text":
            rendered = value if value is not None else "n/a"
        else:
            rendered = format_cell(scalar["cell"], scalar["unit"])
        name = scalar["name"]
        dots = "." * max(3, LABEL_WIDTH + 8 - len(name))
        out.append("%s %s %s" % (name, dots, rendered))
    return out


def render_text(analysis: Analysis) -> str:
    """Render the whole analysis as a readable report."""
    out: List[str] = []
    rule = "=" * 96
    out.append(rule)
    out.append("RATIO ANALYSIS - %s" % analysis.company)
    out.append("Basis: %s | Currency/units: %s | Periods: %s"
               % (analysis.basis, analysis.currency, ", ".join(analysis.labels)))
    if analysis.sector_raw:
        out.append("Sector: %s" % analysis.sector_raw)
    if analysis.source:
        out.append("Source: %s" % analysis.source)
    out.append(rule)

    gate = analysis.sector_gate()
    if gate:
        out.append("")
        out.append("!" * 96)
        out.append("SECTOR GATE - THE STANDARD RATIO SET DOES NOT APPLY HERE")
        out.extend(wrap(gate))
        if analysis.sector_key in EV_MEANINGLESS_SECTOR_KEYS:
            tail = ("Ratios below are still computed where the arithmetic is defined, but "
                    "ROIC, invested capital, net debt/EBITDA and interest coverage must not "
                    "be quoted for this sector, and every EV multiple has been suppressed. "
                    "Use the sector playbook's metric set instead.")
        else:
            tail = ("Ratios below are still computed where the arithmetic is defined, but "
                    "ROIC, invested capital and the earnings-based multiples will mislead "
                    "for this sector. Use the sector playbook's metric set instead.")
        out.extend(wrap(tail))
        out.append("!" * 96)

    # Input integrity.
    derivations = [d for period in analysis.periods for d in period.derivations]
    out.append("")
    out.append("INPUT INTEGRITY")
    out.append("-" * 60)
    if derivations:
        out.append("  Derived line items (not taken from the filing directly):")
        for item in derivations:
            out.append("    - " + item)
    else:
        out.append("  No line items had to be derived; everything came from the input.")
    if analysis.cautions:
        out.append("  Cautions:")
        for caution in analysis.cautions:
            out.extend(wrap("- " + caution, indent="    "))
    out.append("  Normalised tax rate for NOPAT: %s (%s)" % (
        "n/a" if analysis.normalised_tax_rate is None
        else "%.1f%%" % (analysis.normalised_tax_rate * 100.0),
        analysis.tax_rate_basis))

    for section in analysis.sections:
        if section.title.startswith("VALUATION"):
            out.extend(render_ev_bridge(analysis))
        out.extend(render_section(section))

    # Quality warnings.
    out.append("")
    out.append("QUALITY WARNINGS")
    out.append("-" * 60)
    if not analysis.warnings:
        out.append("  No automatic quality test triggered on the data supplied.")
        out.extend(wrap(
            "That is not a clean bill of health: these tests only see the line items given "
            "to them. Related-party transactions, contingent liabilities, auditor changes, "
            "pledging and segment disclosure are not testable from this input.",
            indent="  "))
    else:
        for index, warning in enumerate(analysis.warnings, start=1):
            out.append("  %d. [%s] %s" % (index, warning.severity.upper(), warning.test))
            out.extend(wrap(warning.detail, indent="     "))
            out.extend(wrap("triggering values: " + json.dumps(warning.values, default=str),
                            indent="     "))
            out.append("")

    # Not computed.
    missing = analysis.not_computed()
    out.append("")
    out.append("NOT COMPUTED (and why)")
    out.append("-" * 60)
    if not missing:
        out.append("  Every metric in every section was computable from the input supplied.")
    else:
        for item in sorted(missing, key=lambda m: (m["section"], m["metric"])):
            scope = ("all periods" if len(item["periods"]) == len(analysis.labels)
                     else ", ".join(item["periods"]) if item["periods"] else "whole period")
            out.extend(wrap("- %s / %s [%s]: %s"
                            % (item["section"].split("  ")[0], item["metric"], scope, item["reason"]),
                            indent="  "))

    # Method notes.
    out.append("")
    out.append("METHOD NOTES")
    out.append("-" * 60)
    for note in analysis.method_notes:
        out.extend(wrap("- " + note, indent="  "))
    out.extend(wrap(
        "- Every band implied by these tests is indicative only. Sector, market, rate cycle "
        "and accounting regime move all of them; peer comparison and the company's own "
        "multi-year record override any absolute threshold used here.", indent="  "))
    out.extend(wrap(
        "- This script computes; it does not judge. A number is not a conclusion until it is "
        "set against the peer set and the company's own history.", indent="  "))
    out.append("")
    return "\n".join(out)


def render_ev_bridge(analysis: Analysis) -> List[str]:
    """Render the enterprise-value bridge as an explicit component table."""
    bridge = analysis.ev_bridge
    out: List[str] = []
    out.append("")
    out.append("ENTERPRISE VALUE BRIDGE (%s)" % bridge.get("period", ""))
    out.append("-" * 60)
    out.extend(wrap(
        "Most 'cheap on EV/EBITDA' findings are arithmetic errors in EV, so the bridge is "
        "built once, shown component by component, and reused in every enterprise multiple."))
    out.append("")
    if bridge.get("enterprise_value") is None:
        out.extend(wrap("NOT BUILT: " + (bridge.get("reason") or "insufficient market data")))
        return out
    bridge_width = max(
        [len(c["name"]) for c in bridge["components"]] + [len("ENTERPRISE VALUE")]) + 2
    for component in bridge["components"]:
        out.append("  %s %s %s   [%s]" % (
            component["sign"],
            component["name"].ljust(bridge_width),
            format_number(component["value"]).rjust(16),
            component["source"],
        ))
    out.append("  = %s %s" % (
        "ENTERPRISE VALUE".ljust(bridge_width),
        format_number(bridge["enterprise_value"]).rjust(16)))
    if bridge["not_supplied"]:
        out.append("")
        out.extend(wrap(
            "Components NOT supplied and therefore treated as zero: %s. Each one that exists "
            "in reality makes the EV above too low, and every EV multiple correspondingly too "
            "cheap." % ", ".join(bridge["not_supplied"])))
    for assumption in bridge["assumptions"]:
        out.extend(wrap("Assumption: " + assumption))
    return out


def render_json(analysis: Analysis) -> str:
    """Serialise the whole analysis, including reasons for every missing value."""
    payload: Dict[str, Any] = {
        "company": analysis.company,
        "basis": analysis.basis,
        "currency": analysis.currency,
        "sector": analysis.sector_raw or None,
        "source": analysis.source,
        "periods": analysis.labels,
        "sector_gate_warning": analysis.sector_gate(),
        "input_integrity": {
            "derivations": [d for p in analysis.periods for d in p.derivations],
            "cautions": analysis.cautions,
            "normalised_tax_rate_pct": (None if analysis.normalised_tax_rate is None
                                        else analysis.normalised_tax_rate * 100.0),
            "normalised_tax_rate_basis": analysis.tax_rate_basis,
        },
        "sections": [],
        "enterprise_value_bridge": analysis.ev_bridge,
        "quality_warnings": [w.to_dict() for w in analysis.warnings],
        "not_computed": analysis.not_computed(),
        "method_notes": analysis.method_notes,
    }
    for section in analysis.sections:
        block: Dict[str, Any] = {
            "title": section.title,
            "periods": section.period_labels,
            "note": section.note,
            "suppressed": section.suppressed,
            "metrics": [],
            "scalars": [],
        }
        for row in section.rows:
            block["metrics"].append({
                "name": row["name"],
                "unit": row["unit"],
                "values": [
                    {"period": (section.period_labels[i] if i < len(section.period_labels) else None),
                     "value": cell[0], "unavailable_because": cell[1]}
                    for i, cell in enumerate(row["cells"])
                ],
            })
        for scalar in section.scalars:
            block["scalars"].append({
                "name": scalar["name"],
                "unit": scalar["unit"],
                "value": scalar["cell"][0],
                "unavailable_because": scalar["cell"][1],
            })
        payload["sections"].append(block)
    return json.dumps(payload, indent=2, default=str)


# --------------------------------------------------------------------------- #
# Worked example plumbing
# --------------------------------------------------------------------------- #

EXAMPLE_BEGIN = "--- EXAMPLE INPUT (begin) ---"
EXAMPLE_END = "--- EXAMPLE INPUT (end) ---"


def example_input_text() -> str:
    """Return the worked example JSON embedded in this module's docstring.

    Extracting it from the docstring rather than duplicating it guarantees the
    documented example and the emitted example can never drift apart.
    """
    doc = __doc__ or ""
    try:
        start = doc.index(EXAMPLE_BEGIN) + len(EXAMPLE_BEGIN)
        end = doc.index(EXAMPLE_END)
    except ValueError:  # pragma: no cover - only if the docstring is edited badly
        raise RuntimeError("worked example markers are missing from the module docstring")
    text = doc[start:end].strip()
    json.loads(text)  # fail loudly if the documented example stopped being valid JSON
    return text


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def build_parser() -> argparse.ArgumentParser:
    """Construct the command-line interface."""
    parser = argparse.ArgumentParser(
        prog="ratios.py",
        description=(
            "Compute the full derived ratio set (growth, margins, returns, DuPont, ROIIC, "
            "leverage, liquidity, working capital, cash-flow quality, per-share, EV bridge "
            "and valuation multiples) from a JSON file of raw financial line items, and "
            "flag quality warnings automatically."
        ),
        epilog=(
            "For banks, NBFCs, insurers and REITs most of these ratios are meaningless: pass "
            "--sector to get the gate warning, and use the sector playbook's metric set "
            "instead. Run --example to print a complete worked input file."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", nargs="?", help="path to the JSON input file ('-' for stdin)")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="emit machine-readable JSON instead of the text table")
    parser.add_argument("--example", action="store_true",
                        help="print the complete worked example input file and exit")
    parser.add_argument("--sector", default=None,
                        help="sector key (e.g. banks, nbfc, insurance, reit, it-saas, auto); "
                             "financial sectors trigger the sector gate warning and suppress "
                             "EV multiples")
    parser.add_argument("--tax-rate", type=float, default=None, metavar="PCT",
                        help="override the normalised tax rate used for NOPAT, in percent")
    parser.add_argument("--use-cash-tax", action="store_true",
                        help="derive the normalised tax rate from cash taxes paid rather than "
                             "the book tax charge")
    parser.add_argument("--statutory-tax", type=float, default=None, metavar="PCT",
                        help="statutory tax rate in percent, used only by the effective-tax-rate "
                             "anomaly test (India post-115BAA is about 25.2%%; US federal 21%%)")
    parser.add_argument("--operating-cash-pct", type=float, default=0.0, metavar="PCT",
                        help="percent of revenue treated as operating cash and therefore NOT "
                             "deducted as surplus cash in the EV bridge (typically 2-5); "
                             "default 0, i.e. all cash treated as surplus")
    parser.add_argument("--roiic-years", type=int, default=3, metavar="N",
                        help="window in years for return on incremental invested capital "
                             "(default 3; single-year ROIIC is noise)")
    parser.add_argument("--period-years", type=float, default=1.0, metavar="Y",
                        help="years between consecutive periods, for CAGRs (default 1.0)")
    parser.add_argument("--interest-cover-threshold", type=float, default=2.5, metavar="X",
                        help="interest coverage below this triggers a quality warning "
                             "(default 2.5x)")
    parser.add_argument("--growth-gap-pp", type=float, default=4.0, metavar="PP",
                        help="percentage-point gap between receivables/inventory CAGR and "
                             "revenue CAGR that triggers a warning (default 4.0)")
    return parser


def load_document(path: str) -> Dict[str, Any]:
    """Read and parse the input JSON file (or stdin when path is '-')."""
    if path == "-":
        text = sys.stdin.read()
    else:
        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read()
    try:
        doc = json.loads(text)
    except json.JSONDecodeError as error:
        raise ValueError("input is not valid JSON: %s" % error)
    if not isinstance(doc, dict):
        raise ValueError("input JSON must be an object at the top level")
    return doc


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Entry point. Returns a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.example:
        sys.stdout.write(example_input_text() + "\n")
        return 0
    if not args.input:
        parser.error("an input JSON file is required (or use --example)")

    try:
        doc = load_document(args.input)
        analysis = Analysis(doc, args)
        analysis.build_all()
    except (ValueError, OSError) as error:
        sys.stderr.write("ratios.py: %s\n" % error)
        return 2

    if args.as_json:
        sys.stdout.write(render_json(analysis) + "\n")
    else:
        sys.stdout.write(render_text(analysis) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
