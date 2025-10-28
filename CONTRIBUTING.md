# Contributing to Claude Skills Library

Thank you for your interest in contributing to the Claude Skills Library! This repository aims to democratize professional expertise through reusable, production-ready skill packages for Claude AI.

## 🎯 Ways to Contribute

### 1. Create New Skills

Add domain expertise in your field:
- Marketing, sales, customer success
- Engineering specializations
- Business functions (finance, HR, operations)
- Industry-specific skills (FinTech, EdTech, etc.)

### 2. Enhance Existing Skills

Improve current skills with:
- Better frameworks and templates
- Additional Python automation tools
- Updated best practices
- More reference materials
- Real-world examples and case studies

### 3. Improve Documentation

Help others use skills effectively:
- Clearer how-to guides
- Additional usage examples
- Better README files
- Translations to other languages

### 4. Fix Bugs

Report or fix issues in:
- Python scripts
- Documentation errors
- Broken links
- Outdated information

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7+ (for running/testing scripts)
- Git and GitHub account
- Claude AI or Claude Code account (for testing skills)
- Familiarity with the skill domain you're contributing to

### Fork and Clone

```bash
# Fork the repository on GitHub first
git clone https://github.com/YOUR_USERNAME/claude-skills.git
cd claude-skills

# Add upstream remote
git remote add upstream https://github.com/alirezarezvani/claude-skills.git
```

### Create a Branch

```bash
# Create feature branch
git checkout -b feature/my-new-skill

# Or for improvements
git checkout -b improvement/enhance-content-creator
```

---

## 📝 Skill Creation Guidelines

### Following Anthropic's Official Spec

