---
title: "/cs-pm — Slash Command for AI Coding Agents"
description: "Top-level project-management router. Classifies a PM inquiry across 8 lanes (sprint/flow, portfolio health, Jira, Confluence, admin, templates. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-pm

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/project-management/commands/cs-pm.md">Source</a></span>
</div>


Route this inquiry through the `pm-skills` orchestrator:

**$ARGUMENTS**

## Routing (deterministic — run the script, don't eyeball)

```bash
python3 project-management/skills/pm-skills/scripts/pm_goal_router.py --text "$ARGUMENTS" --output json
```

- Exit 0 → load `skill_path`/SKILL.md and follow that skill's own workflow in a fork.
- Exit 2 → ask ONE clarifying question naming the listed candidates, recommended answer
  first.
- Exit 3 → ask the user to restate the goal with the deliverable named. Never guess.
- Explore the workspace first — a saved Jira snapshot, retro log, or transcript resolves
  the lane silently. Never silently chain a second sub-skill.

## Output (≤200-word digest)

- What was analyzed (with the data source — snapshot file, not memory)
- Top 3 findings, each anchored to a canon citation
- Top 3 next actions with a named human owner
- Artifact path
- One grill challenge (e.g. "Your health report is self-reported RAG — where's the
  derived diff that catches watermelons?")

## Hard rules

- Flow numbers come from `jira_snapshot_bridge.py` on real snapshot data.
- Forecasts are Monte Carlo percentile ranges, never single dates.
- Live Jira/Confluence ops use only the tools in
  `project-management/references/atlassian-mcp-tools.md` — never invent tool names.
- Goals (not questions) go to `/cs:pm-loop` instead.

## Distinct from

- `product-team` — what to build. This domain is how to deliver it.
- `/cs:harness` — the generic loop engine; `/cs:pm-loop` is its PM-domain adapter.
