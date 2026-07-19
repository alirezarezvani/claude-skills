---
description: Matt Pocock-style interrogation of a delivery plan against the PM canon (Kanban Guide 2025, Vacanti, DORA 2025, EBM, Klein, GitLab async-first). One forcing question per turn with a recommended answer; refuses to invoke any sub-skill or start a loop until the lane-defining decisions are locked. Use before running /cs:pm or /cs:pm-loop on a fuzzy plan.
argument-hint: "<delivery plan, goal, or status quo to interrogate>"
---

# /cs:grill-pm — grill a delivery plan before running it

Interrogate this plan — do not execute anything yet:

**$ARGUMENTS**

Five rules (preserved from Matt Pocock, MIT): one question per turn · always give a
recommended answer · explore the workspace before asking · walk the decision tree
depth-first · track answered questions and their dependencies.

## Decision tree

- **Branch 1 — Outcome**: "What single observable outcome means DONE, and which command
  proves it? Recommended: a named artifact + a command that exits 0 against it. Canon:
  agent-harness verifier's law."
- **Branch 2 — Measurement**: "Are you measuring flow before forecasting? Recommended:
  run `jira_snapshot_bridge.py --to flow` first — WIP, throughput, cycle time, age.
  Canon: Kanban Guide (May 2025) four mandatory measures."
- **Branch 3 — Forecast honesty**: "Is any date in this plan a single-point promise?
  Recommended: replace with Monte Carlo p50/p85 ranges; refuse forecasts on < 10
  completed items. Canon: Vacanti, *When Will It Be Done?*"
- **Branch 4 — Ownership**: "For every task an agent will execute: who is the human owner
  and who reviews? Recommended: name both now; `delivery_loop_gate.py` will refuse the
  plan otherwise. Canon: Linear agents model; Atlassian Rovo audit discipline."
- **Branch 5 — Risk**: "Have you run a pre-mortem on this plan? Recommended: 30 minutes,
  'it's six months later and this failed — why?'; convert top clusters to owned risks.
  Canon: Klein, HBR 2007."
- **Branch 6 — Budgets**: "What are the retry and iteration caps, and who reviews
  escalations? Recommended: 3 attempts/task, 12 iterations/goal, a named human. Canon:
  loop-library terminal states."

Per-turn output format:

```
Q[i]/[total]: [precise question]
Recommended: [answer + canon-cited rationale]

(Confirm, or override?)
```

## Stop conditions

- All branches resolved → invoke `/cs:pm` (question) or `/cs:pm-loop` (goal) with the
  locked decisions inlined.
- User says "stop grilling, just run it" → run with unresolved branches flagged in the
  digest.
- Abandoned → save the partial grill to `pm-grill-{timestamp}.md`.

## Distinct from

- `engineering/grill-me` — generic plan interrogation. This grills against the PM canon.
- `/cs:pm` — routes; this refuses to route until decisions are locked.
