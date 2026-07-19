#!/usr/bin/env python3
"""weekly_review_gate.py — Gate a GTD weekly review: completion %, named gaps, one honest verdict.

Encodes David Allen's weekly-review checklist as three phases and ten numbered steps:

  GET CLEAR    1. Collect loose inputs (papers, receipts, notes, downloads)
               2. Process inboxes to zero (clarify, don't do)
               3. Empty your head (mind sweep — capture everything still riding in RAM)
  GET CURRENT  4. Review next-action lists (mark done, prune dead, surface stuck)
               5. Review previous calendar (missed/spawned commitments become actions)
               6. Review upcoming calendar (prepare, don't react)
               7. Review waiting-for list (chase, re-date, or drop each item)
               8. Review project lists (every active project has exactly one next action)
  GET CREATIVE 9. Review someday/maybe (activate, keep, or kill)
              10. Capture new ideas (add to the system while your head is clear)

The gate's one hard rule: ALL FIVE GET CURRENT steps (4-8) are mandatory. A GET CURRENT step that
is neither done nor explicitly skipped with a reason ALWAYS forces INCOMPLETE — a review that
skims the core is a guilt ritual, not a review.

Deterministic logic. No LLM calls. Stdlib only.

Usage:
    python weekly_review_gate.py --list
    python weekly_review_gate.py --done "1,2,3,4,5,6,7,8,10" --skip "9:no someday list yet"
    python weekly_review_gate.py --done "1,4,6" --json
    python weekly_review_gate.py --sample

Exit codes:
    0  review COMPLETE (every step done or skipped with a reason) — also --list / --sample / --help
    2  review INCOMPLETE (at least one step neither done nor skipped)
    3  bad input (unknown step number, malformed --done/--skip, step both done and skipped)
"""

import argparse
import json
import sys
from typing import Any, Dict, List

STEPS = [
    (1, "GET CLEAR", "Collect loose inputs (papers, receipts, notes, downloads)"),
    (2, "GET CLEAR", "Process inboxes to zero (clarify, don't do)"),
    (3, "GET CLEAR", "Empty your head (mind sweep — capture everything still in RAM)"),
    (4, "GET CURRENT", "Review next-action lists (mark done, prune dead, surface stuck)"),
    (5, "GET CURRENT", "Review previous calendar (missed/spawned commitments become actions)"),
    (6, "GET CURRENT", "Review upcoming calendar (prepare, don't react)"),
    (7, "GET CURRENT", "Review waiting-for list (chase, re-date, or drop each item)"),
    (8, "GET CURRENT", "Review project lists (every active project has one next action)"),
    (9, "GET CREATIVE", "Review someday/maybe (activate, keep, or kill)"),
    (10, "GET CREATIVE", "Capture new ideas (add them while your head is clear)"),
]

MANDATORY_PHASE = "GET CURRENT"
PHASE_ORDER = ["GET CLEAR", "GET CURRENT", "GET CREATIVE"]


def parse_done(raw: str) -> List[int]:
    if not raw or not raw.strip():
        return []
    nums = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if not part.isdigit():
            raise ValueError(f"--done entries must be step numbers, got: {part!r}")
        nums.append(int(part))
    return sorted(set(nums))


def parse_skips(raw_list: List[str]) -> Dict[int, str]:
    skips: Dict[int, str] = {}
    for raw in raw_list or []:
        if ":" not in raw:
            raise ValueError(f"--skip must be 'N:reason', got: {raw!r}")
        num_s, reason = raw.split(":", 1)
        num_s, reason = num_s.strip(), reason.strip()
        if not num_s.isdigit():
            raise ValueError(f"--skip step must be a number, got: {num_s!r}")
        if not reason:
            raise ValueError(f"--skip requires a non-empty reason: {raw!r}")
        skips[int(num_s)] = reason
    return skips


