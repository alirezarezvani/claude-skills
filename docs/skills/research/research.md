---
title: "Research — Hybrid Router + Fallback — Agent Skill for Research Workflows"
description: "Default entry point for any research request — a hybrid router that classifies the question deterministically and either delegates to a specialist. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Research — Hybrid Router + Fallback

<div class="page-meta" markdown>
<span class="meta-badge">:material-magnify: Research</span>
<span class="meta-badge">:material-identifier: `research`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/research/research/skills/research/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install research-skills</code>
</div>


**The runtime orchestrator for the research domain.** Architecture C: deterministic classification → specialist delegation OR own plan-decompose-search-synthesize-cite workflow.

## Portability

Requires `WebSearch` + `WebFetch` for the fallback workflow; specialist skills (`pulse`, `grants`, `litreview`, `syllabus`, `patent`, `dossier`) must be present for delegation to work. Node.js with `docx` package required if Q2 = document mode. Works in Claude Code CLI natively. In Claude.ai with web tools + Code Execution, the workflow is supported.

## Distinct From `engineering/autoresearch-agent`

These two skills share the word "research" but serve **completely different use cases**:

- **`research/research/`** (this skill) — research-query router + fallback workflow ("Research X")
- **`engineering/autoresearch-agent/`** — Karpathy's autonomous file-optimization experiment loop ("Make this code faster")

No overlap. They coexist.

## Hybrid Architecture (C)

Every invocation produces one of three outcomes:

1. **Delegation** — Classified as specialist-domain. Routes there. User sees the specialist's output.
2. **Fallback execution** — Classified as general research. Runs own plan → search → synthesize workflow.
3. **Clarification request** — Classification ambiguous. Asks one forcing question to disambiguate, then routes.

The skill **never silently runs its fallback** when a specialist would have done better. **Routing transparency** is what makes the hybrid architecture trustworthy.

## Specialist Registry

| Specialist | Routing signals | Domain |
|---|---|---|
| `pulse` | reddit / hn / x / buzz / sentiment / trending / "what's people saying" / "pulse on" / "take the pulse" / "current conversation" | Multi-source recency research |
| `grants` | NIH / grant / R01 / K-award / RePORTER / NOSI / "grants for" / FDA / "study section" / "principal investigator" | NIH grant-funding intelligence |
| `litreview` | literature review / PICO / SPIDER / systematic review / "review papers on" / meta-analysis | Academic literature orientation |
| `syllabus` | syllabus / course outline / curriculum / "reading list" / "for my class" / "for my students" | Course supplementary reading |
| `patent` | prior art / FTO / freedom to operate / patent / "patent landscape" / invention / novelty search / "ip landscape" | Patent prior-art + landscape |
| `dossier` | "dossier on" / "due diligence" / "background check" / "prep me for" / "competitor research" / "investor diligence" / "interview prep" / "background on" | Decision-grade entity research |

## Agent Integrity Rules

This skill obeys the research-pack convention:

- **Execution discipline (fallback only)**: Sequential searches. 1 q/sec rate limit. Confirm response received before next call.
- **Source discipline**: Cite only sources returned by this session's tool calls. Training knowledge labeled `[Background — not from search]` and excluded from counts.
- **Three-count tracking (fallback only)**: Queries sent / sources received / sources cited.
- **Retry policy**: On failure → wait 3s → retry once → log. After 3 consecutive failures: stop, alert user.
- **Plan-tier detection**: If delegated to Consensus-using specialist, that specialist handles detection. In fallback mode, surface any rate-limit signals.
- **Routing discipline**: Never delegate silently. Always state the decision + accept override.

## Phase 1: Grill-Me Intake (2–4 Questions)

Intake is intentionally minimal — the goal is to route fast, not to interrogate. One question per turn.

### Q1 (always) — Research question

> **What's the research question? State it in 1–2 sentences. Specific is better than broad — "AI for healthcare" gets you a vague survey; "How are health systems integrating LLM-based clinical decision support in 2026?" gets you a useful answer.**
>
> *Why I'm asking:* Specificity dictates classification accuracy and search precision. A vague question routes to fallback; a specific question often matches a specialist cleanly.

**Refuse mush.** If user says "research AI", push back once: "What about AI specifically — adoption, safety, capability, funding, regulation, comparison? Pick an angle."

### Q2 (always) — Output preference

> **What output do you want? Pick one:**
> 1. Quick chat briefing (5-min read, markdown in chat)
> 2. Standalone document (.docx with citations, shareable)
>
> *Why I'm asking:* Document mode triggers deeper search budgets and full audit logs. Chat mode optimizes for fast delivery.

Forcing choice.

### Q3 (asked only if classification ambiguous — ≤1 signal) — Domain disambiguation

