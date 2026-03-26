# risk-threat-modeling

**Level:** L1 (Architecture) | **Category:** Risk | **Intent:** `read_only` exclusively

Principal threat modeling specialist applying STRIDE, PASTA, and LINDDUN methodologies to new systems, features, and architecture changes. Builds Level 0 and Level 1 DFDs, applies STRIDE per element, maps every threat to MITRE ATT&CK, scores risk using Likelihood x Impact (0-25 scale), and produces prioritized mitigations in three time horizons: immediate / sprint / architectural. Entirely advisory — intent is always read_only.

---

## When to trigger

- New system design submitted for security review
- Significant feature addition with data flow changes
- Architecture change request (new external integrations, trust boundary changes)
- Pre-development security review as part of Secure SDLC
- Post-incident: threat model the affected system retrospectively to find missed threats

---

## Methodologies applied

| Methodology | Focus | Best for |
|---|---|---|
| STRIDE | Spoofing, Tampering, Repudiation, Information disclosure, DoS, Elevation | System components and data flows |
| PASTA | Process for Attack Simulation and Threat Analysis (attacker-centric) | Business impact prioritization |
| LINDDUN | Privacy threat modeling | Systems processing PII, PHI, or financial data |

---

## Key outputs

| Field | Type | Description |
|---|---|---|
| `threat_list` | array | Per-threat: ID, STRIDE category, component, MITRE ATT&CK technique, risk score (0-25), risk level, existing controls, mitigation |
| `attack_trees` | array | Goal-decomposed attacker path diagrams |
| `overall_risk_rating` | string | `critical`, `high`, `medium`, or `low` |
| `trust_boundaries` | array | Identified trust boundaries in the system |
| `mitre_coverage_map` | object | ATT&CK tactic coverage from TA0001 through TA0010 |

---

## Risk scoring

```
risk_score = likelihood (1-5) × impact (1-5)

risk_level:
  20-25: Critical — block launch
  15-19: High — mitigate before launch
  10-14: Medium — mitigate within sprint
  5-9:   Low — track and mitigate within quarter
  1-4:   Info — document and accept with owner sign-off
```

---

## Works with

**Upstream:** System design documents, architecture diagrams, `security-architecture` review output

**Downstream:** `findings-tracker` (threat model findings), `sast-dast-coordinator` (code-level threats requiring scanning), `detection-engineering` (detection requirements from identified TTPs)

---

## Standalone use

```bash
cat risk-threat-modeling/SKILL.md
# Paste into system prompt, then send a system design context:

{
  "event_type": "threat_model_request",
  "severity": "medium",
  "raw_payload": {
    "system_name": "Payment Processing API",
    "components": ["React SPA", "Node.js API Gateway", "PostgreSQL DB", "Stripe API"],
    "data_flows": [
      "User -> API Gateway (HTTPS, card data)",
      "API Gateway -> Stripe (HTTPS, card data)",
      "API Gateway -> PostgreSQL (internal, transaction records)"
    ],
    "external_actors": ["Customer browser", "Stripe API", "Internal admin users"],
    "data_classification": "PCI_DSS_scope",
    "trust_boundaries": ["Internet/DMZ", "DMZ/Internal", "Internal/Stripe"],
    "existing_controls": ["WAF", "TLS 1.3", "field-level encryption"]
  }
}
```

---

## Runtime Contract

- ../../agents/risk-threat-modeling.yaml
