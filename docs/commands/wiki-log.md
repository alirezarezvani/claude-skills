---
title: "/wiki-log — Slash Command for AI Coding Agents"
description: "Show recent entries from the LLM Wiki log (wiki/log.md). Uses the standardized ## [YYYY-MM-DD] header format so grep + tail works. Usage /wiki-log. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /wiki-log

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/commands/wiki-log.md">Source</a></span>
</div>


Show recent entries from `wiki/log.md`. Every LLM operation on the wiki leaves a standardized entry:

```
## [YYYY-MM-DD] <op> | <title>
<optional detail>
```

## Usage

```
/wiki-log                            # last 10 entries
/wiki-log --last 20
/wiki-log --op ingest --last 10      # only ingest entries
/wiki-log --op lint                  # recent lint passes
/wiki-log --since 2026-04-01
```

## What it does

Parses `wiki/log.md` and prints matching entries. No LLM involvement needed — this is essentially:

```bash
grep "^## \[" wiki/log.md | tail -N
```

…plus optional filters for op type and date range.

## Valid ops

- `ingest` — a source was read and integrated
- `query` — a question was answered (when filed back)
- `lint` — a health check ran
- `create` — a new page was created outside an ingest
- `update` — a page was updated outside an ingest
- `delete` — a page was removed
- `note` — freeform note (contradictions flagged, thesis revisions, etc.)

## Example output

```
## [2026-04-11] lint | weekly health check
3 contradictions, 12 orphans, 2 broken links. Fixed broken links; left contradictions for next session.

## [2026-04-10] ingest | Anthropic Monosemanticity
Added sources/monosemanticity.md. Updated concepts/sparse-autoencoder, concepts/polysemanticity, entities/anthropic.

## [2026-04-09] query | SAE vs probing
Filed back to comparisons/sae-vs-probing.md.
```

## Scripts

- Uses `grep` + `tail` directly on `wiki/log.md`. No dedicated script needed; that's the point of the standardized header format.

## Skill Reference

→ `engineering/llm-wiki/SKILL.md`
