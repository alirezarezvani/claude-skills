---
name: video-animatic
description: Use when building an animation, motion graphic, kinetic type, animated chart from data, or animatic with code and rendering it to MP4 frame-exact. Compiles a scene.v1 JSON into a seekable HTML timeline, lints readability, flashes and contrast, renders with Playwright, and exports clean keyframes for AI shot upgrades.
argument-hint: "[scene.json]"
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "scene.v1 JSON → one self-contained HTML page with window.__seek(t) → deterministic Playwright frame capture → ffmpeg. Five stdlib scripts; Playwright is the only install."
  distinct_from: "demo-video (screenshot walkthroughs); markdown-html md-slides (presentations, not video); cinematic-shot-prompting (prompts for generated clips)"
---

# Video Animatic

> **Portability:** Python stdlib scripts + Playwright (`pip install playwright && python -m playwright install chromium`, or Node Playwright) + ffmpeg. Free, offline with `--offline`.

The film is data. `scene.json` describes shots and layers in normalized
coordinates; `timeline_compiler.py` turns it into one HTML page whose
`window.__seek(t)` draws the exact frame at time `t`. Nothing runs on a wall
clock, so frame 214 is the same pixels every render, and one changed shot
re-renders alone.

## Workflow

```bash
S=${CLAUDE_PLUGIN_ROOT}/skills/video-animatic/scripts
python3 $S/motion_linter.py --scene film/scene.json                 # exit 4 = fix first
python3 $S/timeline_compiler.py --scene film/scene.json --out film/animatic.html
# open film/animatic.html in a browser: play, scrub, review
python3 $S/frame_renderer.py --html film/animatic.html --fps 12 --mp4 film/animatic.mp4   # review cut
python3 $S/frame_renderer.py --html film/animatic.html --shots s3   # re-render one shot after an edit
python3 $S/timeline_compiler.py --scene film/scene.json --aspect 9:16 --out film/vertical.html   # same film, vertical
```

Always lint the target aspect too (`motion_linter.py --aspect 9:16`): text that
fits 16:9 often leaves the safe area when re-framed.

## scene.v1 in one screen

```json
{"schema": "scene.v1",
 "meta": {"title": "Launch", "aspect": "16:9", "fps": 30, "target_duration": 12, "mode": "greybox"},
 "theme": {"bg": "#0b0d12", "fg": "#f5f7fa", "accent": "#5b8cff", "font_heading": "Inter"},
 "shots": [{"id": "s1", "duration": 4, "transition": "cut",
            "camera": {"move": "push-in", "amount": 0.06},
            "vo": "One line of narration.",
            "layers": [{"type": "text", "text": "Headline", "style": "title", "x": 0.5, "y": 0.45, "in": 0.2, "anim": "words"}]}]}
```

| Field | Values |
|---|---|
| layer `type` | `text`, `shape`, `image`, `chart` (bar/line, `data` or `csv`), `counter`, `lower_third`, `plate` (full-frame footage slot) |
| `anim` | `fade`, `rise`, `slide`, `scale`, `type`, `words`, `draw`, `grow`, `kenburns`, `none` |
| `camera.move` | `static`, `push-in`, `pull-out`, `pan-left/right`, `tilt-up/down`, `drift` |
| `transition` | `cut`, `fade` (crossfade), `dip` (through background) |
| `mode` | `greybox` (images and plates as labelled boxes) or `final` (real media; plate `src` may be an MP4) |

Text styles: `title`, `subtitle`, `body`, `caption`, `kicker`. Colours take a
hex value or a theme key (`fg`, `accent`, `muted`). `fixed: true` keeps a layer
out of the camera move.

## Linter (exit 4 blocks)

ML1 total vs target length · ML2 text leaves before it can be read · ML3
voice-over longer than its shot · ML4 more than 3 flashes per second (WCAG
2.3.1) · ML5 text contrast under 4.5:1 · ML6 layer timed outside its shot ·
ML7 upgrade shot without a prompt. Warnings: ML8 safe area, ML9 pacing, ML10
more than two fonts.

## Keyframes and the upgrade manifest

For shots marked `upgrade: true`, give the plate a storyboard still as `src`,
compile with `--mode final`, then:

```bash
python3 $S/frame_renderer.py --html film/final.html --out film/keyframes --keyframes
python3 $S/shot_manifest.py --scene film/scene.json --keyframes film/keyframes --out film/shots.json
```

`shots.json` (shots.v1) holds per shot: prompt, exact duration, aspect, a
camera-intent sentence, first/last keyframes and what stays as code overlay.
It names no provider and calls nothing; `video-director` quotes and sends it.
A greybox placeholder is never sent as a keyframe, because it carries no framing.

Render only pages you compiled yourself: `frame_renderer.py` opens the HTML in
Chromium from `file://`, where its script can read local files.

## Design rules

- One idea per shot; one heading face and one body face.
- Motion explains, never decorates: every move should point at what matters.
- Numbers count up, bars grow, lines draw; the viewer watches the change, not a slide.
- Keep the plate prompt free of text: titles and figures stay code.

See [motion_craft.md](references/motion_craft.md) for timing, easing,
accessibility and render sources.
