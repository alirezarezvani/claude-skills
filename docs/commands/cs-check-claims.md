---
title: "/cs-check-claims — Slash Command for AI Coding Agents"
description: "Check an agent's summary, handoff or 'tests pass' against what its recorded run actually did.. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-check-claims

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/engineering/agent-run-forensics/commands/cs-check-claims.md">Source</a></span>
</div>


Turn each factual sentence of the summary in `$ARGUMENTS` (default: your own last
report in this session) into a typed claim and check it.

```bash
S=${CLAUDE_PLUGIN_ROOT}/skills/agent-run-forensics/scripts
python3 $S/claim_checker.py --trace <path> \
  --claim "passed:<test command>" --claim "edited:<file>" --claim "not-edited:<file>" --claim "ran:<command>"
```

Claim kinds: `ran:`, `not-run:`, `passed:`, `failed:`, `edited:`, `not-edited:`, `read:`.

## Report

1. The verdict line.
2. Every CONTRADICTED claim first, with the step that contradicts it, as a correction.
3. STALE, PARTIAL, INFERRED and NOT_IN_TRACE claims, one line each.
4. Claims that held, briefly.
