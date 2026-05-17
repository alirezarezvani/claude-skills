---
name: "product-skills"
description: "Plugin index and orchestration router for the 10-skill product-team family covering PM toolkit (RICE), agile PO, product strategist (OKR), UX researcher/designer, UI design system, competitive teardown, landing page generator, SaaS scaffolder, product analytics, product discovery, roadmap communicator, spec-to-repo, and research summarizer. Triggers include \"product-skills overview,\" \"what product skills are available,\" \"list product tools,\" \"product capabilities,\" \"product plugin help,\" \"what can the product plugin do.\" Relevant for Mo: this is the umbrella under which product decisions for Mo platform (psychology-first matching, broker-owner SaaS, founder-tier pricing), Curb (consumer iOS, dual SKU, home-readiness score), askminimo ($19.99/mo agent AI tool), and Maureen Personal (Door 01/02/03 founder-led offerings) get routed. Pair with marketing-skills for GTM execution and engineering-skills for build."
version: 1.1.0
author: Alireza Rezvani
license: MIT
tags:
  - product
  - product-management
  - ux
  - ui
  - saas
  - agile
agents:
  - claude-code
  - codex-cli
  - openclaw
---

# Product Team Skills

8 production-ready product skills covering product management, UX/UI design, and SaaS development.

## Quick Start

### Claude Code
```
/read product-team/product-manager-toolkit/SKILL.md
```

### Codex CLI
```bash
npx agent-skills-cli add alirezarezvani/claude-skills/product-team
```

## Skills Overview

| Skill | Folder | Focus |
|-------|--------|-------|
| Product Manager Toolkit | `product-manager-toolkit/` | RICE prioritization, customer discovery, PRDs |
| Agile Product Owner | `agile-product-owner/` | User stories, sprint planning, backlog |
| Product Strategist | `product-strategist/` | OKR cascades, market analysis, vision |
| UX Researcher Designer | `ux-researcher-designer/` | Personas, journey maps, usability testing |
| UI Design System | `ui-design-system/` | Design tokens, component docs, responsive |
| Competitive Teardown | `competitive-teardown/` | Systematic competitor analysis |
| Landing Page Generator | `landing-page-generator/` | Conversion-optimized pages |
| SaaS Scaffolder | `saas-scaffolder/` | Production SaaS boilerplate |

## Python Tools

9 scripts, all stdlib-only:

```bash
python3 product-manager-toolkit/scripts/rice_prioritizer.py --help
python3 product-strategist/scripts/okr_cascade_generator.py --help
```

## Rules

- Load only the specific skill SKILL.md you need
- Use Python tools for scoring and analysis, not manual judgment
