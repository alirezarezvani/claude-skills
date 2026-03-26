# Output Schema

Every asset discovery and finding output must conform to this structure:

```json
{
  "finding_id": "ASM-2026-XXXX",
  "asset_type": "domain | ip | certificate | cloud_resource | open_port | api | admin_interface | shadow_it",
  "asset_identifier": "string",
  "discovery_source": "ct_logs | dns_enum | shodan | cloud_api | active_probe | passive_dns",
  "discovery_timestamp": "ISO8601",
  "exposure_class": "internet-facing | cloud-perimeter | partner-accessible | internal | isolated",
  "exposure_verified": true,
  "exposure_verification_method": "string",
  "risk_score": 0.0,
  "finding_type": "new_exposure | takeover_candidate | cert_expiry | admin_interface | shadow_it | trend_alert",
  "severity": "Critical | High | Medium | Low | Informational",
  "sla_deadline": "ISO8601",
  "recommended_action": "string",
  "in_approved_inventory": true,
  "surface_trend": "expanding | stable | contracting | first_scan",
  "intent": "read_only | mutating/remediation_action",
  "approval_required": false,
  "evidence_chain": []
}
```
