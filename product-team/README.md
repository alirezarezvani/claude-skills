# Product Team Skills Collection

**8 production-ready product skills** covering product management, agile delivery, strategy, UX research, design systems, competitive intelligence, landing pages, and SaaS scaffolding.

---

## Overview

- **8 skills** covering the full product lifecycle from discovery to delivery
- **9 Python automation tools** (stdlib only, zero dependencies)
- **4 agents** orchestrating skills across product workflows
- **5 slash commands** for quick access to common operations

---

## Skills Catalog

### 1. Product Manager Toolkit
**Python Tools:** `rice_prioritizer.py`, `customer_interview_analyzer.py`

RICE prioritization with portfolio analysis, customer interview NLP analysis, PRD templates, and discovery frameworks.

### 2. Agile Product Owner
**Python Tools:** `user_story_generator.py`

INVEST-compliant user story generation, sprint planning with capacity allocation, epic breakdown, and acceptance criteria.

### 3. Product Strategist
**Python Tools:** `okr_cascade_generator.py`

OKR cascade generation (company to product to team), alignment scoring, and 5 strategy templates.

### 4. UX Researcher Designer
**Python Tools:** `persona_generator.py`

Data-driven persona generation, journey mapping frameworks, usability testing protocols, and empathy maps.

### 5. UI Design System
**Python Tools:** `design_token_generator.py`

Design token generation from brand color (CSS, JSON, SCSS), typography scales, spacing grids, and responsive breakpoints.

### 6. Competitive Teardown
**Python Tools:** `competitive_matrix_builder.py`

12-dimension competitive scoring, feature matrices, SWOT analysis, positioning maps, and stakeholder presentations.

### 7. Landing Page Generator
**Python Tools:** `landing_page_scaffolder.py`

Next.js/React TSX components with Tailwind CSS, 4 design styles, copy frameworks (PAS, AIDA, BAB), SEO optimization. Also supports HTML output.

### 8. SaaS Scaffolder
**Python Tools:** `project_bootstrapper.py`

Production SaaS boilerplate with Next.js, TypeScript, auth (NextAuth/Clerk/Supabase), payments (Stripe/Lemon Squeezy), and Docker.

---

## Slash Commands

| Command | Script | Purpose |
|---------|--------|---------|
| `/rice` | `rice_prioritizer.py` | Feature prioritization |
| `/okr` | `okr_cascade_generator.py` | OKR cascade generation |
| `/persona` | `persona_generator.py` | Persona generation |
| `/user-story` | `user_story_generator.py` | User story generation |
| `/competitive-matrix` | `competitive_matrix_builder.py` | Competitive analysis |

---

## Quick Start

```bash
# Prioritize your backlog
python product-manager-toolkit/scripts/rice_prioritizer.py features.csv --capacity 20

# Generate user stories for a sprint
python agile-product-owner/scripts/user_story_generator.py sprint 30

# Create OKR cascade
python product-strategist/scripts/okr_cascade_generator.py growth

# Generate personas
python ux-researcher-designer/scripts/persona_generator.py

# Generate design tokens
python ui-design-system/scripts/design_token_generator.py "#0066CC" modern css

# Competitive analysis
python competitive-teardown/scripts/competitive_matrix_builder.py competitors.json

# Scaffold a landing page (TSX + Tailwind)
python landing-page-generator/scripts/landing_page_scaffolder.py config.json --format tsx

# Bootstrap a SaaS project
python saas-scaffolder/scripts/project_bootstrapper.py config.json
```

---

## Agents

| Agent | Skills Orchestrated |
|-------|-------------------|
| `cs-product-manager` | All 8 product skills |
| `cs-agile-product-owner` | Agile product owner + product manager toolkit |
| `cs-product-strategist` | Product strategist + competitive teardown |
| `cs-ux-researcher` | UX researcher + product manager toolkit + UI design system |

---

**Last Updated:** March 10, 2026
**Version:** v2.1.2
**Skills Deployed:** 8/8 production-ready
**Total Tools:** 9 Python automation tools
