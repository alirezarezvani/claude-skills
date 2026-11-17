---
disable-model-invocation: true
description: Full NIS2 readiness pass - classify entities as essential, important or out, check Article 23 reporting deadlines, and gap-check the Article 21 measures.
argument-hint: "entities.csv [incidents.csv] [assessment.csv]"
---

# /cs-nis2-readiness

Answer one question about `$ARGUMENTS`: **does NIS2 catch us, as what, is any report due now, and what stands between us and the Article 21 baseline?**

Ask first for anything missing: sectors, headcount, turnover and balance sheet per entity, where each is established, and whether an incident is live. Do not assume a measure is in place because nobody mentioned it.

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/nis2-readiness/scripts/nis2_incident_clock.py --incidents <incidents.csv>
python ${CLAUDE_PLUGIN_ROOT}/skills/nis2-readiness/scripts/nis2_scope_classifier.py --entities <entities.csv>
python ${CLAUDE_PLUGIN_ROOT}/skills/nis2-readiness/scripts/art21_gap_check.py --assessment <assessment.csv>
```

Run the clock first when an incident log exists. Use `art21_gap_check.py --template` to start an assessment, and `--digital-provider` for DNS, cloud, MSP and similar providers.

## Report

1. Any report overdue or due within 24 hours: incident, deadline, recipient.
2. Per entity: category, supervising Member State, registration duty and date, DORA overlap.
3. Article 21 gaps, blockers first, with owners; what the management body must approve.
4. What was not checked: evidence quality, national designations, legal questions (counsel).

Never submit a report. Name who does.
