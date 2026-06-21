---
description: Skill-package editor for this repository. Use when changing a specific skill or domain package while preserving the repo's standalone skill structure.
---

# Skill Editor

Use this agent for changes inside skill-package domains such as `engineering-team/`, `engineering/`, `product-team/`, `marketing-skill/`, `project-management/`, `research-ops/`, `markdown-html/`, and related top-level domains.

## Read first

1. `README.md`
2. `CLAUDE.md`
3. The nearest domain `CLAUDE.md`
4. The relevant `SKILL.md`
5. `.github/instructions/skills.instructions.md`

## Core operating rules

- Preserve the standard package pattern: `SKILL.md`, `scripts/`, `references/`, and `assets/` when present.
- Do not turn one skill into a runtime dependency of another.
- Prefer deterministic Python CLI tools and existing local patterns.
- If a change updates counts, install notes, or examples, update the directly related docs in the same change.

## Validation

- Markdown-only changes: verify paths, examples, and related docs.
- Python script changes: run targeted Python compilation or existing script help checks.
- Manifest changes: keep `plugin.json` paths and schema aligned with existing repo conventions.
