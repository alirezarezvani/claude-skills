# Changelog Generator

**Tier:** POWERFUL  
**Category:** Engineering  
**Domain:** Release Management / Documentation  

---

## Overview

Parse conventional commits, determine semantic version bumps, and generate structured changelogs in Keep a Changelog format. Supports monorepo changelogs, GitHub Releases integration, and separates user-facing from developer changelogs.

## Core Capabilities

- **Conventional commit parsing** — feat, fix, chore, docs, refactor, perf, test, build, ci
- **SemVer bump determination** — breaking change → major, feat → minor, fix → patch
- **Keep a Changelog format** — Added, Changed, Deprecated, Removed, Fixed, Security
- **Monorepo support** — per-package changelogs with shared version strategy
- **GitHub/GitLab Releases** — auto-create release with changelog body
- **Audience-aware output** — user-facing (what changed) vs developer (why + technical details)

---

## When to Use

- Before every release to generate the CHANGELOG.md entry
- Setting up automated changelog generation in CI
- Converting git log into readable release notes for GitHub Releases
- Maintaining monorepo changelogs for individual packages
- Generating internal release notes for the engineering team

---

## Conventional Commits Reference

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types and SemVer impact

| Type | Changelog section | SemVer bump |
|------|------------------|-------------|
| `feat` | Added | minor |
| `fix` | Fixed | patch |
| `perf` | Changed | patch |
| `refactor` | Changed (internal) | patch |
| `docs` | — (omit or include) | patch |
| `chore` | — (omit) | patch |
| `test` | — (omit) | patch |
| `build` | — (omit) | patch |
| `ci` | — (omit) | patch |
| `security` | Security | patch |
| `deprecated` | Deprecated | minor |
| `remove` | Removed | major (if breaking) |
| `BREAKING CHANGE:` footer | — (major bump) | major |
| `!` after type | — (major bump) | major |

### Examples

```
feat(auth): add OAuth2 login with Google
fix(api): correct pagination offset calculation
feat!: rename /users endpoint to /accounts (BREAKING)
perf(db): add index on users.email column
security: patch XSS vulnerability in comment renderer
docs: update API reference for v2 endpoints
```

---

## Changelog Generation Script

```bash
#!/usr/bin/env bash
# generate-changelog.sh — generate CHANGELOG entry for the latest release

set -euo pipefail

CURRENT_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
PREVIOUS_TAG=$(git describe --tags --abbrev=0 "${CURRENT_TAG}^" 2>/dev/null || echo "")
DATE=$(date +%Y-%m-%d)

if [ -z "$CURRENT_TAG" ]; then
  echo "No tags found. Create a tag first: git tag v1.0.0"
  exit 1
fi

RANGE="${PREVIOUS_TAG:+${PREVIOUS_TAG}..}${CURRENT_TAG}"
echo "Generating changelog for: $RANGE"

# Parse commits
ADDED=""
CHANGED=""
DEPRECATED=""
REMOVED=""
FIXED=""
SECURITY=""
BREAKING=""

while IFS= read -r line; do
  # Skip empty lines
  [ -z "$line" ] && continue
  
  # Detect type
  if [[ "$line" =~ ^feat(\([^)]+\))?\!:\ (.+)$ ]]; then
    desc="${BASH_REMATCH[2]}"
    BREAKING="${BREAKING}- **BREAKING** ${desc}\n"
    ADDED="${ADDED}- ${desc}\n"
  elif [[ "$line" =~ ^feat(\([^)]+\))?:\ (.+)$ ]]; then
    ADDED="${ADDED}- ${BASH_REMATCH[2]}\n"
  elif [[ "$line" =~ ^fix(\([^)]+\))?:\ (.+)$ ]]; then
    FIXED="${FIXED}- ${BASH_REMATCH[2]}\n"
  elif [[ "$line" =~ ^perf(\([^)]+\))?:\ (.+)$ ]]; then
    CHANGED="${CHANGED}- ${BASH_REMATCH[2]}\n"
  elif [[ "$line" =~ ^security(\([^)]+\))?:\ (.+)$ ]]; then
    SECURITY="${SECURITY}- ${BASH_REMATCH[2]}\n"
  elif [[ "$line" =~ ^deprecated(\([^)]+\))?:\ (.+)$ ]]; then
    DEPRECATED="${DEPRECATED}- ${BASH_REMATCH[2]}\n"
  elif [[ "$line" =~ ^remove(\([^)]+\))?:\ (.+)$ ]]; then
    REMOVED="${REMOVED}- ${BASH_REMATCH[2]}\n"
  elif [[ "$line" =~ ^refactor(\([^)]+\))?:\ (.+)$ ]]; then
    CHANGED="${CHANGED}- ${BASH_REMATCH[2]}\n"
  fi
done < <(git log "${RANGE}" --pretty=format:"%s" --no-merges)

# Build output
OUTPUT="## [${CURRENT_TAG}] - ${DATE}\n\n"

[ -n "$BREAKING" ] && OUTPUT="${OUTPUT}### ⚠ BREAKING CHANGES\n${BREAKING}\n"
[ -n "$SECURITY" ] && OUTPUT="${OUTPUT}### Security\n${SECURITY}\n"
[ -n "$ADDED" ] && OUTPUT="${OUTPUT}### Added\n${ADDED}\n"
[ -n "$CHANGED" ] && OUTPUT="${OUTPUT}### Changed\n${CHANGED}\n"
[ -n "$DEPRECATED" ] && OUTPUT="${OUTPUT}### Deprecated\n${DEPRECATED}\n"
[ -n "$REMOVED" ] && OUTPUT="${OUTPUT}### Removed\n${REMOVED}\n"
[ -n "$FIXED" ] && OUTPUT="${OUTPUT}### Fixed\n${FIXED}\n"

printf "$OUTPUT"

# Optionally prepend to CHANGELOG.md
if [ "${1:-}" = "--write" ]; then
  TEMP=$(mktemp)
  printf "$OUTPUT" > "$TEMP"
  
  if [ -f CHANGELOG.md ]; then
    # Insert after the first line (# Changelog header)
    head -n 1 CHANGELOG.md >> "$TEMP"
    echo "" >> "$TEMP"
    printf "$OUTPUT" >> "$TEMP"
    tail -n +2 CHANGELOG.md >> "$TEMP"
  else
    echo "# Changelog" > CHANGELOG.md
    echo "All notable changes to this project will be documented here." >> CHANGELOG.md
    echo "" >> CHANGELOG.md
    cat "$TEMP" >> CHANGELOG.md
  fi
  
  mv "$TEMP" CHANGELOG.md
  echo "✅ CHANGELOG.md updated"
fi
```

