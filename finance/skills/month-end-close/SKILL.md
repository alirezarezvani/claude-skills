---
name: month-end-close
description: Use when running, planning or speeding up a month-end (or quarter-end) close — building or reviewing the close checklist and calendar, reconciling a bank statement or sub-ledger to the general ledger, writing or reviewing flux (variance) explanations, or finding why the close takes too many days. Orders close tasks by dependency and finds the critical path, proves each reconciliation and ages what is left, and refuses to sign off material fluctuations explained with boilerplate.
argument-hint: "[close plan JSON | GL and bank CSVs | trial balance comparison CSV]"
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "Three-gate close (calendar, reconciliation proof, flux explanations) with 3 deterministic stdlib scripts and blocking exit codes; control expectations cited to COSO 2013 and PCAOB AS 2201 / AS 2305 / SAPA 11"
  distinct_from: "financial-analyst (ratios, DCF, budgets, forecasts); saas-metrics-coach (ARR, churn, unit economics); research-finance (R&D program budgets and capitalisation); this skill runs the accounting close itself"
---

# Month-End Close

> **Portability:** 3 stdlib scripts, no network, no ERP connection. Export CSV or JSON; the scripts plan, prove and gate.
> **Not accounting or audit advice.** Thresholds and aging limits are your policy; the scripts make you state them.

A slow close is rarely slow everywhere. One chain of dependent tasks sets the
close date, reconciliations "agree" without a proof, and flux review accepts
"timing" as a reason. Each script attacks one of those.

## Workflow

```bash
# 1 - Calendar: dependency order, critical path, owners, reviewers, load.
python scripts/close_calendar_planner.py --plan close_plan.json
# 2 - Reconciliations: match, prove, age. One run per account.
python scripts/reconciliation_matcher.py --gl gl_cash.csv --source bank.csv \
  --gl-balance 52708.60 --source-balance 47144.72 --as-of 2026-10-31 --preparer Sam --reviewer Lee
# 3 - Flux: every material change needs a quantified, evidenced explanation.
python scripts/flux_analyzer.py --input tb_compare.csv --pct 10 --abs 10000 --reviewer Lee
```

**Step 1** schedules each task as soon as its predecessors finish, then checks
the plan against people: one person booked for 1.5 days on WD1 is a plan that
will slip. Speed up the critical path, nothing else.

**Step 2** matches by reference, then by amount within a date window. What is
left is a reconciling item: in the GL only (timing) or in the source only (book
a journal entry). The proof must close to zero. An unexplained difference that
was already in the opening balances points back to last month's reconciliation;
one that divides by 9 is flagged as a likely transposition.

**Step 3** marks an account material when it passes your threshold rule, flips
sign, or appears or disappears. Its explanation fails if it is missing, stock
("timing", "in line with expectations"), or has no number in it.

## The gates block on (exit 4)

1. A task with no owner, or a key control with no reviewer or reviewed by its preparer.
2. A plan whose critical path ends after the target workday.
3. A reconciliation that does not prove, or an item older than the stale limit (default 90 days, policy).
4. Preparer and reviewer being the same person, or a flux reviewer who owns the line.
5. A material fluctuation with a missing, boilerplate or unquantified explanation.

## Hard rules

- **A sign-off is not evidence of review.** Record what was checked and where the support is.
- **Never plug a reconciliation.** An unexplained difference is a finding until someone explains it.
- **Thresholds are policy, not standards.** No auditing standard prescribes "10% and 10,000". State yours.
- **Explanations name the driver and the amount**: what moved, by how much, why, and the document behind it.
- **Do not speed up off-critical-path tasks** to shorten the close; they have slack.

## Scripts

| Script | Role | Exit codes |
|---|---|---|
| `scripts/close_calendar_planner.py` | Topological order, critical path, slack, WD deadlines, calendar dates, owner load, reviewer segregation | 0 · 2 at risk · 3 bad input or cycle · 4 blocked |
| `scripts/reconciliation_matcher.py` | Two-pass matching, proof, aging buckets, journal entries needed, review check | 0 · 2 items · 3 · 4 unreconciled |
| `scripts/flux_analyzer.py` | Materiality by your rule, sign flips, explanation lint, evidence check, self-review | 0 · 2 evidence · 3 · 4 incomplete |

All support `--sample` and `--output json`.

## References and assets

- [`references/close_calendar_and_benchmarks.md`](references/close_calendar_and_benchmarks.md) — task order, critical path, days-to-close benchmarks and their caveats (6 sources)
- [`references/reconciliation_standards.md`](references/reconciliation_standards.md) — what a reconciliation must contain, aging, segregation, review precision (6 sources)
- [`references/flux_analysis_and_materiality.md`](references/flux_analysis_and_materiality.md) — expectations, thresholds, corroboration, materiality rules of thumb (6 sources)
- [`assets/close_plan.example.json`](assets/close_plan.example.json), [`assets/gl_cash.example.csv`](assets/gl_cash.example.csv), [`assets/bank_statement.example.csv`](assets/bank_statement.example.csv), [`assets/flux_input.example.csv`](assets/flux_input.example.csv) — input formats
- [`assets/reconciliation_signoff.md`](assets/reconciliation_signoff.md) — sign-off sheet with the evidence fields a reviewer fills in
