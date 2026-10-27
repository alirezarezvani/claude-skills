# Access review campaigns that survive an audit

A campaign is a population, a set of decisions and a set of removals. Auditors test
all three, and most rejected campaigns fail on the first.

Confidence key: 🟢 read in the primary source · 🟡 secondary or practitioner source · 🔴 recommendation.

## 1. Population: the review is only as complete as the export

PCAOB AS 1105.10: when using information produced by the company, the auditor
evaluates whether it is sufficient and appropriate, which includes testing its
accuracy and completeness, or testing the controls over it. 🟢 [AS1105] A user
access review run on an export that left out a system, a domain or the service
accounts did not review the population, however carefully each line was decided.

What to keep with every campaign: 🔴
- the query or report name and its parameters;
- the pull timestamp and who pulled it;
- the row count, reconciled to the source system's own count.

`access_review_campaign.py --population` compares the campaign to the export.
An enabled account missing from the campaign blocks. A campaign line with no
matching account means the campaign was built from a different pull.

## 2. Reviewers

- Users may not review their own access. 🟡 [SD] It is also a segregation-of-duties
  failure in ISO 27001 A.5.3 and NIST AC-5. 🟢 [NIST]
- Every decision names a reviewer. An anonymous "keep" is not evidence of review.
- The reviewer should know the role: the line manager for business access, the
  system owner for privileged and service accounts. 🔴

## 3. Decisions and rubber-stamping

"All access should be reviewed," and a cover-page sign-off over a list nobody
read is rejected. 🟡 [SD] PCAOB Staff Audit Practice Alert 11 makes the general
point for review controls: the auditor tests the precision of the review, not the
signature. 🟢 [SAPA11]

The rubber-stamp signal (default: 20 or more lines, all keep, a median of 10
seconds or less between decisions) is a prompt to ask the reviewer what they
checked. It is not proof they did not. Thresholds are flags because what is
plausible depends on how much context the review tool shows. 🔴

## 4. Cadence

| Source | Cadence |
|---|---|
| PCI DSS v4.0.1 7.2.4 | All user accounts, including third-party and vendor accounts, at least once every six months 🟢 [PCI] |
| PCI DSS v4.0.1 7.2.5.1 | Application and system accounts, per targeted risk analysis 🟢 [PCI] |
| NIST AC-2 j | Organization-defined frequency 🟢 [NIST]; FedRAMP High: privileged quarterly, others annually 🟡 [FedRAMP] |
| SOC 2, ISO 27001 | None prescribed; set in policy and follow it 🟢 [TSC] |

Quarterly is common practice for SOX-relevant systems, with the review completed
about 15 days after quarter-end. 🟡 [SD]

## 5. Remediation: the step that is skipped

PCI 7.2.4 requires that inappropriate access is addressed and management
acknowledges the access remains appropriate. 🟢 [PCI] Neither PCI nor SOC 2 gives a
number of days, so `--remediation-days` is required. Ten business days is a
common internal choice; the standard is whatever you wrote. 🔴

Confirm removals by re-running the export, not by closing the ticket. 🟡 [SD]
Keep both exports: before and after.

## 6. What auditors reject

1. A population that cannot be shown to be complete.
2. Self-review, or no reviewer recorded.
3. Revokes decided but still active at the next export.
4. Lines left undecided at campaign close.
5. Sign-off without any record of what was checked.

## Sources

- [AS1105] PCAOB AS 1105, *Audit Evidence*, paragraph .10. https://pcaobus.org/oversight/standards/auditing-standards/details/AS1105
- [SAPA11] PCAOB Staff Audit Practice Alert No. 11, *Considerations for Audits of Internal Control over Financial Reporting* (October 2013). https://pcaobus.org/Standards/QandA/10-24-2013_SAPA_11.pdf
- [PCI] PCI Security Standards Council, *PCI DSS v4.0.1*, Requirements 7.2.4, 7.2.5.1. https://www.pcisecuritystandards.org/document_library/
- [NIST] NIST SP 800-53 Rev. 5, AC-2 j, AC-5. https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- [FedRAMP] FedRAMP Rev. 5 baselines. https://www.fedramp.gov/documents-templates/
- [TSC] AICPA, *2017 Trust Services Criteria* (revised points of focus, 2022), CC6.2–CC6.3. https://www.aicpa-cima.com/resources/download/2017-trust-services-criteria-with-revised-points-of-focus-2022
- [SD] Schneider Downs, "How can you understand and meet auditor expectations on complete user access reviews?" (practitioner). https://schneiderdowns.com/?p=62986
