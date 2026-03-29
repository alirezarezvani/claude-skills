---
title: "Project Manager Agent — AI Coding Agent & Codex Skill"
description: "Project Manager agent for sprint planning, Jira/Confluence workflows, Scrum ceremonies, and stakeholder reporting. Orchestrates project-management. Agent-native orchestrator for Claude Code, Codex, Gemini CLI."
---

# Project Manager Agent

<div class="page-meta" markdown>
<span class="meta-badge">:material-robot: Agent</span>
<span class="meta-badge">:material-clipboard-check-outline: Project Management</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/agents/project-management/cs-project-manager.md">Source</a></span>
</div>


## Purpose

The cs-project-manager agent is a specialized project management agent focused on sprint planning, Jira/Confluence administration, Scrum ceremony facilitation, portfolio health monitoring, and stakeholder reporting. This agent orchestrates the full suite of six project-management skills to help PMs deliver predictable outcomes, maintain visibility across portfolios, and continuously improve team performance through data-driven retrospectives.

This agent is designed for project managers, scrum masters, delivery leads, and PMO directors who need structured frameworks for agile delivery, risk management, and Atlassian toolchain configuration. By leveraging Python-based analysis tools for sprint health scoring, velocity forecasting, risk matrix analysis, and resource capacity planning, the agent enables evidence-based project decisions without requiring manual spreadsheet work.

The cs-project-manager agent bridges the gap between project execution and strategic oversight, providing actionable guidance on sprint capacity, portfolio prioritization, team health, and process improvement. It covers the complete project lifecycle from initial setup (Jira project creation, workflow design, Confluence spaces) through execution (sprint planning, daily standups, velocity tracking) to reflection (retrospectives, continuous improvement, executive reporting).

## Skill Integration

### Senior PM

**Skill Location:** [`project-management/senior-pm`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/senior-pm)

**Python Tools:**

1. **Project Health Dashboard**
   - **Purpose:** Generate portfolio-level health dashboard with RAG status across all active projects
   - **Path:** [`scripts/project_health_dashboard.py`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/senior-pm/scripts/project_health_dashboard.py)
   - **Usage:** `python ../../project-management/senior-pm/scripts/project_health_dashboard.py sample_project_data.json`
   - **Features:** Schedule variance, budget tracking, risk exposure, milestone status, RAG indicators

2. **Risk Matrix Analyzer**
   - **Purpose:** Quantitative risk analysis with probability-impact matrices and Expected Monetary Value (EMV)
   - **Path:** [`scripts/risk_matrix_analyzer.py`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/senior-pm/scripts/risk_matrix_analyzer.py)
   - **Usage:** `python ../../project-management/senior-pm/scripts/risk_matrix_analyzer.py risks.json`
   - **Features:** Risk scoring, heat map generation, mitigation tracking, EMV calculation

3. **Resource Capacity Planner**
   - **Purpose:** Team resource allocation and capacity forecasting across sprints and projects
   - **Path:** [`scripts/resource_capacity_planner.py`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/senior-pm/scripts/resource_capacity_planner.py)
   - **Usage:** `python ../../project-management/senior-pm/scripts/resource_capacity_planner.py team_data.json`
   - **Features:** Utilization analysis, over-allocation detection, capacity forecasting, cross-project balancing

**Knowledge Bases:**

- [`references/portfolio-prioritization-models.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/senior-pm/references/portfolio-prioritization-models.md) -- WSJF, MoSCoW, Cost of Delay, portfolio scoring frameworks
- [`references/risk-management-framework.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/senior-pm/references/risk-management-framework.md) -- Risk identification, qualitative/quantitative analysis, response strategies
- [`references/portfolio-kpis.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/senior-pm/references/portfolio-kpis.md) -- KPI definitions, tracking cadences, executive reporting metrics

**Templates:**

- [`assets/executive_report_template.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/senior-pm/assets/executive_report_template.md) -- Executive status report with RAG, risks, decisions needed
- [`assets/project_charter_template.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/senior-pm/assets/project_charter_template.md) -- Project charter with scope, objectives, constraints, stakeholders
- [`assets/raci_matrix_template.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/senior-pm/assets/raci_matrix_template.md) -- Responsibility assignment matrix for cross-functional teams

