---
title: "/cs-grill-agent-launcher — Slash Command for AI Coding Agents"
description: "Matt Pocock docs-anchored grill for an agent-launcher goal — walks the phase's forcing questions ONE at a time, each with a recommended answer and a. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-grill-agent-launcher

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/agent-launcher/commands/cs-grill-agent-launcher.md">Source</a></span>
</div>


Grill the current goal's phase using its SKILL.md "Forcing-question library".

**$ARGUMENTS**

## Discipline

- **One question per turn.** Never batch. Wait for the answer before the next.
- **Recommend an answer.** Lead with the strongest default and why.
- **Cite the canon.** Each question names its reference doc (cma-primitives.md,
  interview-to-config.md, loops-and-workflows.md, session-goal-model.md).
- **Refuse to advance on fuzz.** If the answer is vague, restate the question with a
  sharper recommended option.

## Question sources

| Phase | Forcing questions live in |
|---|---|
| interview | `skills/interview/SKILL.md` |
| stage-launch | `skills/stage-launch/SKILL.md` |
| grade-iterate | `skills/grade-iterate/SKILL.md` |
| run-without-you | `skills/run-without-you/SKILL.md` |
| wrap-up | `skills/wrap-up/SKILL.md` |
| (whole plan) | `skills/agent-launcher-orchestrator/SKILL.md` |

Start with the orchestrator's five questions unless `$ARGUMENTS` names a phase.
