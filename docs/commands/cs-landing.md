---
title: "/cs-landing — Slash Command for AI Coding Agents"
description: "/cs:landing <product-or-brief> — Generate a premium single-file HTML landing page with GSAP 3D animations, scroll-triggered reveals, and. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-landing

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/marketing/landing/commands/cs-landing.md">Source</a></span>
</div>


**Command:** `/cs:landing <product-or-brief>`

The `cs-landing` persona generates one polished, self-contained `.html` landing page with GSAP animations, mouse parallax, and 3D CSS effects.

## When to Run

- Launch pages where the page IS the experience (visual-premium one-pagers)
- Product showcases with motion design
- Brand sites where conversion rate isn't the primary metric — impression is

## When NOT to Run (use `landing-page-generator` instead)

If you need **conversion-optimized lead-gen** with copy frameworks (PAS / AIDA / BAB), Next.js TSX components, multiple section variants for A/B testing — use `product-team/skills/landing-page-generator/` instead. That's a different skill optimizing for different outcomes.

| Need | Skill |
|---|---|
| Visual premium one-pager | **`/cs:landing`** (this command) |
| Conversion-optimized lead-gen | `landing-page-generator` |

## Trigger Phrases (auto-invoke without /cs:)

- "create a landing page"
- "build a landing page"
- "make a landing page for X"
- "I need a web page for Y"
- "promotional page"
- "product page"
- "one-pager"
- "web presence"
- "sales page"

**Note:** these trigger phrases may match either this skill OR `landing-page-generator`. If both are installed, Claude picks based on the conversation context (premium-visual hints → this skill; conversion / lead-gen / A/B-test hints → the other).

## Forcing Intake (3–4 Questions, One at a Time)

| Q | Asks | Default if forcing-choice |
|---|---|---|
| Q1 | Product / service: name + 1–2 sentence elevator pitch | refuses vague answers ("app for productivity" gets pushed back once) |
| Q2 | Audience register: technical / business / consumer / internal | forcing choice |
| Q3 | Brand overrides: primary HEX + accent HEX + optional bg HEX, OR "default" | default = dark navy + teal |
| Q4 | Tone: professional / playful / authoritative / minimal | forcing choice (recommended: professional for B2B, playful for consumer, minimal for design-led) |

**Stop condition:** Max 4 questions. No follow-up during generation.

## What You Get

A single `.html` file at `${OUTPUT_DIR}/<product-kebab>.html` (default `./landing-pages/`) with:

- **Hero** — 100vh, animated H1 entrance via GSAP timeline, scroll-down indicator, mouse-parallax depth layers
- **Features** — 3-column grid (responsive 2-col at 900px, 1-col at 580px), SVG icons, scroll-triggered card reveals with `rotateX` lift
- **Closing CTA** — large closing headline + ambient radial-gradient glow behind button

All CSS inline. All JS inline. Externals: Google Fonts (Inter) + GSAP via CDN only.

## Discipline

- **One intake question per turn.** Never bundle.
- **Refuse vague Q1 once.** Push back; deliver with caveat if user won't sharpen.
- **No FOUC.** Every animated element gets `gsap.set()` initial state.
- **Inline-only.** All CSS + JS in the file. No external `.css` / `.js` references.
- **Responsive.** Breakpoints at 900px + 580px.
- **No hardcoded paths.** `${OUTPUT_DIR}` variable.
- **Single-pass write.** No outline → draft → polish cycle.

## Workflow

```bash
# 1. Intake (Q1-Q4 one at a time)

# 2. If brand override provided, validate:
python ../skills/landing/scripts/brand_palette_validator.py \
  --primary "#FF6B35" --accent "#2EC4B6" --bg "#011627"

# 3. Generate output filename
python ../skills/landing/scripts/kebab_slug_generator.py \
  --product "<product name from Q1>" --output-dir ./landing-pages

# 4. Write the .html file in one pass (Hero + Features + Closing CTA + GSAP + mouse parallax + ScrollTrigger + CSS floats)

# 5. Validate structure
python ../skills/landing/scripts/html_validator.py \
  --file ./landing-pages/<slug>.html

# 6. Deliver:
#    CLI → file path
#    Web → HTML artifact
```

## Stop Conditions

- All 4 Qs answered + HTML generated + validator PASS → done
- User says "skip intake" → use defaults for any unanswered Q (default brand, professional tone, audience inferred from elevator pitch)
- Validator FAIL → regenerate the failing sections in one targeted pass; do NOT abandon the file

## Anti-Patterns Rejected

- Hardcoded absolute paths in output directory
- Single brand palette without override documentation
- Outlining before writing — write in one pass
- External CSS or JS files (must be inline)
- Skipping `gsap.set()` initial states (causes FOUC)
- More than 6 features in default grid (becomes unscannable)
- Brand-specific content references in the skill itself
- Bundling intake questions

## Related

- Agent: [`cs-landing`](https://github.com/alirezarezvani/claude-skills/tree/main/marketing/landing/agents/cs-landing.md)
- Skill: [`landing`](https://github.com/alirezarezvani/claude-skills/tree/main/marketing/landing/skills/landing/SKILL.md)
- Source spec: [`megaprompts/04-landing-megaprompt.md`](https://github.com/alirezarezvani/claude-skills/tree/main/megaprompts/04-landing-megaprompt.md)
- Sibling (different optimization): `product-team/skills/landing-page-generator/`
- Adjacent v2 commands: `/cs:capture`, `/cs:pulse`, `/cs:inbox-setup`, `/cs:inbox-triage`

---

**Version:** 1.0.0
**Source:** Path-B direct conversion of `megaprompts/04-landing-megaprompt.md`
