---
disable-model-invocation: true
description: Classify ICT incidents as major under DORA (RTS 2024/1772) and run the reporting clock (RTS 2025/301) - initial, intermediate and final deadlines, weekend rule, client notice.
argument-hint: "incidents.csv (or describe: aware at, classified at, services hit, clients, downtime, cost)"
---

# /cs-dora-incident

Classify each incident in `$ARGUMENTS` and say which report is due when: initial 4 h after classification and no later than 24 h after awareness, intermediate 72 h after the initial, final one month after the last intermediate.

If the user describes an incident instead of giving a file, write a one-row CSV with the columns from `--help` first. Ask for the entity kind (credit institution, CCP, trading venue, NIS2-identified, other): it decides weekend relief.

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/dora-readiness/scripts/dora_incident_classifier.py --incidents <incidents.csv> --entity <kind> [--holidays YYYY-MM-DD,...]
```

## Report

1. The next deadline in the user's time zone, which report, and that it goes to the competent authority.
2. Major or not, and the criteria behind it; recurring incidents found.
3. Overdue or late reports, and whether clients must be informed (DORA Art 19(3)).

The user submits; never claim a report was sent.
