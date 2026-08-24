# run-without-you (Phase 4 — the recurring loop)

Turn a graded agent into a **recurring POSIX-cron scheduled deployment** (each
firing can nest a self-grading outcome), an event-driven curl trigger, or
confirmed on-demand use. Always test with one manual `run` before trusting the
schedule.

## Usage

```bash
python3 scripts/cron_validator.py --cron "0 9 * * *" --timezone Europe/Berlin
python3 scripts/deployment_builder.py --sheet ./my-agent/build-sheet.json \
  --agent-id agent_… --env-id env_… --nest-outcome \
  --out ./my-agent/payloads/deployment.json
python3 scripts/next_directions_writer.py --sheet ./my-agent/build-sheet.json \
  --loop-shape cron-loop --out-dir ./my-agent
```

## Tools

| Tool | Purpose |
|---|---|
| `deployment_builder.py` | `POST /v1/deployments` payload + BYOK create/test-run curl |
| `cron_validator.py` | 5-field POSIX cron + IANA tz + wall-clock DST note (exit 1 on invalid) |
| `next_directions_writer.py` | write/refresh `NEXT-DIRECTIONS.md` from deferrals |

DST and deployment semantics: [`../../references/cma-primitives.md`](../../references/cma-primitives.md).
