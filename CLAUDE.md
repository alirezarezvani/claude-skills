# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a **comprehensive skills library** for Claude AI - reusable, production-ready skill packages that bundle domain expertise, best practices, analysis tools, and strategic frameworks across marketing, executive leadership, and product development. The repository provides modular skills that teams can download and use directly in their workflows.

**Current Scope:** 34 production-ready skills across 5 domains:
- **Marketing (1):** Content creation, SEO, brand voice, social media
- **C-Level Advisory (2):** CEO strategic planning, CTO technical leadership
- **Product Team (5):** Product management, agile delivery, UX research, UI design, strategic planning
- **Engineering Team (14):**
  - Core Engineering (9): Architecture, frontend, backend, fullstack, QA, DevOps, SecOps, code review, security
  - AI/ML/Data (5): Data science, data engineering, ML engineering, prompt engineering, computer vision
- **Regulatory Affairs & Quality Management (12):**
  - Strategic Leadership (2): RA Manager, Quality Manager (QMR)
  - Quality Systems (3): QMS ISO 13485, CAPA Officer, Documentation Manager
  - Risk & Security (2): Risk Management (ISO 14971), Information Security (ISO 27001)
  - Regulatory Specialists (2): MDR 2017/745, FDA Consultant
  - Audit & Compliance (3): QMS Audit, ISMS Audit, GDPR/DSGVO

**Key Distinction**: This is NOT a traditional application. It's a library of skill packages meant to be extracted and deployed by users into their own Claude workflows.

## Architecture Overview

### Skill Package Structure

The repository is organized by domain, with each skill following a consistent modular architecture:

```
claude-skills/
├── marketing-skill/
│   └── content-creator/
│       ├── SKILL.md                # Master documentation
│       ├── scripts/                # Python CLI tools
│       ├── references/             # Knowledge bases
│       └── assets/                 # User templates
├── c-level-advisor/
│   ├── ceo-advisor/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── references/
│   └── cto-advisor/
│       ├── SKILL.md
│       ├── scripts/
│       └── references/
└── product-team/
    ├── product-manager-toolkit/
    │   ├── SKILL.md
    │   ├── scripts/
    │   └── references/
    ├── agile-product-owner/
    │   ├── SKILL.md
    │   └── scripts/
    ├── product-strategist/
    │   ├── SKILL.md
    │   └── scripts/
    ├── ux-researcher-designer/
    │   ├── SKILL.md
    │   └── scripts/
    └── ui-design-system/
        ├── SKILL.md
        └── scripts/
└── engineering-team/
    ├── senior-architect/
    ├── senior-frontend/
    ├── senior-backend/
    ├── senior-fullstack/
    ├── senior-qa/
    ├── senior-devops/
    ├── senior-secops/
    ├── code-reviewer/
    ├── senior-security/
    ├── senior-data-scientist/
    ├── senior-data-engineer/
    ├── senior-ml-engineer/
    ├── senior-prompt-engineer/
    ├── senior-computer-vision/
    ├── README.md                      # Engineering skills overview
    ├── START_HERE.md                  # Quick start guide
    └── TEAM_STRUCTURE_GUIDE.md        # Team composition recommendations

Each skill contains:
    ├── SKILL.md                       # Master documentation
    ├── scripts/                       # 3 Python automation tools
    └── references/                    # 3 comprehensive guides

└── ra-qm-team/
    ├── regulatory-affairs-head/
    ├── quality-manager-qmr/
    ├── quality-manager-qms-iso13485/
    ├── capa-officer/
    ├── quality-documentation-manager/
    ├── risk-management-specialist/
    ├── information-security-manager-iso27001/
    ├── mdr-745-specialist/
    ├── fda-consultant-specialist/
    ├── qms-audit-expert/
    ├── isms-audit-expert/
    ├── gdpr-dsgvo-expert/
    ├── README.md                      # RA/QM team overview
    ├── START_HERE.md                  # Quick start (if exists)
    └── final-complete-skills-collection.md  # Complete skills summary
```

