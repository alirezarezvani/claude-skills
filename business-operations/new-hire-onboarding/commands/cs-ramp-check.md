---
disable-model-invocation: true
description: Check a new hire's first 90 days against their plan - missed day-30/60/90 checkpoints, overdue milestones, a lapsed buddy or a long gap between manager 1:1s.
argument-hint: "<ramp.json> [--today YYYY-MM-DD] [--grace 5]"
---

# /cs-ramp-check

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/new-hire-onboarding/scripts/ramp_check.py --log <json> [flags]
```

Template: `${CLAUDE_PLUGIN_ROOT}/skills/new-hire-onboarding/assets/ramp.example.json`.

## Report

1. Verdict and day number, then each finding with what to do this week.
2. Where a milestone slipped with no checkpoint held, say so first: ask what blocked it before judging the hire.
3. No probation or performance verdict; that belongs to the manager and HR.
