---
description: Matt Pocock-style interrogation of a product plan against the product canon (Torres, Cagan Transformed, Reinertsen/WSJF, Amplitude North Star, evals-as-PRD). One forcing question per turn with a recommended answer; refuses to invoke any sub-skill or start a loop until the outcome-defining decisions are locked. Use before running /cs:product or /cs:product-loop on a fuzzy plan.
argument-hint: "<product plan, roadmap, feature idea, or strategy to interrogate>"
---

# /cs:grill-product — grill a product plan before running it

Interrogate this plan — do not execute anything yet:

**$ARGUMENTS**

Five rules (preserved from Matt Pocock, MIT): one question per turn · always give a
recommended answer · explore the workspace before asking · walk the decision tree
depth-first · track answered questions and their dependencies.

## Decision tree

- **Branch 1 — Outcome**: "What single measurable outcome does this serve, with a number?
  Recommended: write it as the OST root before anything else. Canon: Torres,
  *Continuous Discovery Habits*."
- **Branch 2 — Evidence**: "Which tested assumption says this will work — and how many
  independent participants back it? Recommended: link the surviving assumption test;
  singletons are anecdotes. Canon: Bland, *Testing Business Ideas*; Torres."
- **Branch 3 — Structure**: "Does the tree pass the linter? Recommended: run
  `ost_linter.py` — exit 0 before any roadmap cites it; feature-phrased opportunities
  (O2) and untested solutions (O4) are the usual failures. Canon: Torres OST discipline."
- **Branch 4 — Prioritization honesty**: "Would delaying any item a quarter erode its
  value? Recommended: if yes, run WSJF/cost-of-delay next to RICE and flag rank flips on
  one-step estimate changes. Canon: Reinertsen; the WSJF false-precision critique."
- **Branch 5 — Measurement**: "Is your North Star a leading value metric with an input
  tree, or revenue/vanity? Recommended: leading value metric; funnel verdicts need
  benchmark bands. Canon: Amplitude, *The North Star Playbook*; ProductLed benchmarks."
- **Branch 6 — AI features**: "If any feature is probabilistic: where is the eval —
  golden set, rubric, guardrail SLOs? Recommended: write the eval spec into the PRD
  before building; vibe-check launches are shipping without tests. Canon: evals-as-PRD
  (Lenny's/Braintrust)."

Per-turn output format:

```
Q[i]/[total]: [precise question]
Recommended: [answer + canon-cited rationale]

(Confirm, or override?)
```

## Stop conditions

- All branches resolved → invoke `/cs:product` (question) or `/cs:product-loop`
  (recurring discovery) with the locked decisions inlined.
- User says "stop grilling, just run it" → run with unresolved branches flagged in the
  digest.
- Abandoned → save the partial grill to `product-grill-{timestamp}.md`.

## Distinct from

- `engineering/grill-me` — generic plan interrogation. This grills against the product
  canon.
- `/cs:product` — routes; this refuses to route until decisions are locked.
