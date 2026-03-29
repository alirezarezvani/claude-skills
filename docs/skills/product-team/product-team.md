---
title: "Product Team Skills — Agent Skill for Product Teams"
description: "10 product agent skills and plugins for Claude Code, Codex, Gemini CLI, Cursor, OpenClaw. PM toolkit (RICE), agile PO, product strategist (OKR), UX."
---

# Product Team Skills

<div class="page-meta" markdown>
<span class="meta-badge">:material-lightbulb-outline: Product</span>
<span class="meta-badge">:material-identifier: `product-team`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/product-team/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install product-skills</code>
</div>


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
