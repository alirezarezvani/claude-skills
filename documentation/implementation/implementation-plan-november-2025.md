# Claude Skills - Skill-Agent Integration Implementation Plan

**Version:** 1.0
**Created:** November 5, 2025
**Status:** In Progress
**Milestone:** Skill-Agent Integration v1.0

---

## Executive Summary

This plan outlines the integration of specialized agents (cs-* prefix) with the existing 42 production-ready skills in the claude-code-skills repository. The implementation creates a seamless workflow where users can invoke domain-specific agents that automatically discover and execute the appropriate Python tools and reference knowledge bases.

**Key Objectives:**
- Create 5 foundational agents covering marketing, C-level advisory, and product management
- Implement simple installation system via interactive script
- Maintain 100% backwards compatibility with existing skill structure
- Prepare foundation for future Anthropic plugin marketplace distribution

**Timeline:** Days 1-4 (Phase 1-2)
**Future Work:** Days 5-10 (Phase 3-7, including plugin creation)

---

## Architecture Overview

### Directory Structure

```
claude-code-skills/
├── agents/                    # cs-* prefixed agents (NEW)
│   ├── marketing/
│   │   ├── cs-content-creator.md
│   │   └── cs-demand-gen-specialist.md
│   ├── c-level/
│   │   ├── cs-ceo-advisor.md
│   │   └── cs-cto-advisor.md
│   └── product/
│       └── cs-product-manager.md
├── commands/                  # Slash commands (NEW)
├── standards/                 # Standards library (NEW)
│   ├── communication/
│   ├── quality/
│   ├── git/
│   ├── documentation/
│   └── security/
├── templates/                 # Templates (NEW)
├── marketing-skill/          # EXISTING - unchanged
├── c-level-advisor/          # EXISTING - unchanged
├── product-team/             # EXISTING - unchanged
├── project-management/       # EXISTING - unchanged
├── engineering-team/         # EXISTING - unchanged
├── ra-qm-team/               # EXISTING - unchanged
├── install.sh                # Installation script (FUTURE)
├── uninstall.sh              # Cleanup script (FUTURE)
├── INSTALL.md                # Installation guide (FUTURE)
├── USAGE.md                  # Usage examples (FUTURE)
├── .claude/                  # Dev-only workflows
└── .github/                  # GitHub automation
```

### Design Principles

1. **Non-invasive:** Agents reference existing skills via relative paths
2. **Zero conflicts:** cs-* prefix prevents collision with user's existing agents
3. **Backwards compatible:** Existing skill folders remain untouched
4. **Plugin-ready:** Structure designed for future marketplace distribution
5. **Simple installation:** Single script with 3 Q&A questions (Phase 3)

---

## Phase 1: Core Structure Setup (Day 1)

### 1.1 Create Root-Level Directories

**Task:** Set up foundational directory structure
**Owner:** Implementation team
**Estimated Time:** 30 minutes

**Directories to create:**
```bash
mkdir -p agents/marketing
mkdir -p agents/c-level
mkdir -p agents/product
mkdir -p commands
mkdir -p standards/communication
mkdir -p standards/quality
mkdir -p standards/git
mkdir -p standards/documentation
mkdir -p standards/security
mkdir -p templates
```

**Success Criteria:**
- All directories created in repository root
- Directory structure matches architecture diagram
- No conflicts with existing folders

**GitHub Issue:** #[TBD] - Create root-level directory structure

---

### 1.2 Port Core Standards from Factory

**Task:** Copy and adapt 5 essential standards from claude-code-skills-factory
**Owner:** Documentation team
**Estimated Time:** 2 hours

**Standards to port:**

1. **communication-standards.md** → `standards/communication/`
   - Absolute honesty, zero fluff, pragmatic focus
   - Critical analysis requirements
   - Response protocol
   - Prohibited responses

2. **quality-standards.md** → `standards/quality/`
   - Code quality requirements
   - Testing standards
   - Review checklist

3. **git-workflow-standards.md** → `standards/git/`
   - Conventional commits
   - Branch naming
   - PR requirements
   - Commit message templates

4. **documentation-standards.md** → `standards/documentation/`
   - Markdown formatting
   - File naming conventions
   - Structure requirements
   - Living documentation principles

5. **security-standards.md** → `standards/security/`
   - Secret detection
   - Dependency scanning
   - Security checklist
   - Vulnerability reporting

**Adaptation Notes:**
- Replace factory-specific references with claude-skills context
- Update file paths to match new structure
- Reference existing skills (not rr-* agents)
- Maintain standard library focus (no external dependencies)

