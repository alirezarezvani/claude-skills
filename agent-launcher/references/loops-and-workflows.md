# Loops and workflows — how a goal compiles

`loop_compiler.py` turns a session **goal + phase** into exactly one execution
shape. This file is the decision table it implements.

## The three shapes

### 1. Single-pass workflow (Phases 1–2)
A fixed, ordered path with no repeat: **interview → plan → validate → stage →
launch**. Deterministic, no self-grading. Used while the agent is still being
scoped and first launched. Anthropic's "Building effective agents" calls this a
*workflow*: predefined code paths orchestrate the steps.

Terminal state: a live session exists and produced its first output.

### 2. Grade→iterate loop (Phase 3) — bounded
The CMA **outcome** primitive. Send `user.define_outcome` with a required
`rubric`; an isolated grader returns pass/fail; failing verdicts feed the next
attempt. The loop is **bounded by `max_iterations`** (default 3, max 20) — never
unbounded. This is the plugin's answer to "make it good", not "run it forever".

Loop invariant: each iteration must move a rubric line from fail→pass or the run
halts at `max_iterations_reached` and escalates to the founder. Verdict-reading
(`verdict_reader.py`) decides the next move: **sharpen** the prompt/tools,
**re-run** as-is, or **promote to schedule**.

Terminal states: `satisfied` (ship it), `max_iterations_reached` / `failed`
(escalate), `interrupted` (resume).

### 3. Recurring deployment loop (Phase 4) — cron
A **scheduled deployment** (`depl_…`) fires a fresh session on a POSIX-cron
cadence — "run without you". Each firing is a `drun_…`. Optionally each firing
carries its own `user.define_outcome`, nesting a bounded grade→iterate loop
*inside* each recurring run.

Terminal state: none by design — it runs until paused/archived. Safety comes from
`always_ask` MCP permissions, `limited` networking, `read_only` memory where
possible, `max_iterations` per firing, and workspace spend limits. Always test
with a manual `run` before committing the schedule.

## Decision table (goal.phase → shape)

| Phase | Recurrence answer | Shape |
|---|---|---|
| interview / stage-launch | any | single-pass workflow |
| grade-iterate | "make it good", "grade it" | grade→iterate loop (bounded) |
| run-without-you | "every morning", "weekly", cron given | recurring deployment loop |
| run-without-you | "when X happens" (event) | event-driven curl (documented, not scheduled) |
| run-without-you | "only when I ask" | on-demand (no deployment) |

## Nesting rule

The most valuable production shape is a **cron loop whose `initial_events`
include a `user.define_outcome`** — every scheduled firing self-grades before it
finishes. `deployment_builder.py` supports this by accepting the outcome payload
from `outcome_builder.py`.

## Why bounded beats unbounded

An unbounded "keep improving" loop has no terminal state and burns budget with no
guarantee of convergence. CMA's `max_iterations` is a hard cap; this plugin never
emits a loop without one. Mirrors the repo's own loop-discipline canon
(engineering/agent-harness AR5, loop-library stop-states, tc-tracker).

## Sources

1. Anthropic — "Building effective agents" (workflows vs agents; prompt chaining, evaluator-optimizer).
2. Claude Managed Agents — Overview (outcomes, scheduled deployments).
3. anthropics/launch-your-agent — Phase 3 / Phase 4 design.
4. Google SRE Workbook — error budgets & bounded retries (loop-discipline analogue).
5. POSIX crontab(5) — 5-field schedule semantics.
6. IANA Time Zone Database — DST wall-clock behavior.
