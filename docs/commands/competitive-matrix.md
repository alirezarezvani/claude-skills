---
title: "/competitive-matrix — Slash Command for AI Coding Agents"
description: "Build competitive analysis matrices with scoring and gap analysis. Usage: /competitive-matrix <analyze> [options]. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /competitive-matrix

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/commands/competitive-matrix.md">Source</a></span>
</div>


Build competitive matrices with weighted scoring, gap analysis, and market positioning insights.

## Usage

```
/competitive-matrix analyze <competitors.json>                    Full analysis
/competitive-matrix analyze <competitors.json> --weights pricing=2,ux=1.5    Custom weights
```

## Input Format

```json
{
  "your_product": { "name": "MyApp", "scores": {"ux": 8, "pricing": 7, "features": 9} },
  "competitors": [
    { "name": "Competitor A", "scores": {"ux": 7, "pricing": 9, "features": 6} }
  ],
  "dimensions": ["ux", "pricing", "features"]
}
```

## Examples

```
/competitive-matrix analyze competitors.json
/competitive-matrix analyze competitors.json --format json --output matrix.json
```

## Scripts
- `product-team/competitive-teardown/scripts/competitive_matrix_builder.py` — Matrix builder

## Skill Reference
→ `product-team/competitive-teardown/SKILL.md`
