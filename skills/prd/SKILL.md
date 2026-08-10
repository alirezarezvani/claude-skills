---
name: prd
description: "Gated PRD generation — interrogates problem, user, and metric before drafting; refuses to draft on unknowns. Usage: /prd <feature-or-problem>"
argument-hint: <feature-or-problem>
---

# /prd

Generate a concise, evidence-gated product requirements document for `$ARGUMENTS`.

## Usage

```bash
/prd <feature-or-problem>
```

`$ARGUMENTS` is the feature, initiative, or problem statement. If empty, ask for it before doing anything else.

## Phase 1 — Forcing Questions (before any drafting)

Walk these one at a time. Do not batch them. Each answer feeds a required PRD section.

1. **Problem** — What user problem does this solve, and how do you know it exists? (Evidence: support tickets, interview quotes, funnel data — "the CEO wants it" is not evidence.)
2. **User** — Who specifically has this problem? (Segment, role, frequency of pain. "Everyone" is a non-answer.)
3. **Metric** — What single number moves if this works, by how much, measured where?
4. **Alternatives** — What do these users do today instead? Why is that not good enough?
5. **Non-goals** — What adjacent asks are explicitly out of scope for v1?

## Drafting Gate (hard refusal)

**Refuse to draft the PRD if the answer to question 1 (problem), 2 (user), or 3 (metric) is unknown, circular, or "we'll figure it out later."** Instead, output the open questions and the cheapest way to answer each (e.g., 5 customer interviews, a funnel query, a fake-door test). A PRD without a problem, a user, and a metric is a feature wish, not a requirements document.

## Phase 2 — Draft (required-sections checklist)

Every PRD must contain all of these sections — emit the checklist at the end and mark each:

- [ ] Problem statement (with the evidence from Q1)
- [ ] Target user and segment (from Q2)
- [ ] Goals and explicit non-goals (from Q5)
- [ ] User stories with acceptance criteria
- [ ] Success metric + threshold + measurement source (from Q3)
- [ ] Alternatives considered / "do nothing" baseline (from Q4)
- [ ] Scope, dependencies, and timeline assumptions
- [ ] Open questions and risks

Keep it to ~2 pages. Use the repo template as the skeleton.

## Phase 3 — Prioritization hook (optional)

If the user has multiple candidate features, offer to RICE-score them before committing the PRD:

```bash
python3 product-team/skills/product-manager-toolkit/scripts/rice_prioritizer.py features.csv --capacity 20
```

## Repo Assets (verified paths)

- Skill: `product-team/skills/product-manager-toolkit/SKILL.md`
- PRD template: `product-team/skills/product-manager-toolkit/assets/prd_template.md`
- PRD patterns reference: `product-team/skills/product-manager-toolkit/references/prd_templates.md`
- RICE tool: `product-team/skills/product-manager-toolkit/scripts/rice_prioritizer.py`

## Related

- `/code-to-prd` — reverse-engineer a PRD from an existing codebase
- `/rice` — standalone RICE prioritization
