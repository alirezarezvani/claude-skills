# Changelog

All notable changes to the Claude Skills Library will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.2] - 2026-03-10

### Changed — Product Team Quality & Cross-Domain Integration

**Landing Page Generator — TSX + Brand Voice Integration:**
- Landing page scaffolder now defaults to **Next.js/React TSX output** with Tailwind CSS (HTML preserved via `--format html`)
- 4 Tailwind design styles: `dark-saas`, `clean-minimal`, `bold-startup`, `enterprise` with complete class mappings
- 7 section generators: nav, hero, features, testimonials, pricing, CTA, footer
- Brand voice integration: generation workflow now includes brand voice analysis (step 2) using `marketing-skill/content-production/scripts/brand_voice_analyzer.py` to map voice profile to design style + copy framework
- Added Related Skills cross-references to SKILL.md

**Documentation Updates:**
- `product-team/CLAUDE.md` — Added Workflow 4 (Brand-Aligned Landing Page), updated scaffolder section with TSX docs, added Cross-Domain Integration section
- `product-team/README.md` — Fixed ghost script references (removed 7 scripts that never existed), corrected skill/tool/agent/command counts
- `product-team/.codex/instructions.md` — Added brand voice cross-domain workflow and TSX default note

### Fixed
- **competitive-teardown/SKILL.md** — Fixed 6 broken file references (`DATA_COLLECTION.md` → `references/data-collection-guide.md`, `TEMPLATES.md` → `references/analysis-templates.md`)
- **saas-scaffolder/scripts/project_bootstrapper.py** — Fixed f-string backslash syntax incompatible with Python <3.12
- **237 Python scripts verified** — All pass `--help` without errors (previous session fixed 25 scripts across all domains)

### Added
- `landing-page-generator/SKILL.md` — Brand voice analysis as prerequisite step in generation workflow
- Codex and Gemini skill indexes re-synced with updated SKILL.md content

### Backward Compatibility
- `--format html` still works for landing page scaffolder (TSX is new default)
- All existing script CLIs and arguments unchanged
- No skill removals or renames
- Plugin source paths unchanged — existing installations will not break

---

## [2.1.1] - 2026-03-07

### Changed — Tessl Quality Optimization (#287)
18 skills optimized from 66-83% to 85-100% via `tessl skill review --optimize`:

| Skill | Before | After |
|-------|--------|-------|
| `project-management/confluence-expert` | 66% | 94% |
| `project-management/jira-expert` | 77% | 97% |
| `product-team/product-strategist` | 76% | 85%+ |
| `marketing-skill/campaign-analytics` | 70% | 85%+ |
| `business-growth/customer-success-manager` | 70% | 85%+ |
| `business-growth/revenue-operations` | 70% | 85%+ |
| `finance/financial-analyst` | 70% | 85%+ |
| `engineering-team/senior-secops` | 75% | 94% |
| `marketing-skill/prompt-engineer-toolkit` | 79% | 90% |
| `ra-qm-team/quality-manager-qms-iso13485` | 76% | 85%+ |
| `engineering-team/senior-security` | 80% | 93% |
| `engineering-team/playwright-pro` | 82% | 100% |
| `engineering-team/senior-backend` | 83% | 100% |
| `engineering-team/senior-qa` | 83% | 100% |
| `engineering-team/senior-ml-engineer` | 82% | 99% |
| `engineering-team/ms365-tenant-manager` | 83% | 100% |
| `engineering-team/aws-solution-architect` | 83% | 94% |
| `c-level-advisor/cto-advisor` | 82% | 99% |
| `marketing-skill/marketing-demand-acquisition` | 72% | 99% |

