# Metrics review, week 48

Two things before Friday's exec review.

1. PR #412 edits our dbt semantic layer. `base/semantic_manifest.json` is from main,
   `pr/semantic_manifest.json` and `pr/manifest.json` are from the PR branch (both from `dbt parse`).
   Is it safe to merge? What changes for whom? Also tell us anything wrong with the definitions themselves.

2. The CFO's daily revenue (warehouse, `warehouse_daily_revenue.csv`) and the Looker dashboard
   (`looker_daily_revenue.csv`) disagree on most days of November. Finance wants to "fix Looker".
   Who is right, and what is going on?
