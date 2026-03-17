---
title: "Atlassian Template & Files Creator Expert — Agent Skill for PM"
description: "Atlassian Template and Files Creator/Modifier expert for creating, modifying, and managing Jira and Confluence templates, blueprints, custom layouts. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Atlassian Template & Files Creator Expert

<div class="page-meta" markdown>
<span class="meta-badge">:material-clipboard-check-outline: Project Management</span>
<span class="meta-badge">:material-identifier: `atlassian-templates`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/project-management/atlassian-templates/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install pm-skills</code>
</div>


Specialist in creating, modifying, and managing reusable templates and files for Jira and Confluence. Ensures consistency, accelerates content creation, and maintains org-wide standards.

---

## Workflows

### Template Creation Process
1. **Discover**: Interview stakeholders to understand needs
2. **Analyze**: Review existing content patterns
3. **Design**: Create template structure and placeholders
4. **Implement**: Build template with macros and formatting
5. **Test**: Validate with sample data — confirm template renders correctly in preview before publishing
6. **Document**: Create usage instructions
7. **Publish**: Deploy to appropriate space/project via MCP (see MCP Operations below)
8. **Verify**: Confirm deployment success; roll back to previous version if errors occur
9. **Train**: Educate users on template usage
10. **Monitor**: Track adoption and gather feedback
11. **Iterate**: Refine based on usage

### Template Modification Process
1. **Assess**: Review change request and impact
2. **Version**: Create new version, keep old available
3. **Modify**: Update template structure/content
4. **Test**: Validate changes don't break existing usage; preview updated template before publishing
5. **Migrate**: Provide migration path for existing content
6. **Communicate**: Announce changes to users
7. **Support**: Assist users with migration
8. **Archive**: Deprecate old version after transition; confirm deprecated template is unlisted, not deleted

### Blueprint Development
1. Define blueprint scope and purpose
2. Design multi-page structure
3. Create page templates for each section
4. Configure page creation rules
5. Add dynamic content (Jira queries, user data)
6. Test blueprint creation flow end-to-end with a sample space
7. Verify all macro references resolve correctly before deployment
8. **HANDOFF TO**: Atlassian Admin for global deployment

---

## Confluence Templates Library

See **TEMPLATES.md** for full reference tables and copy-paste-ready template structures. The following summarises the standard types this skill creates and maintains.

### Confluence Template Types
| Template | Purpose | Key Macros Used |
|----------|---------|-----------------|
| **Meeting Notes** | Structured meeting records with agenda, decisions, and action items | `{date}`, `{tasks}`, `{panel}`, `{info}`, `{note}` |
| **Project Charter** | Org-level project scope, stakeholder RACI, timeline, and budget | `{panel}`, `{status}`, `{timeline}`, `{info}` |
| **Sprint Retrospective** | Agile ceremony template with What Went Well / Didn't Go Well / Actions | `{panel}`, `{expand}`, `{tasks}`, `{status}` |
| **PRD** | Feature definition with goals, user stories, functional/non-functional requirements, and release plan | `{panel}`, `{status}`, `{jira}`, `{warning}` |
| **Decision Log** | Structured option analysis with decision matrix and implementation tracking | `{panel}`, `{status}`, `{info}`, `{tasks}` |

**Standard Sections** included across all Confluence templates:
- Header panel with metadata (owner, date, status)
- Clearly labelled content sections with inline placeholder instructions
- Action items block using `{tasks}` macro
- Related links and references

### Complete Example: Meeting Notes Template

The following is a copy-paste-ready Meeting Notes template in Confluence storage format (wiki markup):

```
{panel:title=Meeting Metadata|borderColor=#0052CC|titleBGColor=#0052CC|titleColor=#FFFFFF}
*Date:* {date}
*Owner / Facilitator:* @[facilitator name]
*Attendees:* @[name], @[name]
*Status:* {status:colour=Yellow|title=In Progress}
{panel}

h2. Agenda
# [Agenda item 1]
# [Agenda item 2]
# [Agenda item 3]

h2. Discussion & Decisions
{panel:title=Key Decisions|borderColor=#36B37E|titleBGColor=#36B37E|titleColor=#FFFFFF}
* *Decision 1:* [What was decided and why]
* *Decision 2:* [What was decided and why]
{panel}

{info:title=Notes}
[Detailed discussion notes, context, or background here]
{info}

h2. Action Items
{tasks}
* [ ] [Action item] — Owner: @[name] — Due: {date}
* [ ] [Action item] — Owner: @[name] — Due: {date}
{tasks}

h2. Next Steps & Related Links
* Next meeting: {date}
* Related pages: [link]
* Related Jira issues: {jira:key=PROJ-123}
```

> Full examples for all other template types (Project Charter, Sprint Retrospective, PRD, Decision Log) and all Jira templates can be generated on request or found in **TEMPLATES.md**.

