---
title: "/cs-commit-craft — Slash Command for AI Coding Agents"
description: "Turn the current working tree into a clean commit series - plan the groups, gate each one for secrets, write messages that say why, and lint the. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-commit-craft

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/engineering/commit-craft/commands/cs-commit-craft.md">Source</a></span>
</div>


Turn the uncommitted work in `$ARGUMENTS` (default: the current repo) into a reviewable series.

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/commit-craft/scripts/commit_planner.py
# for each planned group, in order:
git add -- <files>            # git add -p -- <file> for MIXED_FORMATTING files
python ${CLAUDE_PLUGIN_ROOT}/skills/commit-craft/scripts/secret_gate.py
python ${CLAUDE_PLUGIN_ROOT}/skills/commit-craft/scripts/message_linter.py -m "<message>" --staged
git commit -m "<message>"
# then the series
python ${CLAUDE_PLUGIN_ROOT}/skills/commit-craft/scripts/message_linter.py --range @{upstream}..HEAD
```

Stop at the first BLOCKED gate and report it; do not commit around it. Push only if `--push` was given.

## Report

1. The plan: numbered groups with subject and files, and each default you chose (type, scope, order).
2. Anything held back: secrets files, waivers with their reasons, files you staged by hunk.
3. The final `git log --oneline` of the new commits.
4. Whether every commit was tested (`git rebase -x "<test command>" @{upstream}`) or that this is still owed.
