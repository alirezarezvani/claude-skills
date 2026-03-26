# Proactive Triggers and Output Artifacts

## Proactive Triggers

Surface the following without being asked, whenever the condition is met:

- **Pattern match with no entropy score available**: Cap confidence at 0.70 regardless of other factors — flag this explicitly in `key_findings` as "entropy score unavailable; confidence capped."
- **Secret found in `/ci/`, `.github/`, or any pipeline path**: Flag org-wide blast radius — every developer with repo access may have seen this credential in pipeline logs.
- **Exposure window >14 days**: Treat as assumed-compromise — the T+10 backdoor creation window has elapsed; state "assumed-compromise posture" in rationale.
- **Multiple secret types in the same commit or file**: Flag as potential developer credential dump — all secrets in the commit must be individually classified and assessed.
- **`blast_radius = full_account` AND no CloudTrail or equivalent audit log evidence provided**: Flag that exfiltration cannot be ruled out and that absence of evidence is not evidence of absence.

## Output Artifacts

| When operator asks for... | You produce... |
|---|---|
| Exposure verdict | JSON payload with `intent_type`, `action`, `confidence`, `blast_radius`, `secret_type`, `key_findings`, `evidence_references` |
| Remediation plan | Ordered `remediation_steps` array — each step specifies the exact action, the system/service to act on, and the approver role required |
| Blast radius assessment | Structured table: `secret_type` → `blast_radius_tier` → `attacker_capabilities` → `exposure_window` → `regulatory_implications` |
| Post-incident review checklist | PIR questions 1–6 from the Post-Incident Review section, formatted as a markdown checklist with owner roles assigned |

## Related Skills

- `containment-advisor` — Use when blast_radius is `full_account` or `service_scoped` and confidence >= 0.70 to determine isolation scope. NOT for advisory-only findings below confidence threshold.
- `compliance-mapping` — Use when regulatory_scope includes PCI, GDPR, or HIPAA and a confirmed credential exposure requires notification mapping. NOT for unconfirmed or low-confidence findings.
- `incident-classification` — Use when this skill's output severity is `critical` or `high` to trigger formal incident triage. NOT for findings with `action: verify_false_positive`.
- `telemetry-signal-quality` — Use when the source data source reliability is unknown or flagged as degraded. NOT as a substitute for entropy analysis.
