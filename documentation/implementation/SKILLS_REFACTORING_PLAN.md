# Claude Skills Systematic Refactoring Plan

**Goal:** Optimize all 36 skills to follow Anthropic's official best practices while maintaining comprehensive domain expertise.

**Approach:** Phased refinement with metadata enhancement integrated throughout.

**Timeline:** 4 weeks (progressive implementation)

**Expected Outcome:** Better Claude activation, faster loading, clearer skill discovery, professional metadata.

---

## 📋 Table of Contents

- [Executive Summary](#executive-summary)
- [Refactoring Principles](#refactoring-principles)
- [Phase 1: Foundation Enhancement](#phase-1-foundation-enhancement-week-1)
- [Phase 2: Pilot Optimization](#phase-2-pilot-optimization-week-2)
- [Phase 3: Full Rollout](#phase-3-full-rollout-week-3)
- [Phase 4: Validation & Documentation](#phase-4-validation--documentation-week-4)
- [Before/After Examples](#beforeafter-examples)
- [Implementation Checklist](#implementation-checklist)

---

## 📊 Executive Summary

### Current State Analysis

**Strengths:**
- ✅ 36 production-ready skills with comprehensive domain expertise
- ✅ 97 Python automation tools
- ✅ Excellent reference materials and frameworks
- ✅ Real-world benchmarks and best practices

**Optimization Opportunities:**
- ⚠️ SKILL.md files too long (200-1,000 lines vs. recommended 50-200)
- ⚠️ Missing metadata (license, version, category)
- ⚠️ No keywords sections for better discovery
- ⚠️ Not using allowed-tools for security/safety
- ⚠️ Some skills too broad (covering multiple capabilities)

### Expected Improvements

**After Refactoring:**
- ✅ Faster skill loading (50-70% reduction in SKILL.md size)
- ✅ Better Claude activation (clearer triggers)
- ✅ Professional metadata (license, versioning, categorization)
- ✅ Enhanced discovery (keywords sections)
- ✅ Safer execution (allowed-tools restrictions)
- ✅ Maintained expertise (moved to references/, not deleted)

**ROI:**
- Implementation time: ~40 hours
- Benefit: Permanent improvement to all 36 skills
- User impact: Better Claude performance, clearer documentation

---

## 🎯 Refactoring Principles

### Following Anthropic's Official Pattern

1. **Focused Scope** - One skill = one clear capability (not entire domains)
2. **Lean SKILL.md** - 50-200 lines (core instructions only)
3. **Progressive Disclosure** - Metadata → SKILL.md → References → Scripts
4. **Rich Descriptions** - What + When + Triggers + Keywords
5. **Proper Metadata** - License, version, category tracking
6. **Tool Restrictions** - Use allowed-tools for safety when appropriate
7. **Keywords Section** - Help users discover skills

### What NOT to Change

- ✅ Keep all Python scripts (they're excellent)
- ✅ Keep all reference materials (move to references/)
- ✅ Keep all frameworks and benchmarks
- ✅ Keep domain expertise (just reorganize)
- ✅ Keep current folder structure (already good)

### Optimization Strategy

**Move FROM SKILL.md:**
- Detailed frameworks (reference in 1-2 sentences, full content in references/)
- Extensive examples (keep 1-2, move rest to references/examples.md)
- Long procedural guides (summarize, detail in references/)
- Comprehensive checklists (link to references/)

**Keep IN SKILL.md:**
- Quick start guide (3-5 examples)
- Core workflow overview (high-level steps)
- When to use each script/reference (pointers)
- Essential decision points
- Keywords for discovery

---

## Phase 1: Foundation Enhancement (Week 1)

**Goal:** Add professional metadata and discovery aids to all 36 skills

**Time:** ~20 hours (30 min per skill × 36 skills + 2 hours documentation)

### Task 1.1: Create Metadata Template

**File:** `.claude/skills-metadata-template.yaml`

```yaml
---
name: skill-name
description: [What it does in 1 sentence]. [Key capabilities in 1 sentence]. Use when [primary trigger], [secondary trigger], or when user mentions [keyword 1], [keyword 2], [keyword 3].
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing | c-level | product | engineering | regulatory
  domain: content | demand-gen | product-marketing | ceo-advisory | etc
  updated: 2025-10-20
  python-tools: script1.py, script2.py, script3.py
  tech-stack: HubSpot, GA4, React, etc (if applicable)
---
```

### Task 1.2: Update All Marketing Skills (3 skills, 1.5 hours)

**For each skill:**

#### content-creator

**Current:**
```yaml
---
name: content-creator
description: Comprehensive content marketing skill for creating blog posts, social media content, and SEO-optimized materials. Includes brand voice development, content templates, SEO analysis tools, and social media optimization strategies. Use when creating any marketing content, developing brand guidelines, optimizing for SEO, or planning content calendars.
---
```

**Enhanced:**
```yaml
---
name: content-creator
description: Create SEO-optimized marketing content with consistent brand voice. Includes brand voice analyzer, SEO optimizer, content frameworks, and social media templates. Use when writing blog posts, creating social media content, analyzing brand voice, optimizing SEO, planning content calendars, or when user mentions content creation, brand voice, SEO optimization, social media marketing, or content strategy.
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  domain: content-marketing
  updated: 2025-10-20
  python-tools: brand_voice_analyzer.py, seo_optimizer.py
  tech-stack: SEO, social-media-platforms
---

# Content Creator

...existing content with added keywords section...

## Keywords
content creation, blog posts, SEO, brand voice, social media, content calendar, marketing content, content strategy, content marketing, brand consistency, content optimization, social media marketing, content planning
```

#### marketing-demand-acquisition

**Enhanced:**
```yaml
---
name: marketing-demand-acquisition
description: Multi-channel demand generation, paid media optimization, SEO strategy, and partnership programs for Series A+ startups. Includes CAC calculator, channel playbooks, HubSpot integration, and international expansion tactics. Use when planning demand generation campaigns, optimizing paid media, building SEO strategies, establishing partnerships, or when user mentions demand gen, paid ads, LinkedIn ads, Google ads, CAC, acquisition, lead generation, or pipeline generation.
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  domain: demand-generation
  updated: 2025-10-20
  python-tools: calculate_cac.py
  tech-stack: HubSpot, LinkedIn-Ads, Google-Ads, Meta-Ads, SEO-tools
  target-market: B2B-SaaS, Series-A+
---

## Keywords
demand generation, paid media, paid ads, LinkedIn ads, Google ads, Meta ads, CAC, customer acquisition cost, lead generation, MQL, SQL, pipeline generation, acquisition strategy, performance marketing, paid social, paid search, partnerships, affiliate marketing, SEO strategy
```

#### marketing-strategy-pmm

**Enhanced:**
```yaml
---
name: marketing-strategy-pmm
description: Product marketing, positioning, GTM strategy, and competitive intelligence. Includes ICP definition, April Dunford positioning methodology, launch playbooks, competitive battlecards, and international market entry guides. Use when developing positioning, planning product launches, creating messaging, analyzing competitors, entering new markets, enabling sales, or when user mentions product marketing, positioning, GTM, go-to-market, competitive analysis, market entry, or sales enablement.
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  domain: product-marketing
  updated: 2025-10-20
  frameworks: April-Dunford, ICP-definition, messaging-hierarchy
  target-market: B2B-SaaS, international-expansion
---

## Keywords
product marketing, positioning, GTM, go-to-market strategy, competitive analysis, competitive intelligence, battlecards, ICP, ideal customer profile, messaging, value proposition, product launch, market entry, international expansion, sales enablement, win loss analysis
```

### Task 1.3: Update All C-Level Skills (2 skills, 1 hour)

#### ceo-advisor

```yaml
---
name: ceo-advisor
description: Executive leadership guidance for strategic decision-making, organizational development, and stakeholder management. Includes strategy analyzer, financial scenario modeling, board governance, and investor relations frameworks. Use when planning strategy, modeling financial scenarios, preparing board presentations, managing investors, developing culture, or when user mentions strategic planning, board meetings, investor updates, organizational culture, or executive decisions.
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: c-level
  domain: ceo-leadership
  updated: 2025-10-20
  python-tools: strategy_analyzer.py, financial_scenario_analyzer.py
---

## Keywords
CEO, executive leadership, strategic planning, board governance, investor relations, financial modeling, organizational culture, stakeholder management, executive decisions, board presentations, strategic initiatives
```

#### cto-advisor

```yaml
---
name: cto-advisor
description: Technical leadership guidance for engineering teams, architecture decisions, and technology strategy. Includes tech debt analyzer, team scaling calculator, engineering metrics, technology evaluation, and ADR templates. Use when assessing technical debt, scaling engineering teams, evaluating technologies, making architecture decisions, or when user mentions tech debt, engineering metrics, team scaling, technology selection, or architecture decisions.
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: c-level
  domain: cto-leadership
  updated: 2025-10-20
  python-tools: tech_debt_analyzer.py, team_scaling_calculator.py
  frameworks: DORA-metrics, architecture-decision-records
---

## Keywords
CTO, technical leadership, tech debt, technical debt, engineering team, team scaling, architecture decisions, technology evaluation, engineering metrics, DORA metrics, ADR, architecture decision records, technology strategy
```

### Task 1.4: Update All Product Team Skills (5 skills, 2.5 hours)

**Standard metadata template for product skills:**
```yaml
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: product
  domain: [product-management|agile-delivery|product-strategy|ux-research|ui-design]
  updated: 2025-10-20
  python-tools: [specific tools]
```

**Keywords sections to add:**

- product-manager-toolkit: `product management, RICE, prioritization, feature prioritization, customer interviews, PRD, product requirements, product discovery, user research, product metrics`

- agile-product-owner: `agile, product owner, user stories, sprint planning, backlog, velocity, acceptance criteria, sprint execution, scrum, agile ceremonies`

- product-strategist: `product strategy, OKR, objectives and key results, product vision, roadmap, strategic planning, product positioning, team organization`

- ux-researcher-designer: `UX research, user research, personas, journey mapping, usability testing, design thinking, user interviews, research synthesis`

- ui-design-system: `UI design, design system, design tokens, component library, design consistency, visual design, responsive design, design handoff`

### Task 1.5: Update All Engineering Skills (14 skills, 7 hours)

**Add to all engineering core skills:**
```yaml
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: engineering
  domain: [architecture|frontend|backend|fullstack|qa|devops|secops|review|security]
  updated: 2025-10-20
  python-tools: [specific tools]
  tech-stack: React, Next.js, Node.js, PostgreSQL, etc
```

**Add allowed-tools where appropriate:**

- **senior-architect:** `allowed-tools: Read, Grep, Glob, Bash` (analysis-heavy)
- **code-reviewer:** `allowed-tools: Read, Grep, Glob` (read-only review)
- **senior-qa:** `allowed-tools: Read, Bash` (testing execution)

**AI/ML/Data skills metadata:**
```yaml
category: engineering
domain: [data-science|data-engineering|ml-ops|prompt-engineering|computer-vision]
tech-stack: PyTorch, TensorFlow, Spark, Airflow, etc
```

### Task 1.6: Update All RA/QM Skills (12 skills, 6 hours)

**Add to all RA/QM skills:**
```yaml
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: regulatory-quality
  domain: [regulatory|quality-management|risk|security|audit|compliance]
  updated: 2025-10-20
  python-tools: [specific tools]
  compliance-frameworks: [ISO-13485|ISO-14971|ISO-27001|EU-MDR|FDA-QSR|GDPR]
  industry: HealthTech, MedTech
---
```

**Add allowed-tools for audit skills:**
- **qms-audit-expert:** `allowed-tools: Read, Grep, Glob` (read-only audit)
- **isms-audit-expert:** `allowed-tools: Read, Grep, Glob` (read-only audit)

---

## Phase 2: Pilot Optimization (Week 2)

**Goal:** Refine 3 representative skills as proof of concept

**Time:** ~12 hours (4 hours per skill)

**Selected Pilot Skills:**
1. **content-creator** (Marketing) - 236 lines → target 120 lines
2. **product-manager-toolkit** (Product) - 352 lines → target 150 lines
3. **senior-fullstack** (Engineering) - Estimate ~300 lines → target 150 lines

### Task 2.1: Refactor content-creator Skill

**Current Issues:**
- 236 lines (good but can be better)
- Contains full brand voice framework details
- Extensive social media platform guidance
- Many detailed examples

**Refactoring Steps:**

#### Step 1: Enhanced Frontmatter (Already done in Phase 1)

#### Step 2: Add Keywords Section
```markdown
# Content Creator

Professional-grade brand voice analysis, SEO optimization, and platform-specific content frameworks.

## Keywords
content creation, blog posts, SEO, brand voice, social media, content calendar, marketing content, content strategy, content marketing, brand consistency, content optimization, social media marketing, content planning, blog writing, content frameworks, brand guidelines, social media strategy
```

#### Step 3: Slim Down SKILL.md

**Current Structure (236 lines):**
- Quick Start: 15 lines
- Core Workflows: 120 lines (4 workflows with details)
- Key Scripts: 40 lines
- Reference Documents: 25 lines
- Best Practices: 36 lines

**Refined Structure (120 lines):**
- Quick Start: 15 lines (keep as-is)
- Core Workflows: 40 lines (overview only, point to references)
- Key Scripts: 20 lines (essentials only)
- Reference Documents: 15 lines (clear pointers)
- Best Practices: 15 lines (top 5 only)
- Keywords: 5 lines
- Examples: 10 lines (2 concrete examples)

**Moved to References:**

Create new reference files:
- `references/brand-voice-detailed-framework.md` - Move detailed archetype descriptions
- `references/social-media-platform-deep-dive.md` - Move platform-specific details
- `references/content-creation-examples.md` - Move extensive examples

**Updated SKILL.md Content:**
```markdown
### Establishing Brand Voice

1. **Analyze Existing Content**
   ```bash
   python scripts/brand_voice_analyzer.py existing_content.txt
   ```

2. **Define Voice Attributes**
   - Review personality archetypes in references/brand-voice-detailed-framework.md
   - Select primary and secondary archetypes
   - Document chosen voice

3. **Create Consistent Content**
   - Apply voice across all content
   - Verify consistency with analyzer

For complete brand voice framework including all 5 archetypes, tone dimensions, and implementation guide, see [references/brand-voice-detailed-framework.md](references/brand-voice-detailed-framework.md).
```

#### Step 4: Create New Reference Files

**references/brand-voice-detailed-framework.md** (New file, ~150 lines)
- Move all archetype details here
- Full tone attribute framework
- Extensive voice samples
- Implementation checklists

**references/social-media-platform-deep-dive.md** (New file, ~200 lines)
- Move all platform-specific details
- Posting time recommendations
- Character limits and formats
- Algorithm optimization tactics

**references/content-creation-examples.md** (New file, ~100 lines)
- 10+ complete content examples
- Before/after SEO optimization
- Various content types

---

### Task 2.2: Refactor product-manager-toolkit Skill

**Current Issues:**
- 352 lines (too long)
- Covers RICE + Interviews + PRDs + Discovery + Metrics
- Multiple distinct workflows

**Refactoring Steps:**

#### Step 1: Enhanced Frontmatter (Already done in Phase 1)

#### Step 2: Add Keywords
```markdown
## Keywords
product management, RICE prioritization, feature prioritization, customer interviews, user research, PRD, product requirements document, product discovery, customer discovery, product metrics, north star metric, product strategy, backlog prioritization, roadmap planning
```

#### Step 3: Slim Down SKILL.md

**Current: 352 lines → Target: 150 lines**

**Keep in SKILL.md:**
- Quick start (3 commands)
- High-level workflow overview
- Script usage basics
- Pointers to references

**Move to References:**
- Detailed RICE methodology → `references/rice-prioritization-guide.md`
- Interview frameworks → `references/customer-discovery-methods.md`
- Full PRD templates → Already in references/ ✅
- Extensive metrics frameworks → `references/product-metrics-frameworks.md`

**Refined Structure:**
```markdown
# Product Manager Toolkit

## Keywords
[as above]

## Quick Start

Three core capabilities, pick yours:

### Feature Prioritization
```bash
python scripts/rice_prioritizer.py features.csv --capacity 20
```

### Interview Analysis
```bash
python scripts/customer_interview_analyzer.py transcript.txt
```

### PRD Creation
Use templates from references/prd_templates.md

## Core Workflows

### 1. Feature Prioritization
Score features with RICE framework:
1. Gather feature requests
2. Score with RICE (Reach × Impact × Confidence / Effort)
3. Generate roadmap

For complete RICE methodology, see [references/rice-prioritization-guide.md](references/rice-prioritization-guide.md).

### 2. Customer Discovery
Extract insights from interviews:
1. Conduct interviews
2. Analyze with customer_interview_analyzer.py
3. Synthesize findings

For interview frameworks and methodologies, see [references/customer-discovery-methods.md](references/customer-discovery-methods.md).

### 3. PRD Development
Document requirements:
1. Choose template from references/prd_templates.md
2. Fill sections based on discovery
3. Collaborate with stakeholders

## Scripts

### rice_prioritizer.py
Calculate RICE scores and generate roadmaps.
- Usage: `python scripts/rice_prioritizer.py features.csv --capacity 20`
- Output: Prioritized list, portfolio analysis, roadmap

### customer_interview_analyzer.py
Extract insights from interview transcripts.
- Usage: `python scripts/customer_interview_analyzer.py transcript.txt`
- Output: Pain points, feature requests, themes, sentiment

## References

- **rice-prioritization-guide.md** - Complete RICE methodology
- **customer-discovery-methods.md** - Interview frameworks, synthesis
- **prd_templates.md** - 4 PRD formats with examples
- **product-metrics-frameworks.md** - North Star, funnel analysis, feature metrics

## Best Practices

- Start with customer problems, not solutions
- Use RICE for objective prioritization
- Keep PRDs focused on "why" not "how"
- Measure everything: adoption, frequency, retention

## Examples

### Example 1: Quarterly Planning
User: "Help me prioritize our backlog for Q1"
1. Export features to CSV
2. Run rice_prioritizer.py with team capacity
3. Review portfolio balance (quick wins vs big bets)

### Example 2: Interview Synthesis
User: "Analyze these 5 customer interviews"
1. Run analyzer on each transcript
2. Identify common themes across interviews
3. Map to opportunity areas
```

**Result:** 150 lines (58% reduction from 352)

---

### Task 2.3: Refactor senior-fullstack Skill

**Refactoring Steps:**

#### Step 1: Enhanced Frontmatter

```yaml
---
name: senior-fullstack
description: End-to-end application development with Next.js, GraphQL, PostgreSQL stack. Includes project scaffolder, code quality analyzer, architecture patterns, and complete development workflows. Use when building fullstack applications, scaffolding new projects, analyzing code quality, implementing architecture patterns, or when user mentions fullstack development, Next.js projects, code quality analysis, or project setup.
license: MIT
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: engineering
  domain: fullstack-development
  updated: 2025-10-20
  python-tools: fullstack_scaffolder.py, project_scaffolder.py, code_quality_analyzer.py
  tech-stack: Next.js, React, GraphQL, PostgreSQL, Node.js, TypeScript, Docker
---
```

#### Step 2: Add Keywords
```markdown
## Keywords
fullstack development, fullstack engineer, Next.js, React, GraphQL, PostgreSQL, project scaffolding, code quality analysis, architecture patterns, TypeScript, Node.js, fullstack project, end-to-end development, project setup, code analysis, quality metrics
```

#### Step 3: Slim Down SKILL.md

**Estimated Current: ~300 lines → Target: 150 lines**

**Keep:**
- Quick start (3 script examples)
- High-level capabilities overview
- Script descriptions
- Essential workflows

**Move:**
- Detailed architecture patterns → references/
- Extensive tech stack guide → references/
- Long development workflow details → references/

---

## Phase 3: Full Rollout (Week 3)

**Goal:** Apply refinements to remaining 33 skills

**Time:** ~20 hours

### Task 3.1: Product Team Skills (4 remaining, 8 hours)

Apply same pattern to:
- agile-product-owner
- product-strategist
- ux-researcher-designer
- ui-design-system

**For each:**
1. ✅ Metadata already added (Phase 1)
2. Add keywords section
3. Reduce SKILL.md to <200 lines
4. Move details to references/

### Task 3.2: Engineering Core Skills (8 remaining, 6 hours)

**Skills:**
- senior-architect
- senior-frontend
- senior-backend
- senior-qa
- senior-devops
- senior-secops
- code-reviewer
- senior-security

**For each:**
1. ✅ Metadata already added (Phase 1)
2. Add appropriate allowed-tools
3. Add keywords section
4. Reduce to <200 lines
5. Move patterns to references/

### Task 3.3: Engineering AI/ML/Data Skills (5 skills, 4 hours)

**Skills:**
- senior-data-scientist
- senior-data-engineer
- senior-ml-engineer
- senior-prompt-engineer
- senior-computer-vision

**For each:**
1. ✅ Metadata already added (Phase 1)
2. Add keywords section
3. Optimize SKILL.md length
4. Add ML/AI specific frameworks to metadata

### Task 3.4: RA/QM Skills (12 skills, 2 hours)

**Note:** These skills likely already follow good patterns

**For each:**
1. ✅ Metadata already added (Phase 1)
2. Add keywords section
3. Add compliance frameworks to metadata
4. Add allowed-tools for audit skills

---

## Phase 4: Validation & Documentation (Week 4)

**Goal:** Test, validate, and document the refined skills

**Time:** ~8 hours

### Task 4.1: Testing Protocol (4 hours)

**Test Each Skill:**

1. **Activation Test**
   - Ask question that should trigger skill
   - Verify Claude uses the skill
   - Check skill loads correctly

2. **Script Test**
   - Run each Python script with --help
   - Verify scripts still work
   - Check paths are correct

3. **Reference Test**
   - Verify all reference links work
   - Check references/ files load correctly
   - Ensure no broken links

**Test Matrix Template:**

| Skill Name | Activation Test | Scripts Test | References Test | Issues |
|------------|----------------|--------------|-----------------|--------|
| content-creator | ✅ Pass | ✅ Pass | ✅ Pass | None |
| ... | | | | |

### Task 4.2: Update Documentation (2 hours)

**Update These Files:**

**README.md:**
- Add note about skill structure following Anthropic best practices
- Update any references to skill lengths
- Add "Skills optimized for Claude AI activation" badge

**CLAUDE.md:**
- Add section on skill refactoring
- Document metadata standards
- Include keywords best practices

**Create SKILLS_AUTHORING_GUIDE.md:**
```markdown
# Skills Authoring Guide

## Anthropic Best Practices

Our skills follow Anthropic's official Agent Skills specification.

## Skill Template

[Include refined template]

## Metadata Standards

All skills include:
- MIT license
- Version tracking (semantic versioning)
- Author attribution
- Category and domain classification
- Tool and tech stack documentation

## SKILL.md Structure

Target length: 100-200 lines
- Keywords section
- Quick start (2-3 examples)
- Core workflows (high-level)
- Scripts overview
- References guide
- Best practices (top 5)
- Examples (2-3 concrete)

## Progressive Disclosure

- SKILL.md: Core instructions only
- references/: Detailed frameworks and guides
- scripts/: Automation tools
- assets/: Templates and resources
```

### Task 4.3: Version Control (2 hours)

**Create Git Tags:**
```bash
# Tag current state before refactoring
git tag v1.0.0-pre-refactor

# After refactoring
git tag v1.1.0-refactored
```

**Commit Strategy:**
```bash
# Phase 1
git commit -m "feat: add professional metadata to all 36 skills

- Add MIT license to all skills
- Add semantic versioning (v1.0.0)
- Add category and domain classification
- Add python-tools and tech-stack documentation
- Add keywords sections for better discovery"

# Phase 2
git commit -m "refactor: optimize 3 pilot skills following Anthropic best practices

- Reduce content-creator from 236 to 120 lines
- Reduce product-manager-toolkit from 352 to 150 lines
- Reduce senior-fullstack from 300 to 150 lines
- Move detailed content to references/
- Add allowed-tools where appropriate"

# Phase 3
git commit -m "refactor: optimize remaining 33 skills following Anthropic pattern

- Reduce all SKILL.md files to <200 lines
- Move detailed frameworks to references/
- Add keywords sections to all skills
- Add allowed-tools for restricted skills"
```

---

## 📐 Before/After Examples

### Example 1: content-creator Skill

#### BEFORE (236 lines total):

```markdown
---
name: content-creator
description: Comprehensive content marketing skill for creating blog posts, social media content, and SEO-optimized materials. Includes brand voice development, content templates, SEO analysis tools, and social media optimization strategies. Use when creating any marketing content, developing brand guidelines, optimizing for SEO, or planning content calendars.
---

# Content Creator

A comprehensive skill for creating high-performing marketing content with consistent brand voice, SEO optimization, and platform-specific best practices.

## Quick Start

### For Brand Voice Development
1. Run `scripts/brand_voice_analyzer.py` on existing content to establish baseline
2. Review `references/brand_guidelines.md` to select voice attributes
3. Apply chosen voice consistently across all content

[... 220 more lines including detailed frameworks, extensive examples, etc.]
```

#### AFTER (120 lines total):

```markdown
---
name: content-creator
description: Create SEO-optimized marketing content with consistent brand voice. Includes brand voice analyzer, SEO optimizer, content frameworks, and social media templates. Use when writing blog posts, creating social media content, analyzing brand voice, optimizing SEO, planning content calendars, or when user mentions content creation, brand voice, SEO optimization, social media marketing, or content strategy.
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  domain: content-marketing
  updated: 2025-10-20
  python-tools: brand_voice_analyzer.py, seo_optimizer.py
  tech-stack: SEO, social-media-platforms
---

# Content Creator

Professional-grade brand voice analysis, SEO optimization, and platform-specific content frameworks.

## Keywords
content creation, blog posts, SEO, brand voice, social media, content calendar, marketing content, content strategy, content marketing, brand consistency, content optimization, social media marketing, content planning, blog writing

## Quick Start

### Brand Voice Development
```bash
python scripts/brand_voice_analyzer.py existing_content.txt
```
Then select archetypes from references/brand-voice-detailed-framework.md

### SEO-Optimized Content
```bash
python scripts/seo_optimizer.py article.md "primary keyword" "secondary,keywords"
```
Apply recommendations to improve SEO score to >75/100

### Social Media Content
1. Review platform in references/social-media-platform-deep-dive.md
2. Use templates from references/content_frameworks.md
3. Optimize for platform algorithms

## Core Workflows

### 1. Brand Voice Consistency
Establish and maintain brand voice:
1. Analyze existing content with brand_voice_analyzer.py
2. Select personality archetypes (see references/brand-voice-detailed-framework.md)
3. Apply consistently across all content
4. Verify with analyzer

### 2. SEO Content Creation
Create optimized content:
1. Research keywords for topic
2. Write content using framework from references/content_frameworks.md
3. Run seo_optimizer.py to analyze and score
4. Apply recommendations (target score >75/100)

### 3. Platform-Specific Social Media
Optimize for each platform:
1. Select platform and review references/social-media-platform-deep-dive.md
2. Use appropriate template from references/content_frameworks.md
3. Follow platform-specific best practices
4. Schedule with content calendar

### 4. Content Calendar Planning
Plan and organize content:
1. Use assets/content_calendar_template.md
2. Balance content types and platforms
3. Align with marketing campaigns
4. Track performance

## Scripts

### brand_voice_analyzer.py
Analyze text for brand voice characteristics and readability.
- **Usage:** `python scripts/brand_voice_analyzer.py content.txt [json]`
- **Output:** Formality, tone, readability scores, recommendations

### seo_optimizer.py
Comprehensive SEO analysis and scoring.
- **Usage:** `python scripts/seo_optimizer.py article.md "keyword" "secondary,keywords"`
- **Output:** SEO score (0-100), keyword density, meta tags, recommendations

## References

- **brand-voice-detailed-framework.md** - 5 personality archetypes, tone dimensions, voice samples
- **brand_guidelines.md** - Quick brand voice reference
- **content_frameworks.md** - 15+ content type templates (blog, email, social, video, case studies)
- **social-media-platform-deep-dive.md** - Deep platform optimization (LinkedIn, Twitter, Instagram, Facebook, TikTok)
- **content-creation-examples.md** - 10+ complete examples with before/after

## Best Practices

- ✅ Run brand_voice_analyzer.py on all content before publishing
- ✅ Target SEO score >75/100 for all blog content
- ✅ Match content type to platform (see social media guide)
- ✅ Plan content 30 days ahead with calendar
- ✅ Analyze performance monthly and refine

## Examples

### Example 1: Blog Post Creation
```
User: "Write a blog post about AI automation for marketing teams"
1. Review framework: references/content_frameworks.md (Blog Post template)
2. Create draft in chosen brand voice archetype
3. Run: python scripts/seo_optimizer.py draft.md "AI marketing automation"
4. Apply recommendations (score improved 68→82)
5. Publish optimized content
```

### Example 2: Social Media Campaign
```
User: "Create LinkedIn content calendar for product launch"
1. Review: references/social-media-platform-deep-dive.md (LinkedIn section)
2. Use: assets/content_calendar_template.md
3. Create 30-day calendar with post types
4. Apply LinkedIn best practices (posting times, formats)
```
```

**Result:** 120 lines (49% reduction), all expertise retained in references/

---

### Example 2: product-manager-toolkit Skill

#### BEFORE (352 lines):
- Covers RICE + Interviews + PRDs + Discovery + Metrics in one file
- Extensive frameworks embedded
- Many detailed examples

#### AFTER (150 lines):
- Clear quick start with 3 capabilities
- High-level workflow overview
- Strong pointers to detailed references
- 2 concrete examples
- Keywords section for discovery

**New Reference Files Created:**
- `references/rice-prioritization-guide.md` (detailed RICE methodology)
- `references/customer-discovery-methods.md` (interview frameworks)
- `references/product-metrics-frameworks.md` (North Star, funnels, feature metrics)

---

## 📋 Implementation Checklist

### Week 1: Foundation Enhancement

**Marketing Skills (3 skills):**
- [ ] content-creator - Add metadata, keywords
- [ ] marketing-demand-acquisition - Add metadata, keywords
- [ ] marketing-strategy-pmm - Add metadata, keywords

**C-Level Skills (2 skills):**
- [ ] ceo-advisor - Add metadata, keywords
- [ ] cto-advisor - Add metadata, keywords

**Product Skills (5 skills):**
- [ ] product-manager-toolkit - Add metadata, keywords
- [ ] agile-product-owner - Add metadata, keywords
- [ ] product-strategist - Add metadata, keywords
- [ ] ux-researcher-designer - Add metadata, keywords
- [ ] ui-design-system - Add metadata, keywords

**Engineering Core (9 skills):**
- [ ] senior-architect - Add metadata, keywords, allowed-tools
- [ ] senior-frontend - Add metadata, keywords
- [ ] senior-backend - Add metadata, keywords
- [ ] senior-fullstack - Add metadata, keywords, allowed-tools
- [ ] senior-qa - Add metadata, keywords, allowed-tools
- [ ] senior-devops - Add metadata, keywords
- [ ] senior-secops - Add metadata, keywords
- [ ] code-reviewer - Add metadata, keywords, allowed-tools: Read, Grep, Glob
- [ ] senior-security - Add metadata, keywords

**Engineering AI/ML/Data (5 skills):**
- [ ] senior-data-scientist - Add metadata, keywords
- [ ] senior-data-engineer - Add metadata, keywords
- [ ] senior-ml-engineer - Add metadata, keywords
- [ ] senior-prompt-engineer - Add metadata, keywords
- [ ] senior-computer-vision - Add metadata, keywords

**RA/QM Skills (12 skills):**
- [ ] regulatory-affairs-head - Add metadata, keywords
- [ ] quality-manager-qmr - Add metadata, keywords
- [ ] quality-manager-qms-iso13485 - Add metadata, keywords
- [ ] capa-officer - Add metadata, keywords
- [ ] quality-documentation-manager - Add metadata, keywords
- [ ] risk-management-specialist - Add metadata, keywords
- [ ] information-security-manager-iso27001 - Add metadata, keywords
- [ ] mdr-745-specialist - Add metadata, keywords
- [ ] fda-consultant-specialist - Add metadata, keywords
- [ ] qms-audit-expert - Add metadata, keywords, allowed-tools: Read, Grep, Glob
- [ ] isms-audit-expert - Add metadata, keywords, allowed-tools: Read, Grep, Glob
- [ ] gdpr-dsgvo-expert - Add metadata, keywords

**Deliverables:**
- [ ] All 36 skills have complete metadata
- [ ] All 36 skills have keywords sections
- [ ] Git commit with changes

---

### Week 2: Pilot Optimization

- [ ] Refactor content-creator (236→120 lines)
- [ ] Create new reference files for content-creator
- [ ] Refactor product-manager-toolkit (352→150 lines)
- [ ] Create new reference files for PM toolkit
- [ ] Refactor senior-fullstack (est. 300→150 lines)
- [ ] Test all 3 pilot skills with Claude
- [ ] Document lessons learned
- [ ] Git commit with refactorings

**Success Criteria:**
- [ ] All 3 pilot SKILL.md files <200 lines
- [ ] Skills activate correctly when tested
- [ ] References load properly
- [ ] No broken links

---

### Week 3: Full Rollout

**Product Team (4 skills, 8 hours):**
- [ ] agile-product-owner optimization
- [ ] product-strategist optimization
- [ ] ux-researcher-designer optimization
- [ ] ui-design-system optimization

**Engineering (13 skills, 8 hours):**
- [ ] Optimize all engineering core skills (8 skills)
- [ ] Optimize all AI/ML/Data skills (5 skills)

**RA/QM (12 skills, 4 hours):**
- [ ] Optimize all RA/QM skills
- [ ] Ensure compliance frameworks documented

**Deliverables:**
- [ ] All 33 remaining skills optimized
- [ ] All SKILL.md files <200 lines
- [ ] All details moved to references/
- [ ] Git commit with complete rollout

---

### Week 4: Validation & Documentation

**Testing (4 hours):**
- [ ] Create test prompts for all 36 skills
- [ ] Run activation tests
- [ ] Document any issues
- [ ] Fix any broken references

**Documentation (2 hours):**
- [ ] Create SKILLS_AUTHORING_GUIDE.md
- [ ] Update README.md with optimization notes
- [ ] Update CLAUDE.md with refactoring info
- [ ] Document metadata standards

**Version Control (2 hours):**
- [ ] Tag v1.1.0-optimized
- [ ] Create CHANGELOG.md entry
- [ ] Update all README files
- [ ] Push final changes

---

## 🎯 Pilot Skill Refactoring Details

### Pilot 1: content-creator

**File Changes:**

1. **SKILL.md** - Reduce from 236 to 120 lines
2. **references/brand-voice-detailed-framework.md** (NEW) - 150 lines
3. **references/social-media-platform-deep-dive.md** (NEW) - 200 lines
4. **references/content-creation-examples.md** (NEW) - 100 lines

**Total:** 236 lines SKILL.md → 120 SKILL.md + 450 references = better organization

### Pilot 2: product-manager-toolkit

**File Changes:**

1. **SKILL.md** - Reduce from 352 to 150 lines
2. **references/rice-prioritization-guide.md** (NEW) - 180 lines
3. **references/customer-discovery-methods.md** (NEW) - 150 lines
4. **references/product-metrics-frameworks.md** (NEW) - 120 lines

**Total:** 352 lines SKILL.md → 150 SKILL.md + 450 references = better organization

### Pilot 3: senior-fullstack

**File Changes:**

1. **SKILL.md** - Reduce from ~300 to 150 lines
2. **references/fullstack-architecture-patterns.md** (NEW) - Move detailed patterns
3. **references/fullstack-development-guide.md** (NEW) - Move workflow details
4. **references/tech-stack-implementation.md** (NEW) - Move stack-specific guides

---

## 📊 Success Metrics

### Quantitative Metrics

**Before Refactoring:**
- Average SKILL.md length: ~300 lines
- Skills with metadata: 0/36 (0%)
- Skills with keywords: 0/36 (0%)
- Skills with allowed-tools: 0/36 (0%)
- Total lines in SKILL.md files: ~10,800 lines

**After Refactoring:**
- Average SKILL.md length: ~150 lines (50% reduction)
- Skills with metadata: 36/36 (100%)
- Skills with keywords: 36/36 (100%)
- Skills with allowed-tools: 8/36 (22% where appropriate)
- Total lines in SKILL.md files: ~5,400 lines
- New reference files created: ~30 files, ~4,500 lines

**Net Result:**
- Better organized (same total content)
- Faster skill loading
- Clearer discovery and activation
- Professional metadata

### Qualitative Metrics

- [ ] Claude activates skills more reliably
- [ ] Skills load faster (less context consumed)
- [ ] Clearer which skill to use when
- [ ] Better documented and versioned
- [ ] Easier for team to maintain

---

## 🔧 Implementation Tools & Scripts

### Script 1: Metadata Generator

**Purpose:** Generate consistent metadata for all skills

**Usage:**
```bash
python tools/generate_metadata.py --skill content-creator --category marketing --domain content-marketing --tools "brand_voice_analyzer.py, seo_optimizer.py"
```

**Output:**
```yaml
---
name: content-creator
description: [existing description]
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  domain: content-marketing
  updated: 2025-10-20
  python-tools: brand_voice_analyzer.py, seo_optimizer.py
---
```

### Script 2: SKILL.md Line Counter

**Purpose:** Track progress on reducing SKILL.md lengths

**Usage:**
```bash
python tools/count_skill_lines.py
```

**Output:**
```
Skill Line Count Report:
========================
content-creator: 236 lines (Target: 120) ⚠️
product-manager-toolkit: 352 lines (Target: 150) ⚠️
...
Average: 300 lines (Target: 150)
Total SKILL.md lines: 10,800 (Target: 5,400)
```

### Script 3: Reference Link Validator

**Purpose:** Ensure all reference links work after refactoring

**Usage:**
```bash
python tools/validate_references.py
```

**Output:**
```
Validating references in all skills...
✅ content-creator: All 5 references valid
❌ product-manager-toolkit: Broken link to references/metrics.md
...
```

---

## 📚 Reference Migration Guide

### When to Move Content to References

**Move if:**
- Detailed framework (>50 lines)
- Comprehensive checklists (>20 items)
- Extensive examples (>5 examples)
- Platform-specific details (>30 lines per platform)
- Procedural guides (step-by-step >30 steps)

**Keep in SKILL.md if:**
- Essential workflow (core process)
- Critical decision points
- Quick start examples (2-3)
- Script usage basics
- High-level overview

### Reference File Naming

**Pattern:** `references/[topic]-[type].md`

**Examples:**
- `rice-prioritization-guide.md` (not `rice.md`)
- `brand-voice-detailed-framework.md` (not `brand.md`)
- `social-media-platform-deep-dive.md` (not `social.md`)

**Benefits:**
- Clear what's in the file
- Easy to discover
- Consistent naming

---

## 🎓 Training Your Team

### For Skill Authors

**Before creating/updating a skill:**
1. Read Anthropic's skill-creator skill
2. Review this refactoring plan
3. Follow the refined template
4. Keep SKILL.md lean (<200 lines)
5. Use progressive disclosure

**Checklist for new skills:**
- [ ] YAML frontmatter complete (name, description, license, metadata)
- [ ] Description includes triggers and keywords
- [ ] Keywords section added
- [ ] SKILL.md under 200 lines
- [ ] Detailed content in references/
- [ ] Scripts in scripts/ with clear purposes
- [ ] All links tested
- [ ] Skill tested with Claude

---

## 🚀 Quick Start Implementation

### Day 1: Setup (2 hours)

1. **Create tools/ directory:**
```bash
mkdir -p /Users/rezarezvani/projects/claude-code-skills/tools
```

2. **Create helper scripts:**
- metadata_generator.py
- line_counter.py
- reference_validator.py

3. **Backup current state:**
```bash
git tag v1.0.0-pre-refactor
git branch refactoring/metadata-enhancement
git checkout refactoring/metadata-enhancement
```

### Day 2-3: Metadata Enhancement (12 hours)

**Batch 1 - Marketing & C-Level (5 skills, 2.5 hours):**
- Update all frontmatter
- Add keywords sections
- Test activation

**Batch 2 - Product Team (5 skills, 2.5 hours):**
- Update all frontmatter
- Add keywords sections
- Test activation

**Batch 3 - Engineering Core (9 skills, 4.5 hours):**
- Update all frontmatter
- Add allowed-tools where appropriate
- Add keywords sections

**Batch 4 - Engineering AI/ML (5 skills, 2.5 hours):**
- Update all frontmatter
- Add keywords sections

**Day 4: RA/QM Skills (12 skills, 6 hours):**
- Update all frontmatter with compliance frameworks
- Add keywords sections
- Add allowed-tools for audit skills

**Day 5: Commit Phase 1:**
```bash
git add -A
git commit -m "feat: add professional metadata to all 36 skills"
git push origin refactoring/metadata-enhancement
```

### Week 2: Pilot Optimization

**Monday-Tuesday: content-creator (8 hours):**
- Slim down SKILL.md
- Create 3 new reference files
- Test thoroughly

**Wednesday-Thursday: product-manager-toolkit (8 hours):**
- Slim down SKILL.md
- Create 3 new reference files
- Test thoroughly

**Friday: senior-fullstack (4 hours):**
- Slim down SKILL.md
- Organize references
- Test thoroughly

**Weekend: Review & Commit:**
```bash
git add -A
git commit -m "refactor: optimize 3 pilot skills following Anthropic best practices"
```

---

## 🎯 Success Criteria

### Phase 1 Success
- [ ] All 36 skills have complete metadata
- [ ] All 36 skills have keywords sections
- [ ] No broken skills (all still work)
- [ ] Git committed and pushed

### Phase 2 Success
- [ ] 3 pilot skills reduced to <200 lines each
- [ ] New reference files created and linked
- [ ] All 3 skills activate correctly
- [ ] No regression in functionality

### Phase 3 Success
- [ ] All 33 remaining skills optimized
- [ ] All SKILL.md files <200 lines
- [ ] No broken links or references
- [ ] All skills tested and working

### Phase 4 Success
- [ ] All 36 skills validated
- [ ] Documentation updated
- [ ] SKILLS_AUTHORING_GUIDE.md created
- [ ] Version tagged and pushed

---

## 📞 Support During Refactoring

### Common Issues & Solutions

**Issue: "I broke the skill after refactoring"**
- Solution: Revert to backup branch, identify what broke, fix incrementally

**Issue: "Reference links don't work"**
- Solution: Use relative paths: `references/file.md`, not absolute paths

**Issue: "Claude doesn't activate the skill anymore"**
- Solution: Check description has clear triggers, verify YAML syntax valid

**Issue: "Keywords too generic"**
- Solution: Use specific terms users would actually say

---

## 💡 Pro Tips

### Tip 1: One Skill at a Time
Don't try to refactor all 36 at once. Do 3-5 per day maximum.

### Tip 2: Test Immediately
After each refactor, test the skill works. Don't batch testing.

### Tip 3: Keep Backups
Tag before major changes: `git tag v1.0-before-refactor-skill-name`

### Tip 4: Reference First
When in doubt, move to references/. You can always move back to SKILL.md if needed.

### Tip 5: User Feedback
Have actual users test refined skills and provide feedback.

---

## 🎊 Final Outcome

After completing this plan, you'll have:

✅ **36 professionally structured skills** following Anthropic's official pattern
✅ **Complete metadata** (license, version, categorization)
✅ **Enhanced discovery** (keywords, better descriptions)
✅ **Optimized loading** (lean SKILL.md, rich references)
✅ **Safer execution** (allowed-tools where appropriate)
✅ **Better documentation** (authoring guide, standards)
✅ **Maintained expertise** (all content retained, better organized)

**Your skills will be:**
- Faster to load
- Easier to discover
- Clearer to use
- Safer to execute
- Better organized
- Professionally versioned

**While maintaining:**
- All 97 Python tools
- All reference materials
- All frameworks and benchmarks
- All domain expertise

---

**Ready to start? I recommend beginning with Phase 1, Task 1.2 - updating the 3 marketing skills as they're the smallest domain and perfect for learning the pattern!**
