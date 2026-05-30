# compliance-os

**Compliance OS** — a meta-orchestrator for multi-framework compliance programs. Configure which frameworks apply; compute overlap; simulate audits; consolidate evidence across frameworks.

## What this is

Most compliance teams run **multiple** frameworks in parallel: ISO 27001 + SOC 2 for security, ISO 13485 + FDA QSR for medical devices, ISO 42001 + EU AI Act for AI, GDPR + sector privacy law for personal data. Each framework lives in its own skill (we have 14 existing ra-qm-team skills + 2 new compliance-team-* plugins for ISO 42001 and EU AI Act).

But teams need:
1. A way to **configure** which of the 9 frameworks apply per company profile
2. **Cross-framework overlap** — many controls are the same across frameworks; one piece of evidence often satisfies multiple
3. **Audit simulation** — practice internal audits before the real ones
4. **Unified evidence pool** — collect evidence once, satisfy multiple frameworks

Compliance OS provides exactly that. Four stdlib Python tools + 4 in-depth references + 3 cs-* personas + 3 /cs:* commands.

## Supported frameworks (9)

| ID | Framework | Companion skill |
|---|---|---|
| ISO 27001 | Info security ISMS | `ra-qm-team/skills/information-security-manager-iso27001/` + `isms-audit-expert/` |
| ISO 13485 | Medical device QMS | `ra-qm-team/skills/quality-manager-qms-iso13485/` + `qms-audit-expert/` |
| ISO 42001 | AI Management System | `ra-qm-team/skills/iso42001-specialist/` (new) |
| ISO 14971 | Medical device risk mgmt | `ra-qm-team/skills/risk-management-specialist/` |
| EU AI Act | Regulation (EU) 2024/1689 | `ra-qm-team/skills/eu-ai-act-specialist/` (new) |
| EU MDR 745 | Medical device regulation | `ra-qm-team/skills/mdr-745-specialist/` |
| GDPR | Data protection | `ra-qm-team/skills/gdpr-dsgvo-expert/` |
| SOC 2 | Trust services criteria | `ra-qm-team/skills/soc2-compliance/` |
| FDA QSR | 21 CFR 820 | `ra-qm-team/skills/fda-consultant-specialist/` |

## Quick start

```bash
# Configure which frameworks apply for your company
python skills/compliance-os/scripts/framework_selector.py

# Compute overlap between selected frameworks
python skills/compliance-os/scripts/cross_framework_mapper.py

# Simulate an internal audit
python skills/compliance-os/scripts/audit_simulator.py

# Generate unified evidence checklist
python skills/compliance-os/scripts/evidence_pool_generator.py
```

All four tools run with embedded samples if no JSON is provided. All use stdlib only.

## Slash commands

| Command | Purpose |
|---|---|
| `/cs:compliance-readiness` | 6-question forcing interrogation for compliance program readiness |
| `/cs:aims-audit` | 6-question forcing interrogation specific to ISO 42001 internal audit |
| `/cs:ai-act-readiness` | 6-question forcing interrogation specific to EU AI Act compliance |

## cs-* persona agents

| Agent | Voice |
|---|---|
| `cs-compliance-officer` | Multi-framework orchestrator. "Which frameworks apply, and where do they overlap?" |
| `cs-aims-iso42001` | AIMS implementation operator. "What's the gap against Clauses 4-10?" |
| `cs-ai-act-compliance` | EU AI Act Article-cited operator. "What's the risk tier per Article 6?" |

## What this is NOT

- **NOT executive AI/risk strategy.** For board-level AI / data / risk decisions, see `c-level-advisor/`.
- **NOT a replacement for the per-framework skills.** This orchestrates them. The per-framework skills do the deep work.
- **NOT a binding legal opinion.** Cross-framework mappings reflect published guidance; novel cases need outside counsel.

## License

MIT.
