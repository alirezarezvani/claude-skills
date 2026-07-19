# Worked Example — A Full Deep-Work Day (Audit → Plan → Mid-Day Revision → Shutdown)

> A complete pass through the `deep-work` skill for one realistic day, showing the exact script
> invocations and their outputs, including the mid-day revision that every real day eventually needs.

## The raw task list (as the user gave it)

- Write the Q3 product spec — ~2h, the week's most important output
- Design the onboarding flow — ~1.5h
- Email sweep — 30 min
- Team status update — 20 min
- Expense report — 15 min

Day: 08:30 hard start, 17:00 hard stop, lunch 12:30.

## Step 1 — Shallow audit

```bash
python scripts/shallow_work_auditor.py \
  --task "Write Q3 product spec:120" \
  --task "Design onboarding flow:90" \
  --task "Email sweep:30" \
  --task "Team status update:20" \
  --task "Expense report:15" \
  --budget 50
```

Result: `Write Q3 product spec` and `Design onboarding flow` classify DEEP (write/design signals);
the other three classify SHALLOW (email/status/expense signals). Shallow share = 65 of 275 min =
**23.6% vs a 50% budget → WITHIN-BUDGET (exit 0)**. The forcing question printed for each shallow
item confirmed none of them deserves a promotion to deep. Proceed.

## Step 2 — The plan

```bash
python scripts/time_block_planner.py --start 08:30 --end 17:00 --lunch 12:30 \
  --task "Write Q3 product spec:120:deep" \
  --task "Design onboarding flow:90:deep" \
  --task "Email sweep:30:shallow" \
  --task "Team status update:20:shallow" \
  --task "Expense report:15:shallow"
```

| Start | End | Block | Mode |
|-------|-----|-------|------|
| 08:30 | 10:30 | DEEP — Write Q3 product spec | DEEP |
| 10:30 | 10:40 | Buffer — stand up, reset | BUFFER |
| 10:40 | 12:10 | DEEP — Design onboarding flow | DEEP |
| 12:10 | 12:20 | Buffer — stand up, reset | BUFFER |
| 12:20 | 12:30 | Flex — reset, no inputs | FLEX |
| 12:30 | 13:00 | Lunch — away from the desk | BREAK |
| 13:00 | 13:50 | SHALLOW batch (late morning) — Email sweep · Team status update | SHALLOW |
| 13:50 | 16:45 | Flex — overflow absorber | FLEX |
| 16:45 | 17:00 | SHALLOW batch (end of day) — Expense report | SHALLOW |

Deep 3h30 / 4h cap · Shallow 1h05 · Flex 3h05 · Buffers 20min

Reading the plan: both deep blocks own the morning — the best hours — before the manager-schedule
world wakes up. Shallow work exists in exactly two windows. The big afternoon flex block is not
waste; it is where meetings, overruns, and surprises land without touching the deep blocks.

## The revision (because the day broke, as days do)

At 10:15 an incident call ate the rest of the spec block. The rule: **revise, don't abandon.**
At 11:00, re-plan the remaining day with what actually survives:

```bash
python scripts/time_block_planner.py --start 11:00 --end 17:00 --lunch 12:30 \
  --task "Finish Q3 product spec:90:deep" \
  --task "Email sweep:30:shallow" \
  --task "Team status update:20:shallow" \
  --task "Expense report:15:shallow"
```

The onboarding-flow design moved to tomorrow's first block — named and deferred, not silently
squeezed into the evening. The redrawn day still has one protected 90-minute deep block, and the
hard stop did not move.

## Step 3 — Log what actually happened

```bash
python scripts/focus_session_logger.py log --minutes 75 --label "Q3 product spec (pre-incident)"
python scripts/focus_session_logger.py log --minutes 90 --label "Q3 product spec (finish)"
python scripts/focus_session_logger.py status --target 15
```

2h45 banked today. The week's ledger, not memory, decides whether the 15-hour target is on track.

## Step 4 — Shutdown

Run `assets/shutdown_checklist.md`: the deferred design block is already on tomorrow's plan, the
incident follow-up is captured as a task, tomorrow's first block is confirmed. **"Shutdown
complete."** No work thoughts after the phrase.
