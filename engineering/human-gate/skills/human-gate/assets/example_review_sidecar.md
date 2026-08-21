# Review feedback: q3-launch-plan.md
<!-- human-gate:v1 target=q3-launch-plan.md round=2 -->

reviewer: reza

<!--
  A worked example of the sidecar format. Copy it, or export one from the
  review page. Everything below is hand-writable in any editor — that is what
  keeps this loop working over SSH and in CI, where no browser exists.

  Headings are:  ## <SEVERITY|KIND> [block-id]
  Severities:    BLOCKER  MAJOR  MINOR  NIT     (BLOCKER + MAJOR block the gate)
  Other kinds:   EDIT     NOTE   APPROVE
-->

## BLOCKER b4
> We expect a 40% lift in activation within the first quarter.
No source for 40%, and the whole staffing ask is derived from it. Either cite the
experiment it came from or replace it with the range we can actually defend.

## MAJOR b9
The risk register has no entry for the Acme contract expiring in September. That is
the single largest schedule risk in this plan and it is not written down anywhere.

## EDIT b11
- before: The team will endeavour to deliver incremental value on a continuous basis
+ after: The team ships one usable slice per week
Passive and vague. My replacement is the wording I want — use it as written.

## MINOR b6
The comparison table lists competitors but never says what we compare *on*. Add the
axis, even if it is one sentence above the table.

## NIT b14
"recieve" -> "receive".

## NIT b2
Trailing whitespace at the end of the intro paragraph.

## NOTE
Structure is right and the sequencing argument in §3 is the strongest part — lead with
it. Fix the blocker and the Acme risk and I am happy to sign this off next round.

<!--
  Sign-off, when you are ready, is an explicit item:

      ## APPROVE
      Blocker resolved, Acme risk added. Ship it.

  Absence of blockers is NOT approval — the gate distinguishes the two.
  With this file in place:

      python3 human_gate.py collect q3-launch-plan.md --output json
      python3 human_gate.py close   q3-launch-plan.md
-->