**Success Criteria:**
- All 5 standards files created and validated
- No broken links or factory-specific references
- Standards reference claude-skills architecture
- Files pass markdown linting

**GitHub Issue:** #[TBD] - Port core standards from factory

---

## Phase 2: Agent Implementation (Days 2-4)

### 2.1 Create Marketing Agents (Day 2)

**Task:** Implement 2 marketing domain agents
**Owner:** Marketing team
**Estimated Time:** 4 hours

#### Agent 1: cs-content-creator

**File:** `agents/marketing/cs-content-creator.md`

**Structure:**
```yaml
---
name: cs-content-creator
description: Create SEO-optimized marketing content with brand voice consistency
skills: content-creator
domain: marketing
model: sonnet
tools: [Read, Write, Bash, Grep, Glob]
---

# Content Creator Agent

## Purpose
Specialized agent for creating high-quality marketing content across multiple formats (blog posts, social media, email campaigns, video scripts). Integrates brand voice analysis, SEO optimization, and platform-specific best practices.

## Skill Integration

**Skill Location:** `../../marketing-skill/content-creator/`

### Python Tools

**Brand Voice Analyzer:**
```bash
python ../../marketing-skill/content-creator/scripts/brand_voice_analyzer.py input.txt
python ../../marketing-skill/content-creator/scripts/brand_voice_analyzer.py input.txt json
```

**SEO Optimizer:**
```bash
python ../../marketing-skill/content-creator/scripts/seo_optimizer.py article.md "primary keyword"
python ../../marketing-skill/content-creator/scripts/seo_optimizer.py article.md "primary keyword" "secondary,keywords"
```

### Knowledge Bases

- Brand Guidelines: `../../marketing-skill/content-creator/references/brand_guidelines.md`
- Content Frameworks: `../../marketing-skill/content-creator/references/content_frameworks.md`
- Social Media Optimization: `../../marketing-skill/content-creator/references/social_media_optimization.md`

### Templates

- Content Calendar: `../../marketing-skill/content-creator/assets/content-calendar-template.md`
- Brand Voice Checklist: `../../marketing-skill/content-creator/assets/brand-voice-checklist.md`

## Workflows

### Workflow 1: Create Blog Post
1. Read brief from user
2. Analyze existing brand voice samples using brand_voice_analyzer.py
3. Reference content_frameworks.md for blog post structure
4. Draft content following brand guidelines
5. Run SEO analysis using seo_optimizer.py
6. Refine based on SEO recommendations
7. Output final content + SEO report

### Workflow 2: Create Social Media Campaign
1. Identify target platforms
2. Reference social_media_optimization.md for platform best practices
3. Draft platform-specific content (character limits, hashtags, CTAs)
4. Validate brand voice consistency
5. Generate content calendar using template

### Workflow 3: Analyze Brand Voice
1. Collect content samples from user
2. Run brand_voice_analyzer.py on each sample
3. Aggregate results to identify patterns
4. Map to personality archetype (Expert, Friend, Innovator, Guide, Motivator)
5. Create brand voice profile document

## Integration Examples

**Example 1: Blog post with SEO**
```bash
# User provides brief
# Agent drafts article as draft.md
python ../../marketing-skill/content-creator/scripts/seo_optimizer.py draft.md "content marketing"

# Review SEO score and recommendations
# Refine draft based on suggestions
# Final output: optimized article
```

**Example 2: Brand voice audit**
```bash
# User provides 3 content samples
python ../../marketing-skill/content-creator/scripts/brand_voice_analyzer.py sample1.txt json > voice1.json
python ../../marketing-skill/content-creator/scripts/brand_voice_analyzer.py sample2.txt json > voice2.json
python ../../marketing-skill/content-creator/scripts/brand_voice_analyzer.py sample3.txt json > voice3.json

# Agent analyzes JSON outputs
# Identifies consistency patterns
# Recommends brand voice archetype
```

## Success Metrics

- Content creation time reduced by 40%
- SEO scores improved by 30%+ on average
- Brand voice consistency across all outputs
- Platform-specific best practices followed

## Related Agents

- cs-demand-gen-specialist (acquisition campaigns)
- cs-product-marketing (product launches)

## References

- Skill Documentation: `../../marketing-skill/content-creator/SKILL.md`
- Standards: `../../standards/communication/communication-standards.md`
```

#### Agent 2: cs-demand-gen-specialist

