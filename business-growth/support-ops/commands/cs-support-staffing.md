---
disable-model-invocation: true
description: Size a support team per interval with Erlang C (phone, chat) or workload (email), with shrinkage, occupancy cap and roster gap.
argument-hint: "--intervals volumes.csv --aht SECONDS [--mode live|async] [--concurrency N]"
---

# /cs-support-staffing

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/support-ops/scripts/staffing_plan.py $ARGUMENTS
```

Input format: `${CLAUDE_PLUGIN_ROOT}/skills/support-ops/assets/intervals.example.csv`. Ask for AHT (handle plus wrap-up, in seconds) and the service-level goal if not given; use 80% in 60 s only as a stated default.

## Report

Peak agents to schedule, total agent-hours, intervals where the roster is short, and every assumption used.
