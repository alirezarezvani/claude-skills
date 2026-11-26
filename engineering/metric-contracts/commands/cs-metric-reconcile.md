---
disable-model-invocation: true
description: Two sources report different numbers for one metric - compare two CSV exports by period and name the pattern of the gap (time zone, unit or VAT, step change, late data, excluded subset, fan-out).
argument-hint: "<a.csv> <b.csv> [--key col] [--value col] [--rel-tol 0.005]"
---

# /cs-metric-reconcile

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/metric-contracts/scripts/metric_reconcile.py --a <a.csv> --b <b.csv> [--key <col>] [--value <col>] [--rel-tol 0.005]
```

Each CSV holds one metric at one grain: a key column (period or other key) and a value column. Use the more trusted source as `--a`.

Report the most likely pattern with its evidence, then the next check it names. Do not suggest editing either side until that check confirms the cause. For SUBSET or MIXED, ask for both exports split by one dimension (status, region, account type) and reconcile each slice.
