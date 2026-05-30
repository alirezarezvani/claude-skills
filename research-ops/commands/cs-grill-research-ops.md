---
description: Matt Pocock-style docs-anchored grilling for a Research Operations plan — clinical study, R&D budget, market size, or product study. Walks the plan against the research canon (ICH E9, IAS 38, Cochran, Kotler, Nielsen) one question at a time, recommends an answer per question, and refuses to invoke any sub-skill until the lane-defining decisions are locked. Use before running /cs:research-ops on a fuzzy plan.
argument-hint: "<plan, study, budget, market question, or fuzzy research problem>"
---

# /cs:grill-research-ops — Research grill against the research-ops canon

Apply Matt Pocock's `grill-with-docs` discipline to this plan / problem:

**$ARGUMENTS**

## Five rules (preserved from Matt Pocock, MIT)

1. **One question per turn.** Never bundle.
2. **Recommend an answer with each question.**
3. **Explore the workspace before asking** — protocols, ledgers, market models, interview guides.
4. **Walk depth-first.**
5. **Track dependencies** — endpoint → power → feasibility; budget → burn → treatment; sizing → survey → segmentation; method → saturation → synthesis.

## The Research-Ops decision tree (depth-first)

### Branch 1 — Which lane?

- CLINICAL / RD_FINANCE / MARKET / PRODUCT

### Branch 2 — The forcing question per lane

**CLINICAL:** "Is your primary endpoint a clinical outcome or a surrogate — and if surrogate, is it validated for this indication?"
Recommended: clinical outcome unless the surrogate is on FDA's validated table.
Canon: FDA Surrogate Endpoint Table; BEST glossary; ICH E9.

**RD_FINANCE:** "Is this spend in the research phase or the development phase, and can you evidence technical feasibility?"
Recommended: research = expense; development = capitalize-candidate only with feasibility evidence, routed to a named finance owner.
Canon: IAS 38; ASC 730.

**MARKET:** "Is your TAM top-down or bottoms-up — and have you computed it both ways to triangulate?"
Recommended: both; reconcile the delta before quoting a number.
Canon: Bessemer / a16z market-sizing; Fermi estimation.

**PRODUCT:** "Is this study generative (discover problems) or evaluative (test a solution)?"
Recommended: name it first; the method follows.
Canon: Rohrer's UX-research methods landscape (NN/g).

### Branch 3 — Confidence & assumptions check

"What's your confidence level, and what are the three assumptions the answer rests on?"
Recommended: state confidence (high/moderate/low) and surface the assumptions before any number.

### Branch 4 — Named owner

"Who is the human owner who signs this output?"
Recommended: a named clinician/biostatistician (clinical), a named finance controller (finance), a named decision-maker (market/product) — not "the team".

### Branch 5 — Now invoke the sub-skill

Only after branches 1-4 are locked, invoke `/cs:research-ops` with the synthesized inquiry.

## Output format per turn

```
Q[i]/[total]: [precise question]
Recommended: [answer + canon-cited rationale]

(Confirm, or override?)
```

## Stop conditions

- All branches resolved → invoke `/cs:research-ops <synthesized>`
- User says "stop grilling, just run it" → invoke with whatever's resolved, flag unresolved branches in digest
- User abandons → no sub-skill, save partial grill to `research-ops-grill-{timestamp}.md`

## Distinct from

- `engineering/grill-me` (Matt Pocock) — generic.
- `engineering/grill-with-docs` (Matt Pocock) — codebase + ADR-anchored for engineering. This is **Research-Ops-domain grilling** against the research canon.
- `/cs:research-ops` — **executes** routing. This **interrogates** first.