**Design Philosophy**: Skills are self-contained packages. Each includes executable tools (Python scripts), knowledge bases (markdown references), and user-facing templates. Teams can extract a skill folder and use it immediately.

### Component Relationships

1. **SKILL.md** → Entry point defining workflows, referencing scripts and knowledge bases
2. **scripts/** → Algorithmic analysis tools (brand voice, SEO) that process user content
3. **references/** → Static knowledge bases that inform content creation (frameworks, platform guidelines)
4. **assets/** → Templates that users copy and customize (content calendars, checklists)

**Key Pattern**: Knowledge flows from references → into SKILL.md workflows → executed via scripts → applied using templates.

## Core Components

### Python Analysis Scripts

Located in `scripts/`, these are **pure algorithmic tools** (no ML/LLM calls):

**brand_voice_analyzer.py** (185 lines):
- Analyzes text for formality, tone, perspective, readability
- Uses Flesch Reading Ease formula for readability scoring
- Outputs JSON or human-readable format
- Usage: `python scripts/brand_voice_analyzer.py content.txt [json]`

**seo_optimizer.py** (419 lines):
- Comprehensive SEO analysis: keyword density, structure, meta tags
- Calculates SEO score (0-100) with actionable recommendations
- Usage: `python scripts/seo_optimizer.py article.md "primary keyword" "secondary,keywords"`

**Implementation Notes**:
- Scripts use standard library only (except PyYAML for future features)
- Designed for CLI invocation - no server/API needed
- Process content files directly from filesystem
- Return structured data (JSON) or formatted text

### Reference Knowledge Bases

Located in `references/`, these are **expert-curated guideline documents**:

- **brand_guidelines.md**: Voice framework with 5 personality archetypes (Expert, Friend, Innovator, Guide, Motivator)
- **content_frameworks.md**: 15+ content templates (blog posts, email, social, video scripts, case studies)
- **social_media_optimization.md**: Platform-specific best practices for LinkedIn, Twitter/X, Instagram, Facebook, TikTok

**Critical Architecture Point**: References are NOT code - they're knowledge bases that inform both human users and Claude when creating content. When editing, maintain structured markdown with clear sections, checklists, and examples.

### Product Team Python Scripts

Located in `product-team/*/scripts/`, these are **specialized product development tools**:

**rice_prioritizer.py** (Product Manager Toolkit):
- RICE framework implementation: (Reach × Impact × Confidence) / Effort
- Portfolio analysis (quick wins vs big bets)
- Quarterly roadmap generation with capacity planning
- Supports CSV input/output and JSON for integrations
- Usage: `python scripts/rice_prioritizer.py features.csv --capacity 20`

**customer_interview_analyzer.py** (Product Manager Toolkit):
- NLP-based interview transcript analysis
- Extracts pain points with severity scoring
- Identifies feature requests and priorities
- Sentiment analysis and theme extraction
- Jobs-to-be-done pattern recognition
- Usage: `python scripts/customer_interview_analyzer.py interview.txt [json]`

**user_story_generator.py** (Agile Product Owner):
- INVEST-compliant user story generation
- Sprint planning with capacity allocation
- Epic breakdown into deliverable stories
- Acceptance criteria generation
- Usage: `python scripts/user_story_generator.py sprint 30`

**okr_cascade_generator.py** (Product Strategist):
- Automated OKR hierarchy: company → product → team
- Alignment scoring (vertical and horizontal)
- Strategy templates (growth, retention, revenue, innovation)
- Usage: `python scripts/okr_cascade_generator.py growth`

**persona_generator.py** (UX Researcher Designer):
- Data-driven persona creation from user research
- Demographic and psychographic profiling
- Goals, pain points, and behavior patterns
- Usage: `python scripts/persona_generator.py --output json`

**design_token_generator.py** (UI Design System):
- Complete design token system from brand color
- Generates colors, typography, spacing, shadows
- Multiple export formats: CSS, JSON, SCSS
- Responsive breakpoint calculations
- Usage: `python scripts/design_token_generator.py "#0066CC" modern css`

**Implementation Notes**:
- All scripts use standard library (minimal dependencies)
- CLI-first design for easy automation and integration
- Support both interactive and batch modes
- JSON output for tool integration (Jira, Figma, Confluence)

### Engineering Team Python Scripts

Located in `engineering-team/*/scripts/`, these are **fullstack development automation tools**:

**project_scaffolder.py** (Fullstack Engineer):
- Production-ready project scaffolding for Next.js + GraphQL + PostgreSQL stack
- Docker Compose configuration with all services
- CI/CD pipeline setup with GitHub Actions
- Testing infrastructure (Jest, Cypress)
- TypeScript, ESLint, Prettier configuration
- Usage: `python scripts/project_scaffolder.py my-project --type nextjs-graphql`

**code_quality_analyzer.py** (Fullstack Engineer):
- Comprehensive code quality analysis and metrics
- Security vulnerability scanning
- Performance issue detection
- Test coverage assessment
- Documentation quality evaluation
- Dependency analysis and recommendations
- Usage: `python scripts/code_quality_analyzer.py /path/to/project [--json]`

**fullstack_scaffolder.py** (Fullstack Engineer):
- Rapid fullstack application generation
- Modern stack templates with Docker support
- Automated project structure and boilerplate
- Usage: `python scripts/fullstack_scaffolder.py my-app --stack nextjs-graphql`

**Implementation Notes**:
- Scripts use standard library with minimal external dependencies
- Designed for rapid project bootstrapping and quality assurance
- Support both Docker and manual deployment workflows
- Comprehensive analysis with actionable recommendations

### AI/ML/Data Team Python Scripts

Located in `engineering-team/senior-{data,ml,ai}*/scripts/`, these are **AI/ML and data infrastructure tools**:

**Senior Data Scientist:**
- `experiment_designer.py` - Design A/B tests and statistical experiments
- `feature_engineering_pipeline.py` - Automated feature engineering
- `statistical_analyzer.py` - Statistical modeling and causal inference

**Senior Data Engineer:**
- `pipeline_orchestrator.py` - Build data pipelines with Airflow/Spark
- `data_quality_validator.py` - Data quality checks and monitoring
- `etl_generator.py` - Generate ETL/ELT workflows

**Senior ML Engineer:**
- `model_deployment_pipeline.py` - Deploy ML models to production
- `mlops_setup_tool.py` - Setup MLOps infrastructure (MLflow, monitoring)
- `llm_integration_builder.py` - Integrate LLMs into applications

**Senior Prompt Engineer:**
- `prompt_optimizer.py` - Optimize prompts for LLMs
- `rag_system_builder.py` - Build RAG (Retrieval Augmented Generation) systems
- `agent_orchestrator.py` - Design and orchestrate AI agents

**Senior Computer Vision Engineer:**
- `vision_model_trainer.py` - Train object detection and segmentation models
- `inference_optimizer.py` - Optimize vision model inference
- `video_processor.py` - Process and analyze video streams

**Implementation Notes**:
- AI/ML scripts integrate with modern frameworks (PyTorch, LangChain, OpenCV)
- Data engineering tools support Spark, Airflow, dbt, Kafka
- MLOps workflows include monitoring, versioning, and drift detection
- All tools designed for production deployment at scale

## Development Commands

### Running Analysis Tools

```bash
# Analyze brand voice
python marketing-skill/content-creator/scripts/brand_voice_analyzer.py content.txt

