---
description: Phase 2 — turn a build sheet into exact API payloads and a resumable BYOK curl launch script, then launch (environment → agent → session → kickoff) with the founder's own key via the stage-launch skill. No tool makes API calls; the key never enters chat.
argument-hint: "[optional: path to build-sheet.json, default ./my-agent/build-sheet.json]"
---

# /cs:stage-launch — Phase 2: Stage → Launch

Run the `stage-launch` skill.

**$ARGUMENTS**

## Steps

1. `python3 agent-launcher/skills/stage-launch/scripts/payload_generator.py --sheet ./my-agent/build-sheet.json --out-dir ./my-agent`
2. `python3 agent-launcher/skills/stage-launch/scripts/launch_script_writer.py --out-dir ./my-agent`
3. `python3 agent-launcher/skills/stage-launch/scripts/payload_validator.py --dir ./my-agent`
   — FAIL blocks (especially a key_leak finding).
4. Minimal key step (in the founder's shell, never chat):
   `[ -n "$ANTHROPIC_API_KEY" ] && echo present || echo "export ANTHROPIC_API_KEY=... first"`.
5. `export ANTHROPIC_API_KEY=... && ./my-agent/launch.sh` — watch the first poll,
   mark checkpoints with Console links, then `goal_state.py set --phase grade-iterate`.

## Hard rules

- The key never enters chat, a file, a payload, or a log.
- Sequential launch; watch the first poll foreground. Re-running launch.sh resumes.
