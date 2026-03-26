# identity-access-risk

**Level:** L4 (Technical) | **Category:** Identity | **Intent:** `read_only` + `mutating/credential_operation` + `mutating/policy_change`

Analyzes IAM anomalies, privilege escalation attempts, unusual access patterns, and overprivileged identities. Applies 5 CloudTrail detection patterns (enumeration burst, backdoor creation, defense evasion, role assumption chains, data exfil precursors) and maps to MITRE ATT&CK. Recommends specific IAM actions — access revocations and policy corrections require human approval.

---

## When to trigger

- CloudTrail alert for AssumeRole from an unrecognized account or region
- Root account usage detected for anything other than billing
- MFA bypass or authentication without MFA on a sensitive account
- Cross-account AssumeRole chain with 3+ hops
- Burst of enumeration API calls: ListUsers, DescribeInstances, ListAllMyBuckets
- Defense evasion events: StopLogging, DeleteTrail, DeleteDetector
- Dormant identity (inactive 90+ days) suddenly making API calls
- Impossible travel: same identity authenticated from two regions within 60 minutes

---

## Key outputs

| Field | Type | Description |
|---|---|---|
| `action` | string | `revoke_session_tokens`, `disable_user`, `detach_overprivileged_policy`, `require_mfa_reenrollment`, `apply_permission_boundary`, `quarantine_role`, `flag_for_access_review`, `investigate_automation` |
| `intent_type` | string | `mutating` (severity critical/high + non-minimal blast radius) or `read_only` |
| `confidence` | float | 0.25 (isolated call from known IP) to 0.99 (root usage or defense evasion) |
| `key_findings` | array | Anomaly types matched, CloudTrail patterns detected, blast radius tier |

---

## Intent classification

```
severity IN [critical, high] AND blast_radius NOT minimal:
  credential revocation  -> mutating/credential_operation  (approver: soc_lead, ciso)
  policy correction      -> mutating/policy_change         (approver: soc_lead, ciso)

severity IN [medium, low] OR blast_radius == minimal:
  -> read_only  (flag_for_access_review or investigate_automation)
```

Defense evasion events (StopLogging, DeleteTrail, DeleteDetector) immediately set confidence = 0.99 and severity = Critical regardless of other indicators.

---

## Works with

**Upstream:** `secrets-exposure` (if an exposed AWS key was used, this agent confirms it), `telemetry-signal-quality`, `threat-intelligence` (known C2 IP upgrades blast radius to full_account)

**Downstream:** `containment-advisor`, `incident-classification`, `compliance-mapping` (SOC 2 CC6), `internal-audit-assurance`

---

## Standalone use

```bash
cat identity-access-risk/SKILL.md
# Paste into system prompt, then send a CloudTrail event JSON:

{
  "event_type": "iam_anomaly",
  "severity": "critical",
  "raw_payload": {
    "eventName": "StopLogging",
    "sourceIPAddress": "185.220.101.47",
    "principalId": "AROAIOSFODNN7EXAMPLE:session",
    "accountId": "123456789012",
    "eventTime": "2026-03-08T04:22:11Z"
  }
}
```

---

## Pre-analysis scripts

```bash
# Detect privilege escalation paths in an IAM policy JSON
python identity-access-risk/scripts/analyze_iam_policy.py policy.json

# Pipe directly from AWS CLI
aws iam get-policy-version --policy-arn arn:aws:iam::...:policy/... --version-id v1 \
  | jq '.PolicyVersion.Document' | python identity-access-risk/scripts/analyze_iam_policy.py -
```

Detects 12 privilege escalation combinations including CreatePolicyVersion, AttachGroupPolicy, PassRole + Lambda, iam:*, and multi-hop AssumeRole chains.

---

## Runtime Contract

- ../../agents/identity-access-risk.yaml
