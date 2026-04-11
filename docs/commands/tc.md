---
title: "/tc — Slash Command for AI Coding Agents"
description: "Track technical changes with structured records, a state machine, and session handoff. Usage: /tc. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /tc

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/commands/tc.md">Source</a></span>
</div>


Dispatch a TC (Technical Change) command. Arguments: `$ARGUMENTS`.

If `$ARGUMENTS` is empty, print this menu and stop:

```
/tc init                       Initialize TC tracking in this project
/tc create <name>              Create a new TC record
/tc update <tc-id> [...]       Update fields, status, files, handoff
/tc status [tc-id]             Show one TC or the registry summary
/tc resume <tc-id>             Resume a TC from a previous session
/tc close <tc-id>              Transition a TC to deployed
/tc export                     Re-render derived artifacts
/tc dashboard                  Re-render the registry summary
```

Otherwise, parse `$ARGUMENTS` as `<subcommand> <rest>` and dispatch to the matching protocol below. All scripts live at `engineering/tc-tracker/scripts/`.

## Subcommands

### `init`

1. Run:
   ```bash
   python3 engineering/tc-tracker/scripts/tc_init.py --root . --json
   ```
2. If status is `already_initialized`, report current statistics and stop.
3. Otherwise report what was created and suggest `/tc create <name>` as the next step.

### `create <name>`

1. Parse `<name>` as a kebab-case slug. If missing, ask the user for one.
2. Prompt the user (one question at a time) for:
   - Title (5-120 chars)
   - Scope: `feature | bugfix | refactor | infrastructure | documentation | hotfix | enhancement`
   - Priority: `critical | high | medium | low` (default `medium`)
   - Summary (10+ chars)
   - Motivation
3. Run:
   ```bash
   python3 engineering/tc-tracker/scripts/tc_create.py --root . \
     --name "<slug>" --title "<title>" --scope <scope> --priority <priority> \
     --summary "<summary>" --motivation "<motivation>" --json
   ```
4. Report the new TC ID and the path to the record.

### `update <tc-id> [intent]`

1. If `<tc-id>` is missing, list active TCs (status `in_progress` or `blocked`) from `tc_status.py --all` and ask which one.
2. Determine the user's intent from natural language:
   - **Status change** → `--set-status <state>` with `--reason "<why>"`
   - **Add files** → one or more `--add-file path[:action]`
   - **Add a test** → `--add-test "<title>" --test-procedure "<step>" --test-expected "<result>"`
   - **Update handoff** → any combination of `--handoff-progress`, `--handoff-next`, `--handoff-blocker`, `--handoff-context`
   - **Add a note** → `--note "<text>"`
   - **Add a tag** → `--tag <tag>`
3. Run:
   ```bash
   python3 engineering/tc-tracker/scripts/tc_update.py --root . --tc-id <tc-id> [flags] --json
   ```
4. If exit code is non-zero, surface the error verbatim. The state machine and validator will reject invalid moves — do not retry blindly.

### `status [tc-id]`

- If `<tc-id>` is provided:
  ```bash
  python3 engineering/tc-tracker/scripts/tc_status.py --root . --tc-id <tc-id>
  ```
- Otherwise:
  ```bash
  python3 engineering/tc-tracker/scripts/tc_status.py --root . --all
  ```

### `resume <tc-id>`

1. Run:
   ```bash
   python3 engineering/tc-tracker/scripts/tc_status.py --root . --tc-id <tc-id> --json
   ```
2. Display the handoff block prominently: `progress_summary`, `next_steps` (numbered), `blockers`, `key_context`.
3. Ask: "Resume <tc-id> and pick up at next step 1? (y/n)"
4. If yes, run an update to record the resumption:
   ```bash
   python3 engineering/tc-tracker/scripts/tc_update.py --root . --tc-id <tc-id> \
     --note "Session resumed" --reason "session handoff"
   ```
5. Begin executing the first item in `next_steps`. Do NOT re-derive context — trust the handoff.

### `close <tc-id>`

1. Read the record via `tc_status.py --tc-id <tc-id> --json`.
2. Verify the current status is `tested`. If not, refuse and tell the user which transitions are still required.
3. Check `test_cases`: warn if any are `pending`, `fail`, or `blocked`.
4. Ask the user:
   - "Who is approving? (your name, or 'self')"
   - "Approval notes (optional):"
   - "Test coverage status: none / partial / full"
5. Run:
   ```bash
   python3 engineering/tc-tracker/scripts/tc_update.py --root . --tc-id <tc-id> \
     --set-status deployed --reason "Approved by <approver>" --note "Approval: <approver> — <notes>"
   ```
   Then directly edit the `approval` block via a follow-up update if your script version supports it; otherwise instruct the user to record approval in `notes`.
6. Report: "TC-NNN closed and deployed."

### `export`

There is no automatic HTML export in this skill. Re-validate everything instead:

1. Read the registry.
2. For each record, run:
   ```bash
   python3 engineering/tc-tracker/scripts/tc_validator.py --record <path> --json
   ```
3. Run:
   ```bash
   python3 engineering/tc-tracker/scripts/tc_validator.py --registry docs/TC/tc_registry.json --json
   ```
4. Report: total records validated, any errors, paths to anything invalid.

### `dashboard`

Run the all-records summary:
```bash
python3 engineering/tc-tracker/scripts/tc_status.py --root . --all
```

## Iron Rules

1. **Never edit `tc_record.json` by hand.** Always use `tc_update.py` so revision history is appended and validation runs.
2. **Never skip the state machine.** Walk forward through states even if it feels redundant.
3. **Never delete a TC.** History is append-only — add a final revision and tag it `[CANCELLED]`.
4. **Background bookkeeping.** When mid-task, spawn a background subagent to update the TC. Do not pause coding to do paperwork.
5. **Validate before reporting success.** If a script exits non-zero, surface the error and stop.

## Related Skills

- `engineering/tc-tracker` — Full SKILL.md with schema reference, lifecycle diagrams, and the handoff format.
- `engineering/changelog-generator` — Pair with TC tracker: TCs for the per-change audit trail, changelog for user-facing release notes.
- `engineering/tech-debt-tracker` — For tracking long-lived debt rather than discrete code changes.
