---
name: video-beat-board
description: Use whenever the user asks if a video or reel script, voice-over or narration fits its length, what to trim or cut, or wants a script broken into a timed shot list. beat_board.py times each beat at speaking and reading pace, refuses a script that does not fit and says how many words to cut.
argument-hint: "[brief.json] [beats.json]"
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "Deterministic timing: narration at 150 wpm, on-screen reading at 180 wpm + 0.5 s, 1.5 s floor; refusal with a word-cut number when beats exceed the brief; emits scene.v1"
  distinct_from: "video-content-strategist (what to say and where); video-animatic (how it moves)"
---

# Video Beat Board

> **Portability:** one stdlib script. Input is JSON you can write by hand.

Scripts for short video fail on arithmetic, not ideas: 60 words of narration
do not fit in 15 seconds, and a headline that leaves after one second was never
read. Write the beats; let the tool do the clock.

## Workflow

1. Get a READY brief from `video-director` (`brief_gate.py`). It carries
   `duration_s`, `aspect`, `lane` and `vo_word_budget`.
2. Write `beats.json`: one object per beat.

   ```json
   [{"vo": "Your release notes are a wall of text.", "on_screen": "Release notes nobody reads",
     "visual": "dense changelog scrolling", "kind": "motion"},
    {"vo": "Teams save over an hour per release.", "stat": {"to": 68, "suffix": " min"},
     "on_screen": "saved per release", "kind": "motion"},
    {"vo": "Version two turns them into a brief.", "visual": "engineer at a desk at night, laptop glow",
     "kind": "upgrade"}]
   ```

   `kind: "upgrade"` marks a candidate for generated footage; `visual` becomes
   its plate prompt. Data beats take `stat`, `chart` (`{"kind":"bar","data":[[label,value]]}`)
   or `csv`.
3. Time it:

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-beat-board/scripts/beat_board.py \
     --brief film/brief.json --beats film/beats.json --out film/scene.json
   ```

   - **FITS (exit 0):** `scene.json` is a greybox animatic; hand it to `video-animatic`.
   - **DOES-NOT-FIT (exit 4):** cut the number of words it names, or drop a beat.
     Do not raise the length unless the user agrees: the length came from the brief.
4. A stretch above 1.6x is a warning that the film will drag: add a beat or shorten the brief.

## Rules of thumb the tool encodes

| Rule | Value | Why |
|---|---|---|
| Narration pace | 150 wpm (2.5 words/s) | Clear read with breathing room |
| On-screen reading | 0.5 s + words ÷ 3 per s | Top of the 160-180 wpm subtitle guidance |
| Shortest shot | 1.5 s | Below that a beat registers as a flash |
| Stat or chart beat | +1.6 s | The number has to land after it animates |

## Forcing questions

1. **What is the one line the viewer must remember?** Recommended: make it the on-screen text of the strongest beat.
2. **Which beat can go?** Recommended: the one that restates the previous beat.
3. **Which single shot would gain most from real footage?** Recommended: one emotional or physical moment; keep data and text as motion graphics.

See [beat_timing.md](references/beat_timing.md) for the sources behind the numbers.
