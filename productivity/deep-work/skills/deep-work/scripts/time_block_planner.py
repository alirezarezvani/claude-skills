#!/usr/bin/env python3
"""time_block_planner.py — Build a time-blocked day: deep work first, shallow batched, buffers everywhere.

Encodes Cal Newport's time-block planning discipline as deterministic scheduling:

  1. Deep tasks are scheduled FIRST, in the earliest hours of the day (energy-first).
     Each deep task gets a block of at least 90 minutes — shorter blocks never reach depth.
  2. Total deep time is capped at 4 hours (240 min) — the trained practitioner's daily
     ceiling. Demand beyond the cap is not squeezed in; the planner REFUSES (exit 2)
     and names exactly which deep tasks to cut or defer.
  3. Shallow tasks are batched into at most two batches: one late morning (right after
     the deep blocks) and one at the end of the day. A single shallow task goes to the
     end-of-day batch so the morning stays protected.
  4. A 10-minute buffer separates consecutive work blocks (attention residue is real).
  5. An optional --lunch HH:MM inserts a fixed 30-minute break; blocks never straddle it.
  6. Shallow work that spills past --end is an overflow: the planner REFUSES (exit 2)
     and names the overflow instead of silently extending the day.

NO LLM CALLS. Pure arithmetic. Identical inputs always produce the identical plan.

Exit codes:
  0  plan fits — markdown schedule (or --json) emitted
  1  usage / input error (bad time format, bad task spec, end <= start)
  2  refusal — deep demand exceeds the 4-hour cap, or the day overflows --end

Usage:
    python time_block_planner.py --start 08:30 --end 17:00 --lunch 12:30 \\
        --task "Write product spec:120:deep" --task "Email sweep:30:shallow"
    python time_block_planner.py --sample
    python time_block_planner.py --sample --json
"""

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

DEEP_CAP_MIN = 240        # Newport's trained-limit ceiling: ~4 hours of deep work per day
MIN_DEEP_BLOCK = 90       # a deep block shorter than this never reaches depth
BUFFER_MIN = 10           # context-switch buffer between consecutive work blocks
LUNCH_MIN = 30            # fixed lunch break length


def parse_hhmm(value: str, flag: str) -> int:
    parts = value.split(":")
    if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
        raise ValueError(f"{flag} must be HH:MM, got: {value!r}")
    h, m = int(parts[0]), int(parts[1])
    if h > 23 or m > 59:
        raise ValueError(f"{flag} out of range: {value!r}")
    return h * 60 + m


def fmt(minutes: int) -> str:
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def fmt_dur(minutes: int) -> str:
    h, m = divmod(minutes, 60)
    if h and m:
        return f"{h}h{m:02d}"
    if h:
        return f"{h}h"
    return f"{m}min"


def parse_task(spec: str) -> Dict[str, Any]:
    parts = spec.rsplit(":", 2)
    if len(parts) != 3:
        raise ValueError(f'task must be "name:minutes:deep|shallow", got: {spec!r}')
    name, minutes_s, mode = parts[0].strip(), parts[1].strip(), parts[2].strip().lower()
    if not name:
        raise ValueError(f"task name is empty in: {spec!r}")
    if not minutes_s.isdigit() or int(minutes_s) <= 0:
        raise ValueError(f"task minutes must be a positive integer in: {spec!r}")
    if mode not in ("deep", "shallow"):
        raise ValueError(f'task mode must be "deep" or "shallow" in: {spec!r}')
    return {"name": name, "minutes": int(minutes_s), "mode": mode}


def _ev(start: int, end: int, label: str, kind: str) -> Dict[str, Any]:
    return {"start": start, "end": end, "label": label, "kind": kind,
            "minutes": end - start}


