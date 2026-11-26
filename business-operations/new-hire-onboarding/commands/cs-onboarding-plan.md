---
disable-model-invocation: true
description: Build a new hire's 30/60/90-day plan with checkpoints and buddy meetings in the calendar, refusing milestones nobody could check.
argument-hint: "<plan.json> [--profile standard|engineering|sales|support|executive]"
---

# /cs-onboarding-plan

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/new-hire-onboarding/scripts/plan_builder.py --plan <json> --output md [--profile P]
```

No plan file? Start from `${CLAUDE_PLUGIN_ROOT}/skills/new-hire-onboarding/assets/plan.example.json`. Ask, one at a time: the start date, what the hire should have done by day 30 that someone could see, the buddy (a peer, not the manager), then days 60 and 90.

## Report

The markdown plan the script prints. Rewrite any refused milestone as a checkable suggestion, then re-run until it builds.
