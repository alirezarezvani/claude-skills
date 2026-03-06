# Marketing Team Expansion — Audit & Implementation Plan

## Executive Summary

We have **27 marketing skills** spread across two locations (7 in repo, 20 in workspace), zero orchestration, zero automation on the workspace skills, and significant gaps vs. the two reference repos. This plan consolidates, upgrades, and fills gaps to build a **complete marketing division** — from research to production to analytics.

---

## Part 1: Competitive Audit

### Source Repo Analysis

#### SEO Machine (TheCraigHewitt/seomachine)
- **Focus:** SEO-first content production pipeline
- **Strengths we lack:**
  - 🔴 **Content production workflow** — `/research → /write → /optimize → /publish` pipeline (we have no production workflow)
  - 🔴 **10 specialized agents** — content-analyzer, seo-optimizer, meta-creator, internal-linker, keyword-mapper, editor, performance, headline-generator, cro-analyst, landing-page-optimizer
  - 🔴 **23 Python analysis modules** — search intent, keyword density, readability scoring, content length comparator, SEO quality rater, above-fold analyzer, CTA analyzer, trust signal analyzer, landing page scorer
  - 🔴 **Data integrations** — GA4, Google Search Console, DataForSEO
  - 🔴 **Context-driven system** — brand-voice.md, style-guide.md, writing-examples.md, target-keywords.md, internal-links-map.md, competitor-analysis.md, seo-guidelines.md, cro-best-practices.md
  - 🔴 **Landing page system** — `/landing-write`, `/landing-audit`, `/landing-research`, `/landing-competitor`, `/landing-publish`
  - 🟡 **WordPress publishing** — API integration with Yoast SEO (useful but platform-specific)
  - 🟡 **AI watermark scrubber** — `/scrub` command to remove AI patterns
- **Weaknesses:**
  - No orchestration layer (CMO-level strategy missing)
  - No cross-channel coordination
  - External dependencies (nltk, scikit-learn, beautifulsoup4) — violates our stdlib-only rule
  - WordPress-coupled publishing
  - No quality loop or verification

#### Marketing Skills (coreyhaines31/marketingskills)
- **Focus:** Broad marketing skill coverage for SaaS
- **Strengths we lack:**
  - 🔴 **product-marketing-context** as foundation — every skill reads it first (like our company-context.md)
  - 🔴 **ai-seo** — AI search optimization (AEO, GEO, LLMO) — entirely new category
  - 🔴 **site-architecture** — page hierarchy, navigation, URL structure, internal linking
  - 🔴 **schema-markup** — structured data implementation
  - 🔴 **cold-email** — B2B cold outreach emails and sequences
  - 🔴 **ad-creative** — bulk ad creative generation and iteration
  - 🔴 **churn-prevention** — cancel flows, save offers, dunning, payment recovery
  - 🔴 **referral-program** — referral and affiliate programs
  - 🔴 **pricing-strategy** — pricing, packaging, monetization
  - 🔴 **revops** — lead lifecycle, scoring, routing, pipeline management
  - 🔴 **sales-enablement** — sales decks, one-pagers, objection handling, demo scripts
  - 🔴 **Cross-referencing system** — skills reference each other with Related Skills sections
- **Weaknesses:**
  - Zero Python automation (knowledge-only, same as our workspace skills)
  - No orchestration or routing
  - No quality loop
  - No agents

### What We Have vs What They Have

