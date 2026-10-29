# Access review sign-off

One sheet per system per campaign. Attach the `--output json` results of
`access_review_campaign.py` and `control_evidence_mapper.py`.

| Field | Value |
|---|---|
| System / application | |
| Campaign period and close date | |
| Export used (report or query name) | |
| Export pulled by, and when | |
| Rows in export / rows in source system's own count | / |
| Lines in campaign | |
| Script verdict | COMPLETE / COMPLETE_WITH_FINDINGS / INCOMPLETE |
| Remediation window (policy) | ___ days |

## Population (AS 1105.10)

- How was the export's completeness checked? (row count tie-out, second source, control over the report)
- Accounts excluded from the campaign, and why (must be none, or each justified):

## Revokes and modifications

| Account | Decision | Decided | Removed | Re-export confirming removal (file, date) |
|---|---|---|---|---|
| | revoke / modify | | | |

## Reviewers

A signature alone is not evidence of review. Each reviewer records what they checked.

| Reviewer | Lines | Keep / revoke / modify | What I compared each line against | Date |
|---|---|---|---|---|
| | | / / | (role description, ticket, manager confirmation) | |

No reviewer may appear as the user on a line they decided.

## Exceptions open at sign-off

| Finding | Account | Owner | Due | Compensating step |
|---|---|---|---|---|
| | | | | |

## Approval

- System owner: ________ Date: ________
- Conclusion: ☐ complete ☐ complete with exceptions listed above ☐ returned (reason): ________