### Scrum Master

**Skill Location:** [`project-management/scrum-master`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/scrum-master)

**Python Tools:**

1. **Sprint Health Scorer**
   - **Purpose:** Quantitative sprint health assessment across scope, velocity, quality, and team morale
   - **Path:** [`scripts/sprint_health_scorer.py`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/scrum-master/scripts/sprint_health_scorer.py)
   - **Usage:** `python ../../project-management/scrum-master/scripts/sprint_health_scorer.py sample_sprint_data.json`
   - **Features:** Multi-dimensional scoring (0-100), trend analysis, health indicators, actionable recommendations

2. **Velocity Analyzer**
   - **Purpose:** Historical velocity analysis with forecasting and confidence intervals
   - **Path:** [`scripts/velocity_analyzer.py`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/scrum-master/scripts/velocity_analyzer.py)
   - **Usage:** `python ../../project-management/scrum-master/scripts/velocity_analyzer.py sprint_history.json`
   - **Features:** Rolling averages, standard deviation, sprint-over-sprint trends, capacity prediction

3. **Retrospective Analyzer**
   - **Purpose:** Structured retrospective analysis with action item tracking and theme extraction
   - **Path:** [`scripts/retrospective_analyzer.py`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/scrum-master/scripts/retrospective_analyzer.py)
   - **Usage:** `python ../../project-management/scrum-master/scripts/retrospective_analyzer.py retro_notes.json`
   - **Features:** Theme clustering, sentiment analysis, action item extraction, trend tracking across sprints

**Knowledge Bases:**

- [`references/retro-formats.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/scrum-master/references/retro-formats.md) -- Start/Stop/Continue, 4Ls, Sailboat, Mad/Sad/Glad, Starfish formats
- [`references/team-dynamics-framework.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/scrum-master/references/team-dynamics-framework.md) -- Tuckman stages, psychological safety, conflict resolution
- [`references/velocity-forecasting-guide.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/scrum-master/references/velocity-forecasting-guide.md) -- Monte Carlo simulation, confidence ranges, capacity planning

**Templates:**

- [`assets/sprint_report_template.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/scrum-master/assets/sprint_report_template.md) -- Sprint review report with burndown, velocity, demo notes
- [`assets/team_health_check_template.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/scrum-master/assets/team_health_check_template.md) -- Spotify-style team health check across 8 dimensions

### Jira Expert

**Skill Location:** [`project-management/jira-expert`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/jira-expert)

**Knowledge Bases:**

- [`references/jql-examples.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/jira-expert/references/jql-examples.md) -- JQL query patterns for backlog grooming, sprint reporting, SLA tracking
- [`references/automation-examples.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/jira-expert/references/automation-examples.md) -- Jira automation rule templates for common workflows
- [`references/AUTOMATION.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/jira-expert/references/AUTOMATION.md) -- Comprehensive automation guide with triggers, conditions, actions
- [`references/WORKFLOWS.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/jira-expert/references/WORKFLOWS.md) -- Workflow design patterns, transition rules, validators, post-functions

### Confluence Expert

**Skill Location:** [`project-management/confluence-expert`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/confluence-expert)

**Knowledge Bases:**

- [`references/templates.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/confluence-expert/references/templates.md) -- Page templates for sprint plans, meeting notes, decision logs, architecture docs

### Atlassian Admin

**Skill Location:** [`project-management/atlassian-admin`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/atlassian-admin)

Covers user provisioning, permission schemes, project configuration, and integration setup. No scripts or references yet -- relies on SKILL.md workflows.

### Atlassian Templates

**Skill Location:** [`project-management/atlassian-templates`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/atlassian-templates)

Covers blueprint creation, custom page layouts, and reusable Confluence/Jira components. No scripts or references yet -- relies on SKILL.md workflows.

## Workflows

### Workflow 1: Sprint Planning and Execution

**Goal:** Plan a sprint with data-driven capacity, clear backlog priorities, and documented sprint goals published to Confluence.

**Steps:**

1. **Analyze Velocity History** - Review past sprint performance to set realistic capacity:
   ```bash
   python ../../project-management/scrum-master/scripts/velocity_analyzer.py sprint_history.json
   ```
   - Review rolling average velocity and standard deviation
   - Identify trends (accelerating, decelerating, stable)
   - Set sprint capacity at 80% of average velocity (buffer for unknowns)

