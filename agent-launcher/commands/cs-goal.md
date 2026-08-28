---
description: Set, show, or advance the per-session agent-launcher goal (./my-agent/goal.json) — the through-line of a CMA launch. Backs the opt-in SessionStart hook. Subcommands map to goal_state.py init/set/status/advance.
argument-hint: "set \"<goal>\" | status | advance | phase <name>"
---

# /cs:goal — manage the session goal

The goal is one sentence for one agent. It selects the phase and the loop shape.

**$ARGUMENTS**

Run `goal_state.py` under `agent-launcher/skills/agent-launcher-orchestrator/scripts/`:

- `set "<goal>"` → `goal_state.py init --goal "<goal>"` (or `set --goal` if it exists).
- `status` → `goal_state.py status` (prints goal, agent_name, phase, phases_done, loop).
- `advance` → `goal_state.py advance` (moves to the next phase).
- `phase <name>` → `goal_state.py set --phase <name>` (interview | stage-launch |
  grade-iterate | run-without-you | wrap-up | done).

Enable auto-surfacing each session with `export AGENT_LAUNCHER_SESSION=1` (the
opt-in SessionStart hook). Two jobs → two goals in two `./my-agent-*/` folders.
