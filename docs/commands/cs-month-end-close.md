---
title: "/cs-month-end-close — Slash Command for AI Coding Agents"
description: "Full close pass - plan the calendar on its critical path, prove each reconciliation, and gate flux explanations, with a BLOCKED / AT RISK / READY. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-month-end-close

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/finance/month-end-close/commands/cs-month-end-close.md">Source</a></span>
</div>


Run the close gates over `$ARGUMENTS`. Skip any step whose input was not given and say so.

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/month-end-close/scripts/close_calendar_planner.py --plan <close_plan.json>
python ${CLAUDE_PLUGIN_ROOT}/skills/month-end-close/scripts/reconciliation_matcher.py --gl <gl.csv> --source <source.csv> \
  --gl-balance <n> --source-balance <n> --as-of <period end> --preparer <name> --reviewer <name>
python ${CLAUDE_PLUGIN_ROOT}/skills/month-end-close/scripts/flux_analyzer.py --input <tb_compare.csv> --pct <policy> --abs <policy> --reviewer <name>
```

Ask for any balance, period end, preparer, reviewer or threshold that is missing. Do not assume a materiality threshold.

## Report

1. **Verdict**: BLOCKED if any script exits 4, AT RISK if any exits 2, otherwise READY.
2. **Critical path**: the chain, its finish workday versus target, and who owns most of it.
3. **Blockers**: every BLOCKER line verbatim, each with its owner.
4. **Reconciliations**: proof, unexplained difference and hints, aged items, journal entries needed.
5. **Flux**: material accounts with failing explanations, and what is missing from each.
6. **One change** that would remove the most days from the close.
