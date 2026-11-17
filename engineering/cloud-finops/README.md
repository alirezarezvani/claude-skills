# cloud-finops

Answer "whose spend is this", "is the discount paying off" and "is this spike
real" from a FOCUS cost export. Works the same on AWS, Azure and Google Cloud
because all three export FOCUS. Three stdlib Python scripts; no credentials,
no API calls, read-only.

| Script | Answers |
|---|---|
| `allocation_check.py` | Share of spend with owner tags, biggest unallocated resources, tag values that split an owner |
| `commitment_check.py` | Savings Plan / RI / CUD utilization, coverage, effective savings rate, how much more to commit (if any) |
| `cost_anomaly.py` | Which service or account spiked on which day, and whether cost per order or user moved |

```bash
/plugin install cloud-finops@claude-code-skills
/cs-finops-review focus_export.csv --required-tags team,env,cost-center
/cs-cost-spike focus_export.csv --units orders.csv
```

Definitions follow FOCUS v1.4 and the FinOps Foundation (verified 2026-11-17);
see `skills/cloud-finops/references/`. Agent: `cs-finops-analyst`. License: MIT.
