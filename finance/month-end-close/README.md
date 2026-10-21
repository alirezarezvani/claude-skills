# month-end-close

> A slow close is rarely slow everywhere. One chain of tasks sets the date,
> reconciliations "agree" without a proof, and "timing" passes as a reason.

Three deterministic scripts plan the close on its critical path, prove each
reconciliation, and refuse flux explanations that do not name a driver.
No ERP connection, no network: export CSV or JSON and run.

**Not accounting or audit advice.** Thresholds and aging limits are your policy.

## Install

```bash
/plugin marketplace add alirezarezvani/claude-skills
/plugin install month-end-close
```

## Use

```bash
/cs-month-end-close close_plan.json gl_cash.csv bank.csv tb_compare.csv   # full pass
/cs-flux-review tb_compare.csv --pct 10 --abs 10000                       # just flux
```

Or run the scripts directly. Each has `--help`, `--sample` and `--output json`:

```bash
cd skills/month-end-close
python scripts/close_calendar_planner.py --sample
python scripts/reconciliation_matcher.py --sample
python scripts/flux_analyzer.py --sample
```

## The three scripts

| Script | Question | Exit codes |
|---|---|---|
| `close_calendar_planner.py` | Which tasks set the close date? Topological order, critical path and slack, WD+n deadlines mapped to dates, owner load per day, **key controls without an independent reviewer** | 0 · 2 at risk · 3 bad input or cycle · **4 blocked** |
| `reconciliation_matcher.py` | Does it prove? Match by reference then amount and date, adjusted-balance proof, transposition hints, aging buckets, journal entries needed, **preparer ≠ reviewer** | 0 · 2 items · 3 · **4 unreconciled** |
| `flux_analyzer.py` | Is every material change explained? Your threshold rule, sign flips, new or closed balances, **explanation lint** (missing / boilerplate / no driver / no evidence) | 0 · 2 evidence · 3 · **4 incomplete** |

## What it cites

COSO 2013 Principles 10 and 12; PCAOB AS 2201, AS 2305 and Staff Audit Practice
Alert 11; a published university reconciliation policy for aging buckets; and
APQC days-to-close benchmarks, labelled by how directly they were verified.
Every claim in `skills/month-end-close/references/` carries a confidence marker.

## Distinct from

- `financial-analyst` — ratios, DCF, budgets, forecasts.
- `saas-metrics-coach` — ARR, churn and unit economics.
- `research-finance` — R&D program budgets and capitalisation.

## License

MIT. See the repository [LICENSE](../../LICENSE).
