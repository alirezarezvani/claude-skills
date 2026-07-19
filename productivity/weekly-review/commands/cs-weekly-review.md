---
name: "cs-weekly-review"
description: "/cs:weekly-review — Run a GTD weekly review: GET CLEAR (collect, inboxes to zero, empty your head), GET CURRENT (next actions, both calendars, waiting-for, projects — all mandatory), GET CREATIVE (someday/maybe, new ideas). Deterministic gate names every missing step; commitment auditor scores portfolio health 0-100."
argument-hint: "[optional: directory or notes to review]"
---

# /cs:weekly-review — GTD Weekly Review Loop → Trusted System

**Command:** `/cs:weekly-review [directory or notes]`

The weekly review is the maintenance loop that makes the rest of a personal system trustworthy.
This command walks David Allen's three phases in order, scans for open loops so nothing depends on
memory, and refuses to call the review COMPLETE while any mandatory GET CURRENT step is
unaccounted for.

## When to Run

- "Run my weekly review" / "let's do the weekly review"
- "I have too many open loops" / "help me close open loops"
- End of the work week, before planning the next one
- "I fell off my GTD habit" — restart with a shorter, zero-guilt pass
- You want an honest completion verdict, not a warm feeling of having tidied up.

## When NOT to Run

- You just want to dump what's in your head into actions → use `/cs:capture` (intake, not review).
- You want to reflect on one conversation or piece of work → use `productivity/reflect`.
- A team iteration retro with velocity and ceremonies → that's `project-management`, not this.
- Mid-week micro-check ("what's next right now?") — the review is a weekly cadence, not a task picker.

## What You Get

1. **An open-loop inventory** — unchecked checkboxes, TODO/FIXME markers, and stale files across
   your workspace (`open_loop_scanner.py`), grouped by kind with per-file locations.
2. **A walked three-phase checklist** — GET CLEAR (3 steps), GET CURRENT (5 mandatory steps),
   GET CREATIVE (2 steps), processed in order, two-minute rule enforced.
3. **A deterministic verdict** — `weekly_review_gate.py` computes completion %, names every
   missing step, and returns COMPLETE (exit 0) or INCOMPLETE (exit 2). Unskipped GET CURRENT gaps
   always force INCOMPLETE.
4. **A commitment-health audit** — STALLED / NO-NEXT-ACTION / SOMEDAY-CANDIDATE flags plus a
   0-100 score with the formula shown → HEALTHY / DRIFTING / OVERCOMMITTED (`commitment_auditor.py`).
5. **One first next action** for the coming week, so the review ends in motion, not admin.

## Trigger Phrases (auto-invoke without /cs:)

- "run my weekly review" / "weekly review time"
- "close my open loops" / "too many open loops"
- "GTD review" / "get current" / "mind sweep and review"
- "restart my review habit"

## Discipline

- **Scan before you ask** — evidence from the scanner first; the user's memory is what GTD says not to trust.
- **All five GET CURRENT steps are mandatory** — skip only with `--skip "N:reason"`, and the gate still names it.
- **Never self-certify** — the gate issues the verdict; relay its exit code, don't soften it.
- **Process, don't do** — anything over two minutes becomes a next action, not a detour.
- **Timebox 60-90 minutes** — past two hours, gate what's done and schedule the rest.

## Workflow

```bash
# 1. Inventory open loops in the workspace (checkboxes, TODO/FIXME, stale files)
python ../skills/weekly-review/scripts/open_loop_scanner.py --dir . --stale-days 14

# 2. Show the numbered ten-step checklist, then walk it with the user phase by phase
python ../skills/weekly-review/scripts/weekly_review_gate.py --list

# 3. Gate what was actually done — names every missing step; exit 2 if incomplete
python ../skills/weekly-review/scripts/weekly_review_gate.py \
  --done "1,2,3,4,5,6,7,8,10" --skip "9:no someday list yet"

# 4. Audit the commitment portfolio (JSON list of {name, days_since_touched, has_next_action})
python ../skills/weekly-review/scripts/commitment_auditor.py --input commitments.json
```

## Stop Conditions

- Gate returns COMPLETE + commitment audit delivered + one next action named → done.
- Timebox exceeded → gate the partial review honestly (INCOMPLETE), schedule the remainder, stop.
- User says "stop" → gate what's done so the partial pass still counts, then drop it.

## Related

- Agent: [`cs-weekly-review`](../agents/cs-weekly-review.md)
- Skill: [`weekly-review`](../skills/weekly-review/SKILL.md)
- Siblings: `/cs:capture` (intake side of the same system), `productivity/reflect` (one-off reflection)

---

**Version:** 1.0.0
