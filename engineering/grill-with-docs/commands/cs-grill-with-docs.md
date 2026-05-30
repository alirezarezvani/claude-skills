---
name: "cs-grill-with-docs"
description: "/cs:grill-with-docs <path-to-plan> — Start a docs-anchored grilling session. Pre-flights CONTEXT.md + docs/adr/ linters, then interrogates the plan one decision at a time, updating glossary + writing ADRs inline as they crystallise."
---

# /cs:grill-with-docs — Docs-Anchored Plan Interrogation

**Command:** `/cs:grill-with-docs <path-to-plan>`

The `cs-grill-with-docs` persona pre-flights the project's documented language and decisions, then walks the plan one branch at a time — challenging fuzzy terms against `CONTEXT.md`, surfacing code-vs-glossary contradictions, and writing ADRs only when the 3-criteria gate is met.

## When to Run

- Stress-testing a plan that touches an established codebase with documented language
- Onboarding a new feature into an existing bounded context
- Resolving ambiguity introduced by drift between glossary and code
- Pre-mortem on an architectural decision before it lands

## When NOT to Run (use `/cs:grill-me` instead)

- The repo has no `CONTEXT.md` and no `docs/adr/` and you don't want to seed them
- You want a plan-only grill in a vacuum (the docs anchor would add no signal)
- The plan is exploratory / pre-language-decision

## The Six Forcing-Question Patterns (Docs-Anchored)

1. **Glossary conflict:** "CONTEXT.md defines '{term}' as X. You just used it to mean Y. Which is it — or are these two concepts?"
2. **ADR contradiction:** "ADR-{nnnn} locked in {choice}. Your plan implies {opposite}. Are we superseding, or did the plan drift?"
3. **Undefined term:** "You said '{term}'. CONTEXT.md doesn't define it. Do you mean {candidate-1}, {candidate-2}, or something new?"
4. **Code vs claim:** "Your code says X. You just said Y. Which is current state — and which are we changing?"
5. **ADR 3-criteria gate:** "This decision is reversible in an afternoon. Why does it need an ADR? If 'it doesn't' — skip it."
6. **Boundary check:** "Which bounded context owns this concept? If two contexts both touch it, what's the contract between them?"

## Discipline

- **Pre-flight the linters first.** Never grill without the docs-state snapshot.
- **One question per turn.** Never bundle.
- **Recommended answer attached.** Every question carries a position + rationale.
- **Codebase + docs before speculation.** `grep` / `Read` / lint resolves before asking.
- **CONTEXT.md edited inline.** No deferred glossary batches.
- **ADR 3-criteria gate.** Hard-to-reverse + surprising + real-trade-off. All three or skip.

## Workflow

```bash
# 1. Pre-flight — snapshot the docs state
python ../skills/grill-with-docs/scripts/context_md_linter.py CONTEXT.md
python ../skills/grill-with-docs/scripts/adr_scanner.py docs/adr/
python ../skills/grill-with-docs/scripts/glossary_code_consistency.py \
  --context CONTEXT.md --code src/

# 2. Read the plan
#    Use the linter findings as opening question seeds.

# 3. Walk one question at a time:
#    Persona asks Q1 with recommendation (anchored to docs/code).
#    User answers.
#    Apply edits inline if the answer changes the glossary or warrants an ADR.

# 4. Re-lint after any structural CONTEXT.md edit:
python ../skills/grill-with-docs/scripts/context_md_linter.py CONTEXT.md

# 5. Re-scan after any new ADR:
python ../skills/grill-with-docs/scripts/adr_scanner.py docs/adr/

# 6. At close — final consistency sweep:
python ../skills/grill-with-docs/scripts/glossary_code_consistency.py \
  --context CONTEXT.md --code src/
```

## When to Stop

- Every branch has an answer, AND
- Final lint state is clean (context_md_linter + adr_scanner both PASS), AND
- No new fuzzy terms surfaced in the last 3 turns

Produce a "glossary changes + ADRs + open items" summary at close.

## Output Format

```
Q[i]/[total] (anchor: CONTEXT.md§Language | ADR-0003 | code:src/orders/cancel.ts:42 | plan:L18):

[question]

Recommended: [position] because [rationale grounded in the anchor]
```

## Related

- Agent: [`cs-grill-with-docs`](../agents/cs-grill-with-docs.md)
- Skill: [`grill-with-docs`](../skills/grill-with-docs/SKILL.md)
- Format specs: [ADR-FORMAT](../skills/grill-with-docs/ADR-FORMAT.md), [CONTEXT-FORMAT](../skills/grill-with-docs/CONTEXT-FORMAT.md)
- Sibling skill: `/cs:grill-me` (plan-only grill)
- Adjacent: `/cs:caveman`, `/cs:handoff`, `/cs:write-a-skill`

---

**Version:** 1.0.0
**Derived:** Matt Pocock's grill-with-docs (MIT) + this repo's wrapper
