# CMMC Level 2 readiness sign-off

One sheet per assessment scope. Attach the `--output json` results of
`sprs_score.py`, `scope_classifier.py` and, if you defer anything,
`poam_closeout.py`. This sheet records readiness; it is not an affirmation.
Affirmations are made in SPRS by the Affirming Official.

| Field | Value |
|---|---|
| Organization / CAGE code | |
| Assessment scope name (enclave, whole company) | |
| Contract requirement | Level 2 (Self) / Level 2 (C3PAO) |
| SSP version and date | |
| Scope verdict (`scope_classifier.py`) | CLEAN / FINDINGS / BLOCKED |
| Assets in scope / out of scope | / |
| Score (`sprs_score.py`) | ___ / 110 |
| Score verdict | FINAL_ELIGIBLE / CONDITIONAL_ELIGIBLE / NOT_ELIGIBLE / BLOCKED_NO_SSP |
| Requirements deferred to POA&M | |
| Planned assessment date | |

## Before booking the assessment

- [ ] Every "fix before any assessment" item from `sprs_score.py` is implemented and re-scored.
- [ ] No NA without a written reason in the SSP.
- [ ] Every in-scope asset is in the inventory, the SSP and the scope diagram.
- [ ] Every cloud provider holding CUI has FedRAMP Moderate (or higher) authorization, or you hold its equivalency body of evidence.
- [ ] Every ESP has a customer responsibility matrix that matches the SSP.
- [ ] Evidence is filed per capability (MFA, logging, baselines), with the date it was produced.

## If the result will be Conditional

- Conditional status date (expected): ______
- Closeout deadline (status date + 180 days): ______
- Closeout assessment performed by: OSA / C3PAO (name) ______
- Owner of each POA&M item named: yes / no

## Sign-off

| Role | Name | Date |
|---|---|---|
| Prepared by (compliance lead) | | |
| Reviewed by (IT / security owner) | | |
| Affirming Official (informed, not affirming here) | | |
