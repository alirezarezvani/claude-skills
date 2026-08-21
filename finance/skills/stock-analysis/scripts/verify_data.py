#!/usr/bin/env python3
"""verify_data.py -- data-intake verification gate for the stock-analysis skill.

Purpose
-------
Blinded adversarial review of this skill's real reports found the dominant
weakness is not analysis quality but DATA INTEGRITY: figures that could not be
traced to a source, a peer's NPA stated wrong, and reports that silently omitted
a quarter which was already public on the analysis date. Those are intake
defects, not reasoning defects -- and an intake defect contaminates every ratio,
every peer comparison and the final verdict, invisibly and confidently.

This script runs the data the agent has *gathered* through a gate BEFORE the
analysis touches it, so the defect is caught at intake instead of surfacing in
the verdict. It reads a JSON description of the gathered datapoints, applies a
fixed set of provenance / consistency / recency rules, and prints findings with
a PASS / PASS-WITH-WARNINGS / FAIL headline. It exits non-zero on any
error-severity finding so it can gate a pipeline.

It never fetches anything and never invents anything. It only checks the
internal consistency, completeness and freshness of what it was given. A clean
PASS here does not mean the numbers are *right* -- it means they are traceable,
mutually consistent and current enough to analyse. Those are the preconditions
the review found were being skipped.

Standard library only. Python 3.8+. No network, no third-party packages.

--------------------------------------------------------------------------------
INPUT SCHEMA
--------------------------------------------------------------------------------
A JSON object. Top-level fields:

  company                 str   -- issuer name (free text).
  ticker                  str   -- exchange:symbol, e.g. "NSE:MERIDBANK".
  as_of                   str   -- ISO date the data was gathered, "2026-07-23".
                                   Staleness is measured from THIS, never from
                                   the wall clock -- the gate must be reproducible.
  reporting_basis         str   -- "consolidated" or "standalone"; the basis the
                                   analysis will be run on.
  currency                str   -- file-level currency, e.g. "INR", "USD".
  units                   str   -- file-level scale, e.g. "crore", "million".
  fiscal_year_end         str   -- optional. Month the fiscal year ends, e.g.
                                   "March" or 3. Defaults to March (Indian
                                   convention). Governs how "FY26"/"Q1 FY27"
                                   labels are converted to period-end dates.
  latest_reported_period  obj   -- {"period": "Q1 FY27", "published": "2026-07-11"}
                                   The newest period the company has ACTUALLY
                                   reported (from an exchange/filing check), which
                                   may be newer than anything gathered below.
  datapoints              list  -- the gathered figures (see below).
  not_available           list  -- optional. Metric names the agent could not
                                   source and has explicitly left blank. Declaring
                                   these is GOOD discipline and is reported as
                                   coverage context, never as a defect.

Each entry in "datapoints" is an object:

  metric   str   -- REQUIRED. Canonical metric name, e.g. "revenue",
                    "net_profit", "gross_npa_pct". Grouping is by this name.
  value    num   -- the figure. May be null or "not available" to mark the metric
                    as explicitly unsourced (counts toward coverage, not defects).
  period   str   -- REQUIRED for a real figure. "FY26", "Q1 FY27", "CY2025",
                    "TTM to Sep-2025", "year ended Dec-2025".
  basis    str   -- "consolidated" or "standalone".
  unit     str   -- e.g. "INR crore", "USD million", "%", "x", "days".
  source   str   -- REQUIRED for a real figure. Where it came from, with enough
                    detail to re-find it: "FY26 annual report, p.142".
  source_tier int -- optional 1-4. 1 primary filing (annual report/10-K/exchange
                    results/DRHP), 2 company-published secondary (presentation,
                    concall, release), 3 regulator/third-party primary (rating
                    rationale, MCA/ROC, SEBI, shareholding pattern), 4 aggregator
                    (screener/tickertape/yahoo/moneycontrol...). If omitted it is
                    INFERRED from the `source` text. Tier 4 is a navigation aid,
                    never a source of record: a HEADLINE metric (revenue, PAT,
                    EBITDA, debt, equity, operating cash flow) that is Tier-4-only
                    is an ERROR. Current price/market cap is the one sanctioned
                    exception and is exempt.
  entity   str   -- optional. Whose figure this is, when it is not the subject
                    company -- a peer's, for a benchmark. Defaults to `company`.
                    Lets the peer's-NPA-stated-wrong case be period-aligned and
                    cross-checked in its own right.
  note     str   -- optional. A free-text acknowledgement that legitimises an
                    otherwise-flagged deviation (e.g. a deliberately standalone
                    figure, or a figure in a different unit). Its PRESENCE
                    downgrades basis/unit mismatches from silent to disclosed.
  alt      list  -- optional. Cross-source corroborating reads of the SAME figure:
                    [{"value": 59480, "source": "screener.in 2026-07-21"}].
                    The gate compares each against `value`.

The template printed by --template is annotated with these rules. Comment lines
(whole lines whose first non-space characters are `//`) are stripped by the
loader, so a filled-in template loads directly; keep comments on their own line.

--------------------------------------------------------------------------------
CHECKS
--------------------------------------------------------------------------------
  1  PROVENANCE     source/period missing = error; unit/basis missing = warn.
  2  CROSS-SOURCE   `alt` vs `value` divergence: >2% warn, >10% error.
  3  BASIS MIXING   consolidated and standalone both present, unlabelled = error.
  4  UNIT/CURRENCY  unit/currency differs from the file declaration = warn;
                    a clean 10x/100x gap between comparable figures = error.
  5  PERIOD ALIGN   comparing FY vs CY vs TTM, or misaligned year-ends = warn.
  6  RECENCY        a newer reported period exists but is not incorporated, or
                    as_of is >~4 months past the newest period-end = warn.
  7  COVERAGE       count of metrics explicitly marked not-available = info.
  8  SOURCE TIER    a HEADLINE metric sourced only from a Tier-4 aggregator =
                    error; a non-headline aggregator-only figure = warn; a
                    headline figure whose source cannot be confirmed as a filing
                    = warn; plus a % primary-sourced coverage line = info.

--------------------------------------------------------------------------------
USAGE
--------------------------------------------------------------------------------
    python verify_data.py intake.json            # readable report
    python verify_data.py intake.json --json      # machine-readable findings
    python verify_data.py --template              # annotated blank intake
    python verify_data.py --example               # run the built-in example
    python verify_data.py --example --json

Exit code: 0 if no error-severity finding (PASS or PASS-WITH-WARNINGS),
1 if any error-severity finding (FAIL), 2 on unusable input (bad path / bad JSON).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any, Dict, List, Optional, Sequence, Tuple

SCRIPT = "verify_data.py"

SEVERITY_ERROR = "error"
SEVERITY_WARN = "warn"
SEVERITY_INFO = "info"
# Sort order for grouping the report: errors first, then warnings, then info.
_SEVERITY_RANK = {SEVERITY_ERROR: 0, SEVERITY_WARN: 1, SEVERITY_INFO: 2}

# Divergence thresholds for cross-source disagreement, in percent. A gap of a
# few percent is usually a definitional difference (other income in/out of
# EBITDA, leases, average vs closing balances). A gap above ~10% almost always
# means a different basis, period or unit -- i.e. the two "sources" are not
# measuring the same thing, and trusting either blindly is how a wrong figure
# (the peer-NPA case) reaches the report. So >2% is worth a human glance (warn)
# and >10% must block until reconciled (error).
DIVERGENCE_WARN_PCT = 2.0
DIVERGENCE_ERROR_PCT = 10.0

# How close a ratio between two "comparable" figures must be to a power of ten
# before it is treated as a unit/scale error rather than a real difference.
# 1 crore = 10 million, so the crore-vs-million slip lands almost exactly on 10x.
MAGNITUDE_TOLERANCE = 0.03  # +/-3% around 10x, 100x, 1000x.
MAGNITUDE_FACTORS = (10.0, 100.0, 1000.0)

# Recency thresholds, in days, measured against as_of (never the wall clock).
# ~20 days separates "same reporting period, rounding" from "a genuinely later
# period exists". ~4 months (123 days) past a period-end means at least one
# quarterly result has almost certainly been published since and was not checked.
RECENCY_NEWER_PERIOD_DAYS = 20
RECENCY_STALE_DAYS = 123

_MONTHS = {
    "jan": 1, "january": 1, "feb": 2, "february": 2, "mar": 3, "march": 3,
    "apr": 4, "april": 4, "may": 5, "jun": 6, "june": 6, "jul": 7, "july": 7,
    "aug": 8, "august": 8, "sep": 9, "sept": 9, "september": 9, "oct": 10,
    "october": 10, "nov": 11, "november": 11, "dec": 12, "december": 12,
}

# Currency spellings -> canonical code. `$` is deliberately ambiguous across
# USD/SGD/HKD/AUD/CAD; it is mapped to USD only so a `$` figure inside an INR
# file still trips the currency-mismatch check rather than passing silently.
_CURRENCY_ALIASES = {
    "inr": "INR", "rs": "INR", "rs.": "INR", "₹": "INR", "rupee": "INR",
    "rupees": "INR", "usd": "USD", "us$": "USD", "$": "USD", "dollar": "USD",
    "eur": "EUR", "€": "EUR", "euro": "EUR", "gbp": "GBP", "£": "GBP",
    "jpy": "JPY", "¥": "JPY", "yen": "JPY", "cny": "CNY", "rmb": "CNY",
    "sgd": "SGD", "hkd": "HKD", "aud": "AUD", "cad": "CAD",
}

# Scale spellings -> canonical scale name.
_SCALE_ALIASES = {
    "cr": "crore", "cr.": "crore", "crore": "crore", "crores": "crore",
    "lakh": "lakh", "lakhs": "lakh", "lac": "lakh", "lacs": "lakh",
    "mn": "million", "mm": "million", "mio": "million", "million": "million",
    "millions": "million", "bn": "billion", "billion": "billion",
    "billions": "billion", "k": "thousand", "thousand": "thousand",
    "thousands": "thousand", "'000": "thousand", "000s": "thousand",
    "trillion": "trillion", "tn": "trillion",
}

# Unit tokens that describe a ratio/percentage/count rather than a monetary
# amount. These are never compared against the file's currency/units, and never
# enter the 10x magnitude test (a 0.9% vs 9% pair must not read as a unit error).
_NON_MONETARY_TOKENS = {
    "%", "percent", "pct", "bps", "bp", "x", "times", "ratio", "days", "day",
    "years", "months", "count", "number", "no", "units", "per", "share",
    "shares", "eps", "dps", "bv",
}

# Strings that, as a datapoint value, mean "the agent looked and it is not
# available" -- deliberate, disclosed gaps. These are coverage, not defects.
_UNAVAILABLE_RE = re.compile(
    r"^\s*(n/?a|not\s+available|not\s+disclosed|not\s+sourced|unavailable|"
    r"nd|--|-)\s*$",
    re.IGNORECASE,
)

# ---- Source-tier vocabulary (Check 8) ------------------------------------- #
# The skill is document-first: figures must trace to the company's own filings,
# and aggregators (screener/tickertape/yahoo...) are navigation aids, never a
# source of record. These patterns infer a tier (1-4) from a free-text `source`
# when the datapoint does not state `source_tier` explicitly. Priority is
# highest-tier-wins: a source naming both a filing and an aggregator ("FY26 AR,
# cross-checked screener") is Tier 1, because it means the figure was traced to
# the filing.
_TIER1_SOURCE_RE = re.compile(
    r"annual report|integrated report|10-?k|10-?q|20-?f|8-?k|6-?k|"
    r"quarterly results|results filing|results intimation|audited|"
    r"financial statements?|balance sheet|cash ?flow statement|"
    r"statement of profit|profit (?:&|and) loss|prospectus|drhp|rhp|"
    r"\bs-?1\b|\bf-?1\b|red herring|offer document|exchange filing|"
    r"bse filing|nse filing|regulation ?30|\bcaro\b|financial report",
    re.IGNORECASE,
)
_TIER2_SOURCE_RE = re.compile(
    r"investor presentation|investor deck|earnings call|con-?call|"
    r"earnings transcript|\btranscript\b|earnings release|press release|"
    r"fact ?sheet|investor update|analyst meet|management commentary",
    re.IGNORECASE,
)
_TIER3_SOURCE_RE = re.compile(
    r"rating rationale|credit rating|crisil|icra|care ratings|india ratings|"
    r"acuit|brickwork|\bmca\b|\broc\b|registrar of companies|\bsebi\b|"
    r"shareholding pattern|bulk deal|block deal|\brbi\b|irdai|edgar|"
    r"pillar ?3|form ?4\b|13-?[dfg]\b|def ?14a",
    re.IGNORECASE,
)
_TIER4_SOURCE_RE = re.compile(
    r"screener|tikr|tijori|trendlyne|tickertape|moneycontrol|"
    r"yahoo\s*finance|google\s*finance|marketsmojo|investing\.com|stockanalysis|"
    r"wsj\.com|morningstar|simplywall|value\s*research|valueresearch|"
    r"finology|equitymaster|5paisa|\bgroww\b|angelone|zerodha|wikipedia|"
    r"\baggregator\b|capitaline|smart-?investing|marketscreener",
    re.IGNORECASE,
)

# Metrics whose reliability drives the whole verdict: an aggregator-only read of
# any of these is an error, not a warning.
_HEADLINE_METRIC_RE = re.compile(
    r"revenue|turnover|net\s*sales|\bsales\b|net\s*profit|\bpat\b|"
    r"profit after tax|net income|ebitda|operating profit|"
    r"total\s*debt|borrowing|net\s*debt|\bequity\b|net\s*worth|"
    r"shareholders?\s*funds|operating cash|cash from operations|\bcfo\b|\bocf\b",
    re.IGNORECASE,
)
# Market data legitimately sourced from an exchange/finance site -- the one
# sanctioned exception to the document-first rule. Exempt from the tier check.
_MARKET_DATA_METRIC_RE = re.compile(
    r"price|market\s*cap|mcap|market capitalis|52-?week|enterprise value|\bev\b",
    re.IGNORECASE,
)


# --------------------------------------------------------------------------- #
# Finding model
# --------------------------------------------------------------------------- #
@dataclass
class Finding:
    """A single verification result.

    rule_id  -- stable, greppable identifier for the rule that fired.
    severity -- error | warn | info.
    message  -- human-readable sentence that NAMES the offending datapoint(s).
    metric / period / entity -- structured anchors, echoed in --json so a
                                pipeline can route the finding without parsing
                                the message.
    """

    rule_id: str
    severity: str
    message: str
    metric: Optional[str] = None
    period: Optional[str] = None
    entity: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Return the finding as a plain dict for the --json output."""
        out: Dict[str, Any] = {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "message": self.message,
        }
        if self.metric is not None:
            out["metric"] = self.metric
        if self.period is not None:
            out["period"] = self.period
        if self.entity is not None:
            out["entity"] = self.entity
        return out


