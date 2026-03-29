---
title: "CI/CD Pipeline Builder — Agent Skill for Codex & OpenClaw"
description: "CI/CD Pipeline Builder. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# CI/CD Pipeline Builder

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Engineering - POWERFUL</span>
<span class="meta-badge">:material-identifier: `ci-cd-pipeline-builder`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/engineering/ci-cd-pipeline-builder/SKILL.md">Source</a></span>
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

## Common Pitfalls

1. Copying a Node pipeline into Python/Go repos
2. Enabling deploy jobs before stable tests
3. Forgetting dependency cache keys
4. Running expensive matrix builds for every trivial branch
5. Missing branch protections around prod deploy jobs
6. Hardcoding secrets in YAML instead of CI secret stores

## Best Practices

1. Detect stack first, then generate pipeline.
2. Keep generated baseline under version control.
3. Add one optimization at a time (cache, matrix, split jobs).
4. Require green CI before deployment jobs.
5. Use protected environments for production credentials.
6. Regenerate pipeline when stack changes significantly.

## References

- [references/github-actions-templates.md](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/ci-cd-pipeline-builder/references/github-actions-templates.md)
- [references/gitlab-ci-templates.md](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/ci-cd-pipeline-builder/references/gitlab-ci-templates.md)
- [references/deployment-gates.md](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/ci-cd-pipeline-builder/references/deployment-gates.md)
- [README.md](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/ci-cd-pipeline-builder/README.md)

## Detection Heuristics

The stack detector prioritizes deterministic file signals over heuristics:

- Lockfiles determine package manager preference
- Language manifests determine runtime families
- Script commands (if present) drive lint/test/build commands
- Missing scripts trigger conservative placeholder commands

## Generation Strategy

Start with a minimal, reliable pipeline:

1. Checkout and setup runtime
2. Install dependencies with cache strategy
3. Run lint, test, build in separate steps
4. Publish artifacts only after passing checks

Then layer advanced behavior (matrix builds, security scans, deploy gates).

## Platform Decision Notes

- GitHub Actions for tight GitHub ecosystem integration
- GitLab CI for integrated SCM + CI in self-hosted environments
- Keep one canonical pipeline source per repo to reduce drift

## Validation Checklist

1. Generated YAML parses successfully.
2. All referenced commands exist in the repo.
3. Cache strategy matches package manager.
4. Required secrets are documented, not embedded.
5. Branch/protected-environment rules match org policy.

## Scaling Guidance

- Split long jobs by stage when runtime exceeds 10 minutes.
- Introduce test matrix only when compatibility truly requires it.
- Separate deploy jobs from CI jobs to keep feedback fast.
- Track pipeline duration and flakiness as first-class metrics.
