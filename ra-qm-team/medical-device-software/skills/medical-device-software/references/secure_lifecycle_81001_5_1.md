# IEC 81001-5-1: the security lifecycle on top of IEC 62304

IEC 81001-5-1:2021 (Edition 1.0, 2021-12) adds security activities to the
health software lifecycle. Its process requirements are derived from
IEC 62443-4-1 and its structure follows IEC 62304, so a 62304 QMS extends rather
than duplicates. Unlike 62304 it has **no safety classes**: every activity
applies to all health software, scoped by the manufacturer under 4.1.3
(identification of applicability).

Confidence legend as in `classification_and_documentation_levels.md`.
🟡 Clause headings below are from the public IEC **FDIS** sample; the published
2021 text may word a heading differently. Requirement content is summarised,
not quoted.

## Clause map

| Clause | Activities (ids used by `lifecycle_gap_check.py --security`) |
|---|---|
| 4.1 Quality management | S4.1.1 QMS · S4.1.2 responsibilities · S4.1.3 applicability · S4.1.4 security expertise · S4.1.5 third-party software items · S4.1.6 continuous improvement · S4.1.7 disclosing security-related issues · S4.1.8 periodic review of security defect management · S4.1.9 accompanying documentation review |
| 4.2 / 4.3 | S4.2 security risk management · S4.3 software item classification relating to risk transfer |
| 5 Development | S5.1.1-S5.1.3 lifecycle activities, development environment security, secure coding standards · S5.2.1-S5.2.3 security requirements, their review, risks of required software · S5.3.1-S5.3.3 defence-in-depth architecture, secure design practices, architecture review · S5.4.1-S5.4.4 secure design and interfaces, design verification · S5.5.1-S5.5.2 secure coding, implementation review · S5.6 integration testing · S5.7.1-S5.7.5 security requirements testing, threat mitigation testing, vulnerability testing, penetration testing, tester/developer conflicts of interest · S5.8.1-S5.8.7 resolve findings before release, release documentation, file integrity, private-key controls, security issues, activity completion, secure decommissioning guidelines |
| 6 Maintenance | S6.1.1 timely delivery of security updates · S6.2.1 monitoring public incident reports · S6.2.2 security update verification · S6.3.1-S6.3.3 update documentation, delivery and integrity |
| 7 Security risk management | S7.1.2 product security context · S7.2 vulnerabilities, threats, adverse impacts · S7.3 estimate and evaluate · S7.4 control · S7.5 monitor effectiveness of controls |
| 8 Configuration management | S8 |
| 9 Problem resolution | S9.2 receiving vulnerability notifications · S9.3 reviewing · S9.4 analysing · S9.5 addressing security-related issues |

Informative annexes: A (rationale, relationship to IEC 62443 and IEC 62304, risk
transfer), B (implementation guidance), C (threat modelling: attack-defence
trees, CAPEC/OWASP/SANS, CWSS, DREAD, OCTAVE, STRIDE, Trike, VAST), D (mapping to
IEC 62443-4-1:2018 practices), E (documents specified in 62443-4-1). Normative:
**F (transitional health software)**, G (object identifiers).

## Risk transfer: maintained, supported, required software (4.3, ISH1:2025)

🟢 Interpretation Sheet 1 (IEC 81001-5-1:2021/ISH1:2025, published
3 December 2025) clarifies 4.3. The three categories are **nested, not
exclusive**: SUPPORTED includes MAINTAINED, and REQUIRED includes SUPPORTED, so a
clause that names a category also covers the ones inside it.

| Category | What it means | Clauses ISH1 maps to it |
|---|---|---|
| **Maintained** | the manufacturer provides the security updates | 5.2.3, 6.3.1 (notify users), **6.3.2 delivery and 6.3.3 integrity of updates** |
| **Supported** | the operator controls selection and timing of updates (e.g. a database shared by several devices); the manufacturer still notifies | 5.2.3, 6.3.1 |
| **Required** | the manufacturer cannot obtain notifications or updates (e.g. end-of-support items) and must keep the product secure by other means | 5.2.3 |

Categories move over the life cycle, usually downwards (maintained to supported
or required, supported to required); each move triggers a re-evaluation of the
associated clauses. An organisation may use its own terms if its procedure maps
them to these. **Transitional** (Annex F) is an attribute of the whole product
developed before the standard existed, not a fourth item category.

