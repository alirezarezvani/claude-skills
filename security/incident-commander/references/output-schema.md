# Output Schema

```json
{
  "agent_slug": "incident-commander",
  "intent_type": "read_only",
  "incident_severity": "sev1|sev2|sev3|sev4",
  "summary": "string",
  "declared_at_utc": "ISO8601",
  "affected_systems": ["string"],
  "response_tracks": [
    {
      "track": "containment|investigation|notification|recovery",
      "assigned_to": "agent_slug or human_role",
      "priority": "immediate|1h|4h|24h",
      "actions": ["string"]
    }
  ],
  "mutating_actions_ordered": [
    {
      "action": "string",
      "intent_type": "mutating",
      "mutating_category": "network_change|credential_operation|device_config_change",
      "requires_approval": true,
      "approver_role": "ciso"
    }
  ],
  "regulatory_notification_required": true,
  "regulatory_frameworks": ["GDPR"],
  "notification_deadline_utc": "ISO8601",
  "next_update_due_utc": "ISO8601",
  "confidence": 0.0,
  "timestamp_utc": "ISO8601"
}
```
