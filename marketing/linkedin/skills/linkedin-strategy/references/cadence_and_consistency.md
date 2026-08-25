# Cadence and Consistency — the variable that actually compounds

Every LinkedIn strategy that fails, fails the same way: it was designed for a
week the person happened to have free. Week five arrives, the plan needs six
hours, ninety minutes exist, and the plan is abandoned rather than reduced.

`cadence_planner.py` exists to make that failure visible in week zero, when it is
still an arithmetic problem.

---

## What one post actually costs

Time estimates people use are drafting time. Real cost includes revision and the
reply window.

| Activity | Minutes | What is in there |
|---|---|---|
| Text post | 25 | Draft 15, revise and lint 10 |
| Image post | 30 | Above plus asset and alt text |
| Document carousel | 90 | Outline, 8-12 slides, export, cover |
| Native video | 120 | Script, record, edit, captions |
| Article | 180 | It is an essay |
| Newsletter issue | 150 | An essay with a standing promise attached |
| One substantive comment | 6 | Read the post properly, write something worth reading |
| Replying to your own post | 20 | Per published post, in the hours after |
| One outreach message | 5 | Read their work, write the specific line |

The line people leave out is the last-but-one. **Replying to comments on your own
post is part of the post**, not an optional extra: it is where readers actually
meet you, and skipping it wastes the distribution the post earned.

## Why the allocation shifts with stage

| Stage | Engagement share | Reasoning |
|---|---|---|
| **starting** (<~1k followers, or restarting) | 60% | Your posts have almost no distribution. A substantive comment on a post that already has an audience is the only lever that works from zero. |
| **rebuilding** (audience exists, went quiet) | 45% | Reach recovers with consistency, not with one big swing. |
| **established** (posts reach non-connections) | 30% | Distribution works; the constraint is now what you publish. |

The counter-intuitive part: **from a standing start, most of your budget belongs
in other people's comment sections.** People resist this because commenting feels
like helping someone else. It is the cheapest distribution available, and it is
the only one that works before anyone follows you.

## The floor

Under 90 minutes a week, `cadence_planner.py` refuses to plan a posting schedule
and returns a comment-only week instead. This is a deliberate refusal, not a
limitation:

- A cadence abandoned in week five is worse than one never started, because the
  abandonment is visible on the profile — a burst of posts followed by silence
  reads as a failed attempt, which is exactly the impression you were trying to
  avoid.
- Commenting degrades gracefully. A week with no time costs you a week. A missed
  publishing slot costs you the schedule.

## The minimum viable week

Every plan ships with the subset that survives a bad week:

1. One text post, on the same day each week.
2. One substantive comment per weekday.
3. Reply to every comment on your own post within 24 hours.

That is roughly two hours and it is enough to compound. Everything above it is
acceleration, and acceleration is optional in a way consistency is not.

## Same day, same time

The schedule is the product; the topic varies. Two reasons, one soft and one
mechanical:

- **Soft:** a returning reader learns when you appear. That is the beginning of
  an audience rather than a series of impressions.
- **Mechanical:** it makes your own data comparable. If you post at random times,
  time-of-day confounds every comparison you will ever want to make — see
  `linkedin-analytics/references/evidence_thresholds.md`.

## Batching, and its one real risk

Writing four posts in one sitting is more efficient than four separate sittings,
and it protects the cadence against a bad week. The risk is that batched posts
drift toward the abstract, because the specific detail that makes a post good
usually comes from the day you had.

The working compromise: batch the *drafting*, keep a running note of specifics as
they happen, and let each post steal one from the note.

## Streaks are a trap, consistency is not

A skipped week is fine. A skipped month resets you to the starting stage, because
the audience's memory is shorter than anyone's ego expects. The failure mode to
avoid is not the missed week — it is treating the missed week as proof the whole
thing failed, and stopping.

---

## Sources

1. Clear, J. **Atomic Habits** — systems over goals, and designing for the bad
   day rather than the good one.
2. Fogg, B.J. **Tiny Habits** — behaviour = motivation × ability × prompt;
   lowering the ability cost is what the minimum viable week does.
3. Newport, C. **Deep Work** — fixed-schedule productivity, and why the budget
   should be declared before the plan rather than after.
4. Reinertsen, D. **The Principles of Product Development Flow** — queues and
   work-in-progress limits; a content plan is a queue and overloading it stalls it.
5. Orbit Media. **Annual Blogger Survey** — the long-running longitudinal record
   showing that publishing frequency and time-per-post both rose while typical
   returns did not, which is the case for choosing a sustainable floor.
6. Parkinson, C.N. **Parkinson's Law** (*The Economist*, 1955) — work expands to
   fill the time available, which is why a timeboxed post cost is more honest
   than an open-ended one.
7. Kahneman, D. & Tversky, A. **"Intuitive Prediction: Biases and Corrective
   Procedures"** (1979) — the planning fallacy, the specific bias that makes
   every content calendar optimistic.
