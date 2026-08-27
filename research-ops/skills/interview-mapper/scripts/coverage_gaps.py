#!/usr/bin/env python3
"""
coverage_gaps.py — which chunks of the transcript reached NO cell of the mapping.

Omissions are more dangerous than fabrications (omission 3.45% vs hallucination 1.47%, see
references/reliability.md), yet the omission check was the one pipeline step without a tool: the
model looked for what it missed by eye across the whole text — the same way it missed it.

Computed mechanically: takes the quotes verify_quotes confirmed, locates them in the text, and
returns the blocks of utterances none of them covered. This is not a verdict ("everything uncovered
is an omission"): the interviewer, greetings and small talk are not supposed to land in a cell.
It is a list of places that MUST be eyeballed, sorted so you read from the top.

Input claims.json — the same one verify_quotes takes (preferably its `--emit-enriched` output,
where statuses are already set). Quotes whose status is not verified do not count as coverage: a
rejected quote confirms nothing.

CLI:
  python coverage_gaps.py --transcript T_nl.txt --claims claims.json [--min-block 3]
                          [--skip-speaker "Interviewer|Moderator"] [--out gaps.json]
                          [--output {human,json}]
  python coverage_gaps.py --sample
"""

import argparse
import importlib.util
import json
import os
import re
import sys

_VQ_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_quotes.py")

SAMPLE_TRANSCRIPT = "\n".join(
    [
        "L1: Interviewer: Tell me about the reports",
        "L2: Respondent: I put the report together by hand every Friday evening",
        "L3: Interviewer: And the leads?",
        "L4: Respondent: We lose leads every single day",
        "L5: Interviewer: What else gets in the way?",
        "L6: Respondent: Nobody knows where the current data lives",
        "L7: Respondent: Sign-offs drag on for weeks with no explanation",
        "L8: Respondent: Half the work goes into email threads",
    ]
)

SAMPLE_CLAIMS = [
    {"cell": "K1", "quote": "I put the report together by hand every Friday evening"},
    {"cell": "K2", "quote": "We lose leads every single day"},
]


def _load_verify_quotes():
    """Loads the sibling verify_quotes.py: normalization and the line index must be THE SAME."""
    spec = importlib.util.spec_from_file_location("_vq_for_coverage_gaps", _VQ_PATH)
    if spec is None or spec.loader is None:
        sys.exit(f"error: {_VQ_PATH} not found")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _read_text(path):
    """Reads a text file or exits with a clear error."""
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError as e:
        sys.exit(f"error: {path}: {e.strerror or e}")
    except UnicodeDecodeError as e:
        sys.exit(f"error: {path}: not UTF-8 ({e.reason})")


def _read_json(path):
    """Reads a JSON file; malformed JSON or a missing file → a clear error, exit 1."""
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


def covered_lines(vq, claims, norm_full, index, threshold=88.0, min_cov=0.6):
    """The set of line numbers covered by confirmed quotes.

    A fuzzy match counts only against the same thresholds verify_quotes uses: without them any
    fabrication would "cover" arbitrary lines and mask the very omission being looked for.
    """
    covered, unlocated = set(), []
    for c in claims:
        status = str(c.get("status") or c.get("verify_status") or "").lower()
        if status and not status.startswith("verified"):
            continue  # a rejected quote confirms nothing
        qn = vq.normalize(c.get("quote") or "")
        if not qn:
            continue
        pos = norm_full.find(qn)
        span = len(qn)
        if pos == -1:
            score, matched = vq.fuzzy_score(qn, norm_full)
            cov = vq.lcs_coverage(qn, matched) if matched else 0.0
            if score < threshold or cov < min_cov:
                matched = ""
            pos = norm_full.find(matched) if matched else -1
            span = len(matched) if matched else 0
        if pos == -1:
            unlocated.append(c.get("cell"))
            continue
        for p in range(pos, pos + max(span, 1)):
            ln = vq.locate_line(p, index)
            if ln is not None:
                covered.add(ln)
    return covered, unlocated


