---
disable-model-invocation: true
description: Explain a cloud cost spike from a FOCUS export - which service or account, which day, how far above baseline, and whether unit cost moved.
argument-hint: "<focus_export.csv> [--by ServiceName|SubAccountName] [--units units.csv]"
---

# /cs-cost-spike

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/cloud-finops/scripts/cost_anomaly.py --input <csv> --by <column> [--units <csv>]
```

For each anomaly, filter the export to that group and day and name the resources (ResourceId) and charge descriptions that carry the excess. Then say whether the business grew with it (unit cost) and who owns the resource (Tags). Do not call a spike waste until both are checked.
