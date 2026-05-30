---
name: "cs-aeo"
description: "/cs:aeo — Answer Engine Optimization workflow. Audit content for E-E-A-T + structure signals that drive LLM citation (ChatGPT, Perplexity, Claude, Gemini, Mistral). Optimize content in 3 modes (conservative/balanced/aggressive). Track which LLMs cite which pages via local ledger. Industry-aware thresholds (8 industries with YMYL calibration). Distinct from SEO — refuses to optimize one at expense of the other."
---

# /cs:aeo — Answer Engine Optimization

**Command:** `/cs:aeo [action] [args]`

The `cs-aeo` command is the **entry point for AEO workflows**: audit → optimize → publish → track citations.

## Distinct From `/cs:seo-audit`

These share a foundation (E-E-A-T) but optimize for different conversion events:

- **`/cs:seo-audit`** — optimizes for ranking + click-through in Google/Bing search results
- **`/cs:aeo`** (this command) — optimizes for being cited as authoritative source by LLMs

They can run on the same content. The cs-aeo agent will surface this and recommend running both for high-leverage pages.

## When To Run

- Auditing existing content for AI-search readiness (E-E-A-T + structure signals)
- Optimizing a page for LLM citation before publishing
- Tracking which LLMs cite which pages over time (citation ledger)
- Researching whether AEO investment is worth it for a given content piece
- Benchmarking against competitor citation rates

## When NOT To Run

- Pure click-through SEO without AI-citation intent → use `/cs:seo-audit`
- Brand-voice content with no factual claims (citations require facts)
- Time-sensitive news (LLM training lag means citation comes months later)
- Topics where LLMs already have strong training (e.g., elementary math)

## Actions

### `audit` — Score content for AEO readiness

```bash
/cs:aeo audit --input post.md --industry saas
/cs:aeo audit --url https://example.com/blog/post --industry healthcare
/cs:aeo audit --sample
```

Returns composite 0-100 with per-dimension breakdown (E-E-A-T + Structure) and top 5 fixes in priority order.

### `optimize` — Generate AEO-improved variant

```bash
/cs:aeo optimize --input post.md --mode balanced --output post-aeo.md
/cs:aeo optimize --input post.md --mode aggressive --industry finance
```

Three modes:
- `conservative` — touch <10% of words (schema + corrections footer only)
- `balanced` — touch <30% (citation markers + heading restructure + schema + footer)
- `aggressive` — full restructure + fact-first lede + maximum citation density

### `track` — Log a citation you observed in an LLM response

```bash
/cs:aeo track --url https://example.com/post --llm perplexity --query "what is AEO" --date 2026-05-17
```

Maintains a local ledger at `~/.aeo-data/citations.json`. No telemetry.

### `report` — Aggregate citation report for a URL

```bash
/cs:aeo report --url https://example.com/post
```

Returns total citations, LLM coverage, velocity, top queries, verdict (EARLY / EMERGING / STRONG).

### `export` — Emit citation ledger as CSV

```bash
/cs:aeo export --output citations.csv
```

For reporting to clients / stakeholders.

## Minimal Intake (3 Questions)

| Q | Asks | When |
|---|---|---|
| Q1 | What action — audit / optimize / track / report? | Always |
| Q2 | Industry (saas / healthcare / finance / legal / ecommerce / b2b / media / education) | Always (calibrates thresholds) |
| Q3 | For `optimize`: mode (conservative / balanced / aggressive)? | Only when action=optimize |

Most invocations exit intake after Q2.

## Workflow

```bash
# Phase 1: Audit
python3 marketing-skill/skills/aeo/scripts/aeo_audit.py --input <file> --industry <industry>
# → composite score 0-100 + top fixes

# Phase 2: Optimize (if audit < industry threshold)
python3 marketing-skill/skills/aeo/scripts/aeo_optimizer.py \
  --input <file> --mode <mode> --industry <industry> --output <file>-aeo.md
# → optimized variant + changelog

# Phase 3: Publish (manual step — review the optimized variant, then deploy)

# Phase 4: Track (over 4-12 weeks)
python3 marketing-skill/skills/aeo/scripts/citation_tracker.py \
  --action add --url <url> --llm <llm> --query <query> --date <YYYY-MM-DD>
# → ledger updated

# Phase 5: Report (monthly)
python3 marketing-skill/skills/aeo/scripts/citation_tracker.py \
  --action report --url <url>
# → per-URL citation report
```

## Industry-Specific Thresholds

The auditor calibrates per-industry. YMYL ("Your Money or Your Life") topics use stricter thresholds:

| Industry | Min Composite | Why |
|---|---|---|
| Healthcare | 85 | Direct health implications |
| Finance | 85 | Real financial decisions |
| Legal | 85 | Legal jeopardy if misapplied |
| Education | 75 | Learning outcomes |
| SaaS, B2B, Media | 70 | Business decisions, moderate stakes |
| E-commerce | 65 | Product reviews, lower individual risk |

Content for YMYL topics scoring below threshold is unlikely to be cited regardless of other signals — the cs-aeo agent will flag this and refuse aggressive optimization until the foundational dimensions improve.

## Anti-Patterns Rejected

- LLM-generated AEO content with no human review (RAG retrieval deprioritizes generic LLM output)
- Fabricated credentials in author bylines (LLMs cross-reference via LinkedIn/Wikipedia)
- Schema spam (false structured-data markup gets filtered)
- Authority laundering (linking out doesn't confer authority)
- Per-LLM optimization tunnel-vision (73% cross-LLM citation correlation — optimize for shared signals)
- Optimizing AEO at expense of SEO (and vice versa) — they complement, don't substitute

## Trigger Phrases

- "AEO audit"
- "optimize for ChatGPT / Perplexity / Claude / Gemini"
- "get cited by [LLM]"
- "LLM citation strategy"
- "answer engine optimization"
- "E-E-A-T audit"
- "content for AI search"
- "track AI citations"
- "schema for AI"

## Related

- Agent: [`cs-aeo`](../agents/cs-aeo.md)
- Skill: [`aeo`](../skills/aeo/SKILL.md)
- Companion: `/cs:seo-audit` (SEO + AEO often run together)
- Source: ported from [`alirezarezvani/aeo-box`](https://github.com/alirezarezvani/aeo-box)

---

**Version:** 2.7.3
**License:** MIT
