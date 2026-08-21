# CLAUDE.md — agent-launcher domain

Guidance for working inside `agent-launcher/`. See the root `CLAUDE.md` for
repo-wide rules.

## What this domain is

A plugin that scaffolds and launches **Claude Managed Agents (CMA)** in the user's
own Anthropic account, organized around a **per-session goal** that compiles into a
**loop or workflow**. Inspired by `anthropics/launch-your-agent` (Apache-2.0);
independent re-implementation, not a fork.

## Non-negotiable rules (enforced by SPEC.md + validators)

1. **Deterministic scaffolders only.** Every script under `skills/*/scripts/` is
   stdlib-only and makes **no** network/API calls. Live launches are emitted as
   BYOK curl. Do not add `requests`, `anthropic`, or any network client.
2. **Never surface the API key.** Launch scripts read `$ANTHROPIC_API_KEY`; no
   tool echoes/logs/writes a key. `payload_validator.py` and reviewers check this.
3. **CMA limits are law.** Keep `references/cma-primitives.md` as the source of
   truth for ceilings; validators must match it.
4. **Bounded loops only.** `loop_compiler.py` never emits a grade→iterate loop
   without a `max_iterations` cap (1..20).
5. **The hook is opt-in and crash-proof.** Gated by `AGENT_LAUNCHER_SESSION=1`;
   exits 0 on any error. Never make it fire unconditionally.
6. **The folder is the user's.** All artifacts go under `./my-agent/`; scripts
   accept `--out-dir` and default there. Never write into the plugin folder.

## Structure

- `skills/agent-launcher-orchestrator/` — `context: fork` goal router
  (`goal_router.py`, `goal_state.py`, `loop_compiler.py`).
- `skills/{interview,stage-launch,grade-iterate,run-without-you,wrap-up}/` — one
  phase each, 3 tools each.
- `agents/` — `cs-agent-launcher-orchestrator` + 3 phase specialists.
- `commands/` — 8 `/cs:*` commands.
- `hooks/` — opt-in `session_start.py` / `session_end.py` + `hooks.json`.
- `references/` — 5 shared docs. `assets/` — schema + templates + example.

## Tool conventions

- Every tool: `argparse` with real `--help`, a `--sample` that runs a deterministic
  demo and exits 0, and JSON output via `--json` where a machine reads it.
- Default output dir `./my-agent/`; never assume network access.
- Import shared logic via relative `sys.path` insert (see how the orchestrator
  tools import `goal_state`).

## Forcing-question discipline

Every SKILL.md ships a "Forcing-question library" (Matt Pocock grill-with-docs):
walk one question at a time, recommend an answer, cite the reference. The
`/cs:grill-agent-launcher` command surfaces them.

## When editing

- Changing a CMA limit → update `references/cma-primitives.md` **and** every
  validator in lockstep.
- Adding a loop shape → update `loop_compiler.py` **and**
  `references/loops-and-workflows.md`.
- Keep `SPEC.md` authoritative; if you ship something different, record it in the
  delivery report.
