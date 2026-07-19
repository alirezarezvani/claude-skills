---
title: "/cs-md-document — Slash Command for AI Coding Agents"
description: "Convert long-form markdown (specs, RFCs, reports, plans, explainers) into a single-file interactive HTML document. Runs the md-document pipeline. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-md-document

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/markdown-html/commands/cs-md-document.md">Source</a></span>
</div>


Convert the markdown at **$ARGUMENTS** into a single-file interactive HTML document.

## Pre-flight gates (refuse, never override)

1. **Input < 100 lines** → refuse (markdown wins below the threshold per Shihipar). `wc -l <path>` to confirm.
2. **Design-system not onboarded** → refuse, surface `/cs:design-system`.
3. **Output directory unwritable** → refuse, ask user for an alternate via `--out`.

## Pipeline

```bash
# 1. Classify (if not already routed by orchestrator)
python3 markdown-html/skills/markdown-html-orchestrator/scripts/doctype_classifier.py \
    --input "<path>.md" --output json \
  | python3 markdown-html/skills/markdown-html-orchestrator/scripts/route_explainer.py

# 2. Resolve the output path
python3 markdown-html/skills/markdown-html-orchestrator/scripts/output_path_resolver.py \
    --input "<path>.md" --doctype document

# 3. Parse → render → inject
python3 markdown-html/skills/md-document/scripts/markdown_parser.py \
    --input "<path>.md" --output /tmp/sections.json
python3 markdown-html/skills/md-document/scripts/html_renderer.py \
    --sections /tmp/sections.json --output <resolved-out>.html
python3 markdown-html/skills/md-document/scripts/interactivity_injector.py \
    --file <resolved-out>.html \
    --features search,copycode,smoothscroll,scrollspy
```

## What ships in the HTML

- Sticky-sidebar TOC (default; configurable via `toc.behavior` in design-system)
- Scrollspy: `aria-current="location"` on the TOC entry for the section in view
- Search bar (Esc clears): filters which H2 sections are visible
- Code-copy buttons on every `<pre>` (vanilla `navigator.clipboard` with `execCommand` fallback)
- Smooth-scroll on TOC link clicks
- Prism.js syntax highlighting (autoloader fetches only the languages this doc uses)
- 12 brand CSS custom properties from the design-system's `derived_palette`
- `@media (prefers-reduced-motion: reduce)` honored
- Print-friendly via the browser's native print stylesheet (no `@page` overrides needed for documents)

## Hard rules

- Output is one `.html` file. No multi-file output, no extracted CSS/JS, no asset folders.
- External CDN: `fonts.googleapis.com` + `cdn.jsdelivr.net` (Prism). Nothing else.
- No JS framework runtime. Vanilla JS + IntersectionObserver only.
- Re-running on the same input writes `doc-{slug}-2.html` etc. (collision suffix).

## Output

Returns: input lines, output path, design style applied, top 3 features used, one forcing question.

## References

See `markdown-html/skills/md-document/references/`:
- `information_density_patterns.md` — Shihipar + Tufte + Wattenberger
- `toc_and_nav_ux.md` — NN/g + WCAG + ARIA
- `single_file_html_discipline.md` — Single-file artifact rationale
