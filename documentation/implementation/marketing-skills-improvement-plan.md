# Marketing Skills Improvement Plan — Inspired by claude-seo/ads/blog

**Status:** Active (created 2026-04-13)
**Inspired by:** claude-seo (4.7k stars), claude-ads (2.4k stars), claude-blog (466 stars)
**Scope:** Improve 5 existing marketing skills with 8 cross-cutting patterns. No replacements — purely additive.

---

## The 8 patterns to adopt

1. **Weighted 0-100 scoring** — replace binary pass/fail with numeric health scores
2. **Priority levels with SLAs** — Critical/High/Medium/Low + time-to-fix
3. **Industry auto-detection** — route to different check weights by business type
4. **On-demand reference loading** — modular .md files instead of inline knowledge
5. **Quality gates (hard stops)** — non-negotiable rules that block action
6. **Multi-tier API fallback** — free tier always works, premium tier enhances
7. **Quick Wins prioritization** — severity × impact / time-to-fix
8. **AI citation readiness** — dual-optimize for Google + AI platforms

---

## Phase 1 — Scoring systems + references (seo-audit, paid-ads)

### seo-audit improvements
- Weighted 0-100 health score: Technical 22%, Content 23%, On-Page 20%, Schema 10%, Performance 10%, AI Readiness 10%, Images 5%
- Priority levels (Critical/High/Medium/Low) with SLAs on every finding
- Industry auto-detection (SaaS/local/ecommerce/publisher) → different weight profiles
- New references: cwv-thresholds.md, schema-types.md, eeat-framework.md
- New script: seo_health_scorer.py (compute weighted score from check results)

### paid-ads improvements
- Platform-specific checks with weighted scoring (Google 74, Meta 46, LinkedIn 25, TikTok 25)
- Severity multiplier matrix (Critical=5x, High=3x, Medium=1.5x, Low=0.5x) × category weights
- Budget-weighted cross-platform aggregation: Score = Σ(Platform_Score × Budget_Share)
- Brand DNA extraction (7 voice axes) as reusable JSON
- Copy framework selection logic: AIDA vs PAS vs BAB by product type
- Quick Wins: severity × estimated_impact / time_to_fix
- New references: google-audit.md, meta-audit.md, scoring-system.md, copy-frameworks.md
- New script: ad_health_scorer.py

## Phase 2 — Content scoring + quality gates (content-creator, content-production)

### content-creator improvements
- Dual-optimization: Google rankings + AI citation platforms (Perplexity, ChatGPT, AI Overviews)
- 12 content templates with auto-selection logic
- Answer-first formatting (40-60 word paragraphs at H2) for AI extractability
- Passage-level citability checks (120-180 word chunks, Q&A formatting)
- New references: content-templates.md, ai-citation-readiness.md

### content-production improvements
- 100-point scoring: Content Quality 30, SEO 25, E-E-A-T 15, Technical 15, AI Citation 15
- Score bands → action: <60 rewrite, 60-69 rework, 70-79 target, 80-89 publish, 90+ flagship
- Quality gates: zero fabricated stats, heading hierarchy, image alt text, source tier
- Freshness signals: dateModified tracking, decay detection
- New script: content_scorer.py

## Phase 3 — AI detection + readability (copy-editing)

### copy-editing improvements
- AI content detection: burstiness (sentence length variance), vocabulary diversity (TTR), 17 AI phrases
- Readability bands: Consumer (Flesch 60-80), Professional (50-60), Technical (30-50)
- Anti-pattern enforcement: passive voice ≤10%, AI words ≤5/1K, transition words 20-30%
- Paragraph micro-scoring: 40-80 word ideal, >150 blocking
- New scripts: ai_content_detector.py, readability_scorer.py

---

## What we DON'T adopt (anti-patterns to avoid)

- No timeout fallbacks on parallel agents (claude-ads blocks if one agent fails — we should fail gracefully)
- No paid API requirements (claude-seo needs DataForSEO for full coverage — we keep stdlib-only)
- No external ML model dependencies (claude-blog uses Google NLP — we use deterministic analysis)
- No WeasyPrint/matplotlib for reporting (heavy deps — we use markdown/JSON output)

---

## Execution

- Each phase: feature branch → PR to dev → /plugin-audit → merge
- Each skill keeps its existing SKILL.md structure; new files are additive
- Scripts are Python stdlib-only, CLI-first, --json output
- References are lazy-loaded .md files, not inline in SKILL.md