**File:** `agents/marketing/cs-demand-gen-specialist.md`

**Structure:** (Similar YAML frontmatter + content structure)
- Integrates with `../../marketing-skill/marketing-demand-acquisition/`
- Python tool: campaign_analyzer.py
- Workflows: Lead gen campaigns, conversion optimization, funnel analysis

**Success Criteria:**
- Both agents created with complete YAML frontmatter
- All relative paths validated (../../ references work)
- Python tool invocation examples tested
- Workflow sections comprehensive
- No broken links

**GitHub Issue:** #[TBD] - Create marketing agents (cs-content-creator, cs-demand-gen-specialist)

---

### 2.2 Create C-Level Advisory Agents (Day 3)

**Task:** Implement 2 C-level advisory agents
**Owner:** Strategy team
**Estimated Time:** 4 hours

#### Agent 3: cs-ceo-advisor

**File:** `agents/c-level/cs-ceo-advisor.md`

**Integration Points:**
- Skill: `../../c-level-advisor/ceo-advisor/`
- Python tools: strategic_framework_generator.py, scenario_planner.py, okr_tracker.py
- Knowledge bases: Strategic frameworks, decision templates, board reporting

**Workflows:**
- Strategic planning (3-year vision)
- Quarterly OKR setting
- Board deck preparation
- Scenario analysis (market shifts, competition)

#### Agent 4: cs-cto-advisor

**File:** `agents/c-level/cs-cto-advisor.md`

**Integration Points:**
- Skill: `../../c-level-advisor/cto-advisor/`
- Python tools: tech_stack_analyzer.py, architecture_auditor.py, team_velocity_tracker.py
- Knowledge bases: Tech stack decisions, architecture patterns, engineering metrics

**Workflows:**
- Technology roadmap planning
- Build vs buy analysis
- Technical debt assessment
- Engineering team scaling

**Success Criteria:**
- Both C-level agents created
- Strategic frameworks integrated
- Python tools documented with examples
- Workflow sections cover executive use cases
- References to CEO/CTO skill packages working

**GitHub Issue:** #[TBD] - Create C-level agents (cs-ceo-advisor, cs-cto-advisor)

---

### 2.3 Create Product Management Agent (Day 4)

**Task:** Implement product management agent
**Owner:** Product team
**Estimated Time:** 3 hours

#### Agent 5: cs-product-manager

**File:** `agents/product/cs-product-manager.md`

**Integration Points:**
- Skill: `../../product-team/product-manager-toolkit/`
- Python tools: rice_prioritizer.py, customer_interview_analyzer.py
- Knowledge bases: Product frameworks, roadmap templates, prioritization methods

**Workflows:**
- Feature prioritization (RICE framework)
- Customer interview analysis
- Product roadmap generation
- Quarterly planning

**Example Integration:**
```bash
# User uploads features.csv
python ../../product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv --capacity 20 --output json

# Agent analyzes RICE scores
# Categorizes: Quick Wins, Big Bets, Maybes, Time Sinks
# Generates quarterly roadmap
```

**Success Criteria:**
- Product manager agent created
- RICE prioritization workflow functional
- Interview analysis integrated
- Roadmap generation examples documented

**GitHub Issue:** #[TBD] - Create product agent (cs-product-manager)

---

### 2.4 Create Agent Structure Template & Documentation (Day 4)

**Task:** Standardize agent creation process
**Owner:** Documentation team
**Estimated Time:** 2 hours

**Deliverables:**

1. **Agent Template:** `templates/agent-template.md`
   - YAML frontmatter structure
   - Required sections (Purpose, Skill Integration, Workflows, Success Metrics)
   - Python tool invocation patterns
   - Knowledge base reference format
   - Related agents linking

2. **Agent Creation Guide:** `documentation/AGENT_CREATION_GUIDE.md`
   - Step-by-step process
   - Naming conventions (cs-* prefix)
   - Relative path resolution
   - Testing checklist
   - Integration validation

**Success Criteria:**
- Template covers all required agent sections
- Creation guide is actionable (developers can create new agents)
- Examples from cs-content-creator referenced
- Template passes validation

**GitHub Issue:** #[TBD] - Create agent structure template and documentation

---

## Future Phases (Days 5-10)

### Phase 3: Installation System (Day 5)
- Create install.sh with 3 Q&A questions
- Create uninstall.sh
- Implement backwards compatibility detection

### Phase 4: Documentation (Day 6)
- Update README.md with agent catalog
- Create INSTALL.md
- Create USAGE.md
- Update CLAUDE.md

