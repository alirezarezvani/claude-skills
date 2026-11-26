# Breaking metric changes: what moves the number, and what to do about it

A metric change is breaking when a consumer looking at the same period gets a
different number afterwards. That includes fixes. "We were double counting
refunds" is a good change and still a breaking one: a target, an alert, a
board slide and a trend line were built on the old number.

## Classes `metric_diff.py` reports

| Class | Meaning | Gate |
|---|---|---|
| BREAKING | A number-deciding field changed (see `metric_contract_spec.md`) | Fails unless the version went up |
| REMOVED | The name is gone | Fails unless `--accept <name>` |
| RENAMED | Gone under one name, identical computation under another | Fails unless `--accept <old>`; consumers of the old name break |
| AFFECTED | Own definition unchanged, but built on a BREAKING or REMOVED metric | Never fails; its consumers are told |
| COSMETIC | Description, label, owner or unit text only | Passes |
| ADDED | New name | Passes; run the linter on it |

A rename upstream is mapped through before downstream metrics are compared, so
`revenue / customers` becoming `revenue / active_customers` is not a change to
the ratio when `active_customers` is `customers` renamed.

## The edits that most often move a number without anyone noticing

1. **A filter change**: adding a status (`partially_refunded`), dropping test accounts, a new region. It looks like housekeeping in review.
2. **`count` to `count_distinct`** (or back). Counts rows vs unique entities; differs whenever an entity has more than one row.
3. **The time dimension**: `ordered_at` to `shipped_at`, or the time zone. Totals stay, periods shift.
4. **The source table**: a new model with a different grain or deduplication.
5. **A join path**: a dimension added through a one-to-many join fans out the rows (the measure is repeated per joined row).
6. **Window or grain-to-date** on cumulative metrics.
7. **An input of a ratio or derived metric**: the downstream metric did not change, its number did (AFFECTED).

## Versioning rule

Apply Semantic Versioning's intent to the number, not the YAML: any change in
what the metric returns for a past period is a major change, a new optional
property or a description is not. dbt has no metric version field, so keep it
in `config.meta.version` and bump it in the same PR as the change. When the
history matters (targets, board reporting), keep the old definition alive as
`<name>_v<old>` for a stated period, which is the same pattern dbt model
versions use for models.

## Wiring it into CI

```bash
# in the PR job, after checking out the base branch's artifact
dbt parse --target-path target_head
git worktree add ../base origin/main && (cd ../base && dbt parse --target-path "$OLDPWD/target_base")
python scripts/metric_contract_lint.py --input target_head/semantic_manifest.json --require-version
python scripts/metric_diff.py --base target_base/semantic_manifest.json \
  --head target_head/semantic_manifest.json --manifest target_head/manifest.json
```

Exit 2 blocks the merge. The fix is never to skip the gate: bump the version,
or have the owner pass `--accept`, and send the notice in
`assets/metric_change_notice.md` to every `tell:` line. dbt Cloud's
state-based CI (`state:modified`) tells you which nodes changed; it does not
tell you that a filter edit moved revenue, which is the gap this closes.

## What the diff cannot see

- Two filters that mean the same thing but are written differently (`a = 1 and b = 2` vs `b = 2 and a = 1`, other quoting) are compared as text after whitespace is collapsed, so they show as BREAKING. This errs toward a false alarm, never a missed change; the owner confirms and bumps or reverts the rewording.

- A change in the upstream model's SQL (a new dedup step) that keeps the metric YAML identical. Pair the diff with model contracts and data tests on the model, and reconcile old vs new output with `metric_reconcile.py`.
- Consumers outside dbt exposures. List them in the contract (`consumers`) or declare exposures; an undeclared dashboard will not be warned.

## Sources

1. Semantic Versioning 2.0.0. https://semver.org/
2. dbt Labs, "Model versions" (`versions` property, keeping a prior version alive). https://docs.getdbt.com/reference/resource-properties/versions
3. dbt Labs, "contract" model config. https://docs.getdbt.com/reference/resource-configs/contract
4. dbt Labs, "Add Exposures to your DAG". https://docs.getdbt.com/docs/build/exposures
5. dbt Labs, "Semantic manifest" artifact. https://docs.getdbt.com/reference/artifacts/sl-manifest
6. Bitol, "Open Data Contract Standard" (contract versioning and change management for datasets). https://bitol-io.github.io/open-data-contract-standard/latest/home
