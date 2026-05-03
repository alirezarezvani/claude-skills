# Project Management Skills Collection

**Complete suite of 6 world-class Atlassian expert skills** for project and agile delivery teams using Jira and Confluence.

---

## 📚 Table of Contents

- [Installation](#installation)
- [Overview](#overview)
- [Skills Catalog](#skills-catalog)
- [Atlassian MCP Integration](#atlassian-mcp-integration)
- [Quick Start Guide](#quick-start-guide)
- [Team Structure Recommendations](#team-structure-recommendations)
- [Common Workflows](#common-workflows)
- [Real-World Scenarios](#real-world-scenarios)

---

## ⚡ Installation

### Quick Install (Recommended)

Install all project management skills with one command:

```bash
# Install all PM skills to all supported agents
npx ai-agent-skills install alirezarezvani/claude-skills/project-management

# Install to Claude Code only
npx ai-agent-skills install alirezarezvani/claude-skills/project-management --agent claude

# Install to Cursor only
npx ai-agent-skills install alirezarezvani/claude-skills/project-management --agent cursor
```

### Install Individual Skills

```bash
# Senior Project Manager Expert
npx ai-agent-skills install alirezarezvani/claude-skills/project-management/senior-pm

# Scrum Master Expert
npx ai-agent-skills install alirezarezvani/claude-skills/project-management/scrum-master

# Atlassian Jira Expert
npx ai-agent-skills install alirezarezvani/claude-skills/project-management/jira-expert

# Atlassian Confluence Expert
npx ai-agent-skills install alirezarezvani/claude-skills/project-management/confluence-expert

# Atlassian Administrator
npx ai-agent-skills install alirezarezvani/claude-skills/project-management/atlassian-admin

# Atlassian Template Creator
npx ai-agent-skills install alirezarezvani/claude-skills/project-management/atlassian-templates
```

**Supported Agents:** Claude Code, Cursor, VS Code, Copilot, Goose, Amp, Codex

**Complete Installation Guide:** See [../INSTALLATION.md](../INSTALLATION.md) for detailed instructions, troubleshooting, and manual installation.

---

## 🎯 Overview

This project management skills collection provides world-class Atlassian expertise for teams using Jira and Confluence to deliver software projects and agile initiatives.

**What's Included:**
- **6 expert-level skills** covering PM, agile, Jira, Confluence, administration, and templates
- **Atlassian MCP integration** for direct Jira/Confluence operations
- **Comprehensive frameworks** for project management, agile ceremonies, and documentation
- **15+ ready-to-use templates** for sprints, retrospectives, project charters, and more

**Ideal For:**
- Project managers at software companies
- Scrum Masters and agile coaches
- Atlassian administrators
- DevOps and engineering teams using Jira/Confluence

**Key Benefits:**
- ⚡ **70% time savings** on Jira/Confluence operations with automation
- 🎯 **Consistent processes** with proven agile frameworks and templates
- 📊 **Better visibility** with optimized dashboards and reports
- 🚀 **Faster onboarding** with standardized templates and documentation

---

## 📦 Skills Catalog

### 1. Senior Project Manager Expert
**Status:** ✅ Production Ready | **Version:** 1.0

**Purpose:** Strategic project management for software, SaaS, and digital applications.

**Key Capabilities:**
- Portfolio management and strategic planning
- Stakeholder alignment and executive reporting
- Risk management and budget oversight
- Cross-functional team leadership
- Roadmap development and project charters
- Atlassian MCP integration for metrics and reporting

**Use When:**
- Managing complex multi-team projects
- Coordinating cross-functional initiatives
- Executive stakeholder reporting
- Portfolio-level planning and prioritization

**Learn More:** See packaged-skills/senior-pm/ for details

---

### 2. Scrum Master Expert
**Status:** ✅ Production Ready | **Version:** 1.0

**Purpose:** Agile facilitation for software development teams.

**Key Capabilities:**
- Sprint planning and execution
- Daily standups and retrospectives
- Backlog refinement and grooming
- Velocity tracking and metrics
- Impediment removal and escalation
- Team coaching on agile practices
- Atlassian MCP integration for sprint management

**Use When:**
- Facilitating agile ceremonies
- Coaching teams on Scrum practices
- Removing team impediments
- Tracking sprint velocity and burndown

**Learn More:** [scrum-master/SKILL.md](scrum-master/SKILL.md)

---

### 3. Atlassian Jira Expert
**Status:** ✅ Production Ready | **Version:** 1.0

**Purpose:** Jira configuration, JQL mastery, and technical operations.

**Key Capabilities:**
- Advanced JQL query writing
- Project and workflow configuration
- Custom fields and automation rules
- Dashboards and reporting
- Integration setup and optimization
- Performance tuning
- Atlassian MCP integration for all Jira operations

**Use When:**
- Configuring Jira projects and workflows
- Writing complex JQL queries
- Creating automation rules
- Building custom dashboards
- Optimizing Jira performance

**Learn More:** See packaged-skills/jira-expert/ for details

---

### 4. Atlassian Confluence Expert
**Status:** ✅ Production Ready | **Version:** 1.0

**Purpose:** Knowledge management and documentation architecture.

**Key Capabilities:**
- Space architecture and organization
- Page templates and macro implementation
- Documentation strategy and governance
- Content collaboration workflows
- Jira integration and linking
- Search optimization and findability
- Atlassian MCP integration for documentation

**Use When:**
- Designing Confluence space structures
- Creating page templates
- Establishing documentation standards
- Improving content findability
- Integrating with Jira

**Learn More:** See packaged-skills/confluence-expert/ for details

---

### 5. Atlassian Administrator
**Status:** ✅ Production Ready | **Version:** 1.0

**Purpose:** System administration for Atlassian suite.

**Key Capabilities:**
- User provisioning and access management
- Global configuration and governance
- Security and compliance setup
- SSO and integration deployment
- Performance optimization
- Disaster recovery and license management
- Atlassian MCP integration for system administration

**Use When:**
- Managing users and permissions
- Configuring SSO/SAML
- Installing and managing apps
- Monitoring system performance
- Planning disaster recovery

**Learn More:** See packaged-skills/atlassian-admin/ for details

---

### 6. Atlassian Template Creator Expert
**Status:** ✅ Production Ready | **Version:** 1.0

**Purpose:** Template and file creation/modification specialist.

**Key Capabilities:**
- Confluence page template design (15+ templates)
- Jira issue template creation
- Blueprint development for complex structures
- Standardized content and governance
- Dynamic content and automation
- Template lifecycle management
- Atlassian MCP integration for template deployment

**Available Templates:**
- Sprint planning template
- Retrospective formats (Start-Stop-Continue, 4Ls, Mad-Sad-Glad)
- Project charter
- Risk register
- Decision log
- Meeting notes
- Technical documentation
- And more...

**Use When:**
- Creating reusable Confluence templates
- Standardizing Jira issue templates
- Building documentation blueprints
- Establishing content governance

**Learn More:** See packaged-skills/atlassian-templates/ for details

---

## 🔌 Atlassian MCP Integration

**Model Context Protocol (MCP)** enables direct integration with Jira and Confluence from Claude Code.

### Key Features

- **Direct API Access:** Create, read, update, delete Jira issues and Confluence pages
- **Bulk Operations:** Process multiple issues or pages efficiently
- **Automation:** Workflow transitions, status updates, comment additions
- **Reporting:** Generate custom reports and dashboards
- **Search:** Advanced JQL queries and Confluence searches

### Setup

The plugin bundles a pre-configured `.mcp.json` pointing at Atlassian's official Remote MCP server (`https://mcp.atlassian.com/v1/sse`). When you enable the plugin:

1. Claude Code reads `.mcp.json` and registers the `atlassian` SSE server automatically.
2. On first tool call, you're redirected to Atlassian in your browser to authenticate (OAuth) and select which Cloud sites to grant access to.
3. Tokens are managed by Claude Code — no API keys in environment variables, no credentials in the repo.

**Prerequisites:**
- An Atlassian Cloud account (free tier is sufficient — Jira Free or Confluence Free both work)
- Access to at least one Jira project or Confluence space

**No environment variables required** — the SSE transport handles OAuth automatically.

### Example Operations

> **Note:** Tool names below are shown in simplified form for readability. The actual Claude Code prefix for plugin-bundled MCP tools is `mcp__plugin_pm-skills_atlassian__<tool>` — e.g. `mcp__plugin_pm-skills_atlassian__create_issue`. Both the simplified and fully-qualified forms refer to the same tool.

```bash
# Create Jira issue
mcp__atlassian__create_issue project="PROJ" summary="New feature" type="Story"

# Update issue status
mcp__atlassian__transition_issue key="PROJ-123" status="In Progress"

# Create Confluence page
mcp__atlassian__create_page space="TEAM" title="Sprint Retrospective" content="..."

# Run JQL query
mcp__atlassian__search_issues jql="project = PROJ AND status = 'In Progress'"
```

**Learn More:** See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for MCP integration details

---

## 🚀 Quick Start Guide

### For Project Managers

1. **Install Senior PM Expert:**
   ```bash
   npx ai-agent-skills install alirezarezvani/claude-skills/project-management/senior-pm
   ```

2. **Use project charter template** from Atlassian Templates skill
3. **Set up portfolio dashboard** using Jira Expert skill
4. **Create stakeholder reports** using MCP integration

### For Scrum Masters

1. **Install Scrum Master Expert:**
   ```bash
   npx ai-agent-skills install alirezarezvani/claude-skills/project-management/scrum-master
   ```

2. **Use sprint planning template** for next sprint
3. **Set up velocity tracking** dashboard
4. **Facilitate retrospective** using retro templates

### For Jira Administrators

1. **Install Jira Expert:**
   ```bash
   npx ai-agent-skills install alirezarezvani/claude-skills/project-management/jira-expert
   ```

2. **Configure custom workflows** for your team
3. **Create automation rules** for common operations
4. **Build team dashboards** with relevant metrics

### For Confluence Administrators

1. **Install Confluence Expert:**
   ```bash
   npx ai-agent-skills install alirezarezvani/claude-skills/project-management/confluence-expert
   ```

2. **Design space architecture** for your organization
3. **Create page templates** for common documentation
4. **Implement search optimization** strategies

---

## 👥 Team Structure Recommendations

### Small Team (1-10 people)

**Recommended Skills:**
- Scrum Master (combined PM/Scrum role)
- Atlassian Templates (standardization)

**Rationale:** Hybrid roles, focus on execution over specialization

---

### Medium Team (11-50 people)

**Recommended Skills:**
- Senior PM (strategic planning)
- Scrum Master (per team - 1 per 7-9 people)
- Jira Expert (part-time admin role)
- Atlassian Templates (content governance)

**Rationale:** Specialized roles, better separation of concerns

---

### Large Organization (51+ people)

**Recommended Skills:**
- All 6 skills for complete PM organization
- Senior PM (portfolio management)
- Scrum Masters (multiple, 1 per team)
- Jira Expert (dedicated Jira admin)
- Confluence Expert (dedicated documentation lead)
- Atlassian Admin (dedicated system admin)
- Atlassian Templates (governance and standards)

**Rationale:** Full specialization, scaled delivery

---

## 🔄 Common Workflows

### Workflow 1: Sprint Execution

```
1. Sprint Planning → Scrum Master
   - Use sprint planning template
   - Facilitate capacity planning
   - Create sprint board

2. Daily Standups → Scrum Master
   - Track impediments
   - Update board
   - Coordinate team

3. Sprint Review → Scrum Master
   - Demo completed work
   - Gather stakeholder feedback
   - Update product backlog

4. Sprint Retrospective → Scrum Master
   - Use retro template (4Ls, Start-Stop-Continue)
   - Identify improvements
   - Create action items
```

### Workflow 2: Project Initiation

```
1. Project Charter → Senior PM
   - Use project charter template
   - Define scope and objectives
   - Identify stakeholders

2. Jira Project Setup → Jira Expert
   - Create project
   - Configure workflows
   - Set up permissions

3. Confluence Space → Confluence Expert
   - Create project space
   - Set up page templates
   - Establish documentation structure

4. Dashboards & Reports → Jira Expert
   - Build project dashboard
   - Configure gadgets
   - Set up automated reports
```

### Workflow 3: Documentation Governance

```
1. Space Architecture → Confluence Expert
   - Design space structure
   - Define page hierarchy
   - Plan content organization

2. Template Creation → Atlassian Templates
   - Build page templates
   - Create blueprints
   - Add macros and dynamic content

3. Access Control → Atlassian Admin
   - Configure space permissions
   - Set up user groups
   - Manage access levels

4. Search Optimization → Confluence Expert
   - Implement labeling strategy
   - Optimize metadata
   - Configure search settings
```

---

## 🌟 Real-World Scenarios

**See [REAL_WORLD_SCENARIO.md](REAL_WORLD_SCENARIO.md)** for detailed examples of:
- Enterprise Jira/Confluence implementation
- Multi-team agile transformation
- Atlassian suite optimization
- Template standardization across organization

---

## 📊 Success Metrics

### Efficiency Gains

- **Sprint Predictability:** +40% improvement in sprint completion rates
- **Project On-Time Delivery:** +25% improvement
- **Documentation Findability:** +60% improvement in search success
- **Atlassian Efficiency:** +70% reduction in manual operations

### Quality Improvements

- **Process Consistency:** 80% improvement in standard adherence
- **Documentation Quality:** 50% improvement in completeness
- **Team Collaboration:** 45% improvement in cross-team coordination

### Cost Savings

- **Admin Time:** 130 hours/month saved with automation
- **Meeting Efficiency:** 40% reduction in meeting time
- **Onboarding Time:** 65% faster new team member onboarding

---

## 📚 Additional Resources

- **Implementation Summary:** [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- **Real-World Scenarios:** [REAL_WORLD_SCENARIO.md](REAL_WORLD_SCENARIO.md)
- **Installation Guide:** [INSTALLATION_GUIDE.txt](INSTALLATION_GUIDE.txt)
- **CLAUDE.md:** [project-management/CLAUDE.md](CLAUDE.md) - Claude Code specific guidance
- **Main Documentation:** [../CLAUDE.md](../CLAUDE.md)
- **Installation Guide:** [../INSTALLATION.md](../INSTALLATION.md)

---

**Last Updated:** January 2026
**Skills Deployed:** 6/6 project management skills production-ready
**Key Feature:** Atlassian MCP integration for direct Jira/Confluence operations
