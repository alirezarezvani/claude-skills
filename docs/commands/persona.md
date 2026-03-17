---
title: "/persona — Slash Command for AI Coding Agents"
description: "Generate data-driven user personas for UX research and product design. Usage: /persona generate [options]. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /persona

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/commands/persona.md">Source</a></span>
</div>


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
