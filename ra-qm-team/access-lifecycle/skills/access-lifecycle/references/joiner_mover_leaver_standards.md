# Joiner, mover, leaver: what the frameworks require

What each framework says about granting, changing and removing access, and which
numbers are the standard's and which are yours to set.

Confidence key: 🟢 read in the primary source · 🟡 secondary or practitioner source · 🔴 recommendation.

## 1. Leavers: the control auditors test first

| Framework | Requirement | Number given? |
|---|---|---|
| PCI DSS v4.0.1 8.2.5 | "Access for terminated users is immediately revoked." 🟢 [PCI] | "Immediately"; no hours |
| AICPA TSC CC6.2 | "user system credentials are removed when user access is no longer authorized" 🟢 [TSC] | None; your policy |
| NIST SP 800-53 Rev 5 AC-2 | Notify account managers and disable accounts when users are terminated or transferred, within an organization-defined period 🟢 [NIST] | ODP; FedRAMP High uses 8 hours 🟡 [FedRAMP] |
| HIPAA 45 CFR 164.308(a)(3)(ii)(C) | "Implement procedures for terminating access to electronic protected health information when the employment of a workforce member ends" 🟢 [HIPAA] | None; addressable, so document what you do instead if you do not implement it as written |
| ISO/IEC 27001:2022 A.6.5, A.5.18 | Responsibilities after termination or change of employment; access rights removed on exit 🟡 [ISO] (titles only; text is in the licensed standard) | None |

`access_diff.py` defaults `--leaver-grace-days` to 0 because the strictest common
reading is "immediately". Set it to your written policy, never higher. 🔴

**Login after exit is the finding that ends audits.** An enabled account is a gap;
a login after the termination date is evidence the gap was used. Both block,
and the second needs a security review of what that session did. 🔴

## 2. Inactive and orphaned accounts

- PCI DSS 8.2.6: "Inactive user accounts are removed or disabled within 90 days of inactivity." 🟢 [PCI]
- NIST AC-2(3): disable accounts within an organization-defined period when they have expired, are no longer associated with a user or individual, are in violation of policy, or have been inactive for an organization-defined period. 🟢 [NIST]

The 90 in PCI is the only published number. That is why `--inactive-days` is
required and the error message cites 8.2.6 rather than defaulting to it: an
organization outside PCI scope may choose 30 or 180, and must write that down. 🔴

An orphan is an account that matches nobody on the roster. It is AC-2(3)(b)
in NIST terms. A privileged orphan blocks; a standard one is HIGH because
contractors and external users are often legitimately absent from the HR
roster. Feed their register in as roster rows rather than lowering the severity. 🔴

## 3. Service and system accounts

PCI DSS 7.2.5 and 7.2.5.1 cover application and system accounts, reviewed at the
frequency your targeted risk analysis sets (12.3.1). 🟢 [PCI] The test that fails
most often is earlier than the review: the account has no named human owner, so
nobody can be asked to review it. `SERVICE_OWNER_MISSING` checks that. 🔴

## 4. Joiners

CC6.2 requires that the entity registers and authorizes new users "prior to issuing
system credentials and granting system access". 🟢 [TSC] These scripts cannot
test that: approval evidence lives in the ticketing system, not the account
export. The mapper reports CC6.2 as tested only for removal. Sample joiner
tickets against creation dates separately. 🔴

## 5. Movers

CC6.3 requires access to be authorized, modified or removed based on roles and
responsibilities, "considering the concepts of least privilege and segregation of
duties". 🟢 [TSC] The common failure is accumulation: a mover gets the new role's
access and keeps the old one. `MOVER_NOT_REVIEWED` flags an enabled account whose
last review is older than the person's role change. 🔴

## 6. Privileged access

ISO 27001 A.8.2 (privileged access rights) and NIST AC-2 expect more frequent
review for privileged accounts. FedRAMP's High baseline values are quarterly for
privileged and annually for non-privileged. 🟡 [FedRAMP] Your cadence is
`--privileged-review-days`. If you leave it out, the report says privileged review
age was not checked. It does not assume a period.

## Sources

- [TSC] AICPA, *2017 Trust Services Criteria for Security, Availability, Processing Integrity, Confidentiality, and Privacy* (revised points of focus, 2022), CC6.1–CC6.3. https://www.aicpa-cima.com/resources/download/2017-trust-services-criteria-with-revised-points-of-focus-2022
- [PCI] PCI Security Standards Council, *PCI DSS v4.0.1* (June 2024), Requirements 7.2.4, 7.2.5, 7.2.5.1, 8.2.5, 8.2.6, 12.3.1. https://www.pcisecuritystandards.org/document_library/
- [NIST] NIST SP 800-53 Rev. 5, *Security and Privacy Controls for Information Systems and Organizations*, AC-2, AC-2(3), AC-5. https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- [FedRAMP] FedRAMP Rev. 5 baselines, AC-2 parameter values. https://www.fedramp.gov/documents-templates/
- [HIPAA] 45 CFR 164.308(a)(3)(ii)(C), Security Rule administrative safeguards. https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-C/section-164.308
- [ISO] ISO/IEC 27001:2022, Annex A controls 5.15, 5.16, 5.18, 6.5, 8.2 (titles only; verify text in a licensed copy). https://www.iso.org/standard/27001
- [SD] Schneider Downs, "How can you understand and meet auditor expectations on complete user access reviews?" (practitioner). https://schneiderdowns.com/?p=62986
