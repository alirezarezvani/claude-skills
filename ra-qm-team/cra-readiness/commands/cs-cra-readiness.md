---
disable-model-invocation: true
description: Full Cyber Resilience Act readiness pass - scope and classify the product portfolio, check Article 14 reporting deadlines, and check Annex I conformity and the SBOM.
argument-hint: "inventory.csv [events.csv] [assessment.csv] [sbom.json]"
---

# /cs-cra-readiness

Answer one question about `$ARGUMENTS`: **which products does the CRA catch, is any report due now, and what stands between each product and its EU declaration of conformity?**

Ask first for anything missing: where each product is sold, when it first shipped, and whether any vulnerability or incident is live. Do not assume a requirement is met because nobody mentioned it.

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/cra-readiness/scripts/art14_report_clock.py --events <events.csv>
python ${CLAUDE_PLUGIN_ROOT}/skills/cra-readiness/scripts/cra_scope_classifier.py --inventory <inventory.csv>
python ${CLAUDE_PLUGIN_ROOT}/skills/cra-readiness/scripts/annex_i_gap_check.py --assessment <assessment.csv>
python ${CLAUDE_PLUGIN_ROOT}/skills/cra-readiness/scripts/sbom_check.py --sbom <sbom.json>
```

Run the reporting clock first when an event log exists. Use `annex_i_gap_check.py --template` to start an assessment.

## Report

1. Any Article 14 report overdue or due within 24 hours: event, deadline, CSIRT.
2. Per product: in or out of scope, class, open conformity routes, blockers with the article.
3. Annex I and SBOM gaps, blockers first, with owners.
4. What was not checked: evidence quality, borderline categories (notified body), legal questions (counsel).

Never submit a report or sign a declaration. Name who does.
