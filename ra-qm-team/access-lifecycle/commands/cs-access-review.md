---
description: Full access-lifecycle pass - diff the HR roster against account exports, check the review campaign, and map every exception to the controls it breaks.
argument-hint: "hr_roster.csv accounts.csv [campaign.csv] [--framework soc2,iso27001,pci,nist80053,hipaa,sox]"
---

# /cs-access-review

Answer one question about `$ARGUMENTS`: **would this access review survive the auditor's walkthrough?**

Ask first for anything policy-defined that is missing: the inactivity period, the privileged review cadence and
the remediation window. Do not supply them yourself.

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/access-lifecycle/scripts/access_diff.py --roster <roster.csv> --accounts <accounts.csv> \
  --inactive-days <policy> --privileged-review-days <policy> --output json > diff.json
python ${CLAUDE_PLUGIN_ROOT}/skills/access-lifecycle/scripts/access_review_campaign.py --decisions <campaign.csv> \
  --population <accounts.csv> --remediation-days <policy> [--close-date YYYY-MM-DD] --output json > campaign.json
python ${CLAUDE_PLUGIN_ROOT}/skills/access-lifecycle/scripts/control_evidence_mapper.py --diff diff.json --campaign campaign.json \
  --framework <frameworks>
```

Skip the campaign step if no campaign file was given; the mapper then reports campaign-tested controls as PARTLY_TESTED or NOT_TESTED.

## Report

1. Verdict per script, blockers first: account, person, why, action.
2. The per-control table from the mapper.
3. Evidence to keep, and what was not tested.

Do not decide keep or revoke for anyone. The reviewer does.
