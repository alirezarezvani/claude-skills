---
title: "Gemini CLI Skills & Plugins Guide (2026)"
description: "Install and use 192 agent skills with Gemini CLI. Free evaluation calls, engineering, marketing, and DevOps skills for Google's coding agent."
---

# Gemini CLI Agent Skills Guide

Use 192 production-ready agent skills with Gemini CLI. Every skill in this collection is compatible with Gemini's agent skills specification and installs via the `.gemini/skills/` directory.

---

## Quick Install

```bash
# Clone the repository
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills

# Run the Gemini setup script (converts and installs all skills)
./scripts/gemini-install.sh

# Or convert individual skills
./scripts/convert.sh --skill frontend-design --tool gemini
./scripts/convert.sh --skill autoresearch-agent --tool gemini
```

### How It Works

Gemini CLI reads agent skills from `.gemini/skills/<skill-name>/SKILL.md` in your project directory. The setup script converts all skills to Gemini-compatible format, including `gemini-extension.json` for the extension registry.

---

## Why Use Skills with Gemini CLI?

Gemini CLI's free tier gives you **unlimited evaluation calls** — perfect for:

- **Autoresearch loops** — run overnight experiments with zero API cost
- **Content optimization** — LLM-judge evaluators for headlines, copy, prompts
- **Code review** — systematic multi-pass reviews without burning tokens

### Free Evaluators with Gemini

The autoresearch-agent skill includes LLM judge evaluators that work with Gemini's free tier:

```bash
# Set up an autoresearch experiment using Gemini as the evaluator
python scripts/setup_experiment.py \
  --domain marketing \
  --name headline-optimization \
  --target content/headlines.md \
  --eval "python evaluate.py" \
  --metric ctr_score \
  --direction higher \
  --evaluator llm_judge_content

# The evaluator calls gemini CLI for scoring — free!
```

---

## Top Skills for Gemini CLI

| Skill | What It Does |
|-------|-------------|
| **autoresearch-agent** | Autonomous experiment loop — edit, evaluate, keep or revert. Free with Gemini. |
| **frontend-design** | Production-grade React/Tailwind UI with high design quality. |
| **pr-review-expert** | Multi-pass code review: logic, security, tests, architecture. |
| **content-creator** | SEO-optimized content with brand voice analysis and frameworks. |
| **senior-devops** | IaC, CI/CD, monitoring, and incident response. |
| **cto-advisor** | Tech debt analysis, team scaling, architecture decisions. |
| **research-summarizer** | Structured research → summary → citations workflow. |
| **docker-development** | Dockerfile optimization, multi-stage builds, security scanning. |

---

## Gemini Extension Integration

This repo includes `gemini-extension.json` for Gemini's extension registry:

```json
{
  "name": "claude-skills",
  "version": "2.0.0",
  "description": "192 agent skills for engineering, marketing, product, and more",
  "skills": ["engineering/*", "marketing-skill/*", "product-team/*", "..."]
}
```

See the [Gemini CLI extensions docs](https://geminicli.com/docs/cli/skills/) for integration details.

---

## Project-Level vs User-Level

```bash
# Project-level (scoped to one repo)
cp -r claude-skills/.gemini/skills/ ./.gemini/skills/

# User-level (available in all projects)
mkdir -p ~/.gemini/skills/
cp -r claude-skills/.gemini/skills/* ~/.gemini/skills/
```

---

## Cross-Platform

These skills work on 10 other coding agents too:

Claude Code · OpenAI Codex · Cursor · OpenClaw · Aider · Windsurf · Kilo Code · OpenCode · Augment · Antigravity

See the [full catalog](https://github.com/alirezarezvani/claude-skills) for all 192 skills.

---

*Last updated: March 2026 · [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)*
