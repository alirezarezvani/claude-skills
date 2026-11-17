# Cost anomalies and unit economics

Verified 2026-11-17. 🟢 read on the primary page this session, 🟡 primary not re-read, 🔴 convention.

## What counts as an anomaly

🟢 The Framework defines Anomaly Management as detecting, identifying, alerting on and managing unexpected cost events, where an anomaly is spend that differs from normal historical or expected spend. Crawl teams find anomalies more than a week late through budget alerts; Walk teams have automated detection with context-relevant thresholds routed to the owning team. Its KPIs are mean time to detect, mean time to notify the owner, and how long anomalies stay unresolved. [1]

## The detector in `cost_anomaly.py`

Per group and day, against the previous `--window` days (default 14):

1. **Robust z-score.** Median and MAD (scaled by 1.4826 to estimate a standard deviation under normality) instead of mean and SD, so last week's spike does not hide this week's. [2][3]
2. **Relative floor** (`--min-rel`, default 30%) so a noisy service does not fire on every wobble.
3. **Money floor** (`--min-abs`, default 50 in billing currency) so a service that went from 0.40 to 1.20 does not page anyone.

All three must hold. Defaults are judgement calls (🔴): tighten `-k` for steady services, loosen for batch workloads with weekly cycles, and set `--min-abs` to the amount worth an engineer's hour. Fewer than 14 days is refused: there is no baseline.

Weekly seasonality (weekday vs weekend) is absorbed by a 14-day window only partly; for strongly weekly services compare like weekdays or use the provider's detector, which models seasonality (AWS Cost Anomaly Detection, Azure anomaly alerts). 🟡 [4][5]

## Unit economics

🟡 The Framework's Unit Economics capability ties cloud cost to a business output (cost per order, per active user, per transaction) so growth in total spend can be judged against growth in the business. [6] `--units` takes a daily `date,units` file and compares cost per unit between the two halves of the period; a rising unit cost is a finding even when no single day is anomalous.

Pick a unit the business already reports, that cloud cost actually scales with, and that the owning team can move. 🔴 [7]

## Sources

1. FinOps Foundation, "Anomaly Management" FinOps Framework capability, finops.org/framework/capabilities/anomaly-management/
2. P. J. Rousseeuw & C. Croux, "Alternatives to the Median Absolute Deviation", Journal of the American Statistical Association 88(424), 1993
3. B. Iglewicz & D. Hoaglin, *How to Detect and Handle Outliers*, ASQC Basic References in Quality Control vol. 16, 1993
4. AWS, "Detecting unusual spend with AWS Cost Anomaly Detection", docs.aws.amazon.com/cost-management/latest/userguide/manage-ad.html
5. Microsoft Learn, "Identify anomalies and unexpected changes in cost", learn.microsoft.com/azure/cost-management-billing/understand/analyze-unexpected-charges
6. FinOps Foundation, "Unit Economics" FinOps Framework capability, finops.org/framework/capabilities/unit-economics/
7. J.R. Storment & Mike Fuller, *Cloud FinOps*, 2nd ed., O'Reilly 2023, chapters on unit economics
