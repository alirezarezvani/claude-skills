# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a **marketing skills library** for Claude AI - reusable, production-ready skill packages that bundle marketing best practices, analysis tools, and strategic frameworks. The repository provides modular skills (starting with `content-creator`) that marketing teams can download and use directly.

**Key Distinction**: This is NOT a traditional application. It's a library of skill packages meant to be extracted and deployed by users into their own Claude workflows.

## Architecture Overview

### Skill Package Structure

Each skill follows a consistent modular architecture:

```
marketing-skill/
└── {skill-name}/
    ├── SKILL.md                    # Master documentation: workflows, usage, best practices
    ├── scripts/                    # Python CLI tools for analysis/optimization
    ├── references/                 # Knowledge bases: frameworks, guidelines, templates
    └── assets/                     # Reusable templates for end users
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
```

### Development Environment

No build system, package managers, or test frameworks currently exist. This is intentional - skills are designed to be lightweight and dependency-free.

**If adding dependencies**:
- Keep scripts runnable with minimal setup (`pip install package` at most)
- Document all dependencies in SKILL.md
- Prefer standard library implementations over external packages

## Working with Skills

### Creating New Skills

Follow the roadmap in `marketing-skill/marketing_skills_roadmap.md`. When adding a new skill:

1. Create skill folder: `marketing-skill/{skill-name}/`
2. Copy structure from `content-creator/` as template
3. Write SKILL.md first (defines workflows before building tools)
4. Build scripts if algorithmic analysis is needed
5. Curate reference knowledge bases
6. Create user-facing templates in assets/

**Quality Standard**: Each skill should save users 40%+ time while improving consistency/quality by 30%+.

### Editing Existing Skills

**SKILL.md**: This is the master document users read first. Changes here impact user workflows directly.

**Scripts**: Pure logic implementation. No LLM calls, no external APIs (keeps skills portable and fast).

**References**: Expert knowledge curation. Focus on actionable checklists, specific metrics, and platform-specific details.

**Critical**: Maintain consistency across all markdown files. Use the same voice, formatting, and structure patterns established in content-creator.

## Git Workflow

Repository is initialized but has no commits yet. Recommended workflow:

```bash
# Feature branches for new skills
git checkout -b feature/seo-optimizer-skill

# Semantic versioning by skill
git tag v1.0-content-creator
git tag v1.0-seo-optimizer

# Commit messages
feat(content-creator): add LinkedIn content framework
fix(seo-optimizer): correct keyword density calculation
docs(social-media): update TikTok best practices
```

**.gitignore excludes**: .vscode/, CLAUDE.md, AGENTS.md, PROMPTS.md, .env* (these are user-specific configuration files)

## Roadmap Context

Current status: **Phase 1 Complete** (content-creator skill ready for deployment)

Next priorities:
- Phase 2 (Weeks 3-6): seo-optimizer, social-media-manager, campaign-analytics skills
- Phase 3 (Weeks 7-10): email-marketing, paid-ads-manager, competitor-intelligence skills
- Phase 4 (Weeks 11-12): conversion-optimizer, influencer-outreach skills

See `marketing-skill/marketing_skills_roadmap.md` for detailed implementation plan and ROI projections.

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
