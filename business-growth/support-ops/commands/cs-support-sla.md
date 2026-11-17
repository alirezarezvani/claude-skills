---
disable-model-invocation: true
description: Check support SLA attainment and breach risk from a ticket export on the contract's business or calendar clock.
argument-hint: "<tickets.csv> <sla_policy.json> [--risk-hours 2] [--reopen-breaches]"
---

# /cs-support-sla

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/support-ops/scripts/sla_check.py --tickets <csv> --policy <json> [flags]
```

No policy file? Build one from `${CLAUDE_PLUGIN_ROOT}/skills/support-ops/assets/sla_policy.example.json` after asking for each priority's targets, the clock (business or calendar), working hours, timezone and holidays.

## Report

1. Verdict and the open tickets already breached, then those at risk, each with hours over or left.
2. Attainment per priority for first response and resolution, against the target.
3. Backlog age and reopen rate, and the defaults used.