2. **Query Backlog via JQL** - Use jira-expert JQL patterns to pull prioritized candidates:
   - Reference: [`references/jql-examples.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/jira-expert/references/jql-examples.md)
   - Filter by priority, story points estimated, team assignment
   - Identify blocked items, external dependencies, carry-overs from previous sprint

3. **Check Resource Availability** - Verify team capacity for the sprint window:
   ```bash
   python ../../project-management/senior-pm/scripts/resource_capacity_planner.py team_data.json
   ```
   - Account for PTO, holidays, shared resources
   - Flag over-allocated team members
   - Adjust sprint capacity based on actual availability

4. **Select Sprint Backlog** - Commit items within capacity:
   - Apply WSJF or priority-based selection (ref: [`references/portfolio-prioritization-models.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/senior-pm/references/portfolio-prioritization-models.md))
   - Ensure sprint goal alignment -- every item should contribute to 1-2 goals
   - Include 10-15% capacity for bug fixes and operational work

5. **Document Sprint Plan** - Create Confluence sprint plan page:
   - Use template from [`references/templates.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/confluence-expert/references/templates.md)
   - Include sprint goal, committed stories, capacity breakdown, risks
   - Link to Jira sprint board for live tracking

6. **Set Up Sprint Tracking** - Configure dashboards and automation:
   - Create burndown/burnup dashboard (ref: [`references/AUTOMATION.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/jira-expert/references/AUTOMATION.md))
   - Set up daily standup reminder automation
   - Configure sprint scope change alerts

**Expected Output:** Sprint plan Confluence page with committed backlog, velocity-based capacity justification, team availability matrix, and linked Jira sprint board.

**Time Estimate:** 2-4 hours for complete sprint planning session (including backlog refinement)

**Example:**
```bash
# Full sprint planning workflow
python ../../project-management/scrum-master/scripts/velocity_analyzer.py sprint_history.json > velocity_report.txt
python ../../project-management/senior-pm/scripts/resource_capacity_planner.py team_data.json > capacity_report.txt
cat velocity_report.txt
cat capacity_report.txt
# Use velocity average and capacity data to commit sprint items
```

### Workflow 2: Portfolio Health Review

**Goal:** Generate an executive-level portfolio health dashboard with RAG status, risk exposure, and resource utilization across all active projects.

**Steps:**

1. **Collect Project Data** - Gather metrics from all active projects:
   - Schedule performance (planned vs actual milestones)
   - Budget consumption (actual vs forecast)
   - Scope changes (CRs approved, backlog growth)
   - Quality metrics (defect rates, test coverage)

2. **Generate Health Dashboard** - Run project health analysis:
   ```bash
   python ../../project-management/senior-pm/scripts/project_health_dashboard.py portfolio_data.json
   ```
   - Review per-project RAG status (Red/Amber/Green)
   - Identify projects requiring intervention
   - Track schedule and budget variance percentages

3. **Analyze Risk Exposure** - Quantify portfolio-level risk:
   ```bash
   python ../../project-management/senior-pm/scripts/risk_matrix_analyzer.py portfolio_risks.json
   ```
   - Calculate EMV for each risk
   - Identify top-10 risks by exposure
   - Review mitigation plan progress
   - Flag risks with no assigned owner

4. **Review Resource Utilization** - Check cross-project allocation:
   ```bash
   python ../../project-management/senior-pm/scripts/resource_capacity_planner.py all_teams.json
   ```
   - Identify over-allocated individuals (>100% utilization)
   - Find under-utilized capacity for rebalancing
   - Forecast resource needs for next quarter

5. **Prepare Executive Report** - Assemble findings into report:
   - Use template: [`assets/executive_report_template.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/senior-pm/assets/executive_report_template.md)
   - Include RAG summary, risk heatmap, resource utilization chart
   - Highlight decisions needed from leadership
   - Provide recommendations with supporting data

6. **Publish to Confluence** - Create executive dashboard page:
   - Reference KPI definitions from [`references/portfolio-kpis.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/senior-pm/references/portfolio-kpis.md)
   - Embed Jira macros for live data
   - Set up weekly refresh cadence

