---
title: "/cs-internal-comms — Slash Command for AI Coding Agents"
description: "Internal-only change-management comms using ADKAR (Prosci) + Kotter's 8-step. NOT marketing (external) and NOT executive narrative strategy. Direct. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-internal-comms

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/business-operations/commands/cs-internal-comms.md">Source</a></span>
</div>


Run the `internal-comms` skill on this input:

**$ARGUMENTS**

## Three-tool workflow

1. **`comms_template_filler.py`** — ADKAR-anchored comms package (pre-comm / announcement / FAQ / follow-up). Each touchpoint tagged with which ADKAR stage it serves (Awareness / Desire / Knowledge / Ability / Reinforcement).

2. **`change_announcement_builder.py`** — Kotter 8-step compliant announcement (Urgency → Coalition → Vision → Communicate → Empower → Wins → Sustain → Anchor). Validates: no "exciting news" on disruptive change, no "minor update" on high-magnitude change. Tone calibration via `--profile {tech-startup,scaleup,enterprise,public-company,non-profit}`.

3. **`comms_calendar_builder.py`** — 7-touchpoint sequencing (Prosci minimum for behavioral change). Flags gaps: 2-touchpoint plans for disruptive change, Slack-only for layoffs (anti-pattern — requires synchronous channel), magnitude mismatches.

## Hard rules

- **Layoff comms** never go Slack-only. Synchronous channel required.
- **Disruptive change** needs ≥ 5 touchpoints with manager-cascade enabled.
- **Magnitude downplaying** ("minor restructuring" for 30% RIF) is auto-flagged.

## Distinct from

- `marketing-skill/*` — external-facing
- `c-level-advisor/internal-narrative` — strategic narrative framing (CEO voice)
- `c-level-advisor/change-management` — executive change strategy. Internal-comms is the tactical authoring layer underneath.
