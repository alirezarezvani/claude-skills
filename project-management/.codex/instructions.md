# Project Management Skills — Codex CLI Instructions

When working on project management tasks, use the PM skill system:

## Routing

1. **Identify the task:** PM methodology, Scrum, Jira, Confluence, or Atlassian admin
2. **Read the specialist SKILL.md** for detailed instructions

## Python Tools

All scripts in `project-management/*/scripts/` are stdlib-only and CLI-first:

```bash
python3 project-management/senior-pm/scripts/project_health_dashboard.py --help
python3 project-management/scrum-master/scripts/velocity_analyzer.py --help
```

## Key Skills by Task

| Task | Skill |
|------|-------|
| Portfolio management | senior-pm |
| Sprint health | scrum-master |
| Jira automation | jira-expert |
| Knowledge bases | confluence-expert |
| Atlassian setup | atlassian-admin |
| Templates/layouts | atlassian-templates |

## Rules

- Load only 1-2 skills per request — don't bulk-load
- Use MCP tools for live Jira/Confluence operations when available
