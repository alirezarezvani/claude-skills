# Development Workflow

**Repository:** claude-code-skills
**Branch Strategy:** feature → dev → main (PR only)
**Last Updated:** November 5, 2025

---

## Quick Start

```bash
# 1. Always start from dev
git checkout dev
git pull origin dev

# 2. Create feature branch
git checkout -b feature/agents-{name}

# 3. Work and commit
git add .
git commit -m "feat(agents): implement {name}"

# 4. Push to remote
git push origin feature/agents-{name}

# 5. Create PR to dev (NOT main)
gh pr create --base dev --head feature/agents-{name}

# 6. After PR approved and merged, delete feature branch
git branch -d feature/agents-{name}
```

---

## Branch Structure

### Main Branches

**main**
- Production-ready code only
- Protected: requires PR approval
- No direct pushes allowed
- Tagged releases only

**dev**
- Integration branch
- All feature branches merge here first
- Testing and validation happens here
- Periodically merged to main via PR

### Feature Branches

**Naming Convention:**
```bash
feature/{domain}-{component}      # New features
fix/{issue-number}-{description}  # Bug fixes
docs/{component}                  # Documentation updates
refactor/{component}              # Code refactoring
test/{feature}                    # Testing updates
```

**Examples:**
```bash
feature/agents-cfo-advisor
feature/marketing-email-campaign-tool
fix/42-broken-relative-paths
docs/installation-guide
refactor/skill-directory-structure
test/python-tool-integration
```

---

## Daily Workflow

### Starting New Work

```bash
# 1. Update dev branch
git checkout dev
git pull origin dev

# 2. Create feature branch (use correct naming)
git checkout -b feature/agents-data-scientist

# 3. Verify you're on the right branch
git branch
# Should show: * feature/agents-data-scientist
```

### Making Changes

```bash
# 1. Make your changes
# ... edit files ...

# 2. Check status
git status

# 3. Stage changes
git add agents/engineering/cs-data-scientist.md

# 4. Commit with conventional commit format
git commit -m "feat(agents): implement cs-data-scientist agent

- Add YAML frontmatter with required fields
- Document 4 workflows (data analysis, ML pipeline, A/B testing, metrics dashboard)
- Add integration with data analysis Python tools
- Test relative path resolution

Issue: #25"

# 5. Continue working or push
```

### Pushing to Remote

```bash
# 1. Push feature branch to remote
git push origin feature/agents-data-scientist

# 2. If first push, set upstream
git push -u origin feature/agents-data-scientist
```

### Creating Pull Request

```bash
# 1. Create PR to dev (NOT main!)
gh pr create \
  --base dev \
  --head feature/agents-data-scientist \
  --title "feat(agents): implement cs-data-scientist agent" \
  --body "Closes #25

## Summary
Implements data scientist agent with ML pipeline workflows and statistical analysis tools.

## Changes
- Created cs-data-scientist.md (425 lines)
- Added 4 complete workflows
- Integrated with 3 Python tools
- Tested all relative paths

## Testing
- [x] YAML frontmatter valid
- [x] Relative paths resolve correctly
- [x] Python tools execute successfully
- [x] All workflows documented with examples
- [x] Success metrics defined

## Checklist
- [x] Follows communication standards
- [x] Meets quality standards
- [x] Conventional commit format
- [x] Documentation updated
- [x] No security issues"

# 2. Verify PR created
gh pr list
```

### After PR Approval

```bash
# 1. PR gets approved and merged to dev by reviewer
# (automatic via GitHub UI or gh CLI by reviewer)

# 2. Switch back to dev
git checkout dev

# 3. Pull latest (includes your merged changes)
git pull origin dev

# 4. Delete local feature branch
git branch -d feature/agents-data-scientist

# 5. Delete remote feature branch (if not auto-deleted)
git push origin --delete feature/agents-data-scientist
```

---

## Branch Protection Rules

### Main Branch (Protected)

