---
description: Phase 4 — make the agent run without you. Turn a graded agent into a recurring POSIX-cron scheduled deployment (optionally self-grading each firing), an event-driven curl trigger, or on-demand use, then finalize NEXT-DIRECTIONS, via the run-without-you skill. Tests with a manual run before trusting the schedule.
argument-hint: "[optional: cron expression, e.g. \"0 9 * * *\"]"
---

# /cs:run-without-you — Phase 4: Run Without You

Run the `run-without-you` skill.

**$ARGUMENTS**

## Steps

1. `python3 agent-launcher/skills/run-without-you/scripts/cron_validator.py --cron "0 9 * * *" --timezone Europe/Berlin`
   — invalid → exit 1; read the wall-clock DST note.
2. `python3 agent-launcher/skills/run-without-you/scripts/deployment_builder.py --sheet ./my-agent/build-sheet.json --agent-id agent_… --env-id env_… --nest-outcome --out ./my-agent/payloads/deployment.json`
   — prints BYOK curl to create + manually test the deployment.
3. Fire ONE manual `run`, read the verdict, then leave the cron in place; pin the
   agent version.
4. `python3 agent-launcher/skills/run-without-you/scripts/next_directions_writer.py --sheet ./my-agent/build-sheet.json --loop-shape cron-loop --out-dir ./my-agent`
5. `goal_state.py set --phase wrap-up`.

Test before you trust. Safety rails on by default. DST is wall-clock. ≤1,000
deployments/org.
