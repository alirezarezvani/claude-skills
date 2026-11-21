---
disable-model-invocation: true
description: Finish a video - mix VO and music, normalize loudness, write or burn captions, export a QC-checked MP4.
argument-hint: "render.json|video.mp4 [--vo file] [--music file] [--loudness speech|music|broadcast]"
---

# /cs-conform

Conform `$ARGUMENTS` with the `video-conform` skill. First print the plan, then run it:

```bash
C=${CLAUDE_PLUGIN_ROOT}/skills/video-conform/scripts/conform.py
python3 $C --render <render.json> --scene <scene.json> [--vo <vo>] [--music <music>] --out <final.mp4>
python3 $C --render <render.json> --scene <scene.json> [--vo <vo>] [--music <music>] --out <final.mp4> --run
```

Exit 4 means QC failed (duration or loudness off target): report the measured numbers and the likely
cause instead of re-running until it passes.
