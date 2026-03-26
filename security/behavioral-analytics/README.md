# behavioral-analytics

**Level:** L3 (SOC) | **Category:** Detection | **Intent:** `read_only` (risk scoring, anomaly reporting) + `mutating/credential_operation` (MFA step-up, account suspension)

UEBA agent that establishes behavioral baselines (minimum 30-day window, refreshed every 7 days) for users, service accounts, workstations, and servers. Detects deviations using z-score analysis, peer group comparison (PDS score), and new-behavior weighted signals. Computes entity risk scores every 15 minutes for active entities. Identifies composite insider threat and account takeover patterns. Account lockdown and credential operations require human approval.

---

## When to trigger

- Continuous evaluation cycle (15-minute cadence for active entities)
- Entity risk score crosses 0.60 threshold (SOC alert)
- Entity risk score crosses 0.80 threshold (account suspension recommendation)
- HR action (PIP, termination notice) triggers enhanced monitoring
- `incident-commander` requests behavioral context on a suspected insider

---

## Anomaly dimensions tracked

| Dimension | Soft flag (z-score) | Hard flag (z-score) |
|---|---|---|
| Login time | >= 2.0 | >= 3.0 |
| Login location | New country first-ever | >= 2.0 + new ASN |
| Data volume (outbound) | > mean + 3 SD | > 5x p95 |
| Peer group deviation (PDS) | > 0.6 | > 0.8 |
| New application access | Weighted by sensitivity | HR/financial system = 4 pts |

---

## Composite patterns detected

**Insider threat:**
- Pattern A: Disgruntled + data staging (large outbound + USB/cloud copy + after-hours)
- Pattern B: Pre-departure exfiltration (resignation + bulk email forward + mass download)
- Pattern C: Privileged account abuse (admin rights + off-hours access + lateral movement)

**Account takeover:**
- ATO Pattern 1: Credential change + bulk access + impossible travel
- ATO Pattern 2: Session behavior divergence (new user-agent, geo, timing) after credential change
- ATO Pattern 3: Service account interactive login from unexpected IP + new commands

---

## Key outputs

| Field | Type | Description |
|---|---|---|
| `entity_risk_score` | float (0.0-1.0) | Composite risk score per entity |
| `anomaly_flags` | array | Categorized by dimension: time, volume, peer_group, new_behavior |
| `pattern_match` | string | Insider threat or ATO pattern matched (if any) |
| `recommendation` | string | `monitor`, `mfa_step_up`, `suspend_account` |
| `confidence` | float | Reduced by 0.5 if baseline < 30 days |

---

## Works with

**Upstream:** `detection-engineering` (ML feature inputs)

**Downstream:** SOC analyst (risk >= 0.60), HR system (insider patterns), `incident-commander` (privilege escalation anomalies, ATO), `threat-hunting` (workstation anomalies as hunt leads), cloud security team (service account anomalies)

---

## Standalone use

```bash
cat behavioral-analytics/SKILL.md
# Paste into system prompt, then send a behavioral event:

{
  "event_type": "iam_anomaly",
  "severity": "high",
  "raw_payload": {
    "entity_id": "jsmith@company.com",
    "entity_type": "user",
    "baseline_days": 90,
    "anomaly_signals": {
      "login_time_zscore": 3.4,
      "data_volume_bytes_today": 4500000000,
      "data_volume_p95_bytes": 800000000,
      "new_country_login": "RU",
      "first_ever_hr_system_access": true,
      "hr_action_active": "performance_improvement_plan"
    },
    "peer_group_pds": 0.82
  }
}
```

---

## Runtime Contract

- ../../agents/behavioral-analytics.yaml