def evaluate(done: List[int], skips: Dict[int, str]) -> Dict[str, Any]:
    valid = {n for n, _, _ in STEPS}
    for n in done:
        if n not in valid:
            raise ValueError(f"unknown step number in --done: {n} (valid: 1-10)")
    for n in skips:
        if n not in valid:
            raise ValueError(f"unknown step number in --skip: {n} (valid: 1-10)")
    overlap = set(done) & set(skips)
    if overlap:
        raise ValueError(f"step(s) both done and skipped: {sorted(overlap)}")

    rows = []
    missing: List[Dict[str, Any]] = []
    for n, phase, label in STEPS:
        if n in done:
            status = "DONE"
        elif n in skips:
            status = "SKIPPED"
        else:
            status = "MISSING"
            missing.append({"step": n, "phase": phase, "label": label})
        rows.append({"step": n, "phase": phase, "label": label, "status": status,
                     "skip_reason": skips.get(n)})

    considered = len(STEPS) - len(skips)
    completion_pct = round(100.0 * len(done) / considered, 1) if considered else 100.0

    missing_mandatory = [m for m in missing if m["phase"] == MANDATORY_PHASE]
    skipped_mandatory = [n for n in skips if 4 <= n <= 8]

    verdict = "COMPLETE" if not missing else "INCOMPLETE"
    forced = bool(missing_mandatory)

    warnings = []
    if skipped_mandatory:
        warnings.append(
            f"GET CURRENT step(s) {sorted(skipped_mandatory)} skipped with a reason — "
            "allowed, but the core of the review was not fully walked. Do them first next week."
        )
    if forced:
        warnings.append(
            "Unskipped GET CURRENT step(s) missing — this ALWAYS forces INCOMPLETE, "
            "regardless of completion %."
        )

    return {
        "steps": rows,
        "done_count": len(done),
        "skipped_count": len(skips),
        "missing_count": len(missing),
        "completion_pct": completion_pct,
        "missing_steps": missing,
        "missing_mandatory": missing_mandatory,
        "mandatory_gate_forced_incomplete": forced,
        "warnings": warnings,
        "verdict": verdict,
        "exit_code": 0 if verdict == "COMPLETE" else 2,
    }


def render_list() -> str:
    out = ["GTD Weekly Review — the ten steps", "=" * 64]
    for phase in PHASE_ORDER:
        tag = " (all mandatory)" if phase == MANDATORY_PHASE else ""
        out.append(f"\n{phase}{tag}")
        for n, p, label in STEPS:
            if p == phase:
                out.append(f"  {n:>2}. {label}")
    out.append("\nMark progress with --done \"1,2,3\" and --skip \"N:reason\".")
    return "\n".join(out)


def render_human(r: Dict[str, Any]) -> str:
    out = ["Weekly Review Gate (GET CLEAR -> GET CURRENT -> GET CREATIVE)", "=" * 64]
    current_phase = None
    for row in r["steps"]:
        if row["phase"] != current_phase:
            current_phase = row["phase"]
            tag = " (mandatory)" if current_phase == MANDATORY_PHASE else ""
            out.append(f"\n  {current_phase}{tag}")
        mark = {"DONE": "[x]", "SKIPPED": "[s]", "MISSING": "[ ]"}[row["status"]]
        line = f"    {mark} {row['step']:>2}. {row['label']}"
        if row["status"] == "SKIPPED":
            line += f"  (skipped: {row['skip_reason']})"
        out.append(line)
    out.append("")
    out.append(f"  Completion: {r['completion_pct']}%  "
               f"(done {r['done_count']} · skipped {r['skipped_count']} · missing {r['missing_count']})")
    if r["missing_steps"]:
        out.append("\n  Missing steps (do these to finish):")
        for m in r["missing_steps"]:
            star = "  <- MANDATORY" if m["phase"] == MANDATORY_PHASE else ""
            out.append(f"    - {m['step']}. [{m['phase']}] {m['label']}{star}")
    for w in r["warnings"]:
        out.append(f"\n  WARNING: {w}")
    out.append("")
    out.append(f"  VERDICT: {r['verdict']}" +
               ("  (mandatory GET CURRENT gate forced this)" if r["mandatory_gate_forced_incomplete"] else ""))
    return "\n".join(out)


def main(argv: List[str]) -> int:
    p = argparse.ArgumentParser(
        description="Gate a GTD weekly review: completion %, named gaps, COMPLETE/INCOMPLETE verdict.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--done", default="", help='Comma-separated step numbers completed, e.g. "1,3,5"')
    p.add_argument("--skip", action="append", default=[],
                   help='Skip a step with a reason, e.g. --skip "9:no someday list yet" (repeatable)')
    p.add_argument("--list", action="store_true", help="Show the numbered ten-step checklist and exit")
    p.add_argument("--sample", action="store_true",
                   help="Run an embedded example review (always exits 0; the sample shows an INCOMPLETE verdict)")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    args = p.parse_args(argv)

    if args.list:
        print(render_list())
        return 0

    try:
        if args.sample:
            done = parse_done("1,2,3,4,6,7,8")
            skips = parse_skips(["9:no someday list yet"])
        else:
            done = parse_done(args.done)
            skips = parse_skips(args.skip)
        result = evaluate(done, skips)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 3

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render_human(result))

    if args.sample:
        return 0  # sample is illustrative; documented to always exit 0
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
