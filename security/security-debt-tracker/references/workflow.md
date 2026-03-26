# Security Debt Tracker — Workflow Reference

## Debt Aging Model

Security debt is the accumulation of unresolved security findings past their assigned SLA. The `security-debt-tracker` skill models debt using three concepts: bucket classification, SLA breach counting, and accumulation rate.

### Why Debt Aging Matters

A single finding open beyond its SLA is a policy exception. Ten findings open 2× their SLA is a program failure. The debt tracker distinguishes between these states by tracking not just breach presence but breach magnitude and the rate at which debt is accumulating vs. being resolved.

---

## SLA Breach Logic

### SLA Assignment

SLA days are assigned per finding based on CVSS severity and EPSS exploitation probability:

| Severity | Base SLA | EPSS > 0.5 SLA |
|---|---|---|
| Critical | 15 days | 7 days |
| High | 30 days | 15 days |
| Medium | 60 days | 30 days |
| Low | 90 days | 60 days |

If a finding provides an explicit `sla_days` field, that value overrides the computed SLA.

### Breach Detection

A finding is breached when `age_days >= sla_days`. Breach magnitude determines bucket placement:
- `age_days < sla_days` → `current` (no breach)
- `sla_days <= age_days < 2 × sla_days` → `overdue` (single-breach)
- `age_days >= 2 × sla_days` → `critical_debt` (double-breach — program failure indicator)

---

## Accumulation Rate Formula

```
accumulation_rate = new_findings_per_week - closed_findings_per_week

new_findings_per_week = count(opened_date within last 30 days) / 4.33
closed_findings_per_week = count(closed_date within last 30 days) / 4.33
```

A positive accumulation rate means the organization is creating security debt faster than it is resolving it. This is a leading indicator of posture degradation and should trigger program-level intervention before SLA breaches occur.

### Accumulation Rate Interpretation

| Rate | Direction | Meaning |
|---|---|---|
| > 5 net new/week | Growing | Capacity crisis — remediation velocity insufficient |
| 1–5 net new/week | Growing | Normal growth — monitor; review at next passive scan |
| -1 to +1 net new/week | Stable | Program operating within capacity |
| < -1 net new/week | Reducing | Debt being actively cleared — positive signal |

---

## Exit Code Semantics

Exit codes are designed for programmatic consumption by `cs-security-program-manager` and CI/CD integrations:

| Code | Condition | Action Required |
|---|---|---|
| 0 | No overdue findings AND accumulation_rate <= 0 | Document clean digest; no routing |
| 1 | overdue_count > 0 OR accumulation_rate > 0 | Route to vulnerability-management; alert security manager |
| 2 | Any critical/high finding in critical_debt bucket | Immediate routing to cs-security-analyst + ciso-brief-generator |

Exit code 2 takes precedence. If both exit code 1 and 2 conditions are true, exit code 2 is returned.

---

## Integration with Passive Scan Workflow

The security-debt-tracker is always Step 1 in the Proactive Security Scan (SC) workflow run by `cs-security-program-manager`. This ordering is intentional: debt aging is the primary passive signal. All other scan steps (ASM drift, vulnerability SLA, behavioral baselines) provide context to the debt picture but do not override it.

### Passive Scan Integration Pattern

```
[sc-security-program-manager: SC workflow]
  Step 1: security-debt-tracker (exit 0/1/2) ← PRIMARY SIGNAL
  Step 2: attack-surface-management          ← CONTEXT
  Step 3: vulnerability-management           ← CONTEXT
  Step 4: behavioral-analytics               ← CONTEXT
  Step 5: compile digest using all signals
```

A finding is only routed to `cs-security-analyst` (reactive workflow) when:
1. It is severity Critical or High, AND
2. It appears in the `critical_debt` bucket (SLA breached 2×+), AND
3. At least one other passive scan step confirms the risk (e.g., ASM shows the asset exposed, or vuln-mgmt shows no patch scheduled)

---

## QoQ Comparison Guidance

The passive scan digest must include a quarter-over-quarter comparison. To support this, the debt tracker output should be persisted between scans:

```bash
# Recommended: save each scan digest
python security-debt-tracker_tool.py --output json > /var/log/usap/debt-$(date +%Y%m%d).json
```

QoQ delta fields to compare:
- `debt_summary.sla_breach_count`: Are we breaching more or fewer SLAs?
- `debt_summary.critical_debt_count`: Is critical debt growing or shrinking?
- `debt_summary.accumulation_rate`: Is the trend improving?

---

## References

- NIST SP 800-40 Rev. 4 — Guide to Enterprise Patch Management Planning
- CIS Control 7 — Continuous Vulnerability Management
- OWASP Vulnerability Management Guide
- `governance/findings-tracker/SKILL.md` — upstream findings lifecycle management
- `governance/vulnerability-management/SKILL.md` — downstream remediation tracking
