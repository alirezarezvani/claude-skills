---
name: access-lifecycle
description: Use when preparing or running a user access review, checking that leavers lost their access, finding orphaned or ownerless service accounts, answering an auditor's access-control request for SOC 2, ISO 27001, PCI DSS, HIPAA or NIST 800-53, or checking whether a finished review campaign will hold up. Diffs the HR roster against account exports, tests the campaign for coverage, self-review, unremoved revokes and rubber-stamping, and maps every exception to the controls it breaks.
argument-hint: "[HR roster CSV + account export CSV | campaign decisions CSV | access_diff / campaign JSON]"
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "Three deterministic stdlib scripts (roster-vs-export diff, review-campaign checker, control evidence mapper) with blocking exit codes; policy periods required as flags, never defaulted; controls cited to AICPA TSC CC6.1-6.3, NIST SP 800-53 Rev 5 AC-2/AC-2(3)/AC-5, PCI DSS v4.0.1 7.2.4/7.2.5.1/8.2.5/8.2.6, HIPAA 164.308(a)(3)(ii)(C), PCAOB AS 1105.10 and ISO/IEC 27001:2022 Annex A titles"
  distinct_from: "soc2-compliance and information-security-manager-iso27001 (whole-programme readiness and ISMS design); isms-audit-expert (audit programme and findings); this skill runs the joiner/mover/leaver and access-review evidence itself"
---

# Access Lifecycle

> **Portability:** 3 stdlib scripts, no network, no IdP or HR connection. Export CSV, run, keep the output as evidence.
> **Not audit advice.** Periods and thresholds are your policy; the scripts make you state them.

Access reviews fail audits in four ordinary ways: the review ran on an incomplete
export, someone approved their own access, a revoke was decided and never
carried out, and leavers kept working accounts nobody looked at. Each script
catches one class of these before the auditor does.

## Workflow

```bash
# 1 - Diff: who has access that the HR roster says they should not?
python scripts/access_diff.py --roster hr_roster.csv --accounts accounts.csv \
  --inactive-days 90 --privileged-review-days 90 --as-of 2026-10-31
# 2 - Campaign: did the review cover everything, and did the revokes happen?
python scripts/access_review_campaign.py --decisions campaign.csv --population accounts.csv \
  --remediation-days 10 --close-date 2026-10-20
# 3 - Map: which controls do the exceptions break, and what evidence do you keep?
python scripts/control_evidence_mapper.py --diff diff.json --campaign campaign.json --framework soc2,iso27001
```

**Step 1** joins each account to the roster on employee ID, then email. A
terminated person with an enabled account is a blocker; one who logged in after
their exit date is a worse one. Accounts that match nobody are orphans; service
accounts need a named owner. Inactivity and privileged-review age use your periods.

**Step 2** checks the campaign against the export it was built from. An enabled
account missing from the campaign means the review did not cover the population,
whatever the sign-off sheet says. It also catches undecided lines, self-review,
revokes not removed inside your window, late decisions, and a reviewer who kept
every line of a large batch at machine speed.

**Step 3** turns findings into a per-control table: FAIL, EXCEPTIONS,
NO_EXCEPTIONS, PARTLY_TESTED, NOT_TESTED or NOT_COVERED, each with what an
auditor tests and the evidence to keep. There is no PASS.

## The gates block on (exit 4)

1. A leaver with an enabled account, or any login after the exit date.
2. A privileged orphan account, or a privileged service account with no owner.
3. An enabled account the campaign never reviewed.
4. An undecided line, a self-review, or a decision with no reviewer named.
5. A revoke or modify with no removal recorded past your remediation window.

## Hard rules

- **Periods are policy.** `--inactive-days` and `--remediation-days` have no default. PCI DSS 8.2.6 says 90 days; your policy may differ.
- **Prove removals by re-export.** A closed ticket is not evidence the access is gone.
- **The export is evidence too.** Keep the query, the pull time and the row count (PCAOB AS 1105.10).
- **A rubber-stamp flag is a signal, not proof.** Ask the reviewer what they checked; do not call it fraud.
- **No PASS from a script.** Operating effectiveness is the auditor's conclusion.

## Scripts

| Script | Role | Exit codes |
|---|---|---|
| `scripts/access_diff.py` | Roster vs account export: leavers, orphans, ownerless service accounts, movers, privileged review age, inactivity | 0 clean · 2 findings · 3 bad input · 4 blocked |
| `scripts/access_review_campaign.py` | Population coverage, undecided, self-review, unremoved revokes, late decisions, rubber-stamp signal | 0 · 2 · 3 · 4 incomplete |
| `scripts/control_evidence_mapper.py` | Findings → per-control status for ISO 27001, SOC 2, NIST 800-53, PCI DSS, HIPAA, SOX IPE | 0 · 2 exceptions · 3 · 4 fail |

All support `--help`, `--sample` and `--output json`.

## References and assets

- [`references/joiner_mover_leaver_standards.md`](references/joiner_mover_leaver_standards.md) — what each framework requires for provisioning, change and removal (7 sources)
- [`references/access_review_campaigns.md`](references/access_review_campaigns.md) — population, reviewers, cadence, remediation, what auditors reject (6 sources)
- [`references/control_crosswalk.md`](references/control_crosswalk.md) — finding codes to controls across six frameworks, with the caveats (7 sources)
- [`assets/hr_roster.example.csv`](assets/hr_roster.example.csv), [`assets/accounts.example.csv`](assets/accounts.example.csv), [`assets/campaign.example.csv`](assets/campaign.example.csv) — input formats
- [`assets/access_review_signoff.md`](assets/access_review_signoff.md) — campaign sign-off with the evidence fields a reviewer fills in
