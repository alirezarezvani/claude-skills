---
title: "Litreview — Academic Literature Orientation — Agent Skill for Research Workflows"
description: "Academic literature orientation skill that searches papers via Consensus, builds a strategic search plan using PICO (default) or SPIDER /. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Litreview — Academic Literature Orientation

<div class="page-meta" markdown>
<span class="meta-badge">:material-magnify: Research</span>
<span class="meta-badge">:material-identifier: `litreview`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/research/litreview/skills/litreview/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install research-skills</code>
</div>


> **Portability:** Requires a Consensus MCP connection, Node.js with `docx` package for document generation, and (in CLI) `bash_tool`. Works in Claude Code CLI natively. In Claude.ai with Consensus MCP + Code Execution, the workflow is supported.

Produce a **launching pad** — not a finished literature review, but an orientation document that gives a researcher entering an unfamiliar field everything they need to start reading and searching with confidence. Think: what a generous colleague who knows the field would tell you over coffee.

## Agent Integrity Rules (Research-Pack Convention)

Inherited from the research-pack convention; locked verbatim per PR #657's cross-skill consistency audit.

- **Source discipline.** Only cite Consensus-returned papers from THIS session. Training knowledge labeled `[Not from Consensus — model knowledge]` and excluded from cited count. Sparse results stated explicitly, never silently filled.
- **Counting discipline.** Three numbers tracked: searches executed / unique papers received (deduplicated) / papers cited. Every cited paper has a retrievable Consensus URL from this session. Use `scripts/citation_tracker.py` for deterministic counts.
- **Tool constraints.** Consensus per-query cap depends on plan tier. **Detect at first search**, report at checkpoint. Rate limit is **1 query/sec** — sequential execution mandatory.
- **Retry policy.** On failure → wait 3s → retry once → log. After 3 consecutive failures: stop, alert user, share what was collected.
- **Plan-tier detection.** Parse first-search response for "Showing top 10" / "upgrade" → free tier (10/search). 20 returned → Pro (20/search). Calculate theoretical ceiling and surface at checkpoint so user can recalibrate.

