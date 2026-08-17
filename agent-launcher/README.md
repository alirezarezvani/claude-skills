# agent-launcher

Build, launch, grade, and schedule **Claude Managed Agents (CMA)** in your own
Anthropic account — as a Claude Code plugin where **every session starts with a
goal** and that goal compiles into a **loop or a workflow**.

Inspired by Anthropic's reference skill
[`anthropics/launch-your-agent`](https://github.com/anthropics/launch-your-agent)
(Apache-2.0). This is an independent re-implementation for the claude-skills
marketplace — not a fork — that adds agents/sub-agents, an opt-in session-start
goal, deterministic scaffolders, and explicit loop/workflow compilation.

## The four phases

| Phase | Skill | Command | Loop/workflow |
|---|---|---|---|
| 1 · Interview → Plan | `interview` | `/cs:interview` | single-pass workflow |
| 2 · Stage → Launch | `stage-launch` | `/cs:stage-launch` | single-pass workflow |
| 3 · Grade → Iterate | `grade-iterate` | `/cs:grade` | **grade→iterate loop** (bounded by `max_iterations`) |
| 4 · Run Without You | `run-without-you` | `/cs:run-without-you` | **recurring cron deployment loop** |
| — · Close out | `wrap-up` | `/cs:wrap-up` | — |

`agent-launcher-orchestrator` (`context: fork`) reads the session goal, routes to
the right phase, and compiles the loop.

## Every session starts with a goal

- State lives in `./my-agent/goal.json` (your folder — it keeps working after the
  session ends).
- **Set it:** `/cs:goal set "Launch an agent that triages my inbox every morning"`.
- **Resume it automatically:** enable the opt-in hook with
  `export AGENT_LAUNCHER_SESSION=1`; the `SessionStart` hook surfaces the current
  goal + phase so you pick up exactly where you left off. Disabled by default — no
  ambient behavior in unrelated repos.
- **Advance it:** `/cs:goal advance` moves to the next phase.

## Loops vs workflows

`loop_compiler.py` compiles the goal + phase into exactly one shape:

- **single-pass workflow** — interview → plan → stage → launch (Phases 1–2).
- **grade→iterate loop** — CMA `user.define_outcome` self-grading, **bounded** by
  `max_iterations` (1..20); never unbounded (Phase 3).
- **recurring deployment loop** — POSIX-cron scheduled deployment that re-runs the
  goal "without you", optionally self-grading each firing (Phase 4).

See [`references/loops-and-workflows.md`](references/loops-and-workflows.md).

## Safety & hard rules

- **Deterministic scaffolders only** — every tool is stdlib-only and makes no API
  calls. Live launches are emitted as **BYOK curl scripts** you run with your own
  `$ANTHROPIC_API_KEY`. The key is never printed, logged, or written.
- Validators enforce CMA limits (≤20 skills/session, ≤8 memory stores, depth-1
  multiagent, `max_iterations` ≤20, …).
- The opt-in hook can never break a session (exits 0 on any error).

## Quick start

```bash
export AGENT_LAUNCHER_SESSION=1          # optional: auto-surface the goal each session
/cs:goal set "Nightly repo dependency auditor that writes report.md"
/cs:launch                               # runs the orchestrator from the current phase
```

## Layout

```
agent-launcher/
├── SPEC.md                     # the build goal (verification target)
├── skills/                     # 6 skills, 3 stdlib tools each
├── agents/                     # 4 agents (orchestrator + interviewer + grader + deployer)
├── commands/                   # 8 /cs:* commands
├── hooks/                      # opt-in SessionStart / SessionEnd
├── references/                 # 5 shared reference docs
└── assets/                     # build-sheet schema, overview + NEXT-DIRECTIONS templates, example
```

## Attribution

Inspired by `anthropics/launch-your-agent` (Apache-2.0). CMA primitive semantics
are drawn from the public [Claude Managed Agents docs](https://platform.claude.com/docs/en/managed-agents/overview).
No upstream code is copied verbatim. License: MIT (this plugin).
