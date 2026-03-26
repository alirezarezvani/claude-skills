# secrets-exposure

**Level:** L4 (Technical) | **Category:** Detection | **Intent:** `read_only` + `mutating/credential_operation`

Detects exposed credentials in code, commits, logs, and configuration files. Classifies secret type, calculates entropy-based confidence, estimates blast radius, and maps the attacker's post-exposure timeline. For high-confidence findings with broad blast radius, recommends key rotation or revocation — which requires human approval before execution.

---

## When to trigger

- A secrets scanner detected a pattern match in a commit, PR diff, or file scan
- A SIEM alert fired on a string matching a known credential pattern (AWS access key, GitHub PAT, Stripe key, etc.)
- A developer reported accidentally committing credentials
- An anomalous AWS CloudTrail event suggests a key may have been used by an unauthorized party
- CI/CD pipeline exit code 2 from `scan_for_secrets.py`

---

## Key outputs

| Field | Type | Description |
|---|---|---|
| `action` | string | `rotate_and_revoke_immediately`, `rotate_and_revoke`, `verify_scope`, `verify_false_positive`, `monitor_only` |
| `intent_type` | string | `mutating` (confidence >= 0.70 + non-minimal blast radius) or `read_only` |
| `confidence` | float | 0.0 – 1.0 based on pattern strength, entropy, file path, variable naming |
| `key_findings` | array | Secret type, blast radius tier, attacker TTPs already in play |
| `rationale` | string | Attacker timeline applied to this specific finding |

---

## Intent classification

```
confidence >= 0.85 AND blast_radius == full_account
  -> rotate_and_revoke_immediately (mutating — requires soc_lead + ciso approval)

confidence >= 0.70 AND blast_radius == service_scoped
  -> rotate_and_revoke (mutating — requires soc_lead + ciso approval)

confidence 0.55-0.70 OR blast_radius == minimal
  -> verify_scope or monitor_only (read_only — no approval gate)

likely false positive (placeholder value, test file, comment)
  -> verify_false_positive (read_only)
```

---

## Blast radius tiers

| Tier | Example secrets | Attacker window |
|---|---|---|
| `full_account` | AWS access key, SSH private key, Stripe live key | T+10 min: backdoor created; T+30 min: data exfil begins |
| `service_scoped` | GitHub PAT, Slack bot token, database URL | T+5 min: private repos cloned; T+30 min: persistence established |
| `minimal` | Test key, recently rotated, no live system access | Low urgency; verify before escalating |

---

## Works with

**Upstream (consumes):**
- `telemetry-signal-quality` — confidence boost if high signal fidelity; confidence reduction if data quality flagged
- `incident-classification` — if SEV1/SEV2 already declared, urgency escalates

**Downstream (feeds):**
- `containment-advisor` — receives blast_radius and secret_type to determine isolation scope
- `compliance-mapping` — receives `credential_operation` intent for GDPR Art.33 / PCI DSS Req.3 analysis
- `metrics-reporting` — receives confidence score for MTTR tracking

---

## Standalone use

```bash
# Paste SKILL.md into AnythingLLM or any LLM as system prompt, then send:
cat secrets-exposure/SKILL.md

# User message example:
{
  "event_type": "secret_exposure",
  "severity": "critical",
  "raw_payload": {
    "file_path": "config/database.py",
    "line_number": 42,
    "matched_pattern": "aws_access_key",
    "matched_value": "AKIAIOSFODNN7EXAMPLE",
    "commit_hash": "a1b2c3d",
    "branch": "main",
    "repo": "acme-corp/backend"
  }
}
```

---

## Pre-analysis script

`scripts/scan_for_secrets.py` runs before the LLM call and performs deterministic regex + entropy scanning:

```bash
# Scan a directory
python secrets-exposure/scripts/scan_for_secrets.py /path/to/repo

# Get JSON output for SecurityFact ingestion
python secrets-exposure/scripts/scan_for_secrets.py . --json --output findings.json

# CI/CD gate — exits 2 if critical findings
python secrets-exposure/scripts/scan_for_secrets.py . --severity high
```

**15 patterns covered:** AWS access key/secret, GitHub PAT/OAuth/Actions tokens, Stripe live/test keys, Slack bot token, PEM private keys, JWT secrets, database connection strings, Google API keys, SSH private keys, SendGrid keys, generic high-entropy secrets.

---

## Reference documents

| File | Contents |
|---|---|
| `references/secret_patterns.md` | Regex patterns, entropy thresholds, blast radius per secret type |
| `references/attacker_timeline.md` | Full TTP timeline per secret type (AWS, GitHub, database) |
