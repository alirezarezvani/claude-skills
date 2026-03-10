# Project Management Skills - Claude Code Guidance

This guide covers the 6 production-ready project management skills, 12 Python automation tools, and Atlassian MCP integration.

## PM Skills Overview

**Available Skills:**
1. **senior-pm/** - Portfolio health, risk analysis, resource planning (3 scripts)
2. **scrum-master/** - Sprint health, velocity forecasting, retrospectives (3 scripts)
3. **jira-expert/** - JQL building, workflow validation (2 scripts)
4. **confluence-expert/** - Space structure, content auditing (2 scripts)
5. **atlassian-admin/** - Permission auditing (1 script)
6. **atlassian-templates/** - Template scaffolding (1 script)

**Total Tools:** 12 Python automation tools
**Agent:** cs-project-manager (orchestrates all 6 skills)
**Slash Commands:** 3 (/sprint-health, /project-health, /retro)
**Key Feature:** Atlassian MCP Server integration for direct Jira/Confluence operations

## Atlassian MCP Integration

**Purpose:** Direct integration with Jira and Confluence via Model Context Protocol (MCP)

**Capabilities:**
- Create, read, update Jira issues
- Manage Confluence pages and spaces
- Automate workflows and transitions
- Generate reports and dashboards
- Bulk operations on issues

**Setup:** Atlassian MCP server configured in Claude Code settings

**Usage Pattern:**
```bash
# Jira operations via MCP
mcp__atlassian__create_issue project="PROJ" summary="New feature" type="Story"

# Confluence operations via MCP
mcp__atlassian__create_page space="TEAM" title="Sprint Retrospective"
```

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
# 1. Create sprint in Jira (via MCP)
mcp__atlassian__create_sprint board="TEAM-board" name="Sprint 23" start="2025-11-06"

# 2. Generate user stories (product-team integration)
python ../product-team/agile-product-owner/scripts/user_story_generator.py sprint 30

# 3. Import stories to Jira
# (Manual or via Jira API integration)
```

### Pattern 2: Documentation Workflow

```bash
# 1. Create Confluence page template
mcp__atlassian__create_page space="DOCS" title="Feature Spec" template="feature-spec"

# 2. Link to Jira epic
mcp__atlassian__link_issue issue="PROJ-123" confluence_page_id="456789"
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

**Last Updated:** March 9, 2026
**Skills Deployed:** 6/6 PM skills production-ready
**Total Tools:** 12 Python automation tools
**Agent:** cs-project-manager | **Commands:** 3
**Integration:** Atlassian MCP Server for Jira/Confluence automation
