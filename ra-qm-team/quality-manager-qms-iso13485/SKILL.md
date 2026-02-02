---
name: quality-manager-qms-iso13485
description: ISO 13485 Quality Management System implementation and maintenance for medical device organizations. Provides QMS design, documentation control, internal auditing, CAPA management, and certification support.
triggers:
  - ISO 13485
  - QMS implementation
  - quality management system
  - document control
  - internal audit
  - management review
  - quality manual
  - CAPA process
  - process validation
  - design control
  - supplier qualification
  - quality records
---

# Quality Manager - QMS ISO 13485 Specialist

ISO 13485:2016 Quality Management System implementation, maintenance, and certification support for medical device organizations.

---

## Table of Contents

- [QMS Implementation Workflow](#qms-implementation-workflow)
- [Document Control Workflow](#document-control-workflow)
- [Internal Audit Workflow](#internal-audit-workflow)
- [Process Validation Workflow](#process-validation-workflow)
- [Supplier Qualification Workflow](#supplier-qualification-workflow)
- [QMS Process Reference](#qms-process-reference)
- [Decision Frameworks](#decision-frameworks)
- [Tools and References](#tools-and-references)

---

## QMS Implementation Workflow

Implement ISO 13485:2016 compliant quality management system from gap analysis through certification.

### Workflow: Initial QMS Implementation

1. Conduct gap analysis against ISO 13485:2016 requirements
2. Document current state vs. required state for each clause
3. Prioritize gaps by:
   - Regulatory criticality
   - Risk to product safety
   - Resource requirements
4. Develop implementation roadmap with milestones
5. Establish Quality Manual per Clause 4.2.2:
   - QMS scope with justified exclusions
   - Process interactions
   - Procedure references
6. Create required documented procedures:
   - Document control (4.2.3)
   - Record control (4.2.4)
   - Internal audit (8.2.4)
   - Nonconforming product (8.3)
   - Corrective action (8.5.2)
   - Preventive action (8.5.3)
7. Deploy processes with training
8. **Validation:** Gap analysis complete; Quality Manual approved; all required procedures documented and trained

### Gap Analysis Matrix

| Clause | Requirement | Current State | Gap | Priority | Action |
|--------|-------------|---------------|-----|----------|--------|
| 4.2.2 | Quality Manual | Not documented | Major | High | Create QM |
| 4.2.3 | Document control | Informal | Moderate | High | Formalize SOP |
| 5.6 | Management review | Ad hoc | Major | High | Establish schedule |
| 7.3 | Design control | Partial | Moderate | Medium | Complete procedures |
| 8.2.4 | Internal audit | None | Major | High | Create program |

### QMS Structure

| Level | Document Type | Purpose | Example |
|-------|---------------|---------|---------|
| 1 | Quality Manual | QMS overview, policy | QM-001 |
| 2 | Procedures | How processes work | SOP-02-001 |
| 3 | Work Instructions | Task-level detail | WI-06-012 |
| 4 | Records | Evidence of conformity | Training records |

### Required Procedure List

| Clause | Procedure | Minimum Content |
|--------|-----------|-----------------|
| 4.2.3 | Document Control | Approval, review, distribution, obsolete control |
| 4.2.4 | Record Control | Identification, storage, retention, disposal |
| 8.2.4 | Internal Audit | Program, auditor qualification, reporting |
| 8.3 | Nonconforming Product | Identification, segregation, disposition |
| 8.5.2 | Corrective Action | Investigation, root cause, effectiveness |
| 8.5.3 | Preventive Action | Risk identification, implementation, verification |

---

## Document Control Workflow

Establish and maintain document control per ISO 13485 Clause 4.2.3.

### Workflow: Document Creation and Approval

1. Identify need for new document or revision
2. Assign document number per numbering convention:
   - Format: `[TYPE]-[AREA]-[SEQUENCE]-[REV]`
   - Example: `SOP-02-001-01`
3. Draft document using approved template
4. Route for review to subject matter experts
5. Collect and address review comments
6. Obtain required approvals based on document type
7. Update Document Master List
8. **Validation:** Document numbered correctly; all reviewers signed; Master List updated

### Document Numbering Convention

| Prefix | Document Type | Approval Authority |
|--------|---------------|-------------------|
| QM | Quality Manual | Management Rep + CEO |
| POL | Policy | Department Head + QA |
| SOP | Procedure | Process Owner + QA |
| WI | Work Instruction | Supervisor + QA |
| TF | Template/Form | Process Owner |
| SPEC | Specification | Engineering + QA |

### Area Codes

| Code | Area | Examples |
|------|------|----------|
| 01 | Quality Management | Quality Manual, policy |
| 02 | Document Control | This procedure |
| 03 | Training | Competency procedures |
| 04 | Design | Design control |
| 05 | Purchasing | Supplier management |
| 06 | Production | Manufacturing |
| 07 | Quality Control | Inspection, testing |
| 08 | CAPA | Corrective actions |

### Document Change Control

| Change Type | Approval Level | Examples |
|-------------|----------------|----------|
| Administrative | Document Control | Typos, formatting |
| Minor | Process Owner + QA | Clarifications |
| Major | Full review cycle | Process changes |
| Emergency | Expedited + retrospective | Safety issues |

### Document Review Schedule

| Document Type | Review Period | Trigger for Unscheduled Review |
|---------------|---------------|-------------------------------|
| Quality Manual | Annual | Organizational change |
| Procedures | Annual | Audit finding, regulation change |
| Work Instructions | 2 years | Process change |
| Forms | 2 years | User feedback |

---

## Internal Audit Workflow

Plan and execute internal audits per ISO 13485 Clause 8.2.4.

### Workflow: Annual Audit Program

1. Identify processes and areas requiring audit coverage
2. Assess risk factors for audit frequency:
   - Previous audit findings
   - Regulatory changes
   - Process changes
   - Complaint trends
3. Assign qualified auditors (independent of area audited)
4. Develop annual audit schedule
5. Obtain management approval
6. Communicate schedule to process owners
7. Track completion and reschedule as needed
8. **Validation:** All processes covered; auditors qualified and independent; schedule approved

### Workflow: Individual Audit Execution

1. Prepare audit plan with scope, criteria, and schedule
2. Notify auditee minimum 1 week prior
3. Review procedures and previous audit results
4. Prepare audit checklist
5. Conduct opening meeting
6. Collect evidence through:
   - Document review
   - Record sampling
   - Process observation
   - Personnel interviews
7. Classify findings:
   - Major NC: Absence or breakdown of system
   - Minor NC: Single lapse or deviation
   - Observation: Risk of future NC
8. Conduct closing meeting
9. Issue audit report within 5 business days
10. **Validation:** All checklist items addressed; findings supported by evidence; report distributed

### Audit Program Template

| Audit # | Process | Clauses | Q1 | Q2 | Q3 | Q4 | Auditor |
|---------|---------|---------|----|----|----|----|---------|
| IA-001 | Document Control | 4.2.3, 4.2.4 | X | | | | [Name] |
| IA-002 | Management Review | 5.6 | | X | | | [Name] |
| IA-003 | Design Control | 7.3 | | X | | | [Name] |
| IA-004 | Production | 7.5 | | | X | | [Name] |
| IA-005 | CAPA | 8.5.2, 8.5.3 | | | | X | [Name] |

### Auditor Qualification Requirements

| Criterion | Requirement |
|-----------|-------------|
| Training | ISO 13485 awareness + auditor training |
| Experience | Minimum 1 audit as observer |
| Independence | Not auditing own work area |
| Competence | Understanding of audited process |

### Finding Classification Guide

| Classification | Criteria | Response Time |
|----------------|----------|---------------|
| Major NC | System absence, total breakdown, regulatory violation | 30 days for CAPA |
| Minor NC | Single instance, partial compliance | 60 days for CAPA |
| Observation | Potential risk, improvement opportunity | Track in next audit |

---

## Process Validation Workflow

Validate special processes per ISO 13485 Clause 7.5.6.

### Workflow: Process Validation Protocol

1. Identify processes requiring validation:
   - Output cannot be verified by inspection
   - Deficiencies appear only in use
   - Sterilization, welding, sealing, software
2. Form validation team with subject matter experts
3. Write validation protocol including:
   - Process description and parameters
   - Equipment and materials
   - Acceptance criteria
   - Statistical approach
4. Execute Installation Qualification (IQ):
   - Verify equipment installed correctly
   - Document equipment specifications
5. Execute Operational Qualification (OQ):
   - Test parameter ranges
   - Verify process control
6. Execute Performance Qualification (PQ):
   - Run production conditions
   - Verify output meets requirements
7. Write validation report with conclusions
8. **Validation:** IQ/OQ/PQ complete; acceptance criteria met; validation report approved

### Validation Documentation Requirements

| Phase | Content | Evidence |
|-------|---------|----------|
| Protocol | Objectives, methods, criteria | Approved protocol |
| IQ | Equipment verification | Installation records |
| OQ | Parameter verification | Test results |
| PQ | Performance verification | Production data |
| Report | Summary, conclusions | Approval signatures |

### Revalidation Triggers

| Trigger | Action Required |
|---------|-----------------|
| Equipment change | Assess impact, revalidate affected phases |
| Parameter change | OQ and PQ minimum |
| Material change | Assess impact, PQ minimum |
| Process failure | Full revalidation |
| Periodic | Per validation schedule (typically 3 years) |

### Special Process Examples

| Process | Validation Standard | Critical Parameters |
|---------|--------------------|--------------------|
| EO Sterilization | ISO 11135 | Temperature, humidity, EO concentration, time |
| Steam Sterilization | ISO 17665 | Temperature, pressure, time |
| Radiation Sterilization | ISO 11137 | Dose, dose uniformity |
| Sealing | Internal | Temperature, pressure, dwell time |
| Welding | ISO 11607 | Heat, pressure, speed |

---

## Supplier Qualification Workflow

Evaluate and approve suppliers per ISO 13485 Clause 7.4.

### Workflow: New Supplier Qualification

1. Identify supplier category:
   - Category A: Critical (affects safety/performance)
   - Category B: Major (affects quality)
   - Category C: Minor (indirect impact)
2. Request supplier information:
   - Quality certifications
   - Product specifications
   - Quality history
3. Evaluate supplier based on:
   - Quality system (ISO certification)
   - Technical capability
   - Quality history
   - Financial stability
4. For Category A suppliers:
   - Conduct on-site audit
   - Require quality agreement
5. Calculate qualification score
6. Make approval decision:
   - >80: Approved
   - 60-80: Conditional approval
   - <60: Not approved
7. Add to Approved Supplier List
8. **Validation:** Evaluation criteria scored; qualification records complete; supplier categorized

### Supplier Evaluation Criteria

| Criterion | Weight | Scoring |
|-----------|--------|---------|
| Quality System | 30% | ISO 13485=30, ISO 9001=20, Documented=10, None=0 |
| Quality History | 25% | Reject rate: <1%=25, 1-3%=15, >3%=0 |
| Delivery | 20% | On-time: >95%=20, 90-95%=10, <90%=0 |
| Technical Capability | 15% | Exceeds=15, Meets=10, Marginal=5 |
| Financial Stability | 10% | Strong=10, Adequate=5, Questionable=0 |

### Supplier Category Requirements

| Category | Qualification | Monitoring | Agreement |
|----------|---------------|------------|-----------|
| A - Critical | On-site audit | Annual review | Quality agreement |
| B - Major | Questionnaire | Semi-annual review | Quality requirements |
| C - Minor | Assessment | Issue-based | Standard terms |

### Supplier Performance Metrics

| Metric | Target | Calculation |
|--------|--------|-------------|
| Accept Rate | >98% | (Accepted lots / Total lots) × 100 |
| On-Time Delivery | >95% | (On-time / Total orders) × 100 |
| Response Time | <5 days | Average days to resolve issues |
| Documentation | 100% | (Complete CoCs / Required CoCs) × 100 |

---

## QMS Process Reference

### ISO 13485 Clause Structure

| Clause | Title | Key Requirements |
|--------|-------|-----------------|
| 4.1 | General Requirements | Process identification, interaction, outsourcing |
| 4.2 | Documentation | Quality Manual, procedures, records |
| 5.1-5.5 | Management Responsibility | Commitment, policy, objectives, organization |
| 5.6 | Management Review | Inputs, outputs, records |
| 6.1-6.4 | Resource Management | Personnel, infrastructure, environment |
| 7.1 | Product Realization Planning | Quality plan, risk management |
| 7.2 | Customer Requirements | Determination, review, communication |
| 7.3 | Design and Development | Planning, inputs, outputs, review, V&V, transfer, changes |
| 7.4 | Purchasing | Supplier control, purchasing info, verification |
| 7.5 | Production | Control, cleanliness, validation, identification, traceability |
| 7.6 | Monitoring Equipment | Calibration, control |
| 8.1 | Measurement Planning | Monitoring and analysis planning |
| 8.2 | Monitoring | Feedback, complaints, reporting, audits, process, product |
| 8.3 | Nonconforming Product | Control, disposition |
| 8.4 | Data Analysis | Trend analysis |
| 8.5 | Improvement | CAPA |

### Management Review Required Inputs (Clause 5.6.2)

| Input | Source | Prepared By |
|-------|--------|-------------|
| Audit results | Internal and external audits | QA Manager |
| Customer feedback | Complaints, surveys | Customer Quality |
| Process performance | Process metrics | Process Owners |
| Product conformity | Inspection data, NCs | QC Manager |
| CAPA status | CAPA system | CAPA Officer |
| Previous actions | Prior review records | QMR |
| Changes affecting QMS | Regulatory, organizational | RA Manager |
| Recommendations | All sources | All Managers |

### Record Retention Requirements

| Record Type | Minimum Retention | Regulatory Basis |
|-------------|-------------------|------------------|
| Device Master Record | Life of device + 2 years | 21 CFR 820.181 |
| Device History Record | Life of device + 2 years | 21 CFR 820.184 |
| Design History File | Life of device + 2 years | 21 CFR 820.30 |
| Complaint Records | Life of device + 2 years | 21 CFR 820.198 |
| Training Records | Employment + 3 years | Best practice |
| Audit Records | 7 years | Best practice |
| CAPA Records | 7 years | Best practice |
| Calibration Records | Equipment life + 2 years | Best practice |

---

## Decision Frameworks

### Exclusion Justification (Clause 4.2.2)

| Clause | Permissible Exclusion | Justification Required |
|--------|----------------------|------------------------|
| 6.4.2 | Contamination control | Product not affected by contamination |
| 7.3 | Design and development | Organization does not design products |
| 7.5.2 | Product cleanliness | No cleanliness requirements |
| 7.5.3 | Installation | No installation activities |
| 7.5.4 | Servicing | No servicing activities |
| 7.5.5 | Sterile products | No sterile products |

### Nonconformity Disposition Decision Tree

```
Nonconforming Product Identified
            │
            ▼
    Can it be reworked?
            │
       Yes──┴──No
        │       │
        ▼       ▼
    Is rework     Can it be used
    procedure     as is?
    available?        │
        │        Yes──┴──No
    Yes─┴─No     │       │
     │    │     ▼       ▼
     ▼    ▼  Concession  Scrap or
  Rework  Create    approval    return to
  per SOP  rework    needed?    supplier
          procedure     │
                    Yes─┴─No
                     │    │
                     ▼    ▼
                 Customer  Use as is
                 approval  with MRB
                          approval
```

### CAPA Initiation Criteria

| Source | Automatic CAPA | Evaluate for CAPA |
|--------|----------------|-------------------|
| Customer complaint | Safety-related | All others |
| External audit | Major NC | Minor NC |
| Internal audit | Major NC | Repeat minor NC |
| Product NC | Field failure | Trend exceeds threshold |
| Process deviation | Safety impact | Repeated deviations |

---

## Tools and References

### Scripts

| Tool | Purpose | Usage |
|------|---------|-------|
| [qms_audit_checklist.py](scripts/qms_audit_checklist.py) | Generate audit checklists by clause or process | `python qms_audit_checklist.py --help` |

**Audit Checklist Generator Features:**
- Generate clause-specific checklists (e.g., `--clause 7.3`)
- Generate process-based checklists (e.g., `--process design-control`)
- Full system audit checklist (`--audit-type system`)
- Text or JSON output formats
- Interactive mode for guided selection

### References

| Document | Content |
|----------|---------|
| [iso13485-clause-requirements.md](references/iso13485-clause-requirements.md) | Detailed requirements for each ISO 13485:2016 clause with audit questions |
| [qms-process-templates.md](references/qms-process-templates.md) | Ready-to-use templates for document control, audit, CAPA, supplier, training |

### Quick Reference: Mandatory Documented Procedures

| Procedure | Clause | Key Elements |
|-----------|--------|--------------|
| Document Control | 4.2.3 | Approval, distribution, obsolete control |
| Record Control | 4.2.4 | Identification, retention, disposal |
| Internal Audit | 8.2.4 | Program, auditor qualification, reporting |
| NC Product Control | 8.3 | Identification, segregation, disposition |
| Corrective Action | 8.5.2 | Root cause, implementation, verification |
| Preventive Action | 8.5.3 | Risk identification, implementation |

---

## Related Skills

| Skill | Integration Point |
|-------|-------------------|
| [quality-manager-qmr](../quality-manager-qmr/) | Management review, quality policy |
| [capa-officer](../capa-officer/) | CAPA system management |
| [qms-audit-expert](../qms-audit-expert/) | Advanced audit techniques |
| [quality-documentation-manager](../quality-documentation-manager/) | DHF, DMR, DHR management |
| [risk-management-specialist](../risk-management-specialist/) | ISO 14971 integration |
