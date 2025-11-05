# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a **comprehensive skills library** for Claude AI - reusable, production-ready skill packages that bundle domain expertise, best practices, analysis tools, and strategic frameworks. The repository provides modular skills that teams can download and use directly in their workflows.

**Current Scope:** 42 production-ready skills across 6 domains with 97 Python automation tools.

**Key Distinction**: This is NOT a traditional application. It's a library of skill packages meant to be extracted and deployed by users into their own Claude workflows.

## Navigation Map

This repository uses **modular documentation**. For domain-specific guidance, see:

| Domain | CLAUDE.md Location | Focus |
|--------|-------------------|-------|
| **Agent Development** | [agents/CLAUDE.md](agents/CLAUDE.md) | cs-* agent creation, YAML frontmatter, relative paths |
| **Marketing Skills** | [marketing-skill/CLAUDE.md](marketing-skill/CLAUDE.md) | Content creation, SEO, demand gen Python tools |
| **Product Team** | [product-team/CLAUDE.md](product-team/CLAUDE.md) | RICE, OKRs, user stories, UX research tools |
| **Engineering** | [engineering-team/CLAUDE.md](engineering-team/CLAUDE.md) | Scaffolding, fullstack, AI/ML, data tools |
| **C-Level Advisory** | [c-level-advisor/CLAUDE.md](c-level-advisor/CLAUDE.md) | CEO/CTO strategic decision-making |
| **Project Management** | [project-management/CLAUDE.md](project-management/CLAUDE.md) | Atlassian MCP, Jira/Confluence integration |
| **RA/QM Compliance** | [ra-qm-team/CLAUDE.md](ra-qm-team/CLAUDE.md) | ISO 13485, MDR, FDA compliance workflows |
| **Standards Library** | [standards/CLAUDE.md](standards/CLAUDE.md) | Communication, quality, git, security standards |
| **Templates** | [templates/CLAUDE.md](templates/CLAUDE.md) | Template system usage |

**Current Sprint:** See [documentation/delivery/sprint-11-05-2025/](documentation/delivery/sprint-11-05-2025/) for active sprint context and progress.

## Architecture Overview

### Repository Structure

```
claude-code-skills/
├── agents/                    # cs-* prefixed agents (in development)
├── marketing-skill/           # 3 marketing skills + Python tools
├── product-team/              # 5 product skills + Python tools
├── engineering-team/          # 14 engineering skills + Python tools
├── c-level-advisor/           # 2 C-level skills
├── project-management/        # 6 PM skills + Atlassian MCP
├── ra-qm-team/                # 12 RA/QM compliance skills
├── standards/                 # 5 standards library files
├── templates/                 # Reusable templates
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

Follow conventional commits and semantic versioning:

```bash
# Feature branches by domain
git checkout -b feature/marketing/seo-optimizer
git checkout -b feature/agents/content-creator

# Conventional commit format
feat(agents): implement cs-content-creator agent
fix(seo-optimizer): correct keyword density calculation
docs(README): update agent catalog section

# Semantic versioning by skill
git tag v1.0-content-creator
git tag v1.0-product-manager-toolkit
```

**Branch Strategy**: Domain-based branches, squash merge to main, semantic tags per skill release.

See [standards/git/git-workflow-standards.md](standards/git/git-workflow-standards.md) for complete workflow details.

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

## Current Sprint

**Active Sprint:** sprint-11-05-2025 (Nov 5-19, 2025)
**Goal:** Skill-Agent Integration Phase 1-2
**Status:** Day 1 complete (foundation), Day 2 ready (marketing agents)

**Progress Tracking:**
- [Sprint Plan](documentation/delivery/sprint-11-05-2025/plan.md) - Day-by-day execution plan
- [Sprint Context](documentation/delivery/sprint-11-05-2025/context.md) - Goals, scope, risks
- [Sprint Progress](documentation/delivery/sprint-11-05-2025/PROGRESS.md) - Real-time auto-updating tracker

## Roadmap

**Phase 1 Complete:** 42 production-ready skills deployed
- Marketing (3), C-Level (2), Product (5), PM (6), Engineering (14), RA/QM (12)
- 97 Python automation tools, 90+ reference guides
- Complete enterprise coverage from marketing through regulatory compliance

**Next Priorities:**
- **Phase 2 (Q1 2026):** Marketing expansion - SEO optimizer, social media manager, campaign analytics
- **Phase 3 (Q2 2026):** Business & growth - Sales engineer, customer success, growth marketer
- **Phase 4 (Q3 2026):** Specialized domains - Mobile, blockchain, web3, finance

**Target:** 50+ skills by Q3 2026

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
- **Standards Library:** [standards/](standards/) - Communication, quality, git, documentation, security
- **Implementation Plans:** [documentation/implementation/](documentation/implementation/)
- **Sprint Delivery:** [documentation/delivery/](documentation/delivery/)

---

**Last Updated:** November 5, 2025
**Current Sprint:** sprint-11-05-2025 (Skill-Agent Integration Phase 1-2)
**Status:** 42 skills deployed, agent system in development
