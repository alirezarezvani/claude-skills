---
name: stage-launch
description: "Use when a managed-agent build sheet is ready to launch ('launch it', 'deploy the agent'). Generates and validates API payloads with payload_generator.py and payload_validator.py and writes a resumable curl script with launch_script_writer.py that uses the user's own key."
license: MIT
metadata:
  version: 2.11.2
  author: Alireza Rezvani
  tags: [cma, launch, payloads, curl, byok, api-key-safety, environment, agent, session]
  compatible_tools: [claude-code, codex-cli, cursor, antigravity, opencode, gemini-cli]
---

# Phase 2 — Stage → Launch

Turn the build sheet into runnable artifacts, then let the founder launch with
their own key. **No script here touches the network or the key** — the user runs
`launch.sh`.

## Workflow

1. **Generate payloads.**
   ```bash
   python3 scripts/payload_generator.py \
     --sheet ./my-agent/build-sheet.json --out-dir ./my-agent
   # -> ./my-agent/payloads/{01-environment,02-agent,03-session,04-kickoff}.json
   ```
   Agent toolset → `always_allow`; every MCP toolset → `always_ask` (baked into
   the agent payload's `permission_policies`).
2. **Write the launch script.**
   ```bash
   python3 scripts/launch_script_writer.py --out-dir ./my-agent
   ```
   `launch.sh` creates environment → agent → session → kickoff **in order**,
   chaining IDs, and **resumes** on re-run (each step skips if its `*.id` file
   exists). It reads `$ANTHROPIC_API_KEY` at runtime.
3. **Validate before launch.**
   ```bash
   python3 scripts/payload_validator.py --dir ./my-agent
   ```
   FAIL blocks — especially a `key_leak` finding. Fix and re-run.
4. **Minimal key step (never in chat).** Check the shell first:
   ```bash
   [ -n "$ANTHROPIC_API_KEY" ] && echo "key present" || echo "export ANTHROPIC_API_KEY=... first"
   ```
   Point the founder to platform.claude.com → API keys. **Never print the key to
   chat, never write it to a file.**
5. **Launch + watch the first poll.**
   ```bash
   export ANTHROPIC_API_KEY=...      # in their shell, not in chat
   ./my-agent/launch.sh
   ```
   Mark checkpoints with Console deep links. Then `goal_state.py set --phase
   grade-iterate` and advance.

## Hard rules (API-key safety)

- **The key never enters chat, a file, a payload, or a log.** `launch.sh` reads it
  from the environment; `payload_validator.py` scans for `sk-ant-…` leaks and FAILs.
- **Sequential launch.** environment → agent → session → kickoff. Watch the first
  poll foreground before declaring success.
- **Resumable.** Re-running `launch.sh` continues from the last created ID.

## Forcing-question library (recommend + cite)

1. "Is the key in your shell env already?" *Recommend:* check `$ANTHROPIC_API_KEY`
   before anything. *Cite:* this SKILL, key-safety rules.
2. "Cloud or self-hosted environment?" *Recommend:* cloud for v0. *Cite:*
   cma-primitives.md (environment).
3. "Any MCP server in the payload?" *Recommend:* keep it `always_ask`. *Cite:*
   cma-primitives.md (permissions).
4. "Did the first poll return idle/running cleanly?" *Recommend:* watch it
   foreground before moving on. *Cite:* cma-primitives.md (session lifecycle).

## Tools

- `scripts/payload_generator.py` — build sheet → 4 ordered API payloads.
- `scripts/launch_script_writer.py` — resumable BYOK curl launcher (no key handling).
- `scripts/payload_validator.py` — pre-launch check + API-key-leak scan.
