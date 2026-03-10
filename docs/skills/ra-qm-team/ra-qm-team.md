---
title: "Regulatory Affairs & Quality Management Skills"
description: "Regulatory Affairs & Quality Management Skills - Claude Code skill from the Regulatory & Quality domain."
---

# Regulatory Affairs & Quality Management Skills

**Domain:** Regulatory & Quality | **Skill:** `ra-qm-team` | **Source:** [`ra-qm-team/SKILL.md`](https://github.com/alirezarezvani/claude-skills/tree/main/ra-qm-team/SKILL.md)

---


# Regulatory Affairs & Quality Management Skills

12 production-ready compliance skills for HealthTech and MedTech organizations.

## Quick Start

### Claude Code
```
/read ra-qm-team/regulatory-affairs-head/SKILL.md
```

### Codex CLI
```bash
npx agent-skills-cli add alirezarezvani/claude-skills/ra-qm-team
```

## Skills Overview

| Skill | Folder | Focus |
|-------|--------|-------|
| Regulatory Affairs Head | `regulatory-affairs-head/` | FDA/MDR strategy, submissions |
| Quality Manager (QMR) | `quality-manager-qmr/` | QMS governance, management review |
| Quality Manager (ISO 13485) | `quality-manager-qms-iso13485/` | QMS implementation, doc control |
| Risk Management Specialist | `risk-management-specialist/` | ISO 14971, FMEA, risk files |
| CAPA Officer | `capa-officer/` | Root cause analysis, corrective actions |
| Quality Documentation Manager | `quality-documentation-manager/` | Document control, 21 CFR Part 11 |
| QMS Audit Expert | `qms-audit-expert/` | ISO 13485 internal audits |
| ISMS Audit Expert | `isms-audit-expert/` | ISO 27001 security audits |
| Information Security Manager | `information-security-manager-iso27001/` | ISMS implementation |
| MDR 745 Specialist | `mdr-745-specialist/` | EU MDR classification, CE marking |
| FDA Consultant | `fda-consultant-specialist/` | 510(k), PMA, QSR compliance |
| GDPR/DSGVO Expert | `gdpr-dsgvo-expert/` | Privacy compliance, DPIA |

## Python Tools

17 scripts, all stdlib-only:

```bash
python3 risk-management-specialist/scripts/risk_matrix_calculator.py --help
python3 gdpr-dsgvo-expert/scripts/gdpr_compliance_checker.py --help
```

## Rules

- Load only the specific skill SKILL.md you need
- Always verify compliance outputs against current regulations
