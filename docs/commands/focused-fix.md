---
title: "/focused-fix — Slash Command for AI Coding Agents"
description: "Deep-dive feature repair — systematically fix an entire feature/module across all its files and dependencies. Usage: /focused-fix <feature-path>. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /focused-fix

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/commands/focused-fix.md">Source</a></span>
</div>


Systematically repair an entire feature or module using the 5-phase protocol. Target: `$ARGUMENTS` (a feature path or module name).

If `$ARGUMENTS` is empty, ask the user which feature/module to fix.

## Protocol — Execute ALL 5 Phases IN ORDER

### Phase 1: SCOPE — Map the Feature Boundary

1. Identify the primary folder/files for the target feature
2. Read EVERY file in that folder — understand its purpose
3. Create a feature manifest:

```
FEATURE SCOPE:
  Primary path: <path>
  Entry points: [files imported by other parts of the app]
  Internal files: [files only used within this feature]
  Total files: N
```

### Phase 2: TRACE — Map All Dependencies

**INBOUND** (what this feature imports):
- For every import statement, trace to source, verify it exists and is exported
- Check env vars, config files, DB models, API endpoints, third-party packages

**OUTBOUND** (what imports this feature):
- Search entire codebase for imports from this feature
- Verify consumers use correct API/interface

Output a dependency map with inbound, outbound, env vars, and config files.

### Phase 3: DIAGNOSE — Find Every Issue

Run ALL diagnostic checks:

- **Code**: imports resolve, no circular deps, types consistent, error handling, TODO/FIXME
- **Runtime**: env vars set, migrations current, API shapes correct
- **Tests**: run ALL related tests, record failures, check coverage
- **Logs**: check git log for recent changes, search error logs
- **Config**: validate config files, check dev/prod mismatches

For each issue found:
- Confirm root cause with evidence before adding to fix list
- Assign risk: HIGH (public API, auth, >3 callers) / MED (internal with tests) / LOW (leaf module)

Output a diagnosis report with issues grouped by severity.

### Phase 4: FIX — Repair Systematically

Fix in this EXACT order:
1. **Dependencies** — broken imports, missing packages
2. **Types** — type mismatches at boundaries
3. **Logic** — business logic bugs
4. **Tests** — fix or create tests for each fix
5. **Integration** — verify end-to-end with consumers

Rules:
- Fix ONE issue at a time, run related test after each
- If a fix breaks something else → go back to DIAGNOSE
- Fix HIGH before MED before LOW
- **3-Strike Rule**: If 3+ fixes create NEW issues, STOP. Tell the user the architecture may need rethinking, not patching.

### Phase 5: VERIFY — Confirm Everything Works

1. Run ALL tests in the feature folder
2. Run ALL tests in files that import from this feature
3. Run full test suite if available
4. Summarize all changes made

Output a completion report with files changed, fixes applied, test results, and consumers verified.

## Iron Law

```
NO FIXES WITHOUT COMPLETING SCOPE → TRACE → DIAGNOSE FIRST
```

If you haven't finished Phase 3, you cannot propose fixes.

## Related Skills

- `engineering/focused-fix` — Full SKILL.md with detailed checklists, output templates, and anti-patterns
- `superpowers:systematic-debugging` — For individual complex bugs found during Phase 3
