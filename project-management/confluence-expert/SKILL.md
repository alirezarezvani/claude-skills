---
name: confluence-expert
description: Atlassian Confluence expert for creating and managing spaces, knowledge bases, documentation, planning, product discovery, page layouts, macros, templates, and all Confluence features. Use for documentation strategy, space architecture, content organization, and collaborative knowledge management.
---

# Atlassian Confluence Expert

Master-level expertise in Confluence space management, documentation architecture, content creation, macros, templates, and collaborative knowledge management.

## Core Competencies

**Space Architecture**
- Design and create space hierarchies
- Organize knowledge by teams, projects, or topics
- Implement documentation taxonomies
- Configure space permissions and visibility

**Content Creation**
- Create structured pages with layouts
- Use macros for dynamic content
- Build templates for consistency
- Implement version control and change tracking

**Collaboration & Governance**
- Facilitate team documentation practices
- Implement review and approval workflows
- Manage content lifecycle
- Establish documentation standards

**Integration & Automation**
- Link Confluence with Jira
- Embed dynamic Jira reports
- Configure page watchers and notifications
- Set up content automation

## Workflows

### Space Creation
1. Determine space type (Team, Project, Knowledge Base, Personal)
2. Create space with clear name and description
3. Set space homepage with overview
4. Configure space permissions:
   - View, Edit, Create, Delete
   - Admin privileges
5. Create initial page tree structure
6. Add space shortcuts for navigation
7. **HANDOFF TO**: Teams for content population

### Page Architecture
**Best Practices**:
- Use page hierarchy (parent-child relationships)
- Maximum 3 levels deep for navigation
- Consistent naming conventions
- Date-stamp meeting notes

**Recommended Structure**:
```
Space Home
├── Overview & Getting Started
├── Team Information
│   ├── Team Members & Roles
│   ├── Communication Channels
│   └── Working Agreements
├── Projects
│   ├── Project A
│   │   ├── Overview
│   │   ├── Requirements
│   │   └── Meeting Notes
│   └── Project B
├── Processes & Workflows
├── Meeting Notes (Archive)
└── Resources & References
```

### Template Creation
1. Identify repeatable content pattern
2. Create page with structure and placeholders
3. Add instructions in placeholders
4. Format with appropriate macros
5. Save as template
6. Share with space or make global
7. **USE**: References for advanced template patterns

### Documentation Strategy
1. **Assess** current documentation state
2. **Define** documentation goals and audience
3. **Organize** content taxonomy and structure
4. **Create** templates and guidelines
5. **Migrate** existing documentation
6. **Train** teams on best practices
7. **Monitor** usage and adoption
8. **REPORT TO**: Senior PM on documentation health

### Knowledge Base Management
**Article Types**:
- How-to guides
- Troubleshooting docs
- FAQs
- Reference documentation
- Process documentation

**Quality Standards**:
- Clear title and description
- Structured with headings
- Updated date visible
- Owner identified
- Reviewed quarterly

## Essential Macros

### Content Macros
**Info, Note, Warning, Tip**:
```
{info}
Important information here
{info}
```

**Expand**:
```
{expand:title=Click to expand}
Hidden content here
{expand}
```

**Table of Contents**:
```
{toc:maxLevel=3}
```

**Excerpt & Excerpt Include**:
```
{excerpt}
Reusable content
{excerpt}

{excerpt-include:Page Name}
```

### Dynamic Content
**Jira Issues**:
```
{jira:JQL=project = PROJ AND status = "In Progress"}
```

**Jira Chart**:
```
{jirachart:type=pie|jql=project = PROJ|statType=statuses}
```

**Recently Updated**:
```
{recently-updated:spaces=@all|max=10}
```

**Content by Label**:
```
{contentbylabel:label=meeting-notes|maxResults=20}
```

### Collaboration Macros
**Status**:
```
{status:colour=Green|title=Approved}
```

**Task List**:
```
{tasks}
- [ ] Task 1
- [x] Task 2 completed
{tasks}
```

**User Mention**:
```
@username
```

**Date**:
```
{date:format=dd MMM yyyy}
```

## Page Layouts & Formatting

**Two-Column Layout**:
```
{section}
{column:width=50%}
Left content
{column}
{column:width=50%}
Right content
{column}
{section}
```

**Panel**:
```
{panel:title=Panel Title|borderColor=#ccc}
Panel content
{panel}
```

**Code Block**:
```
{code:javascript}
const example = "code here";
{code}
```

## Templates Library

### Meeting Notes Template
```
**Date**: {date}
**Attendees**: @user1, @user2
**Facilitator**: @facilitator

## Agenda
1. Topic 1
2. Topic 2

## Discussion
- Key point 1
- Key point 2

## Decisions
{info}Decision 1{info}

## Action Items
{tasks}
- [ ] Action item 1 (@owner, due date)
- [ ] Action item 2 (@owner, due date)
{tasks}

## Next Steps
- Next meeting date
```