| Capability | Us (repo) | Us (workspace) | SEO Machine | Marketing Skills |
|-----------|-----------|----------------|-------------|-----------------|
| **CRO skills** | 0 | 6 (page, form, signup, onboard, popup, paywall) | 2 (cro-analyst, landing-page-optimizer) | 6 (same as ours) |
| **SEO skills** | 0 | 3 (seo-audit, programmatic-seo, competitor-alt) | Full stack (5 agents + 5 modules) | 5 (seo-audit, ai-seo, programmatic, schema, site-arch) |
| **Content/Copy** | 1 (content-creator) | 4 (content-strategy, copywriting, copy-editing, social-content) | Full pipeline (research→write→optimize→publish) | 3 (copywriting, copy-editing, cold-email) |
| **Email** | 0 | 1 (email-sequence) | 0 | 2 (email-sequence, cold-email) |
| **Paid/Ads** | 0 | 1 (paid-ads) | 0 | 2 (paid-ads, ad-creative) |
| **Analytics** | 1 (campaign-analytics) | 1 (ab-test-setup) | 3 (GA4, GSC, DataForSEO) | 1 (analytics-tracking) |
| **Strategy** | 2 (pmm, demand-acq) | 3 (content-strategy, launch-strategy, marketing-ideas) | Content prioritization | 4 (launch, pricing, marketing-ideas, marketing-psych) |
| **Growth/Retention** | 0 | 0 | 0 | 3 (referral, free-tool, churn-prevention) |
| **Sales/RevOps** | 0 | 0 | 0 | 2 (revops, sales-enablement) |
| **Python tools** | 18 scripts | 0 | 23 modules (external deps) | 0 |
| **Agents** | 0 | 0 | 10 | 0 |
| **Orchestration** | 0 | 0 | 0 | product-marketing-context (foundation only) |
| **Context system** | 0 | 0 | 8 context files | 1 (product-marketing-context) |
| **Production workflow** | 0 | 0 | Full (research→write→optimize→publish) | 0 |
| **Landing pages** | 0 | 0 | Full (5 commands) | 0 |

---

## Part 2: Gap Analysis — What's Missing

### 🔴 Critical Gaps (must build)

1. **Orchestration layer** — no router, no coordination between 27 skills
2. **Content production pipeline** — no research→write→optimize→publish workflow
3. **SEO automation** — our seo-audit is knowledge-only, no analysis tools
4. **Landing page system** — no landing page creation or CRO analysis
5. **AI SEO (AEO/GEO/LLMO)** — entirely missing category, increasingly important
6. **Context system** — no brand-voice, style-guide, or product-marketing-context foundation
7. **Cross-referencing** — skills don't know about each other

### 🟡 Important Gaps (should build)

8. **Schema markup** — structured data implementation
9. **Site architecture** — URL structure, navigation, internal linking strategy
10. **Cold email / outreach** — B2B outreach sequences
11. **Ad creative** — bulk ad generation and iteration
12. **Churn prevention** — cancel flows, save offers, dunning
13. **Referral programs** — referral and affiliate program design
14. **Pricing strategy** — pricing, packaging, monetization
15. **RevOps** — lead lifecycle, scoring, routing
16. **Sales enablement** — sales decks, objection handling

### ⚪ Nice to Have

17. **WordPress/CMS publishing** — platform-specific, lower priority
18. **AI watermark scrubber** — content de-robotification
19. **Social media manager** — full management vs. current analyzer

---

## Part 3: Architecture

```
CMO Advisor (C-Suite — strategy, budget, growth model)
         │
         │ reads company-context.md + marketing-context.md
         │
    Marketing Ops (router + orchestrator)
         │
    ┌────┼────────┬──────────┬──────────┬──────────┬──────────┐
    │    │        │          │          │          │          │
 Content SEO    CRO      Channels   Growth    Intel     Sales
  Pod    Pod    Pod       Pod        Pod       Pod       Pod
  (8)    (5)    (6)       (5)        (4)       (4)       (3)

Total: 35 skills + 1 orchestration + 1 context foundation = 37
```

### Pod Breakdown

#### Context Foundation (1 skill — NEW)
| Skill | Status | Source |
|-------|--------|--------|
| **marketing-context** | 🆕 Build | Inspired by SEO Machine's context system + marketingskills' product-marketing-context |

Creates and maintains: brand-voice.md, style-guide.md, target-keywords.md, internal-links-map.md, competitor-analysis.md, writing-examples.md. Every marketing skill reads this first.

#### Orchestration (1 skill — NEW)
| Skill | Status | Source |
|-------|--------|--------|
| **marketing-ops** | 🆕 Build | Router + campaign orchestrator (like C-Suite Chief of Staff) |

Routes questions, coordinates campaigns, enforces quality loop, connects to CMO above.

