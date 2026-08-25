---
description: Phase 1 — interview the founder into a validated CMA build sheet (primitives table + v1/v2 deferrals + eval plan) via the interview skill. No API key needed. Walks the six intake slots, maps to primitives, validates against CMA limits.
argument-hint: "[optional: a one-line description of the agent's job]"
---

# /cs:interview — Phase 1: Interview → Plan

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
