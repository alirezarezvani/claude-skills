# Claude Skills Slash Commands

**Git workflow and quality assurance commands for the claude-skills repository.**

---

## 🎯 Essential Commands

### Git Workflow

```
/git:cm         → Stage and commit (no push)
/git:cp         → Stage, commit, and push
/git:pr         → Create pull request
/git:clean      → Delete merged branches (local + remote)
```

### Quality Gates

```
/review         → Run local quality checks
/security-scan  → Run security validation
/update-docs    → Post-creation sync (CLI platforms, marketplace, docs, GitHub Pages)
```

---

## 📋 Git Commands

### /git:cm - Commit (No Push)

**Purpose**: Stage changes and create a conventional commit without pushing

**Usage**:
```
/git:cm
```

**What it does**:
1. Shows `git status --short`
2. Reviews each file diff for secrets
3. Stages files intentionally
4. Generates conventional commit message
5. Creates commit (no push)

**When to use**: When you want to commit locally before pushing

---

### /git:cp - Commit and Push

**Purpose**: Complete git workflow with quality checks

**Usage**:
```
/git:cp
```

**What it does**:
1. Runs `/review` for quality checks
2. Stages changes
3. Creates conventional commit
4. Pushes to origin
5. Triggers CI workflows

**When to use**: When ready to publish changes

---

### /git:pr - Create Pull Request

**Purpose**: Create a PR from current branch

**Usage**:
```
/git:pr              # PR to main
/git:pr dev          # PR to dev branch
```

**What it does**:
1. Verifies quality checks passed
2. Creates PR using template
3. Adds appropriate labels
4. Shares PR link

**When to use**: After pushing changes and ready for review

---

## 🔒 Quality Commands

### /review - Local Quality Gate

**Purpose**: Run all quality checks before pushing

**Usage**:
```
/review
```

**What it checks**:
- ✅ YAML linting (workflows)
- ✅ GitHub workflow schema validation
- ✅ Python syntax (all skill directories)
- ✅ Markdown link validation
- ✅ Dependency security audit (optional)

**When to use**: Before committing/pushing changes

---

### /security-scan - Security Validation

**Purpose**: Scan for security issues

**Usage**:
```
/security-scan
```

**What it checks**:
- 🔍 Gitleaks (committed secrets detection)
- 🔍 Safety (Python dependency vulnerabilities)

**When to use**: Before pushing, especially with new dependencies

---

## 🔄 Complete Workflow

### Standard Feature Development

```
# 1. Make changes to skills
[Edit files in marketing-skill/, product-team/, etc.]

# 2. Run quality checks
/review

# 3. Run security scan
/security-scan

# 4. Commit and push
/git:cp

# 5. Create pull request
/git:pr

# 6. Wait for:
   - ✅ Claude Code Review comment
   - ✅ CI Quality Gate passing
   - ✅ Human approval

# 7. Merge PR
   - Issue auto-closes (if linked)
   - Project board updates
```

---

## 💡 Quick Reference

| Command | Stage | Commit | Push | Quality Check | Create PR |
|---------|-------|--------|------|---------------|-----------|
| **/git:cm** | ✅ | ✅ | ❌ | ❌ | ❌ |
| **/git:cp** | ✅ | ✅ | ✅ | ✅ | ❌ |
| **/git:pr** | ❌ | ❌ | ❌ | Verify | ✅ |
| **/review** | ❌ | ❌ | ❌ | ✅ | ❌ |
| **/security-scan** | ❌ | ❌ | ❌ | ✅ | ❌ |

---

## 📊 Commit Message Format

All commits follow **Conventional Commits**:

```
<type>(<scope>): <subject>

## Context
- Why this change was needed
- What problem it solves

## Testing
- [ ] All Python scripts tested
- [ ] Skills validated with Claude
- [ ] /review passed
- [ ] /security-scan passed

## Reviewers
- [ ] @username
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

**Scopes**: `marketing-skill`, `product-team`, `c-level-advisor`, `engineering-team`, `ra-qm-team`, `workflows`, `docs`, `ci`

**Examples**:
```
feat(marketing-skill): add LinkedIn content framework
fix(product-team): correct RICE prioritization calculation
docs(README): update skill installation instructions
ci(workflows): add auto-close issues on PR merge
```

---

## 🎯 Use Cases

### Quick Fix

```
# Fix typo in skill
[Edit file]
/review              # Quick check
/git:cp              # Commit + push
```

### New Skill Addition

```
# Create new skill
[Create skill directory and files]
/review              # Validate structure
/security-scan       # Check for issues
/git:cm              # Commit locally
[Test skill activation]
/git:cp              # Push when ready
/git:pr              # Create PR for review
```

### Major Feature with Multiple Skills

```
# Work on branch
git checkout -b feature/enterprise-skills

# Add multiple skills
[Create skill 1]
/git:cm

[Create skill 2]
/git:cm

[Create skill 3]
/git:cm

# Final quality check
/review
/security-scan

# Push and create PR
git push origin feature/enterprise-skills
/git:pr

# Or use /git:cp if you want to push single commit
```

---

## 🚨 Emergency Bypass

### Skip Reviews (Emergency Only)

If you need to bypass checks:

```bash
# Method 1: Use --no-verify flag
git push --no-verify

# Method 2: PR title bypass
[EMERGENCY] Fix critical bug

# Method 3: PR label
Add label: emergency, skip-review, or hotfix
```

**Note**: These bypass automated reviews but manual review is still recommended.

---

## 📖 Integration with Automation

These commands work seamlessly with the GitHub automation:

**After running `/git:cp`**:
- Triggers CI Quality Gate workflow
- Shows results in GitHub Actions

**After running `/git:pr`**:
- Triggers Claude Code Review
- Runs CI Quality Gate
- Updates project board status

**After merging PR**:
- Auto-closes linked issues
- Updates project board to "Done"
- Posts completion comments

---

## 🔗 Related Documentation

- **Automation Setup**: `.github/AUTOMATION_SETUP.md`
- **PR Template**: `.github/pull_request_template.md`
- **Commit Template**: `.github/commit-template.txt`
- **Workflow Guide**: See factory project for detailed reference

---

## 📍 Command Locations

```
.claude/commands/
├── git/
│   ├── cm.md           # Commit (no push)
│   ├── cp.md           # Commit and push
│   └── pr.md           # Create PR
├── review.md           # Quality checks
├── security-scan.md    # Security validation
└── README.md           # This file
```

---

## 💡 Tips

**Before committing**:
- ✅ Run `/review` to catch issues early
- ✅ Run `/security-scan` if adding dependencies
- ✅ Test skills with Claude before pushing

**When creating PRs**:
- ✅ Link related issues (`Fixes #123`)
- ✅ Fill out PR template completely
- ✅ Add appropriate labels
- ✅ Request specific reviewers

**For quality**:
- ✅ Keep commits focused and atomic
- ✅ Write clear, descriptive commit messages
- ✅ Follow conventional commit format
- ✅ Update documentation with changes

---

**Last Updated**: 2025-11-04
**Version**: 1.0.0
**Status**: ✅ Ready to use

**Streamline your Git workflow with simple commands!** 🚀