#### Content Pod (8 skills — 5 existing + 3 new)
| Skill | Status | Source |
|-------|--------|--------|
| content-creator | ✅ Upgrade | Repo (add context integration, quality loop) |
| content-strategy | ✅ Import | Workspace |
| copywriting | ✅ Import | Workspace |
| copy-editing | ✅ Import | Workspace |
| social-content | ✅ Import | Workspace |
| marketing-ideas | ✅ Import | Workspace |
| **content-production** | 🆕 Build | Inspired by SEO Machine's /research→/write→/optimize pipeline |
| **content-humanizer** | 🆕 Build | Inspired by SEO Machine's editor agent + /scrub command |

#### SEO Pod (5 skills — 2 existing + 3 new)
| Skill | Status | Source |
|-------|--------|--------|
| seo-audit | ✅ Import | Workspace (+ add Python tools) |
| programmatic-seo | ✅ Import | Workspace |
| **ai-seo** | 🆕 Build | From marketingskills (AEO, GEO, LLMO optimization) |
| **schema-markup** | 🆕 Build | From marketingskills (structured data) |
| **site-architecture** | 🆕 Build | From marketingskills (URL structure, nav, internal linking) |

#### CRO Pod (6 skills — all existing)
| Skill | Status | Source |
|-------|--------|--------|
| page-cro | ✅ Import | Workspace |
| form-cro | ✅ Import | Workspace |
| signup-flow-cro | ✅ Import | Workspace |
| onboarding-cro | ✅ Import | Workspace |
| popup-cro | ✅ Import | Workspace |
| paywall-upgrade-cro | ✅ Import | Workspace |

#### Channels Pod (5 skills — 3 existing + 2 new)
| Skill | Status | Source |
|-------|--------|--------|
| email-sequence | ✅ Import | Workspace |
| paid-ads | ✅ Import | Workspace |
| social-media-analyzer → social-media-manager | ✅ Upgrade | Repo (expand from analyzer to manager) |
| **cold-email** | 🆕 Build | From marketingskills (B2B outreach) |
| **ad-creative** | 🆕 Build | From marketingskills (bulk ad generation) |

#### Growth & Retention Pod (4 skills — 1 existing + 3 new)
| Skill | Status | Source |
|-------|--------|--------|
| ab-test-setup | ✅ Import | Workspace |
| **churn-prevention** | 🆕 Build | From marketingskills (cancel flows, save offers, dunning) |
| **referral-program** | 🆕 Build | From marketingskills (referral + affiliate) |
| **free-tool-strategy** | 🆕 Build | From marketingskills (engineering as marketing) |

#### Intelligence Pod (4 skills — 3 existing + 1 new)
| Skill | Status | Source |
|-------|--------|--------|
| campaign-analytics | ✅ Upgrade | Repo (add cross-channel synthesis) |
| competitor-alternatives | ✅ Import | Workspace |
| marketing-psychology | ✅ Import | Workspace |
| **analytics-tracking** | 🆕 Build | From marketingskills (GA4, GTM, event tracking setup) |

#### Sales & GTM Pod (3 skills — 1 existing + 2 new)
| Skill | Status | Source |
|-------|--------|--------|
| launch-strategy | ✅ Import | Workspace |
| **pricing-strategy** | 🆕 Build | From marketingskills (pricing, packaging, monetization) |
| **sales-enablement** | 🆕 Build | From marketingskills (sales decks, objection handling) |

### Also Import (not in pods)
| Skill | Status |
|-------|--------|
| brand-guidelines | ✅ Import (merge into marketing-context) |
| marketing-demand-acquisition | ✅ Keep in repo |
| marketing-strategy-pmm | ✅ Keep in repo |
| app-store-optimization | ✅ Keep in repo |
| prompt-engineer-toolkit | ✅ Keep in repo |

---

## Part 4: Totals

| Category | Existing (import/upgrade) | New (build) | Total |
|----------|--------------------------|-------------|-------|
| Context | 0 | 1 | 1 |
| Orchestration | 0 | 1 | 1 |
| Content | 5 + 1 upgrade | 2 | 8 |
| SEO | 2 | 3 | 5 |
| CRO | 6 | 0 | 6 |
| Channels | 2 + 1 upgrade | 2 | 5 |
| Growth | 1 | 3 | 4 |
| Intelligence | 2 + 1 upgrade | 1 | 4 |
| Sales & GTM | 1 | 2 | 3 |
| Standalone | 4 (keep as-is) | 0 | 4 |
| **TOTAL** | **24** | **15** | **41** |

