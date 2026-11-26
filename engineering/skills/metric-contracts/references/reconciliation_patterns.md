# Why two sources disagree: the patterns and what each means

Two correct pipelines report different numbers when they answer slightly
different questions. The shape of the difference across periods usually names
the question. `metric_reconcile.py` tests for these shapes in this order and
reports every one that fits; the first is the most likely.

| Pattern | Signature in the data | Usual cause | Next check |
|---|---|---|---|
| COVERAGE | Keys on one side only | Not loaded yet (end), different history start (start), failed load (middle) | Load times; date filters |
| BUCKETING | Totals agree, periods differ | Time zone (UTC vs local), or a different date column (order vs ship vs payment date) | Time zone and date column of both |
| SCALE | b = k x a on every period, k steady | Cents vs units, percent vs fraction, VAT or tax included, FX | Unit, currency, tax treatment |
| OFFSET | b = a + c on every period | A manual adjustment or a single record on one side | Adjustment tables, seeds |
| STEP | Agree until a date, differ from then on | Definition change, deploy, new filter, source switch | What changed on that date (`metric_diff.py`, git log) |
| TAIL | Only the last 1-3 periods differ | Late-arriving data, restatement, different refresh time | Rerun after the next load |
| SUBSET | One side always lower, by a varying share | Excludes refunds, cancellations, test or internal accounts, a region | Split both by status and account type |
| SUBSET (higher) | One side always higher, varying share | Join fan-out double counting, looser filter | Row counts before and after each join |
| MIXED | None fits | Several causes at once | Diff the definitions, then split by one dimension at a time |

Defaults: relative tolerance 0.5% (`--rel-tol`), absolute 0 (`--abs-tol`).
Both are policy; finance close usually wants 0 on currency amounts, product
dashboards often accept 1%. State what you used.

## Two definitional errors that look like data problems

**Averaging ratios.** The average of per-order discount rates is not the
discount rate: a 50% discount on a 2 EUR order weighs as much as 5% on a 2,000
EUR order. The rate is sum(discount) / sum(amount). Aggregating ratios across
groups of different size can even reverse a comparison (Simpson's paradox).
Define a ratio metric of two sums; the linter flags `agg: average` over an
expression containing `/` (MC05).

**Adding snapshots.** A balance, MRR, inventory or headcount is a level at a
point in time. Summing it across days gives a meaningless number (Kimball's
semi-additive fact: additive across accounts, not across time). Take the
period-end value with a `non_additive_dimension` on the snapshot date (MC07).

**Counting rows for people.** `count(customer_id)` on an orders table counts
orders. Users, customers and accounts are `count_distinct` (MC06). Active
users also need the window stated (daily, 28-day), or two teams will compute
DAU and MAU and call both "active users".

## How to get the two CSVs

Export the same metric at the same grain from both places: one row per period
(or per key such as region), columns `key,value`, no subtotals. From
MetricFlow: `dbt sl query --metrics revenue --group-by metric_time__day` or
`mf query`; from a BI tool, export the chart's data. Use the source you trust
more as `--a`. When the pattern is SUBSET or MIXED, export both again split by
one dimension (status, region, account type) and reconcile each slice; the
slice with the gap is the cause.

## Sources

1. Kimball Group, "Additive, Semi-Additive, and Non-Additive Facts". https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/additive-semi-additive-non-additive-fact/
2. dbt Labs, "Measures" (`non_additive_dimension` for balances and MRR). https://docs.getdbt.com/docs/build/measures
3. dbt Labs, "Creating metrics" (ratio metrics as numerator and denominator). https://docs.getdbt.com/docs/build/metrics-overview
4. Stanford Encyclopedia of Philosophy, "Simpson's Paradox". https://plato.stanford.edu/entries/paradox-simpson/
5. dbt Labs, "MetricFlow time spine" (time granularity and bucketing). https://docs.getdbt.com/docs/build/metricflow-time-spine
6. dbt Labs, "Joins" (MetricFlow join types and fan-out avoidance). https://docs.getdbt.com/docs/build/join-logic
7. dbt Labs, "Semantic manifest" artifact. https://docs.getdbt.com/reference/artifacts/sl-manifest
