---
name: cra-readiness
description: Use when a company that sells software, connected devices or firmware in the EU asks whether the Cyber Resilience Act (CRA, Regulation 2024/2847) applies, has to report an actively exploited vulnerability or security incident under Article 14 (24h/72h deadlines, ENISA Single Reporting Platform), must classify products as important or critical, pick a conformity route or support period, check an SBOM, or get to CE marking by December 2027. Four deterministic scripts with cited articles.
argument-hint: "[product inventory CSV | event log CSV | Annex I assessment CSV | SBOM JSON]"
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "Four deterministic stdlib scripts with blocking exit codes (scope + class + route classifier, Article 14 reporting clock, Annex I/II/VII completeness gate, SBOM floor check); every rule cites Regulation (EU) 2024/2847, checked against the Official Journal text, Implementing Regulation (EU) 2025/2392 and Commission guidance C(2026) 5252"
  distinct_from: "eu-ai-act-specialist (AI Act); information-security-manager-iso27001 and isms-audit-expert (management systems, not product law); mdr-745-specialist (medical devices, which the CRA excludes); cmmc-readiness (US defence); compliance-os (multi-framework orchestration without CRA)"
---

# CRA Readiness

> **Portability:** 4 stdlib scripts, no network, nothing submitted anywhere. Fill CSVs, run, keep the output with the technical documentation.
> **Not legal advice and not a conformity assessment.** The manufacturer signs the declaration; on routes B+C and H a notified body decides.

The CRA has two clocks. **Article 14 reporting has applied since 11 September
2026** to every in-scope product on the EU market, including ones shipped years
ago. **Everything else applies from 11 December 2027** (Art 71(2)). Teams fail in
predictable ways: nobody can say when they became "aware", class I products are
planned on self-assessment while no harmonised standard is cited, a five-year
support period is set for a router people keep for eight, and the SBOM lists
packages but not what the product depends on.

## Workflow

```bash
# 1 - Scope: which products, which class, which route, which CSIRT?
python scripts/cra_scope_classifier.py --inventory assets/inventory.example.csv
# 2 - Report: is any Article 14 report due or overdue right now?
python scripts/art14_report_clock.py --events assets/events.example.csv
# 3 - Conformity: can we sign the EU declaration of conformity?
python scripts/annex_i_gap_check.py --assessment assets/assessment.example.csv
python scripts/sbom_check.py --sbom assets/sbom.example.cdx.json
```

Run step 2 first whenever a vulnerability or incident is live: it is the only
step with a 24-hour deadline. `--list-categories`, `--list` and `--template`
print the Annex III/IV categories and the 39 assessment ids.

## The gates block on (exit 4)

1. A conformity route the class does not allow (class I on module A without full harmonised standards; class II or critical on A) — Art 32.
2. A support period under five years when the product is used for five or more — Art 13(8).
3. No Member State to route Article 14 reports to — Art 14(7).
4. An Article 14 report past its deadline, or an event with no recorded awareness time — Art 14(2), 14(4).
5. An Annex I requirement NOT MET, or NA on one that applies to every product (all of Part II) — Annex I.
6. An SBOM that is not CycloneDX/SPDX JSON, names no product, or has no top-level dependencies — Annex I Part II(1).

## Hard rules

- **Unassessed is not MET.** The gap check refuses a file that skips any of the 39 ids.
- **The clock runs from awareness, and you prove awareness.** No timestamp means the clock runs from detection.
- **Legacy is not exempt from reporting.** Products placed before 11 Dec 2027 owe Article 14 even unmodified, and after their support period ends (Art 69(3); Commission guidance).
- **Late is still owed.** Micro and small enterprises escape fines for a missed 24-hour early warning (Art 64(10)(a)), not the report.
- **Cite the article.** Every class, route and deadline call names its paragraph; borderline categories go to the notified body or authority, with Implementing Regulation (EU) 2025/2392 open.
- **Never submit for the user.** The scripts prepare; a named person submits on the SRP and signs the declaration.

## Scripts

| Script | Role | Exit codes |
|---|---|---|
| `scripts/cra_scope_classifier.py` | Scope (Art 2), role (Arts 19-22, 24), class (Art 7-8, Annex III/IV), routes (Art 32), legacy (Art 69), support period (Art 13(8)), reporting CSIRT (Art 14(7)) | 0 clear · 2 findings · 3 bad input · 4 blocked |
| `scripts/art14_report_clock.py` | 24h / 72h / 14-day / one-month deadlines, content per report, user notice | 0 on time · 2 open · 3 · 4 overdue |
| `scripts/annex_i_gap_check.py` | 39 ids across Annex I Parts I-II, Annex VII, Annex II; NA rules; evidence | 0 ready · 2 gaps · 3 · 4 blocked |
| `scripts/sbom_check.py` | CycloneDX/SPDX JSON, primary component, top-level dependencies, versions, purl/CPE coverage | 0 pass · 2 · 3 · 4 fail |

All support `--help`, `--sample` and `--output json`.

## References and assets

- [`references/reporting_article14.md`](references/reporting_article14.md) — dates, triggers, the three clocks, CSIRT routing, legacy products, penalties (7 sources)
- [`references/scope_classes_and_routes.md`](references/scope_classes_and_routes.md) — scope and exclusions, roles, Annex III/IV, Art 32 routes, support period (6 sources)
- [`references/essential_requirements_and_evidence.md`](references/essential_requirements_and_evidence.md) — every Annex I/II/VII item with typical evidence, retention periods, standards status (8 sources)
- [`assets/article14_runbook.md`](assets/article14_runbook.md) — standing set-up and per-event record for the SRP
- [`assets/inventory.example.csv`](assets/inventory.example.csv), [`assets/events.example.csv`](assets/events.example.csv), [`assets/assessment.example.csv`](assets/assessment.example.csv), [`assets/sbom.example.cdx.json`](assets/sbom.example.cdx.json) — input formats
