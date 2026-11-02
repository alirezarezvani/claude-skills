---
disable-model-invocation: true
description: Check an agent's summary, handoff or "tests pass" against what its recorded run actually did.
argument-hint: "[--session ID | --trace PATH] <claims or summary text>"
---

# /cs-check-claims

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