`soup_register_check.py` asks for the category on every SOUP row because it
decides who ships the patch when 524B(b)(2) or a customer asks, and an item past
end of support has effectively become "required" whether or not the register
says so.

🟢 A revision of IEC 81001-5-1:2021 was approved as a new IEC project on
22 September 2025 (stage "new project approved"). Plan on Edition 1.0 + ISH1.

## How the pieces map

| Need | IEC 81001-5-1 | FD&C Act 524B | EU |
|---|---|---|---|
| Postmarket vulnerability monitoring and coordinated disclosure | S4.1.7, S6.2.1, S9.2-S9.5 | (b)(1) plan in the submission | MDR Annex I 17.2 state of the art; MDCG 2019-16 |
| Secure-by-design processes, patch cadence | S5.x, S6.1.1, S6.3.x | (b)(2) | MDR Annex I 17.2, 17.4, 18.8 |
| Component inventory | S4.1.5, S8 | (b)(3) SBOM incl. commercial, open-source, OTS | MDCG 2019-16 |
| Security testing | S5.7.1-S5.7.5 | FDA guidance section on testing (2025) | notified bodies ask for fuzz and penetration testing (BSI 2025) |

🟢 FDA recognises IEC 81001-5-1 Ed. 1.0 2021-12 as consensus standard **13-122**
(entered 19 December 2022) and ANSI/ISA 62443-4-1-2018 as 13-119.

🟢 MDCG 2019-16 rev. 1 (December 2019, revised July 2020) predates the standard.
Its Annex III lists the work under its **draft** designation, "ISO/IEC 80001-5-1
... Part 5-1: Activities in the product life-cycle", alongside EN 62304,
IEC 62443-4-1/-4-2 and IEC TR 60601-4-5, and notes that standards give a
presumption of conformity only once harmonised and cited in the OJ. Guides that
say MDCG 2019-16 "explicitly references EN IEC 81001-5-1" are paraphrasing.

## What the gap check enforces, and why

`lifecycle_gap_check.py --security` lets a manufacturer mark most S-activities
NA with a written justification (4.1.3 is the standard's own scoping clause).
It never accepts NA on security risk management (S4.2, S7.x), vulnerability
intake and handling (S9.2-S9.5), disclosure (S4.1.7), monitoring public
incident reports (S6.2.1), timely security updates (S6.1.1) or resolving
findings before release (S5.8.1). That is this skill's policy, not a clause:
524B(b)(1) requires the postmarket plan for any cyber device, and a connected
device without these activities has no answer to a notified body.

## Sources

1. IEC FDIS 81001-5-1 public sample (TOC, scope, relationship to 62304 and 62443-4-1) — https://cdn.standards.iteh.ai/samples/76097/404d057953ef4f20867c4dbbac1848f7/IEC-FDIS-81001-5-1.pdf
2. IEC 81001-5-1:2021 + ISH1:2025 preview (interpretation sheet on 4.3) — https://www.en-standard.eu/publicdoc/iec_previews/1151833.pdf; ISH1 catalogue entry — https://standards.iteh.ai/catalog/standards/iec/29a26217-1c68-4c2a-bc8a-7c2e0bae69f8/iec-81001-5-1-2021-ish1-2025; revision project — https://standards.iteh.ai/catalog/standards/iso/20a7a3c0-589b-41ff-bc3a-f7892fc35973/iec-awi-81001-5-1
3. FDA Recognized Consensus Standards (13-122 IEC 81001-5-1; 13-119 ANSI/ISA 62443-4-1) — https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/results.cfm?title=524B
4. 21 U.S.C. 360n-2 (FD&C Act 524B) — https://www.law.cornell.edu/uscode/text/21/360n-2
5. MDCG 2019-16 rev. 1, Guidance on Cybersecurity for medical devices (Annex III) — https://health.ec.europa.eu/document/download/b23b362f-8a56-434c-922a-5b3ca4d0a7a1_en
6. FDA, Cybersecurity in Medical Devices (issued 27 June 2025) — https://www.hhs.gov/guidance/sites/default/files/hhs-guidance-documents/FDA/GUI00001825-final-PremarketCybersecurity-2025.pdf
7. BSI notified-body webinar, 27 March 2025 — https://bsigroup.com/siteassets/pdf/en/insights-and-media/media/webinars/bsi-md-software-under-mdr-perspectives-notified-body-270325-en-gb.pdf
