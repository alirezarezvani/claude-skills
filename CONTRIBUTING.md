# Contributing to Claude Code Skills

Thank you for your interest in contributing! This repository is the largest open-source Claude Code skills & agent plugins library (6,800+ stars, 205 production-ready skills).

**Before you start:** Read [CONVENTIONS.md](CONVENTIONS.md) — it contains the mandatory technical rules that every contribution must follow. PRs that violate conventions will be closed.

---

## Target Branch: `dev`

**All PRs must target the `dev` branch.** PRs targeting `main` will be closed automatically.

```bash
git clone https://github.com/YOUR_USERNAME/claude-skills.git
cd claude-skills
git remote add upstream https://github.com/alirezarezvani/claude-skills.git
git fetch upstream dev
git checkout -b feature/my-skill upstream/dev
```

---

## What We Accept

### New Skills

Add domain expertise that doesn't already exist in the repo:
- Engineering tools and workflows
- Marketing, sales, customer success patterns
- Product management frameworks
- Regulatory and compliance (ISO, SOC, GDPR, FDA)
- Business functions (finance, HR, operations)

**Before building:** Check existing skills to avoid overlap. Open an issue to discuss if unsure.

### Improvements to Existing Skills

- Better workflows and actionable patterns
- Additional Python automation scripts
- New reference material
- More code examples and cross-references
- Bug fixes in scripts or documentation

### Bug Fixes

- Python scripts that fail `--help`
- Broken cross-references between skills
- Incorrect information in reference docs

---

## What We Do NOT Accept

| Type | Reason |
|------|--------|
| Links to external repos/tools in README | No 3rd party promotion |
| Skills requiring paid API keys | Must work without external services |
| Scripts with pip dependencies | stdlib-only Python |
| PRs that change the skill count (205) | Curated number |
| PRs modifying `.codex/`, `.gemini/`, `marketplace.json` | Auto-generated files |
| Bloated diffs with fork merge history | Rebase on `dev` first |
| Generic advice without actionable frameworks | Must be executable by an AI agent |

---

## Skill Creation Guide

### 1. Create the directory

```bash
# Example: new engineering skill
mkdir -p engineering/my-new-skill/scripts
mkdir -p engineering/my-new-skill/references
```

### 2. Write SKILL.md

**Frontmatter — only `name` and `description`:**

```yaml
---
name: "my-new-skill"
description: "Use when the user asks to [specific trigger]. Covers [key capabilities]."
---
```

> **Important:** Do NOT add `license`, `metadata`, `triggers`, `version`, `author`, or any other fields. See [CONVENTIONS.md](CONVENTIONS.md) for the full specification.

**Content must be:**
- Under 500 lines (move detailed content to `references/`)
- Opinionated (recommend specific approaches)
- Actionable (agent can execute, not just advise)
- Include anti-patterns and cross-references sections

### 3. Write Python scripts (optional but valuable)

```python
#!/usr/bin/env python3
"""Tool Name — brief description."""

import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser(description="Tool description")
    parser.add_argument("input", help="Input file or value")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    # Your logic here
    result = {"status": "ok"}

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Result: {result['status']}")

if __name__ == "__main__":
    main()
```

**Script rules:** stdlib-only, argparse, `--help`, `--json`, proper exit codes (0/1/2). See [CONVENTIONS.md](CONVENTIONS.md) for full requirements.

### 4. Add reference docs (optional)

Place detailed material in `references/`:
```
my-new-skill/references/
├── patterns.md          # Detailed patterns and examples
├── best-practices.md    # Best practices guide
└── decision-matrix.md   # Comparison tables
```

Reference them from SKILL.md:
```markdown
> See [references/patterns.md](references/patterns.md) for detailed patterns.
```

### 5. Validate before submitting

```bash
# Structure validation
python3 engineering/skill-tester/scripts/skill_validator.py <your-skill-path>

# Script testing
python3 engineering/skill-tester/scripts/script_tester.py <your-skill-path> --verbose

# Security audit
python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py <your-skill-path> --strict
```

---

## PR Checklist

Before submitting your PR, verify:

- [ ] **Targets `dev` branch** (not `main`)
- [ ] **SKILL.md frontmatter** has only `name` + `description`
- [ ] **SKILL.md under 500 lines** (detailed content in `references/`)
- [ ] **All scripts pass** `python3 script.py --help`
- [ ] **Scripts use stdlib only** (no pip dependencies)
- [ ] **Scripts support `--json` output**
- [ ] **Anti-patterns section** included in SKILL.md
- [ ] **Cross-references** to related skills included
- [ ] **No modifications** to `.codex/`, `.gemini/`, `marketplace.json`, or index files
- [ ] **No 3rd party links** added to README
- [ ] **Clean diff** — rebased on `dev`, no merge commit history
- [ ] **Security audit passes** with zero CRITICAL/HIGH findings

---

## Commit Messages

[Conventional Commits](https://www.conventionalcommits.org/) format:

```
feat(engineering): add browser-automation skill
fix(self-improving-agent): use absolute path for hooks
improve(tdd-guide): add per-language examples
docs: update CONTRIBUTING.md
```

---

## PR Description Template

```markdown
## Summary
- What: [What does this add/change/fix?]
- Why: [Why is this valuable?]

## Checklist
- [x] Targets dev branch
- [x] SKILL.md frontmatter: name + description only
- [x] Under 500 lines
- [x] Scripts pass --help
- [x] Security audit: 0 critical/high findings
```

---

## After Your PR is Merged

Maintainers will handle:
1. Running sync scripts (Codex, Gemini, integrations)
2. Generating docs pages
3. Updating mkdocs.yml navigation
4. Updating domain plugin.json counts
5. Updating marketplace.json
6. Merging dev → main for deployment

You do NOT need to do any of these steps in your PR.

---

## Recognition

Contributors are credited via:
- `Co-Authored-By:` in commit messages
- PR merge messages and changelogs
- Attribution in SKILL.md when skills are improved from community submissions

---

## Questions?

- **General:** Open a [discussion](https://github.com/alirezarezvani/claude-skills/discussions)
- **Bugs:** Use the [issue tracker](https://github.com/alirezarezvani/claude-skills/issues)
- **Contact:** [alirezarezvani.com](https://alirezarezvani.com)

---

**Full technical conventions:** [CONVENTIONS.md](CONVENTIONS.md)
