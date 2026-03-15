---
title: "Cursor Agent Skills & Rules Guide (2026)"
description: "Install and use 192 agent skills with Cursor IDE. Engineering, marketing, and product plugins for Cursor's AI coding agent."
---

# Cursor Agent Skills Guide

Use 192 production-ready agent skills with Cursor IDE. Every skill converts to Cursor's rules format and installs via the `.cursor/skills/` directory.

---

## Quick Install

```bash
# Clone the repository
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills

# Convert all skills to Cursor format
./scripts/convert.sh --all --tool cursor

# Or convert individual skills
./scripts/convert.sh --skill frontend-design --tool cursor
./scripts/convert.sh --skill pr-review-expert --tool cursor
```

### How It Works

Cursor reads agent rules from `.cursor/rules/` and `.cursorrules` files. The convert script transforms SKILL.md files into Cursor-compatible rule sets, preserving workflows, decision frameworks, and domain knowledge.

---

## Top Skills for Cursor Users

| Skill | What It Does | Best For |
|-------|-------------|----------|
| **frontend-design** | Production-grade UI with React, Tailwind, shadcn/ui. | Building polished interfaces |
| **pr-review-expert** | Multi-pass code review catching logic, security, and test gaps. | Code quality |
| **senior-fullstack** | Full-stack patterns: API design, auth, state management. | Application architecture |
| **tdd-guide** | Test-driven development with red-green-refactor. | Writing tests first |
| **content-creator** | SEO-optimized content with brand voice frameworks. | Marketing content |
| **agile-product-owner** | User stories, acceptance criteria, sprint planning. | Product work |
| **cto-advisor** | Tech debt analysis, team scaling, architecture decisions. | Technical leadership |
| **database-designer** | Schema design, migrations, indexing, query optimization. | Database work |

---

## Cursor-Specific Integration

### Using with Cursor's Subagents

Cursor's multi-model subagent system works well with skills:

```
# In Cursor's Composer, reference a skill:
@skill frontend-design Build a dashboard with charts and data tables

# Or use slash commands from the skill:
/design:component Create a pricing card with toggle for monthly/annual
```

### Project Rules

Add skills to your `.cursorrules` for project-wide availability:

```bash
# Append skill instructions to cursor rules
cat .cursor/skills/frontend-design/SKILL.md >> .cursorrules
```

---

## Full Catalog

All 192 skills across 9 domains. See the [full README](https://github.com/alirezarezvani/claude-skills) for the complete list.

**Also works with:** Claude Code · OpenAI Codex · Gemini CLI · OpenClaw · Aider · Windsurf · Kilo Code · OpenCode · Augment · Antigravity

---

*Last updated: March 2026 · [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)*
