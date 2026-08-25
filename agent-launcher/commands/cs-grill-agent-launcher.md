---
description: Matt Pocock docs-anchored grill for an agent-launcher goal — walks the phase's forcing questions ONE at a time, each with a recommended answer and a citation to a reference doc, refusing to advance on a fuzzy input. Use to pressure-test a CMA plan before launching.
argument-hint: "[optional: phase name to grill — interview | grade-iterate | run-without-you]"
---

# /cs:grill-agent-launcher — pressure-test the plan

Grill the current goal's phase using its SKILL.md "Forcing-question library".

**$ARGUMENTS**

## Discipline

- **One question per turn.** Never batch. Wait for the answer before the next.
- **Recommend an answer.** Lead with the strongest default and why.
- **Cite the canon.** Each question names its reference doc (cma-primitives.md,
  interview-to-config.md, loops-and-workflows.md, session-goal-model.md).
- **Refuse to advance on fuzz.** If the answer is vague, restate the question with a
  sharper recommended option.

## Question sources

| Phase | Forcing questions live in |
|---|---|
| interview | `skills/interview/SKILL.md` |
| stage-launch | `skills/stage-launch/SKILL.md` |
| grade-iterate | `skills/grade-iterate/SKILL.md` |
| run-without-you | `skills/run-without-you/SKILL.md` |
| wrap-up | `skills/wrap-up/SKILL.md` |
| (whole plan) | `skills/agent-launcher-orchestrator/SKILL.md` |

Start with the orchestrator's five questions unless `$ARGUMENTS` names a phase.
