# Reconciliation standards

What a reconciliation must contain to be evidence, how to age what is left,
and why "reviewed" needs more than a signature.

Confidence key: 🟢 read in the primary source · 🟡 institutional policy or secondary source · 🔴 recommendation.

## 1. A reconciliation is a proof

Agreement of two balances is a result. A reconciliation is the proof that the
difference between them is fully explained by named items:

```
adjusted source = source balance + items in GL not yet in source   (timing)
adjusted GL     = GL balance + items in source not yet in GL       (entries to book)
unexplained     = adjusted source - adjusted GL                    → must be 0
```

`reconciliation_matcher.py` builds this proof for any pair of detail files:
bank to cash GL, AR sub-ledger to AR control, payroll register to payroll
liabilities. A non-zero unexplained difference blocks sign-off. Plugging it
with a "reconciling difference" line hides the one number someone should
investigate. 🔴

Hints the script gives, from long-standing bookkeeping practice: 🔴
- a difference already present in the opening balances implied by each side
  (ending balance minus the period's detail) was carried in from last period:
  fix it in that reconciliation, not this one;
- a difference divisible by 9 often means transposed digits (54 for 45);
- a difference equal to an open item, or twice one, often means a posting
  missed or doubled, or entered with the wrong sign.

## 2. What it must contain

One university's published policy is a good, concrete example: 🟡 [Vanderbilt]

- a preparer and an approver who sign off and **cannot be the same person**;
- support clear enough that someone without deep knowledge of the account can
  understand the balance;
- every reconciling item identified, explained and supported;
- frequency set by risk (daily, monthly, quarterly);
- aging from the first day after month-end in buckets 0-30, 31-60, 61-90, >90 days;
- items over 90 days and over 10,000 need a documented resolution plan sent to the controller.

The 60- and 90-day limits in the script are this example's policy, not a
standard. Set `--escalate-days` and `--stale-days` to yours.

COSO 2013 Principle 10 names reconciliations among the control activities an
entity selects to mitigate risk, alongside authorizations, approvals,
verifications and business performance reviews. 🟢 [COSO P10]

## 3. Review precision

PCAOB Staff Audit Practice Alert 11 on management review controls: 🟢 [SAPA 11]

- "Verifying that a review was signed off provides little or no evidence by itself."
- Precision depends on the review's objective, level of aggregation,
  consistency, correlation to the assertion, predictability of expectations,
  and the criteria for investigation.
- A review threshold close to materiality has less precision and greater risk.

AS 2201 ¶.23 distinguishes entity-level controls that only monitor from those
designed to operate precisely enough to prevent or detect misstatements. 🟢 [AS 2201]

So the sign-off sheet in `assets/reconciliation_signoff.md` asks the reviewer
what they checked, against which document, and which items they challenged,
not just for a name. 🔴

## 4. Segregation of duties

The preparer cannot be the reviewer. `reconciliation_matcher.py` blocks when
the names match; `close_calendar_planner.py` blocks a key control whose
reviewer is its owner. In a team too small to separate, document the
compensating control (e.g. CFO review of all reconciliations above a threshold)
in the plan. 🔴

## Sources

1. Vanderbilt University. *Account Reconciliations Policy.* https://finance.vanderbilt.edu/policies/Account_Reconciliations_Policy.pdf
2. PCAOB. *Staff Audit Practice Alert No. 11: Considerations for Audits of Internal Control Over Financial Reporting.* https://pcaobus.org/Standards/QandA/10-24-2013_SAPA_11.pdf
3. PCAOB. *AS 2201.* https://pcaobus.org/oversight/standards/auditing-standards/details/AS2201
4. COSO (2013). *Internal Control — Integrated Framework*, Principle 10, via AAA. https://aaahq.org/node/35143
5. COSO (2013). Principle 12, via AAA. https://aaahq.org/node/35157
6. PCAOB. *AS 2305: Substantive Analytical Procedures.* https://pcaobus.org/oversight/standards/auditing-standards/details/AS2305
