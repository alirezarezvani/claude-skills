---
name: "pm-skills"
description: "6 production-ready project management skills for Atlassian users: senior PM with portfolio management, scrum master with velocity forecasting, Jira expert with JQL mastery, Confluence expert, Atlassian admin, and template creator. MCP integration for live Jira/Confluence automation. Works with Claude Code, Codex CLI, and OpenClaw."
version: 1.0.0
author: Alireza Rezvani
license: MIT
tags:
  - project-management
  - jira
  - confluence
  - atlassian
  - scrum
  - agile
agents:
  - claude-code
  - codex-cli
  - openclaw
---

# Project Management Skills

6 production-ready project management skills with Atlassian MCP integration.

## Quick Start

### Claude Code
```
/read project-management/jira-expert/SKILL.md
```

### Codex CLI
```bash
npx agent-skills-cli add alirezarezvani/claude-skills/project-management
```

## Skills Overview

| Skill | Folder | Focus |
|-------|--------|-------|
| Senior PM | `senior-pm/` | Portfolio management, risk analysis, resource planning |
| Scrum Master | `scrum-master/` | Velocity forecasting, sprint health, retrospectives |
| Jira Expert | `jira-expert/` | JQL queries, workflows, automation, dashboards |
| Confluence Expert | `confluence-expert/` | Knowledge bases, page layouts, macros |
| Atlassian Admin | `atlassian-admin/` | User management, permissions, integrations |
| Atlassian Templates | `atlassian-templates/` | Blueprints, custom layouts, reusable content |

## Python Tools

6 scripts, all stdlib-only:

```bash
python3 senior-pm/scripts/project_health_dashboard.py --help
python3 scrum-master/scripts/velocity_analyzer.py --help
```

## Rules

- Load only the specific skill SKILL.md you need
- Use MCP tools for live Jira/Confluence operations when available