**Requirements:**
- ✅ Pull request required (no direct push)
- ✅ 1 approval required
- ✅ Dismiss stale reviews
- ✅ Require conversation resolution
- ✅ Enforce for admins
- ❌ No force pushes
- ❌ No deletions

**Implications:**
- You cannot `git push origin main` directly
- All changes must go through PR process
- Reviewers must approve before merge
- CI checks must pass (when configured)

### Dev Branch (Unprotected)

**Current State:**
- Direct push allowed (but discouraged)
- PRs from feature branches preferred
- Integration testing happens here

**Best Practice:**
- Still use PRs for feature branches → dev
- Allows multiple developers to work in parallel
- Easier to review changes in isolation

---

## Common Scenarios

### Scenario 1: New Agent Development

```bash
# Start work
git checkout dev
git pull origin dev
git checkout -b feature/agents-product-designer

# Create agent file
vim agents/product/cs-product-designer.md

# Commit
git add agents/product/cs-product-designer.md
git commit -m "feat(agents): implement cs-product-designer agent"

# Push
git push origin feature/agents-product-designer

# Create PR to dev
gh pr create --base dev --head feature/agents-product-designer

# After merge, cleanup
git checkout dev
git pull origin dev
git branch -d feature/agents-product-designer
```

### Scenario 2: Bug Fix

```bash
# Start from dev
git checkout dev
git pull origin dev
git checkout -b fix/34-yaml-validation-error

# Fix the bug
vim agents/marketing/cs-content-creator.md

# Commit
git add agents/marketing/cs-content-creator.md
git commit -m "fix(agents): correct YAML frontmatter in cs-content-creator

Problem: YAML frontmatter missing 'tools' field causing validation errors
Solution: Added tools: [Read, Write, Bash, Grep, Glob] to frontmatter
Impact: All agents now validate correctly

Fixes #34"

# Push and PR
git push origin fix/34-yaml-validation-error
gh pr create --base dev --head fix/34-yaml-validation-error
```

### Scenario 3: Documentation Update

```bash
# Start from dev
git checkout dev
git pull origin dev
git checkout -b docs/workflow-guide

# Update documentation
vim documentation/WORKFLOW.md

# Commit
git add documentation/WORKFLOW.md
git commit -m "docs(workflow): add branch protection section"

# Push and PR
git push origin docs/workflow-guide
gh pr create --base dev --head docs/workflow-guide
```

### Scenario 4: Sprint Work

```bash
# Sprint planning complete, ready to implement
git checkout dev
git pull origin dev
git checkout -b feature/sprint-11-12-2025

# Work on multiple related files
git add agents/engineering/cs-ml-engineer.md
git commit -m "feat(agents): implement cs-ml-engineer"

git add agents/engineering/cs-devops-engineer.md
git commit -m "feat(agents): implement cs-devops-engineer"

git add documentation/delivery/sprint-11-12-2025/PROGRESS.md
git commit -m "docs(sprint): update progress tracker"

# Push all commits
git push origin feature/sprint-11-12-2025

# Create PR
gh pr create --base dev --head feature/sprint-11-12-2025
```

### Scenario 5: Hotfix (Critical Bug in Production)

```bash
# Start from main for hotfixes
git checkout main
git pull origin main
git checkout -b hotfix/critical-path-resolution

# Fix critical issue
vim agents/product/cs-product-manager.md

# Commit
git commit -am "fix(agents)!: resolve critical path resolution failure

BREAKING CHANGE: relative paths now require project root reference

Fixes #89
Priority: P0"

# Push to remote
git push origin hotfix/critical-path-resolution

# Create PR directly to main (exception for hotfixes)
gh pr create --base main --head hotfix/critical-path-resolution --label "P0,hotfix"

# After merge to main, also merge to dev
git checkout dev
git merge main
git push origin dev
```

---

## Merge Strategy

### Feature → Dev

```bash
# Prefer squash merge for clean history
gh pr merge feature/agents-new-agent \
  --squash \
  --delete-branch
```

### Dev → Main

