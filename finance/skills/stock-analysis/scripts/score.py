#!/usr/bin/env python3
"""Sector-relative, multi-factor scoring for the stock-analysis skill.

A metric value carries no meaning until you know the sector it came from and the
company's own history. This script encodes that: every metric is scored against
its own sector's benchmark band, against the company's own history, or against a
supplied peer set -- never against a universal absolute. A 20% operating margin in
distribution can and should outscore a 30% margin in software.

The composite is built from eight weighted CATEGORIES, not from a flat average of
metrics, so no single ratio can dominate. Disqualifying findings (going-concern
doubt, auditor qualification, heavy promoter pledging, sustained cash-vs-profit
divergence) are handled by GATES that cap or veto the composite, because averaging
a fraud signal against a good ROCE produces a number that is worse than no number.

Standard library only. Python 3.8+.

--------------------------------------------------------------------------------
USAGE
--------------------------------------------------------------------------------
    python score.py input.json                 # readable scorecard
    python score.py input.json --json          # machine-readable, same numbers
    python score.py --list-sectors             # available sector keys
    python score.py --explain                  # how the method works
    python score.py --explain roce_pct --sector fmcg-consumer
    python score.py --example > input.json     # write a starter input file
    python score.py input.json --preset deep_value
    python score.py input.json --weight valuation=0.20 --weight risk=0.10
    python score.py --example-segments > seg.json   # multi-segment starter file
    python score.py seg.json --weight-basis ebit --segment-detail

--------------------------------------------------------------------------------
MULTI-SEGMENT INPUT
--------------------------------------------------------------------------------
A company that is 55% EPC, 30% IT services and 15% lending has no single correct
sector key, and scoring all of it against one set of bands is wrong for 45% of the
profit. Add a top-level "segments" array and each segment is scored against ITS OWN
sector, then blended by EBIT (or capital employed, revenue, or explicit weights):

{
  "company": "...", "as_of": "2026-07-22", "basis": "consolidated",
  "weight_basis": "ebit",
  "flags": ["<group-level gate ids>"],
  "segments": [
    {"name": "EPC", "sector": "infra-capitalgoods", "ebit": 12000,
     "capital_employed": 60000, "revenue": 150000,
     "metrics": {...}, "flags": ["<segment-level gate ids>"]}
  ]
}

The array is auto-detected; without it the single-sector behaviour is unchanged.
A blended composite is a quality summary, never a substitute for sum-of-the-parts
valuation -- see the diagnostics the segmented renderer prints.

--------------------------------------------------------------------------------
EXAMPLE INPUT (a distributor: thin margin, high turnover, negative working capital)
--------------------------------------------------------------------------------
{
  "company": "Example Distribution Ltd",
  "ticker": "NSE:EXAMPLED",
  "as_of": "2026-07-22",
  "basis": "consolidated",
  "currency": "INR",
  "sector": "retail-ecommerce",
  "metrics": {
    "opm_pct":            {"value": 4.2,  "source": "FY25 AR, consolidated", "period": "FY25"},
    "roce_pct":           {"value": 26.0, "source": "computed, EBIT/(net debt+equity+leases)"},
    "roic_wacc_spread_pp": 12.0,
    "cash_conversion_cycle_days": {"value": -18, "note": "Suppliers fund inventory; terms verified in AR note 14"},
    "cfo_to_pat_3y":      {"value": 1.05, "source": "FY23-FY25 cash flow statements"},
    "fcf_margin_pct":     1.9,
    "sssg_pct":           {"value": 9.0,  "peer_values": [3.0, 4.5, 6.0, 11.0]},
    "store_payback_years": 2.2,
    "net_debt_to_ebitda": {"value": 0.4,  "own_history": [1.8, 1.4, 1.1, 0.7], "basis": "own_history"},
    "promoter_pledge_pct": 0,
    "capital_allocation_score": {"value": 7.0, "note": "Exited two loss-making formats in FY23; no equity raised since FY21"},
    "moat_width_score":   {"value": 6.5, "note": "Density advantage in 3 states; share gains 4 straight years"},
    "pe_x":               31.0,
    "reverse_dcf_growth_gap_pp": 1.5
  },
  "flags": {
    "receivables_blowout": {"present": false}
  },
  "overrides": {
    "category_weights": {"valuation": 0.14, "risk": 0.06},
    "thresholds": {"opm_pct": {"poor": 1.5, "average": 3.0, "good": 5.0, "excellent": 8.0}},
    "note": "Thresholds narrowed to the Indian organised-distribution peer set, FY25."
  }
}

Anything you cannot source is simply left out. Missing metrics are dropped and the
remaining category weights renormalised -- a missing number is never scored as a
bad number -- but coverage is reported, and below the coverage floor the composite
is emitted as INDICATIVE ONLY rather than as a confident score.
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
from typing import Any, Dict, List, Optional, Sequence, Tuple

try:  # keep non-ASCII notes from the benchmark file printable on Windows consoles
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:  # pragma: no cover - older interpreters or redirected streams
    pass

DEFAULT_BENCHMARKS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "benchmarks.json")

ANCHOR_POOR = 2.5
ANCHOR_AVERAGE = 5.0
ANCHOR_GOOD = 7.5
ANCHOR_EXCELLENT = 10.0

GRADES: Sequence[Tuple[float, str]] = (
    (8.5, "Exceptional"),
    (7.5, "Strong"),
    (6.5, "Above average"),
    (5.5, "Average"),
    (4.5, "Below average"),
    (3.5, "Weak"),
    (0.0, "Poor"),
)


class ScoringError(Exception):
    """Raised for malformed benchmarks or input that cannot be scored."""


# ---------------------------------------------------------------------------
# Loading and sector resolution
# ---------------------------------------------------------------------------

def load_benchmarks(path: str) -> Dict[str, Any]:
    """Load the benchmark file and check the structural invariants we rely on."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        raise ScoringError("benchmark file not found: %s" % path)
    except json.JSONDecodeError as exc:
        raise ScoringError("benchmark file is not valid JSON (%s): %s" % (path, exc))
    for required in ("_category_weights", "_categories", "generic"):
        if required not in data:
            raise ScoringError("benchmark file is missing the '%s' block" % required)
    return data


def sector_keys(bm: Dict[str, Any]) -> List[str]:
    """Return the sector keys, excluding the underscore-prefixed metadata blocks."""
    return sorted(k for k in bm if not k.startswith("_"))


def resolve_sector(bm: Dict[str, Any], sector: Optional[str]) -> Tuple[str, Dict[str, Any], List[str]]:
    """Resolve a sector key to a fully merged metric set.

    Follows the ``extends`` chain (sector metrics deep-merge onto the parent's, so a
    sector can override only the thresholds it disagrees with), applies ``disable``,
    and falls back to ``generic`` with a warning when the key is unknown.
    """
    warnings: List[str] = []
    key = (sector or "generic").strip().lower()
    if key not in bm or key.startswith("_"):
        warnings.append(
            "unknown sector '%s' -- falling back to the generic metric set. "
            "The generic set is NOT valid for banks, NBFCs, insurers or REITs; "
            "for those, pass the right sector key or the scores will be meaningless."
            % (sector or "")
        )
        key = "generic"

    chain: List[str] = []
    cursor: Optional[str] = key
    seen = set()
    while cursor:
        if cursor in seen:
            raise ScoringError("circular 'extends' chain at sector '%s'" % cursor)
        seen.add(cursor)
        if cursor not in bm:
            raise ScoringError("sector '%s' extends missing sector '%s'" % (key, cursor))
        chain.append(cursor)
        cursor = bm[cursor].get("extends")
    chain.reverse()  # parents first

    metrics: Dict[str, Dict[str, Any]] = {}
    category_weights = dict(bm["_category_weights"])
    label = key
    notes = ""
    disabled: List[str] = []
    for name in chain:
        node = bm[name]
        for mkey, spec in node.get("metrics", {}).items():
            if mkey in metrics:
                merged = dict(metrics[mkey])
                merged.update(spec)  # partial override: thresholds/weight/note only
                metrics[mkey] = merged
            else:
                metrics[mkey] = dict(spec)
        for mkey in node.get("disable", []):
            disabled.append(mkey)
        if node.get("category_weights"):
            category_weights = dict(node["category_weights"])
        label = node.get("label", name)
        notes = node.get("notes", notes)

    for mkey in disabled:
        metrics.pop(mkey, None)

    for mkey, spec in metrics.items():
        if "category" not in spec or "direction" not in spec:
            raise ScoringError(
                "metric '%s' in sector '%s' is incomplete: a metric introduced by a "
                "sector needs at least 'label', 'category' and 'direction'." % (mkey, key)
            )
        spec.setdefault("label", mkey)
        spec.setdefault("weight", 1.0)

    resolved = {
        "key": key,
        "label": label,
        "notes": notes,
        "metrics": metrics,
        "category_weights": category_weights,
        "chain": chain,
    }
    return key, resolved, warnings


# ---------------------------------------------------------------------------
# Metric scoring
# ---------------------------------------------------------------------------

