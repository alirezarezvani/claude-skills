---
title: "Phase 1 — Interview → Plan — Agent Skill for Claude Managed Agents"
description: "Phase 1 of building a Claude Managed Agent — interview the founder about the one job the agent should do, then produce a build sheet (CMA primitives. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Phase 1 — Interview → Plan

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch-outline: Agent Launcher</span>
<span class="meta-badge">:material-identifier: `interview`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/agent-launcher/skills/interview/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install agent-launcher-skills</code>
</div>


Open warmly with one or two examples from
[[`references/examples-bank.md`](https://github.com/alirezarezvani/claude-skills/tree/main/agent-launcher/references/examples-bank.md)](https://github.com/alirezarezvani/claude-skills/tree/main/agent-launcher/references/examples-bank.md), then interview
the founder into a **build sheet**. No API key needed in this phase — the output
is a plan.

## The six intake slots (ask one at a time; use AskUserQuestion for choices)

| Slot | Question | Maps to |
|---|---|---|
| **Job** | "What one job should this agent do end-to-end?" | `agent.system` + outcome `description` |
| **Trigger** | "What kicks it off — you ask it, an event, or a schedule?" | on-demand / event / cron |
| **Inputs** | "What does it read?" (files, repo, memory, gmail/slack/github, web) | resources / MCP servers / memory |
| **Actions** | "What does it do?" (draft, write, call APIs, run code) | agent toolset / custom tools / MCP |
| **Done** | "How would you grade a good run?" | outcome `rubric` (required) |
| **Recurrence** | "Once, on request, or on a cadence?" | single-pass / grade-loop / cron-loop |

See [[`references/interview-to-config.md`](https://github.com/alirezarezvani/claude-skills/tree/main/agent-launcher/references/interview-to-config.md)](https://github.com/alirezarezvani/claude-skills/tree/main/agent-launcher/references/interview-to-config.md)
for the full mapping.

## Workflow

1. **Interview.** Walk the six slots. Capture the founder's own words — never
   invent specifics they didn't claim.
2. **Map to primitives.**
   ```bash
   python3 scripts/interview_planner.py \
     --job "Triage overnight support email" --trigger schedule \
     --inputs "gmail,memory" --actions "label,reply" \
     --dod "one label per email, grounded reason, no invented facts" \
     --recurrence daily --out ./my-agent/plan.json
   ```
   MCP inputs become **schema-true mock custom tools** in v0 and a **v1 deferral**
   to wire the real server. Irreversible actions (send/publish) become **v2
   deferrals** behind `always_ask`.
3. **Assemble the sheet.**
   ```bash
   python3 scripts/build_sheet_builder.py --plan ./my-agent/plan.json --out-dir ./my-agent
   ```
4. **Validate limits.**
   ```bash
   python3 scripts/primitives_validator.py --sheet ./my-agent/build-sheet.json
   ```
   FAIL blocks progress; fix and re-run. WARN is advisory (surface it).
5. **Record the plan in the goal.** `goal_state.py set --phase stage-launch
   --artifact build_sheet=./my-agent/build-sheet.json`, then advance.

## Hard rules

- **v0 is the core job only.** Everything else is a versioned deferral with a
  reason and an exact mechanism.
- **Their problem, their words.**
- **No key yet.** The interview produces a plan; the key is a Phase-2 concern.

## Forcing-question library (recommend + cite)

1. "What one job — singular?" *Recommend:* the most-repeated task. *Cite:*
   interview-to-config.md. Two jobs → two agents.
2. "Real integration or v0 mock?" *Recommend:* mock; wire MCP as v1. *Cite:*
   interview-to-config.md rule 1.
3. "How do you grade it?" *Recommend:* 3–5 grounded rubric lines. *Cite:*
   cma-primitives.md (rubric required).
4. "Smarter over time?" *Recommend:* attach memory only if yes. *Cite:*
   cma-primitives.md (memory limits + injection).
5. "Once, or on a cadence?" *Recommend:* on-demand v0, schedule as Phase-4.
   *Cite:* loops-and-workflows.md.

## Tools

- `scripts/interview_planner.py` — answers → primitives skeleton + deferrals.
- `scripts/build_sheet_builder.py` — assemble/normalize build-sheet.json.
- `scripts/primitives_validator.py` — validate vs CMA limits (PASS/WARN/FAIL).
