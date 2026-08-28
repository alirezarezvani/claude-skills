#!/usr/bin/env python3
"""render_report.py — render a validated report.json into one self-contained HTML page.

Single file, zero JavaScript, no CDN, no external assets, no vendor branding:
scorecard with letter grade and score bars, stat tiles, findings, and every
suggested skill edit with its unified diff colored in pure CSS. Long diffs
collapse behind a native <details> toggle. Honors prefers-color-scheme and
prints cleanly (Cmd+P gives the shareable PDF).

Derived from warpdotdev/common-skills skill-doctor (MIT). Upstream shipped a
1,531-line prebuilt JS diff bundle, canvas share-image code, and a vendor CTA;
this rebuild drops all three — see the plugin README deviations list.

Usage:
    python render_report.py --report RUN/report.json
    python render_report.py --report RUN/report.json --out RUN/report.html
    python render_report.py --sample --out /tmp/demo.html
    python render_report.py --sample --output json

Exit codes: 0 rendered, 3 bad input (missing/invalid report.json).

Stdlib only. No ML/LLM calls.
"""

import argparse
import html
import json
import os
import sys
from pathlib import Path

REQUIRED_FIELDS = ("scores", "stats", "top_findings", "suggestions")
DIFF_COLLAPSE_LINES = 24

PAGE_CSS = """
* { box-sizing: border-box; }
:root {
  --fg: #1d2129; --muted: #5f6672; --accent: #2456d6; --line: #d6d9e0;
  --panel: #f4f5f8; --add-bg: #e3f4e6; --add-fg: #135723;
  --del-bg: #fbe4e4; --del-fg: #7c1d1d; --hunk: #6a5acd; --bg: #ffffff;
}
@media (prefers-color-scheme: dark) {
  :root {
    --fg: #e4e6eb; --muted: #9aa1ad; --accent: #7ea2f5; --line: #3a3f4a;
    --panel: #23262e; --add-bg: #1c3a24; --add-fg: #8fd39b;
    --del-bg: #43201f; --del-fg: #f0a6a1; --hunk: #b3a6f7; --bg: #16181d;
  }
}
body { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  background: var(--bg); color: var(--fg); max-width: 880px; margin: 0 auto;
  padding: 48px 24px; line-height: 1.65; font-size: 14px; }
h1 { font-weight: 600; font-size: 30px; margin: 4px 0 0; letter-spacing: -1px; }
h2 { font-weight: 600; font-size: 19px; margin: 40px 0 8px; }
p, .muted { color: var(--muted); }
.muted { font-size: 12px; }
li { margin-bottom: 10px; }
code { background: var(--panel); border: 1px solid var(--line); padding: 1px 5px; border-radius: 3px; }
.scorecard { display: flex; align-items: center; gap: 40px; border: 1px solid var(--line);
  background: var(--panel); padding: 26px 28px; margin-top: 20px; border-radius: 6px; }
.grade-col { text-align: center; flex: none; width: 160px; }
.grade { font-size: 84px; font-weight: 700; line-height: 1; color: var(--accent); }
.grade-label { font-size: 11px; color: var(--muted); margin-top: 8px;
  text-transform: uppercase; letter-spacing: 0.12em; }
.bars { flex: 1; display: flex; flex-direction: column; gap: 18px; min-width: 0; }
.bar-head { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px; }
.bar-track { height: 8px; background: var(--line); border-radius: 4px; overflow: hidden; }
.bar-fill { height: 100%; background: var(--accent); }
.stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px;
  background: var(--line); border: 1px solid var(--line); margin-top: 8px; border-radius: 6px; overflow: hidden; }
.stat { padding: 14px 20px; background: var(--bg); }
.stat .num { font-size: 30px; font-weight: 700; }
.stat .lbl { font-size: 12px; color: var(--muted); }
.evidence { color: var(--muted); font-size: 12px; margin: 4px 0 6px; }
details.diff { margin: 8px 0 4px; border: 1px solid var(--line); border-radius: 6px; overflow: hidden; }
details.diff summary { cursor: pointer; padding: 6px 12px; background: var(--panel);
  font-size: 12px; color: var(--muted); user-select: none; }
pre.diff-body { margin: 0; padding: 10px 0; overflow-x: auto; font-size: 12px; line-height: 1.55; }
pre.diff-body span { display: block; padding: 0 14px; white-space: pre; }
span.d-add { background: var(--add-bg); color: var(--add-fg); }
span.d-del { background: var(--del-bg); color: var(--del-fg); }
span.d-hunk { color: var(--hunk); }
span.d-meta { color: var(--muted); }
.warnings { border-left: 3px solid var(--accent); padding: 2px 14px; background: var(--panel); }
footer { margin-top: 48px; padding-top: 14px; border-top: 1px solid var(--line);
  font-size: 12px; color: var(--muted); }
@media print {
  body { max-width: none; padding: 0; font-size: 12px; }
  details.diff { break-inside: avoid; }
  details.diff:not([open]) summary::after { content: " (collapsed — open before printing for full diff)"; }
}
"""


