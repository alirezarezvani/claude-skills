# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a **comprehensive skills library** for Claude AI and Claude Code - reusable, production-ready skill packages that bundle domain expertise, best practices, analysis tools, and strategic frameworks. The repository provides modular skills that teams can download and use directly in their workflows.

**Current Scope:** 170 production-ready skills across 9 domains with 210+ Python automation tools, 310+ reference guides, 12 agents, and 5 slash commands.

**Key Distinction**: This is NOT a traditional application. It's a library of skill packages meant to be extracted and deployed by users into their own Claude workflows.

## Navigation Map

This repository uses **modular documentation**. For domain-specific guidance, see:

| Domain | CLAUDE.md Location | Focus |
|--------|-------------------|-------|
| **Agent Development** | [agents/CLAUDE.md](agents/CLAUDE.md) | cs-* agent creation, YAML frontmatter, relative paths |
| **Marketing Skills** | [marketing-skill/CLAUDE.md](marketing-skill/CLAUDE.md) | Content creation, SEO, ASO, demand gen, campaign analytics |
| **Product Team** | [product-team/CLAUDE.md](product-team/CLAUDE.md) | RICE, OKRs, user stories, UX research, SaaS scaffolding |
| **Engineering (Core)** | [engineering-team/CLAUDE.md](engineering-team/CLAUDE.md) | Fullstack, AI/ML, DevOps, security, data, QA tools |
| **Engineering (POWERFUL)** | [engineering/](engineering/) | Agent design, RAG, MCP, CI/CD, database, observability |
| **C-Level Advisory** | [c-level-advisor/CLAUDE.md](c-level-advisor/CLAUDE.md) | CEO/CTO strategic decision-making |
| **Project Management** | [project-management/CLAUDE.md](project-management/CLAUDE.md) | Atlassian MCP, Jira/Confluence integration |
| **RA/QM Compliance** | [ra-qm-team/CLAUDE.md](ra-qm-team/CLAUDE.md) | ISO 13485, MDR, FDA, GDPR, ISO 27001 compliance |
| **Business & Growth** | [business-growth/CLAUDE.md](business-growth/CLAUDE.md) | Customer success, sales engineering, revenue operations |
| **Finance** | [finance/CLAUDE.md](finance/CLAUDE.md) | Financial analysis, DCF valuation, budgeting, forecasting |
| **Standards Library** | [standards/CLAUDE.md](standards/CLAUDE.md) | Communication, quality, git, security standards |
| **Templates** | [templates/CLAUDE.md](templates/CLAUDE.md) | Template system usage |

## Architecture Overview

### Repository Structure

```
claude-code-skills/
├── .claude-plugin/            # Plugin registry (marketplace.json)
├── agents/                    # 12 cs-* prefixed agents across all domains
├── commands/                  # 5 slash commands (changelog, tdd, tech-debt, etc.)
├── engineering-team/          # 23 core engineering skills + Playwright Pro + Self-Improving Agent
├── engineering/               # 25 POWERFUL-tier advanced skills
├── product-team/              # 8 product skills + Python tools
├── marketing-skill/           # 42 marketing skills (7 pods) + Python tools
├── c-level-advisor/           # 28 C-level advisory skills (10 roles + orchestration)
├── project-management/        # 6 PM skills + Atlassian MCP
├── ra-qm-team/                # 12 RA/QM compliance skills
├── business-growth/           # 4 business & growth skills + Python tools
├── finance/                   # 1 finance skill + Python tools
├── eval-workspace/            # Skill evaluation results (Tessl)
├── standards/                 # 5 standards library files
├── templates/                 # Reusable templates
├── docs/                      # MkDocs Material documentation site
├── scripts/                   # Build scripts (docs generation)
└── documentation/             # Implementation plans, sprints, delivery
```

### Skill Package Pattern

Each skill follows this structure:
```
skill-name/
├── SKILL.md              # Master documentation
├── scripts/              # Python CLI tools (no ML/LLM calls)
├── references/           # Expert knowledge bases
└── assets/               # User templates
```

**Design Philosophy**: Skills are self-contained packages. Each includes executable tools (Python scripts), knowledge bases (markdown references), and user-facing templates. Teams can extract a skill folder and use it immediately.

**Key Pattern**: Knowledge flows from `references/` → into `SKILL.md` workflows → executed via `scripts/` → applied using `assets/` templates.

## Git Workflow

**Branch Strategy:** feature → dev → main (PR only)

**Branch Protection Active:** Main branch requires PR approval. Direct pushes blocked.

