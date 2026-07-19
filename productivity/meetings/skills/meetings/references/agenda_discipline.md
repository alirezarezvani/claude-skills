# Agenda Discipline — questions, timeboxes, decisions first, an owner, a pre-read

The second discipline of the `meetings` skill: a meeting that passed the cost gate still fails if
its agenda is a list of nouns. This file documents the canon behind `agenda_builder.py` — why every
topic must carry a desired outcome, why timeboxes are budgets rather than suggestions, why decision
topics go first, and why the pre-read and the closing actions-recap slot are non-negotiable.

## Agendas as questions (the desired-outcome rule)

Steven Rogelberg's meeting research produced a counterintuitive result: merely *having* an agenda
does not predict meeting effectiveness — attendees rate agenda'd and agenda-less meetings about the
same. What predicts effectiveness is an agenda built from **questions to be answered**, because a
question forces the organizer to know what "done" looks like, makes the right attendee list
self-evident (invite whoever is needed to answer), and gives the meeting a natural end (the
question is answered) (Rogelberg, *The Surprising Science of Meetings*, Oxford University Press,
2019; and his HBR guidance "Why Your Meetings Stink — and What to Do About It," *Harvard Business
Review*, January–February 2019).

`agenda_builder.py` operationalizes this as a hard rule: **no desired outcome, no agenda slot.**
A topic supplied with an empty outcome field is refused by name (exit 2). "Roadmap" is a noun;
"Decide whether the roadmap slips two weeks" is a meeting.

## Timeboxing (Parkinson's law made operational)

"Work expands so as to fill the time available for its completion" (C. Northcote Parkinson,
"Parkinson's Law," *The Economist*, 1955). Discussion is the purest case: an unbounded topic
consumes whatever remains. The counter-discipline is the timebox — a fixed allocation that ends
the topic whether or not the room feels finished — which is the load-bearing mechanism of Scrum's
every ceremony: the sprint, the daily scrum's fifteen minutes, the review, the retro (Jeff
Sutherland, *Scrum: The Art of Doing Twice the Work in Half the Time*, Crown Business, 2014;
Schwaber & Sutherland, *The Scrum Guide*). The builder therefore:

- requires per-topic minutes and refuses an agenda whose timeboxes (plus the closing buffer)
  exceed the meeting length, naming the exact overflow (exit 3) — a budget you can silently
  overdraw is not a budget;
- prints start–end offsets per topic so the running meeting can see the clock, not just the list;
- treats slack as a feature: finish early, end early.

## Decisions first

The builder sorts topics whose outcome starts with **decide / choose / approve** ahead of
discuss/inform topics. Three converging reasons:

1. **Energy and attention decay.** Decision quality degrades as a session wears on; putting the
   decision in the last five minutes buys either a rushed call or a follow-up meeting. HBR's
   practical agenda guidance consistently recommends sequencing the most important items first —
   also because meetings compress from the end when they start late or run over.
2. **Grove's mission-meeting logic.** If the meeting exists to produce a decision (Grove, *High
   Output Management*, 1983), the decision *is* the meeting; everything else is garnish and should
   be treated as such — or moved to the pre-read.
3. **Inform topics are the weakest claim on synchronous time.** If an inform topic gets squeezed
   out by the sort order, that is the system working: it likely belonged in the memo anyway.

## The owner role

Every topic carries a named owner — the person who drives that timebox, states the question, and
is accountable for its outcome landing in the actions recap. The meeting as a whole has an owner
too (checked upstream by the cost gate). This is Rogelberg's "meeting leader as steward of
everyone's time" plus Grove's chairman-accountability rule, made explicit per-slot so
responsibility cannot diffuse across the invite list.

## The pre-read line

Every generated agenda opens with a pre-read instruction: circulate the material ahead; the
meeting starts assuming it was read. This is Amazon's narrative-memo practice inverted for
ordinary meetings — Bezos's argument for the six-page memo (documented in Amazon shareholder
letters and public remarks) is that writing forces complete thoughts and reading in advance means
the meeting spends its synchronous minutes on the decision, not the download. A meeting that
re-presents the pre-read punishes exactly the people who prepared.

## The closing actions-recap slot

The builder reserves a mandatory 5-minute closing slot: read every action aloud — owner and due
date — before anyone leaves. Two safety properties motivate making it structural rather than
aspirational. First, follow-through is the most commonly dropped meeting phase (Rogelberg), and a
slot on the clock cannot be skipped invisibly. Second, in decision meetings, dissent and confusion
surface late; a recap slot is the last cheap moment to catch "wait, that's not what I agreed to" —
which only happens if people feel safe saying it, Amy Edmondson's core argument for psychological
safety in decision-making teams (Amy C. Edmondson, *The Fearless Organization*, Wiley, 2018).

## Sources

1. Steven G. Rogelberg, *The Surprising Science of Meetings*, Oxford University Press, 2019
   (agenda-as-questions; leader as steward; follow-through gap).
2. Steven G. Rogelberg, "Why Your Meetings Stink — and What to Do About It," *Harvard Business
   Review*, January–February 2019 (question-shaped agendas; invite-list implications).
3. C. Northcote Parkinson, "Parkinson's Law," *The Economist*, 1955 (work expands to fill the time
   available — the case for timeboxes).
4. Jeff Sutherland, *Scrum: The Art of Doing Twice the Work in Half the Time*, Crown Business,
   2014 (timeboxing as the core ceremony mechanism; also Schwaber & Sutherland, *The Scrum Guide*).
5. Andrew S. Grove, *High Output Management*, Random House, 1983 (process vs mission meetings;
   the decision is the meeting; chairman accountability).
6. Jeff Bezos, Amazon shareholder letters + public remarks (narrative memo pre-read; synchronous
   time spent on the decision, not the download).
7. Amy C. Edmondson, *The Fearless Organization*, Wiley, 2018 (psychological safety in decision
   meetings — why the recap slot must invite dissent).
