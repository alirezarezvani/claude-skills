---
title: "/cs-claude-rollout — Slash Command for AI Coding Agents"
description: "Full Claude Code team-rollout audit - settings across scopes, MCP/plugin inventory, CLAUDE.md layering, and adoption stage.. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-claude-rollout

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/engineering/coding-agent-rollout/commands/cs-claude-rollout.md">Source</a></span>
</div>


Audit the Claude Code setup for `$ARGUMENTS` (default: the current repository) as a team policy.

## Run

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/coding-agent-rollout/scripts/settings_linter.py --repo <repo> [--managed <managed-settings.json>]
python ${CLAUDE_PLUGIN_ROOT}/skills/coding-agent-rollout/scripts/mcp_plugin_inventory.py --repo <repo> [--allowlist <approved.json>]
python ${CLAUDE_PLUGIN_ROOT}/skills/coding-agent-rollout/scripts/claude_md_layering_audit.py --repo <repo>
```

If the user has adoption summaries, add:

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/coding-agent-rollout/scripts/adoption_tracker.py --merge <summaries...> --seats <N> [--weeks-since-launch <W>]
```

No managed settings yet? Start from `skills/coding-agent-rollout/assets/managed-settings.example.json`
and lint it with `--managed` before proposing it.

## Report

1. **Blockers** across all three scripts, each with its one-line fix.
2. **Effective policy** in plain words: what runs unprompted, what asks, what is denied, which MCP servers and plugins load.
3. **Warnings** grouped by script.
4. **Adoption stage**, if summaries were given.
5. **Next phase** from `skills/coding-agent-rollout/assets/rollout_plan.md` and its exit criterion.

## Do not

- Do not edit settings files without being asked; propose the diff.
- Do not read or request session transcripts. Counts only.
