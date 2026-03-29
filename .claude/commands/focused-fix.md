---
description: Deep-dive feature repair — systematically fix an entire feature/module. Usage: /focused-fix <feature-path>
---

Systematically repair the feature/module at `$ARGUMENTS` using the focused-fix 5-phase protocol.

If `$ARGUMENTS` is empty, ask which feature/module to fix.

Read `engineering/focused-fix/SKILL.md` and execute ALL 5 phases IN ORDER:

1. **SCOPE** — Map the feature boundary (all files, entry points, internal files)
2. **TRACE** — Map inbound + outbound dependencies across the entire codebase
3. **DIAGNOSE** — Check code, runtime, tests, logs, config. Assign risk labels (HIGH/MED/LOW). Confirm root causes with evidence.
4. **FIX** — Repair in order: deps → types → logic → tests → integration. One fix at a time, test after each. 3-strike escalation if fixes cascade.
5. **VERIFY** — Run all feature tests + consumer tests. Summarize changes.

**Iron Law:** No fixes before completing Phase 3. No exceptions.