# --------------------------------------------------------------------------- #
# Loading and small parsers
# --------------------------------------------------------------------------- #
def strip_line_comments(text: str) -> str:
    """Remove whole-line `//` comments so an annotated template loads as JSON.

    Only lines whose first non-whitespace characters are `//` are dropped. This
    is deliberately conservative: it never touches `//` inside a string value
    (a source URL such as ``https://...`` is mid-line, never at column zero after
    trimming), and it never removes trailing commas, so it cannot silently
    corrupt an otherwise-valid file.
    """
    kept = []
    for line in text.splitlines():
        if line.lstrip().startswith("//"):
            continue
        kept.append(line)
    return "\n".join(kept)


def load_intake(path: str) -> Dict[str, Any]:
    """Read and parse the intake file, raising ValueError with a clear message.

    Every failure mode (missing file, unreadable file, invalid JSON, wrong
    top-level type) is turned into a ValueError carrying a human sentence, so the
    caller can print one clean line instead of a traceback.
    """
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


def to_number(value: Any) -> Optional[float]:
    """Coerce a datapoint value to float, or return None if it is not numeric.

    Accepts ints/floats and numeric strings with thousands separators or a
    leading currency symbol ("1,23,456", "₹ 59,500"). Booleans and free text
    return None so they are simply skipped by numeric checks rather than
    crashing them.
    """
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = re.sub(r"[,\s₹$£€¥]", "", value)
        cleaned = re.sub(r"(?i)(cr|crore|mn|million|bn|billion|lakh|k)$", "", cleaned)
        try:
            return float(cleaned)
        except ValueError:
            return None
    return None


