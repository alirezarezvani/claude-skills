# Meeting Cost Canon — what a meeting really costs, and the should-this-exist gate

The first discipline of the `meetings` skill is treating a meeting as a purchase. Nobody would sign
a $600 invoice without asking what it buys, yet a six-person hour at a $90 fully-loaded rate is
exactly that — approved with one calendar click. This file documents the canon behind
`meeting_cost_calculator.py`: why the price must be said out loud, why the refocus overhead is real,
and why "no decision, no meeting" is the correct default.

## The scale of the problem

- **Executives average ~23 hours a week in meetings**, up from under 10 hours in the 1960s, and 71%
  of senior managers surveyed said meetings are unproductive and inefficient (Leslie Perlow,
  Constance Noonan Hadley & Eunice Eun, "Stop the Meeting Madness," *Harvard Business Review*,
  July–August 2017). Perlow et al.'s core finding: dysfunctional meeting cultures self-perpetuate
  because no individual meeting ever gets billed for its cost.
- **Most meetings fail by design, not execution.** Steven Rogelberg's research program (surveying
  thousands of employees and leaders) finds roughly half of meeting time is rated ineffective by
  attendees, and the strongest lever is what happens *before* the meeting: whether it should exist,
  who is invited, and what the agenda demands (Steven G. Rogelberg, *The Surprising Science of
  Meetings*, Oxford University Press, 2019).
- **Deleting meetings works.** Shopify started 2023 by removing all recurring meetings with more
  than two people (~12,000 events) and later shipped an internal **meeting cost calculator** that
  embeds a dollar figure into every calendar invite — a typical 30-minute, 3-person meeting priced
  between $700 and $1,600. The point was behavioral: people decline purchases they would have
  accepted as invites.
- **Industry surveys agree on the waste.** Doodle's "State of Meetings" report estimated poorly
  organized meetings cost businesses in the tens of billions annually across the US and UK alone;
  Atlassian's long-running "you waste a lot of time at work" meeting statistics put the average
  employee at ~31 hours per month in unproductive meetings. Exact figures vary by survey; the
  direction never does.

## The refocus overhead (`--include-refocus`)

The invite says 30 minutes; the attention bill is larger. Gloria Mark's interruption research at
UC Irvine measured an average of about **23 minutes to return to the interrupted task** after a
context switch (Gloria Mark, Daniela Gudith & Ulrich Klocke, "The Cost of Interrupted Work: More
Speed and Stress," *CHI*, 2008). A mid-morning meeting is an interruption for every attendee doing
focused work, which is why the calculator's `--include-refocus` flag adds 23 minutes per attendee
at the same hourly rate. It is an estimate — deliberately conservative (one refocus, not two) — and
it routinely doubles the sticker price of short meetings, which is the point.

## The gate: decision, agenda, owner

The calculator refuses a MEET verdict unless three things exist:

1. **A decision** (`--has-decision`). Andy Grove's taxonomy separates *process* meetings
   (one-on-ones, staff reviews — scheduled, informational) from *mission* meetings, which exist to
   produce a decision (Andrew S. Grove, *High Output Management*, Random House, 1983). An ad-hoc
   meeting with no decision is a status update wearing a meeting's clothes — Grove's rule was that
   a mission meeting that produces no decision is a failure of the chairman, not the attendees.
   Status flows async: Amazon's practice replaces presentation meetings with a silently-read
   six-page narrative memo, and its "two-pizza team" rule caps the audience — both documented across
   Jeff Bezos's shareholder letters and his explanation that "PowerPoint-style presentations
   somehow give permission to gloss over ideas."
2. **An agenda** (`--has-agenda`). Rogelberg's finding is blunt: agendas per se don't correlate
   with meeting quality — *prepared, question-shaped* agendas do (see
   [`agenda_discipline.md`](agenda_discipline.md)). The gate checks existence; the agenda builder
   enforces quality.
3. **An owner** (`--has-owner`). Perlow et al. and Rogelberg converge here: someone must be
   accountable for the meeting achieving its outcome and for follow-through afterwards. A meeting
   nobody owns produces minutes nobody reads.

Missing the decision → **ASYNC** (the cheapest meeting is no meeting). Missing agenda or owner with
a real decision on the table → **NOT-READY**: the meeting may deserve to exist, but not yet.

## Why the verdict is ternary, not a score

A 0–100 "meeting quality score" invites negotiation. Three verdicts with hard edges do not:
ASYNC ends the conversation (write the memo), NOT-READY names exactly what to fix, and MEET prints
the invoice — total cost plus cost-per-minute — so the agenda's timeboxes get budgeted like money.
This mirrors Shopify's design insight: the number changes behavior only when it arrives *before*
the commitment is made.

## Sources

1. Leslie Perlow, Constance Noonan Hadley & Eunice Eun, "Stop the Meeting Madness," *Harvard
   Business Review*, July–August 2017 (23 hrs/week; self-perpetuating meeting cultures).
2. Steven G. Rogelberg, *The Surprising Science of Meetings*, Oxford University Press, 2019
   (meeting-science canon; pre-meeting levers dominate).
3. Shopify meeting-cost calculator + recurring-meeting purge, 2023 (cost surfaced in the invite;
   ~12,000 events deleted; widely covered, incl. Bloomberg/Reuters reporting).
4. Jeff Bezos, Amazon shareholder letters + public remarks (silent six-page narrative memo;
   two-pizza team rule capping meeting size).
5. Doodle, "State of Meetings" report (survey-based estimate of the cost of poorly organized
   meetings across US/UK).
6. Atlassian, "You Waste a Lot of Time at Work" meeting statistics (~31 unproductive meeting
   hours/month per employee).
7. Andrew S. Grove, *High Output Management*, Random House, 1983 (meetings as the medium of
   managerial work; process vs mission meetings; a decision-less mission meeting is a failure).
8. Gloria Mark, Daniela Gudith & Ulrich Klocke, "The Cost of Interrupted Work," *CHI* 2008
   (~23-minute refocus after interruption — the basis of `--include-refocus`).
