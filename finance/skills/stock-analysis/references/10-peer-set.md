# Building a Defensible Peer Set

Use this when: you are at Stage 5 and about to make any statement of the form "margins are high", "the stock is cheap", "returns are best in class" — every one of those claims is a comparison, and the peer set is its denominator.

This skill's governing rule is that a financial metric means nothing until you know its sector and the company's own history. The peer set is the machinery that makes the first half of that rule operational. Get it wrong and you do not get a slightly noisier answer — you get a confidently inverted one, because the peer set silently determines whether every metric reads as strength or weakness. It is also the easiest place in an analysis to cheat without noticing: quietly drop the two peers that outperform, and a mediocre company becomes a compounder. So construct the set explicitly, normalise its members onto one accounting basis before comparing anything, present results as ranks within the set rather than raw absolutes, and write down who you excluded and why.

## Contents

- [1. What a true comparable is: the six axes](#1-what-a-true-comparable-is-the-six-axes)
- [2. Operating comps vs valuation comps: two different sets](#2-operating-comps-vs-valuation-comps-two-different-sets)
- [3. Sourcing the candidate list](#3-sourcing-the-candidate-list)
- [4. Sizing and tiering the set](#4-sizing-and-tiering-the-set)
- [5. Peer-set quality diagnostics](#5-peer-set-quality-diagnostics)
- [6. Normalising peers before you compare anything](#6-normalising-peers-before-you-compare-anything)
- [7. Presenting the comparison: percentiles, not raw numbers](#7-presenting-the-comparison-percentiles-not-raw-numbers)
- [8. When the company has no good peers](#8-when-the-company-has-no-good-peers)
- [9. The traps](#9-the-traps)
- [10. Worked illustration: one company, three peer sets](#10-worked-illustration-one-company-three-peer-sets)
- [11. Sector translation: where the peer logic changes shape](#11-sector-translation-where-the-peer-logic-changes-shape)
- [12. Documenting the set so it can be audited](#12-documenting-the-set-so-it-can-be-audited)
- [Checklist](#checklist)

---

## 1. What a true comparable is: the six axes

A peer is not "a company in the same sector". A peer is a company whose economics respond to the same drivers in roughly the same way, so that a difference in a ratio is evidence about execution rather than evidence about structure. Test every candidate on all six axes below, and record the score. A candidate failing two axes badly is not a peer; it is context.

| Axis | What to check | Why it matters |
|---|---|---|
| **Same sub-sector / end market** | Not the GICS or NSE sector tag — the actual revenue mix. What does the customer buy, and why do they switch? A speciality chemicals maker selling agrochemical intermediates and one selling pharma intermediates share a sector tag and almost no demand driver. | Sector tags mix distributors with manufacturers and marketplaces with retailers. Demand cyclicality, pricing power and working-capital rhythm all come from the end market, not the tag. |
| **Comparable business model and value-chain position** | Manufacturer vs assembler vs distributor vs franchisor vs marketplace. Owned vs asset-light. Gross vs net revenue recognition. Integration level (does the peer make its own key input?). | Margin *levels* are set by where you sit in the chain. A 4% net-margin distributor and a 25% net-margin brand owner can earn identical returns on capital. Comparing their margins ranks business models, not businesses. |
| **Similar capital intensity** | Gross block / revenue, capex / revenue over five years, asset turnover, working-capital days. Also: does the peer lease what the subject owns (or vice versa)? | Capital intensity is the hinge between margin and return. Two companies with the same ROCE can have a 3x margin gap purely from turnover. If capital intensity differs by more than ~2x, only ROCE/ROIC comparisons survive; margin comparisons do not. |
| **Similar geography and regulatory regime** | Where revenue is earned (not where the company is listed), tariff and price-control exposure, labour regime, tax regime, subsidy dependence, currency of revenue vs cost. | A domestic Indian formulations player and a US-generics exporter face different pricing regimes, different customer concentration, and different tax rates. Net margin and ROE differences between them are largely regime, not skill. |
| **Similar scale** | Revenue, and separately, unit scale (plants, stores, installed base). Aim to keep the largest/smallest revenue ratio inside ~10x. | Scale buys procurement discounts, fixed-cost absorption, distribution density and cheaper capital. A ₹500 crore company benchmarked against a ₹50,000 crore one is being measured against advantages it cannot buy. Also, small caps have structurally noisier ratios. |
| **Similar accounting framework and fiscal calendar** | IFRS (IASB), EU-endorsed IFRS, US GAAP, Ind-AS, J-GAAP, PRC GAAP — record it as a column per ticker. Then record fiscal year-end and the exact TTM window. | Ratios are not defined identically across frameworks; Ind-AS is IFRS-converged but has carve-outs, making it a third dialect. Without alignment you are ranking accounting policy and calendar luck. Section 6 handles this. |

**Scoring convention.** Score each axis Pass / Partial / Fail and keep the grid in the comp sheet. Any candidate with a Fail on *end market*, *value-chain position* or *capital intensity* is excluded from the core set — those three cannot be fixed by adjustment. Fails on *framework* and *fiscal calendar* are fixable: normalise (Section 6) and keep. A Fail on *scale* means keep as reference-only, marked, and never let it into a percentile calculation.

---

## 2. Operating comps vs valuation comps: two different sets

Do not use one list for both jobs. They answer different questions and the criteria diverge.

- **Operating comps** answer "is this a good business, run well?" Selection is driven by business-model similarity: same end market, same value-chain position, same capital intensity. Listing venue and valuation are irrelevant. A private-equity-owned competitor that files public accounts, or an unlisted subsidiary of a foreign group filing in India (MCA/ROC filings) is a perfectly valid operating comp even though it has no share price.
- **Valuation comps** answer "what should this trade at?" Selection adds three requirements the operating set does not need: comparable *growth*, comparable *return on capital*, and comparable *risk/liquidity/market regime*. A company can be an excellent operating comp and a terrible valuation comp — same business, but growing at 4% instead of 20%, or listed in a market that structurally trades at half the multiple.

The single most common error here is importing the domestic-market multiple onto a foreign peer, or vice versa. Indian mid-caps have traded at a persistent multiple premium to global sector medians for long stretches; that premium reflects domestic liquidity, index flows and growth expectations, not accounting. If you cross markets in a valuation comp table, split the table by market and say what the cross-market spread has historically been, rather than blending into one median and calling the subject cheap or dear.

---

## 3. Sourcing the candidate list

Never build the list from memory or from a single screener tab. Triangulate — each source has a distinct bias, and the intersection is far more reliable than any one of them.

**Universal sources (best first):**

1. **The company's own competitive disclosure.** US: 10-K Item 1 "Competition" often names rivals directly. India: the annual report's *Management Discussion & Analysis* / "Industry Structure and Developments" section, plus the **earnings concall** — management naming a competitor unprompted in Q&A is the highest-signal peer identification available, because it reveals who they actually lose deals to.
2. **Customer-side and channel evidence.** Who else bids for the same tenders, sits on the same distributor's shelf, appears on the same approved-vendor list, or shows up in the same RFP. This is the ground truth the tags approximate.
3. **Credit rating agency reports** (CRISIL / ICRA / CARE / India Ratings; Moody's / S&P / Fitch). Rating rationales usually contain an explicit peer comparison table with the agency's own reasoning for the set. Free, and built by someone with a different incentive than the equity market.
4. **Regulatory market definitions.** Competition Commission of India (CCI) merger orders, and US DOJ/FTC filings, define the "relevant market" with evidence. Where they exist for your sector, they are the most rigorously argued peer sets you will find.
5. **Sell-side initiation notes and screener peer tabs** (screener.in, Trendlyne, Tijori for India; Bloomberg/CapIQ/FinViz/stockanalysis.com globally) — as a *starting candidate pool only*, never as the final set. These are tag-driven and inherit every classification error in Section 9.
6. **Index and classification codes** — GICS sub-industry, NAICS/SIC (US, in the EDGAR header), NIC codes and the NSE/BSE industry indices (India). Use them to *generate* candidates and to check you have not missed anyone. Never to *validate* the set.
7. **IPO documents.** India: the DRHP/RHP section "Basis for Offer Price" lists peers with their multiples — chosen by the issuer, so treat as a flattery-biased but informative list. US: the S-1 equivalent.
8. **Proxy / compensation peer groups.** US: DEF 14A compensation committee peer group. India: the remuneration section of the Board's Report. Useful and rarely used — but note the bias: comp peers are systematically chosen to be *larger*, because that justifies higher pay. Mine them for names, discard the framing.
9. **EDGAR full-text search** (efts.sec.gov) for the subject's own name: competitors frequently name the subject in their risk factors. India equivalent: full-text search of exchange filings and rating rationales.

**India-specific note.** Many genuine competitors are unlisted (family-owned, MNC subsidiaries). Their financials are filed with the MCA/ROC and are purchasable cheaply; industry-association data (e.g. sectoral bodies publishing volume/capacity shares) often covers them too. Excluding them because they are unlisted systematically biases the peer set toward whoever chose to list — usually the larger and more governance-conscious operators. At minimum, note the unlisted share of the market so the reader knows how much of the competitive field the comp table omits.

**Survivorship.** When you compare against peer *history*, include companies that were acquired, delisted or went bankrupt during the window. A five-year sector margin history built only from today's survivors overstates the sector's stability and its returns — the failures are exactly the observations that tell you what the downside looks like.

---

## 4. Sizing and tiering the set

**Target 5–10 core peers.** Below 4, percentile ranking is arithmetic theatre — with 3 peers a "75th percentile" is one company. Above ~12, you are almost certainly admitting members that fail an axis, and the median drifts toward the sector tag rather than the business.

Tier explicitly:

| Tier | Definition | Use |
|---|---|---|
| **Core** | Passes all six axes, or fails only on fixable axes (framework, fiscal calendar) and has been normalised. | The set that generates percentiles, medians and the relative verdict. |
| **Adjacent** | Same end market, different value-chain position or materially different capital intensity. | Context and directional sanity checks. Quote individually, never blended into the core median. |
| **Reference** | Global best-in-class operators in the same business, regardless of market or scale. | Answers "what does world-class look like structurally?" — a ceiling, not a benchmark. |
| **Excluded** | Failed an axis unfixably, or data unusable. | Listed with the reason. This list is part of the deliverable (Section 12). |

If the core set has fewer than 4 members after honest filtering, do not pad it. Say so, and shift weight to own-history benchmarking (Section 8). A thin, honest peer set plus a deep own-history series beats a fat, contaminated one.

---

## 5. Peer-set quality diagnostics

Run these on the assembled set *before* drawing conclusions from it. They are cheap, and they catch most contamination. Ranges are indicative only — they vary by market, sector concentration and period, and a well-argued exception beats the band.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| **Core peer count** | Number of Tier-1 peers with usable normalised data | 5–10 | Below 4, percentiles are noise; above 12, the set has drifted to the sector tag. |
| **Size dispersion** | Largest core peer revenue ÷ smallest | ≤ 10x (≤ 5x preferred) | Scale advantages (procurement, fixed-cost absorption, cost of capital) are structural, not managerial. Wide dispersion turns a size effect into a false quality signal. |
| **Revenue-mix overlap** | % of the subject's revenue falling in segments the peer also serves (use segment notes / Ind-AS 108 / ASC 280) | ≥ 60% for core | Below this you are comparing two different companies that happen to share a label. |
| **Capital-intensity spread** | max ÷ min of (gross block / revenue) or (capex / revenue, 5-yr avg) across the set | ≤ 2–3x | Beyond this, margin comparisons are invalid and only ROCE/ROIC comparisons carry meaning. |
| **Framework homogeneity** | % of core peers on the same reporting framework, or restated onto one | 100% after normalisation; flag if <70% before | Mixed frameworks mean the ranking partly measures accounting policy. See Section 6. |
| **Period alignment** | Max offset between peer TTM windows | ≤ 1 quarter | A one-quarter offset can place two peers on opposite sides of a commodity move or rate turn. |
| **Gross-margin dispersion (CV)** | Standard deviation ÷ mean of gross margin across the set | < 0.30–0.40 | High dispersion in a genuinely homogeneous set almost always means *cost-classification* differences (depreciation/freight in COGS vs SG&A), not real margin differences. Treat a high CV as a data alarm, not a finding. |
| **Median stability** | Recompute the peer median with each single peer removed in turn (leave-one-out) | No single removal should move the median more than ~10–15% relative | If dropping one name moves the median materially, your conclusion is a statement about that one company, not about the sector. |

---

## 6. Normalising peers before you compare anything

This is the step analysts skip and the reason most comp tables are wrong. Before any ratio goes into a table, put every member on one basis. Work down this ladder in order — each step depends on the ones above it. Record every adjustment with its note reference; an unsourced adjustment is indistinguishable from a fudge.

### 6.1 The adjustment ladder

| # | Adjustment | What to do | Consequence of skipping |
|---|---|---|---|
| 1 | **Reporting framework** | Record IFRS / US GAAP / Ind-AS / local GAAP per ticker from the basis-of-preparation note. For ADRs, check whether the 20-F contains a full IFRS-to-GAAP reconciliation (only some do) or is filed under IFRS with none. | EV/EBITDA, ROCE, net debt/EBITDA and gross margin are not identically defined across frameworks. You end up ranking policy. |
| 2 | **Consolidation scope** | Identify full consolidation vs proportionate vs equity accounting. Reconcile net income attributable to owners against total net income; compute the minority share. Confirm EV adds minority interest and treats equity-accounted investments consistently across all members. Look for structured entities, ESOP trusts and off-balance-sheet JVs. | A company consolidating 100% of a 60%-owned subsidiary shows all its EBITDA but owns 60% of the earnings; if EV is not grossed up for minorities it looks artificially cheap. A peer running the same business through JVs shows almost no revenue at all. |
| 3 | **Gross vs net revenue (principal vs agent)** | Read the IFRS 15 / ASC 606 / Ind-AS 115 revenue note. Marketplaces, travel, distribution, telecom handset bundles, ad-tech and EPC are the danger zones. Cross-check the disclosed take rate against revenue; look for a presentation change between years. | Two identical marketplaces can report revenue differing by 10x. Every P/S, EV/Sales, revenue-growth and revenue-per-employee comparison collapses. It is also a favourite way to manufacture growth with zero economic change. |
| 4 | **Lease treatment** | Confirm IFRS 16 / Ind-AS 116 (all leases capitalised; rent becomes depreciation + interest) vs ASC 842 (operating leases stay a single operating expense). Pull ROU assets, lease liabilities, ROU depreciation, lease interest, the undiscounted maturity table and the discount rate. Then build **both** conventions across the whole set: (a) lease-neutral — add rent/operating-lease expense back out of IFRS EBITDA so everyone is post-cash-rent; (b) fully capitalised — add the PV of operating-lease commitments to net debt for US GAAP filers, and include ROU assets in capital employed for ROCE. State which convention the table uses. | IFRS 16 mechanically inflates EBITDA *and* reported debt; a US operating lease does neither. Retail, airlines, telecom, hotels and logistics are worst affected — an unadjusted EV/EBITDA screen ranks the IFRS lessee cheap and the US lessee expensive for no economic reason. Many screeners also exclude lease liabilities from "total debt". |
| 5 | **Capitalisation policy** | Development costs: IFRS/Ind-AS *require* capitalisation once IAS 38 criteria are met; US GAAP expenses most R&D (narrow software/cloud exceptions). Pull capitalised development additions from the intangibles note and cash flow statement; compute capitalised-dev as % of total R&D. Apply the same test to software, interest and major-maintenance capitalisation. Build a common baseline — usually expensing everything. | Capitalisation simultaneously inflates EBIT, EBITDA, CFO and invested capital while deflating FCF after capex. It is the largest single source of non-comparability in pharma, software, autos and engineering, and a classic earnings-management lever. |
| 6 | **Cost classification** | Determine what sits in COGS vs SG&A vs other income for each member: depreciation, freight and distribution, R&D, share-based comp, warranty, warehousing. Note whether the P&L is by nature (IFRS-common: material cost, employee cost, other expense) or by function. Rebuild margins at EBITDA and EBIT level where classification washes out. | Gross margin is among the least comparable metrics in existence — depreciation and freight inside COGS can cost several margin points versus an economically identical peer. Ranking a sector on gross margin reproduces exactly the single-metric error this skill forbids. |
| 7 | **Inventory costing (US-specific)** | US GAAP permits LIFO; IFRS and Ind-AS prohibit it. Read the inventory note for the LIFO reserve and any LIFO liquidation. Restate to FIFO: add the LIFO reserve to inventory and to equity (net of tax), and adjust COGS by the change in reserve. | In inflation, LIFO depresses reported gross margin and inventory while inflating cash flow via lower tax. Uncorrected, the US filer looks less profitable and less asset-heavy than an identical IFRS peer, and asset-turnover/ROCE comparisons are meaningless. |
| 8 | **Goodwill, PPA and acquired-intangible amortisation** | Check whether goodwill is amortised (some local GAAPs; US private-company alternative) or impairment-tested only. Pull the purchase price allocation for recent deals: goodwill vs amortisable intangibles, and assigned useful lives. Quantify acquired-intangible amortisation as a share of EBIT and show EBIT both with and without it. | An acquisitive company carries a PPA amortisation drag an organic peer does not, while goodwill inflates its capital base and depresses ROCE. Unadjusted EBIT comparisons arbitrarily penalise or flatter acquirers. |
| 9 | **One-offs and "adjusted" figures — symmetrically** | Reconcile every adjusted number back to statutory. Tabulate add-backs by type and year: restructuring, impairment, share-based comp, acquired-intangible amortisation, litigation. Count consecutive years each "one-off" recurs, and compute cumulative add-backs as % of cumulative reported profit. Then build your own normalised series: strip asset-sale gains, insurance recoveries, one-time tax settlements, FX on debt — removing *favourable and unfavourable* items with equal rigour. In cyclicals use mid-cycle margins over a full cycle, not the latest year. | Recurring restructuring is not a one-off and SBC is a real cost of labour. Investors habitually strip losses and keep gains, biasing normalised earnings up. Applied unevenly across a peer set, this alone can reverse a ranking. |
| 10 | **Currency and translation** | Record presentation currency, functional currency of major subsidiaries, and the translation method (current-rate: assets/liabilities at closing, P&L at average, difference to CTA; or IAS 29 restatement for hyperinflation). Convert peers using a *consistent* convention: average rate for P&L, closing rate for balance sheet, per year. Never apply today's spot rate to historical years. Check for a change of presentation currency. Look at the CTA balance and the P&L FX line. | Reported growth for a multinational can be entirely FX. Mixing rate conventions introduces errors of several percent; using spot on history destroys the growth series outright. |
| 11 | **Constant-currency / organic growth** | Find each company's own bridge from reported to organic growth — FX, acquisitions, divestments, scope, extra trading week — or rebuild it. Verify acquisitions are excluded for a full 12-month anniversary and divestments removed from the base year too. | "Organic" is unaudited and defined differently by each company. Without a like-for-like bridge you cannot tell whether a peer's superior growth is execution, currency, or debt-funded bolt-ons — which changes what the growth is worth. |
| 12 | **Fiscal-year offset** | Record each year-end: India and Japan typically 31 March; many US retailers use 52/53-week years ending late Jan/early Feb; others 30 June or 31 December. Where ends differ by more than a quarter, rebuild a **TTM series from quarterly data** so every member covers the same calendar window. Watch 53-week years and stub/transition periods after a year-end change. | Comparing "FY2025" across a March-end and a December-end company can offset the economic period by a full quarter — enough to put them on opposite sides of a commodity move and make one look like a share gainer when it is merely earlier in the calendar. |
| 13 | **Tax regime** | Reconcile effective to statutory rate per member and identify drivers: tax holidays, SEZ/incentive regimes, India's optional lower corporate-tax regime, unrecognised DTAs, one-off remeasurements. Compare at EBIT/EBITDA level, or normalise every member to a sustainable rate. | Cross-border comparisons of net margin, ROE and P/E are dominated by tax regime and by temporary incentives that expire. Only pre-tax or normalised-tax comparisons isolate operating performance. |
| 14 | **Share count and per-share integrity** | Use diluted weighted-average shares from the EPS note, not a data feed's current count. Adjust the whole history for splits, bonus issues, rights issues (theoretical ex-rights factor) and consolidations. Add options, RSUs, warrants, convertibles, ESOP-trust shares. Ensure market cap covers *all* share classes, including unlisted or dual-class lines. | Dual-class and multi-line issuers (common in India, Brazil, Korea, Europe) are routinely mis-capitalised by providers using only the listed line — understating EV and making the stock look far cheaper than it is. |
| 15 | **Restatements and transition years** | Search filings for "restated", "reclassified", "prior period error", "IAS 8", Item 4.02 (US 8-K non-reliance). Compare last year's reported comparatives line-by-line against this year's. For each new standard (IFRS 16/15/9, ASC 842/606/326, new Ind-AS notifications) record whether transition was full retrospective or modified retrospective. **Mark the transition year on every chart.** | Providers often store originally-reported figures for old years and restated figures for recent ones, silently corrupting CAGRs. Under modified retrospective, the adoption year is a hard break and growth rates across it are arithmetic nonsense. |
| 16 | **Provider field definitions** | For every screened metric, read the vendor's definition: does "debt" include leases, preference shares, acceptances? Is EBITDA EBIT+D&A or a vendor model? Is EPS basic/diluted/reported/adjusted? Trailing, forward or last-fiscal-year? Then hand-verify the top three and bottom three names against primary filings. | Screener errors cluster exactly where screens are most extreme — misparsed one-offs, missing quarters, stale share counts, mis-tagged currencies. The outliers your screen surfaces are disproportionately data artefacts. |
| 17 | **Cash-flow classification** | Check where interest paid, interest received and dividends sit — IFRS permits choices that US GAAP largely fixes. Reclassify all members to one convention before comparing CFO, FCF or FCF yield. Watch supply-chain finance / reverse factoring, receivables securitisation, and capex reclassified between operating and investing. | CFO and FCF yield are not directly comparable across frameworks without this. Reverse factoring in particular converts debt into trade payables and flatters both leverage and CFO. |

### 6.2 Proportionality

Not every comparison needs all seventeen. Apply the **materiality filter**: run the adjustment if it could plausibly move the metric you are ranking on by more than the gap between the subject and the peer median. If the subject is at a 22% EBITDA margin and the median is 21%, a lease-convention difference worth 400bp decides the entire conclusion and is mandatory. If the subject is at 22% against a median of 8%, it is not.

In **Screen mode**, do steps 1, 4, 6 and 12 at minimum — framework, leases, cost classification and period alignment — because those four flip signs most often. In **Deep dive**, do all seventeen and show the adjustment bridge.

---

## 7. Presenting the comparison: percentiles, not raw numbers

Once the set is normalised, present **position within the set**, not absolutes. A raw table of numbers invites the reader (and you) to sort a column — which is precisely the single-metric ranking this skill forbids.

**How to build it:**

1. For each metric, compute the subject's **percentile rank** within the core peer set, plus the peer **median** and the **interquartile range**. Report as: `ROCE 19.4% — 80th pctile (peer median 14.1%, IQR 11–17%)`.
2. State the **direction convention** explicitly per metric (higher is better for ROCE; lower is better for net debt/EBITDA and working-capital days). Getting one inverted quietly corrupts a composite score.
3. Show the **dispersion**. An 80th percentile in a set where the IQR is 11–17% is a real gap. An 80th percentile in a set spanning 18.5–19.6% is a rounding difference. Percentile without spread is misleading precision.
4. With fewer than ~6 peers, report **rank out of N** ("3rd of 6") rather than a percentile. A percentile implies a distribution you do not have.
5. Report the subject's **own-history percentile alongside** the peer percentile — where does today's ROCE sit within the company's own 5–10 year distribution? Best-in-class-but-decaying and worst-in-class-but-improving are the two most valuable findings in the whole exercise, and only the two-axis view surfaces them.
6. Use **medians, not means**, throughout. One outlier peer moves a mean enough to reverse a verdict; that is how a comp table lies without a single wrong number.
7. Never collapse the peer table into a single composite score without showing the components and weights. Composite scores hide exactly the trade-offs (margin vs turnover, growth vs returns) the analysis exists to expose.

**Always report absolutes too, in a secondary column.** A percentile tells you the relative position; it does not tell you whether the whole sector is destroying capital. A company at the 90th percentile of an industry earning 6% ROIC against a 11% WACC is the best of a value-destroying set — a fact percentiles alone will never reveal. Cross-check every relative conclusion against the absolute ROIC-vs-WACC spread.

---

## 8. When the company has no good peers

Genuinely peerless companies exist: sole domestic licensees, unusual conglomerates, first-of-kind business models, monopoly infrastructure concessions. The failure mode is inventing a peer set anyway. Do not. Say plainly that no defensible peer set exists, and substitute the following, in this order.

**1. Own-history benchmarking becomes primary.** Build a 10-year (minimum 5-year) series for every core metric and compare the current value against the company's *own* distribution — median, range, and current percentile. Then split the variance into cycle and structure: overlay the series against the relevant cycle driver (commodity price, rate cycle, capacity utilisation, order-book/book-to-bill) and ask whether the current position is where you would expect the company to be at this point in the cycle. A company at the low end of its own margin range in a trough is normal; at the low end at a cycle peak, something structural has broken. Adjust the history for accounting-standard transitions (Section 6, item 15) or the series is not self-comparable either.

**2. Cross-sector comparison only via ROIC vs WACC.** This is the one comparison that survives crossing industries, because it is unit-free and measures the same economic question everywhere: *is this business earning more on invested capital than the capital costs?*

- Compute **ROIC = NOPAT / invested capital**, with NOPAT = EBIT × (1 − normalised tax rate), and invested capital = total debt + equity + lease liabilities − cash and non-operating assets (or, equivalently, net working capital + net fixed assets + capitalised intangibles). Use the same lease and capitalisation conventions you applied in Section 6 — the spread is only cross-sector-valid if the numerator and denominator are built consistently.
- Compare against **WACC**, built from a local risk-free rate (India: 10-year G-Sec; US: 10-year Treasury), an equity risk premium appropriate to that market, a beta reflecting the business not just the stock, and the company's actual after-tax cost of debt.
- Report the **spread (ROIC − WACC) and the growth rate**. Positive spread plus growth creates value; negative spread plus growth destroys it faster. That statement is true in software, cement and shipping alike.
- Report the **duration** of the spread — how many of the last ten years was it positive, and is it widening or narrowing? A single year's spread is a cycle observation, not a quality judgement.

What does *not* transfer across sectors: margin, asset turnover, working-capital days, EV/EBITDA, P/E, net debt/EBITDA, gross margin. Do not use them cross-sector under any framing.

**3. Sub-segment peering.** A conglomerate may have no company-level peer while each segment has excellent ones. Peer each segment separately using segment disclosures (Ind-AS 108 / ASC 280), then value sum-of-the-parts with an explicit holdco discount. This is nearly always better than forcing a company-level comp.

**4. Value-chain and analogue peering.** Where a direct peer does not exist, an *analogue* may: a company with a different product but the same economic structure (subscription with high retention, toll-road-like annuity, franchised network with low capital intensity). Label it clearly as an analogue, use it only for structural questions (what should retention/capital intensity/incremental margin look like in a model like this?), and never for valuation multiples.

**5. Historical-case reasoning.** Where a business model has played out before in another market or era, use it qualitatively — what typically happened to margins as the model matured, what killed the ones that failed. Qualitative only; do not import numbers.

---

## 9. The traps

**Conglomerate contamination.** A diversified peer's consolidated ratios are a revenue-weighted blend of businesses with different economics. Including one in a focused peer set drags the median toward a mixture nobody actually operates. *Fix:* use the peer's segment disclosure and compare segment-to-company, or move it to Adjacent tier. Segment data is imperfect — unallocated corporate costs and transfer pricing distort it — so state that limitation rather than pretending segment EBIT is clean. The same applies in reverse: if the *subject* is diversified, do not compare its consolidated ratios to focused peers.

**Size mismatch.** Beyond about 10x revenue difference, you are measuring scale economics, not management. It runs both ways: large peers enjoy procurement, distribution and funding-cost advantages; small peers often show flattering ratios because a single contract or a lumpy capitalisation dominates a small base, and because they are earlier on the growth curve. *Fix:* cap dispersion, tier by size, and where scale is the explicit question, say so and compare unit economics (per store, per tonne, per MW, per seat) rather than consolidated ratios.

**A peer set chosen to flatter.** The most dangerous trap, because it is invisible in the output. It happens through omission far more often than through commission: the strongest competitor is "not really comparable", the weakest is "close enough". *Fixes, applied together:* (a) fix the selection criteria in writing **before** you look at any peer's numbers; (b) keep the exclusion list with reasons in the deliverable; (c) run leave-one-out on the median (Section 5); (d) run the **adversarial test** — deliberately construct the most hostile defensible peer set and see whether the conclusion survives. If the verdict flips between two defensible sets, the honest output is "the answer depends on the comparison set", with both shown. That is a real finding, not a failure. Beware of inherited sets carrying someone else's incentive: IPO-prospectus peer lists (issuer wants a high price), compensation peer groups (management wants large comparators), and company-presentation peer charts (chosen to win).

**Index and classification labels that mislead.** Sector tags are constructed for index and portfolio-construction purposes, not analytical ones. Recurring failures: payments and exchange businesses have been reclassified between technology and financials, moving the "sector median multiple" without any business changing; broad national indices labelled by consumption category bundle staples with hotels and tobacco; "Consumer Discretionary" spans autos and luxury and restaurants; "Industrials" spans defence primes and staffing agencies; "Diversified Financials" is not a business model. Also watch the *self-selected* tag: companies choose their own NAICS/SIC code on EDGAR and their industry classification on Indian exchanges, and they sometimes choose the one that trades at a higher multiple. *Fix:* treat every tag as a candidate generator and validate on the six axes in Section 1. If your peer set was produced by a single dropdown filter, it is not a peer set.

**Time-varying peer sets.** A peer that was comparable five years ago may have divested its way out of the business. When you build a multi-year peer median, verify comparability *in each year*, not just today, or you will attribute an industry-mix shift to the subject's performance.

**Circular valuation.** Concluding a stock is cheap because it trades below the peer median tells you nothing if the whole sector is expensive. Anchor at least one valuation leg to something absolute — a reverse DCF, a ROIC-vs-WACC spread, or the sector's own long-run multiple range — before letting relative cheapness carry a conclusion.

---

## 10. Worked illustration: one company, three peer sets

*Figures below are hypothetical and constructed to show the mechanism. They are not any real company's data.*

**The subject.** A mid-sized manufacturer of engineered components, revenue ~₹4,000 crore, Ind-AS, March year-end. Reported EBITDA margin 14%, ROCE 17%, EV/EBITDA 13x. It owns its plants; it capitalises a modest amount of development cost; roughly 70% of revenue is domestic.

**Peer set A — "the sector tag."** Everything in the exchange's broad "capital goods" industry index. Includes two large diversified engineering conglomerates (project EPC plus products), one pure distributor of imported components, and one asset-light design-and-outsource player. Median EBITDA margin: 9%. Median ROCE: 14%. Median EV/EBITDA: 22x.

> **Conclusion this set produces:** margins 500bp above the sector, returns above median, and trading at a 40% discount to the sector multiple. *A high-quality compounder, unjustifiably cheap.*

**Peer set B — "flattery by omission."** Four domestic peers, chosen after glancing at the numbers: three sub-scale players at ₹600–1,200 crore revenue and one loss-making turnaround. The two genuinely comparable ₹5,000–7,000 crore competitors were excluded as "not directly comparable — different product mix". Median EBITDA margin: 10%. Median ROCE: 11%.

> **Conclusion this set produces:** best-in-class on every operating metric. *Category leader.*

**Peer set C — the defensible set.** Six manufacturers of engineered components: revenue ₹2,000–9,000 crore (dispersion 4.5x), all owning their manufacturing, all majority-domestic revenue, four on Ind-AS and two on IFRS, fiscal years aligned to a common TTM window using quarterly data. Then normalised: one IFRS peer's development capitalisation expensed to match the baseline (subject margin −80bp, one peer −190bp); two peers' freight reclassified out of COGS for a like-for-like gross margin; one peer's ROU assets added to capital employed; one peer's recurring three-year "restructuring" add-back reversed into statutory EBIT; the subject's asset-sale gain in the latest year removed.

Post-normalisation medians: EBITDA margin 15.5%, ROCE 21%, EV/EBITDA 12x. The subject's normalised figures: EBITDA margin 13.2%, ROCE 15.5%, EV/EBITDA 13x.

> **Conclusion this set produces:** 2nd-lowest margin of 7, 6th of 7 on ROCE, and trading at a modest *premium* to the peer median despite weaker returns. Own-history check: ROCE at the 30th percentile of its own ten-year range, and the peer gap has widened for three consecutive years. *A share-losing operator at a full price.*

**What changed between A, B and C was not a single reported number.** The subject's filings are identical in all three. Set A's median was dragged down by conglomerates, a distributor and an asset-light player whose margin structures are simply different, and dragged *up* on multiple by companies with faster growth — producing a false discount. Set B was contaminated by size mismatch and selective exclusion. Set C survived the six axes and the normalisation ladder, and reversed the verdict entirely.

Two lessons to carry into every comp table: the largest single swing came from **who was in the set**, not from the normalisation adjustments — get selection right before you get precise. And the normalisation still mattered at the margin: without it, the subject's reported 14% margin sat above an unnormalised peer median of 13.9%, which would have read as parity rather than a deficit.

---

## 11. Sector translation: where the peer logic changes shape

The six axes hold everywhere, but for some sectors the metrics that go into the comparison must change entirely — the standard ratios are undefined or inverted. Read the relevant playbook in `references/sectors/` before building the table.

| Sector | What breaks | Peer-set implication |
|---|---|---|
| **Banks / NBFCs** | EBITDA, EV and net debt are meaningless; debt is raw material. Provisioning models differ (IFRS 9 / Ind-AS 109 ECL vs US CECL vs older incurred-loss). | Peer on loan-book composition (secured/unsecured, retail/corporate, tenor), funding mix (CASA, borrowings), NIM, cost-to-income, credit cost through a cycle, GNPA/NNPA and coverage, and capital adequacy. Never blend a deposit-funded bank with a wholesale-funded NBFC. |
| **Insurers** | IFRS 17 broke the historical series outright; older embedded-value reporting is not comparable to it. Revenue is not a meaningful concept. | Peer within one reporting regime and one product mix (life vs general vs health; par vs non-par vs ULIP). Compare VNB margin, persistency, combined ratio, solvency. Mark the IFRS 17 transition year on every chart. |
| **REITs / real estate** | IAS 40 fair-value gains flow through the IFRS income statement; US GAAP cost model does not. EPS and P/E are near-meaningless. | Peer on FFO/AFFO, NAV, occupancy, WALE, cap rates, LTV — and only within the same measurement model. Fair-value vs cost model peers are not comparable on earnings at all. |
| **Miners / E&P** | Successful-efforts vs full-cost accounting; reserve-estimate standards differ by jurisdiction. Earnings are a commodity-price derivative. | Peer on cost curve position (all-in sustaining cost per unit), reserve life and grade, and mid-cycle rather than spot economics. Never compare a trailing-year P/E across the cycle. |
| **Utilities / regulated infra** | Regulatory assets, allowed-return frameworks and tariff regimes dominate outcomes. | Peer only within the same regulatory regime. Compare regulated asset base growth, allowed vs achieved RoE, and collection efficiency. A cross-regime "utility peer set" compares regulators, not managements. |
| **Conglomerates / holdcos** | No company-level peer exists by construction. | Peer each segment separately; value sum-of-the-parts; benchmark the holdco discount against other holdcos in the same market. |

---

## 12. Documenting the set so it can be audited

The peer table is a deliverable, not scratch work. Include this in the report:

1. **The selection criteria, written before selection** — the six axes with the thresholds you chose (size band, revenue-mix overlap, geography).
2. **The inclusion table** — one row per core peer: ticker, exchange, revenue, framework, fiscal year-end, TTM window used, and a Pass/Partial/Fail on each of the six axes.
3. **The exclusion list with reasons** — every candidate considered and rejected, and which axis it failed. This is what makes the set defensible, and it is the single strongest defence against unconscious flattery.
4. **The adjustment log** — every normalisation applied, per company, with the note or filing reference and the quantum. A reader must be able to get from the reported number to your number.
5. **The convention statement** — one line naming the lease convention, the capitalisation baseline, the currency rate convention, the tax normalisation and the TTM window. Everything in the table obeys it.
6. **The as-of date and source for every price and multiple.**
7. **A sensitivity note** — how the conclusion changes under the adversarial peer set (Section 9). If it does not change, say so; that is the strongest form the relative claim can take.

An undocumented comp table cannot be updated, audited or defended — and it quietly reintroduces single-metric ranking the moment anyone sorts a column.

---

## Checklist

- [ ] Selection criteria written down **before** looking at any peer's numbers.
- [ ] Every candidate scored on all six axes; end market, value-chain position and capital intensity treated as unfixable fails.
- [ ] Candidate list triangulated from at least three independent sources (company disclosure/concall, rating agency, regulator/index/screener) — never one dropdown filter.
- [ ] Unlisted and delisted/acquired competitors considered; survivorship bias in multi-year peer history noted (India: MCA/ROC filings).
- [ ] 5–10 core peers; size dispersion ≤10x; tiers marked (core / adjacent / reference / excluded).
- [ ] Operating comps and valuation comps kept as separate sets; cross-market multiple differences stated, not blended.
- [ ] Reporting framework recorded per ticker (IFRS / US GAAP / Ind-AS / local), and normalised or flagged.
- [ ] One lease convention applied to the whole set, stated explicitly; ROU assets in capital employed for ROCE.
- [ ] Capitalisation policy (development, software, interest) put on a common baseline.
- [ ] Cost classification checked (depreciation/freight/R&D/SBC in COGS vs SG&A); margins rebuilt at EBITDA/EBIT level.
- [ ] Gross vs net revenue recognition verified before any P/S or revenue-growth comparison.
- [ ] Consolidation scope and minority interests reconciled; EV grossed up consistently.
- [ ] One-offs normalised **symmetrically** — gains stripped as rigorously as losses; recurring "one-offs" counted.
- [ ] Currency converted on a consistent rate convention (average for P&L, closing for balance sheet, per year).
- [ ] Fiscal-year offsets fixed by rebuilding TTM from quarterly data; 53-week and stub periods flagged.
- [ ] Restatements and standard-transition years identified and marked on every chart.
- [ ] Provider field definitions read; top and bottom screen hits hand-verified against primary filings.
- [ ] Comparison presented as percentile/rank within the set with median and IQR — not raw sorted absolutes.
- [ ] Own-history percentile reported alongside every peer percentile.
- [ ] Absolute ROIC-vs-WACC spread reported so a "best of a value-destroying sector" verdict cannot hide behind percentiles.
- [ ] Leave-one-out test run on the peer median; adversarial peer set tested and the outcome disclosed.
- [ ] Sector-specific metric set used where standard ratios are undefined (banks, insurers, REITs, miners, utilities, holdcos).
- [ ] Exclusion list, adjustment log, convention statement and as-of dates published with the table.
- [ ] Indicative ranges in this file treated as starting points only — they vary by market, cycle and period, and peer/own-history evidence overrides them.