# Analyze with JSON output
python marketing-skill/content-creator/scripts/brand_voice_analyzer.py content.txt json

# SEO optimization
python marketing-skill/content-creator/scripts/seo_optimizer.py article.md "main keyword"

# SEO with secondary keywords
python marketing-skill/content-creator/scripts/seo_optimizer.py article.md "main keyword" "secondary,keywords"

# Product Manager - RICE prioritization
python product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv
python product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv --capacity 20 --output json

# Product Manager - Interview analysis
python product-team/product-manager-toolkit/scripts/customer_interview_analyzer.py interview.txt
python product-team/product-manager-toolkit/scripts/customer_interview_analyzer.py interview.txt json

# Product Owner - User stories
python product-team/agile-product-owner/scripts/user_story_generator.py
python product-team/agile-product-owner/scripts/user_story_generator.py sprint 30

# Product Strategist - OKR cascade
python product-team/product-strategist/scripts/okr_cascade_generator.py growth
python product-team/product-strategist/scripts/okr_cascade_generator.py retention

# UX Researcher - Personas
python product-team/ux-researcher-designer/scripts/persona_generator.py
python product-team/ux-researcher-designer/scripts/persona_generator.py --output json

# UI Designer - Design tokens
python product-team/ui-design-system/scripts/design_token_generator.py "#0066CC" modern css
python product-team/ui-design-system/scripts/design_token_generator.py "#0066CC" modern json

