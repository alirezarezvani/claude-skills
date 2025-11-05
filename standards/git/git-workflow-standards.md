# Git Workflow Standards

## Core Principles

### **1. Conventional Commits**
- All commits follow conventional commits specification
- Enable automated changelog generation
- Clear categorization of all changes
- Explicit marking of breaking changes

### **2. Semantic Versioning**
- Automated versioning based on commit types
- MAJOR version: BREAKING CHANGE
- MINOR version: feat type commits
- PATCH version: fix type commits

### **3. Branch Protection**
- Main branch requires review
- All quality gates must pass
- No force pushes to main
- Signed commits recommended

## Conventional Commits Specification

### **Commit Message Structure**

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### **Standard Types**

```yaml
feat:     # New features (agents, skills, tools)
fix:      # Bug fixes
docs:     # Documentation only changes
style:    # Formatting changes (no functional impact)
refactor: # Code restructuring without feature changes
perf:     # Performance improvements
test:     # Adding or correcting tests
chore:    # Maintenance tasks (dependencies, build)
ci:       # CI/CD configuration changes
```

### **Examples**

```bash
# New agent implementation
feat(agents): implement cs-content-creator agent

# Bug fix in Python tool
fix(seo-optimizer): correct keyword density calculation

# Documentation update
docs(README): add agent catalog section

# Breaking change
feat(agents)!: replace agent template structure

BREAKING CHANGE: agent frontmatter now requires 'tools' field
```

### **Scopes for Claude Skills**

```yaml
Common Scopes:
  agents:           # Agent implementation
  skills:           # Skill packages
  standards:        # Standards library
  templates:        # Templates
  docs:             # Documentation
  foundation:       # Core infrastructure
  marketing:        # Marketing domain
  c-level:          # C-level domain
  product:          # Product domain
  engineering:      # Engineering domain
  ra-qm:            # RA/QM domain
```

## Branch Strategy

### **Branch Naming Conventions**

```yaml
# Feature branches (agent/skill development)
feature/agents-{name}:         # New agent implementation
feature/skills-{name}:         # New skill package
feature/{domain}-{component}:  # Domain-specific features

# Documentation branches
docs/{component}:              # Documentation updates
docs/standards-{name}:         # Standards library updates

# Bug fixes
fix/{issue-number}-{description}: # Bug fixes

# Hotfixes (critical production issues)
hotfix/{issue}-{description}:   # Emergency fixes

# Test branches
test/{feature}:                # Testing and validation
```

### **Examples**

```bash
# Create feature branch for new agent
git checkout -b feature/agents-ceo-advisor

# Create documentation branch
git checkout -b docs/installation-guide

# Create fix branch
git checkout -b fix/23-broken-relative-paths

# Create test branch
git checkout -b test/agent-path-resolution
```

## Workflow Process

### **1. Development Workflow**

```bash
# Start new feature
git checkout -b feature/agents-product-manager

# Make changes
# ... edit files ...

# Stage changes
git add agents/product/cs-product-manager.md

# Commit with conventional message
git commit -m "feat(agents): implement cs-product-manager agent

- Add YAML frontmatter
- Document RICE prioritization workflow
- Add interview analysis integration
- Test relative path resolution

Phase: 2.3
Issue: #13"

# Push to remote
git push origin feature/agents-product-manager
```

### **2. Pull Request Workflow**

```bash
# Create PR using gh CLI
gh pr create \
  --base main \
  --head feature/agents-product-manager \
  --title "feat(agents): implement cs-product-manager agent" \
  --body "Closes #13

## Summary
Implements product management agent with RICE prioritization and interview analysis.

## Testing
- [x] Relative paths resolve correctly
- [x] Python tools execute successfully
- [x] Workflows documented
- [x] Quality gates pass"
```

### **3. Review & Merge**

```bash
# After review approval
gh pr merge feature/agents-product-manager \
  --squash \
  --delete-branch
```

### **4. Release Workflow**

```bash
# Create release with semantic versioning
git tag v1.0.0-agents
git push origin v1.0.0-agents

# GitHub Actions automatically creates release with changelog
```

## Commit Message Templates

### **For Agent Implementation**

```
feat(agents): implement cs-{agent-name}

- Add YAML frontmatter with required fields
- Document {number} workflows
- Add integration examples
- Test Python tool execution
- Verify relative path resolution

Phase: {phase-number}
Issue: #{issue-number}
```

### **For Skill Development**

```
feat(skills): add {skill-name} to {domain} domain

- Create skill directory structure
- Implement {number} Python automation tools
- Add knowledge base references
- Create user templates

Domain: {domain}
Issue: #{issue-number}
```

### **For Standards Updates**

```
docs(standards): update {standard-name} for {context}

- Adapt for claude-skills context
- Remove factory-specific references
- Add agent-specific guidelines
- Update examples

Issue: #{issue-number}
```

