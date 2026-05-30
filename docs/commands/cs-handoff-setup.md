---
title: "/cs-handoff-setup — Slash Command for AI Coding Agents"
description: "First-run setup for the handoff skill. Walks 5 questions (save location, retention, redaction strictness, git context, recommender scope) and writes. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-handoff-setup

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/productivity/handoff/commands/cs-handoff-setup.md">Source</a></span>
</div>


Configure the handoff skill. Walks 5 questions (plus 1-2 optional) and writes the config. Re-run any time.

## Invocation

```
/cs:handoff-setup                 # configure global defaults
/cs:handoff-setup --project       # set project-specific overrides
```

## Questions

1. **Save location** — OS temp / home folder / hidden home folder / per-project / custom. *No pre-selected default — explicit choice required on first run.*
2. **Retention window** — 7 / 30 days / forever / manual.
3. **Redaction strictness** — strict / warn / off.
4. **Git context** — auto-include branch + last commit + dirty file count? yes/no.
5. **Skill recommendation scope** — all repo / current domain only / off.
6. **Filename style** *(only if save location ≠ temp)* — date_slug / timestamp / mktemp.

## Behaviour

- **Global config** at `~/.config/handoff/config.json`.
- **Project override** at `<repo>/.handoff/config.json` (with `--project`). Missing keys fall back to global.
- For `save_location.mode = project`, setup offers to append `.handoff/` to `.gitignore`.
- Idempotent. Re-running pre-fills current values.

## Reset to defaults

Delete the config and rerun:

```bash
rm ~/.config/handoff/config.json
rm ~/.config/handoff/.setup-declined 2>/dev/null
```

## Run

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/handoff/scripts/setup.py
```

For project-scoped overrides:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/handoff/scripts/setup.py --reconfigure --project
```
