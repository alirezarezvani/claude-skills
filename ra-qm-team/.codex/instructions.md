# RA/QM Skills — Codex CLI Instructions

When working on regulatory or quality management tasks, use the RA/QM skill system:

## Routing

1. **Identify the domain:** Regulatory (FDA/MDR), quality (ISO 13485), security (ISO 27001), or privacy (GDPR)
2. **Read the specialist SKILL.md** for detailed instructions

## Python Tools

All scripts in `ra-qm-team/*/scripts/` are stdlib-only and CLI-first:

```bash
python3 ra-qm-team/risk-management-specialist/scripts/risk_matrix_calculator.py --help
python3 ra-qm-team/gdpr-dsgvo-expert/scripts/gdpr_compliance_checker.py --help
```

## Key Skills by Task

| Task | Skill |
|------|-------|
| FDA submissions | regulatory-affairs-head |
| EU MDR compliance | mdr-745-specialist |
| FDA 510(k)/PMA | fda-consultant-specialist |
| ISO 13485 QMS | quality-manager-qms-iso13485 |
| QMS governance | quality-manager-qmr |
| Risk management | risk-management-specialist |
| CAPA management | capa-officer |
| Document control | quality-documentation-manager |
| ISO 13485 audits | qms-audit-expert |
| ISO 27001 ISMS | information-security-manager-iso27001 |
| ISO 27001 audits | isms-audit-expert |
| GDPR compliance | gdpr-dsgvo-expert |

## Rules

- Load only 1-2 skills per request — don't bulk-load
- Always verify outputs against current regulations
