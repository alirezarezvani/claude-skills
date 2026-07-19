# Action-Item Discipline — why meetings without owned actions are theater

The third discipline of the `meetings` skill: the meeting's output is not the discussion, the
slides, or even the decision — it is the set of committed next actions that exist afterwards. A
meeting that ends without owned, dated actions consumed its budget and produced a feeling. This
file documents the canon behind `action_item_extractor.py` and its two flags, **ORPHAN** (no
owner) and **NO-DUE** (no date).

## The next-action rule (why vague intentions don't survive)

David Allen's *Getting Things Done* (Penguin, 2001) built its entire system on one observation:
outcomes don't get done, **next actions** do. "Handle the pricing situation" is a project;
"Maria sends the pricing one-pager by Friday" is an action. Allen's test — *what's the very next
physical, visible activity, and who takes it?* — is exactly the shape the extractor demands: a
verb, an owner, a date. Anything in the notes that fails the test ("we should think about X",
"the team agreed X matters") is deliberately not extracted, because promoting sentiment to a
checklist launders vagueness into false progress.

## One owner, not a committee

Every extracted item gets exactly one owner or an **ORPHAN** flag. This is the "Driver" /
"Accountable" insight of the DACI and RACI decision frameworks (documented in the Atlassian Team
Playbook's DACI play): when a task has two owners it has zero, because each can reasonably assume
the other has it. The extractor never auto-assigns an orphan — assignment is a human commitment,
and a name typed by a script is not a commitment. The flag's job is to force the assignment
conversation while the room (or thread) still remembers agreeing to the work.

## A date, or it drifts

George Doran's original SMART memo ("There's a S.M.A.R.T. Way to Write Management's Goals and
Objectives," *Management Review*, 1981) made **time-bound** one of the five criteria for a reason:
an undated commitment cannot be late, so it never becomes urgent, so it loses every scheduling
contest against work that can. The extractor captures "by/due/before <date>" phrasings and flags
the rest **NO-DUE**. The fix costs five seconds at recap time ("Alex — by when?") and is the
highest-leverage edit anyone makes to meeting notes.

## Implementation intentions (the psychology of "who + when")

The owner + date rule is not managerial superstition; it has a mechanism. Peter Gollwitzer's
implementation-intentions research shows that goals formulated as *if-then* plans — specifying
when, where, and how the action happens — are acted on at substantially higher rates than
equally-motivated abstract goals, across dozens of studies (Peter M. Gollwitzer, "Implementation
Intentions: Strong Effects of Simple Plans," *American Psychologist*, 1999; meta-analysis:
Gollwitzer & Sheeran, *Advances in Experimental Social Psychology*, 2006). An action item with an
owner and a date is an implementation intention; one without is a wish. Likewise, Locke and
Latham's goal-setting research — the most replicated result in organizational psychology — shows
specific, difficult goals reliably outperform "do your best" vagueness (Edwin A. Locke & Gary P.
Latham, "Building a Practically Useful Theory of Goal Setting and Task Motivation,"
*American Psychologist*, 2002).

## Follow-through is the dropped phase

Steven Rogelberg's meeting research finds the post-meeting phase is where most meeting value
leaks: actions go unrecorded, unowned, or unrevisited, and recurring meetings quietly re-discuss
last week's conclusions (*The Surprising Science of Meetings*, Oxford University Press, 2019).
His prescriptions map one-to-one onto this skill's mechanics: end with a recap of commitments
(the agenda builder's mandatory closing slot), record owner + deadline for each (the extractor's
output shape), and open the next meeting against the last list (the emitted markdown checklist is
built to be pasted into the next agenda's pre-read).

## Why extraction is deterministic

The extractor uses fixed patterns — checkboxes, `ACTION:`/`TODO:` prefixes, "@name will …",
"Name will … by date" — rather than judgment. Two reasons. First, auditability: anyone can look at
a line of notes and know whether it will extract, so the discipline is teachable ("write it as
`ACTION: @sam … by Friday` and it will never be lost"). Second, honesty: a fuzzy extractor that
infers actions from vibes recreates the original problem — commitments nobody actually made. If
the notes contain no extractable actions, the correct output is the uncomfortable summary line
saying so, not an invented checklist.

## Sources

1. David Allen, *Getting Things Done: The Art of Stress-Free Productivity*, Penguin, 2001
   (next-action discipline; the verb-owner test).
2. Steven G. Rogelberg, *The Surprising Science of Meetings*, Oxford University Press, 2019
   (follow-through as the dropped phase; end-with-recap prescription).
3. Atlassian Team Playbook, "DACI: Decision-making framework" (single Driver/Accountable;
   two owners = zero owners).
4. George T. Doran, "There's a S.M.A.R.T. Way to Write Management's Goals and Objectives,"
   *Management Review*, 1981 (time-bound as a first-class criterion).
5. Peter M. Gollwitzer, "Implementation Intentions: Strong Effects of Simple Plans," *American
   Psychologist*, 1999 (and Gollwitzer & Sheeran 2006 meta-analysis) — who/when/where plans get
   acted on; wishes don't.
6. Edwin A. Locke & Gary P. Latham, "Building a Practically Useful Theory of Goal Setting and
   Task Motivation," *American Psychologist*, 2002 (specific goals beat vague ones).
