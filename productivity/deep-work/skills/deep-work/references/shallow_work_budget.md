# The Shallow-Work Budget — The 30-50% Band, Saying No, and the Shutdown Ritual

> Reference for `shallow_work_auditor.py` and the Step-4 shutdown ritual. Why shallow work gets
> an explicit percentage budget, how to enforce it (batching, refusal), and why the day must be
> closed with a ritual rather than simply stopped.

## 1. The 30-50% band

Newport's prescription in *Deep Work* (Rule #4, "Drain the Shallows") is to confront shallow work
quantitatively: decide, ideally with whoever you answer to, **what fraction of your time should go
to shallow work — and hold the line**. His reported experience: for almost anyone in a
non-entry-level knowledge role, the honest answer lands in the **30-50% band**. Below 30% is
usually fantasy (organizations run on some coordination overhead); consistently above 50% means
the role is being consumed by work "easy to replicate" and the deep output that justifies the
seat is quietly starving.

The auditor's `--budget` default of 50 is deliberately the *top* of the band — the most permissive
defensible line. `OVER-BUDGET` (exit 2) at 50% is not a style warning; it means the day as listed
cannot contain the deep work that matters, so something must be cut, batched, or delegated
*before* a schedule is built. Budgeting after scheduling is how shallow work wins.

## 2. The recent-graduate heuristic

Classifying honestly is the hard part — everything feels important to the person doing it. Newport's
forcing question, printed by the auditor for every shallow item:

> **"How long would it take (in months) to train a smart recent college graduate with no
> specialized training in my field to complete this task?"**

Months of training → the task leverages hard-won expertise → probably deep. Days or weeks → the
task is shallow *regardless of how urgent, social, or visible it is*. The question works because
it strips away urgency and identity and asks only about the skill embedded in the work.

## 3. What time audits actually find

Self-estimates of deep time are systematically inflated, which is why the auditor computes the
share from declared minutes instead of asking for a feeling:

- **RescueTime's** analyses of anonymized knowledge-worker data found users averaging only about
  **2 hours 48 minutes of productive device time per day**, checking email or IM roughly every
  6 minutes, and getting long uninterrupted focus stretches rarely — most days contained no block
  of more than an hour without a communication check.
- **Atlassian's** workplace research aggregates put the average worker at **~62 meetings a month**,
  with half of surveyed workers rating many of them unnecessary, and inbox/context-switch overhead
  consuming a large share of nominal working hours.

The pattern across both: unbudgeted shallow work does not stay small; it metastasizes to fill
whatever attention is left unclaimed. Hence: budget first, then schedule.

## 4. Saying no and batching — enforcing the budget

Three enforcement moves, in order of leverage:

1. **Refuse.** The budget gives the refusal a number: "that puts me over my shallow budget this
   week" is a policy, not a mood. Newport pairs this with fixed-schedule productivity — a hard
   stop makes every yes visibly displace something.
2. **Batch.** Shallow work that survives triage is consolidated into at most two windows (the
   planner enforces this), converting many context switches into two. Leslie Perlow's field
   experiments — from "quiet time" studies with software engineers to the **predictable time off**
   program run with Boston Consulting Group teams (*HBR*, "Making Time Off Predictable — and
   Required," 2009) — showed that even elite always-on teams could carve out protected,
   communication-free periods and see collaboration, satisfaction, and work quality *improve*.
   Protection works when it is scheduled and collectively respected, not heroic.
3. **Delegate or automate.** Anything a recent graduate could learn in days is a candidate.

## 5. The shutdown ritual — why closing loops works

Newport's rule: end every workday with a **shutdown ritual** — review every open loop, capture it
into a trusted plan (today's incompletes get a home on tomorrow's list or the calendar), glance at
the next day, and mark completion with a fixed phrase ("shutdown complete"). No work thoughts
after the phrase.

The mechanism is Zeigarnik's classic finding (1927) that **interrupted and unfinished tasks
intrude on memory far more than finished ones** — open loops keep firing. Masicampo and
Baumeister's follow-up (2011) supplies the crucial refinement: unfulfilled goals stop intruding
**not only when completed, but as soon as a specific plan for them is made**. The shutdown ritual
is that plan-making, done in batch at day's end: it purchases a genuinely recovered evening, and
recovery is what refills the capacity the 4-hour ceiling spends. Skipping the ritual leaks
rumination into the evening and taxes tomorrow's first — best — deep block.

The `assets/shutdown_checklist.md` template operationalizes exactly this sequence, and
`focus_session_logger.py status` gives the ritual its review step: hours banked this week vs the
target, and the streak worth protecting.

## Sources

1. Cal Newport, *Deep Work*, Rule #4 "Drain the Shallows" (Grand Central, 2016) — the shallow-work budget, the 30-50% band, the recent-graduate question, and the shutdown ritual ("shutdown complete").
2. Bluma Zeigarnik, "Über das Behalten von erledigten und unerledigten Handlungen" ("On Finished and Unfinished Tasks"), *Psychologische Forschung* 9, 1927 — unfinished tasks intrude on memory.
3. E. J. Masicampo and Roy F. Baumeister, "Consider It Done! Plan Making Can Eliminate the Cognitive Effects of Unfulfilled Goals," *Journal of Personality and Social Psychology* 101(4), 2011 — making a plan quiets the loop without finishing the task.
4. RescueTime research reports on knowledge-worker attention (rescuetime.com/blog) — ~2h48m of daily productive device time; communication checks about every 6 minutes; rarity of hour-plus focus stretches.
5. Leslie A. Perlow and Jessica L. Porter, "Making Time Off Predictable — and Required," *Harvard Business Review*, October 2009 (and Perlow, *Sleeping with Your Smartphone*, HBR Press, 2012) — predictable, protected off-time improves both wellbeing and output.
6. Atlassian, "You Waste a Lot of Time at Work" workplace research (atlassian.com/time-wasting-at-work-infographic) — meeting load (~62/month) and the cost of unnecessary coordination overhead.
