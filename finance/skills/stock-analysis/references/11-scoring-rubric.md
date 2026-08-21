# The Sector-Relative Multi-Factor Scoring Rubric

Use this when: you are at Stage 8, the analysis is done, and you need to convert a pile of evidence into a scorecard that a reader can argue with line by line.

A score is not a verdict; it is a disciplined summary of judgements you have already made and documented. Its value comes entirely from three properties: every metric is benchmarked against its own sector or the company's own record rather than a universal absolute, the weighting happens at the level of *categories* so no single ratio can dominate, and disqualifying findings cap or void the number instead of being averaged into it. Get any of those wrong and the composite becomes an authoritative-looking number that is confidently misleading — worse than publishing no score at all, because a number invites action in a way that prose does not.

## Contents

- [1. What the score is for, and what it is not](#1-what-the-score-is-for-and-what-it-is-not)
- [2. The eight categories, and why category weighting beats metric weighting](#2-the-eight-categories-and-why-category-weighting-beats-metric-weighting)
- [3. From a raw value to a sub-score: the 0–10 scale](#3-from-a-raw-value-to-a-sub-score-the-010-scale)
- [4. Choosing the benchmark: peer percentile, own history, sector band](#4-choosing-the-benchmark-peer-percentile-own-history-sector-band)
- [5. Sector-relative in practice: one metric, three sectors](#5-sector-relative-in-practice-one-metric-three-sectors)
- [6. Gates: findings that cap or void rather than average](#6-gates-findings-that-cap-or-void-rather-than-average)
- [7. Missing data, coverage, and the honesty of an incomplete score](#7-missing-data-coverage-and-the-honesty-of-an-incomplete-score)
- [8. Adjusting the weights to the investor's objective](#8-adjusting-the-weights-to-the-investors-objective)
- [9. Running the scorer](#9-running-the-scorer)
- [10. Multi-segment companies](#10-multi-segment-companies)
- [11. Worked example A — the lower-margin company scores higher](#11-worked-example-a--the-lower-margin-company-scores-higher)
- [12. Worked example B — a gate overrides a strong scorecard](#12-worked-example-b--a-gate-overrides-a-strong-scorecard)
- [13. Worked example C — renormalisation when data is missing](#13-worked-example-c--renormalisation-when-data-is-missing)
- [14. Interpreting a composite](#14-interpreting-a-composite)
- [15. The limits of scoring](#15-the-limits-of-scoring)
- [16. What goes in the report](#16-what-goes-in-the-report)
- [Checklist](#checklist)

**Every band quoted in this file and in `scripts/benchmarks.json` is indicative only.** Benchmark levels move with market, sector, cycle, accounting regime, interest rates and period. A peer-set percentile or the company's own multi-year record overrides any absolute band printed anywhere in this skill. Treat an unedited benchmark file as a first draft and say so in the report.

---

## 1. What the score is for, and what it is not

The scorecard does three jobs:

1. **It forces completeness.** Eight categories must each be addressed or explicitly marked missing, so a great story about a moat cannot quietly substitute for a look at the balance sheet.
2. **It makes disagreement cheap.** Because every metric shows its raw value, its benchmark band, its sub-score and its weight, a reader who thinks the ROCE band is wrong for this sector can dispute *that one line* rather than rejecting the whole analysis. This is the single most important property of the output.
3. **It resists the single-metric reflex.** "Y has a 30% margin and X has 20%, so Y is better" is the error this whole skill exists to prevent. A category-weighted composite makes that inference structurally impossible.

It does **not** do these jobs, and the report must not imply otherwise: it is not a prediction of returns, not a recommendation, not a substitute for the written thesis, and not comparable across analysts who used different weights or edited the bands differently. A composite quoted without its weight vector, its coverage and its as-of date is not a reproducible number.

---

## 2. The eight categories, and why category weighting beats metric weighting

| Category | Default weight | What it answers |
|---|---|---|
| Business quality & moat | 15% | Are the economics structurally defensible, and is the advantage widening or decaying? |
| Profitability & returns on capital | 20% | What does the business earn on the money tied up in it? |
| Earnings quality & cash conversion | 15% | Does reported profit become cash? |
| Balance sheet & solvency | 12% | Does it survive a bad two years? |
| Growth & reinvestment | 12% | Is there somewhere to put the next rupee or dollar at the same return? |
| Governance & management | 10% | Who controls the cash flows, and do minority owners get their share? |
| Valuation & margin of safety | 10% | What does the price already assume? |
| Risk | 6% | What could invalidate the thesis regardless of the fundamentals? |

**Why weight categories and not metrics.** Financial data is not evenly distributed across the things that matter. Any sector's metric set contains a dozen ways to measure profitability and perhaps three ways to measure governance, because profitability is easy to compute and governance is not. Average the metrics flat and the composite silently becomes 60–70% a profitability score with a governance rounding error attached — the exact failure this skill exists to prevent, reproduced one level up. Weighting by category fixes the *importance* of each dimension in advance, then lets each dimension use however many metrics the data supports. Within a category, individual metric weights (1.0 default, up to 2.5 for the decisive ones) express relative evidential value, not importance to the thesis.

**Why these eight and not more.** They are close to independent. Adding a ninth category that overlaps an existing one double-counts the same fact — a common way scorecards get quietly captured by whatever is easiest to measure.

---

## 3. From a raw value to a sub-score: the 0–10 scale

Each metric maps onto 0–10 through four anchors defined in the sector's benchmark entry:

| Anchor | Sub-score | Meaning |
|---|---|---|
| poor | 2.5 | Bottom of the sector's plausible range; a real weakness |
| average | 5.0 | Unremarkable for this sector, this cycle |
| good | 7.5 | Clearly better than the sector's middle |
| excellent | 10.0 | Best-in-sector territory |

Values between anchors interpolate linearly. Beyond *excellent* the score clamps at 10 — a company twice as good as excellent is not 20/10, and letting one heroic number run away would recreate single-metric dominance. Below *poor* the score falls linearly to 0 over one further band width, so a catastrophic reading is distinguished from a merely weak one.

Three metric shapes exist:

- **higher_better / lower_better** — the usual directional metrics.
- **band** — metrics where *both* extremes are bad, scored 10 inside the excellent interval and tapering outward. Use it for advertising spend (cutting it buys a year of margin and loses a decade of brand), R&D intensity, loan or AUM growth (a lender growing at 3x the system is buying share with credit standards), capex/depreciation, current ratio, effective tax rate, and NBFC leverage. Any metric where you would be uneasy about the top decile belongs here.
- **judgement** — qualitative factors (moat width, capital allocation record, disclosure quality, regulatory exposure) that the analyst scores 0–10 directly. These are not a loophole. Each one requires a written justification tied to evidence, and the scorer warns when a judgement score arrives without one. A judgement metric with no note is an opinion dressed as a measurement.

Judgement metrics are always oriented so **10 = good for the owner**. A risk metric scored 8 means low risk, not high risk.

---

## 4. Choosing the benchmark: peer percentile, own history, sector band

Precedence, strongest first:

**1. Peer percentile.** If you have a defensible peer set (built per `references/10-peer-set.md`, normalised for accounting regime and fiscal calendar), pass the peers' values and score the company on where it sits among them. This is the best available benchmark because it controls for cycle, geography, accounting and market conditions simultaneously — all the things a shipped band cannot know. Three comparable peers is the practical minimum; below that, percentiles are noise.

**2. Own history.** Where the peer set is weak — a company with no true comparables, a conglomerate, a market with three listed players — score the company against its own median over 5–10 years. Anchors sit at 0.85× / 1.00× / 1.15× / 1.30× the own median for higher-is-better metrics, inverted for lower-is-better. This answers "is this company getting better or worse", which no cross-sectional band can, and it is immune to sector-wide band error. It cannot detect a company that has been consistently mediocre, so never use it alone.

**3. Sector band.** The shipped default in `scripts/benchmarks.json`. Adequate for a first pass and for sectors where the dispersion is well understood. Edit it whenever you have better information for the specific market and period, and say in the report that you did.

State the basis used for each metric in the output — the scorer prints it in the `Basis` column. A reader who does not know whether 8.3/10 came from a peer set or from a shipped default cannot evaluate the claim.

---

## 5. Sector-relative in practice: one metric, three sectors

The same operating margin, scored against three sectors' bands from the shipped benchmark file:

| Sector | poor / average / good / excellent | 4% margin scores | 20% margin scores | 30% margin scores |
|---|---|---|---|---|
| Retail & e-commerce | 2 / 5 / 9 / 14 | **4.2** | 10.0 | 10.0 |
| Generic operating company | 6 / 12 / 18 / 26 | 1.7 | **8.1** | 10.0 |
| IT services & SaaS | 10 / 18 / 25 / 35 | 0.6 | **5.7** | **8.8** |

A 20% margin is exceptional in retail, good-to-strong in a generic industrial, and merely average in software. Scoring all three against one band would rank business models, not businesses. The same logic applies to every metric with a sector override: ROCE (asset-light branded consumer routinely earns 40%+, telecom rarely exceeds 15%), net debt/EBITDA (a regulated utility at 4x is normal, a cyclical at 4x is fragile), P/E (30× for a staple is not the same signal as 30× for a miner at the top of the cycle), and customer concentration (structurally extreme in semiconductors, alarming in FMCG).

Sectors where the *entire metric set* changes rather than just the bands — because the standard ratios are undefined or inverted — are banks, NBFCs, insurers and REITs. Those use standalone sets: NIM, GNPA/NPL, PCR, CAR/CET1, ROA and cost-to-income for banks; ALM gap, credit cost and CRAR for NBFCs; VNB margin, ROEV and combined ratio for insurers; AFFO, occupancy, LTV and the cap-rate-to-cost-of-debt spread for REITs. Miners and other commodity producers keep the generic frame but score cost-curve position, reserve life and *mid-cycle* ROCE, because spot-price ROCE peaks exactly when the shares are most dangerous.

---

## 6. Gates: findings that cap or void rather than average

Some findings are not evidence to be weighed. They are statements that the weighing exercise does not apply.

**Why averaging is the wrong operation.** A composite summarises a distribution of ordinary evidence, on the implicit assumption that the numbers being summarised are *true* and that the entity being scored will *continue to exist*. A going-concern paragraph attacks the second assumption; an auditor's qualification, a forensic audit or three years of cash flow running at half of reported profit attack the first. Blending such a finding into an average produces the absurd arithmetic where a superb ROCE, a fortress balance sheet and a cheap multiple "outvote" the auditor. In a flat average, scoring a single governance metric 0/10 inside a 10%-weighted category typically moves the composite by about two tenths — visually indistinguishable from a good company having a mediocre quarter. That is precisely the error pattern behind every scorecard that rated a fraud highly right up until the disclosure.

So gates operate *outside* the arithmetic:

| Severity | Effect | Examples |
|---|---|---|
| **Veto** | Composite is withheld entirely; verdict reads DISQUALIFIED | Going-concern material uncertainty; adverse or disclaimer audit opinion; active fraud/forensic investigation or regulator enforcement on the accounts; payment default, rating at D, or an unwaived covenant breach |
| **Cap 4.0–4.5** | Composite cannot exceed the cap | Qualified audit opinion; auditor resignation mid-term; **[India]** >50% of promoter holding pledged; cumulative CFO below 50% of cumulative PAT over 3+ years; material unexplained related-party leakage |
| **Cap 5.0–6.5** | Composite cannot exceed the cap | Material restatement; opaque group structure or unconsolidated material subsidiaries; receivables/unbilled growing far faster than sales for 2+ years; **[India]** 25–50% promoter pledging or pledging rising; **[India]** exchange surveillance (ASM/GSM) or a SEBI restraint order; compromised board/audit-committee independence; serial dilution at or below book; the analyst being unable to explain the revenue model or the key accounting judgement |

Notes on use:

- **A veto is not a score of zero.** It is a refusal to score. Report the finding prominently and early, state what would resolve it (a clean subsequent audit opinion, the forensic report, a completed refinancing), and re-run afterwards.
- **Raise a gate on evidence, not on suspicion.** Each gate in `benchmarks.json` carries an `evidence_needed` field naming the document that settles it: the auditor's report opinion paragraph, the Basis for Qualified Opinion, the quarterly shareholding pattern's encumbrance table **[India]**, an Item 4.01 or 4.02 8-K **[US]**, the rating rationale, the five-year cash flow statements.
- **Distinguish "cleared" from "not checked".** The scorer prints "GATES: none raised" either way. Say in the report which gate checks you actually performed. An unperformed check is not a pass.
- **The cap is a ceiling, not a target.** A capped composite of 4.0 does not mean the business is worth 4.0; it means no evidence can raise it above 4.0 while the finding stands.

---

## 7. Missing data, coverage, and the honesty of an incomplete score

Missing metrics are **dropped**, and the remaining category weights are **renormalised to 1.0**. They are never scored as zero.

Scoring absence as failure would mean an under-disclosing company reads as fraudulent and a fully transparent one reads as risky, which inverts the signal you actually want. It also creates a perverse incentive in the analysis itself: the easiest way to raise a score would be to stop looking for hard-to-find numbers.

What is reported instead:

- **Category coverage** — the share of total category weight carried by categories with at least one scored metric.
- **Metric coverage** — the share of the sector's total metric weight actually scored.
- **Per-category coverage** — so a category resting on one metric out of eight is visible as fragile.

**The confidence rule.** The composite is marked `** INDICATIVE ONLY **` when category coverage falls below the floor (default 70%) *or* when any category weighted 10% or more has no data at all. Both conditions matter: 85% coverage with governance entirely empty is not a scoreable company, it is a company you have not finished analysing. When the composite is indicative, say so in the report, name the empty categories, and state what data would close the gap.

Where you have a strong qualitative view but no metrics — governance on a company with three years of listed history, say — you may set a category score directly. The output marks it `[MANUAL OVERRIDE]`. Use this sparingly and always with a written justification; it is the one place where the scorecard's discipline can be bypassed.

---

## 8. Adjusting the weights to the investor's objective

Weights are a statement of what the reader cares about, not a fact about the company. Change them deliberately, and always print them.

| Preset | Bias | Use when |
|---|---|---|
| `default` | Balanced quality and price | No stated objective |
| `quality_compounder` | Business quality 22%, profitability 22%, valuation 5% | Long-hold compounding mandate that accepts a full price for durability |
| `deep_value` | Valuation 24%, balance sheet 20%, growth 4% | Asset- or price-led approach where survival and discount dominate |
| `income` | Earnings quality 22%, balance sheet 20%, growth 4% | Distribution durability is the objective |
| `forensic` | Earnings quality 26%, governance 26%, valuation 4% | A company you already distrust — use *with* the gates, never instead of them |

Sector defaults already shift weights where the sector demands it: banks and NBFCs raise balance sheet to 18–20% because capital adequacy and ALM decide survival; holdcos raise governance to 20% because the entire question is whether subsidiary value ever reaches the parent's shareholders; shipping and metals raise valuation and balance sheet because entry price and leverage, not operating skill, decide cyclical outcomes; IT/SaaS raises growth and business quality and cuts balance sheet to 6% because a net-cash software company's solvency is not the interesting question.

Two rules: **change weights before you see the scores, not after** (post-hoc weight tuning is how a scorecard becomes a rationalisation), and **run the alternative weighting as a sensitivity**. If a company scores 7.4 on quality-compounder weights and 5.1 on deep-value weights, that gap *is* the finding — it says the thesis depends entirely on paying up for durability, and the report should say so.

---

## 9. Running the scorer

`scripts/score.py` does the arithmetic. Standard library only.

```
python scripts/score.py --example > input.json     # starter input, edit it
python scripts/score.py input.json                 # readable scorecard
python scripts/score.py input.json --json          # same numbers, machine-readable
python scripts/score.py --list-sectors             # the 21 sector keys
python scripts/score.py --explain                  # the method
python scripts/score.py --explain gates            # every gate, with evidence required
python scripts/score.py --explain roce_pct --sector fmcg-consumer
python scripts/score.py input.json --preset deep_value --weight risk=0.10
python scripts/score.py --example-segments > seg.json   # multi-segment starter file
python scripts/score.py seg.json --segment-detail        # per-segment + blended group score
```

Input is one JSON object: `sector`, `metrics`, optional `flags`, optional `overrides`. A metric value can be a bare number or an object carrying the workings:

```json
"roce_pct": {"value": 22.4, "source": "FY25 AR consolidated", "period": "FY25"},
"sssg_pct": {"value": 9.0, "peer_values": [3.0, 4.5, 6.0, 11.0]},
"net_debt_to_ebitda": {"value": 0.4, "own_history": [1.8, 1.4, 1.1, 0.7], "basis": "own_history"}
```

Overrides let you narrow a band to your actual peer set (`overrides.thresholds`), change category weights, disable a metric that does not apply, or set a category score by hand. An unknown sector key falls back to the generic set with a loud warning — never accept that silently for a bank, NBFC, insurer or REIT, where the generic ratios are meaningless.

---

## 10. Multi-segment companies

A single sector key is wrong for a company that is 55% EPC, 30% IT services and 15% lending. Scoring the group against one set of bands benchmarks 45% of its profit against a sector it does not operate in, which is the precise error this whole rubric exists to prevent, committed one level up. The routing rules in `references/sectors/_index.md` (Step 3) already require per-segment analysis and sum-of-the-parts; the scorer makes it mechanical.

**Input shape.** Add a top-level `segments` array. It is auto-detected — with no `segments` key nothing about single-sector behaviour changes.

```json
{
  "company": "Example Diversified Industries Ltd",
  "as_of": "2026-07-22",
  "basis": "consolidated",
  "weight_basis": "ebit",
  "flags": {"opaque_structure": {"present": true, "evidence": "FY25 AR note 41"}},
  "segments": [
    {"name": "EPC & capital goods", "sector": "infra-capitalgoods",
     "ebit": 12000, "capital_employed": 60000, "revenue": 150000,
     "metrics": {"roce_pct": 16.5, "…": 0},
     "flags": {"receivables_blowout": {"present": true, "evidence": "…"}}},
    {"name": "Lending arm", "sector": "nbfc",
     "ebit": 4000, "capital_employed": 28000, "revenue": 9000,
     "metrics": {"roa_pct": 2.2, "nim_pct": 6.4, "…": 0}}
  ]
}
```

`python scripts/score.py --example-segments` prints a complete, runnable three-segment example (industrial + IT + lending). Each segment is scored against **its own sector's** metric set, bands and category weights by the ordinary scoring machinery; only the finished composites are blended. Raw metrics are never blended across segments — an NBFC's NIM and an EPC contractor's order book are not commensurable quantities, and averaging them would be arithmetic without meaning.

**Weighting.** `--weight-basis {ebit,capital_employed,revenue,explicit}`, default `ebit`, overriding `weight_basis` in the input. EBIT is the default because profit mix, not revenue mix, is what the owner owns: a trading segment can be 60% of revenue and 5% of profit. `explicit` reads a `weight` field per segment and normalises it to 1.0.

**The negative-EBIT rule.** If *any* segment has EBIT at or below zero, EBIT weighting is refused outright and the scorer falls back automatically — to `capital_employed` if every segment supplies it, otherwise `revenue`, otherwise equal weights — printing a prominent warning that names the fallback and the reason. This is not fussiness about a rounding case. A negative weight does not down-weight a bad segment, it *subtracts* that segment's score from the group, so a business burning capital would mechanically raise the composite; and where losses roughly offset profits the denominator approaches zero and every weight explodes. The same positivity test is applied to whichever basis is chosen, so a zero or negative capital-employed figure is rejected the same way. Weights are never negative and never sum to zero.

**A loss-making segment is reported prominently regardless of its weight**, flagged on its own row in the summary table and again in the diagnostics with the capital employed there and that capital's share of the group. The analytical point is that a segment destroying capital deserves attention in proportion to the *capital at risk*, not to the small weight a loss earns it in a blend. Say what capital sits there, what the group intends to do with it, and how the composite moves if it is closed, sold or fixed.

**Diagnostics printed with every segmented run:**

- **Concentration.** The mix, and the largest segment's share. Above 60%, that segment's playbook governs the analysis and the others are adjustments to it. If *no* segment reaches 40%, the company is a de facto conglomerate: run it through `references/sectors/holdco-assetmgr.md` as well and value it sum-of-the-parts.
- **Mixed families.** When the group spans a financial sector (`banks`, `nbfc`, `insurance`) and a non-financial one, the consolidated ratios are contaminated and must not be read at face value. The lending arm's loan-book growth sits inside consolidated operating cash flow, so group cash conversion measures disbursement rather than cash generation; and the lender's borrowings — its raw material, not its financing — inflate group debt/equity and net debt/EBITDA to levels that mean nothing. Use each segment's own metric set, and value the group sum-of-the-parts.
- **Valuation caveat**, printed every time: the blended composite scores quality across the group. It is not a valuation and it never substitutes for SOTP. Never apply a single consolidated multiple across a mixed group.

**Gates.** Group-level `flags` cap or void the blended composite exactly as in single-sector mode. Segment-level `flags` bind that segment's own composite, and the capped number is what enters the blend — segment caps are not applied twice. But **any segment gate of severity `veto` escalates to the group** and withholds the group composite. A fraud investigation, an adverse opinion or a going-concern paragraph in one segment does not stay inside that segment: the numbers are consolidated into the group accounts, certified by the same auditor and signed by the same board. Blending a vetoed segment away at 15% weight would convert "we cannot believe these accounts" into a two-tenths deduction. The output labels every raised gate with the level it came from.

**Coverage** is reported per segment and as a weighted group figure, checked against the same `--min-coverage` floor. A segment that could not be scored at all is dropped from the blend and the remaining weights renormalised, with the share of the weight base actually covered printed alongside the number — the same discipline applied to missing metrics, one level up.

`--segment-detail` prints each segment's full scorecard below the group summary, which is what you reproduce in the report when a segment is doing the work. `--json` emits the group blend with every segment's complete result nested inside.

**The blended composite never replaces sum-of-the-parts valuation.** It is a quality summary, weighted by size. Valuation of a mixed group is done segment by segment on each family's own basis — the lender on P/B or P/adjusted book, the brand on EV/EBITDA or P/E, property on NAV — net of holding-company debt and capitalised holdco costs, with a holding discount where the segments are not separately monetisable. A group composite quoted as though it were a valuation conclusion is a misuse of the tool.

---

## 11. Worked example A — the lower-margin company scores higher

Two illustrative companies, generic and hypothetical. **Distributor A**: 4% operating margin, negative working capital, high asset turnover. **Software B**: 30% operating margin, net cash, heavy stock-based compensation. Scored on their own sectors' bands and sector weights.

Metric level, showing the margin metric doing the opposite of what the composite does:

| Metric | Distributor A | sub-score | Software B | sub-score |
|---|---|---|---|---|
| Operating margin | 4.0% (band 2/5/9/14) | 4.2 | 30% (band 10/18/25/35) | **8.8** |
| ROCE | 26% (band 8/14/22/35) | **8.3** | 24% (band 15/25/35/50) | 4.8 |
| ROIIC | 24% | **9.0** | 13% | 5.4 |
| Cash conversion cycle | −20 days | 9.0 | +40 days | 7.1 |
| FCF margin | 2.0% | 3.8 | 12.0% | **8.9** |
| SBC / revenue | not applicable | — | 14% | 4.4 |
| 5y dilution | +2% | 7.8 | +18% | 4.7 |
| P/E | 34× (band 90/60/40/28) | **8.8** | 42× (band 60/38/25/17) | 4.6 |
| Reverse-DCF growth gap | +1.0pp | 6.7 | +4.0pp | 4.5 |

Category level:

| Category | Distributor A | Software B |
|---|---|---|
| Business quality & moat | 5.9 | 5.6 |
| Profitability & returns | 7.6 | 7.4 |
| Earnings quality | 6.9 | 6.5 |
| Balance sheet | 9.2 | 9.4 |
| Growth & reinvestment | 8.0 | 5.8 |
| Governance | 7.9 | 7.2 |
| Valuation | 6.4 | 4.3 |
| Risk | 5.5 | 5.8 |
| **Composite** | **7.14 — Above average** | **6.30 — Average** |

Software B wins the margin comparison decisively — 8.8 against 4.2 — and still loses the composite. Three mechanisms produce that, and each is a real economic fact rather than a scoring artefact:

1. **Sector-relative bands neutralise the structural margin gap.** 4% is strong for a distributor; 30% is unremarkable for software. The margin difference was never information about quality.
2. **Return on capital, not margin, is what compounds.** Distributor A converts a thin margin into 26% ROCE through turnover and supplier-funded working capital, and reinvests at 24% incremental returns. Software B's high margin sits on a capital base that earns less than its sector's median, and its incremental returns are half the distributor's.
3. **Per-share and price effects.** Software B's 18% five-year dilution and 14% SBC mean the owner captures less of the profit than the income statement implies, and it is priced 4pp of growth above what the analysis can defend.

If Distributor A's numbers had come with three years of CFO at half of PAT, the cash-flow divergence gate would cap the composite at 4.0 and the entire comparison above would become irrelevant. That is the intended behaviour.

---

## 12. Worked example B — a gate overrides a strong scorecard

An illustrative company scores well across the board: profitability 8.1, earnings quality 7.4, balance sheet 7.9, growth 7.7, valuation 6.2 — a pre-gate composite around 7.6, comfortably "Strong". Then the shareholding pattern shows 62% of promoter holding pledged, up from 31% two years ago.

- **Flat-average treatment**: promoter pledging is one governance metric at weight 2.0 inside a 10% category. Scoring it 0 instead of 10 moves the composite by 0.22 — from roughly 7.6 to roughly 7.4. The reader sees a strong company with a slight governance blemish.
- **Gate treatment**: composite capped at 4.0, printed with the pre-gate figure alongside so nothing is hidden, and the finding stated in the report's opening section.

The gate treatment is right because the mechanism is not gradual. Heavy pledging couples the share price to control: a price fall triggers margin calls, invoked shares and forced selling, which drives a further fall. That reflexive loop is independent of business quality and has repeatedly destroyed operationally sound companies. Averaging spreads a step-function risk across a continuous scale and makes it disappear. **[India]** This gate is India-specific in its data source — the encumbrance table in the quarterly shareholding pattern — but the underlying risk exists anywhere insiders have pledged control blocks; in US filings, look for margin-loan disclosure in the proxy and Schedule 13D/G footnotes.

---

## 13. Worked example C — renormalisation when data is missing

A recently listed company: no governance history worth scoring and no reliable multi-year growth series. Six of eight categories carry data.

| Category | Default weight | Score | Renormalised weight | Contribution |
|---|---|---|---|---|
| Business quality | 15% | 6.0 | 19.2% | 1.15 |
| Profitability | 20% | 8.0 | 25.6% | 2.05 |
| Earnings quality | 15% | 7.0 | 19.2% | 1.34 |
| Balance sheet | 12% | 6.5 | 15.4% | 1.00 |
| Growth | 12% | *no data* | dropped | — |
| Governance | 10% | *no data* | dropped | — |
| Valuation | 10% | 5.0 | 12.8% | 0.64 |
| Risk | 6% | 6.0 | 7.7% | 0.46 |
| **Composite** | | | **100%** | **6.65 — INDICATIVE ONLY** |

Category coverage is 78%, above the 70% floor — but governance carries a default weight of 10%, so the empty-major-category rule fires and the composite is marked indicative. That is the correct outcome: a company whose governance you have not assessed is not a 6.65, it is an unfinished analysis.

Had the two missing categories been scored 0 instead of dropped, the composite would read **5.19** — a full grade lower, and lower purely because of what the analyst could not find. The report would then be describing the state of the data as though it were the state of the business.

---

## 14. Interpreting a composite

| Composite | Grade | What it means in practice |
|---|---|---|
| 8.5–10 | Exceptional | Best-in-sector on most dimensions with a defensible price. Rare; re-check the inputs and the peer set before believing it. |
| 7.5–8.4 | Strong | Clear quality with no disqualifying weakness. Usually the top of a realistic range. |
| 6.5–7.4 | Above average | Good business, or a very good business at a full price. Read the category spread. |
| 5.5–6.4 | Average | Unremarkable, or excellent on some dimensions and weak on others. The spread matters more than the number. |
| 4.5–5.4 | Below average | Something material is wrong — usually returns, cash conversion or price. |
| 3.5–4.4 | Weak | Multiple failing dimensions, or a gate has capped it. |
| Below 3.5 | Poor | Avoid, or a special-situation case that this framework does not price. |
| Withheld | Disqualified | A veto gate is open. Not a low score — a refusal to score. |

**Read the spread, not just the level.** A 6.5 built from eight scores between 6 and 7 is a genuinely average business. A 6.5 built from profitability 9.5 and governance 3.0 is a completely different object: a strong business with a control problem, where the whole question is whether the owner ever receives the economics. The composite is identical; the investment case is not. Always show the category table, never the composite alone.

**Small differences are noise.** The difference between 6.8 and 7.1 is well inside the error of the bands, the estimates and the judgement scores. Treat gaps under roughly 0.5 as indistinguishable. Never rank a portfolio by composite to two decimals.

---

## 15. The limits of scoring

- **Garbage in, precision out.** The scorecard cannot detect a fabricated input. It will format a hallucinated ROCE to two decimals as readily as a sourced one. This is why `SKILL.md` treats "never invent a number" as the primary non-negotiable.
- **It cannot see what is not in it.** A technology shift that will halve demand in four years, a founder about to leave, a regulator drafting a rule — none of these appear unless you encode them in a judgement metric. The judgement metrics exist precisely as the entry point for what the ratios cannot see, and they are the least reliable part of the output.
- **Bands embed a period.** Thresholds calibrated in a low-rate decade misprice a high-rate one, especially in valuation and balance sheet. Re-derive from live peer data whenever you can.
- **Judgement scores can be reverse-engineered.** If you set the moat score after seeing that the composite came out lower than your prior, you have written down your prior with extra steps. Score judgement metrics before running the totals.
- **It is not comparable across analysts.** Different weights, edited bands and different judgement calibration make two composites incomparable unless both scorecards are shown in full.
- **It does not price a special situation.** Deep cyclicals at cycle extremes, turnarounds, pre-revenue businesses, holdcos trading at persistent discounts and companies in restructuring need `references/13-situations.md`, not a composite. Score them if it helps structure the evidence, but lead the report with the situation logic.
- **It says nothing about fit.** Position size, horizon, tax, currency and concentration are the user's, not the company's. Producing analysis, not advice, is a hard boundary of this skill.

---

## 16. What goes in the report

Reproduce, at minimum:

1. The **composite and grade**, with the pre-gate figure shown separately if a gate bound.
2. The **category table** — score, default weight, renormalised weight, contribution.
3. The **per-metric workings** for at least the decisive metrics — raw value, basis used (peer / own history / sector band), the band itself, the sub-score.
4. The **weights and preset** used, and any band overrides you applied, with the reason.
5. **Coverage**, the missing categories, and what data would close the gap.
6. **Gates**: which were raised, which were checked and cleared, and which were not checked.
7. The line that every scorecard needs: bands are indicative, peer and own-history comparison override them, and this is research rather than advice.

---

## Checklist

- [ ] Sector key chosen deliberately; banks / NBFCs / insurers / REITs use their standalone metric sets, never the generic one.
- [ ] Multi-segment companies scored per segment against each segment's own sector, weighted by profit (or by capital employed where a segment loses money), with the blend never presented as a valuation — SOTP done separately.
- [ ] Bands edited to the actual peer set and period where better data exists, and the edit disclosed.
- [ ] Peer percentile used where 3+ comparable peers exist; own-history basis used where the peer set is weak.
- [ ] Every judgement metric carries a written, evidence-linked justification.
- [ ] Judgement scores set before the totals were computed, not after.
- [ ] Category weights chosen for the stated objective, fixed before scoring, and printed in the output.
- [ ] Sensitivity run under a second weight preset; any large gap reported as a finding.
- [ ] All gate checks explicitly performed; raised gates evidenced by a named document, not an impression.
- [ ] Veto findings reported early and prominently, with the composite withheld rather than lowered.
- [ ] Missing metrics dropped and weights renormalised — never scored as zero.
- [ ] Coverage reported; composite marked INDICATIVE ONLY below the floor or with an empty major category.
- [ ] Category spread discussed, not just the composite level.
- [ ] Differences under ~0.5 treated as noise; no ranking to two decimals.
- [ ] Every number in the input carries a source and a period; nothing recalled or estimated without being labelled.
- [ ] Report states plainly that this is research, not licensed financial advice.