---

## Part 5: What Each New Skill Needs

Every new skill gets the C-Suite quality standard:
- YAML frontmatter (name, description, license, metadata)
- Keywords section (trigger-optimized)
- Quick Start (3-step)
- Key Questions (diagnostic)
- Integration table (which skills it works with)
- Proactive Triggers (context-driven alerts)
- Output Artifacts (request → deliverable)
- Communication standard (bottom line first, structured output)
- Related Skills section (cross-references)
- Python tools (stdlib-only, CLI-first, JSON output)
- Reference docs (heavy content here, not SKILL.md)

---

## Part 6: Python Tools Plan

### Import SEO Machine concepts (rebuilt stdlib-only)
| Script | Original | Our version |
|--------|----------|-------------|
| search_intent_analyzer.py | Uses nltk | Regex + heuristic (stdlib) |
| keyword_analyzer.py | Uses scikit-learn | Counter + re (stdlib) |
| readability_scorer.py | Uses textstat | Flesch formula (stdlib, pure math) |
| seo_quality_rater.py | External deps | Checklist scorer (stdlib) |
| content_length_comparator.py | Web scraping | Input-based comparison (stdlib) |
| above_fold_analyzer.py | BeautifulSoup | html.parser (stdlib) |
| cta_analyzer.py | BeautifulSoup | html.parser (stdlib) |
| landing_page_scorer.py | External | Composite scorer (stdlib) |

### New tools for existing skills
| Skill | New tool | Purpose |
|-------|----------|---------|
| seo-audit | seo_checker.py | On-page SEO scoring (0-100) |
| content-strategy | topic_cluster_mapper.py | Map topic clusters and gaps |
| copywriting | headline_scorer.py | Score headlines by power words, length, emotion |
| email-sequence | email_flow_designer.py | Design drip sequences with timing |
| paid-ads | roas_calculator.py | ROAS and budget allocation |
| campaign-analytics | channel_mixer.py | Cross-channel attribution synthesis |
| pricing-strategy | pricing_modeler.py | Price sensitivity and packaging optimizer |
| churn-prevention | churn_risk_scorer.py | Score churn signals |

---

## Part 7: Execution Phases

### Phase 1: Foundation + Import (batch 1)
**Goal:** Import 20 workspace skills, create context foundation, build orchestration
**Estimated:** ~80 files, 6 subagents
- Import all 20 workspace skills into `marketing-skill/`
- Add YAML frontmatter standardization where needed
- Create `marketing-context/` (context foundation)
- Create `marketing-ops/` (router/orchestrator)
- Add Related Skills cross-references to all imported skills
- Update CLAUDE.md

### Phase 2: New Skills (batch 2)
**Goal:** Build 13 missing skills
**Estimated:** ~100 files, 6 subagents
- SEO: ai-seo, schema-markup, site-architecture
- Content: content-production, content-humanizer
- Channels: cold-email, ad-creative
- Growth: churn-prevention, referral-program, free-tool-strategy
- Intelligence: analytics-tracking
- Sales: pricing-strategy, sales-enablement

### Phase 3: Python Tools (batch 3)
**Goal:** Add automation to knowledge-only skills
**Estimated:** ~20 scripts
- SEO analysis tools (search intent, keyword, readability, SEO quality)
- Content tools (headline scorer, topic mapper)
- CRO tools (above-fold, CTA, landing page scorer)
- Channel tools (ROAS calculator, email flow designer)
- Growth tools (churn risk scorer, pricing modeler)

### Phase 4: Quality Upgrade (batch 4)
**Goal:** Apply C-Suite quality standard to all 37 skills
- Proactive triggers on all skills
- Output artifacts on all skills
- Integration tables on all skills
- Communication standard references
- Quality loop integration
- Final parity check

---

## Part 8: Already Exists Elsewhere in Repo — DO NOT DUPLICATE

Cross-repo audit found these "missing" capabilities already exist in other domains. The marketing team should **reference** them, not rebuild them.

