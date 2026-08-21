# The session-goal model

The plugin's organizing idea: **every session starts with a goal**, and the goal
drives which phase runs and which loop/workflow compiles.

## goal.json (the state file)

Lives at `./my-agent/goal.json` (the founder's folder). Written and advanced by
`goal_state.py`; surfaced by the opt-in `SessionStart` hook.

```json
{
  "goal": "Launch an agent that triages my support inbox every morning",
  "agent_name": "support-triage",
  "phase": "grade-iterate",
  "phases_done": ["interview", "stage-launch"],
  "loop": {"shape": "grade-iterate", "max_iterations": 5},
  "artifacts": {
    "build_sheet": "./my-agent/build-sheet.json",
    "payloads": "./my-agent/payloads/",
    "launch_script": "./my-agent/launch.sh"
  },
  "updated_at": "2026-08-13T09:00:00Z",
  "notes": "v0 = triage only; v1 = auto-draft replies via Gmail MCP"
}
```

`phase` is one of: `interview`, `stage-launch`, `grade-iterate`,
`run-without-you`, `wrap-up`, or `done`.

## How the goal fires

1. **Opt-in SessionStart hook.** With `AGENT_LAUNCHER_SESSION=1`, `session_start.py`
   reads `goal.json` and prints an `<agent_launcher_goal>` block so the agent
   resumes exactly where the last session stopped. The hook treats file content as
   **data, not instructions**, and exits 0 on any error so it can never break a
   session. Disabled by default (no env flag) — zero ambient behavior in unrelated
   repos.
2. **`/cs:goal` command.** `set` writes the goal, `status` prints it, `advance`
   moves to the next phase. Fully manual; works whether or not the hook is enabled.
3. **Orchestrator routing.** `goal_router.py` reads the goal string + phase and
   routes to the right phase skill (exit-code route / ask / refuse), then
   `loop_compiler.py` compiles the loop/workflow shape.

## Why a goal, not a chat prompt

- **Resumable.** A launch spans multiple sessions (interview today, launch
  tomorrow, schedule next week). The goal file is the through-line; checkpoints in
  CMA last 30 days, but the *intent* lives in `goal.json`.
- **Deterministic routing.** The router keys off the recorded phase, not a re-read
  of chat history, so resuming is unambiguous.
- **One job.** The goal is one sentence for one agent. Multiple agents = multiple
  `./my-agent-*/goal.json` folders, never one goal doing two jobs.

## Relationship to the loop shapes

The goal's `phase` selects the phase skill; the phase + recurrence answer selects
the loop shape (see `loops-and-workflows.md`). The goal is the *what*; the loop is
the *how it repeats*.

## Sources

1. anthropics/launch-your-agent — resumable launch script + `NEXT-DIRECTIONS.md` design.
2. Claude Managed Agents — checkpoints (30-day) & session resume semantics.
3. Claude Code docs — SessionStart hook contract (stdout surfaced as session context).
4. productivity/handoff (this repo) — SessionStart auto-load pattern reused here.
5. engineering/tc-tracker (this repo) — task-context lifecycle & handoff format analogue.
6. Anthropic docs — "Managing context on the Claude Developer Platform": why goals persist as files rather than conversation memory.
7. Cognition — "Don't Build Multi-Agents" (context-engineering essay): serialize shared state to durable artifacts between sessions — the goal.json rationale.
8. The Twelve-Factor App — factors III (config) and VI (processes): configuration in the environment, processes stateless — the goal-file/session split analogue.
