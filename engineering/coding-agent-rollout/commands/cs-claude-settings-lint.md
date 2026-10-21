---
description: Lint Claude Code settings across shared, local, user and managed scopes, and say what the merged permission policy actually allows.
argument-hint: "[repo path] [managed-settings.json] [user settings.json]"
---

# /cs-claude-settings-lint

```bash
python skills/coding-agent-rollout/scripts/settings_linter.py --repo <repo> [--managed <file>] [--user <file>]
```

Remember while reading the result: `permissions.allow` arrays **merge** across scopes, and evaluation is
deny, then ask, then allow, first match wins. A strict shared file does not cancel a permissive user file.

## Report

1. Verdict: CLEAN (0) / WARNINGS (2) / **BLOCKED (4)**.
2. Every BLOCKER with its fix: blanket `Bash` allows, pre-approved destructive commands, literal credentials,
   committed `.claude/settings.local.json`, managed `bypassPermissions`.
3. Dead rules (an allow shadowed by deny or ask, `mcp__*` in allow, `defaultMode` set where Claude Code ignores it).
4. Whether a managed policy disables bypass mode. If not, say that any engineer can skip every prompt.
