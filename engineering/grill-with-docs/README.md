# grill-with-docs

Docs-anchored grilling session. Walks the decision tree of a plan one branch at a time, but does so against the project's existing **language** (`CONTEXT.md`) and recorded **decisions** (`docs/adr/`). Sharpens terminology + records architecturally-significant decisions inline as they crystallise.

## Attribution

**Derived from [Matt Pocock's grill-with-docs](https://github.com/mattpocock/skills/tree/main/skills/engineering/grill-with-docs)** (MIT, © 2026 Matt Pocock). Matt's interview discipline + domain-awareness rules preserved verbatim per his MIT license — relentless one-question-at-a-time grilling, codebase-and-docs-first exploration, the three-criterion gate for offering an ADR (hard-to-reverse + surprising-without-context + real-trade-off).

## How this differs from `grill-me`

| Aspect | `grill-me` | `grill-with-docs` |
|---|---|---|
| Grounding | Plan text only | Plan + `CONTEXT.md` + `docs/adr/` + codebase |
| Output | Session notes | Session notes **plus** inline updates to CONTEXT.md and (when warranted) new ADRs |
| Question source | Decision tree extracted from plan | Decision tree **plus** language conflicts, fuzzy terms, code-vs-glossary contradictions |
| When to use | Stress-testing a fresh plan | Onboarding a plan into an established codebase with documented language |

Both ship as separate plugins; pick whichever matches the situation. The `grill-me` skill is plan-only; `grill-with-docs` is plan + project memory.

## What this adds on top of Matt's original

| Addition | Where | Why |
|---|---|---|
| **3 stdlib Python tools** | `skills/grill-with-docs/scripts/` | Lint CONTEXT.md format · Walk docs/adr/ for numbering + body integrity · Cross-reference bold terms in CONTEXT.md against codebase usage (dead glossary + code-only common nouns) |
| **3 in-depth references** (7+ sources each) | `skills/grill-with-docs/references/` | Ubiquitous language canon · ADR practice canon · CONTEXT.md as living artifact |
| **cs-grill-with-docs persona agent** | `agents/cs-grill-with-docs.md` | Docs-aware grill voice; pre-flights the linters before the first question |
| **`/cs:grill-with-docs` slash command** | `commands/cs-grill-with-docs.md` | Activation + workflow handoff |

## Matt's original (preserved)

> "Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer. Ask the questions one at a time, waiting for feedback on each question before continuing. If a question can be answered by exploring the codebase, explore the codebase instead."

> "Only offer to create an ADR when all three are true: hard to reverse, surprising without context, the result of a real trade-off. If any of the three is missing, skip the ADR."

## Quick start

```bash
# 1. Lint existing CONTEXT.md (if present)
python skills/grill-with-docs/scripts/context_md_linter.py CONTEXT.md

# 2. Scan existing ADRs (if present)
python skills/grill-with-docs/scripts/adr_scanner.py docs/adr/

# 3. Cross-reference glossary terms against codebase
python skills/grill-with-docs/scripts/glossary_code_consistency.py \
  --context CONTEXT.md --code src/

# 4. Use /cs:grill-with-docs to start the session
```

## License

MIT (matching Matt's upstream).
