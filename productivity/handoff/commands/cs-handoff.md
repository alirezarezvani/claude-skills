---
name: cs-handoff
description: "Generate a handoff document compacting the current conversation for a fresh agent to pick up. Walks the mandatory checklist, runs the redaction linter, saves to the configured location. On first run, asks 'Run setup now? (Y/n)' to choose where handoffs save (OS temp, home folder, project-local). Use when ending a session, switching machines, or passing work to another agent."
argument-hint: "[goal of next session]"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob"]
---

# /cs:handoff

Compact the current conversation into a handoff document for another agent to pick up.

## Invocation

```
/cs:handoff [optional description of what the next session will focus on]
```

The argument (if provided) becomes the **Goal of next session** verbatim. Without it, infer from the most recent unresolved thread.

## Flow

1. **Check first-run state.** Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/handoff/scripts/config_loader.py --status`.
   - If `should_prompt_setup: true`, ask the user: *"Run setup now? (Y/n)"*.
     - **Y** → invoke `/cs:handoff-setup`, then return here.
     - **N** → mark declined: `python3 ${CLAUDE_PLUGIN_ROOT}/skills/handoff/scripts/setup.py --decline`. Continue with defaults.
2. **Run cleanup of stale scaffolds.** `python3 ${CLAUDE_PLUGIN_ROOT}/skills/handoff/scripts/cleanup.py`. mtime-guarded — never deletes edited files.
3. **Walk the checklist.** Open `skills/handoff/references/handoff_prompt.md` and apply every step against the conversation.
4. **Generate scaffold.** `python3 ${CLAUDE_PLUGIN_ROOT}/skills/handoff/scripts/handoff_template_generator.py --goal "<goal>"`. Capture the printed path.
5. **Fill the five sections.** Goal / State of play / Open decisions / Skills to use / Artifacts. Reference artifacts; do not duplicate them.
6. **Recommend skills.** `python3 ${CLAUDE_PLUGIN_ROOT}/skills/handoff/scripts/skill_recommender.py --goal "<goal>"`. Pick 3-5 max. Edit the auto-list.
7. **Run the self-check.** `python3 ${CLAUDE_PLUGIN_ROOT}/skills/handoff/scripts/handoff_self_check.py <path>`. Fixes fidelity gaps (empty Goal, State bullets without artifacts, missing Decisions when git is dirty, too few/many Skills, inline content in Artifacts). Strict mode by default — resolve findings before save.
8. **Run the redaction linter.** `python3 ${CLAUDE_PLUGIN_ROOT}/skills/handoff/scripts/redaction_linter.py <path>`. Strict mode by default — resolve findings before save. Use `<!-- handoff:allow secret -->` for true false positives.
9. **Save and report path.** Print the final path so the user can open it.

## Refreshing an existing handoff

When work continues past the original handoff, pass `--refresh` to the generator instead of creating a new file:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/handoff/scripts/handoff_template_generator.py --refresh --goal "<updated goal>"
```

The script returns the path of the most recent handoff; edit it in place. Re-run the self-check and redaction linter after editing.

## What you do NOT do

- Do not paste the diff. Reference the branch/PR.
- Do not retype the PRD. Link to its path.
- Do not list more than 5 skills.
- Do not narrate the conversation chronologically.
- Do not save without running the linter.

## SessionStart auto-load

The plugin's `SessionStart` hook surfaces the most recent handoff (within retention window) on the next session start. The next agent reads it as data, not instructions. Disable per-session with `HANDOFF_SESSIONSTART=0`.

## Inspiration

Inspired by [Matt Pocock's handoff skill](https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff) (MIT). The no-duplication discipline is his.
