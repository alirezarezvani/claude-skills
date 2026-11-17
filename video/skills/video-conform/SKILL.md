---
name: video-conform
description: Use when finishing a video for delivery - mix voice-over and music, normalize loudness, add or burn in captions, and export a checked MP4 that plays everywhere. conform.py builds the ffmpeg command, then fails the export if duration or loudness misses its target.
argument-hint: "[render.json | video.mp4] [--vo file] [--music file]"
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "One ffmpeg command (H.264/yuv420p/+faststart, AAC 48 kHz, loudnorm to a named target, -1 dBTP), SRT from the scene's VO lines, post-encode QC on duration and integrated loudness"
  distinct_from: "video-animatic (makes the picture); video-content-strategist (platform strategy)"
---

# Video Conform

> **Portability:** one stdlib script driving ffmpeg. Without `--run` it only prints the plan and command.

Conform is where a good cut gets rejected: wrong loudness, music drowning the
voice, no captions, a file that will not play on a phone. The script makes one
ffmpeg pass and then checks the result instead of trusting it.

## Workflow

```bash
C=${CLAUDE_PLUGIN_ROOT}/skills/video-conform/scripts/conform.py
python3 $C --render film/frames/render.json --scene film/scene.json --vo film/vo.wav --music film/bed.mp3 --out film/final.mp4      # plan
python3 $C --render film/frames/render.json --scene film/scene.json --vo film/vo.wav --music film/bed.mp3 --out film/final.mp4 --run
python3 $C --video film/cut.mp4 --scene film/scene.json --loudness music --burn-captions --out film/final.mp4 --run
```

| Target (`--loudness`) | Integrated | True peak | Source |
|---|---|---|---|
| `speech` (default) | -18 LUFS | -1 dBTP | AES TD1008, speech and mixed content |
| `music` | -16 LUFS | -1 dBTP | AES TD1008, music |
| `broadcast` | -23 LUFS | -1 dBTP | EBU R 128 |

Music is mixed about 12 dB under the voice. `captions.srt` is always written
when a scene is given (one cue per shot, two lines of up to 42 characters);
`--burn-captions` also draws them in, which most social feeds need because
they autoplay muted.

QC after encode: duration within one frame of the scene and loudness within
1 LU of the target. Loudness is single-pass `loudnorm`, which lands within
1 LU on clips of about 5 s and longer; on very short stings measure and re-run
rather than widening the gate. A voice-over longer than the picture is warned
about, and a render with missing frames is refused. A miss is exit 4; fix the input (a clipped VO, a silent
track) rather than re-running until it passes.

## Delivery checklist

- [ ] `conform.py` PASS on the final file
- [ ] Captions present (sidecar or burned)
- [ ] Generated footage labelled as AI-generated where published
- [ ] One file per aspect: re-render the scene with `--aspect`, then conform each

See [delivery_specs.md](references/delivery_specs.md) for sources.
