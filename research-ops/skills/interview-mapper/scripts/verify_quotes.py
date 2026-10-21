#!/usr/bin/env python3
"""
verify_quotes.py — verbatim verification of mapping quotes WITHOUT external APIs.

Cascade (cheap → expensive), inspired by LLMCode / DeTAILS + fuzzy practices:
  1) normalization (case, punctuation, fillers, spaces) + exact match → verified_exact
  2) fuzzy substring (difflib) → verified_fuzzy (+coordinates, line)
  3) coverage check via LCS share (guard against the leniency of token metrics)
  4) otherwise → rejected  (or paraphrase, if --semantic-hint is given)

Verbatim != support. This script checks ONLY verbatim-ness.
The «quote ⊨ claim» (entailment) check is done by the model as a separate step (see SKILL.md).

Dependencies: stdlib only (difflib).

CLI:
  python verify_quotes.py --transcript T.txt --claims claims.json [--threshold 88]
                          [--min-coverage 0.6] [--window 6] [--out result.json]

Formats:
  transcript: plain text. If lines start with "L12: " or "12\t", the line number is recognized.
  claims.json: [{"cell":"К5","claim":"...","quote":"...","line":61}]  (line — optional)
Output: JSON with a status for each quote.
"""

import argparse
import json
import re
import sys
import unicodedata
from difflib import SequenceMatcher


def _read_text(path):
    """Read a text file, or exit with a clear error."""
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError as e:
        sys.exit(f"error: {path}: {e.strerror or e}")
    except UnicodeDecodeError as e:
        sys.exit(f"error: {path}: not UTF-8 ({e.reason})")


