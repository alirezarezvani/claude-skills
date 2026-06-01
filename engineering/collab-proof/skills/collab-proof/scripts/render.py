#!/usr/bin/env python3
"""
collab-proof HTML renderer — stdlib only, no pip required.

Usage:
  python3 render.py                        # most recent session-history file
  python3 render.py session-history/X.md  # specific session
"""

from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path


# ─── parsers ─────────────────────────────────────────────────────────────────

def parse_decisions(path: Path) -> list[dict]:
    if not path.exists():
        return []
    text = path.read_text()
    blocks = re.split(r"\n## ", text)
    decisions = []
    for block in blocks[1:]:  # skip header
        d: dict = {}
        # title line: "2026-06-01 Some title"
        first_line = block.split("\n")[0].strip()
        date_match = re.match(r"(\d{4}-\d{2}-\d{2})\s+(.*)", first_line)
        if date_match:
            d["date"] = date_match.group(1)
            d["title"] = date_match.group(2)
        else:
            d["date"] = ""
            d["title"] = first_line

        for field in ["Context", "Decision", "Alternatives considered",
                      "Reasoning", "Intent class", "Signal score", "Outcome"]:
            m = re.search(rf"\*\*{re.escape(field)}\*\*:\s*(.*?)(?=\n\*\*|\Z)",
                          block, re.DOTALL)
            raw = m.group(1).strip() if m else ""
            # strip trailing DECISIONS.md section dividers (---)
            raw = re.sub(r"\s*---+\s*$", "", raw).strip()
            d[field.lower().replace(" ", "_")] = raw

        # AI contribution block
        ai_block_match = re.search(
            r"\*\*AI contribution\*\*:(.*?)(?=\n\*\*|\Z)", block, re.DOTALL
        )
        ai_raw = ai_block_match.group(1).strip() if ai_block_match else ""
        d["ai_identified"] = _extract_ai_lines(ai_raw, "Identified")
        d["ai_suggested"]  = _extract_ai_lines(ai_raw, "Suggested")
        d["ai_developer"]  = _extract_ai_lines(ai_raw, "Developer-driven")

        decisions.append(d)
    return decisions


def _extract_ai_lines(text: str, label: str) -> list[str]:
    lines = []
    for line in text.splitlines():
        stripped = line.strip().lstrip("- ")
        if stripped.startswith(f"{label}:"):
            lines.append(stripped[len(label) + 1:].strip())
    return lines


def parse_session(path: Path) -> dict:
    text = path.read_text()
    s: dict = {"raw": text}

    # metadata
    s["date"]    = _field(text, "Session (.+)")
    s["intent"]  = _field(text, r"\*\*Intent\*\*:\s*(.+?)(?:\s*\(|$)")
    s["runner"]  = _field(text, r"\(runner-up:\s*(.+?)\)")
    s["signal"]  = _field(text, r"\*\*Signal score\*\*:\s*([\d.]+)")
    s["frames"]  = _field(text, r"\*\*Frames active\*\*:\s*(.+)")

    # sections
    for section in ["What shipped", "What was figured out",
                    "Where it got hard", "AI contribution summary",
                    "Next steps inferred", "Decisions made this session"]:
        s[section] = _section(text, section)

    return s


def _field(text: str, pattern: str) -> str:
    m = re.search(pattern, text)
    return m.group(1).strip() if m else ""


def _section(text: str, heading: str) -> str:
    m = re.search(
        rf"## {re.escape(heading)}\n(.*?)(?=\n## |\Z)", text, re.DOTALL
    )
    return m.group(1).strip() if m else ""


def parse_worklog(path: Path) -> list[str]:
    if not path.exists():
        return []
    lines = [l.strip() for l in path.read_text().splitlines()
             if l.strip() and not l.startswith("#")]
    return lines


# ─── intent badge colours ─────────────────────────────────────────────────────

