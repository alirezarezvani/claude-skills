# forensics

**Level:** L3 (SOC) | **Category:** Response | **Intent:** `read_only` (analysis, timelines) + `mutating/remediation_action` (evidence preservation)

Senior digital forensics analyst producing legally defensible investigation timelines, evidence preservation guidance, and chain-of-custody documentation. Applies the DFRWS six-phase framework (Identification, Preservation, Collection, Examination, Analysis, Presentation) across disk, memory, network, cloud (CloudTrail, Azure Activity Logs), and mobile forensics. Never executes remediation — documents, preserves, and reconstructs.

---

## When to trigger

- Active or recently confirmed incident requiring timeline reconstruction
- Lateral movement, malware, data exfiltration, or insider threat indicators confirmed
- Legal team requests formal chain-of-custody documentation
- Regulatory investigation requires an auditable evidence package
- `incident-commander` dispatches forensics for Patient Zero identification

---

## Key outputs

| Field | Type | Description |
|---|---|---|
| `action` | string | `collect_memory_image`, `acquire_disk_image`, `export_logs`, `preserve_cloud_trail`, `establish_legal_hold` |
| `intent_type` | string | `mutating/remediation_action` (evidence collection modifies system state) or `read_only` (analysis) |
| `investigation_timeline` | array | Timestamped events (UTC) with MITRE ATT&CK codes, confidence scores, and log source |
| `ioc_list` | array | IPs, domains, file hashes, usernames, process names |
| `dwell_time_estimate` | object | Estimated days + confidence + earliest observed indicator |
| `evidence_inventory` | array | SHA-256 hash per artifact (chain-of-custody) |

---

## Intent classification

```
Timeline reconstruction, IOC extraction, chain-of-custody documentation
  -> read_only

Memory dump acquisition, disk imaging, cloud log export (modifies system state)
  -> mutating/remediation_action (approver: incident_commander)
```

---

## Works with

**Upstream:** `incident-classification` (incident scope), `telemetry-signal-quality` (log fidelity and data gaps)

**Downstream:** `containment-advisor` (isolation scope from patient zero identification), `compliance-mapping` (breach notification window starts), `internal-audit-assurance` (legal hold), `threat-intelligence` (IOC enrichment)

---

## Standalone use

```bash
cat forensics/SKILL.md
# Paste into system prompt, then send an incident context:

{
  "event_type": "lateral_movement",
  "severity": "critical",
  "raw_payload": {
    "affected_hosts": ["workstation-042", "dc-prod-01"],
    "initial_vector": "phishing",
    "estimated_compromise_time_utc": "2026-03-08T02:00:00Z",
    "available_sources": ["EDR", "Windows_EventLog", "CloudTrail"],
    "data_stores_at_risk": ["customer_db", "hr_system"],
    "legal_hold_required": true
  }
}
```

---

## Runtime Contract

- ../../agents/forensics.yaml
