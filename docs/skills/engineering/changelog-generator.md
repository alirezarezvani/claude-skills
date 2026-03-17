---
title: "Changelog Generator — Agent Skill for Codex & OpenClaw"
description: "Changelog Generator. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Changelog Generator

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Engineering - POWERFUL</span>
<span class="meta-badge">:material-identifier: `changelog-generator`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/engineering/changelog-generator/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


**Tier:** POWERFUL  
**Category:** Engineering  
**Domain:** Release Management / Documentation

## Overview

Use this skill to produce consistent, auditable release notes from Conventional Commits. It separates commit parsing, semantic bump logic, and changelog rendering so teams can automate releases without losing editorial control.

## Core Capabilities

- Parse commit messages using Conventional Commit rules
- Detect semantic bump (`major`, `minor`, `patch`) from commit stream
- Render Keep a Changelog sections (`Added`, `Changed`, `Fixed`, etc.)
- Generate release entries from git ranges or provided commit input
- Enforce commit format with a dedicated linter script
- Support CI integration via machine-readable JSON output

## When to Use

- Before publishing a release tag
- During CI to generate release notes automatically
- During PR checks to block invalid commit message formats
- In monorepos where package changelogs require scoped filtering
- When converting raw git history into user-facing notes

## Key Workflows

### 1. Generate Changelog Entry From Git

```bash
python3 scripts/generate_changelog.py \
  --from-tag v1.3.0 \
  --to-tag v1.4.0 \
  --next-version v1.4.0 \
  --format markdown
```

### 2. Generate Entry From stdin/File Input

```bash
git log v1.3.0..v1.4.0 --pretty=format:'%s' | \
  python3 scripts/generate_changelog.py --next-version v1.4.0 --format markdown

python3 scripts/generate_changelog.py --input commits.txt --next-version v1.4.0 --format json
```

### 3. Update `CHANGELOG.md`

```bash
python3 scripts/generate_changelog.py \
  --from-tag v1.3.0 \
  --to-tag HEAD \
  --next-version v1.4.0 \
  --write CHANGELOG.md
```

### 4. Lint Commits Before Merge

```bash
python3 scripts/commit_linter.py --from-ref origin/main --to-ref HEAD --strict --format text
```

Or file/stdin:

```bash
python3 scripts/commit_linter.py --input commits.txt --strict
cat commits.txt | python3 scripts/commit_linter.py --format json
```

## Conventional Commit Rules

Supported types:

- `feat`, `fix`, `perf`, `refactor`, `docs`, `test`, `build`, `ci`, `chore`
- `security`, `deprecated`, `remove`

Breaking changes:

- `type(scope)!: summary`
- Footer/body includes `BREAKING CHANGE:`

SemVer mapping:

- breaking -> `major`
- non-breaking `feat` -> `minor`
- all others -> `patch`

## Script Interfaces

- `python3 scripts/generate_changelog.py --help`
  - Reads commits from git or stdin/`--input`
  - Renders markdown or JSON
  - Optional in-place changelog prepend
- `python3 scripts/commit_linter.py --help`
  - Validates commit format
  - Returns non-zero in `--strict` mode on violations

## Common Pitfalls

1. Mixing merge commit messages with release commit parsing
2. Using vague commit summaries that cannot become release notes
3. Failing to include migration guidance for breaking changes
4. Treating docs/chore changes as user-facing features
5. Overwriting historical changelog sections instead of prepending

## Best Practices

1. Keep commits small and intent-driven.
2. Scope commit messages (`feat(api): ...`) in multi-package repos.
3. Enforce linter checks in PR pipelines.
4. Review generated markdown before publishing.
5. Tag releases only after changelog generation succeeds.
6. Keep an `[Unreleased]` section for manual curation when needed.

## References

- [references/ci-integration.md](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/changelog-generator/references/ci-integration.md)
- [references/changelog-formatting-guide.md](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/changelog-generator/references/changelog-formatting-guide.md)
- [references/monorepo-strategy.md](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/changelog-generator/references/monorepo-strategy.md)
- [README.md](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/changelog-generator/README.md)

## Release Governance

Use this release flow for predictability:

1. Lint commit history for target release range.
2. Generate changelog draft from commits.
3. Manually adjust wording for customer clarity.
4. Validate semver bump recommendation.
5. Tag release only after changelog is approved.

## Output Quality Checks

- Each bullet is user-meaningful, not implementation noise.
- Breaking changes include migration action.
- Security fixes are isolated in `Security` section.
- Sections with no entries are omitted.
- Duplicate bullets across sections are removed.

## CI Policy

- Run `commit_linter.py --strict` on all PRs.
- Block merge on invalid conventional commits.
- Auto-generate draft release notes on tag push.
- Require human approval before writing into `CHANGELOG.md` on main branch.

## Monorepo Guidance

- Prefer commit scopes aligned to package names.
- Filter commit stream by scope for package-specific releases.
- Keep infra-wide changes in root changelog.
- Store package changelogs near package roots for ownership clarity.

## Failure Handling

- If no valid conventional commits found: fail early, do not generate misleading empty notes.
- If git range invalid: surface explicit range in error output.
- If write target missing: create safe changelog header scaffolding.
