---
disable-model-invocation: true
description: Check that a new hire can work on day one - every preboarding task dated against the start date, the I-9 or UK right-to-work deadline, and a named manager and buddy.
argument-hint: "<hire.json> [--today YYYY-MM-DD] [--jurisdiction US|UK|other]"
---

# /cs-preboarding-check

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/new-hire-onboarding/scripts/preboarding_gate.py --hire <json> [flags]
```

No hire file? Build one from `${CLAUDE_PLUGIN_ROOT}/skills/new-hire-onboarding/assets/hire.example.json` after asking the start date, the country of employment, remote or on site, the manager, the buddy, and each task's owner.

## Report

1. Verdict, then LATE and AT_RISK tasks with owner and due date, blocking ones first.
2. The right-to-work deadline (I-9 Section 1 and 2 dates, or the UK check date).
3. Missing items and the defaults used.