---

## Jira Templates Library

### Jira Template Types
| Template | Purpose | Key Sections |
|----------|---------|--------------|
| **User Story** | Feature requests in As a / I want / So that format | Acceptance Criteria (Given/When/Then), Design links, Technical Notes, Definition of Done |
| **Bug Report** | Defect capture with reproduction steps | Environment, Steps to Reproduce, Expected vs Actual Behavior, Severity, Workaround |
| **Epic** | High-level initiative scope | Vision, Goals, Success Metrics, Story Breakdown, Dependencies, Timeline |

**Standard Sections** included across all Jira templates:
- Clear summary line
- Acceptance or success criteria as checkboxes
- Related issues and dependencies block
- Definition of Done (for stories)

---

## Macro Usage Guidelines

**Dynamic Content**: Use macros for auto-updating content (dates, user mentions, Jira queries)
**Visual Hierarchy**: Use `{panel}`, `{info}`, and `{note}` to create visual distinction
**Interactivity**: Use `{expand}` for collapsible sections in long templates
**Integration**: Embed Jira charts and tables via `{jira}` macro for live data

---

## Atlassian MCP Integration

**Primary Tools**: Confluence MCP, Jira MCP

### Template Operations via MCP

All MCP calls below use the exact parameter names expected by the Atlassian MCP server. Replace angle-bracket placeholders with real values before executing.

**Create a Confluence page template:**
```json
{
  "tool": "confluence_create_page",
  "parameters": {
    "space_key": "PROJ",
    "title": "Template: Meeting Notes",
    "body": "<storage-format template content>",
    "labels": ["template", "meeting-notes"],
    "parent_id": "<optional parent page id>"
  }
}
```

**Update an existing template:**
```json
{
  "tool": "confluence_update_page",
  "parameters": {
    "page_id": "<existing page id>",
    "version": "<current_version + 1>",
    "title": "Template: Meeting Notes",
    "body": "<updated storage-format content>",
    "version_comment": "v2 — added status macro to header"
  }
}
```

**Create a Jira issue description template (via field configuration):**
```json
{
  "tool": "jira_update_field_configuration",
  "parameters": {
    "project_key": "PROJ",
    "field_id": "description",
    "default_value": "<template markdown or Atlassian Document Format JSON>"
  }
}
```

**Deploy template to multiple spaces (batch):**
```json
// Repeat for each target space key
{
  "tool": "confluence_create_page",
  "parameters": {
    "space_key": "<SPACE_KEY>",
    "title": "Template: Meeting Notes",
    "body": "<storage-format template content>",
    "labels": ["template"]
  }
}
// After each create, verify:
{
  "tool": "confluence_get_page",
  "parameters": {
    "space_key": "<SPACE_KEY>",
    "title": "Template: Meeting Notes"
  }
}
// Assert response status == 200 and page body is non-empty before proceeding to next space
```

**Validation checkpoint after deployment:**
- Retrieve the created/updated page and assert it renders without macro errors
- Check that `{jira}` embeds resolve against the target Jira project
- Confirm `{tasks}` blocks are interactive in the published view
- If any check fails: revert using `confluence_update_page` with `version: <current + 1>` and the previous version body

---

## Best Practices & Governance

**Org-Specific Standards:**
- Track template versions with version notes in the page header
- Mark outdated templates with a `{warning}` banner before archiving; archive (do not delete)
- Maintain usage guides linked from each template
- Gather feedback on a quarterly review cycle; incorporate usage metrics before deprecating

**Quality Gates (apply before every deployment):**
- Example content provided for each section
- Tested with sample data in preview
- Version comment added to change log
- Feedback mechanism in place (comments enabled or linked survey)

**Governance Process**:
1. Request and justification
2. Design and review
3. Testing with pilot users
4. Documentation
5. Approval
6. Deployment (via MCP or manual)
7. Training
8. Monitoring

---

## Handoff Protocols

See **HANDOFFS.md** for the full handoff matrix. Summary:

| Partner | Receives FROM | Sends TO |
|---------|--------------|---------|
| **Senior PM** | Template requirements, reporting templates, executive formats | Completed templates, usage analytics, optimization suggestions |
| **Scrum Master** | Sprint ceremony needs, team-specific requests, retro format preferences | Sprint-ready templates, agile ceremony structures, velocity tracking templates |
| **Jira Expert** | Issue template requirements, custom field display needs | Issue description templates, field config templates, JQL query templates |
| **Confluence Expert** | Space-specific needs, global template requests, blueprint requirements | Configured page templates, blueprint structures, deployment plans |
| **Atlassian Admin** | Org-wide standards, global deployment requirements, compliance templates | Global templates for approval, usage reports, compliance status |
