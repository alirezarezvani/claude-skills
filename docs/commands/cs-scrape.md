---
title: "/cs-scrape — Slash Command for AI Coding Agents"
description: "Route, extract, and validate a scraping job (URL or local file) via the universal-scraping-architect skill — refuses to deliver unvalidated data.. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-scrape

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/engineering/universal-scraping-architect/commands/cs-scrape.md">Source</a></span>
</div>


Run a gated extraction pipeline for `$ARGUMENTS` using `skills/universal-scraping-architect/SKILL.md`.

## Pre-flight gates (stop if any fails)

1. **Target stated?** If `$ARGUMENTS` is empty, ask for the URL or file path plus the desired output format — do not guess.
2. **Live-site etiquette:** for URLs, check `robots.txt` and plan rate limits; refuse disallowed targets.
3. **Privacy:** if the target is a local/sensitive file, do not send it to an external API — force Mode 2 (local Python).
4. **Secrets:** Firecrawl key only via `os.getenv('FIRECRAWL_API_KEY')`; if a key appears inline anywhere, fix that first.

## Workflow

1. **Route** — state the mode and why (per the skill's routing rules):
   Mode 1 Firecrawl (public/JS-heavy URL, bulk crawl) · Mode 2 local Python (local files, private data, simple static HTML) · Mode 3 hybrid (Firecrawl extract + pandas clean).
2. **Budget** — estimate API quota / token limits before multi-page jobs; add checkpointing + pagination.
3. **Extract** — start from the matching runner template (run from the plugin root; `--sample` previews the summary shape offline):
   ```bash
   python3 skills/universal-scraping-architect/scripts/firecrawl_example.py --sample
   python3 skills/universal-scraping-architect/scripts/local_bs4_example.py --sample
   ```
4. **Validate (mandatory, exit-code gated):**
   ```bash
   python3 skills/universal-scraping-architect/scripts/validate_extraction.py extracted_output.json --json
   ```
   - exit 0 (`status: ok`) → continue
   - exit 1 (`warning` = empty output, `error` = malformed JSON) → fix and re-extract; **never deliver unvalidated data**

   Then check required fields and duplicates against the job spec.
5. **Deliver** — CSV (tabular) / JSON (nested) / Markdown (docs, chunked), per the user's requested format, with a summary of mode chosen, row counts, empty values, and the validation verdict.
