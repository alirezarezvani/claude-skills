---
name: "cs-spinning-up-deep-rl"
description: "/cs:spinning-up-deep-rl [topic | framework | chNN] — query the knowledge base compiled from Spinning Up in Deep RL by Joshua Achiam (OpenAI). Use when applying its frameworks while working, looking up a term, or reading one chapter's summary."
---

# /cs:spinning-up-deep-rl — Spinning Up in Deep RL

**Command:** `/cs:spinning-up-deep-rl [topic | framework name | chNN]`

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
