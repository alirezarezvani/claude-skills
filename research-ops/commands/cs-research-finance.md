---
description: R&D program finance. Build a multi-period program budget with the F&A (indirect) split, track burn rate and runway against value-inflection milestones, and route R&D cost items to a capitalize-vs-expense determination. Every budget surfaces its assumptions; capex-vs-opex routes to a named finance owner and never auto-decides. Direct invocation of the research-finance skill.
argument-hint: "<program context: work packages, F&A rate, cash on hand, milestones, cost items>"
---

# /cs:research-finance — Program budget + burn/runway + capex-vs-opex routing

Run the `research-finance` skill on this input:

**$ARGUMENTS**

## Three-tool workflow

1. **`program_budget_planner.py`** — Build a multi-period budget from work-package lines, apply the F&A rate to an MTDC-style eligible base (excludes capital equipment + subaward portions over $25k), roll up direct / F&A / fully-loaded cost per period with an explicit assumptions block. Industry tuning via `--profile`.

2. **`burn_runway_tracker.py`** — Compute average + trailing burn, runway in periods/months, and whether each value-inflection milestone is reachable before cash runs out. Flags accelerating burn and below-threshold runway.

3. **`capex_vs_opex_router.py`** — Score each cost item against IAS 38 development-phase criteria (or flag ASC 730 expense-as-incurred under US GAAP). Route to CAPITALIZE-CANDIDATE / EXPENSE / FINANCE-OWNER-REVIEW with a named owner. Never books an entry.

## Output

- Budget rollup (direct / F&A / fully-loaded) with assumptions
- Runway + milestone verdicts + flags
- Per-item capex/opex routing with named owner
- Top 3 next actions

## Hard rule

**Every number carries its assumptions; accounting-treatment calls route to a named finance owner.** This skill never books an entry or decides treatment.

## First run + optimization

- **Onboard first:** `python3 skills/research-finance/scripts/onboard.py` (R&D area, F&A rate, runway threshold, accounting standard, finance owner) — saved config pre-configures every tool. `--show` lists the questions.
- **Optimize (opt-in):** only if the user asks to optimize/extend runway, hand off to autoresearch via `skills/research-finance/scripts/ar_evaluator.py` (`runway_months`, higher is better).

## Distinct from

- `finance/financial-analysis` — that's corporate DCF / close / valuation. This is R&D-program-level.
- `research/grants` — that **finds funding**. This **manages money already won**.
