# cloud-security-posture

**Level:** L4 (Technical) | **Category:** Cloud | **Intent:** `read_only` (posture scanning, drift analysis) + `mutating/device_config_change` (remediation)

Cloud Security Posture Management (CSPM) covering AWS, Azure, and GCP. Evaluates configurations against 40+ CIS Benchmark check IDs, detects misconfigurations, identifies unauthorized configuration drift, and maps every finding to compliance frameworks (CIS, NIST 800-53, SOC 2, PCI DSS, HIPAA). Uses configuration data no older than 24 hours. Cross-account and cross-project resources are always in scope — single-account assessments are never treated as complete.

---

## When to trigger

- Periodic posture scan cycle (recommended: daily)
- IaC deployment event that may introduce misconfigurations
- Drift detected from a known-good baseline
- Another agent reports a cloud misconfiguration (network-exposure, iac-security)
- Pre-certification audit requiring CIS/SOC 2/PCI posture evidence

---

## Key findings per issue

| Field | Description |
|---|---|
| `check_id` | CIS Benchmark check ID (e.g., `CIS-AWS-2.1.1`) |
| `severity_final` | Adjusted for internet exposure, data classification, environment |
| `compliance_mapping` | CIS, NIST 800-53, PCI DSS, SOC 2 control IDs |
| `drift_detected` | Whether config changed from baseline |
| `unauthorized_drift` | True if no change ticket exists for this drift |
| `remediation_command` | CLI command (documented for human execution) |

---

## Severity modifiers applied

Findings are scored based on base CIS severity, then modified by:
- Internet exposure: +1 severity level if resource is publicly reachable
- Data classification: Critical data stores get +1 level
- Production environment: +1 level vs. development
- Compensating controls: -1 level if effective mitigation exists

---

## Intent classification

```
Posture scanning, misconfiguration detection, drift analysis, compliance mapping
  -> read_only

Configuration remediation, resource modification, policy deployment
  -> mutating/device_config_change (requires approval)
```

---

## Works with

**Upstream:** Cloud account configuration APIs, previous scan snapshots (baseline)

**Downstream:**
- `attack-surface-management` — public S3 / cloud storage findings
- `network-exposure` — security group 0.0.0.0/0 findings
- `iac-security` — IaC drift events
- `vulnerability-management` — IAM wildcard policy findings
- `orchestrator` — Critical production findings trigger immediate cascade

---

## Standalone use

```bash
cat cloud-security-posture/SKILL.md
# Paste into system prompt, then send a posture event:

{
  "event_type": "cloud_misconfiguration",
  "severity": "high",
  "raw_payload": {
    "provider": "aws",
    "account_id": "123456789012",
    "region": "us-east-1",
    "resource_type": "s3_bucket",
    "resource_id": "acme-data-prod",
    "check_id": "CIS-AWS-2.1.2",
    "check_name": "S3 bucket public access not blocked",
    "internet_facing": true,
    "data_classification": "pii",
    "environment": "production",
    "last_scan_utc": "2026-03-08T10:00:00Z"
  }
}
```

---

## Runtime Contract

- ../../agents/cloud-security-posture.yaml
