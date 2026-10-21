---
title: "/cs-spinning-up-deep-rl — Slash Command for AI Coding Agents"
description: "/cs-spinning-up-deep-rl [topic | framework | chNN] — query the knowledge base compiled from Spinning Up in Deep RL by Joshua Achiam (OpenAI). Use. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-spinning-up-deep-rl

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/engineering/spinning-up-deep-rl/commands/cs-spinning-up-deep-rl.md">Source</a></span>
</div>


**Command:** `/cs-spinning-up-deep-rl [topic | framework name | chNN]`

## When to run

- Applying a framework from this source to work in progress
- Looking up the author's exact formulation of a term
- Reading one chapter's compiled summary without opening the source
- Checking whether the source covers a question at all

## What it does

1. Loads `engineering/spinning-up-deep-rl/skills/spinning-up-deep-rl/SKILL.md` — Core Frameworks plus the Chapter and Topic indexes.
2. **No argument** → reports the core frameworks and the chapter index.
3. **A topic or framework name** → resolves it through the Topic Index and reads only the
   matching chapter file.
4. **`chNN`** → reads that chapter's summary directly.
5. Answers with the author's naming and cites the chapter.

## Boundary

This command answers from **one source** (20 chapters indexed). Anything it does not
cover gets said out loud rather than filled in — and hands-on work in your codebase belongs to the
engineering skills, not here.
