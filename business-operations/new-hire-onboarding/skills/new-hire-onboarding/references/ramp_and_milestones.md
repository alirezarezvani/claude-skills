# Ramp-up and milestones

A 30/60/90 plan is only useful if the day-30 conversation can answer "is this
done?" without asking the hire how they feel. `plan_builder.py` refuses any
milestone without a `done_when`.

## What newcomer research says to watch

Bauer, Bodner, Erdogan, Truxillo and Tucker (2007) meta-analysed 70 samples of
newcomer adjustment. Three signals carry the effect of onboarding onto
performance, satisfaction and intent to stay: **role clarity**, **self-efficacy**
and **social acceptance**. A plan maps to them directly: checkable milestones
give role clarity, an early win builds self-efficacy, and a buddy and regular
1:1s build acceptance. Confidence: high (peer-reviewed meta-analysis).

Gallup (Wetherell and Nelson, 2021) reports that only 12% of US employees say
their company does a good job of onboarding, only 29% of new hires feel fully
prepared after it, and new employees typically take around 12 months to reach
peak performance. Use the 12-month figure to set expectations: day 90 is a
checkpoint, not the finish. Confidence: moderate (Gallup survey, method summary
only).

## Early wins

Watkins (2003) argues that a new leader's first months should secure early
wins: small, visible results that build credibility before the big bets. The
same logic holds for individual contributors. Mark one 30-day milestone
`early_win: true`; the script warns when none is marked.

## Writing a milestone someone can check

Doran (1981) gave the SMART test (specific, measurable, assignable, realistic,
time-related). In practice one rule does most of the work: **name what someone
else will see when it is done.**

| Hope (refused) | Milestone (accepted) |
|---|---|
| Understand the billing architecture | Draw the billing services on one page; buddy reviews it |
| Get familiar with the product | Run the standard demo for the manager without notes |
| Ramp up on the queue | Solve 40 starter-queue tickets at or above the QA bar |
| Build relationships | Hold 1:1s with the 6 people named in the plan; one-line notes each |

Keep 3 to 5 milestones per phase; the script warns above 5.

## Profiles

`--profile` sets the horizon and example milestones: standard, engineering,
sales, support (90 days) and executive (120 days, checkpoints at 30/60/90/120,
buddy every two weeks). Examples are starting points; replace them with the
team's own.

## Sources

1. Bauer, T. N., Bodner, T., Erdogan, B., Truxillo, D. M., & Tucker, J. S. (2007). Newcomer adjustment during organizational socialization: A meta-analytic review of antecedents, outcomes, and methods. *Journal of Applied Psychology*, 92(3), 707-721.
2. Wetherell, E., & Nelson, B. (2021). "8 Practical Tips for Leaders for a Better Onboarding Process". Gallup. https://www.gallup.com/workplace/353096/practical-tips-leaders-better-onboarding-process.aspx
3. Watkins, M. D. (2003). *The First 90 Days*. Harvard Business School Press.
4. Doran, G. T. (1981). There's a S.M.A.R.T. way to write management's goals and objectives. *Management Review*, 70(11), 35-36.
5. Bauer, T. N. (2010). *Onboarding New Employees: Maximizing Success*. SHRM Foundation.
