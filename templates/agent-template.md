---
name: cs-agent-name
description: One-line description of what this agent does (keep under 150 characters)
skills: skill-folder-name
domain: domain-name
model: sonnet
tools: [Read, Write, Bash, Grep, Glob]
---

# Agent Name

<!--
  INSTRUCTIONS FOR USING THIS TEMPLATE:

  1. Replace "cs-agent-name" with your agent's name (use kebab-case with cs- prefix)
  2. Replace "Agent Name" with the display name (Title Case)
  3. Fill in all sections below following the structure
  4. Test all relative paths (../../) before committing
  5. Ensure minimum 3 workflows documented
  6. Provide concrete integration examples
  7. Define measurable success metrics

  EXAMPLES OF COMPLETED AGENTS:
  - agents/marketing/cs-content-creator.md
  - agents/marketing/cs-demand-gen-specialist.md
  - agents/c-level/cs-ceo-advisor.md
  - agents/c-level/cs-cto-advisor.md
  - agents/product/cs-product-manager.md
-->

## Purpose

<!--
  Write 2-3 paragraphs describing:
  - What this agent does
  - Who it's designed for (target users)
  - How it enables better decisions/outcomes
  - The specific gap it bridges

  Example structure:
  Paragraph 1: Agent's primary function and skill orchestration
  Paragraph 2: Target audience and their pain points
  Paragraph 3: Value proposition and outcome focus
-->

[Paragraph 1: Describe what this agent does and which skill package it orchestrates]

[Paragraph 2: Describe target users, their roles, and why they need this agent]

[Paragraph 3: Explain the gap this agent bridges and the outcomes it enables]

## Skill Integration

**Skill Location:** `../../domain-skill/skill-name/`

<!--
  Document how this agent integrates with the underlying skill package.
  Test all paths to ensure they resolve correctly from agents/domain/ directory.
-->

### Python Tools

<!--
  List all Python automation tools from the skill package.
  Minimum 1 tool, ideally 2-4 tools.

  For each tool, provide:
  - Clear purpose statement
  - Exact file path (relative from agent location)
  - Usage examples with arguments
  - Key features
  - Common use cases
-->

1. **Tool Name**
   - **Purpose:** What this tool does (one sentence)
   - **Path:** `../../domain-skill/skill-name/scripts/tool_name.py`
   - **Usage:** `python ../../domain-skill/skill-name/scripts/tool_name.py [arguments]`
   - **Features:** Key capabilities (bullet list)
   - **Use Cases:** When to use this tool

2. **Second Tool** (if applicable)
   - **Purpose:** What this tool does
   - **Path:** `../../domain-skill/skill-name/scripts/second_tool.py`
   - **Usage:** `python ../../domain-skill/skill-name/scripts/second_tool.py [arguments]`
   - **Features:** Key capabilities
   - **Use Cases:** When to use this tool

### Knowledge Bases

<!--
  List reference documentation from the skill package.
  These are markdown files with frameworks, best practices, templates.
-->

1. **Reference Name**
   - **Location:** `../../domain-skill/skill-name/references/reference_file.md`
   - **Content:** What knowledge this file contains
   - **Use Case:** When to consult this reference

2. **Second Reference** (if applicable)
   - **Location:** `../../domain-skill/skill-name/references/second_reference.md`
   - **Content:** What knowledge this file contains
   - **Use Case:** When to consult this reference

### Templates

<!--
  List user-facing templates from the skill package's assets/ folder.
  Optional section - only if skill has templates.
-->

1. **Template Name** (if applicable)
   - **Location:** `../../domain-skill/skill-name/assets/template.md`
   - **Use Case:** When users would copy and customize this template

## Workflows

<!--
  Document MINIMUM 3 workflows. Ideally 4 workflows.
  Each workflow must have: Goal, Steps, Expected Output, Time Estimate

  Workflow types to consider:
  - Primary use case (most common)
  - Advanced use case (complex scenario)
  - Integration use case (combining multiple tools)
  - Automated workflow (scripting/batching)
-->

### Workflow 1: [Primary Use Case Name]

**Goal:** One-sentence description of what this workflow accomplishes

**Steps:**
1. **[Action Step]** - Description of first step
   ```bash
   # Command example if applicable
   python ../../domain-skill/skill-name/scripts/tool.py input.txt
   ```
2. **[Action Step]** - Description of second step
3. **[Action Step]** - Description of third step
4. **[Action Step]** - Description of fourth step
5. **[Action Step]** - Description of final step

