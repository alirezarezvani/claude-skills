# Control crosswalk

How each finding code maps to controls, and where the mapping is a judgment call.
`control_evidence_mapper.py` uses exactly this table.

Confidence key: 🟢 read in the primary source · 🟡 secondary source, or title only · 🔴 our mapping judgment.

## Finding → controls

| Finding | ISO 27001:2022 | SOC 2 | NIST 800-53 r5 | PCI DSS 4.0.1 | Other |
|---|---|---|---|---|---|
| LEAVER_ENABLED, LEAVER_USED_AFTER_EXIT | A.5.18, A.6.5 | CC6.2 | AC-2 | 8.2.5 | HIPAA 164.308(a)(3)(ii)(C) |
| ORPHAN_ACCOUNT | A.5.16, A.5.18 | CC6.2 | AC-2(3) | 7.2.4 | |
| SERVICE_OWNER_MISSING | A.5.16 | CC6.2 | AC-2 | 7.2.5.1 | |
| MOVER_NOT_REVIEWED | A.5.18, A.6.5 | CC6.3 | AC-2 | | |
| PRIVILEGED_REVIEW_OVERDUE | A.8.2, A.5.18 | CC6.3 | AC-2 | 7.2.4 | |
| INACTIVE | A.5.18 | | AC-2(3) | 8.2.6 | |
| POPULATION_GAP | A.5.18 | CC6.2 | AC-2 | 7.2.4 | PCAOB AS 1105.10 |
| UNDECIDED, NO_REVIEWER, LATE_DECISION | A.5.18 | CC6.3 | AC-2 | 7.2.4 | |
| SELF_REVIEW | A.5.3 | CC6.3 | AC-5 | | |
| REVOKE_NOT_REMOVED, REVOKE_PENDING | A.5.18 | CC6.2, CC6.3 | AC-2 | 7.2.4 | |
| RUBBER_STAMP | A.5.18 | CC6.3 | | 7.2.4 | |

ISO references are 🟡: Annex A titles are public, the requirement text is not.
SOC 2, NIST, PCI and HIPAA rows are 🟢 against the requirement text. Which
finding lands on which control is 🔴: an auditor may map ORPHAN_ACCOUNT to CC6.3
instead of CC6.2, or treat INACTIVE as a CC6.2 removal failure. The mapper
reports both the code and the control so the reader can re-map.

## Controls these scripts do not test

| Control | Why not |
|---|---|
| ISO A.5.15, SOC 2 CC6.1 | Policy and architecture; no export shows them. Reported as NOT_COVERED. |
| SOC 2 CC6.2, joiner half | Approval before provisioning lives in tickets. Sample tickets against `created` dates. |
| MFA, password rules (PCI 8.3, 8.4) | Authentication configuration, not account lifecycle. |
| Logging of privileged actions | Monitoring, not lifecycle. |

## Why there is no PASS

Finding nothing in one export on one date is evidence about that date. Operating
effectiveness over a period is an auditor's conclusion, drawn from samples across
it. The mapper's best status is NO_EXCEPTIONS, and PARTLY_TESTED when one input
was missing. 🔴

## SOX and information produced by the entity

For SOX, the user access review is usually an ITGC, and the export it ran on is
IPE. AS 1105.10 asks for its completeness and accuracy to be tested, or the
controls over it. 🟢 [AS1105] Pass `--framework sox` to see AS 1105.10 in the map;
it is tested by the campaign's population check only.

## Sources

- [ISO] ISO/IEC 27001:2022 Annex A, controls 5.3, 5.15, 5.16, 5.18, 6.5, 8.2. https://www.iso.org/standard/27001
- [TSC] AICPA, *2017 Trust Services Criteria* (revised points of focus, 2022), CC6.1–CC6.3. https://www.aicpa-cima.com/resources/download/2017-trust-services-criteria-with-revised-points-of-focus-2022
- [NIST] NIST SP 800-53 Rev. 5, AC-2, AC-2(3), AC-5. https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- [PCI] PCI DSS v4.0.1, Requirements 7.2.4, 7.2.5.1, 8.2.5, 8.2.6. https://www.pcisecuritystandards.org/document_library/
- [HIPAA] 45 CFR 164.308(a)(3)(ii)(C). https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-C/section-164.308
- [AS1105] PCAOB AS 1105, paragraph .10. https://pcaobus.org/oversight/standards/auditing-standards/details/AS1105
- [SAPA11] PCAOB Staff Audit Practice Alert No. 11 (2013). https://pcaobus.org/Standards/QandA/10-24-2013_SAPA_11.pdf
