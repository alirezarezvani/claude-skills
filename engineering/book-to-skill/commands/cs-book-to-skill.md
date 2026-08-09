---
name: "cs-book-to-skill"
description: "/cs:book-to-skill <path|folder|glob>... [skill-name] — convert a book, documentation folder, or source collection into a structured agent skill (core frameworks + on-demand chapters + glossary + patterns + cheatsheet). Use when the user wants to study a document with an agent, apply an author's frameworks while working, or turn internal docs into a reusable knowledge base."
---

# /cs:book-to-skill — Compile a Source into an Agent Skill

**Command:** `/cs:book-to-skill <path|folder|glob>... [skill-name-slug]`

Runs the converter end to end: extract → analyze → chapter files → supporting files → master
`SKILL.md` → validate. Add "analyze only" to stop after the extraction report.

## Pre-flight gates

The command refuses, with a reason, when:

| Gate | Refusal |
|------|---------|
| No path given | Prints usage. This tool converts files on disk — not titles from memory, not URLs. |
| No supported file resolves | Names what was searched and the supported extensions. |
| Source is smaller than ~3× the compiled skill | Says converting is not worth it and recommends handing the agent the document. |
| Cost estimate not approved | Waits. Generation is the expensive step and the user approves it with numbers in front of them. |
| Validation errors after generation | Blocks. Dead chapter links and dangling topic references break navigation silently. |

## The six forcing questions

Asked one at a time, each with a recommended answer.

### 1. Is this source worth converting, or should I just read it?
*Recommended:* convert when it is > 3× the compiled skill's size **and** you will return to it.
One-shot reads are cheaper unconverted. `token_budget_estimator.py` prints the verdict.

### 2. Reference or study?
*Recommended:* reference, unless you intend to internalize the author's reasoning. Study depth
roughly doubles generation cost and only earns it with real worked examples.

### 3. Technical or text?
*Recommended:* technical only when tables, code, or formulas carry meaning. Docling costs
~1.5s/page and buys nothing on a prose book.

### 4. What will you actually ask this skill?
*Recommended:* name three real questions before generating. They decide what belongs in Core
Frameworks and what the topic index must resolve.

### 5. Do you have the right to redistribute this?
*Recommended:* assume not. Keep it local unless the source is public-domain, openly licensed,
your organisation's own documentation, or you have written permission.

### 6. Does this belong beside an existing skill?
*Recommended:* check for a compiled skill on the same subject first. Folding new sources into
one skill beats two skills that half-cover a topic and give the agent no way to choose.

## Pipeline

```bash
SKILL_ROOT=engineering/book-to-skill/skills/book-to-skill

# 0. environment (optional — reports extractors, installs nothing)
python3 "$SKILL_ROOT/scripts/extract_document.py" --check

# 1. extract
python3 "$SKILL_ROOT/scripts/extract_document.py" <paths> --mode text|technical

# 2. worth-it verdict, before spending a generation pass
python3 "$SKILL_ROOT/scripts/token_budget_estimator.py" --full-text "$WORKDIR/full_text.txt"

# 3. generate (agent work: chapters, glossary, patterns, cheatsheet, SKILL.md)

# 4. gate
python3 "$SKILL_ROOT/scripts/book_skill_validator.py" "$SKILLS_HOME/<slug>"
python3 "$SKILL_ROOT/scripts/token_budget_estimator.py" --skill-dir "$SKILLS_HOME/<slug>"
```

## Output digest

```
✅ <slug> — <Title> by <Author>   <N> chapters
   SKILL.md ~<N> tokens (resident) · chapters ~<N> each (on demand)
   validator: <N> error(s), <N> warning(s)
   next: /cs:book-to-plugin to package it for this repo
```

## Related

- `/cs:book-to-plugin` — wrap a compiled skill as a claude-skills plugin
- `/cs:write-a-skill` — author a skill from your own expertise instead of a document
