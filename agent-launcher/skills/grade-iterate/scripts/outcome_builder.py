#!/usr/bin/env python3
"""outcome_builder.py — build a CMA user.define_outcome payload (the grade->iterate loop).

The rubric is REQUIRED; max_iterations is clamped to 1..20 (CMA ceiling, default
3). Can pull description + rubric from a build sheet's primitives.outcome, or take
them on the command line. Stdlib-only; no network calls.

Examples:
  outcome_builder.py --sheet ./my-agent/build-sheet.json --max-iterations 5 --out ./my-agent/payloads/outcome.json
  outcome_builder.py --description "Label every email" --rubric-file rubric.md
  outcome_builder.py --sample
"""
import argparse
import json
import sys
from pathlib import Path

MAX_ITER = 20
DEFAULT_ITER = 3


def clamp(n):
    try:
        n = int(n)
    except (TypeError, ValueError):
        return DEFAULT_ITER, "non-integer -> default 3"
    if n < 1:
        return 1, f"{n} < 1 -> 1"
    if n > MAX_ITER:
        return MAX_ITER, f"{n} > {MAX_ITER} -> clamped {MAX_ITER}"
    return n, None


def build(description, rubric, max_iterations):
    cap, note = clamp(max_iterations)
    if not (rubric or "").strip():
        return None, "rubric is required and cannot be empty", cap, note
    payload = {
        "type": "user.define_outcome",
        "description": description.strip(),
        "rubric": rubric.strip(),
        "max_iterations": cap,
    }
    return payload, None, cap, note


def main() -> int:
    ap = argparse.ArgumentParser(description="Build a user.define_outcome payload (rubric required, max_iterations clamped 1..20).")
    ap.add_argument("--sheet", help="build-sheet.json to read primitives.outcome from.")
    ap.add_argument("--description", help="Outcome/task description.")
    ap.add_argument("--rubric", help="Inline markdown rubric.")
    ap.add_argument("--rubric-file", help="Path to a markdown rubric file.")
    ap.add_argument("--max-iterations", default=DEFAULT_ITER)
    ap.add_argument("--out", help="Write payload JSON here.")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--sample", action="store_true")
    args = ap.parse_args()

    if args.sample:
        payload, err, cap, note = build(
            "Label every overnight support email with one grounded category.",
            "- Every email has exactly one label\n- Reason quotes the email (no invented facts)\n- Urgent = outage / paying-customer blocker",
            99,
        )
        print(json.dumps(payload, indent=2))
        print(f"\n(max_iterations note: {note})", file=sys.stderr)
        return 0

    description = args.description
    rubric = args.rubric
    if args.rubric_file:
        rubric = Path(args.rubric_file).read_text()
    if args.sheet:
        sheet = json.loads(Path(args.sheet).read_text())
        oc = sheet.get("primitives", {}).get("outcome", {})
        description = description or oc.get("description") or sheet.get("goal", "")
        rubric = rubric or oc.get("rubric", "")
        if args.max_iterations == DEFAULT_ITER and oc.get("max_iterations"):
            args.max_iterations = oc["max_iterations"]

    if not description:
        print("Provide --description or --sheet.", file=sys.stderr)
        return 2

    payload, err, cap, note = build(description, rubric or "", args.max_iterations)
    if err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 1
    text = json.dumps(payload, indent=2)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text + "\n")
        print(f"Wrote {args.out} (max_iterations={cap})")
    if args.json or not args.out:
        print(text)
    if note:
        print(f"# {note}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
