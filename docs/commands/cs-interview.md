---
title: "/cs-interview — Slash Command for AI Coding Agents"
description: "Phase 1 — interview the founder into a validated CMA build sheet (primitives table + v1/v2 deferrals + eval plan) via the interview skill. No API key. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-interview

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/agent-launcher/commands/cs-interview.md">Source</a></span>
</div>


Run the `interview` skill.

**$ARGUMENTS**

## Steps

1. Walk the six intake slots (job, trigger, inputs, actions, definition-of-done,
   recurrence) with AskUserQuestion — one at a time, recommend + cite.
2. `python3 agent-launcher/skills/interview/scripts/interview_planner.py --job "..." ... --out ./my-agent/plan.json`
3. `python3 agent-launcher/skills/interview/scripts/build_sheet_builder.py --plan ./my-agent/plan.json --out-dir ./my-agent`
4. `python3 agent-launcher/skills/interview/scripts/primitives_validator.py --sheet ./my-agent/build-sheet.json`
   — fix FAIL, surface WARN.
5. `goal_state.py set --phase stage-launch --artifact build_sheet=./my-agent/build-sheet.json`.

Mock connectors in v0 (schema-true custom tools); wire real MCP servers as v1
deferrals. v0 is the core job only.
