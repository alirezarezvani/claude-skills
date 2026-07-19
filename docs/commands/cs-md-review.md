---
title: "/cs-md-review — Slash Command for AI Coding Agents"
description: "Convert a markdown PR writeup or code review (with ```diff blocks and > [!BLOCKER]/[!MAJOR]/[!MINOR]/[!NIT] severity callouts) into a single-file. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-md-review

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/markdown-html/commands/cs-md-review.md">Source</a></span>
</div>


Convert the review markdown at **$ARGUMENTS** into a single-file 2-column HTML review.

## Pre-flight gates (refuse, never override)

1. **Input < 100 lines** → refuse (markdown wins below Shihipar's threshold).
2. **Design-system not onboarded** → refuse, surface `/cs:design-system`.
3. **`--reviewer` missing** → refuse (a code review must name a human reviewer).
4. **No diff hunks present** → refuse, route to `md-document` instead.
5. **Output directory unwritable** → refuse, ask user for alternate via `--out`.

## Pipeline

```bash
# 1. Resolve output path (uses doctype=review → review- prefix)
python3 markdown-html/skills/markdown-html-orchestrator/scripts/output_path_resolver.py \
    --input "<path>.md" --doctype review

# 2. Parse diff hunks
python3 markdown-html/skills/md-review/scripts/diff_parser.py \
    --input "<path>.md" --output /tmp/hunks.json

# 3. Extract severity-tagged annotations, attached to nearest hunk
python3 markdown-html/skills/md-review/scripts/annotation_extractor.py \
    --input "<path>.md" --diff-blocks /tmp/hunks.json --output /tmp/annotations.json

# 4. Render — --reviewer is mandatory
python3 markdown-html/skills/md-review/scripts/review_html_renderer.py \
    --diff-blocks /tmp/hunks.json --annotations /tmp/annotations.json \
    --reviewer "<reviewer-name>" --title "<PR title>" \
    --output <resolved-out>.html
```

## What ships in the HTML

- **Top jump-nav** — every finding with severity badge (color + icon + aria-label) + 80-char preview + jump link; counts in the heading ("3 BLOCKER · 2 MAJOR · 1 NIT")
- **2-col hunk rows** — unified diff on left (line numbers both sides, +/− marks, addition/deletion bg tints from design-system tokens), annotation cards on right
- **Severity coding** — BLOCKER = computed danger color (accent rotated 120° toward red), MAJOR = `--md-warn`, MINOR = `--md-link`, NIT = `--md-text-muted`. Every badge has icon (■ / ▲ / ● / ◦) + aria-label per WCAG 1.4.1
- **Approval bar** — if LGTM markers and no findings, success-tinted bar
- **General-comments section** — for unanchored annotations
- **Reviewer footer** — "Reviewer: \<name\>" (mandatory)
- **Responsive** — 2-col collapses to stacked under 900px

## Hard rules

- Output is one `.html` file. No external CSS/JS. Only external is Google Fonts CSS (no Prism — diff colors conflict with syntax highlighting).
- No JS framework runtime. The page is fully static; jump-nav links are plain anchors.
- Severity is never color-only (WCAG 1.4.1).
- Re-running on the same input writes `review-{slug}-2.html` etc.

## Custom severity convention

```bash
--severity-convention "critical,important,suggestion,nit"
```

Swaps tier names; position 0 is most severe. Default: `BLOCKER,MAJOR,MINOR,NIT` (Google *Code Review Developer Guide*).

## Output

Returns: hunk count, annotation count, severity breakdown, output path, reviewer name, one forcing question.

## References

See `markdown-html/skills/md-review/references/`:
- `diff_rendering_canon.md` — POSIX diff format + GitHub/GitLab conventions + difftastic + SWE at Google
- `severity_coding.md` — WCAG 1.4.1 + Google review taxonomy + Don Norman signifier
- `pr_annotation_ux.md` — Convergent 2-col UX from GitHub/GitLab/Reviewable/CodeStream
