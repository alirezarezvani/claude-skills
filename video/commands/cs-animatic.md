---
disable-model-invocation: true
description: Lint, compile and render a scene.v1 file to an HTML preview and an MP4 animatic (free, no generation).
argument-hint: "scene.json [--aspect 9:16] [--shots s2,s3]"
---

# /cs-animatic

Render the animatic for `$ARGUMENTS` with the `video-animatic` skill.

```bash
S=${CLAUDE_PLUGIN_ROOT}/skills/video-animatic/scripts
python3 $S/motion_linter.py --scene <scene.json>        # exit 4: fix the findings first
python3 $S/timeline_compiler.py --scene <scene.json> --out <dir>/animatic.html
python3 $S/frame_renderer.py --html <dir>/animatic.html --fps 12 --mp4 <dir>/animatic.mp4
```

Pass `--aspect` to the linter and compiler for another aspect ratio, and `--shots` to the renderer
to re-render only the shots that changed. If no renderer is installed, the renderer prints the one
install line; say it to the user rather than guessing another tool.
