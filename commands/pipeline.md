---
name: pipeline
description: Detect stack and generate CI/CD pipeline configs. Usage: /pipeline <detect|generate> [options]
---

# /pipeline

Detect project stack and generate CI/CD pipeline configurations for GitHub Actions or GitLab CI.

## Usage

```
/pipeline detect [<project-dir>]                    Detect stack, tools, and services
/pipeline generate [--platform github|gitlab]       Generate pipeline YAML
```

## Examples

```
/pipeline detect ./my-project
/pipeline generate --platform github
/pipeline generate --platform gitlab --stages build,test,deploy
```

## Scripts
- `engineering/ci-cd-pipeline-builder/scripts/stack_detector.py` — Detect stack and tooling
- `engineering/ci-cd-pipeline-builder/scripts/pipeline_generator.py` — Generate pipeline YAML

## Skill Reference
→ `engineering/ci-cd-pipeline-builder/SKILL.md`
