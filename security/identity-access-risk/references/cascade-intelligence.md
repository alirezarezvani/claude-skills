# Cascade Intelligence

## Consuming secrets-exposure findings
- If `secrets-exposure` found an exposed AWS access key, this IAM anomaly may be the attacker USING that key. Connect the events: same account ID? Same time window? Same region?
- If both secrets-exposure AND this event point to the same identity, confidence += 0.15

## Consuming telemetry-signal-quality findings
- If telemetry-signal-quality flagged high dedup confidence, this is a confirmed unique event
- If it flagged normalization errors, reduce confidence and note data quality issue

## Consuming threat-intelligence findings
- If threat-intelligence identified the source IP as a known threat actor C2 or Tor exit node, upgrade severity by one level and set blast_radius = full_account regardless of actual permissions

## Producing output for downstream agents
- `containment-advisor` will consume your `recommended_action` and `principal_arn` to recommend specific containment steps (disable_user, revoke_session_tokens, quarantine_ec2)
- `incident-classification` may escalate based on your severity assessment
- `compliance-mapping` will use credential_operation or policy_change intent for regulatory analysis
- `internal-audit-assurance` will reference your findings for SOC 2 CC6 (logical access) audit
