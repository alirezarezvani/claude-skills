---
title: "/tdd — Slash Command for AI Coding Agents"
description: "Generate tests, analyze coverage, and run TDD workflows. Usage: /tdd <generate|coverage|validate> [options]. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /tdd

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/commands/tdd.md">Source</a></span>
</div>


Generate tests, analyze coverage, and validate test quality using the TDD Guide skill.

## Usage

```
/tdd generate <file-or-dir>     Generate tests for source files
/tdd coverage <test-dir>        Analyze test coverage and gaps
/tdd validate <test-file>       Validate test quality (assertions, edge cases)
```

## Examples

```
/tdd generate src/auth/login.ts
/tdd coverage tests/ --threshold 80
/tdd validate tests/auth.test.ts
```

## Scripts
- `engineering-team/tdd-guide/scripts/test_generator.py` — Test case generation (library module)
- `engineering-team/tdd-guide/scripts/coverage_analyzer.py` — Coverage analysis (library module)
- `engineering-team/tdd-guide/scripts/tdd_workflow.py` — TDD workflow orchestration (library module)
- `engineering-team/tdd-guide/scripts/fixture_generator.py` — Test fixture generation (library module)
- `engineering-team/tdd-guide/scripts/metrics_calculator.py` — TDD metrics calculation (library module)

> **Note:** These scripts are library modules without CLI entry points. Import them in Python or use via the SKILL.md workflow guidance.

## Skill Reference
→ `engineering-team/tdd-guide/SKILL.md`
