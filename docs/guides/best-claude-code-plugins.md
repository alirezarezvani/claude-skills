---
title: "Best Claude Code Plugins & Skills (2026)"
description: "The 20 best Claude Code plugins and agent skills for engineering, marketing, product, and DevOps. Install in one command."
---

# Best Claude Code Plugins & Skills (2026)

Looking for the best Claude Code plugins to supercharge your workflow? This guide covers 20 production-ready plugins and agent skills — from engineering and DevOps to marketing, product management, and C-level advisory.

All plugins listed here are open-source (MIT), tested in production, and installable in one command.

---

## What's the Difference Between Plugins and Skills?

**Claude Code plugins** use the `.claude-plugin/plugin.json` format and install via `/plugin install`. **Agent skills** use `SKILL.md` files and work across Claude Code, Codex, Gemini CLI, Cursor, and 8 other coding agents.

This repo provides **both formats** — every skill includes a `.claude-plugin` directory for native Claude Code plugin support, plus a `SKILL.md` for cross-platform compatibility.

---

## Quick Install

Inside Claude Code:

```text
# Add the marketplace once
/plugin marketplace add alirezarezvani/claude-skills

# Install by domain
/plugin install engineering-skills@claude-code-skills
/plugin install engineering-advanced-skills@claude-code-skills
/plugin install marketing-skills@claude-code-skills

# Install individual plugins
/plugin install autoresearch-agent@claude-code-skills
/plugin install docker-development@claude-code-skills
```

Every plugin and its install command is listed in the [plugin catalogue](../plugins/index.md).

---

## Top 20 Claude Code Plugins

### Engineering & DevOps

| Plugin | What It Does | Install |
|--------|-------------|---------|
| **senior-frontend** | Frontend architecture, React and Next.js components, performance and accessibility. | `/plugin install engineering-skills@claude-code-skills` |
| **pr-review-expert** | Multi-pass code review: logic bugs, security, test coverage, architecture. | `/plugin install engineering-advanced-skills@claude-code-skills` |
| **autoresearch-agent** | Autonomous experiment loop — optimizes any file by a measurable metric. | `/plugin install autoresearch-agent@claude-code-skills` |
| **senior-devops** | Infrastructure as Code, CI/CD pipelines, monitoring, incident response. | `/plugin install engineering-skills@claude-code-skills` |
| **docker-development** | Dockerfile optimization, multi-stage builds, container security scanning. | `/plugin install docker-development@claude-code-skills` |
| **aws-solution-architect** | AWS architecture design with serverless patterns and IaC templates. | `/plugin install engineering-skills@claude-code-skills` |
| **tdd-guide** | Test-driven development workflows with red-green-refactor cycles. | `/plugin install engineering-skills@claude-code-skills` |
| **database-designer** | Schema design, migrations, indexing strategies, query optimization. | `/plugin install engineering-advanced-skills@claude-code-skills` |

### Marketing & Content

| Plugin | What It Does | Install |
|--------|-------------|---------|
| **content-creator** | SEO-optimized content with consistent brand voice and frameworks. | `/plugin install marketing-skills@claude-code-skills` |
| **copywriting** | Marketing copy for landing pages, pricing pages, CTAs. | `/plugin install marketing-skills@claude-code-skills` |
| **email-sequence** | Drip campaigns, nurture sequences, lifecycle email programs. | `/plugin install marketing-skills@claude-code-skills` |
| **app-store-optimization** | ASO keyword research, metadata optimization, A/B testing. | `/plugin install marketing-skills@claude-code-skills` |

### Product & Business

| Plugin | What It Does | Install |
|--------|-------------|---------|
| **research-summarizer** | Structured research → summary → citations for papers and reports. | `/plugin install research-summarizer@claude-code-skills` |
| **agile-product-owner** | User stories, acceptance criteria, sprint planning, velocity tracking. | `/plugin install agile-product-owner@claude-code-skills` |
| **ab-test-setup** | A/B test design, hypothesis creation, statistical significance. | `/plugin install marketing-skills@claude-code-skills` |
| **analytics-tracking** | GA4, GTM, conversion tracking, UTM parameters, tracking plans. | `/plugin install marketing-skills@claude-code-skills` |

### C-Level & Strategy

| Plugin | What It Does | Install |
|--------|-------------|---------|
| **cto-advisor** | Tech debt analysis, team scaling, architecture decisions, DORA metrics. | `/plugin install c-level-skills@claude-code-skills` |
| **ceo-advisor** | Strategy, board governance, investor relations, organizational development. | `/plugin install c-level-skills@claude-code-skills` |
| **cfo-advisor** | Financial modeling, fundraising, burn rate analysis, unit economics. | `/plugin install c-level-skills@claude-code-skills` |
| **marketing-strategy-pmm** | Positioning (April Dunford), GTM strategy, competitive intelligence. | `/plugin install marketing-skills@claude-code-skills` |

---

## Why These Plugins?

Unlike single-purpose plugins, these are **POWERFUL-tier** agent skills — each includes:

- **Structured workflows** with slash commands (not just prompts)
- **Python CLI tools** (254 total, zero pip dependencies)
- **Reference documents** — templates, checklists, domain-specific knowledge
- **Cross-platform support** — works on 11 coding agents, not just Claude Code

---

## Cross-Platform Compatibility

Every plugin in this collection works across multiple AI coding agents:

| Tool | Format | Install Method |
|------|--------|---------------|
| Claude Code | `.claude-plugin` | `/plugin install` |
| OpenAI Codex | `.codex/skills/` | `./scripts/codex-install.sh --category <name>` |
| Gemini CLI | `.gemini/skills/` | `./scripts/gemini-install.sh` |
| Cursor | `.cursor/skills/` | `./scripts/convert.sh --tool cursor` |
| OpenClaw | `clawhub install` | Via ClawHub marketplace |
| Aider, Windsurf, Kilo Code, OpenCode, Augment, Antigravity | Converted formats | `./scripts/convert.sh --tool <name>` |

---

## Related Resources

- [Full Skill Catalog](https://github.com/alirezarezvani/claude-skills) — all {{ count.skills }} skills
- [Agent Skills for Codex](./agent-skills-for-codex.md) — Codex-specific guide
- [Gemini CLI Skills Guide](./gemini-cli-skills-guide.md) — Gemini CLI setup
- [Cursor Skills Guide](./cursor-skills-guide.md) — Cursor integration

---

*Last updated: March 2026 · [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)*