---

## Python Changelog Generator (more robust)

```python
#!/usr/bin/env python3
"""generate_changelog.py — parse conventional commits and emit Keep a Changelog"""

import subprocess
import re
import sys
from datetime import date
from dataclasses import dataclass, field
from typing import Optional

COMMIT_RE = re.compile(
    r"^(?P<type>feat|fix|perf|refactor|docs|test|chore|build|ci|security|deprecated|remove)"
    r"(?:\((?P<scope>[^)]+)\))?(?P<breaking>!)?: (?P<desc>.+)$"
)

SECTION_MAP = {
    "feat": "Added",
    "fix": "Fixed",
    "perf": "Changed",
    "refactor": "Changed",
    "security": "Security",
    "deprecated": "Deprecated",
    "remove": "Removed",
}

@dataclass
class Commit:
    type: str
    scope: Optional[str]
    breaking: bool
    desc: str
    body: str = ""
    sha: str = ""

@dataclass
class ChangelogEntry:
    version: str
    date: str
    added: list[str] = field(default_factory=list)
    changed: list[str] = field(default_factory=list)
    deprecated: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    fixed: list[str] = field(default_factory=list)
    security: list[str] = field(default_factory=list)
    breaking: list[str] = field(default_factory=list)


def get_commits(from_tag: str, to_tag: str) -> list[Commit]:
    range_spec = f"{from_tag}..{to_tag}" if from_tag else to_tag
    result = subprocess.run(
        ["git", "log", range_spec, "--pretty=format:%H|%s|%b", "--no-merges"],
        capture_output=True, text=True, check=True
    )
    
    commits = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("|", 2)
        sha = parts[0] if len(parts) > 0 else ""
        subject = parts[1] if len(parts) > 1 else ""
        body = parts[2] if len(parts) > 2 else ""
        
        m = COMMIT_RE.match(subject)
        if m:
            commits.append(Commit(
                type=m.group("type"),
                scope=m.group("scope"),
                breaking=m.group("breaking") == "!" or "BREAKING CHANGE" in body,
                desc=m.group("desc"),
                body=body,
                sha=sha[:8],
            ))
    
    return commits


def determine_bump(commits: list[Commit], current_version: str) -> str:
    parts = current_version.lstrip("v").split(".")
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    
    has_breaking = any(c.breaking for c in commits)
    has_feat = any(c.type == "feat" for c in commits)
    
    if has_breaking:
        return f"v{major + 1}.0.0"
    elif has_feat:
        return f"v{major}.{minor + 1}.0"
    else:
        return f"v{major}.{minor}.{patch + 1}"


def build_entry(commits: list[Commit], version: str) -> ChangelogEntry:
    entry = ChangelogEntry(version=version, date=date.today().isoformat())
    
    for c in commits:
        scope_prefix = f"**{c.scope}**: " if c.scope else ""
        desc = f"{scope_prefix}{c.desc}"
        
        if c.breaking:
            entry.breaking.append(desc)
        
        section = SECTION_MAP.get(c.type)
        if section == "Added":
            entry.added.append(desc)
        elif section == "Fixed":
            entry.fixed.append(desc)
        elif section == "Changed":
            entry.changed.append(desc)
        elif section == "Security":
            entry.security.append(desc)
        elif section == "Deprecated":
            entry.deprecated.append(desc)
        elif section == "Removed":
            entry.removed.append(desc)
    
    return entry


def render_entry(entry: ChangelogEntry) -> str:
    lines = [f"## [{entry.version}] - {entry.date}", ""]
    
    sections = [
        ("⚠ BREAKING CHANGES", entry.breaking),
        ("Security", entry.security),
        ("Added", entry.added),
        ("Changed", entry.changed),
        ("Deprecated", entry.deprecated),
        ("Removed", entry.removed),
        ("Fixed", entry.fixed),
    ]
    
    for title, items in sections:
        if items:
            lines.append(f"### {title}")
            for item in items:
                lines.append(f"- {item}")
            lines.append("")
    
    return "\n".join(lines)


if __name__ == "__main__":
    tags = subprocess.run(
        ["git", "tag", "--sort=-version:refname"],
        capture_output=True, text=True
    ).stdout.splitlines()
    
    current_tag = tags[0] if tags else ""
    previous_tag = tags[1] if len(tags) > 1 else ""
    
    if not current_tag:
        print("No tags found. Create a tag first.")
        sys.exit(1)
    
    commits = get_commits(previous_tag, current_tag)
    entry = build_entry(commits, current_tag)
    print(render_entry(entry))
```