def parse_iso_date(value: Any) -> Optional[date]:
    """Parse an ISO ``YYYY-MM-DD`` string to a date, or None if unparseable."""
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value.strip()[:10])
    except ValueError:
        return None


def normalise_basis(value: Any) -> Optional[str]:
    """Map a basis string to 'consolidated' / 'standalone' / other, or None."""
    if not isinstance(value, str) or not value.strip():
        return None
    low = value.strip().lower()
    if low.startswith("cons"):
        return "consolidated"
    if low.startswith("stand") or low.startswith("sa") or low == "parent":
        return "standalone"
    return low


def resolve_fy_end_month(doc: Dict[str, Any]) -> int:
    """Return the file's fiscal-year-end month (1-12); default March (Indian).

    A fiscal-year label like "FY26" carries no month on its face, so converting
    it to a period-end date requires knowing the year-end. The skill is
    India-leaning (crore/INR), where the year ends in March, so that is the
    default; it can be overridden with a top-level ``fiscal_year_end`` field.
    """
    raw = doc.get("fiscal_year_end")
    if isinstance(raw, (int, float)) and 1 <= int(raw) <= 12:
        return int(raw)
    if isinstance(raw, str):
        key = raw.strip().lower()[:3]
        if key in _MONTHS:
            return _MONTHS[key]
    return 3


# --------------------------------------------------------------------------- #
# Unit parsing
# --------------------------------------------------------------------------- #
@dataclass
class ParsedUnit:
    """Decomposition of a unit string into currency, scale and monetary-ness."""

    currency: Optional[str]
    scale: Optional[str]
    monetary: bool
    raw: str


def parse_unit(unit: Any) -> Optional[ParsedUnit]:
    """Split a unit string into a currency code and a scale name.

    Returns None when there is nothing to parse. ``monetary`` is False for
    percentages, multiples, day-counts and the like -- those describe ratios, not
    amounts, and must be exempt from the currency/units comparison and the 10x
    magnitude test.
    """
    if not isinstance(unit, str) or not unit.strip():
        return None
    raw = unit.strip()
    tokens = re.split(r"[\s/,]+", raw.lower())
    currency: Optional[str] = None
    scale: Optional[str] = None
    non_monetary = False
    for tok in tokens:
        if not tok:
            continue
        if tok in _CURRENCY_ALIASES and currency is None:
            currency = _CURRENCY_ALIASES[tok]
        elif tok in _SCALE_ALIASES and scale is None:
            scale = _SCALE_ALIASES[tok]
        elif tok in _NON_MONETARY_TOKENS or "%" in tok:
            non_monetary = True
    monetary = (currency is not None or scale is not None) and not non_monetary
    return ParsedUnit(currency=currency, scale=scale, monetary=monetary, raw=raw)


def normalise_currency(value: Any) -> Optional[str]:
    """Map a bare currency declaration to a canonical code."""
    if not isinstance(value, str) or not value.strip():
        return None
    key = value.strip().lower()
    return _CURRENCY_ALIASES.get(key, value.strip().upper())


def normalise_scale(value: Any) -> Optional[str]:
    """Map a bare scale declaration to a canonical name."""
    if not isinstance(value, str) or not value.strip():
        return None
    key = value.strip().lower()
    return _SCALE_ALIASES.get(key, key)


# --------------------------------------------------------------------------- #
# Period parsing
# --------------------------------------------------------------------------- #
@dataclass
class ParsedPeriod:
    """A period label resolved to a kind, a fiscal-year-end month and an end date.

    kind          -- one of: fiscal_year, quarter, calendar_year, ttm,
                     bare_year, unknown.
    fy_end_month  -- the resolved year-end month (explicit if the label carried
                     one, else the file default).
    end_date      -- approximate period-end, used only for chronological ordering
                     and staleness math; None when it cannot be inferred.
    ambiguous     -- True for a bare "2025" that could be FY or CY.
    """

    kind: str
    fy_end_month: Optional[int]
    end_date: Optional[date]
    ambiguous: bool = False


def _last_day_of_month(year: int, month: int) -> date:
    """Return the last calendar day of the given month."""
    if month == 12:
        return date(year, 12, 31)
    return date(year, month + 1, 1) - timedelta(days=1)


def _shift_months(year: int, month: int, delta: int) -> Tuple[int, int]:
    """Return (year, month) shifted by ``delta`` months (delta may be negative)."""
    total = year * 12 + (month - 1) + delta
    return total // 12, total % 12 + 1


def _fy_year(token: str) -> int:
    """Turn a fiscal-year token ('27', '2027') into a 4-digit year."""
    digits = int(token)
    if len(token) <= 2:
        return 2000 + digits
    return digits


def _find_month_and_year(text: str) -> Tuple[Optional[int], Optional[int]]:
    """Extract a (month, year) pair from free text, if both are present."""
    month = None
    for name, num in _MONTHS.items():
        if re.search(r"\b" + name + r"\b", text, re.IGNORECASE):
            month = num
            break
    ym = re.search(r"((?:19|20)\d{2})", text)
    year = int(ym.group(1)) if ym else None
    return month, year


def classify_period(label: Any, default_fy_end_month: int) -> ParsedPeriod:
    """Classify a period label and compute an approximate period-end date.

    Handles the common Indian and global forms: "FY26", "Q1 FY27", "CY2025",
    "TTM to Sep-2025", "year ended Dec-2025", and a bare "2025". Anything it
    cannot place is returned as kind 'unknown' with no end date -- degraded, never
    a crash.
    """
    if not isinstance(label, str) or not label.strip():
        return ParsedPeriod("unknown", None, None)
    up = label.upper()

    # Trailing-twelve-months: a rolling window, not a discrete fiscal period.
    if "TTM" in up or "LTM" in up:
        month, year = _find_month_and_year(label)
        end = _last_day_of_month(year, month) if (month and year) else None
        return ParsedPeriod("ttm", month, end)

    # Quarter, fiscal ("Q1 FY27") or calendar ("Q1 2027" / "Q1 CY2027").
    qm = re.search(r"Q\s*([1-4])", up)
    if qm:
        quarter = int(qm.group(1))
        fy = re.search(r"FY\s*([0-9]{2,4})", up)
        if fy:
            year = _fy_year(fy.group(1))
            fem = default_fy_end_month
            end = _quarter_end(year, fem, quarter)
            return ParsedPeriod("quarter", fem, end)
        cy = re.search(r"(?:CY\s*)?((?:19|20)\d{2})", up)
        if cy:
            year = int(cy.group(1))
            end = _quarter_end(year, 12, quarter)
            return ParsedPeriod("quarter", 12, end)
        return ParsedPeriod("quarter", None, None)

    # Fiscal year: "FY26", "FY2026".
    fy = re.search(r"FY\s*([0-9]{2,4})", up)
    if fy:
        year = _fy_year(fy.group(1))
        # An explicit month token overrides the default year-end.
        month, _ = _find_month_and_year(label)
        fem = month if month else default_fy_end_month
        return ParsedPeriod("fiscal_year", fem, _last_day_of_month(year, fem))

    # Calendar year: "CY2025".
    cy = re.search(r"CY\s*([0-9]{2,4})", up)
    if cy:
        year = _fy_year(cy.group(1))
        return ParsedPeriod("calendar_year", 12, _last_day_of_month(year, 12))

    # Explicit month-year: "Mar-2026", "year ended Dec-2025", "December 2025".
    month, year = _find_month_and_year(label)
    if month and year:
        return ParsedPeriod("fiscal_year", month, _last_day_of_month(year, month))

    # Bare year: "2025" -- genuinely ambiguous between FY and CY.
    bare = re.fullmatch(r"\s*((?:19|20)\d{2})\s*", label)
    if bare:
        year = int(bare.group(1))
        return ParsedPeriod("bare_year", 12, _last_day_of_month(year, 12), ambiguous=True)

    return ParsedPeriod("unknown", None, None)


def _quarter_end(fy_year: int, fy_end_month: int, quarter: int) -> date:
    """Return the period-end date of fiscal quarter ``quarter``.

    Q4 ends on the fiscal-year-end; each earlier quarter ends three months
    before the next. With a March year-end, FY27 Q1 ends 30-Jun-2026, exactly the
    conversion the recency check needs to notice a gathered FY figure is a
    quarter behind the latest reported quarter.
    """
    months_before_year_end = 3 * (4 - quarter)
    year, month = _shift_months(fy_year, fy_end_month, -months_before_year_end)
    return _last_day_of_month(year, month)


