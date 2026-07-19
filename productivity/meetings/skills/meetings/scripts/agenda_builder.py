#!/usr/bin/env python3
"""agenda_builder.py — Build a timeboxed, decision-first agenda where every topic has an outcome.

The `meetings` skill's second discipline. Feed it topics as
    --topic "title:desired_outcome:minutes:owner"
plus the total meeting length (--length). It enforces the agenda canon deterministically:

  1. NO DESIRED OUTCOME, NO AGENDA SLOT — any topic with an empty outcome is refused, by name.
  2. TIMEBOXES ARE A BUDGET — topic timeboxes + a mandatory 5-minute closing "actions recap"
     buffer must fit --length, or the agenda is refused with the exact overflow.
  3. DECISIONS FIRST — topics whose outcome starts with decide/choose/approve sort before
     discuss/inform topics, so the decision gets fresh brains, not the last five minutes.
  4. PRE-READ — the agenda opens with a pre-read line (circulate ahead; the meeting assumes it
     was read) and closes with the actions-recap slot (every action gets an owner + a date).

NO LLM CALLS. Pure parsing + ordering + arithmetic. Stdlib only. Nothing is sent or scheduled.

Usage:
    python agenda_builder.py --length 45 \\
        --topic "Q3 pricing:Decide usage-based vs seat-based:15:maria" \\
        --topic "Launch risks:Discuss open launch blockers:15:sam"
    python agenda_builder.py --sample
    python agenda_builder.py --sample --json
"""

import argparse
import json
import sys
from typing import Any, Dict, List

CLOSING_BUFFER_MIN = 5  # mandatory closing "actions recap" slot
DECISION_PREFIXES = ("decide", "choose", "approve")

EPILOG = """\
exit codes:
  0   agenda built (timeboxes + 5-min closing buffer fit --length; all outcomes present)
  1   usage error — malformed --topic spec or bad/missing flags (never a verdict)
  2   refused — one or more topics has an empty desired outcome (named in output)
  3   refused — timeboxes + 5-min closing buffer exceed --length (overflow named in output)

--help and --sample exit 0.
"""


def parse_topic(spec: str) -> Dict[str, Any]:
    # Split the two structured fields (minutes, owner) from the right, then the
    # title at the first colon — so a desired outcome may itself contain colons.
    parts = spec.rsplit(":", 2)
    if len(parts) != 3 or ":" not in parts[0]:
        raise ValueError(
            f'malformed --topic "{spec}" — expected 4 colon-separated fields: '
            '"title:desired_outcome:minutes:owner" (colons are allowed inside '
            "desired_outcome; the title must not contain one)"
        )
    head, minutes_raw, owner = parts
    title, outcome = head.split(":", 1)
    title, outcome, minutes_raw, owner = (p.strip() for p in (title, outcome, minutes_raw, owner))
    try:
        minutes = int(minutes_raw)
    except ValueError:
        raise ValueError(f'malformed --topic "{spec}" — minutes must be an integer, got "{minutes_raw}"')
    if minutes < 1:
        raise ValueError(f'malformed --topic "{spec}" — minutes must be >= 1')
    if not title:
        raise ValueError(f'malformed --topic "{spec}" — title is empty')
    is_decision = outcome.lower().startswith(DECISION_PREFIXES)
    return {"title": title, "outcome": outcome, "minutes": minutes, "owner": owner,
            "kind": "decision" if is_decision else "discuss/inform"}