> **Quick clarification — pick the closest match:**
> 1. Academic literature (papers, peer-reviewed)
> 2. Industry / trends (what's the buzz, news, sentiment)
> 3. Specific entity (a company, person, organization)
> 4. Technology / patents (prior art, IP landscape)
> 5. Grant funding (NIH, foundations)
> 6. Course material (syllabus or curriculum)
> 7. None of the above — run general research
>
> *Why I'm asking:* I couldn't classify confidently from your question alone. This routes you to the right specialist or confirms general-research fallback.

**Skip if Q1 + Q2 produced clear specialist match (≥2 signals).**

### Q4 (asked only if Q3 was needed AND user picked "none of the above") — General-research scope

> **For general research, what's your time horizon — quick scan (5 searches) or thorough (15 searches)?**
>
> *Why I'm asking:* General research has no specialist budget; you pick it. Quick is good for "what's the lay of the land". Thorough is for "I'll make a decision based on this".

Skip if a specialist took over.

**Stop condition:** After Q4 (or earlier if dependency skips applied), commit and start Phase 2. **Most invocations exit intake after Q1 + Q2.**

## Phase 2: Deterministic Classification

This is **deterministic, not LLM-reasoned** — for speed, debuggability, and consistency.

```python
SIGNALS = {
  pulse:    ["reddit", "hn", "hacker news", "x.com", "twitter", "buzz",
             "sentiment", "trending", "what are people saying",
             "what's happening", "the conversation around",
             "pulse on", "take the pulse", "current conversation"],
  grants:   ["nih", "grant", "grants for", "r01", "r21", "k-award", "reporter",
             "nosi", "funding", "fda", "study section", "principal investigator"],
  litreview:["literature review", "lit review", "litreview", "pico", "spider",
             "systematic review", "review papers on", "research papers on",
             "papers about", "meta-analysis"],
  syllabus: ["syllabus", "course outline", "curriculum", "reading list",
             "for my class", "for my students", "course material"],
  patent:   ["prior art", "fto", "freedom to operate", "patent",
             "patent landscape", "invention", "novelty search",
             "patent search", "ip landscape"],
  dossier:  ["dossier on", "due diligence", "background check",
             "prep me for", "competitor research", "investor diligence",
             "interview prep", "research my competitor", "background on"]
}

# Signals are case-insensitive literal phrases (multi-word substring match).
# Bracketed placeholders (e.g., "research [company]") are intentionally NOT
# signals — they over-trigger on generic "research X" queries that should
# fall back to general research, not auto-route to dossier. Specific phrases
# pair the verb with the noun ("dossier on", "background on") and route reliably.

For each specialist S:
  score[S] = count of SIGNALS[S] phrases matched in question (case-insensitive substring)

if max(score) >= 2:
  route_to = argmax(score)                                  # high confidence
elif max(score) == 1 and only one specialist has score 1:
  route_to = that specialist                                # weak match, single specialist
else:
  route_to = "fallback"                                     # ambiguous or no match — ask Q3
```

**Implementation:** `scripts/classifier.py --question "..."` returns the routing decision + matched signals + per-specialist scores. Use it; don't re-implement.

## Phase 3a: Specialist Delegation (≥2 signals OR single weak match)

When delegating:

1. Pass the user's question **verbatim** plus the output preference (Q2)
2. **Let the specialist run its own grill-me intake** — do NOT pre-answer specialist questions
3. Return specialist output as the user-visible result
4. Tag the result with `[Delegated to: research → {specialist}]` in the chat output so the user knows what skill produced it
5. Tag the audit log via `scripts/routing_transparency_logger.py --action record_delegation`

## Phase 3b: Own Fallback Workflow

If routing produced no specialist match, run the 8-step fallback.

### Step 1: Decompose

Break the research question into 3–5 sub-questions. Use the framework: what / why / how / who / what's next. Show the decomposition to the user before searching. Use `scripts/fallback_decomposer.py --question "..."` for a deterministic starting point.

### Step 2: Source Selection

For each sub-question, choose source(s) deterministically:

- **Recency-sensitive** → WebSearch + WebFetch + (optionally Reddit/HN if signal)
- **Technical specs / docs** → WebSearch + WebFetch
- **Academic** → Consensus MCP if connected; otherwise WebSearch with `scholar.google.com` site filter
- **Data / numbers** → WebSearch for sources; then WebFetch for primary documents
- **Person / company entity-level** → consider routing to `dossier` (offer override)

### Step 3: Search

Sequential per sub-question. 1 q/sec etiquette. Per source: 2–4 queries, broad-to-narrow.

### Step 4: Read + Extract

For each result that looks high-signal: WebFetch and extract the relevant section. Note the source URL.

### Step 5: Synthesize

Per sub-question: 2–4 paragraphs answering it with inline citations. Surface disagreement when sources disagree.

### Step 6: Cross-Cutting Patterns

After per-sub-question synthesis: 1–2 paragraphs of patterns across sub-questions — consensus, controversy, gaps.

### Step 7: Output

Markdown brief by default (Q2 choice). DOCX if user picked document mode.

### Step 8: Audit Log

Three-count summary (sent / received / cited) + per-source list with reliability tier (primary / secondary / tertiary).

## Routing Transparency Protocol (Mandatory)

After classification, the skill **always**:

1. **States the decision** in one sentence: "Routing to `litreview` because you mentioned PICO and meta-analysis (2 signals)."
2. **Offers override**: "If you want general research instead OR a different specialist, say so now. Otherwise proceeding in 5 seconds."
3. **Waits 1 turn** for confirmation (or auto-proceeds after 5s in interactive contexts).
4. **If user overrides** → accept, re-route, log the override via `routing_transparency_logger.py --action record_override`.

**Never delegates silently.** This is the trust-building property that makes the hybrid pattern work.

## Output Format

### Markdown brief (Q2 = quick chat briefing)

```markdown
# [Research Question] — Briefing
*Generated: [DATE] | Routed: [delegated specialist | fallback]*

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
[Numbered list with hyperlinks, reliability tier per source]

## Audit
[Three counts + per-source tier + failures]
```

### DOCX (Q2 = standalone document)

Use the standard research-pack DOCX patterns: Arial 12pt, navy headings, blue table headers, hyperlinked sources, mandatory audit log section. Reference the `docx` skill for setup.

## Audit Log Requirement (Fallback Mode)

```
Queries sent:        N
Sources received:    M
Sources cited:       K
Failures:            F (3-consecutive-failures triggered: yes/no)
Per-source tier:     [URL — primary | secondary | tertiary]
Routing decision:    fallback (no specialist matched)
Sub-questions:       [list]
```

All routing decisions + overrides also logged to `~/.research_sessions/<session>.json` via `routing_transparency_logger.py`.

## Failure Modes

| Failure | Behavior |
|---|---|
| Classification ambiguous (≤1 signal) | Ask Q3 (domain disambiguation). |
| Specialist delegation fails | Note in chat. Offer to retry or fall back to general research. |
| User overrides routing | Accept. Re-route to chosen specialist or fallback. Log the override. |
| Fallback search returns thin results | Surface explicitly. Suggest the question may be too niche or too new. Do not fabricate. |
| 3 consecutive tool failures in fallback | Stop, alert user, share what was collected. |
| Question is non-research (e.g., "write me code") | Decline politely. Suggest the user invoke an appropriate skill. |
| Sub-question can't be answered | Note in synthesis as "limited public signal on this"; don't omit silently. |
| Output format mismatch | Honor Q2 preference; if format unavailable, fall back to markdown with note. |
| Specialist skill missing from environment | Skip it in classification scoring; route to fallback or next-best specialist. |

## Anti-Patterns Rejected

- LLM-reasoned classification (must be deterministic keyword + intent matching)
- Silent delegation (always surface routing decision)
- Refusing to route to a specialist when ≥2 signals match
- Routing to a specialist when classification is genuinely ambiguous (≤1 signal across all)
- Pre-answering the specialist's grill-me intake (let it run its own)
- Running fallback when a specialist would clearly do better
- Fabricating sources in fallback when search is thin
- Skipping audit log in fallback mode
- Treating "dossier on [company]" as fallback when `dossier` is the right specialist (the verb-noun-paired phrase, not the generic "research X" form, is what routes)
- Treating "what are people saying about X" as fallback when `pulse` is the right specialist
- Auto-routing generic "research [topic]" queries to a specialist when the user hasn't paired the verb with a specialist-specific noun (e.g., "research Microsoft" alone is ambiguous — could be dossier or general; ask Q3 instead of guessing)

## Tooling

### Python (stdlib only)

- **`scripts/classifier.py`** — Deterministic SIGNALS matching → routing decision + per-specialist score + matched phrases. `--question "..." --output json`.
- **`scripts/routing_transparency_logger.py`** — JSON-backed audit log at `~/.research_sessions/<session>.json`. Records every routing decision, override, and delegation handoff.
- **`scripts/fallback_decomposer.py`** — Heuristic question → 3–5 sub-questions using what / why / how / who / what's next framework.

### Reference Docs (each cites 7+ authoritative sources)

- **`references/hybrid_router_architecture.md`** — router-vs-run trade-offs + routing transparency principle
- **`references/deterministic_classification_canon.md`** — why keyword > LLM-reasoned for routing
- **`references/fallback_workflow_canon.md`** — plan-decompose-search-synthesize methodology

## Dependencies

- **`WebSearch`** + **`WebFetch`** — Required for fallback workflow
- **Specialist skills** — Required for delegation: `pulse`, `grants`, `litreview`, `syllabus`, `patent`, `dossier`. If a specialist is missing, the router skips it in classification and routes to fallback instead.
- **Node.js `docx` library** — Required if user picks document output (Q2 = standalone)
- **Consensus MCP** — Optional; used in fallback if academic sub-questions surface

## Trigger Phrases

- "research [topic]"
- "look into [topic]"
- "what do we know about [topic]"
- "investigate [topic]"
- "find me information on [topic]"
- "do some research on [topic]"
- "I need to understand [topic]"
- Any research request that doesn't obviously match a more-specific specialist

---

**Version:** 1.0.0
**Source spec:** [`megaprompts/13-research-megaprompt.md`](https://github.com/alirezarezvani/claude-skills/tree/main/megaprompts/13-research-megaprompt.md)
**Build pattern:** Path B (direct conversion)
