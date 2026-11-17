# NIS2 Article 21 measures and evidence

The ten measures every essential and important entity must take, with what an
auditor usually asks to see, and the Annex section of Implementing Regulation
2024/2690 that makes each concrete for digital providers.

Confidence: 🟢 legal text · 🟡 authority guidance · 🔴 our reading, typical evidence only

## Governance (Art 20)

| id | Requirement | Typical evidence | Source |
|---|---|---|---|
| GOV-1 | Management body approves the measures | board resolution with date | 🟢 Art 20(1) |
| GOV-2 | Management body oversees implementation | recurring board agenda item, CISO reports | 🟢 Art 20(1) |
| GOV-3 | Management body members trained | training records per member | 🟢 Art 20(2) |
| GOV-4 | Staff offered similar training regularly | training plan and attendance | 🟢 Art 20(2) |

## Article 21(2)

| Letter | Measure | Typical evidence | 2024/2690 Annex |
|---|---|---|---|
| (a) | Policies on risk analysis and information system security | approved policy set, risk register | 1, 2 |
| (b) | Incident handling | incident procedure, logs, post-incident reviews | 3 |
| (c) | Business continuity, backup management, disaster recovery, crisis management | BCP, restore tests, crisis exercise reports | 4 |
| (d) | Supply chain security, incl. supplier relationships | supplier inventory, security clauses, supplier assessments | 5 |
| (e) | Security in acquisition, development and maintenance, incl. vulnerability handling and disclosure | SDLC policy, patch SLAs, disclosure policy | 6 |
| (f) | Policies to assess effectiveness of the measures | internal audit plan, metrics, test results | 7 |
| (g) | Basic cyber hygiene and training | awareness programme, hygiene baseline | 8 |
| (h) | Cryptography and, where appropriate, encryption | crypto policy, key management | 9 |
| (i) | HR security, access control policies, asset management | joiner/mover/leaver process, access reviews, asset inventory | 10, 11, 12 |
| (j) | MFA or continuous authentication, secured voice/video/text, secured emergency communications | MFA coverage report, secure channels | 11 |

Annex 13 (environmental and physical security) is required by Art 21(1)'s
all-hazards approach and checked as `P-1`. 🟢 Art 21(1); 2024/2690 Annex 13

Measures must be proportionate to exposure, size, likelihood and severity, and
take account of the state of the art and relevant European and international
standards. 🟢 Art 21(1)

## Where the gate is strict

- Only GOV-4 and the (j) items accept `NA`: everything else applies to every entity. 🔴 our reading of Art 21(2) ("at least")
- `PARTIAL` is a HIGH finding, `NOT_MET` a BLOCKER, `MET` without evidence or owner a MEDIUM.
- Supply chain (d) means *your* suppliers' security, including the ENISA coordinated risk assessments of critical supply chains. 🟢 Art 21(3), Art 22

## Mapping to ISO/IEC 27001:2022

Most measures map to Annex A controls, but certification alone does not prove
NIS2 compliance: management approval and liability (Art 20) and reporting
(Art 23) sit outside 27001. 🟡 ENISA mapping tables · 🔴

## Sources

1. Directive (EU) 2022/2555, Arts 20-22 — https://eur-lex.europa.eu/eli/dir/2022/2555/oj
2. Implementing Regulation (EU) 2024/2690, Annex — https://eur-lex.europa.eu/eli/reg_impl/2024/2690/oj
3. ENISA, Technical implementation guidance (June 2025) 🟡 — https://www.enisa.europa.eu/
4. ISO/IEC 27001:2022, Annex A
5. NIS2UmsuCG, BGBl. 2025 I Nr. 301 (BSIG §§30, 38)
6. BSI IT-Grundschutz-Kompendium (mapping aid) 🟡 — https://www.bsi.bund.de/
