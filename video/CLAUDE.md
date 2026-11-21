# video/ — guidance for Claude Code

One plugin, `video-studio`: four skills that take a brief to a finished MP4
through a code animatic (`video-director`, `video-beat-board`,
`video-animatic`, `video-conform`).

- `scene.v1` (see `skills/video-animatic/scripts/scene_model.py`) is the one
  source of truth for a film. Every tool reads or writes it; do not add a
  second format.
- Coordinates are normalized 0..1 so one scene renders at every aspect.
  Re-render, never stretch.
- Scripts stay stdlib-only. Playwright and ffmpeg are runtime tools the
  scripts call, not imports at module level (`frame_renderer.py` imports
  Playwright lazily).
- No script calls a generation service. Upgrades go through the user's own
  MCP connector, quoted per shot, after an explicit yes (see the
  `video-director` skill).
- Exit codes: 0 ok, 2 bad input, 3 ask or missing dependency, 4 blocking
  refusal or failed QC.
