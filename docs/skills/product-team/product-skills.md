---
title: "Product Skills — Router — Agent Skill for Product Teams"
description: "Router/index for the 12 product skills bundled in this plugin (RICE prioritization, OKRs, UX research, design tokens, competitive teardown. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Product Skills — Router

<div class="page-meta" markdown>
<span class="meta-badge">:material-lightbulb-outline: Product</span>
<span class="meta-badge">:material-identifier: `product-skills`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/product-team/skills/product-skills/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install product-skills</code>
</div>


This plugin bundles **12 product skills** (this router is the 13th folder under `product-team/skills/`). Each skill is self-contained: read its `SKILL.md`, run its `scripts/`, apply its `references/` and `assets/`.

## Routing table

Match the request against the signals below, then load `product-team/skills/<skill>/SKILL.md`. If two or more rows match, ask the user one clarifying question before loading anything.

| Request signals | Skill | Path |
|---|---|---|
| Prioritize features, RICE scores, interview synthesis | product-manager-toolkit | `skills/product-manager-toolkit/` |
| OKRs, strategy cascade, objective alignment | product-strategist | `skills/product-strategist/` |
| Personas, usability findings, research synthesis | ux-researcher-designer | `skills/ux-researcher-designer/` |
| Design tokens, component specs, WCAG contrast | ui-design-system | `skills/ui-design-system/` |
| Competitor analysis, feature/pricing matrix | competitive-teardown | `skills/competitive-teardown/` |
| Retention, cohorts, funnel analysis | product-analytics | `skills/product-analytics/` |
| A/B test design, sample size, hypothesis gates | experiment-designer | `skills/experiment-designer/` |
| Opportunity trees, assumption mapping, discovery | product-discovery | `skills/product-discovery/` |
| Roadmap formats per audience, changelogs | roadmap-communicator | `skills/roadmap-communicator/` |
| Turn a written spec into a repo scaffold | spec-to-repo | `skills/spec-to-repo/` |
| Landing page (Next.js TSX + Tailwind) | landing-page-generator | `skills/landing-page-generator/` |
| Bootstrap a SaaS app skeleton | saas-scaffolder | `skills/saas-scaffolder/` |

## Quick start

```bash
# Example: route a prioritization request
cat product-team/skills/product-manager-toolkit/SKILL.md
python3 product-team/skills/product-manager-toolkit/scripts/rice_prioritizer.py --help
```

## Related product-team plugins (packaged separately, not in this bundle)

- `product-team/agile-product-owner/` — user stories, sprint capacity
- `product-team/code-to-prd/` — reverse-engineer a PRD from a codebase
- `product-team/apple-hig-expert/` — Apple HIG audits (Liquid Glass era)
- `product-team/research-summarizer/` — document summarization with citation extraction

## Rules

- Route to exactly one skill, then follow that skill's own workflow.
- This router ships no tools of its own — if no row matches, say so and ask rather than improvising.
