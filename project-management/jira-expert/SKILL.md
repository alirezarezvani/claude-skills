---
name: "jira-expert"
description: Atlassian Jira expert for creating and managing projects, planning, product discovery, JQL queries, workflows, custom fields, automation, reporting, and all Jira features. Use for Jira project setup, configuration, advanced search, dashboard creation, workflow design, and technical Jira operations.
---

# Atlassian Jira Expert

Master-level expertise in Jira configuration, project management, JQL, workflows, automation, and reporting. Handles all technical and operational aspects of Jira.

## Quick Start — Most Common Operations

**Create a project**:
```
mcp jira create_project --name "My Project" --key "MYPROJ" --type scrum --lead "user@example.com"
```

**Run a JQL query**:
```
mcp jira search_issues --jql "project = MYPROJ AND status != Done AND dueDate < now()" --maxResults 50
```

For full command reference, see [Atlassian MCP Integration](#atlassian-mcp-integration). For JQL functions, see [JQL Functions Reference](#jql-functions-reference). For report templates, see [Reporting Templates](#reporting-templates).

---

## Workflows

### Project Creation
1. Determine project type (Scrum, Kanban, Bug Tracking, etc.)
2. Create project with appropriate template
3. Configure project settings:
   - Name, key, description
   - Project lead and default assignee
   - Notification scheme
   - Permission scheme
4. Set up issue types and workflows
5. Configure custom fields if needed
6. Create initial board/backlog view
7. **HANDOFF TO**: Scrum Master for team onboarding

### Workflow Design
1. Map out process states (To Do → In Progress → Done)
2. Define transitions and conditions
3. Add validators, post-functions, and conditions
4. Configure workflow scheme
5. **Validate**: Deploy to a test project first; verify all transitions, conditions, and post-functions behave as expected before associating with production projects
6. Associate workflow with project
7. Test workflow with sample issues

### JQL Query Building
**Basic Structure**: `field operator value`

**Common Operators**:
- `=, !=` : equals, not equals
- `~, !~` : contains, not contains
- `>, <, >=, <=` : comparison
- `in, not in` : list membership
- `is empty, is not empty`
- `was, was in, was not`
- `changed`

**Powerful JQL Examples**:

Find overdue issues:
```jql
dueDate < now() AND status != Done
```

Sprint burndown issues:
```jql
sprint = 23 AND status changed TO "Done" DURING (startOfSprint(), endOfSprint())
```

Find stale issues:
```jql
updated < -30d AND status != Done
```

Cross-project epic tracking:
```jql
"Epic Link" = PROJ-123 ORDER BY rank
```

Velocity calculation:
```jql
sprint in closedSprints() AND resolution = Done
```

Team capacity:
```jql
assignee in (user1, user2) AND sprint in openSprints()
```

### Dashboard Creation
1. Create new dashboard (personal or shared)
2. Add relevant gadgets:
   - Filter Results (JQL-based)
   - Sprint Burndown
   - Velocity Chart
   - Created vs Resolved
   - Pie Chart (status distribution)
3. Arrange layout for readability
4. Configure automatic refresh
5. Share with appropriate teams
6. **HANDOFF TO**: Senior PM or Scrum Master for use

### Automation Rules
1. Define trigger (issue created, field changed, scheduled)
2. Add conditions (if applicable)
3. Define actions:
   - Update field
   - Send notification
   - Create subtask
   - Transition issue
   - Post comment
4. Test automation with sample data
5. Enable and monitor

## Advanced Features

### Custom Fields
**When to Create**:
- Track data not in standard fields
- Capture process-specific information
- Enable advanced reporting

**Field Types**: Text, Numeric, Date, Select (single/multi/cascading), User picker

**Configuration**:
1. Create custom field
2. Configure field context (which projects/issue types)
3. Add to appropriate screens
4. Update search templates if needed

### Issue Linking
**Link Types**:
- Blocks / Is blocked by
- Relates to
- Duplicates / Is duplicated by
- Clones / Is cloned by
- Epic-Story relationship

**Best Practices**:
- Use Epic linking for feature grouping
- Use blocking links to show dependencies
- Document link reasons in comments

### Permissions & Security

**Permission Schemes**:
- Browse Projects
- Create/Edit/Delete Issues
- Administer Projects
- Manage Sprints

**Security Levels**:
- Define confidential issue visibility
- Control access to sensitive data
- Audit security changes

### Bulk Operations
**Bulk Change**:
1. Use JQL to find target issues
2. Select bulk change operation
3. Choose fields to update
4. **Validate**: Preview all changes before executing; confirm the JQL filter matches only intended issues — bulk edits are difficult to reverse
5. Execute and confirm
6. Monitor background task

**Bulk Transitions**:
- Move multiple issues through workflow
- Useful for sprint cleanup
- Requires appropriate permissions
- **Validate**: Run the JQL filter and review results in small batches before applying at scale

## JQL Functions Reference

> **Tip**: Save frequently used queries as named filters instead of re-running complex JQL ad hoc. See [Best Practices](#best-practices) for performance guidance.

**Date**: `startOfDay()`, `endOfDay()`, `startOfWeek()`, `endOfWeek()`, `startOfMonth()`, `endOfMonth()`, `startOfYear()`, `endOfYear()`

**Sprint**: `openSprints()`, `closedSprints()`, `futureSprints()`

**User**: `currentUser()`, `membersOf("group")`

**Advanced**: `issueHistory()`, `linkedIssues()`, `issuesWithFixVersions()`

## Reporting Templates

> **Tip**: These JQL snippets can be saved as shared filters or wired directly into Dashboard gadgets (see [Dashboard Creation](#dashboard-creation)).

| Report | JQL |
|---|---|
| Sprint Report | `project = PROJ AND sprint = 23` |
| Team Velocity | `assignee in (team) AND sprint in closedSprints() AND resolution = Done` |
| Bug Trend | `type = Bug AND created >= -30d` |
| Blocker Analysis | `priority = Blocker AND status != Done` |

## Decision Framework

**When to Escalate to Atlassian Admin**:
- Need new project permission scheme
- Require custom workflow scheme across org
- User provisioning or deprovisioning
- License or billing questions
- System-wide configuration changes

**When to Collaborate with Scrum Master**:
- Sprint board configuration
- Backlog prioritization views
- Team-specific filters
- Sprint reporting needs

**When to Collaborate with Senior PM**:
- Portfolio-level reporting
- Cross-project dashboards
- Executive visibility needs
- Multi-project dependencies

## Handoff Protocols

**FROM Senior PM**:
- Project structure requirements
- Workflow and field needs
- Reporting requirements
- Integration needs

**TO Senior PM**:
- Cross-project metrics
- Issue trends and patterns
- Workflow bottlenecks
- Data quality insights

**FROM Scrum Master**:
- Sprint board configuration requests
- Workflow optimization needs
- Backlog filtering requirements
- Velocity tracking setup

**TO Scrum Master**:
- Configured sprint boards
- Velocity reports
- Burndown charts
- Team capacity views

## Best Practices

**Data Quality**:
- Enforce required fields with field validation rules
- Use consistent issue key naming conventions per project type
- Schedule regular cleanup of stale/orphaned issues

**Performance**:
- Avoid leading wildcards in JQL (`~` on large text fields is expensive)
- Use saved filters instead of re-running complex JQL ad hoc
- Limit dashboard gadgets to reduce page load time
- Archive completed projects rather than deleting to preserve history

**Governance**:
- Document rationale for custom workflow states and transitions
- Version-control permission/workflow schemes before making changes
- Require change management review for org-wide scheme updates
- Run permission audits after user role changes

## Atlassian MCP Integration

**Primary Tool**: Jira MCP Server

**Key Operations with Example Commands**:

Create a project:
```
mcp jira create_project --name "My Project" --key "MYPROJ" --type scrum --lead "user@example.com"
```

Execute a JQL query:
```
mcp jira search_issues --jql "project = MYPROJ AND status != Done AND dueDate < now()" --maxResults 50
```

Update an issue field:
```
mcp jira update_issue --issue "MYPROJ-42" --field "status" --value "In Progress"
```

Create a sprint:
```
mcp jira create_sprint --board 10 --name "Sprint 5" --startDate "2024-06-01" --endDate "2024-06-14"
```

Create a board filter:
```
mcp jira create_filter --name "Open Blockers" --jql "priority = Blocker AND status != Done" --shareWith "project-team"
```

**Integration Points**:
- Pull metrics for Senior PM reporting
- Configure sprint boards for Scrum Master
- Create documentation pages for Confluence Expert
- Support template creation for Template Creator

## Related Skills

- **Confluence Expert** (`project-management/confluence-expert/`) — Documentation complements Jira workflows
- **Atlassian Admin** (`project-management/atlassian-admin/`) — Permission and user management for Jira projects
