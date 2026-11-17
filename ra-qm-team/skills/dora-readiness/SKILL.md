---
name: dora-readiness
description: Use when a bank, payment or e-money institution, investment firm, insurer, crypto-asset service provider or fund manager in the EU faces DORA (Regulation 2022/2554, Digital Operational Resilience Act) - is an ICT outage or cyber incident major, when the initial (4h/24h), intermediate (72h) and final reports are due, weekends included; the register of information; ICT or cloud contracts missing audit rights, exit plans or other Article 30 terms; scope and the simplified framework for small firms. Not for DORA DevOps metrics. Three deterministic scripts with cited articles.
argument-hint: "[entities CSV | ICT incident log CSV | register of information CSV]"
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "Three deterministic stdlib scripts with blocking exit codes (Art 2 scope + simplified framework + CTPP check, major-incident classifier with the RTS 2025/301 clock, register of information and Art 30 contract check); rules from Regulation (EU) 2022/2554, Delegated Regulations (EU) 2024/1772 and 2025/301, Implementing Regulation (EU) 2024/2956"
  distinct_from: "nis2-readiness (non-financial entities; DORA is lex specialis); vpe-advisor (DORA DevOps delivery metrics, a different DORA); information-security-manager-iso27001 (management system); cra-readiness (products)"
---

# DORA Readiness

> **Portability:** 3 stdlib scripts, no network, nothing submitted anywhere. Fill CSVs, run, keep the output as evidence.
> **Not legal advice.** Your competent authority supervises; national transposition choices (e.g. CSIRT copies) vary.

DORA has applied since 17 January 2025 to 20 types of financial entity and to
the ICT providers that serve them. Supervisors first asked for two things: the
register of information and major-incident reports. Teams fail in predictable
ways: they classify on gut feeling instead of the RTS thresholds, start the
4-hour clock at awareness instead of at classification, miss recurring incidents
that are major together, and sign cloud contracts for critical functions with no
audit right or exit plan.

## Workflow

```bash
# 1 - Scope: full regime, simplified (Art 16), excluded, or ICT provider?
python scripts/dora_scope_check.py --entities assets/entities.example.csv
# 2 - Incidents: which are major, which report is due, is any overdue?
python scripts/dora_incident_classifier.py --incidents assets/incidents.example.csv --entity credit-institution
# 3 - Third parties: does the register and every contract hold up?
python scripts/register_of_information_check.py --register assets/register.example.csv
```

Run step 2 first whenever an ICT incident is live. `--list-types`,
`--list-exemptions`, `--list-simplified` and `--list-terms` print the Art 2
entity types, exclusions, Art 16 cases and the Art 30 contract terms.

## How an incident becomes major (RTS 2024/1772 Art 8)

It affects **critical services** (Art 6) **and** either a successful malicious
unauthorised access that may cause data loss, **or** two of: clients (>10%,
>100 000, >30% counterparts, >10% transactions, or relevant clients),
reputation, duration (>24 h, or >2 h down on a critical function), two Member
States, data impact, economic loss >EUR 100 000. Incidents with the same root
cause, at least twice in six months, that meet this together are one major
incident (Art 8(2)).

## The gates block on (exit 4)

1. An entity type DORA does not list, or no type at all (Art 2(1)).
2. A report past its deadline: initial 4 h after classification and no later than 24 h after awareness; intermediate 72 h after the initial; final one month after the last intermediate (RTS 2025/301 Art 5).
3. A contract for a critical or important function missing an Art 30(3) term or an exit plan (Art 28(8)), or a contract never assessed for criticality.

## Hard rules

- **Classify against the thresholds, write the classification time down.** It starts the 4-hour clock.
- **Weekend relief is narrow.** Noon of the next working day applies, but not to initial and intermediate reports of credit institutions, CCPs, trading venues or NIS2-identified entities (Art 5(5)): pass `--entity`.
- **Late still owes the report, and the warning.** Tell the authority before a deadline passes (Art 5(3)).
- **Clients hear from you.** If their financial interests are hit, inform them without undue delay (DORA Art 19(3)).
- **Microenterprises and Art 16 entities** skip the recurring check, not the reporting.
- **Never submit for the user.** The scripts prepare; a named person files with the competent authority.

## Scripts

| Script | Role | Exit codes |
|---|---|---|
| `scripts/dora_scope_check.py` | Entity type (Art 2(1)(a)-(u)), exclusions (Art 2(3)), simplified framework (Art 16), microenterprise, NIS2 overlap, CTPP (Arts 31-35) | 0 · 2 findings · 3 bad input · 4 unplaced |
| `scripts/dora_incident_classifier.py` | Art 6/8/9 classification, recurring incidents, initial / intermediate / final deadlines, weekend rule, client notice | 0 on time · 2 open · 3 · 4 overdue |
| `scripts/register_of_information_check.py` | LEI, criticality, Art 30(2) and 30(3) terms, exit plan (Art 28(8)), risk assessment (Art 28(4)), concentration and third country (Art 29) | 0 clean · 2 gaps · 3 · 4 blocked |

All support `--help`, `--sample` and `--output json`.

## References and assets

- [`references/scope_and_proportionality.md`](references/scope_and_proportionality.md) — entity types, exclusions, simplified framework, CTPP oversight, NIS2 overlap (6 sources)
- [`references/major_incident_reporting.md`](references/major_incident_reporting.md) — classification criteria, thresholds, deadlines, report content, client notice (6 sources)
- [`references/third_party_register_and_contracts.md`](references/third_party_register_and_contracts.md) — register of information, Art 30 terms, exit plans, concentration risk (6 sources)
- [`assets/major_incident_runbook.md`](assets/major_incident_runbook.md) — classification record and reporting timeline
- [`assets/entities.example.csv`](assets/entities.example.csv), [`assets/incidents.example.csv`](assets/incidents.example.csv), [`assets/register.example.csv`](assets/register.example.csv) — input formats
