# GitHub Copilot workspace instructions

This repository is a **skills library**, not a single application. Most work happens inside self-contained skill packages, agent definitions, command docs, and plugin manifests rather than inside a runnable app.

## Start here

Prefer local repository files over external lookups. The fastest high-signal entry points are:

- `README.md` for installation, platform support, and top-level navigation
- `CLAUDE.md` for repository-wide architecture, conventions, and current version context
- `agents/CLAUDE.md` when touching `agents/**`
- The nearest domain `CLAUDE.md` when touching a specific domain folder
- `.claude/commands/README.md` when a task references the local Claude workspace commands

## Repository map

- `agents/` — cs-* task agents and persona definitions
- `commands/` — shipped slash-command docs
- Domain folders such as `engineering-team/`, `engineering/`, `product-team/`, `marketing-skill/`, `c-level-advisor/`, `research-ops/`, `markdown-html/`, and others — each holds standalone skill packages
- `.claude/` — Claude Code workspace customizations for this repository
- `.github/copilot-instructions.md`, `.github/instructions/`, `.github/prompts/`, and `.github/agents/` — GitHub Copilot workspace customizations for this repository

## Change rules

- Reuse existing patterns; do not invent a second structure for skills, agents, commands, or plugin manifests.
- Skills stay self-contained: `SKILL.md`, `scripts/`, `references/`, and `assets/` travel together.
- Keep skill automation deterministic and CLI-first. Prefer Python standard library only unless the skill already documents a dependency.
- Do not add cross-skill runtime dependencies just to share logic.
- Agents orchestrate skills; they should reference existing skills and tools instead of duplicating long skill content.
- Commands are reusable workflow docs. Preserve their YAML frontmatter and keep examples aligned with the repository's actual scripts and paths.

## Skill-first and agent-first execution

- For every user prompt, first check whether an installed skill, a repository skill package, or a custom agent is a direct fit for the task.
- When a relevant skill or agent exists, prefer using it over solving the task from scratch. Treat direct ad hoc work as the fallback, not the default.
- Prefer the smallest capable orchestrator:
  - use a skill when the work is domain-specific and the skill already contains the workflow or tooling
  - use a custom agent when the task spans multiple files, domains, or workflow steps and should orchestrate skills
  - use direct editing only when no meaningful skill or agent match exists
- When several options match, prefer the closest domain-specific skill first, then the closest custom agent, then a general-purpose direct approach.
- Do not duplicate a skill's logic into workspace instructions or agent files. Route to the existing source of truth instead.

## Context and token discipline

- Keep context lean: read only the files needed, avoid repeating the same repository context, and prefer bounded handoffs over full-history dumps.
- If session overhead or instruction sprawl becomes a problem, audit with the available `context-budget` skill before adding more persistent instructions.
- Prefer scoped rules and targeted guidance over growing broad global instructions when the behavior only applies to one file type, domain, or workflow.
- When delegating, pass the minimum context needed for the receiving agent or skill to succeed.

## Validation

There is no single app build for this repository. Validate only the surfaces you touch:

- Markdown-only changes: keep links, paths, and examples accurate.
- Python changes in skill packages: run `python -m py_compile <file>` or `python -m compileall <touched-dir>`.
- Workflow or manifest changes: keep them compatible with the existing repository layout and CI expectations.

Prefer targeted validation over adding new tools, new dependencies, or repo-wide setup steps unless the task truly requires them.
