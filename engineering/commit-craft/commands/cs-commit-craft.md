---
disable-model-invocation: true
description: Turn the current working tree into a clean commit series - plan the groups, gate each one for secrets, write messages that say why, and lint the series before push.
argument-hint: "[repo path] [--push]"
---

# /cs-commit-craft

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
