---
name: cto-advisor
description: Strategic technology leadership skill providing frameworks for architecture decisions, team scaling, technical debt management, technology evaluation, and engineering metrics. Use when making technology strategy decisions, evaluating vendors, scaling engineering teams, managing technical debt, establishing engineering KPIs, or creating architecture decision records.
---

# CTO Advisor

Strategic frameworks and tools for technology leadership, team scaling, and engineering excellence.

## Quick Start

### For Technical Debt Assessment
```bash
python scripts/tech_debt_analyzer.py
```
Analyzes system architecture and provides prioritized debt reduction plan.

### For Team Scaling Planning
```bash
python scripts/team_scaling_calculator.py
```
Calculates optimal hiring plan and team structure for growth.

### For Architecture Decisions
Review `references/architecture_decision_records.md` for ADR templates and examples.

### For Technology Evaluation
Use framework in `references/technology_evaluation_framework.md` for vendor selection.

### For Engineering Metrics
Implement KPIs from `references/engineering_metrics.md` for team performance tracking.

## Core Responsibilities

### 1. Technology Strategy

#### Vision & Roadmap
- Define 3-5 year technology vision
- Create quarterly roadmaps
- Align with business strategy
- Communicate to stakeholders

#### Innovation Management
- Allocate 20% time for innovation
- Run hackathons quarterly
- Evaluate emerging technologies
- Build proof of concepts

#### Technical Debt Strategy
```bash
# Assess current debt
python scripts/tech_debt_analyzer.py

# Allocate capacity
- Critical debt: 40% capacity
- High debt: 25% capacity  
- Medium debt: 15% capacity
- Low debt: Ongoing maintenance
```

### 2. Team Leadership

#### Scaling Engineering
```bash
# Calculate scaling needs
python scripts/team_scaling_calculator.py

# Key ratios to maintain:
- Manager:Engineer = 1:8
- Senior:Mid:Junior = 3:4:2
- Product:Engineering = 1:10
- QA:Engineering = 1.5:10
```

#### Performance Management
- Set clear OKRs quarterly
- Conduct 1:1s weekly
- Review performance quarterly
- Provide growth opportunities

#### Culture Building
- Define engineering values
- Establish coding standards
- Create learning programs
- Foster collaboration

### 3. Architecture Governance

#### Decision Making
Use ADR template from `references/architecture_decision_records.md`:
1. Document context and problem
2. List all options considered
3. Record decision and rationale
4. Track consequences

#### Technology Standards
- Language choices
- Framework selection
- Database standards
- Security requirements
- API design guidelines

#### System Design Review
- Weekly architecture reviews
- Design documentation standards
- Prototype requirements
- Performance criteria

### 4. Vendor Management

#### Evaluation Process
Follow framework in `references/technology_evaluation_framework.md`:
1. Gather requirements (Week 1)
2. Market research (Week 1-2)
3. Deep evaluation (Week 2-4)
4. Decision and documentation (Week 4)

#### Vendor Relationships
- Quarterly business reviews
- SLA monitoring
- Cost optimization
- Strategic partnerships

### 5. Engineering Excellence

#### Metrics Implementation
From `references/engineering_metrics.md`:

**DORA Metrics** (Deploy to production targets):
- Deployment Frequency: >1/day
- Lead Time: <1 day
- MTTR: <1 hour
- Change Failure Rate: <15%

**Quality Metrics**:
- Test Coverage: >80%
- Code Review: 100%
- Technical Debt: <10%

**Team Health**:
- Sprint Velocity: ±10% variance
- Unplanned Work: <20%
- On-call Incidents: <5/week

## Weekly Cadence

### Monday
- Leadership team sync
- Review metrics dashboard
- Address escalations

### Tuesday
- Architecture review
- Technical interviews
- 1:1s with directs

### Wednesday
- Cross-functional meetings
- Vendor meetings
- Strategy work

### Thursday
- Team all-hands (monthly)
- Sprint reviews (bi-weekly)
- Technical deep dives

### Friday
- Strategic planning
- Innovation time
- Week recap and planning

## Quarterly Planning

### Q1 Focus: Foundation
- Annual planning
- Budget allocation
- Team goal setting
- Technology assessment

### Q2 Focus: Execution
- Major initiatives launch
- Mid-year hiring push
- Performance reviews
- Architecture evolution

### Q3 Focus: Innovation
- Hackathon
- Technology exploration
- Team development
- Process optimization

