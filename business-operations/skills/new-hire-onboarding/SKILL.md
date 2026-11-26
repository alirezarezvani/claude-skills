---
name: new-hire-onboarding
description: "Use when someone new is joining a team and the first day, first week or first 90 days need to go right: a 30/60/90-day onboarding plan for a new hire, a preboarding checklist before the start date (laptop, accounts, signed contract, I-9 or right-to-work check, a named buddy), or a check on how a new employee's ramp-up is going against their plan. Works from a small JSON file with stdlib scripts."
argument-hint: "<hire.json> | --plan plan.json | --log ramp.json"
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "Three deterministic stdlib scripts over one JSON file per hire: a preboarding gate that dates every task against the start date in business days and applies the US I-9 and UK right-to-work deadlines, a 30/60/90 plan builder that refuses milestones nobody could check and schedules checkpoints and buddy meetings, and a ramp check that finds missed checkpoints, overdue milestones and a lapsed buddy; cited to USCIS, GOV.UK, Bauer (SHRM Foundation 2010), Bauer et al. 2007, Watkins 2003, Gallup 2021 and Microsoft's buddy pilot"
  distinct_from: "codebase-onboarding (docs that onboard engineers to a repository); knowledge-ops (writes the onboarding SOP itself); chro-advisor (people strategy, hiring plans, comp); access-lifecycle (joiner/mover/leaver access reviews for auditors); capacity-planner (how many people to hire)"
---

# New-Hire Onboarding

> **Portability:** 3 stdlib Python scripts over one JSON file per hire. No HRIS API, no credentials, nothing sent anywhere.

Most onboarding fails in three places: the laptop or the account is not there
on day one, the plan says "get familiar with the codebase" so nobody can tell
whether week six is going well, and the day-30 check-in quietly never happens.
Gallup found only 12% of US employees say their company onboards well. This
skill turns each of those into a check a manager can run in a minute.

## Workflow

```bash
# 1 - Before the start date: can this person actually work on day one?
python scripts/preboarding_gate.py --hire hire.json            # --today 2026-11-30 to judge another day
# 2 - The 30/60/90 plan: every milestone checkable, checkpoints in the calendar
python scripts/plan_builder.py --plan plan.json --output md
# 3 - During the ramp: is the onboarding on track?
python scripts/ramp_check.py --log ramp.json
```

**Step 1** dates each preboarding task `lead_days` business days before the
start, marks it DONE, OPEN, AT_RISK or LATE, and requires a contract, right to
work, equipment, accounts, payroll, a day-one agenda, a named manager and a
named buddy. US: I-9 Section 1 by day one and Section 2 within 3 business days
(the script prints the date). UK: the right-to-work check before the first day.
Any other country: the task must exist and the local rule comes from HR.
Weekends are skipped; public holidays are skipped only when the hire file lists
them under `"holidays"`, so add the local bank holidays before trusting a LATE.

**Step 2** refuses a plan when a phase has no milestone, a milestone has no
`done_when`, or the buddy is missing or is the manager. It puts day 1, the end
of week 1 and the day-30/60/90 checkpoints in the calendar and counts weekly
manager 1:1s and buddy meetings. `--profile` (standard, engineering, sales,
support, executive) sets the horizon (executive: 120 days) and the example
milestones it suggests for an empty phase.

**Step 3** reads the plan's milestones with `done_on` dates and the meetings
held, and reports CHECKPOINT_MISSED, MILESTONE_OVERDUE, BUDDY_LAPSED,
MANAGER_GAP and NO_CHECKPOINT_BEFORE_OVERDUE, with ON_TRACK, AT_RISK or
OFF_TRACK.

## Hard rules

- **Run the script, don't eyeball dates.** Business-day lead times across weekends are where manual checklists slip. Name each LATE and AT_RISK task with its owner and due date.
- **NOT_READY means move the start date or fix the item.** Never advise starting someone who cannot legally work or has no laptop "and sorting it out on day one".
- **A milestone is something someone else can see.** Rewrite "understand the architecture" as "draw the billing services on one page, reviewed by the buddy". Never accept "learn", "get familiar" or "ramp up" as a milestone.
- **Ask the jurisdiction** before stating a right-to-work deadline. The script knows the US and UK rules only; anywhere else, say so and send the user to HR or counsel.
- **The ramp check judges the onboarding, not the person.** Never say a hire is failing probation. Report what slipped and whether anyone reviewed it; the decision is the manager's and HR's, with the hire's account.
- **The buddy is a peer, never the manager**, and meets the hire weekly.
- **State every default** (lead days, at-risk window, checkpoint grace, profile). Lead days are starting points, not legal minimums; only the I-9 and UK right-to-work deadlines are law.
- **Don't quote the "onboarding raises retention 82%" figure.** See `references/buddy_and_checkins.md`: it has no public primary study.

## Forcing-question library

Ask one at a time, with the recommended answer, before building a plan:

1. **What date does this person start, and where are they employed?** Recommended: a weekday at least 10 business days out, and the country of the employment contract. Canon: USCIS I-9 Central; GOV.UK right-to-work guidance.
2. **What should they have done by day 30 that you could see without asking them?** Recommended: one early win, small and visible. Canon: Watkins, *The First 90 Days* (2003).
3. **Who is their buddy, and is that person not their manager?** Recommended: a peer on the same team with time blocked weekly. Canon: Microsoft buddy pilot (Klinghoffer, Young and Haspas, HBR 2019).
4. **Who owns each preboarding task, and how long does it take?** Recommended: one named owner per task; remote equipment 7 business days. Canon: Bauer, *Onboarding New Employees* (SHRM Foundation 2010), "Compliance".
5. **When are the day-30, 60 and 90 checkpoints, and are they in the calendar now?** Recommended: booked on day one. Canon: Bauer et al. (2007), role clarity as the strongest adjustment signal.

## Report

Answer in the reply, not only in a file, and never edit the user's input files.
Lead with the verdict, then the tasks or milestones to act on this week, each
with owner and date, then the defaults used. For a plan, give the markdown plan
the script prints, with any refused milestone rewritten as a suggestion.

## Scripts

| Script | Role | Exit codes |
|---|---|---|
| `scripts/preboarding_gate.py` | Tasks dated against the start, right-to-work deadline, READY / AT_RISK / NOT_READY | 0 ready · 2 at risk · 3 bad input · 4 not ready |
| `scripts/plan_builder.py` | 30/60/90 plan with checkpoints and cadence; refuses uncheckable milestones | 0 ok · 2 warnings · 3 bad input · 4 refused |
| `scripts/ramp_check.py` | Missed checkpoints, overdue milestones, buddy and manager gaps | 0 on track · 2 at risk · 3 bad input · 4 off track |

All support `--help`, `--sample` and `--output json` (`--format` is an alias).

## References and assets

- [`references/preboarding_and_compliance.md`](references/preboarding_and_compliance.md): lead times, I-9, UK right to work, Germany's Nachweisgesetz (6 sources)
- [`references/ramp_and_milestones.md`](references/ramp_and_milestones.md): what newcomer research says to measure, writing checkable milestones (5 sources)
- [`references/buddy_and_checkins.md`](references/buddy_and_checkins.md): buddy cadence, checkpoints, claims not to repeat (6 sources)
- [`assets/hire.example.json`](assets/hire.example.json), [`assets/plan.example.json`](assets/plan.example.json), [`assets/ramp.example.json`](assets/ramp.example.json)
