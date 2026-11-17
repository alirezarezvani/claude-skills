---
name: video-director
description: Use whenever the user asks you to make, plan or produce a whole video - a launch teaser, promo, explainer, trailer, social clip or short film - from an idea, a brief, a changelog or data. Start here before animating anything; brief_gate.py fixes length, aspect and voice-over budget, then it runs beat board, code animatic, optional AI shots and conform to a finished MP4.
argument-hint: "[brief.json | one-sentence goal]"
context: fork
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "Previz-to-final pipeline: deterministic brief gate, beat timing, seekable HTML animatic rendered frame-exact with Playwright, ffmpeg conform with loudness QC. Generation MCPs are optional and only touch shots the user approved and paid for."
  distinct_from: "demo-video (screenshots to product walkthrough); video-content-strategist (channel strategy, hooks, SEO); cinematic-shot-prompting (camera prompts for one generated clip)"
---

# Video Director

> **Portability:** every step up to the final MP4 runs locally with Python, a browser engine (Playwright) and ffmpeg. No account, no credits. Generated footage is an optional, opt-in upgrade per shot.

You direct short films the way previz studios do: lock the story, timing and
framing in a cheap animatic first, and spend money only on shots that survive
review. The animatic is code (a seekable HTML timeline), so it renders the same
every time and a one-word change re-renders one shot, not the film.

## Workflow

```bash
P=${CLAUDE_PLUGIN_ROOT}/skills
# 1 Brief: derive aspect + VO word budget; ask what is open; refuse what is unsafe
python3 $P/video-director/scripts/brief_gate.py --brief film/brief.json --out film/brief.json
# 2 Beats → timed scene (refuses beats that do not fit the length)
python3 $P/video-beat-board/scripts/beat_board.py --brief film/brief.json --beats film/beats.json --out film/scene.json
# 3 Lint, compile, preview, render
python3 $P/video-animatic/scripts/motion_linter.py --scene film/scene.json
python3 $P/video-animatic/scripts/timeline_compiler.py --scene film/scene.json --out film/animatic.html
python3 $P/video-animatic/scripts/frame_renderer.py --html film/animatic.html --fps 12 --mp4 film/animatic.mp4
# 4 (previz-to-final lane only, after the animatic is approved) build the upgrade manifest
python3 $P/video-animatic/scripts/shot_manifest.py --scene film/scene.json --out film/shots.json
# 5 Final: switch mode to final, render at full fps, conform
python3 $P/video-animatic/scripts/timeline_compiler.py --scene film/scene.json --mode final --out film/final.html
python3 $P/video-animatic/scripts/frame_renderer.py --html film/final.html --out film/frames
python3 $P/video-conform/scripts/conform.py --render film/frames/render.json --scene film/scene.json --vo film/vo.wav --out film/final.mp4 --run
```

Exit codes carry the decisions: `brief_gate` 3 = ask (one question at a time,
recommended answer first), 4 = refuse; `beat_board` 4 = cut words or raise the
length; `motion_linter` 4 = fix before rendering; `conform` 4 = QC failed.

## Phase gates

| Phase | Done when | Hand-off |
|---|---|---|
| Brief | `brief_gate` READY | `brief.json` with lane, aspect, VO budget |
| Beats | `beat_board` FITS | `scene.json` (greybox) |
| Animatic | linter PASS, user watched `animatic.mp4` and approved | approved scene |
| Upgrade (optional) | every shot quoted, user said yes to the total | plates in `film/plates/`, set as plate `src` |
| Final | `conform` PASS | `final.mp4`, `captions.srt` |

Show the animatic before anything else is polished. Most notes land there, and
there they cost seconds.

## Shot upgrades with a generation MCP

Only in the `previz-to-final` lane and only after the animatic is approved.
Use whatever video-generation MCP the user has connected (Higgsfield,
ElevenLabs, Adobe, Canva or another); read its tool list at run time, never
assume model ids. For each shot in `shots.json`:

1. Get the provider's price without generating (Higgsfield `generate_video`
   takes `get_cost: true`). Show per-shot and total against `budget_credits`.
2. Generate only after the user says yes to that total. One batch, no retries
   on timeout: a timed-out job may still be charged; ask before resubmitting.
3. Save the plate, set it as the shot's plate `src`, re-render that shot only
   (`frame_renderer.py --shots s2`). Text, charts and logos stay as code layers
   on top, so they never come out garbled.

Data flow: prompts and any reference stills go to that provider under the
user's account. Nothing goes anywhere else.

## Hard rules

- No render before `brief_gate` READY; no generation without a quote and a yes.
- Never generate a real person's likeness without recorded consent.
- Label generated footage as AI-generated where it is published.
- Captions ship with every final (`captions.srt`).

## Forcing-question library

Ask one at a time, recommended answer first.

1. **What should the viewer do after watching?** Recommended: one action they can take today.
2. **Where does it run first?** Recommended: the platform with the most viewers; other aspects re-render from the same scene.
3. **How long?** Recommended: 15-30 s for social; every extra 10 s needs its own reason.
4. **Is there a voice-over, and who records it?** Recommended: a recorded human read; captions either way.
5. **May any shot be generated, and what is the credit cap?** Recommended: no at first; approve the free animatic, then upgrade one hero shot.
6. **Do real people appear, and is consent recorded?** Recommended: no generated likeness without it.

## References

- [previz_pipeline.md](references/previz_pipeline.md) — why animatic first, what each phase decides
- Sibling skills: `video-beat-board`, `video-animatic`, `video-conform`
