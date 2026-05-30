# compliance-team-iso42001

Standalone plugin for **ISO/IEC 42001:2023 — AI Management Systems (AIMS)** compliance.

**Dual-published**: also bundled inside `ra-qm-skills` (`../skills/iso42001-specialist/`). The content in `./skills/iso42001-specialist/` mirrors `../skills/iso42001-specialist/`; `scripts/sync_skill_bundles.py` keeps them in sync.

See `./skills/iso42001-specialist/SKILL.md` for the full skill documentation.

## What this is

ISO/IEC 42001:2023 is the first international management-system standard for artificial intelligence (published Dec 2023). It mirrors the structure of ISO 9001 / 27001 / 13485 (Annex SL high-level structure) and prescribes how an organization establishes, implements, maintains, and continually improves an **AI Management System (AIMS)**.

This plugin gives a compliance team three deterministic tools to operate ISO 42001 at the internal-audit level:

1. **`aims_gap_analyzer.py`** — scores Clauses 4–10 coverage from an evidence inventory; outputs gap matrix + remediation priority
2. **`ai_risk_register_builder.py`** — constructs the AI risk register required by Clause 6 + Annex A.5, mapping risks to Annex A controls
3. **`aims_audit_scheduler.py`** — generates the Clause 9.2 internal audit 12-month plan (scope, frequency, auditor independence)

## What this is NOT

- **NOT an executive AI strategy skill.** For build-vs-buy, cost economics, board-level AI risk, see `c-level-advisor/chief-ai-officer-advisor/`.
- **NOT an EU AI Act compliance skill.** For Regulation (EU) 2024/1689 conformity assessment, Annex III classification, GPAI obligations, see `ra-qm-team/compliance-team-eu-ai-act/`.
- **NOT a generic ISMS skill.** For ISO 27001 information-security controls, see `ra-qm-team/skills/information-security-manager-iso27001/`.

## Critical scope boundary

ISO 42001 governs the **management system**. It does NOT prescribe specific AI risk thresholds, model evaluation methods, or technical controls. Those come from companion standards:

- **ISO/IEC 23894:2023** — AI risk management process (input to your risk register)
- **ISO/IEC 22989:2022** — AI concepts and terminology
- **ISO/IEC 38507:2022** — Governance implications of AI for organizations
- **NIST AI RMF 1.0** — US risk-management framework (voluntary; maps cleanly to 42001)

The skill's `cross_framework_mapping_ai.md` reference shows the alignment.

## Quick start

```bash
# Gap analysis from your AIMS evidence inventory
python skills/iso42001-specialist/scripts/aims_gap_analyzer.py
python skills/iso42001-specialist/scripts/aims_gap_analyzer.py path/to/evidence.json

# AI risk register
python skills/iso42001-specialist/scripts/ai_risk_register_builder.py path/to/risks.json

# Internal audit 12-month plan
python skills/iso42001-specialist/scripts/aims_audit_scheduler.py path/to/scope.json
```

All three tools run with embedded samples if no JSON path is provided.

## License

MIT.
