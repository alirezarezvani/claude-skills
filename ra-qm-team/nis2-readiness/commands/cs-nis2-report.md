---
disable-model-invocation: true
description: Run the NIS2 Article 23 clock on an incident log - which incidents are significant, which report is due, overdue or late, and what each must contain.
argument-hint: "incidents.csv (or describe the incident: detected at, aware at, impact)"
---

# /cs-nis2-report

Check `$ARGUMENTS` against Article 23(4): early warning 24 h and notification 72 h after awareness (24 h for trust service providers), final report one month after the notification.

If the user describes an incident instead of giving a file, write a one-row CSV with the columns from `--help` first. Ask for the awareness time if it is missing; until it is given, the clock runs from detection.

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/nis2-readiness/scripts/nis2_incident_clock.py --incidents <incidents.csv>
```

## Report

1. The next deadline in the user's time zone, which report, and the recipient (CSIRT or authority; BSI in Germany).
2. Significance and the criterion behind it (Art 23(3), or 2024/2690 for digital providers).
3. Overdue or late reports, missing content, and whether service recipients were informed (Art 23(1)).

The user submits; never claim a report was sent.
