#!/usr/bin/env python3
"""Finished-report linter for the stock-analysis skill.

WHAT THIS IS
============
A *mechanical* QA pass that the analysis agent runs on its OWN finished
markdown report before delivering it. It exists because adversarial review
found real reports that silently violated the skill's non-negotiables:

    * every figure must carry a source and a period;
    * figures must trace to filings, not be cited only to an aggregator;
    * units and consolidated-vs-standalone must be stated;
    * a recency statement must be present;
    * disqualifying gates must be marked checked-or-not (when a score is shown);
    * a bear case must exist, with thesis-invalidation triggers;
    * the output must read as research, not personalised investment advice.

This script is the first line of defence so a human reviewer is not. It is a
*linter*, not a fact-checker: it can tell you a number has no visible source,
it cannot tell you the number is right.

WHAT THIS IS NOT
================
The figure-sourcing check is the core of the tool and it is a **heuristic**.
It measures how many financial figures sit near a provenance cue (a page
number, a filing name, a fiscal-year/period label, a URL, "as of", ...). A
figure counted as "cued" is not proven sourced, and a figure counted as
"bare" is not proven fabricated -- it may draw on a source stated a paragraph
away, or in a cell the heuristic could not associate with it. The output is a
*prompt to review*, deliberately tuned to over-report rather than miss silent
un-sourcing. Read the flagged snippets; do not treat the percentage as a grade
of honesty.

Design choices that bound the heuristic (and their limits):
    * A figure's "window" is the unit it lives in -- the whole line for a table
      row, list item, or heading; the enclosing sentence for prose. A cue
      anywhere in that window counts for every figure in it. This mirrors how
      analysts cite ("... 18.4%, 12.1%, 9.7% [FY25 AR, p.142]") but it means a
      long prose sentence with one cue can shield several figures, and a cue in
      an *adjacent* sentence is not credited. Both effects are accepted.
    * Sentence splitting is conservative (it will not break "3.26%" or "p.142")
      but it is not a parser; unusual punctuation can mis-segment.
    * The cue vocabulary is fixed. A genuine but exotic citation style the list
      does not know will read as bare. That is the safe direction to err.

Stdlib only. Python 3.7+. No third-party dependencies.

USAGE
=====
    python lint_report.py REPORT.md
    python lint_report.py REPORT.md --json
    python lint_report.py REPORT.md --strict     # warnings count as errors

Exit codes: 0 = clean or warnings only; 1 = at least one error (grade FAIL);
2 = usage / file-access error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

# ---------------------------------------------------------------------------
# Result model
# ---------------------------------------------------------------------------

PASS, WARN, FAIL, INFO, SKIP = "PASS", "WARN", "FAIL", "INFO", "SKIP"

GROUP_STRUCTURE = "STRUCTURE"
GROUP_SOURCING = "FIGURE SOURCING"
GROUP_HYGIENE = "HYGIENE"

GROUP_ORDER = [GROUP_STRUCTURE, GROUP_SOURCING, GROUP_HYGIENE]


@dataclass
class Finding:
    """One rule's verdict on the report."""

    id: str
    group: str
    status: str  # PASS / WARN / FAIL / INFO / SKIP
    message: str
    line: Optional[int] = None
    snippet: Optional[str] = None
    details: List[str] = field(default_factory=list)
    # Machine-readable extras (only figure-sourcing populates this today).
    extra: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = {
            "id": self.id,
            "group": self.group,
            "status": self.status,
            "message": self.message,
        }
        if self.line is not None:
            d["line"] = self.line
        if self.snippet:
            d["snippet"] = self.snippet
        if self.details:
            d["details"] = self.details
        if self.extra:
            d["extra"] = self.extra
        return d


# ---------------------------------------------------------------------------
# Text utilities
# ---------------------------------------------------------------------------

def clip(text: str, width: int = 100) -> str:
    """Collapse whitespace and truncate for single-line display."""
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= width else text[: width - 3] + "..."


def strip_md(text: str) -> str:
    """Drop the noisiest markdown emphasis markers for cleaner snippets."""
    return text.replace("**", "").replace("`", "").replace("__", "")


