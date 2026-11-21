---
name: "game-universe-studio"
description: "Use when building a browser game prototype (Canvas, WebGL, Three.js, PixiJS, Babylon) and its character turnaround sheet, sprite set, procedural Web Audio sound effects or showcase card. Checks the game's asset manifest with game_manifest_validator.py before you ship it."
---

# Game Universe Studio

Plan the assets of a small browser game as one JSON manifest, then check that manifest before any art is generated or any code is wired up. The manifest holds the viewport, the main character's turnaround sheet and palette, the sprite animations, the procedural sound cues and the showcase card. A mismatch found here costs a JSON edit; found after the sprites are drawn, it costs a redraw.

Camera moves and shot language are out of scope; use `cinematic-shot-prompting` for those.

## Workflow

1. **Write the manifest.** Start from `examples/indie-game-showcase-manifest.json`. Field rules are in `references/game-manifest-schema.md`.
2. **Lock the character.** Fill `character` with all four turnaround views, the sheet size and 3 to 6 palette colors, and write the image prompt from `references/character-ortho-spec.md` (head-unit proportions, HEX palette, invariant features, no perspective change between views).
3. **Define the sounds.** Each `audio_cues` entry is one oscillator sweep. Build them with the recipes in `references/web-audio-synth-primitives.md`, resume the `AudioContext` on the first user gesture, and keep peak gain at or below 0.4.
4. **Validate.** Fix every BLOCKER; read each WARN and fix it or keep it on purpose:
   ```bash
   python3 scripts/game_manifest_validator.py --manifest game-manifest.json
   python3 scripts/game_manifest_validator.py --manifest game-manifest.json --strict --format json
   ```
   Exit 0 means valid, 1 means BLOCKERs (or WARNs under `--strict`), 2 means the file is missing or not a JSON object. Run `--sample` to see a passing report.
5. **Only then generate.** Generate the turnaround sheet first, then sprites from it, so every frame inherits the locked palette and proportions.

## What the validator checks

| Area | BLOCKER | WARN |
|---|---|---|
| Meta | missing `title`, unknown `engine` | `game_id` not kebab-case |
| Viewport | width or height missing or not positive | `aspect_ratio` disagrees with width:height |
| Character | | missing turnaround view, palette outside 3 to 6 colors, invalid HEX |
| Sprites | frames, fps or `tile_size` not positive, no `action` | no sprites defined |
| Audio | gain outside (0, 1], frequency outside 20 Hz to 20 kHz, duration not positive | unknown oscillator type, gain above 0.4 |
| Showcase card | `contrast_ratio` below 4.5 (WCAG 2.2 AA body text) | invalid `theme_accent` HEX |

The validator checks numbers it is given. It does not measure contrast from colors or listen to audio; `contrast_ratio` is the value you measured.
