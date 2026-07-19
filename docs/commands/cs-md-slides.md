---
title: "/cs-md-slides — Slash Command for AI Coding Agents"
description: "Convert a markdown deck (slides separated by --- HR boundaries or by # H1 headings, with optional <!-- notes: ... --> presenter notes blocks) into a. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-md-slides

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/markdown-html/commands/cs-md-slides.md">Source</a></span>
</div>


Convert the markdown deck at **$ARGUMENTS** into a single-file interactive HTML presentation.

## Pre-flight gates (refuse, never override)

1. **Input < 100 lines** → refuse (markdown wins below Shihipar's threshold).
2. **Design-system not onboarded** → refuse, surface `/cs:design-system`.
3. **No clear slide boundaries** (auto mode: need ≥ 3 HR or ≥ 5 H1) → refuse, route to md-document.
4. **1-slide deck** → refuse (it's a poster, not a deck).
5. **`--strict-notes` with < 50% notes coverage** → refuse.
6. **Output directory unwritable** → refuse, ask user for `--out`.

## Pipeline

```bash
# 1. Resolve output path (doctype=slides → deck- prefix)
python3 markdown-html/skills/markdown-html-orchestrator/scripts/output_path_resolver.py \
    --input "<path>.md" --doctype slides

# 2. Split slides on --- HR or H1 (auto-detect)
python3 markdown-html/skills/md-slides/scripts/slide_splitter.py \
    --input "<path>.md" --boundary auto --output /tmp/slides.json

# 3. Extract <!-- notes: ... --> blocks per slide
python3 markdown-html/skills/md-slides/scripts/presenter_notes_parser.py \
    --slides /tmp/slides.json --output /tmp/deck.json

# 4. Render single-file HTML deck
python3 markdown-html/skills/md-slides/scripts/deck_html_renderer.py \
    --slides /tmp/deck.json --title "<deck title>" \
    --output <resolved-out>.html
```

## What ships in the HTML

- **All slides as `<section class="slide">`** with one visible at a time (CSS-controlled, no JS-required content)
- **Keyboard navigation**:
  - `→` / `Space` / `PgDn` → next slide
  - `←` / `PgUp` → previous slide
  - `Home` / `End` → first / last slide
  - `P` → toggle presenter mode
  - `Esc` → exit presenter mode
- **Presenter mode** — split view: current slide (60% width) + panel (40% width with clock + speaker notes + next-slide preview)
- **URL-hash deep linking** — `#3` jumps to slide 3; back/forward walks slides; share `deck.html#5` to land on slide 5
- **Progress bar** at top (3px); slide counter in bottom-right
- **Print-to-PDF** via browser's native print dialog: `@media print` makes each slide one page (`Cmd+P` / `Ctrl+P`)
- **`prefers-reduced-motion`** honored
- **12 brand CSS tokens** from design-system; design_style affects layout density

## Hard rules

- Output is one `.html` file. No multi-file output.
- External CDN: `fonts.googleapis.com` always; `cdn.jsdelivr.net` (Prism) only when `--syntax` is passed.
- No JS framework runtime. Vanilla JS + keyboard event handlers.
- Re-running on the same input writes `deck-{slug}-2.html` etc.

## Useful flags

- `--boundary {auto,hr,h1}` — slide boundary mode (default: auto)
- `--title "My Talk"` — sets the `<title>` and tab name
- `--syntax` — enable Prism.js CDN for code blocks (off by default; decks rarely need it)
- `--strict-notes` — refuse if < 50% of slides have presenter notes (use when presenter mode is essential)

## Output

Returns: slide count, notes coverage %, output path, design style applied, top features used, one forcing question.

## References

See `markdown-html/skills/md-slides/references/`:
- `presentation_ux.md` — Atkinson + Reynolds + Tufte + NN/g + Weinschenk + Marp/reveal.js/Big convergence
- `keyboard_nav_patterns.md` — reveal.js / Big / Spectacle keymap + WCAG 2.1.1 + 2.4.3 + MDN KeyboardEvent
- `single_file_deck_conventions.md` — Big + Marp + Pandoc + WCAG 2.3.3 + @media print
