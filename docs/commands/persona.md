---
title: "/persona"
description: "/persona — Claude Code slash command."
---

# /persona

**Type:** Slash Command | **Source:** [`commands/persona.md`](https://github.com/alirezarezvani/claude-skills/tree/main/commands/persona.md)

---


# /persona

Generate structured user personas with demographics, goals, pain points, and behavioral patterns.

## Usage

```
/persona generate                                            Generate persona (interactive)
/persona generate json                                       Generate persona as JSON
```

## Input Format

Interactive mode prompts for product context. Alternatively, provide context inline:

```
/persona generate
> Product: B2B project management tool
> Target: Engineering managers at mid-size companies
> Key problem: Cross-team visibility
```

## Examples

```
/persona generate
/persona generate json
/persona generate json > persona-eng-manager.json
```

## Scripts
- `product-team/ux-researcher-designer/scripts/persona_generator.py` — Persona generator (positional `json` arg for JSON output)

## Skill Reference
> `product-team/ux-researcher-designer/SKILL.md`
