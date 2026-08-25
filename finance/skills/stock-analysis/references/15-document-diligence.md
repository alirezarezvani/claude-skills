# Primary-Document Diligence

Use this when: you have moved past screener data and need to work the actual filings — annual report, auditor's report, transcripts, rating rationales, exchange disclosures — either as the Stage 3 red-flag pass, the Stage 4 deep dive, or any time a number from an aggregator needs to be believed rather than merely quoted.

Everything else in this skill assumes the inputs are real. This file is where you establish that. A ratio computed from a figure you never traced to a primary document is a guess with decimal places, and the documents below are also the only place where the *non-quantitative* evidence lives — the auditor's own map of where the balance sheet is fragile, the promises management made three years ago, the guarantee issued to a promoter entity, the clause in CARO that says statutory dues went unpaid for six months. The governing principle applies throughout: a disclosure is meaningless until you know the sector and the company's own history. A large contingent liability is routine for an EPC contractor and alarming for a branded consumer company; a KAM on loan-loss provisioning is expected at every bank and would be extraordinary at a software firm.

## Contents

- [0. The annual report contains all of this — a complete contents map](#0-the-annual-report-contains-all-of-this--a-complete-contents-map)
- [1. Reading order when time is limited](#1-reading-order-when-time-is-limited)
- [2. The liability gradient: how much each document is worth](#2-the-liability-gradient-how-much-each-document-is-worth)
- [3. MD&A / Management Discussion and Analysis](#3-mda--management-discussion-and-analysis)
- [4. Notes to accounts: policies, estimates and changes therein](#4-notes-to-accounts-policies-estimates-and-changes-therein)
- [5. Contingent liabilities and commitments](#5-contingent-liabilities-and-commitments)
- [6. Related-party transactions note](#6-related-party-transactions-note)
- [7. Segment note](#7-segment-note)
- [8. The auditor's report — read this in full, every year](#8-the-auditors-report--read-this-in-full-every-year)
- [9. Consolidated vs standalone, AOC-1 and the subsidiary map](#9-consolidated-vs-standalone-aoc-1-and-the-subsidiary-map)
- [10. Earnings-call transcripts and Q&A behaviour](#10-earnings-call-transcripts-and-qa-behaviour)
- [11. Investor presentations vs audited filings](#11-investor-presentations-vs-audited-filings)
- [12. DRHP / RHP / S-1 and offer documents](#12-drhp--rhp--s-1-and-offer-documents)
- [13. Credit rating rationales and rating actions](#13-credit-rating-rationales-and-rating-actions)
- [14. Exchange filings and continuous disclosure](#14-exchange-filings-and-continuous-disclosure)
- [15. Shareholding pattern and promoter pledge](#15-shareholding-pattern-and-promoter-pledge)
- [16. Proxy / AGM materials and voting results](#16-proxy--agm-materials-and-voting-results)
- [17. Short-seller reports, forensic notes and adverse media](#17-short-seller-reports-forensic-notes-and-adverse-media)
- [18. Secretarial audit and Directors' Report annexures](#18-secretarial-audit-and-directors-report-annexures)
- [19. Sector translation: which documents replace the standard set](#19-sector-translation-which-documents-replace-the-standard-set)
- [20. Archive and data-provenance hygiene](#20-archive-and-data-provenance-hygiene)
- [Checklist](#checklist)

---

## 0. The annual report contains all of this — a complete contents map

The annual report is the single most complete document a company publishes about itself, and **almost every section carries something an investor should weigh** — the strategy in the chairman's letter, the pay ratio in an obscure annexure, the covenant in a borrowings note, the one live case in a litigation schedule that is otherwise routine. The discipline is therefore: **read and consider all of it, then report selectively.** Coverage in the reading is comprehensive; the write-up stays focused on what proved material. Skipping a section because it "looks like boilerplate" is exactly how the single live disclosure inside it gets missed — the boilerplate-versus-substance judgement is made *after* reading the section, never by not reading it.

Use the map below as a **coverage checklist**: walk every section, extract what matters, and for a section that is genuinely empty this year, record "read — nothing material" rather than leaving it unopened (next year it may not be empty). §1 below then tells you the *order* to read the high-yield sections under time pressure, and §§3–18 tell you *how* to read each one. This map exists so that nothing is skipped.

### Indian annual report (Companies Act 2013 + SEBI LODR) — section by section

| Section | What lives here | What to pull |
|---|---|---|
| Financial highlights / 5–10-year record | The company's own multi-year summary | The long-run trend, and any year quietly restated or omitted from the series |
| Chairman's / MD's letter | Strategy, capital-allocation intent, tone | Stated priorities and promises — checked next year against delivery |
| Corporate overview / business model | Products, brands, plants, geographies, operating KPIs | The revenue-model map and operational scale, before the numbers frame it |
| **MD&A** | Industry structure, segment performance, outlook, risks & concerns, internal-control adequacy, **key financial ratios with explanation of any change >25%** | Volume/price/mix decomposition, guidance, and the ratio-change explanations (§3) |
| **Board's / Directors' Report** | State of affairs, dividend, share-capital/ESOP changes, deposits, **s.186 loans/guarantees/investments**, **AOC-2 related-party contracts**, risk-management policy, board evaluation | The statutory narrative plus its annexures (below) |
| — Annexure **AOC-1** | Salient financials of every subsidiary / associate / JV | Loss-making, negative-net-worth, newly acquired and newly deconsolidated entities (§9) |
| — Annexure **CSR report** | Spend vs 2% obligation, projects, unspent transfers | A clean compliance signal; repeatedly deferred/unspent amounts (§18) |
| — Annexure **particulars of employees (s.197)** | Median remuneration, MD/WTD pay, pay ratio, top earners | Promoter/KMP pay vs PAT and its trajectory (§16) |
| — Annexure energy / tech absorption / **forex** | R&D and technology, **forex earnings and outgo** | Net forex exposure and any large unexplained outflow |
| **Corporate Governance Report** | Board composition & independence, committee membership and **attendance**, remuneration policy, RPT policy, **general shareholder information** (AGM, dividend, listing, stock data, shareholding distribution, plant locations), dividend distribution policy | Governance quality and the full shareholder-information block (§8, §16, §18) |
| **BRSR** (top listed cos) | ESG across 9 principles; BRSR-Core assured metrics | Regulatory, environmental and litigation exposure; treat unassured parts as narrative (§18) |
| Secretarial audit (MR-3) + LODR 24A | Statutory-compliance qualifications | Any qualification — late filings, invalid appointments, RPT/committee failures (§18) |
| **Independent Auditor's Report** (standalone *and* consolidated) | Opinion, basis, **KAMs**, EOM, Other Matter, **CARO** annexure, **IFC** opinion | The highest-yield section per minute — read in full, both bases (§8) |
| Balance sheet, P&L (+OCI), cash flow, changes in equity | The four primary statements | The numbers — reconcile all four and tie them together (§4; 01-data-sourcing §4) |
| Significant accounting policies + critical estimates | What "profit" means for this company | Revenue recognition, depreciation lives, capitalisation, ECL, impairment, DTA (§4) |
| **Notes to accounts — every one** | PPE/CWIP ageing, intangibles, **receivables & payables ageing**, borrowings with terms & covenants, revenue disaggregation, employee-benefit/actuarial, tax & deferred tax, **segment**, **related party (incl. year-end balances)**, **contingent liabilities & commitments**, financial-instrument risk (credit/liquidity/market), leases, **ratios**, **subsequent events** | This is where the analysis actually is — not one note is safe to skip (§4–§7) |

### US 10-K (SEC) — item by item

| Item | Contains | What to pull |
|---|---|---|
| 1 Business | Model, products, customers, competition, seasonality, regulation | The business map and moat evidence |
| 1A Risk Factors | Legally-obliged risk admissions | Diff across years; a dropped risk is a disclosure choice (§3) |
| 1C Cybersecurity | Cyber-risk governance and material incidents | Incident history and board oversight |
| 2 Properties / 3 Legal Proceedings | Facilities; litigation | Owned-vs-leased footprint; material litigation (§5) |
| 5 Market / dividends / repurchases | Buybacks, dividends, equity-plan info | Capital returned, and at what prices |
| 7 MD&A / 7A Market risk | Management narrative; FX/rate/commodity exposure | Growth decomposition, guidance, hedging (§3) |
| 8 Financial statements & notes | Statements + full notes + segment | Same depth as the Indian notes above (§4–§7) |
| 9A Controls & Procedures | ICFR assessment | Material weakness — and whether a 404(b) auditor attestation exists at all (§8.6) |
| 10–14 (often via DEF 14A) | Directors/governance, **executive comp**, **security ownership**, **related transactions**, accountant fees | Governance, pay-for-performance, RPTs, auditor independence (§16) |
| 15 Exhibits | **Ex-21 subsidiaries**, material contracts, debt indentures | Group map and covenant packages |

For sectors where the standard set is replaced (banks, insurers, REITs, miners, pharma), the additional documents in §19 sit **alongside** this map, not instead of it.

### Where abnormalities concentrate — the anomaly scan

Reading every section is *coverage*; this is the *detection* lens laid over it. A handful of sections are where genuine abnormalities almost always surface first — legal disputes, related-party dealings, and the shareholding-and-pledge pattern chief among them — and a serious one here can outweigh every positive on the scorecard, so it escalates to the Stage 3 kill-criteria screen rather than sitting in a footnote. For each, the question is never "is there a number?" but "does the pattern deviate from this company's own history and its peers?"

| Annual-report section | Normal | Abnormal — the tell | Go deep |
|---|---|---|---|
| **Litigation / legal proceedings & contingent-liability note** | Routine tax disputes, small vs net worth, stable | Contingent liabilities approaching or exceeding net worth; a demand growing every year with no provision; guarantees to entities that are *not* consolidated subsidiaries; the largest item also flagged as a KAM | §5; `07` §10 |
| **Related-party transactions note** | Small, stable, arm's-length, board-approved | RPT sales/purchases a rising share of the total; interest-free or perpetually-rolled advances to promoter entities; a new related party with a large first-year transaction; year-end balances growing regardless of performance; transactions sized just under approval thresholds | §6; `07` §10 |
| **Shareholding pattern & pledge** | Promoter stake stable, zero pledge, ≥25% public float | Promoter stake sliding over consecutive quarters; pledge rising or >25% of promoter holding; pledge against *promoter-entity* borrowing; quiet exits by long-standing domestic funds; a retail surge alongside an institutional exit | §15; `07` §10 |
| **Auditor's report & CARO** | Clean opinion; procedural CARO answers | Any qualification / emphasis-of-matter / going-concern; CARO positives on fraud, unpaid statutory dues, loan default, evergreening, short-term-funds-for-long-term-use, or bank-returns-vs-books divergence; mid-term auditor resignation | §8; `07` §8, §12 |
| **Accounting policies & estimates** | Stable year to year | A useful-life extension, capitalisation loosening, or estimate change that lifts profit with no cash effect — especially a policy changed the year the number it flatters turned down | §4; `07` §5, §7 |
| **Year-over-year disclosure** | Consistent detail | A disclosure that *disappears* — a segment folded into "others", a named large customer dropped from the concentration note, a KPI or volume figure that stops being reported | `07` §7 |

The calibration discipline from `references/07-forensic-red-flags.md` §16 governs every row: state the innocent explanation alongside the flag, require a *cluster* pointing at the same line item before calling it a finding, and never assert fraud — describe what the disclosure shows and what evidence would resolve it.

---

## 1. Reading order when time is limited

Documents are not equally informative per minute spent. Work down this list and stop when the time budget runs out; the order is deliberately front-loaded with the disclosures that most often end an analysis outright.

| # | Read | Time | Why it is this early |
|---|---|---|---|
| 1 | **Auditor's report** — opinion paragraph first, then KAMs, EOM, Other Matter | 15 min | A qualified or adverse opinion invalidates the numbers you were about to analyse. Free of charge, the auditor tells you which line items are most fragile. |
| 2 | **CARO annexure** (India) / **Item 9A controls + 8-K Item 4.01/4.02 history** (US) | 15 min | Factual yes/no answers the narrative cannot smooth over: defaults, unpaid statutory dues, fraud reported, auditor resignation, non-reliance on prior financials. |
| 3 | **Related-party note + contingent-liability note** | 20 min | The two commonest routes for value to leave a minority shareholder, and both are quantifiable in one sitting. |
| 4 | **Cash flow statement + segment note** | 20 min | Where the profit actually is and whether it became cash. Segment ROCE is usually the most surprising number in the report. |
| 5 | **Shareholding pattern, last 12 quarters, incl. pledge** | 10 min | Promoter stress and institutional exits show up here before anywhere else. |
| 6 | **Latest 2 earnings-call transcripts, Q&A only** | 30 min | Fastest read on management credibility and on which questions are being refused. |
| 7 | **MD&A for the last 3 years, side by side** | 30 min | Promise-versus-delivery drift; the cheapest credibility test available. |
| 8 | **Latest credit rating rationale** | 15 min | Liquidity and covenant detail equity filings never show. |
| 9 | **Significant accounting policies + critical estimates note** | 30 min | Determines whether the earnings you are valuing are policy-driven. |
| 10 | **AGM voting results + remuneration resolutions** | 15 min | A quantified governance verdict from investors who have met management. |
| 11 | **Investor deck reconciled to audited numbers** | 30 min | Measures management's willingness to flatter. |
| 12 | **DRHP / S-1, exchange filing history, short-seller material, secretarial audit** | 2 hr+ | Deep-dive mode only, or when steps 1–11 raised a specific question. |

**Screen mode** stops after step 5. **Standard mode** covers 1–9. **Deep dive** does all of it. If a document is unavailable, say so in the data-quality note rather than substituting inference — "FY23 annual report not retrievable; policy note not verified" is a legitimate output.

---

## 2. The liability gradient: how much each document is worth

Weight evidence by the legal consequence of it being wrong. This single heuristic resolves most conflicts between sources.

| Tier | Documents | Assurance |
|---|---|---|
| **Highest** | Offer documents (DRHP/RHP, S-1, prospectus); audited financial statements and auditor's report | Signed by directors and auditors with civil and criminal liability; restatement adjustments disclosed |
| **High** | Notes to accounts, CARO, secretarial audit, statutory annexures; exchange material-event filings; scrutiniser's voting results | Statutory format, prescribed content, auditable |
| **Medium** | MD&A, Directors' Report, quarterly results (limited review, not full audit), credit rating rationales, proxy statements | Management-owned narrative or third-party opinion; not audited |
| **Low** | Investor presentations, press releases, earnings-call scripted remarks, guidance | Marketing documents, usually carrying an explicit safe-harbour disclaimer |
| **Contextual** | Media, short-seller reports, forums, sell-side notes | Hypothesis generators; every checkable claim must be verified against a higher tier |

**Rule:** when two sources disagree, the higher tier wins and the discrepancy itself becomes a finding. A deck showing "net debt" materially below the balance sheet's borrowings is not a rounding issue — it is a definitional choice you must decompose (see §11).

**Triangulation.** The most valuable technique in this file is checking the same fact across tiers. A large receivable should appear consistently in the balance sheet, the KAM, the MD&A explanation, the concall answer, and the rating agency's liquidity comment. Where those four disagree, you have found something.

---

## 3. MD&A / Management Discussion and Analysis

India: a standalone MD&A section in the annual report, mandated by SEBI LODR Schedule V. US: Item 7 of the 10-K, plus Item 1A Risk Factors and Item 3 Legal Proceedings. Foreign private issuers: Item 5 of the 20-F.

**Read 3–5 consecutive years side by side, not one year alone.** A single MD&A is a press release. Five stacked MD&As are a track record.

**Extract:**
- Management's own decomposition of growth into **volume versus realisation/price versus mix** — and check it against the segment note and any volume data disclosed elsewhere.
- Capacity, capacity utilisation, and planned capex with timing and funding source.
- Order book / backlog, book-to-bill, and stated execution period.
- Segment-wise outlook statements, verbatim, with the year attached.
- The risk-factor list, verbatim, year by year.
- Ratio disclosures (India requires key financial ratios with explanation of any change over 25%).

**What a problem looks like:**
- **Recycled promises.** "Demand recovery expected in H2" appearing three years running. Build a two-column table: *what was promised in year N* | *what was delivered in year N+1*. Management that never acknowledges a miss is telling you how it will handle the next one.
- **Narrative-to-numbers divergence.** MD&A attributes growth to a premium segment; the segment note shows that segment shrinking. The segment note is the higher tier.
- **A risk silently dropped.** Compare risk lists year to year. A customer-concentration risk that disappears without the concentration disappearing is a disclosure decision, not a business change.
- **Boilerplate expansion.** MD&A that grows in length while shedding specifics (numbers replaced by adjectives) is a deliberate reduction in falsifiability.
- **US-specific:** watch for new risk factors added quietly (10-K Item 1A must flag material changes; 10-Q Item 1A carries updates), and for legal proceedings moving from Item 3 into a note or vice versa.

**Why:** MD&A is the only management-owned, management-signed narrative sitting inside an audited document. It is unaudited, so it is where optimism lives — which makes the drift between it and the audited statements a direct measurement of that optimism.

---

## 4. Notes to accounts: policies, estimates and changes therein

Read the **significant accounting policies** note and the **critical estimates and judgements** note in full. These two notes determine what "profit" means for this company. Cross-read with `references/14-accounting-comparability.md` for Ind-AS/IFRS/GAAP differences.

**Extract, and compare against 2–3 sector peers — never against an absolute standard:**

| Policy area | What to extract | What a problem looks like |
|---|---|---|
| Revenue recognition | Point-in-time vs over-time; percentage-of-completion inputs; principal vs agent (gross vs net); variable consideration and rebate estimates | Over-time recognition with milestone estimates management controls; a switch from net to gross that inflates revenue with zero profit impact |
| Inventory | Valuation basis (FIFO/weighted average), overhead absorption, obsolescence provisioning policy | Provisioning rate falling while inventory days rise |
| Depreciation | Method and **useful lives per asset class**, residual values | Useful life extended (e.g. plant from 15 to 25 years) — flows straight to profit with no cash effect. Quantify the disclosed P&L impact. |
| Capitalisation | Borrowing costs capitalised, development costs capitalised, CWIP ageing | Capitalised development cost rising as a share of R&D; CWIP sitting >2–3 years without transfer to fixed assets |
| Expected credit loss (ECL) | Staging methodology, loss rates by bucket, forward-looking overlays | ECL coverage falling while receivable ageing worsens |
| Impairment | Goodwill/CGU allocation, discount rate, terminal growth, headroom and sensitivity disclosure | Terminal growth near or above the discount rate; headroom disclosed as "sufficient" without numbers; the same CGU tested with a friendlier rate each year |
| Leases | Discount rate on Ind-AS 116/IFRS 16 liabilities; short-term and low-value exemptions used | A high incremental borrowing rate that shrinks the recognised liability |
| Deferred tax | Recognition of DTA on carried-forward losses and the profitability forecast supporting it | A large DTA recognised by a loss-making entity — an assertion about future profits, booked as an asset today |

*Indicative comparisons vary by market, cycle and period; peer and own-history comparison overrides any absolute band.*

**Always do this:** list every change in policy, estimate or useful life, quantify the disclosed P&L impact, and **restate the affected years yourself** so the trend you analyse is on a consistent basis. If the impact is not quantified, say the trend is not comparable.

**Why:** policy and estimate changes are the most common *legal* way to manufacture earnings. Because acceptable ranges are entirely sector-specific — a 25-year life is normal for a cement kiln and absurd for a server — only a peer-relative reading tells you whether the company sits at the aggressive end.

---

## 5. Contingent liabilities and commitments

Tabulate by category for five years: disputed direct tax, disputed indirect tax (GST/excise/service tax/customs), guarantees given (split: to subsidiaries, JVs, promoter/group entities, third parties), claims not acknowledged as debts, letters of credit and bills discounted, and pending litigation.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Contingent liabilities / net worth | Total contingent liabilities ÷ shareholders' equity | Typically <25–30% for a consumer or services business; 50%+ is normal for EPC/infra where performance guarantees are the business | Sizes the claim against equity if matters go against the company |
| Contingent liabilities / market cap | Same numerator ÷ market cap | Small enough that full crystallisation is survivable | Converts a footnote into a valuation input |
| Growth rate vs net worth growth | 5y CAGR of contingent liabilities vs 5y CAGR of net worth | Contingent growth ≤ net-worth growth | Faster growth means the off-balance-sheet claim is compounding against a shrinking cushion |
| Guarantees to group entities / net worth | Guarantees issued for subsidiaries, JVs and promoter entities ÷ net worth | As low as possible; any material figure needs an explanation | The classic channel for pushing leverage off the listed entity while keeping the risk |
| Capital commitments not provided for | "Estimated amount of contracts remaining to be executed on capital account" | Consistent with stated capex plans and funding capacity | Committed future cash outflow the balance sheet does not show |

*Ranges are indicative only and vary by sector, market and cycle; the company's own history and its closest peers override any absolute band.*

**What a problem looks like:** contingent liabilities exceeding net worth; a disputed tax demand that keeps growing with no resolution and no provision; guarantees to entities that are not consolidated subsidiaries; management's non-provisioning rationale being a single boilerplate line ("the company expects a favourable outcome") with no legal basis stated; the largest item also appearing as a KAM (that is the auditor agreeing with your concern).

**Cross-check** the biggest items against the KAM section, the litigation schedule in any DRHP, and exchange filings on adverse orders. In India also check whether disputed amounts are at the Commissioner (Appeals), ITAT, High Court or Supreme Court stage — later stages mean longer duration but usually more crystallised risk.

**Why:** these are off-balance-sheet claims that convert into real cash. A number that dwarfs net worth is a solvency question, not a footnote.

---

## 6. Related-party transactions note

List every related party and every transaction type: sales, purchases, job work, loans and advances given and taken, guarantees, rent, royalty and brand fees, technical/management fees, managerial remuneration, and **year-end outstanding balances** (which the transaction table alone will not show).

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| RPT sales share | Sales to related parties ÷ total revenue | Low and stable unless the group structure genuinely requires it | High or rising share means reported revenue is not arm's-length-validated |
| RPT purchase share | Purchases from related parties ÷ total purchases/COGS | Low and stable | The main route for margin to be routed out of the listed entity |
| Royalty / brand fee intensity | Royalty paid to promoter entity ÷ revenue, and its growth vs revenue growth | Flat as % of revenue if genuinely usage-based | A royalty growing faster than revenue is a rising tax on minority shareholders |
| Promoter remuneration | Total promoter-family pay ÷ PAT (India: statutory ceiling 11% of net profits, 5%/10% for individual MD/WTD under s.197) | Small share of PAT; falls when profits fall | Pay that rises while profit falls is the cleanest evidence of a board that does not constrain the promoter |
| Related-party receivables | Loans/advances/receivables due from related parties ÷ net worth, and ageing | Minimal, and recovered on stated terms | Interest-free advances that never return are, economically, a dividend paid only to the promoter |

*Indicative only; sector and group structure change what is normal — peer and own-history comparison governs.*

**What a problem looks like:** interest-free or below-market loans to related parties; advances perpetually rolled over rather than repaid; a related-party balance that grows every year regardless of business performance; sales to a related party at a margin implausibly different from third-party sales; a new related party appearing with a large transaction in its first year; "loans to bodies corporate" in the balance sheet that exceed the amounts disclosed as related-party in the note (check the s.186 disclosure in the Directors' Report against the RPT note).

**Governance trail — verify each step, don't assume it:** audit-committee approval; where material, a shareholder special resolution with **related parties abstaining** (India: SEBI LODR Reg 23, materiality threshold ₹1,000 crore or 10% of consolidated turnover, whichever lower; half-yearly RPT disclosures to exchanges); then read the AGM voting results for institutional dissent on that specific resolution. US: related-party transactions appear in the DEF 14A under Item 404 of Reg S-K, and the audit committee charter governs approval.

**Why:** RPTs are the primary mechanism of minority-value leakage in promoter- or founder-controlled companies. No accounting rule needs to be broken for profit to be routed out.

---

## 7. Segment note

Extract, for each reported segment across five years: segment revenue, inter-segment revenue, segment result/EBIT, segment assets, segment liabilities, capital employed, and capex. Then compute **segment margin and segment ROCE** yourself.

**What to look for:**
- **One segment subsidising another.** A high-return cash cow funding a structurally loss-making segment that absorbs most of the capex. Consolidated margin hides this completely; segment ROCE reveals it. This is the single most common surprise in the entire annual report.
- **Segment redefinition.** Segments merged, renamed, split, or re-mapped between years. Ask what became invisible. A deteriorating business folded into a healthy one is the standard way it stops being discussed. When it happens, request or reconstruct the restated prior-year segment data; if it is not available, state that the segment trend is broken.
- **A swelling "unallocated" or "others" bucket.** Unallocated corporate expense and unallocable assets growing faster than the business are where inconvenient items go to be un-analysed.
- **Segment set versus management's own language.** If the concall discusses five businesses and the note reports two, management has chosen to report at a level that prevents you from checking the story.
- **Geography split** alongside the business split — matters for FX, tax rate and political risk.

**Standards note:** Ind-AS 108 and IFRS 8 / ASC 280 all use the "management approach" — segments are what the chief operating decision maker reviews. That makes the segment note a *disclosure choice*, which is exactly why changes to it are informative. Also check the major-customer disclosure (required where a customer exceeds 10% of revenue).

**Why:** consolidated economics are an average. Capital allocation happens at segment level, and so does destruction of value.

---

## 8. The auditor's report — read this in full, every year

This is the highest-yield section of the annual report per minute spent, and the one most often skipped. Read the **standalone and the consolidated audit reports separately — they can and do differ.**

### 8.1 Opinion type

Find it on the first page, in the paragraph headed "Opinion".

| Opinion | Meaning | What you do |
|---|---|---|
| **Unmodified / unqualified ("clean")** | Statements give a true and fair view | Proceed — but a clean opinion is a floor, not a positive |
| **Qualified** ("except for…") | A specific, named item is wrong or unverifiable; the rest is fine | Stop and quantify. Read "Basis for Qualified Opinion", extract exactly what the auditor could not verify or disagreed with, take the quantified impact if given, and **restate the financials yourself** before computing any ratio |
| **Adverse** | The statements as a whole do not give a true and fair view | The accounts are not usable. Do not produce a valuation from them |
| **Disclaimer of opinion** | The auditor could not obtain sufficient evidence to form any opinion | Effectively no audit happened. Treat the financials as unaudited management assertions |

Track opinion type across five years and flag **any new modification**. In India, SEBI additionally requires a **Statement on Impact of Audit Qualifications** filed with annual audited results — it forces management to quantify the qualification or explain why it cannot; read management's number and the auditor's comment on it side by side.

### 8.2 Basis for opinion and going concern

Beyond the modification paragraph, look for a **"Material Uncertainty Related to Going Concern"** section. This is not a qualification and is easy to miss, but it is the auditor stating that the entity's ability to continue operating depends on events outside its control (refinancing, a court outcome, promoter support). Extract the specific dependency and its date. In the US, going-concern doubt also drives disclosure under ASC 205-40 and is usually echoed in the risk factors.

### 8.3 Key Audit Matters (KAM) / Critical Audit Matters (CAM)

India and IFRS jurisdictions: KAMs under SA 701 / ISA 701, required for listed entities, typically 2–6 per report. US: **Critical Audit Matters** under PCAOB AS 3101, generally fewer (often 1–2) and narrower.

For each KAM extract three things: **(a)** the balance or judgement involved, **(b)** why the auditor considered it high risk, **(c)** the specific procedures performed — and whether those procedures actually address the risk (a KAM on inventory existence "addressed" only by reviewing management's reconciliation is weaker assurance than physical attendance).

Then **track KAMs across years.** A newly added or persistently repeated KAM is the auditor pointing at the line item most likely to be restated or impaired later. The highest-signal recurring KAMs:
- Recoverability of trade receivables / expected credit loss
- Revenue recognition on long-term or over-time contracts
- Impairment of goodwill or of investment in a named subsidiary
- Recoverability of loans and advances to related parties
- Capitalisation of development costs or CWIP
- Litigation and tax provisions
- Inventory existence and valuation, especially at third-party locations

Map each KAM to the corresponding note and check the disclosed sensitivity of the assumptions. Compare the KAM list with the company's peers audited by the same firm — a KAM that everyone in the sector carries is a sector characteristic, not a company flag. This is the governing principle applied to auditor language.

### 8.4 Emphasis of Matter (EOM) and Other Matter

**Emphasis of Matter** is not a qualification — the auditor is drawing attention to something already disclosed. That framing makes it easy to skip, which is precisely why serious things live there: going-concern uncertainty, a court-approved **scheme of arrangement** whose accounting overrides normal standards (a recurring device for routing write-offs through reserves instead of the P&L), regulatory forbearance, a pending investigation, or the effects of a material subsequent event. Read every EOM and follow it to the underlying note.

**Other Matter** is where the auditor discloses what they did *not* audit. In a consolidated report, quantify from this paragraph:
- % of consolidated **total assets, revenue and profit** audited by **other (component) auditors**
- % based on **unaudited, management-certified** subsidiary accounts

If 40% of consolidated profit comes from components the principal auditor never touched — or from entities that are unaudited — the word "audited" on the consolidated statements carries far less assurance than it appears to. State this percentage explicitly in your data-quality note.

### 8.5 CARO annexure — India-specific, read clause by clause

The Companies (Auditor's Report) Order 2020 forces the auditor to answer specific factual questions. Read the annexure itself, not the summary; a "no exceptions noted" clause takes seconds, and the exceptions are where the information is. Highest-signal clauses:

| Clause | What it answers | What a problem looks like |
|---|---|---|
| 3(i)(c) | Title deeds of immovable property held in the company's name | Properties on the balance sheet whose title is not with the company |
| 3(i)(d)–(e) | Revaluation of PPE; benami property proceedings | A revaluation gain propping up net worth; any benami proceeding at all |
| 3(ii)(a) | Physical verification of inventory and discrepancies | Discrepancies >10% in any class — the auditor must report them |
| **3(ii)(b)** | Where working-capital limits exceed ₹5 crore: whether **quarterly returns filed with banks agree with the books** | Divergence between what the banks were told and what was booked. Extremely high signal; banks see stock statements monthly |
| 3(iii) | Loans/advances/guarantees given: overdue amounts, terms, **renewals or fresh loans used to settle existing overdues (evergreening)**, loans repayable on demand with no stated terms | Evergreening; interest-free demand loans to group entities |
| 3(iv) | Compliance with s.185/186 on loans and investments | Non-compliance means the transaction itself was unlawful |
| 3(vii) | Statutory dues (GST, PF, ESI, TDS, income tax, customs) — undisputed dues **unpaid beyond six months**; and a list of disputed dues with forum | Unpaid statutory dues are hard evidence of a liquidity squeeze months before ratios show it — companies pay taxes last |
| **3(viii)** | Transactions **not recorded in the books but surrendered/disclosed as income in income-tax assessments** | Direct evidence of unrecorded transactions. Treat any positive answer as a full stop |
| 3(ix)(a)–(f) | Default in repayment to lenders (with amounts and dates); declared **wilful defaulter**; term loans applied for the stated purpose; **short-term funds used for long-term purposes**; funds raised on pledge of subsidiary shares; obligations of subsidiaries/JVs met from group funds | Short-term funds funding long-term assets is a classic pre-crisis asset-liability mismatch. Wilful-defaulter status is disqualifying |
| 3(x) | End-use of IPO/FPO/preferential allotment/private placement proceeds | Money raised for capex deployed into loans to group entities |
| **3(xi)** | Any **fraud** on or by the company; auditor's ADT-4 report to the Central Government; **whistle-blower complaints** considered | The single highest-signal paragraph in the annual report |
| 3(xiii) | Compliance with s.177/188 on related-party transactions and their disclosure | Procedural failure on RPTs, which is usually where substantive failure begins |
| 3(xiv) | Existence and adequacy of internal audit, and whether the auditor considered its reports | No internal audit function in a company of scale |
| 3(xv) | Non-cash transactions with directors (s.192) | Directors acquiring assets from the company without cash |
| 3(xvi) | NBFC/CIC registration where required; unregistered lending activity; number of CICs in the group | A group operating a finance business without registration, or an unexpectedly large CIC count signalling structural complexity |
| 3(xvii) | **Cash losses** in the current and immediately preceding financial year | Cash losses two years running |
| **3(xviii)** | **Resignation of the statutory auditors during the year** and whether the auditor considered the issues raised by the outgoing firm | See §8.7 — this is the strongest routinely available negative signal |
| 3(xix) | Whether, based on ratios, ageing and expected dates of realisation, any **material uncertainty exists about meeting liabilities falling due within one year** | An auditor-endorsed liquidity warning, stated in plain language |
| 3(xx) | Transfer of unspent CSR amounts | Small money, but non-compliance with an easy statutory obligation predicts non-compliance elsewhere |
| 3(xxi) | Qualifications or adverse remarks in the CARO reports of **companies included in the consolidation** | Problems at subsidiaries that the parent's own CARO would not show |

**US analogue:** there is no CARO. The nearest equivalents are Item 9A (Controls and Procedures), Item 3 (Legal Proceedings), Item 4 (Mine Safety, where relevant), the ICFR attestation, and 8-K Items 4.01/4.02. The factual granularity of CARO simply does not exist in the US regime — which means for a US issuer you compensate with more weight on Item 9A, the auditor-change 8-Ks and the PCAOB inspection record.

### 8.6 Internal financial controls (IFC/ICFR)

**India:** a separate opinion under s.143(3)(i) on the adequacy and **operating effectiveness** of internal financial controls over financial reporting, appearing as an annexure to the audit report.
**US:** management's assessment under SOX 404(a) in Item 9A, plus the **auditor's attestation under 404(b) — required only for accelerated and large accelerated filers.** Non-accelerated filers, smaller reporting companies and recent IPOs (which get a transition exemption) have *no* auditor opinion on controls. Note that gap explicitly; it is common in small caps and in newly listed companies. Also read the SOX 302 certifications signed by the CEO and CFO.

Determine whether the opinion is clean or identifies a **material weakness**, and read its description: revenue cut-off, vendor master data, inventory at third-party locations, segregation of duties, IT general controls and access rights, period-end financial reporting process. Distinguish a *material weakness* (reasonable possibility that a material misstatement would not be prevented or detected) from a *significant deficiency* (less severe). Then check whether a weakness reported last year was **remediated or repeated**.

**Why:** a material weakness means the machinery producing the numbers cannot be relied upon to catch a material error. It undermines every ratio you compute downstream. A repeated, unremediated weakness signals either management indifference or deliberate tolerance.

### 8.7 Auditor identity, tenure, rotation, fees and resignation

| What to extract | Where | What a problem looks like |
|---|---|---|
| Audit firm name, appointment year, engagement partner | Audit report signature block; India: firm registration no. and partner membership no.; US: PCAOB Form AP names the engagement partner | A firm with no other listed clients of comparable size; the same small firm auditing multiple group entities |
| Rotation status | India: s.139(2) — individual auditor 5 years, firm 10 years (two terms of five), 5-year cooling off, applicable to listed and prescribed companies | Rotation due but a "new" firm staffed by the same partners, or an affiliate/network firm of the outgoing one |
| **Audit fee vs non-audit fee** | Notes to accounts ("Payment to auditors"); US: DEF 14A audit fee table (audit / audit-related / tax / all other) | Non-audit fees approaching or exceeding audit fees — a direct independence problem. India: s.144 prohibits specified non-audit services outright |
| Fee level vs size | Audit fee vs revenue and vs peer fees | An implausibly low fee for a complex multi-subsidiary group means the work was not done |
| **Auditor change or resignation** | India: exchange filing plus the resignation letter, which must state reasons (SEBI requires detailed reasons and the auditor must comment on unresolved issues); US: **8-K Item 4.01**, which must disclose disagreements and reportable events, with a Letter from the former accountant as Exhibit 16 | Any mid-term resignation. Cited reasons of "pre-occupation" or "other commitments" in a company under stress should be treated as a euphemism |
| **Non-reliance on previously issued financials** | US: **8-K Item 4.02**; India: restatement or revision under s.130/131 | The company formally telling you its old numbers were wrong |
| Late filing | US: NT 10-K / NT 10-Q; India: delayed results filing and exchange penalties | An issuer that cannot close its books on time |
| Auditor quality signals | PCAOB inspection reports for the firm; regulatory bans (India: NFRA/ICAI orders, SEBI debarments) | An auditor under regulatory action, or one whose inspection reports show high deficiency rates |

**Why:** auditors rarely walk away from fees without cause, which makes mid-term resignation arguably the strongest single negative signal in public disclosure. A downgrade in auditor quality, or heavy non-audit fees, weakens the assurance behind every number you are about to use. Read this section together with §9 of `references/07-forensic-red-flags.md` on CFO and audit-committee turnover — auditor and CFO exits often cluster.

---

## 9. Consolidated vs standalone, AOC-1 and the subsidiary map

**Analyse consolidated as the primary basis** for business economics and valuation, then reconcile against standalone. Never mix them within one ratio, and always label which basis each figure came from. Aggregators and screeners routinely show one and label it the other.

| Reconciliation | How to compute | Why it matters |
|---|---|---|
| Revenue, EBITDA, PAT gap | Consolidated minus standalone, per year | Locates where the business actually is — parent or subsidiaries |
| **Debt location** | Borrowings: consolidated vs standalone | Debt sitting in subsidiaries with profit in the parent looks healthy on one basis and stressed on the other |
| **Cash location** | Cash and investments: consolidated vs standalone; then by entity from AOC-1 | Cash in a 51%-owned or overseas subsidiary may be **trapped** — unavailable for dividends, buybacks or parent debt service without tax leakage or minority consent |
| Dividend capacity | Standalone free reserves and standalone cash flow vs dividend paid | A dividend not funded by parent-level cash flow is being funded by borrowing or by upstreaming that may not repeat |
| **PAT attributable to owners vs NCI** | Consolidated PAT split into owners' share and non-controlling interest | Headline consolidated PAT includes profit that is not yours. **Always value on the owners' share**, and use owners' equity for ROE |

**The AOC-1 statement (India)** — the "salient features of the financial statement of subsidiaries/associates/joint ventures", filed as an annexure to the Board's Report. This is the single most underused page in an Indian annual report. It lists **every** subsidiary, associate and JV with shareholding %, turnover, PAT, net worth and investments. US equivalents: **Exhibit 21.1** (list of subsidiaries, but no financials), Reg S-X **Rule 4-08(g)** summarised financial information, and **Rule 3-09** separate audited financial statements for significant equity investees.

**From the AOC-1, extract:**
- Every loss-making subsidiary, **and how many consecutive years** it has been loss-making.
- Whether the parent keeps funding those entities through equity infusion, loans, or guarantees (cross-check the RPT note and CARO 3(iii)).
- Subsidiaries with negative net worth — these are contingent claims on the parent regardless of legal separation.
- Entities with large turnover and negligible profit (possible pass-through or round-tripping structures), and entities with negligible turnover and large assets.
- Newly incorporated, newly acquired, **newly deconsolidated** or struck-off entities. A subsidiary that disappears between two annual reports needs an explanation; deconsolidation is a legitimate route to removing losses and debt from view.
- Overseas subsidiaries in jurisdictions with no operational rationale.

**Consolidation method matters enormously:**
- **Subsidiaries** — line-by-line; their debt and losses are visible.
- **Associates and JVs** — equity method; only the net share of profit appears, and **their debt is entirely invisible on your balance sheet**. A group can carry very large leverage inside 49%-owned entities while showing modest consolidated debt. Read the Ind-AS 112 / IFRS 12 disclosure of interests in other entities, which gives summarised financials for material associates and JVs, and add back your share of their debt when assessing group leverage.
- **Structured entities / SPVs** — check the control assessment. Off-balance-sheet vehicles are disclosed under Ind-AS 112 / IFRS 12; read that note in any infrastructure, real estate or financial company.

**Why:** consolidated shows the economic group; standalone shows what the listed entity actually controls and can pay dividends from. Both are true, and the difference between them is often the whole story.

---

## 10. Earnings-call transcripts and management Q&A behaviour

**Read the transcripts; do not listen to the calls.** Reading is faster, searchable, and lets you compare quarters side by side. Cover the last 8–12 quarters. Sources: company investor-relations page, exchange filings (India: transcripts must be filed within five working days under LODR), and 8-K Item 2.02 furnishings in the US.

**Split every transcript into scripted opening remarks and Q&A.** The opening remarks are a press release read aloud — tier "low". The Q&A is unscripted and is where the evidence is.

**Track across quarters:**

| Signal | How to observe it | What it means |
|---|---|---|
| **Guidance vs delivery** | Log every numeric commitment (revenue growth, margin, capex, debt reduction, capacity commissioning date) with the quarter it was made, then mark it met/missed/quietly dropped | Produces an objective management-credibility score no financial statement can give you |
| **Miss acknowledgement** | When a target is missed, is it named and explained, or reframed as if it never existed? | Acknowledgement is the cheapest possible honesty test |
| **Numeric question → numeric answer?** | Count questions asking for a specific number (segment margin, receivable days, subsidiary loss, capex phasing, one-off quantum) and how many get a number | "We don't disclose that", "directionally positive", "let's take this offline" clustering on the same line item quarter after quarter is a map of the problem |
| **Analyst access** | Which analysts are called on; whether known sceptics stop appearing; whether the call is cut short with questions in the queue | Curated Q&A is a governance signal, not a scheduling accident |
| **Attribution pattern** | Are misses always external (weather, elections, GST, freight, FX, "channel destocking") while beats are always management execution? | Consistent externalisation over many quarters is a stable trait, not a run of bad luck |
| **Who speaks** | Is the CFO on the call? Does a new CFO answer confidently on prior periods? | A CFO absent from calls, or unable to answer on their own numbers, is a real flag |
| **Format degradation** | Calls discontinued, moved to written-questions-only, pre-submitted questions, or transcripts stopped being filed | Reduction in accountability channels almost always precedes bad news |
| **Language recycling** | Diff the opening remarks across quarters | Identical paragraphs quarter after quarter mean nothing is being said |

**Maintain a running list of unanswered questions** and check whether they are ever answered. Also note what analysts stop asking about — a question that gets refused three times stops being asked, and the silence looks like resolution.

**India note:** many small- and mid-cap companies hold no calls at all. Absence of a concall is itself a data point about investor engagement, and it means you must lean harder on the filings.

---

## 11. Investor presentations vs audited filings

Take every headline metric in the deck — adjusted EBITDA, cash EBITDA, pre-exceptional PAT, "normalised" margin, net debt, order book, ARR, EBITDA pre-Ind-AS-116 — and reconcile it line by line to the audited statements.

**Interrogate every add-back:**
- Is it genuinely non-recurring? An "exceptional item" that appears in four of five years is an operating cost. Sum five years of exceptionals and compare to five years of reported PAT — the ratio is often startling.
- Restructuring, impairment, legal settlements and inventory write-downs are the usual repeat offenders.
- Share-based compensation added back is a real cost to you as a shareholder; see `references/03-earnings-quality.md`.
- Pre-IFRS-16/Ind-AS-116 EBITDA is legitimate for comparability, but only if lease payments are then deducted somewhere.

**Interrogate net debt specifically.** Check whether the deck's net debt excludes: acceptances / buyer's credit / channel financing, bills discounted with recourse, factoring, lease liabilities, preference shares and other compound instruments, deferred acquisition consideration, and cash that is restricted or held in subsidiaries. Reconcile to the balance sheet borrowings line and state the gap. See `references/06-valuation.md` for the full EV bridge.

**Interrogate unaudited operating metrics.** Order book, capacity, "addressable market", store count, ARR, GMV, and customer counts appear nowhere in the audited statements and are never verified by anyone. Ask whether the metric definition has changed (an ARR definition that quietly starts including one-time revenue), and whether an order book converts into revenue at the rate implied.

**What a problem looks like:** the gap between presented and audited figures widening year over year; a new adjusted metric introduced in the exact year the old one turned down; a metric definition changed without restating prior periods; charts with no y-axis; growth shown only in indexed form.

**Why:** presentations carry far weaker liability than audited filings. The size and direction of the gap is a direct measure of management's willingness to flatter, and non-GAAP metrics drifting further from GAAP each year is among the most reliable governance warning signs available.

---

## 12. DRHP / RHP / S-1 and offer documents

The offer document is the most legally exhaustive disclosure a company ever makes. It remains valuable long after listing — for an already-listed company, the old DRHP is still the best single source of pre-listing history.

**Extract:**
- **Litigation and regulatory-action history** of the company, subsidiaries, group companies, promoters and directors — criminal, tax, statutory and civil, with amounts. Nothing later in the company's life re-discloses this at the same granularity.
- **Objects of the issue**: how much is fresh capital going into the business versus **offer for sale** enriching selling shareholders. Also check whether stated objects include repayment of debt or "general corporate purposes" (which should be capped).
- **Pre-IPO placements and the price paid by earlier investors** versus the IPO price. A steep step-up in the months before listing tells you what sophisticated buyers thought the business was worth very recently.
- **Restated financials and the restatement adjustments**, with reasons. This shows how the pre-IPO accounts were originally kept — a long list of restatement adjustments is a statement about historical accounting discipline.
- **Risk factors**, written by lawyers under liability and far more candid than any subsequent annual report. Many risks disclosed in a DRHP are never mentioned again.
- **Promoter group entity list** — the definitive map for later RPT work.
- **Lock-in expiry dates** (India: promoter and anchor-investor lock-ins) or US lock-up expiry, which tell you about future supply and insider intent.
- Related-party transactions for the pre-IPO period, and any pre-IPO restructuring, transfer of assets or business between promoter entities and the issuer.

**US equivalents:** S-1 (domestic IPO), F-1 (foreign issuer), 424B prospectus, and for SPAC de-listings the S-4/proxy. Note that projections appear in SPAC merger documents and essentially nowhere else in US filings — and are almost never met.

**Why:** it is the one document written under maximum liability with maximum detail, and its restatement adjustments plus offer structure reveal both how the accounts were kept and what insiders intend to do with their shares.

---

## 13. Credit rating rationales and rating actions

Pull the **full rationale document**, not just the symbol, from **every** agency covering the company, plus the complete rating history. India: CRISIL, ICRA, CARE, India Ratings, Acuité, Brickwork — all publish detailed public rationales. US/global: Moody's, S&P, Fitch — press releases and credit opinions, less granular publicly but still valuable; supplement with bond indentures and covenant disclosures.

**Extract:**
- **Key rating strengths and weaknesses** in the agency's own words.
- **Liquidity assessment** (India: agencies grade it explicitly — Superior / Strong / Adequate / Stretched / Poor). This is the single most useful line, because balance-sheet ratios do not show undrawn lines, cash-flow timing or repayment bunching.
- **Rating sensitivities** — the explicit metric thresholds that would trigger an upgrade or downgrade. These are effectively externally-set covenants on your thesis; check your own computed numbers against them.
- The **list of rated facilities** with amounts, which reveals the bank-debt structure (fund-based vs non-fund-based limits, working-capital limits, term loans) far better than the balance sheet.
- Utilisation of working-capital limits over the past 12 months — agencies frequently disclose average and peak utilisation, and sustained near-100% utilisation is a liquidity warning.

**Rating actions to treat as events:**
- Outlook change (Stable → Negative) and placement on **Rating Watch**.
- Any downgrade, and especially a multi-notch downgrade.
- **Migration to "Issuer Not Cooperating" (INC)** — India-specific and widely ignored. The company has simply stopped supplying information to its own rating agency. Read it as a refusal to be examined.
- A rating withdrawal at the company's request.
- Any **default or "D" rating on any instrument of any group entity**, including unlisted ones. Contagion within promoter groups is real, and lenders act on group exposure.
- India: rating actions are themselves disclosable to exchanges under LODR Reg 30, so the exchange filing history gives you the timeline.

**Why:** rating agencies see bank facility details, covenant terms, month-by-month utilisation and management interactions that equity investors never get. Their liquidity paragraph routinely identifies stress one to four quarters before the equity market notices.

---

## 14. Exchange filings and continuous disclosure

Scan the company's **entire filing history**, not just results. This is where governance events surface first.

**India (NSE/BSE, SEBI LODR):**
- **Reg 30 material events** — board and KMP changes, plant shutdowns, contract wins/losses, litigation and regulatory orders, tax search/survey, acquisitions and disposals, fund-raising, default on payment obligations. Schedule III Para A events are automatically material; Para B events apply a quantitative threshold (broadly 2% of turnover, 2% of net worth, or 5% of average PAT of the last three years).
- **Reg 30(11) rumour verification** — top-listed companies must confirm or deny material market rumours; the response is informative.
- **Reg 31 pledge/encumbrance disclosures** and SAST Reg 29 acquisition/disposal disclosures.
- **PIT Reg 7 insider-trading disclosures** — promoter, director and KMP trades above ₹10 lakh in a quarter.
- **Reg 23 half-yearly RPT disclosures** in the prescribed format — often more granular than the annual note.
- **Reg 32 statement of deviation** in use of issue proceeds, and **Reg 33** quarterly results (limited review, not audited — check the review report for qualifications too).
- Scheme-of-arrangement filings, NCLT applications, IBC/insolvency petitions filed by or against the company or its subsidiaries, and any SEBI, RBI, CCI, NCLT, ED or tax-authority order.

**US (EDGAR):**
- **8-K** by item number — 1.01 material agreement, 1.03 bankruptcy, 2.02 results, 2.04 triggering of a direct financial obligation (covenant breach/acceleration), **4.01 auditor change**, **4.02 non-reliance on prior financials**, 5.02 departure/appointment of officers and directors, 5.07 shareholder-vote results.
- 10-Q, 10-K, DEF 14A, S-8 (equity plan registrations — a dilution signal), Form 144 (proposed insider sales), NT 10-K/NT 10-Q (late filing), and comment-letter correspondence (UPLOAD/CORRESP), which shows exactly what the SEC challenged in the accounting and how the company responded. Comment letters are underused and often excellent.

**Patterns that matter more than any single filing:**
- **Serial resignation of CFOs, company secretaries, or independent directors.** Read every resignation letter; independent directors resigning citing "personal reasons" shortly after a contentious board matter is a well-worn euphemism. This pattern reliably *precedes* trouble rather than following it.
- Insider transactions: what the people with full information do with their own money.
- **Filing timing.** Material bad news released late on a Friday, immediately before a long holiday, or minutes before/after market close is a deliberate attention-management choice. Log the timestamps.
- Repeated delays in filing results, or auditors' limited-review reports with qualifications.

---

## 15. Shareholding pattern and promoter pledge

**India:** quarterly shareholding pattern under LODR Reg 31. Track 12+ quarters.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Promoter holding trend | Promoter + promoter group % of total equity, quarter by quarter | Stable or rising; India requires ≥25% public float | A steady decline needs an explanation; "reclassification" of a promoter to public is a disclosed exit route worth checking |
| **Pledged shares** | Shares pledged/encumbered ÷ promoter holding, **and** ÷ total equity | Zero is the only comfortable level; >25% of promoter holding warrants a specific explanation; >50% is a live risk | A price fall triggers margin calls, forced sale and potentially loss of control — converting a valuation problem into a solvency and control crisis |
| Institutional holding | FII/FPI and DII/mutual-fund %, and the named funds | — | Quiet exits by long-standing institutional holders, especially domestic funds with local access, deserve investigation |
| Retail shareholder count | Number of small individual shareholders (disclosed in India) | — | A sudden surge in retail holders alongside institutional exit is a distribution pattern |
| Concentrated public holders | Non-institutional holders above 1%, named | — | Unknown FPIs or entities appearing across several promoter-linked companies suggest undisclosed concert |

*Indicative only; norms vary by market and ownership structure — a widely held US company has no promoter concept at all.*

**Also check:** invocation of pledged shares (disclosed separately); creeping acquisition under SAST; promoter share transfers to family trusts or holdcos; and whether the pledge is against borrowing by the *listed company* or by *promoter entities* — the latter means the listed company's shares are collateral for debt you cannot see and do not benefit from.

**US/global equivalents:** no promoter concept. Instead: SC 13D/13G (5%+ holders, with 13D signalling activist intent), Form 4 (insider transactions within two business days), 13F (institutional holdings, quarterly, 45-day lag), the DEF 14A beneficial-ownership table, dual-class structures and the proxy's disclosure of **pledging of company stock by executives** (many boards prohibit it — check the policy).

---

## 16. Proxy / AGM materials and voting results

**India:** the AGM/EGM notice with explanatory statements under s.102, plus the **scrutiniser's report on voting results** filed with the exchanges within two working days.
**US:** the DEF 14A, plus **8-K Item 5.07** for the voting outcome.

**Read each resolution and its explanatory statement for:**
- **Managerial remuneration** — total promoter/founder-family pay against PAT, against peer CEO pay, and against its own trajectory. Check the fixed/variable split and what the variable is actually linked to. India: s.197 caps (11% of net profits overall; 5% for one MD/WTD, 10% for all together) and the requirement for a special resolution to exceed them, or in the case of inadequate profits, Schedule V compliance. US: the Compensation Discussion and Analysis, CEO pay ratio, and the pay-versus-performance table (which does the comparison for you).
- **Director appointments and re-appointments** — genuine independence (prior employment, business relationships, tenure), number of other board seats (over-boarding), attendance record, and any regulatory disqualification.
- **Related-party approvals** — see §6; confirm interested parties abstained.
- **Share issuance, preferential allotment, warrants and ESOP authorisations** — size the potential dilution and the exercise price. Warrants issued to promoters at a price near a cyclical low are a value transfer.
- **Auditor appointment/re-appointment** and the proposed fee.

**Then read the voting results themselves.** This is the part most analysts skip and it is quantified, public and unambiguous.

- Compute, per resolution, the **% of institutional votes cast against** and the **% of non-promoter public votes cast against**.
- A resolution that passes only on promoter votes while 60–90% of institutional votes oppose it is an explicit no-confidence vote from investors who have met management. Treat it as a governance finding of the same weight as an accounting flag.
- Rising against-votes across successive years on the same theme (remuneration, a specific director, RPTs) shows a board that is not responding to shareholders.
- Read proxy advisory recommendations where available (India: IiAS, SES, InGovern; US: ISS, Glass Lewis) — and read the company's rebuttal if it issued one.
- US: say-on-pay support below ~70% is conventionally treated as a rebuke requiring board response.

---

## 17. Short-seller reports, forensic notes and adverse media

Search for any short-seller report, forensic accounting note, regulator order, or investigative journalism on the company **or any group entity**.

**How to read one properly:**
1. **Read the report and the company's rebuttal side by side, allegation by allegation.** Build a three-column table: allegation | company's response | your verification. This is the whole method.
2. **Judge the rebuttal by what it engages with.** Specific allegations answered with documents, bank confirmations, registry records and named counterparties are genuine responses. Allegations answered with adjectives ("baseless", "malicious"), attacks on the author's motives, nationalist framing, or a defamation suit are non-responses — and a systematic pattern of non-response across allegations is itself high-grade evidence.
3. **Verify the checkable claims yourself** against primary sources: registry filings for the alleged shell counterparties (India: MCA21; UK: Companies House; equivalents elsewhere), subsidiary statutory accounts, customs and trade data, land and property records, litigation dockets, employee counts, satellite imagery for claimed facilities. A report's value is concentrated in the claims you can independently confirm.
4. **Note the author's disclosed position and incentive.** A short seller profits from the price falling and is selecting evidence accordingly. That does not make the evidence false; it means treat the report as a **hypothesis generator, never a conclusion**.
5. **Separate the allegations by type.** Accounting-manipulation claims can often be checked from filings. Claims about undisclosed related parties, circular revenue or shell counterparties require outside records. Claims about intent or future regulatory action cannot be verified at all — discount them.

**Why:** these reports concentrate months of forensic work into one document and frequently surface structures — undisclosed related parties, circular transactions, shell counterparties, inflated asset claims — that filings alone would take years to find. See §13 of `references/07-forensic-red-flags.md` for the independent-verification techniques.

---

## 18. Secretarial audit and Directors' Report annexures

Largely India-specific, and consistently under-read.

- **Secretarial audit report (Form MR-3)**, mandatory for listed and prescribed companies under s.204, plus the **Annual Secretarial Compliance Report** under LODR Reg 24A. Read the qualifications and observations. These reveal statutory non-compliance — late filings, invalid appointments, procedural failures on RPTs or on board/committee composition — that never touches the financial statements. Also check whether material unlisted subsidiaries got their own secretarial audit, which is required.
- **Corporate governance report**: board composition and independent-director count, whether the chair is independent or is the promoter, board and audit-committee meeting frequency and **individual attendance**, committee composition, and the number of board meetings held at short notice. An audit committee that meets four times a year for an hour is not overseeing anything.
- **Independent director resignations** — read the letter and the stated reasons (India requires the reason to be disclosed and requires the director to confirm there are no other material reasons).
- **ESOP disclosures** — grants, exercises, outstanding options, exercise prices and potential dilution.
- **s.186 loans, guarantees and investments** disclosure — cross-check against the RPT note.
- **CSR** spend vs obligation and unspent transfers (small money, but a clean compliance signal).
- **BRSR** (Business Responsibility and Sustainability Report) for the top listed companies, with BRSR Core assured — useful for regulatory, environmental and litigation exposure; treat unassured sections as management narrative.
- **Cost audit report** where applicable (regulated and manufacturing sectors) — segment-level cost data unavailable anywhere else.

**US analogues:** corporate governance content sits in the DEF 14A (board independence, committee composition, attendance, related-party policy), governance guidelines and committee charters on the IR site, and NYSE/Nasdaq listing-standard compliance disclosures.

---

## 19. Sector translation: which documents replace the standard set

The governing principle applies to documents, not just ratios. For several sectors, the documents above are secondary and the real disclosure lives elsewhere. Read the sector playbook before deciding what to prioritise.

| Sector | Read instead of / in addition to the standard set | What to extract |
|---|---|---|
| **Banks** | Basel **Pillar 3 disclosures**; notes on asset quality; RBI risk-assessment **divergence disclosure**; restructuring and resolution-framework notes; annual report "Notes on accounts" schedules | GNPA/NNPA reconciliation and slippages, provision coverage, sector and borrower concentration, restructured and SMA book, divergence between RBI-assessed and reported NPAs (an auditor-adjacent disclosure with no equivalent elsewhere), capital adequacy and its components |
| **NBFCs / HFCs** | ALM (asset-liability maturity) statement, borrowing mix disclosure, RBI scale-based-regulation disclosures, securitisation/direct-assignment notes, co-lending arrangements | Maturity mismatch by bucket, dependence on short-term funding, off-book AUM, credit-enhancement obligations retained on securitised pools |
| **Insurers** | Public disclosures forms (India: L-series for life, NL-series for general); **embedded value report and its actuarial assumptions**; appointed actuary's certificate; solvency statement | EV movement analysis, VNB margin and its assumption sensitivity, persistency, solvency ratio, reserving assumptions. Standard ratios like EBITDA and ROCE are undefined here |
| **REITs / InvITs** | Independent **valuation report** (half-yearly in India), distribution statement, manager fee structure, related-party leases | Valuer identity and independence, cap rate assumptions, NAV movement, NDCF computation, manager fees as % of AUM, sponsor-related leases |
| **Miners / E&P** | **Reserve and resource statements** under JORC / NI 43-101 / SEC S-K 1300 / SPE-PRMS; technical reports; independent qualified person's sign-off | Proven vs probable split, reserve life, grade trend, the commodity price deck used, who certified it and their independence. Reserves are the balance sheet for these companies and are *not* audited by the financial auditor |
| **Utilities / regulated** | Tariff orders, regulatory-asset notes, PPA terms, regulator filings | Regulated return allowed vs earned, regulatory assets/deferrals recoverable, true-up timing |
| **Pharma** | Regulatory inspection outcomes (US FDA Form 483s, warning letters, import alerts), ANDA/patent litigation dockets | Facility-level compliance status, remediation timelines, exclusivity expiries |

For all of these, standard EBITDA/ROCE/working-capital analysis is either undefined or misleading. Read the matching `references/sectors/*.md` before computing anything.

---

## 20. Archive and data-provenance hygiene

**Build your own archive.** Companies remove old documents from their websites, and they do it most often when the old documents are inconvenient. Download and retain: 7–10 years of annual reports, all quarterly results and transcripts, the DRHP, credit rating rationales, investor decks and material exchange filings. India: BSE/NSE announcement archives and SEBI's filings retain much of it independently; US: EDGAR retains everything permanently and is the canonical source.

**Compute key figures yourself from primary filings.** Aggregators are useful for screening and unreliable for conclusions.
- Verify at least the top five metrics (revenue, EBITDA, PAT, total debt, cash) against the source document before building any thesis on them.
- Establish whether the aggregator is showing **standalone or consolidated** — many silently mix the two across years or across companies within the same peer table.
- Establish how it treats **exceptional items, lease accounting (Ind-AS 116/IFRS 16), and minority interest**. Different treatments make peer comparisons meaningless.
- Check its **fiscal-year alignment** convention when comparing companies with different year ends.

**Reconcile restated comparatives.** Take last year's annual report and this year's, and compare the prior-year column in each. Silent restatements — prior-period figures quietly changed with no note explaining why — are a specific, detectable form of manipulation, and only a self-maintained multi-year archive will reveal them. Legitimate restatements (a genuine error corrected under Ind-AS 8 / IAS 8, a discontinued operation reclassified, a segment redefinition) carry a note explaining the change; the absence of that note is the flag.

**Record provenance for every number you use**: document, page or note number, period, consolidated/standalone, currency and units, and the date you retrieved it. This feeds directly into the data-quality note required by the output contract in `SKILL.md`.

---

## Checklist

- [ ] **Entire annual report walked section by section against the §0 contents map**; every section either mined for material content or recorded as "read — nothing material" — none left unopened.
- [ ] Auditor's report read in full for **both standalone and consolidated**; opinion type recorded for 5 years.
- [ ] Any modification quantified and the financials restated before any ratio was computed.
- [ ] Going-concern paragraph checked; every KAM/CAM extracted, mapped to its note, and tracked across years.
- [ ] Emphasis of Matter and Other Matter read; **% of consolidated assets/revenue/profit not audited by the principal auditor, or unaudited, quantified**.
- [ ] India: CARO annexure read clause by clause — statutory dues, defaults, short-term funds for long-term use, evergreening, bank-return divergence, fraud reporting, auditor resignation, one-year liquidity uncertainty.
- [ ] IFC/ICFR opinion checked for material weakness and for repeat weaknesses; US: noted whether a 404(b) auditor attestation exists at all.
- [ ] Auditor tenure, rotation, audit vs non-audit fees checked; any resignation letter or 8-K Item 4.01/4.02 read.
- [ ] MD&A read for 3–5 years side by side; promise-vs-delivery table built; risk-factor changes diffed.
- [ ] Accounting policies and critical estimates read; every change quantified and peer-compared; affected years restated.
- [ ] Contingent liabilities tabulated 5 years, expressed as % of net worth and market cap; group guarantees isolated; capital commitments sized.
- [ ] RPT note fully extracted, including **year-end balances**; RPT sales/purchase shares computed; approvals and voting dissent verified.
- [ ] Segment revenue, EBIT, capital employed and ROCE computed per segment for 5 years; any segment redefinition explained.
- [ ] Consolidated vs standalone reconciled for revenue, EBITDA, PAT, **debt and cash**; trapped cash identified; NCI stripped out before valuation.
- [ ] AOC-1 / Exhibit 21.1 read; loss-making, negative-net-worth, newly acquired and newly deconsolidated entities listed; equity-method associate debt added back to group leverage.
- [ ] 8–12 transcripts read; guidance-vs-delivery log built; refused questions and analyst-access patterns recorded.
- [ ] Investor-deck metrics reconciled to audited figures; every add-back tested for recurrence; net-debt definition decomposed.
- [ ] DRHP/S-1 checked for litigation history, OFS share, pre-IPO pricing, restatement adjustments and lock-in expiry.
- [ ] Full rating rationales pulled from all agencies; liquidity grade, rating sensitivities and any INC/watch/downgrade recorded.
- [ ] Exchange filing history scanned for KMP resignations, insider trades, pledge changes, regulatory orders and Friday-evening disclosures.
- [ ] Shareholding pattern tracked 12+ quarters; pledge as % of promoter holding **and** of total equity computed.
- [ ] AGM notice and **scrutiniser's voting results** read; institutional against-votes per resolution recorded.
- [ ] Short-seller/forensic material located; allegations, rebuttal and your own verification tabulated.
- [ ] Secretarial audit (MR-3) qualifications, board composition and attendance checked.
- [ ] Sector-specific primary documents (Pillar 3, EV report, valuation report, reserve statement) read where the standard set does not apply.
- [ ] Top five metrics verified against primary filings; prior-year comparatives reconciled across two annual reports for silent restatements; provenance recorded for every figure used.
