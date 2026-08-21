#!/usr/bin/env python3
"""overview_page.py — regenerate a single-file ./my-agent/agent-overview.html.

Fills assets/agent-overview.template.html with the build sheet's primitives, the
latest verdict, and the next moves. Self-contained (inline CSS, no external
assets, theme-aware). Stdlib-only; no network calls.

Examples:
  overview_page.py --sheet ./my-agent/build-sheet.json --out-dir ./my-agent \
     --status live --loop-shape cron-loop --last-verdict satisfied
  overview_page.py --sample
"""
import argparse
import datetime as dt
import html
import json
import sys
from pathlib import Path


def _now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def _esc(x):
    return html.escape(str(x), quote=True)


def render(sheet, status, loop_shape, last_verdict, console_link):
    prim = sheet.get("primitives", {})
    agent = prim.get("agent", {})
    env = prim.get("environment", {})
    session = prim.get("session", {})

    rows = []

    def row(k, v):
        rows.append(f"<tr><td>{_esc(k)}</td><td>{_esc(v)}</td></tr>")

    row("agent model", agent.get("model", "?"))
    row("tools", ", ".join(t.get("type", t.get("name", "?")) for t in agent.get("tools", [])) or "—")
    if agent.get("skills"):
        row("skills", ", ".join(agent["skills"]))
    row("environment", f"{env.get('type', 'cloud')} / {env.get('networking', 'unrestricted')}")
    if session.get("resources"):
        row("resources", ", ".join(r.get("type", "?") for r in session["resources"]))
    if session.get("memory_stores"):
        row("memory stores", str(len(session["memory_stores"])))
    row("outcome", "self-grading rubric" if prim.get("outcome") else "none")

    schedule = "none (on-demand)"
    if prim.get("deployment"):
        s = prim["deployment"].get("schedule", {})
        schedule = f"{s.get('expression', '?')} [{s.get('timezone', 'UTC')}]"
    iterations = str(prim.get("outcome", {}).get("max_iterations", "-")) if prim.get("outcome") else "-"

    moves = []
    for d in (sheet.get("deferrals", []) or [])[:2]:
        moves.append(f"<li>{_esc(d.get('version', 'v?'))}: {_esc(d.get('item', ''))} — {_esc(d.get('mechanism', ''))}</li>")
    if not moves:
        moves.append("<li>Monitor the first scheduled runs; tighten the rubric if verdicts drift.</li>")

    tmpl = (Path(__file__).resolve().parents[3] / "assets" / "agent-overview.template.html").read_text()
    out = tmpl
    subs = {
        "{{agent_name}}": _esc(sheet.get("agent_name", "agent")),
        "{{status}}": _esc(status),
        "{{loop_shape}}": _esc(loop_shape or sheet.get("loop_hint", "single-pass")),
        "{{goal}}": _esc(sheet.get("goal", "")),
        "{{primitives_rows}}": "\n      ".join(rows),
        "{{last_verdict}}": _esc(last_verdict or "(not graded yet)"),
        "{{iterations}}": _esc(iterations),
        "{{schedule}}": _esc(schedule),
        "{{next_moves}}": "".join(moves),
        "{{updated_at}}": _esc(_now()),
        "{{console_link}}": _esc(console_link or "https://platform.claude.com/"),
    }
    for k, v in subs.items():
        out = out.replace(k, v)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Regenerate a single-file agent-overview.html.")
    ap.add_argument("--sheet", help="build-sheet.json.")
    ap.add_argument("--out-dir", default="./my-agent")
    ap.add_argument("--status", default="live")
    ap.add_argument("--loop-shape", default=None)
    ap.add_argument("--last-verdict", default=None)
    ap.add_argument("--console-link", default=None)
    ap.add_argument("--stdout", action="store_true")
    ap.add_argument("--sample", action="store_true")
    args = ap.parse_args()

    if args.sample:
        sheet = json.loads((Path(__file__).resolve().parents[3] / "assets" / "example-build-sheet.json").read_text())
        html_out = render(sheet, "live", "cron-loop", "satisfied", None)
        print(html_out[:800] + "\n... [truncated in --sample] ...")
        return 0

    if not args.sheet:
        print("Provide --sheet path.", file=sys.stderr)
        return 2
    sheet = json.loads(Path(args.sheet).read_text())
    html_out = render(sheet, args.status, args.loop_shape, args.last_verdict, args.console_link)
    if args.stdout:
        print(html_out)
        return 0
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "agent-overview.html"
    dest.write_text(html_out)
    print(f"Wrote {dest} ({len(html_out)} bytes, self-contained)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
