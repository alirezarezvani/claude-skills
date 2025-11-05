# Standards Library - Claude Code Guidance

This guide explains how to use the standards library for consistent quality across all skills and agents.

## Standards Overview

**Location:** `standards/`

**Available Standards:**
1. **communication/** - Communication principles and response protocols
2. **quality/** - Code quality, testing, and validation standards
3. **git/** - Git workflow, conventional commits, branching strategy
4. **documentation/** - Markdown quality, structure consistency, living docs
5. **security/** - Secret detection, dependency security, input validation

## When to Reference Standards

### Communication Standards

**Reference when:**
- Writing agent documentation
- Creating SKILL.md files
- Drafting user-facing content
- Providing technical guidance

**Key Principles:**
- Absolute honesty - Direct assessments without cushioning
- Zero fluff - Eliminate vague statements
- Pragmatic focus - Actionable suggestions only
- File economy - Edit existing files vs creating new ones

**Location:** `communication/communication-standards.md`

### Quality Standards

**Reference when:**
- Creating Python automation tools
- Writing agent workflows
- Implementing skill features
- Testing integration points

**Key Areas:**
- Python tool quality (PEP 8, type hints, docstrings)
- Agent workflow clarity (minimum 3 workflows documented)
- Testing requirements (functional, integration, documentation)
- Completion criteria (zero defect handoff, validation requirements)

**Location:** `quality/quality-standards.md`

### Git Workflow Standards

**Reference when:**
- Committing code changes
- Creating feature branches
- Tagging releases
- Writing commit messages

**Commit Format:**
```bash
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:** feat, fix, docs, style, refactor, perf, test, chore, ci

**Examples:**
```bash
feat(agents): implement cs-content-creator agent
fix(seo-optimizer): correct keyword density calculation
docs(README): add agent catalog section
```

**Location:** `git/git-workflow-standards.md`

### Documentation Standards

**Reference when:**
- Writing SKILL.md files
- Creating agent documentation
- Updating README files
- Writing reference guides

**Best Practices:**
- Max 200 lines per CLAUDE.md file
- Markdown formatting standards (headings, lists, code blocks)
- Living documentation (README, CLAUDE, AGENTS updated regularly)
- Link validation (no 404s, no broken references)

**Location:** `documentation/documentation-standards.md`

### Security Standards

**Reference when:**
- Writing Python scripts
- Handling user input
- Managing dependencies
- Committing code

**Critical Checks:**
- No hardcoded API keys, passwords, or tokens
- Environment variables for sensitive data
- Input validation for all user input
- Dependency security audits

**Location:** `security/security-standards.md`

## Standards Application Workflow

### For New Skills

```bash
# 1. Reference communication standards
cat standards/communication/communication-standards.md

# 2. Review quality standards for Python tools
cat standards/quality/quality-standards.md

# 3. Follow documentation standards for SKILL.md
cat standards/documentation/documentation-standards.md

# 4. Apply security standards to scripts
cat standards/security/security-standards.md

# 5. Use git standards for commits
cat standards/git/git-workflow-standards.md
```

### For New Agents

```bash
# 1. Communication: Write clear, actionable agent docs
# 2. Quality: Minimum 3 workflows, tested relative paths
# 3. Documentation: Follow agent template structure
# 4. Git: Conventional commit with feat(agents) scope
```

## Standards Hierarchy

**Priority Order:**
1. **Security** - Non-negotiable, always enforced
2. **Quality** - Zero defect handoff required
3. **Git** - Conventional commits for all changes
4. **Documentation** - Living docs stay current
5. **Communication** - Clear, pragmatic, actionable

## Standards Compliance Checklist

### Before Committing Code

- [ ] Communication: Documentation is clear and actionable
- [ ] Quality: All tests passing, code reviewed
- [ ] Git: Conventional commit message format
- [ ] Documentation: Living docs updated if needed
- [ ] Security: No secrets, input validated, dependencies secure

### Before Creating PR

- [ ] All standards compliance checks passed
- [ ] Related documentation updated
- [ ] Examples tested and working
- [ ] No broken links or references

## Related Documentation

- **Main CLAUDE.md:** `../CLAUDE.md`
- **Agent Development:** `../agents/CLAUDE.md`
- **Domain Skills:** See navigation map in main CLAUDE.md

---

**Last Updated:** November 5, 2025
**Standards Count:** 5 comprehensive standards
**Enforcement:** Required for all skills and agents