# --------------------------------------------------------------------------- #
# Datapoint helpers
# --------------------------------------------------------------------------- #
def is_unavailable(dp: Dict[str, Any]) -> bool:
    """True if the datapoint is an explicit 'not available' marker, not a figure."""
    value = dp.get("value", None)
    if value is None and "value" in dp:
        return True
    if isinstance(value, str) and _UNAVAILABLE_RE.match(value):
        return True
    return False


def dp_entity(dp: Dict[str, Any], company: Optional[str]) -> str:
    """Return whose figure this is -- the named entity, else the subject company."""
    ent = dp.get("entity")
    if isinstance(ent, str) and ent.strip():
        return ent.strip()
    return company or "(company)"


def dp_label(dp: Dict[str, Any], company: Optional[str]) -> str:
    """Build a stable, human descriptor of a datapoint for finding messages."""
    metric = dp.get("metric") or "(unnamed metric)"
    period = dp.get("period") or "no period"
    entity = dp_entity(dp, company)
    if company and entity != company:
        return "%s / %s (%s)" % (entity, metric, period)
    return "%s (%s)" % (metric, period)


def infer_source_tier(source: Any) -> Optional[int]:
    """Infer a source tier (1-4) from a free-text source string, or None.

    Highest tier wins: a source that names a primary filing is Tier 1 even if it
    also mentions an aggregator, because that means the figure was traced to the
    filing and merely cross-checked. A source that names only an aggregator is
    Tier 4. Anything the vocabulary does not recognise returns None ('unknown'),
    which the caller treats as unconfirmed rather than assuming the best.
    """
    if not isinstance(source, str) or not source.strip():
        return None
    if _TIER1_SOURCE_RE.search(source):
        return 1
    if _TIER2_SOURCE_RE.search(source):
        return 2
    if _TIER3_SOURCE_RE.search(source):
        return 3
    if _TIER4_SOURCE_RE.search(source):
        return 4
    return None


def resolve_source_tier(dp: Dict[str, Any]) -> Tuple[Optional[int], bool]:
    """Return (tier, inferred). An explicit `source_tier` wins over inference.

    ``inferred`` is True when the tier came from reading the source text rather
    than from an explicit field, so the caller can phrase findings honestly.
    """
    raw = dp.get("source_tier")
    if isinstance(raw, bool):
        raw = None
    if isinstance(raw, (int, float)) and int(raw) in (1, 2, 3, 4):
        return int(raw), False
    if isinstance(raw, str):
        m = re.search(r"[1-4]", raw)
        if m:
            return int(m.group(0)), False
    return infer_source_tier(dp.get("source")), True


def _normalise_metric(metric: str) -> str:
    """Turn snake_case / kebab-case metric names into space-separated words.

    Canonical metric names in the intake are snake_case ("net_profit",
    "operating_cash_flow", "market_cap"), so the word-oriented patterns must see
    "net profit", not "net_profit" -- otherwise every headline metric slips the
    check and the market-cap exemption never fires.
    """
    return re.sub(r"[_\-]+", " ", metric)


def is_headline_metric(metric: Any) -> bool:
    """True for the load-bearing metrics whose source tier is enforced hardest."""
    if not isinstance(metric, str):
        return False
    norm = _normalise_metric(metric)
    if _MARKET_DATA_METRIC_RE.search(norm):
        return False
    return bool(_HEADLINE_METRIC_RE.search(norm))


def is_market_data_metric(metric: Any) -> bool:
    """True for price/market-cap style metrics -- exempt from the tier check."""
    if not isinstance(metric, str):
        return False
    return bool(_MARKET_DATA_METRIC_RE.search(_normalise_metric(metric)))


def _iter_real_datapoints(
    doc: Dict[str, Any]
) -> List[Tuple[int, Dict[str, Any]]]:
    """Yield (index, datapoint) for well-formed datapoints that carry a value.

    'Not available' markers and malformed entries are excluded here; malformed
    entries are reported separately by :func:`check_datapoint_shape`.
    """
    out = []
    for idx, dp in enumerate(doc.get("datapoints", []) or []):
        if not isinstance(dp, dict):
            continue
        if is_unavailable(dp):
            continue
        out.append((idx, dp))
    return out


# --------------------------------------------------------------------------- #
# Structural / metadata checks
# --------------------------------------------------------------------------- #
def check_datapoint_shape(doc: Dict[str, Any]) -> List[Finding]:
    """Flag datapoints that are not objects or lack a metric name (error).

    A datapoint with no metric cannot be grouped, cited or reasoned about, so it
    is a hard error rather than a skipped row -- silently dropping it would hide
    data the analyst believes is present.
    """
    findings: List[Finding] = []
    datapoints = doc.get("datapoints", [])
    if not isinstance(datapoints, list) or not datapoints:
        findings.append(
            Finding(
                "NO_DATAPOINTS",
                SEVERITY_ERROR,
                "No datapoints to verify: the 'datapoints' array is missing or empty.",
            )
        )
        return findings
    for idx, dp in enumerate(datapoints):
        if not isinstance(dp, dict):
            findings.append(
                Finding(
                    "MALFORMED_DATAPOINT",
                    SEVERITY_ERROR,
                    "Datapoint #%d is not an object (got %s)."
                    % (idx, type(dp).__name__),
                )
            )
            continue
        metric = dp.get("metric")
        if not isinstance(metric, str) or not metric.strip():
            findings.append(
                Finding(
                    "MALFORMED_DATAPOINT",
                    SEVERITY_ERROR,
                    "Datapoint #%d has no 'metric' name; it cannot be cited or grouped."
                    % idx,
                )
            )
    return findings


def check_metadata(doc: Dict[str, Any]) -> List[Finding]:
    """Flag missing file-level declarations that weaken downstream checks (warn).

    None of these are fatal on their own, but each disables or narrows a later
    check -- a missing as_of makes staleness unmeasurable, a missing currency
    makes unit mixing invisible -- so the analyst is told which guarantees the
    gate could not provide.
    """
    findings: List[Finding] = []
    if not (isinstance(doc.get("company"), str) and doc["company"].strip()):
        findings.append(
            Finding("META_MISSING_COMPANY", SEVERITY_WARN,
                    "File-level 'company' is missing; datapoints cannot be attributed.")
        )
    if parse_iso_date(doc.get("as_of")) is None:
        findings.append(
            Finding("META_MISSING_AS_OF", SEVERITY_WARN,
                    "File-level 'as_of' is missing or not an ISO date; "
                    "staleness/recency checks are skipped.")
        )
    if normalise_basis(doc.get("reporting_basis")) is None:
        findings.append(
            Finding("META_MISSING_BASIS", SEVERITY_WARN,
                    "File-level 'reporting_basis' is missing; "
                    "cannot tell which basis the analysis is meant to run on.")
        )
    if normalise_currency(doc.get("currency")) is None:
        findings.append(
            Finding("META_MISSING_CURRENCY", SEVERITY_WARN,
                    "File-level 'currency' is missing; currency mixing cannot be detected.")
        )
    if normalise_scale(doc.get("units")) is None:
        findings.append(
            Finding("META_MISSING_UNITS", SEVERITY_WARN,
                    "File-level 'units' is missing; scale mixing (the 10x error) "
                    "cannot be detected.")
        )
    return findings


# --------------------------------------------------------------------------- #
# Check 1 -- provenance
# --------------------------------------------------------------------------- #
def check_provenance(doc: Dict[str, Any]) -> List[Finding]:
    """Every real figure must be traceable: source, period, unit, basis.

    Source and period are the two fields without which a number cannot be
    re-found or placed in time, so their absence is an error. Unit and basis can
    often be inferred from the file-level declaration, so their absence is a
    warning -- but an unstated basis is exactly how consolidated and standalone
    get mixed, so it is never silent.
    """
    company = doc.get("company")
    findings: List[Finding] = []
    for _, dp in _iter_real_datapoints(doc):
        label = dp_label(dp, company)
        metric = dp.get("metric")
        entity = dp_entity(dp, company)
        period = dp.get("period")
        if not (isinstance(dp.get("source"), str) and dp["source"].strip()):
            findings.append(
                Finding("PROVENANCE_MISSING_SOURCE", SEVERITY_ERROR,
                        "%s has no source; the figure cannot be traced or re-verified."
                        % label, metric, period, entity)
            )
        if not (isinstance(period, str) and period.strip()):
            findings.append(
                Finding("PROVENANCE_MISSING_PERIOD", SEVERITY_ERROR,
                        "%s has no period; a figure without a period is not yet a fact."
                        % label, metric, period, entity)
            )
        if not (isinstance(dp.get("unit"), str) and dp["unit"].strip()):
            findings.append(
                Finding("PROVENANCE_MISSING_UNIT", SEVERITY_WARN,
                        "%s has no unit; scale/currency must be inferred from the "
                        "file declaration." % label, metric, period, entity)
            )
        if normalise_basis(dp.get("basis")) is None:
            findings.append(
                Finding("PROVENANCE_MISSING_BASIS", SEVERITY_WARN,
                        "%s has no basis; consolidated vs standalone is left implicit."
                        % label, metric, period, entity)
            )
    return findings


