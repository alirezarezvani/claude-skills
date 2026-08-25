# Risk Factors: Company, Macro and External

Use this when: you are at Stage 7 building the bear case and invalidation triggers, or any time you need to convert a pile of "things that could go wrong" into a ranked, sized set of risks that actually changes the recommendation.

Most risk sections are useless because they are inventories. Twenty bullet points, each true, none sized, none ranked, none monitorable — the reader learns nothing and the analyst has bought deniability rather than insight. Your job is the opposite: identify the two or three exposures that could permanently impair the equity, quantify them against the specific business, name the observable event that would tell you they are materialising, and be explicit about everything else you deliberately excluded. The governing rule of this skill applies here as hard as anywhere: a risk metric means nothing until you know the sector and the company's own history. Net debt/EBITDA of 5x is a red alert for a consumer-goods company, unremarkable for a regulated utility, and an undefined quantity for a bank.

## Contents

- [0. The method: from risk list to sized risk map](#0-the-method-from-risk-list-to-sized-risk-map)
- [1. Balance-sheet risk: leverage, liquidity, refinancing](#1-balance-sheet-risk-leverage-liquidity-refinancing)
- [2. Operating leverage and cost-structure rigidity](#2-operating-leverage-and-cost-structure-rigidity)
- [3. Concentration: customers, suppliers, geography](#3-concentration-customers-suppliers-geography)
- [4. Supply-chain single-source dependency and business continuity](#4-supply-chain-single-source-dependency-and-business-continuity)
- [5. FX: economic exposure and the hedging book](#5-fx-economic-exposure-and-the-hedging-book)
- [6. Commodity and input-cost exposure](#6-commodity-and-input-cost-exposure)
- [7. Interest-rate sensitivity](#7-interest-rate-sensitivity)
- [8. Regulatory, policy, subsidy and tariff dependency](#8-regulatory-policy-subsidy-and-tariff-dependency)
- [9. Litigation, antitrust and enforcement exposure mapping](#9-litigation-antitrust-and-enforcement-exposure-mapping)
- [10. Tax disputes and transfer pricing](#10-tax-disputes-and-transfer-pricing)
- [11. IP portfolio and IP litigation](#11-ip-portfolio-and-ip-litigation)
- [12. Cybersecurity, data privacy and IT resilience](#12-cybersecurity-data-privacy-and-it-resilience)
- [13. Organisational health and human capital](#13-organisational-health-and-human-capital)
- [14. Country, political and sovereign risk](#14-country-political-and-sovereign-risk)
- [15. Sanctions, export controls and geopolitics](#15-sanctions-export-controls-and-geopolitics)
- [16. ESG: climate physical and transition risk, cross-sector](#16-esg-climate-physical-and-transition-risk-cross-sector)
- [17. Technological disruption and the AI-obsolescence test](#17-technological-disruption-and-the-ai-obsolescence-test)
- [18. Tail risk, hidden liabilities and contagion](#18-tail-risk-hidden-liabilities-and-contagion)
- [19. Macro regime and cycle positioning: the top-down gate](#19-macro-regime-and-cycle-positioning-the-top-down-gate)
- [20. Broad-market valuation context](#20-broad-market-valuation-context)
- [21. Sector translation: where the standard risk lens breaks](#21-sector-translation-where-the-standard-risk-lens-breaks)
- [22. Writing the bear case and the invalidation triggers](#22-writing-the-bear-case-and-the-invalidation-triggers)
- [Checklist](#checklist)

---

## 0. The method: from risk list to sized risk map

Do this **first**, then use sections 1–18 as the sweep that populates it. The output of this file is a table of at most seven risks, not a taxonomy.

### Step 1 — Sweep

Walk sections 1–18 and write one line per exposure that is *actually present* in this business. Discard generic risks that apply to all equities ("economic conditions may deteriorate"). A risk earns its place only if you can name the mechanism: what specifically happens to revenue, margin, capital or the multiple.

Source it from primary disclosure, not memory:
- **US/global:** 10-K Item 1A (Risk Factors), Item 3 (Legal Proceedings), Item 1C (Cybersecurity, mandatory from FY2023), Item 7A (Quantitative and Qualitative Disclosures About Market Risk — this is where FX, rate and commodity sensitivity tables live), and the Commitments & Contingencies note. Redline Item 1A against last year's 10-K: **new or newly specific risk language is management telling you something changed.**
- **India:** the annual report's Risk Management section and Board's Report, the contingent-liabilities note (Ind-AS 37 / Schedule III), CARO 2020 reporting — especially clause 3(vii)(b), disputed statutory dues with the forum where each is pending — related-party note, and SEBI LODR Regulation 30 material-event filings on the exchange. Concall Q&A is often the only place where a single-source dependency or a customer loss is discussed candidly.

### Step 2 — Size each risk

| Dimension | How to score | Note |
|---|---|---|
| **Severity (S)** | 1 = <5% of intrinsic value; 2 = 5–15%; 3 = 15–30%; 4 = 30–50%; 5 = >50%, or forces a dilutive raise / default | Size in value or EPS terms, not adjectives. "A 300bp gross-margin hit is roughly 25% of EBIT at this cost structure" beats "significant". |
| **Likelihood (L)** over your stated horizon | 1 = <5%; 2 = 5–15%; 3 = 15–35%; 4 = 35–60%; 5 = >60% | State the horizon explicitly (typically 3 years). Probability without a horizon is meaningless. |
| **Permanence** | Cyclical (recovers) / semi-permanent (years) / permanent impairment | The single most important column. |
| **Lead indicator** | The specific observable that moves first | If you cannot name one, the risk is unmonitorable — that is a sizing argument, not a footnote. |
| **Mitigant** | Hedge, insurance, contract, balance-sheet buffer — and its expiry | Hedges roll off. Always state the tenor. |

Expected loss = midpoint(S%) × midpoint(L%). Rank by expected loss, then apply two overrides:

1. **Permanence override.** A 10% chance of a permanent 60% impairment outranks a 60% chance of a temporary 15% drawdown, even though the expected losses are similar. Permanent capital loss is not recoverable by waiting; cyclical drawdown is. Rank on permanence first when the expected losses are within a factor of two.
2. **Solvency-first ordering.** Any risk that can force a distressed equity raise, a covenant breach or a default ranks above every margin-and-multiple risk regardless of arithmetic, because equity is subordinated and the recovery is typically zero.

### Step 3 — Cluster correlated risks

Risks that share a driver are one risk, not three. A company selling discretionary goods on credit to a single cyclical end-market has one risk — the end-market — expressing itself through volume, receivable losses and covenant headroom simultaneously. Listing them separately triples the apparent diversification of the risk map and understates the tail. Explicitly ask: **which of these fire together?** Leverage, concentration and illiquidity are the classic cluster; they compound precisely when financing disappears.

### Step 4 — Test what is already in the price

A well-known risk that has already de-rated the stock is not a reason to avoid it; an unpriced risk is. Cross-check against the reverse-DCF in `06-valuation.md`: if the market-implied growth is already near zero, the cyclical-demand risk is largely priced and the *upside* asymmetry may be the more interesting finding. Say which of your top risks you believe are priced and which are not, and why you think you are seeing something the market is not.

### Step 5 — Publish the map

Report the top five to seven, with S, L, permanence, lead indicator and mitigant. Then add one line naming the risks you considered and deliberately excluded, and why. Excluding a risk explicitly is analysis; omitting it silently is not.

---

## 1. Balance-sheet risk: leverage, liquidity, refinancing

Full treatment is in `04-balance-sheet-and-cashflow.md`; here you are asking only one question — **can this company be forced into a transaction it does not want?** Forced asset sales, rescue rights issues and covenant renegotiations are where permanent equity loss happens.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Net debt/EBITDA | (Debt + leases − cash & liquid investments) ÷ EBITDA, on **trough** EBITDA not peak | <2x for cyclicals; <3x general industry; 4–7x normal for utilities/infra with contracted cash flows; undefined for banks and NBFCs | The peak-EBITDA denominator is the most common leverage error; a cyclical at 2.5x on peak earnings is at 5x mid-cycle |
| EBIT interest coverage | EBIT ÷ gross interest expense | >4–5x comfortable; <2–3x fragile | Coverage fails before leverage ratios do, and coverage covenants trip first |
| Covenant headroom | Distance to the tightest covenant, in % of the tested metric | >20–25% | Under ~15% management starts managing to the covenant instead of the business |
| Near-term maturity cover | (Cash + undrawn **committed** facilities) ÷ debt maturing in 12–24 months | >1.5x | Solvent companies fail from illiquidity; uncommitted lines vanish when needed |
| Weighted-average maturity | Debt-weighted years to maturity | Longer than the asset payback | Funding long-life assets with short paper (commercial paper, working-capital lines) is the classic ALM failure |
| Structural subordination | Where the debt sits: parent vs operating subsidiary | — | Cash at a subsidiary behind subsidiary-level debt is not available to the parent's creditors, let alone shareholders |

Hunt for hidden debt: leases (IFRS 16 / Ind-AS 116 / ASC 842), receivables factoring and securitisation, supply-chain finance / reverse factoring parked in trade payables, PIK/toggle notes deferring cash interest, guarantees to associates and JVs, put options over minority stakes.

**India-specific.** Check promoter share pledging (shareholding pattern, quarterly). A pledged promoter block plus falling price creates a margin-call feedback loop that destroys the equity independently of operating performance. Also check inter-corporate deposits and guarantees to group entities in the related-party note — the leakage channel is loans out, not just sales.

---

## 2. Operating leverage and cost-structure rigidity

Financial leverage magnifies whatever operating leverage delivers; the two multiply. Estimate the degree of operating leverage (DOL) as %ΔEBIT ÷ %ΔRevenue over the last downturn, and sanity-check it against a fixed/variable cost split.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| DOL | %Δ EBIT ÷ %Δ revenue, measured across a real downturn | <2x flexible; >3–4x fragile | Tells you how far revenue can fall before profit disappears |
| Fixed costs % of total | Employee cost + depreciation + rent + other fixed opex ÷ total cost | Sector-dependent; compare to peers only | Airlines, hotels, semiconductors, steel are structurally high; distribution and services are low |
| Contribution margin | (Revenue − variable cost) ÷ revenue | — | High contribution margin plus high fixed cost = violent operating leverage both ways |
| Breakeven utilisation | Utilisation/occupancy/load factor at which EBIT = 0 | Well below current | For hotels, airlines, cement, steel, this single number is the risk |

Run a −10% and −20% revenue scenario explicitly and report EBIT, interest cover and covenant headroom at each. That one table does more work than a page of prose. Note where costs genuinely cannot flex: unionised labour, take-or-pay input contracts, long leases, minimum-offtake obligations, committed capex already under contract.

---

## 3. Concentration: customers, suppliers, geography

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Top-customer revenue share | % of revenue from largest customer | <10% comfortable; >20% material; >30% is a single-point-of-failure | Loss or renegotiation by one buyer can reset earnings power overnight |
| Top-5 / top-10 share | Cumulative | <40% / <60% typical | Also proxies bargaining power over price and payment terms |
| Customer HHI | Σ (customer revenue share)² | — | Better than a top-1 number when the tail matters |
| Net revenue retention (subscription) | (Starting ARR + expansion − churn − downgrade) ÷ starting ARR | >100% healthy; >110–120% strong | Concentration is tolerable if retention is proven; concentration plus churn is not |
| Revenue/EBIT/assets by geography | Segment note | — | Demand concentration and asset concentration are different risks; separate them |

**Disclosure.** US 10-K requires naming any customer >10% of revenue (ASC 280). India: Ind-AS 108 requires disclosure of revenue from customers exceeding 10%, though the customer is usually unnamed — the concall and the receivables ageing are your cross-checks.

Escalating concerns, in order: a large customer that is itself in distress; a large customer that is vertically integrating or in-sourcing; concentration that is *rising*; dependence on a single platform, app store, distributor or channel that controls access to the customer; and — for India — dependence on government or PSU orders where payment cycles stretch and receivables become an unfunded working-capital loan (state power distribution companies are the canonical case).

---

## 4. Supply-chain single-source dependency and business continuity

Balance-sheet strength cannot offset a plant that cannot run. This is a physical, not financial, risk and requires a physical map.

**Build a dependency map.** For each critical input: number of qualified suppliers, whether the sole source is contractual or technical (a qualified-vendor lock is much harder to break than a commercial one), lead time, days of inventory held against that lead time, geographic location of the supplier's *own* production, and the availability of a second source and how long qualification would take. Semiconductor, pharma API, specialty chemical and aerospace supply chains routinely have sole-source nodes three tiers upstream that tier-1 disclosure never reveals.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Sole-sourced % of COGS | Value of inputs with no qualified alternative ÷ COGS | As low as possible; >15–20% is a live risk | The size of the production you cannot protect |
| Inventory cover vs lead time | Days of inventory ÷ supplier lead time in days | >1.5–2x for critical parts | Thin buffers against long lead times mean any disruption stops the line |
| Supplier geographic HHI | Concentration of sourcing by country | — | One country + one hazard (earthquake, export ban, conflict) = correlated failure |
| Single-site revenue exposure | % of revenue produced at the largest single plant/site/data centre | <30–40% | Insurance pays for the asset, not for the lost customer relationship |

**Business continuity.** Ask what the recovery time would be, not just whether a plan exists: alternate site capacity, qualification time for a replacement supplier, insurance including **business-interruption and contingent business-interruption** cover, and the deductible/sub-limits. Note that BI insurance replaces gross profit for a capped period; it does not replace a customer that qualified a competitor in the meantime.

**India-specific.** Add pharma API and key-starting-material dependence on China, monsoon and water-availability risk for agri-linked and thermal/hydro assets, land acquisition and environmental-clearance delays for greenfield capacity, and freight/port chokepoints for exporters.

---

## 5. FX: economic exposure and the hedging book

The reported FX gain/loss line is the least important part of this. Analyse **economic** exposure: the mismatch between the currency of revenue, the currency of cost, and the currency of debt.

Build a three-row table by currency: % of revenue, % of costs, % of debt. Then:

| Exposure type | What it does | How to size it |
|---|---|---|
| Transaction | Contracted flows in a foreign currency | Net exposure per currency × expected move |
| Translation | Foreign subsidiaries restated into the reporting currency | Watch the cumulative translation adjustment (CTA) in equity; it is non-cash but it is real value |
| Economic / competitive | A competitor's currency devalues and undercuts you at home | Not on the balance sheet at all; the most-missed exposure |
| Balance-sheet mismatch | Hard-currency debt against local-currency revenue | The classic emerging-market blow-up; a devaluation becomes a solvency event |

**Interrogate the hedging book, do not just note that one exists.** Hedge ratio, tenor, instrument (forwards vs options vs natural hedge), the rate at which existing hedges are struck versus spot, and the roll-off schedule. A company hedged 80% for 12 months at rates far better than spot is enjoying a temporary earnings subsidy that will reverse — that is a forecastable margin headwind, not a risk. Say when it lands. Hedges delay exposure; they do not remove it.

- **US/global:** Item 7A carries the sensitivity table (typically EPS or fair-value impact of a 10% adverse move). Check for hyperinflationary subsidiaries under IAS 29 / ASC 830.
- **India:** the notes disclose hedged and **unhedged** foreign-currency exposure — the unhedged line is the one that matters. External commercial borrowings (ECB) carry RBI hedging expectations; IT exporters typically run long-dated USD forward books whose realised rate can differ materially from spot for several quarters.
- **Investor level (separate decision):** for a foreign-listed holding, the investor's base-currency translation is a distinct exposure from the company's operating FX. A correct stock call in a depreciating listing currency can still lose money. Flag it; do not conflate it with company risk.

---

## 6. Commodity and input-cost exposure

Two different situations, and conflating them produces nonsense:

1. **Price taker on output** (miners, steel, oil and gas producers, commodity chemicals). The commodity price *is* the business, not a risk factor bolted onto it. The real risk is position on the industry cost curve — a first-quartile producer survives the trough that kills the fourth quartile — plus balance-sheet capacity to sit through the trough. Do not present "commodity prices may fall" as a risk; present the trough-price EBITDA and the cash cost per tonne/barrel versus the curve.
2. **Price taker on input** (FMCG, autos, cement, packaging, food processing). Here the question is pass-through: magnitude, lag and mechanism.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Key input % of COGS | Largest single raw material or energy ÷ COGS | — | Determines whether a 20% input move is noise or the whole margin |
| Gross-margin sensitivity | bps of gross margin per 10% input-price move, assuming no pass-through | — | Converts a commodity chart into an EPS number |
| Pass-through lag | Months from input move to realised price change | 1 quarter good; 2–3 quarters painful | The lag, not the level, is what hits reported quarters |
| Hedge coverage and tenor | % of next-12-month requirement hedged, and at what strike | — | Same roll-off logic as FX |

A useful framing: **a distributor at 4% operating margin cannot absorb a 200bp input shock — it has no margin to absorb it with.** Thin-margin, high-throughput businesses are far more input-fragile than their revenue scale suggests. Contractual escalators (common in EPC, logistics and long-term supply agreements) materially change the answer; check whether they exist, what index they track, and the reset frequency.

---

## 7. Interest-rate sensitivity

Rates hit three channels at once — interest expense, demand, and the discount rate applied to the multiple — which is why rate shocks de-rate long-duration equities so violently.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Floating-rate debt share | Floating debt ÷ total debt | Lower is safer in a tightening cycle; not per se bad | Direct EPS transmission |
| EPS impact per +100bp | Floating debt × 1% × (1 − tax rate) ÷ shares | <3–5% of EPS is tolerable | Makes the exposure concrete |
| Repricing wall | Fixed debt maturing in the next 24 months × (current market rate − coupon) | — | Cheap legacy fixed debt repricing higher is a permanent, forecastable earnings cut |
| Duration gap (financials) | Asset duration − liability duration | Near zero for banks; deliberately positive for life insurers | See §21 — for lenders this replaces most of the above |
| Demand beta to rates | Historical volume correlation with policy rate / mortgage rate | — | Housing, autos, consumer durables, capital goods transmit rates through demand before interest expense |

Long-duration equities (loss-making growth, businesses whose value sits in terminal cash flows) carry rate risk in the multiple even with zero debt. Say so; it is frequently the largest rate exposure in the name.

---

## 8. Regulatory, policy, subsidy and tariff dependency

The question that matters: **what fraction of current profit exists because of a policy that could be withdrawn?**

Map the regimes that govern the business — price controls, licensing, environmental, sector regulators, data protection, tariffs — then quantify dependency:

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Subsidy/incentive-dependent profit | Incentive income + tariff-protected margin ÷ EBIT | The lower the better; >25% is a policy-reversal bet | Distinguishes an economic business from a policy arbitrage |
| Regulated-price revenue share | Revenue subject to administered or formula pricing | — | Caps upside and transfers the operating risk to a regulator's discretion |
| Compliance cost / revenue | Direct compliance and licensing spend | Rising trend is the signal | Rising compliance cost is a moat for incumbents and a margin drag for everyone |
| Tariff-exposed cost base | Imported inputs subject to duty ÷ COGS | — | Tariff changes hit COGS with almost no lag |

Treat a policy tailwind as a **finite-life asset with an expiry date**, and check whether the market is capitalising it into a perpetual multiple. That mispricing is common and asymmetric.

- **India-specific:** production-linked incentive (PLI) schemes, export incentives (RoDTEP and predecessors), anti-dumping and safeguard duties, GST rate changes, state-level capital and power subsidies, sector regulators (RBI, IRDAI, TRAI, CERC/SERCs, NPPA drug price control), and environmental clearances / NGT orders. Many mid-cap manufacturing theses are, in substance, PLI-and-anti-dumping-duty theses; name that when it is true.
- **US/global:** IRA and similar credits, Section 232/301 tariffs, FDA/EMA approval and pricing pathways, EU CBAM (a tariff in all but name for carbon-intensive imports), sector-specific rate regulation for utilities, and the pending-rulemaking docket in the relevant agency.

---

## 9. Litigation, antitrust and enforcement exposure mapping

Do not summarise the legal-proceedings note. **Map** it: for each material matter record the claim, the plaintiff type, jurisdiction, stage, amount claimed, amount reserved, insurance cover, and realistic timeline.

| Check | What to look for |
|---|---|
| Reserve adequacy | Amount claimed vs amount reserved vs the disclosed "reasonably possible" range. Under ASC 450 a US filer reserves only when a loss is probable and estimable, and discloses a range for reasonably possible losses — that range is the number you should stress, not the reserve |
| Category | Product liability and mass tort (open-ended, compounding), class actions, environmental remediation and Superfund-type liability (long-tailed, joint-and-several), employment, contract, IP (§11) |
| Antitrust / competition | Market-share and pricing-conduct exposure; remedies can be structural (forced divestiture, mandated interoperability) rather than monetary — structural remedies impair the moat permanently, fines do not |
| Enforcement / regulatory | Bribery and corruption (FCPA, UK Bribery Act), securities enforcement, environmental prosecution. Look for deferred prosecution agreements and monitorships — they carry ongoing cost and constrain expansion |
| Serial pattern | Repeated settlements in the same category are a business-model signal, not bad luck |

**India-specific.** Material litigation must be disclosed under SEBI LODR Regulation 30 and in the offer/annual documents; the contingent-liabilities note plus CARO 3(vii)(b) gives you disputed statutory dues by forum (Commissioner Appeals, ITAT, High Court, Supreme Court). Note the timelines — a matter at Supreme Court stage may be a decade from resolution, which changes the discounting entirely. Also check National Company Law Tribunal (NCLT) proceedings, Competition Commission of India (CCI) orders, and SEBI/ED actions against promoters (governance overlap, `08-governance.md`).

**Sizing rule.** Compare the plausible adverse outcome to *annual earnings and to equity*, not to revenue. A single adverse judgment that exceeds two years of net profit is a solvency-adjacent event and belongs at the top of the risk map even at low probability.

---

## 10. Tax disputes and transfer pricing

An abnormally low effective tax rate is an earnings-quality issue *and* a risk. Both need saying.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Effective tax rate vs statutory | Tax expense ÷ PBT, compared to the domestic statutory rate | Within a few points, or explained by a **durable** reason (tax holiday with a stated expiry, R&D credit, geographic mix) | An unexplained gap normalises upward eventually and permanently cuts after-tax profit |
| Cash tax vs book tax | Taxes paid (cash flow statement) ÷ book tax expense | Converging over 3–5 years | A persistent gap means deferred liabilities accumulating or aggressive positions |
| Uncertain tax positions | Unrecognised tax benefits (ASC 740-10 / former FIN 48) balance and roll-forward | Small and stable vs earnings | Management's own estimate of what it might lose |
| Disputed tax demands | India: contingent-liabilities note, by tax head and forum | Small vs equity | Indian demands are often gross and include interest and penalty; assess winnability, not just size |
| DTA recoverability | Deferred tax assets ÷ equity, and the profit needed to use them | — | DTAs on carried-forward losses are worthless if profitability does not return; write-downs hit book value |

**Transfer pricing.** For any group with cross-border intercompany flows, ask where profit is booked relative to where value is created. Indicators: a subsidiary in a low-tax jurisdiction holding the IP; management fees and royalties flowing to the parent; a principal/limited-risk-distributor structure. Exposure is multiplied because a single position can be challenged by **both** tax authorities. India: Form 3CEB filings, DRP/ITAT transfer-pricing litigation, advance pricing agreements (APAs — an APA in place materially de-risks the exposure, so check for one). Global: OECD BEPS Pillar Two 15% global minimum tax progressively removes the benefit of low-tax structuring, which mechanically raises the ETR of groups that had engineered it below 15% — quantify that specifically for the name rather than mentioning it in passing.

---

## 11. IP portfolio and IP litigation

Where the moat is legal rather than economic, the moat has an expiry date printed on it.

- **Expiry mapping.** Build the revenue-weighted expiry schedule of the patents that protect the top products. For pharma this is the patent cliff and it is fully forecastable — the exclusivity date is public. Model the post-expiry revenue decline explicitly (generic entry can remove the majority of branded revenue within a year or two in an open market).
- **Validity risk.** A granted patent is not a safe patent. In the US, inter partes review at the PTAB invalidates a meaningful share of challenged claims; Paragraph IV ANDA filings signal a generic challenge years ahead; ITC Section 337 actions can block imports outright. India: Section 3(d) of the Patents Act restricts evergreening, and the compulsory-licence provisions exist — relevant for pharma theses built on patent protection in India.
- **Freedom to operate.** Is the company the defendant? Recurring infringement suits, non-practising-entity exposure, and royalty-bearing licences that could be renegotiated all sit on the cost line.
- **Trade secrets and non-patented know-how.** Protected by employment law and practice rather than registration; exposure runs through employee mobility (§13) and joint-venture technology transfer (§14–15).
- **Metrics worth carrying:** % of revenue from products losing exclusivity within five years; R&D spend versus the revenue at risk (does the pipeline replace the cliff?); litigation reserve versus the disputed royalty stream.

---

## 12. Cybersecurity, data privacy and IT resilience

For data-intensive, platform, financial and healthcare businesses this is now a first-order operational risk, and it is under-covered in most analyses because it produces no line item until it produces a very large one.

| Check | What to look for |
|---|---|
| Disclosure | **US:** 10-K Item 1C describes risk-management processes, board oversight and management expertise; Form 8-K Item 1.05 requires disclosure of a material incident within four business days of the materiality determination. **India:** CERT-In directions require incident reporting within six hours; the Digital Personal Data Protection Act 2023 carries penalties up to ₹250 crore per instance of certain failures, and RBI/IRDAI/SEBI impose sector-specific IT and outsourcing frameworks |
| Incident history | Prior breaches, the disclosed cost, whether the remediation is complete, and whether the same failure mode recurs |
| Attack-surface concentration | Single data centre or single cloud region; a critical legacy core system (core banking, policy admin, ERP) mid-migration; third-party/vendor access as the ingress path — supply-chain compromise is now a leading vector |
| Regulatory regime | GDPR (up to 4% of global turnover), CCPA/CPRA, sectoral rules (HIPAA, PCI-DSS). Data-localisation requirements can force duplicated infrastructure |
| Resilience | Recovery-time and recovery-point objectives, tested failover, cyber-insurance limits and exclusions (many policies exclude nation-state acts) |
| Cost of a breach | Direct remediation + regulatory fine + customer attrition + class action, against annual EBIT |

The value-relevant question is **whether trust is the product**. For an exchange, a payments processor, a bank, or a healthcare data business, a serious breach damages the franchise itself, not just the P&L — that is a permanence-column-5 risk. For a cement plant it is an IT expense.

---

## 13. Organisational health and human capital

For people-driven businesses (IT services, consulting, asset management, specialty pharma R&D, brokerages) human capital *is* the productive asset, and it is entirely off the balance sheet.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Voluntary attrition | Voluntary exits ÷ average headcount, trailing 12m | Highly sector-specific; compare to direct peers and to the company's own history only. Indian IT services disclose it quarterly and it swings widely with the demand cycle | Rising attrition raises replacement and wage cost before it shows in margin, and signals culture or compensation stress |
| Revenue and gross profit per employee | Revenue ÷ headcount, tracked over time | Rising | The cleanest productivity cross-check; falling revenue/employee while headcount grows is a margin warning |
| Utilisation and bench (services) | Billable hours ÷ available hours | Sector norm; disclosed by Indian IT firms | Both too low (idle cost) and too high (burnout, delivery risk) are bad |
| Employee cost / revenue | — | Stable or improving | A sudden jump usually means retention spending, i.e. an attrition problem being paid off |
| Senior-management turnover | Departures of CxO / business-head level in 24 months | Low | Repeated senior exits, especially CFO, are a governance and integrity signal — see `07-forensic-red-flags.md` |
| Key-person dependence | Is the franchise the founder, a star fund manager, a lead scientist? | — | Concentrated human capital can leave, and often takes clients with it |

Read Glassdoor-type employee sentiment, LinkedIn headcount trend and job postings as **alternative-data corroboration** of the reported story: hiring that contradicts a growth narrative, or a shrinking sales organisation alongside guided acceleration, is a real signal. Also check succession planning, union/collective-bargaining agreements and their renewal dates, safety and injury rates for industrial operations, and — India — contract-labour dependence and the associated regulatory exposure.

---

## 14. Country, political and sovereign risk

For overseas operations, split **demand exposure** (revenue from a country) from **asset exposure** (production, licences, cash trapped there). Asset exposure is far harder to exit.

Assess per material country: political stability and rule of law, contract enforceability and the local courts, expropriation and forced-localisation history, capital controls and repatriation restrictions, local-content mandates, currency convertibility and peg sustainability, sovereign rating and CDS spread, and the host regulator's track record with foreign owners.

- **Trapped cash.** Quantify it. Cash that cannot be repatriated should be haircut or excluded from a net-debt calculation and from any sum-of-the-parts valuation; treating it at face value overstates value.
- **Sovereign linkage.** For companies whose customer is a government or state utility, sovereign stress arrives as receivables, not as headlines.
- **Valuation.** If you add a country risk premium in the discount rate, say the size and the basis (typically the sovereign default spread, sometimes scaled for equity volatility) — and do not also haircut the cash flows for the same risk. Double-counting country risk is a common error.
- **India-specific for inbound/outbound:** FDI sectoral caps and press-note restrictions on investment from land-bordering countries; ODI rules for Indian companies' overseas subsidiaries; and for domestically-focused names, state-level political risk (land, power tariffs, local approvals) is often more binding than national risk.

---

## 15. Sanctions, export controls and geopolitics

Distinct from country risk: here the risk is that a **third-country government** makes it illegal to keep doing what the company does.

- **Sanctions.** OFAC SDN and sectoral lists, EU and UK regimes, secondary sanctions that reach non-US parties. Screen for revenue, assets, suppliers and counterparties in sanctioned jurisdictions, and for ownership links (the 50%-ownership rule captures entities not themselves listed).
- **Export controls.** US EAR and Entity List, the foreign direct product rule (which reaches products made abroad with US technology), ITAR for defence, and the equivalent EU/Japan/Netherlands controls that matter for semiconductor equipment. The relevant question is not only "does the company sell to a restricted party" but "could its product become controlled". Advanced computing, semiconductor equipment, and dual-use materials are the live categories.
- **Inbound/outbound investment screening.** CFIUS and equivalents can block M&A; outbound-investment rules restrict capital into specified technology sectors. This constrains the growth path, not just current operations.
- **Chokepoints.** Map physical supply routes: Taiwan Strait, Strait of Hormuz, Red Sea/Suez, Panama. Route disruption shows up as freight cost and inventory first.
- **The lesson to carry:** the 2022 Russia exit showed that geopolitical exposure resolves not as a discount but as a **write-off** — assets became unsaleable and unhedgeable at any price. Geopolitical asset exposure therefore belongs in the permanence column, not the cyclical one.

---

## 16. ESG: climate physical and transition risk, cross-sector

Ignore aggregate ESG scores as an analytical input; rating providers disagree with each other substantially. Analyse **financially material** exposures, and note separately that ESG scores matter as a *flow* signal because mandated funds trade on them.

**Transition risk** (policy, technology, market shifting away from carbon):
- Carbon cost exposure: tonnes CO₂e × plausible carbon price ÷ EBIT. Under EU ETS and CBAM this is already a cash cost for European operations and for exporters into the EU in covered sectors (cement, steel, aluminium, fertiliser, electricity, hydrogen).
- Stranded assets: reserve life and asset life extending past plausible demand — thermal coal, refining, ICE powertrain tooling.
- Demand-side substitution: EV penetration against ICE component makers, renewables against thermal generation, and the second-order effects (grid, storage, copper).
- Financing and insurance exclusion: banks and insurers withdrawing from high-carbon assets raises cost of capital before it raises operating cost.

**Physical risk** (the part usually skipped): geolocate the major plants, mines, ports, warehouses and data centres, then check flood plain, cyclone/hurricane exposure, wildfire, heat stress on process efficiency and labour, and — critically for India — **water availability**. Water is the binding physical constraint for thermal power, cement, textiles, beverages, paper and semiconductors well before sea-level rise is.

**Social and governance components that convert into cash flow:** supply-chain labour practice and forced-labour import bans (which stop shipments outright), product safety and recall history, community and land-acquisition opposition to expansion, and safety incident rates for industrial operators. In India, mandatory disclosure sits in the **BRSR** (Business Responsibility and Sustainability Report) for the top 1,000 listed companies by market capitalisation, with BRSR Core assurance for the top tier — use its quantitative sections (energy, water, emissions, safety, complaints) rather than the narrative. Globally use CSRD filings, ISSB/IFRS S1–S2 reporting and the emissions notes.

---

## 17. Technological disruption and the AI-obsolescence test

The moat questions belong in `02-core-factors.md`; here the question is sharper and more uncomfortable.

**Ask explicitly: could this product or service be structurally displaced within the holding horizon?** Then answer it with evidence rather than reassurance. Diagnostic indicators: market-share trend (not level), unit-price deflation, R&D or capex intensity versus the credible attackers, the share of revenue from products less than five years old, the age of the current product cycle, and whether new entrants are appearing and being funded.

**The AI-obsolescence test.** For each major revenue line, classify:
1. **Displaced** — the value delivered is the production of text, code, images, routine analysis, tier-1 support, or the arbitrage of an information asymmetry that a model now closes. Per-seat or per-hour pricing on such work is the exposed configuration; effort-based pricing collapses faster than outcome-based pricing.
2. **Compressed** — the work survives but the labour content and therefore the price falls. Headcount-linked revenue models (staffing, traditional IT services, BPO) are structurally exposed even where demand persists.
3. **Neutral or amplified** — the constraint is physical, regulatory, relationship-based, or a proprietary data/distribution asset the model cannot access. Here AI lowers cost and may widen the moat.

Then ask the harder second-order questions: does the company own **proprietary data or a distribution choke point** that makes it a beneficiary rather than a victim? Is the incumbency legal or regulatory (which AI does not dissolve)? And is the disruption arriving through the customer's budget rather than the product — for example, a customer whose own headcount falls buying fewer seats?

Be calibrated in both directions. Disruption narratives are over-applied at the top of hype cycles and under-applied to slow structural decline. Where you conclude "compressed", give the timeline and the observable that would confirm it — pricing per unit of work, revenue per employee, and headcount trend are the fastest tells.

---

## 18. Tail risk, hidden liabilities and contagion

Inventory the exposures that do not appear in EBITDA and can nonetheless consume the equity:

- **Unfunded pension and post-retirement obligations** versus market capitalisation. A deficit approaching a meaningful fraction of market cap makes the pension scheme a senior claim on future cash flow, and it is rate-sensitive in the opposite direction to the assets.
- **Guarantees**, letters of comfort, and support undertakings to associates, JVs and — India especially — group companies.
- **Derivative notionals** and counterparty exposure, especially where hedging has drifted into position-taking.
- **Asset-retirement and decommissioning obligations** (mines, oil and gas, nuclear, landfills), which are long-dated, discounted, and highly sensitive to the discount rate and cost inflation.
- **Warranty, recall and product-liability tails**, and environmental remediation.
- **Variable interest entities / structured entities** and any consolidation boundary that looks designed.
- **Insurance adequacy** against maximum probable loss, including the exclusions.

Then run the contagion question: which of these fire **together** with the leverage and concentration risks already identified? The failure mode that actually destroys equity is rarely one risk at full size; it is three medium risks with a common driver arriving in the same quarter while financing is closed.

---

## 19. Macro regime and cycle positioning: the top-down gate

Bottom-up conviction with no top-down gate produces full investment at exactly the wrong point in the cycle. This section is not a forecast; it is a positioning statement.

Locate the company in three cycles simultaneously — they do not move together:

| Cycle | What to read | Why it matters for this name |
|---|---|---|
| **Business cycle** | PMI (manufacturing and services), IIP, GDP nowcasts, unemployment, capacity utilisation | Determines whether cyclical earnings are near a peak or a trough. Extrapolating peak earnings is the single most expensive cyclical error |
| **Monetary/liquidity cycle** | Policy rate and its direction, real rates, yield curve shape, central-bank balance sheet. India: RBI repo, CRR, system liquidity, credit growth | Sets the discount rate and risk appetite; long-duration equities are levered to this |
| **Credit cycle** | Corporate credit spreads, bank lending standards, default rates, issuance windows. India: bank credit growth, NBFC funding costs and spreads, corporate bond spreads | Determines refinancing availability — the difference between a leverage risk being theoretical and being live |
| **Capital cycle (sector)** | Industry capacity additions, capex announcements, incremental supply versus demand | Often the dominant driver for commodities, shipping, semiconductors, hotels, real estate: returns peak when supply is scarce and collapse when the new capacity lands |

Then position the name honestly: is this a late-cycle cyclical at peak margins being valued on peak earnings? Is it a long-duration compounder being bought into a tightening cycle? Is the sector's capital cycle turning against it? For India add the specific overlays that drive earnings: monsoon and rural demand, government capex and the fiscal stance, GST collections as an activity proxy, and FII/DII flow direction, which drives small- and mid-cap valuations far more than fundamentals over one-to-two-year windows.

State the conclusion as a sizing input, not a market call: *"Late-cycle for this sector; the capital cycle is adding supply through the next 24 months; that argues for a wider margin of safety and a smaller initial position rather than an avoid."*

---

## 20. Broad-market valuation context

A stock that is cheap against its peers can still deliver poor absolute returns if the whole market is expensive. Anchor the recommendation to an asset-class expectation:

| Check | How to compute | Why it matters |
|---|---|---|
| Index valuation vs own history | Nifty 50 / S&P 500 forward P/E and trailing P/E, and CAPE where available, versus 10- and 20-year percentiles | Frames whether a "cheap" relative call is cheap in absolute terms |
| Equity risk premium | Index earnings yield − long government bond yield (India: 10y G-sec; US: 10y Treasury, real where possible) | When the yield gap compresses toward zero, equities are being priced for perfection and cash/bonds become a genuine competitor |
| Market cap to GDP | India: the Buffett indicator versus its own history | Crude, cycle-sensitive, and useful only as a percentile — not a timing tool |
| Breadth and dispersion | How much of the index return is a handful of names; small/mid-cap premium or discount versus large-cap | India's small- and mid-cap indices periodically trade at large premiums to large caps, which is a warning about the *cohort*, not any single stock |

Use this as a gate on aggressiveness, not as permission to avoid analysis: an expensive market raises the required margin of safety and argues for staged entry rather than a full position. Say explicitly where the market sits and how it affected your conclusion.

**Never turn this into personalised allocation advice.** State the market context as analytical background; asset allocation is the user's decision.

---

## 21. Sector translation: where the standard risk lens breaks

The ratios in sections 1–7 are undefined or inverted for several sectors. Use the sector playbook and replace the lens:

| Sector | What breaks | What to use instead |
|---|---|---|
| **Banks** | Leverage ratios are meaningless — a bank is *supposed* to run ~10:1 or more; net debt is not a concept; interest expense is a cost of goods | Asset quality (GNPA/NNPA, PCR, slippage, restructured book), credit cost versus through-cycle normal, capital adequacy versus regulatory minimum plus buffers, LCR/NSFR, deposit franchise and CASA stickiness, ALM duration gap and repricing table, concentration by borrower and sector, unsecured-book share |
| **NBFCs / HFCs (India)** | Same as banks, plus no deposit base | Funding mix and concentration, ALM mismatch in the sub-1-year buckets (the classic Indian NBFC failure mode is a liquidity mismatch, not a credit event), bank-line dependence, co-lending and securitisation reliance |
| **Insurers** | Revenue and EBITDA are not meaningful; float distorts everything | Reserve adequacy and development triangles, combined ratio and its trend, catastrophe accumulation and reinsurance programme (including retention and reinstatement), investment-portfolio credit and duration risk, persistency for life |
| **REITs / InvITs** | EPS and P/E are distorted by depreciation; leverage looks high by design | Refinancing schedule against cap-rate and rate moves, LTV and interest coverage covenants, tenant concentration and WALE, lease expiry ladder, occupancy versus submarket supply, distribution coverage from AFFO |
| **Miners and E&P** | "Commodity price risk" is not a risk factor; it is the business | Position on the cost curve, reserve life and grade trend, jurisdiction and licence security, decommissioning liability, trough-price cash flow and balance-sheet survival |
| **Utilities / regulated infra** | High leverage is normal and financeable | Regulatory reset risk and the allowed return, counterparty (discom) receivables, tariff-formula durability, PPA tenor and renewal, capex approval |
| **Airlines / hotels / shipping** | Extreme operating leverage makes single-year metrics useless | Breakeven load factor/occupancy, fleet or fixture commitments, EV/EBITDAR with capitalised leases, fuel/bunker hedge book and tenor |
| **Early-stage / loss-making** | Coverage and leverage ratios are undefined | Cash runway in months, path to funding, dilution scenarios, and the terms of any structured or convertible financing |

---

## 22. Writing the bear case and the invalidation triggers

**The bear case must be the strongest version of the argument against the position, not a strawman you can knock down.** Standard for acceptance: someone who is short the stock would recognise their own thesis in it.

Construct it as a narrative, not a list. Take the top three clustered risks and connect them into one coherent story of how the investment loses money, with numbers: what happens to revenue, to margin, to the multiple, and therefore to the price. Produce a bear-case fair value the same way you produced the base case, so the downside is a figure and not an adjective. Where a credible short thesis or a published bear argument exists, engage its specific claims rather than dismissing them.

Then define **invalidation triggers**: specific, observable, dated events that would prove the positive thesis wrong. A good trigger is falsifiable and checkable from public disclosure.

| Weak trigger | Strong trigger |
|---|---|
| "If growth slows" | "Two consecutive quarters of volume decline with pricing flat or negative" |
| "If margins deteriorate" | "Gross margin below X% for two quarters without an identified one-off" |
| "If leverage rises" | "Net debt/EBITDA above the covenant threshold minus 20% headroom at any test date" |
| "If governance worsens" | "Auditor resignation, a new qualification, CFO departure, or promoter pledge rising above X%" |
| "If competition intensifies" | "Market share below X%, or the top customer not renewing at the [date] contract expiry" |

Attach a monitoring cadence: quarterly results, exchange filings, the shareholding pattern (India, quarterly), 8-K/Reg 30 events, and the two or three lead indicators identified in the risk map. Close by restating, in one line each, the top three risks with their severity, likelihood and permanence — that summary is what the reader will actually retain.

---

## Checklist

- [ ] Populated the risk map by sweeping sections 1–18 against **primary disclosure** (10-K Items 1A/1C/3/7A; India: risk section, contingent liabilities, CARO 3(vii)(b), LODR filings, concall Q&A).
- [ ] Redlined this year's risk-factor language against last year's; flagged anything newly added or newly specific.
- [ ] Scored each risk for severity, likelihood over a stated horizon, and permanence; applied the permanence and solvency-first overrides.
- [ ] Clustered correlated risks into single entries; named which ones fire together.
- [ ] Ranked and reported at most seven risks, each with a named lead indicator and mitigant (with the mitigant's expiry).
- [ ] Named the risks considered and deliberately excluded, with the reason.
- [ ] Ran a −10% and −20% revenue scenario through EBIT, interest cover and covenant headroom.
- [ ] Tested leverage on trough EBITDA, not peak; checked maturity wall, committed-vs-uncommitted liquidity, and structural subordination.
- [ ] Quantified top-customer, sole-source-input and single-site revenue concentration.
- [ ] Interrogated the hedging book: ratio, tenor, strike versus spot, roll-off date — for both FX and commodities.
- [ ] Quantified the share of EBIT dependent on a subsidy, tariff, tax holiday or other reversible policy, and its expiry.
- [ ] Mapped material litigation by claim, reserve, insurance and forum; compared the plausible adverse outcome to annual earnings and equity.
- [ ] Compared ETR to statutory and cash tax to book tax; checked transfer-pricing structure, APA status, and Pillar Two impact.
- [ ] Mapped revenue-weighted IP expiry and any live validity challenge.
- [ ] Assessed cyber/data-privacy exposure in proportion to whether trust is the product; checked incident history and disclosure regime.
- [ ] Checked attrition, revenue per employee, senior-management turnover and key-person dependence against the company's own history.
- [ ] Split overseas exposure into demand versus assets; quantified trapped cash; checked sanctions, export controls and chokepoints.
- [ ] Assessed material climate transition and physical risk, including water, using BRSR/CSRD quantitative data rather than ESG scores.
- [ ] Ran the AI-obsolescence test on each major revenue line: displaced, compressed, or neutral/amplified — with a timeline and a tell.
- [ ] Inventoried off-balance-sheet and contingent liabilities against market cap.
- [ ] Positioned the name in the business, monetary, credit and sector capital cycles; stated the implication for sizing and margin of safety.
- [ ] Anchored the call to broad-market valuation and the equity risk premium; did not turn it into allocation advice.
- [ ] Replaced the standard risk lens with the sector-appropriate one for banks, NBFCs, insurers, REITs, miners, utilities and high-operating-leverage sectors.
- [ ] Wrote a bear case a short-seller would recognise, priced it, and listed falsifiable invalidation triggers with a monitoring cadence.
