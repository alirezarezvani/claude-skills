---
name: write-a-skill
description: Create new agent skills with proper structure, progressive disclosure, and bundled resources. Use when user wants to create, write, build, or author a new skill.
license: MIT
metadata:
  derived_from: "https://github.com/mattpocock/skills/tree/main/skills/productivity/write-a-skill"
  original_author: "Matt Pocock (@mattpocock)"
  original_license: MIT
  voice: "Matt Pocock — direct, concrete, imperative, example-driven"
  version: 1.0.0
---

# Writing Skills

> Derived from [Matt Pocock's write-a-skill](https://github.com/mattpocock/skills/tree/main/skills/productivity/write-a-skill) (MIT). Matt's voice and 3-phase workflow preserved verbatim. Additions: validation tools + references + cs-* wrapper (see *Tooling + Companions* below).

## Process

1. **Gather requirements** - ask user about:
   - What task/domain does the skill cover?
   - What specific use cases should it handle?
   - Does it need executable scripts or just instructions?
   - Any reference materials to include?

2. **Draft the skill** - create:
   - SKILL.md with concise instructions
   - Additional reference files if content exceeds 500 lines
   - Utility scripts if deterministic operations needed

3. **Review with user** - present draft and ask:
   - Does this cover your use cases?
   - Anything missing or unclear?
   - Should any section be more/less detailed?

## Skill Structure

```
skill-name/
├── SKILL.md           # Main instructions (required)
├── REFERENCE.md       # Detailed docs (if needed)
├── EXAMPLES.md        # Usage examples (if needed)
└── scripts/           # Utility scripts (if needed)
    └── helper.js
```

## SKILL.md Template

```md
---
name: skill-name
description: Brief description of capability. Use when [specific triggers].
---

# Skill Name

## Quick start

[Minimal working example]

## Workflows

[Step-by-step processes with checklists for complex tasks]

## Advanced features

[Link to separate files: See [REFERENCE.md](REFERENCE.md)]
```

## Description Requirements

The description is **the only thing your agent sees** when deciding which skill to load. It's surfaced in the system prompt alongside all other installed skills. Your agent reads these descriptions and picks the relevant skill based on the user's request.

**Goal**: Give your agent just enough info to know:

1. What capability this skill provides
2. When/why to trigger it (specific keywords, contexts, file types)

**Format**:

- Max 1024 chars
- Write in third person
- First sentence: what it does
- Second sentence: "Use when [specific triggers]"

**Good example**:

```
Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, or document extraction.
```

**Bad example**:

```
Helps with documents.
```

The bad example gives your agent no way to distinguish this from other document skills.

## When to Add Scripts

Add utility scripts when:

- Operation is deterministic (validation, formatting)
- Same code would be generated repeatedly
- Errors need explicit handling

Scripts save tokens and improve reliability vs generated code.

## When to Split Files

Split into separate files when:

- SKILL.md exceeds 100 lines
- Content has distinct domains (finance vs sales schemas)
- Advanced features are rarely needed

## Review Checklist

After drafting, verify:

- [ ] Description includes triggers ("Use when...")
- [ ] SKILL.md under 100 lines
- [ ] No time-sensitive info
- [ ] Consistent terminology
- [ ] Concrete examples included
- [ ] References one level deep

## Tooling + Companions

Validation tools + cs-* wrapper sit alongside this skill. Run all 6 review-checklist items programmatically:

```
python scripts/skill_review_checklist_runner.py path/to/skill-folder
```

See [references/companion_tooling.md](references/companion_tooling.md) for the tool catalogue, cs-skill-author persona agent, and `/cs:write-a-skill` slash command.

## When the knowledge is in a document, not your head

This skill authors from expertise you already have. When the source is a book, a docs folder,
a standard, or a pile of specs, use `engineering/book-to-skill` instead — it compiles the
document into a knowledge-base skill (core frameworks + on-demand chapters + glossary +
patterns + cheatsheet) and can package the result as a plugin.

```
/cs:book-to-skill <path|folder|glob> [skill-name]     # compile the source
/cs:book-to-plugin <compiled-skill-dir>               # wrap it as a plugin
```

Rule of thumb: **author first, compile second.** A hand-written skill states what you want the
agent to do; a compiled book skill is the reference it consults while doing it. If you have
both, they are two skills, not one.

---

**Version:** 1.0.0
**Derived:** Matt Pocock (MIT) + this repo's wrapper
