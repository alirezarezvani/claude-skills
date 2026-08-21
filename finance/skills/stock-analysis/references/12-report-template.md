# Report Template — Final Output Structure

Use this when: you have finished the analytical work and are assembling the deliverable, or you are in screen mode and need the short form.

The report is where an analysis either survives contact with a reader or dies. A reader who stops after one screen must still receive the verdict, the reasoning that drives it, and the risks that would break it. Every number you print must carry its provenance — the reader cannot check your arithmetic if they cannot find your inputs, and an unsourced number is indistinguishable from a hallucinated one. Structure is not decoration here: the ordering below front-loads conclusions and pushes supporting evidence down, so the report degrades gracefully when read partially.

## Contents

- [Non-negotiables](#non-negotiables)
- [Formatting conventions](#formatting-conventions)
- [Full report template](#full-report-template)
- [Short-form variant (screen mode)](#short-form-variant-screen-mode)
- [Common failure modes in report writing](#common-failure-modes-in-report-writing)
- [Checklist](#checklist)

---

## Non-negotiables

Four rules govern every section below. They come from the skill's governing principle: a metric is meaningless until you know its sector and the company's own history.

1. **Never print a bare metric.** Every ratio appears with at least one of: the peer-set median, the company's own 3–5 year range, or both. `ROCE 18%` is noise. `ROCE 18% (own 5y range 12–19%; peer median 15%)` is information.
2. **Never rank on a single metric.** If the report contains a ranking of any kind, it must be composite and the weights must be visible.
3. **State the sector playbook explicitly** and say which standard ratios you suppressed because they are undefined or inverted for that sector. Banks, insurers, REITs, miners, and asset-heavy utilities all break at least one default ratio. Silence here reads as an error.
4. **Mark every estimate.** A derived, interpolated, annualised, or eyeballed number is not the same class of object as a reported one, and the reader must be able to tell at a glance.

---

## Formatting conventions

Apply these consistently. They are what make the report auditable.

### Showing a number with its source

Inline form, for prose and table cells:

```
₹4,812 cr [FY25 AR, Consolidated P&L, p.142]
18.4% [computed: EBIT 4,812 / (TA 34,100 − CL 8,050), FY25 AR]
$2.31 [10-K FY2024, Item 8, Consolidated Statements of Operations]
```

Rules:
- Source goes in square brackets immediately after the number.
- For computed metrics, show the formula with the inputs, not just the label. The reader must be able to reproduce the arithmetic without opening the filing.
- Cite the statement and page/item, not just the document. "FY25 AR" alone is a weak citation; "FY25 AR, Note 32, p.211" is a real one.
- India: cite the Annual Report, the quarterly results filing (NSE/BSE intimation), the concall transcript with date, or the CARO annexure by clause number. Say `Consolidated` or `Standalone` every time — they are different companies for analytical purposes.
- US/global: cite 10-K/10-Q by Item number, 20-F for foreign private issuers, 8-K by item, or the EDGAR accession number. Say GAAP or IFRS where the treatment differs (leases, R&D capitalisation, goodwill amortisation).
- Prices and market cap must carry an as-of date and time zone or close reference: `₹1,842 (NSE close, 2026-07-21)`.

### Marking estimates

Use a consistent marker and define it once in the Data Quality Note.

```
~14.2% (est.)   — derived or approximated by the analyst
[E]             — compact marker for table cells
[TTM]           — trailing twelve months, stitched from quarterlies; say which quarters
[Ann.]          — annualised from a partial period; state the periods used
[Adj.]          — analyst adjustment applied; the adjustment must be described in a footnote
```

Every `[E]` and `[Adj.]` needs a one-line note saying how it was produced and what would change if the assumption were wrong. An unexplained adjustment is worse than no adjustment, because it launders judgement as fact.

### Showing not-available

Never leave a cell blank and never substitute zero. Blank reads as an oversight; zero is an actual claim and usually a false one.

```
n/a — undefined for sector      (e.g. inventory turnover for a bank)
n/a — not disclosed             (company does not report the line)
n/a — not comparable            (peer uses different segment definition or accounting basis)
n/d — not yet determined        (you ran out of time or data; say so honestly)
```

`n/a — undefined for sector` is a *finding*, not a gap. It tells the reader you applied the right playbook.

### Units and scale

- India: state crore vs lakh explicitly in the column header (`₹ cr`). Never mix. If the source reports in ₹ lakh and you converted, mark the conversion.
- US/global: state `$ m` or `$ bn` in the header. For non-USD reporters, state the presentation currency and never silently FX-convert; if you do convert, give the rate and its date.
- Per-share figures: state whether basic or diluted, and whether the share count is period-end or weighted average.
- Percentages: one decimal is enough. More implies precision the inputs do not support.

---

## Full report template

Copy the structure below. Replace bracketed guidance; delete guidance lines that do not apply, but never delete a required heading — if a section is empty, say why.

````markdown
# [Company Name] ([EXCHANGE:TICKER]) — Equity Analysis

**Analysis date:** [YYYY-MM-DD]
**Basis:** [Consolidated / Standalone] · [Ind-AS / US GAAP / IFRS] · [Currency and scale, e.g. ₹ crore]
**Latest reported period:** [FY25 (Mar-2025) audited / Q1 FY26 (Jun-2025) unaudited / FY2024 10-K]
**Price reference:** [₹X,XXX, NSE close YYYY-MM-DD] · **Market cap:** [₹X,XXX cr] · **EV:** [₹X,XXX cr]

---

## RECENCY STATEMENT
Most recent reported period incorporated: <e.g. Q1 FY27, published DD-MMM-YYYY>
Events checked through: <date>
Material events since the last full-year data: <list, or "none found">
Any invalidation trigger already tripped at the time of writing: <yes + which, or no>

## DATA QUALITY NOTE

> Read this before the numbers. It defines what the numbers are.

| Item | Statement |
|---|---|
| **Primary sources** | [Annual Report FY25 (audited); Q4 FY25 results intimation; FY25 concall transcript dated YYYY-MM-DD; CARO FY25. / 10-K FY2024 filed YYYY-MM-DD; 10-Q Q1 FY2025; latest DEF 14A.] |
| **Secondary sources** | [Aggregator screens used, and for what — typically peer medians and price data only. Name them. Never source a fundamental from an aggregator when the filing is available.] |
| **As-of dates** | Financials as of [date]. Prices as of [date]. Shareholding as of [date]. Any data older than the latest reported period is flagged inline. |
| **Consolidated vs standalone** | [Consolidated used throughout. Standalone differs materially in X because of Y — noted where relevant.] India: if subsidiaries or JVs are significant, consolidated is the only honest basis; say so. |
| **Currency and units** | [All figures in ₹ crore unless stated. 1 crore = 10 million. / All figures in $ millions.] [FX conversions, if any, at rate R as of date D.] |
| **What is estimated** | [List every `[E]`, `[TTM]`, `[Ann.]`, `[Adj.]` used, with the method in one line each. If none, say "No analyst estimates used."] |
| **What is missing** | [Segment-level capital employed not disclosed; related-party pricing not disclosed; peer X has not filed FY25 so FY24 used and marked. Be specific — "some data gaps" is not a disclosure.] |
| **Known accounting comparability issues** | [Lease treatment differs between company and peer set; one peer capitalises development cost, company expenses it; company changed revenue recognition in FY24. State the direction of the distortion.] |

---

## VERDICT AND KEY RISKS

**Verdict:** [One sentence. State the assessment and the confidence level. Example: "Fundamentally sound compounder trading at a valuation that already prices in continued mid-teens growth — quality high, margin of safety thin. Confidence: moderate-high on fundamentals, low on the valuation call."]

**Composite score:** [X.X / 10] · **Sector playbook applied:** [name] · **Situation flags:** [none / cyclical peak / turnaround / holding company / recent large acquisition]

**The three things that matter most:**
1. [Claim in one line, with the single number that supports it and its source.]
2. [ditto]
3. [ditto]

**Key risks — what could break this:**
1. **[Risk name]** — [What happens, how likely, what it does to earnings or the balance sheet. Quantify where you can: "a 200bps gross margin reversion takes EPS down ~18%".]
2. **[Risk name]** — [ditto]
3. **[Risk name]** — [ditto]

**What would change the verdict:** [One line pointing forward to the invalidation triggers section.]

---

## 1. The Business — What It Sells and How It Makes Money

[3–6 short paragraphs, or a table plus prose. Cover:]

- **What the customer actually buys, and why they pick this company.** Write it so a non-specialist understands. If you cannot explain the revenue model in three sentences, you do not yet understand it, and that is itself a finding.
- **Revenue build:** volume × price, or subscribers × ARPU, or AUM × yield, or loans × NIM. Show the actual driver decomposition, not just "sells products".
- **Revenue mix** by segment / geography / channel, with the share of each and the growth rate of each. Mix shift is usually the story.
- **Where the money leaks out:** the cost structure and its fixed/variable split, because that determines operating leverage in both directions.
- **The cash conversion path:** how long between spending and collecting. Working capital intensity is a structural feature of the business model, not an accounting detail.

---

## 2. Sector Classification and Playbook Applied

**Sector / sub-sector:** [e.g. Specialty chemicals — CDMO-weighted / Private sector bank / Equity REIT — office]
**Playbook applied:** [name of the playbook reference used]

**Why this classification:** [One paragraph. Companies often sit between sectors, or report under one classification while economically belonging to another. Justify the choice — it determines which metrics are valid.]

**Metrics suppressed as undefined or inverted for this sector:**

| Standard metric | Status here | Why |
|---|---|---|
| [e.g. Debt/Equity] | n/a — inverted | [For a bank, leverage is the business; assess CAR / CET1 instead.] |
| [e.g. EV/EBITDA] | n/a — undefined | [EV is not meaningful for a lender; deposits are operating liabilities, not debt.] |
| [e.g. Operating margin] | Use with care | [For a REIT, use NOI margin and FFO; depreciation is non-economic on appreciating property.] |

**Sector-specific metrics used instead:** [List, with the reason each is the right substitute.]

---

## 3. Situation Classification

[Include only if a special situation applies; if none, write "No special situation identified — analysed as a going-concern operating business."]

**Situation:** [Cyclical at/near peak · Turnaround · Deep value / possible value trap · Holding company with cross-holdings · Post-large-acquisition · Recent IPO with short history · Regulatory overhang · Promoter-pledge stress (India)]

**Implications for the analysis:** [What this changes. A cyclical at peak earnings must not be valued on peak-cycle P/E. A holding company needs a sum-of-the-parts with an explicit holdco discount. A turnaround needs the balance sheet weighted above the P&L. Say what you did differently.]

---

## 4. Scorecard

| Category | Score /10 | Weight | Weighted | One-line rationale |
|---|---:|---:|---:|---|
| Business quality & moat | [X] | [XX%] | [X.XX] | [why] |
| Earnings quality | [X] | [XX%] | [X.XX] | [why] |
| Balance sheet strength | [X] | [XX%] | [X.XX] | [why] |
| Cash flow | [X] | [XX%] | [X.XX] | [why] |
| Returns on capital | [X] | [XX%] | [X.XX] | [why] |
| Growth (quality & durability) | [X] | [XX%] | [X.XX] | [why] |
| Management & governance | [X] | [XX%] | [X.XX] | [why] |
| Valuation | [X] | [XX%] | [X.XX] | [why] |
| **Composite** | | **100%** | **[X.X]** | |

**Weighting rationale:** [State why these weights, for this sector. Weights are not universal — balance sheet carries more weight for a lender or a leveraged cyclical; moat and returns carry more for an asset-light compounder. If you used the playbook's default weights, say so.]

**Scoring basis:** [Scores are relative to the peer set and the company's own history, not to an absolute ideal. State the anchor: "6 = peer median, 8 = clearly above peer set on that dimension, 3 = materially below."]

---

## 5. Core Analysis by Dimension

Each sub-section: the numbers with sources, the trend over 3–5 years, the peer comparison, then the interpretation. Interpretation last — do not lead with your conclusion inside the evidence section.

### 5.1 Business Quality and Moat

[Evidence for or against durable advantage: pricing power (price realisation vs input cost trend), customer retention/churn, switching costs, scale economics, regulatory or distribution barriers, brand. The test of a moat is not that returns are high today; it is that returns stayed high while competitors were trying. Show the multi-year return series, not the latest year.]

### 5.2 Earnings Quality

| Metric | Value | Own 3–5y range | Peer median | Read |
|---|---|---|---|---|
| CFO / EBITDA | | | | |
| CFO / PAT | | | | |
| Accruals ratio | | | | |
| Other income / PBT | | | | |
| Effective tax rate vs statutory | | | | |
| Receivable days vs revenue growth | | | | |

[Interpretation. Flag: profit growing faster than cash, one-off gains embedded in "operating" profit, tax rate anomalies, revenue recognition changes, capitalised costs that peers expense. India: check related-party transactions and CARO clauses on statutory dues and fund diversion. US: check non-GAAP-to-GAAP reconciliation and what is being added back.]

### 5.3 Balance Sheet

[Leverage, maturity profile, covenants, contingent liabilities, off-balance-sheet items, working capital structure, goodwill and intangibles as % of net worth. India-specific: promoter pledge %, inter-corporate deposits, guarantees to group entities. For lenders: capital adequacy, NPA/stage-3 movement, provision coverage, restructured book — not D/E.]

### 5.4 Cash Flow

[CFO, capex split maintenance vs growth (say how you split it and that the split is an estimate), FCF, FCF conversion, and the multi-year cumulative FCF vs cumulative PAT. The cumulative test over a full cycle is more informative than any single year.]

### 5.5 Returns on Capital

[ROCE, ROIC, ROE with DuPont decomposition, incremental ROIC on capital deployed over the last 3–5 years. Incremental return is the one that predicts the future; the average return reflects capital deployed long ago. State the capital base definition you used and be consistent with peers.]

### 5.6 Growth

[Revenue, EBITDA, PAT, and per-share growth over 3, 5, 10 years where available. Separate organic from acquired. Separate volume from price. Growth funded by equity issuance is not the same as growth funded by internal cash — show share count over the period. State reinvestment rate and whether growth is consistent with returns × reinvestment.]

---

## 6. Peer Comparison

**Peer set:** [List each peer with ticker.]

**Why these peers:** [Justify explicitly. Peers must match on business model and economics, not merely on sector label or index membership. State what you excluded and why — "excluded X because 60% of its revenue is a different business", "excluded Y because it reports under a different accounting basis and is not comparable on margins". A weak peer set silently invalidates the entire relative analysis, so this justification is load-bearing.]

**Comparability caveats:** [Size differences, geographic mix, accounting differences, fiscal year-end differences. If fiscal years differ, say which periods you aligned.]

| Metric | [Company] | [Peer 1] | [Peer 2] | [Peer 3] | Peer median |
|---|---:|---:|---:|---:|---:|
| Revenue [₹ cr / $ m] | | | | | |
| Revenue CAGR 5y | | | | | |
| Gross margin | | | | | |
| EBITDA margin | | | | | |
| ROCE | | | | | |
| ROE | | | | | |
| Net debt / EBITDA | | | | | |
| CFO / EBITDA | | | | | |
| [Sector-specific metric] | | | | | |
| [Valuation multiple, sector-appropriate] | | | | | |

[Two or three paragraphs of interpretation. Where the company sits above or below the median, say whether the gap is structural (business model, mix, geography) or performance-driven. A structural gap should not be scored as skill; a performance gap should not be assumed permanent.]

---

## 7. Valuation

**Method used:** [e.g. Reverse-DCF cross-checked against EV/EBIT vs own history and peers]
**Why this method for this sector:** [Justify. DCF for predictable cash generators; P/B and ROE-based for lenders; FFO/AFFO and cap-rate/NAV for REITs; EV/EBITDA through-cycle or P/NAV and reserve life for miners; EV/Sales only where margins are not yet representative and only with an explicit path to margin. Say why the default multiple is inappropriate if you rejected it.]

**Key inputs:** [Discount rate and how derived; terminal growth; forecast horizon; tax rate; capex and working-capital assumptions. Every input gets a one-line justification. Do not import a discount rate as a convention — state the risk-free rate used and its date.]

### Reverse-DCF: what the current price implies

[State it as a sentence a reader can argue with: "At ₹X, the market is embedding roughly Y% revenue growth for N years at Z% EBIT margin, with terminal growth of T%." Then judge it: is that within what this company has actually delivered, and within what the industry can support? The reverse-DCF is the most useful single output in this section because it converts a price into a testable claim about the future.]

**Historical reality check:** [Company's actual 5y and 10y delivery against the implied figures. Industry-wide growth ceiling if relevant.]

### Scenario table

| Scenario | Probability | Key assumptions | Implied value / share | vs current price |
|---|---:|---|---:|---:|
| Bear | [XX%] | [growth, margin, multiple — 1 line] | [₹X] | [−XX%] |
| Base | [XX%] | | [₹X] | [±XX%] |
| Bull | [XX%] | | [₹X] | [+XX%] |
| **Probability-weighted** | 100% | | **[₹X]** | **[±XX%]** |

[Probabilities are judgements — say so, and say what drives them. A scenario table with a bear case that is not genuinely bad is a marketing document, not an analysis. The bear case should assume things you consider unlikely but possible, not merely slower growth.]

---

## 8. Red Flags and Governance

[List findings, most severe first. If none material, write "No material red flags identified" and list what you specifically checked — a clean bill of health is only credible if the reader knows what was tested.]

| # | Flag | Severity | Evidence [source] | Why it matters |
|---|---|---|---|---|
| 1 | | High/Med/Low | | |

Checked and clear: [enumerate — auditor changes, qualified opinions, related-party transactions, promoter pledge, contingent liabilities, frequent restatements, CFO/CEO turnover, dilution history, capital allocation record, subsidiary opacity.]

**India-specific checks:** promoter shareholding trend and pledge %, auditor resignation history, CARO qualifications by clause, SEBI/exchange actions, related-party approvals, royalty payments to promoter entities, concall responsiveness (management that dodges the same question across three calls is telling you something).

**US/global checks:** auditor opinion and any ICFR material weakness, restatements, insider selling patterns in Form 4, share-based compensation as % of revenue and its treatment in non-GAAP, buybacks at valuation peaks, board independence and related-party disclosures in the proxy.

---

## 9. The Bear Case

[Write this as though you were short the stock and had to defend the position. Not a list of generic risks — a coherent argument that the thesis is wrong. Cover: what the bull is assuming that may not hold; what would cause returns to mean-revert; which competitive, regulatory, technological, or cyclical force is being underweighted; and where the accounting could be flattering the picture.

If you cannot write a bear case that you find at least partly persuasive, you have not done the work. Say explicitly what the strongest counter-argument is and why you still net out where you do — but do not defang the bear case in the process of writing it. Keep the rebuttal separate and after.]

**Strongest counter to the bear case:** [1–2 sentences, kept honest.]

---

## 10. Thesis-Invalidation Triggers

Specific, observable, and time-bound. "Deteriorating fundamentals" is not a trigger. A trigger is something a reader could check in a future filing and get an unambiguous yes/no.

| # | Trigger | Where to observe | By when | Action if hit |
|---|---|---|---|---|
| 1 | [Gross margin falls below XX% for two consecutive quarters] | [Quarterly results / 10-Q] | [Q2–Q3 FY27] | [Revisit — thesis rests on pricing power] |
| 2 | [Net debt/EBITDA exceeds X.Xx] | [Half-year balance sheet] | [FY27] | [Downgrade balance sheet score] |
| 3 | [Promoter pledge rises above X% / insider selling exceeds X% of holding] | [Shareholding pattern / Form 4] | [any quarter] | [Governance re-review] |
| 4 | [Incremental ROIC on last 3y capital deployed falls below cost of capital] | [Annual report] | [FY27 AR] | [Growth is value-destructive — thesis fails] |
| 5 | [Named competitor / regulatory event] | [specific source] | [date] | [specific] |

---

## Disclaimer

This document is research and analysis produced for informational purposes only. It is **not** investment advice, not a recommendation to buy, sell, or hold any security, and not a personalised financial recommendation. The author is not a licensed or registered investment adviser. Figures are drawn from public filings and may contain errors of transcription, computation, or interpretation; items marked as estimates are the analyst's own and are not company-reported. Past performance and historical financial trends do not predict future results. Any investment decision is the reader's own responsibility and should be made in consultation with a licensed financial adviser who is aware of the reader's circumstances, objectives, and risk tolerance.
````

---

## Short-form variant (screen mode)

Use when the task is a screen across many names, a first-pass triage, or the user asked for a quick read. Target roughly one screen per company. Same provenance and estimate-marking rules apply — brevity does not license unsourced numbers.

````markdown
### [Company] ([EXCHANGE:TICKER]) — [Sector] — [Score X.X/10]

**Basis:** [Consolidated, Ind-AS, ₹ cr] · **Data:** [FY25 AR + Q1 FY26] · **Price:** [₹X,XXX, DD-MMM-YY]

**Verdict:** [One or two sentences: what it is, what the composite score reflects, and the single biggest reason to look closer or pass.]

| | Value | Peer med. | Own 5y |
|---|---:|---:|---:|
| [Sector-appropriate metric 1] | | | |
| [Sector-appropriate metric 2] | | | |
| [Sector-appropriate metric 3] | | | |
| [Valuation multiple] | | | |

**Playbook:** [name] · **Suppressed:** [metrics n/a for this sector]
**For:** [strongest positive, one line, with a number]
**Against:** [strongest negative, one line, with a number]
**Flags:** [red flags, or "none found in screen-level checks"]
**Data gaps:** [what a full analysis would need to resolve]
**Next step:** [Full analysis / Pass — reason / Watch, revisit at trigger X]

*Screen-level output. Research, not investment advice. Not a licensed adviser.*
````

Screen mode carries an extra obligation: state that it is screen-level. A short report that reads like a full one invites the reader to over-trust it.

---

## Common failure modes in report writing

Each of these has changed a reader's conclusion in the wrong direction. Check for them before finalising.

- **The buried verdict.** Conclusion appears on the third screen after a wall of tables. Fix: front-load.
- **The decorative bear case.** Bear section says "valuation could de-rate" and nothing else. Fix: make it argue.
- **The metric without a home.** A ratio printed with no peer or history anchor. Fix: never print bare.
- **The wrong-sector ratio.** D/E for a bank, P/E for a loss-making biotech, EV/EBITDA for a REIT. Fix: run the suppression table.
- **The laundered estimate.** An analyst assumption formatted identically to a reported figure. Fix: mark everything.
- **The convenient peer set.** Peers chosen so the company looks good. Fix: justify the set before you compute, not after you see the results.
- **The unfalsifiable trigger.** "Watch for execution issues." Fix: name the line item, the threshold, and the filing.
- **The precision illusion.** A DCF output to two decimals off inputs that are ±30%. Fix: round to the precision the inputs support and show the scenario range, not a point estimate.
- **The peak-cycle P/E.** Cyclical valued on peak earnings and a peak multiple. Fix: the situation classification section exists to catch this.
- **Score without weights.** Composite presented as authoritative with weighting hidden. Fix: weights and rationale always visible.

---

## Checklist

- [ ] Title carries company, ticker, date, basis (consolidated/standalone), accounting standard, currency and scale.
- [ ] Data Quality Note appears before any number and lists sources, as-of dates, estimates, and gaps.
- [ ] Verdict, composite score, top-three drivers, and key risks all fit within the first screen.
- [ ] Sector classification stated, playbook named, and suppressed metrics listed with reasons.
- [ ] Situation classification present, or explicitly stated as "none".
- [ ] Scorecard shows category scores, weights, weighted contributions, composite, and the weighting rationale.
- [ ] Every dimension section shows value + own history + peer median before interpretation.
- [ ] Peer set listed, justified, and exclusions explained; comparability caveats stated.
- [ ] Valuation method justified by sector; discount rate and terminal growth each justified.
- [ ] Reverse-DCF stated as a testable sentence and checked against actual historical delivery.
- [ ] Scenario table with probabilities, assumptions, implied values, and a probability-weighted figure.
- [ ] Red flags listed by severity; "checked and clear" list included; India and US-specific checks run as applicable.
- [ ] Bear case written to persuade, with the rebuttal kept separate and after.
- [ ] At least three invalidation triggers that are specific, observable, sourced, and time-bound.
- [ ] Every number carries a bracketed source; every estimate carries `[E]`/`(est.)` with a method note.
- [ ] No blank cells and no zeros standing in for missing data — `n/a` with a reason instead.
- [ ] No single-metric ranking anywhere in the document.
- [ ] Disclaimer present and unedited: research, not licensed financial advice.
