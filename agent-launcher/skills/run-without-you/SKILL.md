---
name: run-without-you
description: "Use when a graded managed agent should run on a schedule, on an event trigger or on demand ('run it every morning'). Validates cron with cron_validator.py and builds the deployment with deployment_builder.py."
license: MIT
metadata:
  version: 2.11.2
  author: Alireza Rezvani
  tags: [cma, deployment, cron, schedule, recurring, run-without-you, next-directions, dst]
  compatible_tools: [claude-code, codex-cli, cursor, antigravity, opencode, gemini-cli]
---

# Phase 4 — Run Without You (the recurring loop)

A **scheduled deployment** fires a fresh session on a cron cadence — the agent
runs without you. Each firing can carry its own outcome, nesting the bounded
grade→iterate loop inside every recurring run.

See [`../../references/loops-and-workflows.md`](../../references/loops-and-workflows.md).

## Choose the trigger

| Answer | Shape | Tool |
|---|---|---|
| "every morning / weekly / nightly" | recurring cron deployment | `deployment_builder.py` + `cron_validator.py` |
| "when X happens" | event-driven curl (documented, not scheduled) | `deployment_builder.py` (message only) |
| "only when I ask" | on-demand (no deployment) | none — just re-send a `user.message` |

## Workflow (recurring)

1. **Validate the schedule.**
   ```bash
   python3 scripts/cron_validator.py --cron "0 9 * * *" --timezone Europe/Berlin
   ```
   Invalid cron/timezone → exit 1. Read the **DST note**: wall-clock semantics mean
   spring-forward times are skipped and fall-back times fire twice — avoid
   02:00–03:00 in DST zones if exactly-once matters.
2. **Build the deployment payload.**
   ```bash
   python3 scripts/deployment_builder.py \
     --sheet ./my-agent/build-sheet.json --agent-id agent_123 --env-id env_456 \
     --nest-outcome --out ./my-agent/payloads/deployment.json
   ```
   `--nest-outcome` includes the rubric so **each firing self-grades**. The tool
   prints the BYOK curl to create it and to **test it once** with the manual `run`
   endpoint before trusting the schedule.
3. **Test before you trust.** Fire one manual `run`, read the verdict, only then
   leave the cron in place. Pin the agent version in the deployment once it passes.
4. **Finalize the roadmap.**
   ```bash
   python3 scripts/next_directions_writer.py \
     --sheet ./my-agent/build-sheet.json --loop-shape cron-loop --last-verdict satisfied --out-dir ./my-agent
   ```
5. **Advance + hand to wrap-up.** `goal_state.py set --phase wrap-up`, then invoke
   the `wrap-up` skill.

## Hard rules

- **Test with a manual `run` first.** Never commit a schedule you haven't fired once.
- **Safety rails on by default.** `always_ask` MCP, `limited` networking where you
  can, `read_only` untrusted memory, `max_iterations` per firing, workspace spend
  limit. There is no spend cap inside CMA.
- **DST is wall-clock.** Surface the note; pick safe times.
- **≤1,000 deployments/org.**

## Forcing-question library (recommend + cite)

1. "Cadence, event, or on-request?" *Recommend:* on-request v0 → cadence once graded.
   *Cite:* loops-and-workflows.md.
2. "Should each firing self-grade?" *Recommend:* yes — nest the outcome. *Cite:*
   loops-and-workflows.md (nesting rule).
3. "Which timezone, and is the time DST-safe?" *Recommend:* avoid 02:00–03:00 in
   DST zones. *Cite:* cma-primitives.md (wall-clock DST).
4. "Did you fire one manual run first?" *Recommend:* always. *Cite:* this SKILL.

## Tools

- `scripts/deployment_builder.py` — POST /v1/deployments payload (+ test-run curl).
- `scripts/cron_validator.py` — 5-field cron + IANA tz + DST note.
- `scripts/next_directions_writer.py` — write/refresh NEXT-DIRECTIONS.md.
