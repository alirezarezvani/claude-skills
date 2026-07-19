---
name: "cs-time-block"
description: "/cs:time-block — Build today's time-block plan from a task list, fast: deep blocks of at least 90 minutes in the earliest hours under a hard 4-hour ceiling, shallow work batched into at most two windows, 10-minute buffers, fixed lunch, immovable hard stop. The quick variant of /cs:deep-work — schedule only, no audit, no ledger."
argument-hint: "[task list with minutes, plus start/end times]"
---

# /cs:time-block — Just Build Today's Blocks

**Command:** `/cs:time-block [task list + start/end]`

The quick variant of `/cs:deep-work`: skip the shallow audit and the ledger, take a ready task
list, and emit the time-blocked day. Same arithmetic, same refusals — deep work first and
earliest, capped at 4 hours; shallow work batched; the hard stop does not move.

## When to Run

- "Time-block my day" with a task list already in hand
- Mid-day re-plan after a block broke — feed the surviving tasks and the current time as `--start`
- You already know what's deep and what's shallow and just need the schedule

## When NOT to Run

- The task list hasn't been triaged — shallow work will eat the plan → run `/cs:deep-work` (it
  audits first)
- You need to pick WHAT matters today → `/cs:andreessen` (3x5 card)
- Team capacity or sprint planning → `project-management` skills

## What You Get

A markdown schedule table from hard start to hard stop with **no unassigned minutes**: deep blocks
(≥90 min, earliest hours), at most two shallow batches (late morning + end of day), 10-minute
buffers, optional fixed 30-minute lunch, and named flex blocks that absorb what the plan didn't
foresee. Or a refusal (exit 2) that names exactly what to cut or defer — which is the plan working,
not failing.

## Trigger Phrases (auto-invoke without /cs:)

- "time-block my day" / "build my time blocks"
- "block out my calendar for today"
- "re-plan the rest of my day"

## Discipline

- **Every task needs minutes and a mode** — `"name:minutes:deep|shallow"`. If the user doesn't
  know a task's mode, that's the tell to run `/cs:deep-work` instead.
- **Deep demand past 4 hours is deferred by name** — never shrunk below 90 minutes or squeezed.
- **Overflow past `--end` is deferred by name** — the day never silently extends.
- **Revision is normal** — a broken day is re-planned from the current time, same rules.

## Workflow

```bash
# Build the day (markdown table; add --json for machine-readable output)
python ../skills/deep-work/scripts/time_block_planner.py --start 08:30 --end 17:00 --lunch 12:30 \
  --task "Write product spec:120:deep" \
  --task "Design onboarding flow:90:deep" \
  --task "Email sweep:30:shallow" \
  --task "Expense report:15:shallow"

# Mid-day re-plan: surviving tasks, current time as --start, same hard stop
python ../skills/deep-work/scripts/time_block_planner.py --start 13:00 --end 17:00 \
  --task "Finish product spec:90:deep" --task "Email sweep:30:shallow"
```

## Stop Conditions

- Schedule emitted and accepted → done.
- Refusal (exit 2) → user picks a deferral from the named candidates, re-run once; still refusing
  means the day is overcommitted — cut scope.
- User says "stop" → drop it.

## Related

- Full workflow: [`/cs:deep-work`](cs-deep-work.md) — audit + plan + ledger + shutdown
- Agent: [`cs-deep-work`](../agents/cs-deep-work.md)
- Skill: [`deep-work`](../skills/deep-work/SKILL.md)

---

**Version:** 1.0.0
