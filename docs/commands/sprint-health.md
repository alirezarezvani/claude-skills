---
title: "/sprint-health — Slash Command for AI Coding Agents"
description: "Sprint health scoring and velocity analysis for agile teams. Usage: /sprint-health <analyze|velocity> [options]. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /sprint-health

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/commands/sprint-health.md">Source</a></span>
</div>


Score sprint health across delivery, quality, and team metrics with velocity trend analysis.

## Usage

```
/sprint-health analyze <sprint_data.json>                    Full sprint health score
/sprint-health velocity <sprint_data.json>                   Velocity trend analysis
```

## Input Format

```json
{
  "sprint_name": "Sprint 24",
  "committed_points": 34,
  "completed_points": 29,
  "stories": {"total": 12, "completed": 10, "carried_over": 2},
  "blockers": [{"description": "API dependency", "days_blocked": 3}],
  "ceremonies": {"planning": true, "daily": true, "review": true, "retro": true}
}
```

## Examples

```
/sprint-health analyze sprint-24.json
/sprint-health velocity last-6-sprints.json
/sprint-health analyze sprint-24.json --format json
```

## Scripts
- `project-management/scrum-master/scripts/sprint_health_scorer.py` — Sprint health scorer (`<data_file> [--format text|json]`)
- `project-management/scrum-master/scripts/velocity_analyzer.py` — Velocity analyzer (`<data_file> [--format text|json]`)

## Skill Reference
> `project-management/scrum-master/SKILL.md`
