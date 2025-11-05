# Product Team Skills - Claude Code Guidance

This guide covers the 5 production-ready product management skills and their Python automation tools.

## Product Skills Overview

**Available Skills:**
1. **product-manager-toolkit/** - RICE prioritization, customer interview analysis (2 tools)
2. **agile-product-owner/** - User story generation, sprint planning (1 tool)
3. **product-strategist/** - OKR cascade, strategic planning (1 tool)
4. **ux-researcher-designer/** - Persona generation, user research (1 tool)
5. **ui-design-system/** - Design token generation, component systems (1 tool)

**Total Tools:** 6 Python automation tools

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

## Roadmap

**Current (Phase 1):** 5 skills deployed with 6 tools

**Phase 2 (Q1 2026):** Product analytics
- A/B test analyzer
- Funnel conversion tracker
- Cohort retention analyzer

**Phase 3 (Q2 2026):** Advanced PM tools
- Competitive analysis framework
- Product-market fit assessment
- Revenue impact calculator

See `product_team_implementation_guide.md` for detailed plans.

## Additional Resources

- **Implementation Guide:** `product_team_implementation_guide.md`
- **Real-World Scenario:** `REAL_WORLD_SCENARIO.md` (if exists)
- **Main Documentation:** `../CLAUDE.md`

---

**Last Updated:** November 5, 2025
**Skills Deployed:** 5/5 product skills production-ready
**Total Tools:** 6 Python automation tools
