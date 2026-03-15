---
title: "Agent Skills for OpenAI Codex CLI (2026)"
description: "Install and use 192 agent skills with OpenAI Codex CLI. Engineering, marketing, product, and DevOps plugins for Codex."
---

# Agent Skills for OpenAI Codex CLI

Use 192 production-ready agent skills with OpenAI Codex CLI. Every skill in this collection works natively with Codex via the `.codex/skills/` directory format.

---

## Quick Install

```bash
# Clone the repository
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills

# Option 1: Install all skills for Codex
./scripts/codex-install.sh

# Option 2: Convert specific skills
./scripts/convert.sh --skill frontend-design --tool codex
./scripts/convert.sh --skill autoresearch-agent --tool codex

# Option 3: Convert all skills at once
./scripts/convert.sh --all --tool codex
```

### How It Works

Codex reads agent skills from `.codex/skills/<skill-name>/SKILL.md` in your project or home directory. The `convert.sh` script transforms Claude Code's SKILL.md format into Codex-compatible instructions, preserving all workflows, slash commands, and references.

---

## Top Skills for Codex Users

### Engineering

| Skill | Codex Command | What It Does |
|-------|--------------|-------------|
| **autoresearch-agent** | `/ar:run` | Autonomous experiment loop — edit, evaluate, keep or revert. Karpathy-inspired. |
| **pr-review-expert** | `/review:full` | Multi-pass code review catching logic bugs, security issues, missing tests. |
| **frontend-design** | `/design:component` | Production-grade React/Tailwind UI with high design quality. |
| **tdd-guide** | `/tdd:start` | Red-green-refactor TDD workflow with coverage tracking. |
| **senior-devops** | `/devops:deploy` | IaC, CI/CD, monitoring, and incident response playbooks. |
| **docker-development** | `/docker:optimize` | Dockerfile optimization, multi-stage builds, container security. |

### Beyond Engineering

| Skill | Codex Command | What It Does |
|-------|--------------|-------------|
| **content-creator** | `/content:write` | SEO-optimized content with brand voice analysis. |
| **cto-advisor** | `/cto:assess` | Tech debt scoring, team scaling, architecture decisions. |
| **agile-product-owner** | `/po:story` | User stories, acceptance criteria, sprint planning. |
| **research-summarizer** | `/research:summarize` | Structured research → summary → citations workflow. |

---

## Codex-Specific Tips

### AGENTS.md Fallback

If your Codex setup uses `AGENTS.md` instead of the skills directory, you can use the generated agents file:

```bash
# Copy the bundled AGENTS.md to your project
cp claude-skills/agents/AGENTS.md ~/.codex/AGENTS.md
```

### Using with `--full-auto`

Skills work seamlessly with Codex's auto-approval mode:

```bash
# Run a skill in full-auto mode
codex exec --full-auto "Use the frontend-design skill to build a dashboard component"

# Run autoresearch overnight
codex exec --full-auto "Use autoresearch-agent to optimize src/api/search.py for response time"
```

### Project-Level vs Global

```bash
# Project-level (only this repo)
cp -r claude-skills/.codex/skills/ ./.codex/skills/

# Global (available everywhere)
cp -r claude-skills/.codex/skills/ ~/.codex/skills/
```

---

## Full Skill Catalog

All 192 skills organized by domain:

| Domain | Skills | Highlights |
|--------|--------|-----------|
| **Engineering** | 28 | autoresearch-agent, pr-review-expert, database-designer, migration-architect |
| **Engineering Team** | 15 | senior-frontend, senior-backend, senior-devops, senior-security, senior-qa |
| **Marketing** | 22 | content-creator, copywriting, email-sequence, SEO audit, app-store-optimization |
| **Product** | 12 | agile-product-owner, ux-researcher, research-summarizer, analytics-tracking |
| **Business Growth** | 10 | launch-strategy, competitor-alternatives, free-tool-strategy |
| **C-Level Advisory** | 8 | cto-advisor, ceo-advisor, cfo-advisor, marketing-strategy-pmm |
| **Finance** | 6 | financial modeling, fundraising, unit economics |
| **Compliance** | 8 | ISO 27001, ISO 13485, MDR, FDA, GDPR |
| **Project Management** | 5 | Jira expert, sprint planning, retrospective facilitator |

---

## Cross-Platform

These same skills work on 10 other coding agents:

Claude Code · Gemini CLI · Cursor · OpenClaw · Aider · Windsurf · Kilo Code · OpenCode · Augment · Antigravity

See the [full README](https://github.com/alirezarezvani/claude-skills) for platform-specific install guides.

---

*Last updated: March 2026 · [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)*
