---
description: Full CMMC Level 2 readiness pass - classify the asset inventory, score all 110 requirements, and check the POA&M against the 180-day closeout deadline.
argument-hint: "inventory.csv assessment.csv [poam.csv --conditional-date YYYY-MM-DD]"
---

# /cs-cmmc-readiness

Answer one question about `$ARGUMENTS`: **would this organization pass a CMMC Level 2 assessment, and if not, what must be fixed first?**

Ask first for anything missing: the contract's level and assessment type (Level 2 Self or C3PAO), and the Conditional
status date if a POA&M is in play. Do not assume a requirement is MET because nobody mentioned it.

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/cmmc-readiness/scripts/scope_classifier.py --inventory <inventory.csv>
python ${CLAUDE_PLUGIN_ROOT}/skills/cmmc-readiness/scripts/sprs_score.py --assessment <assessment.csv> --output json > score.json
python ${CLAUDE_PLUGIN_ROOT}/skills/cmmc-readiness/scripts/poam_closeout.py --score score.json --poam <poam.csv> \
  --conditional-date <YYYY-MM-DD> [--final-date YYYY-MM-DD --last-affirmation YYYY-MM-DD]
```

Skip the POA&M step when the score verdict is FINAL_ELIGIBLE or there is no POA&M yet; say which gaps would go on one.

## Report

1. Score and verdict, then the fix-before-assessment list, largest deduction first.
2. Scope blockers: asset, why, fix.
3. POA&M deadline, days left, and blockers.
4. What was not checked (evidence quality is the assessor's call).

Never affirm or tell the user to affirm. Name the Affirming Official.
