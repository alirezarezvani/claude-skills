---
title: Skill Authoring Best Practices Guide
description: "A comprehensive guide to writing high-quality Claude Code skills and agent plugins. Learn the 10 essential patterns, avoid common pitfalls, and create production-ready skills."
---

# Skill Authoring Best Practices Guide

This guide consolidates the essential patterns, practices, and examples for writing high-quality skills for Claude Code and other AI coding tools.

## Quick Navigation

- [The Skill Package](#the-skill-package)
- [SKILL.md Structure](#skillmd-structure)
- [The 10 Essential Patterns](#the-10-essential-patterns)
- [Good vs Bad Examples](#good-vs-bad-examples)
- [Common Pitfalls](#common-pitfalls)
- [Quality Checklist](#quality-checklist)
- [Templates](#templates)

---

## The Skill Package

Every skill is a self-contained package with this structure:

```
skill-name/
├── SKILL.md                    # Required — Core instructions (≤10KB)
├── scripts/                    # Optional — Python CLI tools
│   └── tool_name.py
├── references/                 # Optional — Expert knowledge
│   ├── frameworks.md
│   ├── benchmarks.md
│   └── examples.md
├── assets/                     # Optional — Templates, configs
│   └── template.md
└── .claude-plugin/
    └── plugin.json             # Required for marketplace
```

### File Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Skill folder | `kebab-case` | `senior-architect` |
| Python scripts | `snake_case.py` | `dependency_analyzer.py` |
| Reference docs | `kebab-case.md` | `architecture-patterns.md` |
| Templates | `kebab-case-template.md` | `prd-template.md` |

---

## SKILL.md Structure

### Required YAML Frontmatter

```yaml
---
name: skill-name
description: "When to use this skill. Include trigger keywords and phrases users might say. Mention related skills for disambiguation."
license: MIT
metadata:
  version: 1.0.0
  author: Your Name
  category: domain-name
  updated: YYYY-MM-DD
---
```

### The "Pushy Description" Pattern

The description field should be "pushy" — it should aggressively claim when the skill should activate:

???+ example "Good Description"

    ```yaml
    description: This skill should be used when the user asks to "design system architecture", 
      "evaluate microservices vs monolith", "create architecture diagrams", "analyze dependencies", 
      "choose a database", "plan for scalability", "make technical decisions", or "review system design". 
      Use for architecture decision records (ADRs), tech stack evaluation, system design reviews, 
      dependency analysis, and generating architecture diagrams in Mermaid, PlantUML, or ASCII format.
    ```

??? danger "Bad Description"

    ```yaml
    description: A skill for architecture design.
    ```

### Core Sections

Every SKILL.md should include these sections:

1. **Opening Statement** — Who you are and what you do
2. **Quick Start** — Immediate actionable commands
3. **How This Skill Works** — Modes and workflows
4. **Tools Overview** — Available scripts and their purposes
5. **Proactive Triggers** — Issues to surface without being asked
6. **Output Artifacts** — What the user gets from common requests
7. **Related Skills** — Navigation with WHEN/NOT disambiguation

---

## The 10 Essential Patterns

### Pattern 1: Context-First

**Principle:** Check for existing context before asking questions. Only ask for what's missing.

???+ example "Implementation"

    ```markdown
    ## Before Starting

    **Check for context first:**
    If `marketing-context.md` exists, read it before asking questions. 
    Use that context and only ask for information not already covered 
    or specific to this task.

    Gather this context (ask if not provided):

    ### 1. Current State
    - What exists today?
    - What's working / not working?

    ### 2. Goals
    - What outcome do they want?
    - What constraints exist?
    ```

**Domain Context Files:**

| Domain | Context File | Created By |
|--------|-------------|-----------|
| C-Suite | `company-context.md` | `cs-onboard` skill |
| Marketing | `marketing-context.md` | `marketing-context` skill |
| Engineering | `project-context.md` | `codebase-onboarding` skill |
| Product | `product-context.md` | `product-strategist` skill |
| RA/QM | `regulatory-context.md` | `regulatory-affairs-head` skill |

---

### Pattern 2: Practitioner Voice

**Principle:** Write as a senior practitioner, not a textbook author. Be opinionated and direct.

???+ success "Good"

    ```markdown
    You are an expert in SaaS pricing. Your goal is to help design pricing 
    that captures value. Lead with their world, not yours. If it sounds 
    like marketing copy, rewrite it.
    ```

??? danger "Bad"

    ```markdown
    This skill provides comprehensive coverage of SaaS pricing strategies 
    and methodologies. The following section outlines the various approaches 
    to pricing optimization that one might consider.
    ```

**Rules:**
- Use contractions, direct language
- "Do X" beats "You might consider X"
- Industry jargon is fine when talking to practitioners
- Explain jargon when talking to founders

---

### Pattern 3: Multi-Mode Workflows

**Principle:** Most skills have 2-3 natural entry points. Design for all of them.

???+ example "Implementation"

    ```markdown
    ## How This Skill Works

    ### Mode 1: Build from Scratch
    When starting fresh — no existing architecture to work with.
    Start with requirements gathering, then proceed to design.

    ### Mode 2: Optimize Existing
    When architecture exists but isn't performing. Analyze → 
    identify gaps → recommend improvements.

    ### Mode 3: Migration Planning
    When migrating from one architecture to another. Focus on 
    compatibility, rollback strategies, and phased migration.
    ```

**Common Mode Pairs:**

| Skill Type | Mode 1 | Mode 2 | Mode 3 |
|-----------|--------|--------|--------|
| CRO skills | Audit a page | Redesign flow | A/B test element |
| Content skills | Write new | Rewrite/optimize | Repurpose |
| SEO skills | Full audit | Fix specific issue | Competitive gap |
| Strategy skills | Create plan | Review/critique | Pivot existing |

---

### Pattern 4: Related Skills Navigation

**Principle:** Every skill ends with curated related skills. Include WHEN to use and WHEN NOT to.

???+ example "Implementation"

    ```markdown
    ## Related Skills

    - **copywriting**: For landing page and web copy. NOT for email sequences or ad copy.
    - **page-cro**: For optimizing any marketing page. NOT for signup flows (use signup-flow-cro).
    - **email-sequence**: For lifecycle/nurture emails. NOT for cold outreach (use cold-email).
    - **seo-audit**: For technical SEO analysis. NOT for content optimization (use content-production).
    ```

**Rules:**
- Include 3-7 related skills (curate, don't list everything)
- Each entry: skill name + WHEN to use + WHEN NOT TO
- Cross-references must be bidirectional

---

### Pattern 5: Reference Separation

**Principle:** SKILL.md is the workflow. Reference docs are the knowledge base. Keep them separate.

**File Organization:**

```
skill-name/
├── SKILL.md              # ≤10KB — what to do, how to decide
├── references/
│   ├── frameworks.md      # Deep framework catalog
│   ├── benchmarks.md      # Industry data and benchmarks
│   └── examples.md        # Real-world examples
```

**Linking Pattern:**

```markdown
For detailed architecture patterns, see 
[references/architecture-patterns.md](references/architecture-patterns.md).
```

**Rules:**
- SKILL.md ≤10KB — if longer, move content to references
- Each reference doc is self-contained
- Templates are user-fillable files with clear placeholders

---

### Pattern 6: Proactive Triggers

**Principle:** Surface issues without being asked when detecting patterns in context.

???+ example "Implementation"

    ```markdown
    ## Proactive Triggers

    Surface these without being asked:

    - **Conversion rate >40%** → Flag potential underpricing
    - **Form has >7 fields** → Flag conversion risk, suggest multi-step
    - **No content updated in 6+ months** → Flag content freshness issue
    - **Keyword cannibalization detected** → Flag SEO conflict
    ```

**Rules:**
- 4-6 triggers per skill
- Each trigger: specific condition + business consequence
- Trigger on hidden risks, not obvious things

---

### Pattern 7: Output Artifacts

**Principle:** Map common requests to specific, concrete deliverables.

???+ example "Implementation"

    ```markdown
    ## Output Artifacts

    | When you ask for... | You get... |
    |---------------------|------------|
    | "Help with pricing" | Pricing recommendation with tier structure, value metrics, and competitive positioning |
    | "Audit my SEO" | SEO scorecard (0-100) with prioritized fixes and quick wins |
    | "Review architecture" | Architecture assessment with risk analysis and recommendations |
    ```

**Rules:**
- 4-6 artifacts per skill
- Each artifact has a specific format
- Artifacts are actionable with next steps

---

### Pattern 8: Quality Loop

**Principle:** Skills self-verify before presenting findings.

???+ example "Implementation"

    ```markdown
    ## Communication

    All output passes quality verification:
    - Self-verify: source attribution, assumption audit, confidence scoring
    - Peer-verify: cross-functional claims validated by the owning skill
    - Output format: Bottom Line → What (with confidence) → Why → How to Act
    - Results only. Every finding tagged: 🟢 verified, 🟡 medium, 🔴 assumed.
    ```

**Output Format:**

```
BOTTOM LINE: [One sentence answer]

WHAT:
• [Finding 1] — 🟢/🟡/🔴
• [Finding 2] — 🟢/🟡/🔴

WHY THIS MATTERS: [Business impact]

HOW TO ACT:
1. [Action] → [Owner] → [Deadline]
```

---

### Pattern 9: Communication Standard

**Principle:** Structured output format for all skill output.

**Standard Output Structure:**

1. **Bottom line first** — Always the one-sentence answer
2. **Max 5 bullets per section** — Keep it scannable
3. **Actions have owners and deadlines** — No "we should consider"
4. **Decisions framed as options with trade-offs** — Help the user choose
5. **No process narration** — Results only, skip "First I analyzed..."

---

### Pattern 10: Python Tools

**Principle:** Stdlib-only automation that provides quantitative analysis.

???+ example "Implementation"

    ```python
    #!/usr/bin/env python3
    """
    dependency_analyzer.py - Analyze project dependencies for coupling 
    and circular dependencies.

    Usage:
        python dependency_analyzer.py ./project --output json
    """

    import json
    import sys
    from collections import Counter
    from pathlib import Path

    def main():
        import argparse
        parser = argparse.ArgumentParser(description='Analyze dependencies')
        parser.add_argument('path', help='Project directory')
        parser.add_argument('--output', choices=['json', 'text'], default='text')
        parser.add_argument('--check', choices=['circular', 'outdated'])
        args = parser.parse_args()

        # Analysis logic here...

    if __name__ == "__main__":
        main()
    ```

**Rules:**
- **stdlib-only** — Zero external dependencies
- **CLI-first** — Run from command line with `--help`
- **JSON output** — `--output json` for automation
- **Sample data embedded** — Runs with zero config for demo
- **Scoring uses 0-100 scale** — Consistent across all tools

---

## Good vs Bad Examples

### Description Field

???+ success "Good"

    ```yaml
    description: Use when the user asks to "set up A/B tests", "run experiments", 
      "optimize conversion rate", "test landing pages", or "validate design changes". 
      Triggers for experiment design, hypothesis formation, statistical analysis, 
      and test implementation for marketing pages and user flows.
    ```

??? danger "Bad"

    ```yaml
    description: A skill for A/B testing.
    ```

### Opening Statement

???+ success "Good"

    ```markdown
    You are an expert in conversion rate optimization. Your goal is to 
    identify friction points and recommend data-driven improvements that 
    increase conversions without sacrificing user trust.
    ```

??? danger "Bad"

    ```markdown
    # A/B Testing Skill

    This skill provides comprehensive guidance on A/B testing methodologies 
    for digital marketing optimization.
    ```

### Proactive Triggers

???+ success "Good"

    ```markdown
    ## Proactive Triggers

    - **Page load time >3s** → Flag UX/SEO impact, suggest performance audit
    - **Conversion rate <2%** → Flag potential CRO opportunity
    - **Bounce rate >70%** → Flag content/UX mismatch
    ```

??? danger "Bad"

    ```markdown
    ## Proactive Triggers

    - Check if the page is slow
    - Look for conversion issues
    - Identify problems
    ```

### Related Skills

???+ success "Good"

    ```markdown
    ## Related Skills

    - **seo-audit**: For technical SEO analysis. NOT for conversion optimization.
    - **analytics-tracking**: For setting up metrics. NOT for test design.
    - **landing-page-generator**: For creating pages. NOT for optimizing existing ones.
    ```

??? danger "Bad"

    ```markdown
    ## Related Skills

    - seo-audit
    - analytics-tracking
    - landing-page-generator
    ```

---

## Common Pitfalls

### Pitfall 1: Generic Advice

??? danger "Don't"

    ```markdown
    ## Best Practices

    - Write good content
    - Optimize for keywords
    - Use proper formatting
    ```

???+ success "Do"

    ```markdown
    ## Best Practices

    - **Write for search intent** — Match content to the 4 intent types: 
      informational, navigational, commercial, transactional
    - **Target keyword density 1-2%** — Use the keyword naturally every 
      100-200 words, not stuffed
    - **Use H2-H3 hierarchy** — One H1, multiple H2s for main sections, 
      H3s for subsections
    ```

### Pitfall 2: Missing Trigger Phrases

The description field is how the agent knows when to activate your skill. Without trigger phrases, it won't activate.

??? danger "Don't"

    ```yaml
    description: Architecture design skill.
    ```

???+ success "Do"

    ```yaml
    description: Use when the user asks to "design architecture", "review system design", 
      "evaluate microservices", "create architecture diagram", "analyze dependencies", 
      "choose a database", or "plan for scalability". Covers ADRs, tech stack evaluation, 
      and architecture diagrams in Mermaid, PlantUML, or ASCII.
    ```

### Pitfall 3: SKILL.md Too Long

??? danger "Don't"

    A 500+ line SKILL.md with all knowledge inline.

???+ success "Do"

    A 150-200 line SKILL.md that links to reference files for deep knowledge.

```markdown
For detailed architecture patterns and trade-offs, see 
[references/architecture-patterns.md](references/architecture-patterns.md).
```

### Pitfall 4: Python Tools with Dependencies

??? danger "Don't"

    ```python
    import pandas as pd
    import numpy as np
    from openai import OpenAI
    ```

???+ success "Do"

    ```python
    import json
    import sys
    import csv
    from pathlib import Path
    from collections import Counter
    ```

### Pitfall 5: Missing Disambiguation

??? danger "Don't"

    ```markdown
    ## Related Skills

    - seo-audit
    - content-strategy
    ```

???+ success "Do"

    ```markdown
    ## Related Skills

    - **seo-audit**: For technical SEO analysis. NOT for content planning.
    - **content-strategy**: For editorial calendars. NOT for technical SEO.
    ```

---

## Quality Checklist

Before submitting a skill, verify all items:

### Structure

- [ ] YAML frontmatter with `name`, `description`, `license`, `metadata`
- [ ] Description includes trigger phrases and disambiguation
- [ ] SKILL.md ≤10KB (move heavy content to references)
- [ ] File naming follows conventions (kebab-case folders, snake_case scripts)

### Content

- [ ] Practitioner voice — "You are an expert in X"
- [ ] Context-first — Checks for domain context before asking
- [ ] Multi-mode — At least 2 workflows (build/optimize)
- [ ] Opinionated — States what works, not just options
- [ ] Tables for structured information
- [ ] Checklists for processes

### Integration

- [ ] Related Skills section with WHEN/NOT disambiguation
- [ ] Cross-references are bidirectional
- [ ] Proactive Triggers (4-6 per skill)
- [ ] Output Artifacts table (4-6 per skill)

### Python Tools (if applicable)

- [ ] Stdlib-only (no pip installs)
- [ ] CLI with `--help` support
- [ ] JSON output option (`--output json`)
- [ ] Sample data embedded for demo
- [ ] Scoring uses 0-100 scale

### Marketplace (if publishing)

- [ ] `.claude-plugin/plugin.json` with required fields
- [ ] Listed in category's index file
- [ ] Tested installation via `/plugin install`

---

## Templates

### Minimal SKILL.md Template

```markdown
---
name: skill-name
description: Use when the user asks to "[trigger phrase 1]", "[trigger phrase 2]", 
  or "[trigger phrase 3]". Covers [scope] for [use cases].
license: MIT
metadata:
  version: 1.0.0
  author: Your Name
  category: domain-name
  updated: YYYY-MM-DD
---

# Skill Name

You are an expert in [domain]. Your goal is [specific outcome].

## Before Starting

**Check for context first:**
If `[domain]-context.md` exists, read it before asking questions.

Gather this context (ask if not provided):
- [Context item 1]
- [Context item 2]

## How This Skill Works

### Mode 1: Build from Scratch
[Description]

### Mode 2: Optimize Existing
[Description]

## Proactive Triggers

- **[Condition]** → [What to flag and why]

## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| [Request] | [Deliverable] |

## Related Skills

- **skill-name**: Use when [scenario]. NOT for [disambiguation].
```

### Python Tool Template

```python
#!/usr/bin/env python3
"""
tool_name.py - Brief description of what this tool does.

Usage:
    python tool_name.py input_path [--output json] [--verbose]

Examples:
    python tool_name.py ./project
    python tool_name.py ./project --output json
"""

import argparse
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description='Brief description of tool functionality'
    )
    parser.add_argument('path', help='Path to analyze')
    parser.add_argument(
        '--output', 
        choices=['json', 'text'], 
        default='text',
        help='Output format'
    )
    parser.add_argument(
        '--verbose', 
        action='store_true',
        help='Show detailed output'
    )
    
    args = parser.parse_args()
    
    # Validate input
    path = Path(args.path)
    if not path.exists():
        print(f"Error: Path not found: {args.path}", file=sys.stderr)
        sys.exit(1)
    
    # Process
    result = analyze(path)
    
    # Output
    if args.output == 'json':
        print(json.dumps(result, indent=2))
    else:
        print_human_readable(result, args.verbose)


def analyze(path: Path) -> dict:
    """Analyze the target and return results."""
    result = {
        'path': str(path),
        'score': 0,
        'findings': []
    }
    
    # Analysis logic here...
    
    return result


def print_human_readable(result: dict, verbose: bool = False) -> None:
    """Print results in human-readable format."""
    print(f"Analysis Results for: {result['path']}")
    print(f"Score: {result['score']}/100")
    
    if verbose:
        for finding in result['findings']:
            print(f"  - {finding}")


if __name__ == "__main__":
    main()
```

### plugin.json Template

```json
{
  "name": "skill-name",
  "description": "One-line description for marketplace",
  "version": "1.0.0",
  "author": "your-github-username",
  "homepage": "https://github.com/alirezarezvani/claude-skills",
  "repository": "https://github.com/alirezarezvani/claude-skills",
  "license": "MIT",
  "skills": "./"
}
```

---

## Next Steps

- Read the [Skill Authoring Standard](../skill-authoring-standard.md) for detailed pattern documentation
- Check the [Skill Pipeline](../skill_pipeline.md) for production workflow
- Browse [existing skills](../skills/) for real-world examples
- Join the [discussions](https://github.com/alirezarezvani/claude-skills/discussions) for questions

---

*This guide is part of the claude-skills documentation. Last updated: 2026-03-26.*