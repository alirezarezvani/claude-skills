# Scene Design System

Reference material for demo video scene design — colors, typography, animation timing, voice options, and pacing.

## Color Language

| Color | Meaning | Use for |
|-------|---------|---------|
| `#c5d5ff` | Trust | Titles, logo |
| `#7c6af5` | Premium | Subtitles, badges |
| `#4ade80` | Success | "After" states |
| `#f28b82` | Problem | "Before" states |
| `#fbbf24` | Energy | Callouts |
| `#0d0e12` | Background | Always dark mode |

## Animation Timing

```
Element entrance:     0.5-0.8s  (cubic-bezier(0.16, 1, 0.3, 1))
Between elements:     0.2-0.4s  gap
Scene transition:     0.3-0.5s  crossfade
Hold after last anim: 1.0-2.0s
```

## Typography

```
Title:     48-72px, weight 800
Subtitle:  24-32px, weight 400, muted
Bullets:   18-22px, weight 600, pill background
Font:      Inter (Google Fonts)
```

## HTML Scene Layout (1920x1080)

```html
<body>
  <h1 class="title">...</h1>      <!-- Top 15% -->
  <div class="hero">...</div>     <!-- Middle 65% -->
  <div class="footer">...</div>   <!-- Bottom 20% -->
</body>
```

Background: dark with subtle purple-blue glow gradients. Screenshots: always `border-radius: 12px` with `box-shadow`. Easing: always `cubic-bezier(0.16, 1, 0.3, 1)` — never `ease` or `linear`.

## Voice Options (edge-tts)

| Voice | Best for |
|-------|----------|
| `andrew` | Product demos, launches |
| `jenny` | Tutorials, onboarding |
| `davis` | Enterprise, security |
| `emma` | Consumer products |

## Pacing Guide

| Duration | Max words | Fill |
|----------|-----------|------|
| 3-4s | 8-12 | ~70% |
| 5-6s | 15-22 | ~75% |
| 7-8s | 22-30 | ~80% |

## Atlas Cloud Scene Generation

Use this optional path only for conceptual B-roll that cannot be captured from the real
product. Product UI, results, dashboards, and workflows must use real screenshots.

### Preconditions

1. Confirm `ATLASCLOUD_API_KEY` is set without printing it.
2. Read the live model catalog at `https://api.atlascloud.ai/api/v1/models`.
3. Confirm the selected model is an enabled text-to-image model and read its live schema.
4. Keep the demo-video screenshot and HTML pipeline as the default.

`google/nano-banana-2-lite/text-to-image-developer` is a suitable low-latency example
when it is present in the live catalog. Its current text-to-image schema accepts a prompt
and supports a `16:9` aspect ratio.

### Submit Once

Create one request per approved conceptual scene:

```bash
curl --fail-with-body https://api.atlascloud.ai/api/v1/model/generateImage \
  -H "Authorization: Bearer $ATLASCLOUD_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: demo-video-skill/1.0" \
  -d '{
    "model": "google/nano-banana-2-lite/text-to-image-developer",
    "prompt": "<describe one conceptual scene; do not invent product UI>",
    "aspect_ratio": "16:9",
    "resolution": "1k"
  }'
```

Do not automatically retry this POST. Save the returned prediction ID immediately. If the
request fails, use the HTML scene fallback instead of spending on another generation.

### Poll and Save

Poll only the returned prediction with bounded backoff:

```bash
curl --fail-with-body \
  -H "Authorization: Bearer $ATLASCLOUD_API_KEY" \
  -H "User-Agent: demo-video-skill/1.0" \
  "https://api.atlascloud.ai/api/v1/model/prediction/<prediction-id>"
```

Stop on `completed` or `failed`, and stop after the agreed timeout. Download the first
completed output into `demo-output/scenes/` and inspect it before compositing. Reject any
asset that resembles fabricated product UI, contains broken text, or conflicts with the
real product branding.

Record each generated asset in `demo-output/generated-assets.json`:

```json
{
  "scene": 3,
  "model": "google/nano-banana-2-lite/text-to-image-developer",
  "prediction_id": "<prediction-id>",
  "prompt": "<exact prompt>",
  "output": "scenes/scene-03-broll.png"
}
```
