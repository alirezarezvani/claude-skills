# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a **comprehensive skills library** for Claude AI - reusable, production-ready skill packages that bundle domain expertise, best practices, analysis tools, and strategic frameworks across marketing, executive leadership, and product development. The repository provides modular skills that teams can download and use directly in their workflows.

**Current Scope:** 8 production-ready skills across 3 domains:
- **Marketing:** Content creation, SEO, brand voice, social media
- **C-Level Advisory:** CEO strategic planning, CTO technical leadership
- **Product Team:** Product management, agile delivery, UX research, UI design, strategic planning

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
- 4 commits total
- 8 skills deployed across 3 domains
- All skills v1.0 production-ready

**.gitignore excludes**: .vscode/, .DS_Store, AGENTS.md, PROMPTS.md, .env* (CLAUDE.md is tracked as living documentation)

## Roadmap Context

**Current Status: Phase 1 Complete** - 8 production-ready skills deployed

**Delivered Skills:**
- **Marketing (1):** content-creator
- **C-Level Advisory (2):** ceo-advisor, cto-advisor
- **Product Team (5):** product-manager-toolkit, agile-product-owner, product-strategist, ux-researcher-designer, ui-design-system

**Next Priorities:**
- Phase 2 (Q1 2026): Marketing expansion - SEO optimizer, social media manager, campaign analytics
- Phase 3 (Q2 2026): Engineering & ops - DevOps engineer, security engineer, data engineer
- Phase 4 (Q3 2026): Business & growth - Sales engineer, customer success, growth marketer

**Target: 18+ skills by Q3 2026**

See detailed roadmaps:
- `marketing-skill/marketing_skills_roadmap.md`
- `product-team/product_team_implementation_guide.md`

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
