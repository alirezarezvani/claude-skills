# Product Team Skills - Claude Code Guidance

This guide covers the 12 production-ready product management skills and their Python automation tools.

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
9. **product-analytics/** - KPI design, retention/cohort/funnel analysis (1 tool)
10. **experiment-designer/** - Experiment design and sample size planning (1 tool)
11. **product-discovery/** - Discovery frameworks and assumption mapping (1 tool)
12. **roadmap-communicator/** - Roadmap communication and changelog generation (1 tool)

**Total Tools:** 13 Python automation tools

**Agents:** 5 (cs-product-manager, cs-agile-product-owner, cs-product-strategist, cs-ux-researcher, cs-product-analyst)

**Slash Commands:** 7 (/rice, /okr, /persona, /user-story, /competitive-matrix, /prd, /sprint-plan)

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

**Usage:**
```bash
python ux-researcher-designer/scripts/persona_generator.py
python ux-researcher-designer/scripts/persona_generator.py --output json
```

### 6. Design Token Generator (`ui-design-system/scripts/design_token_generator.py`)

**Purpose:** Complete design token system from brand color

**Usage:**
```bash
python ui-design-system/scripts/design_token_generator.py "#0066CC" modern css
python ui-design-system/scripts/design_token_generator.py "#0066CC" modern scss
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

**Usage:**
```bash
python landing-page-generator/scripts/landing_page_scaffolder.py config.json --format tsx
python landing-page-generator/scripts/landing_page_scaffolder.py config.json --format html
```

### 9. Project Bootstrapper (`saas-scaffolder/scripts/project_bootstrapper.py`)

**Purpose:** SaaS project scaffolding with auth, billing, and API setup

**Usage:**
```bash
python saas-scaffolder/scripts/project_bootstrapper.py project_config.json
```

### 10. Metrics Calculator (`product-analytics/scripts/metrics_calculator.py`)

**Purpose:** Product analytics — retention, cohort, and funnel analysis

**Features:**
- Retention curve analysis from event data
- Funnel conversion tracking with stage-by-stage drop-off
- Cohort grouping and comparison

**Usage:**
```bash
# Retention analysis
python product-analytics/scripts/metrics_calculator.py retention events.csv

# Funnel analysis
python product-analytics/scripts/metrics_calculator.py funnel funnel.csv --stages visit,signup,activate,pay

# KPI summary
python product-analytics/scripts/metrics_calculator.py kpi metrics.csv --json
```

### 11. Sample Size Calculator (`experiment-designer/scripts/sample_size_calculator.py`)

**Purpose:** Statistical sample size planning for A/B tests and experiments

**Features:**
- Minimum detectable effect (MDE) calculation
- Absolute and relative effect size modes
- Power analysis with configurable alpha/beta

**Usage:**
```bash
# Absolute MDE
python experiment-designer/scripts/sample_size_calculator.py --baseline-rate 0.12 --mde 0.02 --mde-type absolute

# Relative MDE
python experiment-designer/scripts/sample_size_calculator.py --baseline-rate 0.12 --mde 0.15 --mde-type relative

# Custom power/significance
python experiment-designer/scripts/sample_size_calculator.py --baseline-rate 0.12 --mde 0.02 --alpha 0.01 --power 0.9
```

### 12. Assumption Mapper (`product-discovery/scripts/assumption_mapper.py`)

**Purpose:** Map and prioritize product assumptions for discovery validation

**Features:**
- Risk × uncertainty scoring for prioritization
- CSV input with structured assumption fields
- Categorization by assumption type (desirability, viability, feasibility, usability)

**Usage:**
```bash
python product-discovery/scripts/assumption_mapper.py assumptions.csv
python product-discovery/scripts/assumption_mapper.py assumptions.csv --json
```

### 13. Changelog Generator (`roadmap-communicator/scripts/changelog_generator.py`)

**Purpose:** Generate structured changelogs from git commit history

**Note:** Requires `git` on PATH — must be run inside a git repository.

**Usage:**
```bash
python roadmap-communicator/scripts/changelog_generator.py --from v1.0.0 --to HEAD
python roadmap-communicator/scripts/changelog_generator.py --from v1.0.0 --to v2.0.0 --json
```

## Product Workflows

### Workflow 1: Feature Prioritization to Sprint Execution

```bash
python product-manager-toolkit/scripts/rice_prioritizer.py features.csv --capacity 30
python agile-product-owner/scripts/user_story_generator.py sprint 30
```

### Workflow 2: Strategy to Team-Level OKRs

```bash
python product-strategist/scripts/okr_cascade_generator.py growth --json > okrs.json
```

### Workflow 3: Research to Persona Artifacts

```bash
python ux-researcher-designer/scripts/persona_generator.py json > personas.json
```

### Workflow 4: Brand-Aligned Landing Page

```bash
python ../marketing-skill/content-production/scripts/brand_voice_analyzer.py website_copy.txt --format json > voice.json
python ui-design-system/scripts/design_token_generator.py "#0066CC" modern css
python landing-page-generator/scripts/landing_page_scaffolder.py config.json --format tsx
python competitive-teardown/scripts/competitive_matrix_builder.py competitors.json
```

### Workflow 5: Product Analytics and Experimentation

```bash
python product-analytics/scripts/metrics_calculator.py retention events.csv
python product-analytics/scripts/metrics_calculator.py funnel funnel.csv --stages visit,signup,activate,pay
python experiment-designer/scripts/sample_size_calculator.py --baseline-rate 0.12 --mde 0.02 --mde-type absolute
```

### Workflow 6: Discovery and Opportunity Validation

```bash
python product-discovery/scripts/assumption_mapper.py assumptions.csv
```

### Workflow 7: Roadmap and Release Communication

```bash
python roadmap-communicator/scripts/changelog_generator.py --from v1.0.0 --to HEAD
```

## Quality Standards

**All product Python tools must:**
- CLI-first design for automation
- Support both interactive and batch modes
- JSON output for tool integration
- Standard library only (minimal dependencies)
- Actionable recommendations

## Additional Resources

- **Main Documentation:** `../CLAUDE.md`
- **Marketing Brand Voice:** `../marketing-skill/content-production/scripts/brand_voice_analyzer.py`

---

**Last Updated:** March 11, 2026
**Skills Deployed:** 12/12 product skills production-ready
**Total Tools:** 13 Python automation tools
**Agents:** 5 | **Commands:** 7
