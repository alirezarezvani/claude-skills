---
description: Main entry / resume for building a Claude Managed Agent. Runs the agent-launcher-orchestrator skill from the current session goal — reads ./my-agent/goal.json, routes to the right phase (interview → stage-launch → grade-iterate → run-without-you → wrap-up), compiles the loop/workflow, and forks to the phase skill. Emits BYOK curl; never makes API calls or prints the key.
argument-hint: "[optional: a one-sentence goal to set first]"
---

# /cs:launch — build/resume a Claude Managed Agent

Route through the `agent-launcher-orchestrator` skill.

**$ARGUMENTS**

## Steps

1. If `$ARGUMENTS` is a goal and no `./my-agent/goal.json` exists, set it:
   `python3 agent-launcher/skills/agent-launcher-orchestrator/scripts/goal_state.py init --goal "$ARGUMENTS"`.
2. Route from the current phase:
   `python3 agent-launcher/skills/agent-launcher-orchestrator/scripts/goal_router.py --out-dir ./my-agent`
   — act on exit 0 (route) / 3 (ask the printed question) / 4 (refuse; get one sentence).
3. Compile the loop:
   `python3 agent-launcher/skills/agent-launcher-orchestrator/scripts/loop_compiler.py --out-dir ./my-agent`.
4. Invoke the routed phase skill; on completion, `goal_state.py advance` and print a
   ≤100-word digest (phase done, artifact paths, loop shape, one next step).

## Refusals

- No goal set → run `/cs:goal set "..."` first.
- Under-3-word goal → get one sentence naming the one job.
- Never touch the network or the API key.