# Fullstack Engineer - Project scaffolding
python engineering-team/fullstack-engineer/scripts/project_scaffolder.py my-project --type nextjs-graphql
cd my-project && docker-compose up -d

# Fullstack Engineer - Code quality
python engineering-team/fullstack-engineer/scripts/code_quality_analyzer.py /path/to/project
python engineering-team/fullstack-engineer/scripts/code_quality_analyzer.py /path/to/project --json

# Fullstack Engineer - Rapid scaffolding
python engineering-team/fullstack-engineer/scripts/fullstack_scaffolder.py my-app --stack nextjs-graphql
```

### Development Environment

No build system, package managers, or test frameworks currently exist. This is intentional - skills are designed to be lightweight and dependency-free.

**If adding dependencies**:
- Keep scripts runnable with minimal setup (`pip install package` at most)
- Document all dependencies in SKILL.md
- Prefer standard library implementations over external packages

## Working with Skills

### Creating New Skills

Follow the appropriate roadmap for your skill domain. When adding a new skill:

**For Marketing Skills:**
1. Create skill folder: `marketing-skill/{skill-name}/`
2. Copy structure from `content-creator/` as template
3. Follow roadmap in `marketing-skill/marketing_skills_roadmap.md`

**For C-Level Advisory Skills:**
1. Create skill folder: `c-level-advisor/{role}-advisor/`
2. Copy structure from `ceo-advisor/` or `cto-advisor/`
3. Focus on strategic decision-making tools

**For Product Team Skills:**
1. Create skill folder: `product-team/{skill-name}/`
2. Copy structure from `product-manager-toolkit/` as template
3. Follow guide in `product-team/product_team_implementation_guide.md`

**For Engineering Team Skills:**
1. Create skill folder: `engineering-team/{skill-name}/`
2. Copy structure from `fullstack-engineer/` as template
3. Follow guide in `engineering-team/engineering_skills_roadmap.md`

**Universal Process:**
1. Write SKILL.md first (defines workflows before building tools)
2. Build Python scripts if algorithmic analysis is needed
3. Curate reference knowledge bases (frameworks, templates)
4. Create user-facing templates and examples
5. Package as .zip for distribution

**Quality Standard**: Each skill should save users 40%+ time while improving consistency/quality by 30%+.

### Editing Existing Skills

**SKILL.md**: This is the master document users read first. Changes here impact user workflows directly.

**Scripts**: Pure logic implementation. No LLM calls, no external APIs (keeps skills portable and fast).

**References**: Expert knowledge curation. Focus on actionable checklists, specific metrics, and platform-specific details.

**Critical**: Maintain consistency across all markdown files. Use the same voice, formatting, and structure patterns established in content-creator.

## Git Workflow

The repository follows a domain-based branching strategy. Recommended workflow:

```bash
# Feature branches by domain
git checkout -b feature/marketing/seo-optimizer
git checkout -b feature/product/ux-research-tools
git checkout -b feature/c-level/cfo-advisor

