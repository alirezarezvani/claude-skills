# Release Manager

A comprehensive release management toolkit for automating changelog generation, version bumping, and release planning based on conventional commits and industry best practices.

## Overview

The Release Manager skill provides three powerful Python scripts and comprehensive documentation for managing software releases:

1. **changelog_generator.py** - Generate structured changelogs from git history
2. **version_bumper.py** - Determine correct semantic version bumps
3. **release_planner.py** - Assess release readiness and generate coordination plans

## Quick Start

### Prerequisites

- Python 3.7+
- Git repository with conventional commit messages
- No external dependencies required (uses only Python standard library)

### Basic Usage

```bash
# Generate changelog from recent commits
git log --oneline --since="1 month ago" | python changelog_generator.py

# Determine version bump from commits since last tag  
git log --oneline $(git describe --tags --abbrev=0)..HEAD | python version_bumper.py -c "1.2.3"

# Assess release readiness
python release_planner.py --input assets/sample_release_plan.json
```

## Scripts Reference

### changelog_generator.py

Parses conventional commits and generates structured changelogs in multiple formats.

**Input Options:**
- Git log text (oneline or full format)
- JSON array of commits
- Stdin or file input

**Output Formats:**
- Markdown (Keep a Changelog format)
- JSON structured data
- Both with release statistics

```bash
# From git log (recommended)
git log --oneline --since="last release" | python changelog_generator.py \
  --version "2.1.0" \
  --date "2024-01-15" \
  --base-url "https://github.com/yourorg/yourrepo"

# From JSON file
python changelog_generator.py \
  --input assets/sample_commits.json \
  --input-format json \
  --format both \
  --summary

# With custom output
git log --format="%h %s" v1.0.0..HEAD | python changelog_generator.py \
  --version "1.1.0" \
  --output CHANGELOG_DRAFT.md
```

