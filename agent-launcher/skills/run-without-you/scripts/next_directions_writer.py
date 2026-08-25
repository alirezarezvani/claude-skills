#!/usr/bin/env python3
"""next_directions_writer.py — write/refresh ./my-agent/NEXT-DIRECTIONS.md.

Renders the versioned roadmap from a build sheet's deferrals + the current goal
state: v0 (live) plus a table of deferred upgrades (version/item/reason/mechanism)
and the suggested next 1-2 moves. Uses the assets/NEXT-DIRECTIONS.template.md
shape. Stdlib-only; no network calls.

Examples:
  next_directions_writer.py --sheet ./my-agent/build-sheet.json --out-dir ./my-agent
  next_directions_writer.py --sample
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path


def _now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def render(sheet, loop_shape, last_verdict):
    goal = sheet.get("goal", "")
    name = sheet.get("agent_name", "agent")
    prim = sheet.get("primitives", {})
    live = []
    if prim.get("agent", {}).get("model"):
        live.append(f"agent[{prim['agent']['model']}]")
    live.append(f"env[{prim.get('environment', {}).get('type', 'cloud')}]")
    if prim.get("outcome"):
        live.append("outcome[rubric]")
    if prim.get("session", {}).get("memory_stores"):
        live.append(f"memory[{len(prim['session']['memory_stores'])}]")
    if prim.get("deployment"):
        live.append("deployment[cron]")

    deferrals = sheet.get("deferrals", []) or []
    if deferrals:
        rows = "\n".join(
            f"| {d.get('version','v?')} | {d.get('item','')} | {d.get('reason','')} | {d.get('mechanism','')} |"
            for d in deferrals
        )
    else:
        rows = "| — | (none recorded) | | |"

    next_moves = _next_moves(deferrals, prim)

    tmpl_path = Path(__file__).resolve().parents[3] / "assets" / "NEXT-DIRECTIONS.template.md"
    tmpl = tmpl_path.read_text()
    return tmpl.format(
        agent_name=name,
        goal=goal,
        loop_shape=loop_shape or sheet.get("loop_hint", "single-pass"),
        live_primitives=", ".join(live),
        last_verdict=last_verdict or "(not graded yet)",
        deferral_rows=rows,
        next_moves=next_moves,
        updated_at=_now(),
    )


def _next_moves(deferrals, prim):
    moves = []
    v1s = [d for d in deferrals if d.get("version") == "v1"]
    if v1s:
        moves.append(f"1. Ship {v1s[0].get('item')} — {v1s[0].get('mechanism')}")
    if not prim.get("deployment"):
        moves.append(f"{len(moves)+1}. Promote to a scheduled deployment once a version passes the rubric.")
    elif prim.get("environment", {}).get("networking") == "unrestricted":
        moves.append(f"{len(moves)+1}. Harden networking to 'limited' with an allowed_hosts list.")
    if not moves:
        moves.append("1. Monitor the first few scheduled runs; tighten the rubric if verdicts drift.")
    return "\n".join(moves)


def main() -> int:
    ap = argparse.ArgumentParser(description="Write/refresh NEXT-DIRECTIONS.md from a build sheet.")
    ap.add_argument("--sheet", help="build-sheet.json.")
    ap.add_argument("--out-dir", default="./my-agent")
    ap.add_argument("--loop-shape", default=None)
    ap.add_argument("--last-verdict", default=None)
    ap.add_argument("--stdout", action="store_true")
    ap.add_argument("--sample", action="store_true")
    args = ap.parse_args()

    if args.sample:
        sheet = json.loads((Path(__file__).resolve().parents[3] / "assets" / "example-build-sheet.json").read_text())
        print(render(sheet, "cron-loop", "satisfied"))
        return 0

    if not args.sheet:
        print("Provide --sheet path.", file=sys.stderr)
        return 2
    sheet = json.loads(Path(args.sheet).read_text())
    md = render(sheet, args.loop_shape, args.last_verdict)
    if args.stdout:
        print(md)
        return 0
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "NEXT-DIRECTIONS.md"
    dest.write_text(md)
    print(f"Wrote {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