def plan(start: int, end: int, tasks: List[Dict[str, Any]],
         lunch: Optional[int]) -> Dict[str, Any]:
    """Return a plan dict. verdict is PLANNED, DEEP-CAP-EXCEEDED, or OVERFLOW."""
    deep = [t for t in tasks if t["mode"] == "deep"]
    shallow = [t for t in tasks if t["mode"] == "shallow"]
    notes: List[str] = []

    # --- 1. Deep blocks: at least 90 min each, earliest hours, capped at 4h total ---
    deep_blocks = []
    for t in deep:
        dur = max(MIN_DEEP_BLOCK, t["minutes"])
        if dur > t["minutes"]:
            notes.append(f'"{t["name"]}" widened from {t["minutes"]} to {dur} min '
                         f"(deep blocks below {MIN_DEEP_BLOCK} min never reach depth).")
        deep_blocks.append({"name": t["name"], "dur": dur})
    total_deep = sum(b["dur"] for b in deep_blocks)
    if total_deep > DEEP_CAP_MIN:
        acc, cut = 0, []
        for b in deep_blocks:
            if acc + b["dur"] <= DEEP_CAP_MIN:
                acc += b["dur"]
            else:
                cut.append(b["name"])
        return {
            "verdict": "DEEP-CAP-EXCEEDED",
            "reason": (f"Deep demand is {fmt_dur(total_deep)} but the trained daily ceiling "
                       f"is {fmt_dur(DEEP_CAP_MIN)}. Depth past the cap is fake depth — "
                       f"cut or defer to another day: " + ", ".join(f'"{n}"' for n in cut)),
            "deep_demand_minutes": total_deep,
            "deep_cap_minutes": DEEP_CAP_MIN,
            "cut_or_defer": cut,
        }

    # --- 2. Shallow batches: at most two (late morning + end of day) ---
    if len(shallow) >= 2:
        n_a = (len(shallow) + 1) // 2
        batch_a, batch_b = shallow[:n_a], shallow[n_a:]
    elif len(shallow) == 1:
        batch_a, batch_b = [], shallow[:]   # single batch goes end-of-day
    else:
        batch_a, batch_b = [], []
    dur_a = sum(t["minutes"] for t in batch_a)
    dur_b = sum(t["minutes"] for t in batch_b)

    # --- 3. Forward pass: deep blocks, then shallow batch A, lunch-aware ---
    events: List[Dict[str, Any]] = []
    ctx = {"lunch": lunch, "lunch_placed": lunch is None}
    cursor = start

    def advance(cursor: int, dur: int, label: str, kind: str) -> int:
        if events and events[-1]["kind"] in ("deep", "shallow"):
            events.append(_ev(cursor, cursor + BUFFER_MIN, "Buffer — stand up, reset", "buffer"))
            cursor += BUFFER_MIN
        if not ctx["lunch_placed"]:
            if cursor >= ctx["lunch"]:
                events.append(_ev(cursor, cursor + LUNCH_MIN, "Lunch — away from the desk", "break"))
                cursor += LUNCH_MIN
                ctx["lunch_placed"] = True
            elif cursor + dur > ctx["lunch"]:
                if ctx["lunch"] > cursor:
                    events.append(_ev(cursor, ctx["lunch"], "Flex — reset, no inputs", "flex"))
                events.append(_ev(ctx["lunch"], ctx["lunch"] + LUNCH_MIN,
                                  "Lunch — away from the desk", "break"))
                cursor = ctx["lunch"] + LUNCH_MIN
                ctx["lunch_placed"] = True
        events.append(_ev(cursor, cursor + dur, label, kind))
        return cursor + dur

    for b in deep_blocks:
        cursor = advance(cursor, b["dur"], f'DEEP — {b["name"]}', "deep")
    if batch_a:
        label_a = "SHALLOW batch (late morning) — " + " · ".join(t["name"] for t in batch_a)
        cursor = advance(cursor, dur_a, label_a, "shallow")

    # --- 4. Backward pass: shallow batch B ends exactly at --end ---
    # The 10-min buffer invariant applies before batch B too: when batch B would
    # directly follow a work block, that buffer is part of the day's budget.
    need_buffer = (BUFFER_MIN if batch_b and events and events[-1]["kind"] in ("deep", "shallow")
                   else 0)
    if cursor + need_buffer + dur_b > end:
        overflow = cursor + need_buffer + dur_b - end
        return {
            "verdict": "OVERFLOW",
            "reason": (f"The day overflows {fmt(end)} by {overflow} min. "
                       + (("Defer shallow work instead of extending the day: "
                           + ", ".join(f'"{t["name"]}"' for t in (batch_b or batch_a)))
                          if (batch_b or batch_a) else
                          "Deep demand alone exceeds the day — trim a deep block or extend --end.")),
            "overflow_minutes": overflow,
            "defer_candidates": [t["name"] for t in (batch_b or batch_a)],
        }
    if need_buffer:
        events.append(_ev(cursor, cursor + BUFFER_MIN, "Buffer — stand up, reset", "buffer"))
        cursor += BUFFER_MIN
    start_b = end - dur_b
    if start_b > cursor:
        if not ctx["lunch_placed"] and cursor <= ctx["lunch"] and ctx["lunch"] + LUNCH_MIN <= start_b:
            if ctx["lunch"] > cursor:
                events.append(_ev(cursor, ctx["lunch"], "Flex — overflow absorber", "flex"))
            events.append(_ev(ctx["lunch"], ctx["lunch"] + LUNCH_MIN,
                              "Lunch — away from the desk", "break"))
            cursor = ctx["lunch"] + LUNCH_MIN
            ctx["lunch_placed"] = True
        if start_b > cursor:
            events.append(_ev(cursor, start_b, "Flex — overflow absorber", "flex"))
    if not ctx["lunch_placed"]:
        notes.append(f"Lunch could not be placed at {fmt(lunch)} without splitting a block — "
                     "move it or shorten a block.")
    if batch_b:
        label_b = "SHALLOW batch (end of day) — " + " · ".join(t["name"] for t in batch_b)
        events.append(_ev(start_b, end, label_b, "shallow"))

    totals = {}
    for e in events:
        totals[e["kind"]] = totals.get(e["kind"], 0) + e["minutes"]
    return {
        "verdict": "PLANNED",
        "start": fmt(start),
        "end": fmt(end),
        "events": [{"start": fmt(e["start"]), "end": fmt(e["end"]),
                    "label": e["label"], "kind": e["kind"], "minutes": e["minutes"]}
                   for e in events],
        "totals_minutes": totals,
        "deep_total_minutes": totals.get("deep", 0),
        "deep_cap_minutes": DEEP_CAP_MIN,
        "notes": notes,
    }


