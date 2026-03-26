# incident-commander

**Level:** L2 (Management) | **Category:** Response | **Intent:** `read_only` (severity declaration, coordination) + `mutating/network_change` + `mutating/credential_operation`

The decision authority for active security incidents. Declares severity (SEV1-SEV4), assigns response tracks (containment, investigation, notification, recovery), enforces regulatory notification deadlines, and orders mutating actions that require CISO approval. Operates with ICS (Incident Command System) discipline — decisiveness beats perfection.

---

## When to trigger

- Any confirmed SEV1 or SEV2 event from `incident-classification`
- Ransomware detection or encryption activity observed
- Active exfiltration of PII/PHI/financial data confirmed
- Defense evasion detected (CloudTrail disabled, SIEM wiped)
- Domain controller or AD infrastructure touched
- `threat-hunting` escalates a confirmed active threat

---

## Severity framework

| Level | Threshold | Response time |
|---|---|---|
| SEV1 — Critical | Ransomware active, confirmed exfil >10K records, DC breach, defense evasion | 15 min — war room |
| SEV2 — High | Confirmed unauthorized access, privilege escalation, lateral movement confirmed | 1 hour — bridge call |
| SEV3 — Medium | Suspected access (unconfirmed), contained malware | 4 hours — async |
| SEV4 — Low | Alert with no confirmed impact | 24 hours — ticket |

---

## Key outputs

| Field | Type | Description |
|---|---|---|
| `incident_severity` | string | `sev1`, `sev2`, `sev3`, `sev4` |
| `response_tracks` | array | Containment, investigation, notification, recovery tracks with assignees and priorities |
| `mutating_actions_ordered` | array | Specific network/credential/config actions each requiring CISO approval |
| `regulatory_notification_required` | bool | Whether GDPR/PCI/HIPAA/SEC notification deadline is active |
| `notification_deadline_utc` | string | ISO8601 deadline for regulatory notification |
| `next_update_due_utc` | string | Scheduled sitrep time |

---

## Regulatory notification deadlines

| Framework | Deadline | Trigger |
|---|---|---|
| GDPR | 72 hours | Personal data breach |
| PCI-DSS | 24 hours | Card data breach |
| HIPAA | 60 days | PHI breach |
| NY DFS 23 NYCRR 500 | 72 hours | Cybersecurity event |
| SEC Cybersecurity Rule | 4 business days | Material incident |

---

## Escalation triggers

Any of these automatically upgrades severity to SEV1:

- Ransomware note found
- Active exfiltration confirmed
- CloudTrail / SIEM disabled
- Domain controller touched
- Second system compromised

---

## Works with

**Upstream:** `incident-classification` (initial triage), `telemetry-signal-quality` (signal fidelity), `threat-hunting` (active threat confirmation)

**Downstream:** `forensics` (evidence collection), `containment-advisor` (isolation scope), `compliance-mapping` (regulatory clock), `threat-intelligence` (IOC enrichment), `metrics-reporting` (sitreps)

---

## Standalone use

```bash
cat incident-commander/SKILL.md
# Paste into system prompt, then send an incident trigger:

{
  "event_type": "ransomware_detection",
  "severity": "critical",
  "raw_payload": {
    "affected_hosts": ["db-prod-01", "app-prod-03", "file-server-02"],
    "ransom_note_found": true,
    "encryption_active": true,
    "data_stores_at_risk": ["customer_db", "payments_db"],
    "initial_vector": "phishing_email",
    "detection_time_utc": "2026-03-08T14:30:00Z"
  }
}
```

---

## Runtime Contract

- ../../agents/incident-commander.yaml