def _read_json(path):
    """Read a JSON file; broken JSON or a missing file → a clear error, exit 1."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except OSError as e:
        sys.exit(f"error: {path}: {e.strerror or e}")
    except UnicodeDecodeError as e:
        sys.exit(f"error: {path}: not UTF-8 ({e.reason})")
    except json.JSONDecodeError as e:
        sys.exit(
            f"error: {path}: invalid JSON — line {e.lineno}, column {e.colno} ({e.msg})"
        )


FILLERS = {
    # ru
    "ну",
    "вот",
    "как бы",
    "типа",
    "короче",
    "это самое",
    "в общем",
    "эээ",
    "ээ",
    "мм",
    "ммм",
    "то есть",
    "так сказать",
    "знаете",
    "понимаете",
    "скажем так",
    # en
    "um",
    "uh",
    "erm",
    "you know",
    "like",
    "sort of",
    "kind of",
    "i mean",
    "as you know",
    "basically",
    "actually",
}


def strip_accents(s: str) -> str:
    """Strips diacritics via NFKD decomposition."""
    return "".join(
        c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)
    )


def normalize(s: str) -> str:
    """lowercase, ё→е, strip punctuation, fillers, collapse spaces."""
    s = s.lower().replace("ё", "е")
    s = strip_accents(s)
    s = re.sub(r"[«»\"'`”“„.,;:!?()\[\]{}\-—–…/\\|]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    if s:
        # remove fillers as standalone tokens/bigrams
        for f in sorted(FILLERS, key=len, reverse=True):
            s = re.sub(rf"(?<!\w){re.escape(f)}(?!\w)", " ", s)
        s = re.sub(r"\s+", " ", s).strip()
    return s


def parse_lines(text: str):
    """Returns a list of (line_no, original_line). Recognizes prefixes 'L12: ' and '12\\t'."""
    out = []
    for i, raw in enumerate(text.splitlines(), 1):
        m = re.match(r"^\s*L?(\d+)[:\t]\s?(.*)$", raw)
        if m:
            out.append((int(m.group(1)), m.group(2)))
        else:
            out.append((i, raw))
    return out


def fuzzy_score(needle: str, hay: str):
    """Returns (score 0..100, matched_substring_in_hay)."""
    if not needle or not hay:
        return 0.0, ""
    # autojunk=False is required: on hay >200 chars the heuristic marks frequent characters
    # (space, vowels) as "junk" and matching falls apart — the score of one and the same
    # quote swings 0..96 depending on its position in the text.
    sm = SequenceMatcher(None, needle, hay, autojunk=False)
    blocks = sm.get_matching_blocks()
    best = max(blocks, key=lambda b: b.size) if blocks else None
    if not best or best.size == 0:
        return 0.0, ""
    # The window spans the QUOTE length from the presumed start (best.b - best.a), not the
    # matched block length: a single dropped word splits the quote into two blocks, and a
    # block-sized window would compare the quote against half of itself.
    start = max(0, best.b - best.a)
    end = min(len(hay), start + len(needle))
    window = hay[start:end]
    score = SequenceMatcher(None, needle, window, autojunk=False).ratio() * 100
    return score, window


def lcs_coverage(needle: str, hay: str) -> float:
    """Share of the quote covered by the longest common fragment (0..1)."""
    if not needle:
        return 0.0
    sm = SequenceMatcher(None, needle, hay, autojunk=False)
    total = sum(b.size for b in sm.get_matching_blocks())
    return min(1.0, total / max(1, len(needle)))


def verify_one(
    quote, lines, norm_full, line_index, threshold, min_cov, window, claimed_line
):
    """Verifies a single quote via the exact → fuzzy → rejected cascade."""
    qn = normalize(quote)
    if not qn:
        return {"status": "empty", "score": 0}
    # 1) exact normalized
    pos = norm_full.find(qn)
    if pos != -1:
        ln = locate_line(pos, line_index)
        return {
            "status": "verified_exact",
            "score": 100,
            "line_found": ln,
            "matched": quote.strip(),
            "coverage": 1.0,
            "line_ok": line_ok(ln, claimed_line, window),
        }
    # 2) fuzzy — over a window around the claimed line if present, otherwise over the whole text
    hay = norm_full
    if claimed_line is not None:
        hay = window_text(lines, claimed_line, window)
        hay_n = normalize(hay)
        score, matched = fuzzy_score(qn, hay_n)
        if score < threshold:  # window didn't match — try the whole text
            score, matched = fuzzy_score(qn, norm_full)
            hay_n = norm_full
    else:
        score, matched = fuzzy_score(qn, norm_full)
        hay_n = norm_full
    cov = lcs_coverage(qn, matched) if matched else 0.0
    if score >= threshold and cov >= min_cov:
        pos2 = norm_full.find(matched) if matched else -1
        ln = locate_line(pos2, line_index) if pos2 != -1 else None
        return {
            "status": "verified_fuzzy",
            "score": round(score, 1),
            "coverage": round(cov, 2),
            "line_found": ln,
            "matched": matched,
            "line_ok": line_ok(ln, claimed_line, window),
        }
    return {
        "status": "rejected",
        "score": round(score, 1),
        "coverage": round(cov, 2),
        "line_found": None,
        "matched": matched,
    }


def window_text(lines, center_line, k):
    """Returns a ±k line window around the claimed line (or the whole text if the line isn't found)."""
    nums = [ln for ln, _ in lines]
    if center_line not in nums:
        return " ".join(t for _, t in lines)
    idx = nums.index(center_line)
    lo, hi = max(0, idx - k), min(len(lines), idx + k + 1)
    return " ".join(t for _, t in lines[lo:hi])


def build_index(lines):
    """Builds the normalized full text and a position->line-number map."""
    parts, index = [], []
    cursor = 0
    for ln, txt in lines:
        nt = normalize(txt)
        if not nt:
            continue
        parts.append(nt)
        index.append((cursor, cursor + len(nt), ln))
        cursor += len(nt) + 1  # +1 for the space separator
    return " ".join(parts), index


def locate_line(pos, index):
    """Given a position in the normalized full text, finds the original line number."""
    for start, end, ln in index:
        if start <= pos <= end:
            return ln
    return index[-1][2] if index else None


def line_ok(found, claimed, k):
    """True/False whether the found line falls within ±k of the claimed line; None if there's nothing to compare."""
    if claimed is None or found is None:
        return None
    return abs(found - claimed) <= k


def main():
    """CLI: parses arguments, verifies all quotes, and prints/writes the result."""
    ap = argparse.ArgumentParser(
        description="Verify mapping quotes against a transcript, verbatim-ness only."
    )
    ap.add_argument(
        "--transcript", default=None, help="Required unless --sample is given"
    )
    ap.add_argument(
        "--claims",
        default=None,
        help="JSON: list of {cell,claim,quote,line?}; required unless --sample",
    )
    ap.add_argument(
        "--threshold",
        type=float,
        default=88.0,
        help="Fuzzy threshold (calibrate! 0..100)",
    )
    ap.add_argument(
        "--min-coverage",
        type=float,
        default=0.6,
        help="Min. share of the quote covered by a verbatim fragment",
    )
    ap.add_argument(
        "--window", type=int, default=6, help="±lines around the claimed line"
    )
    ap.add_argument("--out", default=None)
    ap.add_argument(
        "--emit-enriched",
        default=None,
        help="Path: write claims with the line filled in (line_found). "
        "The model must NOT guess the line number — the script sets it.",
    )
    ap.add_argument(
        "--sample",
        action="store_true",
        help="Run on a built-in sample transcript + claims",
    )
    ap.add_argument(
        "--output",
        choices=["human", "json"],
        default="json",
        help="Output format (default json — this script's stdout is machine-consumed by calibrate_threshold.py)",
    )
    a = ap.parse_args()

    if a.sample:
        text = (
            "L1: Interviewer: Tell me about the last time you tried to reconcile the budget.\n"
            "L2: Respondent: Honestly, I opened three tabs and gave up after twenty minutes.\n"
            "L3: Interviewer: What made you give up?\n"
            "L4: Respondent: The export didn't match what I saw on screen, so I stopped trusting it.\n"
        )
        claims = [
            {
                "cell": "K1",
                "claim": "gave up reconciling",
                "quote": "I opened three tabs and gave up after twenty minutes",
                "line": 2,
            },
            {
                "cell": "A1",
                "claim": "lost trust in the export",
                "quote": "The export didn't match what I saw on screen",
                "line": 4,
            },
            {
                "cell": "X1",
                "claim": "fabricated for the demo",
                "quote": "I have never once opened a spreadsheet in my life",
            },
        ]
    else:
        if not a.transcript or not a.claims:
            sys.exit(
                "error: --transcript and --claims are required unless --sample is given"
            )
        text = _read_text(a.transcript)
        claims = _read_json(a.claims)
    lines = parse_lines(text)
    norm_full, index = build_index(lines)

    results = []
    for c in claims:
        r = verify_one(
            c.get("quote", ""),
            lines,
            norm_full,
            index,
            a.threshold,
            a.min_coverage,
            a.window,
            c.get("line"),
        )
        r["cell"] = c.get("cell")
        r["claim"] = (c.get("claim", "") or "")[:120]
        r["quote"] = c.get("quote", "")
        results.append(r)

    n = len(results)
    ok = sum(1 for r in results if r["status"].startswith("verified"))
    summary = {
        "backend": "difflib",
        "total": n,
        "verified": ok,
        "rejected": n - ok,
        "verified_share": round(ok / n, 3) if n else 0.0,
        "rejected_cells": [r["cell"] for r in results if r["status"] == "rejected"],
        "line_mismatches": [r["cell"] for r in results if r.get("line_ok") is False],
    }
    out = {"summary": summary, "results": results}
    js = json.dumps(out, ensure_ascii=False, indent=2)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(js)
    if a.emit_enriched:
        enriched = []
        for c, r in zip(claims, results):
            e = dict(c)
            e["line"] = r.get("line_found")  # authority is the script, not the model
            e["verify_status"] = r["status"]
            enriched.append(e)
        open(a.emit_enriched, "w", encoding="utf-8").write(
            json.dumps(enriched, ensure_ascii=False, indent=2)
        )

    if a.output == "json":
        print(js)
    else:
        print(f"Verified: {ok}/{n} ({summary['verified_share']:.0%})")
        if summary["rejected_cells"]:
            print(f"  Rejected: {summary['rejected_cells']}")
        if summary["line_mismatches"]:
            print(f"  Line mismatches: {summary['line_mismatches']}")
        if a.out:
            print(f"  → {a.out}")


if __name__ == "__main__":
    main()
