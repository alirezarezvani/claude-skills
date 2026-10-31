---
title: "/cs-commit-check — Slash Command for AI Coding Agents"
description: "Check what is staged, or a range about to be pushed, for secrets, sensitive files, vague messages and leftover fixup commits.. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-commit-check

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/engineering/commit-craft/commands/cs-commit-check.md">Source</a></span>
</div>


With no argument, check what is staged. With a range, check the series before push.

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/commit-craft/scripts/secret_gate.py            # staged
python ${CLAUDE_PLUGIN_ROOT}/skills/commit-craft/scripts/secret_gate.py --range <range>
python ${CLAUDE_PLUGIN_ROOT}/skills/commit-craft/scripts/message_linter.py --range <range>
```

## Report

1. The verdict line of each script.
2. Blockers with file:line or commit, and the fix. For a secret: if the range was ever pushed, say to rotate it first, then remove it.
3. Warnings, briefly.
4. Offer to install the hooks from `${CLAUDE_PLUGIN_ROOT}/skills/commit-craft/assets/hooks/` so this runs on every commit and push.
