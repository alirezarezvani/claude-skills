# FOCUS exports and cost allocation

Verified 2026-11-17. 🟢 read on the primary page this session, 🟡 primary but not re-read, 🔴 practitioner convention.

## Why FOCUS

🟢 FOCUS (FinOps Open Cost and Usage Specification) is the FinOps Foundation's open schema for billing data; v1.4 is the current version and its Cost and Usage dataset has 65 columns (21 mandatory). [1] AWS (Data Exports), Microsoft (Cost Management exports) and Google Cloud (BigQuery FOCUS view) publish FOCUS-shaped exports, so one script works on all three. [2][3]

Columns the scripts use:

| Column | Level in v1.4 | Used for |
|---|---|---|
| BilledCost, EffectiveCost, ListCost, ContractedCost | Mandatory | invoice view, amortised view, on-demand equivalent |
| ChargeCategory (Usage, Purchase, Tax, Credit, Adjustment) | Mandatory | excluding tax, separating purchases |
| ChargePeriodStart, BillingCurrency | Mandatory | daily series, refusing mixed currencies |
| ServiceCategory, ServiceName | Mandatory | grouping |
| SubAccountName / SubAccountId | Conditional | account view |
| ResourceId | Conditional | naming unallocated resources |
| Tags | Conditional | allocation |
| PricingCategory, CommitmentDiscountId, CommitmentDiscountStatus | Conditional | commitments |

🟢 **Use EffectiveCost for allocation and trends.** On a commitment purchase row EffectiveCost is 0 and the cost is spread over the usage rows it covered; unused commitment appears as `Unused` rows that carry EffectiveCost and no resource. [4] BilledCost is the invoice view and puts a whole upfront purchase on one day.

## Allocation coverage

The script measures: EffectiveCost on rows carrying every required tag with a non-empty value, over all non-tax EffectiveCost.

🟢 The FinOps Framework's Allocation capability describes maturity qualitatively ("a significant portion" at Crawl, "a majority" at Walk, "consistently high levels" at Run) and gives **no numeric target**. [5] Figures like "80% at Walk, 90% at Run" circulate widely (🔴) but are not in the Framework text; the script's default `--target 0.9` is a policy choice, so state it as yours.

What coverage misses:
- **Shared costs** (support plans, networking, unused commitments) have no owner tag by nature. Allocate them with a split rule (proportional to direct cost, even, or fixed) agreed with finance, and report them separately. [5][6]
- **Case and spelling variants** (`Prod`, `prod`, `production`) count as tagged but split one owner into several in every report; the script flags them.
- **Tags apply forward only** on most providers: tagging today does not re-tag last month's rows. 🟡 [7]

## Sources

1. FinOps Foundation, FOCUS Specification v1.4, Cost and Usage dataset, focus.finops.org/docs/specification/v1-4/datasets/cost-and-usage/
2. Microsoft Learn, "FOCUS cost and usage details file schema", learn.microsoft.com/azure/cost-management-billing/dataset-schema/cost-usage-details-focus
3. Microsoft Learn, FinOps toolkit, "Validate FOCUS data", learn.microsoft.com/cloud-computing/finops/focus/validate
4. FinOps Foundation, FOCUS v1.4 Appendix 8.2 "Examples: Commitment Discounts", focus.finops.org/docs/specification/v1-4/sections/appendix/commitment-discounts/
5. FinOps Foundation, "Allocation" FinOps Framework capability, finops.org/framework/capabilities/allocation/
6. J.R. Storment & Mike Fuller, *Cloud FinOps*, 2nd ed., O'Reilly 2023, ch. on allocation and shared costs
7. AWS Billing User Guide, "Organizing and tracking costs using AWS cost allocation tags", docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html
