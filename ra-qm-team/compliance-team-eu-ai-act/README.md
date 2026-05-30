# compliance-team-eu-ai-act

Standalone plugin for **Regulation (EU) 2024/1689 — the EU Artificial Intelligence Act** compliance.

**Dual-published**: also bundled inside `ra-qm-skills` (`../skills/eu-ai-act-specialist/`). Manually mirrored to `ra-qm-team/skills/eu-ai-act-specialist/`.

See `./skills/eu-ai-act-specialist/SKILL.md` for the full skill documentation.

## What this is

The EU AI Act is the world's first comprehensive horizontal regulation of AI systems. Adopted in 2024 (Regulation (EU) 2024/1689; OJEU L of 12 July 2024), it entered into force on 1 August 2024 and applies in phases:

| Date | Obligation |
|---|---|
| **2 Feb 2025** | Article 5 (prohibited AI practices) + Article 4 (AI literacy) in force |
| **2 Aug 2025** | GPAI obligations (Articles 51–55) + governance + penalties in force |
| **2 Aug 2026** | High-risk AI obligations (Title III) in force (general) |
| **2 Aug 2027** | High-risk obligations for products already covered by sectoral law (Annex I) |

The Act is binding and directly applicable across all 27 EU Member States. Penalties reach EUR 35M or 7% of worldwide annual turnover (whichever is higher) for Article 5 violations.

## What this plugin provides

Three deterministic stdlib tools that operate at the Article level:

1. **`ai_system_risk_classifier.py`** — input: AI system characteristics → output: tier (prohibited / high-risk / limited-risk / minimal-risk) with citing Article and Annex
2. **`conformity_assessment_planner.py`** — input: high-risk AI system + classification → output: Module A (internal control) vs Module H (full QMS) routing per Article 43 + Annex IV technical documentation checklist
3. **`ai_act_obligation_tracker.py`** — input: organization role per Article 25 (provider / deployer / importer / distributor / authorized representative) → output: obligation matrix with deadlines

Four references each citing 5+ authoritative sources (the Regulation itself + EDPB + European Commission guidelines + ENISA + IAPP tracker + national supervisory authority guidance).

## What this is NOT

- **NOT executive AI strategy.** For board-level AI decisions (build-vs-buy, model selection, US/EU strategy), see `c-level-advisor/chief-ai-officer-advisor/`.
- **NOT ISO 42001 compliance.** That's a voluntary management-system standard; this is a binding regulation. They complement each other. See `compliance-team-iso42001`.
- **NOT GDPR compliance.** For personal-data processing (which AI systems frequently trigger), see `ra-qm-team/skills/gdpr-dsgvo-expert/`. The two regulations interact (Recital 10, Article 10).
- **NOT a legal substitute.** This skill produces Article-cited compliance artifacts. For binding legal advice, especially on novel cases (e.g., is a chatbot a "general-purpose AI model"?), engage outside counsel.

## Critical scope reminders

- **Extraterritorial reach** (Article 2): The Act applies to providers placing AI systems on the EU market regardless of where they are established. US/UK/Asian companies serving EU users are in scope.
- **Definition of "AI system"** (Article 3(1) + Commission Guidelines Feb 2025): broader than ML; includes rule-based systems if they exhibit "varying levels of autonomy" and "adaptiveness." Most modern enterprise software does NOT qualify; foundation models, predictive models, and decision-support systems frequently do.
- **GPAI separate track** (Articles 51–55): General-purpose AI models (e.g., large foundation models) have a parallel regime with stricter rules for "systemic risk" GPAI (10²⁵ FLOPs training threshold). Article 55 obligations include systemic-risk evaluations, adversarial testing, and incident reporting.

## Quick start

```bash
# Classify an AI system per the Act
python skills/eu-ai-act-specialist/scripts/ai_system_risk_classifier.py

# Plan conformity assessment for a high-risk system
python skills/eu-ai-act-specialist/scripts/conformity_assessment_planner.py

# Track obligations per organizational role
python skills/eu-ai-act-specialist/scripts/ai_act_obligation_tracker.py
```

All three tools run with embedded samples if no JSON path is provided.

## License

MIT.