def is_table_row(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and s.count("|") >= 2


def is_table_separator(line: str) -> bool:
    s = line.strip()
    # e.g. |---|---:|:--| ...
    return bool(re.fullmatch(r"\|?[\s:|-]*\|[\s:|-]*", s)) and "-" in s


def is_list_item(line: str) -> bool:
    return bool(re.match(r"\s*(?:[-*+]\s+|\d+[.)]\s+)", line))


def is_heading(line: str) -> bool:
    return bool(re.match(r"\s*#{1,6}\s+", line)) or bool(
        re.match(r"\s*\*\*[^*]+\*\*\s*$", line)
    )


# Conservative sentence splitter. Splits on . ! ? ; followed by whitespace and
# an opening character (capital letter, bracket, or currency symbol). It will
# NOT split "3.26%" (period followed by a digit) nor "p.142" for the same
# reason, which is what we want -- those are the two ways a naive splitter
# separates a figure from its citation.
_SENT_SPLIT = re.compile(r"(?<=[.!?;])\s+(?=[A-Z(\[₹$£€])")


def split_sentences(text: str) -> List[str]:
    parts = _SENT_SPLIT.split(text)
    return [p for p in parts if p.strip()] or [text]


def iter_units(lines: List[str]):
    """Yield (line_number, unit_text) pairs.

    Table rows, list items, and headings are emitted whole (their window is the
    row / bullet). Prose lines are split into sentences so a lone citation does
    not vouch for figures three sentences away.
    """
    for idx, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")
        if not line.strip():
            continue
        if is_table_row(line) or is_list_item(line) or is_heading(line):
            yield idx, line
        else:
            for sent in split_sentences(line):
                yield idx, sent


# ---------------------------------------------------------------------------
# Figure detection
# ---------------------------------------------------------------------------
# A "financial figure" is a percentage, a currency amount, a scaled quantity
# (crore / lakh / bn / mn ...), a valuation multiple (15.2x), or a basis-point
# figure. Bare integers and years are deliberately NOT figures: "in 2021" or
# "9,694 branches" are not the kind of claim that needs a filing citation, and
# counting them would swamp the signal.

_CUR = r"(?:₹|Rs\.?|INR|US\$|USD|\$|£|€)"
_SCALE = r"(?:cr|crores?|lakhs?|bn|mn|billion|million|trillion|thousand)"
_NUM = r"\d[\d,]*(?:\.\d+)?"

FIGURE_RE = re.compile(
    r"(?P<currency>" + _CUR + r"\s?" + _NUM + r"(?:\s?" + _SCALE + r")?)"
    r"|(?P<scaled>" + _NUM + r"\s?" + _SCALE + r"\b)"
    r"|(?P<percent>" + _NUM + r"\s?%)"
    r"|(?P<bps>\d+(?:\.\d+)?\s?bps\b)"
    r"|(?P<multiple>\d+(?:\.\d+)?\s?[x×](?![a-wyz]))",
    re.IGNORECASE,
)


def find_figures(text: str) -> List[str]:
    """Return the surface strings of financial figures in *text*."""
    out = []
    for m in FIGURE_RE.finditer(text):
        out.append(m.group(0).strip())
    return out


# ---------------------------------------------------------------------------
# Provenance cues
# ---------------------------------------------------------------------------
# The vocabulary that, appearing in a figure's window, marks the figure as
# carrying a source or a period. Enumerated (not open-ended) on purpose: a
# fixed list makes "bare" reproducible and keeps the check auditable.

_CUE_PATTERNS = [
    r"\bsources?\b",                              # "source", "sources"
    r"\bFY\s?-?\s?\d{2,4}\b",                     # FY25, FY2024
    r"\bH[12]\s?FY\b|\bQ[1-4]\s?FY\b",            # H1 FY, Q1 FY (period label)
    r"(?<![\d,])(?:19|20)\d{2}(?![\d,])",         # a standalone 4-digit year
    r"\b(?:10-K|10-Q|20-F|8-K|6-K|DEF\s?14A|S-1|F-1)\b",  # SEC filings
    r"\b(?:CARO|LODR|SEBI|EDGAR|accession|DRHP|RHP)\b",   # India/US filing refs
    r"\bannual report\b",
    r"\bAR\b",                                    # "FY25 AR"
    r"\bscreener\b",
    r"\b(?:concall|con-?call)\b",
    r"\bearnings\s+(?:call|presentation|release|report|deck)\b",
    r"\b(?:presentation|transcript|prospectus|filing|filed|intimation)\b",
    r"\b(?:press|results?)\s+release\b",
    r"\bas[-\s]?(?:of|at)\b",
    r"\bpp?\.\s?\d",                              # p.142 / pp.10
    r"\bpage\s?\d",
    r"\bItem\s?\d",                               # 10-K Item 8
    r"\bNote\s?\d",                               # Note 32
    r"§\s?\d",                                     # §12 / [§3] section reference
    r"\bclause\b",
    r"\bTTM\b",                                   # trailing-twelve-months period
    r"https?://|www\.",                           # explicit URL
    r"\b[\w-]{2,}\.(?:in|com|org|net|gov|io|co)\b",       # bare domain
    # month-year date, incl. 2-digit years the year-rule above misses (Jul-26)
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[-\s]?\d{2,4}\b",
]

CUE_RE = re.compile("|".join(_CUE_PATTERNS), re.IGNORECASE)


def has_cue(text: str) -> bool:
    return bool(CUE_RE.search(text))


@dataclass
class SourcingResult:
    total: int
    cued: int
    bare_samples: List[Tuple[int, str]]

    @property
    def ratio(self) -> float:
        return (self.cued / self.total) if self.total else 1.0


# A pure unit-conversion identity ("1 bn = 100 crore = 10 million") states no
# claim about the company and needs no citation; skip it so it does not count
# as bare noise.
_CONVERSION_RE = re.compile(
    r"^\s*\d[\d,.]*\s*(?:bn|cr|crore|lakh|mn|million|billion|thousand)\b\s*=",
    re.IGNORECASE,
)


def table_block_context_cue(lines: List[str]) -> dict:
    """For each table-row line index (0-based), does its table carry a cue?

    Analysts routinely source a table once -- in a caption line just above it
    ("Advances under management ... [p.10]:") or in the header row -- rather
    than in every cell. This credits every row of such a table with that
    table-level cue. LIMIT: a single caption citation then vouches for the whole
    table, so a genuinely mixed table (some rows sourced, some invented) can be
    scored generously. That is the accepted direction of error for a linter
    meant to prompt review, not to adjudicate.
    """
    n = len(lines)
    result: dict = {}
    i = 0
    while i < n:
        if not is_table_row(lines[i]):
            i += 1
            continue
        start = i
        while i < n and is_table_row(lines[i]):
            i += 1
        end = i  # exclusive
        # Caption = the immediately preceding non-blank line, if it is prose.
        j = start - 1
        while j >= 0 and lines[j].strip() == "":
            j -= 1
        caption = lines[j] if (j >= 0 and not is_table_row(lines[j])) else ""
        header = lines[start]  # first row of the block
        ctx_cue = has_cue(caption) or has_cue(header)
        for k in range(start, end):
            result[k] = ctx_cue
    return result


def analyse_sourcing(lines: List[str], max_samples: int = 12) -> SourcingResult:
    """Core heuristic: fraction of financial figures near a provenance cue."""
    total = 0
    cued = 0
    bare: List[Tuple[int, str]] = []
    block_cue = table_block_context_cue(lines)
    for line_no, unit in iter_units(lines):
        if _CONVERSION_RE.match(unit):
            continue
        figs = find_figures(unit)
        if not figs:
            continue
        unit_has_cue = has_cue(unit)
        if not unit_has_cue and is_table_row(unit):
            unit_has_cue = block_cue.get(line_no - 1, False)
        for fig in figs:
            total += 1
            if unit_has_cue:
                cued += 1
            elif len(bare) < max_samples:
                bare.append((line_no, "%s  --  %s" % (fig, clip(strip_md(unit), 80))))
    return SourcingResult(total=total, cued=cued, bare_samples=bare)


# ---------------------------------------------------------------------------
# Structural checks
# ---------------------------------------------------------------------------

# A forensic-mode review (references/18-forensic-mode.md) is a different document:
# it answers "can these accounts bear weight?", so it deliberately has no
# investment bear case and no thesis-invalidation triggers, and it uses a
# "Document base" section in place of a Data Quality Note. Detect it so those
# standard-report checks relax instead of failing a correct forensic report.
# The verdict clause must be the forensic "Verdict: <LETTER> — <label>" form
# (letter followed by a dash separator), so a Standard verdict that happens to
# start with the article "A" ("Verdict: A high-quality compounder") is not
# misread as forensic.
_FORENSIC_RE = re.compile(
    r"^#{1,3}\s*forensic review\b|\bforensic mode\b"
    r"|verdict:\s*\**[A-DU]\**\s*[—–-]",
    re.IGNORECASE | re.MULTILINE,
)


def is_forensic_report(text: str) -> bool:
    """True if the report is a Forensic-mode review rather than a Standard one."""
    return bool(_FORENSIC_RE.search(text[:3000]))


def _first_match(lines: List[str], pattern: str, flags=re.IGNORECASE,
                 upto: Optional[int] = None) -> Optional[Tuple[int, str]]:
    rx = re.compile(pattern, flags)
    end = len(lines) if upto is None else min(upto, len(lines))
    for i in range(end):
        if rx.search(lines[i]):
            return i + 1, lines[i].strip()
    return None


def check_recency(lines: List[str], text: str) -> Finding:
    """Recency statement present (period label + a checked-through date)."""
    hit = _first_match(
        lines,
        r"##\s*RECENCY\b|\brecency statement\b|latest reported (?:period|quarter)"
        r"|most recent (?:reported|period|quarter|full)|events checked through",
    )
    if hit:
        return Finding("recency-statement", GROUP_STRUCTURE, PASS,
                       "Recency statement found.", hit[0], clip(strip_md(hit[1])))
    # Weaker fallback: an "as of" plus an explicit period somewhere.
    weak = _first_match(lines, r"\bas[-\s]?of\b") and _first_match(
        lines, r"\bFY\s?\d{2}\b|\bQ[1-4]\s?FY")
    if weak:
        return Finding("recency-statement", GROUP_STRUCTURE, WARN,
                       "No explicit recency statement; only scattered 'as of' / "
                       "period labels. Add a RECENCY block stating the most "
                       "recent period incorporated and events-checked-through date.")
    return Finding("recency-statement", GROUP_STRUCTURE, FAIL,
                   "No recency statement. A reader cannot tell how current the "
                   "analysis is. State the latest reported period and the date "
                   "through which events were checked.")


def check_data_quality(lines: List[str], text: str) -> Finding:
    """Data Quality Note present (sources, as-of dates, estimates, gaps)."""
    if is_forensic_report(text):
        doc_base = _first_match(lines, r"document base|documents obtained")
        if doc_base:
            return Finding("data-quality-note", GROUP_STRUCTURE, PASS,
                           "Forensic 'Document base' section found (the forensic "
                           "equivalent of the Data Quality Note).",
                           doc_base[0], clip(strip_md(doc_base[1])))
    hit = _first_match(lines, r"data[\s-]*quality note|##\s*DATA QUALITY")
    if hit:
        return Finding("data-quality-note", GROUP_STRUCTURE, PASS,
                       "Data Quality Note found.", hit[0], clip(strip_md(hit[1])))
    softer = _first_match(lines, r"\bprimary sources\b|##\s*sources\b|\bdata note\b")
    if softer:
        return Finding("data-quality-note", GROUP_STRUCTURE, WARN,
                       "No formal Data Quality Note; found a lighter sources/data "
                       "note instead. Add a note that defines sources, as-of "
                       "dates, what is estimated, and what is missing.",
                       softer[0], clip(strip_md(softer[1])))
    return Finding("data-quality-note", GROUP_STRUCTURE, WARN,
                   "No Data Quality Note found. The reader needs one before the "
                   "numbers: sources, as-of dates, estimates, and known gaps.")


def check_reporting_basis(lines: List[str], text: str) -> Finding:
    """Consolidated vs standalone stated (a non-negotiable)."""
    hit = _first_match(lines, r"\bconsolidated\b|\bstandalone\b")
    if hit:
        return Finding("reporting-basis", GROUP_STRUCTURE, PASS,
                       "Reporting basis (consolidated / standalone) stated.",
                       hit[0], clip(strip_md(hit[1])))
    return Finding("reporting-basis", GROUP_STRUCTURE, FAIL,
                   "Reporting basis not stated. Say consolidated or standalone "
                   "-- for many groups they are different companies.")


def check_currency_units(lines: List[str], text: str) -> Finding:
    """Currency and scale stated somewhere (a non-negotiable)."""
    # Prefer an explicit units statement; fall back to a symbol + scale word.
    explicit = _first_match(lines, r"currency and (?:units|scale)|\ball figures (?:in|are)\b")
    symbol_scale = re.search(
        r"(?:" + _CUR + r").{0,40}?" + _SCALE + r"|\b" + _SCALE + r"\b.{0,20}?(?:" + _CUR + r")",
        text, re.IGNORECASE,
    )
    header_units = re.search(r"₹\s?(?:cr|crore|bn|mn|lakh)\b|\$\s?(?:m|bn|million|billion)\b",
                             text, re.IGNORECASE)
    if explicit:
        return Finding("currency-units", GROUP_STRUCTURE, PASS,
                       "Currency and units explicitly stated.",
                       explicit[0], clip(strip_md(explicit[1])))
    if symbol_scale or header_units:
        return Finding("currency-units", GROUP_STRUCTURE, PASS,
                       "Currency symbol and scale word present in the text.")
    return Finding("currency-units", GROUP_STRUCTURE, FAIL,
                   "Currency and/or units not stated. State the currency and "
                   "whether figures are in crore / lakh / mn / bn.")


def check_verdict(lines: List[str], text: str) -> Finding:
    """A verdict / summary near the top so a one-screen reader gets the point."""
    nonblank = sum(1 for line in lines if line.strip())
    top_cut = max(60, int(0.35 * len(lines)))
    pattern = (r"##\s*(?:VERDICT|SUMMARY|BOTTOM LINE)|"
               r"\bverdict\b|\bthe short version\b|\bshort version\b|"
               r"\bkey (?:risks|takeaways?)\b|\bat a glance\b|\btl;?dr\b|\bbottom line\b")
    hit = _first_match(lines, pattern)
    if not hit:
        return Finding("verdict-summary", GROUP_STRUCTURE, WARN,
                       "No verdict / summary section found. Front-load a one-line "
                       "assessment so a reader who stops after one screen still "
                       "gets the conclusion.")
    if hit[0] <= top_cut:
        return Finding("verdict-summary", GROUP_STRUCTURE, PASS,
                       "Verdict / summary present near the top.",
                       hit[0], clip(strip_md(hit[1])))
    return Finding("verdict-summary", GROUP_STRUCTURE, WARN,
                   "Verdict / summary is present but buried (line %d of ~%d). "
                   "Move it up: the conclusion should survive a partial read."
                   % (hit[0], nonblank), hit[0], clip(strip_md(hit[1])))


def check_risks_bear(lines: List[str], text: str) -> Finding:
    """A risks or bear-case section (bear case is a non-negotiable)."""
    if is_forensic_report(text):
        return Finding("risks-bear-case", GROUP_STRUCTURE, SKIP,
                       "Forensic review: an investment bear case is not expected "
                       "in forensic mode (the question is accounts integrity, not "
                       "investment merit).")
    bear = _first_match(lines, r"\bbear case\b|##\s*.*\bbear\b")
    risks = _first_match(lines, r"\bkey risks\b|##\s*.*\brisks?\b|what could break")
    if bear:
        return Finding("risks-bear-case", GROUP_STRUCTURE, PASS,
                       "Bear-case section found.", bear[0], clip(strip_md(bear[1])))
    if risks:
        return Finding("risks-bear-case", GROUP_STRUCTURE, WARN,
                       "A risks section is present but no dedicated, argued bear "
                       "case. Write the short thesis as if defending it.",
                       risks[0], clip(strip_md(risks[1])))
    return Finding("risks-bear-case", GROUP_STRUCTURE, FAIL,
                   "No risks or bear-case section. A report without a bear case "
                   "is a marketing document.")


def check_invalidation(lines: List[str], text: str) -> Finding:
    """Thesis-invalidation triggers (recommended -> warn if absent)."""
    if is_forensic_report(text):
        return Finding("thesis-invalidation", GROUP_STRUCTURE, SKIP,
                       "Forensic review: thesis-invalidation triggers are a "
                       "Standard-mode construct; a forensic verdict rests on "
                       "evidence and a 'what was not verified' section instead.")
    hit = _first_match(
        lines,
        r"invalidat|thesis[- ]?invalidat|invalidation trigger|"
        r"what would change (?:the |my )|change (?:my mind|the verdict|the thesis)|"
        r"what would (?:it take|break|settle|move)|settle the argument|"
        r"\bmonitorables?\b|\bsignposts?\b|what to watch|would break (?:the |this )?thesis")
    if hit:
        return Finding("thesis-invalidation", GROUP_STRUCTURE, PASS,
                       "Thesis-invalidation / change-my-mind triggers found.",
                       hit[0], clip(strip_md(hit[1])))
    return Finding("thesis-invalidation", GROUP_STRUCTURE, WARN,
                   "No thesis-invalidation triggers. Add specific, observable, "
                   "time-bound conditions that would break the thesis "
                   "(recommended, not mandatory).")


def check_disclaimer(lines: List[str], text: str) -> Finding:
    """Not-financial-advice disclaimer (research, not personalised advice)."""
    hit = _first_match(
        lines,
        r"not (?:investment|financial) advice|not a recommendation|"
        r"informational purposes only|not a licensed|not a registered|"
        r"not licensed|not personalised|not personalized|research,? not advice|"
        r"not an allegation of wrongdoing|"
        r"consult (?:a|your) (?:licensed )?(?:financial )?advis")
    if hit:
        return Finding("disclaimer", GROUP_STRUCTURE, PASS,
                       "Not-financial-advice disclaimer found.",
                       hit[0], clip(strip_md(hit[1])))
    return Finding("disclaimer", GROUP_STRUCTURE, FAIL,
                   "No not-financial-advice disclaimer. The output must state it "
                   "is research, not personalised investment advice.")


def check_scorecard_gates(lines: List[str], text: str) -> Finding:
    """If a composite/scorecard is shown, gates must be disclosed."""
    scorecard = _first_match(
        lines, r"\bcomposite score\b|\bscorecard\b|composite\b.{0,12}/\s?10|\bweighted\b.*\bscore\b")
    if not scorecard:
        return Finding("scorecard-gates", GROUP_STRUCTURE, SKIP,
                       "No scorecard / composite shown; gate disclosure not required.")
    gate = _first_match(
        lines,
        r"\bgates?\b|gate check|disqualif|gate:\s*(?:none|checked|not checked)|"
        r"no gate (?:was )?(?:raised|triggered)")
    if gate:
        return Finding("scorecard-gates", GROUP_STRUCTURE, PASS,
                       "Scorecard shown and gate status disclosed.",
                       gate[0], clip(strip_md(gate[1])))
    return Finding("scorecard-gates", GROUP_STRUCTURE, WARN,
                   "A composite / scorecard is shown but no disqualifying-gate "
                   "disclosure. State 'gates: none / checked / not checked' -- a "
                   "score without gate disclosure can launder a failing name.",
                   scorecard[0], clip(strip_md(scorecard[1])))


# ---------------------------------------------------------------------------
# Hygiene checks
# ---------------------------------------------------------------------------

_PLACEHOLDER_TOKENS = re.compile(
    r"\bTODO\b|\bTBD\b|\bFIXME\b|\bXXX+\b|lorem ipsum|"
    r"\bYYYY\b|\bDD-MMM\b|\bMMM-YYYY\b|\bDD-MMM-YYYY\b|"
    r"\bXX%|\bX,XXX\b|\[X\.X|\[XX%\]|\[X\]",
    re.IGNORECASE,
)

# A small set of real HTML tags we should NOT treat as leaked <placeholders>.
_HTML_TAGS = {
    "br", "hr", "b", "i", "u", "em", "strong", "sub", "sup", "code", "small",
    "kbd", "mark", "span", "div", "p", "ul", "ol", "li", "table", "tr", "td",
    "th", "thead", "tbody", "a", "img", "pre", "blockquote", "details", "summary",
}


def _strip_code_spans(line: str) -> str:
    """Blank out inline `code` spans so their contents are not scanned.

    Angle-bracket notation inside a code span (e.g. `score.py <that file>`) is
    conventional CLI-argument syntax shown to the reader, not a leaked template
    field, so it must not be flagged as placeholder leakage.
    """
    return re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line)


