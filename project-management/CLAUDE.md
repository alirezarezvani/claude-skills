# Project Management Skills - Claude Code Guidance

This guide covers the 9 production-ready project management skills, 15 Python automation tools, and bundled Atlassian Remote MCP integration (`.mcp.json` ships with the plugin — OAuth handled by Claude Code, no env vars required).

## PM Skills Overview

**Available Skills:**
1. **pm-skills/** - Domain orchestrator (`context: fork`) + agentic delivery loop (3 scripts: goal router, Jira snapshot bridge, delivery loop gate)
2. **senior-pm/** - Portfolio health, risk analysis, resource planning (3 scripts)
3. **scrum-master/** - Sprint health, velocity forecasting, retrospectives (3 scripts)
4. **jira-expert/** - JQL building, workflow validation (2 scripts)
5. **confluence-expert/** - Space structure, content auditing (2 scripts)
6. **atlassian-admin/** - Permission auditing (1 script)
7. **atlassian-templates/** - Template scaffolding (1 script)
8. **meeting-analyzer/** - Meeting transcript behavioral analysis (prompt-driven; scripts are follow-up work)
9. **team-communications/** - 3P updates, newsletters, FAQs (reference-driven)

**Total Tools:** 15 Python automation tools
**Agents:** 2 — cs-pm-orchestrator (routing + delivery loop) and cs-project-manager (legacy per-skill orchestration)
**Slash Commands:** 6 (/cs:pm, /cs:grill-pm, /cs:pm-loop, /sprint-health, /project-health, /retro)
**Key Feature:** Atlassian MCP Server integration for direct Jira/Confluence operations

## Orchestrator & Delivery Loop (pm-skills)

`skills/pm-skills/` is the domain's `context: fork` orchestrator and agent harness adapter:

```bash
# Route a PM goal deterministically (exit 0 route / 2 ask / 3 no signal)
python3 skills/pm-skills/scripts/pm_goal_router.py --text "our sprints feel off"

# Bridge a saved searchJiraIssuesUsingJql result into analyzable inputs
python3 skills/pm-skills/scripts/jira_snapshot_bridge.py --input snapshot.json --to flow --forecast 20
python3 skills/pm-skills/scripts/jira_snapshot_bridge.py --input snapshot.json --to sprint > sprint_data.json
python3 skills/scrum-master/scripts/velocity_analyzer.py sprint_data.json

# Gate agent-executed delivery loops (G1 human owner … G6 exhausted budget = escalation)
python3 skills/pm-skills/scripts/delivery_loop_gate.py --plan plan.json --mode plan   # exit 2 = blocked
python3 skills/pm-skills/scripts/delivery_loop_gate.py --plan plan.json --mode close  # exit 4 = refused
```

Multi-task goals compile through the repo-wide harness
(`engineering/agent-harness` with the `project-management.json` manifest). Hard rules:
agents contribute, humans own; forecasts are Monte Carlo ranges, never dates; exhausted
budgets escalate — never reported as success. The five reusable PM loops (sprint-flow,
health, retro-action, RAID-hygiene, comms) are documented in
`skills/pm-skills/references/pm_loop_playbook.md`.

## Atlassian MCP Integration

**Purpose:** Direct integration with Jira and Confluence via Model Context Protocol (MCP)

**Canonical tool list:** [references/atlassian-mcp-tools.md](references/atlassian-mcp-tools.md) — the single source of truth for real tool names. Never invent tool names; if a capability isn't in that list (project creation, sprint management, field configuration, automation rules, space creation, …), it is NOT available via MCP — use the Atlassian web UI or REST API.

**Capabilities (real tools, camelCase):**
- Jira issues: `createJiraIssue`, `getJiraIssue`, `editJiraIssue`, `searchJiraIssuesUsingJql`, `transitionJiraIssue`, `addCommentToJiraIssue`, `createIssueLink`
- Confluence pages: `createConfluencePage`, `getConfluencePage`, `updateConfluencePage`, `searchConfluenceUsingCql`, `getConfluencePageDescendants`
- Discovery: `getAccessibleAtlassianResources` (get `cloudId` first), `getVisibleJiraProjects`, `getConfluenceSpaces`

**Setup:** Bundled `.mcp.json` registers the `atlassian` SSE server; tools surface as `mcp__atlassian__<toolName>`.

**Usage Pattern:**
```
# Jira: create an issue (call getAccessibleAtlassianResources first to obtain cloudId)
mcp__atlassian__createJiraIssue (cloudId, projectKey="PROJ", issueTypeName="Story", summary="New feature")

# Confluence: create a page (body must be storage-format XHTML or ADF, not wiki markup)
mcp__atlassian__createConfluencePage (cloudId, space, title="Sprint Retrospective", body=<storage-format XHTML>)
```

**Not available via MCP** (use web UI/REST API): project creation, sprints, boards, filters, space creation, page deletion, labels, field/workflow/permission configuration, user provisioning, automation rules.

## Skill-Specific Guidance

### Senior PM (`senior-pm/`)

**Focus:** Project planning, stakeholder management, risk mitigation

**Key Workflows:**
- Project charter creation
- Stakeholder analysis and communication plans
- Risk register maintenance
- Status reporting and escalation

### Scrum Master (`scrum-master/`)

**Focus:** Agile ceremonies, team coaching, impediment removal

**Key Workflows:**
- Sprint planning facilitation
- Daily standup coordination
- Sprint retrospectives
- Backlog refinement

### Jira Expert (`jira-expert/`)

**Focus:** Jira configuration, custom workflows, automation rules

**Scripts:**
- `scripts/jql_query_builder.py` — Pattern-matching JQL builder from natural language
- `scripts/workflow_validator.py` — Validates workflow definitions for anti-patterns

**Key Workflows:**
- Workflow customization
- Automation rule creation
- Board configuration
- JQL query optimization

### Confluence Expert (`confluence-expert/`)

**Focus:** Documentation strategy, templates, knowledge management

**Scripts:**
- `scripts/space_structure_generator.py` — Generates space hierarchy from team description
- `scripts/content_audit_analyzer.py` — Analyzes page inventory for stale/orphaned content

**Key Workflows:**
- Space architecture design
- Template library creation
- Documentation standards
- Search optimization

### Atlassian Admin (`atlassian-admin/`)

**Focus:** Suite administration, user management, integrations

**Scripts:**
- `scripts/permission_audit_tool.py` — Analyzes permission schemes for security gaps

**Key Workflows:**
- User provisioning and permissions
- SSO/SAML configuration
- App marketplace management
- Performance monitoring

### Atlassian Templates (`atlassian-templates/`)

**Focus:** Ready-to-use templates for common PM tasks

**Scripts:**
- `scripts/template_scaffolder.py` — Generates Confluence storage-format XHTML templates

**Available Templates:**
- Sprint planning template
- Retrospective formats (Start-Stop-Continue, 4Ls, Mad-Sad-Glad)
- Project charter
- Risk register
- Decision log

## Integration Patterns

### Pattern 1: Sprint Planning

```bash
# 1. Create the sprint in the Jira board UI (sprint creation is NOT available via MCP —
#    use Jira Software UI or REST /rest/agile/1.0/sprint)

# 2. Generate user stories (product-team integration)
python ../product-team/agile-product-owner/scripts/user_story_generator.py sprint 30

# 3. Import stories to Jira via MCP: one mcp__atlassian__createJiraIssue call per story
#    (cloudId, projectKey, issueTypeName="Story", summary, description)
```

### Pattern 2: Documentation Workflow

```bash
# 1. Scaffold storage-format XHTML, then create the Confluence page via MCP
python skills/atlassian-templates/scripts/template_scaffolder.py meeting-notes
#    → pass the emitted markup as the body of mcp__atlassian__createConfluencePage

# 2. Link the page to a Jira issue: paste the page URL into the issue via
#    mcp__atlassian__editJiraIssue or as a comment via mcp__atlassian__addCommentToJiraIssue
#    (read existing links with mcp__atlassian__getJiraIssueRemoteIssueLinks)
```

## Python Automation Tools

### New Scripts (Phase 2)

```bash
# JQL from natural language
python jira-expert/scripts/jql_query_builder.py "high priority bugs assigned to me"

# Validate Jira workflow
python jira-expert/scripts/workflow_validator.py workflow.json

# Generate Confluence space structure
python confluence-expert/scripts/space_structure_generator.py team_info.json

# Audit Confluence content health
python confluence-expert/scripts/content_audit_analyzer.py pages.json

# Audit Atlassian permissions
python atlassian-admin/scripts/permission_audit_tool.py permissions.json

# Scaffold Confluence templates
python atlassian-templates/scripts/template_scaffolder.py meeting-notes
```

## Additional Resources

- **Installation Guide:** `INSTALLATION_GUIDE.txt`
- **Implementation Summary:** `IMPLEMENTATION_SUMMARY.md`
- **Real-World Scenario:** `REAL_WORLD_SCENARIO.md`
- **PM Overview:** `README.md`
- **Main Documentation:** `../CLAUDE.md`

---

**Last Updated:** July 3, 2026
**Skills Deployed:** 9/9 PM skills production-ready (pm-skills is now a fork-orchestrator + delivery loop)
**Total Tools:** 15 Python automation tools
**Agents:** cs-pm-orchestrator, cs-project-manager | **Commands:** 6
**Integration:** Atlassian Remote MCP Server (bundled via `.mcp.json`) for Jira/Confluence automation
