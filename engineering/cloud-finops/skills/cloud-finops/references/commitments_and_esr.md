# Commitments, coverage and the effective savings rate

Verified 2026-11-17. 🟢 read on the primary page this session, 🟡 primary not re-read, 🔴 convention.

## Definitions the script uses

- 🟢 **Coverage:** "the percentage of eligible workloads that were covered by active commitments during the specified period". [1]
- 🟢 **Utilization:** "the percentage of active commitments utilized during the specified period". [1]
- 🟢 **Effective savings rate (ESR)** = savings / on-demand equivalent (ODE) spend; equivalently utilization × coverage × discount. The Foundation's worked example: 90% × 100% × 50% = 45%. [1]

FOCUS makes these computable: usage covered by a commitment has `CommitmentDiscountStatus = Used` and `PricingCategory = Committed`; capacity nobody used appears as `Unused` rows whose EffectiveCost is the waste. [2]

Formulas in `commitment_check.py`:

```
utilization = EffectiveCost(Used) / EffectiveCost(Used + Unused)
coverage    = ListCost(Used, eligible) / ListCost(eligible usage)
ESR         = (ListCost(eligible) - EffectiveCost(eligible) - EffectiveCost(Unused)) / ListCost(eligible)
```

Coverage uses ListCost because a covered hour is cheaper: measuring coverage in EffectiveCost understates it by the discount. ListCost equals the on-demand price for AWS, Azure and Google public pricing; for negotiated-rate accounts it is an approximation (🟡). ESR counts unused commitment as negative savings, which is the point: a 72% discount at 60% utilization can save less than a 40% discount at 100%.

## Decisions the numbers drive

1. **Utilization first.** Under-used commitments are sunk cost; buying more while one sits at 80% compounds the waste. The script reports `BUY_WHILE_WASTING` rather than a coverage gap in that case.
2. **Size to the floor.** The lowest daily uncovered eligible spend over the window is what a new commitment would cover every day. Above it you are betting on growth, which may be right, but say so. 🔴 (standard practice; see [3][4])
3. **Prefer flexible instruments when the floor moves.** Compute Savings Plans cover instance family, Region and some serverless; EC2 Instance Savings Plans and Standard RIs discount more but bind more. 🟡 [4][5]
4. **Commitment terms outlive architecture.** A 3-year term on a workload you plan to move to containers or ARM is a migration tax. 🔴

## Sources

1. FinOps Foundation working group, "How to Calculate Effective Savings Rate (ESR)", finops.org/wg/how-to-calculate-effective-savings-rate-esr/
2. FinOps Foundation, FOCUS v1.4 Appendix 8.2 "Examples: Commitment Discounts", focus.finops.org/docs/specification/v1-4/sections/appendix/commitment-discounts/
3. FinOps Foundation, "Rate Optimization" FinOps Framework capability, finops.org/framework/capabilities/rate-optimization/
4. AWS, Savings Plans User Guide, "What are Savings Plans?", docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html
5. Google Cloud, "Committed use discounts", cloud.google.com/docs/cuds
6. Microsoft Learn, "What are Azure savings plans for compute?", learn.microsoft.com/azure/cost-management-billing/savings-plan/savings-plan-compute-overview