See [`references/search_budget_allocation.md`](https://github.com/alirezarezvani/claude-skills/tree/main/research/litreview/skills/litreview/references/search_budget_allocation.md) for the sequential-execution rationale + plan-tier signals.

## Error Handling

| Failure | Behavior |
|---|---|
| Consensus rate-limit hit | Wait 3s, retry once, log outcome |
| Search returns 0 results | Note explicitly; "either niche terminology or genuine gap"; never silently fill |
| Plan-tier cap detected | Log tier; report at checkpoint; surface in audit |
| 3 consecutive failures | Stop searching, alert user, share what's collected, ask how to proceed |
| Sub-area returns thin results (<5 papers) | Flag in audit; suggest manual PubMed/Scholar supplementation |
| User wants to adjust sub-areas | Update table, re-confirm before searching |
| DOCX validation fails | Unpack XML, fix, repack |

## Phase 0: Grill-Me Intake (3 forcing questions, one at a time)

Each question carries explicit "why I'm asking". Stop condition: max 3 before Phase 1.

### Q1 (root) — Research question specificity

> **State the research question in 1–2 sentences. Specific is better — "How do LLMs perform on clinical reasoning tasks compared to physicians?" beats "AI in medicine". Vague questions produce vague reviews.**
>
> *Why I'm asking:* The reconnaissance search hinges on precise terminology. Vague questions produce thin recon results that don't yield a useful framework breakdown.

**Refuse mush.** Re-ask once with examples if user is too broad. If still vague, deliver with explicit "broad-scope orientation, not depth review" caveat.

### Q2 (depends on Q1) — Framework hint

> **Framework — pick one or say "you pick":**
>
> 1. **PICO** (Population / Intervention / Comparison / Outcome — most clinical questions)
> 2. **SPIDER** (Sample / Phenomenon / Design / Evaluation / Research-type — social/qualitative)
> 3. **Decomposition** (Problem / Solution / Evaluation / Limitations — technology-focused)
> 4. **Hybrid** (you pick which components from which framework)
> 5. **You pick** — analyze Q1 and recommend
>
> *Why I'm asking:* PICO is the default for ~70% of clinical questions but maps poorly to qualitative work or technology evaluation. Picking upfront saves the recon search from suggesting a misaligned framework.

Forcing choice with default ("you pick"). The skill surfaces its own framework recommendation after the recon search so user can override. Use `scripts/framework_recommender.py` for the heuristic.

See [`references/framework_selection.md`](https://github.com/alirezarezvani/claude-skills/tree/main/research/litreview/skills/litreview/references/framework_selection.md) for PICO / SPIDER / Decomposition canon.

### Q3 (depends on Q1) — Tentative depth

> **Tentative depth — pick one. Final confirmation comes after the framework breakdown:**
>
> 1. **Quick scan** (5 searches)
> 2. **Standard review** (10 searches)
> 3. **Deep dive** (20 searches)
>
> *Why I'm asking:* I ask this twice — once now to calibrate the recon search emphasis, once after the framework breakdown to confirm. Tentative answer affects which sub-areas to surface first; final answer drives search budget allocation.

Forcing choice. **Re-asked** at the post-Phase-2 checkpoint after the user has seen the framework breakdown.

**Stop condition:** 3 questions max before Phase 1. The post-Phase-2 checkpoint is its own grill-me moment (framework table + sub-area-adjustment + depth-reconfirmation).

## Phase 1: Initial Reconnaissance

**One broad Consensus search** to map themes, terminology, methodological distinctions.

- Query: broad version of Q1 (terminology variants are okay; first search casts wide)
- Record: `citation_tracker.py --action record_search --session NAME --query "..."`
- Record received count: `citation_tracker.py --action record_papers_received --session NAME --count N`
- **Detect plan tier** from response: "Showing top 10" / "upgrade" → free; 20 returned → Pro

Synthesize for the checkpoint:
- Themes that surfaced
- Terminology variations (e.g., "LLM" vs "large language model" vs "GPT-style model")
- Methodological distinctions (clinical trials vs benchmark eval vs case study)
- Coverage gaps (sub-questions absent from recon results)

## Phase 2: Framework Selection + Sub-area Generation

Choose framework (from Q2 OR override based on recon):
- **PICO** — most clinical questions (~70% default)
- **SPIDER** — social / qualitative
- **Decomposition** — technology focus (Problem / Solution / Evaluation / Limitations)
- **Hybrid** — explicit cross-framework mapping

Generate **4-5 sub-area questions** mapped to framework components. Each becomes a targeted Phase 3 search.

## Checkpoint (grill-me forcing-options moment)

After Phase 2, halt and present:

### 3-4 sentence recon summary
- What themes surfaced
- Terminology landscape
- Evidence landscape characterization

### Framework breakdown table

| Framework Component | How It Maps to This Topic | Proposed Sub-area to Explore |
|---|---|---|
| (Component 1) | ... | Sub-area 1 |
| (Component 2) | ... | Sub-area 2 |
| (Component 3) | ... | Sub-area 3 |
| (Component 4) | ... | Sub-area 4 |
| Cross-cutting theme | ... | Sub-area 5 |

### Depth re-confirmation (forcing choice)

Surface the **practical constraint**: detected plan tier + theoretical ceiling.

- Quick scan (5 searches × ~10 results each = ~50 papers max)
- Standard review (10 searches × ~10 = ~100 papers)
- Deep dive (20 searches × ~10 = ~200 papers)

### Sub-area forcing options

- "Looks good — proceed with these sub-areas"
- "Adjust: add sub-area on [X]"
- "Adjust: remove and replace [Y] with [Z]"
- "Restart with different framework"

### Why I'm asking (the rationale)

> A wrong framework or sub-area set wastes the search budget. This is the **last cheap moment** to correct course.

**Wait for user response before Phase 3.** Refuse to start Phase 3 without explicit user choice.

## Phase 3: Targeted Searches

Sequential (1 query/sec), budget per depth tier. See [`references/search_budget_allocation.md`](https://github.com/alirezarezvani/claude-skills/tree/main/research/litreview/skills/litreview/references/search_budget_allocation.md) for full canon.

### Quick scan (5 searches)
- 5 sub-area searches (one per sub-area)
- Skip era-gated + review-specific

### Standard review (10 searches)
- 5 sub-area searches
- 2 review article searches (top 2 sub-areas): `"systematic review [topic]"` / `"meta-analysis [topic]"`
- 2 era-gated searches (most important sub-area): `year_max: 2015` + `year_min: 2021`
- 1 follow-up on highest-cited paper using its key terms + `year_min` after publication

### Deep dive (20 searches)
- 5 sub-area searches
- 5 review article searches (one per sub-area)
- 4 era-gated searches (top 2 sub-areas, old + new each)
- 3 follow-ups on top 3 highest-cited papers
- 3 spare for emerging threads (surprising findings to chase)

Throughout: 1 q/sec rate limit. Sequential. Confirm response before next call. Record each via `citation_tracker.py`.

## Cross-Search Intelligence

Three trackers across ALL search results — run `scripts/cross_search_aggregator.py --session NAME` after Phase 3 completes:

1. **Repeat-hit papers** — same paper appearing in 3+ sub-area searches = likely foundational
2. **Recurring authors** — same author in multiple searches = dominant research group; top 3-5 most frequent matter
3. **Citation-per-year heuristic** — a 2023 paper with 150 citations >> 2008 paper with 150 citations. Use for seminal-work identification.

These feed the "Start Here" + "Key Research Groups" + "Bibliography" DOCX sections.

## Phase 4: DOCX Research Guide

Generate via Node.js + `docx` library. 8 sections (see [`references/docx_8_sections.md`](https://github.com/alirezarezvani/claude-skills/tree/main/research/litreview/skills/litreview/references/docx_8_sections.md) for full spec):

1. **Topic Overview** — single tight paragraph (4-6 sentences)
2. **Start Here — Priority Reading Order** — 5-7 papers ordered: best recent review → foundational → 2-3 frontier → gap/controversy. Each: hyperlinked title + authors/year + 1-sentence contribution + 1-sentence "what to look for"
3. **How the Field Got Here** — chronological narrative (1-2 paragraphs) + timeline table (5-8 milestones: Year / Milestone / Significance) + terminology evolution note
4. **Sub-area Guides** (one per sub-area, 4 parts each)
   - 4a. What the Research Shows (2-3 sentence synthesis with inline citations)
   - 4b. Key Papers (3-5 hyperlinked papers with citation count, year, 1-sentence importance)
   - 4c. Key Search Terms (6-10 keywords, synonyms, MeSH, historical terms)
   - 4d. Boolean Search Strings (2-3 ready-to-paste strings)
5. **Key Research Groups** — top 3-5 authors/groups with affiliations, sub-area coverage, representative paper link (from cross-search aggregator)
6. **Open Questions & Gaps** — three categories: methodological / population-context / conceptual-theoretical. Each gap explains *why it matters*.
7. **Bibliography** — alphabetical by first author. Every entry has clickable "View on Consensus" link. Every inline citation matches a bibliography entry.
8. **Audit Log** — search summary table (#, query, filters, papers returned, status), counts block, coverage notes including detected tier and theoretical ceiling

### DOCX Technical Requirements

Document the key `docx` library patterns:

- Page: US Letter, 1-inch margins
- Lists: `LevelFormat.BULLET` (never unicode bullets)
- Hyperlinks: `ExternalHyperlink` with `style: "Hyperlink"`, full URL (never truncated)
- Tables: dual widths (`columnWidths` + cell `width`), `ShadingType.CLEAR`
- Validation step after save (`python scripts/office/validate.py output.docx`)

Reference the **docx skill** for setup patterns and best practices.

## Output

```
research_guide_<topic-slug>_<YYYY-MM-DD>.docx
```

Plus:
- Chat summary block: "Saved: <path>. Audit: N searches × M unique papers / K cited. Plan tier: <tier>."
- Audit log printed inline if user asks for it

## Tooling

| Script | Role |
|---|---|
| `scripts/citation_tracker.py` | JSON-backed three-count audit at `~/.litreview_sessions/<session>.json` |
| `scripts/framework_recommender.py` | Heuristic PICO/SPIDER/Decomposition suggestion from research question |
| `scripts/cross_search_aggregator.py` | Repeat-hits + recurring-authors + citation-per-year ranking after Phase 3 |

## References

- [`references/framework_selection.md`](https://github.com/alirezarezvani/claude-skills/tree/main/research/litreview/skills/litreview/references/framework_selection.md) — PICO / SPIDER / Decomposition canon (7+ sources)
- [`references/search_budget_allocation.md`](https://github.com/alirezarezvani/claude-skills/tree/main/research/litreview/skills/litreview/references/search_budget_allocation.md) — depth tiers + cross-search intelligence + sequential execution rationale (7+ sources)
- [`references/docx_8_sections.md`](https://github.com/alirezarezvani/claude-skills/tree/main/research/litreview/skills/litreview/references/docx_8_sections.md) — research guide DOCX spec + technical requirements (7+ sources)

## Anti-Patterns To Reject

- Parallelizing Consensus calls
- Skipping the interactive checkpoint (running all searches without user confirmation)
- Padding thin results with training knowledge
- Defaulting to non-PICO framework without justification
- Citing papers in chat that didn't come from Consensus this session
- Hardcoding plan tier instead of detecting from first response
- Skipping era-gated searches in standard/deep budgets
- Skipping cross-search intelligence (repeat-hits, recurring authors)
- Truncating Consensus URLs in hyperlinks

---

**Version:** 1.0.0
**Source spec:** [`megaprompts/09-litreview-megaprompt.md`](https://github.com/alirezarezvani/claude-skills/tree/main/megaprompts/09-litreview-megaprompt.md)
**Build pattern:** Path B (direct conversion). Sibling of `pulse` (research-pack shape).
