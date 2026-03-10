# Product Team Skills - Claude Code Guidance

This guide covers the 8 production-ready product management skills and their Python automation tools.

## Product Skills Overview

**Available Skills:**
1. **product-manager-toolkit/** - RICE prioritization, customer interview analysis (2 tools)
2. **agile-product-owner/** - User story generation, sprint planning (1 tool)
3. **product-strategist/** - OKR cascade, strategic planning (1 tool)
4. **ux-researcher-designer/** - Persona generation, user research (1 tool)
5. **ui-design-system/** - Design token generation, component systems (1 tool)
6. **competitive-teardown/** - Competitive matrix building, gap analysis (1 tool)
7. **landing-page-generator/** - Landing page scaffolding (1 tool)
8. **saas-scaffolder/** - SaaS project bootstrapping (1 tool)

**Total Tools:** 9 Python automation tools

**Agents:** 4 (cs-product-manager, cs-agile-product-owner, cs-product-strategist, cs-ux-researcher)

**Slash Commands:** 5 (/rice, /okr, /persona, /user-story, /competitive-matrix)

## Python Automation Tools

### 1. RICE Prioritizer (`product-manager-toolkit/scripts/rice_prioritizer.py`)

**Purpose:** RICE framework implementation for feature prioritization

**Formula:** (Reach × Impact × Confidence) / Effort

**Features:**
- Portfolio analysis (quick wins vs big bets)
- Quarterly roadmap generation
- Capacity planning (story points or dev days)
- CSV input/output for Jira/Linear integration
- JSON export for dashboards

**Usage:**
```bash
# Basic prioritization
python product-manager-toolkit/scripts/rice_prioritizer.py features.csv

# With capacity planning
python product-manager-toolkit/scripts/rice_prioritizer.py features.csv --capacity 20

# JSON output
python product-manager-toolkit/scripts/rice_prioritizer.py features.csv --output json
```

**CSV Format:**
```csv
feature,reach,impact,confidence,effort
User Dashboard,500,3,0.8,5
API Rate Limiting,1000,2,0.9,3
Dark Mode,300,1,1.0,2
```

### 2. Customer Interview Analyzer (`product-manager-toolkit/scripts/customer_interview_analyzer.py`)

**Purpose:** NLP-based interview transcript analysis

**Features:**
- Pain point extraction with severity scoring
- Feature request identification
- Sentiment analysis
- Theme extraction
- Jobs-to-be-done pattern recognition

**Usage:**
```bash
# Analyze transcript
python product-manager-toolkit/scripts/customer_interview_analyzer.py interview.txt

# JSON output
python product-manager-toolkit/scripts/customer_interview_analyzer.py interview.txt json
```

### 3. User Story Generator (`agile-product-owner/scripts/user_story_generator.py`)

**Purpose:** INVEST-compliant user story generation

**Features:**
- Sprint planning with capacity allocation
- Epic breakdown into deliverable stories
- Acceptance criteria generation
- Story point estimation
- Priority scoring

**Usage:**
```bash
# Interactive mode
python agile-product-owner/scripts/user_story_generator.py

# Sprint planning (30 story points)
python agile-product-owner/scripts/user_story_generator.py sprint 30
```

**Output Format:**
```
US-001: As a user, I want to...
Priority: High | Points: 5
Acceptance Criteria:
- Given... When... Then...
```

### 4. OKR Cascade Generator (`product-strategist/scripts/okr_cascade_generator.py`)

**Purpose:** Automated OKR hierarchy (company → product → team)

**Features:**
- Alignment scoring (vertical and horizontal)
- Strategy templates (growth, retention, revenue, innovation)
- Key result tracking
- Progress visualization

**Usage:**
```bash
# Growth strategy OKRs
python product-strategist/scripts/okr_cascade_generator.py growth

# Retention strategy
python product-strategist/scripts/okr_cascade_generator.py retention
```

### 5. Persona Generator (`ux-researcher-designer/scripts/persona_generator.py`)

**Purpose:** Data-driven persona creation from user research

**Features:**
- Demographic and psychographic profiling
- Goals, pain points, and behavior patterns
- User journey mapping integration
- Empathy map generation

**Usage:**
```bash
# Interactive persona creation
python ux-researcher-designer/scripts/persona_generator.py

# JSON export
python ux-researcher-designer/scripts/persona_generator.py --output json
```

### 6. Design Token Generator (`ui-design-system/scripts/design_token_generator.py`)

**Purpose:** Complete design token system from brand color

**Features:**
- Color palette generation (primary, secondary, neutrals)
- Typography scale (font sizes, line heights, weights)
- Spacing system (4px/8px grid)
- Shadow and elevation tokens
- Export formats: CSS, JSON, SCSS

**Usage:**
```bash
# Generate design tokens
python ui-design-system/scripts/design_token_generator.py "#0066CC" modern css

# SCSS output
python ui-design-system/scripts/design_token_generator.py "#0066CC" modern scss

# JSON for Figma integration
python ui-design-system/scripts/design_token_generator.py "#0066CC" modern json
```

### 7. Competitive Matrix Builder (`competitive-teardown/scripts/competitive_matrix_builder.py`)

**Purpose:** Weighted competitive scoring with gap analysis

**Usage:**
```bash
python competitive-teardown/scripts/competitive_matrix_builder.py competitors.json
```

### 8. Landing Page Scaffolder (`landing-page-generator/scripts/landing_page_scaffolder.py`)

**Purpose:** Generate production-ready landing pages as Next.js/React TSX components with Tailwind CSS (default) or plain HTML.

**Features:**
- TSX output (default): Next.js 14+ App Router components with Tailwind classes
- 4 design styles: `dark-saas`, `clean-minimal`, `bold-startup`, `enterprise`
- 7 section generators: nav, hero, features, testimonials, pricing, CTA, footer
- Copy frameworks: PAS, AIDA, BAB
- SEO metadata export
- HTML output preserved via `--format html`

**Usage:**
```bash
# TSX output (default) with design style
python landing-page-generator/scripts/landing_page_scaffolder.py config.json --format tsx

# HTML output
python landing-page-generator/scripts/landing_page_scaffolder.py config.json --format html

# JSON manifest (dry run)
python landing-page-generator/scripts/landing_page_scaffolder.py config.json --format json
```

**Config JSON format:**
```json
{
  "product_name": "Acme",
  "tagline": "Ship faster. Break less.",
  "design_style": "dark-saas",
  "copy_framework": "PAS",
  "sections": ["nav", "hero", "features", "pricing", "cta", "footer"],
  "features": [
    {"title": "Fast deploys", "description": "Zero-downtime deployments"}
  ],
  "pricing": [
    {"name": "Free", "price": "$0/mo", "features": ["5 projects"]},
    {"name": "Pro", "price": "$29/mo", "features": ["Unlimited"], "highlighted": true}
  ]
}
```

**Brand Voice Integration:** Before generating copy, run the brand voice analyzer to establish tone and formality:
```bash
# 1. Analyze existing brand content to establish voice profile
python ../marketing-skill/content-production/scripts/brand_voice_analyzer.py brand_samples.txt --format json > voice_profile.json

# 2. Use the voice profile (formality, tone, perspective) to guide copy framework selection
# 3. Generate landing page with matching style
python landing-page-generator/scripts/landing_page_scaffolder.py config.json --format tsx
```

### 9. Project Bootstrapper (`saas-scaffolder/scripts/project_bootstrapper.py`)

**Purpose:** SaaS project scaffolding with auth, billing, and API setup

**Usage:**
```bash
python saas-scaffolder/scripts/project_bootstrapper.py project_config.json
```

## Product Workflows

### Workflow 1: Feature Prioritization

```bash
# 1. Collect feature requests
cat feature-requests.csv

# 2. Run RICE prioritization
python product-manager-toolkit/scripts/rice_prioritizer.py features.csv --capacity 30

# 3. Generate quarterly roadmap

# 4. Create user stories for top priorities
python agile-product-owner/scripts/user_story_generator.py sprint 30
```

### Workflow 2: User Research to Product

```bash
# 1. Conduct user interviews

# 2. Analyze transcripts
python product-manager-toolkit/scripts/customer_interview_analyzer.py interview-001.txt

# 3. Generate personas
python ux-researcher-designer/scripts/persona_generator.py

# 4. Create OKRs based on insights
python product-strategist/scripts/okr_cascade_generator.py growth
```

### Workflow 3: Sprint Planning

```bash
# 1. Set sprint capacity (story points)
CAPACITY=30

# 2. Generate user stories
python agile-product-owner/scripts/user_story_generator.py sprint $CAPACITY

# 3. Export to Jira (via JSON)
python product-manager-toolkit/scripts/rice_prioritizer.py features.csv --output json > priorities.json
```

### Workflow 4: Brand-Aligned Landing Page

This workflow connects the marketing brand voice skill with the landing page generator to ensure copy consistency.

```bash
# 1. Analyze existing brand content for voice profile
python ../marketing-skill/content-production/scripts/brand_voice_analyzer.py website_copy.txt --format json > voice.json
# Output: formality (formal/casual), tone (professional/friendly), perspective (authoritative/conversational)

# 2. Map voice profile to design style + copy framework:
#    - formal + professional → enterprise style, AIDA framework
#    - casual + friendly → bold-startup style, BAB framework
#    - professional + authoritative → dark-saas style, PAS framework
#    - casual + conversational → clean-minimal style, BAB framework

# 3. Generate design tokens for brand consistency
python ui-design-system/scripts/design_token_generator.py "#0066CC" modern css

# 4. Generate the landing page
python landing-page-generator/scripts/landing_page_scaffolder.py config.json --format tsx

# 5. Run competitive teardown to refine positioning
python competitive-teardown/scripts/competitive_matrix_builder.py competitors.json
```

## Integration Patterns

### Jira Integration

All tools support JSON output for Jira import:

```bash
# Export prioritized features
python product-manager-toolkit/scripts/rice_prioritizer.py features.csv --output json > jira-import.json
```

### Figma Integration

Design tokens export for Figma plugins:

```bash
# Generate tokens
python ui-design-system/scripts/design_token_generator.py "#0066CC" modern json > design-tokens.json
```

### Confluence Documentation

Use persona generator output for user documentation:

```bash
python ux-researcher-designer/scripts/persona_generator.py --output json > personas.json
```

## Quality Standards

**All product Python tools must:**
- CLI-first design for automation
- Support both interactive and batch modes
- JSON output for tool integration
- Standard library only (minimal dependencies)
- Actionable recommendations

## Cross-Domain Integration

### Brand Voice → Landing Page

The landing page generator integrates with the marketing brand voice analyzer (`marketing-skill/content-production/scripts/brand_voice_analyzer.py`) to ensure copy on generated pages matches the brand's established voice. The analyzer outputs formality, tone, and perspective dimensions which map to design style and copy framework choices. See Workflow 4 above.

### Design Tokens → Landing Page

Design tokens from `ui-design-system/scripts/design_token_generator.py` can be generated alongside landing pages to ensure consistent color, typography, and spacing across the product.

### Competitive Teardown → Landing Page

Competitive positioning from `competitive-teardown/scripts/competitive_matrix_builder.py` informs landing page messaging — use SWOT analysis to identify differentiation points and translate them into hero copy and feature sections.

## Additional Resources

- **Main Documentation:** `../CLAUDE.md`
- **Marketing Brand Voice:** `../marketing-skill/content-production/scripts/brand_voice_analyzer.py`

---

**Last Updated:** March 10, 2026
**Skills Deployed:** 8/8 product skills production-ready
**Total Tools:** 9 Python automation tools
**Agents:** 4 | **Commands:** 5
