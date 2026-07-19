---
name: skillopt-sleep
description: "Use when the user wants their Claude agent to self-improve from past usage, asks about a nightly/offline 'sleep' or 'dream' cycle, memory/skill consolidation, or says things like 'make my agent better the more I use it', 'review my past sessions', 'learn my preferences', 'consolidate what you learned', 'run the sleep cycle', or wants to schedule offline self-optimization. Drives the skillopt_sleep engine: harvest past sessions -> mine recurring tasks -> replay offline -> consolidate validated CLAUDE.md and SKILL.md behind a held-out gate."
---

# SkillOpt-Sleep: offline self-evolution for a local Claude agent

SkillOpt-Sleep gives the user's agent a **sleep cycle**. While the user is
offline (e.g. nightly), it reviews their real past Claude Code sessions,
re-runs recurring tasks on their own API budget, and consolidates what it
learns into **memory** (`CLAUDE.md`) and **skills** (`SKILL.md`) — but only
keeps changes that pass a held-out validation gate, and only after the user
adopts them. The agent gets measurably better at *this* user's recurring work,
with no model-weight training. It is the deployment-time analogue of training:
short-term experience → long-term competence.

It synthesizes three ideas:
- **SkillOpt** — the skill/memory doc is trainable text; bounded add/delete/replace
  edits; accepted only through a held-out gate; rejected edits become negative feedback.
- **Claude Dreams** — offline consolidation that reads past sessions and rebuilds
  memory (dedup/merge/resolve); the input is never mutated; output is reviewed then adopted.
- **Agent sleep** — periodic offline replay turns episodes into durable skill.

## When to use this skill

Trigger when the user wants any of:
- "make my agent learn from how I use it" / "get better the more I use it" / "remember my preferences across sessions"
- a nightly/scheduled or on-demand **offline self-improvement / dream / sleep** run
- to **review past sessions/trajectories** and distill recurring tasks
- to **consolidate** feedback into `CLAUDE.md` or a managed skill
- to **schedule** the cycle (cron) or **adopt** a staged proposal

## The cycle (six stages)

1. **Harvest** — read `~/.claude/projects/*/<session>.jsonl` + `~/.claude/history.jsonl` (READ-ONLY) → session digests.
2. **Mine** — digests → `TaskRecord`s (recurring intents + outcome labels + checkable refs where possible).
3. **Replay** — re-run tasks offline under the *current* skill+memory → (hard, soft) scores.
4. **Consolidate** — reflect on failures → propose bounded edits → **gate** on a held-out slice; accept only if it strictly improves.
5. **Stage** — write `proposed_CLAUDE.md`, `proposed_SKILL.md`, a diff, and `report.md` into `<project>/.skillopt-sleep/staging/<date>/`. **Nothing live changes.**
6. **Adopt** — explicit (or opt-in auto): copy staged files over live ones, backing up first.

## How to drive it

Prefer the `/skillopt-sleep` command. Under the hood it calls the bundled runner:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/sleep.sh" status                       # what's happened
"${CLAUDE_PLUGIN_ROOT}/scripts/sleep.sh" dry-run --project "$(pwd)"    # safe preview
"${CLAUDE_PLUGIN_ROOT}/scripts/sleep.sh" run --project "$(pwd)"        # full cycle, stages a proposal
"${CLAUDE_PLUGIN_ROOT}/scripts/sleep.sh" adopt --project "$(pwd)"      # apply staged proposal (with backup)
```

- Default backend is `mock` (deterministic, **no API spend**) — good for trying the plumbing.
- Add `--backend claude` or `--backend codex` to spend the user's real budget for genuine improvement.
- Scope defaults to the invoked project; `--scope all` harvests every project.

### Scheduling

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/sleep.sh" schedule --project "$(pwd)" --hour 3 --minute 17
"${CLAUDE_PLUGIN_ROOT}/scripts/sleep.sh" unschedule --project "$(pwd)"
```

Installs a nightly cron entry. `unschedule --all` removes every managed entry.

## All CLI flags

| Flag | Default | Description |
|------|---------|-------------|
| `--project PATH` | cwd | Project directory to evolve |
| `--scope all\|invoked` | invoked | Harvest scope |
| `--backend mock\|claude\|codex\|copilot` | mock | Replay backend (mock = no API spend) |
| `--model NAME` | backend default | Override the model used for replay |
| `--source claude\|codex\|auto` | claude | Transcript source |
| `--lookback-hours N` | 72 | Harvest window |
| `--max-sessions N` | unlimited | Cap harvested sessions |
| `--max-tasks N` | 40 | Cap mined tasks |
| `--target-skill-path PATH` | auto | Explicit SKILL.md to evolve |
| `--tasks-file PATH` | — | Reviewed TaskRecord JSON (skip harvest) |
| `--progress` | off | Print phase progress to stderr |
| `--auto-adopt` | off | Auto-adopt if gate passes |
| `--edit-budget N` | 4 | Max bounded edits per night |
| `--json` | off | Machine-readable JSON output |

## Config keys (`~/.skillopt-sleep/config.json`)

Beyond the CLI flags, advanced behavior is controlled via config:

- **`preferences`** — free-text house rules injected into the optimizer's reflect step (e.g. "Always use async/await", "Answers in `\boxed{}`").
- **`gate_mode`** — `on` (default, validation-gated) or `off` (greedy, accept all edits).
- **`gate_metric`** — `hard`, `soft`, or `mixed` (default). Controls how the held-out gate scores.
- **`dream_rollouts`** — >1 enables multi-rollout contrastive reflection per task.
- **`recall_k`** — >0 recalls K similar past tasks into the dream (long-term memory).
- **`evolve_memory`** / **`evolve_skill`** — independently toggle CLAUDE.md vs SKILL.md consolidation.

## Memory consolidation

The sleep cycle can consolidate both:
- **SKILL.md** — the managed skill file (bounded edits: add/delete/replace)
- **CLAUDE.md** — the project memory (same bounded edits)

Both are gated by the same held-out validation score. Set `evolve_memory: false` to consolidate only skills, or `evolve_skill: false` for only memory.

## Hard rules

- **Never** hand-edit the user's `CLAUDE.md` / `SKILL.md` as part of this skill.
  Only the `adopt` action changes live files, and it backs them up first.
- Harvest is read-only. `mock` replay has no side effects.
- Always show the user the **held-out baseline → candidate** score and the
  exact proposed edits before suggesting adoption. Evidence before adoption.
- If asked whether it really helps, run
  `python -m skillopt_sleep.experiments.run_experiment --persona researcher --json`
  — a deterministic demo that proves held-out lift and that the gate blocks
  harmful edits.

## Validate / demo

```bash
# deterministic proof (no API): held-out score rises, gate blocks regressions
python -m skillopt_sleep.experiments.run_experiment --persona researcher --assert-improves
python -m skillopt_sleep.experiments.run_experiment --persona programmer  --assert-improves
```

See the upstream SkillOpt-Sleep guide section
(https://microsoft.github.io/SkillOpt/docs/guideline.html#sleep) for recorded
output and the full design. (The original repo-relative design-doc path,
`docs/superpowers/specs/...`, is not vendored into this repo — see this
skill's README.md "What was and wasn't vendored" table.)
