# Reconciliation sign-off

One sheet per account per period. Attach the `reconciliation_matcher.py --output json` result.

| Field | Value |
|---|---|
| Entity / account | |
| Period end | |
| GL balance | |
| Source (bank / sub-ledger) balance | |
| Unexplained difference (must be 0.00) | |
| Script verdict | RECONCILED / RECONCILED_WITH_ITEMS / UNRECONCILED |

## Reconciling items

| Date | Amount | Reference | Side | Action | Age (days) | Owner | Resolved by |
|---|---|---|---|---|---|---|---|
| | | | GL only / source only | timing / journal entry | | | |

Items over the escalation limit (policy: ___ days) need a resolution plan below.

## Preparer

- Name: ________ Date: ________
- Source documents used (statement, sub-ledger report, export file name):
- Journal entries raised for source-only items (entry numbers):

## Reviewer (must not be the preparer)

A signature alone is not evidence of review. Record what you did.

- Name: ________ Date: ________
- I agreed the source balance to: ________ (document)
- I agreed the GL balance to: ________ (trial balance / report)
- Items I tested or challenged, and the outcome:
- Items over the escalation limit, and the plan for each:
- Conclusion: ☐ approved ☐ returned to preparer (reason): ________
