---
title: "/cs-wrap-up — Slash Command for AI Coding Agents"
description: "Close out a launched Claude Managed Agent — recap every primitive owned, regenerate the single-file overview page, and suggest the next 1–2 upgrades. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-wrap-up

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/agent-launcher/commands/cs-wrap-up.md">Source</a></span>
</div>


Run the `wrap-up` skill.

**$ARGUMENTS**

## Steps

1. `python3 agent-launcher/skills/wrap-up/scripts/primitives_inventory.py --sheet ./my-agent/build-sheet.json --goal ./my-agent/goal.json`
2. `python3 agent-launcher/skills/wrap-up/scripts/overview_page.py --sheet ./my-agent/build-sheet.json --out-dir ./my-agent --status live`
3. `python3 agent-launcher/skills/wrap-up/scripts/upgrade_suggester.py --sheet ./my-agent/build-sheet.json --top 2`
4. Ensure `NEXT-DIRECTIONS.md` is current, then `goal_state.py advance` → phase=done.

Recap what's actually live (read from the sheet + goal state). The overview page is
single-file and shareable. Every next move names its exact mechanism.
