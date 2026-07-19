---
name: "cs-arquiteto"
description: "/cs:arquiteto — Builds a company from scratch as an OKF bundle (tree of .md with type + link graph). Guides the 12-phase interview, one at a time, and generates conformant markdown concepts. In English."
---

# /cs:arquiteto — Company Architect

**Command:** `/cs:arquiteto`

## When to run

- You want to create/structure/document an entire company as folders and `.md` files.
- You want a company knowledge base that humans and AI agents read without translation.
- You are starting a business from scratch and want the "blueprint" before operations.

## What you get

A conformant **OKF bundle**: folder tree of the 12 phases, each concept as a `.md` with frontmatter `type`, linked by markdown links, plus `index.md` (dashboard) and `log.md` (decisions).

## Triggers (auto-invocation without typing /cs:)

- "I want to build my company from scratch"
- "create the company as folders"
- "document my business as code"
- "company knowledge base for the agents to read"
- "company as a wiki for AI", "OKF", "knowledge bundle"

## Discipline

- Interview before building; one phase at a time; 3-5 questions per block.
- Confirm the file list (+ `type`) before writing.
- Update the root `index.md` and `log.md` after each phase.

## Flow

1. Ask for the bundle name (company/root folder).
2. Run `scaffold_bundle.py "<name>" --out ./<slug>` (or build the folders by hand).
3. Start **PHASE 0** (discovery) — only its questions; stop and wait.
4. Each phase: confirm → write concepts → run `okf_linter.py` + `index_generator.py --write` → show the "suggested next step".

Details in `skills/arquiteto-de-empresa/SKILL.md` and `references/phase_playbook.md`.
