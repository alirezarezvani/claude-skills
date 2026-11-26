# Metric contract: fields and input formats

A metric contract is the definition of one business number, written down with
the facts a consumer needs to trust it and an owner who approves changes. The
scripts read it from dbt's semantic layer artifact or from a plain JSON file.

## The fields that matter

| Field | Why it is in the contract | Lint rule |
|---|---|---|
| `name` | The one name the business uses. Synonyms become aliases, not copies | MC04, MC10 |
| `owner` | Who approves a change and answers "why did it move" | MC01 |
| `description` | What is counted, what is excluded, unit | MC02 |
| `version` | Tells a fix that moves the number from a cosmetic edit | MC09, diff gate |
| `type` | simple, ratio, derived, cumulative, conversion | MC11 |
| `agg` + `expr` | The computation: sum, count, count_distinct, average, min, max, median, percentile, sum_boolean | MC05, MC06, MC11 |
| `filter` | Which rows count (paid only, no test accounts) | diff |
| `time_dimension` | Which date the number is bucketed by, and in which time zone | MC13 |
| `source_table` / relation | Where the rows come from | diff |
| `numerator`, `denominator`, `inputs` | What a ratio or derived metric is built from | MC03, MC08, MC12 |
| `non_additive_dimension` | The snapshot date for balances, MRR, inventory: take the last value, do not add days | MC07 |
| `consumers` | Dashboards and reports to warn on a breaking change | diff `tell:` |

The number-deciding fields (`metric_common.NUMERIC_FIELDS`) are agg, expr,
filter, time dimension, relation, inputs, numerator, denominator, non-additive
dimension, window, grain-to-date, percentile, conversion parameters,
fill-nulls and time-spine join. A change to any of them is BREAKING in
`metric_diff.py`. Description, label, owner and unit text are COSMETIC.

## dbt: read the artifact, not the YAML

`dbt parse` writes `target/semantic_manifest.json` without querying the
warehouse. It is JSON, so the scripts stay stdlib-only, and it is the resolved
form after Jinja, so what is linted is what MetricFlow will run. The loader
reads both shapes (verified 2026-11-26 against dbt-core 1.12.7 output):

- **Legacy spec.** Measures live on `semantic_models[].measures[]` with `agg`,
  `expr`, `agg_time_dimension` and `non_additive_dimension`. A simple metric
  points at one through `type_params.measure` (`{name, filter, alias,
  fill_nulls_with, join_to_timespine}`); the loader resolves the measure and
  merges its filter with the metric filter.
- **dbt 1.12 spec.** Simple metrics are defined on the model and the artifact
  carries `type_params.metric_aggregation_params` (`semantic_model`, `agg`,
  `agg_params.percentile`, `agg_time_dimension`, `non_additive_dimension`)
  with the column in `type_params.expr`; `measures` is empty.
- **Both.** Ratio metrics use `type_params.numerator` / `denominator`, derived
  metrics `type_params.expr` plus `type_params.metrics[]`, cumulative metrics
  `type_params.cumulative_type_params.metric`, conversion metrics
  `type_params.conversion_type_params`. Filters are
  `filter.where_filters[].where_sql_template`. Owner and version come from
  `config.meta` (`meta` is also read).

Exposures (the dashboards and reports that read a metric) are in
`target/manifest.json` under `exposures.<id>.depends_on.nodes`, as
`metric.<project>.<name>`. `metric_diff.py --manifest` reads only that key.

dbt has no `version` field for metrics (model versions exist for models only),
so put it in `config.meta.version`. Use integers or dotted versions; the gate
compares them numerically.

## Plain contract format (any other tool)

For Cube, LookML, a BI tool's calculated fields or a spreadsheet, transcribe
each metric once into JSON (YAML works when PyYAML is installed):

```json
{"metrics": [{
  "name": "net_revenue", "owner": "@finance-analytics", "version": "2.0",
  "description": "Paid order value in EUR, excluding VAT, refunds netted on the refund date.",
  "type": "simple", "agg": "sum", "expr": "amount_excl_vat - refunded_amount",
  "filter": "status in ('paid', 'refunded') and is_test_account = false",
  "time_dimension": "order_date (Europe/Berlin)", "source_table": "analytics.fct_orders",
  "consumers": ["Looker: Exec KPIs"]}]}
```

Ratio and derived metrics take `numerator`, `denominator` and `inputs` as a
metric name or `{"name", "filter", "alias"}`. Put the time zone in
`time_dimension`: it is the most common reason two correct numbers differ.

Data contracts for whole datasets (schema, quality rules, SLAs) are a wider
topic: the Open Data Contract Standard (ODCS, Bitol, Linux Foundation AI &
Data; v3.1.0 in December 2025) covers them, and dbt model contracts enforce a
model's column names and types at build time. Neither defines how a metric is
computed, which is what this skill checks. Use them together.

## Sources

1. dbt Labs, "Semantic manifest" (`semantic_manifest.json` artifact reference). https://docs.getdbt.com/reference/artifacts/sl-manifest
2. dbt Labs, "Creating metrics" (metric types, simple metric properties, `config.meta`). https://docs.getdbt.com/docs/build/metrics-overview
3. dbt Labs, "Migrate to the latest YAML spec" (dbt 1.12: measures replaced by simple metrics, `type_params` promoted). https://docs.getdbt.com/docs/build/latest-metrics-spec
4. dbt Labs, "Measures" (aggregations, `non_additive_dimension`). https://docs.getdbt.com/docs/build/measures
5. dbt Labs, "Add Exposures to your DAG". https://docs.getdbt.com/docs/build/exposures
6. Bitol (Linux Foundation AI & Data), "Open Data Contract Standard". https://bitol-io.github.io/open-data-contract-standard/latest/home ; v3.1.0 release: https://bitol.io/bitol-announces-odcs-v3-1-0-stronger-smarter-and-stricter/
7. dbt Labs, "contract" model config (enforced column names and types). https://docs.getdbt.com/reference/resource-configs/contract
