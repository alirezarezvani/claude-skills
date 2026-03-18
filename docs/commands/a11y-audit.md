---
title: "/a11y-audit — Slash Command for AI Coding Agents"
description: "Scan a frontend project for WCAG 2.2 accessibility violations and fix them. Usage: /a11y-audit [path]. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /a11y-audit

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/commands/a11y-audit.md">Source</a></span>
</div>


Scan a frontend project for WCAG 2.2 accessibility issues, show fixes, and optionally check color contrast.

## Usage

```bash
/a11y-audit                     # Scan current project
/a11y-audit ./src               # Scan specific directory
/a11y-audit ./src --fix         # Scan and auto-fix what's possible
```

## What It Does

### Step 1: Scan

Run the a11y scanner on the target directory:

```bash
python3 {skill_path}/scripts/a11y_scanner.py {path} --json
```

Parse the JSON output. Group findings by severity (critical → serious → moderate → minor).

Display a summary:
```
A11y Audit: ./src
  Critical: 3 | Serious: 7 | Moderate: 12 | Minor: 5
  Files scanned: 42 | Files with issues: 15
```

### Step 2: Fix

For each finding (starting with critical):

1. Read the affected file
2. Show the violation with context (before)
3. Apply the fix from `references/framework-a11y-patterns.md`
4. Show the result (after)

**Auto-fixable issues** (apply without asking):
- Missing `alt=""` on decorative images
- Missing `lang` attribute on `<html>`
- `tabindex` values > 0 → set to 0
- Missing `type="button"` on non-submit buttons
- Outline removal without replacement → add `:focus-visible` styles

**Issues requiring user input** (show fix, ask to apply):
- Missing alt text (need description from user)
- Missing form labels (need label text)
- Heading restructuring (may affect layout)
- ARIA role changes (may affect functionality)

### Step 3: Contrast Check

If CSS files are present, run the contrast checker:

```bash
python3 {skill_path}/scripts/contrast_checker.py --batch {path}
```

For each failing color pair, suggest accessible alternatives.

### Step 4: Report

Generate a markdown report at `a11y-report.md`:
- Executive summary (pass/fail, issue counts)
- Per-file findings with before/after diffs
- Remaining manual review items
- WCAG criteria coverage

## Skill Reference

- `engineering-team/a11y-audit/SKILL.md`
- `engineering-team/a11y-audit/scripts/a11y_scanner.py`
- `engineering-team/a11y-audit/scripts/contrast_checker.py`
- `engineering-team/a11y-audit/references/wcag-quick-ref.md`
- `engineering-team/a11y-audit/references/aria-patterns.md`
- `engineering-team/a11y-audit/references/framework-a11y-patterns.md`
