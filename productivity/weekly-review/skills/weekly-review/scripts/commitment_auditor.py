#!/usr/bin/env python3
"""commitment_auditor.py — Audit a commitment portfolio: flags, health score, one honest verdict.

Step 8 of the weekly review (review project lists) in numbers. Reads a JSON list of commitments:

    [{"name": "Website relaunch", "days_since_touched": 3, "has_next_action": true}, ...]

and flags each one:

  STALLED            days_since_touched > 14  (a week-and-a-half of silence is drift, not rest)
  NO-NEXT-ACTION     has_next_action is false (a project with no next action is a wish)
  SOMEDAY-CANDIDATE  days_since_touched > 45  (be honest: activate it or move it to someday/maybe)

Then computes a 0-100 commitment-health score. The formula is printed with the output so the
number is auditable, never mystical:

    score = 100 - 30*(stalled/total) - 40*(no_next_action/total) - 30*(someday/total)

(SOMEDAY-CANDIDATEs also count as STALLED — the double penalty is deliberate escalation.)

Verdict:  HEALTHY (>= 80) · DRIFTING (50-79) · OVERCOMMITTED (< 50)

Deterministic logic. No LLM calls, no network. Stdlib only.

Usage:
    python commitment_auditor.py --input commitments.json
    python commitment_auditor.py --input commitments.json --json
    python commitment_auditor.py --sample

Exit codes:
    0  audit complete (any verdict) — also --sample / --help
    2  input file missing, unreadable, or not the expected JSON shape
"""

import argparse
import json
import sys
from typing import Any, Dict, List

STALLED_DAYS = 14
SOMEDAY_DAYS = 45

FORMULA = ("score = 100 - 30*(stalled/total) - 40*(no_next_action/total) "
           "- 30*(someday_candidates/total)")

SAMPLE_COMMITMENTS = [
    {"name": "Website relaunch", "days_since_touched": 3, "has_next_action": True},
    {"name": "Q3 budget draft", "days_since_touched": 9, "has_next_action": True},
    {"name": "Hire a designer", "days_since_touched": 21, "has_next_action": False},
    {"name": "Learn Spanish", "days_since_touched": 41, "has_next_action": True},
    {"name": "Write a novel", "days_since_touched": 63, "has_next_action": False},
    {"name": "Renew passports", "days_since_touched": 2, "has_next_action": True},
]


def validate(data: Any) -> List[Dict[str, Any]]:
    if not isinstance(data, list) or not data:
        raise ValueError("input must be a non-empty JSON list of commitment objects")
    for i, c in enumerate(data):
        if not isinstance(c, dict):
            raise ValueError(f"entry {i} is not an object")
        for key in ("name", "days_since_touched", "has_next_action"):
            if key not in c:
                raise ValueError(f"entry {i} ({c.get('name', '?')!r}) missing key: {key!r}")
        if not isinstance(c["days_since_touched"], (int, float)) or c["days_since_touched"] < 0:
            raise ValueError(f"entry {i}: days_since_touched must be a non-negative number")
        if not isinstance(c["has_next_action"], bool):
            raise ValueError(f"entry {i}: has_next_action must be true or false")
    return data


def audit(commitments: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(commitments)
    rows = []
    n_stalled = n_no_action = n_someday = 0
    for c in commitments:
        flags = []
        if c["days_since_touched"] > STALLED_DAYS:
            flags.append("STALLED")
            n_stalled += 1
        if not c["has_next_action"]:
            flags.append("NO-NEXT-ACTION")
            n_no_action += 1
        if c["days_since_touched"] > SOMEDAY_DAYS:
            flags.append("SOMEDAY-CANDIDATE")
            n_someday += 1
        rows.append({"name": c["name"],
                     "days_since_touched": c["days_since_touched"],
                     "has_next_action": c["has_next_action"],
                     "flags": flags})

    score = 100.0 - 30.0 * (n_stalled / total) - 40.0 * (n_no_action / total) \
        - 30.0 * (n_someday / total)
    score = round(max(0.0, min(100.0, score)), 1)

    if score >= 80:
        verdict = "HEALTHY"
        headline = ("The portfolio is honest: most commitments are moving and have a next "
                    "action. Keep the cadence.")
    elif score >= 50:
        verdict = "DRIFTING"
        headline = ("Several commitments are coasting on good intentions. Give each flagged "
                    "item a next action, a waiting-for, or a someday/maybe home this review.")
    else:
        verdict = "OVERCOMMITTED"
        headline = ("More commitments than attention. Kill or park the SOMEDAY-CANDIDATEs, "
                    "then rebuild next actions for what survives — fewer, moving projects "
                    "beat many, stalled ones.")

    return {
        "total_commitments": total,
        "flag_counts": {"STALLED": n_stalled, "NO-NEXT-ACTION": n_no_action,
                        "SOMEDAY-CANDIDATE": n_someday},
        "thresholds": {"stalled_days": STALLED_DAYS, "someday_days": SOMEDAY_DAYS},
        "commitments": rows,
        "formula": FORMULA,
        "health_score": score,
        "verdict": verdict,
        "headline": headline,
    }


def render_human(r: Dict[str, Any]) -> str:
    out = ["Commitment Auditor (project lists in numbers)", "=" * 64]
    out.append(f"  Commitments: {r['total_commitments']}   "
               f"Stalled > {r['thresholds']['stalled_days']}d · "
               f"Someday-candidate > {r['thresholds']['someday_days']}d")
    out.append("")
    for c in r["commitments"]:
        mark = "OK " if not c["flags"] else "!! "
        flags = f"  [{', '.join(c['flags'])}]" if c["flags"] else ""
        out.append(f"  {mark}{c['name']}  — {c['days_since_touched']}d since touched, "
                   f"next action: {'yes' if c['has_next_action'] else 'NO'}{flags}")
    fc = r["flag_counts"]
    out.append("")
    out.append(f"  Flags: STALLED {fc['STALLED']} · NO-NEXT-ACTION {fc['NO-NEXT-ACTION']} · "
               f"SOMEDAY-CANDIDATE {fc['SOMEDAY-CANDIDATE']}")
    out.append(f"  Formula: {r['formula']}")
    out.append(f"  COMMITMENT HEALTH: {r['health_score']}/100    VERDICT: {r['verdict']}")
    out.append("")
    out.append(f"  {r['headline']}")
    return "\n".join(out)


def main(argv: List[str]) -> int:
    p = argparse.ArgumentParser(
        description="Audit commitments: STALLED / NO-NEXT-ACTION / SOMEDAY-CANDIDATE flags + 0-100 health score.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", help="Path to a JSON list of "
                   '{"name", "days_since_touched", "has_next_action"} objects')
    p.add_argument("--sample", action="store_true", help="Run on embedded example data and exit 0")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    args = p.parse_args(argv)

    try:
        if args.sample:
            commitments = validate(SAMPLE_COMMITMENTS)
        elif args.input:
            with open(args.input, "r", encoding="utf-8") as f:
                commitments = validate(json.load(f))
        else:
            p.print_help()
            print("\nerror: provide --input <file.json> or --sample", file=sys.stderr)
            return 2
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    result = audit(commitments)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render_human(result))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