# --------------------------------------------------------------------------- #
# Check 2 -- cross-source disagreement
# --------------------------------------------------------------------------- #
def check_cross_source(doc: Dict[str, Any]) -> List[Finding]:
    """Compare every ``alt`` read against the primary ``value``.

    This is the check that would have caught the wrong-NPA case: two sources for
    the same figure that disagree by more than a rounding difference. The
    divergence is reported with BOTH figures and BOTH sources so the analyst
    reconciles rather than averages -- averaging two numbers you cannot reconcile
    is precisely the error that puts a wrong figure into the report.
    """
    company = doc.get("company")
    findings: List[Finding] = []
    for _, dp in _iter_real_datapoints(doc):
        alts = dp.get("alt")
        if not isinstance(alts, list) or not alts:
            continue
        primary = to_number(dp.get("value"))
        if primary is None:
            continue
        label = dp_label(dp, company)
        metric = dp.get("metric")
        entity = dp_entity(dp, company)
        period = dp.get("period")
        primary_src = dp.get("source") or "primary source not given"
        for alt in alts:
            if not isinstance(alt, dict):
                continue
            alt_val = to_number(alt.get("value"))
            if alt_val is None:
                continue
            alt_src = alt.get("source") or "alt source not given"
            if primary == 0.0:
                pct = 0.0 if alt_val == 0.0 else float("inf")
            else:
                pct = abs(alt_val - primary) / abs(primary) * 100.0

            if pct == float("inf"):
                findings.append(
                    Finding("CROSS_SOURCE_DIVERGENCE", SEVERITY_ERROR,
                            "%s: primary is 0 (%s) but a source reports %s (%s); "
                            "reconcile before use." % (
                                label, primary_src, _fmt(alt_val), alt_src),
                            metric, period, entity))
                continue
            if pct <= DIVERGENCE_WARN_PCT:
                continue
            severity = SEVERITY_ERROR if pct > DIVERGENCE_ERROR_PCT else SEVERITY_WARN
            findings.append(
                Finding("CROSS_SOURCE_DIVERGENCE", severity,
                        "%s: sources disagree by %.1f%% -- %s (%s) vs %s (%s). %s"
                        % (label, pct, _fmt(primary), primary_src,
                           _fmt(alt_val), alt_src,
                           "Different basis/period/unit is likely; reconcile before use."
                           if severity == SEVERITY_ERROR else
                           "Probably a definitional difference; confirm which to use."),
                        metric, period, entity))
    return findings


# --------------------------------------------------------------------------- #
# Check 3 -- basis mixing
# --------------------------------------------------------------------------- #
def check_basis_mixing(doc: Dict[str, Any]) -> List[Finding]:
    """Detect consolidated and standalone figures mixed in one dataset.

    A ratio whose numerator is consolidated and denominator standalone looks
    plausible and is meaningless, so mixing the two bases within an analysis is an
    error -- unless each deviating figure carries an explicit note explaining why
    (e.g. standalone debt because subsidiary debt is non-recourse), in which case
    it is a disclosed choice and downgraded to a warning. A dataset whose figures
    all contradict the declared basis is flagged too, because the declaration is
    then almost certainly wrong.
    """
    company = doc.get("company")
    declared = normalise_basis(doc.get("reporting_basis"))
    reals = _iter_real_datapoints(doc)
    bases = {}  # basis -> list of (dp)
    for _, dp in reals:
        b = normalise_basis(dp.get("basis"))
        if b in ("consolidated", "standalone"):
            bases.setdefault(b, []).append(dp)

    present = set(bases)
    findings: List[Finding] = []
    if "consolidated" in present and "standalone" in present:
        # Offenders are the figures that deviate from the declared basis; if no
        # basis is declared, the smaller group is treated as the intrusion.
        if declared in present:
            offender_basis = "standalone" if declared == "consolidated" else "consolidated"
        else:
            offender_basis = min(present, key=lambda b: len(bases[b]))
        offenders = bases[offender_basis]
        unnoted = [dp for dp in offenders
                   if not (isinstance(dp.get("note"), str) and dp["note"].strip())]
        keeper_basis = "consolidated" if offender_basis == "standalone" else "standalone"
        off_labels = ", ".join(dp_label(dp, company) for dp in offenders)
        keep_labels = ", ".join(dp_label(dp, company) for dp in bases[keeper_basis])
        if unnoted:
            findings.append(
                Finding("BASIS_MIXING", SEVERITY_ERROR,
                        "Dataset silently mixes bases: %s on %s vs %s on %s. "
                        "Any ratio spanning both is invalid; put the whole analysis "
                        "on one basis or note each exception."
                        % (off_labels, offender_basis, keep_labels, keeper_basis)))
        else:
            findings.append(
                Finding("BASIS_MIXING_NOTED", SEVERITY_WARN,
                        "Dataset mixes bases but each exception is noted (%s on %s). "
                        "Confirm no single ratio draws inputs from both bases."
                        % (off_labels, offender_basis)))
    elif declared and present and declared not in present:
        only = next(iter(present))
        findings.append(
            Finding("BASIS_DECLARATION_MISMATCH", SEVERITY_WARN,
                    "File declares '%s' basis but every figure is '%s'; "
                    "the declared basis appears wrong." % (declared, only)))
    return findings


# --------------------------------------------------------------------------- #
# Check 4 -- unit / currency mixing
# --------------------------------------------------------------------------- #
def check_unit_currency(doc: Dict[str, Any]) -> List[Finding]:
    """Flag unit/currency drift from the file declaration and 10x magnitude slips.

    Two distinct failures share this check. First, a figure labelled in a
    different currency or scale than the file declares, without a note -- the
    quiet path to the crore-vs-million 10x error. Second, two supposedly
    comparable figures (a value against its own alt, or two reads of the same
    metric+period) whose ratio sits almost exactly on 10x/100x -- the loud
    signature of a scale slip, reported as an error because a clean power of ten
    is never a real difference between the same quantity.
    """
    company = doc.get("company")
    file_currency = normalise_currency(doc.get("currency"))
    file_scale = normalise_scale(doc.get("units"))
    findings: List[Finding] = []

    # Part A -- label drift from the file declaration.
    for _, dp in _iter_real_datapoints(doc):
        parsed = parse_unit(dp.get("unit"))
        if parsed is None or not parsed.monetary:
            continue
        noted = isinstance(dp.get("note"), str) and dp["note"].strip()
        if noted:
            continue
        label = dp_label(dp, company)
        metric = dp.get("metric")
        entity = dp_entity(dp, company)
        period = dp.get("period")
        if file_currency and parsed.currency and parsed.currency != file_currency:
            findings.append(
                Finding("UNIT_CURRENCY_MISMATCH", SEVERITY_WARN,
                        "%s is in %s but the file declares %s; add a note or "
                        "convert (state the FX rate and date)."
                        % (label, parsed.currency, file_currency),
                        metric, period, entity))
        if file_scale and parsed.scale and parsed.scale != file_scale:
            findings.append(
                Finding("UNIT_SCALE_MISMATCH", SEVERITY_WARN,
                        "%s is in %s but the file declares %s; a silent crore/million "
                        "mismatch is a 10x error." % (label, parsed.scale, file_scale),
                        metric, period, entity))

    # Part B -- magnitude slips within comparable figures.
    findings.extend(_check_magnitude(doc))
    return findings


