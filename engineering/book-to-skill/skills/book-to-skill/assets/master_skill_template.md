---
name: <slug>
description: "Knowledge base from \"<Full Title>\" by <Author(s)>. Use when applying <author>'s frameworks for <3–6 key topics>, studying the book, or referencing its concepts."
---

<!--
HARD BUDGET: under 4,000 tokens.

Compaction truncates from the END. The end of this file is the Chapter Index and the
Topic Index — the navigation everything else depends on. Overflow does not degrade this
skill gracefully; it removes exactly the part that makes chapter files reachable. Put the
most important content first and keep the indexes inside the budget.

Frontmatter carries `name` and `description` ONLY. No allowed-tools, no model-invocation
flags — a generated skill never widens its own authority.
-->

# <Full Title>

**Author**: <Author(s)> | **Pages**: ~<N> | **Chapters**: <N> | **Generated**: <YYYY-MM-DD>

## How to Use This Skill

- **No argument** — load the core frameworks below
- **A topic** — ask about `<example topic>`; I resolve it through the Topic Index and read
  that chapter file
- **`chNN`** — I load that chapter's summary
- **"what chapters do you have?"** — the full index

When you ask about something not in Core Frameworks, I read the relevant chapter file before
answering rather than guessing from the index.

---

## Core Frameworks & Mental Models

<!-- ~2,000 tokens. The author's most important named frameworks and principles, exact names
     preserved. Write as instruments: "Use X when Y", "Prefer X over Y because Z".
     A toolkit, not a summary. This is the part that is resident in every session — spend
     the budget on what gets used, not on what was memorable to read. -->

### <Framework Name>

<What it is, when it applies, how to run it.>

### <Framework Name>

<...>

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-<slug>.md) | <Title> | <framework>, <framework> |
| [ch02](chapters/ch02-<slug>.md) | <Title> | <framework> |

## Topic Index

<!-- Alphabetical. Major terms and frameworks → the chapters that cover them. This is how
     the agent navigates; without it the chapter files are unreachable except by guessing.
     Every chapter file must appear at least once across these two indexes. -->

- **<Term>** → ch<N>, ch<N>
- **<Term>** → ch<N>

## Supporting Files

- [glossary.md](glossary.md) — every key term with its definition and chapter
- [patterns.md](patterns.md) — techniques and design patterns with trade-offs
- [cheatsheet.md](cheatsheet.md) — decision rules, thresholds, trade-off matrices

---

## Scope & Limits

This skill covers **<Full Title>** and nothing else. It carries that source's blind spots and
its publication-era assumptions.

For hands-on implementation in a codebase, combine it with project-specific tools. For topics
this source does not cover, say so rather than improvising — a compiled skill that quietly
extrapolates is worse than one that admits its boundary.

<!-- Provenance (see references/rights_and_provenance.md): compiled notes, not a reproduction.
     If this skill is packaged for distribution, the rights basis is recorded in the plugin
     manifest. -->
