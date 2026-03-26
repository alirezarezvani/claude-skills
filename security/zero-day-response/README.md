# zero-day-response

**Level:** L3 (SOC) | **Category:** Response | **Intent:** `read_only` (monitoring, planning) + `mutating/device_config_change` (control deployment) + `mutating/external_communication` (customer notification)

Coordinates compensating controls for confirmed zero-day vulnerabilities where no vendor patch exists. Applies a three-condition classification test to confirm true zero-day status, scopes organizational exposure using an asset inventory scoring model, selects compensating controls, tracks vendor patch timelines, and drives structured executive and customer communications. Nation-state exploitation of the vulnerability automatically escalates all exposure scores to Critical.

---

## When to trigger

- Threat intelligence report: no-patch + active exploitation in the wild + you use the affected product
- CISA KEV addition for a technology in your asset inventory with no vendor patch
- Vendor advisory: critical severity + no patch available + PoC published
- A PoC-only vulnerability gains confirmed exploitation (status upgrade)
- ISAC bulletin indicating sector-targeted active exploitation

---

## Three-condition zero-day test

All three must be true before activating the zero-day response track:

```
1. No vendor patch available (or patch < 24 hours old with insufficient testing time)
2. Active exploitation confirmed in the wild (not just PoC or theoretical)
3. Your organization uses the affected product version
```

If condition 2 is unconfirmed, route to vulnerability-management for standard SLA processing.

---

## Key outputs

| Field | Type | Description |
|---|---|---|
| `exposure_score` | int (0-9) | Per-asset score: `(internet_facing × 3) + (data_sensitivity × 2) + (patch_complexity × 1)` |
| `compensating_controls` | array | Selected from: WAF rule, network block, feature disable, service isolation, detection sensitivity increase |
| `vendor_patch_timeline` | object | 7-milestone tracker updated every 48 hours |
| `communication_matrix` | array | Target, timeline, channel for each stakeholder (CISO, CTO, Board, Legal, customers, regulators) |
| `exploitation_evidence_found` | bool | Whether active exploitation against your systems was detected |

---

## Compensating control options

| Control | When to apply | Approval |
|---|---|---|
| WAF rule | Web-exploitable vulnerability | device_config_change |
| Network block | Network-layer attack surface | device_config_change |
| Feature disable | Specific feature is the attack vector | device_config_change |
| Service isolation | Service is exploitable; isolation accepted | device_config_change + CISO |
| Detection sensitivity increase | No viable prevention — rely on detection | read_only |

---

## Works with

**Upstream:** Threat intelligence feeds, CISA KEV, vendor advisories, ISAC, CMDB/asset inventory

**Downstream:** `incident-commander` (if active exploitation against your org is confirmed — both agents stay active in parallel)

---

## Standalone use

```bash
cat zero-day-response/SKILL.md
# Paste into system prompt, then send a zero-day advisory:

{
  "event_type": "zero_day",
  "severity": "critical",
  "raw_payload": {
    "cve_id": "CVE-2024-XXXXX",
    "product": "Ivanti Connect Secure",
    "version_affected": "< 22.7R2.5",
    "patch_available": false,
    "exploitation_in_wild_confirmed": true,
    "exploitation_sectors": ["government", "financial_services"],
    "your_asset_inventory": [
      {"hostname": "vpn-gw-01", "version": "22.6R1", "internet_facing": true, "data_classification": "confidential"}
    ],
    "vendor_advisory_url": "https://..."
  }
}
```

---

## Runtime Contract

- ../../agents/zero-day-response.yaml
