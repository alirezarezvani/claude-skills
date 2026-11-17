---
disable-model-invocation: true
description: Decide whether to widen, hold or halt a staged (Android) or phased (iOS) rollout from crash and ANR counts against the previous release.
argument-hint: "<rollout.csv> [--min-users N] [--max-regression 0.25]"
---

# /cs-rollout-gate

Run the gate on `$ARGUMENTS`:

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/mobile-release/scripts/rollout_gate.py --input <csv> [flags]
```

If the user has no CSV, build one from `${CLAUDE_PLUGIN_ROOT}/skills/mobile-release/assets/rollout.example.csv`: one baseline row (the last full release) and one row for the new release, with users and crashed users as counts. Percentages alone are not enough; ask for counts.

## Report

1. PROCEED / HOLD / HALT and the action, in one line.
2. Crash and ANR rate for both releases, relative change and p-value.
3. The defaults used (min users, max regression, alpha, ladder).
4. On iOS HALT: a paused phased release can still be downloaded manually, so say whether to pull the build.
