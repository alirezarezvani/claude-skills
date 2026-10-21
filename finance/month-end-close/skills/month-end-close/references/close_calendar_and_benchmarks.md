# Close calendar and benchmarks

How to order a close, why the critical path is the only place to save days,
and what the published days-to-close numbers do and do not say.

Confidence key: 🟢 read in the primary source · 🟡 secondary or vendor source · 🔴 convention or recommendation.

## 1. The close is a dependency graph

A typical group close, as one ERP vendor describes it: 🟡 [Workday]

1. Entity close: sub-ledger cut-off, journal entries, reconciliations, adjustments
2. Trial balance submitted and validated; local charts mapped to the group chart
3. Intercompany matching and elimination
4. Foreign-currency translation
5. Group top-side adjustments, after subsidiary data is consolidated and reconciled
6. Consolidation and review
7. Reporting and filing

Two orderings are stated outright: intercompany before consolidation, and
mapping before eliminations. No auditing body publishes a canonical task
sequence; the order "sub-ledgers → accruals → intercompany → reconciliations →
consolidation → flux → reporting" is industry convention. 🔴

Write your checklist as a graph (`depends_on` in the plan JSON), not a list.
`close_calendar_planner.py` refuses a cycle and an unknown dependency, because
both mean the checklist is wrong, not the calendar.

## 2. Critical path

Forward pass: each task starts when its last predecessor finishes. Backward
pass from the last finish: latest start without delaying the close. Slack =
latest start - earliest start. Tasks with zero slack form the critical path.
🔴 standard project-scheduling method (CPM)

Consequences that change behaviour:

- Automating an off-critical task (e.g. depreciation with two days of slack)
  does not move the close date at all.
- Splitting a long critical task between two people, or starting it earlier
  with a soft cut-off, does.
- A person who owns more than half the critical path is the close date. The
  planner warns on that (C6) and on any day one person is booked above one day of work (C4).

## 3. Workday deadlines

Deadlines are written as WD+n: WD1 is the first business day after period
end. The planner skips weekends and listed holidays when it maps workdays to
dates. COSO 2013 Principle 12 lists "performs in a timely manner" and
"establishes responsibility and accountability" among the points of focus for
deploying control activities, which is what a deadline and a named owner per
task make checkable. 🟢 [COSO P12]

## 4. Days-to-close benchmarks, with caveats

- APQC's Open Standards Benchmarking measure is cycle time "from running the
  trial balance to completing consolidated financial statements". Figures
  widely quoted from it: top performers about 4.8 calendar days, median about
  6.4, bottom performers 10 or more. 🟡 — the APQC article is members-only, and
  these numbers come from vendors quoting APQC data from around 2017. [numeric, APQC]
- APQC's own annual-close article: top performers 10 days or less, median 18,
  slower performers 35. 🟢 [APQC annual]

Use benchmarks to start a conversation, not to set a target. A five-day close
with plugged reconciliations is worse than an eight-day close that proves. 🔴

## 5. Auditor's view of the close

PCAOB AS 2201 requires the auditor to evaluate the period-end financial
reporting process, including how totals are entered into the general ledger
and how recurring and non-recurring adjustments are recorded. 🟢 [AS 2201 ¶.26]
The close calendar, owner list and review evidence are what an auditor walks
through, so the plan JSON doubles as audit documentation. 🔴

## Sources

1. Workday. *Financial consolidation and close process guide.* https://blog.workday.com/en-gb/financial-consolidation-close-process-guide.html (vendor)
2. APQC. *Cycle Time to Perform the Monthly Close* (members-only). https://www.apqc.org/knowledge-base/documents/cycle-time-perform-monthly-close
3. Numeric. *How long does month-end close take?* (vendor, quoting APQC). https://www.numeric.io/blog/how-long-does-month-end-close-take
4. APQC. *How to streamline the annual closing process.* https://www.apqc.org/resources/blog/how-streamline-annual-closing-process-and-speed-year-end-close
5. COSO (2013). *Internal Control — Integrated Framework*, Principle 12, via AAA. https://aaahq.org/node/35157
6. PCAOB. *AS 2201: An Audit of Internal Control Over Financial Reporting.* https://pcaobus.org/oversight/standards/auditing-standards/details/AS2201
