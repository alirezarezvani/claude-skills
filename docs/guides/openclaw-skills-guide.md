---
title: "OpenClaw Skills Guide — Install & Use Agent Skills (2026)"
description: "Install and use {{ count.skills }} agent skills with OpenClaw. One-line install for engineering, marketing, product, compliance, and DevOps skills in your OpenClaw workspace."
---

# OpenClaw Skills Guide — Install & Use Agent Skills with OpenClaw

> **Skills:** {{ count.skills }} · **Release:** v{{ count.version }}

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

```bash
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills
./scripts/openclaw-install.sh --dry-run   # preview
./scripts/openclaw-install.sh
```

The script symlinks every skill folder into `~/.openclaw/workspace/skills/<skill>/` and skips names that already exist there, so re-running it after `git pull` only adds new skills. Run it from a clone: piping it straight from `curl` does not work, because it locates the skills relative to its own path.

### ClawHub

Individual skills are also published on [ClawHub](https://clawhub.com). Where another publisher already owns a skill's name, ours is published with a `cs-` prefix (for example `cs-copywriting`).

## How Skills Work in OpenClaw

OpenClaw has native skill support — it scans `<available_skills>` in your workspace and auto-selects the right skill for each task.

**Automatic selection:** When you ask your OpenClaw agent to "optimize this Dockerfile," it reads the `docker-development` skill's SKILL.md and follows its workflow. No manual activation needed.

**Named workflows:** Many skills define named workflows (for example, docker-development's `optimize`, `compose` and `security`). Ask for one by name to run it.

**Python tools:** Skills include executable scripts in `scripts/` that your agent can run for analysis, validation, and generation tasks.

## Top OpenClaw Skills by Category

### Engineering
| Skill | What It Does |
|---|---|
| `docker-development` | Dockerfile optimization, multi-stage builds, security hardening |
| `terraform-patterns` | Infrastructure-as-code patterns and module design |
| `ci-cd-pipeline-builder` | CI/CD pipelines generated from your stack |
| `senior-frontend` | Frontend architecture, components and performance |
| `mcp-server-builder` | Build MCP servers for external API integrations |

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

Use the `write-a-skill` skill for guided skill creation:
```
Use write-a-skill to create my-custom-skill
```

## Resources

- **GitHub:** [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)
- **ClawHub:** [clawhub.com](https://clawhub.com)
- **OpenClaw Docs:** [docs.openclaw.ai](https://docs.openclaw.ai)
- **Community:** [Discord](https://discord.com/invite/clawd)

---

*Part of the [Claude Code Skills & Agent Plugins](https://github.com/alirezarezvani/claude-skills) repository — {{ count.skills }} production-ready skills for Claude Code and other coding agents.*
