# handoff (productivity)

> Compact the current conversation into a handoff document for another agent to pick up.

A productivity-shaped handoff skill. Configurable save location (no project clutter), redaction enforcement, SessionStart auto-load, mandatory checklist for the agent. Five sections, three to five recommended skills, references not copies.

**Inspired by** [Matt Pocock's handoff skill](https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff) (MIT). Matt's seven sentences are preserved verbatim in `SKILL.md`. The wrapper around them — first-run setup, redaction linter, SessionStart hook, mandatory checklist, skill recommender — is original work in this repo.

## Five must-haves shipped in v1.0.0

| # | Feature | Why |
|---|---|---|
| 1 | **SessionStart hook** auto-loads the latest handoff | Without this, the file is written but unread. The hook turns the artifact into an actual handoff. |
| 2 | **First-run setup** asks where to save | Avoids cluttering project folders. No pre-selected default — user picks explicitly on first run. |
| 3 | **Mandatory checklist** (`handoff_prompt.md`) | Forces the agent to classify every topic (State / Decision / drop) rather than free-handing prose. |
| 4 | **Redaction linter** | Operationalizes Matt's redaction sentence with regex + whitelist marker + strict/warn modes. |
| 5 | **mtime-guarded cleanup** | Auto-cleanup never deletes a handoff the user edited as a working surface. |

## v1.1 additions

| Feature | Why |
|---|---|
| **SessionEnd reminder hook** | Pairs with SessionStart. If a session ends without a recent handoff, prints a one-line reminder so the user doesn't lose context for next time. Disable with `HANDOFF_SESSIONEND=0`. |
| **Self-check script** (`handoff_self_check.py`) | Operationalizes the mandatory checklist. Flags empty Goal, State bullets that reference no artifact, missing Open decisions when git is dirty, too few/many Skills, inline content in Artifacts. Runs before the redaction linter. |
| **`--refresh` flag** on the template generator | Reuses the most recent handoff instead of creating a new file. Keeps the save location uncluttered when work continues past the original handoff. |

## Install

This plugin lives at `productivity/handoff/`. Enable through your plugin manager. On first invocation of `/cs:handoff`, the skill will prompt:

> Run setup now? (Y/n)

- **Y** — walks 5 questions and writes `~/.config/handoff/config.json`.
- **N** — uses defaults this run and never re-prompts (sentinel at `~/.config/handoff/.setup-declined`).

Re-configure any time with `/cs:handoff-setup`.

## Slash commands

| Command | Use |
|---|---|
| `/cs:handoff [goal]` | Generate the handoff doc. |
| `/cs:handoff-setup [--project]` | Configure (or reconfigure) save location, retention, redaction. |

## Tooling

Stdlib-only Python. No external deps.

| Script | Purpose |
|---|---|
| `scripts/setup.py` | First-run Q&A. `--reconfigure`, `--project`, `--decline`, `--sample`. |
| `scripts/config_loader.py` | Shared helper. `--show`, `--status`, `--sample`. |
| `scripts/handoff_template_generator.py` | Writes the 5-section scaffold. `--goal`, `--print-path-only`, `--sample`. |
| `scripts/redaction_linter.py` | Scans for secrets/PII. `--mode strict\|warn\|off`, `--json`, `--sample`. |
| `scripts/skill_recommender.py` | Suggests 3-5 skills. `--goal`, `--scope`, `--json`, `--sample`. |
| `scripts/cleanup.py` | mtime-guarded retention cleanup. `--dry-run`, `--json`, `--sample`. |

## Hooks

`hooks/session_start.py` (wired via `hooks/hooks.json`) — on every SessionStart, finds the most recent handoff in the configured save location and surfaces it as `<handoff_from_previous_session>` data. The next agent reads it as context, not instructions. Disable per-session with `HANDOFF_SESSIONSTART=0`.

## References

| File | Topic |
|---|---|
| `references/handoff_prompt.md` | The mandatory checklist the agent walks before writing. |
| `references/handoff_structure.md` | The 5-section template with a worked example. |
| `references/deduplication_discipline.md` | Matt's no-duplication rule with concrete do-this-not-that pairs. |
| `references/redaction_checklist.md` | Regex patterns + manual review steps + whitelist mechanism. |
| `references/configuration.md` | Field-by-field config reference. |

## Distinct from `engineering/handoff/`

| Aspect | `productivity/handoff/` | `engineering/handoff/` |
|---|---|---|
| Primary audience | End-of-day session handoff, cross-machine handoff | Code/PR handoff |
| First-run setup | Yes (5 questions, configurable save location) | No (fixed `mktemp`) |
| Redaction enforcement | Yes (linter with strict/warn/off + inline whitelist) | No |
| SessionStart auto-load | Yes (hook + retention-aware) | No |
| Mandatory checklist | Yes (`handoff_prompt.md`, 6 steps) | No |
| Retention cleanup | Yes (mtime-guarded) | No |

Both exist deliberately. The engineering version stays optimized for code/PR contexts. This one is for the broader daily routine.

## Inspired by

[Matt Pocock's handoff skill](https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff) (MIT). The seven-sentence body of `SKILL.md` is Matt's, preserved verbatim. The wrapper is this repo's.

## License

MIT.