### Quick Start

```bash
# 1. Always start from dev
git checkout dev
git pull origin dev

# 2. Create feature branch
git checkout -b feature/agents-{name}

# 3. Work and commit (conventional commits)
feat(agents): implement cs-{agent-name}
fix(tool): correct calculation logic
docs(workflow): update branch strategy

# 4. Push and create PR to dev
git push origin feature/agents-{name}
gh pr create --base dev --head feature/agents-{name}

# 5. After approval, PR merges to dev
# 6. Periodically, dev merges to main via PR
```

**Branch Protection Rules:**
- ✅ Main: Requires PR approval, no direct push
- ✅ Dev: Unprotected, but PRs recommended
- ✅ All: Conventional commits enforced

See [documentation/WORKFLOW.md](documentation/WORKFLOW.md) for complete workflow guide.
See [standards/git/git-workflow-standards.md](standards/git/git-workflow-standards.md) for commit standards.

## Development Environment

**No build system or test frameworks** - intentional design choice for portability.

**Python Scripts:**
- Use standard library only (minimal dependencies)
- CLI-first design for easy automation
- Support both JSON and human-readable output
- No ML/LLM calls (keeps skills portable and fast)

**If adding dependencies:**
- Keep scripts runnable with minimal setup (`pip install package` at most)
- Document all dependencies in SKILL.md
- Prefer standard library implementations

## Current Version

**Version:** v2.1.1 (latest)

**v2.1.1 Highlights:**
- 18 skills optimized from 66-83% to 85-100% via Tessl quality review
- 21 over-500-line skills split into SKILL.md + references/
- YAML frontmatter (name + description) added to all SKILL.md files
- 6 new agents + 5 slash commands for full domain coverage
- **Gemini CLI support added** (scripts/gemini-install.sh + GEMINI.md)
- MkDocs Material documentation site at alirezarezvani.github.io/claude-skills

**v2.0.0 (2026-02-16):**
- 25 POWERFUL-tier engineering skills added (engineering/ folder)
- Plugin marketplace infrastructure (.claude-plugin/marketplace.json)
- Multi-platform support: Claude Code, OpenAI Codex, OpenClaw

**Past Sprints:** See [documentation/delivery/](documentation/delivery/) and [CHANGELOG.md](CHANGELOG.md) for history.

## Roadmap

**Phase 1-2 Complete:** 170 production-ready skills deployed across 9 domains
- Engineering Core (23), Engineering POWERFUL (25), Product (8), Marketing (42), PM (6), C-Level (28), RA/QM (12), Business & Growth (4), Finance (1)
- 210+ Python automation tools, 310+ reference guides, 12 agents, 5 commands
- Complete enterprise coverage from engineering through regulatory compliance, sales, customer success, and finance
- MkDocs Material docs site with 170+ indexed pages for SEO

See domain-specific roadmaps in each skill folder's README.md or roadmap files.

## Key Principles

1. **Skills are products** - Each skill deployable as standalone package
2. **Documentation-driven** - Success depends on clear, actionable docs
3. **Algorithm over AI** - Use deterministic analysis (code) vs LLM calls
4. **Template-heavy** - Provide ready-to-use templates users customize
5. **Platform-specific** - Specific best practices > generic advice

## Anti-Patterns to Avoid

- Creating dependencies between skills (keep each self-contained)
- Adding complex build systems or test frameworks (maintain simplicity)
- Generic advice (focus on specific, actionable frameworks)
- LLM calls in scripts (defeats portability and speed)
- Over-documenting file structure (skills are simple by design)

## Working with This Repository

**Creating New Skills:** Follow the appropriate domain's roadmap and CLAUDE.md guide (see Navigation Map above).

**Editing Existing Skills:** Maintain consistency across markdown files. Use the same voice, formatting, and structure patterns.

**Quality Standard:** Each skill should save users 40%+ time while improving consistency/quality by 30%+.

## Additional Resources

- **.gitignore:** Excludes .vscode/, .DS_Store, AGENTS.md, PROMPTS.md, .env*
- **Plugin Registry:** [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) - Marketplace distribution
- **Standards Library:** [standards/](standards/) - Communication, quality, git, documentation, security
- **Implementation Plans:** [documentation/implementation/](documentation/implementation/)
- **Sprint Delivery:** [documentation/delivery/](documentation/delivery/)

---

**Last Updated:** March 2026
**Version:** v2.1.1
**Status:** 170 skills deployed across 9 domains, 18 marketplace plugins, docs site live
