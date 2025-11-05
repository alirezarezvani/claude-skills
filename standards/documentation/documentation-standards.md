# Documentation Standards

## Core Principles

### **1. Living Documentation**
- Documentation stays current with code
- Update docs in the same PR as code changes
- Living docs (README, CLAUDE, AGENTS) updated regularly
- Outdated information removed promptly

### **2. Clarity & Accessibility**
- Write for beginners, not experts
- Use simple, clear language
- Provide examples for all concepts
- Include troubleshooting sections

### **3. Structure & Consistency**
- Follow established templates
- Use consistent formatting
- Maintain clear hierarchy
- Keep related content together

## File Naming Conventions

### **General Rules**

```yaml
# Markdown files
README.md           # Repository root (UPPERCASE)
CLAUDE.md           # Repository root (UPPERCASE)
AGENTS.md           # Repository root (UPPERCASE)
CHANGELOG.md        # Repository root (UPPERCASE)
LICENSE             # Repository root (no extension)

# Other documentation (lowercase with hyphens)
installation-guide.md
user-guide.md
api-reference.md
troubleshooting.md
```

### **Directory-Specific Naming**

```yaml
# Agents (lowercase with hyphens)
agents/marketing/cs-content-creator.md
agents/c-level/cs-ceo-advisor.md

# Skills (lowercase, no hyphens in folder names)
marketing-skill/content-creator/SKILL.md

# Standards (lowercase with hyphens)
standards/communication/communication-standards.md

# Documentation (lowercase with hyphens)
documentation/implementation/implementation-plan-november-2025.md
documentation/delivery/sprint-11-05-2025/context.md
```

## Markdown Formatting Standards

### **1. Headings**

```markdown
# H1 - Document Title (only one per file)

## H2 - Major Sections

### H3 - Subsections

#### H4 - Details

**Don't skip heading levels!**
✅ H1 → H2 → H3
❌ H1 → H3 (skips H2)
```

### **2. Lists**

```markdown
# Unordered lists
- Item 1
- Item 2
  - Sub-item 2.1
  - Sub-item 2.2
- Item 3

# Ordered lists
1. First step
2. Second step
3. Third step

# Task lists
- [ ] Incomplete task
- [x] Completed task
```

### **3. Code Blocks**

```markdown
# Inline code
Use `code` for commands, filenames, and variables.

# Code blocks with syntax highlighting
\`\`\`bash
# Bash commands
git commit -m "feat(agents): implement cs-content-creator"
\`\`\`

\`\`\`python
# Python code
def analyze_content(text: str) -> Dict[str, Any]:
    return {"score": 0.85}
\`\`\`

\`\`\`yaml
# YAML configuration
name: cs-content-creator
domain: marketing
\`\`\`
```

### **4. Links**

```markdown
# External links
[Link text](https://example.com)

# Internal links (relative paths)
[Agent catalog](agents/README.md)
[Installation guide](INSTALL.md)

# Link to specific heading
[See quality standards](#quality-standards)

# Reference-style links (for repeated URLs)
[Claude Code][1]
[GitHub][2]

[1]: https://claude.com/code
[2]: https://github.com
```

### **5. Images**

```markdown
# Standard image
![Alt text describing image](path/to/image.png)

# Image with title
![Alt text](image.png "Image title")

# Linked image
[![Alt text](image.png)](https://link-destination.com)

**Always provide alt text for accessibility!**
```

### **6. Tables**

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |

# Alignment
| Left | Center | Right |
|:-----|:------:|------:|
| L1   |   C1   |    R1 |
```

### **7. Emphasis**

```markdown
*Italic text* or _italic text_
**Bold text** or __bold text__
***Bold and italic*** or ___bold and italic___
~~Strikethrough~~

Use **bold** for emphasis, *italic* for definitions.
```

### **8. Blockquotes**

```markdown
> Single line quote

> Multi-line quote
> continues here
> and here

> **Note:** Important information
> highlighted in a quote block
```

### **9. Horizontal Rules**

```markdown
---

Use sparingly to separate major sections.
```

## Document Structure Templates

### **Agent Documentation (agents/*/cs-*.md)**

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
[1-2 paragraphs describing what this agent does]

## Skill Integration

**Skill Location:** `../../skill-folder/`

### Python Tools
[List with usage examples]

### Knowledge Bases
[List with relative paths]

### Templates
[List with relative paths]

## Workflows

### Workflow 1: [Name]
[Step-by-step process]

### Workflow 2: [Name]
[Step-by-step process]

## Integration Examples
[Concrete examples with code]

## Success Metrics
[How to measure effectiveness]

## Related Agents
[Links to related agents]

## References
[Links to documentation]
```

### **README.md Structure**

```markdown
# Project Title

[1-sentence project description]

## Quick Start

[Installation and first use - 30 seconds]

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

[Detailed installation steps]

## Usage

[Basic usage examples]

## Documentation

- [Installation Guide](INSTALL.md)
- [Usage Guide](USAGE.md)
- [Agent Catalog](agents/README.md)

## Contributing

[Contribution guidelines]

## License

[License information]
```

