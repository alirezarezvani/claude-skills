---
title: "Project Management Skills"
description: "Project Management Skills - Claude Code skill from the Project Management domain."
---

# Project Management Skills

<div class="page-meta" markdown>
<span class="meta-badge">:material-clipboard-check-outline: Project Management</span>
<span class="meta-badge">:material-identifier: `project-management`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/project-management/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install pm-skills</code>
</div>


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
