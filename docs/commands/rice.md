---
title: "/rice"
description: "/rice — Claude Code slash command."
---

# /rice

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/commands/rice.md">Source</a></span>
</div>


Prioritize features using RICE scoring (Reach, Impact, Confidence, Effort) with optional capacity constraints.

## Usage

```
/rice prioritize <features.csv>                              Score and rank features
/rice prioritize <features.csv> --capacity 20                Rank with effort capacity limit
```

## Input Format

```csv
feature,reach,impact,confidence,effort
Dark mode,5000,2,0.8,3
API v2,12000,3,0.9,8
SSO integration,3000,2,0.7,5
Mobile app,20000,3,0.5,13
```

## Examples

```
/rice prioritize features.csv
/rice prioritize features.csv --capacity 20
/rice prioritize features.csv --output json
```

## Scripts
- `product-team/product-manager-toolkit/scripts/rice_prioritizer.py` — RICE prioritizer (`<input.csv> [--capacity N] [--output text|json|csv]`)

## Skill Reference
> `product-team/product-manager-toolkit/SKILL.md`