def _is_power_of_ten_gap(a: float, b: float) -> Optional[float]:
    """Return the ~10^k factor separating a and b, if one does within tolerance.

    Only clean 10x/100x/1000x gaps qualify: two reads of the same quantity never
    differ by an exact order of magnitude for a legitimate reason, so such a gap
    is a scale error rather than a real difference.
    """
    if a <= 0 or b <= 0:
        return None
    hi, lo = (a, b) if a >= b else (b, a)
    ratio = hi / lo
    for factor in MAGNITUDE_FACTORS:
        if abs(ratio / factor - 1.0) <= MAGNITUDE_TOLERANCE:
            return factor
    return None


def _check_magnitude(doc: Dict[str, Any]) -> List[Finding]:
    """Find order-of-magnitude gaps between comparable monetary figures."""
    company = doc.get("company")
    findings: List[Finding] = []

    # (i) value vs its own alt reads.
    for _, dp in _iter_real_datapoints(doc):
        parsed = parse_unit(dp.get("unit"))
        if parsed is not None and not parsed.monetary:
            continue
        primary = to_number(dp.get("value"))
        if primary is None:
            continue
        alts = dp.get("alt")
        if not isinstance(alts, list):
            continue
        for alt in alts:
            if not isinstance(alt, dict):
                continue
            alt_val = to_number(alt.get("value"))
            if alt_val is None:
                continue
            factor = _is_power_of_ten_gap(primary, alt_val)
            if factor:
                findings.append(
                    Finding("UNIT_MAGNITUDE_MISMATCH", SEVERITY_ERROR,
                            "%s: primary %s and source '%s' %s differ by ~%dx -- "
                            "a unit/scale error (e.g. crore vs million), not a real gap."
                            % (dp_label(dp, company), _fmt(primary),
                               alt.get("source") or "?", _fmt(alt_val), int(factor)),
                            dp.get("metric"), dp.get("period"),
                            dp_entity(dp, company)))

    # (ii) two datapoints for the same entity+metric+period.
    groups: Dict[Tuple[str, str, str], List[Dict[str, Any]]] = {}
    for _, dp in _iter_real_datapoints(doc):
        parsed = parse_unit(dp.get("unit"))
        if parsed is not None and not parsed.monetary:
            continue
        if to_number(dp.get("value")) is None:
            continue
        key = (dp_entity(dp, company), str(dp.get("metric")),
               str(dp.get("period")))
        groups.setdefault(key, []).append(dp)
    for dps in groups.values():
        for i in range(len(dps)):
            for j in range(i + 1, len(dps)):
                a = to_number(dps[i].get("value"))
                b = to_number(dps[j].get("value"))
                factor = _is_power_of_ten_gap(a, b)
                if factor:
                    findings.append(
                        Finding("UNIT_MAGNITUDE_MISMATCH", SEVERITY_ERROR,
                                "%s and %s are the same metric and period yet differ "
                                "by ~%dx -- a likely unit/scale error."
                                % (dp_label(dps[i], company),
                                   dp_label(dps[j], company), int(factor)),
                                dps[i].get("metric"), dps[i].get("period"),
                                dp_entity(dps[i], company)))
    return findings


# --------------------------------------------------------------------------- #
# Check 5 -- period alignment
# --------------------------------------------------------------------------- #
def check_period_alignment(doc: Dict[str, Any]) -> List[Finding]:
    """Warn when figures for one metric mix incompatible period conventions.

    Figures compared as like-for-like must share a period convention. A rolling
    TTM window is not the same shape as a discrete fiscal year; a calendar year
    sits ~3 months off an Indian fiscal year; a March year-end and a December
    year-end are not the same year. Having both an annual and a quarterly figure
    for a metric is normal and is NOT flagged -- only genuinely incomparable mixes
    are.
    """
    company = doc.get("company")
    default_fem = resolve_fy_end_month(doc)
    findings: List[Finding] = []

    groups: Dict[Tuple[str, str], List[Tuple[Dict[str, Any], ParsedPeriod]]] = {}
    for _, dp in _iter_real_datapoints(doc):
        parsed = classify_period(dp.get("period"), default_fem)
        if parsed.kind == "unknown":
            continue
        key = (dp_entity(dp, company), str(dp.get("metric")))
        groups.setdefault(key, []).append((dp, parsed))

    for (entity, metric), members in groups.items():
        if len(members) < 2:
            continue
        kinds = {p.kind for _, p in members}
        labels = ", ".join(dp_label(dp, company) for dp, _ in members)

        if "ttm" in kinds and kinds - {"ttm"}:
            findings.append(
                Finding("PERIOD_ALIGNMENT", SEVERITY_WARN,
                        "'%s' mixes a rolling TTM window with discrete-period "
                        "figures (%s); a TTM is not comparable to a fiscal/calendar "
                        "year." % (metric, labels), metric, None,
                        None if entity == company else entity))
        if "calendar_year" in kinds and "fiscal_year" in kinds:
            findings.append(
                Finding("PERIOD_ALIGNMENT", SEVERITY_WARN,
                        "'%s' mixes calendar-year and fiscal-year periods (%s); "
                        "there is a ~3-month offset between them."
                        % (metric, labels), metric, None,
                        None if entity == company else entity))
        if "bare_year" in kinds and "fiscal_year" in kinds:
            findings.append(
                Finding("PERIOD_ALIGNMENT", SEVERITY_WARN,
                        "'%s' mixes a fiscal-year label with a bare calendar-year "
                        "label (%s); the bare year is ambiguous (FY or CY?)."
                        % (metric, labels), metric, None,
                        None if entity == company else entity))
        fiscal_fems = {p.fy_end_month for _, p in members
                       if p.kind == "fiscal_year" and p.fy_end_month}
        if len(fiscal_fems) > 1:
            months = ", ".join(_month_name(m) for m in sorted(fiscal_fems))
            findings.append(
                Finding("PERIOD_ALIGNMENT", SEVERITY_WARN,
                        "'%s' mixes fiscal years with different year-ends (%s) across "
                        "%s; align the fiscal calendars before comparing."
                        % (metric, months, labels), metric, None,
                        None if entity == company else entity))
    return findings


# --------------------------------------------------------------------------- #
# Check 6 -- recency / staleness
# --------------------------------------------------------------------------- #
def check_recency(doc: Dict[str, Any]) -> List[Finding]:
    """Warn when the gathered data is a period behind, or plainly stale.

    Two failure modes, both drawn from real reports. First: the company has
    reported a newer period than anything gathered -- ``latest_reported_period``
    is ahead of the newest datapoint -- meaning a published quarter was omitted.
    Second: even the newest period known here ends more than ~4 months before
    ``as_of``, so a further quarterly result has almost certainly been released
    since and was never checked. All dates come from the file (as_of), never the
    wall clock, so the gate is reproducible.
    """
    findings: List[Finding] = []
    as_of = parse_iso_date(doc.get("as_of"))
    default_fem = resolve_fy_end_month(doc)

    # Newest period-end among gathered datapoints.
    dp_ends: List[Tuple[date, Dict[str, Any]]] = []
    for _, dp in _iter_real_datapoints(doc):
        parsed = classify_period(dp.get("period"), default_fem)
        if parsed.end_date is not None:
            dp_ends.append((parsed.end_date, dp))
    newest_dp = max(dp_ends, key=lambda t: t[0]) if dp_ends else None

    # The latest period the company has actually reported.
    lrp = doc.get("latest_reported_period")
    lrp_end: Optional[date] = None
    lrp_period = None
    lrp_pub = None
    if isinstance(lrp, dict):
        lrp_period = lrp.get("period")
        lrp_end = classify_period(lrp_period, default_fem).end_date
        lrp_pub = parse_iso_date(lrp.get("published"))

    company = doc.get("company")

    # Mode 1: a reported period newer than anything gathered.
    if lrp_end is not None and newest_dp is not None:
        gap = (lrp_end - newest_dp[0]).days
        if gap > RECENCY_NEWER_PERIOD_DAYS:
            pub = (" published %s" % lrp_pub.isoformat()) if lrp_pub else ""
            findings.append(
                Finding("RECENCY_UNINCORPORATED", SEVERITY_WARN,
                        "A more recent reported period exists but is not incorporated: "
                        "latest reported is %s (ends ~%s%s), yet the newest gathered "
                        "figure is %s (ends ~%s). Pull the newer period before analysing."
                        % (lrp_period, lrp_end.isoformat(), pub,
                           dp_label(newest_dp[1], company),
                           newest_dp[0].isoformat())))

    # Mode 2: newest known period-end is far behind as_of.
    reference_ends = [e for e in
                      [newest_dp[0] if newest_dp else None, lrp_end]
                      if e is not None]
    if as_of is not None and reference_ends:
        reference = max(reference_ends)
        stale_days = (as_of - reference).days
        if stale_days > RECENCY_STALE_DAYS:
            findings.append(
                Finding("RECENCY_STALE", SEVERITY_WARN,
                        "The newest period-end known here (%s) is %d days (~%.1f months) "
                        "before as_of %s; a further quarter has almost certainly been "
                        "reported since -- search for results after %s."
                        % (reference.isoformat(), stale_days, stale_days / 30.44,
                           as_of.isoformat(), reference.isoformat())))

    # Consistency: a publish date after the gather date is contradictory.
    if as_of is not None and lrp_pub is not None and lrp_pub > as_of:
        findings.append(
            Finding("RECENCY_DATE_INCONSISTENT", SEVERITY_WARN,
                    "latest_reported_period.published (%s) is after as_of (%s); "
                    "one of the two dates is wrong."
                    % (lrp_pub.isoformat(), as_of.isoformat())))
    return findings


