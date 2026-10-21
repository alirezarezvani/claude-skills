# Flux analysis and materiality

How auditors think about investigating fluctuations, why the script's
thresholds are yours to set, and what makes an explanation acceptable.

Confidence key: 🟢 read in the primary source · 🟡 secondary or vendor source · 🔴 recommendation.

## 1. Start from an expectation

PCAOB AS 2305 on substantive analytical procedures: 🟢 [AS 2305]

- ¶.05 — expectations come from plausible relationships among data.
- ¶.17 — the expectation must be precise enough to give the desired assurance.
- ¶.20 — the amount of difference from the expectation that can be accepted
  without further investigation is influenced by materiality.
- ¶.21 — significant unexpected differences should be evaluated, and
  management's responses "should ordinarily be corroborated with other evidential matter".

AU-C 520 (AICPA) and ISA 520 follow the same shape: develop an expectation,
set an acceptable difference, investigate anything beyond it. 🟡 [AU-C 520 summary]
The PCAOB proposed replacing AS 2305 in June 2024; check its current status
before citing paragraph numbers in an audit file. 🟡 [PCAOB proposal]

Prior period is the weakest expectation; budget or a driver-based estimate
(headcount × average cost, ARR × days) is stronger. `flux_analyzer.py
--compare budget` uses the budget column when you have one. 🔴

## 2. Thresholds are policy

There is no standard flux threshold. One vendor states plainly that "there is
no single agreed-upon number" and sees teams using roughly 0.5% to 10% plus
judgment. 🟡 [Vena] The script's defaults (10% **and** 10,000) are a starting
point, not a rule:

- `--rule and` (default) avoids noise from tiny accounts with large percentages
  and large accounts with tiny percentages.
- `--rule or` is stricter; use it for high-risk accounts.
- Sign flips are always material, and new or closed balances above `--abs` are too.
- SAPA 11's warning applies: a threshold close to materiality has little
  precision. Set the absolute threshold well below planning materiality. 🟢 [SAPA 11]

## 3. Materiality rules of thumb (audit planning, not close thresholds)

Commonly quoted quantitative benchmarks: 5% of pre-tax income, 0.5-1% of
revenue, 0.5-1% of total assets, 1% of equity. 🟡 [CFI] Neither the PCAOB nor
the AICPA prescribes percentages; these are conventions auditors start from.
Use them to sanity-check that your flux `--abs` sits comfortably below what
your auditor will treat as material. 🔴

## 4. What a good explanation contains

The lint in `flux_analyzer.py` encodes a minimum: 🔴

| Status | Example | Problem |
|---|---|---|
| MISSING | (blank) | nothing to review |
| BOILERPLATE | "timing", "in line with expectations", "various" | names a category, not a cause |
| NO_DRIVER | "Higher charges" | says it moved, not why or by how much |
| NO_EVIDENCE | "Released 60k accrual" with no document | not corroborated (AS 2305 ¶.21) |
| OK | "Net new ARR 140k from 6 enterprise deals; churn -10k (2 logos); CRM export" | driver, amount, evidence |

A good explanation adds up: its drivers should roughly sum to the change. When
they do not, the remainder is the next question. 🔴

## Sources

1. PCAOB. *AS 2305: Substantive Analytical Procedures.* https://pcaobus.org/oversight/standards/auditing-standards/details/AS2305
2. PCAOB. *Proposal to replace AS 2305* (news release, June 2024). https://pcaobus.org/news-events/news-releases/news-release-detail/pcaob-continues-its-modernization-drive-with-proposal-to-replace-outdated-standard-on-substantive-analytical-procedures
3. PCAOB. *Staff Audit Practice Alert No. 11.* https://pcaobus.org/Standards/QandA/10-24-2013_SAPA_11.pdf
4. Analytical procedures (AU-C 520 / ISA 520 overview). https://en.wikipedia.org/wiki/Analytical_procedures_(finance_auditing)
5. Vena Solutions. *Flux analysis in accounting* (vendor). https://www.venasolutions.com/blog/flux-analysis-accounting
6. Corporate Finance Institute. *Materiality threshold in audits.* https://corporatefinanceinstitute.com/learn/resources/accounting/materiality-threshold-in-audits
