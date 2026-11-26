---
name: metric-contracts
description: "Use when two dashboards or teams report different numbers for the same metric (revenue, active users, churn, MRR), when a dbt semantic layer or MetricFlow metric changes in a PR and you need to know what it breaks, or when defining metrics with an owner, version and one agreed definition. Lints semantic_manifest.json, diffs metric definitions for breaking changes, reconciles two sources."
argument-hint: "<semantic_manifest.json | contract.json> [--base base.json --head head.json] [--a a.csv --b b.csv]"
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "Three deterministic stdlib scripts over dbt's semantic_manifest.json (legacy and 1.12 spec, verified against dbt-core 1.12.7 artifacts) or a plain contract JSON: a 13-rule definition linter, a base-vs-head metric diff that classifies breaking, transitive and cosmetic changes and gates on version bumps, and a two-source reconciler that names the pattern of the gap"
  distinct_from: "data-quality-auditor (profiles a dataset's values, not metric definitions); senior-data-engineer (builds pipelines and dbt models); snowflake-development (warehouse SQL); product-team analytics skills (choose which metrics matter, not keep their definitions consistent)"
---

# Metric Contracts

> **Portability:** 3 stdlib Python scripts plus a shared loader. Input is a file you already have; no warehouse access, no credentials.
> **dbt artifact shapes verified 2026-11-26** against `semantic_manifest.json` written by dbt-core 1.12.7 (legacy and 1.12 spec).

When finance says revenue was 412k and the product dashboard says 431k, both
are usually right about a different definition. A metric contract makes the
definition an object with an owner and a version, so a change that moves the
number is visible before it ships, and a gap between two sources gets a cause
instead of a meeting.

## Workflow

```bash
# 0 - dbt users: produce the artifacts (no warehouse query runs)
dbt parse                       # writes target/semantic_manifest.json and target/manifest.json
# 1 - Are the definitions sound?
python scripts/metric_contract_lint.py --input target/semantic_manifest.json
# 2 - What does this PR do to the numbers? (base artifact from the main branch)
python scripts/metric_diff.py --base base/semantic_manifest.json --head target/semantic_manifest.json --manifest target/manifest.json
# 3 - Why do two sources disagree? (one CSV per source: period, value)
python scripts/metric_reconcile.py --a warehouse.csv --b dashboard.csv --rel-tol 0.005
```

No dbt? Write the definitions in the plain contract format
(`assets/metric_contracts.example.json`, schema in
`references/metric_contract_spec.md`) and run the same scripts on it.

**Step 1** checks 13 rules. Errors: no owner, an input that does not exist, an
average of a ratio, a derived expression using an undeclared name, the same
name defined differently in two files, cycles. Warnings: no description, two
names with an identical computation, `count` where `count_distinct` is meant,
a balance or MRR summed over time with no `non_additive_dimension`.

**Step 2** compares every metric's number-deciding fields (aggregation,
expression, filter, time dimension, table, inputs, window). A change there is
BREAKING and must raise the metric's version; a removal or rename must be
accepted by its owner (`--accept`). Metrics built on a broken one are listed as
AFFECTED, and with `--manifest` each change names the dashboards (dbt
exposures) to warn. A pure rename upstream does not count as a change downstream.

**Step 3** matches the two series on the key and names the pattern: totals
agree but periods do not (time zone or date column), a constant factor (cents,
VAT, currency), a constant gap, a step from one date, only the latest periods
(freshness), or one side always lower (it excludes refunds, test accounts) or
higher (join fan-out). Each pattern comes with the next check to run.

## Hard rules

- **One business term, one definition.** Two names for the same computation drift; two computations for one name mislead. Keep one, alias the rest.
- **A change that moves the number is a breaking change.** It gets a version bump and a notice to every consumer, even when it is a fix.
- **Every metric has a named owner** who approves changes and answers for the number.
- **Ratios are ratios of sums.** Never average per-row ratios; never sum a snapshot quantity over time.
- **Do not edit either side of a mismatch until the pattern is named.** A forced match hides the real definition gap.
- **Tolerances and version policy are the team's.** State `--rel-tol`, `--abs-tol`, `--require-version` and every `--accept` you used.
- **Read-only.** The scripts never query a warehouse or change a definition; you propose the edit and the owner approves it.

## Scripts

| Script | Role | Exit codes |
|---|---|---|
| `scripts/metric_contract_lint.py` | 13 definition rules (MC01-MC13) over one or more files | 0 clean · 2 findings · 3 bad input |
| `scripts/metric_diff.py` | Base vs head: BREAKING / REMOVED / RENAMED / AFFECTED / COSMETIC / ADDED, version-bump gate, consumers | 0 acknowledged · 2 unacknowledged · 3 bad input |
| `scripts/metric_reconcile.py` | Two sources of one metric: tolerance check and cause pattern | 0 match · 2 mismatch · 3 bad input |

All support `--help`, `--sample` and `--output json`. `scripts/metric_common.py` is the shared loader.

## References and assets

- [`references/metric_contract_spec.md`](references/metric_contract_spec.md): contract fields, the dbt artifact shapes the loader reads, the plain JSON format (7 sources)
- [`references/breaking_changes.md`](references/breaking_changes.md): which edits move the number, versioning, consumer notice, CI wiring (6 sources)
- [`references/reconciliation_patterns.md`](references/reconciliation_patterns.md): the seven gap patterns, additivity, average of ratios (7 sources)
- `assets/semantic_manifest.base.json`, `assets/semantic_manifest.head.json`, `assets/manifest_exposures.example.json`: real dbt 1.12.7 artifacts with planted issues
- `assets/metric_contracts.example.json`: plain contract format
- `assets/revenue_warehouse.csv`, `assets/revenue_bi_tool.csv`: a time-zone mismatch to reconcile
- [`assets/metric_change_notice.md`](assets/metric_change_notice.md): the notice to send consumers of a breaking change