def esc(value):
    return html.escape(str(value if value is not None else ""))


def pct(score):
    return round(float(score) * 100)


def render_diff(diff_text):
    if not (diff_text or "").strip():
        return ""
    lines = diff_text.splitlines()
    spans = []
    for line in lines:
        if line.startswith("+++") or line.startswith("---"):
            cls = "d-meta"
        elif line.startswith("@@"):
            cls = "d-hunk"
        elif line.startswith("+"):
            cls = "d-add"
        elif line.startswith("-"):
            cls = "d-del"
        else:
            cls = "d-ctx"
        spans.append(f'<span class="{cls}">{esc(line) or " "}</span>')
    open_attr = " open" if len(lines) <= DIFF_COLLAPSE_LINES else ""
    return (f'<details class="diff"{open_attr}><summary>{len(lines)}-line diff</summary>'
            f'<pre class="diff-body">{"".join(spans)}</pre></details>')


def render_page(report):
    scores = report["scores"]
    stats = report.get("stats", {})
    grade = report.get("grade", "?")

    bars = "".join(
        f'<div><div class="bar-head"><span>{esc(name)}</span><span>{pct(val)}</span></div>'
        f'<div class="bar-track"><div class="bar-fill" style="width:{pct(val)}%"></div></div></div>'
        for name, val in (("efficiency", scores.get("efficiency", 0)),
                          ("code quality", scores.get("code_quality", 0)),
                          ("skill coverage", scores.get("skill_coverage", 0)))
    )
    stat_cells = "".join(
        f'<div class="stat"><div class="num">{esc(value)}</div><div class="lbl">{esc(label)}</div></div>'
        for value, label in ((stats.get("sessions_analyzed", 0), "conversations scored"),
                             (stats.get("skills_found", 0), "skills installed"),
                             (stats.get("skills_used", 0), "skills used"))
    )
    findings = "".join(f"<li>{esc(f)}</li>" for f in report.get("top_findings", []))
    suggestions = "".join(
        f"<li><b><code>{esc(s.get('skill'))}</code></b> — {esc(s.get('change'))}"
        + (f'<div class="evidence">Evidence: {esc(s["evidence"])}</div>' if s.get("evidence") else "")
        + render_diff(s.get("diff", ""))
        + "</li>"
        for s in report.get("suggestions", [])
    ) or "<li>No skill change cleared the filing bar for this window — a speculative edit is worse than none.</li>"
    warnings = report.get("warnings") or []
    warnings_html = (
        '<div class="warnings"><ul>' + "".join(f"<li>{esc(w)}</li>" for w in warnings) + "</ul></div>"
        if warnings else ""
    )

    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(report.get('title', 'Agent Skill Report'))} — {esc(report.get('handle', ''))}</title>
