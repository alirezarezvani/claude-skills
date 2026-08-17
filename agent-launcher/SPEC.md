# agent-launcher — Build Spec (the goal)

**Status:** authoritative build target. The verification workflow scores every
shipped file against this document. Anything shipped that differs from this spec
must be recorded in the delivery report with a reason.

## What this is

A Claude Code **plugin** that turns Anthropic's reference skill
[`anthropics/launch-your-agent`](https://github.com/anthropics/launch-your-agent)
(Apache-2.0) into a full domain plugin with **agents, sub-agents, skills,
commands, an opt-in session-start goal, and loops/workflows**.

The upstream skill walks a technical founder through building a **Claude Managed
Agent (CMA)** in four phases. This plugin keeps that four-phase spine and adds a
repo-native shape:

- **Every session starts with a goal.** A `./my-agent/goal.json` state file holds
  the current goal + phase. An opt-in `SessionStart` hook (env-gated) surfaces it;
  the `/cs:goal` command sets/advances it manually. The goal is the single source
  of "what are we launching, and where are we in launching it".
- **Goals become loops or workflows.** A deterministic `loop_compiler.py` turns a
  goal + phase into one of:
  - a **grade→iterate loop** (Phase 3) — CMA `user.define_outcome` self-grading,
    bounded by `max_iterations` (1..20);
  - a **recurring deployment loop** (Phase 4) — a POSIX-cron scheduled deployment
    that re-runs the goal "without you";
  - a **single-pass workflow** (Phases 1–2) — interview → plan → stage → launch.

## Hard rules (non-negotiable)

1. **Deterministic scaffolders only.** Every Python tool is stdlib-only and makes
   **no** network/API calls. Live launches are emitted as runnable **BYOK curl
   scripts** the user executes with their own `$ANTHROPIC_API_KEY`. Complies with
   the repo's "no LLM calls in scripts" + ClawHub "no paid dependencies" rules.
2. **Never print the API key.** Launch scripts read `$ANTHROPIC_API_KEY` from the
   environment; no tool echoes, logs, or writes a key.
3. **The folder is theirs.** All artifacts land in `./my-agent/` (build sheet,
   payloads, launch script, eval scaffold, deployment, overview page,
   `NEXT-DIRECTIONS.md`, `goal.json`) and keep working after the session ends.
4. **Everything versioned.** v0 is the core job; v1/v2 capture every deferred item
   with its reason and exact mechanism.
5. **Respect CMA limits.** Validators enforce the documented ceilings (≤20 skills/
   session, ≤8 memory stores, ≤20 roster / 25 threads / depth-1 multiagent,
   `max_iterations` 1..20, ≤20 creds/vault, ≤1000 deployments/org).
6. **The hook is opt-in and can never break a session.** Gated by
   `AGENT_LAUNCHER_SESSION=1`; any error exits 0.

## Deliverables

### Skills (6) — orchestrator + 5 phase skills

| Skill | Phase | Role |
|---|---|---|
| `agent-launcher-orchestrator` | — | `context: fork` session-goal router; classifies the goal, routes to a phase skill, compiles the loop/workflow |
| `interview` | 1 | Interview → Plan: build sheet (primitives table, v1/v2 deferrals, eval plan) |
| `stage-launch` | 2 | Stage → Launch: validated payloads + resumable BYOK curl launch script |
| `grade-iterate` | 3 | Grade → Iterate loop: outcome/rubric, verdict reading, held-back eval scaffold |
| `run-without-you` | 4 | Recurring loop: cron scheduled deployment + NEXT-DIRECTIONS |
| `wrap-up` | — | Close-out: primitive inventory, overview page, next 1–2 upgrades |

### Tools (18) — 3 deterministic stdlib scaffolders per skill

- **orchestrator:** `goal_router.py` (goal → lane, exit-code route/ask/refuse),
  `goal_state.py` (init/set/status/advance goal.json), `loop_compiler.py`
  (goal+phase → plan.v1: grade-loop / cron-loop / single-pass).
- **interview:** `interview_planner.py` (answers → primitives table + deferrals),
  `build_sheet_builder.py` (assemble build-sheet.json), `primitives_validator.py`
  (validate vs CMA limits → PASS/WARN/FAIL).
- **stage-launch:** `payload_generator.py` (build sheet → env/agent/session/kickoff
  JSON payloads), `launch_script_writer.py` (resumable BYOK curl launcher),
  `payload_validator.py` (required-field + limit check pre-launch).
- **grade-iterate:** `outcome_builder.py` (`user.define_outcome` payload, clamps
  max_iterations), `verdict_reader.py` (grader result → table + next move),
  `eval_scaffold.py` (held-back cases + parallel-run plan).
- **run-without-you:** `deployment_builder.py` (`POST /v1/deployments` payload),
  `cron_validator.py` (5-field POSIX cron + IANA tz + DST note), 
  `next_directions_writer.py` (write/refresh NEXT-DIRECTIONS.md).
- **wrap-up:** `primitives_inventory.py` (recap owned primitives),
  `overview_page.py` (regenerate agent-overview.html), `upgrade_suggester.py`
  (next 1–2 upgrades from deferrals).

Every tool passes `--help` and `--sample` (exit 0), stdlib-only.

### Agents (4)

- `cs-agent-launcher-orchestrator` — session-goal router persona (forks context).
- `cs-agent-interviewer` — Phase-1 interview specialist sub-agent.
- `cs-agent-grader` — Phase-3 grade→iterate loop specialist sub-agent.
- `cs-agent-deployer` — Phase-4 scheduling / run-without-you specialist sub-agent.

### Commands (8)

`/cs:launch` (main entry / resume), `/cs:goal` (set/show/advance goal),
`/cs:interview`, `/cs:stage-launch`, `/cs:grade`, `/cs:run-without-you`,
`/cs:wrap-up`, `/cs:grill-agent-launcher` (Matt Pocock docs-anchored grill).

### Hooks (opt-in, env-gated)

`hooks/hooks.json` + `hooks/session_start.py` (surface current goal as
`<agent_launcher_goal>` data; gated by `AGENT_LAUNCHER_SESSION=1`) +
`hooks/session_end.py` (remind to checkpoint goal state; gated by
`AGENT_LAUNCHER_SESSIONEND` default on when session flag set).

### References (shared, domain-level)

`cma-primitives.md`, `interview-to-config.md`, `examples-bank.md`,
`loops-and-workflows.md`, `session-goal-model.md` — each citing authoritative
sources incl. the CMA docs and the upstream repo.

### Assets

`build-sheet.schema.json`, `agent-overview.template.html`,
`NEXT-DIRECTIONS.template.md`, `example-build-sheet.json`.

## Attribution

Inspired by `anthropics/launch-your-agent` (Apache-2.0). This is an independent
plugin re-implementation for the claude-skills marketplace, not a fork; the CMA
primitive semantics are drawn from the public CMA docs. Recorded in
`plugin.json` `source` + this SPEC + README.