# --------------------------------------------------------------------------- #
# Check 7 -- coverage (orphan 'not available')
# --------------------------------------------------------------------------- #
def check_coverage(doc: Dict[str, Any]) -> List[Finding]:
    """Report, as info, how many metrics were explicitly marked unavailable.

    Declaring a metric unsourced is the opposite of a defect: it is the honest
    alternative to fabricating a number to fill a cell. This is surfaced as
    coverage context so the reader can weigh how complete the intake is, never as
    something to fix.
    """
    marked: List[str] = []
    for dp in doc.get("datapoints", []) or []:
        if isinstance(dp, dict) and is_unavailable(dp):
            marked.append(str(dp.get("metric") or "(unnamed)"))
    extra = doc.get("not_available")
    if isinstance(extra, list):
        for item in extra:
            if isinstance(item, str) and item.strip():
                marked.append(item.strip())
            elif isinstance(item, dict) and item.get("metric"):
                marked.append(str(item["metric"]))

    if not marked:
        return []
    unique = sorted(set(marked))
    return [
        Finding("COVERAGE_UNAVAILABLE", SEVERITY_INFO,
                "Coverage: %d metric(s) explicitly marked not-available "
                "(good discipline -- gaps disclosed, not fabricated): %s."
                % (len(unique), ", ".join(unique)))
    ]


# --------------------------------------------------------------------------- #
# Check 8 -- source tier (documents primary, aggregators navigation-only)
# --------------------------------------------------------------------------- #
def check_source_tier(doc: Dict[str, Any]) -> List[Finding]:
    """Enforce the document-first rule: figures must trace to the filings.

    The skill's source of record is the company's own filings (Tier 1),
    company-published secondary (Tier 2) and regulator/third-party primary
    (Tier 3). Aggregators -- screener.in, tickertape, yahoo, moneycontrol -- are
    Tier 4: navigation aids and optional cross-checks, never a citable source.
    This is the exact hole a report falls through when it looks well-sourced (a
    period label sits next to every figure) yet every number actually came from
    an aggregator screen. So:

    * a HEADLINE metric (revenue, PAT, EBITDA, debt, equity, operating cash flow)
      whose only source is Tier 4 is an ERROR -- trace it to the filing;
    * any other aggregator-only figure is a WARN -- fine as a cross-check, but
      replace it with the document before relying on it;
    * a headline figure whose source cannot be confirmed as a filing (unknown
      tier) is a WARN -- tag it or cite the document rather than taking it on
      trust;
    * current price / market cap is the one sanctioned exchange-sourced exception
      and is exempt;
    * a coverage line reports the share of figures that are primary-sourced.
    """
    company = doc.get("company")
    findings: List[Finding] = []
    n_counted = 0      # figures that are not the market-data exception
    n_primary = 0      # Tier 1-3
    n_aggregator = 0   # Tier 4
    n_unknown = 0      # tier could not be established

    for _, dp in _iter_real_datapoints(doc):
        metric = dp.get("metric")
        if is_market_data_metric(metric):
            continue  # price/market cap: exchange-sourced by nature, exempt.
        label = dp_label(dp, company)
        period = dp.get("period")
        entity = dp_entity(dp, company)
        source_text = dp.get("source") if isinstance(dp.get("source"), str) else ""
        tier, inferred = resolve_source_tier(dp)
        headline = is_headline_metric(metric)
        n_counted += 1

        # Guard: an explicit Tier 1-3 label that contradicts an aggregator-looking
        # source. Silent mislabelling would defeat the whole check.
        explicit = dp.get("source_tier")
        explicit_primary = (
            isinstance(explicit, (int, float)) and not isinstance(explicit, bool)
            and int(explicit) in (1, 2, 3)
        )
        if (explicit_primary and _TIER4_SOURCE_RE.search(source_text)
                and not (_TIER1_SOURCE_RE.search(source_text)
                         or _TIER2_SOURCE_RE.search(source_text)
                         or _TIER3_SOURCE_RE.search(source_text))):
            findings.append(
                Finding("SOURCE_TIER_MISLABELLED", SEVERITY_WARN,
                        "%s is labelled Tier %d but its source reads like an "
                        "aggregator (\"%s\"); confirm it traces to a primary "
                        "filing." % (label, int(explicit), source_text),
                        metric, period, entity))

        if tier in (1, 2, 3):
            n_primary += 1
        elif tier == 4:
            n_aggregator += 1
            if headline:
                findings.append(
                    Finding("SOURCE_TIER_HEADLINE_AGGREGATOR", SEVERITY_ERROR,
                            "%s is a headline metric sourced only from an "
                            "aggregator/third-party (\"%s\"). Trace it to the "
                            "primary filing -- an aggregator is a navigation aid, "
                            "not a source of record." % (label, source_text),
                            metric, period, entity))
            else:
                findings.append(
                    Finding("SOURCE_TIER_AGGREGATOR", SEVERITY_WARN,
                            "%s is sourced only from an aggregator (\"%s\"); fine "
                            "as a labelled cross-check, but replace it with the "
                            "filing before relying on it." % (label, source_text),
                            metric, period, entity))
        else:  # unknown tier
            n_unknown += 1
            if headline:
                findings.append(
                    Finding("SOURCE_TIER_UNCONFIRMED", SEVERITY_WARN,
                            "%s is a headline metric whose source (\"%s\") could "
                            "not be confirmed as a primary filing; set source_tier "
                            "or cite the document so it is not taken on trust."
                            % (label, source_text or "no source"),
                            metric, period, entity))

    if n_counted:
        pct = 100.0 * n_primary / n_counted
        findings.append(
            Finding("SOURCE_TIER_COVERAGE", SEVERITY_INFO,
                    "Provenance: %d of %d figures (%.0f%%) trace to a primary "
                    "source (Tier 1-3); %d aggregator-only, %d unconfirmed. "
                    "Headline metrics should be 100%% primary."
                    % (n_primary, n_counted, pct, n_aggregator, n_unknown)))
    return findings


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #
_CHECKS = (
    check_datapoint_shape,
    check_metadata,
    check_provenance,
    check_cross_source,
    check_basis_mixing,
    check_unit_currency,
    check_period_alignment,
    check_recency,
    check_coverage,
    check_source_tier,
)


def verify(doc: Dict[str, Any]) -> List[Finding]:
    """Run every check and return all findings, sorted for the report.

    Findings are ordered by severity (errors, then warnings, then info) so the
    report and the exit-code decision both read off one list.
    """
    findings: List[Finding] = []
    for check in _CHECKS:
        findings.extend(check(doc))
    findings.sort(key=lambda f: (_SEVERITY_RANK.get(f.severity, 9), f.rule_id))
    return findings


def counts(findings: Sequence[Finding]) -> Dict[str, int]:
    """Tally findings by severity."""
    tally = {SEVERITY_ERROR: 0, SEVERITY_WARN: 0, SEVERITY_INFO: 0}
    for f in findings:
        tally[f.severity] = tally.get(f.severity, 0) + 1
    return tally


def verdict(findings: Sequence[Finding]) -> str:
    """Return the headline verdict from the finding severities."""
    tally = counts(findings)
    if tally[SEVERITY_ERROR]:
        return "FAIL"
    if tally[SEVERITY_WARN]:
        return "PASS-WITH-WARNINGS"
    return "PASS"


