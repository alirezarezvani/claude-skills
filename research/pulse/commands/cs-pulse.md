---
name: "cs-pulse"
description: "/cs:pulse <topic> — Multi-source recency research. Grill-me intake (topic / angle / window / scope), then parallel Reddit + HN + Web (1 q/sec per platform), optional X/Twitter, cross-platform synthesis. Output: ${RESEARCH_DIR}/pulse/<slug>-<date>.md + full briefing in chat."
---

# /cs:pulse — Multi-Source Recency Research

**Command:** `/cs:pulse <topic>`

The `cs-pulse` persona takes the pulse of a topic across Reddit, Hacker News, the open web, and (optionally) X/Twitter — within a configurable recent window — and synthesizes a single coherent briefing.

## When to Run

- "What are people saying about X right now?"
- Competitor research with recency flavor
- Trend discovery / tool comparisons / audience sentiment
- Pre-content-creation reconnaissance

The skill ALSO triggers automatically without `/cs:pulse` when you use trigger phrases:
- "pulse on [topic]"
- "what's happening with [topic]"
- "what are people saying about [topic]"
- "current conversation about [topic]"
- "take the pulse of [topic]"
- "trending: [topic]"
- "find me info on [topic]"

`/cs:pulse` is the explicit form.

## Forcing Intake (2–4 Questions, One at a Time)

| Q | Asks | Why |
|---|---|---|
| Q1 | Topic specificity (1–2 sentences, no vague nouns) | Vague Q1 → vague briefing. Refuses "AI" / "tech" once. |
| Q2 | Angle: trend / sentiment / problems / opportunities / comparison | Dictates which platform's voice weights more in synthesis. Default: trend. |
| Q3 | Time window: 7 / 14 / 30 / 60 / 90 days | Default: 30. 7d = breaking, 90d = sustained shift. |
| Q4 | Platform scope (skip any?) | Asked only when angle suggests some platforms off-target. Default: all. |

## What You Get

```
# [TOPIC] — Pulse (Last [N] Days)
*Generated: [DATE] | Angle: [trend|sentiment|problems|opportunities|comparison]*

## TL;DR
[2-3 sentences]

## Reddit
### Top Posts ... ### What Reddit Is Saying

## Hacker News
### Notable Stories ... ### What HN Is Saying

## Web
### Key Sources ... ### What the Web Is Saying

## X/Twitter (if available)
[Or: "Skipped — [reason]"]

## Cross-Platform Patterns
## Key Takeaways
## Content Angles (if applicable)

---
*Audit:* Queries sent: N. Sources received: M. Sources cited: K.
```

Saved to `${RESEARCH_DIR}/pulse/<topic-slug>-<YYYY-MM-DD>.md` AND pasted in chat.

## Discipline

- **One intake question per turn.** Never bundle.
- **Refuse vague Q1 once.** Push back with examples; deliver with caveat if user won't narrow.
- **Parallel Phases 1–3** — Reddit + HN + Web concurrent. Sequential within platform. 1 q/sec.
- **Source discipline** — cite only session-call results. `[Background]` for training knowledge, excluded from cited count.
- **Three-count tracking** — sent / received / cited in audit log.
- **Retry once after 3s** — then log. 3 consecutive failures across sources → stop.
- **Graceful degradation** — single source failure → continue with rest. Never fail the whole run on one source.

## Workflow

```bash
# A. Pre-flight (post-intake)
python ../skills/pulse/scripts/time_window_calculator.py --window 30d
python ../skills/pulse/scripts/topic_slug_generator.py --topic "<topic>" --date $(date +%Y-%m-%d)
python ../skills/pulse/scripts/citation_tracker.py --action start --session NAME

# B. Phases 1–3 (parallel, 1 q/sec per platform)
#    Reddit: search.json sort=top&t=month + sort=new&t=month + top thread comments
#    HN: Algolia stories + comments with timestamp filter
#    Web: 2–3 targeted queries

# C. Phase 4 (optional, sequential): X/Twitter via Grok / X API / browser automation

# D. Synthesis: cross-platform pattern detection

# E. Output: file + chat + audit summary
python ../skills/pulse/scripts/citation_tracker.py --action close --session NAME
```

## Stop Conditions

- All 4 phases complete (or Phase 4 skipped with note) → synthesize + deliver
- 3 consecutive failures across all sources → stop, report what was collected
- User says "stop" → produce partial briefing with what's been collected so far

## Anti-Patterns Rejected

- Starting any search before Q1 (topic specificity) commits
- Batching intake questions
- Hardcoded URLs that won't survive API changes (note format, explain may evolve)
- Specific person/brand references
- Tight coupling to one X/Twitter interface
- Missing fallback behavior
- "Just use [specific tool]" without explaining what the tool does
- Citing training knowledge as session results
- Fabricating sources to fill out a section

## Related

- Agent: [`cs-pulse`](../agents/cs-pulse.md)
- Skill: [`pulse`](../skills/pulse/SKILL.md)
- Source spec: [`megaprompts/01-pulse-megaprompt.md`](../../../megaprompts/01-pulse-megaprompt.md)
- Sibling research skills (after build): `/cs:litreview`, `/cs:grants`, `/cs:syllabus`, `/cs:patent`, `/cs:dossier`, `/cs:research` (router)

---

**Version:** 1.0.0
**Source:** Path-B direct conversion of `megaprompts/01-pulse-megaprompt.md`