INTENT_COLOURS = {
    "FEATURE_BUILDING": ("#238636", "#3fb950"),
    "BUG_FIXING":       ("#b08800", "#d29922"),
    "REFACTORING":      ("#1f6feb", "#58a6ff"),
    "EXPLORING":        ("#6e40c9", "#a371f7"),
    "STUCK":            ("#b62324", "#f85149"),
    "FLOW_STATE":       ("#0e7a6e", "#2ea699"),
}

def intent_colour(intent: str) -> tuple[str, str]:
    key = intent.strip().upper().replace(" ", "_")
    return INTENT_COLOURS.get(key, ("#30363d", "#8b949e"))


# ─── markdown → HTML (minimal, no external lib) ──────────────────────────────

def md_inline(text: str) -> str:
    """Convert inline markdown to HTML (bold, code, links only)."""
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def md_block(text: str) -> str:
    """Convert a block of markdown to simple HTML paragraphs/lists."""
    if not text:
        return "<p><em>—</em></p>"
    lines = text.splitlines()
    html_parts = []
    in_list = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                html_parts.append("<ul>")
                in_list = True
            html_parts.append(f"<li>{md_inline(stripped[2:])}</li>")
        else:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            if stripped:
                html_parts.append(f"<p>{md_inline(stripped)}</p>")
    if in_list:
        html_parts.append("</ul>")
    return "\n".join(html_parts)


# ─── HTML template ─────────────────────────────────────────────────────────────

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: #0d1117;
  color: #c9d1d9;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-size: 14px;
  line-height: 1.6;
  padding: 0 0 60px 0;
}

a { color: #58a6ff; text-decoration: none; }
a:hover { text-decoration: underline; }
code {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 4px;
  padding: 1px 5px;
  font-size: 12px;
  font-family: 'SFMono-Regular', Consolas, monospace;
}
strong { color: #e6edf3; }

/* ── header ── */
.header {
  background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
  border-bottom: 1px solid #30363d;
  padding: 32px 40px 24px;
}
.header-top { display: flex; align-items: flex-start; gap: 16px; flex-wrap: wrap; }
.project-name {
  font-size: 24px;
  font-weight: 700;
  color: #e6edf3;
  flex: 1;
}
.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
  border: 1px solid;
}
.meta-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
  flex-wrap: wrap;
  color: #8b949e;
  font-size: 13px;
}
.signal-container { margin-top: 16px; }
.signal-label {
  font-size: 12px;
  color: #8b949e;
  margin-bottom: 6px;
  display: flex;
  justify-content: space-between;
}
.signal-track {
  height: 6px;
  background: #21262d;
  border-radius: 3px;
  overflow: hidden;
  max-width: 320px;
}
.signal-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.8s ease;
}

/* ── section wrapper ── */
.section {
  max-width: 900px;
  margin: 32px auto 0;
  padding: 0 40px;
}
.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #e6edf3;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #21262d;
  display: flex;
  align-items: center;
  gap: 8px;
}
.section-title .count {
  background: #21262d;
  border-radius: 10px;
  padding: 1px 8px;
  font-size: 11px;
  color: #8b949e;
}

