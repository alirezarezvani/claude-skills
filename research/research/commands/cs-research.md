---
name: "cs-research"
description: "/cs:research <question> — Default research entry point. Hybrid router: classifies question deterministically and either delegates to specialist (pulse / grants / litreview / dossier / patent / syllabus) OR runs own plan-decompose-search-synthesize fallback. Always surfaces routing decision; accepts override. NEVER silent delegation."
---

# /cs:research — Hybrid Research Router + Fallback

**Command:** `/cs:research <research question>`

The `cs-research` persona is the **default entry point for any research request**. Routes to a specialist or runs fallback. Always transparent about the routing decision.

## Distinct from `engineering/autoresearch-agent`

These share the word "research" but serve **different use cases**:
- **`/cs:research`** (this command) — research-query routing + fallback workflow
- **`engineering/autoresearch-agent`** — autonomous file-optimization experiment loop (Karpathy pattern)

No overlap. Don't confuse them.

## When to Run

- Default for ANY research request — let the router pick the right tool
- You're not sure which specialist applies
- You want fallback if no specialist fits
- You want one consistent entry point for research work

## When NOT to Run

- You already know which specialist applies — invoke it directly (`/cs:litreview`, `/cs:grants`, etc.) and skip the routing step
- You want file-optimization experiments — use `engineering/autoresearch-agent`

## The 6 Routing Targets

| Specialist | Routes when question mentions |
|---|---|
| `pulse` | reddit / hn / x / buzz / sentiment / trending / "pulse on" |
| `grants` | NIH / grant / R01 / K-award / RePORTER / "grants for" |
| `litreview` | literature review / PICO / SPIDER / systematic review |
| `syllabus` | syllabus attached / course outline / reading list |
| `patent` | prior art / FTO / freedom to operate / patent / novelty |
| `dossier` | "dossier on" / due diligence / background check / "prep me for" |

## Minimal Intake (2-4 Questions)

| Q | Asks | When |
|---|---|---|
| Q1 | Research question (1-2 sentences, specific) | Always |
| Q2 | Output: quick chat brief OR standalone .docx | Always |
| Q3 | Domain disambiguation (7-option pick-list) | Only when classification is ambiguous (≤1 signal) |
| Q4 | Time horizon for general research (quick 5 vs thorough 15) | Only when Q3 was needed AND user picked "none of the above" |

Most invocations exit at Q2.

## Routing Transparency (Mandatory)

After classification, the skill **always**:

1. States the decision in one sentence: "Routing to `litreview` because you mentioned PICO and systematic review (2 signals)."
2. Offers override: "If you want general research instead or a different specialist, say so."
3. Waits 1 turn for confirmation (or auto-proceeds after 5s in interactive contexts).
4. If user overrides → accepts, re-routes, logs the override.

**Never delegates silently.** This is the trust-building property that makes the hybrid pattern work.

## What You Get

**If delegated to specialist:** the specialist's full output (markdown briefing OR .docx, depending on specialist). Tagged with `[Delegated to: research → {specialist}]`.

**If fallback:** the skill runs its own 8-step workflow and produces:

```
# [Research Question] — Briefing
*Generated: [DATE] | Routed: fallback*

## TL;DR
[2-3 sentences]

## Findings
### [Sub-question 1]
[2-4 paragraphs with inline citations]
### [Sub-question 2]
...

## Cross-Cutting Patterns
[1-2 paragraphs]

## Sources
[Numbered + hyperlinked + reliability tier per source]

## Audit
[Three counts + per-source tier + failures]
```

DOCX version uses same structure with research-pack styling.

## Discipline

- **Deterministic classification** (NOT LLM-reasoned) — keyword signal matching via `classifier.py`
- **Routing transparency mandatory** — never silent
- **Specialist delegation is pass-through** — don't pre-answer specialist questions
- **Fallback after Q3** when no specialist matches
- **Refuse generic "research [topic]"** to a specialist without paired specialist-noun
- **Three-count tracking** in fallback mode
- **Source discipline** — cite only this-session tool calls

## Workflow

```bash
# Phase 1 intake (Q1 + Q2 minimum)

# Phase 2 classification
python ../skills/research/scripts/classifier.py --question "<Q1>"
# Returns: {route_to: "litreview", confidence: "high (2 signals)", matched: [...]}

# Phase 3a delegation (if specialist matched at ≥2 signals)
python ../skills/research/scripts/routing_transparency_logger.py \
  --action record_delegation --session NAME --target litreview --signals "..."
# Pass question to /cs:litreview verbatim; let it run its own intake

# Phase 3b fallback (if no specialist matched)
python ../skills/research/scripts/fallback_decomposer.py --question "<Q1>"
# Returns 3-5 sub-questions
# Run 8-step fallback workflow: source-select → search → read+extract → synthesize → cross-cut → output → audit
```

## Stop Conditions

- Specialist delegated → specialist's stop condition applies
- Fallback complete → markdown brief or DOCX delivered
- Q3 picked but no clear specialist → ask Q4 (time horizon), then run fallback
- User says "stop" → produce partial result with what's been collected

## Trigger Phrases

- "research [topic]"
- "look into [topic]"
- "what do we know about [topic]"
- "investigate [topic]"
- "find me information on [topic]"
- "do some research on [topic]"
- "I need to understand [topic]"
- Plus: any research request that doesn't obviously match a more-specific specialist

## Anti-Patterns Rejected

- LLM-reasoned classification (must be deterministic keyword matching)
- Silent delegation (always surface routing decision)
- Refusing to route to a specialist when ≥2 signals match
- Routing to a specialist when classification is genuinely ambiguous (≤1 signal)
- Pre-answering the specialist's grill-me intake
- Running fallback when a specialist would clearly do better
- Fabricating sources in fallback when search is thin
- Skipping audit log in fallback mode
- Treating "dossier on [company]" as fallback when `dossier` is the right specialist
- Treating "what are people saying about X" as fallback when `pulse` matches
- Auto-routing generic "research [topic]" without paired specialist-noun (ask Q3 instead)

## Related

- Agent: [`cs-research`](../agents/cs-research.md)
- Skill: [`research`](../skills/research/SKILL.md)
- Source spec: [`megaprompts/13-research-megaprompt.md`](../../../megaprompts/13-research-megaprompt.md)
- Routing targets: `/cs:pulse`, `/cs:litreview`, `/cs:grants`, `/cs:dossier`, `/cs:patent`, `/cs:syllabus`
- Adjacent (NOT a routing target): `/cs:notebooklm` (different mode), `engineering/autoresearch-agent` (different use case)

---

**Version:** 1.0.0
**Source:** Path-B direct conversion of `megaprompts/13-research-megaprompt.md`