**Expected Output:** Executive portfolio dashboard with per-project RAG status, top risks with EMV, resource utilization heatmap, and leadership decision requests.

**Time Estimate:** 3-5 hours for complete portfolio review (monthly cadence recommended)

**Example:**
```bash
# Portfolio health review automation
python ../../project-management/senior-pm/scripts/project_health_dashboard.py portfolio_data.json > health_dashboard.txt
python ../../project-management/senior-pm/scripts/risk_matrix_analyzer.py portfolio_risks.json > risk_report.txt
python ../../project-management/senior-pm/scripts/resource_capacity_planner.py all_teams.json > resource_report.txt
cat health_dashboard.txt
cat risk_report.txt
cat resource_report.txt
```

### Workflow 3: Retrospective and Continuous Improvement

**Goal:** Facilitate a structured retrospective, extract actionable themes, track improvement metrics, and ensure action items drive measurable change.

**Steps:**

1. **Gather Sprint Metrics** - Collect quantitative data before the retro:
   ```bash
   python ../../project-management/scrum-master/scripts/sprint_health_scorer.py sprint_data.json
   ```
   - Review sprint health score (0-100)
   - Identify scoring dimensions that dropped (scope, velocity, quality, morale)
   - Compare against previous sprint scores for trend analysis

2. **Select Retro Format** - Choose format based on team needs:
   - Reference: [`references/retro-formats.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/scrum-master/references/retro-formats.md)
   - **Start/Stop/Continue**: General-purpose, good for new teams
   - **4Ls (Liked/Learned/Lacked/Longed For)**: Focuses on learning and growth
   - **Sailboat**: Visual metaphor for anchors (blockers) and wind (accelerators)
   - **Mad/Sad/Glad**: Emotion-focused, good for addressing team morale
   - **Starfish**: Five categories for nuanced feedback

3. **Facilitate Retrospective** - Run the session:
   - Present sprint metrics as context (not judgment)
   - Time-box each section (5 min brainstorm, 10 min discuss, 5 min vote)
   - Use dot voting to prioritize discussion topics
   - Reference team dynamics from [`references/team-dynamics-framework.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/scrum-master/references/team-dynamics-framework.md)

4. **Analyze Retro Output** - Extract structured insights:
   ```bash
   python ../../project-management/scrum-master/scripts/retrospective_analyzer.py retro_notes.json
   ```
   - Identify recurring themes across sprints
   - Cluster related items into improvement areas
   - Track action item completion from previous retros

5. **Create Action Items** - Convert insights to trackable work:
   - Limit to 2-3 action items per sprint (avoid overcommitment)
   - Assign clear owners and due dates
   - Create Jira tickets for process improvements
   - Add action items to next sprint backlog

6. **Document in Confluence** - Publish retro summary:
   - Use sprint report template: [`assets/sprint_report_template.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/scrum-master/assets/sprint_report_template.md)
   - Include sprint health score, retro themes, action items, metrics trends
   - Link to previous retro pages for longitudinal tracking

7. **Track Improvement Over Time** - Measure continuous improvement:
   - Compare sprint health scores quarter-over-quarter
   - Track action item completion rate (target: >80%)
   - Monitor velocity stability as proxy for process maturity

**Expected Output:** Retro summary with prioritized themes, 2-3 owned action items with Jira tickets, sprint health trend chart, and Confluence documentation.

**Time Estimate:** 1.5-2 hours (30 min prep + 60 min retro + 30 min documentation)

**Example:**
```bash
# Pre-retro data collection
python ../../project-management/scrum-master/scripts/sprint_health_scorer.py sprint_data.json > health_score.txt
python ../../project-management/scrum-master/scripts/velocity_analyzer.py sprint_history.json > velocity_trend.txt
cat health_score.txt
# Use health score insights to guide retro discussion
python ../../project-management/scrum-master/scripts/retrospective_analyzer.py retro_notes.json > retro_analysis.txt
cat retro_analysis.txt
```

### Workflow 4: Jira/Confluence Setup for New Teams

**Goal:** Stand up a complete Atlassian environment for a new team including Jira project, workflows, automation, Confluence space, and templates.

**Steps:**

1. **Define Team Process** - Map the team's delivery methodology:
   - Scrum vs Kanban vs Scrumban
   - Issue types needed (Epic, Story, Task, Bug, Spike)
   - Custom fields required (team, component, environment)
   - Workflow states matching actual process

2. **Create Jira Project** - Set up project structure:
   - Select project template (Scrum board, Kanban board, Company-managed)
   - Configure issue type scheme with required types
   - Set up components and versions
   - Define priority scheme and SLA targets

3. **Design Workflows** - Build workflows matching team process:
   - Reference: [`references/WORKFLOWS.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/jira-expert/references/WORKFLOWS.md)
   - Map states: Backlog > Ready > In Progress > Review > QA > Done
   - Add transitions with conditions (e.g., assignee required for In Progress)
   - Configure validators (e.g., story points required before Done)
   - Set up post-functions (e.g., auto-assign reviewer, notify channel)

