---
title: "/code-to-prd — Slash Command for AI Coding Agents"
description: "Reverse-engineer a frontend codebase into a PRD. Usage: /code-to-prd [path]. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /code-to-prd

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/commands/code-to-prd.md">Source</a></span>
</div>


Reverse-engineer a frontend codebase into a complete Product Requirements Document.

## Usage

```bash
/code-to-prd                    # Analyze current project
/code-to-prd ./src              # Analyze specific directory
/code-to-prd /path/to/project   # Analyze external project
```

## What It Does

1. **Scan** — Run `codebase_analyzer.py` to detect framework, routes, APIs, enums, and project structure
2. **Scaffold** — Run `prd_scaffolder.py` to create `prd/` directory with README.md, per-page stubs, and appendix files
3. **Analyze** — Walk through each page following the Phase 2 workflow: fields, interactions, API dependencies, page relationships
4. **Generate** — Produce the final PRD with all pages, enum dictionary, API inventory, and page relationship map

## Steps

### Step 1: Analyze

Determine the project path (default: current directory). Run the frontend analyzer:

```bash
python3 {skill_path}/scripts/codebase_analyzer.py {project_path} -o .code-to-prd-analysis.json
```

Display a summary of findings: framework, page count, API count, enum count.

### Step 2: Scaffold

Generate the PRD directory skeleton:

```bash
python3 {skill_path}/scripts/prd_scaffolder.py .code-to-prd-analysis.json -o prd/
```

### Step 3: Fill

For each page in the inventory, follow the SKILL.md Phase 2 workflow:
- Read the page's component files
- Document fields, interactions, API dependencies, page relationships
- Fill in the corresponding `prd/pages/` stub

Work in batches of 3-5 pages for large projects (>15 pages). Ask the user to confirm after each batch.

### Step 4: Finalize

Complete the appendix files:
- `prd/appendix/enum-dictionary.md` — all enums and status codes found
- `prd/appendix/api-inventory.md` — consolidated API reference
- `prd/appendix/page-relationships.md` — navigation and data coupling map

Clean up the temporary analysis file:
```bash
rm .code-to-prd-analysis.json
```

## Output

A `prd/` directory containing:
- `README.md` — system overview, module map, page inventory
- `pages/*.md` — one file per page with fields, interactions, APIs
- `appendix/*.md` — enum dictionary, API inventory, page relationships

## Skill Reference

- `product-team/code-to-prd/SKILL.md`
- `product-team/code-to-prd/scripts/codebase_analyzer.py`
- `product-team/code-to-prd/scripts/prd_scaffolder.py`
- `product-team/code-to-prd/references/prd-quality-checklist.md`
