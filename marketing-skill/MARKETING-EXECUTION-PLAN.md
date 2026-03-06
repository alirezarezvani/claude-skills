# Marketing Team Expansion — Execution Plan

## Final Architecture

```
CMO Advisor (c-level-advisor/cmo-advisor/)
  │
  │ reads company-context.md + marketing-context.md
  │
Marketing Ops (router + orchestrator)
  │
  ├── Content Pod (8)
  │   ├── content-creator .......... [UPGRADE] add context integration, quality loop
  │   ├── content-strategy ......... [IMPORT]  from workspace
  │   ├── copywriting .............. [IMPORT]  from workspace
  │   ├── copy-editing ............. [IMPORT]  from workspace
  │   ├── social-content ........... [IMPORT]  from workspace
  │   ├── marketing-ideas .......... [IMPORT]  from workspace
  │   ├── content-production ....... [NEW]     research→write→optimize pipeline
  │   └── content-humanizer ........ [NEW]     AI watermark removal, voice injection
  │
  ├── SEO Pod (5)
  │   ├── seo-audit ................ [IMPORT]  from workspace + add seo_checker.py
  │   ├── programmatic-seo ......... [IMPORT]  from workspace
  │   ├── ai-seo ................... [NEW]     AEO, GEO, LLMO optimization
  │   ├── schema-markup ............ [NEW]     JSON-LD, structured data
  │   └── site-architecture ........ [NEW]     URL structure, nav, internal linking
  │
  ├── CRO Pod (6)
  │   ├── page-cro ................. [IMPORT]  from workspace
  │   ├── form-cro ................. [IMPORT]  from workspace
  │   ├── signup-flow-cro .......... [IMPORT]  from workspace
  │   ├── onboarding-cro ........... [IMPORT]  from workspace
  │   ├── popup-cro ................ [IMPORT]  from workspace
  │   └── paywall-upgrade-cro ...... [IMPORT]  from workspace
  │
  ├── Channels Pod (5)
  │   ├── email-sequence ........... [IMPORT]  from workspace
  │   ├── paid-ads ................. [IMPORT]  from workspace
  │   ├── social-media-manager ..... [UPGRADE] rename + expand from social-media-analyzer
  │   ├── cold-email ............... [NEW]     B2B outreach sequences
  │   └── ad-creative .............. [NEW]     bulk ad generation + iteration
  │
  ├── Growth Pod (3)
  │   ├── ab-test-setup ............ [IMPORT]  from workspace
  │   ├── referral-program ......... [NEW]     referral + affiliate programs
  │   └── free-tool-strategy ....... [NEW]     engineering as marketing
  │
  ├── Intelligence Pod (4)
  │   ├── campaign-analytics ....... [UPGRADE] add cross-channel synthesis
  │   ├── competitor-alternatives .. [IMPORT]  from workspace
  │   ├── marketing-psychology ..... [IMPORT]  from workspace
  │   └── analytics-tracking ....... [NEW]     GA4, GTM, event tracking setup
  │
  └── Sales & GTM Pod (2)
      ├── launch-strategy .......... [IMPORT]  from workspace
      └── pricing-strategy ......... [NEW]     pricing, packaging, monetization

  Standalone (keep in place, no pod):
  ├── marketing-demand-acquisition . [KEEP]    already in repo
  ├── marketing-strategy-pmm ....... [KEEP]    already in repo
  ├── app-store-optimization ....... [KEEP]    already in repo
  └── prompt-engineer-toolkit ...... [KEEP]    already in repo

  Cross-Domain References (marketing-ops routes to these):
  ├── business-growth/revenue-operations/     (RevOps)
  ├── business-growth/sales-engineer/         (Sales Enablement)
  ├── business-growth/customer-success-manager/ (Churn Prevention)
  ├── product-team/landing-page-generator/    (Landing Pages)
  ├── product-team/competitive-teardown/      (Competitive Analysis)
  └── engineering-team/email-template-builder/ (Email Templates)
```

## Totals