### **For Bug Fixes**

```
fix({scope}): resolve {issue-description}

Problem: {what was broken}
Solution: {what was fixed}
Impact: {who/what this affects}

Fixes #{issue-number}
```

## Git Hooks

### **Pre-commit Hook**

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running pre-commit checks..."

# Check for secrets
if git diff --cached | grep -iE '(api[_-]?key|secret|password|token).*=.*[^x{5}]'; then
    echo "❌ Potential secret detected in commit"
    exit 1
fi

# Validate Python syntax
python -m compileall $(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')
if [ $? -ne 0 ]; then
    echo "❌ Python syntax errors detected"
    exit 1
fi

echo "✅ Pre-commit checks passed"
```

### **Commit-msg Hook**

```bash
#!/bin/bash
# .git/hooks/commit-msg

# Validate conventional commit format
commit_regex='^(feat|fix|docs|style|refactor|perf|test|chore|ci|build|revert)(\([a-z-]+\))?(!)?:\ .{1,}'

if ! head -1 "$1" | grep -qE "$commit_regex"; then
    echo "❌ Commit message does not follow conventional commits format"
    echo "Format: <type>[(scope)]: <description>"
    echo "Example: feat(agents): implement cs-product-manager"
    exit 1
fi

echo "✅ Commit message format valid"
```

## Quality Gates Integration

### **Pre-push Validation**

```bash
#!/bin/bash
# .git/hooks/pre-push

echo "Running pre-push validation..."

# Run quality checks
/review

# Check for TODO comments in production code
if git diff origin/main...HEAD | grep -i "TODO"; then
    echo "⚠️  TODO comments found - consider addressing before push"
fi

echo "✅ Pre-push validation complete"
```

## Branch Protection Rules

### **Main Branch Protection**

```yaml
branch_protection:
  required_status_checks:
    strict: true
    contexts:
      - "ci-quality-gate"
      - "claude-review"

  required_pull_request_reviews:
    required_approving_review_count: 1
    dismiss_stale_reviews: true
    require_code_owner_reviews: false

  enforce_admins: true
  required_conversation_resolution: true
  allow_force_pushes: false
  allow_deletions: false
```

## Common Workflows

### **Hotfix Process**

```bash
# Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-path-resolution

# Fix issue
# ... make changes ...

# Commit with high priority
git commit -m "fix(agents)!: resolve critical path resolution failure

BREAKING CHANGE: agent path resolution now requires absolute project root

Fixes #42
Priority: P0"

# Create PR with hotfix label
gh pr create --label "P0,hotfix" --base main

# After merge, tag immediately
git tag v1.0.1-hotfix
git push origin v1.0.1-hotfix
```

### **Multi-Agent Coordination**

```bash
# Coordinating changes across multiple agents
git checkout -b feature/update-all-marketing-agents

# Update cs-content-creator
git add agents/marketing/cs-content-creator.md
git commit -m "feat(agents): enhance cs-content-creator workflows"

# Update cs-demand-gen-specialist
git add agents/marketing/cs-demand-gen-specialist.md
git commit -m "feat(agents): enhance cs-demand-gen-specialist workflows"

# Push coordinated changes
git push origin feature/update-all-marketing-agents
```

## Best Practices

### **Do's**

- ✅ Use conventional commit format for all commits
- ✅ Reference issue numbers in commit messages
- ✅ Keep commits atomic (one logical change per commit)
- ✅ Write clear, descriptive commit messages
- ✅ Test changes before committing
- ✅ Pull before pushing to avoid conflicts
- ✅ Use feature branches for all changes
- ✅ Delete branches after merging

### **Don'ts**

- ❌ Commit directly to main (use PRs)
- ❌ Force push to shared branches
- ❌ Commit secrets or credentials
- ❌ Mix multiple unrelated changes in one commit
- ❌ Use vague commit messages ("fix stuff", "updates")
- ❌ Skip quality checks
- ❌ Leave branches unmerged for extended periods

## Emergency Procedures

### **Rollback Commit**

```bash
# Revert the last commit (creates new commit)
git revert HEAD

# Revert specific commit
git revert <commit-hash>

# Force rollback (use with caution!)
git reset --hard HEAD~1
git push origin main --force  # Only if absolutely necessary!
```

### **Fix Bad Commit Message**

```bash
# Amend last commit message (before push)
git commit --amend -m "feat(agents): corrected commit message"

# After push (creates new commit)
git revert HEAD
git commit -m "feat(agents): correct implementation with proper message"
```

---

**Standard**: Conventional Commits v1.0.0
**Versioning**: Semantic Versioning v2.0.0
**Updated**: November 2025
**Review**: Monthly git workflow assessment