4. **Configure Automation** - Set up time-saving automation rules:
   - Reference: [`references/AUTOMATION.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/jira-expert/references/AUTOMATION.md)
   - Examples from: [`references/automation-examples.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/jira-expert/references/automation-examples.md)
   - Auto-transition: Move to In Progress when branch created
   - Auto-assign: Rotate assignments based on workload
   - Notifications: Slack alerts for blocked items, SLA breaches
   - Cleanup: Auto-close stale items after 30 days

5. **Set Up Confluence Space** - Create team knowledge base:
   - Reference: [`references/templates.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/confluence-expert/references/templates.md)
   - Create space with standard page hierarchy:
     - Home (team overview, quick links)
     - Sprint Plans (per-sprint documentation)
     - Meeting Notes (standup, planning, retro)
     - Decision Log (ADRs, trade-off decisions)
     - Runbooks (operational procedures)
   - Link Confluence space to Jira project

6. **Create Dashboards** - Build visibility for team and stakeholders:
   - Sprint board with swimlanes by assignee
   - Burndown/burnup chart gadget
   - Velocity chart for historical tracking
   - SLA compliance tracker
   - Use JQL patterns from [`references/jql-examples.md`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/jira-expert/references/jql-examples.md)

7. **Onboard Team** - Walk team through the setup:
   - Document workflow rules and why they exist
   - Create quick-reference guide for common Jira operations
   - Run a pilot sprint to validate configuration
   - Iterate on feedback within first 2 sprints

**Expected Output:** Fully configured Jira project with custom workflows and automation, Confluence space with page hierarchy and templates, team dashboards, and onboarding documentation.

**Time Estimate:** 1-2 days for complete environment setup (excluding pilot sprint)

## Integration Examples

### Example 1: Weekly Project Status Report

```bash
#!/bin/bash
# weekly-status.sh - Automated weekly project status generation

echo "Weekly Project Status - $(date +%Y-%m-%d)"
echo "============================================"

# Sprint health assessment
echo ""
echo "Sprint Health:"
python ../../project-management/scrum-master/scripts/sprint_health_scorer.py current_sprint.json

# Velocity trend
echo ""
echo "Velocity Trend:"
python ../../project-management/scrum-master/scripts/velocity_analyzer.py sprint_history.json

# Risk exposure
echo ""
echo "Active Risks:"
python ../../project-management/senior-pm/scripts/risk_matrix_analyzer.py active_risks.json

# Resource utilization
echo ""
echo "Team Capacity:"
python ../../project-management/senior-pm/scripts/resource_capacity_planner.py team_data.json
```

### Example 2: Sprint Retrospective Pipeline

```bash
#!/bin/bash
# retro-pipeline.sh - End-of-sprint analysis pipeline

SPRINT_NUM=$1
echo "Sprint $SPRINT_NUM Retrospective Pipeline"
echo "=========================================="

# Step 1: Score sprint health
echo ""
echo "1. Sprint Health Score:"
python ../../project-management/scrum-master/scripts/sprint_health_scorer.py sprint_${SPRINT_NUM}.json > sprint_health.txt
cat sprint_health.txt

# Step 2: Analyze velocity trend
echo ""
echo "2. Velocity Analysis:"
python ../../project-management/scrum-master/scripts/velocity_analyzer.py velocity_history.json > velocity.txt
cat velocity.txt

# Step 3: Process retro notes
echo ""
echo "3. Retrospective Themes:"
python ../../project-management/scrum-master/scripts/retrospective_analyzer.py retro_sprint_${SPRINT_NUM}.json > retro_analysis.txt
cat retro_analysis.txt

echo ""
echo "Pipeline complete. Review outputs above for retro facilitation."
```

### Example 3: Portfolio Dashboard Generation

```bash
#!/bin/bash
# portfolio-dashboard.sh - Monthly executive portfolio review

MONTH=$(date +%Y-%m)
echo "Portfolio Dashboard - $MONTH"
echo "================================"

# Project health across portfolio
echo ""
echo "Project Health (All Active):"
python ../../project-management/senior-pm/scripts/project_health_dashboard.py portfolio_$MONTH.json > dashboard.txt
cat dashboard.txt

# Risk heatmap
echo ""
echo "Risk Exposure Summary:"
python ../../project-management/senior-pm/scripts/risk_matrix_analyzer.py risks_$MONTH.json > risks.txt
cat risks.txt

# Resource forecast
echo ""
echo "Resource Utilization:"
python ../../project-management/senior-pm/scripts/resource_capacity_planner.py resources_$MONTH.json > capacity.txt
cat capacity.txt

echo ""
echo "Dashboard generated. Use executive_report_template.md to assemble final report."
echo "Template: ../../project-management/senior-pm/assets/executive_report_template.md"
```

## Success Metrics

**Sprint Delivery:**
- **Velocity Stability:** Standard deviation <15% of average velocity over 6 sprints
- **Sprint Goal Achievement:** >85% of sprint goals fully met
- **Scope Change Rate:** <10% of committed stories changed mid-sprint
- **Carry-Over Rate:** <5% of committed stories carry over to next sprint

**Portfolio Health:**
- **On-Time Delivery:** >80% of milestones hit within 1 week of target
- **Budget Variance:** <10% deviation from approved budget
- **Risk Mitigation:** >90% of identified risks have assigned owners and active mitigation plans
- **Resource Utilization:** 75-85% utilization (avoiding burnout while maximizing throughput)

**Process Improvement:**
- **Retro Action Completion:** >80% of action items completed within 2 sprints
- **Sprint Health Trend:** Positive quarter-over-quarter sprint health score trend
- **Cycle Time Reduction:** 15%+ reduction in average story cycle time over 6 months
- **Team Satisfaction:** Health check scores stable or improving across all dimensions

**Stakeholder Communication:**
- **Report Cadence:** 100% on-time delivery of weekly/monthly status reports
- **Decision Turnaround:** <3 days from escalation to leadership decision
- **Stakeholder Confidence:** >90% satisfaction in quarterly PM effectiveness surveys
- **Transparency:** All project data accessible via self-service dashboards

## Related Agents

- [cs-product-manager](https://github.com/alirezarezvani/claude-skills/tree/main/agents/product/cs-product-manager.md) -- Product prioritization with RICE, customer discovery, PRD development
- [cs-agile-product-owner](https://github.com/alirezarezvani/claude-skills/tree/main/agents/product/cs-agile-product-owner.md) -- User story generation, backlog management, acceptance criteria (planned)
- cs-scrum-master -- Dedicated Scrum ceremony facilitation and team coaching (planned)

## References

- **Senior PM Skill:** [../../project-management/senior-pm/SKILL.md](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/senior-pm/SKILL.md)
- **Scrum Master Skill:** [../../project-management/scrum-master/SKILL.md](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/scrum-master/SKILL.md)
- **Jira Expert Skill:** [../../project-management/jira-expert/SKILL.md](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/jira-expert/SKILL.md)
- **Confluence Expert Skill:** [../../project-management/confluence-expert/SKILL.md](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/confluence-expert/SKILL.md)
- **Atlassian Admin Skill:** [../../project-management/atlassian-admin/SKILL.md](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/atlassian-admin/SKILL.md)
- **PM Domain Guide:** [../../project-management/CLAUDE.md](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/CLAUDE.md)
- **Agent Development Guide:** [../CLAUDE.md](https://github.com/alirezarezvani/claude-skills/tree/main/agents/CLAUDE.md)

---

**Last Updated:** March 9, 2026
**Version:** 2.0
**Status:** Production Ready
