---
title: "OpenClaw Skills Guide — Install & Use Agent Skills (2026)"
description: "Install and use 345 agent skills with OpenClaw. One-line install for engineering, marketing, product, compliance, and DevOps skills in your OpenClaw workspace."
---

# OpenClaw Skills Guide — Install & Use Agent Skills with OpenClaw

> **Last updated:** June 2026 · **Skills count:** 345 · **Compatibility:** OpenClaw v2024.12+

## What Are OpenClaw Skills?

OpenClaw skills are modular instruction packages that extend your OpenClaw agent with domain expertise — from engineering and DevOps to marketing, compliance, and C-level advisory. Each skill drops into your OpenClaw workspace and works immediately with zero configuration.

Unlike generic prompts, OpenClaw skills include structured workflows, decision frameworks, Python tools, and reference materials that your agent follows autonomously.

## Why Use Skills with OpenClaw?

| Without Skills | With Skills |
|---|---|
| Generic responses | Domain-expert-level outputs |
| Manual prompt engineering | Pre-built workflows with slash commands |
| No tooling | Python scripts for analysis, validation, formatting |
| Starts from scratch | References, templates, best practices included |

OpenClaw's skill system is the most natural fit in the ecosystem — skills live in your workspace directory and are automatically loaded based on task context.

## Installation

### Quick Install (Recommended)

```bash
bash <(curl -s https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/scripts/openclaw-install.sh)
```

This installs all 345 skills into your OpenClaw workspace with the correct directory structure.

### Manual Install

```bash
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills
./scripts/install.sh --tool openclaw
```

### Install Specific Skill Packs

```bash
# Engineering (49 skills)
./scripts/install.sh --tool openclaw --pack engineering

# Marketing (43 skills)
./scripts/install.sh --tool openclaw --pack marketing

# Product (12 skills)
./scripts/install.sh --tool openclaw --pack product

# C-Level Advisory (28 skills)
./scripts/install.sh --tool openclaw --pack c-level

# Regulatory & Quality (12 skills)
./scripts/install.sh --tool openclaw --pack regulatory
```

### ClawHub Install

If you have the ClawHub CLI:

```bash
clawhub install alirezarezvani/claude-skills
```

## How Skills Work in OpenClaw

OpenClaw has native skill support — it scans `<available_skills>` in your workspace and auto-selects the right skill for each task.

**Automatic selection:** When you ask your OpenClaw agent to "optimize this Dockerfile," it reads the `docker-development` skill's SKILL.md and follows its workflow. No manual activation needed.

**Slash commands:** Each skill defines slash commands (e.g., `/docker:optimize`, `/research:summarize`) that trigger specific workflows.

**Python tools:** Skills include executable scripts in `scripts/` that your agent can run for analysis, validation, and generation tasks.

## Top OpenClaw Skills by Category

### Engineering
| Skill | What It Does |
|---|---|
| `docker-development` | Dockerfile optimization, multi-stage builds, security hardening |
| `terraform-patterns` | Infrastructure-as-code patterns and module design |
| `github` | PR workflows, CI/CD, code review automation |
| `frontend-design` | Production-grade UI components with high design quality |
| `mcp-builder` | Build MCP servers for external API integrations |

### Marketing & Content
| Skill | What It Does |
|---|---|
| `content-creator` | SEO-optimized blog posts, social media, brand voice |
| `copywriting` | Landing pages, headlines, CTAs, product copy |
| `email-sequence` | Drip campaigns, onboarding flows, lifecycle emails |
| `launch-strategy` | Product launches, Product Hunt, feature announcements |
| `competitor-alternatives` | Comparison pages, vs pages, alternative pages |

### Product & Research
| Skill | What It Does |
|---|---|
| `research-summarizer` | Academic papers, articles, structured briefs with citations |
| `agile-product-owner` | User stories, sprint planning, backlog management |
| `ab-test-setup` | Experiment design, hypothesis testing, variant analysis |

### C-Level Advisory
| Skill | What It Does |
|---|---|
| `ceo-advisor` | Strategy, board prep, investor relations |
| `cto-advisor` | Tech debt, team scaling, architecture decisions |
| `cfo-advisor` | Financial modeling, fundraising, burn rate analysis |

## OpenClaw vs Other Platforms

| Feature | OpenClaw | Claude Code | Cursor | Codex |
|---|---|---|---|---|
| Native skill loading | ✅ Automatic | ✅ Manual | ⚠️ Rules only | ⚠️ Instructions |
| Slash commands | ✅ | ✅ | ❌ | ❌ |
| Python tool execution | ✅ | ✅ | ❌ | ✅ |
| Multi-agent delegation | ✅ Built-in | ❌ | ❌ | ❌ |
| Persistent memory | ✅ | ⚠️ Session | ❌ | ❌ |
| Cron/scheduled tasks | ✅ | ❌ | ❌ | ❌ |

OpenClaw's architecture — persistent agents, memory, cron jobs, and multi-channel messaging — makes it the most capable platform for running agent skills autonomously.

## Skill Anatomy

Every skill in the repository follows the same structure:

```
skill-name/
├── SKILL.md              # Instructions, workflows, slash commands
├── .claude-plugin/
│   └── plugin.json       # Metadata for plugin registries
├── scripts/
│   ├── tool_one.py       # Executable Python tools
│   └── tool_two.py
└── references/
    ├── patterns.md       # Domain knowledge, templates
    └── best-practices.md
```

## Creating Custom OpenClaw Skills

You can create your own skills following the same format:

1. Create a directory under your workspace skills folder
2. Write a `SKILL.md` with description, slash commands, and workflows
3. Add Python scripts in `scripts/` for any automation
4. Add reference materials in `references/`
5. OpenClaw will auto-discover and use your skill

Use the `skill-creator` meta-skill for guided skill creation:
```
/skill:create my-custom-skill
```

## Resources

- **GitHub:** [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)
- **ClawHub:** [clawhub.com](https://clawhub.com)
- **OpenClaw Docs:** [docs.openclaw.ai](https://docs.openclaw.ai)
- **Community:** [Discord](https://discord.com/invite/clawd)

---

*Part of the [Claude Code Skills & Agent Plugins](https://github.com/alirezarezvani/claude-skills) repository — 345 production-ready skills for 13 AI coding tools.*
