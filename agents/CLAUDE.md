# Agent Development Guide

This guide provides comprehensive instructions for creating **cs-* prefixed agents** that seamlessly integrate with the 42 production skills in this repository.

## Agent Architecture

### What are cs-* Agents?

**cs-* agents** are specialized Claude Code agents that orchestrate the 42 existing skills. Each agent:
- References skills via relative paths (`../../marketing-skill/`)
- Executes Python automation tools from skill packages
- Follows established workflows and templates
- Maintains skill portability and independence

**Key Principle**: Agents ORCHESTRATE skills, they don't replace them. Skills remain self-contained and portable.

### Production Agents

**5 Agents Currently Available** (as of November 5, 2025):

| Agent | Domain | Description | Skills Used | Lines |
|-------|--------|-------------|-------------|-------|
| [cs-content-creator](marketing/cs-content-creator.md) | Marketing | AI-powered content creation with brand voice consistency and SEO optimization | content-creator | 327 |
| [cs-demand-gen-specialist](marketing/cs-demand-gen-specialist.md) | Marketing | Demand generation and customer acquisition specialist | marketing-demand-acquisition | 289 |
| [cs-ceo-advisor](c-level/cs-ceo-advisor.md) | C-Level | Strategic leadership advisor for CEOs covering vision, strategy, board management | ceo-advisor | 360 |
| [cs-cto-advisor](c-level/cs-cto-advisor.md) | C-Level | Technical leadership advisor for CTOs covering tech strategy and team scaling | cto-advisor | 412 |
| [cs-product-manager](product/cs-product-manager.md) | Product | Product management agent for RICE prioritization and customer discovery | product-manager-toolkit | 407 |

**Total**: 1,795 lines of comprehensive agent documentation

**Template Available**: [templates/agent-template.md](../templates/agent-template.md) (318 lines) - Use this to create new agents

### Agent vs Skill

| Aspect | Agent (cs-*) | Skill |
|--------|-------------|-------|
| **Purpose** | Orchestrate and execute workflows | Provide tools, knowledge, templates |
| **Location** | `agents/domain/` | `domain-skill/skill-name/` |
| **Structure** | Single .md file with YAML frontmatter | SKILL.md + scripts/ + references/ + assets/ |
| **Integration** | References skills via `../../` | Self-contained, no dependencies |
| **Naming** | cs-content-creator, cs-ceo-advisor | content-creator, ceo-advisor |

## Agent File Structure

### Required YAML Frontmatter

Every agent file must start with valid YAML frontmatter:

```yaml
---
name: cs-agent-name
description: One-line description of what this agent does
skills: skill-folder-name
domain: domain-name
model: sonnet
tools: [Read, Write, Bash, Grep, Glob]
---
```

**Field Definitions:**
- **name**: Agent identifier with `cs-` prefix (e.g., `cs-content-creator`)
- **description**: Single sentence describing agent's purpose
- **skills**: Skill folder this agent references (e.g., `marketing-skill/content-creator`)
- **domain**: Domain category (marketing, product, engineering, c-level, pm, ra-qm)
- **model**: Claude model to use (sonnet, opus, haiku)
- **tools**: Array of Claude Code tools agent can use

### Required Markdown Sections

After YAML frontmatter, include these sections:

1. **Purpose** (2-3 paragraphs)
2. **Skill Integration** (with subsections)
   - Skill Location
   - Python Tools
   - Knowledge Bases
   - Templates
3. **Workflows** (minimum 3 workflows)
4. **Integration Examples** (concrete code/command examples)
5. **Success Metrics** (how to measure effectiveness)
6. **Related Agents** (cross-references)
7. **References** (links to documentation)

## Relative Path Resolution

### Path Pattern

All skill references use the `../../` pattern:

```markdown
**Skill Location:** `../../marketing-skill/content-creator/`

### Python Tools

1. **Brand Voice Analyzer**
   - **Path:** `../../marketing-skill/content-creator/scripts/brand_voice_analyzer.py`
   - **Usage:** `python ../../marketing-skill/content-creator/scripts/brand_voice_analyzer.py content.txt`

2. **SEO Optimizer**
   - **Path:** `../../marketing-skill/content-creator/scripts/seo_optimizer.py`
   - **Usage:** `python ../../marketing-skill/content-creator/scripts/seo_optimizer.py article.md "keyword"`
```

### Why `../../`?

From agent location: `agents/marketing/cs-content-creator.md`
To skill location: `marketing-skill/content-creator/`

Navigation: `agents/marketing/` → `../../` (up to root) → `marketing-skill/content-creator/`

**Always test paths resolve correctly!**

## Python Tool Integration

### Execution Pattern

Agents execute Python tools from skill packages:

```bash
# From agent context
python ../../marketing-skill/content-creator/scripts/brand_voice_analyzer.py input.txt

# With JSON output
python ../../marketing-skill/content-creator/scripts/brand_voice_analyzer.py input.txt json

# With arguments
python ../../product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv --capacity 20
```

### Tool Requirements

All Python tools must:
- Use standard library only (or minimal dependencies documented in SKILL.md)
- Support both JSON and human-readable output
- Provide `--help` flag with usage information
- Return appropriate exit codes (0 = success, 1 = error)
- Handle missing arguments gracefully

### Error Handling

When Python tools fail:
1. Check file path resolution
2. Verify input file exists
3. Check Python version compatibility (3.8+)
4. Review tool's `--help` output
5. Inspect error messages in stderr

