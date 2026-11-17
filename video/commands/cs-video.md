---
disable-model-invocation: true
description: Make a short video end to end - brief, beats, code animatic, optional AI shot upgrades, conformed MP4 with captions.
argument-hint: "\"one-sentence goal\" | brief.json"
---

# /cs-video

Make the film described by `$ARGUMENTS` with the `video-director` skill.

1. Write `film/brief.json` from what the user said, then gate it:
   `python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-director/scripts/brief_gate.py --brief film/brief.json --out film/brief.json`.
   Exit 3: ask the open questions one at a time. Exit 4: stop and explain.
   A filled example lives at `${CLAUDE_PLUGIN_ROOT}/assets/example-brief.json`.
2. Draft `film/beats.json` (see `${CLAUDE_PLUGIN_ROOT}/assets/example-beats.json`) and run
   `beat_board.py --brief film/brief.json --beats film/beats.json --out film/scene.json`
   from `${CLAUDE_PLUGIN_ROOT}/skills/video-beat-board/scripts/`.
3. Lint, compile and render the animatic with the scripts in
   `${CLAUDE_PLUGIN_ROOT}/skills/video-animatic/scripts/`, then show the user `film/animatic.mp4`.
4. Only in the previz-to-final lane and after approval: build `film/shots.json`, quote each shot
   with the connected generation MCP, and generate after an explicit yes.
5. Render final and conform with `${CLAUDE_PLUGIN_ROOT}/skills/video-conform/scripts/conform.py --run`.