**Expected Output:** What success looks like (deliverable, metric, decision made)

**Time Estimate:** How long this workflow typically takes

**Example:**
```bash
# Complete workflow example with real commands
command1
command2
# Review output
```

### Workflow 2: [Advanced Use Case Name]

**Goal:** One-sentence description

**Steps:**
1. **[Action Step]** - Description
2. **[Action Step]** - Description
3. **[Action Step]** - Description
4. **[Action Step]** - Description

**Expected Output:** What success looks like

**Time Estimate:** Duration estimate

### Workflow 3: [Integration Use Case Name]

**Goal:** One-sentence description

**Steps:**
1. **[Action Step]** - Description
2. **[Action Step]** - Description
3. **[Action Step]** - Description

**Expected Output:** What success looks like

**Time Estimate:** Duration estimate

### Workflow 4: [Optional Fourth Workflow]

<!-- Delete this section if you only have 3 workflows -->

**Goal:** One-sentence description

**Steps:**
1. **[Action Step]** - Description
2. **[Action Step]** - Description

**Expected Output:** What success looks like

**Time Estimate:** Duration estimate

## Integration Examples

<!--
  Provide 2-3 concrete code examples showing real-world usage.
  These should be copy-paste ready bash scripts or commands.

  Example types:
  - Weekly/daily automation scripts
  - Multi-tool workflows
  - Output processing examples
  - Real-time monitoring
-->

### Example 1: [Example Name]

```bash
#!/bin/bash
# script-name.sh - Brief description

# Setup variables
INPUT_FILE=$1

# Execute workflow
python ../../domain-skill/skill-name/scripts/tool.py "$INPUT_FILE"

# Process output
echo "Analysis complete. Review results above."
```

### Example 2: [Example Name]

```bash
# Multi-step workflow example

# Step 1: Prepare data
echo "Step 1: Data preparation"

# Step 2: Run analysis
python ../../domain-skill/skill-name/scripts/tool.py input.csv

# Step 3: Generate report
echo "Report generation complete"
```

### Example 3: [Example Name]

```bash
# Automation example (e.g., weekly report, daily check)

DATE=$(date +%Y-%m-%d)
echo "📊 Report for $DATE"

# Execute tools
python ../../domain-skill/skill-name/scripts/tool.py current-data.csv > report-$DATE.txt
```

## Success Metrics

<!--
  Define how to measure this agent's effectiveness.
  Group metrics into logical categories (3-4 categories).
  Each metric should be specific and measurable.

  Categories might include:
  - Quality metrics
  - Efficiency metrics
  - Business impact metrics
  - User satisfaction metrics
-->

**[Metric Category 1]:**
- **[Metric Name]:** Target value or improvement percentage
- **[Metric Name]:** Target value or improvement percentage
- **[Metric Name]:** Target value or improvement percentage

**[Metric Category 2]:**
- **[Metric Name]:** Target value or improvement percentage
- **[Metric Name]:** Target value or improvement percentage

**[Metric Category 3]:**
- **[Metric Name]:** Target value or improvement percentage
- **[Metric Name]:** Target value or improvement percentage

**[Metric Category 4]** (optional):
- **[Metric Name]:** Target value or improvement percentage

## Related Agents

<!--
  Cross-reference other agents in the same domain or related domains.
  Use relative paths from agents/ directory.
  Explain how agents complement each other.
-->

- [cs-related-agent](../domain/cs-related-agent.md) - How this agent relates (e.g., "Provides strategic context for tactical execution")
- [cs-another-agent](cs-another-agent.md) - How this agent relates (same directory)
- [cs-future-agent](cs-future-agent.md) - Planned agent (mark as "planned")

## References

<!--
  Link to all related documentation.
  Always include these three links with correct relative paths.
-->

- **Skill Documentation:** [../../domain-skill/skill-name/SKILL.md](../../domain-skill/skill-name/SKILL.md)
- **Domain Guide:** [../../domain-skill/CLAUDE.md](../../domain-skill/CLAUDE.md)
- **Agent Development Guide:** [../CLAUDE.md](../CLAUDE.md)

---

<!--
  Update metadata when publishing.
  Sprint format: sprint-MM-DD-YYYY
  Status: Production Ready, Beta, Alpha
-->

**Last Updated:** [Date]
**Sprint:** [sprint-MM-DD-YYYY] (Day X)
**Status:** Production Ready
**Version:** 1.0
