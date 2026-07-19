# deep-work — Time-Block the Day, Budget the Shallow

> Plan a deep work day the Cal Newport way. Attention is the protected resource, not time.

`/deep-work` turns a raw task list into a time-blocked day: every task classified deep vs shallow,
the shallow share audited against a budget, deep blocks of at least 90 minutes placed in the
earliest hours under a hard **4-hour ceiling**, shallow work batched into at most two windows, and
the day closed with a shutdown ritual. A local ledger tracks weekly deep hours and streaks.

## The discipline

| Rule | Enforced by |
|---|---|
| Shallow work gets a budget (default 50%) before anything is scheduled | `shallow_work_auditor.py` — OVER-BUDGET exits 2 |
| Deep blocks: ≥90 minutes, earliest hours, energy-first | `time_block_planner.py` |
| Deep demand past 4 hours is refused, naming what to defer | `time_block_planner.py` — exit 2 |
| Shallow work: at most two batches (late morning + end of day) | `time_block_planner.py` |
| 10-minute buffers drain attention residue between blocks | `time_block_planner.py` |
| The hard stop never silently extends — overflow is refused by name | `time_block_planner.py` — exit 2 |
| Deep hours are measured, not felt | `focus_session_logger.py` — status / streak |
| The day ends with a shutdown ritual, not a fade-out | `assets/shutdown_checklist.md` |

## Quick start

```bash
# 1. Audit the task list — deep vs shallow, share vs budget
python skills/deep-work/scripts/shallow_work_auditor.py --sample

# 2. Build the time-blocked day (refuses >4h deep, refuses overflow)
python skills/deep-work/scripts/time_block_planner.py --sample

# 3. Log real focus sessions; check the weekly target and streak
python skills/deep-work/scripts/focus_session_logger.py log --minutes 90 --label "Write spec"
python skills/deep-work/scripts/focus_session_logger.py status --target 15
```

Or just say **"plan my deep work day: …"**, run `/cs:deep-work` (full workflow), or
`/cs:time-block` (quick plan from a task list).

## What's in the box

- **Skill:** [`skills/deep-work/SKILL.md`](skills/deep-work/SKILL.md)
- **Agent:** [`agents/cs-deep-work.md`](agents/cs-deep-work.md)
- **Commands:** [`commands/cs-deep-work.md`](commands/cs-deep-work.md) — `/cs:deep-work`;
  [`commands/cs-time-block.md`](commands/cs-time-block.md) — `/cs:time-block`
- **3 stdlib scripts:** `shallow_work_auditor.py`, `time_block_planner.py`, `focus_session_logger.py`
- **3 references** (6-7 sources each: Newport, Leroy, Mark, Ericsson, Csikszentmihalyi, Graham,
  Gollwitzer, Eyal, Parkinson, Zeigarnik, Masicampo & Baumeister, Perlow, RescueTime, Atlassian),
  **2 assets** (worked example day + shutdown-ritual checklist)

## Not the same as

- **`productivity/andreessen`** — the 3x5 card picks WHAT matters today. Deep-work plans WHEN and
  HOW, with attention protected. Run the card first, then block the day here.
- **`project-management` capacity planning** — team-level capacity and sprint math. This is one
  person's attention across one day and one week.
- **`productivity/reflect`** — end-of-week reflection prose. The shutdown ritual here is a daily,
  mechanical close.

## License

MIT.