def _dedupe_ascending(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """Collapse duplicate x-values (keeping the highest score) and sort ascending."""
    merged: Dict[float, float] = {}
    for x, y in points:
        x = float(x)
        merged[x] = max(y, merged.get(x, y))
    return sorted(merged.items())


def build_anchor_points(direction: str, thresholds: Dict[str, Any]) -> List[Tuple[float, float]]:
    """Turn poor/average/good/excellent thresholds into an interpolation curve.

    higher_better / lower_better expect scalars; band expects [low, high] pairs.
    The curve anchors poor=2.5, average=5.0, good=7.5, excellent=10.0, clamps at 10
    beyond 'excellent', and falls linearly to 0 one band-width beyond 'poor'.
    """
    need = ("poor", "average", "good", "excellent")
    for k in need:
        if k not in thresholds:
            raise ScoringError("thresholds are missing '%s'" % k)

    if direction in ("higher_better", "lower_better"):
        p, a, g, e = (float(thresholds[k]) for k in need)
        if direction == "higher_better":
            if not (p < a < g < e):
                raise ScoringError("higher_better thresholds must ascend: poor<average<good<excellent")
            floor_x = p - (a - p)
            pts = [(floor_x, 0.0), (p, ANCHOR_POOR), (a, ANCHOR_AVERAGE), (g, ANCHOR_GOOD), (e, ANCHOR_EXCELLENT)]
        else:
            if not (p > a > g > e):
                raise ScoringError("lower_better thresholds must descend: poor>average>good>excellent")
            floor_x = p + (p - a)
            pts = [(e, ANCHOR_EXCELLENT), (g, ANCHOR_GOOD), (a, ANCHOR_AVERAGE), (p, ANCHOR_POOR), (floor_x, 0.0)]
        return _dedupe_ascending(pts)

    if direction == "band":
        try:
            p_lo, p_hi = (float(v) for v in thresholds["poor"])
            a_lo, a_hi = (float(v) for v in thresholds["average"])
            g_lo, g_hi = (float(v) for v in thresholds["good"])
            e_lo, e_hi = (float(v) for v in thresholds["excellent"])
        except (TypeError, ValueError):
            raise ScoringError("band thresholds must each be a [low, high] pair")
        if not (p_lo <= a_lo <= g_lo <= e_lo <= e_hi <= g_hi <= a_hi <= p_hi):
            raise ScoringError("band thresholds must be nested: poor contains average contains good contains excellent")
        taper = max((p_hi - p_lo) * 0.25, 1e-9)
        pts = [
            (p_lo - taper, 0.0), (p_lo, ANCHOR_POOR), (a_lo, ANCHOR_AVERAGE), (g_lo, ANCHOR_GOOD),
            (e_lo, ANCHOR_EXCELLENT), (e_hi, ANCHOR_EXCELLENT),
            (g_hi, ANCHOR_GOOD), (a_hi, ANCHOR_AVERAGE), (p_hi, ANCHOR_POOR), (p_hi + taper, 0.0),
        ]
        return _dedupe_ascending(pts)

    raise ScoringError("unsupported direction '%s'" % direction)


def interpolate(value: float, points: Sequence[Tuple[float, float]]) -> float:
    """Piecewise-linear lookup with clamping at both ends of the curve."""
    if value <= points[0][0]:
        return points[0][1]
    if value >= points[-1][0]:
        return points[-1][1]
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        if x0 <= value <= x1:
            if x1 == x0:
                return max(y0, y1)
            frac = (value - x0) / (x1 - x0)
            return y0 + frac * (y1 - y0)
    return points[-1][1]  # pragma: no cover - unreachable given the clamps


def own_history_thresholds(direction: str, history: Sequence[float]) -> Optional[Dict[str, float]]:
    """Derive thresholds from the company's own median: the company as its own control.

    Anchors are multiples of the own-history median: 0.85 / 1.00 / 1.15 / 1.30 for
    higher_better, inverted for lower_better. Use this when the peer set is weak but
    the company has a long, comparable record -- it answers "is this company getting
    better or worse", which no cross-sectional band can.
    """
    clean = [float(v) for v in history if isinstance(v, (int, float))]
    if len(clean) < 3:
        return None
    median = statistics.median(clean)
    if median <= 0:
        return None
    if direction == "higher_better":
        return {"poor": 0.85 * median, "average": median, "good": 1.15 * median, "excellent": 1.30 * median}
    if direction == "lower_better":
        return {"poor": 1.15 * median, "average": median, "good": 0.85 * median, "excellent": 0.70 * median}
    return None


def peer_percentile(value: float, peers: Sequence[float], direction: str) -> Optional[float]:
    """Fraction of the peer set the company beats, 0..1, direction aware."""
    clean = [float(v) for v in peers if isinstance(v, (int, float))]
    if len(clean) < 3:
        return None
    if direction == "higher_better":
        wins = sum(1.0 for v in clean if value > v) + 0.5 * sum(1.0 for v in clean if value == v)
    elif direction == "lower_better":
        wins = sum(1.0 for v in clean if value < v) + 0.5 * sum(1.0 for v in clean if value == v)
    else:
        return None
    return wins / len(clean)


def _describe_band(direction: str, thresholds: Dict[str, Any]) -> str:
    """One-line rendering of the band actually used, so a reader can dispute it."""
    def fmt(v: Any) -> str:
        if isinstance(v, (list, tuple)):
            return "[%s, %s]" % (_num(v[0]), _num(v[1]))
        return _num(v)
    if direction == "judgement":
        return "analyst 0-10"
    return "%s / %s / %s / %s" % (
        fmt(thresholds["poor"]), fmt(thresholds["average"]),
        fmt(thresholds["good"]), fmt(thresholds["excellent"]),
    )


def _num(v: Any) -> str:
    if isinstance(v, float):
        if abs(v - round(v)) < 1e-9:
            return str(int(round(v)))
        return ("%.2f" % v).rstrip("0").rstrip(".")
    return str(v)


def score_metric(key: str, spec: Dict[str, Any], raw: Any,
                 threshold_override: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Score one metric and return the full workings.

    Basis precedence: explicit peer data > own history (when requested) > sector band.
    Peer data wins because a live peer set is a better benchmark than any shipped
    default; own history wins over the shipped band when the analyst asks for it,
    because a company's own record controls for everything the band cannot.
    """
    detail: Dict[str, Any] = {
        "key": key,
        "label": spec.get("label", key),
        "category": spec["category"],
        "direction": spec["direction"],
        "weight": float(spec.get("weight", 1.0)),
        "scored": False,
        "value": None,
        "sub_score": None,
        "basis": None,
        "band": None,
        "source": None,
        "period": None,
        "note": None,
        "warning": None,
        "spec_note": spec.get("note"),
    }

    meta: Dict[str, Any] = {}
    value: Any = raw
    if isinstance(raw, dict):
        meta = raw
        value = raw.get("value")
    if value is None or (isinstance(value, str) and value.strip().lower() in ("", "na", "n/a", "not available")):
        detail["warning"] = "not supplied"
        return detail
    try:
        value = float(value)
    except (TypeError, ValueError):
        detail["warning"] = "value '%s' is not numeric -- not scored" % (value,)
        return detail

    detail["value"] = value
    detail["source"] = meta.get("source")
    detail["period"] = meta.get("period")
    detail["note"] = meta.get("note")

    direction = spec["direction"]

    if direction == "judgement":
        if not 0.0 <= value <= 10.0:
            detail["warning"] = "judgement score must be 0-10; got %s -- not scored" % _num(value)
            return detail
        detail["sub_score"] = round(value, 2)
        detail["basis"] = "analyst judgement"
        detail["band"] = "0-10 direct"
        detail["scored"] = True
        if not detail["note"]:
            detail["warning"] = "judgement metric supplied without a written justification"
        return detail

    requested = (meta.get("basis") or "").strip().lower()

    # 1. Peer set, if supplied.
    pct = None
    if meta.get("peer_values"):
        pct = peer_percentile(value, meta["peer_values"], direction)
        if pct is None:
            detail["warning"] = "peer_values needs at least 3 comparable values -- fell back to the sector band"
        else:
            detail["sub_score"] = round(pct * 10.0, 2)
            detail["basis"] = "peer percentile (n=%d)" % len(meta["peer_values"])
            detail["band"] = "beats %d%% of the peer set" % round(pct * 100)
            detail["scored"] = True
            return detail
    elif meta.get("peer_percentile") is not None:
        p = float(meta["peer_percentile"])
        p = p / 100.0 if p > 1.0 else p
        p = min(max(p, 0.0), 1.0)
        detail["sub_score"] = round(p * 10.0, 2)
        detail["basis"] = "peer percentile (supplied)"
        detail["band"] = "beats %d%% of the peer set" % round(p * 100)
        detail["scored"] = True
        return detail

    # 2. Own history, when the analyst asks for it.
    thresholds = threshold_override or spec.get("thresholds")
    if requested in ("own_history", "own", "history") and meta.get("own_history"):
        derived = own_history_thresholds(direction, meta["own_history"])
        if derived is None:
            detail["warning"] = "own_history needs 3+ positive values on a directional metric -- used the sector band"
        else:
            points = build_anchor_points(direction, derived)
            detail["sub_score"] = round(interpolate(value, points), 2)
            detail["basis"] = "own history (med %s)" % _num(round(statistics.median(
                [float(v) for v in meta["own_history"]]), 2))
            detail["band"] = _describe_band(direction, {k: round(v, 2) for k, v in derived.items()})
            detail["scored"] = True
            return detail

    # 3. Sector band.
    if not thresholds:
        detail["warning"] = "no thresholds defined for this metric -- not scored"
        return detail
    points = build_anchor_points(direction, thresholds)
    detail["sub_score"] = round(interpolate(value, points), 2)
    detail["basis"] = "sector band" + (" (overridden)" if threshold_override else "")
    detail["band"] = _describe_band(direction, thresholds)
    detail["scored"] = True
    return detail


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def aggregate(details: Sequence[Dict[str, Any]], all_specs: Dict[str, Dict[str, Any]],
              category_weights: Dict[str, float],
              manual_scores: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Roll metric sub-scores into category scores, then into a composite.

    Categories with no data are DROPPED and the remaining weights renormalised to
    1.0. They are never scored as zero: a missing number is not a bad number, and
    treating absence as failure would make an under-disclosed company look fraudulent
    and a fully disclosed one look risky.
    """
    manual_scores = manual_scores or {}
    categories: Dict[str, Dict[str, Any]] = {}
    for cat in category_weights:
        categories[cat] = {
            "category": cat,
            "weight_default": float(category_weights[cat]),
            "metrics_scored": 0,
            "metrics_available": 0,
            "weight_scored": 0.0,
            "weight_available": 0.0,
            "score": None,
            "manual": False,
        }
    for key, spec in all_specs.items():
        cat = spec["category"]
        if cat not in categories:
            categories[cat] = {"category": cat, "weight_default": 0.0, "metrics_scored": 0,
                               "metrics_available": 0, "weight_scored": 0.0, "weight_available": 0.0,
                               "score": None, "manual": False}
        categories[cat]["metrics_available"] += 1
        categories[cat]["weight_available"] += float(spec.get("weight", 1.0))

    numerators: Dict[str, float] = {c: 0.0 for c in categories}
    for det in details:
        if not det["scored"]:
            continue
        cat = det["category"]
        numerators[cat] += det["sub_score"] * det["weight"]
        categories[cat]["metrics_scored"] += 1
        categories[cat]["weight_scored"] += det["weight"]

    for cat, node in categories.items():
        if node["weight_scored"] > 0:
            node["score"] = round(numerators[cat] / node["weight_scored"], 2)
        if cat in manual_scores:
            node["score"] = round(float(manual_scores[cat]), 2)
            node["manual"] = True
        node["metric_coverage"] = (
            round(node["weight_scored"] / node["weight_available"], 3)
            if node["weight_available"] else 0.0
        )

    live = {c: n for c, n in categories.items() if n["score"] is not None and n["weight_default"] > 0}
    live_weight = sum(n["weight_default"] for n in live.values())
    total_weight = sum(n["weight_default"] for n in categories.values())

    composite_raw = None
    for cat, node in categories.items():
        node["weight_renormalised"] = (
            round(node["weight_default"] / live_weight, 4) if (cat in live and live_weight > 0) else 0.0
        )
        node["contribution"] = (
            round(node["score"] * node["weight_renormalised"], 3) if cat in live else 0.0
        )
    if live_weight > 0:
        composite_raw = round(sum(n["contribution"] for n in categories.values()), 2)

    return {
        "categories": categories,
        "composite_raw": composite_raw,
        "category_coverage": round(live_weight / total_weight, 3) if total_weight else 0.0,
        "metric_coverage": round(
            sum(n["weight_scored"] for n in categories.values())
            / max(sum(n["weight_available"] for n in categories.values()), 1e-9), 3),
    }


def apply_gates(bm: Dict[str, Any], flags: Any, composite: Optional[float],
                enabled: bool = True) -> Dict[str, Any]:
    """Apply veto and cap gates to the composite.

    Averaging is the wrong operation for a disqualifying fact. A composite is a
    statement about a distribution of ordinary evidence; a going-concern paragraph
    or a pledged promoter stake is not one more piece of evidence, it is a statement
    that the distribution does not apply. So these findings cap or void the number
    rather than being blended into it.
    """
    gates = {g["id"]: g for g in bm.get("_gates", [])}
    raised: List[Dict[str, Any]] = []
    unknown: List[str] = []

    if isinstance(flags, dict):
        items = []
        for fid, payload in flags.items():
            if isinstance(payload, dict):
                if payload.get("present", True):
                    items.append((fid, payload.get("evidence") or payload.get("note")))
            elif payload:
                items.append((fid, None if payload is True else str(payload)))
    elif isinstance(flags, (list, tuple)):
        items = [(str(f), None) for f in flags]
    else:
        items = []

    for fid, evidence in items:
        gate = gates.get(fid)
        if not gate:
            unknown.append(fid)
            continue
        raised.append({
            "id": fid,
            "label": gate["label"],
            "severity": gate["severity"],
            "cap": gate.get("cap"),
            "why": gate.get("why"),
            "evidence": evidence,
            "evidence_needed": gate.get("evidence_needed"),
        })

    vetoed = any(g["severity"] == "veto" for g in raised)
    caps = [g["cap"] for g in raised if g["severity"] == "cap" and g.get("cap") is not None]
    binding_cap = min(caps) if caps else None

    final = composite
    applied = None
    if enabled and composite is not None:
        if vetoed:
            final = None
            applied = "veto"
        elif binding_cap is not None and composite > binding_cap:
            final = binding_cap
            applied = "cap"
    elif not enabled and raised:
        applied = "suppressed (--no-gates)"

    return {
        "raised": raised,
        "unknown_flags": unknown,
        "vetoed": bool(vetoed and enabled),
        "binding_cap": binding_cap,
        "applied": applied,
        "composite_final": final,
    }


def grade(score: Optional[float]) -> str:
    if score is None:
        return "NOT SCOREABLE"
    for floor, name in GRADES:
        if score >= floor:
            return name
    return "Poor"


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def run_scorecard(bm: Dict[str, Any], payload: Dict[str, Any], args: argparse.Namespace) -> Dict[str, Any]:
    """Score one company end to end and return the full result structure."""
    warnings: List[str] = []
    sector_arg = args.sector or payload.get("sector")
    key, sector, sector_warnings = resolve_sector(bm, sector_arg)
    warnings.extend(sector_warnings)

    overrides = payload.get("overrides", {}) or {}
    metrics_in = payload.get("metrics", {}) or {}
    if not metrics_in:
        raise ScoringError("input has no 'metrics' block -- nothing to score")

    specs = dict(sector["metrics"])
    for dropped in overrides.get("disable_metrics", []) or []:
        specs.pop(dropped, None)

    # Category weights: sector default -> preset -> input override -> CLI flag.
    category_weights = dict(sector["category_weights"])
    preset_name = args.preset or overrides.get("preset")
    if preset_name:
        preset = (bm.get("_weight_presets", {}) or {}).get(preset_name)
        if not preset or "weights" not in preset:
            if preset_name != "default":
                warnings.append("unknown weight preset '%s' -- kept the sector defaults" % preset_name)
        else:
            category_weights = dict(preset["weights"])
    for src in (overrides.get("category_weights") or {}, dict(args.weight_overrides or {})):
        for cat, val in src.items():
            if cat not in category_weights:
                warnings.append("weight override for unknown category '%s' ignored" % cat)
                continue
            category_weights[cat] = float(val)

    weight_sum = sum(category_weights.values())
    if abs(weight_sum - 1.0) > 1e-6:
        warnings.append("category weights summed to %.3f -- rescaled to 1.00" % weight_sum)
        category_weights = {c: w / weight_sum for c, w in category_weights.items()}

    metric_weight_overrides = overrides.get("metric_weights") or {}
    threshold_overrides = overrides.get("thresholds") or {}

    details: List[Dict[str, Any]] = []
    unknown_metrics: List[str] = []
    for mkey, raw in metrics_in.items():
        spec = specs.get(mkey)
        if not spec:
            unknown_metrics.append(mkey)
            continue
        spec = dict(spec)
        if mkey in metric_weight_overrides:
            spec["weight"] = float(metric_weight_overrides[mkey])
        try:
            det = score_metric(mkey, spec, raw, threshold_overrides.get(mkey))
        except ScoringError as exc:
            det = {"key": mkey, "label": spec.get("label", mkey), "category": spec["category"],
                   "direction": spec["direction"], "weight": float(spec.get("weight", 1.0)),
                   "scored": False, "value": None, "sub_score": None, "basis": None, "band": None,
                   "source": None, "period": None, "note": None,
                   "warning": "threshold error: %s" % exc, "spec_note": spec.get("note")}
        details.append(det)
    if unknown_metrics:
        warnings.append(
            "metrics not in the '%s' set were ignored: %s. Either they belong to another "
            "sector or the key is misspelled -- check with --explain." % (key, ", ".join(sorted(unknown_metrics)))
        )

    # Metrics defined for the sector but never supplied still count against coverage.
    supplied = {d["key"] for d in details}
    for mkey, spec in specs.items():
        if mkey not in supplied:
            details.append({
                "key": mkey, "label": spec.get("label", mkey), "category": spec["category"],
                "direction": spec["direction"], "weight": float(spec.get("weight", 1.0)),
                "scored": False, "value": None, "sub_score": None, "basis": None, "band": None,
                "source": None, "period": None, "note": None, "warning": "not supplied",
                "spec_note": spec.get("note"),
            })

    agg = aggregate(details, specs, category_weights, overrides.get("category_scores"))
    gate_result = apply_gates(bm, payload.get("flags"), agg["composite_raw"], enabled=not args.no_gates)
    if gate_result["unknown_flags"]:
        warnings.append("unrecognised flags ignored: %s (see --explain gates)"
                        % ", ".join(gate_result["unknown_flags"]))

    coverage_cfg = bm.get("_coverage", {}) or {}
    min_cov = args.min_coverage if args.min_coverage is not None else float(
        coverage_cfg.get("min_category_coverage", 0.70))
    empty_major = [c for c, n in agg["categories"].items()
                   if n["weight_default"] >= 0.10 and n["score"] is None]
    confident = agg["category_coverage"] >= min_cov and not empty_major
    coverage_reasons: List[str] = []
    if agg["category_coverage"] < min_cov:
        coverage_reasons.append("category coverage %.0f%% is below the %.0f%% floor"
                                % (agg["category_coverage"] * 100, min_cov * 100))
    if empty_major:
        coverage_reasons.append("no data at all in: %s" % ", ".join(sorted(empty_major)))
    thin = [c for c, n in agg["categories"].items()
            if n["score"] is not None and not n["manual"]
            and n["metrics_scored"] < int(coverage_cfg.get("min_metrics_per_category", 2))]
    if thin:
        warnings.append("categories resting on a single metric (fragile, easy to dispute): %s"
                        % ", ".join(sorted(thin)))

    return {
        "company": payload.get("company"),
        "ticker": payload.get("ticker"),
        "as_of": payload.get("as_of"),
        "basis": payload.get("basis"),
        "currency": payload.get("currency"),
        "sector_key": key,
        "sector_label": sector["label"],
        "sector_notes": sector["notes"],
        "sector_chain": sector["chain"],
        "benchmarks_file": args.benchmarks,
        "benchmarks_note": bm.get("_note"),
        "weight_preset": preset_name or "default",
        "category_weights": category_weights,
        "details": details,
        "categories": agg["categories"],
        "composite_raw": agg["composite_raw"],
        "composite": gate_result["composite_final"],
        "grade": "DISQUALIFIED - RESOLVE THE GATE FIRST" if gate_result["vetoed"] else grade(gate_result["composite_final"]),
        "gates": gate_result,
        "category_coverage": agg["category_coverage"],
        "metric_coverage": agg["metric_coverage"],
        "coverage_floor": min_cov,
        "composite_confident": bool(confident and not gate_result["vetoed"]),
        "coverage_reasons": coverage_reasons,
        "warnings": warnings,
    }


# ---------------------------------------------------------------------------
# Multi-segment scoring
# ---------------------------------------------------------------------------
#
# The governing principle of this whole skill is that a metric is meaningless
# outside its sector. A conglomerate breaks that principle by construction: one
# sector key cannot be right for a company that is 55% EPC, 30% IT services and
# 15% lending. Scoring it as a single entity benchmarks 45% of its profit against
# bands that were never meant for it. So each segment is scored against its own
# sector's benchmark set with the ordinary machinery, and only the finished
# composites are blended -- never the raw metrics, which are not commensurable.

FINANCIAL_SECTOR_KEYS = frozenset({"banks", "nbfc", "insurance"})

# Which payload field carries the size measure for each weighting basis.
WEIGHT_BASIS_FIELDS = {
    "ebit": "ebit",
    "capital_employed": "capital_employed",
    "revenue": "revenue",
    "explicit": "weight",
}

# Fallback order per requested basis. The first basis that is supplied for EVERY
# segment and strictly positive everywhere wins; see resolve_segment_weights.
WEIGHT_BASIS_FALLBACK: Dict[str, Tuple[str, ...]] = {
    "ebit": ("ebit", "capital_employed", "revenue"),
    "capital_employed": ("capital_employed", "revenue", "ebit"),
    "revenue": ("revenue", "capital_employed", "ebit"),
    "explicit": ("explicit", "ebit", "capital_employed", "revenue"),
}

DOMINANT_SEGMENT_SHARE = 0.60   # above this, one playbook governs the analysis
CONGLOMERATE_MAX_SHARE = 0.40   # below this for every segment, it is a conglomerate


def _segment_number(seg: Dict[str, Any], field: str) -> Optional[float]:
    """Read one numeric sizing field off a segment, accepting {"value": x} form."""
    raw = seg.get(field)
    if isinstance(raw, dict):
        raw = raw.get("value")
    if raw is None:
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def _basis_values(segments: Sequence[Dict[str, Any]], basis: str) -> Optional[List[float]]:
    """Return the sizing values for a basis, or None if any segment is missing one."""
    field = WEIGHT_BASIS_FIELDS[basis]
    values: List[float] = []
    for seg in segments:
        val = _segment_number(seg, field)
        if val is None:
            return None
        values.append(val)
    return values


def resolve_segment_weights(segments: Sequence[Dict[str, Any]],
                            requested: str) -> Dict[str, Any]:
    """Choose the weighting basis and return normalised weights summing to 1.0.

    EBIT is the right default because profit mix, not revenue mix, is what an
    investor owns -- a trading segment can be 60% of revenue and 5% of profit.

    But EBIT weighting breaks completely the moment a segment loses money. A
    negative EBIT produces a negative weight, and a negative weight does not
    down-weight a bad segment, it SUBTRACTS its score from the group: a segment
    burning capital would mechanically raise the composite. Worse, if the losses
    roughly offset the profits the denominator approaches zero and every weight
    explodes. Neither failure is a rounding problem, so we do not clamp or floor
    the value -- we refuse the basis entirely and fall back to a size measure that
    is positive by construction (capital employed, then revenue), because the
    question "how much of this group is this segment" still has a sensible answer
    even when the segment's profit is negative.

    The same positivity test is applied to every basis, so a nonsensical zero or
    negative capital-employed figure is rejected the same way.
    """
    requested = (requested or "ebit").strip().lower()
    if requested not in WEIGHT_BASIS_FALLBACK:
        requested = "ebit"

    warnings: List[str] = []
    rejections: List[Tuple[str, str]] = []

    for basis in WEIGHT_BASIS_FALLBACK[requested]:
        values = _basis_values(segments, basis)
        if values is None:
            rejections.append((basis, "not supplied for every segment"))
            continue
        bad = [segments[i].get("name") or "segment %d" % (i + 1)
               for i, v in enumerate(values) if v <= 0]
        if bad:
            rejections.append((basis, "zero or negative for: %s" % ", ".join(bad)))
            continue
        total = sum(values)
        if total <= 0:  # pragma: no cover - impossible once every value is positive
            rejections.append((basis, "values sum to zero"))
            continue
        weights = [v / total for v in values]
        if basis != requested:
            why = rejections[0][1] if rejections else "unavailable"
            warnings.append(
                "WEIGHTING FALLBACK: '%s' weighting was requested but is %s. A loss-making "
                "segment under EBIT weighting produces a NEGATIVE weight, which would subtract "
                "that segment's score from the group composite instead of reducing its "
                "influence. Fell back to '%s' weighting, which is positive by construction. "
                "Read the loss-making segments on their own terms -- the capital at risk, not "
                "the weight, is the measure of how much they matter."
                % (requested, why, basis)
            )
        return {"basis": basis, "requested": requested, "weights": weights,
                "values": values, "field": WEIGHT_BASIS_FIELDS[basis],
                "warnings": warnings, "rejected": rejections}

    # Nothing usable was supplied. Equal weighting is the only remaining honest
    # choice: it makes no claim about relative size rather than inventing one.
    n = len(segments)
    warnings.append(
        "WEIGHTING FALLBACK: no usable size measure was supplied (%s). Fell back to EQUAL "
        "weights across %d segments. This asserts nothing about relative size -- supply "
        "'ebit', 'capital_employed' or 'revenue' per segment and re-run before quoting the "
        "group composite."
        % ("; ".join("%s: %s" % r for r in rejections) or "none supplied", n)
    )
    return {"basis": "equal", "requested": requested, "weights": [1.0 / n] * n,
            "values": [1.0] * n, "field": None, "warnings": warnings,
            "rejected": rejections}


def _segment_args(args: argparse.Namespace) -> argparse.Namespace:
    """Clone the CLI namespace for per-segment scoring.

    ``--sector`` is dropped: it overrides the sector key in the input, which is
    exactly the mistake segmented scoring exists to prevent -- forcing one sector
    onto every segment would silently rescore the lending arm as an EPC business.
    Everything else (preset, weight overrides, coverage floor, gate switch) is a
    property of the reader's objective, so it carries into every segment.
    """
    clone = argparse.Namespace(**vars(args))
    clone.sector = None
    return clone


def _segment_payload(payload: Dict[str, Any], seg: Dict[str, Any], name: str) -> Dict[str, Any]:
    """Build the single-sector payload for one segment, reusing run_scorecard verbatim.

    Group identity fields are inherited so the per-segment scorecard is readable on
    its own. Group ``flags`` are NOT inherited -- a group-level gate applies to the
    blended composite once, and copying it into every segment would apply the same
    cap several times over. Group ``overrides`` are not inherited either: thresholds
    and category weights tuned for one sector are not valid for another.
    """
    return {
        "company": "%s | segment: %s" % (payload.get("company") or "(unnamed)", name),
        "ticker": payload.get("ticker"),
        "as_of": payload.get("as_of"),
        "basis": payload.get("basis"),
        "currency": payload.get("currency"),
        "sector": seg.get("sector"),
        "metrics": seg.get("metrics") or {},
        "flags": seg.get("flags"),
        "overrides": seg.get("overrides") or {},
    }


def blend_composites(entries: Sequence[Dict[str, Any]], field: str) -> Dict[str, Any]:
    """Weighted mean of one composite field across segments, renormalising for gaps.

    A segment whose composite could not be computed (no data, or a veto) is dropped
    and the remaining weights renormalised, for the same reason missing metrics are
    dropped rather than zeroed: absence of a number is not evidence of a bad number.
    The share of weight that actually made it into the blend is reported so a reader
    can see how much of the group the number really covers.
    """
    usable = [e for e in entries if e["result"].get(field) is not None]
    covered = sum(e["weight"] for e in usable)
    if not usable or covered <= 0:
        return {"value": None, "weight_covered": 0.0, "segments_used": 0}
    value = sum(e["result"][field] * (e["weight"] / covered) for e in usable)
    return {"value": round(value, 2), "weight_covered": round(covered, 4),
            "segments_used": len(usable)}


def segment_diagnostics(entries: Sequence[Dict[str, Any]], weighting: Dict[str, Any]) -> List[Dict[str, str]]:
    """Structural findings about the segment mix that the composite alone cannot show.

    These are the observations that decide HOW the group should be analysed --
    which playbook governs, whether consolidated ratios can be read at all, and
    whether a single multiple may be applied to the whole group. They are printed
    with the score rather than left to the analyst to remember.
    """
    diags: List[Dict[str, str]] = []
    if not entries:
        return diags

    basis = weighting["basis"]
    ranked = sorted(entries, key=lambda e: -e["weight"])
    top = ranked[0]

    diags.append({
        "id": "concentration",
        "severity": "info",
        "text": "Largest segment: %s (%s) at %.0f%% of the %s base. Segment mix by %s: %s."
                % (top["name"], top["sector_key"], top["weight"] * 100, basis, basis,
                   ", ".join("%s %.0f%%" % (e["name"], e["weight"] * 100) for e in ranked)),
    })

    if top["weight"] > DOMINANT_SEGMENT_SHARE:
        diags.append({
            "id": "dominant_segment",
            "severity": "note",
            "text": "%s is %.0f%% of the %s base, above the 60%% dominance threshold. Its playbook "
                    "(references/sectors/%s.md) governs the analysis; the other segments are "
                    "adjustments to it, not co-equal lenses. Name each secondary segment and state "
                    "in one line what it does to the consolidated numbers."
                    % (top["name"], top["weight"] * 100, basis, top["sector_key"]),
        })
    elif all(e["weight"] < CONGLOMERATE_MAX_SHARE for e in entries):
        diags.append({
            "id": "conglomerate",
            "severity": "warning",
            "text": "No segment reaches 40%% of the %s base. This is a de facto conglomerate, and no "
                    "single operating playbook governs it. Run it through "
                    "references/sectors/holdco-assetmgr.md as well and value it sum-of-the-parts: "
                    "the questions that decide the outcome are the holding-company discount, where "
                    "incremental capital goes, and whether subsidiary value ever reaches minority "
                    "shareholders -- none of which any operating scorecard measures."
                    % basis,
        })

    # Loss-makers are reported before the structural notes, and before any blended
    # number, because the weighting scheme is exactly what tends to hide them.
    losers = [e for e in entries if e.get("ebit") is not None and e["ebit"] <= 0]
    if losers:
        diags.append({
            "id": "loss_making_segments",
            "severity": "warning",
            "text": "LOSS-MAKING SEGMENTS: %s. A segment destroying capital deserves attention in "
                    "proportion to the CAPITAL AT RISK, not to the small (or excluded) weight its "
                    "loss earns it in the blend. State for each one what capital is employed there, "
                    "what the group's plan for it is, and how the composite would move if it were "
                    "closed, sold or fixed."
                    % "; ".join(
                        "%s (EBIT %s%s)" % (
                            e["name"], _num(e["ebit"]),
                            ", capital employed %s = %.0f%% of group" % (
                                _num(e["capital_employed"]), e["capital_employed_share"] * 100)
                            if e.get("capital_employed_share") is not None else "")
                        for e in losers),
        })

    fin = sorted({e["sector_key"] for e in entries if e["sector_key"] in FINANCIAL_SECTOR_KEYS})
    non_fin = sorted({e["sector_key"] for e in entries if e["sector_key"] not in FINANCIAL_SECTOR_KEYS})
    if fin and non_fin:
        diags.append({
            "id": "mixed_families",
            "severity": "warning",
            "text": "MIXED FAMILIES: this group spans a financial business (%s) and non-financial "
                    "businesses (%s). The CONSOLIDATED ratios are contaminated and must not be read "
                    "at face value: the lending arm's loan-book growth sits inside consolidated "
                    "operating cash flow, so group cash conversion measures disbursement rather than "
                    "cash generation; and the lender's borrowings -- its raw material, not its "
                    "financing -- inflate group debt/equity and net debt/EBITDA to levels that mean "
                    "nothing. Read group-level cash-conversion and leverage metrics as invalid, use "
                    "each segment's own set instead, and value the group sum-of-the-parts (the "
                    "lender on P/B or P/adjusted book, the operating businesses on their own "
                    "multiples)." % (", ".join(fin), ", ".join(non_fin)),
        })

    diags.append({
        "id": "valuation_caveat",
        "severity": "mandatory",
        "text": "VALUATION CAVEAT: the blended composite scores QUALITY across the group. It is not a "
                "valuation and never substitutes for sum-of-the-parts. Never apply a single "
                "consolidated multiple across a mixed group -- value each segment on its own "
                "family's basis, net out holding-company debt and recurring holdco costs, and apply "
                "a holding discount where the segments are not separately monetisable.",
    })
    return diags


def merge_segment_gates(group_gates: Dict[str, Any], entries: Sequence[Dict[str, Any]],
                        blended: Optional[float], enabled: bool) -> Dict[str, Any]:
    """Combine group-level gates with segment-level gates, escalating any veto.

    Group flags cap or void the blended composite exactly as in single-sector mode.
    Segment flags have already bound that segment's own composite inside
    run_scorecard, so a segment CAP needs no further action -- it is already in the
    blend through the capped number.

    A segment VETO is different in kind. A going-concern paragraph, an adverse
    opinion or a fraud investigation in one segment is a statement that the numbers
    are unreliable, and unreliable numbers do not stay inside their segment: they
    are consolidated into the group accounts, audited by the same auditor, signed by
    the same board. Blending a vetoed segment away at 15% weight would convert "we
    cannot believe these accounts" into a small deduction. So any segment veto
    escalates and withholds the group composite too.
    """
    raised: List[Dict[str, Any]] = []
    for gate in group_gates["raised"]:
        entry = dict(gate)
        entry["level"] = "group"
        raised.append(entry)

    escalated: List[Dict[str, Any]] = []
    for seg in entries:
        for gate in seg["result"]["gates"]["raised"]:
            entry = dict(gate)
            entry["level"] = "segment: %s" % seg["name"]
            entry["segment"] = seg["name"]
            raised.append(entry)
            if gate["severity"] == "veto":
                escalated.append(entry)

    vetoed = bool(group_gates["vetoed"]) or bool(enabled and escalated)
    final = group_gates["composite_final"]
    applied = group_gates["applied"]
    if enabled and escalated and final is not None:
        final = None
        applied = "veto (escalated from segment)" if not group_gates["vetoed"] else "veto"
    elif not enabled and raised and not applied:
        applied = "suppressed (--no-gates)"

    return {
        "raised": raised,
        "unknown_flags": list(group_gates["unknown_flags"]),
        "vetoed": vetoed,
        "binding_cap": group_gates["binding_cap"],
        "applied": applied,
        "composite_final": final,
        "escalated_from_segments": [
            {"segment": e["segment"], "id": e["id"], "label": e["label"]} for e in escalated
        ],
        "group_composite_pre_gate": blended,
    }


def run_segmented_scorecard(bm: Dict[str, Any], payload: Dict[str, Any],
                            args: argparse.Namespace) -> Dict[str, Any]:
    """Score a multi-segment company: each segment on its own sector, then blend.

    Returns a result structure with ``mode`` set to ``"segmented"``, the full
    single-sector result for every segment under ``segments[i]["result"]``, and the
    group blend, diagnostics and gates alongside it.
    """
    segments_in = payload.get("segments") or []
    if not isinstance(segments_in, list) or not segments_in:
        raise ScoringError("'segments' must be a non-empty array of segment objects")

    warnings: List[str] = []
    if args.sector:
        warnings.append("--sector is ignored for segmented input; each segment uses its own "
                        "'sector' key, which is the entire point of segmented scoring.")
    if payload.get("overrides"):
        warnings.append("top-level 'overrides' is ignored for segmented input -- thresholds and "
                        "category weights are sector-specific and cannot be valid for every "
                        "segment at once. Put overrides inside the segment they belong to.")
    if payload.get("sector"):
        warnings.append("top-level 'sector' is ignored because 'segments' is present.")
    if payload.get("metrics"):
        warnings.append("top-level 'metrics' is ignored because 'segments' is present. Consolidated "
                        "metrics for a multi-segment group are the contaminated numbers segmented "
                        "scoring exists to avoid; move them into the segment they describe.")

    # 1. Weighting basis, resolved before any scoring so the fallback is decided on
    #    the reported segment economics rather than on the scores.
    requested_basis = (args.weight_basis or payload.get("weight_basis") or "ebit")
    weighting = resolve_segment_weights(segments_in, requested_basis)
    warnings.extend(weighting["warnings"])

    # 2. Score each segment against its own sector using the ordinary machinery.
    seg_args = _segment_args(args)
    entries: List[Dict[str, Any]] = []
    ce_values = _basis_values(segments_in, "capital_employed")
    ce_total = sum(ce_values) if ce_values and sum(ce_values) > 0 else None
    for idx, seg in enumerate(segments_in):
        if not isinstance(seg, dict):
            raise ScoringError("segment %d is not an object" % (idx + 1))
        name = str(seg.get("name") or "segment %d" % (idx + 1))
        if not seg.get("sector"):
            warnings.append("segment '%s' has no 'sector' key -- it will fall back to the generic "
                            "metric set, which is not valid for lenders, insurers or REITs." % name)
        try:
            result = run_scorecard(bm, _segment_payload(payload, seg, name), seg_args)
        except ScoringError as exc:
            raise ScoringError("segment '%s': %s" % (name, exc))
        ebit = _segment_number(seg, "ebit")
        cap = _segment_number(seg, "capital_employed")
        entries.append({
            "name": name,
            "sector_key": result["sector_key"],
            "sector_label": result["sector_label"],
            "weight": round(weighting["weights"][idx], 4),
            "weight_value": weighting["values"][idx],
            "ebit": ebit,
            "capital_employed": cap,
            "revenue": _segment_number(seg, "revenue"),
            "capital_employed_share": (round(cap / ce_total, 4)
                                       if cap is not None and ce_total else None),
            "note": seg.get("note"),
            "result": result,
        })
        for warn in result["warnings"]:
            warnings.append("[%s] %s" % (name, warn))

    # 3. Blend the segment composites. Gated composites are blended, not raw ones:
    #    a segment cap is a real statement about that segment's evidence and must
    #    survive into the group number.
    blend = blend_composites(entries, "composite")
    blend_pre_gate = blend_composites(entries, "composite_raw")

    group_gates = apply_gates(bm, payload.get("flags"), blend["value"], enabled=not args.no_gates)
    if group_gates["unknown_flags"]:
        warnings.append("unrecognised group flags ignored: %s (see --explain gates)"
                        % ", ".join(group_gates["unknown_flags"]))
    gates = merge_segment_gates(group_gates, entries, blend["value"], enabled=not args.no_gates)

    # 4. Coverage: weighted across segments, checked against the same floor.
    coverage_cfg = bm.get("_coverage", {}) or {}
    min_cov = args.min_coverage if args.min_coverage is not None else float(
        coverage_cfg.get("min_category_coverage", 0.70))
    cat_cov = sum(e["weight"] * e["result"]["category_coverage"] for e in entries)
    met_cov = sum(e["weight"] * e["result"]["metric_coverage"] for e in entries)

    coverage_reasons: List[str] = []
    if cat_cov < min_cov:
        coverage_reasons.append("weighted category coverage %.0f%% is below the %.0f%% floor"
                                % (cat_cov * 100, min_cov * 100))
    weak = [e["name"] for e in entries if not e["result"]["composite_confident"]
            and not e["result"]["gates"]["vetoed"]]
    if weak:
        coverage_reasons.append("segment composites that are themselves indicative only: %s"
                                % ", ".join(weak))
    if blend["value"] is not None and blend["weight_covered"] < 0.999:
        coverage_reasons.append("the blend covers only %.0f%% of the weight base; %s could not be "
                                "scored" % (blend["weight_covered"] * 100,
                                            ", ".join(e["name"] for e in entries
                                                      if e["result"]["composite"] is None)))

    diagnostics = segment_diagnostics(entries, weighting)

    return {
        "mode": "segmented",
        "company": payload.get("company"),
        "ticker": payload.get("ticker"),
        "as_of": payload.get("as_of"),
        "basis": payload.get("basis"),
        "currency": payload.get("currency"),
        "benchmarks_file": args.benchmarks,
        "benchmarks_note": bm.get("_note"),
        "weight_preset": (args.preset or "default"),
        "weight_basis": weighting["basis"],
        "weight_basis_requested": weighting["requested"],
        "weight_basis_rejected": [{"basis": b, "reason": r} for b, r in weighting["rejected"]],
        "segments": entries,
        "composite_blend_pre_segment_gates": blend_pre_gate["value"],
        "composite_raw": blend["value"],
        "composite": gates["composite_final"],
        "grade": ("DISQUALIFIED - RESOLVE THE GATE FIRST" if gates["vetoed"]
                  else grade(gates["composite_final"])),
        "blend_weight_covered": blend["weight_covered"],
        "gates": gates,
        "category_coverage": round(cat_cov, 3),
        "metric_coverage": round(met_cov, 3),
        "coverage_floor": min_cov,
        "composite_confident": bool(not coverage_reasons and not gates["vetoed"]),
        "coverage_reasons": coverage_reasons,
        "diagnostics": diagnostics,
        "warnings": warnings,
    }


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def _wrap(text: str, width: int, indent: str = "") -> List[str]:
    words, lines, cur = text.split(), [], ""
    for word in words:
        candidate = (cur + " " + word).strip()
        if len(candidate) + len(indent) > width and cur:
            lines.append(indent + cur)
            cur = word
        else:
            cur = candidate
    if cur:
        lines.append(indent + cur)
    return lines


def render_text(result: Dict[str, Any], width: int = 108) -> str:
    """Render the scorecard so every input can be disputed individually."""
    out: List[str] = []
    rule = "=" * width
    thin = "-" * width
    out.append(rule)
    title = "SECTOR-RELATIVE SCORECARD"
    if result.get("company"):
        title += "  |  " + str(result["company"])
    if result.get("ticker"):
        title += "  (%s)" % result["ticker"]
    out.append(title)
    meta = "Sector: %s [%s]" % (result["sector_label"], result["sector_key"])
    for label, key in (("Basis", "basis"), ("Currency", "currency"), ("As of", "as_of")):
        if result.get(key):
            meta += "  |  %s: %s" % (label, result[key])
    out.append(meta)
    out.append("Weights: %s preset  |  Scale 0-10 (2.5 poor / 5.0 average / 7.5 good / 10 excellent)"
               % result["weight_preset"])
    out.append("Benchmarks: %s" % result["benchmarks_file"])
    out.append(rule)

    if result.get("sector_notes"):
        out.append("")
        out.extend(_wrap("SECTOR NOTE: " + result["sector_notes"], width))

    cats = result["categories"]
    order = sorted(cats, key=lambda c: -cats[c]["weight_default"])
    for cat in order:
        node = cats[cat]
        rows = [d for d in result["details"] if d["category"] == cat]
        rows.sort(key=lambda d: (not d["scored"], -d["weight"], d["label"]))
        if not rows:
            continue
        out.append("")
        out.append(thin)
        head = cat.replace("_", " ").upper()
        if node["score"] is None:
            head += "   [NO DATA - dropped, weights renormalised]"
        else:
            head += "   score %5.2f   weight %.0f%% -> %.0f%%   coverage %.0f%%" % (
                node["score"], node["weight_default"] * 100,
                node["weight_renormalised"] * 100, node["metric_coverage"] * 100)
            if node["manual"]:
                head += "   [MANUAL OVERRIDE]"
        out.append(head)
        out.append(thin)
        out.append("  %-42s %9s  %-20s %-20s %5s %4s" %
                   ("Metric", "Value", "Basis", "Band p/a/g/e", "Score", "Wt"))
        for d in rows:
            if d["scored"]:
                out.append("  %-42.42s %9s  %-20.20s %-20.20s %5.1f %4.1f" % (
                    d["label"], _num(d["value"]), d["basis"] or "", d["band"] or "",
                    d["sub_score"], d["weight"]))
                for extra in ("source", "period", "note"):
                    if d.get(extra):
                        out.extend(_wrap("%s: %s" % (extra, d[extra]), width, indent="      "))
                if d.get("warning"):
                    out.extend(_wrap("! " + d["warning"], width, indent="      "))
            else:
                out.append("  %-42.42s %9s  %s" % (d["label"], "--", d.get("warning") or "not supplied"))
        out.append("")

    out.append(rule)
    comp = result["composite"]
    if result["gates"]["vetoed"]:
        out.append("COMPOSITE: WITHHELD - a veto gate is open. See GATES below.")
    elif comp is None:
        out.append("COMPOSITE: not computable - no category carried any data.")
    else:
        label = "COMPOSITE %.2f / 10   (%s)" % (comp, result["grade"])
        if not result["composite_confident"]:
            label += "   ** INDICATIVE ONLY **"
        out.append(label)
        if result["composite_raw"] is not None and abs(result["composite_raw"] - comp) > 1e-9:
            out.append("  Pre-gate composite was %.2f; capped to %.2f by the binding gate below."
                       % (result["composite_raw"], comp))
    out.append("Coverage: categories %.0f%% (floor %.0f%%), metric weight %.0f%%"
               % (result["category_coverage"] * 100, result["coverage_floor"] * 100,
                  result["metric_coverage"] * 100))
    for reason in result["coverage_reasons"]:
        out.extend(_wrap("! " + reason, width, indent="  "))
    if not result["composite_confident"] and not result["gates"]["vetoed"] and comp is not None:
        out.extend(_wrap(
            "Report this as an indicative composite and name the missing categories in the write-up. "
            "Do not present a confident single number on partial evidence.", width, indent="  "))
    out.append(rule)

    gates = result["gates"]
    if gates["raised"]:
        out.append("")
        out.append("GATES RAISED - these cap or void the composite rather than being averaged into it")
        out.append(thin)
        for g in gates["raised"]:
            marker = "VETO" if g["severity"] == "veto" else "CAP %.1f" % (g["cap"] or 0.0)
            out.append("  [%s] %s" % (marker, g["label"]))
            if g.get("why"):
                out.extend(_wrap("why: " + g["why"], width, indent="      "))
            if g.get("evidence"):
                out.extend(_wrap("evidence: " + str(g["evidence"]), width, indent="      "))
            elif g.get("evidence_needed"):
                out.extend(_wrap("evidence needed: " + g["evidence_needed"], width, indent="      "))
        if gates["applied"] == "veto":
            out.extend(_wrap(
                "A veto is not a low score. Resolve or disprove the finding, then re-run. "
                "Report the finding prominently and early rather than burying it in a scorecard.",
                width, indent="  "))
    else:
        out.append("")
        out.append("GATES: none raised. State in the report which gate checks were actually performed --")
        out.append("       an unchecked gate and a cleared gate look identical in this output.")

    if result["warnings"]:
        out.append("")
        out.append("NOTES AND WARNINGS")
        out.append(thin)
        for w in result["warnings"]:
            out.extend(_wrap("- " + w, width, indent="  "))

    out.append("")
    out.extend(_wrap("BENCHMARK CAVEAT: " + (result.get("benchmarks_note") or ""), width))
    out.append("")
    return "\n".join(out)


def render_json(result: Dict[str, Any]) -> str:
    slim = dict(result)
    slim["details"] = [
        {k: v for k, v in d.items() if k != "spec_note" or v} for d in result["details"]
    ]
    return json.dumps(slim, indent=2, ensure_ascii=False)


def render_segmented_text(result: Dict[str, Any], width: int = 108,
                          segment_detail: bool = False) -> str:
    """Render the group scorecard: segment table, blend, diagnostics, gates.

    The segment table comes first because the mix IS the analysis for a group like
    this -- which playbook governs, and how much of the profit each set of bands is
    responsible for, decides how every later number should be read.
    """
    out: List[str] = []
    rule = "=" * width
    thin = "-" * width

    out.append(rule)
    title = "SEGMENTED SECTOR-RELATIVE SCORECARD"
    if result.get("company"):
        title += "  |  " + str(result["company"])
    if result.get("ticker"):
        title += "  (%s)" % result["ticker"]
    out.append(title)
    meta = "Segments: %d" % len(result["segments"])
    for label, key in (("Basis", "basis"), ("Currency", "currency"), ("As of", "as_of")):
        if result.get(key):
            meta += "  |  %s: %s" % (label, result[key])
    out.append(meta)
    basis_line = "Weighting: %s" % result["weight_basis"]
    if result["weight_basis"] != result["weight_basis_requested"]:
        basis_line += "  (FALLBACK -- '%s' was requested; see warnings)" % result["weight_basis_requested"]
    basis_line += "  |  Weights: %s preset  |  Scale 0-10" % result["weight_preset"]
    out.append(basis_line)
    out.append("Benchmarks: %s" % result["benchmarks_file"])
    out.append(rule)

    out.append("")
    out.append("SEGMENTS - each scored against its OWN sector's bands, never a group-wide set")
    out.append(thin)
    out.append("  %-22s %-20s %7s %10s %-16s %9s" %
               ("Segment", "Sector", "Weight", "Composite", "Grade", "Coverage"))
    for seg in sorted(result["segments"], key=lambda e: -e["weight"]):
        res = seg["result"]
        comp = res["composite"]
        if res["gates"]["vetoed"]:
            comp_s, grade_s = "WITHHELD", "VETOED"
        elif comp is None:
            comp_s, grade_s = "--", "not scoreable"
        else:
            comp_s = "%.2f" % comp
            grade_s = res["grade"] + ("" if res["composite_confident"] else " *")
        out.append("  %-22.22s %-20.20s %6.1f%% %10s %-16.16s %8.0f%%" % (
            seg["name"], seg["sector_key"], seg["weight"] * 100, comp_s, grade_s,
            res["category_coverage"] * 100))
        size_bits = []
        for label, key in (("EBIT", "ebit"), ("capital employed", "capital_employed"),
                           ("revenue", "revenue")):
            if seg.get(key) is not None:
                size_bits.append("%s %s" % (label, _num(seg[key])))
        if seg.get("ebit") is not None and seg["ebit"] <= 0:
            # Flagged on the row itself: a weighting scheme is exactly what buries a
            # loss-making segment, so it must be visible before the weights are read.
            size_bits.append("<< LOSS-MAKING")
        if size_bits:
            out.append("      " + "  |  ".join(size_bits))
        if seg.get("note"):
            out.extend(_wrap("note: " + str(seg["note"]), width, indent="      "))
    out.append(thin)
    out.append("  * segment composite is indicative only (its own coverage is below the floor)")

    out.append("")
    out.append(rule)
    comp = result["composite"]
    if result["gates"]["vetoed"]:
        out.append("GROUP COMPOSITE: WITHHELD - a veto gate is open. See GATES below.")
    elif comp is None:
        out.append("GROUP COMPOSITE: not computable - no segment produced a composite.")
    else:
        label = "GROUP COMPOSITE %.2f / 10   (%s)" % (comp, result["grade"])
        if not result["composite_confident"]:
            label += "   ** INDICATIVE ONLY **"
        out.append(label)
        blended_n = len([s for s in result["segments"] if s["result"]["composite"] is not None])
        out.append("  Weighted mean of %d segment composites on the %s base, covering %.0f%% of it."
                   % (blended_n, result["weight_basis"], result["blend_weight_covered"] * 100))
        raw = result["composite_raw"]
        pre = result["composite_blend_pre_segment_gates"]
        if raw is not None and abs(raw - comp) > 1e-9:
            out.append("  Pre-gate blend was %.2f; capped to %.2f by the binding group gate below."
                       % (raw, comp))
        if pre is not None and raw is not None and abs(pre - raw) > 1e-9:
            out.append("  Before segment-level gates the blend was %.2f; segment caps pulled it to %.2f."
                       % (pre, raw))
    out.append("Coverage: weighted categories %.0f%% (floor %.0f%%), weighted metric weight %.0f%%"
               % (result["category_coverage"] * 100, result["coverage_floor"] * 100,
                  result["metric_coverage"] * 100))
    for reason in result["coverage_reasons"]:
        out.extend(_wrap("! " + reason, width, indent="  "))
    out.append(rule)

    out.append("")
    out.append("DIAGNOSTICS - structural findings about the mix; read these before the number")
    out.append(thin)
    for diag in result["diagnostics"]:
        marker = {"warning": "!!", "mandatory": ">>", "note": "->"}.get(diag["severity"], "  ")
        out.extend(_wrap("%s %s" % (marker, diag["text"]), width, indent="  "))
        out.append("")

    gates = result["gates"]
    if gates["raised"]:
        out.append(thin)
        out.append("GATES RAISED - these cap or void the composite rather than being averaged into it")
        out.append(thin)
        for g in gates["raised"]:
            marker = "VETO" if g["severity"] == "veto" else "CAP %.1f" % (g["cap"] or 0.0)
            out.append("  [%s] %s   <%s>" % (marker, g["label"], g["level"]))
            if g.get("why"):
                out.extend(_wrap("why: " + g["why"], width, indent="      "))
            if g.get("evidence"):
                out.extend(_wrap("evidence: " + str(g["evidence"]), width, indent="      "))
            elif g.get("evidence_needed"):
                out.extend(_wrap("evidence needed: " + g["evidence_needed"], width, indent="      "))
        if gates["escalated_from_segments"]:
            out.extend(_wrap(
                "A veto raised inside a segment has been ESCALATED to the group: %s. Unreliable "
                "accounts do not stay inside their segment -- they are consolidated into the group "
                "statements, audited by the same auditor and signed by the same board. Resolve or "
                "disprove the finding, then re-run."
                % ", ".join("%s (%s)" % (e["segment"], e["id"])
                            for e in gates["escalated_from_segments"]), width, indent="  "))
        elif gates["applied"] == "veto":
            out.extend(_wrap(
                "A veto is not a low score. Resolve or disprove the finding, then re-run.",
                width, indent="  "))
        out.extend(_wrap(
            "Segment CAPS are not re-applied at group level: they already bound that segment's own "
            "composite, and that capped number is what entered the blend.", width, indent="  "))
    else:
        out.append(thin)
        out.append("GATES: none raised at group or segment level. State in the report which gate")
        out.append("       checks were actually performed, per segment -- an unchecked gate and a")
        out.append("       cleared gate look identical in this output.")

    if result["warnings"]:
        out.append("")
        out.append("NOTES AND WARNINGS")
        out.append(thin)
        for w in result["warnings"]:
            out.extend(_wrap("- " + w, width, indent="  "))

    out.append("")
    out.extend(_wrap("BENCHMARK CAVEAT: " + (result.get("benchmarks_note") or ""), width))
    out.append("")

    if segment_detail:
        for seg in sorted(result["segments"], key=lambda e: -e["weight"]):
            out.append("")
            out.append("#" * width)
            out.append("# SEGMENT DETAIL: %s   (%.0f%% of the %s base)"
                       % (seg["name"], seg["weight"] * 100, result["weight_basis"]))
            out.append("#" * width)
            out.append(render_text(seg["result"], width))

    return "\n".join(out)


def render_segmented_json(result: Dict[str, Any]) -> str:
    """Serialise the group result, with each segment's full scorecard nested inside."""
    slim = dict(result)
    slim["segments"] = []
    for seg in result["segments"]:
        node = dict(seg)
        node["result"] = json.loads(render_json(seg["result"]))
        slim["segments"].append(node)
    return json.dumps(slim, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# --explain
# ---------------------------------------------------------------------------

METHOD_TEXT = """\
HOW THIS SCORE IS BUILT

1. Sector first. The sector key selects the metric set, the benchmark bands and the
   category weights. Banks, NBFCs, insurers and REITs use standalone sets because
   ROIC, EV/EBITDA and net debt/EBITDA are undefined or inverted for them. Other
   sectors extend the generic set and override the bands they disagree with -- which
   is why a 20% operating margin can score 8/10 in distribution and 5/10 in software.

2. Per-metric sub-score, 0-10. Values are interpolated between four anchors:
   poor=2.5, average=5.0, good=7.5, excellent=10.0. Beyond 'excellent' the score
   clamps at 10; beyond 'poor' it falls to 0 over one more band width. 'band' metrics
   (where both too little and too much are bad -- ad spend, R&D, loan growth) score 10
   inside the excellent interval and taper outward. 'judgement' metrics are supplied
   directly on the 0-10 scale and require a written justification.

3. Basis precedence: peer percentile > own history (if requested) > sector band.
   Supply peer_values and the metric is scored on where the company sits in that peer
   set, which beats any shipped default. Supply own_history with basis="own_history"
   and the company is scored against its own median (anchors at 0.85x / 1.00x / 1.15x /
   1.30x of it) -- the right basis when peers are poor but the record is long.

4. Category scores. Metrics roll up into eight categories by weighted mean of their
   sub-scores. Weighting by CATEGORY rather than by metric is deliberate: it stops a
   sector with twelve profitability ratios and two governance checks from producing a
   score that is 85% profitability. Categories are the unit of judgement; metrics are
   evidence within them.

5. Composite = sum(category score x renormalised category weight). Categories with no
   data are dropped and the remaining weights renormalised to 1.0. A missing number is
   never scored as zero -- that would make an under-disclosed company look fraudulent
   rather than unknown. Coverage is reported instead, and below the coverage floor the
   composite is marked INDICATIVE ONLY.

6. Gates. Certain findings cap the composite (auditor qualification 4.0, heavy promoter
   pledging 4.0, sustained cash-vs-profit divergence 4.0, opaque structure 5.5) or void
   it entirely (going-concern doubt, adverse opinion, active fraud investigation, payment
   default). Averaging is the wrong operation for a disqualifying fact: a composite
   summarises a distribution of ordinary evidence, and these findings say the
   distribution does not apply. A 9/10 business with a going-concern paragraph is not
   an 8/10 -- it is an unanswered question with an equity option attached.

7. Nothing here is a recommendation. The composite ranks quality-adjusted-for-price on
   the evidence supplied. It cannot see what you did not put in it, and it has no view
   on your portfolio, horizon or tax position.

ADJUSTING THE WEIGHTS
   --preset quality_compounder | deep_value | income | forensic
   --weight valuation=0.20 --weight risk=0.10   (renormalised automatically)
   Always show the weights used. A composite without its weight vector is not a
   reproducible number.

FLAGS AND GATES
   Pass "flags": ["auditor_qualification", ...] or, better, a dict carrying evidence:
   "flags": {"promoter_pledge_high": {"present": true, "evidence": "62% pledged, Q1 FY26 SHP"}}
   Run --explain gates for the full list.\
"""


def explain(bm: Dict[str, Any], topic: Optional[str], sector_arg: Optional[str], width: int = 108) -> str:
    out: List[str] = []
    topic = (topic or "method").strip()

    if topic in ("method", "", "*"):
        out.append(METHOD_TEXT)
        out.append("")
        out.append("CATEGORY WEIGHTS (defaults; sectors may override)")
        for cat, w in sorted(bm["_category_weights"].items(), key=lambda kv: -kv[1]):
            info = bm["_categories"].get(cat, {})
            out.append("  %-18s %5.0f%%  %s" % (cat, w * 100, info.get("label", "")))
            out.extend(_wrap(info.get("why", ""), width, indent="        "))
        return "\n".join(out)

    if topic == "gates":
        out.append("GATES -- findings that cap or void the composite instead of being averaged in")
        out.append("")
        for g in bm.get("_gates", []):
            marker = "VETO   " if g["severity"] == "veto" else "CAP %.1f" % g.get("cap", 0.0)
            out.append("  [%s] %-42s id: %s" % (marker, g["label"], g["id"]))
            out.extend(_wrap("why: " + g.get("why", ""), width, indent="        "))
            out.extend(_wrap("evidence: " + g.get("evidence_needed", ""), width, indent="        "))
            out.append("")
        return "\n".join(out)

    if topic in ("presets", "weights"):
        out.append("WEIGHT PRESETS")
        for name, node in (bm.get("_weight_presets") or {}).items():
            out.append("  %s -- %s" % (name, node.get("note", "")))
            if node.get("weights"):
                out.append("    " + "  ".join("%s=%.2f" % (c, w) for c, w in node["weights"].items()))
        return "\n".join(out)

    # Otherwise: explain a metric within a sector.
    key, sector, warns = resolve_sector(bm, sector_arg)
    for w in warns:
        out.extend(_wrap("! " + w, width))
    spec = sector["metrics"].get(topic)
    if not spec:
        matches = [k for k in sector["metrics"] if topic.lower() in k.lower()]
        out.append("No metric '%s' in sector '%s'." % (topic, key))
        if matches:
            out.append("Did you mean: %s" % ", ".join(sorted(matches)))
        else:
            out.append("Metrics in this sector: %s" % ", ".join(sorted(sector["metrics"])))
        return "\n".join(out)

    out.append("%s  [%s]" % (spec.get("label", topic), topic))
    out.append("  sector    : %s (%s)" % (sector["label"], key))
    out.append("  category  : %s" % spec["category"])
    out.append("  direction : %s" % spec["direction"])
    out.append("  weight    : %.1f (within its category)" % float(spec.get("weight", 1.0)))
    if spec.get("thresholds"):
        out.append("  band      : %s" % _describe_band(spec["direction"], spec["thresholds"]))
        out.append("              (poor=2.5 / average=5.0 / good=7.5 / excellent=10.0)")
    if spec.get("anchors"):
        for level, text in sorted(spec["anchors"].items()):
            out.extend(_wrap("%s/10: %s" % (level, text), width, indent="              "))
    if spec.get("note"):
        out.append("  note      :")
        out.extend(_wrap(spec["note"], width, indent="              "))
    out.append("")
    out.extend(_wrap("This band is an indicative default. If you have a comparable peer set, pass "
                     "peer_values for this metric and the peer percentile will be used instead.", width))
    return "\n".join(out)


EXAMPLE_INPUT = {
    "company": "Example Distribution Ltd",
    "ticker": "NSE:EXAMPLED",
    "as_of": "2026-07-22",
    "basis": "consolidated",
    "currency": "INR",
    "sector": "retail-ecommerce",
    "metrics": {
        "opm_pct": {"value": 4.2, "source": "FY25 AR, consolidated", "period": "FY25"},
        "roce_pct": {"value": 26.0, "source": "computed: EBIT/(net debt+equity+leases)"},
        "roic_wacc_spread_pp": 12.0,
        "cash_conversion_cycle_days": {"value": -18, "note": "Suppliers fund inventory; AR note 14"},
        "cfo_to_pat_3y": {"value": 1.05, "source": "FY23-FY25 cash flow statements"},
        "fcf_margin_pct": 1.9,
        "inventory_days": 58,
        "sssg_pct": {"value": 9.0, "peer_values": [3.0, 4.5, 6.0, 11.0]},
        "store_payback_years": 2.2,
        "store_ebitda_margin_pre_lease_pct": 15.0,
        "net_debt_to_ebitda": {"value": 0.4, "own_history": [1.8, 1.4, 1.1, 0.7], "basis": "own_history"},
        "interest_coverage_x": 11.0,
        "promoter_pledge_pct": 0,
        "promoter_insider_holding_pct": 51.0,
        "dilution_5y_pct": 1.0,
        "capital_allocation_score": {"value": 7.0, "note": "Exited two loss-making formats FY23; no raise since FY21"},
        "disclosure_quality_score": {"value": 6.0, "note": "Segment data adequate; no store-level cohort disclosure"},
        "moat_width_score": {"value": 6.5, "note": "Density advantage in 3 states; share gains 4 straight years"},
        "pricing_power_score": {"value": 5.0, "note": "Passes input costs with a one-quarter lag"},
        "pe_x": 31.0,
        "fcf_yield_pct": 2.4,
        "reverse_dcf_growth_gap_pp": 1.5,
        "cyclicality_resilience_score": {"value": 6.0, "note": "Profitable through FY21 demand shock, no dilution"},
        "platform_disruption_score": {"value": 4.5, "note": "Quick-commerce overlap in 2 of 3 core states"},
    },
    "flags": {"receivables_blowout": {"present": False}},
    "overrides": {
        "category_weights": {"valuation": 0.14, "risk": 0.06, "growth": 0.14},
        "thresholds": {"opm_pct": {"poor": 1.5, "average": 3.0, "good": 5.0, "excellent": 8.0}},
        "note": "Bands narrowed to the Indian organised-distribution peer set, FY25.",
    },
}


EXAMPLE_SEGMENTED_INPUT = {
    "company": "Example Diversified Industries Ltd",
    "ticker": "NSE:EXAMPLEDI",
    "as_of": "2026-07-22",
    "basis": "consolidated",
    "currency": "INR",
    "weight_basis": "ebit",
    "note": ("Three reported segments per the Ind-AS 108 note in the FY25 annual report. "
             "Segment EBIT is segment result before unallocated corporate costs of 1,100 and "
             "inter-segment eliminations of 2,400; both are noted in the report but neither is "
             "large enough to change the mix."),
    "flags": {
        "opaque_structure": {
            "present": True,
            "evidence": "Two unconsolidated JV SPVs in the roads business, FY25 AR note 41; "
                        "combined exposure not disclosed segment-wise.",
        }
    },
    "segments": [
        {
            "name": "EPC & capital goods",
            "sector": "infra-capitalgoods",
            "ebit": 12000,
            "capital_employed": 60000,
            "revenue": 150000,
            "note": "Order book 3.1x revenue; 62% government counterparties.",
            "metrics": {
                "opm_pct": {"value": 8.0, "source": "FY25 AR segment note", "period": "FY25"},
                "roce_pct": {"value": 16.5, "source": "computed: segment EBIT / segment capital employed"},
                "roic_wacc_spread_pp": 3.5,
                "roe_pct": 13.0,
                "gross_margin_pct": 22.0,
                "cfo_to_pat_3y": {"value": 0.78, "source": "FY23-FY25 consolidated cash flow, segment-attributed"},
                "fcf_margin_pct": 1.2,
                "receivable_days": 118,
                "unbilled_revenue_to_revenue_pct": 19.0,
                "accruals_ratio_pct": 6.0,
                "effective_tax_rate_pct": 25.0,
                "net_debt_to_ebitda": 1.9,
                "interest_coverage_x": 3.8,
                "current_ratio": 1.35,
                "bg_lc_to_networth_x": 1.6,
                "cash_conversion_cycle_days": 96,
                "order_book_to_revenue_x": 3.1,
                "order_inflow_growth_pct": 14.0,
                "revenue_cagr_5y_pct": 11.0,
                "roiic_pct": 14.0,
                "moat_width_score": {"value": 4.5, "note": "L1 tendering in most verticals; edge only in "
                                                           "defence electricals where prequalification is scarce"},
                "pricing_power_score": {"value": 3.5, "note": "Fixed-price contracts with partial escalation clauses"},
                "customer_concentration_top5_pct": 44.0,
                "execution_cycle_months": 30,
                "capital_allocation_score": {"value": 5.5, "note": "Exited two BOT road SPVs FY24; still funding "
                                                                   "the lending arm's growth from group cash"},
                "disclosure_quality_score": {"value": 5.0, "note": "Segment result disclosed; segment capital "
                                                                   "employed only partially split"},
                "promoter_pledge_pct": 0,
                "promoter_insider_holding_pct": 54.0,
                "dilution_5y_pct": 2.0,
                "fixed_price_orderbook_pct": 61.0,
                "cyclicality_resilience_score": {"value": 4.5, "note": "Order inflow fell 28% in FY21; margin "
                                                                       "went negative for two quarters"},
                "regulatory_risk_score": {"value": 5.0, "note": "Government receivables subject to budget cycles"},
                "pe_x": 24.0,
                "ev_ebitda_x": 13.0,
                "fcf_yield_pct": 1.1,
                "reverse_dcf_growth_gap_pp": 2.5,
            },
            "flags": {
                "receivables_blowout": {
                    "present": True,
                    "evidence": "Receivables + unbilled up 31% CAGR against 11% revenue CAGR over FY23-FY25; "
                                "FY25 AR notes 12 and 13.",
                }
            },
        },
        {
            "name": "IT services",
            "sector": "it-saas",
            "ebit": 6000,
            "capital_employed": 12000,
            "revenue": 30000,
            "note": "Captive-turned-external engineering services arm; 40% of revenue still intra-group.",
            "metrics": {
                "opm_pct": {"value": 20.0, "source": "FY25 AR segment note", "period": "FY25"},
                "roce_pct": 50.0,
                "roic_wacc_spread_pp": 38.0,
                "roe_pct": 32.0,
                "gross_margin_pct": 34.0,
                "revenue_per_employee_kusd": 48.0,
                "cfo_to_pat_3y": 1.02,
                "fcf_margin_pct": 14.0,
                "accruals_ratio_pct": 2.0,
                "receivable_days_gap_pp": 3.0,
                "effective_tax_rate_pct": 25.5,
                "sbc_to_revenue_pct": 1.5,
                "net_debt_to_ebitda": -1.2,
                "interest_coverage_x": 40.0,
                "current_ratio": 2.1,
                "cash_conversion_cycle_days": 62,
                "revenue_cagr_5y_pct": 17.0,
                "eps_cagr_5y_pct": 19.0,
                "roiic_pct": 41.0,
                "organic_share_of_growth_pct": 88.0,
                "book_to_bill_x": 1.15,
                "moat_width_score": {"value": 5.0, "note": "Engineering domain depth in two verticals; "
                                                           "no proprietary IP, switching costs are moderate"},
                "pricing_power_score": {"value": 4.5, "note": "T&M rates flat in USD for three years"},
                "client_concentration_top10_pct": 58.0,
                "attrition_pct": 17.0,
                "capital_allocation_score": {"value": 6.0, "note": "Cash swept to parent; no acquisitions since FY22"},
                "disclosure_quality_score": {"value": 4.5, "note": "No separate headcount, utilisation or "
                                                                   "constant-currency growth disclosure"},
                "promoter_pledge_pct": 0,
                "promoter_insider_holding_pct": 54.0,
                "dilution_5y_pct": 2.0,
                "ai_disruption_exposure_score": {"value": 4.0, "note": "Large share of revenue in testing and "
                                                                       "maintenance work exposed to code generation"},
                "key_person_dependence_score": {"value": 5.0, "note": "Segment head drove the external-client pivot"},
                "pe_x": 24.0,
                "ev_ebitda_x": 13.0,
                "fcf_yield_pct": 3.0,
                "reverse_dcf_growth_gap_pp": 1.5,
            },
        },
        {
            "name": "Lending arm",
            "sector": "nbfc",
            "ebit": 4000,
            "capital_employed": 28000,
            "revenue": 9000,
            "note": "Equipment finance NBFC, 71% of the book lent against the group's own machinery sales.",
            "metrics": {
                "roa_pct": {"value": 2.2, "source": "FY25 subsidiary financials"},
                "roe_pct": 14.0,
                "nim_pct": 6.4,
                "cost_to_income_pct": 41.0,
                "credit_cost_pct": 1.6,
                "stage3_pct": 3.4,
                "pcr_stage3_pct": 48.0,
                "collection_efficiency_pct": 96.5,
                "restructured_book_pct": 1.8,
                "leverage_x": 4.6,
                "capital_adequacy_pct": 19.0,
                "alm_cumulative_gap_1y_pct": 8.0,
                "liquidity_buffer_months": 3.5,
                "funding_mix_diversification_pct": 62.0,
                "aum_growth_pct": 26.0,
                "book_value_cagr_5y_pct": 15.0,
                "liability_franchise_score": {"value": 4.0, "note": "Bank lines and NCDs only; no retail deposits, "
                                                                    "no rating upgrade since FY22"},
                "borrowing_cost_vs_peer_pp": 0.6,
                "product_niche_score": {"value": 5.5, "note": "Captive origination through the group's dealer "
                                                              "network is a genuine cost advantage, and a "
                                                              "concentration risk in the same breath"},
                "capital_allocation_score": {"value": 4.5, "note": "Book grew 26% while group capital was needed "
                                                                   "for EPC working capital"},
                "disclosure_quality_score": {"value": 4.0, "note": "No vintage or bucket-wise delinquency curves"},
                "promoter_pledge_pct": 0,
                "dilution_5y_pct": 0.0,
                "single_state_concentration_pct": 38.0,
                "unsecured_share_pct": 6.0,
                "rate_sensitivity_score": {"value": 4.5, "note": "Largely fixed-rate book funded at floating rates"},
                "pb_x": 1.8,
                "pe_x": 13.0,
            },
        },
    ],
}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

class _WeightAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        current = dict(getattr(namespace, "weight_overrides", None) or {})
        if "=" not in values:
            parser.error("--weight expects category=value, e.g. --weight valuation=0.20")
        cat, _, val = values.partition("=")
        try:
            current[cat.strip()] = float(val)
        except ValueError:
            parser.error("--weight value must be numeric: %s" % values)
        setattr(namespace, "weight_overrides", current)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="score.py",
        description=("Sector-relative, multi-factor scoring. Every metric is benchmarked against its "
                     "own sector, the company's own history or a supplied peer set -- never against a "
                     "universal absolute. Disqualifying findings cap or void the composite instead of "
                     "being averaged into it."),
        epilog=("Examples:\n"
                "  python score.py input.json\n"
                "  python score.py input.json --json > scorecard.json\n"
                "  python score.py --example > input.json\n"
                "  python score.py --list-sectors\n"
                "  python score.py --explain gates\n"
                "  python score.py --explain roce_pct --sector fmcg-consumer\n"
                "  python score.py input.json --preset deep_value --weight risk=0.10\n"
                "  python score.py --example-segments > seg.json\n"
                "  python score.py seg.json --weight-basis capital_employed --segment-detail\n"),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", nargs="?",
                        help="JSON input file, or '-' for stdin: {sector, metrics, flags, overrides}, "
                             "or {segments: [...]} for a multi-segment group")
    parser.add_argument("--benchmarks", default=DEFAULT_BENCHMARKS,
                        help="path to benchmarks.json (default: alongside this script)")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="emit the full result as JSON instead of the text scorecard")
    parser.add_argument("--list-sectors", action="store_true",
                        help="list the sector keys and their metric counts, then exit")
    parser.add_argument("--explain", nargs="?", const="method", metavar="TOPIC",
                        help="explain the method (default), 'gates', 'presets', or a metric key")
    parser.add_argument("--example", action="store_true",
                        help="print a runnable example input file to stdout, then exit")
    parser.add_argument("--example-segments", action="store_true", dest="example_segments",
                        help="print a runnable multi-segment example (industrial + IT + lending)")
    parser.add_argument("--weight-basis", dest="weight_basis",
                        choices=sorted(WEIGHT_BASIS_FIELDS), default=None,
                        help="how to weight segments: ebit (default), capital_employed, revenue, "
                             "or explicit (a 'weight' field per segment). Overrides 'weight_basis' "
                             "in the input. Falls back automatically if any segment's measure is "
                             "not positive")
    parser.add_argument("--segment-detail", action="store_true", dest="segment_detail",
                        help="also print each segment's full scorecard below the group summary")
    parser.add_argument("--sector", help="override the sector key in the input file")
    parser.add_argument("--preset", help="weight preset: quality_compounder, deep_value, income, forensic")
    parser.add_argument("--weight", action=_WeightAction, dest="weight_overrides", metavar="CAT=VAL",
                        help="override one category weight; repeatable")
    parser.add_argument("--min-coverage", type=float, default=None,
                        help="category-coverage floor for a confident composite (default from benchmarks)")
    parser.add_argument("--no-gates", action="store_true",
                        help="compute the ungated composite for diagnostics; gates are still listed")
    parser.add_argument("--width", type=int, default=108, help="output width in characters (default 108)")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "weight_overrides"):
        args.weight_overrides = {}

    if args.example:
        print(json.dumps(EXAMPLE_INPUT, indent=2, ensure_ascii=False))
        return 0

    if args.example_segments:
        print(json.dumps(EXAMPLE_SEGMENTED_INPUT, indent=2, ensure_ascii=False))
        return 0

    try:
        bm = load_benchmarks(args.benchmarks)
    except ScoringError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2

    if args.list_sectors:
        print("Sector keys in %s\n" % args.benchmarks)
        for key in sector_keys(bm):
            _, sector, _ = resolve_sector(bm, key)
            standalone = "standalone" if not bm[key].get("extends") else "extends %s" % bm[key]["extends"]
            print("  %-22s %3d metrics  (%s)" % (key, len(sector["metrics"]), standalone))
            for line in _wrap(sector["label"], args.width, indent="      "):
                print(line)
        print("\nUnknown keys fall back to 'generic' with a warning. 'generic' is not valid for")
        print("banks, nbfc, insurance or realestate-reit -- those need their own key.")
        return 0

    if args.explain is not None:
        sector_arg = args.sector
        if not sector_arg and args.input and os.path.exists(args.input):
            try:
                with open(args.input, "r", encoding="utf-8") as handle:
                    sector_arg = json.load(handle).get("sector")
            except Exception:
                sector_arg = None
        try:
            print(explain(bm, args.explain, sector_arg, args.width))
        except ScoringError as exc:
            print("error: %s" % exc, file=sys.stderr)
            return 2
        return 0

    if not args.input:
        parser.error("an input JSON file is required (or use --example, --example-segments, "
                     "--list-sectors, --explain)")

    try:
        if args.input == "-":
            payload = json.load(sys.stdin)
        else:
            with open(args.input, "r", encoding="utf-8") as handle:
                payload = json.load(handle)
    except FileNotFoundError:
        print("error: input file not found: %s" % args.input, file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print("error: input is not valid JSON: %s" % exc, file=sys.stderr)
        return 2

    # Auto-detect the shape: a 'segments' array switches to segmented scoring, and
    # its absence leaves the single-sector path byte-identical to what it always was.
    segmented = isinstance(payload, dict) and bool(payload.get("segments"))

    try:
        if segmented:
            result = run_segmented_scorecard(bm, payload, args)
        else:
            if args.weight_basis or args.segment_detail:
                print("note: --weight-basis/--segment-detail apply only to input with a 'segments' "
                      "array; ignored here.", file=sys.stderr)
            result = run_scorecard(bm, payload, args)
    except ScoringError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2

    if segmented:
        print(render_segmented_json(result) if args.as_json
              else render_segmented_text(result, args.width, args.segment_detail))
    else:
        print(render_json(result) if args.as_json else render_text(result, args.width))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
