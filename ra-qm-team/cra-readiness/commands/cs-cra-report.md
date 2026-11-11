---
disable-model-invocation: true
description: Run the CRA Article 14 reporting clock on a vulnerability or incident log - what is due, overdue or late, and what each report must contain.
argument-hint: "events.csv (or describe the event: detected at, aware at, product, exploited?)"
---

# /cs-cra-report

Check `$ARGUMENTS` against the Article 14 deadlines: early warning 24 h and notification 72 h after awareness; final report 14 days after a fix is available (vulnerability) or one month after the notification (severe incident).

If the user describes an event instead of giving a file, write a one-row CSV with the columns from `--help` first. Ask for the awareness time if it is missing; until it is given, the clock runs from detection.

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/cra-readiness/scripts/art14_report_clock.py --events <events.csv>
```

## Report

1. The next deadline in the user's time zone, which report, and the receiving CSIRT (Art 14(7)).
2. Overdue or late reports, and the content each report must carry.
3. Whether users have been informed (Art 14(8)).

The user submits on the ENISA Single Reporting Platform; never claim a report was sent.