### Fixed
- Created missing `finance/financial-analyst/references/industry-adaptations.md` (reference was declared but file didn't exist)
- Removed dead `project-management/packaged-skills/` folder (zip files redundant)

### Added
- `SKILL_PIPELINE.md` — Mandatory 9-phase production pipeline for all skill work

### Verified
- Claude Code compliance: 18/18 pass (after fix)
- All YAML frontmatter valid
- All file references resolve
- All SKILL.md files under 500 lines

## [Unreleased]

### Added
- **skill-security-auditor** (POWERFUL tier) — Security audit and vulnerability scanner for AI agent skills. Scans for malicious code, prompt injection, data exfiltration, supply chain risks, and privilege escalation. Zero dependencies, PASS/WARN/FAIL verdicts.
- `engineering/git-worktree-manager` enhancements:
  - Added `scripts/worktree_manager.py` (worktree creation, port allocation, env sync, optional dependency install)
  - Added `scripts/worktree_cleanup.py` (stale/dirty/merged analysis with safe cleanup options)
  - Added extracted references and new skill README
- `engineering/mcp-server-builder` enhancements:
  - Added `scripts/openapi_to_mcp.py` (OpenAPI -> MCP manifest + scaffold generation)
  - Added `scripts/mcp_validator.py` (tool definition validation and strict checks)
  - Extracted templates/guides into references and added skill README
- `engineering/changelog-generator` enhancements:
  - Added `scripts/generate_changelog.py` (conventional commit parsing + Keep a Changelog rendering)
  - Added `scripts/commit_linter.py` (strict conventional commit validation)
  - Extracted CI/format/monorepo docs into references and added skill README
- `engineering/ci-cd-pipeline-builder` enhancements:
  - Added `scripts/stack_detector.py` (stack and tooling detection)
  - Added `scripts/pipeline_generator.py` (GitHub Actions / GitLab CI YAML generation)
  - Extracted platform templates into references and added skill README
- `marketing-skill/prompt-engineer-toolkit` enhancements:
  - Added `scripts/prompt_tester.py` (A/B prompt evaluation with per-case scoring)
  - Added `scripts/prompt_versioner.py` (prompt history, diff, changelog management)
  - Extracted prompt libraries/guides into references and added skill README

### Changed
- Refactored the five enhanced skills to slim, workflow-first `SKILL.md` documents aligned to Anthropic best practices.
- Updated `engineering/.claude-plugin/plugin.json` metadata:
  - Description now reflects 25 advanced engineering skills
  - Version bumped from `1.0.0` to `1.1.0`
- Updated root `README.md` with a dedicated \"Recently Enhanced Skills\" section.

### Planned
- Complete Anthropic best practices refactoring (5/42 skills remaining)
- Production Python tools for remaining RA/QM skills
- Marketing expansion: SEO Optimizer, Social Media Manager skills

---

## [2.0.0] - 2026-02-16

### ⚡ POWERFUL Tier — 25 New Skills

A new tier of advanced, deeply-engineered skills with comprehensive tooling:

- **incident-commander** — Incident response playbook with severity classifier, timeline reconstructor, and PIR generator
- **tech-debt-tracker** — Codebase debt scanner with AST parsing, debt prioritizer, and trend dashboard
- **api-design-reviewer** — REST API linter, breaking change detector, and API design scorecard
- **interview-system-designer** — Interview loop designer, question bank generator, and hiring calibrator
- **migration-architect** — Migration planner, compatibility checker, and rollback generator
- **observability-designer** — SLO designer, alert optimizer, and dashboard generator
- **dependency-auditor** — Multi-language dependency scanner, license compliance checker, and upgrade planner
- **release-manager** — Automated changelog generator, semantic version bumper, and release readiness checker
- **database-designer** — Schema analyzer with ERD generation, index optimizer, and migration generator
- **rag-architect** — RAG pipeline builder, chunking optimizer, and retrieval evaluator
- **agent-designer** — Multi-agent architect, tool schema generator, and agent performance evaluator
- **skill-tester** — Meta-skill validator, script tester, and quality scorer
- **agent-workflow-designer** — Multi-agent orchestration system designer with sequential, parallel, router, orchestrator, and evaluator patterns
- **api-test-suite-builder** — API route scanner and test suite generator across frameworks (Next.js, Express, FastAPI, Django REST)
- **changelog-generator** — Conventional commit parser, semantic version bumper, and structured changelog generator
- **ci-cd-pipeline-builder** — Stack-aware CI/CD pipeline generator for GitHub Actions, GitLab CI, and more
- **codebase-onboarding** — Codebase analyzer and onboarding documentation generator for new team members
- **database-schema-designer** — Database schema design and modeling tool with migration support
- **env-secrets-manager** — Environment and secrets management across dev/staging/prod lifecycle
- **git-worktree-manager** — Systematic Git worktree management for parallel development workflows
- **mcp-server-builder** — MCP (Model Context Protocol) server scaffolder and implementation guide
- **monorepo-navigator** — Monorepo management for Turborepo, Nx, pnpm workspaces, and Lerna
- **performance-profiler** — Systematic performance profiling for Node.js, Python, and Go applications
- **pr-review-expert** — Structured code review for GitHub PRs and GitLab MRs with systematic analysis
- **runbook-generator** — Production-grade operational runbook generator with stack detection

### 🆕 New Domains & Skills

- **business-growth** domain (3 skills):
  - `customer-success-manager` — Onboarding, retention, expansion, health scoring (2 Python tools)
  - `sales-engineer` — Technical sales, solution design, RFP responses (2 Python tools)
  - `revenue-operations` — Pipeline analytics, forecasting, process optimization (2 Python tools)
- **finance** domain (1 skill):
  - `financial-analyst` — DCF valuation, budgeting, forecasting, financial modeling (3 Python tools)
- **marketing** addition:
  - `campaign-analytics` — Multi-touch attribution, funnel conversion, campaign ROI (3 Python tools)

### 🔄 Anthropic Best Practices Refactoring (37/42 Skills)

Major rewrite of existing skills following Anthropic's agent skills specification. Each refactored skill received:
- Professional metadata (license, version, category, domain, keywords)
- Trigger phrases for better Claude activation
- Table of contents with proper section navigation
- Numbered workflows with validation checkpoints
- Progressive Disclosure Architecture (PDA)
- Concise SKILL.md (<200 lines target) with layered reference files

**Engineering skills refactored (14):**
- `senior-architect`, `senior-frontend`, `senior-backend`, `senior-fullstack`
- `senior-qa`, `senior-secops`, `senior-security`, `code-reviewer`
- `senior-data-engineer`, `senior-computer-vision`, `senior-ml-engineer`
- `senior-prompt-engineer`, `tdd-guide`, `tech-stack-evaluator`

**Product & PM skills refactored (5):**
- `product-manager-toolkit`, `product-strategist`, `agile-product-owner`
- `ux-researcher-designer`, `ui-design-system`

**RA/QM skills refactored (12):**
- `regulatory-affairs-head`, `quality-manager-qmr`, `quality-manager-qms-iso13485`
- `capa-officer`, `quality-documentation-manager`, `risk-management-specialist`
- `information-security-manager-iso27001`, `mdr-745-specialist`, `fda-consultant-specialist`
- `qms-audit-expert`, `isms-audit-expert`, `gdpr-dsgvo-expert`

**Marketing skills refactored (4):**
- `marketing-demand-acquisition`, `marketing-strategy-pmm`
- `content-creator`, `app-store-optimization`

**Other refactored (2):**
- `aws-solution-architect`, `ms365-tenant-manager`

### 🔧 Elevated Skills
- `scrum-master` and `senior-pm` elevated to POWERFUL tier — PR #190

### 🤖 Platform Support
- **OpenAI Codex support** — Full compatibility without restructuring — PR #43, #45, #47
- **Claude Code native marketplace** — `marketplace.json` and plugin support — PR #182, #185
- **Codex skills sync** — Automated symlink workflow for Codex integration

### 📊 Stats
- **86 total skills** across 9 domains (up from 42 across 6)
- **92+ Python automation tools** (up from 20+)
- **26 POWERFUL-tier skills** in `engineering/` domain (including skill-security-auditor)
- **37/42 original skills refactored** to Anthropic best practices

### Fixed
- CI workflows (`smart-sync.yml`, `pr-issue-auto-close.yml`) — PR #193
- Installation documentation (Issue #189) — PR #193
- Plugin JSON with correct counts and missing domains — PR #186
- PM skills extracted from zips into standard directories — PR #184, #185
- Marketing skill count corrected (6 total) — PR #182
- Codex skills sync workflow fixes — PR #178, #179, #180
- `social-media-analyzer` restructured with proper organization — PR #147, #151

---

## [1.1.0] - 2025-10-21 - Anthropic Best Practices Refactoring (Phase 1)

### Changed — Marketing & C-Level Skills

**Enhanced with Anthropic Agent Skills Specification:**

**Marketing Skills (3 skills):**
- Added professional metadata (license, version, category, domain)
- Added keywords sections for better discovery
- Enhanced descriptions with explicit triggers
- Added python-tools and tech-stack documentation

**C-Level Skills (2 skills):**
- Added professional metadata with frameworks
- Added keywords sections (20+ keywords per skill)
- Enhanced descriptions for better Claude activation
- Added technical and strategic terminology

### Added
- `documentation/implementation/SKILLS_REFACTORING_PLAN.md` — Complete 4-phase refactoring roadmap
- `documentation/PYTHON_TOOLS_AUDIT.md` — Comprehensive tools quality assessment

**Refactoring Progress:** 5/42 skills complete (12%)

---

## [1.0.2] - 2025-10-21

### Added
- `LICENSE` file — Official MIT License
- `CONTRIBUTING.md` — Contribution guidelines and standards
- `CODE_OF_CONDUCT.md` — Community standards (Contributor Covenant 2.0)
- `SECURITY.md` — Security policy and vulnerability reporting
- `CHANGELOG.md` — Version history tracking

### Documentation
- Complete GitHub repository setup for open source
- Professional community health files
- Clear contribution process
- Security vulnerability handling

---

## [1.0.1] - 2025-10-21

### Added
- GitHub Star History chart to README.md
- Professional repository presentation

### Changed
- README.md table of contents anchor links fixed
- Project management folder reorganized (packaged-skills/ structure)

---

## [1.0.0] - 2025-10-21

### Added — Complete Initial Release

**42 Production-Ready Skills across 6 Domains:**

#### Marketing Skills (3)
- `content-creator` — Brand voice analyzer, SEO optimizer, content frameworks
- `marketing-demand-acquisition` — Demand gen, paid media, CAC calculator
- `marketing-strategy-pmm` — Positioning, GTM, competitive intelligence

#### C-Level Advisory (2)
- `ceo-advisor` — Strategy analyzer, financial scenario modeling, board governance
- `cto-advisor` — Tech debt analyzer, team scaling calculator, engineering metrics

#### Product Team (5)
- `product-manager-toolkit` — RICE prioritizer, interview analyzer, PRD templates
- `agile-product-owner` — User story generator, sprint planning
- `product-strategist` — OKR cascade generator, strategic planning
- `ux-researcher-designer` — Persona generator, user research
- `ui-design-system` — Design token generator, component architecture

#### Project Management (6)
- `senior-pm` — Portfolio management, stakeholder alignment
- `scrum-master` — Sprint ceremonies, agile coaching
- `jira-expert` — JQL mastery, configuration, dashboards
- `confluence-expert` — Knowledge management, documentation
- `atlassian-admin` — System administration, security
- `atlassian-templates` — Template design, 15+ ready templates

#### Engineering — Core (9)
- `senior-architect` — Architecture diagrams, dependency analysis, ADRs
- `senior-frontend` — React components, bundle optimization
- `senior-backend` — API scaffolder, database migrations, load testing
- `senior-fullstack` — Project scaffolder, code quality analyzer
- `senior-qa` — Test suite generator, coverage analyzer, E2E tests
- `senior-devops` — CI/CD pipelines, Terraform, deployment automation
- `senior-secops` — Security scanner, vulnerability assessment, compliance
- `code-reviewer` — PR analyzer, code quality checker
- `senior-security` — Threat modeling, security audits, pentesting

#### Engineering — AI/ML/Data (5)
- `senior-data-scientist` — Experiment designer, feature engineering, statistical analysis
- `senior-data-engineer` — Pipeline orchestrator, data quality validator, ETL
- `senior-ml-engineer` — Model deployment, MLOps setup, RAG system builder
- `senior-prompt-engineer` — Prompt optimizer, RAG evaluator, agent orchestrator
- `senior-computer-vision` — Vision model trainer, inference optimizer, video processor

#### Regulatory Affairs & Quality Management (12)
- `regulatory-affairs-head` — Regulatory pathway analyzer, submission tracking
- `quality-manager-qmr` — QMS effectiveness monitor, compliance dashboards
- `quality-manager-qms-iso13485` — QMS compliance checker, design control tracker
- `capa-officer` — CAPA tracker, root cause analyzer, trend analysis
- `quality-documentation-manager` — Document version control, technical file builder
- `risk-management-specialist` — Risk register manager, FMEA calculator
- `information-security-manager-iso27001` — ISMS compliance, security risk assessment
- `mdr-745-specialist` — MDR compliance checker, UDI generator
- `fda-consultant-specialist` — FDA submission packager, QSR compliance
- `qms-audit-expert` — Audit planner, finding tracker
- `isms-audit-expert` — ISMS audit planner, security controls assessor
- `gdpr-dsgvo-expert` — GDPR compliance checker, DPIA generator

### Documentation
- Comprehensive README.md with all 42 skills
- Domain-specific README files (6 domains)
- CLAUDE.md development guide
- Installation and usage guides
- Real-world scenario walkthroughs

### Automation
- 20+ verified production-ready Python CLI tools
- 90+ comprehensive reference guides
- Atlassian MCP Server integration

---

## Version History Summary

| Version | Date | Skills | Domains | Key Changes |
|---------|------|--------|---------|-------------|
| 2.1.2 | 2026-03-10 | 170 | 9 | Landing page TSX output, brand voice integration, 25 script fixes |
| 2.1.1 | 2026-03-07 | 170 | 9 | 18 skills optimized via Tessl, YAML frontmatter, agents + commands |
| 2.0.0 | 2026-02-16 | 86 | 9 | 26 POWERFUL-tier skills, 37 refactored, Codex support, 3 new domains |
| 1.1.0 | 2025-10-21 | 42 | 6 | Anthropic best practices refactoring (5 skills) |
| 1.0.2 | 2025-10-21 | 42 | 6 | GitHub repository pages (LICENSE, CONTRIBUTING, etc.) |
| 1.0.1 | 2025-10-21 | 42 | 6 | Star History, link fixes |
| 1.0.0 | 2025-10-21 | 42 | 6 | Initial release — 42 skills, 6 domains |

---

## Semantic Versioning

- **Major (x.0.0):** Breaking changes, major new domains, significant architecture shifts
- **Minor (1.x.0):** New skills, significant enhancements
- **Patch (1.0.x):** Bug fixes, documentation updates, minor improvements

---

[Unreleased]: https://github.com/alirezarezvani/claude-skills/compare/v2.1.2...HEAD
[2.1.2]: https://github.com/alirezarezvani/claude-skills/compare/v2.1.1...v2.1.2
[2.1.1]: https://github.com/alirezarezvani/claude-skills/compare/v2.0.0...v2.1.1
[2.0.0]: https://github.com/alirezarezvani/claude-skills/compare/v1.0.2...v2.0.0
[1.1.0]: https://github.com/alirezarezvani/claude-skills/compare/v1.0.1...v1.1.0
[1.0.2]: https://github.com/alirezarezvani/claude-skills/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/alirezarezvani/claude-skills/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/alirezarezvani/claude-skills/releases/tag/v1.0.0
