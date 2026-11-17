---
name: nis2-readiness
description: Use when a cyberattack, ransomware or outage hits a hospital, utility, transport, digital-infrastructure or other EU company and it must report under NIS2 (Directive 2022/2555) or the German NIS2UmsuCG/BSIG - 24h early warning, 72h notification, one-month final report. Also for whether a company is an essential or important entity, BSI registration, management-board liability and training (Article 20), an Article 21 gap analysis, or one incident that also triggers DORA, CRA or GDPR reports. Four deterministic scripts with cited articles.
argument-hint: "[entities CSV | incident log CSV | Article 21 assessment CSV | profile JSON]"
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "Four deterministic stdlib scripts with blocking exit codes (Art 2/3 scope classifier, Art 23 incident clock, Art 21 + Implementing Regulation 2024/2690 gap check, cross-regime router for NIS2/DORA/CRA/GDPR); rules from Directive (EU) 2022/2555, Implementing Regulation (EU) 2024/2690 and the German NIS2UmsuCG (BSIG 2025)"
  distinct_from: "dora-readiness (financial entities, lex specialis); cra-readiness (product law, not entity law); information-security-manager-iso27001 (management system, not the legal duty); gdpr-dsgvo-expert (personal-data breaches)"
---

# NIS2 Readiness

> **Portability:** 4 stdlib scripts, no network, nothing submitted anywhere. Fill CSVs, run, keep the output as evidence.
> **Not legal advice.** Member State transpositions differ; the national authority decides on designation and significance.

NIS2 is an entity duty, not a product duty. It catches medium and large
companies in the 18 Annex I/II sectors, plus some of any size (DNS, TLD, trust
services, public e-comms, sole providers). Management bodies approve and
oversee the measures and can be held liable (Art 20). Germany's NIS2UmsuCG has
applied since 6 December 2025: register with the BSI within three months
(BSIG §33). Teams fail the same ways: they size the group instead of the
entity, nobody records when they became aware, the 72-hour notification is
mistaken for the last report, and DORA entities report twice.

## Workflow

```bash
# 0 - One event, several laws: which clocks run and who gets what?
python scripts/eu_cyber_regime_router.py --profile assets/profile.example.json
# 1 - Scope: essential, important, or out? Which authority, which register?
python scripts/nis2_scope_classifier.py --entities assets/entities.example.csv
# 2 - Report: is an early warning, notification or final report due now?
python scripts/nis2_incident_clock.py --incidents assets/incidents.example.csv
# 3 - Measures: what blocks the Article 21 baseline?
python scripts/art21_gap_check.py --assessment assets/assessment.example.csv [--digital-provider]
```

Run step 2 first whenever an incident is live: it is the only step with a
24-hour deadline. `--list-sectors`, `--list-special`, `--list` and `--template`
print the Annex I/II sectors, size-independent flags and the 30 assessment ids.

## The gates block on (exit 4)

1. An entity with no size data: size decides essential vs important vs out (Art 2(1), Art 3; Rec 2003/361).
2. A report past its deadline, or significance still unassessed 24 h after awareness (Art 23(3)-(4)).
3. An Article 21 measure NOT MET, or an id left unassessed (Art 21(2)(a)-(j)).

## Hard rules

- **Size the entity, not the group,** but count partner and linked enterprises as Rec 2003/361 does; say which figures you used.
- **Awareness is evidence.** No logged awareness time means the clock runs from detection.
- **72 hours is not the end.** A final report is due one month after the notification; a progress report if handling is still open.
- **DORA wins for financial entities** (Art 4 lex specialis): route them to `dora-readiness`, and check whether the Member State wants a copy to the CSIRT (DORA Art 19(1)).
- **Digital providers use 2024/2690.** DNS, TLD, cloud, data centres, CDNs, MSPs, MSSPs, marketplaces, search, social networks and trust services: pass `--digital-provider` for the Annex section behind each measure and the Art 3 significance thresholds.
- **Never submit for the user.** The scripts prepare; a named person reports to the CSIRT or authority (in Germany, the BSI portal).

## Scripts

| Script | Role | Exit codes |
|---|---|---|
| `scripts/nis2_scope_classifier.py` | Sector (Annex I/II), size (Rec 2003/361), essential/important (Art 3), size-independent cases (Art 2(2)), DORA overlap, jurisdiction (Art 26), registration (Art 27; BSIG §33) | 0 · 2 findings · 3 bad input · 4 blocked |
| `scripts/nis2_incident_clock.py` | Significance (Art 23(3); 2024/2690 Arts 3-14), 24h / 72h / one-month deadlines, report content, recipients informed (Art 23(1)) | 0 on time · 2 open · 3 · 4 overdue |
| `scripts/art21_gap_check.py` | 30 ids: governance (Art 20), Art 21(2)(a)-(j), reporting, registration; 2024/2690 Annex mapping | 0 ready · 2 gaps · 3 · 4 blocked |
| `scripts/eu_cyber_regime_router.py` | NIS2 / DORA / CRA / GDPR for one entity and event, parallel clocks, open questions | 0 · 2 open questions · 3 |

All support `--help`, `--sample` and `--output json`.

## References and assets

- [`references/scope_and_registration.md`](references/scope_and_registration.md) — sectors, size rules, essential vs important, jurisdiction, German BSIG thresholds and §33 registration, fines (7 sources)
- [`references/incident_reporting_article23.md`](references/incident_reporting_article23.md) — significance, the three reports, 2024/2690 thresholds, overlap with DORA, CRA and GDPR (7 sources)
- [`references/article21_measures.md`](references/article21_measures.md) — each measure with typical evidence and the 2024/2690 Annex section (6 sources)
- [`assets/incident_runbook.md`](assets/incident_runbook.md) — standing set-up and per-incident record
- [`assets/entities.example.csv`](assets/entities.example.csv), [`assets/incidents.example.csv`](assets/incidents.example.csv), [`assets/assessment.example.csv`](assets/assessment.example.csv), [`assets/profile.example.json`](assets/profile.example.json) — input formats
