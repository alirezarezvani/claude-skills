---
name: regulatory-affairs-head
description: Senior Regulatory Affairs Manager for HealthTech and MedTech companies. Provides regulatory strategy development, submission management, pathway analysis, global compliance coordination, and cross-functional team leadership.
triggers:
  - regulatory strategy
  - FDA submission
  - EU MDR
  - 510(k)
  - PMA approval
  - CE marking
  - regulatory pathway
  - market access
  - clinical evidence
  - regulatory intelligence
  - submission planning
  - notified body
---

# Head of Regulatory Affairs

Regulatory strategy development, submission management, and global market access for medical device organizations.

---

## Table of Contents

- [Regulatory Strategy Workflow](#regulatory-strategy-workflow)
- [FDA Submission Workflow](#fda-submission-workflow)
- [EU MDR Submission Workflow](#eu-mdr-submission-workflow)
- [Global Market Access Workflow](#global-market-access-workflow)
- [Regulatory Intelligence Workflow](#regulatory-intelligence-workflow)
- [Decision Frameworks](#decision-frameworks)
- [Tools and References](#tools-and-references)

---

## Regulatory Strategy Workflow

Develop regulatory strategy aligned with business objectives and product characteristics.

### Workflow: New Product Regulatory Strategy

1. Gather product information:
   - Intended use and indications
   - Device classification (risk level)
   - Technology platform
   - Target markets and timeline
2. Identify applicable regulations per target market:
   - FDA (US): 21 CFR Part 820, 510(k)/PMA/De Novo
   - EU: MDR 2017/745, Notified Body requirements
   - Other markets: Health Canada, PMDA, NMPA, TGA
3. Determine optimal regulatory pathway:
   - Compare submission types (510(k) vs De Novo vs PMA)
   - Assess predicate device availability
   - Evaluate clinical evidence requirements
4. Develop regulatory timeline with milestones
5. Estimate resource requirements and budget
6. Identify regulatory risks and mitigation strategies
7. Obtain stakeholder alignment and approval
8. **Validation:** Strategy document approved; timeline accepted; resources allocated

### Regulatory Pathway Selection Matrix

| Factor | 510(k) | De Novo | PMA |
|--------|--------|---------|-----|
| Predicate Available | Yes | No | N/A |
| Risk Level | Low-Moderate | Low-Moderate | High |
| Clinical Data | Usually not required | May be required | Required |
| Review Time | 90 days (MDUFA) | 150 days | 180 days |
| User Fee | ~$22K (2024) | ~$135K | ~$440K |
| Best For | Me-too devices | Novel low-risk | High-risk, novel |

### Regulatory Strategy Document Template

```
REGULATORY STRATEGY

Product: [Name]
Version: [X.X]
Date: [Date]

1. PRODUCT OVERVIEW
   - Intended use: [Statement]
   - Device classification: [Class I/II/III]
   - Technology: [Description]

2. TARGET MARKETS
   | Market | Priority | Timeline |
   |--------|----------|----------|
   | USA    | 1        | Q1 20XX  |
   | EU     | 2        | Q2 20XX  |

3. REGULATORY PATHWAY
   - FDA: [510(k) / De Novo / PMA]
   - EU: [Class] via [Conformity route]
   - Rationale: [Justification]

4. CLINICAL EVIDENCE STRATEGY
   - Requirements: [Summary]
   - Approach: [Literature / Study / Both]

5. TIMELINE AND MILESTONES
   [Gantt or milestone table]

6. RISKS AND MITIGATION
   | Risk | Probability | Impact | Mitigation |
   |------|-------------|--------|------------|

7. RESOURCE REQUIREMENTS
   - Budget: $[Amount]
   - Personnel: [FTEs]
   - External support: [Consultants, CRO]
```

---

## FDA Submission Workflow

Prepare and submit FDA regulatory applications.

### Workflow: 510(k) Submission

1. Confirm 510(k) pathway suitability:
   - Predicate device identified
   - Substantial equivalence supportable
   - No new intended use or technology concerns
2. Schedule and conduct Pre-Submission (Q-Sub) meeting if needed
3. Compile submission package:
   - Cover letter and administrative information
   - Device description and intended use
   - Substantial equivalence comparison
   - Performance testing data
   - Biocompatibility (if patient contact)
   - Software documentation (if applicable)
   - Labeling and IFU
4. Conduct internal review and quality check
5. Prepare eCopy per FDA format requirements
6. Submit via FDA ESG portal with user fee payment
7. Monitor MDUFA clock and respond to AI/RTA requests
8. **Validation:** Submission accepted; MDUFA date received; tracking system updated

### Workflow: PMA Submission

1. Confirm PMA pathway:
   - Class III device or no predicate
   - Clinical data strategy defined
2. Complete IDE clinical study if required:
   - IDE approval
   - Clinical protocol execution
   - Study report completion
3. Conduct Pre-Submission meeting
4. Compile PMA submission:
   - Administrative and device information
   - Manufacturing information
   - Nonclinical studies
   - Clinical studies
   - Labeling
5. Submit original PMA application
6. Address FDA questions and deficiencies
7. Prepare for FDA facility inspection
8. **Validation:** PMA approved; approval letter received; post-approval requirements documented

### FDA Submission Timeline

| Milestone | 510(k) | De Novo | PMA |
|-----------|--------|---------|-----|
| Pre-Sub Meeting | Day -90 | Day -90 | Day -120 |
| Submission | Day 0 | Day 0 | Day 0 |
| RTA Review | Day 15 | Day 15 | Day 45 |
| Substantive Review | Days 15-90 | Days 15-150 | Days 45-180 |
| Decision | Day 90 | Day 150 | Day 180 |

### Common FDA Deficiencies

| Category | Common Issues | Prevention |
|----------|---------------|------------|
| Substantial Equivalence | Weak predicate comparison | Strong SE argument upfront |
| Performance Testing | Incomplete test protocols | Follow recognized standards |
| Biocompatibility | Missing endpoints | ISO 10993 risk assessment |
| Software | Inadequate documentation | IEC 62304 compliance |
| Labeling | Inconsistent claims | Early labeling review |

See: [references/fda-submission-guide.md](references/fda-submission-guide.md)

---

## EU MDR Submission Workflow

Achieve CE marking under EU MDR 2017/745.

### Workflow: MDR Technical Documentation

1. Confirm device classification per MDR Annex VIII
2. Select conformity assessment route based on class:
   - Class I: Self-declaration
   - Class IIa/IIb: Notified Body involvement
   - Class III: Full NB assessment
3. Select and engage Notified Body (for Class IIa+)
4. Compile Technical Documentation per Annex II:
   - Device description and specifications
   - Design and manufacturing information
   - General Safety and Performance Requirements (GSPR) checklist
   - Benefit-risk analysis and risk management
   - Clinical evaluation per Annex XIV
   - Post-market surveillance plan
5. Establish and document QMS per ISO 13485
6. Submit application to Notified Body
7. Address NB questions and coordinate audit
8. **Validation:** CE certificate issued; Declaration of Conformity signed; EUDAMED registration complete

### MDR Classification Decision Tree

```
Is the device active?
        │
    Yes─┴─No
     │     │
     ▼     ▼
Is it an   Does it contact
implant?   the body?
  │            │
Yes─┴─No   Yes─┴─No
 │    │     │     │
 ▼    ▼     ▼     ▼
III  IIb  Check   Class I
         contact  (measuring/
         type     sterile if
         and      applicable)
         duration
```

### Clinical Evidence Requirements by Class

| Class | Clinical Requirement | Documentation |
|-------|---------------------|---------------|
| I | Clinical evaluation (CE) | CE report |
| IIa | CE with literature focus | CE report + PMCF plan |
| IIb | CE with clinical data | CE report + PMCF + clinical study (some) |
| III | CE with clinical investigation | CE report + PMCF + clinical investigation |

### Notified Body Selection Criteria

| Criterion | Consideration |
|-----------|---------------|
| Scope | Device category expertise |
| Capacity | Availability and review timeline |
| Experience | Track record in your technology |
| Geography | Proximity for audits |
| Cost | Fee structure transparency |
| Communication | Responsiveness and clarity |

See: [references/eu-mdr-submission-guide.md](references/eu-mdr-submission-guide.md)

---

## Global Market Access Workflow

Coordinate regulatory approvals across international markets.

### Workflow: Multi-Market Submission Strategy

1. Define target markets based on business priorities
2. Sequence markets for efficient evidence leverage:
   - Phase 1: FDA + EU (reference markets)
   - Phase 2: Recognition markets (Canada, Australia)
   - Phase 3: Major markets (Japan, China)
   - Phase 4: Emerging markets
3. Identify local requirements per market:
   - Clinical data acceptability
   - Local agent/representative needs
   - Language and labeling requirements
4. Develop master technical file with localization plan
5. Establish in-country regulatory support
6. Execute parallel or sequential submissions
7. Track approvals and coordinate launches
8. **Validation:** All target market approvals obtained; registration database updated

### Market Priority Matrix

| Market | Size | Complexity | Recognition | Priority |
|--------|------|------------|-------------|----------|
| USA | Large | High | N/A | 1 |
| EU | Large | High | N/A | 1-2 |
| Canada | Medium | Medium | MDSAP | 2 |
| Australia | Medium | Low | EU accepted | 2 |
| Japan | Large | High | Local clinical | 3 |
| China | Large | Very High | Local testing | 3 |
| Brazil | Medium | High | GMP inspection | 3-4 |

### Documentation Efficiency Strategy

| Document Type | Single Source | Localization Required |
|---------------|---------------|----------------------|
| Technical file core | Yes | Format adaptation |
| Risk management | Yes | None |
| Clinical data | Yes | Bridging assessment |
| QMS certificate | Yes (ISO 13485) | Market-specific audit |
| Labeling | Master label | Translation, local requirements |
| IFU | Master content | Translation, local symbols |

See: [references/global-regulatory-pathways.md](references/global-regulatory-pathways.md)

---

## Regulatory Intelligence Workflow

Monitor and respond to regulatory changes affecting product portfolio.

### Workflow: Regulatory Change Management

1. Monitor regulatory sources:
   - FDA Federal Register, guidance documents
   - EU Official Journal, MDCG guidance
   - Notified Body communications
   - Industry associations (AdvaMed, MedTech Europe)
2. Assess relevance to product portfolio
3. Evaluate impact:
   - Timeline to compliance
   - Resource requirements
   - Product changes needed
4. Develop compliance action plan
5. Communicate to affected stakeholders
6. Implement required changes
7. Document compliance status
8. **Validation:** Compliance action plan approved; changes implemented on schedule

### Regulatory Monitoring Sources

| Source | Type | Frequency |
|--------|------|-----------|
| FDA Federal Register | Regulations, guidance | Daily |
| FDA Device Database | 510(k), PMA, recalls | Weekly |
| EU Official Journal | MDR/IVDR updates | Weekly |
| MDCG Guidance | EU implementation | As published |
| ISO/IEC | Standards updates | Quarterly |
| Notified Body | Audit findings, trends | Per interaction |

### Impact Assessment Template

```
REGULATORY CHANGE IMPACT ASSESSMENT

Change: [Description]
Source: [Regulation/Guidance]
Effective Date: [Date]
Assessment Date: [Date]
Assessed By: [Name]

AFFECTED PRODUCTS
| Product | Impact | Action Required | Timeline |
|---------|--------|-----------------|----------|
| [Name]  | [H/M/L]| [Description]   | [Date]   |

COMPLIANCE ACTIONS
1. [Action 1] - Owner: [Name] - Due: [Date]
2. [Action 2] - Owner: [Name] - Due: [Date]

RESOURCE REQUIREMENTS
- Budget: $[Amount]
- Personnel: [Hours/FTEs]

APPROVAL
Regulatory: _________________ Date: _______
Management: _________________ Date: _______
```

---

## Decision Frameworks

### Pathway Selection Decision Tree

```
Is predicate device available?
            │
        Yes─┴─No
         │     │
         ▼     ▼
    Is device   Is risk level
    substantially  Low-Moderate?
    equivalent?       │
         │        Yes─┴─No
     Yes─┴─No      │     │
      │     │      ▼     ▼
      ▼     ▼   De Novo  PMA
    510(k)  Consider      required
           De Novo
           or PMA
```

### Pre-Submission Meeting Decision

| Factor | Schedule Pre-Sub | Skip Pre-Sub |
|--------|------------------|--------------|
| Novel Technology | ✓ | |
| New Intended Use | ✓ | |
| Complex Testing | ✓ | |
| Uncertain Predicate | ✓ | |
| Clinical Data Needed | ✓ | |
| Well-established | | ✓ |
| Clear Predicate | | ✓ |
| Standard Testing | | ✓ |

### Regulatory Escalation Criteria

| Situation | Escalation Level | Action |
|-----------|------------------|--------|
| Submission rejection | VP Regulatory | Root cause analysis, strategy revision |
| Major deficiency | Director | Cross-functional response team |
| Timeline at risk | Management | Resource reallocation review |
| Regulatory change | VP Regulatory | Portfolio impact assessment |
| Safety signal | Executive | Immediate containment and reporting |

---

## Tools and References

### Scripts

| Tool | Purpose | Usage |
|------|---------|-------|
| [regulatory_tracker.py](scripts/regulatory_tracker.py) | Track submission status and timelines | `python regulatory_tracker.py` |

**Regulatory Tracker Features:**
- Track multiple submissions across markets
- Monitor status and target dates
- Identify overdue submissions
- Generate status reports

### References

| Document | Content |
|----------|---------|
| [fda-submission-guide.md](references/fda-submission-guide.md) | FDA pathways, requirements, review process |
| [eu-mdr-submission-guide.md](references/eu-mdr-submission-guide.md) | MDR classification, technical documentation, clinical evidence |
| [global-regulatory-pathways.md](references/global-regulatory-pathways.md) | Canada, Japan, China, Australia, Brazil requirements |
| [iso-regulatory-requirements.md](references/iso-regulatory-requirements.md) | ISO 13485, 14971, 10993, IEC 62304, 62366 requirements |

### Key Performance Indicators

| KPI | Target | Calculation |
|-----|--------|-------------|
| First-time approval rate | >85% | (Approved without major deficiency / Total submitted) × 100 |
| On-time submission | >90% | (Submitted by target date / Total submissions) × 100 |
| Review cycle compliance | >95% | (Responses within deadline / Total requests) × 100 |
| Regulatory hold time | <20% | (Days on hold / Total review days) × 100 |

---

## Related Skills

| Skill | Integration Point |
|-------|-------------------|
| [mdr-745-specialist](../mdr-745-specialist/) | Detailed EU MDR technical requirements |
| [fda-consultant-specialist](../fda-consultant-specialist/) | FDA submission deep expertise |
| [quality-manager-qms-iso13485](../quality-manager-qms-iso13485/) | QMS for regulatory compliance |
| [risk-management-specialist](../risk-management-specialist/) | ISO 14971 risk management |
