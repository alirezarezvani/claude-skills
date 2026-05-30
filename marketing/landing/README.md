# landing

Premium single-file HTML landing page generator. Outputs one polished `.html` file with GSAP 3D animations, scroll-triggered reveals, and mouse-parallax depth — all CSS inline, all JS inline, only externals are Google Fonts + GSAP via CDN.

## Important: distinct from `product-team/skills/landing-page-generator/`

This is **NOT** the same skill as the existing `landing-page-generator` in `product-team/`. They serve different needs:

| Skill | Output format | Optimization target | Animation approach | When to use |
|---|---|---|---|---|
| **`marketing/landing/`** (this skill) | Single self-contained `.html` file | **Visual premium / one-pager** | GSAP 3D + mouse parallax + scroll-trigger | Launch page, product showcase, brand site where the page IS the experience |
| **`product-team/skills/landing-page-generator/`** | Next.js TSX components + Tailwind | **Conversion / lead-gen** | Static, copy-framework-driven (PAS / AIDA / BAB) | Lead capture, A/B test variants, campaign pages where conversion rate is the goal |

If you want the prospect to **convert** → use `landing-page-generator`.
If you want the prospect to **be impressed** → use `landing`.

Both are valid; they sit at different points on the visual-premium / conversion-optimization axis.

## What this skill does

Run via `/cs:landing` or trigger phrases like "create a landing page" / "build a landing page".

The skill walks **3–4 forcing intake questions** (one at a time, dependency-ordered):

1. **Product / service** — name + 1–2 sentence elevator pitch (refuses vague answers)
2. **Audience register** — technical / business / consumer / internal (forcing choice)
3. **Brand overrides** — default dark navy + teal, OR provide primary HEX + accent HEX + optional bg HEX (algorithmic derivation if only primary given)
4. **Tone** — professional / playful / authoritative / minimal (forcing choice)

Then generates a single `.html` file with three sections:

- **Hero** — 100vh, animated entrance via GSAP timeline, depth layers behind H1, mouse parallax
- **Features** — 3-column grid (responsive: 2-col at 900px, 1-col at 580px), SVG icons, scroll-triggered card reveals
- **Closing CTA** — ambient radial-gradient glow behind button, large closing headline

Output path: `${OUTPUT_DIR}/<product-name-kebab>.html` (default `${OUTPUT_DIR}=./landing-pages/`).

## Plugin layout

```
marketing/landing/
├── .claude-plugin/plugin.json
├── README.md
├── agents/cs-landing.md             ← landing-generation persona, FOUC-prevention enforcer
├── commands/cs-landing.md           ← /cs:landing
└── skills/landing/
    ├── SKILL.md                     ← Path-B converted from megaprompt 04
    ├── references/
    │   ├── brand_system_design.md   ← color theory + override patterns (7+ sources)
    │   ├── gsap_animation_patterns.md  ← entrance + scroll-trigger + parallax + CSS floats (7+ sources)
    │   └── single_file_html_discipline.md  ← why inline + CDN-only externals (7+ sources)
    └── scripts/
        ├── brand_palette_validator.py  ← stdlib: HEX validation + WCAG contrast + derived palette
        ├── kebab_slug_generator.py     ← stdlib: product-name → kebab slug + duplicate detection
        └── html_validator.py           ← stdlib: post-generation structural check
```

## Quick start

```bash
# Validate a brand override before generation
python skills/landing/scripts/brand_palette_validator.py \
  --primary "#FF6B35" --accent "#2EC4B6" --bg "#011627"

# Generate output filename
python skills/landing/scripts/kebab_slug_generator.py \
  --product "Quill AI" --output-dir ./landing-pages

# Validate generated HTML structurally
python skills/landing/scripts/html_validator.py --file ./landing-pages/quill-ai.html
```

## Source spec

[`megaprompts/04-landing-megaprompt.md`](../../megaprompts/04-landing-megaprompt.md) (PR #657). The megaprompt is canonical; this plugin is the working implementation. Drift between the two is a bug — re-grill with `/cs:grill-with-docs` if they diverge.

## License

MIT.
