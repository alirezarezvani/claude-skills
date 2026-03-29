---
name: "marketing-skills"
description: "42 marketing agent skills and plugins for Claude Code, Codex, Gemini CLI, Cursor, OpenClaw, and 6 more coding agents. 7 pods: content, SEO, CRO, channels, growth, intelligence, sales. Foundation context + orchestration router. 27 Python tools (stdlib-only)."
version: 2.0.0
author: Alireza Rezvani
license: MIT
tags:
  - marketing
  - seo
  - content
  - copywriting
  - cro
  - analytics
  - ai-seo
agents:
  - claude-code
  - codex-cli
  - openclaw
---

# Marketing Skills Division

42 production-ready marketing skills organized into 7 specialist pods with a context foundation and orchestration layer.

## Quick Start

### Claude Code
```
/read marketing-skill/marketing-ops/SKILL.md
```
The router will direct you to the right specialist skill.

### Codex CLI
```bash
codex --full-auto "Read marketing-skill/marketing-ops/SKILL.md, then help me write a blog post about [topic]"
```

### OpenClaw
Skills are auto-discovered from the repository. Ask your agent for marketing help — it routes via `marketing-ops`.

## Architecture

```
marketing-skill/
├── marketing-context/     ← Foundation: brand voice, audience, goals
├── marketing-ops/         ← Router: dispatches to the right skill
│
├── Content Pod (8)        ← Strategy → Production → Editing → Social
├── SEO Pod (5)            ← Traditional + AI SEO + Schema + Architecture
├── CRO Pod (6)            ← Pages, Forms, Signup, Onboarding, Popups, Paywall
├── Channels Pod (5)       ← Email, Ads, Cold Email, Ad Creative, Social Mgmt
├── Growth Pod (4)         ← A/B Testing, Referrals, Free Tools, Churn
├── Intelligence Pod (4)   ← Competitors, Psychology, Analytics, Campaigns
└── Sales & GTM Pod (2)    ← Pricing, Launch Strategy
```

## First-Time Setup

Run `marketing-context` to create your `marketing-context.md` file. Every other skill reads this for brand voice, audience personas, and competitive landscape. Do this once — it makes everything better.

## Pod Overview

| Pod | Skills | Python Tools | Key Capabilities |
|-----|--------|-------------|-----------------|
| **Foundation** | 2 | 2 | Brand context capture, skill routing |
| **Content** | 8 | 5 | Strategy → production → editing → humanization |
| **SEO** | 5 | 2 | Technical SEO, AI SEO (AEO/GEO), schema, architecture |
| **CRO** | 6 | 0 | Page, form, signup, onboarding, popup, paywall optimization |
| **Channels** | 5 | 2 | Email sequences, paid ads, cold email, ad creative |
| **Growth** | 4 | 2 | A/B testing, referral programs, free tools, churn prevention |
| **Intelligence** | 4 | 4 | Competitor analysis, marketing psychology, analytics, campaigns |
| **Sales & GTM** | 2 | 1 | Pricing strategy, launch planning |
| **Standalone** | 4 | 9 | ASO, brand guidelines, PMM strategy, prompt engineering |

## Python Tools (27 scripts)

All scripts are stdlib-only (zero pip installs), CLI-first with JSON output, and include embedded sample data for demo mode.

```bash
# Content scoring
python3 marketing-skill/content-production/scripts/content_scorer.py article.md

# AI writing detection
python3 marketing-skill/content-humanizer/scripts/humanizer_scorer.py draft.md

# Brand voice analysis
python3 marketing-skill/content-production/scripts/brand_voice_analyzer.py copy.txt

# Ad copy validation
python3 marketing-skill/ad-creative/scripts/ad_copy_validator.py ads.json

# Pricing scenario modeling
python3 marketing-skill/pricing-strategy/scripts/pricing_modeler.py

# Tracking plan generation
python3 marketing-skill/analytics-tracking/scripts/tracking_plan_generator.py
```

## Unique Features

- **AI SEO (AEO/GEO/LLMO)** — Optimize for AI citation, not just ranking
- **Content Humanizer** — Detect and fix AI writing patterns with scoring
- **Context Foundation** — One brand context file feeds all 42 skills
- **Orchestration Router** — Smart routing by keyword + complexity scoring
- **Zero Dependencies** — All Python tools use stdlib only