def _angle_placeholders(lines: List[str]) -> List[Tuple[int, str]]:
    """Find leaked <angle-bracket> template fields, skipping real HTML/autolinks."""
    out = []
    for idx, line in enumerate(lines, start=1):
        scan = _strip_code_spans(line)
        for m in re.finditer(r"<([^<>\n]{1,80})>", scan):
            inner = m.group(1).strip()
            if not inner or "://" in inner or "@" in inner:
                continue  # autolink or email-ish
            first = inner.strip("/").split()[0].lower() if inner.strip("/") else ""
            if first in _HTML_TAGS and len(inner.split()) == 1:
                continue  # a plain HTML tag like <br> or <div>
            out.append((idx, m.group(0)))
    return out


def check_placeholders(lines: List[str], text: str) -> Finding:
    """Placeholder / template leakage -- unacceptable in a finished report."""
    hits: List[Tuple[int, str]] = []
    for idx, line in enumerate(lines, start=1):
        for m in _PLACEHOLDER_TOKENS.finditer(_strip_code_spans(line)):
            hits.append((idx, m.group(0)))
    hits.extend(_angle_placeholders(lines))
    hits.sort()
    if not hits:
        return Finding("placeholder-leakage", GROUP_HYGIENE, PASS,
                       "No placeholder or unfilled template fields found.")
    details = ["line %d: %s" % (ln, clip(tok, 60)) for ln, tok in hits[:12]]
    return Finding("placeholder-leakage", GROUP_HYGIENE, FAIL,
                   "%d placeholder / unfilled template field(s) left in the "
                   "report." % len(hits), hits[0][0], details=details)


