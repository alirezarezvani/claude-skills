# Data Sourcing and Verification

Use this when: you are about to pull any number into an analysis, or you are checking a figure someone else supplied.

Every downstream judgment — margin quality, leverage, valuation, sector positioning — inherits the reliability of the numbers you started with. A wrong unit, a standalone-vs-consolidated mix-up, or a stale price destroys a conclusion more thoroughly than a weak argument does, and it does so invisibly. Sourcing discipline is not bookkeeping hygiene; it is the first analytical step. The governing rule of this skill applies here too: a figure without its sector, its period and its basis of preparation is not yet a fact.

## Contents

- [1. Primary vs secondary sources](#1-primary-vs-secondary-sources)
- [2. India: where the data lives](#2-india-where-the-data-lives)
- [3. Global / US: where the data lives](#3-global--us-where-the-data-lives)
- [4. The verification protocol](#4-the-verification-protocol)
- [5. Consolidated vs standalone](#5-consolidated-vs-standalone)
- [6. Units, currency and the 10x error](#6-units-currency-and-the-10x-error)
- [7. Fiscal-year alignment and period labelling](#7-fiscal-year-alignment-and-period-labelling)
- [8. Restatements, reclassifications and discontinued operations](#8-restatements-reclassifications-and-discontinued-operations)
- [9. As-of dates for price, market cap and multiples](#9-as-of-dates-for-price-market-cap-and-multiples)
- [10. Common data-provider errors and ambiguous fields](#10-common-data-provider-errors-and-ambiguous-fields)
- [11. Sector-specific sourcing traps](#11-sector-specific-sourcing-traps)
- [12. When web access is unavailable or data is paywalled](#12-when-web-access-is-unavailable-or-data-is-paywalled)
- [13. Never fabricate](#13-never-fabricate)
- [Checklist](#checklist)

---

## 1. Source hierarchy — documents are the only source of record

This is a **document-first** skill. Every financial figure in the analysis must trace to a raw company document. Rank sources by how many hands the number has passed through, and note the hard boundary between Tiers 1–3 and Tier 4.

### Tiers 1–3: Sources of record

Figures from these sources may be cited in the analysis.

| Tier | What it is | Use it for |
|---|---|---|
| 1. Primary filing | Annual report, 10-K/10-Q, exchange filing (quarterly results), audited financial statements, prospectus (DRHP/RHP/S-1) | Any figure that carries weight in the conclusion — this is the default source |
| 2. Company-published secondary | Investor presentation, earnings release, concall transcript, IR fact sheet | Segment detail, management commentary, guidance, operating KPIs not in the statements |
| 3. Regulator/third-party primary | SEBI/MCA/ROC records, credit rating rationales, exchange bulk-deal and shareholding data | Ownership, pledges, related-party context, debt structure, covenants |

### Tier 4: Navigation and cross-check only — NOT a source of record

| Tier | What it is | Permitted use |
|---|---|---|
| 4. Aggregators | screener.in, Tikr, Yahoo/Google Finance, stockanalysis.com, broker terminals, Wikipedia | (a) Locating the actual documents — e.g. screener.in links to annual reports and concall transcripts. (b) Spotting outliers to investigate in the filing. (c) Optional labelled cross-check *after* a figure is already sourced from a Tier 1–3 document. |

**Hard rule: an aggregator figure must never appear as a cited source in the report.** If a figure exists only in an aggregator and cannot be traced to any Tier 1–3 document, it is `not sourced` — write it as such. Aggregators normalize thousands of filings with rules that cannot fit every company, and their exception handling is invisible to you. When an aggregator figure and a filing figure disagree, the filing wins — and the disagreement itself is information.

Aggregator figures *may* appear alongside a document-sourced figure as a labelled cross-check: `"Revenue ₹4,820 cr (FY25 AR p.112; screener.in agrees at ₹4,818 cr)"`. They must never stand alone.

**One exception: current share price and market cap** are inherently sourced from exchange or finance websites. These must carry an as-of date and time.

Cite the tier in your notes. `"Revenue INR 4,820 cr (FY25, consolidated, annual report p.112)"` is usable. `"Revenue ~4,800 cr"` is not. `"Revenue 4,800 cr (screener.in)"` is not — it fails the document-first rule.

---

## 2. India: where the data lives

**Company investor-relations page.** The canonical starting point. Look for: annual reports (usually 5-10 years archived), quarterly results, investor presentations, earnings call transcripts and audio, press releases, and often an "investor contact" address. IR pages are the fastest route to the actual PDF of the annual report; exchange sites host the same document but with worse navigation.

**Annual report (India-specific structure).** Under the Companies Act 2013, an Indian annual report contains, in order of analytical value:
- Standalone **and** consolidated financial statements with schedules/notes — the notes are where the analysis actually is.
- **Management Discussion & Analysis (MD&A)** — segment commentary, sometimes volume and realization data.
- **CARO report** (Companies Auditor's Report Order) — an underused goldmine. It forces the auditor to comment on fixed-asset verification, inventory discrepancies, loans to related parties, statutory dues in arrears, default in repayment of borrowings, fraud reported, and whether funds raised for one purpose were used for another. Read every CARO qualification.
- **Auditor's report**: check for qualified/adverse/disclaimer opinions, Emphasis of Matter, and Key Audit Matters (KAMs). KAMs tell you which numbers the auditor itself found hardest.
- **Related party transactions note** — sales, purchases, loans, guarantees to promoter-linked entities.
- **Contingent liabilities note** — disputed tax demands, guarantees, litigation. Frequently larger than net worth in infra and telecom.
- **Corporate governance report** and **Business Responsibility & Sustainability Report (BRSR)** for larger listed companies.
- **Secretarial audit report** (Form MR-3).

**NSE and BSE filings and announcements.** Every listed company files quarterly results, shareholding patterns, board-meeting outcomes, material events under SEBI LODR Regulation 30, analyst-meet intimations, credit-rating changes, resignations of directors/auditors/KMP, and pledge disclosures. Search by company on nseindia.com (Corporate Filings) or bseindia.com (Corporate Announcements). Announcements are timestamped — use the exchange timestamp, not a news article's, when sequencing events.
- **Regulation 30 disclosures** are where acquisitions, order wins, plant shutdowns, fires, regulatory actions and litigation first appear.
- **Auditor resignation** filings and **independent-director resignations with reasons** are high-signal governance events.

**Shareholding pattern filings (quarterly, both exchanges).** Gives promoter holding, promoter **pledge** (as % of promoter holding and % of total shares — note which one a source quotes), FII/FPI, DII (mutual funds, insurance), public and, for many companies, the list of shareholders holding above 1%. Track the trend, not the level: a promoter stake declining over consecutive quarters, or pledge rising, deserves an explanation you should find in filings rather than infer.

**Aggregators — navigation and cross-check only.** Sites like screener.in, Tikr, and stockanalysis.com are useful for two things: (a) *finding* the actual documents — screener.in links directly to annual reports and concall transcripts, which is its most valuable feature; and (b) spotting outliers in ratio history or peer sets that you then investigate in the filing. Their computed ratios, standardized financials, TTM columns, and median calculations reflect invisible normalization choices that may not match the company's actual reporting. **Do not extract figures from these sites as your source.** Navigate through them to reach the document, then extract from the document. If you use an aggregator figure as a cross-check alongside a document-sourced number, label it explicitly as such.

**MCA / ROC (Ministry of Corporate Affairs).** The route to unlisted entities: promoter holding companies, subsidiaries, JV partners, related parties, and the private companies behind a group structure. Filed documents include AOC-4 (financial statements), MGT-7 (annual return), charges registered against assets (useful for spotting secured debt not obvious from the consolidated balance sheet), and director/DIN records for cross-directorship mapping. Many documents are pay-per-download.

**SEBI.** Regulatory orders and adjudication (enforcement against companies, promoters, intermediaries), takeover/SAST disclosures, insider-trading (PIT) disclosures, buyback and open-offer documents, and the mutual-fund and FPI regulatory framework. A SEBI order naming the promoter is a governance fact of the first order.

**Credit rating agency rationales — CRISIL, ICRA, CARE, India Ratings, Brickwork.** Free, detailed, and often the single best third-party document on a company's debt. A rationale typically gives: rated instruments and amounts, the agency's own computed leverage and coverage ratios, key rating drivers and sensitivities (explicit numeric thresholds for upgrade/downgrade), liquidity assessment, and the group structure the agency consolidates. Ratings history matters more than the current rating — a sequence of downgrades or a move to "Rating Watch with Negative Implications" precedes trouble more reliably than any screen. Also check for **"Issuer Not Cooperating" (INC)** tags: a company that stopped supplying information to its rating agency is telling you something.

**Concall transcripts.** Usually on the IR page, on exchange filings, and aggregated by screener.in and transcript services. Read the Q&A, not the prepared remarks — the prepared remarks are the press release read aloud. Note: which analysts cover the company, which questions management deflects, whether guidance given last quarter was met, and specific numbers management volunteers (volumes, realizations, capacity utilization, order book, segment margins) that never appear in the statements. Quote the speaker and the quarter when you use them.

**DRHP / RHP (for IPOs and recent listings).** The Draft Red Herring Prospectus is the most information-dense document that exists on an Indian company: multi-year restated financials, risk factors written by lawyers who must disclose, litigation schedules (including against promoters and directors), objects of the issue, promoter background, related-party history, KPI disclosures with a management justification, and peer comparison. For a company listed in the last 3-4 years, always read the DRHP even though it is old — it explains the pre-IPO structure the current filings assume you know.

**Other Indian sources.** RBI (banking sector data, sectoral credit deployment), industry bodies (SIAM for autos, CMIE, ICRA/CRISIL sector reports), IBBI (insolvency filings against the company or its counterparties), GST and customs data vendors (paid), and the company's own regulatory filings with sector regulators (IRDAI, TRAI, CERC, PNGRB).

---

## 3. Global / US: where the data lives

**SEC EDGAR** is the primary source for US registrants and for foreign companies with US listings. Use full-text search and the company's filing index.

| Form | What it contains | Analytical use |
|---|---|---|
| 10-K | Annual report: audited statements, MD&A, risk factors, Item 1 business description, segment note, controls | The base document. Item 7 MD&A and the segment note carry most of the signal |
| 10-Q | Quarterly, unaudited, condensed | Trend within the year; note the comparatives are prior-year quarter, not sequential |
| 8-K | Material events: earnings release (Item 2.02), leadership change, acquisition, auditor change (Item 4.01), impairment (Item 2.06), covenant default | Timeline of events; the earnings press release is an 8-K exhibit |
| DEF 14A (proxy) | Executive compensation, incentive metrics, board composition, auditor fees, shareholder proposals, related-party transactions | Tells you what management is actually paid to maximize — often diverges from what they say on calls |
| Form 4 | Insider transactions within 2 business days | Insider buying/selling; distinguish open-market purchases from option exercises and 10b5-1 plan sales |
| SC 13D/13G, 13F | Large holders; institutional quarterly positions | Ownership concentration and activist presence |
| S-1 / F-1 | IPO registration | The global analogue of the DRHP |
| 20-F / 40-F | Foreign private issuers (annual), often IFRS | Non-US companies with US listings; note IFRS-GAAP reconciliation is no longer required |
| 6-K | Foreign private issuer interim reports | Quarterly data for 20-F filers, format varies by home market |
| NT 10-K / NT 10-Q | Late-filing notification | A material red flag; read the stated reason |

Also: **XBRL "Financial Statement Data Sets"** and the EDGAR company-facts JSON API give machine-readable tagged figures straight from filings — use them when you need many periods, but check the tag actually maps to the line item you think it does (companies use extension tags liberally).

**Non-US primary sources.** UK: Companies House plus the RNS regulatory news service. EU: national registries plus the issuer's own regulatory news; ESEF-tagged annual reports. Japan: EDINET and TDnet. Canada: SEDAR+. Australia: ASX announcements. Hong Kong: HKEXnews. Each has its own equivalent of "material event" filings — find it before concluding nothing happened.

**Company IR and annual reports (global).** Under IFRS, the annual report structure differs from the 10-K: strategic report, governance and remuneration report, then statements with notes. Segment reporting under IFRS 8 and ASC 280 both follow the "management approach", meaning segments reflect how the CEO sees the business — which is itself information, and which changes when management changes.

**Earnings call transcripts.** Company IR sites increasingly post them directly; otherwise use transcript providers. Same rule as India: the Q&A carries the signal. Track guidance given versus guidance delivered across four to eight quarters — this is the cheapest available test of management credibility.

**Other global.** Central bank and statistical agencies for macro inputs; industry regulators; rating agency reports (Moody's/S&P/Fitch — summaries often free, full reports paywalled); bond prospectuses and covenant packages when leverage matters.

---

## 4. The verification protocol

Apply this to every figure that could change a conclusion.

**1. Cite source and period, always.** Format: `value + unit + basis + period + source`. Example: `EBITDA margin 14.2% (FY25, consolidated, computed from annual report P&L, p.104)`. If you cannot state all five, you do not yet have the figure. This is not formatting pedantry — most sourcing errors become visible the moment you try to write the full citation and find one field missing.

**2. Cross-check headline figures across two independent sources — at least one must be a primary document (Tier 1–3).** Headline = revenue, EBITDA/operating profit, PAT, total debt, equity, operating cash flow, share count, market cap. Independent means the two sources did not derive from each other: an aggregator and a news article that both copied the press release are one source, not two. Two aggregators are also not a valid cross-check — at least one side must be a document. Filing vs rating rationale, or annual report vs quarterly results filing, is a real cross-check. Filing vs aggregator is acceptable as the second source, but the aggregator figure is the cross-check, not the source of record.

**3. Reconcile any discrepancy before proceeding.** A gap of a few percent is usually a definitional difference (other income in/out of EBITDA, leases, minority interest). A gap above ~10% usually means different basis, different period, or different units. Do not average two numbers you cannot reconcile — find which one is right, or report both with their definitions.

**4. The primary document always wins.** If the aggregator says one thing and the audited statement says another, use the statement and note the aggregator's error, because that error probably contaminates the aggregator's ratios too. The aggregator figure is never an acceptable substitute for a document-sourced one — it may appear only as a labelled cross-check.

**5. Recompute rather than accept.** Derived metrics — ROCE, ROE, net debt/EBITDA, working capital days, FCF — should be computed by you from raw line items you have sourced, with your formula stated. Providers differ on almost every one of these (see §10). Recomputing also forces you to see the components, which is where the story is.

**6. Sanity-check against the real world.** Does implied revenue per store, per tonne, per employee, per subscriber make sense? Does the balance sheet balance? Do the three statements tie (PAT to cash flow opening line, closing cash to balance sheet)? Does the growth rate imply a market share that exceeds the market? An arithmetic check costs seconds and catches transcription errors that reasoning will not.

**7. Flag single-sourced figures explicitly.** Where a number could not be corroborated, say so in the output: "single source, unverified". A reader can discount a flagged number; they cannot discount one presented with false confidence.

---

## 5. Consolidated vs standalone

India-specific in emphasis, but the same issue exists globally as parent-only versus group accounts.

- **Consolidated** includes subsidiaries line-by-line, associates/JVs by equity method, and shows non-controlling (minority) interest separately. **Standalone** is the parent company only, with subsidiary income appearing mostly as dividends and investments held at cost.
- **Default to consolidated** for operating and valuation analysis. It reflects the economic entity that the equity actually owns.
- **Never mix the two** within a ratio. Consolidated EBITDA over standalone debt, or consolidated PAT over a standalone equity base, produces numbers that look plausible and are meaningless.
- **PAT must be after minority interest** ("profit attributable to owners of the parent") when computing EPS, ROE or P/E. Providers get this wrong regularly for holding-company structures.
- **When the gap is large, investigate it.** A parent with much higher standalone margins than consolidated is carrying loss-making subsidiaries. The reverse suggests value sits in subsidiaries — then ask who else owns them.
- Watch for **subsidiary debt without recourse to the parent**, **associates carried at equity whose losses are capped at carrying value**, and **structured entities**. Rating rationales are useful here because agencies state their own consolidation perimeter explicitly.
- For **holding companies and conglomerates**, consolidated statements can obscure more than they reveal; you may need a sum-of-parts using subsidiary-level filings from MCA or the subsidiaries' own listings.
- Older Indian data pre-Ind AS (before FY16-17 phase-in) is not directly comparable to later years — Ind AS changed revenue recognition, leases (Ind AS 116 from FY20), financial-instrument measurement and consolidation of certain entities. Say so when your series crosses the boundary. The same applies globally to ASC 606 (revenue) and ASC 842 / IFRS 16 (leases), which moved operating leases onto the balance sheet and shifted rent expense into depreciation and interest — inflating EBITDA and leverage simultaneously.

---

## 6. Units, currency and the 10x error

This is the single most common serious error and the easiest to prevent.

- Indian numbering: **1 lakh = 100,000**; **1 crore = 10,000,000 = 10 million**. So **1 crore = 10 million**, and **100 crore = 1 billion**. The recurring failure is treating a crore as a million, understating by 10x, or treating 1 crore as 0.1 billion correctly but then mishandling the next conversion.
- Indian filings variously present in `₹ crore`, `₹ lakh`, `₹ million`, or `₹ '000`. **Read the column header on every table, every time** — the unit sometimes differs between the P&L and a note in the same document.
- Indian listed companies increasingly report in `₹ crore` in presentations but `₹ million` or `₹ lakh` in statutory statements. Fix the unit at the point of extraction, not later.
- State the currency explicitly (`INR`, `USD`, `EUR`) — `$` is ambiguous across USD/SGD/HKD/AUD/CAD, and `₹` vs other symbols matters in copy-paste.
- For cross-currency comparison, state the **FX rate and its date**. Never compare a market cap converted at today's rate with earnings converted at an average rate without saying so. For multi-year series, decide and state whether you use period-average or period-end rates, and be consistent.
- Per-share figures: check the **face value** (Indian shares are commonly ₹1, ₹2, ₹5 or ₹10 par) and adjust historic per-share series for **splits and bonus issues**. An unadjusted EPS series with a 1:1 bonus in the middle shows a fake 50% collapse.
- ADR/GDR ratios distort per-share comparison between the local line and the US line.
- Percentages: distinguish **basis points** from percent, and **percentage-point change** from **percent change** (margin moving 10% to 11% is +100 bps, or +10% relative — say which).

Quick conversion table to keep in working memory:

| Indian unit | Numeric | USD-scale equivalent |
|---|---|---|
| 1 lakh | 1e5 | 0.1 million |
| 1 crore | 1e7 | 10 million |
| 100 crore | 1e9 | 1 billion |
| 1,000 crore | 1e10 | 10 billion |
| 1 lakh crore | 1e12 | 1 trillion |

(USD-scale column is unit scale only, not an FX conversion.)

---

## 7. Fiscal-year alignment and period labelling

- **India**: fiscal year runs 1 April to 31 March. "FY25" almost always means the year ended 31 March 2025 — but confirm, because some Indian companies (and most Indian subsidiaries of foreign groups) use December or June year-ends. Quarters: Q1 = Apr-Jun, Q2 = Jul-Sep, Q3 = Oct-Dec, Q4 = Jan-Mar.
- **US/global**: fiscal years vary widely; retailers commonly end in late January/early February, and many companies use 52/53-week years where one year has an extra week (a ~2% distortion to annual growth that management will mention and providers will not).
- Company "FY2025" labels can refer to the year *beginning* or *ending* in 2025 depending on jurisdiction and company convention. When comparing across companies, **convert everything to the calendar period covered** and say so: "year ended Mar-2025" beats "FY25".
- Never compare an Indian FY-ending-March figure with a US calendar-year figure without noting the ~3-month offset, particularly across a macro inflection.
- Indian quarterly results are **limited-review, not audited** (except often Q4, which is derived as full-year audited minus nine months and therefore absorbs all year-end adjustments — Q4 is systematically the noisiest quarter).
- **TTM/LTM figures**: state the exact window ("TTM to Sep-2025"). A TTM built by adding quarters must handle restated prior quarters and any change in consolidation perimeter mid-year.
- Seasonality: compare year-over-year, not sequentially, unless you have established the seasonal pattern from at least three years of the company's own history.

---

## 8. Restatements, reclassifications and discontinued operations

- When the current annual report's prior-year column differs from what that prior report published, the prior year was **restated or reclassified**. Use the latest restated series for trend analysis and note the restatement; using the original numbers creates phantom growth or decline.
- Distinguish innocuous **reclassification** (moving a cost between lines, new segment definitions) from a **correction of error** or **change in accounting policy**, which are disclosed in the notes and are far more serious. Read the note; it says which.
- **Discontinued operations** are presented separately and prior periods are re-presented. Revenue growth computed across the boundary without adjustment is wrong in both directions.
- **Mergers, demergers, slump sales and scheme-of-arrangement effective dates** (common in India, often with retrospective appointed dates) can make one year non-comparable. The scheme details are in the annual report and in exchange filings.
- **Segment redefinitions** typically arrive with a new CEO or a reorganization. When segments change, either rebuild history from the re-presented comparatives the company gives, or start the series fresh — do not splice.
- **Auditor changes** near a restatement deserve scrutiny; check the 8-K Item 4.01 (US) or the exchange filing and the outgoing auditor's stated reason (India).

---

## 9. As-of dates for price, market cap and multiples

- Stamp every price-derived figure with a date and preferably a time: `P/E 28.4x (price as of close 18-Jul-2026)`. Multiples decay the moment the price moves; an undated multiple is a claim with no verifiable content.
- **Market cap** = current price × current fully-diluted-relevant share count. Check the share count against the latest filing, not a stale field: buybacks, QIPs, preferential allotments, ESOP exercises, conversion of warrants/convertibles and rights issues all move it, and aggregators lag.
- Distinguish **basic**, **diluted** and **fully diluted** share counts, and say which you used. For companies with large option pools or outstanding convertibles, the difference is material.
- **Enterprise value** = market cap + debt + minority interest + preferred − cash and equivalents (and, depending on convention, − investments in associates, ± lease liabilities). State your formula. EV comparisons are only valid when everyone in the peer set used the same formula, which is why you should compute the whole peer set yourself.
- Match numerator and denominator periods: a current price over a trailing EPS is a trailing multiple; over a consensus estimate it is a forward multiple, and you must state whose estimate and as of when.
- **Free float** matters in India, where promoter holding is often 50-75%. Market cap overstates the investable base, and low-float names have unreliable price signals.
- For price history, note whether the series is **adjusted for splits, bonuses and dividends** — and remember that total-return series and price series diverge substantially over long horizons in high-dividend sectors.

---

## 10. Common data-provider errors and ambiguous fields

The list below is not about bad vendors; it is about fields that have no single correct definition. Whenever a metric appears here, compute it yourself and state your formula.

| Field | How it goes wrong |
|---|---|
| EBITDA | Some include other income, some exclude; treatment of exceptional items, ESOP cost and post-IFRS 16/Ind AS 116 lease costs varies. Post-lease-standard EBITDA is not comparable to pre-standard EBITDA |
| Operating profit (India usage) | Often quoted as EBITDA excluding other income; screener.in and broker notes may differ from the company's own presentation |
| Net profit / PAT | Before vs after minority interest; before vs after exceptional items; continuing vs total operations |
| ROE / ROCE | Opening, closing or average capital; capital employed with or without cash, CWIP, goodwill, deferred tax; numerator pre- or post-tax. Ranges of 3-5 percentage points arise from definition alone |
| Total debt | Whether short-term borrowings, current maturities of long-term debt, lease liabilities, acceptances/LC-backed trade financing, and preference shares are included. Indian companies frequently carry large **bill discounting / channel financing** that behaves like debt but sits in payables |
| Net debt | Which "cash" counts — some current investments and mutual-fund holdings are cash-like, some are not; restricted cash and margin money should be excluded |
| Cash flow from operations | Interest paid and taxes may be classified in operating, investing or financing under IFRS/Ind AS at the company's choice; that choice makes OCF non-comparable across peers |
| Free cash flow | OCF − capex, but capex may or may not include intangibles, acquisitions, capitalized R&D, capitalized interest and lease payments |
| Working capital days | Computed on revenue vs COGS, on closing vs average balances, on gross vs net receivables. Days differ by 20%+ across conventions |
| Book value / equity | With or without minority interest, revaluation reserves, treasury shares; Indian "net worth" definitions in loan covenants often exclude intangibles |
| Share count | Point-in-time vs weighted average; basic vs diluted; unadjusted for recent corporate actions |
| Dividend yield | Trailing declared vs paid vs ex-date basis; special dividends included or not; India's dividend taxation changed in FY21, breaking older payout series |
| Growth rates | Base-period restatement not applied; 52/53-week years; acquisitions not separated from organic |
| Sector/industry tag | Aggregator classifications are crude. A "diversified" or "trading" tag can hide the actual business. Always read the business description before accepting a peer set |
| Promoter holding / pledge (India) | Pledge quoted as % of promoter holding in one place and % of total equity in another — a 3x-5x apparent difference |
| Market cap | Stale share count; separate listing lines for different share classes counted or omitted |
| "Employees" | Permanent vs contract vs total headcount; Indian filings often disclose only median remuneration and top-earner counts |

Two structural cautions: aggregator ratio history is often recomputed on today's definitions and applied backwards inconsistently; and any field that is blank in the filing may appear as zero (not null) in a provider's data, which then propagates into averages.

---

## 11. Sector-specific sourcing traps

Consistent with the skill's governing principle — the standard ratios are undefined or inverted for several sectors, and so are the standard data sources.

- **Banks and NBFCs**: revenue, EBITDA, EV and net debt are meaningless. Source instead: net interest income and NIM, gross and net NPA, provision coverage, slippage, credit cost, CASA, cost-to-income, capital adequacy (CET1/CRAR). In India these come from the quarterly results filing plus RBI disclosures (Basel III Pillar 3 disclosures are on the bank's own site) and the annual report's "Notes to accounts" disclosures on asset quality, restructuring and write-offs.
- **Insurers**: use premium growth (new business premium, APE), VNB and VNB margin, embedded value (EV) and its movement analysis, solvency ratio, persistency by cohort (13th/61st month), claims ratio and combined ratio for general insurers. Sources: IRDAI monthly business data, the insurer's EV disclosure and actuarial report.
- **REITs / InvITs**: net income is depreciation-distorted. Use NOI, FFO/AFFO, distribution per unit, occupancy, WALE, loan-to-value, cap rates. Sources: the trust's quarterly distribution statements, valuer reports (Indian REITs publish independent valuations semi-annually), SEBI REIT/InvIT disclosures.
- **Miners, oil and gas**: source reserves and resources from the technical reports that follow a recognized code (JORC, NI 43-101, SEC S-K 1300, SPE-PRMS) — not from the annual report summary. Track reserve life, grade, all-in sustaining cost, and note that reserve estimates are price-dependent and get restated when commodity prices move.
- **Utilities, infrastructure, telecom (India)**: regulated returns, tariff orders and licence conditions come from CERC/SERCs, TRAI, NHAI concession agreements. Contingent liabilities and disputed regulatory dues are often the dominant balance-sheet item.
- **Pharma**: USFDA inspection classifications (EIR, Form 483, warning letters, import alerts) are on the FDA site and are material events; ANDA/DMF filings, Paragraph IV status and patent cliffs come from company disclosures and FDA Orange Book.
- **Early-stage / loss-making / platform businesses**: the operating KPIs (GMV, take rate, contribution margin, cohort retention, CAC payback) exist only in investor presentations and calls, are management-defined, and change definition between quarters. Record the definition alongside the number and re-check it each quarter.

---

## 12. When web access is unavailable or data is paywalled

You will frequently be asked to analyse with incomplete access. Handle it explicitly rather than by inference. The document-first principle still applies: incomplete access means fewer documents, not a licence to substitute aggregator data.

**Sequence:**
1. **Establish what you actually have.** Documents the user supplied, figures stated in the conversation, and your own general knowledge of the sector and its economics — which is durable — as distinct from company-specific figures, which are not.
2. **Ask the user for the documents themselves, naming them specifically.** Not "can you give me more data" but "please upload the FY25 annual report PDF, the last two concall transcripts, and the latest quarterly results filing from BSE." Named document requests get answered; vague ones do not. If you know the exact source (`bseindia.com` Corporate Filings, the company's IR page, EDGAR filing index) say where to get it. **Do not ask for or accept pasted screener.in tables or aggregator screenshots as a substitute for the document** — if the user provides aggregator data, accept it but mark every figure as `aggregator-sourced, unverified` and continue requesting the actual documents.
3. **Work from provided documents rigorously.** Extract with page/section citations so the user can audit you. If a supplied document is a screenshot or partial page, note what was cut off.
4. **State gaps explicitly and place them in the output.** Maintain a visible "Data gaps and their effect on this analysis" section: what is missing, why it matters, and which conclusions would change if the missing data went one way or the other.
5. **Downgrade the conclusion, not the honesty.** Say what the analysis can support at the available evidence level: structural and qualitative conclusions may hold firmly even when precise valuation does not. "On the available data, the business model and competitive position support X; the valuation question cannot be answered without the current share count and net debt" is a complete, useful answer.
6. **Never substitute a remembered or plausible number for a missing one.** Model knowledge of specific company financials is stale by construction, is often wrong at the level of precision that matters, and cannot be cited. If you genuinely recall an approximate figure, present it as an unverified recollection with an explicit uncertainty band and an instruction to verify, or omit it.
7. **Do not launder a guess through arithmetic.** Deriving a metric from an assumed input produces a figure that looks sourced and is not. If an input is assumed, label the output as scenario-based and show the assumption on its face.

**Paywalled specifically:** rating rationales, DRHPs, exchange filings, EDGAR, IRDAI and RBI data and most company IR pages are free — exhaust these before concluding that data is unavailable. What is genuinely paywalled is usually consensus estimates, historical databases, full rating reports and specialist industry data. Say which class of data you are missing, because "no consensus estimate available" and "no financial statements available" are very different constraints.

---

## 13. Never fabricate

State this as a hard rule with no exception clause: **do not produce a company-specific figure you have not sourced.**

The reason is asymmetric cost. An analysis with three acknowledged gaps still helps the reader — they know exactly where to look and exactly how much to trust each part. An analysis with one invented figure is worse than no analysis, because the reader cannot tell which figure is invented, so the entire document loses its evidentiary status. Worse, invented precision is self-reinforcing: a fabricated revenue figure produces a fabricated margin, a fabricated multiple and a fabricated conclusion, all internally consistent and all wrong.

Specific failure modes to avoid:
- Filling a table cell because the table has a column for it. Write `n/a — not disclosed` or `not sourced`.
- Converting a qualitative recollection ("margins are around the mid-teens") into a number in a table.
- Producing a peer-comparison table where some rows are sourced and some are estimated, without marking which.
- Interpolating a missing year in a time series without labelling it as interpolated.
- Quoting a multiple without a price date, which is a fabrication of currency even when the arithmetic was once right.
- Attributing a statement to a concall or filing you did not read.

Preferred vocabulary in output: `not disclosed`, `not sourced — verify`, `single source, unverified`, `estimated by me from [inputs] — not a company figure`, `as of [date]`.

---

## Checklist

- [ ] Every figure carries value + unit + basis (consolidated/standalone) + period + source.
- [ ] Headline figures (revenue, EBITDA, PAT, debt, equity, OCF, share count) cross-checked against a second independent source.
- [ ] Primary filing beats aggregator wherever they disagree; discrepancy investigated, not averaged.
- [ ] Consolidated used throughout; no ratio mixes consolidated and standalone; PAT is post-minority-interest.
- [ ] Units confirmed on every table read — crore vs lakh vs million; 1 crore = 10 million.
- [ ] Currency stated; FX rate and its date stated for any cross-currency comparison.
- [ ] Fiscal periods converted to calendar coverage; India FY ends 31 March; 52/53-week years noted.
- [ ] Prior-year figures checked for restatement, reclassification, discontinued operations and scheme effective dates.
- [ ] Price, market cap and all multiples stamped with an as-of date; share count taken from the latest filing.
- [ ] Derived ratios recomputed by me from raw line items, with formulas stated.
- [ ] Per-share history adjusted for splits and bonuses.
- [ ] India: shareholding pattern, promoter pledge trend, CARO qualifications, contingent liabilities, related-party note, latest rating rationale and rating history all reviewed.
- [ ] Global: 10-K MD&A and segment note, latest 8-Ks, DEF 14A compensation metrics and recent Form 4 activity reviewed.
- [ ] Latest concall/earnings-call Q&A read; prior guidance checked against delivery.
- [ ] Sector-appropriate sources used — banks, insurers, REITs, miners do not use the standard ratio set or the standard sources.
- [ ] Arithmetic sanity checks passed: statements tie, balance sheet balances, per-unit economics plausible.
- [ ] Single-sourced and unverified figures explicitly flagged as such.
- [ ] A visible "Data gaps" section exists wherever access was incomplete.
- [ ] Zero fabricated figures. Every cell is sourced, marked `n/a`, or explicitly labelled as my own estimate.