# Semantic versioning by skill
git tag v1.0-content-creator
git tag v1.0-product-manager-toolkit
git tag v1.0-ceo-advisor

# Commit message conventions
feat(content-creator): add LinkedIn content framework
feat(product-manager): add RICE prioritization script
fix(agile-product-owner): correct sprint capacity calculation
docs(ux-researcher): update persona generation guide
refactor(ui-design-system): improve token generator performance
```

**Current State:**
- 34 skills deployed across 5 domains
- 94 Python automation tools
- All skills v1.0 production-ready
- Complete engineering suite with 14 specialized roles (9 core + 5 AI/ML/Data)
- Complete RA/QM suite with 12 specialized roles for HealthTech/MedTech compliance

**.gitignore excludes**: .vscode/, .DS_Store, AGENTS.md, PROMPTS.md, .env* (CLAUDE.md is tracked as living documentation)

## Roadmap Context

**Current Status: Phase 1 Complete** - 34 production-ready skills deployed

**Delivered Skills:**
- **Marketing (1):** content-creator
- **C-Level Advisory (2):** ceo-advisor, cto-advisor
- **Product Team (5):** product-manager-toolkit, agile-product-owner, product-strategist, ux-researcher-designer, ui-design-system
- **Engineering Team (14):**
  - Core Engineering (9): senior-architect, senior-frontend, senior-backend, senior-fullstack, senior-qa, senior-devops, senior-secops, code-reviewer, senior-security
  - AI/ML/Data (5): senior-data-scientist, senior-data-engineer, senior-ml-engineer, senior-prompt-engineer, senior-computer-vision
- **Regulatory Affairs & Quality Management (12):**
  - Strategic: regulatory-affairs-head, quality-manager-qmr
  - Quality Systems: quality-manager-qms-iso13485, capa-officer, quality-documentation-manager
  - Risk & Security: risk-management-specialist, information-security-manager-iso27001
  - Regulatory: mdr-745-specialist, fda-consultant-specialist
  - Audit: qms-audit-expert, isms-audit-expert, gdpr-dsgvo-expert

**Total Automation:**
- **94 Python automation tools** (34 skills × 2.8 avg tools per skill)
- **90+ comprehensive reference guides** with patterns and best practices
- **Complete enterprise coverage** from marketing through regulatory compliance

**Next Priorities:**
- Phase 2 (Q1 2026): Marketing expansion - SEO optimizer, social media manager, campaign analytics
- Phase 3 (Q2 2026): Business & growth - Sales engineer, customer success, growth marketer
- Phase 4 (Q3 2026): Specialized domains - Mobile, blockchain, web3, finance

**Target: 40+ skills by Q3 2026**

See detailed roadmaps:
- `marketing-skill/marketing_skills_roadmap.md`
- `product-team/product_team_implementation_guide.md`
- `engineering-team/START_HERE.md` and `TEAM_STRUCTURE_GUIDE.md`
- `ra-qm-team/README.md` and `final-complete-skills-collection.md`

## Key Principles

1. **Skills are products**: Each skill should be deployable as a standalone package
2. **Documentation-driven**: Success depends on clear, actionable documentation
3. **Algorithm over AI**: Use deterministic analysis (code) rather than LLM calls when possible
4. **Template-heavy**: Provide ready-to-use templates users can customize
5. **Platform-specific**: Generic advice is less valuable than specific platform best practices

## Anti-Patterns to Avoid

- Creating dependencies between skills (keep each self-contained)
- Adding complex build systems or test frameworks (maintain simplicity)
- Generic marketing advice (focus on specific, actionable frameworks)
- LLM calls in scripts (defeats the purpose of portable, fast analysis tools)
- Over-documenting file structure (skills are simple by design)
