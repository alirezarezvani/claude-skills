# Metric change notice: `<metric>` v<old> -> v<new>

**Owner:** <@team>  **Effective:** <date, and from which period the numbers change>

## What changes

| Field | Before | After |
|---|---|---|
| <filter / agg / expr / time dimension> | <before> | <after> |

From `metric_diff.py`: <paste the BREAKING block>.

## Effect on the number

- Last full period under the old definition: <value>; under the new one: <value> (<+/- %>).
- History: <restated back to <date> | not restated; the series has a break at <date>>.

## Who is affected

- Dashboards and reports (dbt exposures / contract consumers): <list from the `tell:` lines>
- Metrics built on this one (AFFECTED): <list>

## What consumers need to do

- <nothing: dashboards pick it up on the next refresh>
- <annotate the break on trend charts at <date>>
- <targets or alerts set on the old number: re-baseline them>

Questions to <owner>. Old definition kept as `<metric>_v<old>` until <date> | not kept.
