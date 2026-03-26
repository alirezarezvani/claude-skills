# security-debt-tracker

**Domain:** Governance | **Level:** L3 (SOC/Analyst) | **Intent:** analyze

Analyzes aging security findings to surface SLA breach counts, debt accumulation rate, and debt bucket classification. Used as the primary passive scan signal by `cs-security-program-manager`.

## Quick Start

```bash
# Run with sample findings
python scripts/security-debt-tracker_tool.py --input expected_outputs/sample_output.json --output json

# Pipe findings from findings-tracker
python ../findings-tracker/scripts/findings-tracker_tool.py --output json \
  | python scripts/security-debt-tracker_tool.py --output json

# Inline test — critical debt scenario
echo '{"findings": [{"id": "F-001", "severity": "critical", "age_days": 45, "sla_days": 15}]}' \
  | python scripts/security-debt-tracker_tool.py --output json
echo "Exit code: $?"  # Expect 2
```

## Exit Codes

| Code | Meaning |
|---|---|
| 0 | Debt stable — no SLA breaches, accumulation rate <= 0 |
| 1 | Debt accumulating — overdue items present or positive accumulation rate |
| 2 | Critical debt — critical/high finding with SLA breached 2x or more |

## Input Schema

```json
{
  "findings": [
    {
      "id": "F-001",
      "severity": "critical",
      "age_days": 45,
      "sla_days": 15,
      "epss": 0.0,
      "opened_date": "2026-01-15T00:00:00Z",
      "closed_date": null,
      "status": "open"
    }
  ]
}
```

## Debt Buckets

| Bucket | Condition |
|---|---|
| `current` | age_days < sla_days |
| `overdue` | sla_days <= age_days < 2 × sla_days |
| `critical_debt` | age_days >= 2 × sla_days |

## Routing

- `critical_unmitigated > 0` → `cs-security-analyst` (AT workflow) + `ciso-brief-generator`
- `exit_code == 1` → `vulnerability-management`
- `exit_code == 0` → no routing required

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Full LLM system prompt and debt aging methodology |
| `scripts/security-debt-tracker_tool.py` | Debt analysis CLI tool |
| `references/workflow.md` | Debt aging model and SLA breach logic |
| `assets/templates/output-template.json` | Output schema template |
| `expected_outputs/sample_output.json` | Representative tool output |

## Related Skills

- `governance/findings-tracker` — upstream source of findings data
- `governance/vulnerability-management` — downstream remediation routing
- `governance/ciso-brief-generator` — board visibility on critical debt
- `governance/security-posture-score` — consumes debt signals for posture score