### Q4 Focus: Planning
- Next year strategy
- Budget planning
- Promotion cycles
- Debt reduction sprint

## Crisis Management

### Incident Response
1. **Immediate** (0-15 min):
   - Assess severity
   - Activate incident team
   - Begin communication

2. **Short-term** (15-60 min):
   - Implement fixes
   - Update stakeholders
   - Monitor systems

3. **Resolution** (1-24 hours):
   - Verify fix
   - Document timeline
   - Customer communication

4. **Post-mortem** (48-72 hours):
   - Root cause analysis
   - Action items
   - Process improvements

### Types of Crises

#### Security Breach
- Isolate affected systems
- Engage security team
- Legal/compliance notification
- Customer communication plan

#### Major Outage
- All-hands response
- Status page updates
- Executive briefings
- Customer outreach

#### Data Loss
- Stop writes immediately
- Assess recovery options
- Begin restoration
- Impact analysis

## Stakeholder Management

### Board/Executive Reporting
**Monthly**:
- KPI dashboard
- Risk register
- Major initiatives status

**Quarterly**:
- Technology strategy update
- Team growth and health
- Innovation highlights
- Budget review

### Cross-functional Partners

#### Product Team
- Weekly roadmap sync
- Sprint planning participation
- Technical feasibility reviews
- Feature estimation

#### Sales/Marketing
- Technical sales support
- Product capability briefings
- Customer reference calls
- Competitive analysis

#### Finance
- Budget management
- Cost optimization
- Vendor negotiations
- Capex planning

## Strategic Initiatives

### Digital Transformation
1. Assess current state
2. Define target architecture
3. Create migration plan
4. Execute in phases
5. Measure and adjust

### Cloud Migration
1. Application assessment
2. Migration strategy (7Rs)
3. Pilot applications
4. Full migration
5. Optimization

### Platform Engineering
1. Define platform vision
2. Build core services
3. Create self-service tools
4. Enable team adoption
5. Measure efficiency

### AI/ML Integration
1. Identify use cases
2. Build data infrastructure
3. Develop models
4. Deploy and monitor
5. Scale adoption

## Communication Templates

### Technology Strategy Presentation
```
1. Executive Summary (1 slide)
2. Current State Assessment (2 slides)
3. Vision & Strategy (2 slides)
4. Roadmap & Milestones (3 slides)
5. Investment Required (1 slide)
6. Risks & Mitigation (1 slide)
7. Success Metrics (1 slide)
```

### Team All-hands
```
1. Wins & Recognition (5 min)
2. Metrics Review (5 min)
3. Strategic Updates (10 min)
4. Demo/Deep Dive (15 min)
5. Q&A (10 min)
```

### Board Update Email
```
Subject: Engineering Update - [Month]

Highlights:
• [Major achievement]
• [Key metric improvement]
• [Strategic progress]

Challenges:
• [Issue and mitigation]

Next Month:
• [Priority 1]
• [Priority 2]

Detailed metrics attached.
```

## Tools & Resources

### Essential Tools
- **Architecture**: Draw.io, Lucidchart, C4 Model
- **Metrics**: DataDog, Grafana, LinearB
- **Planning**: Jira, Confluence, Notion
- **Communication**: Slack, Zoom, Loom
- **Development**: GitHub, GitLab, Bitbucket

### Key Resources
- **Books**: 
  - "The Manager's Path" - Camille Fournier
  - "Accelerate" - Nicole Forsgren
  - "Team Topologies" - Skelton & Pais
  
- **Frameworks**:
  - DORA metrics
  - SPACE framework
  - Team Topologies
  
- **Communities**:
  - CTO Craft
  - Engineering Leadership Slack
  - LeadDev community

## Success Indicators

✅ **Technical Excellence**
- System uptime >99.9%
- Deploy multiple times daily
- Technical debt <10% capacity
- Security incidents = 0

✅ **Team Success**
- Team satisfaction >8/10
- Attrition <10%
- Filled positions >90%
- Diversity improving

✅ **Business Impact**
- Features on-time >80%
- Engineering enables revenue
- Cost per transaction decreasing
- Innovation driving growth

## Red Flags to Watch

⚠️ Increasing technical debt  
⚠️ Rising attrition rate  
⚠️ Slowing velocity  
⚠️ Growing incidents  
⚠️ Team morale declining  
⚠️ Budget overruns  
⚠️ Vendor dependencies  
⚠️ Security vulnerabilities