```bash
# Create PR from dev to main
git checkout dev
git pull origin dev
gh pr create --base main --head dev \
  --title "release: merge dev to main for v2.1.0" \
  --body "## Release v2.1.0

### New Features
- cs-data-scientist agent
- cs-ml-engineer agent
- cs-devops-engineer agent

### Bug Fixes
- Fixed YAML validation in cs-content-creator
- Corrected relative paths in cs-product-manager

### Documentation
- Added WORKFLOW.md
- Updated sprint progress trackers

### Testing
- All agents validated (100% pass rate)
- All Python tools tested
- All reference files accessible"

# After approval, use merge commit (preserve dev history)
gh pr merge dev --merge --delete-branch=false
```

---

## Quality Checks

### Before Committing

```bash
# 1. Verify no secrets
git diff --cached | grep -iE '(api[_-]?key|secret|password|token).*=.*[^x{5}]'

# 2. Validate Python syntax (if Python files changed)
python3 -m py_compile $(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')

# 3. Check conventional commit format
# Use: <type>[(scope)]: <description>
```

### Before Creating PR

```bash
# 1. Run full test suite (if available)
npm test

# 2. Validate all relative paths
find agents -name "cs-*.md" -exec echo "Testing: {}" \;

# 3. Check documentation links
# (manual review recommended)

# 4. Verify YAML frontmatter
find agents -name "cs-*.md" -exec head -10 {} \; | grep -E "^(name|description|skills|domain|model|tools):"
```

---

## Emergency Procedures

### Accidentally Pushed to Main

```bash
# This will fail now due to branch protection
git push origin main
# Error: protected branch hook declined

# Solution: Create PR instead
git checkout -b fix/emergency-correction
git push origin fix/emergency-correction
gh pr create --base main --head fix/emergency-correction
```

### Need to Rollback Dev

```bash
# Revert specific commit
git checkout dev
git revert <commit-hash>
git push origin dev

# Or reset to previous state (use with caution!)
git checkout dev
git reset --hard <good-commit-hash>
git push origin dev --force  # Only on dev, never main!
```

### Merge Conflict

```bash
# During PR merge, conflicts occur
git checkout feature/my-branch
git pull origin dev
# Resolve conflicts in editor
git add .
git commit -m "chore: resolve merge conflicts with dev"
git push origin feature/my-branch
# PR will update automatically
```

---

## Best Practices

### DO ✅

- Always start from dev branch
- Use conventional commit format
- Create PRs for all changes
- Reference issue numbers in commits
- Test changes before pushing
- Delete branches after merge
- Keep commits atomic (one logical change)
- Write descriptive PR descriptions

### DON'T ❌

- Push directly to main (blocked by protection)
- Push directly to dev (use PRs instead)
- Commit secrets or credentials
- Mix multiple unrelated changes
- Use vague commit messages
- Leave stale branches unmerged
- Skip quality checks
- Force push to shared branches

---

## Related Documentation

- **Git Workflow Standards:** [standards/git/git-workflow-standards.md](../standards/git/git-workflow-standards.md)
- **Quality Standards:** [standards/quality/quality-standards.md](../standards/quality/quality-standards.md)
- **Main CLAUDE.md:** [../CLAUDE.md](../CLAUDE.md)
- **Agent Development:** [../agents/CLAUDE.md](../agents/CLAUDE.md)

---

## FAQ

**Q: Why can't I push to main anymore?**
A: Branch protection is now active. All changes must go through PR process with approval.

**Q: Do I need approval for dev branch too?**
A: Not currently required, but PRs are still recommended for clean review process.

**Q: What if I'm the only developer?**
A: Still use PRs. It provides review checkpoint, CI integration, and clear history.

**Q: Can I merge my own PRs?**
A: For dev branch yes, for main branch you need another reviewer's approval.

**Q: What happens to old commits made directly to main?**
A: They remain in history. Branch protection only affects new pushes.

**Q: How do I bypass branch protection for emergencies?**
A: You can't (by design). Even admins are enforced. Use hotfix PR process.

---

**Last Updated:** November 5, 2025
**Branch Protection:** Active on main
**Status:** Enforced for all contributors including admins
