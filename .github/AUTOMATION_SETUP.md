# GitHub Automation Setup Guide

**Repository**: claude-skills
**Project Number**: 9
**Status**: ⚙️ Configuration Required

---

## Overview

This repository includes AI-powered GitHub automation with:

- ✅ **Claude Code Review** - Automatic PR reviews
- ✅ **Auto-Close Issues** - PRs auto-close linked issues when merged
- ✅ **Smart Sync** - Bidirectional issue ↔ project board synchronization
- ✅ **Quality Gates** - Automated linting, testing, security checks
- ✅ **Kill Switch** - Emergency workflow disable capability

---

## Quick Start (15 minutes)

### 1. Create Required Secrets

You need **2 secrets** for full automation:

#### ✅ CLAUDE_CODE_OAUTH_TOKEN (Already Configured)

This secret is already set up for Claude Code reviews.

#### ⚠️ PROJECTS_TOKEN (Required for Project Board Sync)

**Create Personal Access Token:**

1. Go to: https://github.com/settings/tokens/new
2. Configure:
   - **Note**: "Claude Skills Project Board Access"
   - **Expiration**: 90 days (recommended)
   - **Select scopes**:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `project` (Full control of projects)
3. Click "Generate token"
4. **Copy the token** (you won't see it again!)

**Add to Repository:**

1. Go to: https://github.com/alirezarezvani/claude-skills/settings/secrets/actions
2. Click "New repository secret"
3. **Name**: `PROJECTS_TOKEN`
4. **Value**: [Paste your token]
5. Click "Add secret"

---

### 2. Create Project Board Labels

Run these commands to create all required labels:

```bash
# Status Labels (6)
gh label create "status: triage" --color "fbca04" --description "To Triage column" --repo alirezarezvani/claude-skills
gh label create "status: backlog" --color "d4c5f9" --description "Backlog column" --repo alirezarezvani/claude-skills
gh label create "status: ready" --color "0e8a16" --description "Ready column" --repo alirezarezvani/claude-skills
gh label create "status: in-progress" --color "1d76db" --description "In Progress column" --repo alirezarezvani/claude-skills
gh label create "status: in-review" --color "d876e3" --description "In Review column" --repo alirezarezvani/claude-skills
gh label create "status: done" --color "2ea44f" --description "Done column" --repo alirezarezvani/claude-skills

# Priority Labels (4)
gh label create "P0" --color "b60205" --description "Critical priority" --repo alirezarezvani/claude-skills
gh label create "P1" --color "d93f0b" --description "High priority" --repo alirezarezvani/claude-skills
gh label create "P2" --color "fbca04" --description "Medium priority" --repo alirezarezvani/claude-skills
gh label create "P3" --color "0e8a16" --description "Low priority" --repo alirezarezvani/claude-skills

# Type Labels (already exist - verify)
# bug, feature, documentation, enhancement, etc.
```

---

### 3. Configure Project Board

Your project board columns must match these exact names:

1. **To triage**
2. **Backlog**
3. **Ready**
4. **In Progress**
5. **In Review**
6. **Done**

**Verify Configuration:**

1. Go to: https://github.com/users/alirezarezvani/projects/9
2. Check column names match exactly (case-sensitive)
3. Ensure "Status" field exists

---

### 4. Test the Setup

#### Test 1: Create Test Issue

```bash
gh issue create \
  --title "Test: Automation Setup" \
  --body "Testing GitHub automation workflows" \
  --label "status: triage" \
  --repo alirezarezvani/claude-skills
```

**Expected Results:**
- ✅ Issue created
- ✅ Auto-added to project board (column: "To triage")
- ✅ Label synced

#### Test 2: Change Issue Status

```bash
# Get the issue number from step 1, then:
gh issue edit ISSUE_NUMBER --add-label "status: in-progress" --repo alirezarezvani/claude-skills
```

**Expected Results:**
- ✅ Issue moved to "In Progress" on project board
- ✅ Old status label removed
- ✅ New status label applied

#### Test 3: Create Test PR

```bash
# Create a branch
git checkout -b test/automation-setup
echo "# Test" > TEST.md
git add TEST.md
git commit -m "test: verify automation"
git push origin test/automation-setup

# Create PR that fixes the test issue
gh pr create \
  --title "test: Verify automation workflows" \
  --body "Fixes #ISSUE_NUMBER" \
  --repo alirezarezvani/claude-skills
```

**Expected Results:**
- ✅ Claude review triggers (check Actions tab)
- ✅ CI Quality Gate runs
- ✅ When merged, issue auto-closes
- ✅ Project board updates to "Done"

---

## Active Workflows

| Workflow | Trigger | Status |
|----------|---------|--------|
| **claude-code-review.yml** | PR opened/updated | ✅ Active |
| **pr-issue-auto-close.yml** | PR merged | ✅ Active |
| **smart-sync.yml** | Issue/board changes | ⚠️ Requires PROJECTS_TOKEN |
| **ci-quality-gate.yml** | PR opened/updated | ✅ Active |

---

## Emergency Procedures

### 🚨 Disable All Workflows

If something goes wrong:

```bash
echo "STATUS: DISABLED" > .github/WORKFLOW_KILLSWITCH
git add .github/WORKFLOW_KILLSWITCH
git commit -m "emergency: Disable workflows"
git push origin main --no-verify
```

All workflows check this file and exit immediately if disabled.

### ✅ Re-enable Workflows

```bash
echo "STATUS: ENABLED" > .github/WORKFLOW_KILLSWITCH
git commit -am "chore: Re-enable workflows"
git push
```

---

## Usage Examples

### Auto-Close Issues with PR

In your PR description:

```markdown
## Summary
Fixed the authentication bug

## Related Issues
Fixes #123
Closes #456
```

When merged → Issues #123 and #456 automatically close with comment linking to PR.

### Sync Issue Status

**Option A - Update Label:**
```bash
gh issue edit 123 --add-label "status: in-review"
```
→ Moves to "In Review" on project board

**Option B - Update Board:**
```
Drag issue to "In Review" column on project board
```
→ Adds "status: in-review" label to issue

---

## Troubleshooting

### Smart Sync Not Working

**Problem**: Labels not syncing with project board

**Check:**
```bash
gh secret list --repo alirezarezvani/claude-skills | grep PROJECTS_TOKEN
```

**Solution**: If missing, add PROJECTS_TOKEN (see Step 1 above)

### Claude Review Not Running

**Problem**: No review comment on PR

**Check:**
```bash
gh run list --workflow=claude-code-review.yml --limit 5 --repo alirezarezvani/claude-skills
```

**Solutions**:
- Verify CLAUDE_CODE_OAUTH_TOKEN exists
- Check workflow logs for errors
- Re-run workflow from Actions tab

### Rate Limits

**Check current limits:**
```bash
gh api rate_limit --jq '.resources.core.remaining, .resources.graphql.remaining'
```

**Rate Limit Info:**
- REST API: 5,000/hour
- GraphQL: 5,000/hour
- Workflows require 50+ remaining before executing

---

## Maintenance

### Weekly

```bash
# Check failed runs
gh run list --status failure --limit 10 --repo alirezarezvani/claude-skills

# Verify secrets valid
gh secret list --repo alirezarezvani/claude-skills
```

### Quarterly

```bash
# Regenerate PROJECTS_TOKEN (expires every 90 days)
# 1. Create new token with same scopes
# 2. Update repository secret
# 3. Test with a sync operation
```

---

## Security Notes

**4-Layer Security Model:**

1. **GitHub Permissions** - Only team members trigger workflows
2. **Tool Restrictions** - Allowlist specific commands only
3. **Token Scoping** - Minimal permissions (repo + project)
4. **Branch Protection** - Required reviews, status checks

**Kill Switch**: Emergency disable capability (WORKFLOW_KILLSWITCH file)

---

## Next Steps

1. ✅ Create PROJECTS_TOKEN secret
2. ✅ Create all required labels
3. ✅ Verify project board columns
4. ✅ Test with sample issue and PR
5. ✅ Monitor first few workflow runs
6. ✅ Document any project-specific customizations

---

## Support

**Documentation:**
- This setup guide
- Individual workflow files in `.github/workflows/`
- Factory reference: https://github.com/alirezarezvani/claude-code-skills-factory

**Getting Help:**
- Create issue with `question` label
- Check workflow logs: `gh run view RUN_ID --log`
- Review troubleshooting section above

---

**Last Updated**: 2025-11-04
**Status**: Ready for configuration ⚙️
