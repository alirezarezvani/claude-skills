# Security Requirements Review — Workflow Reference

## Document Type Taxonomy

This reference defines how the `security-requirements-review` skill classifies and analyzes each document type. The `pre_analysis.py` classifier uses keyword signals from this taxonomy.

---

## Document Types and Classification Signals

### POA&M (Plan of Action and Milestones)

**Classification signals:** `POA&M`, `plan of action`, `milestones`, `corrective action`, `POAM`, `weakness`, `scheduled completion`, `deviation`

**Analysis lens:**
- Remediation gap analysis: which weaknesses have no scheduled corrective action
- Control deficiency mapping: weaknesses without compensating controls
- Regulatory deadline tracking: milestones past due or at risk
- Risk acceptance documentation: weaknesses accepted without mitigation

**MITRE mapping focus:** Techniques applicable to unmitigated weaknesses (e.g., unpatched system → T1190, missing encryption → T1005)

**Routing:** Always route to `compliance-mapping` for deadline and control gap analysis.

---

### PRD / Product Requirements Document

**Classification signals:** `product requirements`, `user story`, `acceptance criteria`, `feature`, `release`, `MVP`, `roadmap`, `persona`, `use case`, `epic`

**Analysis lens:**
- STRIDE threat model: Spoofing, Tampering, Repudiation, Information Disclosure, DoS, Elevation of Privilege applied to each user story
- Attack surface identification: new endpoints, integrations, data stores mentioned
- Data classification: PII, PHI, PCI cardholder data, trade secrets identified
- Authentication and authorization design gaps

**MITRE mapping focus:** Initial access (T1190, T1133), data exposure (T1005, T1530), privilege escalation (T1078, T1548)

**Routing:** `appsec-code-review` for code-level requirements; `compliance-mapping` if regulated data detected.

---

### Architecture Document

**Classification signals:** `architecture`, `system design`, `component`, `service mesh`, `microservice`, `data flow`, `trust boundary`, `DMZ`, `network diagram`, `API gateway`, `load balancer`, `database`, `infrastructure`

**Analysis lens:**
- Trust boundary analysis: zones defined and enforced
- Data flow risk: sensitive data crossing unprotected boundaries
- Lateral movement paths: flat network segments, missing segmentation
- Single points of failure: components without redundancy that are also security control points

**MITRE mapping focus:** Lateral movement (T1210, T1021), credential access (T1552), discovery (T1046, T1040)

**Routing:** Always route to `risk-threat-modeling` regardless of severity.

---

### Project Plan

**Classification signals:** `project plan`, `sprint`, `milestone`, `Gantt`, `WBS`, `work breakdown`, `deliverable`, `timeline`, `phase`, `go-live`

**Analysis lens:**
- Security milestone gaps: security reviews, pen tests, and compliance assessments missing from timeline
- Compliance obligation coverage: regulatory deadlines without corresponding security tasks
- Resource gaps: security roles absent from project staffing

**MITRE mapping focus:** Not primary; use project plan to identify when controls will be absent and for how long.

**Routing:** `compliance-mapping` if regulatory deadlines identified.

---

### Requirements Specification

**Classification signals:** `shall`, `must`, `functional requirement`, `non-functional requirement`, `system requirement`, `SRS`, `software requirements specification`, `interface requirement`

**Analysis lens:**
- Misuse case identification: for each "shall" requirement, identify the adversarial inversion
- Input validation surface: all external inputs identified and validation requirements present
- Auth/authz design: authentication and authorization requirements explicitly stated
- Error handling: secure error handling requirements present

**MITRE mapping focus:** Input validation (T1059, T1190), authentication bypass (T1078), information disclosure via errors (T1082)

**Routing:** `appsec-code-review` for validation and auth requirements; `compliance-mapping` for regulatory requirements.

---

## Analysis Lenses Reference

### STRIDE Application

| Threat | Signal to Look For in Document |
|---|---|
| Spoofing | No authentication requirement stated; "any user can access" language |
| Tampering | No integrity check described; unsigned data transmission |
| Repudiation | No audit logging requirement; "no log needed" |
| Information Disclosure | Sensitive data with no access control described; error messages with debug info |
| Denial of Service | No rate limiting; no availability requirement; single-instance design |
| Elevation of Privilege | Role definitions with overly broad permissions; admin access without MFA |

---

### Compliance Framework Signals

| Framework | Keyword Signals | Key Controls to Check |
|---|---|---|
| PCI DSS | `cardholder`, `PAN`, `payment`, `card data`, `CHD`, `CDE` | Encryption at rest/transit, tokenization, network segmentation, logging |
| GDPR | `personal data`, `data subject`, `consent`, `right to erasure`, `DPA`, `DPIA` | Lawful basis, retention limits, data minimization, breach notification |
| HIPAA | `PHI`, `protected health`, `ePHI`, `covered entity`, `BAA` | Access controls, audit controls, transmission security, minimum necessary |
| SOC 2 | `trust service criteria`, `availability`, `processing integrity`, `confidentiality` | CC6, CC7, CC8, CC9 control areas |
| FedRAMP | `federal`, `government`, `FISMA`, `ATO`, `authorization to operate`, `FedRAMP` | NIST SP 800-53 control baseline |
| NIST CSF | `identify`, `protect`, `detect`, `respond`, `recover`, `CSF`, `cybersecurity framework` | CSF function coverage |

---

## Severity Scoring Guide

| Condition | Severity | Rationale |
|---|---|---|
| No authentication on endpoint with sensitive data | critical | Direct exploit path; T1190 applicable |
| Hardcoded credentials or secrets in document text | critical | CWE-798; immediate rotation required |
| No encryption for regulated data at rest or in transit | critical | Compliance violation + data exposure |
| Missing authorization differentiation (all users = admin) | high | Privilege escalation path |
| Regulated data without stated compliance controls | high | Control deficiency; regulatory risk |
| Rate limiting absent from public APIs | high | DoS and abuse vector |
| No input validation requirement stated | medium | Injection surface; CWE-20 |
| Audit logging absent for sensitive operations | medium | SOC 2 CC7 / HIPAA audit control gap |
| Single-instance design for security control point | medium | Availability and resilience gap |
| Security milestones missing from project timeline | low | Process gap; detectable before build |

---

## Pre-Analysis Classifier Logic

The `pre_analysis.py` script uses the following deterministic rules (no LLM):

1. **Document type:** Count keyword frequency per type; classify to the type with highest weighted signal count.
2. **Framework detection:** Substring match against each framework's keyword list; return all matches.
3. **Data flow detection:** Search for terms: `data flow`, `DFD`, `flows to`, `sends to`, `receives from`, `pipeline`, `stream`.
4. **Trust boundary detection:** Search for terms: `trust boundary`, `DMZ`, `zone`, `segment`, `perimeter`, `firewall`, `gateway`.
5. **Critical keywords:** Search for: `no authentication`, `no auth`, `unauthenticated`, `public endpoint`, `admin endpoint`, `hardcoded`, `password:`, `secret:`, `api_key`, `no encryption`, `plaintext`.
6. **Exit code assignment:**
   - Exit 2 if any critical keyword match found OR `critical` gap in compliance check
   - Exit 1 if any framework detected without matching control keywords, OR design gaps detected
   - Exit 0 otherwise