All skills must follow [Anthropic's Agent Skills Specification](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview).

### Required Structure

```
your-skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description, license, metadata)
│   └── Markdown content (instructions, examples, workflows)
├── scripts/ (optional but recommended)
│   ├── tool1.py
│   ├── tool2.py
│   └── tool3.py
├── references/ (optional but recommended)
│   ├── framework.md
│   ├── best-practices.md
│   └── examples.md
└── assets/ (optional)
    └── templates/
```

### SKILL.md Requirements

**YAML Frontmatter (required):**
```yaml
---
name: your-skill-name
description: What it does and when to use it. Include specific triggers and keywords.
license: MIT
metadata:
  version: 1.0.0
  author: Your Name
  category: domain-category
  updated: 2025-10-28
---
```

**Markdown Content (required):**
- Clear heading and overview
- Keywords section for discovery
- Quick start guide
- Core workflows
- Script documentation (if applicable)
- Reference guide (if applicable)
- Best practices
- Examples

**Target Length:** 100-200 lines for SKILL.md
- Keep core instructions lean
- Move detailed content to references/
- Follow progressive disclosure principle

### Python Script Standards

**Quality Requirements:**
- Production-ready code (not placeholders)
- Standard library preferred (minimal dependencies)
- CLI-first design with --help support
- JSON output option for automation
- Clear docstrings and comments
- Error handling and validation

**Example:**
```python
#!/usr/bin/env python3
"""
Tool Name - Brief description

Usage:
    python tool.py input.txt [--output json]
"""

def main():
    # Implementation
    pass

if __name__ == "__main__":
    main()
```

### Documentation Standards

- Clear, actionable guidance
- Real-world examples
- Specific metrics and benchmarks
- No generic advice
- Professional tone
- Proper formatting

---

## 🔄 Contribution Process

### Step 1: Discuss First (Recommended)

For major contributions:
1. Open an issue describing your idea
2. Discuss approach with maintainers
3. Get feedback before investing time
4. Avoid duplicate efforts

### Step 2: Develop Your Contribution

Follow the guidelines above for:
- New skills
- Python tools
- Documentation
- Bug fixes

### Step 3: Test Thoroughly

**For New Skills:**
- [ ] YAML frontmatter valid (no syntax errors)
- [ ] Description triggers Claude correctly
- [ ] All Python scripts work with --help
- [ ] All reference links work
- [ ] Skill activates when expected
- [ ] Tested with Claude AI or Claude Code

**For Python Tools:**
- [ ] Runs without errors
- [ ] Handles edge cases
- [ ] Provides helpful error messages
- [ ] JSON output works (if applicable)
- [ ] Dependencies documented

### Step 4: Submit Pull Request

```bash
# Commit your changes
git add .
git commit -m "feat(domain): add new-skill with [capabilities]"

# Push to your fork
git push origin feature/my-new-skill

# Create pull request on GitHub
```

**PR Title Format:**
- `feat(domain): add new skill for [purpose]`
- `fix(skill-name): correct issue with [component]`
- `docs(domain): improve documentation for [topic]`
- `refactor(skill-name): optimize [component]`

**PR Description Must Include:**
- What: What does this add/change/fix?
- Why: Why is this valuable?
- Testing: How was it tested?
- Documentation: What docs were updated?

---

## ✅ Quality Standards

### Skill Quality Checklist

All new skills must meet these standards:

**Documentation:**
- [ ] Clear SKILL.md with all required sections
- [ ] Enhanced description with triggers and keywords
- [ ] Keywords section for discovery
- [ ] Quick start guide with 2-3 examples
- [ ] Professional metadata (license, version, author)
- [ ] Domain-specific README updated (if applicable)

**Python Tools (if included):**
- [ ] Production-ready code (not placeholders)
- [ ] CLI with --help support
- [ ] Proper error handling
- [ ] Clear docstrings
- [ ] Dependencies minimal and documented

**References (if included):**
- [ ] Actionable frameworks and templates
- [ ] Specific guidance (not generic advice)
- [ ] Real-world benchmarks and examples
- [ ] Properly linked from SKILL.md

**Testing:**
- [ ] Skill activates correctly with Claude
- [ ] All scripts execute without errors
- [ ] All links work
- [ ] No broken references

**ROI:**
- [ ] Demonstrates measurable value
- [ ] Time savings quantified
- [ ] Quality improvements specified
- [ ] Clear use cases documented

---

## 🎨 Style Guide

### Python Code

**Follow PEP 8:**
- 4 spaces for indentation
- Max line length: 100 characters
- Clear variable names
- Docstrings for functions

**Example:**
```python
def analyze_content(text: str, keywords: list) -> dict:
    """
    Analyze text content for keyword density and readability.

    Args:
        text: Content to analyze
        keywords: List of keywords to check

    Returns:
        dict: Analysis results with scores and recommendations
    """
    pass
```

### Markdown Documentation

- Use headers consistently (H1 for title, H2 for sections)
- Include code blocks with language specification
- Use tables for comparisons
- Add emojis sparingly for visual hierarchy
- Keep paragraphs concise

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat(domain): add new capability`
- `fix(skill): correct bug in script`
- `docs(readme): update installation guide`
- `refactor(skill): optimize SKILL.md length`
- `test(tool): add test coverage`

---

## 🏆 Recognition

### Contributors

All contributors will be:
- Listed in CHANGELOG.md for their contributions
- Mentioned in release notes
- Credited in PR merge messages
- Acknowledged in the community

### Significant Contributions

Major contributions may result in:
- Co-author credit in commits
- Feature attribution in documentation
- Highlighted in README
- Social media recognition

---

## 📋 Domain-Specific Guidelines

### Marketing Skills

- Include real benchmarks (CAC, conversion rates, etc.)
- Platform-specific guidance (LinkedIn, Google, etc.)
- B2B or B2C focus clearly stated
- International market considerations

### Engineering Skills

- Include tech stack in metadata
- Provide architecture patterns
- Add code quality standards
- Performance benchmarks

### Product Skills

- Include frameworks (RICE, OKR, etc.)
- Real-world metrics and KPIs
- Template-heavy with examples
- Integration points with tools

### Regulatory/Quality Skills

- Cite specific standards (ISO, FDA, EU MDR)
- Compliance frameworks clear
- Industry-specific (HealthTech, MedTech)
- Regulatory jurisdiction specified

---

## 🚫 What NOT to Contribute

**We will not accept:**
- Generic advice without actionable frameworks
- Placeholder scripts (must be production-ready)
- Skills without clear use cases
- Duplicate capabilities of existing skills
- Proprietary or confidential information
- Content that violates licenses
- Skills promoting unethical practices

---

## 🤝 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

Expected behavior:
- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the community
- Show empathy and kindness

---

## 📞 Questions?

- **General Questions:** Open a [discussion](https://github.com/alirezarezvani/claude-skills/discussions)
- **Bug Reports:** Use [bug report template](https://github.com/alirezarezvani/claude-skills/issues/new?template=bug_report.md)
- **Feature Ideas:** Use [feature request template](https://github.com/alirezarezvani/claude-skills/issues/new?template=feature_request.md)
- **Contact:** [alirezarezvani.com](https://alirezarezvani.com) or [medium.com/@alirezarezvani](https://medium.com/@alirezarezvani)

---

## 🙏 Thank You!

Your contributions help make world-class expertise accessible to everyone through Claude AI. Every skill added, bug fixed, or documentation improved makes a difference.

**Happy contributing!** 🚀
