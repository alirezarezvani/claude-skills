---
name: sprint-plan
description: "Capacity-gated sprint planning — runs capacity math, carry-over check, and a definition-of-ready gate before committing scope. Usage: /sprint-plan <goal> [capacity]"
argument-hint: <goal> [capacity-in-points-or-person-days]
---

# /sprint-plan

Create a sprint plan for `$ARGUMENTS` with explicit capacity math, a carry-over check, and a definition-of-ready gate. The first token(s) of `$ARGUMENTS` are the sprint goal; a trailing number is treated as team capacity (story points or person-days). If no capacity is given, compute it in Phase 1 — never invent it.

## Usage

```bash
/sprint-plan <goal> [capacity]
# e.g. /sprint-plan "Checkout v2 ready for beta" 34
```

## Phase 1 — Capacity Math (do the arithmetic, show it)

1. **Raw capacity** = team size × working days in sprint × focus factor (default 0.7; ask if unknown)
2. **Deductions** — subtract, explicitly and line by line: holidays/PTO, on-call/support rotation, ceremonies (~10%), known interrupts
3. **Velocity cross-check** — compare against the rolling average of the last 3 sprints' *completed* (not committed) points. If computed capacity exceeds trailing velocity by >15%, plan to trailing velocity and say so.

Output a small table: raw → deductions → net capacity → trailing velocity → planning number.

## Phase 2 — Carry-Over Check (before adding anything new)

1. List every item carried over from the last sprint (not Done at sprint close)
2. Re-estimate *remaining* effort — never carry the original estimate
3. Carry-over consumes capacity **first**; new scope only gets what is left
4. If carry-over exceeds ~30% of capacity, flag it as a systemic over-commitment signal and recommend a smaller commitment this sprint, not a bigger push

## Phase 3 — Definition-of-Ready Gate (per story)

A story may enter the committed scope only if **all** of these hold — otherwise it goes to "needs refinement", not the sprint:

- [ ] User story has a clear actor, action, and outcome (INVEST-compliant)
- [ ] Acceptance criteria written and testable
- [ ] Estimated by the team (not by the planner alone)
- [ ] Dependencies identified and either resolved or scheduled
- [ ] Small enough to finish within the sprint (split if not)

Generate INVEST-checked stories from an epic with:

```bash
python3 product-team/agile-product-owner/skills/agile-product-owner/scripts/user_story_generator.py
```

## Phase 4 — Output Structure

- **Sprint goal** — one sentence; everything committed must serve it
- **Capacity table** — from Phase 1
- **Carry-over** — from Phase 2, listed first in committed scope
- **Committed scope** — stories that passed the DoR gate, summing to ≤ planning number
- **Stretch scope** — clearly separated; pulled only if committed scope finishes
- **Risks and dependencies** — with named owners
- **DoR exceptions** — empty if the gate was honored; otherwise justify each

## Repo Assets (verified paths)

- Skill: `product-team/agile-product-owner/skills/agile-product-owner/SKILL.md`
- Sprint planning template: `product-team/agile-product-owner/skills/agile-product-owner/assets/sprint_planning_template.md`
- Sprint planning guide: `product-team/agile-product-owner/skills/agile-product-owner/references/sprint-planning-guide.md`
- Story generator: `product-team/agile-product-owner/skills/agile-product-owner/scripts/user_story_generator.py`

## Related

- `/sprint-health` — mid-sprint health check
- `/user-story` — single-story generation with INVEST checks