| "Missing" Capability | Already Exists At | What It Has |
|---------------------|-------------------|-------------|
| **Revenue Operations / RevOps** | `business-growth/revenue-operations/` | 3 Python tools: pipeline_analyzer, forecast_accuracy_tracker, gtm_efficiency_calculator |
| **Sales Enablement** | `business-growth/sales-engineer/` | 3 Python tools: rfp_response_analyzer, poc_planner, competitive_matrix_builder |
| **Churn Prevention** | `business-growth/customer-success-manager/` | 3 Python tools: churn_risk_analyzer, expansion_opportunity_scorer, health_score_calculator |
| **Landing Pages** | `product-team/landing-page-generator/` | Full Next.js/React landing page generation with copy frameworks, CRO patterns |
| **Competitive Analysis** | `product-team/competitive-teardown/` | Feature matrices, SWOT, positioning maps, UX audits |
| **Email Templates** | `engineering-team/email-template-builder/` | React Email, provider integration, i18n, dark mode, spam optimization |
| **Pricing Strategy** (partial) | `product-team/product-strategist/` | OKR cascade, product strategy (pricing is a component) |
| **Financial Analysis** | `finance/financial-analyst/` | DCF, ratios, budget variance, forecasting |
| **Contract/Proposal** | `business-growth/contract-and-proposal-writer/` | Proposal generation |
| **Stripe/Payments** | `engineering-team/stripe-integration-expert/` | Payment flows, subscription billing |

### Impact on Plan

**Remove from "new to build" list:**
- ~~revops~~ → already at `business-growth/revenue-operations/`
- ~~sales-enablement~~ → already at `business-growth/sales-engineer/`
- ~~churn-prevention~~ → already at `business-growth/customer-success-manager/`

**Keep building (truly missing):**
- ✅ pricing-strategy (dedicated marketing pricing, not product strategy)
- ✅ cold-email (B2B outreach — distinct from email-sequence)
- ✅ ad-creative (bulk ad generation)
- ✅ referral-program (referral + affiliate programs)
- ✅ free-tool-strategy (engineering as marketing)
- ✅ ai-seo (AEO/GEO/LLMO — entirely new category)
- ✅ schema-markup (structured data)
- ✅ site-architecture (URL structure, nav, internal linking)
- ✅ content-production (research→write→optimize pipeline)
- ✅ content-humanizer (AI watermark removal, voice injection)
- ✅ analytics-tracking (GA4, GTM, event tracking setup)
- ✅ marketing-context (foundation — brand voice, style guide, etc.)
- ✅ marketing-ops (orchestration router)

**Cross-reference in marketing-ops routing matrix:**
The marketing-ops router should know about and route to these business-growth/product-team skills when relevant, just like C-Suite's Chief of Staff routes across domains.

### Revised Totals

| Category | Existing (import/upgrade) | New (build) | Total |
|----------|--------------------------|-------------|-------|
| Context | 0 | 1 | 1 |
| Orchestration | 0 | 1 | 1 |
| Content | 5 + 1 upgrade | 2 | 8 |
| SEO | 2 | 3 | 5 |
| CRO | 6 | 0 | 6 |
| Channels | 2 + 1 upgrade | 2 | 5 |
| Growth | 1 | 2 (referral, free-tool) | 3 |
| Intelligence | 2 + 1 upgrade | 1 | 4 |
| Sales & GTM | 1 | 1 (pricing-strategy) | 2 |
| Standalone | 4 (keep as-is) | 0 | 4 |
| **TOTAL** | **24** | **13** | **39** |

Down from 41 to 39 — removed 3 duplicates, cleaner architecture.

---

## Part 9: Skills NOT Included (and why)

| Skill | Source | Reason for exclusion |
|-------|--------|---------------------|
| WordPress publishing | SEO Machine | Platform-specific, not universal |
| DataForSEO integration | SEO Machine | Paid API, violates stdlib-only rule |
| GA4/GSC Python clients | SEO Machine | External deps (google-api-python-client) |
| revops | marketingskills | Already at `business-growth/revenue-operations/` |
| sales-enablement | marketingskills | Already at `business-growth/sales-engineer/` |
| churn-prevention | marketingskills | Already at `business-growth/customer-success-manager/` |
| product-marketing-context | marketingskills | Replaced by our marketing-context (richer) |

---

*Created: 2026-03-06*
*Target: PR on `feat/marketing-expansion` branch*
