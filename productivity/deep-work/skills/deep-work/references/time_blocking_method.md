# The Time-Blocking Method — Plan Every Minute, Revise Without Guilt

> Reference for `time_block_planner.py`. The mechanics of turning a task list into a
> time-blocked day: why every minute gets a job, how big blocks should be, why buffers and
> revision are part of the method (not failures of it), and why the day needs a hard stop.

## 1. Plan every minute

Newport's core scheduling rule: **give every minute of the workday a job.** At the start of the
day (or the evening before), divide the hours into blocks and assign each block to an activity —
including lunch, buffers, and an explicit "flex" block. The point is not rigidity; it is that an
unassigned minute defaults to the path of least resistance, which is almost always shallow:
inboxes, feeds, "quick checks."

Newport's own estimate from years of running this system: a time-blocked hour is worth roughly
**1.5-2x** an unstructured hour of the same nominal work, because decisions about *what to do
next* are made once, in batch, instead of continuously under depletion.

The planner enforces this literally: its output timeline is gap-free from `--start` to `--end`.
Anything not claimed by a deep block, shallow batch, buffer, or lunch becomes a named **flex
block** — scheduled slack, not accidental drift.

## 2. Block sizes

- **Deep blocks: 90 minutes minimum.** Entry into real concentration is slow (see the canon
  reference on flow and attention residue); a 30-minute "deep" block spends most of itself
  ramping. The planner widens any deep task below 90 minutes up to the floor and says so.
- **Shallow batches: consolidated, not sprinkled.** Shallow tasks are individually small; their
  cost is the switch, not the task. Batching them into one late-morning and one end-of-day window
  converts a dozen context switches into two.
- **Buffers: 10 minutes between work blocks.** Attention residue needs somewhere to drain.
  Buffers are also where the tiny physical resets live — stand up, water, close the previous
  block's tabs.

## 3. Implementation intentions — why written blocks beat willpower

The psychology underneath time-blocking is Gollwitzer's research on **implementation intentions**
(1999): plans of the form "at time X in situation Y, I will do Z" dramatically outperform bare
goal intentions ("I'll write the spec this week"). Meta-analytic effect sizes are medium-to-large
(d ≈ .65 across ~94 studies in Gollwitzer & Sheeran's later review). A time-block is exactly an
implementation intention: the when and where are pre-decided, so the depleted 2 p.m. self doesn't
renegotiate the plan — it just follows it.

Nir Eyal (*Indistractable*) builds his "timeboxing" chapter on the same foundation and adds the
inversion that matters for auditing: **"you can't call something a distraction unless you know
what it distracted you from."** Without a time-blocked plan there is no such thing as
off-plan behavior — which is why the planner runs *after* the shallow audit has decided what
deserves time at all.

## 4. Rescheduling without guilt

Every practitioner's day breaks by mid-morning. Newport's rule (*The Time-Block Planner*): the
plan's value survives its own destruction. When a block is blown up — an incident, an overrun, a
surprise call — you do not abandon the system; you **redraw the remaining blocks at the next free
moment**. His planner pages literally provide columns for multiple revisions of the same day. The
goal, in his words, is not to win a fight against a changing schedule; it is "to maintain, at all
times, a thoughtful say in what you're doing with your time going forward."

Two disciplines follow:

1. **Revision is normal.** Re-run the planner with the surviving tasks and the current time as
   `--start`. Same rules, shorter day.
2. **Overflow is a decision, not an accident.** If the redrawn day no longer fits, something gets
   deferred by name. The planner's exit-2 overflow refusal forces that choice to be explicit.

## 5. Fixed-schedule productivity — the hard stop

Newport's "fixed-schedule productivity" (first described on his Study Hacks blog, later formalized
in *Deep Work*, Rule #4): **fix the endpoint of the workday first — then work backward from it.**
The hard stop functions as a forcing constraint: it makes shallow-work budgets real, forces
ruthless triage of commitments, and converts "I'll just stay late" from a safety valve into a
visible system failure.

Parkinson's observation (*The Economist*, 1955) — "work expands so as to fill the time available
for its completion" — is the mechanism the hard stop exploits in reverse: bounded time compresses
work back toward its true size. This is why `--end` in the planner is immovable and why shallow
overflow past it is a refusal (exit 2, naming what to defer) rather than a silent extension of the
evening.

## Sources

1. Cal Newport, *The Time-Block Planner: A Daily Method for Deep Work in a Distracted World* (Portfolio, 2020) — plan every minute, revision columns, the 1.5-2x estimate.
2. Cal Newport, *Deep Work*, Rule #4 "Drain the Shallows" (Grand Central, 2016) — schedule every minute; fixed-schedule productivity as a forcing function.
3. Cal Newport, "Fixed-Schedule Productivity: How I Accomplish a Large Amount of Work in a Small Number of Work Hours" (Study Hacks blog, calnewport.com, 2008) — the original formulation of the hard stop.
4. Peter M. Gollwitzer, "Implementation Intentions: Strong Effects of Simple Plans," *American Psychologist* 54(7), 1999; and Gollwitzer & Sheeran, "Implementation Intentions and Goal Achievement: A Meta-analysis," *Advances in Experimental Social Psychology* 38, 2006.
5. Nir Eyal, *Indistractable: How to Control Your Attention and Choose Your Life* (BenBella, 2019) — the timeboxing chapter; "you can't call something a distraction unless you know what it distracted you from."
6. C. Northcote Parkinson, "Parkinson's Law," *The Economist*, November 1955 — work expands to fill the time available.
7. Paul Graham, "Maker's Schedule, Manager's Schedule" (paulgraham.com, 2009) — why deep blocks must be defended as contiguous half-day units.
