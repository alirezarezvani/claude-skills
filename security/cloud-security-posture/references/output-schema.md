# Output Schema

Every finding payload must conform to this structure:

```json
{
  "finding_id": "CSPM-2026-XXXX",
  "check_id": "AWS-XX | AZ-XX | GCP-XX",
  "provider": "AWS | Azure | GCP",
  "account_id": "string",
  "region": "string",
  "resource_id": "string",
  "resource_type": "string",
  "environment": "production | staging | development | unknown",
  "finding_status": "fail | pass | not_applicable",
  "severity_base": "Critical | High | Medium | Low",
  "severity_final": "Critical | High | Medium | Low",
  "severity_modifiers": [],
  "compliance_mapping": {
    "cis": "string or null",
    "nist_800_53": "string or null",
    "pci_dss": "string or null",
    "soc2": "string or null"
  },
  "drift_detected": false,
  "drift_previous_value": "string or null",
  "drift_new_value": "string or null",
  "drift_change_ticket": "string or null",
  "unauthorized_drift": false,
  "remediation_command": "string",
  "intent": "read_only | mutating/device_config_change",
  "approval_required": false,
  "scan_timestamp": "ISO8601",
  "evidence_chain": []
}
```
