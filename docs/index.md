---
title: Claude Code Skills & Plugins - Documentation
description: "169 production-ready skills and plugins for Claude Code, OpenAI Codex, and OpenClaw. Reusable expertise bundles for engineering, product, marketing, compliance, and more."
---

# Claude Code Skills & Plugins

**169 production-ready skills** that transform AI coding agents into specialized professionals across engineering, product, marketing, compliance, and more.

Works natively with **Claude Code**, **OpenAI Codex**, and **OpenClaw**.

---

## Quick Install

```bash
# Add the marketplace
/plugin marketplace add alirezarezvani/claude-skills

# Install by domain
/plugin install engineering-skills@claude-code-skills          # 23 core engineering
/plugin install engineering-advanced-skills@claude-code-skills  # 25 POWERFUL-tier
/plugin install product-skills@claude-code-skills               # 8 product skills
/plugin install marketing-skills@claude-code-skills             # 42 marketing skills
/plugin install ra-qm-skills@claude-code-skills                 # 12 regulatory/quality
/plugin install pm-skills@claude-code-skills                    # 6 project management
/plugin install c-level-skills@claude-code-skills               # 28 C-level advisory
/plugin install business-growth-skills@claude-code-skills       # 4 business & growth
/plugin install finance-skills@claude-code-skills               # 1 finance
```

---

## Skills by Domain

| Domain | Skills | Highlights |
|--------|--------|------------|
| [**Engineering - Core**](skills/engineering-team/) | 23 | Architecture, frontend, backend, fullstack, QA, DevOps, SecOps, AI/ML, data, Playwright, self-improving agent |
| [**Engineering - POWERFUL**](skills/engineering/) | 25 | Agent designer, RAG architect, database designer, CI/CD builder, security auditor, MCP builder |
| [**Product**](skills/product-team/) | 8 | Product manager, agile PO, strategist, UX researcher, UI design, landing pages, SaaS scaffolder |
| [**Marketing**](skills/marketing-skill/) | 42 | Content, SEO, CRO, Channels, Growth, Intelligence, Sales pods with 27 Python tools |
| [**Project Management**](skills/project-management/) | 6 | Senior PM, scrum master, Jira, Confluence, Atlassian admin |
| [**C-Level Advisory**](skills/c-level-advisor/) | 28 | Full C-suite (10 roles) + orchestration + board meetings + culture |
| [**Regulatory & Quality**](skills/ra-qm-team/) | 12 | ISO 13485, MDR 2017/745, FDA, ISO 27001, GDPR, CAPA, risk management |
| [**Business & Growth**](skills/business-growth/) | 4 | Customer success, sales engineer, revenue ops, contracts & proposals |
| [**Finance**](skills/finance/) | 1 | Financial analyst (DCF, budgeting, forecasting) |

---

## Key Features

- **160+ Python CLI tools** — all stdlib-only, zero pip installs required
- **250+ reference guides** — embedded domain expertise
- **Plugin marketplace** — one-command install for any skill bundle
- **Multi-platform** — Claude Code, OpenAI Codex, OpenClaw
- **Security auditor** — scan skills for malicious code before installation
- **Self-improving agent** — auto-memory curation and pattern promotion

---

## How Skills Work

Each skill is a self-contained package:

```
skill-name/
  SKILL.md       # Instructions + workflows
  scripts/       # Python CLI tools
  references/    # Expert knowledge bases
  assets/        # Templates
```

Knowledge flows from `references/` into `SKILL.md` workflows, executed via `scripts/`, applied using `assets/` templates.

---

## Links

- [GitHub Repository](https://github.com/alirezarezvani/claude-skills)
- [Getting Started](getting-started.md)
- [Contributing](https://github.com/alirezarezvani/claude-skills/blob/main/CONTRIBUTING.md)
- [Skills & Agents Factory](https://github.com/alirezarezvani/claude-code-skills-agents-factory) — methodology for building skills at scale
- [Claude Code Tresor](https://github.com/alirezarezvani/claude-code-tresor) — productivity toolkit with 60+ prompt templates

---

**Built by [Alireza Rezvani](https://alirezarezvani.com)** | [Medium](https://alirezarezvani.medium.com) | [Twitter](https://twitter.com/nginitycloud)