### **SKILL.md Structure**

```markdown
# Skill Name

[1-2 paragraph description]

## What This Skill Does

[Clear explanation of purpose and value]

## Contents

- Python Tools (X scripts)
- Knowledge Bases (X references)
- Templates (X templates)

## Python Automation Tools

### Tool 1: [Name]
**Purpose:** [What it does]
**Usage:**
\`\`\`bash
python scripts/tool-name.py input.txt
\`\`\`

## Knowledge Bases

### Reference 1: [Name]
**Location:** `references/file-name.md`
**Content:** [What's inside]

## Templates

### Template 1: [Name]
**Location:** `assets/template-name.md`
**Use Case:** [When to use]

## Examples

[Real-world usage examples]

## Requirements

- Python 3.8+
- Standard library only (or list dependencies)

## Installation

[How to use this skill]

## Related Skills

[Links to related skills]
```

## Living Documentation

### **Files That Must Stay Current**

```yaml
repository_root:
  README.md:
    update_frequency: "Every major feature"
    purpose: "Primary project documentation"
    audience: "All users"

  CLAUDE.md:
    update_frequency: "Every structural change"
    purpose: "AI context and architecture"
    audience: "Claude Code and developers"

  AGENTS.md:
    update_frequency: "Every agent added/modified"
    purpose: "Agent catalog and reference"
    audience: "Agent developers"

  CHANGELOG.md:
    update_frequency: "Every release"
    purpose: "Version history and changes"
    audience: "All users"
```

### **Update Triggers**

```yaml
update_readme_when:
  - New skill added
  - New agent implemented
  - Installation process changes
  - Major feature added

update_claude_md_when:
  - Directory structure changes
  - Architecture changes
  - New standards added
  - Agent integration patterns change

update_agents_md_when:
  - New agent created
  - Agent modified
  - Agent deprecated
  - Agent template changes
```

## Quality Checklist

### **Pre-Commit Documentation Review**

```yaml
content_quality:
  - [ ] All headings follow hierarchy (no skipped levels)
  - [ ] All code blocks have syntax highlighting
  - [ ] All links work (no 404s)
  - [ ] All images have alt text
  - [ ] No spelling errors
  - [ ] Grammar is correct
  - [ ] Examples are tested and working

formatting:
  - [ ] Consistent heading style
  - [ ] Consistent list formatting
  - [ ] Consistent code block style
  - [ ] No trailing whitespace
  - [ ] Single blank line between sections
  - [ ] Proper indentation

accessibility:
  - [ ] Alt text describes images meaningfully
  - [ ] Link text is descriptive (not "click here")
  - [ ] Heading hierarchy is logical
  - [ ] Tables have headers
  - [ ] Color is not the only way to convey information
```

### **Link Validation**

```bash
# Check for broken markdown links
find . -name "*.md" -exec grep -l "](.*)" {} \; | while read file; do
    echo "Checking links in: $file"
    # Manual check or use markdown-link-check tool
done
```

## Documentation Best Practices

### **Do's**

- ✅ Write for the target audience
- ✅ Use clear, simple language
- ✅ Provide concrete examples
- ✅ Include screenshots where helpful
- ✅ Update docs with code changes
- ✅ Link to related documentation
- ✅ Use consistent terminology
- ✅ Test all code examples

### **Don'ts**

- ❌ Assume prior knowledge
- ❌ Use jargon without explanation
- ❌ Write vague instructions
- ❌ Skip error scenarios
- ❌ Let docs get stale
- ❌ Use "click here" as link text
- ❌ Skip proofreading
- ❌ Forget about mobile users

## Special Documentation Types

### **API Documentation**

```markdown
## Function Name

**Purpose:** What this function does

**Parameters:**
- `param1` (type): Description
- `param2` (type, optional): Description, default: value

**Returns:**
- (type): Description of return value

**Raises:**
- `ExceptionName`: When this is raised

**Example:**
\`\`\`python
result = function_name(param1="value", param2=42)
print(result)
# Output: expected output
\`\`\`
```

### **Troubleshooting Guide**

```markdown
## Problem: [Describe the problem]

**Symptoms:**
- Symptom 1
- Symptom 2

**Cause:**
[What causes this issue]

**Solution:**
1. Step 1
2. Step 2
3. Step 3

**Verification:**
[How to confirm it's fixed]
```

### **Decision Records**

```markdown
# Decision: [Title]

**Date:** YYYY-MM-DD
**Status:** Accepted | Rejected | Superseded

## Context
[What's the situation?]

## Decision
[What did we decide?]

## Rationale
[Why did we decide this?]

## Consequences
[What are the impacts?]

## Alternatives Considered
1. Alternative 1 - [Why rejected]
2. Alternative 2 - [Why rejected]
```

---

**Focus**: Markdown quality, structure consistency, living documentation
**Updated**: November 2025
**Review**: Monthly documentation quality assessment
**Compliance**: Markdown standards, accessibility guidelines
