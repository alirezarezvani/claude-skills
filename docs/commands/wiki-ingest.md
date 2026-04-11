---
title: "/wiki-ingest — Slash Command for AI Coding Agents"
description: "Ingest a source file from raw/ into the LLM Wiki — read, discuss, write summary page, update cross-references across 5-15 pages, regenerate index. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /wiki-ingest

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/commands/wiki-ingest.md">Source</a></span>
</div>


Ingest a new source into the LLM Wiki. This is the most-used command.

The flow: read the source → discuss TL;DR and key claims with you → write a source summary page → update every relevant entity and concept page → flag contradictions → update `index.md` → append to `log.md`.

A typical ingest touches **5-15 wiki pages**. You (the user) are in the loop: the ingestor proposes changes and waits for your confirmation before writing.

## Usage

```
/wiki-ingest <path>
/wiki-ingest raw/papers/monosemanticity.pdf
/wiki-ingest raw/articles/2026-04-01-interpretability-post.md
```

## What happens

1. **Prep** — runs `scripts/ingest_source.py` to get title, preview, and suggested summary path
2. **Read** — reads the source directly
3. **Discuss** — reports TL;DR, key claims, which pages will be touched, any contradictions
4. **Confirm** — waits for your go-ahead (or redirects)
5. **Write** — creates the source summary, updates 5-15 pages, flags contradictions
6. **Index** — runs `scripts/update_index.py` or edits `wiki/index.md` inline
7. **Log** — runs `scripts/append_log.py --op ingest --title "<title>"`
8. **Report** — bulleted wikilinks to every touched page

## Sub-agent

This command dispatches the `wiki-ingestor` sub-agent for the heavy lifting. See `agents/wiki-ingestor.md`.

## Scripts

- `engineering/llm-wiki/scripts/ingest_source.py` — source prep (metadata + preview)
- `engineering/llm-wiki/scripts/update_index.py` — regenerate index
- `engineering/llm-wiki/scripts/append_log.py` — log the ingest

## Rules

- The source must be inside the vault's `raw/` layer. If it isn't, the command will ask you to move it first.
- `raw/` is immutable — the ingestor reads only.
- If a summary page already exists, the ingestor enters **merge mode** and appends a re-ingest section.

## Skill Reference

→ `engineering/llm-wiki/SKILL.md`
→ `engineering/llm-wiki/references/ingest-workflow.md`