---

## Monorepo Changelog Strategy

For repos with multiple packages (e.g., pnpm workspaces, nx, turborepo):

```bash
# packages/api/CHANGELOG.md     — API package only
# packages/ui/CHANGELOG.md      — UI package only
# CHANGELOG.md                  — Root (affects all)

# Filter commits by package path
git log v1.2.0..v1.3.0 --pretty=format:"%s" -- packages/api/
```

With Changesets (recommended for monorepos):

```bash
# Install changesets
pnpm add -D @changesets/cli
pnpm changeset init

# Developer workflow: create a changeset for each PR
pnpm changeset
# → prompts for: which packages changed, bump type, description

# On release branch: version all packages
pnpm changeset version

# Publish and create GitHub release
pnpm changeset publish
```

---

## GitHub Releases Integration

```bash
#!/usr/bin/env bash
# create-github-release.sh

set -euo pipefail

VERSION=$(git describe --tags --abbrev=0)
NOTES=$(python3 generate_changelog.py)

# Using GitHub CLI
gh release create "$VERSION" \
  --title "Release $VERSION" \
  --notes "$NOTES" \
  --verify-tag

# Or via API
curl -s -X POST \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.github.com/repos/${REPO}/releases" \
  -d "$(jq -n \
    --arg tag "$VERSION" \
    --arg name "Release $VERSION" \
    --arg body "$NOTES" \
    '{tag_name: $tag, name: $name, body: $body, draft: false}')"
```

---

## User-Facing vs Developer Changelog

### User-facing (product changelog)
- Plain language, no jargon
- Focus on what changed, not how
- Skip: refactor, test, chore, ci, docs
- Include: feat, fix, security, perf (if user-visible)

```markdown
## Version 2.3.0 — March 1, 2026

**New:** You can now log in with Google.
**Fixed:** Dashboard no longer freezes when loading large datasets.
**Improved:** Search results load 3x faster.
```

### Developer changelog (CHANGELOG.md)
- Technical details, scope, SemVer impact
- Include all breaking changes with migration notes
- Reference PR numbers and issue IDs

```markdown
## [2.3.0] - 2026-03-01

### Added
- **auth**: OAuth2 Google login via passport-google (#234)
- **api**: GraphQL subscriptions for real-time updates (#241)

### Fixed
- **dashboard**: resolve infinite re-render on large datasets (closes #228)

### Performance
- **search**: switch from Elasticsearch to Typesense, P99 latency -67% (#239)
```

---

## GitHub Actions — Automated Changelog CI

```yaml
name: Release

on:
  push:
    tags: ['v*']

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for git log

      - name: Generate changelog
        id: changelog
        run: |
          NOTES=$(python3 scripts/generate_changelog.py)
          echo "notes<<EOF" >> $GITHUB_OUTPUT
          echo "$NOTES" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          body: ${{ steps.changelog.outputs.notes }}
          generate_release_notes: false
```

---

## Common Pitfalls

- **`--depth=1` in CI** — git log needs full history; use `fetch-depth: 0`
- **Merge commits polluting log** — always use `--no-merges`
- **No conventional commits discipline** — enforce with `commitlint` in CI
- **Missing previous tag** — handle first-release case (no previous tag)
- **Version in multiple places** — single source of truth; read from git tag, not package.json

---

## Best Practices

1. **commitlint in CI** — enforce conventional commits before merge
2. **Tag before generating** — tag the release commit first, then generate
3. **Separate user/dev changelog** — product team wants plain English
4. **Keep a link section** — `[2.3.0]: https://github.com/org/repo/compare/v2.2.0...v2.3.0`
5. **Automate but review** — generate in CI, human reviews before publish
