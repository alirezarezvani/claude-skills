# video-studio

Make short films, explainers, teasers and animated charts the way previz
studios do: lock story, timing and framing in a free code animatic, then spend
on generated footage only for the shots you approved.

```
brief ──► beats ──► code animatic ──► review ──► (optional) AI shot upgrades ──► conform ──► MP4 + captions
 gate     timing    seekable HTML,      you       quote per shot, generate        loudness,
                    frame-exact render  approve   only after a yes                QC, aspects
```

## What is in it

| Skill | Tools | Does |
|---|---|---|
| `video-director` | `brief_gate.py` | Orchestrates the pipeline; derives aspect and VO word budget; asks open questions; refuses out-of-scope briefs and AI likeness without consent |
| `video-beat-board` | `beat_board.py` | Times beats (150 wpm VO, 180 wpm reading) and refuses a script that does not fit, naming the words to cut; emits `scene.v1` |
| `video-animatic` | `timeline_compiler.py`, `frame_renderer.py`, `motion_linter.py`, `shot_manifest.py`, `scene_model.py` | Compiles `scene.v1` to a seekable HTML animatic, renders it frame-exact with Playwright, blocks unreadable or flashing cuts, builds the provider-neutral upgrade manifest |
| `video-shot-upgrade` | `provider_adapter.py`, `budget_gate.py`, `drift_check.py` | Maps upgrade shots onto your own video MCP (Higgsfield adapter first, model limits read from its catalog at run time), keeps a spend ledger (quote, your yes to the exact total, one reserved call per shot, never a resubmitted timeout), and checks each generated plate against the animatic's framing |
| `video-conform` | `conform.py` | Mixes VO and music, normalizes loudness (AES TD1008 / EBU R 128), writes or burns captions, QC-checks the MP4 |

Agent: `cs-video-director`. Commands: `/cs-video`, `/cs-animatic`, `/cs-upgrade-shots`, `/cs-conform`.

## Quick start

```bash
pip install playwright && python -m playwright install chromium   # or Node Playwright
S=video/skills
python3 $S/video-beat-board/scripts/beat_board.py --brief video/assets/example-brief.json \
  --beats video/assets/example-beats.json --out film/scene.json
python3 $S/video-animatic/scripts/timeline_compiler.py --scene film/scene.json --out film/animatic.html
python3 $S/video-animatic/scripts/frame_renderer.py --html film/animatic.html --fps 12 --mp4 film/animatic.mp4
```

Open `film/animatic.html` in a browser to play and scrub it.

## Requirements

- Python 3.9+ (stdlib only in every script)
- Playwright (Python or Node) with Chromium, for rendering frames
- ffmpeg, for encoding and conform

## Generated footage, credits and data flow

Every film can be made without any generation service. Shots marked
`upgrade: true` stay greybox placeholders until you choose to upgrade them.

When you do, `video-shot-upgrade` uses a video-generation MCP **you**
connected under **your** account and credits. Higgsfield has an adapter
(verified 2026-11-26); other providers get one by copying
`adapters/template.json`. Before anything is generated it gets the provider's
price for every shot, shows the total against the lower of the brief's
`budget_credits` and your cap, and waits for your yes to that exact total. The
ledger reserves one call per shot and never resubmits a timed-out job, which
the provider may already have charged. `drift_check.py` then compares every
plate with the animatic and only plates that hold go into the final cut.

What leaves your machine, and only on an upgrade: the shot prompt, its
duration and aspect ratio, and any keyframe stills, sent to that provider.
Nothing is sent to this project or anyone else. Label generated footage as
AI-generated where you publish it.

## Roadmap

- **Release 2 (this release):** spend ledger, drift check, Higgsfield adapter.
  Drift thresholds are calibrated on synthetic plates so far; a capped credit
  test on real plates is next and may move them.
- **Release 3:** compositing presets for code layers over plates, more
  adapters, a shot bible for multi-character continuity.

## License

MIT. Independent implementation; no code from Claude Motion, HyperFrames or Remotion.
