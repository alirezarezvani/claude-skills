# Previz-to-final: why the animatic comes first

The pipeline borrows the order film and animation studios use: decide story,
timing and framing in the cheapest medium that can show them, then spend on
the expensive medium only for what survived review. Generated video is the
expensive medium here: every clip costs credits, takes minutes, and comes back
slightly different each time.

## What each phase decides

| Phase | Decides | Cost to change it here | Cost to change it later |
|---|---|---|---|
| Brief | who, where, how long, may we spend | a sentence | the whole film |
| Beats | what is said and shown, in what order, for how long | a JSON edit | re-timing every shot |
| Animatic | framing, camera, pacing, text, transitions | seconds of re-render | regenerating paid clips |
| Upgrade | the look of a few hero shots | credits per shot | credits again |
| Conform | loudness, captions, delivery files | one ffmpeg pass | a rejected upload |

## Claims and confidence

- 🟢 Story reels and animatics (storyboards timed to scratch audio) are standard
  practice in feature animation before production; Pixar's public curriculum
  teaches it as the step that finds story problems early.
  Source: Pixar in a Box, "The art of storytelling" (Khan Academy).
- 🟢 Previsualization is an established VFX discipline for planning shots
  before shooting. Source: Okun & Zwerman (eds.), *The VES Handbook of Visual
  Effects*, previs chapter (Focal Press).
- 🟢 Claude Motion builds animations as code from text, charts, shapes and
  images, exports MP4, does not use a video model, and is a beta on Team and
  Enterprise plans. Source: Claude Help Center, "Get started with Claude Motion"
  (support.claude.com/en/articles/17454997, dated 2026-10-08).
- 🟢 HyperFrames (HeyGen, Apache-2.0) renders HTML/CSS to MP4 with headless
  Chrome and FFmpeg and ships agent skills. Source: github.com/heygen-com/hyperframes.
- 🟢 Remotion is free for individuals and companies of up to 3 people; larger
  companies need a paid license. Source: remotion.dev/docs/license/pricing.
- 🟢 Higgsfield's MCP `generate_video` accepts `get_cost: true` to return a
  price without submitting a job, takes start and end keyframe images on many
  models, and warns not to resubmit after a transport timeout. Source: the live
  MCP tool schema, read 2026-11-17. Tool names change; read them at run time.
- 🟡 Generation models still render on-screen text unreliably, which is why
  text, figures and logos stay as code layers over generated plates. This is
  widely observed; treat it as a design default, not a measured fact.
- 🟡 EU AI Act (Regulation (EU) 2024/1689) Article 50 sets transparency duties
  for AI-generated or manipulated video content ("deep fakes"), applying from
  2 August 2026. Read the article text for your case before relying on this
  summary. Source: eur-lex.europa.eu, Regulation (EU) 2024/1689.

## Why not generate everything

Generating every shot spends credits on drafts that review will reject, gives
no stable framing between shots, and puts text into a model that garbles it.
The animatic fixes all three: drafts are free, framing is locked in code, and
text never leaves code.
