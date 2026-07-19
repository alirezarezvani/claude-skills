---
name: deep-work
description: Use when someone wants to plan a deep work day, time-block their calendar or task list, budget or cut shallow work, protect focus hours, track deep-work sessions and streaks, run an end-of-day shutdown ritual, or says "/deep-work" or "/time-block". Classifies tasks deep vs shallow, builds an energy-first time-blocked schedule that refuses deep demand past the 4-hour ceiling, batches shallow work into at most two windows, and logs focus sessions against a weekly target.
argument-hint: "[today's task list]"
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "Path-B method skill — Cal Newport time-block discipline preserved + deterministic scheduling scripts added"
  distinct_from: "andreessen 3x5 card (picks WHAT to do today; deep-work plans WHEN and HOW with attention protected); project-management capacity planning (team capacity; this is one person's attention)"
---

# Deep Work — Time-Block the Day, Budget the Shallow

> **Portability:** Reasoning-led skill with 3 stdlib Python scripts. No external APIs, no LLM calls in scripts. Works in Claude Code CLI and Claude.ai web. The scripts fix the arithmetic; you keep the judgment.

## What this does

A calendar full of reactions is not a plan. This skill turns a raw task list into a day where
attention is the protected resource: deep tasks get the earliest hours in blocks of at least 90
minutes, shallow work is batched into at most two windows, buffers absorb attention residue, and the
schedule flatly refuses more than 4 hours of deep demand — the trained daily ceiling. A local ledger
of focus sessions keeps the weekly deep-hours target measured, not felt.

## Step 1 — Classify and budget the shallow

Ask for today's task list with rough minutes per task (or take it from `$ARGUMENTS`). The auditor
classifies each task deep vs shallow (keyword heuristics; an explicit `:deep`/`:shallow` suffix always
wins), computes the shallow share against the budget, and prints the forcing question for every
shallow item — *how long would it take to train a smart recent graduate to do this?*

```bash
python scripts/shallow_work_auditor.py \
  --task "Write investor update:60" --task "Email triage:45" \
  --task "Analyze churn cohort:90:deep" --budget 50
```

`OVER-BUDGET` (exit 2) means cut, batch, or delegate before any schedule is built.

## Step 2 — Block the day

Feed the surviving tasks to the planner with the day's hard start and hard end (fixed-schedule
productivity: the end time does not move). Deep first and earliest, 10-minute buffers, shallow in
two batches (late morning + end of day), an optional fixed lunch:

```bash
python scripts/time_block_planner.py --start 08:30 --end 17:00 --lunch 12:30 \
  --task "Write product spec:120:deep" --task "Email sweep:30:shallow"
```

Two refusals, both exit 2: deep demand past the 4-hour cap (the planner names what to defer), and shallow overflow past `--end` (the planner names what to drop — the day never silently extends).

## Step 3 — Log the session, keep the streak

After each real focus block, log it. `status` shows this week's deep hours against the target (default 15); `streak` counts consecutive days with at least one session:

```bash
python scripts/focus_session_logger.py log --minutes 90 --label "Write product spec"
python scripts/focus_session_logger.py status --target 15
```

## Step 4 — Shutdown ritual

End the day with the shutdown checklist (`assets/shutdown_checklist.md`): capture every open loop, glance at tomorrow, say the closing phrase. An incompletely closed day steals tomorrow's first block.

## Scripts

| Script | Role |
|---|---|
| `scripts/shallow_work_auditor.py` | Deep/shallow classification + shallow share vs budget → WITHIN-BUDGET / OVER-BUDGET (exit 2) + the recent-graduate forcing question per shallow item. |
| `scripts/time_block_planner.py` | Energy-first schedule: deep blocks ≥90 min earliest, 4-hour deep cap (refuses, exit 2), ≤2 shallow batches, 10-min buffers, fixed lunch, overflow refusal. |
| `scripts/focus_session_logger.py` | JSON ledger of focus sessions: `log` / `status` (weekly hours vs target) / `streak`; atomic writes. |

## References

- [`references/deep_work_canon.md`](references/deep_work_canon.md) — deep vs shallow, the deep work hypothesis, the 4-hour ceiling, attention residue (6 sources)
- [`references/time_blocking_method.md`](references/time_blocking_method.md) — plan every minute, block sizes, buffers, guilt-free revision, fixed-schedule productivity (6 sources)
- [`references/shallow_work_budget.md`](references/shallow_work_budget.md) — the 30-50% band, saying no, batching, the recent-graduate heuristic, why the shutdown ritual works (6 sources)

## Assets

- [`assets/example_time_block_plan.md`](assets/example_time_block_plan.md) — a full worked day (audit → plan → mid-day revision → shutdown)
- [`assets/shutdown_checklist.md`](assets/shutdown_checklist.md) — end-of-day shutdown ritual template

## Rules

- **Depth first, earliest.** Deep blocks take the best hours; shallow work gets what is left, never the reverse.
- **Respect the refusals.** More than 4 deep hours is fake depth; overflow past the hard stop is a broken budget, not extra output.
- **Batch, never sprinkle.** Shallow work lives in at most two windows; a sprinkled inbox costs a full refocus each time.
- **Revise, don't abandon.** A broken block means redraw the rest of the day, not "the plan failed."
- **Close the day.** No shutdown ritual, no evening — open loops steal tomorrow's first block.

## Distinct From (don't reach for the wrong skill)

- **`productivity/andreessen`** — the 3x5 card picks WHAT matters today. Deep-work plans WHEN and HOW, with attention protected. Run the card first, then block the day here.
- **`project-management` capacity planning** — team-level capacity and sprint math. This is one person's attention across one day and one week.

---

**Version:** 1.0.0
**Build pattern:** Path-B method skill — Newport discipline preserved + deterministic scheduling scripts added.
