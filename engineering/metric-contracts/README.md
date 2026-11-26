# metric-contracts

One owned, versioned definition per business metric, and a reason when two
dashboards disagree. Reads dbt's `semantic_manifest.json` (written by
`dbt parse`, no warehouse query) or a plain contract JSON for any other tool.
Three stdlib Python scripts; read-only.

| Script | Answers |
|---|---|
| `metric_contract_lint.py` | Is every metric owned, resolvable and computed sensibly (no average of ratios, no summed balances, count vs count_distinct, no duplicate or conflicting definitions)? |
| `metric_diff.py` | What does this PR do to the numbers: breaking, renamed, removed, affected downstream, cosmetic; was the version bumped; which dashboards to warn? |
| `metric_reconcile.py` | Why do two sources disagree: time zone bucketing, unit or VAT scale, constant gap, step change, late data, excluded subset, join fan-out? |

```bash
/plugin install metric-contracts@claude-code-skills
/cs-metric-check target/semantic_manifest.json --base base/semantic_manifest.json
/cs-metric-reconcile warehouse.csv dashboard.csv
```

Artifact shapes verified against dbt-core 1.12.7 (2026-11-26); see
`skills/metric-contracts/references/`. Agent: `cs-metric-steward`. License: MIT.
