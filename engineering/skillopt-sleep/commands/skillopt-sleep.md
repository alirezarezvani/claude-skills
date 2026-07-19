---
description: Run or manage the SkillOpt-Sleep self-evolution cycle (review past sessions, replay tasks offline, consolidate validated memory + skills; can also schedule nightly runs)
argument-hint: "[run | dry-run | status | adopt | harvest | schedule | unschedule] (default: status)"
allowed-tools: Bash, Read
---

# /skillopt-sleep — SkillOpt-Sleep nightly self-evolution

You are driving **SkillOpt-Sleep**: a tool that lets this user's Claude agent
improve offline by reviewing past sessions, replaying recurring tasks, and
consolidating what it learns into **validated** memory (`CLAUDE.md`) and skills
(`SKILL.md`). It is gated like SkillOpt: a change is kept only if it improves a
held-out replay score, and nothing live is modified until the user adopts it.

## Requested action: $ARGUMENTS

(If `$ARGUMENTS` is empty, treat it as `status`.)

## How to run it

The engine is the `skillopt_sleep` Python package in this repo. Use the
**plugin's bundled runner** so the right interpreter and repo are on the path:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/sleep.sh" <action> --project "$(pwd)" --scope invoked
```

`<action>` is one of:

| action       | what it does |
|--------------|--------------|
| `status`     | show how many nights have run + the latest staged proposal (READ-ONLY) |
| `dry-run`    | harvest → mine → replay → report, but **stage nothing** (safe preview) |
| `run`        | full cycle: also **stage** a reviewed proposal (still does NOT touch live files) |
| `adopt`      | apply the latest staged proposal to live `CLAUDE.md` / `SKILL.md` (backs up first) |
| `harvest`    | debug: print the recurring tasks mined from recent sessions |
| `schedule`   | install a nightly cron entry for this project (`--hour --minute`, off-:00 by default) |
| `unschedule` | remove the nightly cron entry (`--all` to remove every managed entry) |

Default backend is `mock` (deterministic, no API spend). To use real budget for
genuine improvement, add `--backend claude` or `--backend codex`. To steer what
the optimizer writes, add `--preferences "<your house rules>"`.

## Steps to follow

1. **For `schedule`:** confirm with the user *before* running it. Unlike
   every other action, `schedule` writes directly to the user's real
   crontab the moment it runs (via `scheduler.schedule()` → `crontab -`) —
   it is not a preview. Tell them what will be scheduled (project, hour,
   minute, backend) and get an explicit go-ahead first. If they'd rather
   review the exact line before anything is installed, offer
   `${CLAUDE_PLUGIN_ROOT}/scripts/install-cron.sh` instead (prints the line;
   installs nothing). Once they've confirmed, add `--yes` to the `schedule`
   invocation in step 2 — the CLI itself refuses to install non-interactively
   without it (defense-in-depth for anyone running the CLI directly, outside
   this chat-confirmed flow); `--yes` is how you record that the confirmation
   above already happened.
2. **Run the requested action** via the bundled runner above. Capture stdout.
3. **For `run` / `dry-run`:** after it completes, `Read` the generated
   `report.md` in the staging dir it prints, and show the user:
   - held-out score: baseline → candidate (the proof it helped)
   - the gate decision (accept/reject) and the exact edits it proposes
   - where the proposal is staged
4. **For `run` that produced an accepted proposal:** tell the user the diff is
   staged and that **nothing live changed yet**. Offer to run `/skillopt-sleep adopt`.
5. **For `adopt`:** confirm which live files were updated and that backups were
   written under the staging dir's `backup/`.
6. **Never** edit `CLAUDE.md` or `SKILL.md` yourself — only the `adopt` action
   does that, with a backup. Respect the review gate.

## Safety reminders

- Harvest is **read-only** over `~/.claude`. Replay in `mock` mode runs no
  shell side effects.
- The cycle stages proposals; the user is in control of adoption.
- `schedule` installs a real crontab entry immediately — it is not a preview,
  unlike `run`/`dry-run`. Always confirm with the user first (see Steps to
  follow, step 1), then pass `--yes`. Without `--yes`, the CLI itself refuses
  to install non-interactively — that's a backstop for direct CLI use, not a
  substitute for the chat confirmation above. `${CLAUDE_PLUGIN_ROOT}/scripts/install-cron.sh`
  remains available as a print-only alternative for a user who wants to inspect
  or hand-edit the line before installing anything.