def find_gaps(lines, covered, min_block, skip_re):
    """Blocks of uncovered utterances of length >= min_block, longest first.

    Only a COVERED line breaks a block. Blank lines and interviewer turns are not part of a block
    but do not break it either: in a dialogue the respondent's answers come every other line, and
    treating the interviewer as a break makes a block physically never longer than one line — the
    counter would always read zero.
    """
    gaps, current = [], []
    for ln, txt in lines:
        if ln in covered:
            if len(current) >= min_block:
                gaps.append(current)
            current = []
            continue
        if not txt.strip() or (skip_re and skip_re.search(txt)):
            continue
        current.append((ln, txt))
    if len(current) >= min_block:
        gaps.append(current)
    gaps.sort(key=len, reverse=True)
    return gaps


def main():
    """CLI: computes uncovered transcript blocks and prints them largest first."""
    ap = argparse.ArgumentParser(
        description="Find transcript chunks covered by no confirmed quote."
    )
    ap.add_argument("--transcript")
    ap.add_argument("--claims")
    ap.add_argument(
        "--min-block",
        type=int,
        default=3,
        help="Minimum uncovered utterances in a row to count as an omission",
    )
    ap.add_argument(
        "--skip-speaker",
        default=None,
        help="Regex for turns that are not supposed to land in a cell (e.g. 'Interviewer|Moderator')",
    )
    ap.add_argument("--out", default=None)
    ap.add_argument(
        "--sample",
        action="store_true",
        help="Run on a built-in sample transcript and claims, no input files needed",
    )
    ap.add_argument(
        "--output", choices=["human", "json"], default="json", help="Output format"
    )
    a = ap.parse_args()

    vq = _load_verify_quotes()
    if a.sample:
        lines = vq.parse_lines(SAMPLE_TRANSCRIPT)
        claims = SAMPLE_CLAIMS
    else:
        if not (a.transcript and a.claims):
            sys.exit(
                "error: --transcript and --claims are required unless --sample is given"
            )
        lines = vq.parse_lines(_read_text(a.transcript))
        claims = _read_json(a.claims)
    if not lines:
        sys.exit(f"error: {a.transcript}: empty transcript")
    norm_full, index = vq.build_index(lines)
    skip_pattern = a.skip_speaker or ("Interviewer|Moderator" if a.sample else None)
    skip_re = re.compile(skip_pattern, re.IGNORECASE) if skip_pattern else None

    covered, unlocated = covered_lines(vq, claims, norm_full, index)
    gaps = find_gaps(lines, covered, a.min_block, skip_re)

    total = len(lines)
    gap_lines = sum(len(g) for g in gaps)
    out = {
        "summary": {
            "transcript_lines": total,
            "covered_lines": len(covered),
            "coverage_share": round(len(covered) / total, 3) if total else 0.0,
            "gap_blocks": len(gaps),
            "gap_lines": gap_lines,
            "unlocated_claims": unlocated,
            "note": (
                "An uncovered block is not a verdict but a place to look at with your own eyes: "
                "small talk and interviewer turns are not supposed to land in a cell (--skip-speaker). "
                "An omission is worse than a fabrication: verify_quotes catches fabrications, only "
                "this step catches omissions. unlocated_claims — quotes absent from this transcript: "
                "wrong interview, or the text was swapped after mapping (e.g. de-identified — see "
                "references/ethics.md)."
            ),
        },
        "gaps": [
            {
                "from_line": g[0][0],
                "to_line": g[-1][0],
                "lines": len(g),
                "text": " ".join(t for _, t in g)[:400],
            }
            for g in gaps
        ],
    }
    js = json.dumps(out, ensure_ascii=False, indent=2)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(js)

    if a.output == "json":
        print(js)
    else:
        sm = out["summary"]
        print(
            f"Coverage: {sm['covered_lines']}/{sm['transcript_lines']} lines "
            f"({sm['coverage_share']:.0%}) | uncovered blocks: {sm['gap_blocks']}"
        )
        for g in out["gaps"]:
            print(
                f"  L{g['from_line']}-{g['to_line']} ({g['lines']}): {g['text'][:100]}"
            )
        if sm["unlocated_claims"]:
            print(f"  Quotes absent from this transcript: {sm['unlocated_claims']}")


if __name__ == "__main__":
    main()
