---
disable-model-invocation: true
description: Monthly cloud cost review from a FOCUS export - allocation coverage, commitment utilization, coverage and effective savings rate, anomalies and unit cost.
argument-hint: "<focus_export.csv> [--required-tags team,env,cost-center] [--units units.csv]"
---

# /cs-finops-review

Review the FOCUS export in `$ARGUMENTS`:

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/cloud-finops/scripts/allocation_check.py --input <csv> --required-tags <keys>
python ${CLAUDE_PLUGIN_ROOT}/skills/cloud-finops/scripts/commitment_check.py --input <csv>
python ${CLAUDE_PLUGIN_ROOT}/skills/cloud-finops/scripts/cost_anomaly.py --input <csv> [--units <csv>]
```

If the user has no export, tell them how to create a FOCUS export for their provider and stop.

## Report

Fill `${CLAUDE_PLUGIN_ROOT}/skills/cloud-finops/assets/finops_review_template.md`, then give the three actions with the most money at stake, each with an owner. List the defaults used.