<style>{PAGE_CSS}</style></head><body>
<div class="muted"># skill-doctor</div>
<h1>{esc(report.get('title', 'Agent Skill Report'))}</h1>
<p class="muted">{esc(report.get('handle', ''))} &middot; harness: {esc(report.get('harness', ''))}
 &middot; generated {esc(report.get('generated_at', ''))} &middot; all analysis ran locally</p>
<div class="scorecard">
  <div class="grade-col"><div class="grade">{esc(grade)}</div>
    <div class="grade-label">overall {pct(scores.get('overall', 0))}</div></div>
  <div class="bars">{bars}</div>
</div>
<div class="stats">{stat_cells}</div>
<p class="muted">{esc(stats.get('sessions_scanned', 0))} conversations found in the last
 {esc(stats.get('window_days', 45))} days</p>
<h2>Findings</h2><ul>{findings}</ul>
<h2>Suggested skill changes</h2><ol>{suggestions}</ol>
{('<h2>Aggregation warnings</h2>' + warnings_html) if warnings else ''}
<footer>Generated locally by skill-doctor. Transcripts were condensed and redacted on this
machine and were not uploaded anywhere. Print this page for a shareable PDF.</footer>
</body></html>"""


SAMPLE_REPORT = {
    "title": "Agent Skill Report",
    "generated_at": "2026-01-15T10:06:00+00:00",
    "harness": "claude",
    "handle": "sample-repo",
    "stats": {"sessions_analyzed": 2, "sessions_scanned": 9, "skills_found": 1,
              "skills_used": 1, "window_days": 45},
    "scores": {"efficiency": 0.9, "code_quality": 1.0, "skill_coverage": 0.5, "overall": 0.875},
    "grade": "B+",
    "top_findings": [
        "Files were re-read verbatim in 1 of 2 sessions before any edit was attempted",
        "The only installed skill fired in half the sampled sessions",
    ],
    "suggestions": [
        {"skill": "sample-skill",
         "change": "Add a preflight step: read the failing test output before opening the implementation file.",
         "evidence": "sample-session-1 re-read src/parse.py twice before locating the format string.",
         "sessions": ["sample-session-1"],
         "diff": "--- a/SKILL.md\n+++ b/SKILL.md\n@@ -3,2 +3,3 @@\n # sample-skill\n+1. Read the failing test output first; it usually names the file and line.\n Fix the bug.\n"},
    ],
    "warnings": [],
}


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="Render a skill-doctor report.json into one self-contained HTML page.")
    p.add_argument("--report", help="path to report.json from score_aggregator.py")
    p.add_argument("--out", help="output HTML path (default: report.html next to report.json)")
    p.add_argument("--output", choices=("text", "json"), default="text", help="summary format on stdout")
    p.add_argument("--sample", action="store_true", help="render built-in sample data (demo/smoke test)")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    if args.sample:
        report = SAMPLE_REPORT
        out_path = Path(args.out).expanduser() if args.out else Path("skill-doctor-sample-report.html")
    else:
        if not args.report:
            print("error: --report is required (or use --sample)", file=sys.stderr)
            return 3
        report_path = Path(args.report).expanduser()
        try:
            report = json.loads(report_path.read_text())
        except (OSError, json.JSONDecodeError) as exc:
            print(f"error: could not read report at {report_path}: {exc}", file=sys.stderr)
            return 3
        missing = [f for f in REQUIRED_FIELDS if f not in report]
        if missing:
            print(f"error: report.json is missing required fields: {', '.join(missing)} — "
                  "generate it with score_aggregator.py", file=sys.stderr)
            return 3
        out_path = Path(args.out).expanduser() if args.out else report_path.parent / "report.html"

    out_path.write_text(render_page(report))
    try:
        os.chmod(out_path, 0o600)
    except OSError:
        pass

    if args.output == "json":
        print(json.dumps({"status": "ok", "html": str(out_path),
                          "grade": report.get("grade"),
                          "suggestions": len(report.get("suggestions", []))}, indent=2))
    else:
        print(f"report: {out_path}")
        print("        open it in a browser; print to PDF for a shareable copy")
    return 0


if __name__ == "__main__":
    sys.exit(main())