def build(topics: List[Dict[str, Any]], length: int) -> Dict[str, Any]:
    empty = [t["title"] for t in topics if not t["outcome"]]
    if empty:
        return {
            "status": "REFUSED-NO-OUTCOME",
            "exit_code": 2,
            "offenders": empty,
            "message": ("No desired outcome, no agenda slot. Topics refused: "
                        + ", ".join(f'"{t}"' for t in empty)
                        + ". Go get the outcome, then rebuild."),
        }

    topic_minutes = sum(t["minutes"] for t in topics)
    budget = topic_minutes + CLOSING_BUFFER_MIN
    if budget > length:
        overflow = budget - length
        return {
            "status": "REFUSED-OVERFLOW",
            "exit_code": 3,
            "topic_minutes": topic_minutes,
            "closing_buffer": CLOSING_BUFFER_MIN,
            "length": length,
            "overflow_minutes": overflow,
            "message": (f"Timeboxes ({topic_minutes} min) + closing actions-recap buffer "
                        f"({CLOSING_BUFFER_MIN} min) = {budget} min, but the meeting is "
                        f"{length} min — {overflow} min over. Cut a topic, shrink a timebox, "
                        "or move an inform topic to the pre-read."),
        }

    # Decisions first (stable within each group — caller's order is preserved otherwise).
    ordered = sorted(topics, key=lambda t: 0 if t["kind"] == "decision" else 1)

    cursor = 0
    slots: List[Dict[str, Any]] = []
    for t in ordered:
        slots.append({**t, "start_min": cursor, "end_min": cursor + t["minutes"]})
        cursor += t["minutes"]
    recap_start = length - CLOSING_BUFFER_MIN
    slack = recap_start - cursor

    return {
        "status": "OK",
        "exit_code": 0,
        "length": length,
        "topic_minutes": topic_minutes,
        "closing_buffer": CLOSING_BUFFER_MIN,
        "slack_minutes": slack,
        "slots": slots,
        "recap": {"title": "Actions recap", "start_min": recap_start, "end_min": length,
                  "outcome": "Read every action aloud: owner + due date, or it is not an action"},
    }


def render_markdown(r: Dict[str, Any]) -> str:
    out: List[str] = []
    out.append(f"# Agenda — {r['length']} minutes, {len(r['slots'])} topics")
    out.append("")
    out.append("**Pre-read:** circulate the relevant doc(s) at least a day ahead. "
               "The meeting starts assuming the pre-read was read — no recap slot for skippers.")
    out.append("")
    out.append("| # | Timebox | Topic | Desired outcome | Owner |")
    out.append("|---|---------|-------|-----------------|-------|")
    for idx, s in enumerate(r["slots"], 1):
        out.append(f"| {idx} | {s['start_min']:02d}–{s['end_min']:02d} min ({s['minutes']} min) "
                   f"| {s['title']} | {s['outcome']} | {s['owner']} |")
    rec = r["recap"]
    out.append(f"| ✔ | {rec['start_min']:02d}–{rec['end_min']:02d} min ({CLOSING_BUFFER_MIN} min) "
               f"| **{rec['title']}** | {rec['outcome']} | meeting owner |")
    out.append("")
    if r["slack_minutes"] > 0:
        out.append(f"_{r['slack_minutes']} min of slack before the recap — if topics finish early, "
                   "end early. Nobody has ever complained about a meeting ending early._")
    else:
        out.append("_Zero slack — hold the timeboxes or the recap gets eaten. "
                   "The recap is the most valuable slot; protect it._")
    return "\n".join(out)


SAMPLE_ARGS = {
    "length": 45,
    "topics": [
        "Metrics review:Inform team of the activation trend:5:alex",
        "Q3 pricing:Decide usage-based vs seat-based:15:maria",
        "Launch risks:Discuss open launch blockers:15:sam",
    ],
}


def main(argv: List[str]) -> int:
    p = argparse.ArgumentParser(
        description="Build a timeboxed, decision-first agenda (refuses empty outcomes and overflow).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=EPILOG,
    )
    p.add_argument("--topic", action="append", default=[], metavar="SPEC",
                   help='Repeatable. "title:desired_outcome:minutes:owner" '
                        '(outcome starting decide/choose/approve sorts first)')
    p.add_argument("--length", type=int, help="Total meeting length in minutes")
    p.add_argument("--sample", action="store_true", help="Run the embedded 3-topic sample")
    p.add_argument("--json", action="store_true", help="Emit machine-readable JSON instead of markdown")
    args = p.parse_args(argv)

    if args.sample:
        length, specs = SAMPLE_ARGS["length"], SAMPLE_ARGS["topics"]
    elif args.topic and args.length is not None:
        length, specs = args.length, args.topic
    else:
        p.print_help()
        print("\nerror: provide --length and at least one --topic, or --sample", file=sys.stderr)
        return 1

    if length < CLOSING_BUFFER_MIN + 1:
        print(f"error: --length must be at least {CLOSING_BUFFER_MIN + 1} minutes "
              f"({CLOSING_BUFFER_MIN}-min closing buffer is mandatory)", file=sys.stderr)
        return 1

    try:
        topics = [parse_topic(s) for s in specs]
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    result = build(topics, length)
    if args.json:
        print(json.dumps(result, indent=2))
    elif result["status"] == "OK":
        print(render_markdown(result))
    else:
        print(f"REFUSED ({result['status']}): {result['message']}", file=sys.stderr)
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
