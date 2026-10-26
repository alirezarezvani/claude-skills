---
title: "/cs-claude-settings-lint — Slash Command for AI Coding Agents"
description: "Lint Claude Code settings across shared, local, user and managed scopes, and say what the merged permission policy actually allows.. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-claude-settings-lint

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/engineering/coding-agent-rollout/commands/cs-claude-settings-lint.md">Source</a></span>
</div>


```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/coding-agent-rollout/scripts/settings_linter.py --repo <repo> [--managed <file>] [--user <file>]
```

Remember while reading the result: `permissions.allow` arrays **merge** across scopes, and evaluation is
deny, then ask, then allow, first match wins. A strict shared file does not cancel a permissive user file.

## Report

1. Verdict: CLEAN (0) / WARNINGS (2) / **BLOCKED (4)**.
2. Every BLOCKER with its fix: blanket `Bash` allows, pre-approved destructive commands, literal credentials,
   committed `.claude/settings.local.json`, managed `bypassPermissions`.
3. Dead rules (an allow shadowed by deny or ask, `mcp__*` in allow, `defaultMode` set where Claude Code ignores it).
4. Whether a managed policy disables bypass mode. If not, say that any engineer can skip every prompt.