# --------------------------------------------------------------------------- #
# Formatting helpers
# --------------------------------------------------------------------------- #
def _fmt(number: float) -> str:
    """Format a figure without noise: no trailing .0 on whole numbers."""
    if number == int(number):
        return "{:,}".format(int(number))
    return "{:,.4g}".format(number) if abs(number) < 1 else "{:,.2f}".format(number)


def _month_name(month: Optional[int]) -> str:
    """Return an abbreviated month name for a 1-12 month number."""
    names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    if isinstance(month, int) and 1 <= month <= 12:
        return names[month]
    return "?"


def render_text(doc: Dict[str, Any], findings: Sequence[Finding]) -> str:
    """Render the human report: header, verdict, one-line summary, grouped findings."""
    tally = counts(findings)
    v = verdict(findings)
    n_dp = len([d for d in doc.get("datapoints", []) or []
                if isinstance(d, dict) and not is_unavailable(d)])
    n_na = len([d for d in doc.get("datapoints", []) or []
                if isinstance(d, dict) and is_unavailable(d)])

    lines: List[str] = []
    lines.append("=" * 72)
    lines.append("DATA-INTAKE VERIFICATION")
    lines.append("=" * 72)
    company = doc.get("company") or "(company not stated)"
    ticker = doc.get("ticker")
    lines.append("Company        : %s%s" % (company, " [%s]" % ticker if ticker else ""))
    lines.append("As of          : %s" % (doc.get("as_of") or "(not stated)"))
    lines.append("Basis          : %s" % (doc.get("reporting_basis") or "(not stated)"))
    lines.append("Units          : %s %s"
                 % (doc.get("currency") or "?", doc.get("units") or "?"))
    lrp = doc.get("latest_reported_period")
    if isinstance(lrp, dict):
        lines.append("Latest reported: %s (published %s)"
                     % (lrp.get("period") or "?", lrp.get("published") or "?"))
    lines.append("Datapoints     : %d (+%d marked not-available)" % (n_dp, n_na))
    lines.append("")
    lines.append("VERDICT: %s" % v)
    lines.append("Summary: %d error(s), %d warning(s), %d info."
                 % (tally[SEVERITY_ERROR], tally[SEVERITY_WARN], tally[SEVERITY_INFO]))

    for severity, heading in (
        (SEVERITY_ERROR, "ERRORS (block analysis until resolved)"),
        (SEVERITY_WARN, "WARNINGS (review before relying on the figures)"),
        (SEVERITY_INFO, "INFO (coverage context)"),
    ):
        group = [f for f in findings if f.severity == severity]
        if not group:
            continue
        lines.append("")
        lines.append("-" * 72)
        lines.append("%s -- %d" % (heading, len(group)))
        lines.append("-" * 72)
        for f in group:
            lines.append("[%s] %s" % (f.rule_id, f.message))

    if not findings:
        lines.append("")
        lines.append("No findings: all datapoints are traceable, consistent and current.")
    return "\n".join(lines)


def render_json(doc: Dict[str, Any], findings: Sequence[Finding]) -> str:
    """Render the machine-readable report used by --json."""
    tally = counts(findings)
    payload = {
        "company": doc.get("company"),
        "ticker": doc.get("ticker"),
        "as_of": doc.get("as_of"),
        "verdict": verdict(findings),
        "counts": {
            "error": tally[SEVERITY_ERROR],
            "warn": tally[SEVERITY_WARN],
            "info": tally[SEVERITY_INFO],
        },
        "findings": [f.to_dict() for f in findings],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


# --------------------------------------------------------------------------- #
# Built-in template and example
# --------------------------------------------------------------------------- #
TEMPLATE = """\
// Data-intake verification template for the stock-analysis skill.
// Fill this in with the data you have GATHERED, then run:
//     python verify_data.py this_file.json
// Whole-line // comments (like these) are stripped by the loader; keep any
// comment on its own line. Delete the sample datapoints and add your own.
{
  "company": "",
  "ticker": "",
  "as_of": "YYYY-MM-DD",
  "reporting_basis": "consolidated",
  "currency": "INR",
  "units": "crore",
  "fiscal_year_end": "March",
  "latest_reported_period": {
    "period": "Q1 FY27",
    "published": "YYYY-MM-DD"
  },
  "datapoints": [
    {
      "metric": "revenue",
      "value": 0,
      "period": "FY26",
      "basis": "consolidated",
      "unit": "INR crore",
      "source": "FY26 annual report, p.xxx",
      // source_tier: 1 filing, 2 company secondary, 3 regulator/rating, 4
      // aggregator. Omit to let the source text be classified automatically.
      // A Tier-4-only headline metric (revenue/PAT/EBITDA/debt/equity/OCF) fails.
      "source_tier": 1,
      "alt": [
        {"value": 0, "source": "screener.in (cross-check only), dated"}
      ]
    }
  ],
  "not_available": [
    "any metric you looked for and could not source"
  ]
}
"""


def example_document() -> Dict[str, Any]:
    """Return a filled example that deliberately trips a few warnings.

    It is intentionally clean of errors so --example demonstrates the
    PASS-WITH-WARNINGS path: a ~3% cross-source gap, a datapoint missing its
    unit, a gathered set that stops a quarter behind the latest reported period,
    and a non-headline ratio sourced only from an aggregator -- the common intake
    defects the review found. Every headline metric traces to a filing, so the
    tier check raises no error.
    """
    return {
        "company": "Meridian Bank Ltd",
        "ticker": "NSE:MERIDBANK",
        "as_of": "2026-07-24",
        "reporting_basis": "consolidated",
        "currency": "INR",
        "units": "crore",
        "fiscal_year_end": "March",
        "latest_reported_period": {"period": "Q1 FY27", "published": "2026-07-11"},
        "datapoints": [
            {"metric": "net_interest_income", "value": 18200, "period": "FY26",
             "basis": "consolidated", "unit": "INR crore", "source_tier": 1,
             "source": "FY26 annual report, p.118",
             "alt": [{"value": 18150, "source": "screener.in 2026-07-20"}]},
            {"metric": "net_profit", "value": 8200, "period": "FY26",
             "basis": "consolidated", "unit": "INR crore", "source_tier": 1,
             "source": "FY26 annual report, p.104",
             "alt": [{"value": 8460, "source": "screener.in 2026-07-20"}]},
            {"metric": "gross_npa_pct", "value": 1.9, "period": "FY26",
             "basis": "consolidated",
             "source": "FY26 annual report, asset-quality note"},
            {"metric": "gross_npa_pct", "value": 3.1, "period": "FY26",
             "entity": "Rival Bank Ltd", "basis": "consolidated", "unit": "%",
             "source": "Rival Bank FY26 results filing, 2026-05-08"},
            {"metric": "casa_ratio_pct", "value": 44.0, "period": "FY26",
             "basis": "consolidated", "unit": "%",
             "source": "FY26 investor presentation, slide 12"},
            {"metric": "pe_ratio", "value": 14.2, "period": "FY26",
             "basis": "consolidated", "unit": "x",
             "source": "screener.in 2026-07-20"},
        ],
        "not_available": ["provision_coverage_ratio"],
    }


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    """Construct the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog=SCRIPT,
        description="Verify gathered stock-analysis data BEFORE analysing it: "
                    "provenance, cross-source agreement, basis/unit consistency, "
                    "period alignment and recency.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", nargs="?", help="path to the intake JSON file")
    parser.add_argument("--json", dest="as_json", action="store_true",
                        help="emit findings as JSON instead of a text report")
    parser.add_argument("--template", action="store_true",
                        help="print an annotated blank intake file and exit")
    parser.add_argument("--example", action="store_true",
                        help="run the built-in example (surfaces sample warnings)")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Entry point. Returns a process exit code (0 pass, 1 fail, 2 bad input)."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.template:
        sys.stdout.write(TEMPLATE)
        return 0

    if args.example:
        doc = example_document()
    else:
        if not args.input:
            parser.error("an intake JSON file is required (or use --template / --example)")
        try:
            doc = load_intake(args.input)
        except ValueError as err:
            sys.stderr.write("%s: %s\n" % (SCRIPT, err))
            return 2

    findings = verify(doc)
    if args.as_json:
        sys.stdout.write(render_json(doc, findings) + "\n")
    else:
        sys.stdout.write(render_text(doc, findings) + "\n")

    return 1 if counts(findings)[SEVERITY_ERROR] else 0


if __name__ == "__main__":
    sys.exit(main())
