---
title: "/cs-sprs-score — Slash Command for AI Coding Agents"
description: "Score a NIST SP 800-171 Rev 2 self-assessment for SPRS and CMMC Level 2, and list what must be fixed before Conditional status is possible.. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-sprs-score

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/ra-qm-team/cmmc-readiness/commands/cs-sprs-score.md">Source</a></span>
</div>


Score `$ARGUMENTS` with the 32 CFR 170.24 weights.

If the file does not cover all 110 requirements, stop and list the missing ones. Do not fill them in.

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/cmmc-readiness/scripts/sprs_score.py --assessment <assessment.csv>
```

## Report

1. Score out of 110 and the verdict (FINAL_ELIGIBLE, CONDITIONAL_ELIGIBLE, NOT_ELIGIBLE, BLOCKED_NO_SSP).
2. Fix before any assessment: identifier, deduction, why it cannot be deferred.
3. POA&M candidates, and the score after fixing the blockers.
4. Any NA without a written reason.

The score is what goes into SPRS for a Basic self-assessment; only the organization posts it.