def _split_cells(line: str) -> List[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


# Row labels that legitimately leave value cells blank: aggregate/operator rows
# in a financial build (a "= ROE" ratio row carries no rupee amount, a
# "Composite" row carries no per-category score).
_AGG_LABEL_RE = re.compile(r"^\s*(?:[=×x+*/−–-]|composite|total|sub-?total|weighted)\b",
                           re.IGNORECASE)


def check_blank_cells(lines: List[str], text: str) -> Finding:
    """INFO: blank cells in otherwise-numeric columns, where a figure looks implied.

    Reported as INFO, not a grade-affecting warning, on purpose: a rigorous
    multi-step build (DuPont, SOTP) legitimately blanks the rupee column on a
    ratio row and the commentary column on a data row. A linter cannot reliably
    tell an intentional layout blank from a dropped value, so it surfaces the
    candidates for a human glance rather than penalising the report. The genuine
    fix the skill wants -- 'n/a with a reason' instead of an empty cell -- is
    something the reviewer confirms.
    """
    suspicious: List[str] = []
    count = 0
    n = len(lines)
    i = 0
    while i < n:
        if not is_table_row(lines[i]):
            i += 1
            continue
        start = i
        while i < n and is_table_row(lines[i]):
            i += 1
        # Grid of data rows (skip separators); track original line numbers.
        rows = [(k + 1, _split_cells(lines[k]))
                for k in range(start, i)
                if not is_table_separator(lines[k])]
        if len(rows) < 3:  # header + at least two data rows
            continue
        data_rows = rows[1:]  # drop the header
        ncols = max((len(c) for _, c in data_rows), default=0)
        # Which columns are predominantly numeric across data rows?
        numeric_col = []
        for col in range(ncols):
            filled = num = 0
            for _, cells in data_rows:
                if col < len(cells) and cells[col] != "":
                    filled += 1
                    if FIGURE_RE.search(cells[col]):
                        num += 1
            numeric_col.append(filled >= 2 and num >= 0.6 * filled)
        for ln, cells in data_rows:
            label = cells[0] if cells else ""
            if _AGG_LABEL_RE.match(label):
                continue  # operator / aggregate row: blanks are structural
            for col in range(1, ncols):
                if numeric_col[col] and (col >= len(cells) or cells[col] == ""):
                    count += 1
                    if len(suspicious) < 8:
                        suspicious.append("line %d: %s" % (ln, clip(strip_md(lines[ln - 1]), 80)))
                    break
    if count == 0:
        return Finding("blank-cells", GROUP_HYGIENE, INFO,
                       "No suspicious blank cells in numeric table columns.")
    return Finding("blank-cells", GROUP_HYGIENE, INFO,
                   "%d blank cell(s) sit in otherwise-numeric columns and may be "
                   "dropped values -- prefer 'n/a (reason)' over an empty cell. "
                   "Review: some may be intentional layout blanks." % count,
                   details=suspicious)


def check_na_declarations(lines: List[str], text: str) -> Finding:
    """Info: count explicit not-available declarations (good practice)."""
    matches = re.findall(
        r"\bn/a\b|\bn\.a\.\b|\bn/d\b|not available|not disclosed|not comparable|"
        r"not applicable|not sourced|not yet determined|undefined for sector",
        text, re.IGNORECASE)
    n = len(matches)
    if n == 0:
        return Finding("na-declarations", GROUP_HYGIENE, INFO,
                       "No explicit 'not available / n/a' declarations found. If "
                       "anything is missing, say so explicitly rather than "
                       "leaving it out.")
    return Finding("na-declarations", GROUP_HYGIENE, INFO,
                   "%d explicit 'not available / n/a / undefined' declaration(s) "
                   "-- good: gaps are disclosed rather than hidden." % n)


# Imperative, personalised trade instructions. These are the boundary breach.
# Neutral valuation ranges, target prices, and stated bull/bear cases are NOT
# matched -- context makes those legitimate research, so this is a warn.
_ADVICE_RE = re.compile(
    r"\byou\s+(?:should|must|need to|ought to)\s+(?:buy|sell|hold|avoid|purchase|"
    r"invest|allocate|exit|dump|short|book (?:profits?|gains?))\b"
    r"|\b(?:buy|sell|short)\s+now\b"
    r"|\ballocate\s+\d+\s?%"
    r"|\bput\s+\d+\s?%?\s+of your\b"
    r"|\b(?:buy|sell)\s+\d[\d,]*\s+shares?\b"
    r"|\b(?:i|we)\s+(?:recommend|advise|suggest)\s+(?:you\s+)?(?:buy|sell|hold|exit)\b"
    r"|\bmy recommendation is (?:to )?(?:buy|sell|hold)\b"
    r"|\b(?:load up|back up the truck)\b",
    re.IGNORECASE,
)


def check_advice_boundary(lines: List[str], text: str) -> Finding:
    """Flag imperative personalised trade instructions (possible boundary breach)."""
    hits: List[Tuple[int, str]] = []
    for idx, line in enumerate(lines, start=1):
        for m in _ADVICE_RE.finditer(line):
            hits.append((idx, m.group(0)))
    if not hits:
        return Finding("advice-boundary", GROUP_HYGIENE, PASS,
                       "No imperative personalised trade instructions detected.")
    details = ["line %d: \"%s\"" % (ln, clip(tok, 60)) for ln, tok in hits[:10]]
    return Finding("advice-boundary", GROUP_HYGIENE, WARN,
                   "%d phrase(s) read as personalised buy/sell instructions. This "
                   "skill outputs research, not advice. Re-cast as a neutral "
                   "valuation range or a stated bull/bear case (context matters, "
                   "so review each)." % len(hits), hits[0][0], details=details)


# ---------------------------------------------------------------------------
# Optional template cross-reference
# ---------------------------------------------------------------------------

_STOPWORDS = {
    "the", "and", "for", "with", "what", "how", "its", "makes", "money", "sells",
    "applied", "used", "instead", "this", "that", "into", "from", "your", "vs",
    "each", "shows", "them", "who", "why", "sub", "per",
}


def check_template_sections(lines: List[str], text: str,
                            template_text: str) -> Optional[Finding]:
    """INFO: template `##` sections with no obvious counterpart in the report.

    Supplied only when --template is passed. Conservative on purpose: a section
    is treated as present if at least half of its distinctive words appear
    anywhere in the report (not necessarily as a heading), so a renamed or
    reordered section is not falsely reported missing. It never affects the
    grade -- it is a coverage hint, catching sections the semantic checks above
    do not cover (e.g. Peer Comparison, Valuation).
    """
    report_lc = text.lower()
    missing: List[str] = []
    seen = set()
    in_fence = False
    for line in template_text.splitlines():
        # The actual report structure lives inside the template's fenced code
        # block(s); headings outside the fence (Contents, Non-negotiables,
        # Formatting conventions, Checklist) document the template itself and
        # are not report sections, so only cross-reference inside fences.
        if re.match(r"\s*`{3,}", line):
            in_fence = not in_fence
            continue
        if not in_fence:
            continue
        m = re.match(r"##\s+(.*)", line)  # level-2 sections only, not the title
        if not m:
            continue
        title = re.sub(r"^[\d.\s]+", "", m.group(1)).strip()
        if title.lower() in seen:
            continue
        seen.add(title.lower())
        words = [w for w in re.findall(r"[A-Za-z][A-Za-z-]{2,}", title.lower())
                 if w not in _STOPWORDS]
        if not words:
            continue
        present = sum(1 for w in words if w in report_lc)
        if present < max(1, (len(words) + 1) // 2):
            missing.append(title)
    if not missing:
        return Finding("template-coverage", GROUP_STRUCTURE, INFO,
                       "All template sections have an apparent counterpart in the "
                       "report.")
    return Finding("template-coverage", GROUP_STRUCTURE, INFO,
                   "%d template section(s) have no obvious counterpart (may be "
                   "renamed, merged, or genuinely absent -- review): %s"
                   % (len(missing), "; ".join(missing[:10])))


# ---------------------------------------------------------------------------
# Figure-sourcing finding
# ---------------------------------------------------------------------------

WARN_THRESHOLD = 0.60
ERROR_THRESHOLD = 0.35


# ---------------------------------------------------------------------------
# Aggregator-only sourcing (documents primary, aggregators navigation-only)
# ---------------------------------------------------------------------------
# The skill's rule is that a figure may be *cross-checked* against an aggregator
# but must be *sourced* from a filing. A figure whose only nearby provenance cue
# is an aggregator (screener/tickertape/yahoo...) with no filing/report/
# transcript cue in the same window is exactly the defect this catches: it looks
# sourced to the ratio check above, yet nothing traces to a document.

_AGG_CITE_RE = re.compile(
    r"screener|tikr|tijori|trendlyne|tickertape|moneycontrol|"
    r"yahoo\s*finance|google\s*finance|marketsmojo|investing\.com|stockanalysis|"
    r"morningstar|simplywall|value\s*research|valueresearch|equitymaster|"
    r"wikipedia|5paisa|\bgroww\b|marketscreener",
    re.IGNORECASE,
)
# A cue that denotes an actual primary/company document. If one of these sits in
# the same window as an aggregator mention, the figure is treated as document-
# sourced-and-merely-cross-checked (the sanctioned use), so it is NOT flagged.
_PRIMARY_CITE_RE = re.compile(
    r"annual report|\bAR\b|10-?k|10-?q|20-?f|8-?k|quarterly results|"
    r"results filing|results intimation|financial statements?|balance sheet|"
    r"cash ?flow statement|prospectus|drhp|rhp|red herring|exchange filing|"
    r"regulation ?30|\bcaro\b|con-?call|concall|\btranscript\b|"
    r"investor presentation|earnings (?:call|release|presentation|deck)|"
    r"press release|rating rationale|crisil|icra|care ratings|india ratings|"
    r"\bp\.?\s?\d|\bpp\.?\s?\d|page\s?\d|note\s?\d|item\s?\d|filing|filed",
    re.IGNORECASE,
)
# Windows about price / market cap are the sanctioned exchange-sourced exception.
_PRICE_CTX_RE = re.compile(
    r"\bprice\b|market\s*cap|mcap|market capitalis|52-?week|"
    r"enterprise value|\bclose\b",
    re.IGNORECASE,
)


def analyse_aggregator_only(lines: List[str], max_samples: int = 10
                            ) -> Tuple[int, List[Tuple[int, str]]]:
    """Count figures whose only nearby provenance cue is an aggregator."""
    hits: List[Tuple[int, str]] = []
    count = 0
    for line_no, unit in iter_units(lines):
        if _CONVERSION_RE.match(unit):
            continue
        if not find_figures(unit):
            continue
        if not _AGG_CITE_RE.search(unit):
            continue
        if _PRIMARY_CITE_RE.search(unit) or _PRICE_CTX_RE.search(unit):
            continue
        count += 1
        if len(hits) < max_samples:
            hits.append((line_no, clip(strip_md(unit), 88)))
    return count, hits


def aggregator_finding(lines: List[str]) -> Optional[Finding]:
    """WARN when figures are cited only to an aggregator, with no filing cue."""
    count, samples = analyse_aggregator_only(lines)
    if count == 0:
        return Finding("aggregator-sourcing", GROUP_SOURCING, PASS,
                       "No figures appear cited only to an aggregator.")
    details = ["line %d: %s" % (ln, txt) for ln, txt in samples]
    return Finding("aggregator-sourcing", GROUP_SOURCING, WARN,
                   "%d figure(s) are cited only to an aggregator "
                   "(screener/tickertape/yahoo...) with no filing cue in the same "
                   "line. Aggregators are navigation aids, not a source of record: "
                   "trace each to the annual report / exchange filing, or mark it "
                   "as a labelled cross-check beside the document figure. "
                   "(Price/market cap is exempt.)" % count,
                   samples[0][0] if samples else None, details=details)


def sourcing_finding(res: SourcingResult) -> Finding:
    if res.total == 0:
        return Finding("figure-sourcing", GROUP_SOURCING, INFO,
                       "No financial figures detected to check.",
                       extra={"total": 0, "cued": 0, "ratio": None})
    pct = round(res.ratio * 100, 1)
    base = ("%d%% of %d financial figures sit near a provenance cue (page, "
            "filing, period label, URL, 'as of', ...). HEURISTIC: this is a "
            "prompt to review, not proof of sourcing or fabrication." % (pct, res.total))
    extra = {
        "total": res.total,
        "cued": res.cued,
        "ratio": round(res.ratio, 4),
        "warn_threshold": WARN_THRESHOLD,
        "error_threshold": ERROR_THRESHOLD,
        "bare_samples": [{"line": ln, "text": txt} for ln, txt in res.bare_samples],
    }
    details = ["line %d: %s" % (ln, txt) for ln, txt in res.bare_samples]
    if res.ratio < ERROR_THRESHOLD:
        status, note = FAIL, (" Below %.0f%% -- the report looks largely "
                              "un-sourced and figures may be fabricated; verify "
                              "before delivery." % (ERROR_THRESHOLD * 100))
    elif res.ratio < WARN_THRESHOLD:
        status, note = WARN, (" Below %.0f%% -- too many bare figures; add "
                              "inline sources." % (WARN_THRESHOLD * 100))
    else:
        status, note = PASS, " At or above the 60%% target."
    return Finding("figure-sourcing", GROUP_SOURCING, status, base + note,
                   details=details, extra=extra)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

STRUCTURAL_CHECKS = [
    check_recency,
    check_data_quality,
    check_reporting_basis,
    check_currency_units,
    check_verdict,
    check_risks_bear,
    check_invalidation,
    check_disclaimer,
    check_scorecard_gates,
]

HYGIENE_CHECKS = [
    check_placeholders,
    check_blank_cells,
    check_na_declarations,
    check_advice_boundary,
]


def run_checks(text: str, template_text: Optional[str] = None) -> List[Finding]:
    lines = text.splitlines()
    findings: List[Finding] = []
    for fn in STRUCTURAL_CHECKS:
        findings.append(fn(lines, text))
    if template_text:
        tmpl_finding = check_template_sections(lines, text, template_text)
        if tmpl_finding is not None:
            findings.append(tmpl_finding)
    findings.append(sourcing_finding(analyse_sourcing(lines)))
    agg_finding = aggregator_finding(lines)
    if agg_finding is not None:
        findings.append(agg_finding)
    for fn in HYGIENE_CHECKS:
        findings.append(fn(lines, text))
    return findings


def grade(findings: List[Finding], strict: bool) -> Tuple[str, dict]:
    """Compute overall grade + counts. In strict mode, warnings become errors."""
    counts = {"error": 0, "warn": 0, "info": 0, "pass": 0, "skip": 0}
    for f in findings:
        status = f.status
        if strict and status == WARN:
            status = FAIL
        if status == FAIL:
            counts["error"] += 1
        elif status == WARN:
            counts["warn"] += 1
        elif status == INFO:
            counts["info"] += 1
        elif status == PASS:
            counts["pass"] += 1
        elif status == SKIP:
            counts["skip"] += 1
    if counts["error"]:
        overall = "FAIL"
    elif counts["warn"]:
        overall = "PASS-WITH-WARNINGS"
    else:
        overall = "PASS"
    return overall, counts


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

_STATUS_TAG = {PASS: "PASS", WARN: "WARN", FAIL: "FAIL", INFO: "INFO", SKIP: "SKIP"}


def render_text(path: str, findings: List[Finding], overall: str,
                counts: dict, strict: bool) -> str:
    width = 64
    lines = []
    lines.append("FINISHED-REPORT LINT  --  " + path)
    lines.append("=" * width)
    if strict:
        lines.append("(strict mode: warnings are treated as errors)")
        lines.append("")

    for group in GROUP_ORDER:
        group_findings = [f for f in findings if f.group == group]
        if not group_findings:
            continue
        lines.append(group)
        lines.append("-" * width)
        for f in group_findings:
            tag = _STATUS_TAG.get(f.status, f.status)
            loc = (" (line %d)" % f.line) if f.line else ""
            lines.append("  [%s] %-20s %s" % (tag, f.id, ""))
            lines.append("         %s%s" % (clip(f.message, 300), loc))
            if f.snippet:
                lines.append("         > %s" % clip(f.snippet, 92))
            for d in f.details:
                lines.append("             - %s" % clip(d, 96))
        lines.append("")

    lines.append("-" * width)
    lines.append("OVERALL: %s" % overall)
    lines.append("  errors: %d   warnings: %d   info: %d   pass: %d"
                 % (counts["error"], counts["warn"], counts["info"], counts["pass"]))
    return "\n".join(lines)


def render_json(path: str, findings: List[Finding], overall: str,
                counts: dict, strict: bool) -> str:
    payload = {
        "report": path,
        "strict": strict,
        "grade": overall,
        "counts": counts,
        "findings": [f.to_dict() for f in findings],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def read_report(path: str) -> Tuple[Optional[str], Optional[str]]:
    """Return (text, error). Graceful on missing / unreadable / empty files."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except FileNotFoundError:
        return None, "file not found: %s" % path
    except IsADirectoryError:
        return None, "path is a directory, not a file: %s" % path
    except OSError as exc:
        return None, "could not read %s: %s" % (path, exc)
    return text, None


def _make_output_safe() -> None:
    """Best-effort UTF-8 stdout so report content (₹, ×, en-dashes) never crashes.

    Windows consoles default to a legacy codepage (cp1252) that cannot encode
    the currency and typographic characters common in these reports. Reconfigure
    where possible; fall back to replacement so the linter never dies mid-print.
    """
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (ValueError, OSError):
                pass


def main(argv: Optional[List[str]] = None) -> int:
    _make_output_safe()
    parser = argparse.ArgumentParser(
        prog="lint_report.py",
        description="Mechanical QA lint for a finished stock-analysis markdown "
                    "report (structure, figure sourcing, hygiene).",
    )
    parser.add_argument("report", help="path to the finished markdown report")
    parser.add_argument("--json", action="store_true",
                        help="emit structured JSON instead of the checklist")
    parser.add_argument("--strict", action="store_true",
                        help="promote warnings to errors (fail on any warning)")
    parser.add_argument("--template", default=None,
                        help="optional path to the report template; adds an "
                             "INFO-only section-coverage cross-reference")
    args = parser.parse_args(argv)

    text, err = read_report(args.report)
    if err is not None:
        print("lint_report: %s" % err, file=sys.stderr)
        return 2

    if not text or not text.strip():
        # Empty report: report a single hard failure, still exit gracefully.
        empty = Finding("empty-report", GROUP_STRUCTURE, FAIL,
                        "Report file is empty -- nothing to lint.")
        overall, counts = grade([empty], args.strict)
        if args.json:
            print(render_json(args.report, [empty], overall, counts, args.strict))
        else:
            print(render_text(args.report, [empty], overall, counts, args.strict))
        return 1

    template_text = None
    if args.template:
        template_text, terr = read_report(args.template)
        if terr is not None:
            print("lint_report: --template ignored (%s)" % terr, file=sys.stderr)
            template_text = None

    findings = run_checks(text, template_text)
    overall, counts = grade(findings, args.strict)

    if args.json:
        print(render_json(args.report, findings, overall, counts, args.strict))
    else:
        print(render_text(args.report, findings, overall, counts, args.strict))

    return 1 if overall == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
