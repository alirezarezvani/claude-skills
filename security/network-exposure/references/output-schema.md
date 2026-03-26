# Output Schema

Every finding payload must conform to this structure:

```json
{
  "finding_id": "NET-2026-XXXX",
  "finding_type": "port_exposure | firewall_rule | segmentation_gap | unencrypted_service | lateral_movement_enabler | vpn_weakness | dns_risk | network_ioc",
  "asset_identifier": "ip_address or hostname",
  "source_zone": "internet | dmz | app_tier | db_tier | admin | workstation | ot_iot",
  "destination_zone": "internet | dmz | app_tier | db_tier | admin | workstation | ot_iot",
  "port": 0,
  "protocol": "TCP | UDP | ICMP",
  "service": "string",
  "service_version": "string or null",
  "encryption_in_transit": true,
  "severity": "Critical | High | Medium | Low | Informational",
  "rule_id": "string or null",
  "rule_text": "string or null",
  "ioc_type": "beaconing | dns_tunneling | large_transfer | c2 | null",
  "ioc_indicator": "string or null",
  "recommended_action": "string",
  "intent": "read_only | mutating/network_change",
  "approval_required": false,
  "evidence_chain": []
}
```