### Phase 5: Testing & Quality (Day 7)
- Validate YAML frontmatter
- Test relative path resolution
- Verify Python tool invocation
- Run quality gates

### Phase 6-7: Plugin Creation (Days 8-10)
- Research Anthropic marketplace requirements
- Design plugin.yaml manifest
- Create plugin package structure
- Prepare submission assets (icon, screenshots, description)
- Submit to marketplace

---

## Success Criteria

### Phase 1-2 Completion Checklist

- [ ] All 4 root directories created (agents/, commands/, standards/, templates/)
- [ ] 5 core standards ported and validated
- [ ] 5 agents implemented and tested:
  - [ ] cs-content-creator
  - [ ] cs-demand-gen-specialist
  - [ ] cs-ceo-advisor
  - [ ] cs-cto-advisor
  - [ ] cs-product-manager
- [ ] All relative paths (../../) resolve correctly
- [ ] Python tools execute successfully from agents
- [ ] Agent template created
- [ ] Documentation updated
- [ ] All tasks tracked in GitHub issues
- [ ] Issues linked to Milestone "Skill-Agent Integration v1.0"
- [ ] Issues synced to Project #9 board

### Quality Gates

1. **File Structure:**
   - All files use kebab-case naming
   - Markdown files pass linting
   - YAML frontmatter validates

2. **Path Resolution:**
   - All `../../` relative paths work
   - Python scripts execute from agent context
   - Knowledge bases load correctly

3. **Documentation:**
   - No broken links
   - All examples tested
   - Workflow sections complete

4. **Integration:**
   - Agents discover skills automatically
   - Python tools execute with correct paths
   - Templates load successfully

---

## Risk Mitigation

### Risk 1: Relative path resolution fails
- **Probability:** Medium
- **Impact:** High
- **Mitigation:** Test all paths in isolation before committing
- **Fallback:** Use absolute paths with environment variable

### Risk 2: Agent naming conflicts with user's existing setup
- **Probability:** Low (cs-* prefix chosen to avoid conflicts)
- **Impact:** Medium
- **Mitigation:** Clear documentation, namespace everything
- **Fallback:** Allow users to customize prefix during installation

### Risk 3: GitHub automation workflow issues
- **Probability:** Low (workflows already implemented and tested)
- **Impact:** Low
- **Mitigation:** Test issues creation before full rollout
- **Fallback:** Manual issue creation

### Risk 4: Standards not applicable to all skills
- **Probability:** Medium
- **Impact:** Low
- **Mitigation:** Keep standards general, allow skill-specific overrides
- **Fallback:** Document exceptions in standards files

---

## GitHub Issues Breakdown

### Phase 1 Issues (Day 1)

**Issue 1: Create root-level directory structure**
- Labels: `type:enhancement`, `domain:agents`, `priority:high`
- Milestone: Skill-Agent Integration v1.0
- Checklist:
  - [ ] Create agents/ with subdirectories (marketing/, c-level/, product/)
  - [ ] Create commands/
  - [ ] Create standards/ with subdirectories
  - [ ] Create templates/
  - [ ] Verify no conflicts with existing structure
  - [ ] Update .gitignore if needed

**Issue 2: Port core standards from factory**
- Labels: `type:enhancement`, `domain:documentation`, `priority:high`
- Milestone: Skill-Agent Integration v1.0
- Checklist:
  - [ ] Port communication-standards.md
  - [ ] Port quality-standards.md
  - [ ] Port git-workflow-standards.md
  - [ ] Port documentation-standards.md
  - [ ] Port security-standards.md
  - [ ] Adapt all references to claude-skills context
  - [ ] Validate markdown linting passes

### Phase 2 Issues (Days 2-4)

**Issue 3: Create marketing agents**
- Labels: `type:enhancement`, `domain:agents`, `domain:marketing`, `priority:high`
- Milestone: Skill-Agent Integration v1.0
- Checklist:
  - [ ] Create cs-content-creator.md with full structure
  - [ ] Create cs-demand-gen-specialist.md
  - [ ] Test relative paths to marketing-skill/
  - [ ] Validate Python tool invocation
  - [ ] Document workflows
  - [ ] Add integration examples

**Issue 4: Create C-level agents**
- Labels: `type:enhancement`, `domain:agents`, `priority:high`
- Milestone: Skill-Agent Integration v1.0
- Checklist:
  - [ ] Create cs-ceo-advisor.md
  - [ ] Create cs-cto-advisor.md
  - [ ] Test relative paths to c-level-advisor/
  - [ ] Validate Python tool invocation
  - [ ] Document strategic workflows
  - [ ] Add executive use case examples