def render_human(r: Dict[str, Any]) -> str:
    out: List[str] = []
    if r["verdict"] != "PLANNED":
        out.append(f"REFUSED — {r['verdict']}")
        out.append("=" * 64)
        out.append(f"  {r['reason']}")
        return "\n".join(out)
    out.append(f"## Time-Block Plan — {r['start']} → {r['end']}")
    out.append("")
    out.append("| Start | End | Block | Mode |")
    out.append("|-------|-----|-------|------|")
    for e in r["events"]:
        out.append(f"| {e['start']} | {e['end']} | {e['label']} | {e['kind'].upper()} |")
    out.append("")
    t = r["totals_minutes"]
    out.append(f"Deep {fmt_dur(t.get('deep', 0))} / {fmt_dur(r['deep_cap_minutes'])} cap · "
               f"Shallow {fmt_dur(t.get('shallow', 0))} · "
               f"Flex {fmt_dur(t.get('flex', 0))} · "
               f"Buffers {fmt_dur(t.get('buffer', 0))}")
    for n in r["notes"]:
        out.append(f"- Note: {n}")
    out.append("")
    out.append("Flex absorbs what the plan didn't foresee — when the day breaks, "
               "revise the blocks; never abandon them.")
    return "\n".join(out)


SAMPLE = {
    "start": "08:30", "end": "17:00", "lunch": "12:30",
    "tasks": [
        "Write product spec:120:deep",
        "Design onboarding flow:90:deep",
        "Email sweep:30:shallow",
        "Team status update:20:shallow",
        "Expense report:15:shallow",
    ],
}


def main(argv: List[str]) -> int:
    p = argparse.ArgumentParser(
        description="Build a time-blocked day: deep work first, shallow batched, buffers everywhere.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=("Exit codes:\n"
                "  0  plan fits — schedule emitted\n"
                "  1  usage / input error\n"
                "  2  refusal — deep demand exceeds the 4-hour cap, or the day overflows --end"),
    )
    p.add_argument("--start", help="Day start, HH:MM")
    p.add_argument("--end", help="Day end, HH:MM (hard stop — fixed-schedule productivity)")
    p.add_argument("--task", action="append", default=[],
                   help='Repeatable: "name:minutes:deep|shallow"')
    p.add_argument("--lunch", help="Optional lunch start, HH:MM (fixed 30-min break)")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of markdown")
    p.add_argument("--sample", action="store_true", help="Run the embedded sample day")
    args = p.parse_args(argv)

    if args.sample:
        args.start, args.end = SAMPLE["start"], SAMPLE["end"]
        args.lunch, args.task = SAMPLE["lunch"], SAMPLE["tasks"]
    if not args.start or not args.end or not args.task:
        p.print_help()
        print("\nerror: --start, --end and at least one --task are required (or --sample)",
              file=sys.stderr)
        return 1
    try:
        start = parse_hhmm(args.start, "--start")
        end = parse_hhmm(args.end, "--end")
        lunch = parse_hhmm(args.lunch, "--lunch") if args.lunch else None
        if end <= start:
            raise ValueError("--end must be after --start")
        tasks = [parse_task(s) for s in args.task]
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    result = plan(start, end, tasks, lunch)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render_human(result))
    return 0 if result["verdict"] == "PLANNED" else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