## Workflow Documentation

### Workflow Structure

Each workflow must include:

```markdown
### Workflow 1: [Clear Descriptive Name]

**Goal:** One-sentence description

**Steps:**
1. **[Action]** - Description with specific commands/tools
2. **[Action]** - Description with specific commands/tools
3. **[Action]** - Description with specific commands/tools

**Expected Output:** What success looks like

**Time Estimate:** How long this workflow takes

**Example:**
\`\`\`bash
# Concrete example command
python ../../marketing-skill/content-creator/scripts/seo_optimizer.py article.md "primary keyword"
\`\`\`
```

### Minimum Requirements

Each agent must document **at least 3 workflows** covering:
1. Primary use case (most common scenario)
2. Advanced use case (complex scenario)
3. Integration use case (combining multiple tools)

## Agent Template

Use this template when creating new agents:

```markdown
---
name: cs-agent-name
description: One-line description
skills: skill-folder-name
domain: domain-name
model: sonnet
tools: [Read, Write, Bash, Grep, Glob]
---

# Agent Name

## Purpose

[2-3 paragraphs describing what this agent does, why it exists, and who it serves]

## Skill Integration

**Skill Location:** \`../../domain-skill/skill-name/\`

### Python Tools

1. **Tool Name**
   - **Purpose:** What it does
   - **Path:** \`../../domain-skill/skill-name/scripts/tool.py\`
   - **Usage:** \`python ../../domain-skill/skill-name/scripts/tool.py [args]\`

### Knowledge Bases

1. **Reference Name**
   - **Location:** \`../../domain-skill/skill-name/references/file.md\`
   - **Content:** What's inside

### Templates

1. **Template Name**
   - **Location:** \`../../domain-skill/skill-name/assets/template.md\`
   - **Use Case:** When to use

## Workflows

### Workflow 1: [Name]

**Goal:** Description

**Steps:**
1. Step 1
2. Step 2
3. Step 3

**Expected Output:** Success criteria

**Example:**
\`\`\`bash
python ../../domain-skill/skill-name/scripts/tool.py input.txt
\`\`\`

### Workflow 2: [Name]
[Same structure]

### Workflow 3: [Name]
[Same structure]

## Integration Examples

[Concrete examples with actual commands and expected outputs]

## Success Metrics

- Metric 1: How to measure
- Metric 2: How to measure
- Metric 3: How to measure

## Related Agents

- [cs-related-agent](../domain/cs-related-agent.md) - How they relate

## References

- [Skill Documentation](../../domain-skill/skill-name/SKILL.md)
- [Domain Roadmap](../../domain-skill/roadmap.md)
```

## Quality Standards

### Agent Quality Checklist

Before committing an agent:

- [ ] YAML frontmatter valid (no parsing errors)
- [ ] All required fields present (name, description, skills, domain, model, tools)
- [ ] cs-* prefix used for agent naming
- [ ] Relative paths resolve correctly (../../ pattern)
- [ ] Skill location documented and accessible
- [ ] Python tools referenced with correct paths
- [ ] At least 3 workflows documented
- [ ] Integration examples provided and tested
- [ ] Success metrics defined
- [ ] Related agents cross-referenced

### Testing Agent Integration

Test these aspects:

**1. Path Resolution**
```bash
# From agent directory
cd agents/marketing/
ls ../../marketing-skill/content-creator/  # Should list contents
```

**2. Python Tool Execution**
```bash
# Create test input
echo "Test content" > test-input.txt

# Execute tool
python ../../marketing-skill/content-creator/scripts/brand_voice_analyzer.py test-input.txt

# Verify output
```

**3. Knowledge Base Access**
```bash
# Verify reference files exist
cat ../../marketing-skill/content-creator/references/brand_guidelines.md
```

## Domain-Specific Guidelines

### Marketing Agents (agents/marketing/)
- Focus on content creation, SEO, demand generation
- Reference: `../../marketing-skill/`
- Tools: brand_voice_analyzer.py, seo_optimizer.py

### Product Agents (agents/product/)
- Focus on prioritization, user research, agile workflows
- Reference: `../../product-team/`
- Tools: rice_prioritizer.py, user_story_generator.py, okr_cascade_generator.py

### C-Level Agents (agents/c-level/)
- Focus on strategic decision-making
- Reference: `../../c-level-advisor/`
- Tools: Strategic analysis and planning tools

### Engineering Agents (agents/engineering/)
- Focus on scaffolding, code quality, fullstack development
- Reference: `../../engineering-team/`
- Tools: project_scaffolder.py, code_quality_analyzer.py

## Common Pitfalls

**Avoid these mistakes:**

❌ Hardcoding absolute paths
❌ Skipping YAML frontmatter validation
❌ Forgetting to test relative paths
❌ Documenting workflows without examples
❌ Creating agent dependencies (keep them independent)
❌ Duplicating skill content in agent files
❌ Using LLM calls instead of referencing Python tools

## Next Steps

After creating an agent:

1. Test all relative paths resolve
2. Execute all Python tools from agent context
3. Verify all workflows with concrete examples
4. Update agent catalog in main README.md
5. Create GitHub issue for agent testing
6. Commit with conventional commit message: `feat(agents): implement cs-agent-name`

---

**Last Updated:** November 5, 2025
**Current Sprint:** sprint-11-05-2025 (Skill-Agent Integration Phase 1-2)
**Related:** See [main CLAUDE.md](../CLAUDE.md) for repository overview
