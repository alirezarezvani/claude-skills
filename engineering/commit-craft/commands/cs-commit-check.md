---
disable-model-invocation: true
description: Check what is staged, or a range about to be pushed, for secrets, sensitive files, vague messages and leftover fixup commits.
argument-hint: "[commit range, e.g. origin/main..HEAD]"
---

# /cs-commit-check

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