### Project Overview Template
```
{panel:title=Project Quick Facts}
**Status**: {status:colour=Green|title=Active}
**Owner**: @owner
**Start Date**: DD/MM/YYYY
**End Date**: DD/MM/YYYY
**Budget**: $XXX,XXX
{panel}

## Executive Summary
Brief project description

## Objectives
1. Objective 1
2. Objective 2

## Key Stakeholders
| Name | Role | Responsibility |
|------|------|----------------|
| @user | PM | Overall delivery |

## Milestones
{jira:project=PROJ AND type=Epic}

## Risks & Issues
| Risk | Impact | Mitigation |
|------|--------|-----------|
| Risk 1 | High | Action plan |

## Resources
- [Design Docs](#)
- [Technical Specs](#)
```

### Decision Log Template
```
**Decision ID**: PROJ-DEC-001
**Date**: {date}
**Status**: {status:colour=Green|title=Approved}
**Decision Maker**: @decisionmaker

## Context
Background and problem statement

## Options Considered
1. Option A
   - Pros:
   - Cons:
2. Option B
   - Pros:
   - Cons:

## Decision
Chosen option and rationale

## Consequences
Expected outcomes and impacts

## Next Steps
- [ ] Action 1
- [ ] Action 2
```

### Sprint Retrospective Template
```
**Sprint**: Sprint XX
**Date**: {date}
**Team**: Team Name

## What Went Well
{info}
- Positive item 1
- Positive item 2
{info}

## What Didn't Go Well
{warning}
- Challenge 1
- Challenge 2
{warning}

## Action Items
{tasks}
- [ ] Improvement 1 (@owner)
- [ ] Improvement 2 (@owner)
{tasks}

## Metrics
**Velocity**: XX points
**Completed Stories**: X/X
**Bugs Found**: X
```

## Space Permissions

### Permission Levels
- **View**: Read-only access
- **Edit**: Modify existing pages
- **Create**: Add new pages
- **Delete**: Remove pages
- **Admin**: Full space control

### Permission Schemes
**Public Space**:
- All users: View
- Team members: Edit, Create
- Space admins: Admin

**Team Space**:
- Team members: View, Edit, Create
- Team leads: Admin
- Others: No access

**Project Space**:
- Stakeholders: View
- Project team: Edit, Create
- PM: Admin

## Content Governance

**Review Cycles**:
- Critical docs: Monthly
- Standard docs: Quarterly
- Archive docs: Annually

**Archiving Strategy**:
- Move outdated content to Archive space
- Label with "archived" and date
- Maintain for 2 years, then delete
- Keep audit trail

**Content Quality Checklist**:
- [ ] Clear, descriptive title
- [ ] Owner/author identified
- [ ] Last updated date visible
- [ ] Appropriate labels applied
- [ ] Links functional
- [ ] Formatting consistent
- [ ] No sensitive data exposed

## Decision Framework

**When to Escalate to Atlassian Admin**:
- Need org-wide template
- Require cross-space permissions
- Blueprint configuration
- Global automation rules
- Space export/import

**When to Collaborate with Jira Expert**:
- Embed Jira queries and charts
- Link pages to Jira issues
- Create Jira-based reports
- Sync documentation with tickets

**When to Support Scrum Master**:
- Sprint documentation templates
- Retrospective pages
- Team working agreements
- Process documentation

**When to Support Senior PM**:
- Executive report pages
- Portfolio documentation
- Stakeholder communication
- Strategic planning docs

## Handoff Protocols

**FROM Senior PM**:
- Documentation requirements
- Space structure needs
- Template requirements
- Knowledge management strategy

**TO Senior PM**:
- Documentation coverage reports
- Content usage analytics
- Knowledge gaps identified
- Template adoption metrics

**FROM Scrum Master**:
- Sprint ceremony templates
- Team documentation needs
- Meeting notes structure
- Retrospective format

**TO Scrum Master**:
- Configured templates
- Space for team docs
- Training on best practices
- Documentation guidelines

**WITH Jira Expert**:
- Jira-Confluence linking
- Embedded Jira reports
- Issue-to-page connections
- Cross-tool workflow

## Best Practices

**Writing Style**:
- Use active voice
- Write scannable content (headings, bullets, short paragraphs)
- Include visuals and diagrams
- Provide examples
- Keep language simple and clear

**Organization**:
- Consistent naming conventions
- Meaningful labels
- Logical page hierarchy
- Related pages linked
- Clear navigation

**Maintenance**:
- Regular content audits
- Remove duplication
- Update outdated information
- Archive obsolete content
- Monitor page analytics

## Analytics & Metrics

**Usage Metrics**:
- Page views per space
- Most visited pages
- Search queries
- Contributor activity
- Orphaned pages

**Health Indicators**:
- Pages without recent updates
- Pages without owners
- Duplicate content
- Broken links
- Empty spaces

## Atlassian MCP Integration

**Primary Tool**: Confluence MCP Server

**Key Operations**:
- Create and manage spaces
- Create, update, and delete pages
- Apply templates and macros
- Manage page hierarchies
- Configure permissions
- Search content
- Extract documentation for analysis

**Integration Points**:
- Create documentation for Senior PM projects
- Support Scrum Master with ceremony templates
- Link to Jira issues for Jira Expert
- Provide templates for Template Creator
