# SLA design and measurement

Confidence: 🟢 primary source, 🟡 established secondary source, 🔴 common practice, stated as such.

## What to measure

| Metric | Definition used by `sla_check.py` | Why it matters |
|---|---|---|
| First-response attainment | share of tickets whose first human response came within target, on the ticket's clock | the promise most contracts name |
| Resolution attainment | share resolved within target; with `--reopen-breaches`, a reopened ticket counts as missed | "closed" is not "solved" |
| p50 / p90 | median and 90th percentile elapsed hours | averages hide the tail customers remember |
| Open breached / at risk | open tickets past target, or within `--risk-hours` of it | the only numbers you can still change today |
| Backlog age | open tickets by age bucket | a growing >7d bucket means the queue is not keeping up |
| Reopen rate | reopened / tickets | first-contact resolution in reverse |

Open tickets past target count as misses in attainment. Excluding them is the most common way an SLA report looks better than the queue.

## Business hours vs calendar hours

An 8-hour target means 8 working hours (one day) on a business clock and 8 elapsed hours on a calendar clock. Mixing them is the usual cause of disputes: a ticket created Friday 16:30 with a 4-hour business target is due Monday 12:30, not Friday 20:30. Put the clock, the working days, the hours, the timezone and the holiday calendar in the policy, per priority, and in the customer contract. 🟢 ITIL 4's Service Level Management practice treats the agreed service hours as part of the SLA itself. [1]

Urgent tiers usually run on the calendar clock when someone is on call; give them a calendar clock only if someone actually is. 🔴

## Setting targets

- Start from what the queue already does (p90 over the last quarter), not from a competitor's marketing page. 🔴
- Fewer tiers are easier to keep: three priorities with clear definitions beat five that agents apply inconsistently. 🔴
- Customers judge effort more than speed: reducing repeat contacts and transfers moves loyalty more than shaving response time. 🟡 [2][3]
- A queue's average wait is set by arrivals and capacity (Little's Law, L = λW) [4]; a target the staffing cannot meet is a promise to miss. Size the team with `staffing_plan.py` before committing.

## Sources

1. AXELOS, *ITIL 4 Practice Guide: Service Level Management*, 2020
2. M. Dixon, K. Freeman, N. Toman, "Stop Trying to Delight Your Customers", Harvard Business Review, July-August 2010
3. M. Dixon, N. Toman, R. DeLisi, *The Effortless Experience*, Portfolio/Penguin, 2013
4. J. D. C. Little, "A Proof for the Queuing Formula: L = λW", Operations Research 9(3):383-387, 1961
5. N. Gans, G. Koole, A. Mandelbaum, "Telephone Call Centers: Tutorial, Review, and Research Prospects", Manufacturing & Service Operations Management 5(2):79-141, 2003
