# containment-advisor

**Level:** L3 (SOC) | **Category:** Response | **Intent:** `read_only` (monitoring-only) + `mutating/credential_operation` + `mutating/network_change` + `mutating/remediation_action`

Recommends the most appropriate containment strategy for active incidents across 10 threat types. Evaluates blast radius, whether the threat is active or historical, production impact, and reversibility before composing primary and secondary strategies. Never executes containment — all state-changing actions require human approval from `soc_lead` and `ciso`.

---

## When to trigger

- Any confirmed or suspected active threat requiring containment decision
- `incident-commander` requests containment scope from Operations Section
- `forensics` identifies Patient Zero and isolation is needed
- Active session compromise, ransomware spreading, lateral movement in progress

---

## Threat types covered

| Threat type | Primary containment approach |
|---|---|
| `credential_exposure` | Revoke session tokens, rotate credentials |
| `iam_anomaly` | Quarantine IAM role, apply explicit deny policy |
| `network_intrusion` | Block source IP, isolate network segment |
| `malware_detected` | Quarantine host, terminate process |
| `ransomware` | Isolate affected segment, disable service accounts |
| `data_exfiltration` | Block egress path, revoke data-access permissions |
| `insider_threat` | Suspend account, legal hold, HR notification |
| `supply_chain` | Block compromised package in registry |
| `secret_in_repo` | Rotate/revoke exposed credential immediately |
| `container_escape` | Terminate container, isolate node |

---

## Key outputs

| Field | Type | Description |
|---|---|---|
| `action` | string | Primary containment action |
| `secondary_action` | string | Defense-in-depth secondary action |
| `mutating_category` | string | `credential_operation`, `network_change`, or `remediation_action` |
| `production_impact` | string | Explicit statement: will or will not cause service degradation |
| `urgency` | string | `immediate`, `urgent`, or `scheduled` |
| `reversibility` | string | Assessment of how easily the action can be undone |

Approver roles for all mutating actions: `["soc_lead", "ciso"]` — auto-approval is never recommended.

---

## Works with

**Upstream:** `incident-classification` (event routing), `forensics` (patient zero and isolation scope)

**Downstream:** MCP execution layer receives the approved containment action

---

## Standalone use

```bash
cat containment-advisor/SKILL.md
# Paste into system prompt, then send an active threat context:

{
  "event_type": "ransomware",
  "severity": "critical",
  "raw_payload": {
    "threat_active": true,
    "affected_systems": ["file-server-01", "file-server-02"],
    "network_segment": "10.0.1.0/24",
    "service_accounts_used": ["svc-backup", "svc-fileaccess"],
    "production_services_at_risk": ["hr-portal", "payroll-system"],
    "blast_radius": "full_segment"
  }
}
```

---

## Runtime Contract

- ../../agents/containment-advisor.yaml
