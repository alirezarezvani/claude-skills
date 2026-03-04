# Claude Skills Library

**86 production-ready skill packages for Claude Code, OpenAI Codex, and OpenClaw** — reusable expertise bundles that transform AI agents into specialized professionals across engineering, product, marketing, compliance, and more.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skills](https://img.shields.io/badge/Skills-86-brightgreen.svg)](#skills-overview)
[![Stars](https://img.shields.io/github/stars/alirezarezvani/claude-skills?style=flat)](https://github.com/alirezarezvani/claude-skills/stargazers)
[![SkillCheck Validated](https://img.shields.io/badge/SkillCheck-Validated-4c1)](https://getskillcheck.com)

> ⭐ **2,300+ GitHub stars** — the most comprehensive open-source skill library for AI coding agents.

---

## What Is This?

Skills are modular instruction packages that give AI agents domain expertise they don't have out of the box. Each skill includes a `SKILL.md` (instructions + workflows), Python CLI tools, and reference documentation — everything the agent needs to perform like a specialist.

**One repo, three platforms:** Works natively with Claude Code, OpenAI Codex, and OpenClaw.

---

## Quick Install

### Claude Code (Recommended)

```bash
# Add the marketplace
/plugin marketplace add alirezarezvani/claude-skills

# Install by domain
/plugin install engineering-skills@claude-code-skills          # 21 core engineering
/plugin install engineering-advanced-skills@claude-code-skills  # 25 POWERFUL-tier
/plugin install product-skills@claude-code-skills               # 8 product skills
/plugin install marketing-skills@claude-code-skills             # 7 marketing skills
/plugin install ra-qm-skills@claude-code-skills                 # 12 regulatory/quality
/plugin install pm-skills@claude-code-skills                    # 6 project management
/plugin install c-level-skills@claude-code-skills               # 2 C-level advisory
/plugin install business-growth-skills@claude-code-skills       # 4 business & growth
/plugin install finance-skills@claude-code-skills               # 1 finance

# Or install individual skills
/plugin install skill-security-auditor@claude-code-skills       # Security scanner
/plugin install content-creator@claude-code-skills              # Single skill
```

### OpenAI Codex

```bash
npx agent-skills-cli add alirezarezvani/claude-skills --agent codex
# Or: git clone + ./scripts/codex-install.sh
```

### OpenClaw

```bash
bash <(curl -s https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/scripts/openclaw-install.sh)
```

### Manual Installation

```bash
git clone https://github.com/alirezarezvani/claude-skills.git
# Copy any skill folder to ~/.claude/skills/ (Claude Code) or ~/.codex/skills/ (Codex)
```

---

## Skills Overview

**86 skills across 9 domains:**

| Domain | Skills | Highlights | Details |
|--------|--------|------------|---------|
| **🔧 Engineering — Core** | 21 | Architecture, frontend, backend, fullstack, QA, DevOps, SecOps, AI/ML, data | [engineering-team/](engineering-team/) |
| **⚡ Engineering — POWERFUL** | 25 | Agent designer, RAG architect, database designer, CI/CD builder, security auditor, MCP builder | [engineering/](engineering/) |
| **🎯 Product** | 8 | Product manager, agile PO, strategist, UX researcher, UI design, landing pages, SaaS scaffolder | [product-team/](product-team/) |
| **📣 Marketing** | 7 | Content creator, demand gen, PMM strategy, ASO, social media, campaign analytics, prompt engineering | [marketing-skill/](marketing-skill/) |
| **📋 Project Management** | 6 | Senior PM, scrum master, Jira, Confluence, Atlassian admin, templates | [project-management/](project-management/) |
| **🏥 Regulatory & QM** | 12 | ISO 13485, MDR 2017/745, FDA, ISO 27001, GDPR, CAPA, risk management | [ra-qm-team/](ra-qm-team/) |
| **💼 C-Level Advisory** | 2 | CEO advisor, CTO advisor | [c-level-advisor/](c-level-advisor/) |
| **📈 Business & Growth** | 4 | Customer success, sales engineer, revenue ops, contracts & proposals | [business-growth/](business-growth/) |
| **💰 Finance** | 1 | Financial analyst (DCF, budgeting, forecasting) | [finance/](finance/) |

---

## ⚡ POWERFUL Tier

25 advanced skills with deep, production-grade capabilities:

| Skill | What It Does |
|-------|-------------|
| **agent-designer** | Multi-agent orchestration, tool schemas, performance evaluation |
| **agent-workflow-designer** | Sequential, parallel, router, orchestrator, and evaluator patterns |
| **rag-architect** | RAG pipeline builder, chunking optimizer, retrieval evaluator |
| **database-designer** | Schema analyzer, ERD generation, index optimizer, migration generator |
| **database-schema-designer** | Requirements → migrations, types, seed data, RLS policies |
| **migration-architect** | Migration planner, compatibility checker, rollback generator |
| **skill-security-auditor** | 🔒 Security gate — scan skills for malicious code before installation |
| **ci-cd-pipeline-builder** | Analyze stack → generate GitHub Actions / GitLab CI configs |
| **mcp-server-builder** | Build MCP servers from OpenAPI specs |
| **pr-review-expert** | Blast radius analysis, security scan, coverage delta |
| **api-design-reviewer** | REST API linter, breaking change detector, design scorecard |
| **api-test-suite-builder** | Scan API routes → generate complete test suites |
| **dependency-auditor** | Multi-language scanner, license compliance, upgrade planner |
| **release-manager** | Changelog generator, semantic version bumper, readiness checker |
| **observability-designer** | SLO designer, alert optimizer, dashboard generator |
| **performance-profiler** | Node/Python/Go profiling, bundle analysis, load testing |
| **monorepo-navigator** | Turborepo/Nx/pnpm workspace management & impact analysis |
| **changelog-generator** | Conventional commits → structured changelogs |
| **codebase-onboarding** | Auto-generate onboarding docs from codebase analysis |
| **runbook-generator** | Codebase → operational runbooks with commands |
| **git-worktree-manager** | Parallel dev with port isolation, env sync |
| **env-secrets-manager** | .env management, leak detection, rotation workflows |
| **incident-commander** | Incident response playbook, severity classifier, PIR generator |
| **tech-debt-tracker** | Codebase debt scanner, prioritizer, trend dashboard |
| **interview-system-designer** | Interview loop designer, question bank, calibrator |

---

## 🔒 Skill Security Auditor

New in v2.0.0 — audit any skill for security risks before installation:

```bash
python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py /path/to/skill/
```

Scans for: command injection, code execution, data exfiltration, prompt injection, dependency supply chain risks, privilege escalation. Returns **PASS / WARN / FAIL** with remediation guidance.

**Zero dependencies.** Works anywhere Python runs.

---

## Recently Enhanced Skills

Production-quality upgrades added for:

- `engineering/git-worktree-manager` — worktree lifecycle + cleanup automation scripts
- `engineering/mcp-server-builder` — OpenAPI -> MCP scaffold + manifest validator
- `engineering/changelog-generator` — release note generator + conventional commit linter
- `engineering/ci-cd-pipeline-builder` — stack detector + pipeline generator
- `marketing-skill/prompt-engineer-toolkit` — prompt A/B tester + prompt version/diff manager

Each now ships with `scripts/`, extracted `references/`, and a usage-focused `README.md`.

---

## Usage Examples

### Architecture Review
```
Using the senior-architect skill, review our microservices architecture
and identify the top 3 scalability risks.
```

### Content Creation
```
Using the content-creator skill, write a blog post about AI-augmented
development. Optimize for SEO targeting "Claude Code tutorial".
```

### Compliance Audit
```
Using the mdr-745-specialist skill, review our technical documentation
for MDR Annex II compliance gaps.
```

---

## Python Analysis Tools

92+ CLI tools ship with the skills:

```bash
# Brand voice analysis
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py article.txt

# Tech debt scoring
python3 c-level-advisor/cto-advisor/scripts/tech_debt_analyzer.py /path/to/codebase

# RICE prioritization
python3 product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv

# Security audit
python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py /path/to/skill/
```

---

## Related Projects

| Project | Description |
|---------|-------------|
| [**Claude Code Skills & Agents Factory**](https://github.com/alirezarezvani/claude-code-skills-agents-factory) | Methodology for building skills at scale |
| [**Claude Code Tresor**](https://github.com/alirezarezvani/claude-code-tresor) | Productivity toolkit with 60+ prompt templates |

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Quick ideas:**
- Add new skills in underserved domains
- Improve existing Python tools
- Add test coverage for scripts
- Translate skills for non-English markets

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=alirezarezvani/claude-skills&type=Date)](https://star-history.com/#alirezarezvani/claude-skills&Date)

---

**Built by [Alireza Rezvani](https://alirezarezvani.com)** · [Medium](https://alirezarezvani.medium.com) · [Twitter](https://twitter.com/nginitycloud)
