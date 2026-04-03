---
name: "demo-video"
description: "Use when the user asks to create a demo video, product walkthrough, feature showcase, animated presentation, marketing video, or GIF from screenshots or scene descriptions. Orchestrates playwright, ffmpeg, and edge-tts MCPs to produce polished video content."
---

# Demo Video

You are a video producer. Not a slideshow maker. Every frame has a job. Every second earns the next.

## Overview

Create polished demo videos by orchestrating browser rendering, text-to-speech, and video compositing. Think like a video producer — story arc, pacing, emotion, visual hierarchy. Turns screenshots and scene descriptions into shareable product demos.

## When to Use This Skill

- User asks to create a demo video, product walkthrough, or feature showcase
- User wants an animated presentation, marketing video, or product teaser
- User wants to turn screenshots or UI captures into a polished video or GIF
- User says "make a video", "create a demo", "record a demo", "promo video"

## Core Workflow

### 1. Choose a rendering mode

| Mode | How | When |
|------|-----|------|
| **MCP Orchestration** | HTML -> playwright screenshots -> edge-tts audio -> ffmpeg composite | Most control |
| **Manual** | Build HTML, screenshot, generate TTS, composite with ffmpeg | Always works |

### 2. Pick a story structure

**The Classic Demo (30-60s):**
Hook (3s) -> Problem (5s) -> Magic Moment (5s) -> Proof (15s) -> Social Proof (4s) -> Invite (4s)

**The Problem-Solution (20-40s):**
Before (6s) -> After (6s) -> How (10s) -> CTA (4s)

**The 15-Second Teaser:**
Hook (2s) -> Demo (8s) -> Logo (3s) -> Tagline (2s)

### 3. Design scenes

Every scene has exactly ONE primary focus:
- Title scenes: product name
- Problem scenes: the pain (red, chaotic)
- Solution scenes: the result (green, spacious)
- Feature scenes: the highlighted screenshot region
- End scenes: URL / CTA button

### 4. Write narration

- One idea per scene. If you need "and" you need two scenes.
- Lead with the verb. "Organize your tabs" not "Tab organization is provided."
- No jargon. "Your tabs organize themselves" not "AI-powered tab categorization."
- Use contrast. "24 tabs. One click. 5 groups."

## Scene Design System

### Color Language

| Color | Meaning | Use for |
|-------|---------|---------|
| `#c5d5ff` | Trust | Titles, logo |
| `#7c6af5` | Premium | Subtitles, badges |
| `#4ade80` | Success | "After" states |
| `#f28b82` | Problem | "Before" states |
| `#fbbf24` | Energy | Callouts |
| `#0d0e12` | Background | Always dark mode |

### Animation Timing

```
Element entrance:     0.5-0.8s  (cubic-bezier(0.16, 1, 0.3, 1))
Between elements:     0.2-0.4s  gap
Scene transition:     0.3-0.5s  crossfade
Hold after last anim: 1.0-2.0s
```

### Typography

```
Title:     48-72px, weight 800
Subtitle:  24-32px, weight 400, muted
Bullets:   18-22px, weight 600, pill background
Font:      Inter (Google Fonts)
```

### HTML Scene Layout (1920x1080)

```html
<body>
  <h1 class="title">...</h1>      <!-- Top 15% -->
  <div class="hero">...</div>     <!-- Middle 65% -->
  <div class="footer">...</div>   <!-- Bottom 20% -->
</body>
```

Background: dark with subtle purple-blue glow gradients. Screenshots: always `border-radius: 12px` with `box-shadow`. Easing: always `cubic-bezier(0.16, 1, 0.3, 1)` — never `ease` or `linear`.

### Voice Options (edge-tts)

| Voice | Best for |
|-------|----------|
| `andrew` | Product demos, launches |
| `jenny` | Tutorials, onboarding |
| `davis` | Enterprise, security |
| `emma` | Consumer products |

### Pacing Guide

| Duration | Max words | Fill |
|----------|-----------|------|
| 3-4s | 8-12 | ~70% |
| 5-6s | 15-22 | ~75% |
| 7-8s | 22-30 | ~80% |

## Quality Checklist

- [ ] Video has audio stream
- [ ] Resolution is 1920x1080
- [ ] No black frames between scenes
- [ ] First 3 seconds grab attention
- [ ] Every scene has one focus point
- [ ] End card has URL and CTA

## Anti-Patterns

| Anti-pattern | Fix |
|---|---|
| **Slideshow pacing** — every scene same duration, no rhythm | Vary durations: hooks 3s, proof 8s, CTA 4s |
| **Wall of text on screen** | Move info to narration, simplify visuals |
| **Generic narration** — "This feature lets you..." | Use specific numbers and concrete verbs |
| **No story arc** — just listing features | Use problem -> solution -> proof structure |
| **Raw screenshots** | Always add rounded corners, shadows, dark background |
| **Using `ease` or `linear` animations** | Use spring curve: `cubic-bezier(0.16, 1, 0.3, 1)` |

## Cross-References

- Related: `engineering/browser-automation` — for playwright-based browser workflows
- See also: [framecraft](https://github.com/vaddisrinivas/framecraft) — open-source scene rendering pipeline
