# Accounting Standards, Comparability and Data Integrity

Use this when: you are about to put two or more companies in the same table, or chart one company across a period in which a standard, a currency, a year-end or a share count changed.

Every relative conclusion in this skill rests on an unstated assumption — that the numbers on both sides of the comparison mean the same thing. They usually do not. Reporting framework, lease convention, gross-versus-net revenue, cost classification, consolidation scope, fiscal calendar and currency all move headline ratios by more than the differences in business quality you are trying to detect. This file is the pre-processing layer: establish that the inputs are comparable, or state explicitly that they are not and by how much. A comp table built on uncorrected accounting differences ranks accounting policy, not businesses — the same failure mode as ranking a sector on OPM alone.

## Contents

- [1. The comparability gate — record the framework before anything else](#1-the-comparability-gate--record-the-framework-before-anything-else)
- [2. The break-list: which differences actually move ratios](#2-the-break-list-which-differences-actually-move-ratios)
- [3. Inventory costing — LIFO vs FIFO/weighted average](#3-inventory-costing--lifo-vs-fifoweighted-average)
- [4. Development cost capitalisation vs expensing](#4-development-cost-capitalisation-vs-expensing)
- [5. Leases — IFRS 16 / Ind-AS 116 vs ASC 842](#5-leases--ifrs-16--ind-as-116-vs-asc-842)
- [6. Building lease-neutral EBITDA and lease-inclusive debt](#6-building-lease-neutral-ebitda-and-lease-inclusive-debt)
- [7. Revenue recognition — gross vs net (principal vs agent)](#7-revenue-recognition--gross-vs-net-principal-vs-agent)
- [8. Percentage-of-completion, contract assets and variable consideration](#8-percentage-of-completion-contract-assets-and-variable-consideration)
- [9. Cost classification — COGS vs SG&A vs other income](#9-cost-classification--cogs-vs-sga-vs-other-income)
- [10. Consolidation scope, minorities and associates](#10-consolidation-scope-minorities-and-associates)
- [11. Goodwill, PPA and acquired-intangible amortisation](#11-goodwill-ppa-and-acquired-intangible-amortisation)
- [12. Restatements, prior-period errors and re-presentation](#12-restatements-prior-period-errors-and-re-presentation)
- [13. Transition method and the adoption-year break](#13-transition-method-and-the-adoption-year-break)
- [14. Fiscal-year misalignment and TTM reconstruction](#14-fiscal-year-misalignment-and-ttm-reconstruction)
- [15. Currency — presentation, functional and translation](#15-currency--presentation-functional-and-translation)
- [16. Constant-currency and organic-growth reconciliation](#16-constant-currency-and-organic-growth-reconciliation)
- [17. Deferred tax, effective tax rate and tax-regime differences](#17-deferred-tax-effective-tax-rate-and-tax-regime-differences)
- [18. Non-GAAP figures and the quality of the adjustments](#18-non-gaap-figures-and-the-quality-of-the-adjustments)
- [19. Symmetric normalisation of one-offs and cycle](#19-symmetric-normalisation-of-one-offs-and-cycle)
- [20. Share count, dilution and per-share integrity](#20-share-count-dilution-and-per-share-integrity)
- [21. Data-provider field definitions and error patterns](#21-data-provider-field-definitions-and-error-patterns)
- [22. The cash-flow reconciliation integrity check](#22-the-cash-flow-reconciliation-integrity-check)
- [23. Sector gate — where comparability is a different language](#23-sector-gate--where-comparability-is-a-different-language)
- [24. The comparability worksheet you must produce](#24-the-comparability-worksheet-you-must-produce)
- [Checklist](#checklist)

---

## 1. The comparability gate — record the framework before anything else

Open the basis-of-preparation note (first note to the accounts) and the audit report, and record the **exact** framework for every company in the set — not "IFRS-ish". The distinctions that matter:

| Framework | Where you meet it | What to remember |
|---|---|---|
| IFRS as issued by the IASB | Most non-US listings, many 20-F filers | The reference dialect |
| EU-endorsed IFRS | EU issuers | Endorsement lag and occasional carve-outs |
| US GAAP | 10-K/10-Q filers on EDGAR | LIFO allowed, R&D expensed, ASC 842 dual-model leases |
| **Ind-AS** (India) | Listed Indian companies, Schedule III Division II | IFRS-converged **with carve-outs** — a third dialect, not IFRS |
| Indian GAAP (I-GAAP) | Indian filings before the Ind-AS transition; small unlisted subsidiaries | Not comparable to Ind-AS; hard series break |
| J-GAAP / PRC GAAP / other local GAAP | Japan, China A-shares, several EMs | Goodwill amortisation, different consolidation practice |

Cross-checks worth two minutes each:

- **ADRs and 20-F filers:** a 20-F may be prepared under IFRS with **no** US GAAP reconciliation. Do not assume a US listing means US GAAP numbers.
- **India:** every listed Indian company publishes **standalone and consolidated** statements. Use consolidated unless you are explicitly analysing the parent; mixing the two across years is one of the most common silent errors in Indian data.
- **India — Ind-AS carve-outs that change numbers:** bargain-purchase gains go to capital reserve via OCI rather than the P&L; investment property is carried at **cost only** (fair value disclosed in a note); a first-time-adoption option allows continued capitalisation of exchange differences on long-term foreign-currency monetary items; foreign-currency convertible bonds may be equity-classified where IFRS would create a derivative liability.

**Why it matters:** EV/EBITDA, ROCE, net debt/EBITDA, gross margin and P/S are not defined identically across these dialects. If the framework column is missing from your comp sheet, every ranking downstream is partly a ranking of accounting policy.

---

## 2. The break-list: which differences actually move ratios

Not all GAAP differences are worth your time. These are the ones large enough to change a conclusion, ordered roughly by how often they do:

| Difference | IFRS / Ind-AS | US GAAP | Metrics it corrupts |
|---|---|---|---|
| Operating leases | On balance sheet; rent split into D&A + interest | Dual model; operating lease stays a single operating cost | EBITDA, EBIT, net debt, EV/EBITDA, ROCE, interest cover |
| Inventory costing | LIFO prohibited | LIFO permitted | Gross margin, inventory days, asset turnover, ROCE, cash tax |
| Development costs | Capitalised when IAS 38 criteria met | Mostly expensed (narrow software/cloud exceptions) | EBIT, EBITDA, CFO, capex, FCF, invested capital |
| Impairment reversal | Permitted (not goodwill) | Prohibited | Asset base, depreciation, later-year earnings |
| PPE revaluation | Revaluation model permitted | Cost only | Equity, D&A, ROE, ROCE, P/B |
| Defined-benefit pensions | Net interest on net liability; remeasurements to OCI | Expected return on plan assets in P&L | Operating and net margin, EPS |
| Interest/dividends in cash flow | Policy choice of section | Largely fixed | CFO, FCF, FCF yield |
| Goodwill | Impairment-only | Impairment-only (public); amortisation alternative elsewhere | EBIT, ROCE, book value |
| Bargain purchase gain | **Ind-AS:** capital reserve. IFRS: P&L | P&L | Reported PAT in acquisition years |
| Investment property | IAS 40 fair-value model permitted (**Ind-AS: cost only**) | Cost | Real-estate earnings, book value, P/B |

Use this as a triage list: identify the two or three rows that are live for the peer set in front of you and fix those. Do not attempt a full GAAP-to-GAAP conversion — it is not achievable from public data, and the residual noise is smaller than the errors you would introduce.

---

## 3. Inventory costing — LIFO vs FIFO/weighted average

**What to do.** For US filers, read the inventory note for the **LIFO reserve** (the FIFO-minus-LIFO difference) and for any **LIFO liquidation** disclosure. Restate to a FIFO basis before comparing to IFRS or Ind-AS peers:

- Inventory (FIFO) = reported inventory + LIFO reserve
- Equity (FIFO) = reported equity + LIFO reserve × (1 − tax rate)
- COGS (FIFO) = reported COGS − increase in LIFO reserve during the year
- Deferred tax liability increases by LIFO reserve × tax rate; net debt is unchanged

**Why.** In an inflationary period LIFO charges newer, higher costs to COGS. The US filer shows a lower gross margin, a smaller inventory balance and a lower cash tax bill than an economically identical IFRS peer — so it looks less profitable *and* more capital-efficient at the same time, and asset turnover, inventory days and ROCE comparisons are all meaningless. A **LIFO liquidation** (selling old, cheap layers) does the reverse: a non-repeatable gross-margin gain, to be stripped under §19.

**India:** LIFO is prohibited under Ind-AS 2, as under IFRS. The Indian check is different — confirm the cost formula (FIFO vs weighted average), overhead absorption at abnormal capacity, and the basis of net-realisable-value write-downs in the inventory note.

---

## 4. Development cost capitalisation vs expensing

**What to do.** Pull, from the intangibles note and the investing section of the cash flow statement: additions to internally generated intangibles, the amortisation charged on them, the carrying value of assets under development, and total R&D spend from the expense note or MD&A. Compute:

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Capitalisation rate | Capitalised development ÷ total R&D spend | Low and *stable*; a rising trend is the signal | A rate drifting upward converts current cost into a future asset — the cheapest way to buy margin |
| Capitalised dev ÷ EBIT | Annual capitalised additions ÷ EBIT | Material above ~10% | Sizes the EBIT overstatement versus a full-expensing peer |
| Amortisation ÷ capitalised additions | Yearly amortisation ÷ additions | Approaching 1.0 in steady state | Persistently below 1.0 means the asset balance is inflating; write-off risk builds |

*Indicative ranges vary by market, cycle and period; the company's own history and the peer median override any absolute band.*

**The common baseline.** The only reliably comparable treatment across an IFRS/Ind-AS and US GAAP peer set is to **expense everything**: reduce EBIT/EBITDA by capitalised additions, add back the related amortisation, reduce CFO by the same additions (they sit in investing), and remove the intangible from invested capital. Do it for every member of the set, including the ones that already expense (where the adjustment is zero), and state that you did.

**Why.** Capitalisation simultaneously inflates EBIT, EBITDA, CFO *and* invested capital, and deflates capex-adjusted FCF. It is the single largest comparability gap in pharma, software, autos and engineering peer sets, and a well-worn earnings-management lever — capitalising in bad years, writing off in a "kitchen sink" year.

---

## 5. Leases — IFRS 16 / Ind-AS 116 vs ASC 842

Confirm the convention for each company, then extract the same five items from every one: right-of-use asset, lease liability (current + non-current), ROU depreciation, lease interest, and the undiscounted maturity table with the discount rate.

| | IFRS 16 / Ind-AS 116 | ASC 842 operating lease | ASC 842 finance lease |
|---|---|---|---|
| Balance sheet | ROU asset + lease liability | ROU asset + lease liability | ROU asset + lease liability |
| Income statement | Depreciation + interest | **Single operating lease cost** (straight-line) | Depreciation + interest |
| EBITDA effect | **Inflated** (rent removed) | None | Inflated |
| Reported debt in most screeners | Often excluded from "total debt" despite being a liability | Excluded | Sometimes included |
| Cash flow classification | Principal in financing → **CFO inflated** | Entirely in operating → CFO unaffected | Principal in financing |

**Why.** For a lease-heavy business the difference is not cosmetic: retail, airlines, telecom towers, hotels, QSR, hospitals, diagnostics and 3PL logistics can see EBITDA move by tens of percent and reported debt by a multiple of pre-lease net debt. An unadjusted EV/EBITDA screen ranks the IFRS lessee as cheap and the US operating lessee as expensive, purely because of where rent sits. IFRS 16 also inflates CFO because only the interest portion stays in operating — so FCF-based screens are corrupted in the same direction.

**Watch the discount rate.** The incremental borrowing rate is management's estimate. A low rate inflates the ROU asset and liability and back-loads interest; compare the disclosed rate to the company's own marginal borrowing cost and to peers. A rate materially below the bond curve is a soft red flag and distorts the liability you are about to add to net debt.

---

## 6. Building lease-neutral EBITDA and lease-inclusive debt

Compute **both** conventions across the *entire* peer set, then pick one, apply it to everyone, and say which you used. Never mix.

**Convention A — pre-IFRS 16, "everyone pays cash rent" (EBITDAR-style, then deduct rent).** Best for operating comparisons and margin trends across the transition year.

- For IFRS/Ind-AS filers: EBITDA(A) = reported EBITDA − cash lease payments (principal + interest from the cash flow statement), i.e. remove the rent benefit.
- For US operating-lease filers: EBITDA(A) = reported EBITDA (already after rent).
- Net debt(A) = interest-bearing debt only; exclude all lease liabilities from both sides.
- Capital employed(A) excludes ROU assets.

**Convention B — fully capitalised, "all leases are debt".** Best for leverage, credit and EV work.

- EBITDA(B) = EBITDA before all lease costs (add back rent for US operating lessees; IFRS filers already exclude it).
- Net debt(B) = interest-bearing net debt + lease liability. For US operating leases, use the reported ASC 842 operating lease liability where available; if you must estimate, use the present value of the disclosed maturity table at the company's marginal borrowing rate. A crude 8× rent multiple is a last resort — say so if you use it.
- Capital employed(B) includes ROU assets; EV includes lease liabilities.

| Ratio | Restate under | Why |
|---|---|---|
| EV/EBITDA | B (EV and EBITDA both lease-inclusive) | The only internally consistent lease treatment for a multiple |
| Net debt/EBITDA | B, and report A alongside | Rating agencies and covenants differ; a turn of leverage is a rating notch |
| Interest cover | B: EBITDA(B) ÷ (interest + lease interest) | Rent is a fixed charge whether or not GAAP calls it interest |
| ROCE | Include ROU assets in capital employed when using B | Omitting them flatters a lease-heavy retailer's ROCE |
| EBITDA margin trend across the transition year | A | Otherwise the adoption year shows a fake margin expansion |

**Why this matters more than it looks.** Leverage screens, covenant headroom and "cheapness" all shift by turns of EBITDA depending on convention. Most screeners exclude lease liabilities from "total debt" — meaning a lease-heavy IFRS retailer can appear both high-EBITDA and low-debt in the same row. That is not an opportunity; it is a definition.

---

## 7. Revenue recognition — gross vs net (principal vs agent)

**What to do.** Read the revenue note (IFRS 15 / ASC 606 / Ind-AS 115) and answer one question: does the company book gross transaction value or only its commission? Then triangulate — disclosed take rate × GMV should reconcile to net revenue; revenue per employee, receivable days and gross margin should look like the business model you think it is.

High-risk models: marketplaces and aggregators, travel, ticketing, distributors and stockists, telecom handset bundles, ad-tech and media resellers, EPC contractors with pass-through equipment, pharma CDMO with customer-supplied materials, and commodity traders.

**Why.** Two identical marketplaces can report revenue differing by an order of magnitude. Every P/S, EV/Sales, revenue-growth, revenue-per-employee and gross-margin comparison collapses if one books gross and the other net. A **change** in presentation between years is worse: it manufactures apparent revenue growth or margin expansion with zero economic change, and screeners rarely flag it.

**Tell-tale signs to search for:** "principal versus agent", "gross versus net", "reclassification of revenue", a gross margin that jumps by many points with no cost story, or revenue growth wildly out of line with volume/GMV disclosures.

**India note.** The introduction of GST in July 2017, combined with Ind-AS 115, removed excise duty from reported revenue for manufacturers. Reported revenue for affected companies fell by a high single-digit to low double-digit percentage with **no economic change**, and margins on revenue rose correspondingly. Any Indian revenue series or margin chart spanning FY2017–FY2018 must be flagged; never compute a CAGR straight across it without restating the earlier years net of excise.

---

## 8. Percentage-of-completion, contract assets and variable consideration

For construction, EPC, defence, capital goods, shipbuilding and long-cycle software, revenue is an estimate, not an event.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Unbilled revenue ÷ revenue | Contract assets ÷ trailing revenue | Stable; a rising multi-year trend is the signal | Rising unbilled means revenue recognised ahead of the customer's agreement to pay |
| Contract liabilities ÷ revenue | Advances and deferred revenue ÷ revenue | Healthy when high and rising in advance-funded models | Customer-funded working capital; a fall can precede an order drought |
| (Receivables + unbilled) days | (Trade receivables + contract assets) ÷ revenue × 365 | Compare to peers and own history only | The honest working-capital number in POC businesses |
| Cost-to-complete revisions | Disclosed changes in estimates ÷ segment EBIT | Small and two-sided | Recurring favourable revisions are a margin-smoothing footprint |

*Indicative ranges vary by market, cycle and period; peer median and the company's own history override any absolute band.*

**What to read:** the method of measuring progress (input/cost-to-cost vs output/milestone), disclosures on variable consideration, claims and incentives and the constraint applied to them, onerous-contract provisions, and the order-book-to-revenue conversion commentary.

**Why.** A rising unbilled-to-revenue ratio is a leading indicator of optimistic cost-to-complete assumptions and future write-backs. It also makes revenue non-comparable against a peer recognising on delivery or milestones. **India:** real-estate developers moved from percentage-of-completion to completed-contract on Ind-AS 115 adoption; developer revenue and profit series are not continuous across that transition, and lumpy project completions dominate any single year.

---

## 9. Cost classification — COGS vs SG&A vs other income

**Gross margin is among the least comparable metrics in existence.** A company that puts depreciation, inbound freight, warehousing and direct labour in COGS will show a gross margin many points below an economically identical peer that puts them in SG&A. Ranking a sector on gross margin without checking classification produces a spurious ordering — exactly the single-metric failure this skill exists to prevent.

**What to do:**

1. Determine whether the P&L is presented **by nature** (material cost, employee benefits, other expenses — the IFRS/Schedule III convention) or **by function** (COGS, SG&A, R&D — the US convention). They are not mechanically convertible from the face of the statement.
2. For each company, locate: depreciation, freight and distribution, R&D, share-based compensation, warranty, warehousing, and royalty. Note which line each sits in.
3. Rebuild the comparison at **EBITDA and EBIT**, where most classification differences wash out. If you must use gross margin, define it yourself identically for every peer and say what you included.
4. Check "other income": is it treasury income, scrap sales, government incentives, forex, or genuine operating income? Indian filers routinely park operating items there.

**India specifics.** Schedule III has **no gross profit line** — construct it as revenue from operations less (cost of materials consumed + purchases of stock-in-trade + changes in inventories), and apply that identical definition to every peer. "OPM" in Indian screeners and concalls means **EBITDA margin excluding other income**; a US "operating margin" means EBIT margin. Government incentives (PLI and state subsidies) may appear as other operating revenue for one company and as a credit netted against cost for another — same economics, different margin. See `03-earnings-quality.md` §1 and §3.

---

## 10. Consolidation scope, minorities and associates

**What to check.** For each material subsidiary and JV: fully consolidated, equity-accounted, or (in older data and some JV-heavy sectors) proportionately consolidated. Reconcile net income attributable to owners against total net income and compute the minority share. Look for structured entities, ESOP trusts, SPVs in infrastructure, and off-balance-sheet JVs.

**Why.** A company with 60%-owned operating subsidiaries consolidates **100%** of revenue and EBITDA but owns **60%** of the earnings. If EV is not grossed up for minority interest, EV/EBITDA looks artificially cheap — a systematic distortion in Indian infrastructure, hospitals, cement and telecom-tower structures, and in Korean and Japanese group companies. Conversely, a peer running the identical business through equity-accounted JVs reports almost no revenue at all and looks tiny on EV/Sales.

**Consistency rules for the EV bridge (apply to every peer identically):**

- Add minority interest to EV — at market value where the sub is separately listed, otherwise at an implied multiple, not book value, and say which.
- Subtract the value of equity-accounted investments from EV **only if** their earnings are excluded from the EBITDA denominator. Never subtract the investment *and* keep the associate profit in the numerator metric.
- Where a listed subsidiary or holding structure dominates, switch to the sum-of-the-parts and holdco approach in `13-situations.md` rather than forcing a multiple.
- Check whether the peer's consolidation scope changed mid-year (acquisition/divestment): part-year consolidation makes growth and margin non-comparable until the anniversary.

---

## 11. Goodwill, PPA and acquired-intangible amortisation

**What to check.** Whether goodwill is amortised (some local GAAPs; the US private-company alternative) or impairment-tested only (IFRS, Ind-AS, US GAAP public). For recent acquisitions, pull the **purchase price allocation**: how much went to goodwill versus amortisable intangibles (customer relationships, brands, technology), and the useful lives assigned. Then compute acquired-intangible amortisation as a share of EBIT, and ROIC both including and excluding goodwill.

**Why.** An acquisitive company carries a PPA amortisation drag that an organic peer does not, while goodwill inflates its capital base and depresses ROCE. Unadjusted EBIT comparisons therefore penalise acquirers and flatter organic peers arbitrarily — and adding back all intangible amortisation (the standard non-GAAP move) flatters acquirers just as arbitrarily, because the acquired customer relationships genuinely do decay. The defensible treatment: report both, and judge whether maintenance spend on the acquired asset is already inside opex (if yes, the add-back is more justifiable; if no, it is not).

**Red flags:** an allocation overwhelmingly to goodwill (defers all cost recognition), useful lives far above the peer norm, goodwill never impaired through a demonstrable downturn, or a single cash-generating-unit structure that lets a strong business shelter a failing acquisition from impairment testing. Cross-reference `07-forensic-red-flags.md` for the serial-acquirer pattern.

---

## 12. Restatements, prior-period errors and re-presentation

**How to detect one without being told.** Put last year's annual report next to this year's and compare the **comparative** column line by line. Any difference is a restatement, a reclassification, or a discontinued-operations re-presentation. This mechanical check finds restatements that were never announced as such.

**What to search for:** "restated", "reclassified", "prior period error", "Ind-AS 8" / "IAS 8", "revision to previously issued financial statements", and in the US, an **Item 4.02 8-K** (non-reliance on previously issued statements). In India, also check exchange filings for revised results, auditor qualifications carried into the next year, and any NFRA or SEBI action.

**Classify what you find** — the four types have very different meanings:

1. **Error correction / non-reliance** — a governance event. Among the strongest standalone predictors of further negative surprises. Treat as a hard flag, not a data-cleaning task.
2. **Voluntary accounting policy change** — read the justification; policy changes that raise reported profit deserve scepticism.
3. **Discontinued operations re-presentation** — benign, but it silently rebases historical revenue and margin; your prior-year series must be re-pulled.
4. **Business-combination measurement-period adjustment** — mechanical, but it moves goodwill and PPA amortisation retrospectively.

**Why it matters for data integrity.** Providers commonly store the **originally reported** figure for old years and the **restated** figure for recent ones. Multi-year growth rates and CAGRs computed across that seam are arithmetic nonsense, and the corruption is invisible in the output. When a restatement exists, rebuild the series from filings for the affected years.

---

## 13. Transition method and the adoption-year break

For every new standard adopted in your window (IFRS 16 / Ind-AS 116, IFRS 15 / Ind-AS 115, IFRS 9 / Ind-AS 109, ASC 842 / 606 / 326 CECL, IFRS 17), determine the transition method:

- **Full retrospective** — comparatives restated; the series is continuous.
- **Modified retrospective / cumulative catch-up** — comparatives **not** restated; a plug goes to opening retained earnings. The adoption year is a hard break, and growth, margin and leverage computed across it are meaningless.

Mark the transition year on every chart you build and in any table spanning it.

**India — the series breaks you will actually hit:**

| Break | Effect on the series |
|---|---|
| I-GAAP → Ind-AS (phased from FY2017 for larger companies, FY2018 for the rest) | Pre-transition years are a different framework. Long-run charts crossing this point mix two GAAPs. |
| GST / excise removal from revenue (FY2018) | Reported revenue steps down for manufacturers with no economic change (§7). |
| Ind-AS 115 for real estate (POC → completed contract) | Developer revenue and PAT series discontinuous and lumpy thereafter. |
| Ind-AS 116 leases (FY2020) | EBITDA and reported debt step up for lease-heavy sectors. |
| Section 115BAA tax election (from FY2020) | Statutory rate step-down plus one-off deferred-tax remeasurement (§17). |

**US/global equivalents:** ASC 606 (2018-19), ASC 842 (2019), CECL for lenders (2020-23 phased), IFRS 17 for insurers (2023) — IFRS 17 in particular broke the entire historical earnings series for insurers; do not chart through it.

---

## 14. Fiscal-year misalignment and TTM reconstruction

Record every company's fiscal year-end. Common patterns: **India and Japan 31 March**; many US retailers a **52/53-week year** ending late January/early February; Australia and several others 30 June; most of the rest 31 December.

**Rules:**

- If year-ends differ by **more than one quarter**, do not compare annual figures — rebuild a **trailing-twelve-month** series from quarterly data so every company covers the same calendar window, and state the window explicitly ("TTM to 30 June 2026").
- Beware the **label collision**: an Indian "FY25" means the year ended March 2025; a US "FY2025" often means calendar 2025. Comparing them offsets the economic period by nine to twelve months.
- Flag **53-week years** (an extra ~2% of trading in retail) and remove the extra week before computing growth.
- Flag **stub / transition periods** when a company changes its year-end — a 9-month or 15-month "year" destroys every ratio computed on it.
- **India:** quarterly results under SEBI LODR are limited-reviewed, not audited, and **Q4 is a balancing figure** (audited full year minus the three reviewed quarters). True-ups cluster there, so a TTM built through a Q4 inherits them. See `03-earnings-quality.md`.

**Why.** A one-quarter offset is enough to place two companies on opposite sides of a commodity move, a rate cycle or a demand shock — making one look like a share-gainer when it is merely earlier in the calendar.

---

## 15. Currency — presentation, functional and translation

**What to identify:** the presentation currency, the functional currency of the major operating subsidiaries, the translation method (current-rate: assets/liabilities at closing rate, P&L at average rate, difference to OCI as the cumulative translation adjustment), and whether any subsidiary sits in a hyperinflationary economy requiring IAS 29 / Ind-AS 29 restatement. Check whether the company **changed** its presentation currency in the period — this silently rebases the entire history.

**Conversion rules when comparing across currencies (get these wrong and you inject percentage-point errors):**

- Income statement and cash flow items → **average rate** for the period.
- Balance sheet items → **closing rate** at the period end.
- Never apply today's spot rate to historical years — it destroys the growth series by re-denominating each year at a rate it never traded at.
- Ratios that are currency-on-currency (margins, turnover, leverage, ROCE) need **no** conversion. Convert only when comparing absolute size, EV, or per-share values.
- **India:** figures are in **₹ crore** (1 crore = 10 million) or **₹ lakh** (1 lakh = 0.1 million). Unit errors between crore, lakh, million and billion are the single most common arithmetic failure in cross-market work. Restate everything to one unit at the point of extraction and label the column.

**Where the FX distortion shows up:** read the CTA balance in equity (a large and growing CTA means a big translation exposure) and the FX gain/loss line in the P&L (transaction exposure, often on foreign-currency debt — this is a financing item, not operating performance, and must be normalised out under §19).

---

## 16. Constant-currency and organic-growth reconciliation

Find management's bridge from reported growth to organic/constant-currency growth: **FX · acquisitions · divestments · scope and accounting changes · extra trading week**. If it is not disclosed, rebuild it yourself from segment and acquisition disclosures.

**Verify, do not accept:**

- Acquisitions are excluded from "organic" for the full **12-month anniversary**, not just the stub period.
- Divestments are removed from the **base year** too, not only the current one.
- Constant currency uses prior-year average rates applied to current-year local results — not closing rates.
- The definition did not change between years (it often does, always in a flattering direction).

**Why.** "Organic" is an unaudited, company-defined term. Without a like-for-like bridge you cannot distinguish execution from a currency tailwind or from debt-funded bolt-on M&A — and those three deserve completely different multiples. A company whose entire growth premium is FX will de-rate the moment the currency turns, and one whose growth is acquisition-funded is buying its growth with the balance sheet you are also valuing.

---

## 17. Deferred tax, effective tax rate and tax-regime differences

**What to do.** Reconcile the effective tax rate to the statutory rate using the tax note, and identify the drivers: tax holidays and incentive regimes, geographic mix, unrecognised deferred tax assets, prior-year settlements, and one-off remeasurements. Then form a view on the **sustainable** rate and use it in normalised earnings.

| Check | How | Why it matters |
|---|---|---|
| ETR vs statutory rate | Tax note reconciliation, 5 years | A persistent gap must have a named, dated cause — holidays expire |
| Cash tax vs P&L tax | Tax paid in the cash flow statement ÷ PBT | A large persistent gap points to capitalisation, accelerated depreciation, or aggressive positions |
| Deferred tax asset recognition | DTA note; unrecognised losses | Recognising a DTA on carried-forward losses creates non-cash profit; US GAAP uses valuation allowances, IFRS a single probability model |
| Rate-change remeasurement | One-off tax line in the year of a statutory change | Non-repeatable; strip from normalised earnings both ways |

**Why it matters for comparability.** Cross-border comparisons on net margin, ROE and P/E are dominated by tax regime, not operating performance. Compare at **EBIT/EBITDA**, or normalise every peer to a sustainable tax rate, before drawing a bottom-line conclusion. Presentation also differs: IFRS/Ind-AS classify all deferred tax as non-current, and IFRS has no valuation-allowance mechanic.

**India:** the concessional regime under section 115BAA (from FY2020) produced both a permanent step down in the statutory rate and a **one-off deferred-tax and MAT-credit remeasurement** in the year of election. Any margin or EPS series crossing that point contains a policy step and a one-off; separate them. Also check SEZ / export-incentive holidays with known expiry dates — an IT or pharma peer enjoying a holiday that lapses next year has a structurally rising tax rate that the trailing P/E does not show.

---

## 18. Non-GAAP figures and the quality of the adjustments

**Reconcile every "adjusted" number back to the statutory number**, then tabulate the add-backs by type and by year.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Adjusted-to-statutory gap | (Adjusted PAT − reported PAT) ÷ reported PAT | Small and non-recurring | A persistent gap is a measurable governance signal |
| Cumulative add-backs ÷ cumulative reported profit | Sum over 5–10 years | Well under a fifth of profit | Sizes how much of "earnings power" is a management assertion |
| Recurrence count | Consecutive years each "one-off" item appears | 1, occasionally 2 | Restructuring in five straight years is an operating cost with a euphemism |
| SBC ÷ revenue and SBC ÷ EBITDA | From the cash flow statement or the SBC note | Compare to sector, not absolute | SBC is a real cost of labour; adding it back overstates margin and, with buybacks, hides dilution |

*Indicative ranges vary by market, cycle and period; peer and own-history comparison overrides any absolute band.*

**Rules of thumb worth defending:** never accept an add-back for share-based compensation; treat recurring restructuring as operating cost; treat acquired-intangible amortisation as an adjustment you report **both ways** (§11); treat "one-off" litigation as recurring if the company is structurally litigious.

**India:** the equivalent is the **exceptional items** line under Schedule III (which sits between "profit before exceptional items and tax" and PBT) — there is no direct US analogue. Read the note behind it every year and track how often it is populated. Companies also present "adjusted EBITDA" in investor presentations that reconciles to nothing in the audited statements; use the statutory figures and rebuild adjustments yourself.

---

## 19. Symmetric normalisation of one-offs and cycle

Build a normalised earnings series by removing, **with identical rigour in both directions**:

- Gains: asset and stake sale gains, insurance recoveries, tax settlements in the company's favour, write-backs of provisions, bargain purchase gains, fair-value gains on investments, LIFO liquidation benefits.
- Losses: impairments, restructuring, litigation charges, forex losses on debt, business-interruption effects, one-time regulatory penalties.

Then, for cyclical sectors, use **mid-cycle margins over a full cycle** rather than the trailing year — commodities, autos, shipping, chemicals, cement and lenders are almost never representative in any single year.

**Why.** The habitual bias is to strip losses and keep gains, which mechanically inflates normalised earnings and makes a "normalised P/E" a marketing number. Symmetric normalisation is what makes mid-cycle P/E and EV/EBIT usable. **Document every adjustment with its note reference** — an undocumented normalisation cannot be audited by the next reader (including you, next quarter).

---

## 20. Share count, dilution and per-share integrity

**What to use.** **Diluted weighted-average shares from the EPS note**, not the current outstanding count from a data feed. Then:

- Adjust the entire historical per-share series for splits, bonus issues, share consolidations, and rights issues (via the **theoretical ex-rights price factor** — a rights issue is part capital raise, part bonus, and ignoring the factor creates a fake per-share drop).
- Add outstanding options, RSUs, warrants and convertibles — and check the anti-dilution mechanics of convertibles and any reset clauses.
- Include **all** share classes in market cap: dual-class, DVR lines (India), preference shares that are economically equity, and unlisted classes. Providers routinely capitalise only the primary listed line.
- Check shares held by an **ESOP/ESOS trust** and treasury shares — conventions differ on whether they are netted out.
- **India:** confirm the count against the shareholding pattern filed with the exchanges (promoter, public, DII/FII), and check for warrants issued to promoters on a preferential basis, which convert at a pre-set price and dilute on a known schedule.

**Why.** Unadjusted or partially adjusted per-share history creates fake growth and fake collapses. Multi-class and multi-line issuers — common in India, Brazil, Korea and Europe — are systematically mis-capitalised, which understates EV and makes the stock look far cheaper than it is. This is the most frequent single cause of a screener showing an implausibly low P/E.

---

## 21. Data-provider field definitions and error patterns

**Before you screen on a field, read its definition.** For every metric, answer:

- Does "**debt**" include lease liabilities, preference shares, acceptances/bill discounting, and perpetual instruments?
- Is "**EBITDA**" EBIT + D&A from the filing, or a vendor-standardised model? Does it include other income?
- Is "**EPS**" basic or diluted, reported or adjusted, continuing operations or total?
- Is the multiple on **trailing, forward-consensus, or last-fiscal-year** data — and if forward, how many contributors?
- Is the series **consolidated or standalone**? (India — providers sometimes splice.)
- Is the currency tag correct, and are units crore/lakh/million consistent?

**Then hand-verify the top three and bottom three hits of any screen against the primary filings before acting on it.** This is not optional diligence; it is the highest-yield twenty minutes in the whole process.

**Why.** Provider errors cluster precisely where screens are most extreme: misparsed exceptional items, a missing quarter in a TTM, a stale or unsplit share count, a mis-tagged currency, standalone spliced onto consolidated. The outliers a screen surfaces are disproportionately data artefacts rather than opportunities — which is exactly why the screen surfaced them. Source hierarchy and provider-specific quirks are in `01-data-sourcing.md`; the primary sources to fall back to are EDGAR (10-K/20-F/8-K, XBRL company facts) and, in India, the BSE/NSE announcement filings, the annual report PDF and MCA filings.

---

## 22. The cash-flow reconciliation integrity check

Run this on every company before you trust any income-statement-derived ratio.

| Check | How to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Cumulative CFO ÷ cumulative PAT | Sum both over 5–10 years | Around 1.0 or above for most non-financials | Persistent divergence is the single most reliable flag for revenue-recognition or capitalisation aggression |
| CFO − capex vs reported FCF | Rebuild from the statement | Should tie exactly | If it does not, the company's FCF definition excludes something — find out what |
| Cumulative FCF vs cumulative reported profit | Sum over a full cycle | Directionally consistent | Profit that never becomes cash over a decade is not profit |
| Interest/dividend classification | Read the cash flow statement sections | Restate to one convention across peers | IFRS permits choices; US GAAP largely fixes them |

*Indicative ranges vary by market, cycle and period; peer and own-history comparison overrides any absolute band.*

**The classification trap in detail.** Under IFRS/Ind-AS, interest paid may sit in operating **or** financing, and dividends received in operating **or** investing. Common IFRS practice puts interest paid in financing; US GAAP puts it in operating. For a levered company this means the IFRS filer's CFO is **higher** than an identical US filer's by the entire interest bill — and so is its FCF and FCF yield. Restate every peer to one convention (put interest paid in operating for all, or below CFO for all) and say which.

**Also watch:** supply-chain finance / reverse factoring (a borrowing that presents as trade payables and flatters CFO — disclosure is now required under both frameworks, so its absence is itself informative), receivables securitisation and factoring, capitalised interest, and capex reclassified between operating and investing. Cross-reference `04-balance-sheet-and-cashflow.md` and `07-forensic-red-flags.md`.

---

## 23. Sector gate — where comparability is a different language

Before applying any generic template, confirm the metric set is even defined for the industry. Establish comparability **inside the sector's own accounting language** first.

| Sector | The accounting fault line | Consequence |
|---|---|---|
| Banks / NBFCs | IFRS 9 / Ind-AS 109 expected credit loss vs US CECL vs legacy incurred-loss; IRAC norms in India | EBITDA and EV are meaningless; compare NII, NIM, provisioning coverage, GNPA/NNPA, capital adequacy |
| Insurers | IFRS 17 vs prior embedded-value regimes; Indian insurers on Ind-AS 104-era practice | The historical series is broken at the IFRS 17 boundary; use VNB, EV, combined ratio |
| Real estate / REITs | IAS 40 fair-value gains flow through the IFRS P&L (**Ind-AS: cost model only**); US GAAP cost | An IFRS developer's "profit" may be unrealised revaluation; use NAV, FFO/AFFO |
| Utilities / regulated | Regulatory deferral accounts and regulatory assets | Reported earnings reflect a regulatory compact, not free-market margin |
| Oil & gas E&P | Successful-efforts vs full-cost capitalisation | Asset base, DD&A and EBIT differ materially between identical wells |
| Miners | Stripping-cost capitalisation, reserve-based depreciation, rehabilitation provisions | Unit-cost and ROCE comparisons need identical policies |
| Shipping / airlines | Charter/lease structures, residual value and useful-life assumptions | Lease convention (§5-6) dominates every leverage metric |

Route to `references/sectors/_index.md` for the sector-specific metric set. The governing principle applies with full force here: for banks, insurers, REITs and miners the standard ratios are undefined or inverted, and forcing them produces confident nonsense.

**Audit reliability is a precondition, not a section.** If the auditor resigned mid-cycle, a material subsidiary is audited by a different small firm, there is a going-concern emphasis, an adverse ICFR opinion, or a recurring key audit matter on revenue recognition, then none of the above matters — the inputs are unreliable. Handle this before comparability work; see `08-governance.md` and `15-document-diligence.md`.

---

## 24. The comparability worksheet you must produce

Keep one row per company and carry it into the report. This is the artefact that makes a comp table auditable and stops someone (including you) from silently sorting a column and reintroducing the single-metric ranking error.

| Column | What it records |
|---|---|
| Framework | IFRS / US GAAP / Ind-AS / local GAAP; ADR reconciliation yes/no |
| Fiscal year-end and period used | e.g. "31 Mar; TTM to Jun-2026" |
| Currency and unit | Reporting currency; conversion rate convention used (avg for P&L, closing for BS) |
| Basis | Consolidated / standalone; minority share of PAT |
| Lease convention | A (pre-IFRS 16) or B (fully capitalised); lease liability added to net debt (yes/no) |
| Revenue basis | Gross or net; take rate if applicable |
| Inventory | LIFO restated to FIFO? LIFO reserve value |
| R&D | Expensed / capitalised; capitalisation rate; adjustment applied |
| Normalisations | List of items removed, with note references and sign |
| Breaks | Transition years, restatements, currency changes, stub periods flagged |
| Data source | Filing vs provider, and which fields were hand-verified |

Also record the peers you **excluded** and why. Peer-set construction itself is in `10-peer-set.md`; this worksheet is the comparability layer that sits under it.

State in the report, in one sentence: *"Peers are compared on [lease convention], [currency convention], [period], with [named adjustments] applied identically to all members; residual non-comparability is [X]."* If you cannot write that sentence, the comparison is not ready.

---

## Checklist

- [ ] Record the exact reporting framework for every company in a column; note Ind-AS carve-outs and whether an ADR has a GAAP reconciliation.
- [ ] India: use consolidated statements throughout; never splice standalone and consolidated across years.
- [ ] Identify the two or three GAAP differences that are actually live for this peer set; fix those, not all of them.
- [ ] Restate US LIFO filers to FIFO (inventory, equity, COGS, deferred tax) before any margin or turnover comparison.
- [ ] Compute the R&D capitalisation rate; build a full-expensing baseline across the whole set and say you did.
- [ ] Pull ROU assets, lease liabilities, ROU depreciation, lease interest, maturity table and discount rate for every company.
- [ ] Build both lease conventions (A: pre-IFRS 16; B: fully capitalised); apply one to all peers, state which, and under B put lease liabilities in EV and ROU assets in capital employed.
- [ ] Confirm gross vs net revenue recognition and reconcile take rate to revenue; flag any presentation change between years.
- [ ] India: flag the FY2018 excise/GST revenue step-down before computing any revenue CAGR across it.
- [ ] Track unbilled revenue ÷ revenue and (receivables + unbilled) days for POC businesses.
- [ ] Rebuild margins at EBITDA/EBIT where classification differs; define gross margin identically for all peers or do not use it.
- [ ] Reconcile PAT attributable to owners vs total; gross EV up for minority interest; handle associates consistently on both sides.
- [ ] Pull the PPA for recent deals; report ROIC with and without goodwill and quantify PPA amortisation as a share of EBIT.
- [ ] Compare last year's comparatives to this year's line by line to detect unannounced restatements; classify what you find.
- [ ] Identify the transition method for every new standard; mark adoption years on every chart.
- [ ] India: flag the I-GAAP→Ind-AS break, Ind-AS 115 for real estate, Ind-AS 116, and the 115BAA tax election.
- [ ] Align fiscal periods; rebuild TTM from quarterly data where year-ends differ by more than a quarter; strip 53rd weeks and stub periods.
- [ ] Use average rates for P&L, closing rates for balance sheet; never re-denominate history at today's spot; standardise crore/lakh/million at extraction.
- [ ] Rebuild the reported-to-organic growth bridge (FX, M&A, divestments, extra week) and verify the 12-month anniversary rule.
- [ ] Reconcile ETR to the statutory rate and to cash tax; normalise to a sustainable rate; identify expiring holidays.
- [ ] Reconcile every adjusted figure to statutory; count how many years each "one-off" recurs; never add back share-based compensation.
- [ ] Normalise gains and losses symmetrically, with a note reference for each adjustment; use mid-cycle margins in cyclicals.
- [ ] Use diluted weighted-average shares from the EPS note; adjust history for splits, bonuses and rights (TERP); capitalise all share classes.
- [ ] Read the provider's definition of every field you screen on; hand-verify the top and bottom three hits against primary filings.
- [ ] Run cumulative CFO ÷ cumulative PAT over 5–10 years; restate interest/dividend classification to one convention; check for reverse factoring, securitisation and capex reclassification.
- [ ] Apply the sector gate — confirm the metric set exists for banks, insurers, REITs, utilities, E&P and miners before comparing.
- [ ] Confirm audit reliability first; unreliable inputs void every adjustment above.
- [ ] Produce the comparability worksheet, list excluded peers with reasons, and write the one-sentence comparability statement in the report.