**Features:**
- Parses conventional commit types (feat, fix, docs, etc.)
- Groups commits by changelog categories (Added, Fixed, Changed, etc.)
- Extracts issue references (#123, fixes #456)
- Identifies breaking changes
- Links to commits and PRs
- Generates release summary statistics

### version_bumper.py

Analyzes commits to determine semantic version bumps according to conventional commits.

**Bump Rules:**
- **MAJOR:** Breaking changes (`feat!:` or `BREAKING CHANGE:`)
- **MINOR:** New features (`feat:`)
- **PATCH:** Bug fixes (`fix:`, `perf:`, `security:`)
- **NONE:** Documentation, tests, chores only

```bash
# Basic version bump determination
git log --oneline v1.2.3..HEAD | python version_bumper.py --current-version "1.2.3"

# With pre-release version
python version_bumper.py \
  --current-version "1.2.3" \
  --prerelease alpha \
  --input assets/sample_commits.json \
  --input-format json

# Include bump commands and file updates
git log --oneline $(git describe --tags --abbrev=0)..HEAD | \
  python version_bumper.py \
  --current-version "$(git describe --tags --abbrev=0)" \
  --include-commands \
  --include-files \
  --analysis
```

**Features:**
- Supports pre-release versions (alpha, beta, rc)
- Generates bump commands for npm, Python, Rust, Git
- Provides file update snippets
- Detailed commit analysis and categorization
- Custom rules for specific commit types
- JSON and text output formats

### release_planner.py

Assesses release readiness and generates comprehensive release coordination plans.

**Input:** JSON release plan with features, quality gates, and stakeholders

```bash
# Assess release readiness
python release_planner.py --input assets/sample_release_plan.json

# Generate full release package
python release_planner.py \
  --input release_plan.json \
  --output-format markdown \
  --include-checklist \
  --include-communication \
  --include-rollback \
  --output release_report.md
```

**Features:**
- Feature readiness assessment with approval tracking
- Quality gate validation and reporting
- Stakeholder communication planning
- Rollback procedure generation
- Risk analysis and timeline assessment
- Customizable test coverage thresholds
- Multiple output formats (text, JSON, Markdown)

## File Structure

```
release-manager/
├── SKILL.md                              # Comprehensive methodology guide
├── README.md                             # This file
├── changelog_generator.py                # Changelog generation script
├── version_bumper.py                     # Version bump determination
├── release_planner.py                    # Release readiness assessment
├── references/                           # Reference documentation
│   ├── conventional-commits-guide.md     # Conventional commits specification
│   ├── release-workflow-comparison.md    # Git Flow vs GitHub Flow vs Trunk-based
│   └── hotfix-procedures.md              # Emergency release procedures
├── assets/                               # Sample data for testing
│   ├── sample_git_log.txt               # Sample git log output
│   ├── sample_git_log_full.txt          # Detailed git log format
│   ├── sample_commits.json              # JSON commit data
│   └── sample_release_plan.json         # Release plan template
└── expected_outputs/                     # Example script outputs
    ├── changelog_example.md             # Expected changelog format
    ├── version_bump_example.txt         # Version bump output
    └── release_readiness_example.txt    # Release assessment report
```

## Integration Examples

### CI/CD Pipeline Integration

```yaml
# .github/workflows/release.yml
name: Automated Release
on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
      with:
        fetch-depth: 0  # Need full history
        
    - name: Determine version bump
      id: version
      run: |
        CURRENT=$(git describe --tags --abbrev=0)
        git log --oneline $CURRENT..HEAD | \
          python scripts/version_bumper.py -c $CURRENT --output-format json > bump.json
        echo "new_version=$(jq -r '.recommended_version' bump.json)" >> $GITHUB_OUTPUT
        
    - name: Generate changelog
      run: |
        git log --oneline ${{ steps.version.outputs.current_version }}..HEAD | \
          python scripts/changelog_generator.py \
          --version "${{ steps.version.outputs.new_version }}" \
          --base-url "https://github.com/${{ github.repository }}" \
          --output CHANGELOG_ENTRY.md
          
    - name: Create release
      uses: actions/create-release@v1
      with:
        tag_name: v${{ steps.version.outputs.new_version }}
        release_name: Release ${{ steps.version.outputs.new_version }}
        body_path: CHANGELOG_ENTRY.md
```

### Git Hooks Integration

```bash
#!/bin/bash
# .git/hooks/pre-commit
# Validate conventional commit format

commit_msg_file=$1
commit_msg=$(cat $commit_msg_file)

# Simple validation (more sophisticated validation available in commitlint)
if ! echo "$commit_msg" | grep -qE "^(feat|fix|docs|style|refactor|test|chore|perf|ci|build)(\(.+\))?(!)?:"; then
    echo "❌ Commit message doesn't follow conventional commits format"
    echo "Expected: type(scope): description"
    echo "Examples:"
    echo "  feat(auth): add OAuth2 integration"
    echo "  fix(api): resolve race condition"
    echo "  docs: update installation guide"
    exit 1
fi

echo "✅ Commit message format is valid"
```

### Release Planning Automation

```python
#!/usr/bin/env python3
# generate_release_plan.py - Automatically generate release plans from project management tools

import json
import requests
from datetime import datetime, timedelta

def generate_release_plan_from_github(repo, milestone):
    """Generate release plan from GitHub milestone and PRs."""
    
    # Fetch milestone details
    milestone_url = f"https://api.github.com/repos/{repo}/milestones/{milestone}"
    milestone_data = requests.get(milestone_url).json()
    
    # Fetch associated issues/PRs
    issues_url = f"https://api.github.com/repos/{repo}/issues?milestone={milestone}&state=all"
    issues = requests.get(issues_url).json()
    
    release_plan = {
        "release_name": milestone_data["title"],
        "version": "TBD",  # Fill in manually or extract from milestone
        "target_date": milestone_data["due_on"],
        "features": []
    }
    
    for issue in issues:
        if issue.get("pull_request"):  # It's a PR
            feature = {
                "id": f"GH-{issue['number']}",
                "title": issue["title"],
                "description": issue["body"][:200] + "..." if len(issue["body"]) > 200 else issue["body"],
                "type": "feature",  # Could be parsed from labels
                "assignee": issue["assignee"]["login"] if issue["assignee"] else "",
                "status": "ready" if issue["state"] == "closed" else "in_progress",
                "pull_request_url": issue["pull_request"]["html_url"],
                "issue_url": issue["html_url"],
                "risk_level": "medium",  # Could be parsed from labels
                "qa_approved": "qa-approved" in [label["name"] for label in issue["labels"]],
                "pm_approved": "pm-approved" in [label["name"] for label in issue["labels"]]
            }
            release_plan["features"].append(feature)
    
    return release_plan

# Usage
if __name__ == "__main__":
    plan = generate_release_plan_from_github("yourorg/yourrepo", "5")
    with open("release_plan.json", "w") as f:
        json.dump(plan, f, indent=2)
    
    print("Generated release_plan.json")
    print("Run: python release_planner.py --input release_plan.json")
```

## Advanced Usage

### Custom Commit Type Rules

```bash
# Define custom rules for version bumping
python version_bumper.py \
  --current-version "1.2.3" \
  --custom-rules '{"security": "patch", "breaking": "major"}' \
  --ignore-types "docs,style,test"
```

### Multi-repository Release Coordination

```bash
#!/bin/bash
# multi_repo_release.sh - Coordinate releases across multiple repositories

repos=("frontend" "backend" "mobile" "docs")
base_version="2.1.0"

for repo in "${repos[@]}"; do
    echo "Processing $repo..."
    cd "$repo"
    
    # Generate changelog for this repo
    git log --oneline --since="1 month ago" | \
        python ../scripts/changelog_generator.py \
        --version "$base_version" \
        --output "CHANGELOG_$repo.md"
    
    # Determine version bump
    git log --oneline $(git describe --tags --abbrev=0)..HEAD | \
        python ../scripts/version_bumper.py \
        --current-version "$(git describe --tags --abbrev=0)" > "VERSION_$repo.txt"
    
    cd ..
done

echo "Generated changelogs and version recommendations for all repositories"
```

### Integration with Slack/Teams

```python
#!/usr/bin/env python3
# notify_release_status.py

import json
import requests
import subprocess

def send_slack_notification(webhook_url, message):
    payload = {"text": message}
    requests.post(webhook_url, json=payload)

def get_release_status():
    """Get current release status from release planner."""
    result = subprocess.run(
        ["python", "release_planner.py", "--input", "release_plan.json", "--output-format", "json"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

# Usage in CI/CD
status = get_release_status()
if status["assessment"]["overall_status"] == "blocked":
    message = f"🚫 Release {status['version']} is BLOCKED\n"
    message += f"Issues: {', '.join(status['assessment']['blocking_issues'])}"
    send_slack_notification(SLACK_WEBHOOK_URL, message)
elif status["assessment"]["overall_status"] == "ready":
    message = f"✅ Release {status['version']} is READY for deployment!"
    send_slack_notification(SLACK_WEBHOOK_URL, message)
```

## Best Practices

### Commit Message Guidelines

1. **Use conventional commits consistently** across your team
2. **Be specific** in commit descriptions: "fix: resolve race condition in user creation" vs "fix: bug"
3. **Reference issues** when applicable: "Closes #123" or "Fixes #456"
4. **Mark breaking changes** clearly with `!` or `BREAKING CHANGE:` footer
5. **Keep first line under 50 characters** when possible

### Release Planning

1. **Plan releases early** with clear feature lists and target dates
2. **Set quality gates** and stick to them (test coverage, security scans, etc.)
3. **Track approvals** from all relevant stakeholders
4. **Document rollback procedures** before deployment
5. **Communicate clearly** with both internal teams and external users

### Version Management  

1. **Follow semantic versioning** strictly for predictable releases
2. **Use pre-release versions** for beta testing and gradual rollouts
3. **Tag releases consistently** with proper version numbers
4. **Maintain backwards compatibility** when possible to avoid major version bumps
5. **Document breaking changes** thoroughly with migration guides

## Troubleshooting

### Common Issues

**"No valid commits found"**
- Ensure git log contains commit messages
- Check that commits follow conventional format
- Verify input format (git-log vs json)

**"Invalid version format"**
- Use semantic versioning: 1.2.3, not 1.2 or v1.2.3.beta
- Pre-release format: 1.2.3-alpha.1

**"Missing required approvals"**
- Check feature risk levels in release plan
- High/critical risk features require additional approvals
- Update approval status in JSON file

### Debug Mode

All scripts support verbose output for debugging:

```bash
# Add debug logging
python changelog_generator.py --input sample.txt --debug

# Validate input data
python -c "import json; print(json.load(open('release_plan.json')))" 

# Test with sample data first
python release_planner.py --input assets/sample_release_plan.json
```

## Contributing

When extending these scripts:

1. **Maintain backwards compatibility** for existing command-line interfaces
2. **Add comprehensive tests** for new features
3. **Update documentation** including this README and SKILL.md
4. **Follow Python standards** (PEP 8, type hints where helpful)
5. **Use only standard library** to avoid dependencies

## License

This skill is part of the claude-skills repository and follows the same license terms.

---

For detailed methodology and background information, see [SKILL.md](SKILL.md).
For specific workflow guidance, see the [references](references/) directory.
For testing the scripts, use the sample data in the [assets](assets/) directory.