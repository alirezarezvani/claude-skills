# Buddy and check-ins

Onboarding plans rarely fail on day one. They fail in week five, when the buddy
has stopped meeting and the day-30 checkpoint was never booked.
`ramp_check.py` looks for exactly that.

## The buddy

Microsoft's onboarding buddy pilot found that of new hires who met their buddy
at least once in the first 90 days, 56% said the buddy helped them become
productive quickly; 73% for 2-3 meetings, 86% for 4-8, and 97% for more than 8
(Microsoft Workplace Insights; Klinghoffer, Young and Haspas, HBR 2019).
Confidence: moderate. It is a company survey, self-reported and correlational:
hires who got on with their buddy may simply have met more. It still sets a
cheap, sensible floor. Weekly meetings give 13 in 90 days; `ramp_check.py`
flags fewer than half the weekly pace, or none in the first 10 days.

The buddy is a peer, never the manager: the point is someone the hire can ask
the questions they would not ask the person who reviews them. Bauer et al.
(2007) name social acceptance as one of the three adjustment signals.

## Checkpoints and 1:1s

Book day 30, 60 and 90 on day one. A checkpoint counts as held within
`--grace` days (default 5) of its date. A gap of more than 14 days between
manager 1:1s is flagged.

When a milestone is overdue and no checkpoint was held in its phase,
`ramp_check.py` adds NO_CHECKPOINT_BEFORE_OVERDUE: the plan was never reviewed,
so the first question is what blocked it, not whether the hire is the problem.

Bock (2015) describes Google's "just-in-time" checklist email to managers the
Sunday before a hire starts (assign a buddy, set up 1:1s, introduce the hire)
and reports that hires whose managers acted on it became productive faster.
Confidence: moderate (company-internal measure reported in a book).

## The verdict is about the onboarding

ON_TRACK / AT_RISK / OFF_TRACK describes whether the onboarding ran as
planned. It is not a probation decision. A performance or probation decision
belongs to the manager and HR, with the hire's account of what got in the way,
and in many jurisdictions with its own procedure.

## A claim not to repeat

"Strong onboarding improves new-hire retention by 82% and productivity by over
70%" is attributed to Brandon Hall Group research, often via Glassdoor
marketing material. We could find no public primary study, sample or method
behind it. Treat it as folklore; cite Bauer et al. (2007) or Gallup instead.
Confidence that it is unsupported: moderate (absence of a public source, not a
refutation).

## Sources

1. Microsoft Workplace Insights, "Every new employee needs an onboarding buddy". https://workplaceinsights.microsoft.com/?p=853
2. Klinghoffer, D., Young, C., & Haspas, D. (2019). "Every New Employee Needs an Onboarding 'Buddy'". *Harvard Business Review*.
3. Bauer, T. N., Bodner, T., Erdogan, B., Truxillo, D. M., & Tucker, J. S. (2007). *Journal of Applied Psychology*, 92(3), 707-721.
4. Wetherell, E., & Nelson, B. (2021). Gallup. https://www.gallup.com/workplace/353096/practical-tips-leaders-better-onboarding-process.aspx
5. Bock, L. (2015). *Work Rules!* Twelve.
6. Bauer, T. N. (2010). *Onboarding New Employees: Maximizing Success*. SHRM Foundation.
