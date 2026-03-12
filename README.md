# Claude Code Skills & Plugins

**177 production-ready skills, 16 agents, 3 personas, and an orchestration protocol for 11 AI coding tools.**

Reusable expertise packages that give AI coding agents domain knowledge they don't have out of the box — from architecture and security to marketing, compliance, and C-level advisory.

**Works with:** Claude Code · OpenAI Codex · Gemini CLI · OpenClaw · Cursor · Aider · Windsurf · Kilo Code · OpenCode · Augment · Antigravity

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Skills](https://img.shields.io/badge/Skills-177-brightgreen?style=for-the-badge)](#skills-overview)
[![Agents](https://img.shields.io/badge/Agents-16-blue?style=for-the-badge)](#agents)
[![Personas](https://img.shields.io/badge/Personas-3-purple?style=for-the-badge)](#personas)
[![Commands](https://img.shields.io/badge/Commands-17-orange?style=for-the-badge)](#commands)
[![Stars](https://img.shields.io/github/stars/alirezarezvani/claude-skills?style=for-the-badge)](https://github.com/alirezarezvani/claude-skills/stargazers)
[![SkillCheck Validated](https://img.shields.io/badge/SkillCheck-Validated-4c1?style=for-the-badge)](https://getskillcheck.com)

> **4,400+ GitHub stars** — the most comprehensive open-source skill library for AI coding agents.

---

## What Are Skills?

Skills are modular instruction packages that give AI coding agents domain expertise they don't have out of the box. Each skill includes:

- **SKILL.md** — structured instructions, workflows, and decision frameworks
- **Python tools** — 254 CLI scripts (all stdlib-only, zero pip installs)
- **Reference docs** — templates, checklists, and domain-specific knowledge

**One repo, eleven platforms.** Works natively with Claude Code, and converts to 10 other tools via `scripts/convert.sh`. All 254 Python tools run anywhere Python runs.

### Skills vs Agents vs Personas

| | Skills | Agents | Personas |
|---|---|---|---|
| **Purpose** | How to execute a task | What task to do | Who is thinking |
| **Scope** | Single domain | Single domain | Cross-domain |
| **Voice** | Neutral | Professional | Personality-driven |
| **Example** | "Follow these steps for SEO" | "Run a security audit" | "Think like a startup CTO" |

All three work together. See [Orchestration](#orchestration) for how to combine them.

---

## Quick Install

### Gemini CLI (New)

```bash
# Clone the repository
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills

# Run the setup script
./scripts/gemini-install.sh

# Start using skills
> activate_skill(name="senior-architect")
```

### Claude Code (Recommended)

```bash
# Add the marketplace
/plugin marketplace add alirezarezvani/claude-skills

# Install by domain
/plugin install engineering-skills@claude-code-skills          # 24 core engineering
/plugin install engineering-advanced-skills@claude-code-skills  # 25 POWERFUL-tier
/plugin install product-skills@claude-code-skills               # 12 product skills
/plugin install marketing-skills@claude-code-skills             # 43 marketing skills
/plugin install ra-qm-skills@claude-code-skills                 # 12 regulatory/quality
/plugin install pm-skills@claude-code-skills                    # 6 project management
/plugin install c-level-skills@claude-code-skills               # 28 C-level advisory (full C-suite)
/plugin install business-growth-skills@claude-code-skills       # 4 business & growth
/plugin install finance-skills@claude-code-skills               # 2 finance (analyst + SaaS metrics)

# Or install individual skills
/plugin install skill-security-auditor@claude-code-skills       # Security scanner
/plugin install playwright-pro@claude-code-skills                  # Playwright testing toolkit
/plugin install self-improving-agent@claude-code-skills         # Auto-memory curation
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

## Multi-Tool Support (New)

**Convert all 156 skills to 7 AI coding tools** with a single script:

| Tool | Format | Install |
|------|--------|---------|
| **Cursor** | `.mdc` rules | `./scripts/install.sh --tool cursor --target .` |
| **Aider** | `CONVENTIONS.md` | `./scripts/install.sh --tool aider --target .` |
| **Kilo Code** | `.kilocode/rules/` | `./scripts/install.sh --tool kilocode --target .` |
| **Windsurf** | `.windsurf/skills/` | `./scripts/install.sh --tool windsurf --target .` |
| **OpenCode** | `.opencode/skills/` | `./scripts/install.sh --tool opencode --target .` |
| **Augment** | `.augment/rules/` | `./scripts/install.sh --tool augment --target .` |
| **Antigravity** | `~/.gemini/antigravity/skills/` | `./scripts/install.sh --tool antigravity` |

**How it works:**

```bash
# 1. Convert all skills to all tools (takes ~15 seconds)
./scripts/convert.sh --tool all

# 2. Install into your project (with confirmation)
./scripts/install.sh --tool cursor --target /path/to/project

# Or use --force to skip confirmation:
./scripts/install.sh --tool aider --target . --force

# 3. Verify
find .cursor/rules -name "*.mdc" | wc -l  # Should show 156
```

**Each tool gets:**
- ✅ All 156 skills converted to native format
- ✅ Per-tool README with install/verify/update steps
- ✅ Support for scripts, references, templates where applicable
- ✅ Zero manual conversion work

See [integrations/](integrations/) for tool-specific documentation and pre-generated outputs.

---

## Skills Overview

**177 skills across 9 domains:**

| Domain | Skills | Highlights | Details |
|--------|--------|------------|---------|
| **🔧 Engineering — Core** | 24 | Architecture, frontend, backend, fullstack, QA, DevOps, SecOps, AI/ML, data, Playwright, self-improving agent, Google Workspace CLI | [engineering-team/](engineering-team/) |
| **🎭 Playwright Pro** | 9+3 | Test generation, flaky fix, Cypress/Selenium migration, TestRail, BrowserStack, 55 templates | [engineering-team/playwright-pro](engineering-team/playwright-pro/) |
| **🧠 Self-Improving Agent** | 5+2 | Auto-memory curation, pattern promotion, skill extraction, memory health | [engineering-team/self-improving-agent](engineering-team/self-improving-agent/) |
| **⚡ Engineering — POWERFUL** | 25 | Agent designer, RAG architect, database designer, CI/CD builder, security auditor, MCP builder | [engineering/](engineering/) |
| **🎯 Product** | 12 | Product manager, agile PO, strategist, UX researcher, UI design, landing pages, SaaS scaffolder, analytics, experiment designer, discovery, roadmap communicator | [product-team/](product-team/) |
| **📣 Marketing** | 43 | 7 pods: Content (8), SEO (5), CRO (6), Channels (6), Growth (4), Intelligence (4), Sales (2) + context foundation + orchestration router. 32 Python tools. | [marketing-skill/](marketing-skill/) |
| **📋 Project Management** | 6 | Senior PM, scrum master, Jira, Confluence, Atlassian admin, templates | [project-management/](project-management/) |
| **🏥 Regulatory & QM** | 12 | ISO 13485, MDR 2017/745, FDA, ISO 27001, GDPR, CAPA, risk management | [ra-qm-team/](ra-qm-team/) |
| **💼 C-Level Advisory** | 28 | Full C-suite (10 roles) + orchestration + board meetings + culture & collaboration | [c-level-advisor/](c-level-advisor/) |
| **📈 Business & Growth** | 4 | Customer success, sales engineer, revenue ops, contracts & proposals | [business-growth/](business-growth/) |
| **💰 Finance** | 2 | Financial analyst (DCF, budgeting, forecasting), SaaS metrics coach (ARR, MRR, churn, LTV, CAC) | [finance/](finance/) |

---

## Personas

Pre-configured agent identities with curated skill loadouts, workflows, and distinct communication styles. Personas go beyond "use these skills" — they define how an agent thinks, prioritizes, and communicates.

| Persona | Domain | Best For |
|---------|--------|----------|
| [**Startup CTO**](agents/personas/startup-cto.md) | Engineering + Strategy | Architecture decisions, tech stack selection, team building, technical due diligence |
| [**Growth Marketer**](agents/personas/growth-marketer.md) | Marketing + Growth | Content-led growth, launch strategy, channel optimization, bootstrapped marketing |
| [**Solo Founder**](agents/personas/solo-founder.md) | Cross-domain | One-person startups, side projects, MVP building, wearing all hats |

**Usage:**
```bash
# Claude Code
cp agents/personas/startup-cto.md ~/.claude/agents/

# Any tool
./scripts/convert.sh --tool cursor  # Converts personas too
```

See [agents/personas/](agents/personas/) for details. Create your own with [TEMPLATE.md](agents/personas/TEMPLATE.md).

---

## Orchestration

A lightweight protocol for coordinating personas, skills, and agents on work that crosses domain boundaries. No framework required.

**Four patterns:**

| Pattern | What | When |
|---------|------|------|
| **Solo Sprint** | Switch personas across project phases | Side projects, MVPs, solo founders |
| **Domain Deep-Dive** | One persona + multiple stacked skills | Architecture reviews, compliance audits |
| **Multi-Agent Handoff** | Personas review each other's output | High-stakes decisions, launch readiness |
| **Skill Chain** | Sequential skills, no persona needed | Content pipelines, repeatable checklists |

**Example: 6-week product launch**
```
Week 1-2: startup-cto + aws-solution-architect + senior-frontend → Build
Week 3-4: growth-marketer + launch-strategy + copywriting + seo-audit → Prepare
Week 5-6: solo-founder + email-sequence + analytics-tracking → Ship and iterate
```

See [orchestration/ORCHESTRATION.md](orchestration/ORCHESTRATION.md) for the full protocol and examples.

---

## POWERFUL Tier

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

254 CLI tools ship with the skills (all verified, stdlib-only):

```bash
# SaaS health check
python3 finance/saas-metrics-coach/scripts/metrics_calculator.py --mrr 80000 --customers 200 --churned 3 --json

# Brand voice analysis
python3 marketing-skill/content-production/scripts/brand_voice_analyzer.py article.txt

# Tech debt scoring
python3 c-level-advisor/cto-advisor/scripts/tech_debt_analyzer.py /path/to/codebase

# RICE prioritization
python3 product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv

# Security audit
python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py /path/to/skill/

# Landing page (TSX + Tailwind)
python3 product-team/landing-page-generator/scripts/landing_page_scaffolder.py config.json --format tsx
```

---

## Related Projects

| Project | Description |
|---------|-------------|
| [**Claude Code Skills & Agents Factory**](https://github.com/alirezarezvani/claude-code-skills-agents-factory) | Methodology for building skills at scale |
| [**Claude Code Tresor**](https://github.com/alirezarezvani/claude-code-tresor) | Productivity toolkit with 60+ prompt templates |
| [**Product Manager Skills**](https://github.com/Digidai/product-manager-skills) | Senior PM agent with 6 knowledge domains, 12 templates, 30+ frameworks — discovery, strategy, delivery, SaaS metrics, career coaching, AI product craft |

---

## FAQ

**How do I install Claude Code plugins?**
Add the marketplace with `/plugin marketplace add alirezarezvani/claude-skills`, then install any skill bundle with `/plugin install <name>@claude-code-skills`.

**Do these skills work with OpenAI Codex / Cursor / Windsurf / Aider?**
Yes. Skills work natively with 11 tools: Claude Code, OpenAI Codex, Gemini CLI, OpenClaw, Cursor, Aider, Windsurf, Kilo Code, OpenCode, Augment, and Antigravity. Run `./scripts/convert.sh --tool all` to convert for all tools, then install with `./scripts/install.sh --tool <name>`. See [Multi-Tool Integrations](https://alirezarezvani.github.io/claude-skills/integrations/) for details.

**Will updating break my installation?**
No. We follow semantic versioning and maintain backward compatibility within patch releases. Existing script arguments, plugin source paths, and SKILL.md structures are never changed in patch versions. See the [CHANGELOG](CHANGELOG.md) for details on each release.

**Are the Python tools dependency-free?**
Yes. All 254 Python CLI tools use the standard library only — zero pip installs required. Every script is verified to run with `--help`.

**How do I create my own Claude Code skill?**
Each skill is a folder with a `SKILL.md` (frontmatter + instructions), optional `scripts/`, `references/`, and `assets/`. See the [Skills & Agents Factory](https://github.com/alirezarezvani/claude-code-skills-agents-factory) for a step-by-step guide.

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