/* ── frames ── */
.frames-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}
.frame-card {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 8px;
  padding: 12px 16px;
}
.frame-card.pruned { opacity: 0.4; }
.frame-label {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  color: #8b949e;
  margin-bottom: 4px;
}
.frame-name { font-size: 13px; color: #e6edf3; font-weight: 500; }
.frame-score {
  font-size: 20px;
  font-weight: 700;
  margin-top: 8px;
}
.frame-score.high { color: #3fb950; }
.frame-score.mid  { color: #d29922; }
.frame-score.low  { color: #f85149; }

/* ── decision cards ── */
.decision-card {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 10px;
  padding: 20px 24px;
  margin-bottom: 16px;
}
.decision-card:hover { border-color: #58a6ff44; }
.decision-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
}
.decision-title {
  font-size: 16px;
  font-weight: 600;
  color: #e6edf3;
}
.decision-date { font-size: 12px; color: #8b949e; white-space: nowrap; }
.decision-fields { display: grid; gap: 12px; }
.field-row { display: grid; grid-template-columns: 160px 1fr; gap: 8px; }
.field-label {
  font-size: 12px;
  color: #8b949e;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  padding-top: 2px;
}
.field-value p { color: #c9d1d9; margin-bottom: 4px; }
.field-value ul { padding-left: 16px; color: #c9d1d9; }
.field-value li { margin-bottom: 3px; }
.ai-block { display: grid; gap: 6px; }
.ai-line {
  display: flex;
  gap: 8px;
  align-items: flex-start;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 13px;
}
.ai-line .tag {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.5px;
  padding: 2px 7px;
  border-radius: 4px;
  white-space: nowrap;
  margin-top: 1px;
}
.ai-identified   { background: #2d1b69; }
.ai-identified .tag { background: #a371f7; color: #0d1117; }
.ai-suggested    { background: #2d2208; }
.ai-suggested .tag { background: #d29922; color: #0d1117; }
.ai-developer    { background: #0d2016; }
.ai-developer .tag { background: #3fb950; color: #0d1117; }
.outcome-badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
}
.outcome-implemented { background: #0d2016; color: #3fb950; border: 1px solid #238636; }
.outcome-pending     { background: #2d2208; color: #d29922; border: 1px solid #b08800; }
.outcome-reversed    { background: #2d0f10; color: #f85149; border: 1px solid #b62324; }

/* ── narrative ── */
.narrative-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
@media (max-width: 640px) { .narrative-grid { grid-template-columns: 1fr; } }
.narrative-card {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 8px;
  padding: 16px 20px;
}
.narrative-card h4 {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #8b949e;
  margin-bottom: 10px;
}
.narrative-card p { color: #c9d1d9; margin-bottom: 6px; font-size: 13px; }
.narrative-card ul { padding-left: 16px; }
.narrative-card li { color: #c9d1d9; font-size: 13px; margin-bottom: 4px; }

/* ── worklog ── */
.worklog-entry {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 6px;
  padding: 10px 16px;
  margin-bottom: 8px;
  font-family: 'SFMono-Regular', Consolas, monospace;
  font-size: 12px;
  color: #8b949e;
}
.worklog-entry strong { color: #58a6ff; }

/* ── footer ── */
.footer {
  max-width: 900px;
  margin: 48px auto 0;
  padding: 24px 40px;
  border-top: 1px solid #21262d;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  color: #484f58;
  font-size: 12px;
}
.footer code { font-size: 11px; }
"""


def signal_colour(score: float) -> str:
    if score >= 0.75:
        return "linear-gradient(90deg, #238636, #3fb950)"
    if score >= 0.50:
        return "linear-gradient(90deg, #b08800, #d29922)"
    return "linear-gradient(90deg, #b62324, #f85149)"


def frame_score_class(score: float) -> str:
    if score >= 0.70:
        return "high"
    if score >= 0.40:
        return "mid"
    return "low"


def outcome_class(outcome: str) -> str:
    o = outcome.lower()
    if "implement" in o:
        return "outcome-implemented"
    if "revers" in o:
        return "outcome-reversed"
    return "outcome-pending"


def render_frames(frames_str: str) -> str:
    """Parse 'A (0.9) / B (0.85) / C (0.92) / D (0.8)' into frame cards."""
    frame_meta = [
        ("A", "Technical",      "What choices were made?"),
        ("B", "Uncertainty",    "Where was the developer unsure?"),
        ("C", "Fork",           "What could have gone differently?"),
        ("D", "AI Contribution","Where did Claude change the outcome?"),
    ]
    scores: dict[str, float] = {}
    for m in re.finditer(r"([A-D])\s*\(([\d.]+)\)", frames_str):
        scores[m.group(1)] = float(m.group(2))

    cards = []
    for letter, name, desc in frame_meta:
        score = scores.get(letter, 0.0)
        pruned = " pruned" if score < 0.4 and letter not in frames_str.upper() else ""
        cls = frame_score_class(score)
        cards.append(f"""
<div class="frame-card{pruned}">
  <div class="frame-label">Frame {letter}</div>
  <div class="frame-name">{name}</div>
  <div class="frame-score {cls}">{score:.2f}</div>
  <div style="font-size:11px;color:#8b949e;margin-top:6px;">{desc}</div>
</div>""")
    return "\n".join(cards)


def render_ai_lines(lines: list[str], css_class: str, tag: str) -> str:
    if not lines:
        return ""
    parts = []
    for line in lines:
        parts.append(f"""
<div class="ai-line {css_class}">
  <span class="tag">{tag}</span>
  <span>{md_inline(line)}</span>
</div>""")
    return "\n".join(parts)


def render_decisions(decisions: list[dict]) -> str:
    if not decisions:
        return "<p style='color:#8b949e'>No decisions recorded this session.</p>"
    cards = []
    for d in decisions:
        ai_html = (
            render_ai_lines(d.get("ai_identified", []), "ai-identified", "IDENTIFIED") +
            render_ai_lines(d.get("ai_suggested",  []), "ai-suggested",  "SUGGESTED") +
            render_ai_lines(d.get("ai_developer",  []), "ai-developer",  "DEV-DRIVEN")
        )
        outcome = d.get("outcome", "")
        oc = outcome_class(outcome)
        signal_val = d.get("signal_score", "")

        cards.append(f"""
<div class="decision-card">
  <div class="decision-header">
    <div class="decision-title">{d.get('title', '')}</div>
    <div class="decision-date">{d.get('date', '')}</div>
  </div>
  <div class="decision-fields">
    <div class="field-row">
      <div class="field-label">Context</div>
      <div class="field-value">{md_block(d.get('context',''))}</div>
    </div>
    <div class="field-row">
      <div class="field-label">Decision</div>
      <div class="field-value">{md_block(d.get('decision',''))}</div>
    </div>
    <div class="field-row">
      <div class="field-label">Alternatives</div>
      <div class="field-value">{md_block(d.get('alternatives_considered',''))}</div>
    </div>
    <div class="field-row">
      <div class="field-label">Reasoning</div>
      <div class="field-value">{md_block(d.get('reasoning',''))}</div>
    </div>
    <div class="field-row">
      <div class="field-label">AI contribution</div>
      <div class="field-value">
        <div class="ai-block">{ai_html or '<em style="color:#484f58">None recorded</em>'}</div>
      </div>
    </div>
    <div class="field-row">
      <div class="field-label">Outcome</div>
      <div class="field-value">
        <span class="outcome-badge {oc}">{outcome or '—'}</span>
        {('&nbsp;&nbsp;<span style="font-size:11px;color:#8b949e">signal ' + signal_val + '</span>') if signal_val else ''}
      </div>
    </div>
  </div>
</div>""")
    return "\n".join(cards)


def render(session_path: Path, decisions_path: Path, worklog_path: Path) -> str:
    session   = parse_session(session_path)
    decisions = parse_decisions(decisions_path)
    worklog   = parse_worklog(worklog_path)

    project   = session_path.parent.parent.name
    intent    = session.get("intent", "UNKNOWN")
    runner    = session.get("runner", "")
    signal_s  = session.get("signal", "0.0")
    signal_f  = float(signal_s) if signal_s else 0.0
    date_s    = session.get("date", "")
    frames_s  = session.get("frames", "")

    bg_c, fg_c = intent_colour(intent)
    sig_grad   = signal_colour(signal_f)
    sig_pct    = f"{signal_f * 100:.0f}%"

    runner_html = f'<span style="color:#8b949e;font-size:12px">(runner-up: {runner})</span>' if runner else ""

    worklog_html = ""
    for entry in worklog[-10:]:
        parts = entry.split(" | ", 3)
        if len(parts) == 4:
            ts, intent_w, sig_w, desc = parts
            worklog_html += f'<div class="worklog-entry"><strong>{ts}</strong> &nbsp;|&nbsp; {intent_w} &nbsp;|&nbsp; {sig_w} &nbsp;|&nbsp; {desc}</div>\n'
        else:
            worklog_html += f'<div class="worklog-entry">{entry}</div>\n'

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>collab-proof · {project} · {date_s}</title>
<style>{CSS}</style>
</head>
<body>

<!-- HEADER -->
<div class="header">
  <div style="max-width:900px;margin:0 auto;">
    <div class="header-top">
      <div class="project-name">📋 {project}</div>
      <span class="badge" style="background:{bg_c}22;color:{fg_c};border-color:{bg_c}66;">{intent}</span>
      {runner_html}
    </div>
    <div class="meta-row">
      <span>🗓 {date_s}</span>
      <span>·</span>
      <span>⚡ Signal score: <strong style="color:#e6edf3">{signal_s}</strong></span>
      <span>·</span>
      <span style="color:#484f58">generated by collab-proof</span>
    </div>
    <div class="signal-container">
      <div class="signal-label">
        <span>Signal strength</span>
        <span>{sig_pct}</span>
      </div>
      <div class="signal-track">
        <div class="signal-fill" style="width:{sig_pct};background:{sig_grad};"></div>
      </div>
    </div>
  </div>
</div>

<!-- FRAMES -->
<div class="section">
  <div class="section-title">
    🧠 Cognitive frames
    <span class="count">Layer 02 · ADHD tree-of-thought</span>
  </div>
  <div class="frames-grid">
    {render_frames(frames_s)}
  </div>
</div>

<!-- DECISIONS -->
<div class="section">
  <div class="section-title">
    🔀 Architectural decisions
    <span class="count">{len(decisions)} recorded</span>
  </div>
  {render_decisions(decisions)}
</div>

<!-- NARRATIVE -->
<div class="section">
  <div class="section-title">📖 Session narrative</div>
  <div class="narrative-grid">
    <div class="narrative-card">
      <h4>What shipped</h4>
      {md_block(session.get("What shipped", ""))}
    </div>
    <div class="narrative-card">
      <h4>What was figured out</h4>
      {md_block(session.get("What was figured out", ""))}
    </div>
    <div class="narrative-card">
      <h4>Where it got hard</h4>
      {md_block(session.get("Where it got hard", ""))}
    </div>
    <div class="narrative-card">
      <h4>Next steps inferred</h4>
      {md_block(session.get("Next steps inferred", ""))}
    </div>
  </div>
</div>

<!-- AI CONTRIBUTION SUMMARY -->
<div class="section">
  <div class="section-title">🤝 AI contribution summary</div>
  <div class="narrative-card" style="max-width:none;">
    <h4>Frame D synthesis</h4>
    {md_block(session.get("AI contribution summary", ""))}
  </div>
</div>

<!-- WORKLOG -->
<div class="section">
  <div class="section-title">
    📝 WORKLOG
    <span class="count">last {min(len(worklog), 10)} entries</span>
  </div>
  {worklog_html or '<p style="color:#484f58">No entries yet.</p>'}
</div>

<!-- FOOTER -->
<div class="footer">
  <div>
    Generated by <strong style="color:#8b949e">collab-proof</strong> · {now}
  </div>
  <div>
    Signal computed from: semantic depth · module impact · pattern deviation · conversation signal
  </div>
</div>

</body>
</html>"""
    return html


# ─── entry point ──────────────────────────────────────────────────────────────

def main() -> None:
    root = Path.cwd()

    # find session file
    if len(sys.argv) > 1:
        session_path = Path(sys.argv[1])
    else:
        sessions = sorted(root.glob("session-history/*.md"))
        sessions = [s for s in sessions if not s.name.startswith(".")]
        if not sessions:
            print("No session-history files found. Run /collab-proof first.")
            sys.exit(1)
        session_path = sessions[-1]

    decisions_path = root / "DECISIONS.md"
    worklog_path   = root / "WORKLOG.md"

    print(f"  session   : {session_path}")
    print(f"  decisions : {decisions_path}")
    print(f"  worklog   : {worklog_path}")

    html = render(session_path, decisions_path, worklog_path)

    # write next to the session file
    out_path = session_path.parent / (session_path.stem + "-proof.html")
    out_path.write_text(html, encoding="utf-8")

    print(f"\n  ✓ proof written → {out_path}")
    print(f"    open with: open {out_path}")


if __name__ == "__main__":
    main()
