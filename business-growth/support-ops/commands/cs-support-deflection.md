---
disable-model-invocation: true
description: Rank ticket contact reasons and route each to a help-center article, a macro or workflow, or a product fix.
argument-hint: "<tickets.csv> [--min-tickets 20] [--pareto 0.8]"
---

# /cs-support-deflection

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/support-ops/scripts/deflection_finder.py --tickets <csv> [flags]
```

For each DEFLECT reason, draft the article outline from the top macro. For each FIX_ROOT_CAUSE reason, draft the bug report with ticket count, hours and three example ticket ids. State that deflection hours are an upper bound until the topic's contact rate is measured after launch.
