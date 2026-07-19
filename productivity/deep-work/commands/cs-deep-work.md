---
name: "cs-deep-work"
description: "/cs:deep-work — Plan a deep work day the Cal Newport way: audit the task list deep vs shallow against a budget, build an energy-first time-blocked schedule with a hard 4-hour deep ceiling and an immovable hard stop, then log focus sessions and close with the shutdown ritual."
argument-hint: "[today's task list, with rough minutes per task]"
---

# /cs:deep-work — Audit the Shallow, Block the Day, Bank the Hours

**Command:** `/cs:deep-work [today's task list]`

A calendar full of reactions is not a plan. `/cs:deep-work` runs the full attention-first
workflow: classify every task deep vs shallow, audit the shallow share against a budget, build a
time-blocked day where deep work owns the earliest hours, and close the loop with a focus-session
ledger and a shutdown ritual.

## When to Run

- "Plan my deep work day" / "time-block my day" / "protect my focus hours"
- The task list is drowning in email, meetings, and admin and you want the honest split
- You keep "working all day" and shipping nothing hard — depth is unmeasured
- Start of day (plan), mid-day after the plan broke (re-plan), end of day (log + shutdown)

## When NOT to Run

- You need to pick WHAT matters today → run `/cs:andreessen` (3x5 card) first, then come back
- Team-level capacity or sprint math → `project-management` skills, not personal attention
- You just want a quick schedule from a ready task list with no audit → `/cs:time-block`

## What You Get

1. **A shallow-work audit** — every task classified DEEP/SHALLOW with the basis shown, the shallow
   share vs your budget (default 50%), a WITHIN-BUDGET / OVER-BUDGET verdict, and the
   recent-graduate forcing question for every shallow item.
2. **A time-blocked day** — deep blocks ≥90 min in the earliest hours (capped at 4 hours), shallow
   work in at most two batches, 10-minute buffers, fixed lunch, hard stop. Refusals name exactly
   what to cut or defer.
3. **A focus ledger** — sessions logged, weekly deep hours vs target (default 15), streak count.
4. **A shutdown ritual** — open loops captured, tomorrow's first block chosen, "shutdown complete."

## Trigger Phrases (auto-invoke without /cs:)

- "plan my deep work day" / "deep work plan"
- "time-block my day" / "time block my calendar"
- "how much of my day is shallow work"
- "protect my focus time" / "I need focus hours"

## Discipline

- **Audit before schedule** — an OVER-BUDGET day gets cut, batched, or delegated first.
- **The refusals stand** — >4h deep demand and overflow past the hard stop are deferred by name,
  never squeezed in or pushed into the evening.
- **The hard stop does not move** — fixed-schedule productivity.
- **Batch, never sprinkle** — shallow work lives in at most two windows.
- **Revise, don't abandon** — when a block breaks, re-run the planner from the current time.
- **Measured, not felt** — the weekly target is checked against the ledger, not memory.

## Workflow

```bash
# 1. Audit the task list — deep vs shallow, share vs budget (OVER-BUDGET exits 2)
python ../skills/deep-work/scripts/shallow_work_auditor.py \
  --task "Write investor update:60" --task "Email triage:45" \
  --task "Analyze churn cohort:90:deep" --budget 50

# 2. Build the time-blocked day (deep-cap and overflow refusals exit 2, naming deferrals)
python ../skills/deep-work/scripts/time_block_planner.py --start 08:30 --end 17:00 --lunch 12:30 \
  --task "Write investor update:90:deep" --task "Analyze churn cohort:90:deep" \
  --task "Email triage:45:shallow"

# 3. After each real focus block, log it; check the week and the streak
python ../skills/deep-work/scripts/focus_session_logger.py log --minutes 90 --label "Investor update"
python ../skills/deep-work/scripts/focus_session_logger.py status --target 15
python ../skills/deep-work/scripts/focus_session_logger.py streak

# 4. End of day: walk ../skills/deep-work/assets/shutdown_checklist.md to "shutdown complete"
```

## Stop Conditions

- Plan emitted + user accepts the blocks → done; return at day's end for log + shutdown.
- Planner refuses (exit 2) → user picks what to defer from the named candidates, re-run once; if
  it refuses again, the day is overcommitted — cut scope, don't fight the arithmetic.
- User says "stop" → drop it; the ledger keeps whatever was already logged.

## Related

- Agent: [`cs-deep-work`](../agents/cs-deep-work.md)
- Skill: [`deep-work`](../skills/deep-work/SKILL.md)
- Quick variant: [`/cs:time-block`](cs-time-block.md) — schedule only, no audit
- Siblings: `/cs:andreessen` (picks WHAT today; run before this), `/cs:reflect` (weekly reflection)

---

**Version:** 1.0.0
