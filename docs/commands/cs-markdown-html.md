---
title: "/cs-markdown-html — Slash Command for AI Coding Agents"
description: "Top-level markdown-to-HTML router. Classifies the input markdown (document / review / slides), checks the design-system onboarding gate + 100-line. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-markdown-html

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/markdown-html/commands/cs-markdown-html.md">Source</a></span>
</div>


Route this conversion through the `markdown-html-orchestrator` skill:

**$ARGUMENTS**

## Pre-flight gates (refuse and surface, never override)

1. **Input < 100 lines.** Markdown still wins below the threshold (Shihipar). Refuse with the line count + recommendation to keep as markdown.
2. **Design-system not onboarded.** Surface `python3 markdown-html/skills/design-system/scripts/onboard.py` and re-prompt after.
3. **Output directory unwritable.** Refuse; let the user fix the path or re-onboard.

## Routing (deterministic, two-signal threshold)

| Signal class | Filename hints | Content signals | Sub-skill |
|---|---|---|---|
| DOCUMENT | `report.md`, `spec.md`, `rfc-*.md`, `*-doc.md`, `*-analysis.md`, `*-explainer.md` | `## Table of Contents`, `^# `, `^## `, table rows, GFM callouts | `md-document` |
| REVIEW | `review.md`, `*-pr-*.md`, `*.diff.md`, `code-review*.md` | ` ```diff `, `^[-+]{3} `, `^@@`, `> [!BLOCKER]/[!MAJOR]/[!MINOR]/[!NIT]`, `LGTM`/`nit:`/`blocker:` | `md-review` |
| SLIDES | `deck.md`, `slides.md`, `*-talk.md`, `presentation*.md` | `^---$` ≥ 3, `<!-- notes:`, H1 cadence ≥ 5 with median gap ≤ 12 lines | `md-slides` |

Pipeline:

```bash
python3 markdown-html/skills/markdown-html-orchestrator/scripts/doctype_classifier.py \
    --input "$ARGUMENTS" --output json \
  | python3 markdown-html/skills/markdown-html-orchestrator/scripts/route_explainer.py

python3 markdown-html/skills/markdown-html-orchestrator/scripts/output_path_resolver.py \
    --input "$ARGUMENTS" --doctype <verdict>
```

1. Silent-route only when winner ≥ 3 AND (runner-up = 0 OR winner ≥ 2× runner-up).
2. Single signal or tie → one clarifying question with a recommended answer.
3. No signals → ask which lane, recommend `md-document` as the safe default.

## Output (≤ 100-word digest)

- Input lines + doctype
- Output path (resolved by `output_path_resolver.py`)
- Design style + brand primary applied (from `config_loader.py`)
- Top 3 features used (sticky TOC, scrollspy, code-copy, severity badges, presenter mode, etc.)
- One forcing question for the user (cite Shihipar / WCAG / Lupton / Tufte)

## Hard rules

- Never silently chain two converters. Pick one, finish, ask before chaining.
- Never override a `REFUSE` from `route_explainer.py`.
- Never invent brand colors when the user hasn't onboarded. Surface onboarding.
- Output is single-file HTML. External CDN is limited to Google Fonts + Prism.js.

## Status

All five skills are live (orchestrator + `design-system` + the three converters). This command runs the classifier + design-system gate, then hands the conversion to the routed converter sub-skill (`/cs:md-document`, `/cs:md-review`, or `/cs:md-slides`). Never render HTML inline — the converter scripts own the rendering.
