# stage-launch (Phase 2)

Turn a build sheet into exact CMA API payloads and a **resumable BYOK curl launch
script**. No tool makes API calls; the user runs `launch.sh` with their own
`$ANTHROPIC_API_KEY` — the key is never printed, logged, or written.

## Usage

```bash
python3 scripts/payload_generator.py --sheet ./my-agent/build-sheet.json --out-dir ./my-agent
python3 scripts/launch_script_writer.py --out-dir ./my-agent
python3 scripts/payload_validator.py --dir ./my-agent   # FAILs on an embedded key

export ANTHROPIC_API_KEY=...   # in your shell, never in chat
./my-agent/launch.sh           # env → agent → session → kickoff; re-run resumes
```

## Tools

| Tool | Purpose |
|---|---|
| `payload_generator.py` | build sheet → 4 ordered payloads (env/agent/session/kickoff) |
| `launch_script_writer.py` | resumable BYOK curl launcher (no key handling) |
| `payload_validator.py` | pre-launch check + API-key-leak scan (exit 1 on FAIL) |

CMA payload semantics: [`../../references/cma-primitives.md`](../../references/cma-primitives.md).
