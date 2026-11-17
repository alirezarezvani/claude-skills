---
name: cloud-finops
description: "Analyse a cloud bill (AWS, Azure, Google Cloud) from a FOCUS cost export. Use when the cloud bill jumped, to find who owns untagged spend, to check Savings Plans, Reserved Instances or committed use discounts (utilization, coverage, effective savings rate) before buying more, or to track cost per customer or per order."
argument-hint: "<focus_export.csv> [--required-tags team,env] [--units units.csv]"
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "Three deterministic stdlib scripts over a FOCUS 1.x CSV (allocation coverage and tag hygiene, commitment utilization/coverage/ESR with a sizing floor, robust anomaly and unit-cost detector) with typed exit codes; definitions cited to the FOCUS v1.4 specification and the FinOps Foundation Framework and ESR working-group paper"
  distinct_from: "llm-cost-optimizer (LLM API token spend); procurement-optimizer (SaaS vendor spend); aws-solution-architect, azure-cloud-architect, gcp-cloud-architect (architecture design, not billing data); cfo-advisor (company finance)"
---

# Cloud FinOps

> **Portability:** 3 stdlib Python scripts plus a shared loader. Input is a CSV you export; no cloud credentials, no API calls.
> **Definitions verified 2026-11-17** against FOCUS v1.4 and the FinOps Foundation.

A cloud bill answers "how much"; it rarely answers "whose", "was the discount
worth it" or "is this spike real". FOCUS, the open billing schema that AWS,
Azure and Google Cloud all export, makes the three questions computable the
same way on every provider. This skill computes them and refuses the common
shortcuts: allocating by BilledCost, measuring coverage in discounted dollars,
buying commitments while existing ones sit idle, and alerting on percentages
alone.

## Workflow

```bash
# 0 - Export FOCUS: AWS Data Exports (FOCUS 1.x), Azure Cost Management export (FOCUS), GCP BigQuery FOCUS view
# 1 - Who owns the spend?
python scripts/allocation_check.py --input focus.csv --required-tags team,env,cost-center
# 2 - Are the commitments earning their keep? Should we buy more?
python scripts/commitment_check.py --input focus.csv --eligible Compute
# 3 - What changed, and is it the business or the bill?
python scripts/cost_anomaly.py --input focus.csv --units orders.csv
```

**Step 1** reports the share of EffectiveCost carrying every required tag,
the largest unallocated resources, and tag values that split one owner
(`Prod`/`prod`). Cost with no ResourceId (shared charges, unused commitment)
needs a split rule, not a tag.

**Step 2** computes utilization, coverage in on-demand equivalent (ListCost),
and the effective savings rate with unused commitment counted as negative
savings. It names under-used commitments, says "fix utilization first" when
coverage is low and commitments are idle, and gives the lowest daily uncovered
spend as the size a new commitment would keep fully used.

**Step 3** flags a group-day only when it beats a robust z-score (median and
MAD), a relative floor and a money floor together, and compares cost per
business unit between the two halves of the period. Under 14 days it refuses.

## Hard rules

- **EffectiveCost for ownership and trends; BilledCost only for the invoice.** Purchases are spread by EffectiveCost.
- **Never recommend a commitment purchase while utilization is under target.** Move workloads onto what is paid for first.
- **Size new commitments to the floor, not the average.** Above the floor is a growth bet; say it is one.
- **Thresholds and targets are policy.** State every default you used (`--target`, `--min-coverage`, `-k`, `--min-abs`).
- **A total that rises with the business is not an anomaly.** Check unit cost before calling a spike waste.
- **Read-only.** Never change tags, buy or exchange commitments, or delete resources; produce the recommendation and its numbers.

## Scripts

| Script | Role | Exit codes |
|---|---|---|
| `scripts/allocation_check.py` | Allocation coverage, spend by category and account, unallocated resources, tag hygiene | 0 at target · 2 findings · 3 bad input |
| `scripts/commitment_check.py` | Utilization, coverage, ESR, per-commitment waste, sizing floor | 0 healthy · 2 findings · 3 bad input |
| `scripts/cost_anomaly.py` | Robust daily anomalies by service or account, unit-cost drift | 0 none · 2 findings · 3 bad input |

All support `--help`, `--sample` and `--output json`. `scripts/focus_common.py` is the shared loader.

## References and assets

- [`references/focus_and_allocation.md`](references/focus_and_allocation.md): FOCUS columns, EffectiveCost vs BilledCost, allocation and shared costs (7 sources)
- [`references/commitments_and_esr.md`](references/commitments_and_esr.md): coverage, utilization, ESR formulas and the decisions they drive (6 sources)
- [`references/anomalies_and_unit_economics.md`](references/anomalies_and_unit_economics.md): the detector, its defaults, unit cost (7 sources)
- [`assets/focus_export.example.csv`](assets/focus_export.example.csv): 14-day FOCUS sample
- [`assets/finops_review_template.md`](assets/finops_review_template.md): monthly review write-up
