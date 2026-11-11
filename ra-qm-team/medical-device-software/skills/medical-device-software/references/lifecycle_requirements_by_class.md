# IEC 62304 lifecycle requirements by software safety class

IEC 62304:2006+A1:2015 (Edition 1.1) marks each requirement with the classes it
applies to, in the normative text after the requirement (clause 1.4) and in the
summary Table A.1. The standard is paywalled, so this table is reproduced from
two independent secondary sources that agree on every clause 5 marker (Al
Cohen, "IEC 62304 Items by Class"; SimQ class summary) and from the Johner
Institute's class table. 🟡 **Your licensed copy prevails.**
`lifecycle_gap_check.py --list --class X` prints the same table as ids.

Short titles below are this skill's labels, not quotations.

## Differs by class

| Subclause | Requirement | A | B | C |
|---|---|:-:|:-:|:-:|
| 5.1.4 | Development standards, methods and tools planning | | | ✓ |
| 5.1.5 | Integration and integration test planning | | ✓ | ✓ |
| 5.1.10-5.1.12 | Supporting items controlled; configuration item control before verification; identification and avoidance of common software defects | | ✓ | ✓ |
| 5.2.3 | Risk control measures in the software requirements | | ✓ | ✓ |
| 5.3.1-5.3.4, 5.3.6 | Architecture, interfaces, SOUP functional/performance and HW/SW requirements, architecture verification | | ✓ | ✓ |
| 5.3.5 | Segregation necessary for risk control | | | ✓ |
| 5.4.1 | Subdivide software into units | | ✓ | ✓ |
| 5.4.2-5.4.4 | Detailed design of units and interfaces; verify detailed design | | | ✓ |
| 5.5.2, 5.5.3, 5.5.5 | Unit verification process, acceptance criteria, unit verification | | ✓ | ✓ |
| 5.5.4 | Additional unit acceptance criteria | | | ✓ |
| 5.6.1-5.6.8 | Integration and integration testing | | ✓ | ✓ |
| 5.8.3, 5.8.5, 5.8.6 | Evaluate residual anomalies; document how the release was built; activities complete | | ✓ | ✓ |
| 7.1.1-7.1.4 | Software contributing to hazardous situations, causes, **SOUP anomaly lists** | | ✓ | ✓ |
| 7.2.1-7.2.2, 7.3.1, 7.3.3 | Risk control measures, their verification, traceability | | ✓ | ✓ |
| 7.4.2-7.4.3 | Impact of changes on existing risk controls | | ✓ | ✓ |

## Every class

4.1-4.4 (QMS, ISO 14971 risk management, classification, legacy software);
5.1.1-5.1.3, 5.1.6-5.1.9 (plan, kept current, verification, risk management,
documentation and configuration management planning); 5.2.1, 5.2.2, 5.2.4-5.2.6
(requirements); 5.5.1 (implement units); **5.7.1-5.7.5 (software system testing:
required for class A since A1)**; 5.8.1, 5.8.2, 5.8.4, 5.8.7, 5.8.8 (release);
all of clause 6 (maintenance); 7.4.1 (safety analysis of changes); all of clause
8 (configuration management, including **8.1.2 identify SOUP**); all of clause 9
(problem resolution, 9.1-9.8).

Clause 7.1.5 and 7.3.2 are not used in Edition 1.1.

## Readings that cost teams a finding

- **Class A still means a plan, requirements, system tests, release records,
  maintenance, configuration management and problem resolution.** What it drops
  is architecture, detailed design, unit verification and integration testing.
- **SOUP rigour is class-driven.** Identification (8.1.2) applies to every class;
  stated requirements (5.3.3, 5.3.4) and evaluation of the published anomaly
  list (7.1.3) apply from class B. See `soup_and_traceability.md`.
- **The plan can be agile.** 62304 prescribes activities and outputs, not a
  waterfall. FDA recognises AAMI TIR45:2023 (agile practices) as 13-143.
- **NA is not a status the class table allows.** Inside a class, a required
  activity is done or it is a gap; the gap check blocks NA except where the
  requirement is conditional (no legacy software, no SOUP, no segregation claim).

## Legacy software (clause 4.4, added by A1)

🟡 For software placed on the market before it was developed under 62304 and
still in use: 4.4.1 general, 4.4.2 risk management activities (feedback,
hazardous situations), 4.4.3 gap analysis against the clauses for its class,
4.4.4 gap closure activities (prioritised by risk), 4.4.5 rationale for
continued use. A legacy rationale is not a substitute for 62304 on new
features: changes to legacy software go through clauses 6-9.

IEC 81001-5-1 has the parallel concept for security, **transitional health
software** (normative Annex F): development assessment and gap closure,
rationale for use, post-release activities.

## Regulatory standing

- 🟢 FDA: recognised consensus standard 13-79 (IEC 62304 Ed. 1.1 2015-06), complete
  recognition. Basic documentation can rest on a 62304 declaration of conformity.
- 🟡 EU: notified bodies audit against EN 62304:2006+A1:2015 as state of the art
  under MDR Annex I 17.2. 🔴 OJ citation under the MDR not confirmed; see
  `classification_and_documentation_levels.md` §4.

## Sources

1. IEC 62304 Ed. 1.1 preview (TOC, clause 1.4, Table A.1 title) — https://webstore.ansi.org/preview-pages/IEC/preview_iec62304%7Bed1.1%7Den.pdf
2. Al Cohen, "IEC 62304 Items by Class" — https://alcohen.com/iec-62304-checklist/
3. SimQ, "IEC 62304 Software Safety Classes A, B and C: Requirements per Class" — https://simq.de/en/iec-62304-software-safety-classes/
4. Johner Institute, "IEC 62304 software safety classes" (Table 2) — https://blog.johner-institute.com/iec-62304-medical-software/safety-class-iec-62304/
5. FDA Recognized Consensus Standards: 13-79 (IEC 62304), 13-143 (AAMI TIR45:2023) — https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/results.cfm?title=62304
6. IEC FDIS 81001-5-1 public sample (Annex F heading) — https://cdn.standards.iteh.ai/samples/76097/404d057953ef4f20867c4dbbac1848f7/IEC-FDIS-81001-5-1.pdf
7. BSI notified-body webinar, 27 March 2025 — https://bsigroup.com/siteassets/pdf/en/insights-and-media/media/webinars/bsi-md-software-under-mdr-perspectives-notified-body-270325-en-gb.pdf
