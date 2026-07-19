---
title: "CI/CD Pipeline Builder — Agent Skill for Codex & OpenClaw"
description: "Generate pragmatic CI/CD pipelines from detected project stack signals — fast baseline generation, repeatable checks, environment-aware deployment. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# CI/CD Pipeline Builder

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Engineering - POWERFUL</span>
<span class="meta-badge">:material-identifier: `ci-cd-pipeline-builder`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/ci-cd-pipeline-builder/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


**Tier:** POWERFUL  
**Category:** Engineering  
**Domain:** DevOps / Automation

## Overview

Use this skill to generate pragmatic CI/CD pipelines from detected project stack signals, not guesswork. It focuses on fast baseline generation, repeatable checks, and environment-aware deployment stages.

## Core Capabilities

- Detect language/runtime/tooling from repository files
- Recommend CI stages (`lint`, `test`, `build`, `deploy`)
- Generate GitHub Actions or GitLab CI starter pipelines
- Include caching and matrix strategy based on detected stack
- Emit machine-readable detection output for automation
- Keep pipeline logic aligned with project lockfiles and build commands

## When to Use

- Bootstrapping CI for a new repository
- Replacing brittle copied pipeline files
- Migrating between GitHub Actions and GitLab CI
- Auditing whether pipeline steps match actual stack
- Creating a reproducible baseline before custom hardening

## Key Workflows

### 1. Detect Stack

```bash
python3 scripts/stack_detector.py --repo . --format text
python3 scripts/stack_detector.py --repo . --format json > detected-stack.json
```

Supports input via stdin or `--input` file for offline analysis payloads.

### 2. Generate Pipeline From Detection

```bash
python3 scripts/pipeline_generator.py \
  --input detected-stack.json \
  --platform github \
  --output .github/workflows/ci.yml \
  --format text
```

Or end-to-end from repo directly:

```bash
python3 scripts/pipeline_generator.py --repo . --platform gitlab --output .gitlab-ci.yml
```

### 3. Validate Before Merge

1. Confirm commands exist in project (`test`, `lint`, `build`).
2. Run generated pipeline locally where possible.
3. Ensure required secrets/env vars are documented.
4. Keep deploy jobs gated by protected branches/environments.

### 4. Add Deployment Stages Safely

- Start with CI-only (`lint/test/build`).
- Add staging deploy with explicit environment context.
- Add production deploy with manual gate/approval.
- Keep rollout/rollback commands explicit and auditable.

## Script Interfaces

- `python3 scripts/stack_detector.py --help`
  - Detects stack signals from repository files
  - Reads optional JSON input from stdin/`--input`
- `python3 scripts/pipeline_generator.py --help`
  - Generates GitHub/GitLab YAML from detection payload
  - Writes to stdout or `--output`

## References

- [references/pipeline-design-notes.md](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/ci-cd-pipeline-builder/references/pipeline-design-notes.md) — common pitfalls, best practices, detection heuristics, generation strategy, platform decision notes, pre-merge validation checklist, and scaling guidance
- [references/github-actions-templates.md](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/ci-cd-pipeline-builder/references/github-actions-templates.md)
- [references/gitlab-ci-templates.md](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/ci-cd-pipeline-builder/references/gitlab-ci-templates.md)
- [references/deployment-gates.md](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/ci-cd-pipeline-builder/references/deployment-gates.md)
- [README.md](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/ci-cd-pipeline-builder/README.md)
