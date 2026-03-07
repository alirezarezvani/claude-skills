---
name: changelog
description: Generate changelogs from git history and validate conventional commits. Usage: /changelog <generate|lint> [options]
---

# /changelog

Generate Keep a Changelog entries from git history and validate commit message format.

## Usage

```
/changelog generate [--from <tag>] [--to HEAD]    Generate changelog entries
/changelog lint [--range <from>..<to>]             Lint commit messages
```

## Examples

```
/changelog generate --from v2.0.0
/changelog lint --range main..dev
/changelog generate --from v2.0.0 --to v2.1.0 --format markdown
```

## Scripts
- `engineering/changelog-generator/scripts/generate_changelog.py` — Parse commits, render changelog
- `engineering/changelog-generator/scripts/commit_linter.py` — Validate conventional commit format

## Skill Reference
→ `engineering/changelog-generator/SKILL.md`
