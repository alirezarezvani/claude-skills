# Markdown → HTML — Domain Guide

This file provides domain-specific guidance for skills in `markdown-html/`.

## Purpose

The markdown-html domain converts long markdown files (the actual artifacts produced inside a Claude project — specs, reports, RFCs, PR writeups, slide outlines) into world-class, single-file, lightly-interactive HTML. Inspired by Thariq Shihipar's argument (Medium, 2026): markdown collapses past ~100 lines because it lacks visual machinery for density and lateral navigation; HTML restores both.

It is **not** an interactive prompt-tuning playground (`/playground` plugin owns that lane), **not** a landing-page generator (`marketing/landing/`), **not** a session-handoff brief generator (`engineering/handoff/` + `productivity/handoff/`), and **not** a static-site generator (single-file artifacts, not site indices).

## Skills (v2.10.3 — domain complete)

| Skill | Purpose | `context: fork`? | Status |
|---|---|---|---|
| `markdown-html-orchestrator` | Domain orchestrator — classifies doctype, gates on threshold + onboarding, routes to converter | YES | ✓ live |
| `design-system` | One-time onboarding wizard + WCAG-AA-validated brand palette (12 CSS custom properties) + shared config | NO | ✓ live |
| `md-document` | Long-form converter: sticky TOC, collapsibles, search, code-copy, scrollspy | NO | ✓ live |
| `md-review` | Code-review converter: 2-col diff + severity-tagged margin annotations + jump-nav | NO | ✓ live |
| `md-slides` | Slide-deck converter: arrow-key nav + presenter mode + print-to-PDF | NO | ✓ live |

All three converters are shipped. Routing always targets the converter skill's scripts — never hand-render HTML inline.

## Hard rules (domain-specific)

1. **Refuses input < 100 lines.** Markdown still wins below the threshold (Shihipar). Every converter (and the orchestrator) prints the line count and a "keep as markdown" recommendation.
2. **Refuses without design-system onboarding.** The orchestrator's `route_explainer.py` checks `config_loader.setup_completed()`. If false, refuse and surface onboarding (`python3 markdown-html/skills/design-system/scripts/onboard.py`).
3. **WCAG AA enforced.** `brand_palette_validator.py` rejects color combinations whose body-text contrast falls below 4.5:1 on bg. Link contrast is iteratively walked to 4.5:1 by adjusting luminance.
4. **Single-file HTML output.** All CSS and JS inline. The only permitted external CDN entries are Google Fonts CSS and Prism.js. No bundler, no build step, no JS framework runtimes (vanilla JS + IntersectionObserver only).
5. **Never silently chain converters.** "Convert this markdown AND make slides from it AND a code review" is three operations. Pick one, finish, ask before chaining.
6. **Stdlib-only Python.** Deterministic logic, no LLM calls in scripts.
7. **Customization in use, not decoration.** Every converter MUST render differently when the user changes `design_style`, `brand.primary`, `code_theme`, or `toc.behavior`. If a token doesn't change behavior, it doesn't belong in the schema.
8. **Onboarding-first.** The orchestrator surfaces onboarding the moment it detects a missing `setup_completed_at`. Don't render with placeholder defaults silently.

## Build pattern

Path-B contract per skill: SKILL.md + 3 stdlib scripts + 3 references (each citing 5-7 sources) + (optional) 1 asset template. The orchestrator skill ships `context: fork` in its frontmatter. The `design-system` skill is the shared brand owner — every converter imports its `config_loader.py` via `sys.path.insert(0, .../design-system/scripts)`.

Each SKILL.md ships a "Forcing-question library" section (cited-canon grilling, one question at a time) — same discipline as `research-ops`, `commercial`, and `business-operations`.

## Agent + command pattern

- `cs-markdown-html-orchestrator` — density-first markdown-to-HTML converter. Voice: "What decision does this HTML drive — is the reader skimming, deciding, or presenting?"
- `/cs:markdown-html <path>.md` — top-level router (classifier + route + recommend)
- `/cs:grill-markdown-html <path>.md` — Matt-Pocock-style 5-question grill before conversion
- `/cs:design-system` — surface the onboarding wizard

Per-sub-skill commands (all live):
- `/cs:md-document`, `/cs:md-review`, `/cs:md-slides`

## Anti-patterns (domain-level)

- ❌ Converting markdown < 100 lines — markdown still wins. Refuse + cite Shihipar.
- ❌ Skipping onboarding because "the user wants it done now." Surface onboarding — it's 60 seconds.
- ❌ Multi-file output (separate CSS / JS / image folders). Single file or nothing.
- ❌ External JS framework runtimes (React, Vue, Svelte, Alpine). Vanilla JS + IntersectionObserver only.
- ❌ Silently overwriting existing output files. `output_path_resolver.py` suffixes `-2`, `-3`, … by default.
- ❌ Setting `MARKDOWN_HTML_NO_CONFIG=1` silently for an interactive user.
- ❌ Decorative tokens — every token must change at least one converter's output.
- ❌ Inventing brand colors when the user hasn't onboarded.
- ❌ A skill that overlaps Anthropic's official Playground plugin (sliders/knobs/prompt-copy-back).
- ❌ A skill that overlaps `marketing/landing/` (landing-page generation from scratch).

## Customization pipeline

1. User runs `python3 markdown-html/skills/design-system/scripts/onboard.py`.
2. Wizard validates brand colors via `brand_palette_validator.py`, derives 12-token palette.
3. Result written to `~/.config/markdown-html/design-system.json` (or `./.markdown-html/design-system.json` with `--scope project`).
4. Every converter sub-skill imports `config_loader.py` and calls `load_config()` to read project > global > defaults.
5. Each converter's renderer emits a single `<style>` block with `:root { --md-bg: ...; }` for all 12 tokens, then references those variables throughout the CSS.
6. Result: change a single field via `--set brand.primary=#FF6B35` → next conversion re-renders with the new brand.

## References

- Spec: Thariq Shihipar — *Claude Code HTML output: Why Markdown Lost and How to Switch* (Medium, 2026)
- Forking pattern source: `research-ops/skills/research-ops-skills/SKILL.md` (`context: fork`, two-signal routing)
- Onboarding pattern source: `research-ops/skills/clinical-research/scripts/onboard.py` + `config_loader.py`
- Brand palette math source: `marketing/landing/skills/landing/scripts/brand_palette_validator.py`
- Matt Pocock grill-with-docs: `engineering/grill-with-docs`
- Single-file HTML discipline source: `marketing/landing/skills/landing/SKILL.md`
