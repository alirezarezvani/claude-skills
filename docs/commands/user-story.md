---
title: "/user-story"
description: "/user-story — Claude Code slash command."
---

# /user-story

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/commands/user-story.md">Source</a></span>
</div>


Generate structured user stories with acceptance criteria, story points, and sprint capacity planning.

## Usage

```
/user-story generate                                         Generate user stories (interactive)
/user-story sprint <capacity>                                Plan sprint with story point capacity
```

## Input Format

Interactive mode prompts for feature context. For sprint planning, provide capacity as story points:

```
/user-story generate
> Feature: User authentication
> Persona: Engineering manager
> Epic: Platform Security

/user-story sprint 21
> Stories are ranked by priority and fit within 21-point capacity
```

## Examples

```
/user-story generate
/user-story sprint 34
/user-story sprint 21
```

## Scripts
- `product-team/agile-product-owner/scripts/user_story_generator.py` — User story generator (positional args: `sprint <capacity>`)

## Skill Reference
> `product-team/agile-product-owner/SKILL.md`
