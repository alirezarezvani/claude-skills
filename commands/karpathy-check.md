---
name: karpathy-check
description: Run Karpathy's 4-principle review on staged changes or the last commit. Checks complexity, diff noise, hidden assumptions, and goal verification. Usage /karpathy-check [--last-commit]
---

# /karpathy-check

Review your staged changes (or last commit) against Karpathy's 4 coding principles.

## Usage

```
/karpathy-check                 # review staged changes
/karpathy-check --last-commit   # review the most recent commit
```

## What it runs

1. **Principle #2 (Simplicity):** `scripts/complexity_checker.py` on all changed files — detects over-engineering, premature abstractions, deep nesting, long functions
2. **Principle #3 (Surgical):** `scripts/diff_surgeon.py` on the diff — detects comment-only changes, whitespace noise, style drift, drive-by refactors
3. **Principles #1 + #4 (Think + Goals):** The `karpathy-reviewer` agent reads the diff and applies human-judgment checks — hidden assumptions, missing verification

## Output

A structured report with per-principle verdicts and specific line-level fix recommendations.

## When to run

- Before committing (catches noise and overcomplication early)
- After completing a feature (sanity check before PR)
- When you suspect the LLM overcoded something

## Sub-agent

Dispatches the `karpathy-reviewer` agent. See `agents/karpathy-reviewer.md`.

## Scripts

- `engineering/karpathy-coder/scripts/complexity_checker.py`
- `engineering/karpathy-coder/scripts/diff_surgeon.py`
- `engineering/karpathy-coder/scripts/assumption_linter.py`
- `engineering/karpathy-coder/scripts/goal_verifier.py`

## Skill Reference

→ `engineering/karpathy-coder/SKILL.md`
