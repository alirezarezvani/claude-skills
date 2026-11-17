---
disable-model-invocation: true
description: Full DORA readiness pass - scope and simplified-framework check, major-incident classification and reporting deadlines, and the register of information with Article 30 contract terms.
argument-hint: "entities.csv [incidents.csv] [register.csv]"
---

# /cs-dora-readiness

Answer one question about `$ARGUMENTS`: **which DORA regime applies, is any incident report due now, and what will a supervisor find in our register and contracts?**

Ask first for anything missing: entity type, whether the entity is a microenterprise or identified under NIS2, which functions are critical or important, and whether an ICT incident is live.

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/dora-readiness/scripts/dora_incident_classifier.py --incidents <incidents.csv> --entity <kind>
python ${CLAUDE_PLUGIN_ROOT}/skills/dora-readiness/scripts/dora_scope_check.py --entities <entities.csv>
python ${CLAUDE_PLUGIN_ROOT}/skills/dora-readiness/scripts/register_of_information_check.py --register <register.csv>
```

Run the classifier first when an incident log exists.

## Report

1. Any report overdue or due within 24 hours: incident, deadline, competent authority.
2. Per entity: full, simplified (Art 16), excluded or ICT provider, and what follows.
3. Register and contract gaps, blockers first (Art 30(3) terms, exit plans), with owners; concentration findings.
4. What was not checked: contract wording (counsel), criticality assessments, TLPT.

Never submit a report. Name who does.
