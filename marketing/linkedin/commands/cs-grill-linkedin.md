---
name: "cs-grill-linkedin"
description: "/cs:grill-linkedin — Interrogate a LinkedIn plan one forcing question at a time, each with a recommended answer anchored in the plugin's canon. Refuses to start the work until the objective, the audience, the hours, the proof, and the exclusion list survive the questions."
argument-hint: "[the LinkedIn plan or ambition you want pressure-tested]"
---

# /cs:grill-linkedin — One question at a time, with a recommendation

**Command:** `/cs:grill-linkedin [your plan]`

Most LinkedIn plans fail on inputs, not execution. This walks the five questions that decide
whether any of the tools can run honestly. One question per turn, each with a recommended
answer and the canon it comes from. Never bundle.

## When to run

- The ambition is real but the plan is vague ("I want to build a presence")
- Before committing a quarter to a cadence
- When a previous attempt stalled and nobody has said why

## The questions

**Q1 — What has to be true in 90 days for this to have been worth it?**
*Recommended: one observable outcome another person could verify — an inbound conversation,
an offer, a hire. Not a follower count.*
Canon: [`objective_to_pillars.md`](../skills/linkedin-strategy/references/objective_to_pillars.md). Follower count moves for
reasons unrelated to the objective; optimising the number you can see instead of the outcome
you want is the most common way a LinkedIn strategy fails while appearing to work.

**Q2 — Who is this for, specifically enough that someone is excluded?**
*Recommended: role + company stage + the problem they have this quarter.*
Canon: same document, and `positioning_brief.py` refuses "business leaders" at exit 3. An
audience that excludes nobody cannot guide a single editorial decision.

**Q3 — How many minutes a week will you protect, measured from a bad week?**
*Recommended: the honest number, not the aspirational one. Below 90, the answer is a
comment-only week.*
Canon: [`cadence_and_consistency.md`](../skills/linkedin-strategy/references/cadence_and_consistency.md). A cadence abandoned in
week five is worse than one never started, because the abandonment is visible.

**Q4 — What proof already exists?**
*Recommended: name shipped work, a measurement, a repo, a hire, a talk. If none exists, the
first pillar is process, not results.*
Canon: [`policy_and_account_safety.md`](../skills/linkedin-skills/references/policy_and_account_safety.md) — the fabrication refusal.
A pillar with no proof is a claim you would have to invent evidence for.

**Q5 — What will you not post about?**
*Recommended: two topics, including the trending one you have no edge on.*
Canon: `objective_to_pillars.md`. A positioning that excludes nothing is availability, and
the exclusion list is what settles the "should I comment on this news cycle" question in
advance.

## Discipline

- **One question per turn.** Wait for the answer. Never bundle.
- **Always recommend.** A question with no recommended answer is homework, not a grill.
- **Cite the canon** for each challenge — the reference document, not a feeling.
- **Stop early** when the lane can run honestly. The full set is not a ritual.
- **Push back once on a weak answer, then accept it.** Their presence, their call. Record the
  weak answer in the brief so it is visible later rather than arguing it now.

## Stop conditions

- All five answered well enough that `positioning_brief.py` would exit 0 → hand off to
  [`/cs:linkedin-plan`](cs-linkedin-plan.md).
- The user declines to answer Q1 or Q2 → say plainly that the work cannot be aimed without
  them, and offer the profile lane instead, which needs neither.

## Related

- Agent: [`cs-linkedin-orchestrator`](../agents/cs-linkedin-orchestrator.md)
- Command: [`/cs:linkedin`](cs-linkedin.md)
- Agreement: [`linkedin_operating_agreement.md`](../skills/linkedin-skills/assets/linkedin_operating_agreement.md)
