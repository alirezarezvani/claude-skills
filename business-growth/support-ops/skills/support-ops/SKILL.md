---
name: support-ops
description: "Run a customer support queue on numbers. Use when SLA targets are being missed or disputed (first response, resolution, business hours), to work out how many agents a phone, chat or email queue needs, or to decide which ticket topics to turn into help-center articles, macros or bug fixes, from a helpdesk ticket export."
argument-hint: "<tickets.csv> [--policy sla.json] | --intervals volumes.csv --aht SECONDS"
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "Three deterministic stdlib scripts over a helpdesk ticket export (business-hours SLA attainment and breach risk, Erlang C and workload staffing with shrinkage and occupancy caps, Pareto deflection finder with root-cause routing); methods cited to Erlang 1917, Gans-Koole-Mandelbaum 2003, Little 1961, the KCS v6 Practices Guide and ITIL 4"
  distinct_from: "customer-success-manager (account health, churn, expansion); chief-customer-officer-advisor (retention strategy and CS org); capacity-planner (general team capacity, not queueing); incident-commander (production incidents, not the support queue)"
---

# Support Ops

> **Portability:** 3 stdlib Python scripts over CSV/JSON you export from any helpdesk. No helpdesk API, no credentials.

Support teams usually argue from anecdotes: "we're swamped", "the SLA is
fine", "we need an FAQ". The ticket export settles each one. This skill
measures SLA attainment on the clock the contract actually uses, sizes the
team with queueing math instead of tickets-per-agent rules of thumb, and
separates topics an article can deflect from topics only a product fix will.

## Workflow

```bash
# 1 - Are we keeping the promise? What breaches next?
python scripts/sla_check.py --tickets tickets.csv --policy sla_policy.json
# 2 - How many people, when?
python scripts/staffing_plan.py --mode live --intervals volumes.csv --aht 420 --concurrency 2
python scripts/staffing_plan.py --mode async --arrivals 30 --aht 600 --backlog 120
# 3 - Which contact reasons should stop reaching agents?
python scripts/deflection_finder.py --tickets tickets.csv
```

**Step 1** computes first-response and resolution attainment per priority on
business or calendar hours (holidays included), p50/p90, open tickets already
breached or due within `--risk-hours`, backlog age and reopen rate. Open
tickets past target count as misses.

**Step 2** uses Erlang C for phone and chat (service level, ASA, occupancy cap,
shrinkage, chat concurrency) and workload plus backlog drain for email. With a
`staffed` column it shows the gap per interval.

**Step 3** ranks the Pareto head of contact reasons and routes each one:
DEFLECT when one answer resolves most tickets and few reopen, AUTOMATE when
agents adapt a common answer, FIX_ROOT_CAUSE when tickets reopen or describe a
defect, REVIEW otherwise.

## Hard rules

- **Ask which clock the SLA runs on** (business or calendar, timezone, holidays) before reporting attainment. Never assume.
- **Open breaches count.** Never report attainment on closed tickets only.
- **Staff to the interval, not the day.** A daily average hides the 11:00 peak.
- **Never write an article for a defect.** FIX_ROOT_CAUSE goes to engineering with ticket count and hours.
- **Deflection savings are an upper bound** until contact rate for the topic is measured after launch.
- **State every default** (attainment target, service level, shrinkage, occupancy cap, concurrency, Pareto cut).

## Scripts

| Script | Role | Exit codes |
|---|---|---|
| `scripts/sla_check.py` | Attainment, p50/p90, breached and at-risk open tickets, backlog age, reopens | 0 ok · 2 at risk / below target · 3 bad input · 4 open breaches |
| `scripts/staffing_plan.py` | Agents on line and scheduled per interval, roster gap | 0 ok · 2 roster short · 3 bad input |
| `scripts/deflection_finder.py` | Pareto of contact reasons with DEFLECT / AUTOMATE / FIX_ROOT_CAUSE / REVIEW | 0 none · 2 candidates · 3 bad input |

All support `--help`, `--sample` and `--output json` (`--format` is an alias).

## References and assets

- [`references/sla_design_and_measurement.md`](references/sla_design_and_measurement.md): metrics, clocks, setting targets (5 sources)
- [`references/staffing_and_erlang_c.md`](references/staffing_and_erlang_c.md): the model, its gaps, defaults (5 sources)
- [`references/deflection_and_kcs.md`](references/deflection_and_kcs.md): deflect vs automate vs fix, KCS, honest savings claims (5 sources)
- [`assets/sla_policy.example.json`](assets/sla_policy.example.json), [`assets/tickets.example.csv`](assets/tickets.example.csv), [`assets/intervals.example.csv`](assets/intervals.example.csv)