**Issue 5: Create product agent**
- Labels: `type:enhancement`, `domain:agents`, `domain:product`, `priority:high`
- Milestone: Skill-Agent Integration v1.0
- Checklist:
  - [ ] Create cs-product-manager.md
  - [ ] Test relative paths to product-team/
  - [ ] Validate RICE prioritizer integration
  - [ ] Validate interview analyzer integration
  - [ ] Document roadmap workflows

**Issue 6: Create agent structure template**
- Labels: `type:documentation`, `domain:templates`, `priority:medium`
- Milestone: Skill-Agent Integration v1.0
- Checklist:
  - [ ] Create templates/agent-template.md
  - [ ] Create documentation/AGENT_CREATION_GUIDE.md
  - [ ] Document YAML frontmatter requirements
  - [ ] Document workflow section structure
  - [ ] Add validation checklist

---

## Metrics & KPIs

### Implementation Metrics

- **Time to complete Phase 1-2:** 4 days (target)
- **Number of agents created:** 5
- **Standards ported:** 5
- **GitHub issues created:** 6-8
- **Code review cycles:** 1-2 per agent

### Quality Metrics

- **Path resolution success rate:** 100%
- **Python tool execution success rate:** 100%
- **Documentation coverage:** 100% (all agents fully documented)
- **Markdown linting pass rate:** 100%

### User Experience Metrics (Post Phase 3)

- **Time to install:** <5 minutes
- **Agent discovery time:** <1 minute
- **Skill execution time:** Same as direct Python invocation
- **User satisfaction:** TBD (collect feedback)

---

## Next Steps After Phase 1-2

1. **Phase 3 Planning:** Create detailed plan for installation system
2. **Community Feedback:** Share Phase 1-2 implementation for early feedback
3. **Agent Expansion:** Plan remaining 37 agents (project management, engineering, RA/QM)
4. **Plugin Research:** Deep dive into Anthropic marketplace requirements
5. **Integration Testing:** Comprehensive testing with real user workflows

---

## Appendix A: Agent Naming Convention

**Format:** `cs-{domain}-{role}`

**Examples:**
- cs-content-creator (marketing domain)
- cs-demand-gen-specialist (marketing domain)
- cs-ceo-advisor (c-level domain)
- cs-product-manager (product domain)

**Rules:**
- Always use `cs-` prefix (claude-skills)
- Use kebab-case for multi-word roles
- Keep names concise (<30 characters)
- Match corresponding skill folder name when possible

---

## Appendix B: Directory Tree (Complete)

```
claude-code-skills/
├── .claude/
│   └── commands/              # Development commands (git/, review.md, etc.)
├── .github/
│   ├── workflows/             # CI/CD automation
│   ├── AUTOMATION_SETUP.md
│   └── pull_request_template.md
├── agents/                    # NEW: cs-* agents
│   ├── marketing/
│   │   ├── cs-content-creator.md
│   │   └── cs-demand-gen-specialist.md
│   ├── c-level/
│   │   ├── cs-ceo-advisor.md
│   │   └── cs-cto-advisor.md
│   └── product/
│       └── cs-product-manager.md
├── commands/                  # NEW: User slash commands
├── standards/                 # NEW: Standards library
│   ├── communication/
│   │   └── communication-standards.md
│   ├── quality/
│   │   └── quality-standards.md
│   ├── git/
│   │   └── git-workflow-standards.md
│   ├── documentation/
│   │   └── documentation-standards.md
│   └── security/
│       └── security-standards.md
├── templates/                 # NEW: Templates
│   └── agent-template.md
├── documentation/
│   ├── implementation/
│   │   └── implementation-plan-november-2025.md  # THIS FILE
│   ├── GIST_CONTENT.md
│   └── PYTHON_TOOLS_AUDIT.md
├── marketing-skill/          # EXISTING
├── c-level-advisor/          # EXISTING
├── product-team/             # EXISTING
├── project-management/       # EXISTING
├── engineering-team/         # EXISTING
├── ra-qm-team/               # EXISTING
├── CLAUDE.md
├── README.md
├── LICENSE
└── .gitignore
```

---

## Document History

- **v1.0** (2025-11-05): Initial implementation plan created for Phase 1-2
- Future versions will document Phase 3-7 planning and execution

---

**End of Implementation Plan**
