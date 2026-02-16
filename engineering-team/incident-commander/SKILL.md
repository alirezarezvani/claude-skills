---
name: incident-commander
description: Production incident management with structured timeline analysis, severity classification (SEV1-4), automated postmortem generation, and SLA tracking. Features communication templates, escalation routing, 5-Whys root cause analysis, and MTTR/MTTD metrics for high-reliability engineering teams.
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: engineering
  domain: site-reliability
  updated: 2026-02-16
  python-tools: incident_timeline_builder.py, severity_classifier.py, postmortem_generator.py
  tech-stack: incident-management, sre, on-call, postmortem-analysis
---

# Incident Commander Expert

Advanced incident management specializing in structured response coordination, severity-driven escalation, postmortem excellence, and SLA compliance. Combines PagerDuty/Google SRE/Atlassian incident management frameworks with quantitative reliability metrics for high-performance engineering organizations.

---

## Table of Contents

- [Capabilities](#capabilities)
- [Input Requirements](#input-requirements)
- [Analysis Tools](#analysis-tools)
- [Methodology](#methodology)
- [Templates & Assets](#templates--assets)
- [Reference Frameworks](#reference-frameworks)
- [Implementation Workflows](#implementation-workflows)
- [Assessment & Measurement](#assessment--measurement)
- [Best Practices](#best-practices)
- [Advanced Techniques](#advanced-techniques)
- [Limitations & Considerations](#limitations--considerations)
- [Success Metrics & Outcomes](#success-metrics--outcomes)

---

## Capabilities

### Incident Timeline Intelligence
- **Structured Timeline Construction**: Chronological event assembly from detection through resolution with gap identification via `incident_timeline_builder.py`
- **Phase Duration Analysis**: Automated calculation of time-in-phase for Detection, Triage, Mitigation, and Resolution with bottleneck identification
- **Communication Log Correlation**: Maps status updates, escalation events, and stakeholder notifications against incident progression
- **Gap Detection**: Identifies periods of inactivity or missing log entries that indicate process failures or documentation gaps
- **Multi-Source Aggregation**: Consolidates events from monitoring alerts, Slack messages, PagerDuty pages, and manual entries into a unified timeline

### Severity Classification & Escalation
- **Impact-First Classification**: Four-tier severity model (SEV1-SEV4) driven by customer impact, revenue exposure, and data integrity risk via `severity_classifier.py`
- **Dynamic Re-Classification**: Continuous severity reassessment as incident scope changes, with automatic escalation triggers
- **Escalation Routing Matrix**: Role-based escalation paths with time-boxed response requirements per severity level
- **Blast Radius Estimation**: Quantitative assessment of affected users, services, and revenue based on incident metadata
- **SLA Threshold Mapping**: Automatic SLA timer activation and breach prediction based on classified severity

### Postmortem Excellence
- **Automated Report Generation**: Structured postmortem documents from incident data with timeline, impact summary, and root cause sections via `postmortem_generator.py`
- **5-Whys Root Cause Analysis**: Guided causal chain construction with depth validation and contributing factor identification
- **Action Item Extraction**: Automated identification of remediation tasks with priority scoring and ownership assignment
- **Pattern Recognition**: Cross-incident analysis to surface recurring failure modes and systemic weaknesses
- **Blameless Framing**: Language analysis to ensure postmortem narratives focus on systems and processes, not individuals

### SLA & Reliability Metrics
- **MTTR Tracking**: Mean Time to Resolve computed per severity level with trend analysis and target comparison
- **MTTD Monitoring**: Mean Time to Detect measuring observability effectiveness from incident onset to first alert
- **MTBF Calculation**: Mean Time Between Failures per service, providing reliability baselines for capacity planning
- **SLA Compliance Scoring**: Real-time compliance percentages against defined availability targets (99.9%, 99.95%, 99.99%)
- **Incident Frequency Analysis**: Trend detection in incident volume by severity, service, and time window

---

## Input Requirements

### Incident Data Structure
All analysis tools accept JSON input following this schema:

```json
{
  "incident": {
    "id": "INC-2026-0142",
    "title": "Payment processing service degradation",
    "severity": "SEV2",
    "status": "resolved",
    "commander": "Jane Chen",
    "declared_at": "2026-02-15T14:23:00Z",
    "resolved_at": "2026-02-15T16:47:00Z",
    "services_affected": ["payment-api", "checkout-frontend", "order-service"],
    "customer_impact": {
      "affected_users": 12400,
      "revenue_impact_usd": 84000,
      "data_integrity": false
    }
  },
  "timeline": [
    {
      "timestamp": "2026-02-15T14:18:00Z",
      "type": "alert",
      "source": "datadog",
      "description": "P95 latency > 2000ms on payment-api",
      "actor": "monitoring"
    },
    {
      "timestamp": "2026-02-15T14:23:00Z",
      "type": "declaration",
      "source": "slack",
      "description": "SEV2 declared by on-call engineer",
      "actor": "jane.chen"
    }
  ],
  "root_cause": {
    "summary": "Connection pool exhaustion due to upstream database failover",
    "category": "infrastructure",
    "five_whys": [
      "Payment API returned 503 errors",
      "Connection pool was exhausted (0/50 available)",
      "Database primary failed over to replica",
      "Replica promotion took 47 seconds, exceeding 10s pool timeout",
      "Failover health check interval was set to 30s instead of 5s"
    ]
  },
  "action_items": [
    {
      "id": "AI-001",
      "description": "Reduce database health check interval to 5 seconds",
      "priority": "P1",
      "owner": "platform-team",
      "due_date": "2026-02-22",
      "status": "open"
    }
  ],
  "sla": {
    "target_availability": 99.95,
    "downtime_minutes": 144,
    "monthly_budget_minutes": 21.6,
    "remaining_budget_minutes": -122.4
  }
}
```

### Minimum Data Requirements
- **Timeline Builder**: Incident ID, declared_at timestamp, and 2+ timeline events with timestamps
- **Severity Classifier**: Services affected, customer impact metrics (affected users OR revenue impact), and incident description
- **Postmortem Generator**: Complete incident record with timeline (5+ events recommended), root cause summary, and at least 1 action item
- **SLA Analysis**: Target availability percentage and incident duration; historical incident data for trend analysis (6+ incidents recommended)

---

## Analysis Tools

### Incident Timeline Builder (`scripts/incident_timeline_builder.py`)
Constructs structured, chronological incident timelines from raw event data with phase analysis and gap detection.

**Features**:
- Chronological event ordering with deduplication across sources
- Automatic phase classification (Detection, Triage, Mitigation, Resolution, Postmortem)
- Phase duration calculation with bottleneck identification
- Communication cadence analysis (flags gaps > 15 minutes during active incidents)
- Timeline gap detection for periods with no recorded activity
- Multi-format output (text table, JSON, markdown)

**Usage**:
```bash
# File input with text output
python scripts/incident_timeline_builder.py incident.json --format text

# File input with JSON output for downstream processing
python scripts/incident_timeline_builder.py incident.json --format json

# Stdin support for pipeline integration
cat incident.json | python scripts/incident_timeline_builder.py --format text

# Markdown output for postmortem documents
python scripts/incident_timeline_builder.py incident.json --format markdown

# Filter events by phase
python scripts/incident_timeline_builder.py incident.json --phase mitigation --format text
```

**Options**:
| Flag | Description | Default |
|------|-------------|---------|
| `--format` | Output format: `text`, `json`, `markdown` | `text` |
| `--phase` | Filter to specific phase: `detection`, `triage`, `mitigation`, `resolution` | all |
| `--gap-threshold` | Minutes of silence before flagging a gap | `15` |
| `--include-comms` | Include communication events in timeline | `true` |
| `--verbose` | Show phase duration breakdown and statistics | `false` |

**Output Description**:
- Ordered event list with timestamps, actors, sources, and phase tags
- Phase duration summary (e.g., "Triage: 12 minutes, Mitigation: 47 minutes")
- Communication cadence score (updates per 15-minute window)
- Gap warnings with recommended actions
- Total incident duration from first alert to resolution confirmation

### Severity Classifier (`scripts/severity_classifier.py`)
Impact-driven severity classification with escalation routing and SLA timer activation.

**Features**:
- Four-tier severity classification (SEV1-SEV4) based on quantitative impact thresholds
- Blast radius estimation: affected users, services, and revenue exposure
- Escalation path generation with role assignments and response time requirements
- SLA breach prediction based on current severity and elapsed time
- Re-classification recommendations when incident scope changes
- Confidence scoring for classification decisions

**Classification Thresholds**:
- **SEV1** (Critical): >50% users affected OR >$500K/hour revenue impact OR data breach OR complete service outage
- **SEV2** (Major): >10% users affected OR >$50K/hour revenue impact OR major feature unavailable
- **SEV3** (Minor): >1% users affected OR >$5K/hour revenue impact OR degraded performance
- **SEV4** (Low): <1% users affected AND <$5K/hour revenue impact AND workaround available

**Usage**:
```bash
# Classify from incident file
python scripts/severity_classifier.py incident.json --format text

# Classify with JSON output for automation
python scripts/severity_classifier.py incident.json --format json

# Stdin support
cat incident.json | python scripts/severity_classifier.py --format text

# Re-classify with updated scope
python scripts/severity_classifier.py incident.json --reclassify --format text

# Include escalation routing in output
python scripts/severity_classifier.py incident.json --with-escalation --format text
```

**Options**:
| Flag | Description | Default |
|------|-------------|---------|
| `--format` | Output format: `text`, `json` | `text` |
| `--reclassify` | Compare current vs. recommended severity | `false` |
| `--with-escalation` | Include escalation path and response times | `false` |
| `--sla-predict` | Predict SLA breach probability | `false` |
| `--verbose` | Show classification reasoning and confidence | `false` |

**Output Description**:
- Severity level with confidence percentage (e.g., "SEV2 - 94% confidence")
- Impact summary: affected users, services, estimated revenue loss
- Escalation path: who to page, response time requirements, communication channels
- SLA status: time remaining before breach, recommended actions
- Re-classification recommendation if scope has changed

### Postmortem Generator (`scripts/postmortem_generator.py`)
Automated blameless postmortem document generation with root cause analysis and action item tracking.

**Features**:
- Complete postmortem document generation from incident data
- 5-Whys root cause chain validation (checks for depth and logical consistency)
- Action item extraction with priority scoring (P1-P4) and ownership assignment
- Impact quantification: downtime minutes, affected users, revenue loss, SLA budget consumed
- Contributing factor identification beyond primary root cause
- Cross-incident pattern matching for recurring failure modes
- Blameless language validation (flags accusatory phrasing)

**Usage**:
```bash
# Generate postmortem in markdown format
python scripts/postmortem_generator.py incident.json --format markdown

# Generate in JSON for integration with tracking systems
python scripts/postmortem_generator.py incident.json --format json

# Stdin support
cat incident.json | python scripts/postmortem_generator.py --format markdown

# Include cross-incident pattern analysis (requires historical data)
python scripts/postmortem_generator.py incident.json --history incidents/ --format markdown

# Validate blameless language in existing postmortem
python scripts/postmortem_generator.py incident.json --validate-language --format text
```

**Options**:
| Flag | Description | Default |
|------|-------------|---------|
| `--format` | Output format: `markdown`, `json`, `text` | `markdown` |
| `--history` | Directory of historical incident JSON files for pattern analysis | none |
| `--validate-language` | Check for blame-assigning language patterns | `false` |
| `--include-timeline` | Embed full timeline in postmortem document | `true` |
| `--action-items-only` | Output only extracted action items | `false` |
| `--verbose` | Include classification reasoning and pattern details | `false` |

**Output Description**:
- Complete postmortem document with: title, severity, duration, impact summary
- Chronological timeline embedded from timeline builder
- Root cause analysis with 5-Whys chain and contributing factors
- Action items table with ID, description, priority, owner, due date
- Lessons learned section with systemic improvement recommendations
- SLA impact statement with remaining monthly error budget

---

## Methodology

### The Incident Commander's Decision Framework

#### Incident Lifecycle Model

Every incident follows five phases. The Incident Commander owns the transitions between them.

**Phase 1 - Detection** (Target: <5 minutes from onset to alert)
- Monitoring systems fire alerts based on predefined thresholds
- On-call engineer acknowledges alert within defined SLA (2 minutes for SEV1, 5 minutes for SEV2)
- Initial triage determines whether to declare a formal incident
- If customer-reported: escalate classification by one severity level automatically

**Phase 2 - Triage** (Target: <10 minutes)
- Incident Commander assigned or self-declared
- Severity classified using impact-first methodology (not cause-first)
- Communication channel established (dedicated Slack channel, bridge line)
- Stakeholder notification triggered per severity level
- Responder roles assigned: IC, Technical Lead, Communications Lead, Scribe

**Phase 3 - Mitigation** (Target: varies by severity)
- Focus on restoring service, not finding root cause
- Time-boxed investigation windows (15-minute check-ins for SEV1, 30-minute for SEV2)
- Escalation triggers if mitigation stalls beyond defined thresholds
- Customer communication cadence: every 15 minutes for SEV1, every 30 minutes for SEV2
- Decision framework: rollback vs. forward-fix vs. failover

**Phase 4 - Resolution** (Target: confirmed stable for 15+ minutes)
- Service confirmed restored to baseline metrics
- Monitoring confirms stability for minimum observation window
- Customer-facing all-clear communication sent
- Incident record updated with resolution summary
- Postmortem scheduled within 48 hours (24 hours for SEV1)

**Phase 5 - Postmortem** (Target: completed within 5 business days)
- Blameless postmortem meeting conducted with all responders
- Timeline reconstructed and validated by participants
- 5-Whys root cause analysis completed to systemic level
- Action items assigned with owners, priorities, and due dates
- Postmortem published to incident knowledge base

#### Severity Classification Philosophy

This framework uses **impact-first classification**, not cause-first. The severity of an incident is determined by its effect on customers and business, never by the technical cause.

Rationale: A typo in a config file that takes down all of production is a SEV1. A complex distributed systems failure that affects 0.1% of users is a SEV3. Cause complexity is irrelevant to severity -- only impact matters.

**Classification must happen within the first 5 minutes of declaration.** Reclassification is expected and encouraged as more information surfaces. Upgrading severity is always acceptable; downgrading requires IC approval and documented justification.

#### Communication Cadence Protocol

Silence during an incident is a failure mode. The Incident Commander enforces communication discipline:

| Severity | Internal Update | Customer Update | Executive Update |
|----------|----------------|-----------------|------------------|
| SEV1 | Every 10 min | Every 15 min | Every 30 min |
| SEV2 | Every 15 min | Every 30 min | Every 60 min |
| SEV3 | Every 30 min | Every 60 min | On resolution |
| SEV4 | Every 60 min | On resolution | Not required |

Updates must contain: current status, actions being taken, expected next update time, and any changes in severity or scope.

#### Blameless Postmortem Culture

Postmortems are the highest-leverage activity in incident management. They fail when they become blame sessions.

**Non-Negotiable Principles:**
1. Humans do not cause incidents. Systems that allow humans to trigger failures cause incidents.
2. Every postmortem must produce at least one systemic action item (process, tooling, or architecture change).
3. The 5-Whys analysis must reach a systemic root cause. "Engineer made a mistake" is never a root cause -- the question is why the system allowed that mistake to cause an outage.
4. Postmortem attendance is mandatory for all incident responders. Optional for anyone else who wants to learn.
5. Action items without owners and due dates are not action items. They are wishes.

---

## Templates & Assets

### Incident Response Runbook (`assets/incident_response_runbook.md`)
Step-by-step response protocol for active incidents including:
- Incident Commander checklist (declaration through resolution)
- Role assignments and responsibilities (IC, Tech Lead, Comms Lead, Scribe)
- Severity-specific escalation procedures with contact routing
- Communication templates for each update cadence
- Handoff protocol for long-running incidents (>4 hours)

### Postmortem Template (`assets/postmortem_template.md`)
Production-ready blameless postmortem document featuring:
- Structured header with incident metadata (ID, severity, duration, commander)
- Impact quantification section (users, revenue, SLA budget)
- Chronological timeline with phase annotations
- 5-Whys root cause analysis framework
- Contributing factors and systemic weaknesses
- Action items table with priority, owner, due date, and tracking status
- Lessons learned and process improvement recommendations

### Stakeholder Communication Templates (`assets/stakeholder_comms_templates.md`)
Pre-written communication templates for consistent messaging:
- Initial incident declaration (internal and external)
- Periodic status updates per severity level
- Resolution and all-clear notifications
- Executive briefing format for SEV1/SEV2 incidents
- Customer-facing status page update language
- Post-resolution follow-up communication

### Sample Incident Data (`assets/sample_incident_data.json`)
Comprehensive incident dataset demonstrating:
- Multi-service payment processing outage with realistic timeline
- 24 timeline events across all five lifecycle phases
- Complete 5-Whys root cause chain with contributing factors
- 6 action items with varying priorities and ownership
- SLA impact calculation with monthly error budget tracking
- Cross-referenced monitoring alerts, Slack messages, and PagerDuty events

---

## Reference Frameworks

### SRE Incident Management Guide (`references/sre-incident-management-guide.md`)
Comprehensive incident management methodology derived from Google SRE, PagerDuty, and Atlassian practices:
- Incident Commander role definition and authority boundaries
- On-call rotation best practices (follow-the-sun, escalation tiers)
- Severity classification decision trees with worked examples
- Communication protocols for internal, customer, and executive audiences
- Incident review cadence (weekly incident review, monthly trend analysis, quarterly reliability review)
- Tooling integration patterns (PagerDuty, OpsGenie, Slack, Datadog, Grafana)
- Regulatory incident reporting requirements (SOC2, HIPAA, PCI-DSS, GDPR)

### Reliability Metrics Framework (`references/reliability-metrics-framework.md`)
Quantitative reliability measurement and target-setting guide:
- MTTR, MTTD, MTBF definitions with calculation formulas and edge cases
- SLA/SLO/SLI hierarchy with implementation guidance
- Error budget policy design and enforcement mechanisms
- Incident frequency analysis with statistical trend detection
- Service-level reliability tiering (Tier 1 critical, Tier 2 important, Tier 3 standard)
- Dashboard design for operational visibility (what to measure, what to alert on, what to ignore)
- Benchmarking data: industry-standard targets by company maturity and service tier

---

## Implementation Workflows

### Active Incident Response

#### Step 1: Detection & Declaration (0-5 minutes)
1. **Alert fires** from monitoring system (Datadog, PagerDuty, CloudWatch, custom)
2. **On-call acknowledges** within response SLA (2 min SEV1, 5 min SEV2)
3. **Initial assessment**: Is this a real incident or a false positive?
4. **Declare incident**: Create incident channel, page Incident Commander
   ```
   /incident declare --severity SEV2 --title "Payment API 503 errors" --channel #inc-20260215-payments
   ```
5. **Classify severity** using `severity_classifier.py`:
   ```bash
   python scripts/severity_classifier.py incident.json --with-escalation --format text
   ```
6. **Assign roles**: IC, Technical Lead, Communications Lead, Scribe

#### Step 2: Triage & Mobilization (5-15 minutes)
1. **IC confirms severity** and activates escalation path
2. **Page additional responders** based on affected services
3. **Establish communication rhythm**: Set timer for first status update
4. **Scribe begins timeline**: Record all events with timestamps
5. **Technical Lead begins investigation**: Check dashboards, recent deployments, dependency health
6. **Communications Lead sends initial notification** to stakeholders

#### Step 3: Mitigation (15 minutes - varies)
1. **Focus on restoring service, not diagnosing root cause**
2. **Decision framework** at each check-in:
   - Can we rollback the last deployment? (fastest)
   - Can we failover to a healthy replica? (fast)
   - Can we apply a targeted forward-fix? (moderate)
   - Do we need to scale infrastructure? (slow)
3. **Time-boxed investigation**: If no progress in 15 minutes (SEV1) or 30 minutes (SEV2), escalate
4. **Customer communication**: Send status update per cadence protocol
5. **Re-classify severity** if scope changes:
   ```bash
   python scripts/severity_classifier.py incident_updated.json --reclassify --format text
   ```

#### Step 4: Resolution & Verification (varies)
1. **Confirm fix deployed** and metrics returning to baseline
2. **Observation window**: 15 minutes stable for SEV1/SEV2, 30 minutes for SEV3/SEV4
3. **Resolve incident**: Update status, send all-clear communication
4. **Schedule postmortem**: Within 24 hours for SEV1, 48 hours for SEV2, 5 business days for SEV3
5. **On-call engineer writes initial incident summary** while context is fresh

### Post-Incident Analysis

#### Timeline Reconstruction (Day 1-2)
1. **Gather raw data** from all sources (monitoring, Slack, PagerDuty, git log)
2. **Build unified timeline**:
   ```bash
   python scripts/incident_timeline_builder.py incident.json --format markdown --verbose
   ```
3. **Identify gaps**: Missing events, unexplained delays, undocumented decisions
4. **Validate with responders**: Circulate timeline for corrections before postmortem meeting

#### 5-Whys Root Cause Analysis (Postmortem Meeting)
1. **Start with the observable impact**: "Payment API returned 503 errors for 144 minutes"
2. **Ask "Why?" iteratively** -- each answer must be factual and verifiable
3. **Reach a systemic cause**: The final "why" must point to a process, tooling, or architecture gap
4. **Identify contributing factors**: What else made this incident worse or longer than necessary?
5. **Validate depth**: If the final cause is "human error," ask one more "why"

#### Action Item Generation
1. **Categorize**: Prevention (stop recurrence), Detection (find faster), Mitigation (recover faster)
2. **Prioritize**: P1 items must be completed before next on-call rotation
3. **Assign ownership**: Every action item has exactly one owner (team, not individual)
4. **Set due dates**: P1 within 1 week, P2 within 2 weeks, P3 within 1 month
5. **Generate postmortem**:
   ```bash
   python scripts/postmortem_generator.py incident.json --format markdown --include-timeline
   ```

### SLA Compliance Monitoring

1. **Define SLOs per service tier**:
   - Tier 1 (revenue-critical): 99.99% availability (52.6 min/year downtime budget)
   - Tier 2 (customer-facing): 99.95% availability (4.38 hours/year)
   - Tier 3 (internal tooling): 99.9% availability (8.77 hours/year)

2. **Track error budget consumption**: Monthly rolling window with daily updates
3. **Trigger error budget policy** when >50% consumed:
   - Freeze non-critical deployments
   - Prioritize reliability work over feature work
   - Require IC review for all production changes
4. **Monthly reliability review**: Present SLA compliance, incident trends, action item completion

### On-Call Handoff Protocol

1. **End-of-rotation summary**: Document active incidents, ongoing investigations, known risks
2. **Handoff meeting**: 15-minute synchronous handoff between outgoing and incoming on-call
3. **Runbook review**: Confirm incoming on-call has access to all runbooks and escalation paths
4. **Alert review**: Walk through any alerts that fired during the rotation and their resolutions
5. **Pending action items**: Transfer ownership of time-sensitive items to incoming on-call

---

## Assessment & Measurement

### Key Performance Indicators

#### Response Effectiveness Metrics
- **MTTD (Mean Time to Detect)**: Time from incident onset to first alert. Target: <5 minutes for Tier 1 services, <15 minutes for Tier 2. Measures observability coverage and alert threshold quality.
- **MTTR (Mean Time to Resolve)**: Time from incident declaration to confirmed resolution. Target: <30 minutes for SEV1, <2 hours for SEV2, <8 hours for SEV3. The single most important operational metric.
- **MTBF (Mean Time Between Failures)**: Time between consecutive incidents per service. Target: increasing quarter-over-quarter. Measures systemic reliability improvement.
- **MTTA (Mean Time to Acknowledge)**: Time from alert to human acknowledgment. Target: <2 minutes for SEV1, <5 minutes for SEV2. Measures on-call responsiveness.

#### Process Quality Metrics
- **Postmortem Completion Rate**: Percentage of SEV1-SEV3 incidents with completed postmortems. Target: 100% for SEV1-SEV2, >90% for SEV3.
- **Action Item Completion Rate**: Percentage of postmortem action items completed by due date. Target: >85% for P1, >70% for P2. Below 60% indicates systemic follow-through failure.
- **Postmortem Timeliness**: Days from resolution to published postmortem. Target: <3 business days for SEV1, <5 for SEV2.
- **Severity Accuracy**: Percentage of incidents where initial classification matched final assessment. Target: >80%. Low accuracy indicates classification training gaps.

#### Reliability Metrics
- **SLA Compliance**: Percentage of time meeting availability targets per service tier. Target: 100% compliance with defined SLOs.
- **Error Budget Remaining**: Monthly remaining error budget as percentage. Target: >25% remaining at month-end.
- **Incident Frequency Trend**: Month-over-month incident count by severity. Target: decreasing or stable for SEV1-SEV2.
- **Repeat Incident Rate**: Percentage of incidents with same root cause as a previous incident. Target: <10%. Above 15% indicates postmortem action items are not effective.

### Assessment Schedule
- **Per Incident**: MTTD, MTTR, severity accuracy, communication cadence adherence
- **Weekly**: Incident count review, open action item status, on-call load assessment
- **Monthly**: SLA compliance report, error budget status, MTTR trends, postmortem completion rates
- **Quarterly**: Reliability review with executive stakeholders, MTBF trends, incident pattern analysis, on-call health survey

### Calibration & Validation
- Cross-reference MTTR calculations with customer-reported impact duration
- Validate severity classifications retrospectively during postmortem review
- Compare automated severity classifier output against IC decisions to improve model accuracy
- Audit action item effectiveness by tracking repeat incident rate per root cause category

---

## Best Practices

### "Declare Early, Declare Often"
The single highest-leverage behavior in incident management is lowering the threshold for declaring incidents. Every organization that improves at incident response does so by declaring more incidents, not fewer.

**The cost of a false alarm is one wasted Slack channel. The cost of a missed incident is customer trust.**

Specific guidance:
- If two engineers are discussing whether something is an incident, it is an incident. Declare it.
- Any customer-reported issue that affects more than one user is an incident. Declare it.
- Any alert that requires more than 5 minutes of investigation is an incident. Declare it.
- Declaring an incident does not mean waking people up. It means creating a structured record.

### Anti-Patterns to Eliminate

**Hero Culture**: One engineer who "always fixes things" is a single point of failure, not an asset. If your incident response depends on a specific person being available, your process is broken. Fix the runbooks, not the rotation.

**Blame Games**: The moment a postmortem asks "who did this?" instead of "why did our systems allow this?", the entire process loses value. Engineers who fear blame will hide information. Engineers who trust the process will share everything.

**Skipping Postmortems**: "We already know what happened" is the most dangerous sentence in incident management. The purpose of a postmortem is not to discover what happened -- it is to generate systemic improvements and share learnings across the organization.

**Severity Inflation**: Classifying everything as SEV1 to get faster response trains the organization to ignore severity levels. Classify honestly. Respond proportionally.

**Action Item Graveyards**: Postmortems that generate action items no one tracks are worse than no postmortem at all. They create a false sense of progress. If your action item completion rate is below 50%, stop generating new action items and complete the existing ones first.

### Communication During Incidents

Template-driven communication eliminates cognitive load during high-stress situations:
- Never compose a customer update from scratch during an active incident
- Pre-written templates with fill-in-the-blank fields ensure consistent, professional communication
- The Communications Lead owns all external messaging; the IC approves content but does not write it
- Every update must answer three questions: What is happening? What are we doing about it? When is the next update?

### On-Call Health and Burnout Prevention

On-call is a tax on engineers' personal lives. Treating it as "just part of the job" without active management leads to burnout and attrition.

**Non-Negotiable Standards:**
- Maximum on-call rotation: 1 week in 4 (25% on-call time). Below 1-in-3 requires immediate hiring.
- On-call engineers who are paged overnight get a late start or half-day the following day. No exceptions.
- Track pages-per-rotation. If any rotation consistently exceeds 5 pages, the alert thresholds need tuning.
- Quarterly on-call satisfaction surveys. Scores below 3/5 trigger mandatory process review.
- On-call compensation: either financial (on-call pay) or temporal (comp time). Uncompensated on-call is unacceptable.

---

## Advanced Techniques

### Chaos Engineering Integration
Proactive reliability testing through controlled failure injection:
- **Pre-Incident Drills**: Run tabletop exercises using `postmortem_generator.py` output from past incidents as scenarios
- **Game Days**: Scheduled chaos experiments (Chaos Monkey, Litmus, Gremlin) with full incident response activation
- **Runbook Validation**: Use chaos experiments to verify runbook accuracy and completeness before real incidents test them
- **Detection Validation**: Inject known failures to verify MTTD targets are achievable with current monitoring

### Automated Incident Detection
Reducing MTTD through intelligent alerting:
- **Anomaly Detection**: Statistical baselines (3-sigma) on key metrics with automatic incident creation above threshold
- **Composite Alerts**: Multi-signal correlation (latency + error rate + saturation) to reduce false positive rates below 5%
- **Customer Signal Integration**: Status page report volume, support ticket spike detection, social media monitoring
- **Deployment Correlation**: Automatic incident flagging when metric degradation occurs within 30 minutes of a deployment

### Cross-Team Incident Coordination
Managing incidents that span organizational boundaries:
- **Unified Command Structure**: Single IC with authority across all affected teams, regardless of organizational reporting
- **Liaison Role**: Each affected team designates a liaison who communicates team-specific updates to the IC
- **Shared Timeline**: All teams contribute to a single timeline document, eliminating information silos
- **Joint Postmortems**: Cross-team postmortems with shared action items and joint ownership

### Regulatory Incident Reporting
Meeting compliance obligations during incidents:
- **SOC2**: Document incident detection, response, and resolution within audit trail. Action items must be tracked to completion.
- **HIPAA**: Breach notification within 60 days for incidents involving PHI. Document risk assessment and mitigation steps.
- **PCI-DSS**: Immediate containment for cardholder data exposure. Forensic investigation required for confirmed breaches.
- **GDPR**: 72-hour notification to supervisory authority for personal data breaches. Document legal basis for processing decisions.
- **Automation**: `postmortem_generator.py --format json` output structured to feed directly into compliance reporting workflows

---

## Limitations & Considerations

### Data Quality Dependencies
- **Minimum Event Count**: Timeline analysis requires 5+ events for meaningful phase analysis; fewer events produce incomplete coverage
- **Timestamp Accuracy**: All analysis assumes synchronized timestamps (NTP); clock skew across systems degrades timeline accuracy
- **Source Coverage**: Timeline quality depends on capturing events from all relevant systems; missing sources create blind spots
- **Historical Data**: Cross-incident pattern analysis requires 10+ resolved incidents for statistically meaningful trends

### Organizational Prerequisites
- **Blameless Culture**: Tools generate blameless framing, but cultural adoption requires sustained leadership commitment over 6+ months
- **On-Call Maturity**: Severity classification and escalation routing assume an established on-call rotation with defined response SLAs
- **Tooling Integration**: Full value requires integration with monitoring (Datadog/Grafana), communication (Slack), and paging (PagerDuty/OpsGenie) systems
- **Executive Buy-In**: Error budget policies and deployment freezes require executive sponsorship to enforce during business-critical periods

### Scaling Considerations
- **Team Size**: Communication cadence protocols optimized for 3-8 responders; larger incidents require additional coordination roles (Operations Lead, Customer Liaison)
- **Incident Volume**: Organizations handling >20 incidents/week need automated triage to prevent IC fatigue and classification inconsistency
- **Geographic Distribution**: Follow-the-sun on-call requires adapted handoff protocols and timezone-aware SLA calculations
- **Multi-Product**: Shared infrastructure incidents affecting multiple products require product-specific impact assessment and communication tracks

### Measurement Limitations
- **MTTR Variance**: Mean values obscure outliers; track P50, P90, and P99 MTTR for accurate performance assessment
- **Attribution Complexity**: Incidents with multiple contributing causes resist single-root-cause analysis; 5-Whys may oversimplify
- **Leading Indicators**: Most reliability metrics are lagging; invest in leading indicators (deployment frequency, change failure rate, alert noise ratio)
- **Comparison Pitfalls**: MTTR benchmarks vary dramatically by industry, company size, and service architecture; internal trends are more valuable than external comparisons

---

## Success Metrics & Outcomes

Organizations that implement this incident management framework consistently achieve:

- **40-60% reduction in MTTR** within the first 6 months through structured response protocols and severity-driven escalation
- **70%+ reduction in MTTD** through improved monitoring coverage and composite alert configuration
- **90%+ postmortem completion rate** for SEV1-SEV2 incidents, up from the industry average of 40-50%
- **85%+ action item completion rate** within defined due dates, eliminating the "action item graveyard" anti-pattern
- **50% reduction in repeat incidents** (same root cause) within 12 months through systematic postmortem follow-through
- **30-40% improvement in on-call satisfaction scores** through rotation health management and burnout prevention
- **99.95%+ SLA compliance** for Tier 1 services through error budget policies and proactive reliability investment
- **Sub-5-minute severity classification** with >80% accuracy through impact-first methodology and trained Incident Commanders

The framework transforms incident management from reactive firefighting into a structured, measurable engineering discipline. Teams stop treating incidents as exceptional events and start treating them as opportunities to systematically improve reliability, build organizational trust, and protect customer experience.

---

*This skill combines Google SRE principles, PagerDuty operational best practices, and Atlassian incident management workflows into a unified, tool-supported framework. Success requires organizational commitment to blameless culture, consistent postmortem follow-through, and investment in observability. Adapt severity thresholds, communication cadences, and SLA targets to your specific organizational context and customer expectations.*