| Action | Count |
|--------|-------|
| Import from workspace | 20 |
| Upgrade existing | 3 |
| Build new | 13 |
| Keep as-is | 4 |
| Cross-domain refs | 6 |
| **Total marketing skills** | **39** |
| **New Python tools** | ~20 |
| **New reference docs** | ~25 |
| **New agents** | 5-8 |

---

## Iteration 1: Foundation + Import (20 workspace skills + 2 new)

### 1A: Create branch and foundation skills

**marketing-context/** (NEW — the foundation every skill reads)
```
marketing-context/
├── SKILL.md                    # How to use, interview flow
├── templates/
│   ├── brand-voice.md          # Voice pillars, tone by content type, terminology
│   ├── style-guide.md          # Grammar, formatting, capitalization
│   ├── target-keywords.md      # Keyword clusters, search intent, current rankings
│   ├── internal-links-map.md   # Key pages, anchor text, topic clusters
│   ├── competitor-analysis.md  # Primary competitors, strategies, gaps
│   ├── writing-examples.md     # 3-5 exemplary pieces with annotations
│   └── audience-personas.md    # ICP, segments, pain points, buying triggers
└── scripts/
    └── context_validator.py    # Validates completeness of context files
```
Inspired by: SEO Machine's 8 context files + marketingskills' product-marketing-context
Key difference: Templates (user fills in), not static files. Validator script checks completeness.

**marketing-ops/** (NEW — the router)
```
marketing-ops/
├── SKILL.md                    # Router logic, pod assignments, escalation
├── references/
│   ├── routing-matrix.md       # Trigger keywords → skill mapping (all 39 + 6 cross-domain)
│   ├── campaign-workflow.md    # End-to-end campaign orchestration steps
│   └── quality-checklist.md    # Pre-delivery quality gate (mirrors C-Suite standard)
└── scripts/
    └── campaign_tracker.py     # Track campaign status, tasks, owners, deadlines
```

### 1B: Import 20 workspace skills

For each imported skill:
1. Copy from `~/.openclaw/workspace/skills/{name}/` to `marketing-skill/{name}/`
2. Verify YAML frontmatter (name, description, license, metadata)
3. Add `## Related Skills` section with cross-references
4. Add `## Integration` table (which pod, which skills it works with, cross-domain refs)
5. Add `## Communication` section (references marketing quality standard)

**Import batch (parallel — 4 subagents):**

| Subagent | Skills | Pod |
|----------|--------|-----|
| content-importer | content-strategy, copywriting, copy-editing, social-content, marketing-ideas | Content |
| seo-cro-importer | seo-audit, programmatic-seo, page-cro, form-cro, signup-flow-cro | SEO + CRO |
| cro-channel-importer | onboarding-cro, popup-cro, paywall-upgrade-cro, email-sequence, paid-ads | CRO + Channels |
| growth-intel-importer | ab-test-setup, competitor-alternatives, marketing-psychology, launch-strategy, brand-guidelines | Growth + Intel + GTM |

Each subagent:
- Copies skill folder
- Adds Related Skills section
- Adds Integration table
- Adds Communication standard reference
- Standardizes YAML frontmatter
- Does NOT add Python tools yet (that's Iteration 3)

### 1C: Upgrade 3 existing skills

| Skill | Changes |
|-------|---------|
| content-creator | Add context integration (reads marketing-context), Related Skills, Communication standard |
| social-media-analyzer → social-media-manager | Rename, expand SKILL.md from analyzer to full manager (scheduling, strategy, community) |
| campaign-analytics | Add cross-channel synthesis section, Related Skills, Communication standard |

### 1D: Update CLAUDE.md + marketplace + skills-index

- Rewrite `marketing-skill/CLAUDE.md` (like we did for C-Suite)
- Update `.claude-plugin/marketplace.json`
- Update `.codex/skills-index.json`
- Update root `CLAUDE.md` skill counts
- Update `README.md` badge + counts

### Iteration 1 Deliverables
- [ ] Branch `feat/marketing-expansion`
- [ ] marketing-context/ (foundation)
- [ ] marketing-ops/ (router)
- [ ] 20 imported skills (standardized)
- [ ] 3 upgraded skills
- [ ] Updated CLAUDE.md, marketplace, skills-index
- [ ] PR opened

---

## Iteration 2: Build 13 New Skills (parallel subagents)

### 2A: Content + SEO batch (5 skills — 2 subagents)

**Subagent: content-builder**
| Skill | Key Deliverables |
|-------|-----------------|
| content-production | SKILL.md, references/production-pipeline.md, references/content-brief-template.md, scripts/content_scorer.py (readability + SEO + humanity score), scripts/outline_generator.py |
| content-humanizer | SKILL.md, references/ai-patterns-checklist.md, references/voice-injection-guide.md, scripts/humanizer_scorer.py (detect AI patterns: em-dashes, filler, passive, hedging) |

**Subagent: seo-builder**
| Skill | Key Deliverables |
|-------|-----------------|
| ai-seo | SKILL.md, references/aeo-guide.md (answer engine optimization), references/llm-citation-tactics.md, references/ai-search-landscape.md |
| schema-markup | SKILL.md, references/schema-types-guide.md, references/implementation-patterns.md, scripts/schema_validator.py (validates JSON-LD) |
| site-architecture | SKILL.md, references/url-structure-guide.md, references/internal-linking-strategy.md, scripts/sitemap_analyzer.py |

### 2B: Channels + Growth batch (4 skills — 2 subagents)

**Subagent: channels-builder**
| Skill | Key Deliverables |
|-------|-----------------|
| cold-email | SKILL.md, references/outreach-frameworks.md (AIDA, PAS, BAB), references/deliverability-guide.md, templates/sequence-templates.md, scripts/email_sequence_analyzer.py |
| ad-creative | SKILL.md, references/ad-frameworks.md (by platform), references/creative-testing-guide.md, scripts/headline_scorer.py, scripts/ad_copy_generator.py |

**Subagent: growth-builder**
| Skill | Key Deliverables |
|-------|-----------------|
| referral-program | SKILL.md, references/referral-mechanics.md, references/program-types.md (one-sided, two-sided, tiered), scripts/referral_roi_calculator.py |
| free-tool-strategy | SKILL.md, references/tool-types.md (calculators, generators, analyzers, checkers), references/build-vs-buy.md, scripts/tool_roi_estimator.py |

### 2C: Intelligence + Sales batch (4 skills — 2 subagents)

**Subagent: intel-builder**
| Skill | Key Deliverables |
|-------|-----------------|
| analytics-tracking | SKILL.md, references/ga4-setup-guide.md, references/gtm-patterns.md, references/event-taxonomy.md, scripts/tracking_plan_generator.py |
| pricing-strategy | SKILL.md, references/pricing-models.md (value, cost-plus, competitor, dynamic), references/packaging-guide.md, scripts/pricing_modeler.py, scripts/willingness_to_pay_analyzer.py |

**Subagent: (main agent handles directly)**
These are kept lean — no subagent needed:
- Update marketing-ops routing matrix with all 13 new skills
- Cross-reference all new skills with existing pods

### Iteration 2 Deliverables
- [ ] 13 new skills built (SKILL.md + refs + scripts)
- [ ] All integrated into marketing-ops routing matrix
- [ ] All cross-referenced with Related Skills
- [ ] Commit + push

---

## Iteration 3: Python Tools for Knowledge-Only Skills

Add automation to the 20 imported workspace skills (currently zero scripts).

### Priority 1: SEO + Content tools (highest impact)
| Skill | Script | Purpose |
|-------|--------|---------|
| seo-audit | seo_checker.py | On-page SEO scoring (0-100): title, meta, headings, links, keyword density |
| seo-audit | keyword_density_analyzer.py | Keyword distribution + stuffing detection |
| content-strategy | topic_cluster_mapper.py | Map topic clusters, identify gaps, suggest pillar content |
| copywriting | headline_scorer.py | Score headlines: power words, emotional triggers, length, clarity |
| copy-editing | readability_scorer.py | Flesch Reading Ease, grade level, passive voice, sentence complexity |

### Priority 2: CRO tools
| Skill | Script | Purpose |
|-------|--------|---------|
| page-cro | conversion_audit.py | Above-fold analysis, CTA scoring, trust signals, friction points |
| form-cro | form_friction_analyzer.py | Field count, required fields, multi-step scoring |
| signup-flow-cro | signup_funnel_analyzer.py | Step analysis, drop-off estimation |

### Priority 3: Channel + Growth tools
| Skill | Script | Purpose |
|-------|--------|---------|
| paid-ads | roas_calculator.py | ROAS, CPA, budget allocation optimizer |
| email-sequence | email_flow_designer.py | Sequence timing, open/click estimation |
| ab-test-setup | sample_size_calculator.py | Statistical significance, test duration estimator |
| competitor-alternatives | competitor_matrix_builder.py | Feature comparison matrix generator |

### Priority 4: Intelligence tools
| Skill | Script | Purpose |
|-------|--------|---------|
| campaign-analytics | channel_mixer.py | Cross-channel attribution synthesis |
| marketing-psychology | persuasion_audit.py | Score content against Cialdini's 6 principles |
| launch-strategy | launch_readiness_scorer.py | Pre-launch checklist scoring |

### Iteration 3 Deliverables
- [ ] ~18 new Python scripts (stdlib-only, CLI-first, JSON output)
- [ ] All scripts have embedded sample data for zero-config runs
- [ ] Commit + push

---

## Iteration 4: Quality Upgrade (C-Suite Standard)

Apply to ALL 39 marketing skills:

### 4A: Add to every skill
- [ ] Proactive Triggers (5-6 context-driven alerts per skill)
- [ ] Output Artifacts table (request → deliverable mapping)
- [ ] Communication standard reference
- [ ] Quality loop integration (self-verify, peer-verify)

### 4B: Add marketing-specific agents
| Agent | Location | Purpose |
|-------|----------|---------|
| content-analyzer | marketing-ops/agents/ | Analyzes content for SEO, readability, brand voice |
| seo-optimizer | marketing-ops/agents/ | On-page SEO recommendations |
| meta-creator | marketing-ops/agents/ | Meta title/description generation |
| headline-generator | marketing-ops/agents/ | Headline variations + scoring |
| cro-analyst | marketing-ops/agents/ | CRO audit for any page |

Inspired by SEO Machine's 10 agents, but lean (markdown agents, not Python services).

### 4C: Parity check
Run same audit as C-Suite:
- [ ] All 39 skills: Keywords ✅, QuickStart ✅, Related Skills ✅, Integration ✅, Proactive ✅, Outputs ✅, Communication ✅
- [ ] All Python scripts: syntax valid, sample data works, JSON output
- [ ] All cross-references: bidirectional (A references B, B references A)
- [ ] Marketing-ops routing matrix: all 39 skills + 6 cross-domain

### Iteration 4 Deliverables
- [ ] Quality loop on all 39 skills
- [ ] 5 marketing agents
- [ ] Parity check passed
- [ ] Final commit + PR merge-ready

---

## Execution Timeline

| Iteration | Work | Subagents | Est. Files |
|-----------|------|-----------|-----------|
| 1: Foundation + Import | 22 skills (2 new + 20 import) + 3 upgrades + metadata | 4 | ~80 |
| 2: New Skills | 13 new skills | 6 | ~100 |
| 3: Python Tools | ~18 scripts | 2-3 | ~18 |
| 4: Quality Upgrade | Quality loop + agents + parity | 2-3 | ~50 |
| **Total** | **39 skills** | **~15** | **~250** |

---

## Success Criteria

1. **39 marketing skills** organized into 7 pods + orchestration
2. **~38 Python tools** (18 existing + ~20 new), all stdlib-only
3. **5 marketing agents** (content-analyzer, seo-optimizer, meta-creator, headline-generator, cro-analyst)
4. **Full orchestration** via marketing-ops router with routing matrix
5. **Context foundation** that every skill reads (brand voice, style guide, keywords, etc.)
6. **Cross-domain routing** to 6 skills in business-growth, product-team, engineering-team
7. **C-Suite quality standard** on all skills (proactive triggers, output artifacts, quality loop)
8. **Full cross-referencing** between all skills (Related Skills sections)
9. **CMO integration** — marketing-ops connects to c-level-advisor/cmo-advisor/
10. **Zero external dependencies** — all Python scripts stdlib-only

---

*Ready for execution on Reza's go.*
