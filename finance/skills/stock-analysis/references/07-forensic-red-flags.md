# Forensic Accounting and Red Flags

Use this when: you are running the Stage 3 kill-criteria screen or the Stage 4 forensic pass, or any time reported profit, growth or asset values look better than the business economics you can observe from outside.

Forensic work is not about proving fraud. It is about deciding how much weight the reported numbers can carry, because every figure you use downstream — margin, ROCE, EV/EBITDA, FCF yield — is only as good as the accounting policy that produced it, and management chooses that policy. Your job is to locate where discretion was exercised, quantify how much of reported performance depends on it, and say so plainly. The governing rule of this skill applies at full force here: a red flag is meaningless until you know the sector and the company's own history. Rising receivables are normal in EPC and alarming in FMCG; negative operating cash flow is a fraud signal for a distributor and business as usual for a growing lender.

## Contents

- [0. How frauds are actually caught](#0-how-frauds-are-actually-caught)
- [1. Cash flow vs earnings: the accruals tests](#1-cash-flow-vs-earnings-the-accruals-tests)
- [2. Proof of cash: does the cash exist and is it yours?](#2-proof-of-cash-does-the-cash-exist-and-is-it-yours)
- [3. Revenue-side manipulation](#3-revenue-side-manipulation)
- [4. Working-capital manipulation and period-end window dressing](#4-working-capital-manipulation-and-period-end-window-dressing)
- [5. Cost capitalisation and expense deferral](#5-cost-capitalisation-and-expense-deferral)
- [6. Acquisition accounting and serial acquirers](#6-acquisition-accounting-and-serial-acquirers)
- [7. Disclosure and metric games](#7-disclosure-and-metric-games)
- [8. Auditor signals](#8-auditor-signals)
- [9. People signals: CFO and audit-committee turnover](#9-people-signals-cfo-and-audit-committee-turnover)
- [10. Structural opacity and off-balance-sheet exposure](#10-structural-opacity-and-off-balance-sheet-exposure)
- [11. Tax anomalies](#11-tax-anomalies)
- [12. India: the mandatory disclosures that do forensic work for you](#12-india-the-mandatory-disclosures-that-do-forensic-work-for-you)
- [13. Independent verification: the part that actually catches frauds](#13-independent-verification-the-part-that-actually-catches-frauds)
- [14. Composite forensic scores and statistical tests](#14-composite-forensic-scores-and-statistical-tests)
- [15. Sector translation: where these tests are undefined or inverted](#15-sector-translation-where-these-tests-are-undefined-or-inverted)
- [16. Calibration: how to report a red flag and what it changes](#16-calibration-how-to-report-a-red-flag-and-what-it-changes)
- [Checklist](#checklist)

---

## 0. How frauds are actually caught

Internalise this before you start, because it determines how you allocate effort.

**Every major accounting fraud reconciled internally.** Satyam, Enron, Parmalat, Wirecard, Luckin, NMC Health, Sino-Forest, Carillion — in each case the balance sheet balanced, the cash flow statement tied to the balance sheet, the ratios were computable, and a competent desk analyst working purely from the filings could complete a full checklist without the numbers contradicting each other. Fabricated financials are internally consistent by construction, because whoever fabricated them had to make them tie.

Two consequences:

1. **Filings-based forensics detects distortion, not fabrication.** Ratio work reliably catches aggressive accounting — pulled-forward revenue, deferred costs, cookie-jar reserves, over-capitalisation. It is much weaker against a business that does not exist, because there the "distortion" is complete and self-consistent.
2. **The decisive evidence is almost always non-company evidence.** Bank confirmations, customs and shipping records, satellite imagery, registry filings in the operating jurisdiction, employee and customer contact, alternative data. Section 13 is not an optional extra at the end of this file; for any company where the fraud hypothesis is live, it *is* the analysis.

So run the quantitative tests to **generate hypotheses about which line item is doing the work**, then attack that line item with outside evidence. Never conclude "the accounts reconcile, therefore they are real."

**Triage order when time is limited.** Cash conversion over five years → interest-income reconciliation on the cash balance → DSO and receivables-vs-sales growth → capex vs depreciation → audit opinion, KAMs and auditor changes → related-party and promoter-pledge disclosure. Those six take under an hour from the filings and catch the overwhelming majority of distortion cases. Everything else in this file is depth applied where those six point.

---

## 1. Cash flow vs earnings: the accruals tests

Profit is an opinion; cash is closer to a fact. The single highest-yield forensic exercise is to lay reported profit alongside operating cash flow for five or more years and ask where the difference went.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Cash conversion | CFO ÷ net profit, per year **and cumulative over 3–5 years** | Cumulative ≥ 0.8–1.0 for mature businesses; ≥ 1.0 for asset-light | Cash is far harder to fabricate than accrued profit; a persistent gap means profit is sitting in receivables, inventory or capitalised costs |
| Cumulative gap | Σ CFO (5y) − Σ PAT (5y), in absolute currency | Small relative to cumulative PAT | Single-year gaps are noise; a five-year gap is a structural claim about earnings quality |
| Sloan accrual ratio (balance-sheet) | ΔNOA ÷ average NOA, where NOA = (total assets − cash & investments) − (total liabilities − total debt) | Below ~10%; sustained >15–20% is a flag | Growth funded by expanding non-cash assets rather than cash generation predicts weaker future returns and higher restatement risk |
| Sloan accrual ratio (cash-flow) | (PAT − CFO − CFI) ÷ average NOA | As above | Less vulnerable to acquisition and restatement noise than the balance-sheet version |
| FCF conversion | (CFO − capex) ÷ PAT, cumulative 5y | Positive and rising for a mature business | EBITDA and even CFO can be flattered by classification; capex is where deferred costs finally surface |
| EBITDA-to-FCF gap | EBITDA − (CFO − capex), as % of EBITDA, trend | Stable | A widening gap is the signature of costs migrating from the P&L into the investing section |

*Indicative ranges vary by market, cycle and period; peer and own-history comparison overrides any absolute band.*

**How to run it.** Build a five-year table: PAT, CFO, capex, FCF, ΔWorking capital, D&A, non-cash items. Then answer explicitly: **if profit did not become cash, which asset did it become?** Receivables, inventory, CWIP, intangibles, loans and advances to related parties, and "other current assets" are the usual destinations, and each points to a different section of this file.

**Legitimate explanations you must rule out before flagging.** A genuinely fast-growing, working-capital-intensive business (distribution, EPC, capital goods) consumes cash while growing and will show CFO below PAT for years; that is arithmetic, not fraud. Test it by computing working capital as a **percentage of sales**. If that ratio is stable and only the absolute number grows, the cash gap is growth. If working capital as a % of sales is itself climbing, the growth is being bought.

**Cash-flow-statement integrity check.** Tie the working-capital movements shown in the cash flow statement to the year-on-year changes in the corresponding balance-sheet lines. They will rarely match exactly — acquisitions, disposals, FX translation and reclassifications legitimately break the tie — but the company should be able to explain the bridge, and large unexplained differences are where reclassification games live. If the balance sheet shows receivables up 40% while the cash flow statement shows a small receivables outflow, something was moved: securitised, reclassified to "other assets", or acquired. Find out which.

**Classification traps — resolve before comparing CFO across companies.**
- Under Ind-AS and IFRS, interest paid may sit in operating **or** financing, and interest and dividends received in operating or investing. Under US GAAP the classification is fixed. Two identical businesses can report materially different CFO. **Re-derive CFO on a common basis** (interest paid in financing, interest received in investing is a clean convention) before any cross-company or cross-regime comparison, and state the convention you used.
- Receivables securitisation or factoring turns what is economically borrowing into an operating inflow. Find the disclosed amount factored and add it back to receivables when computing DSO.
- Supply-chain finance / reverse factoring keeps supplier debt inside trade payables and flatters both CFO and reported leverage. Disclosure is often thin; look in the payables note, the liquidity discussion and rating-agency commentary. This is the Carillion and Abengoa mechanism.
- Purchases of "investments" that are economically operating assets; leases restructured so outflows fall below the CFO line.

**Quarterly integrity.** Sum the four reported quarters and compare to the audited annual figure for revenue, EBITDA and PAT. **India:** quarterly results are limited-review, not audited, and Q4 is normally a balancing figure — audited full year minus nine months. Provisions, true-ups and rev-rec adjustments therefore cluster in Q4. A Q4 whose margin, other income or tax rate looks nothing like the 9M run-rate is telling you exactly where discretion was exercised. **US:** compare the 10-K to the sum of the 10-Qs and read the fourth-quarter adjustment disclosure.

---

## 2. Proof of cash: does the cash exist and is it yours?

Fake, pledged or unrepatriable cash is the single most common feature of the largest accounting frauds. Standard analysis nets cash against debt and moves on. Do not. Cash is an asset like any other and requires an existence test.

**The interest-income reconciliation.** The cheapest high-severity test available. Run it on every company holding a large cash balance.

1. Average cash and liquid investments = (opening + closing) ÷ 2. Use quarterly averages where available; annual averages are badly distorted by a fundraise or a year-end sweep.
2. Take interest and investment income from the other-income note. Isolate it from FX gains, dividend income from operating subsidiaries, government grants and profit on asset sales.
3. Implied yield = investment income ÷ average cash and investments.
4. Compare to prevailing short-term deposit and money-market rates for that currency and period. India: bank fixed-deposit and liquid-fund rates, which track the repo. US/global: T-bill and money-market rates.

An implied yield far below the risk-free short rate means one of: the cash is not there; it is pledged or restricted; it sits in non-interest-bearing current accounts; or it sits in a low-rate jurisdiction. Every one of those is something you need to know before treating the balance as net-debt relief.

**Caveats that produce false positives — resolve them before flagging.**
- **India / Ind-AS:** returns on liquid mutual funds are reported as "net gain on fair value changes" under Ind-AS 109, not as interest income. Counting only "interest income" manufactures a false flag. Sum the entire investment-return block.
- Cash raised late in the period earns almost nothing — check the timing of any issuance or asset sale.
- Operating float in current accounts legitimately earns nothing, but a company should not hold years of surplus that way.
- Interest income is netted against interest expense in some presentations.
- Cash in subsidiaries in low-rate or capital-controlled jurisdictions earns local rates and may not be repatriable.

**The other cash tests.**

| Test | What to compute / read | Why it matters |
|---|---|---|
| Gross cash alongside gross debt | Cost of carry = (average debt cost − implied cash yield) × overlapping balance | A company paying 9% to borrow while earning 4% on an equal cash pile destroys value every year for no stated reason. Either the cash is encumbered or absent, or there is an undisclosed constraint. A classic tell; management should have a specific answer |
| Restricted / pledged cash | Balance-sheet split, notes, and the charge registry (India: MCA charges; US: security disclosures in the debt note) | Cash pledged against borrowings is not available to shareholders and must be excluded from net-debt maths |
| Where the cash is banked | Names of banks in the deposits note; jurisdiction | Deposits concentrated in small, obscure, offshore or promoter-linked banks are a severe flag. Large groups bank with large banks |
| Repatriability | Cash held in subsidiaries; tax cost of upstreaming; capital controls | Consolidated cash can be legally unavailable to the listed parent |
| Audit evidence for cash | Is "existence of cash and bank balances" a Key Audit Matter? Did the auditor obtain direct bank confirmations? | If the auditor flagged cash existence as a KAM, so should you |
| Dividend reality | Dividends and buybacks paid ÷ reported PAT, over 5 years | Cash actually leaving the company to shareholders is the hardest confirmation that it existed. A company that reports a decade of profits, never pays out, never deleverages and keeps raising capital is asserting cash it cannot demonstrate |
| **India:** CARO commentary | Funds raised for one purpose applied to another; short-term funds used for long-term purposes; loans and advances to related parties | CARO forces explicit auditor comment on precisely these leakage routes |

---

## 3. Revenue-side manipulation

Revenue is the number valuation multiples attach to, so manipulation concentrates there. Read the revenue-recognition policy in full (Ind-AS 115 / IFRS 15 / ASC 606) and the critical-estimates note, not the summary.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| DSO | (Receivables ÷ revenue) × 365; five-year trend **and** vs peers | Flat to falling; level is sector-bound | Rising DSO means sales are booked faster than collected — the leading indicator of both channel stuffing and fabricated customers |
| Receivables growth ÷ revenue growth | Both in %, same consolidation basis | ≈ 1.0 | Persistently >1.3–1.5 means growth is being bought with credit, or invented |
| Unbilled revenue / contract assets ÷ revenue | Ind-AS 115 / ASC 606 disaggregation note | Stable; low outside project businesses | Unbilled revenue is a management estimate with no invoice behind it — the softest revenue there is |
| Allowance for expected credit loss ÷ gross receivables | Receivables note | Stable or rising as the book grows and ages | A shrinking allowance against a growing, ageing book is deliberate under-reserving |
| Receivables > 6 months / > 1 year (India) | Schedule III ageing table for trade receivables | Small and stable; disputed balances minimal | Old receivables that are not provided for are tomorrow's write-off, disclosed today |
| "Other receivables" / "other current assets" ÷ current assets | Balance sheet and notes | Small and stable | The standard hiding place for balances that belong nowhere legitimate |
| Deferred revenue growth vs revenue growth | Both in % | Similar for subscription models | Revenue growing while deferred revenue shrinks means the future is being consumed today |
| Revenue and gross profit per employee | ÷ headcount, five-year trend and vs peers | Stable to rising | Hard to fabricate; independently validates or refutes claimed scale |

*Indicative ranges vary by market, cycle and period; peer and own-history comparison overrides any absolute band.*

**Mechanisms to look for by name.**
- **Channel stuffing** — shipping to distributors at period end with generous return rights. Tells: quarter-end or Q4 revenue spikes beyond seasonality, DSO jumping in the final quarter, disclosed distributor inventory rising, returns and rebate provisions moving oddly.
- **Bill-and-hold** — revenue on goods not shipped. Requires specific disclosure; if disclosed, treat as material and quantify.
- **Gross vs net (principal vs agent)** — reporting gross merchandise value rather than commission inflates the top line by an order of magnitude without adding a rupee of profit. Critical for marketplaces, travel, energy trading, distribution and payments. Test: revenue ÷ gross profit. A switch from net to gross manufactures "growth" out of nothing and must be restated before any multiple is applied.
- **Percentage-of-completion / input-method revenue** (EPC, infrastructure, defence, capital goods, shipbuilding) — revenue is a function of a cost-to-complete estimate management controls. Watch cost-to-complete revisions, growing unbilled revenue and retention money, claims recognised as receivables, and margin recognised early in contracts.
- **Round-tripping** — sales to entities funded, directly or circularly, by the company or its promoters. Cross-check the related-party note against the customer-concentration disclosure.
- **Vendor / customer financing** — lending to customers, guaranteeing their debt, or accepting long-dated seller notes so they can buy. Track notes receivable, long-dated receivables and off-balance-sheet customer guarantees against revenue growth. It reads as clean organic growth until the credit sours, then reverses violently. Common in telecom equipment, solar, EV, capital goods and anyone selling to weaker counterparties.
- **Policy or estimate change** — any change in recognition timing, standalone-selling-price allocation, or warranty/returns estimate that raises current revenue. Quantify the effect; it is usually disclosed.

**India-specific cross-checks.** Reconcile reported revenue against GST turnover (GSTR-1/3B summary where the company or a data vendor provides it), e-way bill volumes for goods businesses, and DGFT/customs export data for exporters. A material, persistent gap between accounting revenue and tax-reported turnover with no reconciliation in the notes is a serious flag, because the two numbers are filed with different parties who have opposing incentives. Also compare standalone and consolidated revenue: revenue existing only in unlisted or offshore subsidiaries deserves specific scrutiny.

---

## 4. Working-capital manipulation and period-end window dressing

The balance sheet is a snapshot on one day, and management knows which day.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| DIO | (Inventory ÷ COGS) × 365 | Flat vs own history; level sector-bound | Rising inventory is either weakening demand or costs parked in the balance sheet |
| Finished goods ÷ total inventory | Inventory note | Stable | Finished goods rising faster than raw materials means product is not selling |
| Inventory provision ÷ gross inventory | Inventory note | Stable or rising with age | Under-reserving inflates gross margin now and forces a write-down later |
| DPO | (Payables ÷ COGS) × 365 | Stable | A DPO spike is the easiest way to manufacture one year of operating cash flow |
| Cash conversion cycle | DSO + DIO − DPO | Stable or improving; compare to peers | The composite; divergence from peers needs a business reason |
| Period-end vs average balances | Quarter-end cash, receivables, payables and borrowings vs intra-period averages | Similar | Large period-end-only movements are window dressing, especially in borrowings and cash |
| Implied average debt | Interest expense ÷ average interest rate, compared to reported year-end debt | Similar | If actual interest implies materially more debt than the year-end balance, the year-end balance is not representative |

**Specific patterns.** Gross margin expanding while DIO expands (costs absorbed into inventory rather than COGS). Payables stretching in the exact year CFO needed to look good, reversing the next. Receivables factored days before period end to flatter DSO. Borrowings repaid on the last day of the year and redrawn on the first day of the next — the implied-average-debt test above is the leverage analogue of the interest-income test in Section 2, and is worth running on any company with a suspiciously clean year-end balance sheet.

**India:** CARO requires the auditor to state whether inventory verification was performed and whether discrepancies of 10% or more were found and properly dealt with, and — for working-capital limits above ₹5 crore sanctioned against current assets — whether the quarterly statements filed with the banks **agree with the books of account**. That clause is an auditor-attested reconciliation of reported receivables and inventory against what the company told its lenders. Read it. A disagreement there is one of the most concrete red flags available in any annual report anywhere.

---

## 5. Cost capitalisation and expense deferral

Capitalising an operating cost inflates profit and EBITDA, moves the outflow from operating to investing, and therefore flatters CFO as well. It is the WorldCom mechanism, and it survives in far milder everyday forms.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Capex ÷ depreciation | Cash capex ÷ D&A, five-year average and trend | ≈ 1.0–1.5 for a steady business; higher only with matching capacity or revenue growth | Sustained capex far above depreciation without volume growth means the spend is not producing output — or is not really capex |
| Implied useful life | Average gross block ÷ annual depreciation | Stable year to year; in line with peers on similar assets | A lengthening implied life raises profit permanently with no cash effect and no announcement |
| Capitalised development / software ÷ revenue | Intangibles note | Low and stable; zero for many businesses | Under IFRS/Ind-AS development costs *may* be capitalised where US GAAP is stricter — the choice itself is a policy signal, and a cross-regime comparability problem |
| CWIP ÷ gross block, plus CWIP ageing (India) | Schedule III mandates CWIP and intangible-under-development ageing (<1y, 1–2y, 2–3y, >3y) and disclosure of projects overdue or over budget | Little CWIP older than two years; projects capitalised on schedule | CWIP that never converts to fixed assets is where impairments hide. The mandatory ageing table makes this directly checkable |
| Change in useful lives / amortisation periods | Accounting-policy note, year over year | No change without a stated operational reason | The cheapest way to raise reported profit |
| Growth in intangibles and "other assets" vs revenue | Balance sheet vs P&L | In line | The residual dumping ground for deferred costs |

Also check: **capitalised borrowing costs** (raises reported profit and interest coverage simultaneously — recompute coverage using total interest *incurred*, not just interest expensed); capitalised customer-acquisition and contract-fulfilment costs under Ind-AS 115 / ASC 606; capitalised labour; and **capital advances to suppliers**, which in India are a recurring route for funds to leave the company toward related parties without ever appearing as a related-party loan.

The composite tell for this whole section is **strong EBITDA with weak or negative free cash flow, sustained across years**. If an EBITDA growth story is not visible in FCF after a full capex cycle, the costs did not disappear — they moved.

---

## 6. Acquisition accounting and serial acquirers

Acquisitions reset the baseline, and purchase accounting hands management a set of one-time, non-cash levers that present as recurring growth. Treat any company doing more than one deal a year as requiring this section, and pair it with the serial-acquirer overlay in `references/13-situations.md`.

**Separate organic from acquired growth first.** Compute revenue growth excluding acquisitions completed in the last twelve months. If disclosure does not permit it, say so explicitly and treat headline growth as unverified — a serial acquirer that will not disclose organic growth is telling you something. Then ask the decisive question: **what does the growth rate become when M&A pauses?** For many roll-ups the answer is negative, which is precisely why the M&A never pauses.

**Purchase-accounting levers to inspect in the business-combination note.**
- **Fair-value step-ups** on inventory and fixed assets — the step-up depresses post-acquisition gross margin as inventory sells through, which management then adds back as a "non-cash purchase accounting adjustment", permanently.
- **Restructuring and contingency reserves created on acquisition**, later released to earnings. Classic cookie jar: the charge never touches the P&L going in, but the release boosts it coming out.
- **Purchase-price allocation skewed to goodwill and indefinite-lived intangibles** (not amortised) rather than to finite-lived intangibles (amortised). Raises reported EPS for years with no economic difference.
- **Contingent consideration / earnout remeasurement** through the P&L — a gain when the acquired business underperforms is a perverse, non-economic profit.
- **Bargain purchase gains** — a "profit" from buying cheaply, recognised immediately. Never recurring earnings.
- **Recurring "integration" and "deal" costs** — appearing every single year makes them operating expenses, and adjusted EBITDA that excludes them overstates earning power by exactly that amount.
- **Same-store / like-for-like decay hidden under pro-forma presentation** — check whether the acquired businesses shrink after acquisition. That is the specific signature of a roll-up manufacturing EPS from deal flow rather than operations.

**Goodwill and intangibles.**

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Goodwill ÷ total assets | Balance sheet | Modest; interpret against deal history | High goodwill means the balance sheet is mostly prices paid, not assets owned |
| (Goodwill + intangibles) ÷ equity | Balance sheet | Well below 100% | Above 100% means tangible equity is negative, and leverage ratios computed on reported equity become meaningless |
| Tangible book value | Equity − goodwill − intangibles | Positive for most non-software businesses | The capital actually standing behind the debt |
| Impairment-test headroom | Discount rate, terminal growth and disclosed headroom in the impairment note | Assumptions consistent with the company's own cost of capital and realistic growth | An impairment test that passes only on a terminal growth rate above nominal GDP is not passing |

Market capitalisation persistently below book value with no impairment recorded is a direct disagreement between the market and the balance sheet, and the market is usually right first. An impairment landing immediately after the growth narrative breaks confirms the M&A destroyed value; the analytical failure was not marking it earlier.

---

## 7. Disclosure and metric games

Here the manipulation is in the definition, not the arithmetic.

**Non-GAAP / adjusted earnings.** Tally every "exceptional", "one-off", "restructuring" and "impairment" item across five years. Items appearing every year are recurring costs and belong in normalised earnings. Compute the GAAP-to-adjusted gap as a % of reported profit and track whether it widens. Watch for add-backs of ordinary operating costs, of share-based compensation (a real cost paid in dilution — quantify it), and of "growth investments" that are simply opex. Big-bath charges clustered around a CEO or CFO transition and quietly released later are the cookie-jar pattern. US filers must publish a Reg G / Item 10(e) reconciliation — read it rather than the press-release headline.

**Bespoke KPIs.** Catalogue every company-invented metric — ARR, bookings, backlog, GMV, MAU/DAU, take rate, "cash EBITDA", "contribution margin ex-marketing", "adjusted community EBITDA", store-level unit economics — and write down its exact definition from the filing. Then ask three questions: (a) does it reconcile to an audited number? (b) has the definition changed year over year? (c) is management steering attention to it precisely because the audited numbers rolled over? Bespoke metrics are not inherently illegitimate — for a subscription or platform business they may be the most informative numbers available — but they are unaudited, management-defined and definitionally unstable. **Record the definition alongside the number every time you use one**, and never build a valuation on a metric whose definition moved during the period you are measuring.

**Metric-definition drift and disclosure deletion — the year-over-year redline.** Diff consecutive annual reports / 10-Ks, and where relevant the proxy or DRHP, for changes in: risk-factor wording, accounting-policy and critical-estimate language, segment definitions, useful lives and capitalisation policy, KPI definitions, MD&A tone, and customer or product concentration disclosures. **The highest-signal finding is always a deletion.** Management announces what it adds and never mentions what it removed. A volume disclosure that vanishes the year volumes fell, a KPI that stops being reported, a named large customer that disappears from the concentration note, a segment merged into "others" — each is information the company chose to stop giving you, and the reason is rarely favourable. Segment redefinition is the commonest form: it resets comparability exactly when comparability would have been damaging. **Tooling:** EDGAR full-text search and the filing-comparison view for US issuers; for India, the equivalent artefacts to diff are the MD&A, segment note, related-party note (watch entity-list changes), contingent-liabilities note, CARO clauses, and the concall — including which questions management stopped answering and which analysts stopped covering the name.

---

## 8. Auditor signals

The auditor is the last independent check on the numbers, and auditor-related events are among the strongest empirical predictors of restatement and fraud.

| Signal | Where to find it (Global / India) | Why it matters |
|---|---|---|
| Opinion type: unqualified / qualified / adverse / disclaimer | Auditor's report | Anything other than unqualified is a first-order finding, never a footnote |
| Going-concern emphasis | Auditor's report; Emphasis of Matter | The auditor doubts the entity survives twelve months |
| Key / Critical Audit Matters (KAMs / CAMs) | Auditor's report | The auditor is naming the numbers that were hardest to audit. Start your forensic work there — it is a free prioritisation |
| Auditor resignation or dismissal | US: 8-K Item 4.01. India: exchange filing under SEBI LODR Reg 30, with the resignation letter and reasons | Mid-cycle resignation is among the highest-severity signals available. Read the stated reason *and* the company's version of it |
| Downgrade in auditor quality | Compare firm size and network to group complexity | A large multi-jurisdiction group audited by a small firm is a structural problem regardless of that firm's competence |
| Component-auditor coverage | "Other Matters" paragraph of the consolidated audit report | Compute the % of consolidated revenue, assets and profit **not** audited by the principal auditor, plus anything unaudited or "certified by management". This is a direct measure of how much of the accounts nobody independent examined |
| Audit fee vs complexity | Auditor remuneration note / proxy | An implausibly low fee for a large multi-entity group means the work was not done |
| Non-audit fees ÷ total fees | DEF 14A / auditor remuneration note | High non-audit fees compromise independence |
| Internal-control opinion | US: SOX 404 material weakness. India: separate auditor opinion on internal financial controls under s.143(3)(i) | An adverse IFC/404 opinion says the systems producing the numbers are not reliable — every ratio downstream inherits that |
| Late filings | US: NT 10-K/10-Q. India: delayed results and exchange penalties | Companies file late when there is an unresolved disagreement |
| Restatement and regulatory history | US: Big-R restatement via 8-K Item 4.02 vs little-r revisions; SEC comment letters (UPLOAD/CORRESP on EDGAR); enforcement. India: SEBI orders, NFRA orders against the company or its auditors, SFIO and MCA inspections | A prior restatement is among the strongest predictors of the next one |
| **India:** CARO clauses | CARO 2020 report | Direct attestation on fixed-asset and title-deed verification, inventory verification, benami proceedings, loans and guarantees to related parties (including whether fresh loans were granted to settle overdue ones — an evergreening test), statutory dues in arrears, default in repayment to lenders and wilful-defaulter status, end-use of term loans and IPO/preferential-issue proceeds, cash losses in the current and preceding year, whistleblower complaints, fraud reported under s.143(12), and issues raised by the outgoing auditor. Read every clause, not the summary |

Also search for specific, substantiated short-seller reports and read the primary document rather than coverage of it. A short report is an adversarial argument with a financial interest behind it: treat every claim as a hypothesis to verify, note which claims the company answered *specifically* and which it answered only with adjectives, and attribute rather than adopt.

---

## 9. People signals: CFO and audit-committee turnover

Accounting is produced by a small number of identifiable people. When those people leave, it matters — serial finance-leadership churn is among the most reliable pre-restatement tells, and it is observable years before the numbers are.

Track over 5+ years: CFO, controller / chief accounting officer, treasurer, chief internal auditor, audit-committee chair, and (India) company secretary and independent directors. Flag:

- Serial CFO turnover — three finance chiefs in five years is a finding in itself.
- Departures clustered near reporting dates, audit sign-off, or a restatement.
- "Personal reasons" or "to pursue other opportunities" with no successor named, and a long gap before a permanent appointment.
- The audit-committee chair resigning, or independent directors resigning citing governance, disagreement, or inability to obtain information. **India:** SEBI requires disclosure of independent-director resignation letters — read the letter, not the press release.
- Departure of the head of internal audit, or internal audit reporting to the CEO rather than to the audit committee.
- **US:** cross-reference Form 4 insider sales against the departure timeline and against the peak of the growth narrative.

Then correlate: did anything disclosed in the following four quarters explain the departure? People closest to the numbers tend to leave before the numbers become public. Detail on board composition and promoter behaviour sits in `references/08-governance.md`; this section is only the accounting-integrity slice.

---

## 10. Structural opacity and off-balance-sheet exposure

Complexity is sometimes historical accident and sometimes deliberate. Assume nothing; map it.

- **Count and map the group.** Subsidiaries, step-down subsidiaries, associates, JVs, SPEs/VIEs and their jurisdictions. India: the AOC-1 statement of subsidiaries in the annual report, plus MCA/ROC records. Global: Exhibit 21 of the 10-K. Dozens of entities in Mauritius, Singapore, UAE, Cyprus or the Caribbean behind a simple domestic operating business is a structure that needs explaining.
- **Consolidated vs standalone (India).** Compare revenue, profit, debt and related-party balances on both bases. Profit concentrated at standalone with losses in subsidiaries, or debt in subsidiaries while cash sits at the parent, changes the entire risk picture. Never mix bases within one ratio.
- **Equity-method income without cash.** Equity-accounted income ÷ net profit, compared to dividends actually received from those entities. Profit you cannot receive is not profit you own.
- **Guarantees, letters of comfort, commitments and contingent liabilities ÷ equity.** In Indian infrastructure, telecom and real estate these routinely exceed net worth. Read the note in full: disputed tax demands and cross-guarantees to group entities live there.
- **Charges and security.** India: the MCA charge registry shows secured borrowings and pledged assets, including at unlisted group entities the consolidated statements may not reveal.
- **Leases and quasi-debt.** Post Ind-AS 116 / ASC 842 most leases are on balance sheet; check for arrangements structured to stay off it, and for sale-and-leaseback gains recognised in profit.
- **Related-party transactions and tunnelling.** Related-party revenue ÷ total revenue; related-party receivables and loans ÷ total assets; guarantees to related entities ÷ equity; intercompany balances ÷ equity. Look for asset transfers at non-arm's-length prices, management or brand-royalty fees paid to promoter entities, and circular flows that manufacture revenue. India: material RPTs need audit-committee approval and, above the LODR threshold, majority-of-minority approval — check how those votes went and whether transactions were sized just under thresholds.
- **Promoter pledging (India).** Pledged shares as % of promoter holding and % of total equity, plus the trend. Rising pledge is a promoter-liquidity signal that transmits directly into governance behaviour.
- **VIE / contractual-control structures.** For China and some EM ADRs, determine whether the listed entity legally owns the operating assets and profits or holds only contractual claims through offshore shells. Assess enforceability under local law, where cash, licences and IP legally reside, the mechanics and legality of upstreaming cash to foreign holders, and PCAOB inspection access / delisting risk. A genuinely profitable operating company can leave foreign minority holders with nothing — a structural trap invisible to earnings-quality analysis.
- **Frequent restructurings** that reset comparability, and segment reporting too aggregated to see what the business does. Cross-check that segment revenues and profits sum to the consolidated totals and that "unallocated" is not where the losses live.

---

## 11. Tax anomalies

Tax is a useful independent check because a second party — the tax authority — has an opposing interest in the numbers.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Effective tax rate | Tax expense ÷ pre-tax profit | Near the statutory rate, or fully reconciled to it in the tax note | A persistent unexplained gap suggests book profit that does not exist for tax purposes |
| Cash tax rate | Cash taxes paid (cash flow statement) ÷ pre-tax profit | Near the ETR on a 5-year average | Book profit that never generates a cash tax payment is a strong earnings-quality flag |
| Book-tax gap | Pre-tax book profit vs taxable income implied by the tax reconciliation | Small and explained | Widening gaps precede restatements |
| Deferred tax assets and valuation allowance | Tax note, year over year | Stable | Releasing a valuation allowance manufactures an EPS beat with no operating cause |
| Uncertain tax positions | FIN 48 reserve (US); disputed demands in contingent liabilities (India) | Stable | Aggressive structures create future liability and restatement risk |

Read the tax-rate reconciliation table every year: it names the specific items bridging statutory to effective rate, and a large "others" line is itself a disclosure failure. **India:** check the concessional-regime election (s.115BAA), MAT credit utilisation, and tax holidays (SEZ or unit-based) with known expiry dates. A low ETR with a scheduled expiry is a dated earnings cliff, not a moat — never carry it forward indefinitely in a DCF.

---

## 12. India: the mandatory disclosures that do forensic work for you

Indian filings are unusually generous to a forensic analyst, because Schedule III (Division II, as amended) and CARO 2020 force explicit disclosure of exactly the things a distressed or manipulating company would prefer to omit. Read these before doing any ratio work on an Indian issuer; each one is a direct answer to a question you would otherwise have to infer.

| Disclosure | What it tells you |
|---|---|
| Ageing tables: trade receivables, trade payables, CWIP, intangibles under development | Converts "receivables rose" into "how old, how disputed, how overdue" — the difference between a working-capital story and a write-off queue |
| Loans and advances to promoters, directors, KMPs and related parties that are repayable on demand or without stated terms | The tunnelling route, quantified and named |
| Borrowings on security of current assets: whether quarterly returns filed with banks agree with the books | Auditor-attested reconciliation of your receivables and inventory to what the lenders were told |
| Wilful-defaulter declaration; default in repayment of borrowings | Credit distress that has already been adjudicated by someone else |
| Relationship with struck-off companies | Transactions and balances with entities that legally no longer exist — a shell-company tell |
| Title deeds of immovable property not held in the company's name | Assets on the balance sheet that the company may not own |
| Revaluation of PP&E and intangibles; whether by a registered valuer | Equity created by revaluation is not equity earned |
| Utilisation of borrowed funds and share premium: declarations on ultimate beneficiaries and intermediaries | Directly targets round-tripping and fund diversion |
| Undisclosed income surrendered in tax assessments | Income the company admitted to the tax authority but not to you |
| Compliance with the number of layers of companies; pending charge satisfactions | Structural opacity, measured |
| Schedule III ratio disclosures with explanation for any change >25% | Management is required to explain its own ratio deterioration in writing. Read the explanations — they are frequently the weakest paragraphs in the report |
| CARO: cash losses in current and preceding year; material uncertainty on meeting liabilities within one year; issues raised by the outgoing auditor; whistleblower complaints; fraud reported under s.143(12) | Each is a severe, auditor-attested signal that requires no computation from you |

The US analogue is thinner but real: Item 9A internal controls, Item 3 legal proceedings, Exhibit 21 subsidiaries, the schedule of valuation and qualifying accounts (Schedule II) showing reserve additions and releases, 8-K Items 4.01/4.02, and SEC comment-letter correspondence on EDGAR.

---

## 13. Independent verification: the part that actually catches frauds

Everything above is derived from documents the company wrote. This section is not, which is why it is where frauds are actually caught.

**Proof of existence — assets, customers, counterparties.**

| Claim being tested | Independent source |
|---|---|
| Plants, stores, mines, hotels, data centres, warehouses exist and operate | Satellite and street-level imagery, building permits, environmental clearances, power and utility consumption, local news, site visits |
| Named top customers exist and buy at the stated volumes | The customers' own filings (a listed customer discloses major suppliers or purchase volumes), trade press, distributor and channel contact |
| Physical goods actually moved | Customs and shipping records, bills of lading, port and freight data; India: DGFT export data and e-way bills |
| Subsidiary results match the consolidation | India: subsidiary financials filed with MCA/ROC (AOC-4). Global: local registry filings such as UK Companies House and EU registries, which frequently contradict group presentations |
| The auditor, bankers and key suppliers are real firms capable of servicing a client this size | Firm registries, PCAOB/NFRA records, headcount and office footprint |
| Claimed headcount and scale | LinkedIn headcount trend, job postings, employee reviews and attrition; India: EPFO monthly payroll additions, and the employee-count disclosure in the annual report and BRSR |

**Alternative-data corroboration of reported growth.** Web traffic and app-download trends, app-store and marketplace review volumes, card and transaction panels where available, hiring velocity, and freight volumes. **The test is divergence, not level:** reported growth accelerating while every external proxy flattens is the pattern that precedes disclosure. Independent data is the short-seller's actual edge, and a checklist confined to filings can only ever detect problems the company itself chose to disclose.

**Scuttlebutt.** Use the product. Read customer reviews on app stores, G2, Amazon and industry forums. Talk to customers, distributors, suppliers or ex-employees where feasible and permissible. Financial statements lag; ground-level observation often reveals deterioration quarters ahead of the numbers.

**Information-integrity screen.** Establish where the idea came from. Screen for paid promotion and pump-and-dump patterns: unsolicited tips, thinly traded microcaps, reverse mergers, recent shell-to-operating transitions, aggressive newsletter or social promotion. Identify the incentives of whoever is recommending the stock, and verify every claim against the audited filing rather than a deck or a forum post.

**Report what you could not verify.** You will frequently lack access to satellite data, expert networks or customs records. That is a data gap, not an absence of risk. Write it explicitly: *"the existence of the [x] asset base and the [y] customer relationships could not be independently corroborated from available sources; this component of the analysis rests on management representations."* That sentence is honest, useful, and changes how a reader sizes a position.

---

## 14. Composite forensic scores and statistical tests

Use these as screens that direct attention, never as verdicts. Each was calibrated on a specific population, and applying it outside that population produces confident nonsense.

| Model | What it does | Threshold | Limits — read before using |
|---|---|---|---|
| Beneish M-Score | Eight ratios — days-sales-in-receivables, gross margin, asset quality, sales growth, depreciation rate, SG&A, leverage and total accruals — combined into a manipulation probability | Above −1.78 flags elevated risk | Calibrated on US manufacturers; high false-positive rate for fast growers and acquirers; **undefined for banks, NBFCs, insurers and REITs**. Note that six of the eight inputs are tests you have already run individually in this file — the index adds aggregation, not new information |
| Dechow F-Score | Misstatement probability from accruals, performance and market variables | Above 1.0 = above-normal risk | Same population caveats; needs several years of clean, restatement-free data |
| Montier C-Score | Six binary earnings-manipulation flags | Score out of 6 | Blunt; useful as quick triage only |
| Altman Z-Score | Bankruptcy risk from five ratios | >2.99 safe, <1.81 distress (manufacturing variant); use Z″ for non-manufacturers and emerging markets | Measures distress, not fraud; **meaningless for financials**; sensitive to the market-cap input, so it moves with price rather than fundamentals |
| Piotroski F-Score | Nine-point fundamental quality score | 8–9 strong, 0–2 weak | A quality screen, not a fraud test |
| Benford's Law | First-digit distribution test | Deviation from expected frequency | Weak on the few dozen line items in a financial statement; only meaningful on large transaction-level datasets. Do not present a Benford result on annual-report figures as evidence |

**Non-model statistical tells.** Earnings and margins far smoother than the industry's; margins implausibly above best-in-class with no identifiable moat; beating consensus by exactly a cent for many consecutive quarters; near-zero earnings volatility in a demonstrably cyclical sector; reported growth uncorrelated with cash generation. Real businesses are lumpy. Unnatural smoothness is manufactured, and the manufacturing is either legal smoothing or something worse.

Whenever you report a score, report its inputs and its population caveat alongside it. An M-Score quoted without the note that it is undefined for the company's sector is a fabrication dressed as rigour.

---

## 15. Sector translation: where these tests are undefined or inverted

Do not run the generic battery on a business it was not built for. Consult the playbook in `references/sectors/` and substitute the right tests.

- **Banks and NBFCs.** DSO, DIO, DPO, cash conversion cycle and the accrual ratio are meaningless; CFO is dominated by loan-book growth and is *negative* for a healthy growing lender. The manipulation vector is **credit-loss recognition**: GNPA/NNPA trends, provision coverage, restructured and SMA-1/SMA-2 books, evergreening (fresh loans repaying old ones), write-offs and "advances under collection" that flatter reported GNPA, sales of stressed loans to ARCs against security receipts, interest accrued but not received, capitalisation of interest into restructured loans, and rapid growth in a single unseasoned product. **India:** the RBI divergence disclosure — where the regulator's assessed NPAs and provisions exceed the bank's own — is a direct, auditor-independent red flag and must be checked every year.
- **Insurers.** Reserve adequacy is the manipulation vector; under-reserving inflates current profit. Look at reserve development triangles (prior-year releases propping current earnings), assumption changes in life valuation (discount rate, lapse, mortality, expense), and the composition of embedded-value movement. Margins and cash conversion do not apply.
- **REITs, InvITs and real-estate developers.** Depreciation makes accounting profit near-meaningless; use FFO/AFFO and NAV. Watch fair-value gains on investment property routed through the P&L (non-cash profit), capitalised interest into projects, and revenue-recognition timing on developer sales.
- **Miners, oil and gas.** Depletion, reserve estimates and the capitalisation-vs-expensing of exploration (successful-efforts vs full-cost) are the levers. Reserve revisions change both the asset and the depletion charge simultaneously. Judge on mid-cycle economics, not trailing.
- **Utilities and regulated infrastructure.** Regulatory assets and deferrals can hold years of costs; check the recovery mechanism and the regulator's actual orders, not management's expectation of them.
- **Project businesses (EPC, infra, defence, shipbuilding).** Percentage-of-completion estimates, unbilled revenue, retention money and claims recognised as receivables *are* the earnings-quality question.
- **Early-stage and platform businesses.** The statutory statements may say very little; the bespoke KPIs are the analysis, so Section 7 becomes the primary section rather than a supporting one.

---

## 16. Calibration: how to report a red flag and what it changes

Getting this wrong destroys the credibility of everything else in the report.

**Distinguish three severities and label them.**
1. **Aggressive but disclosed and legal** — a capitalisation policy at the permissive end, a non-GAAP measure with generous add-backs, a low ETR from a disclosed holiday. Effect: adjust the numbers yourself, note the adjustment, move on.
2. **Unexplained anomaly** — a metric behaving in a way the disclosure does not account for. Effect: state the anomaly, state the innocent explanation, state what evidence would distinguish them, and raise the required margin of safety.
3. **Structural integrity risk** — auditor resignation, adverse IFC/SOX opinion, cash-existence KAM, a large unaudited share of a consolidated group, Big-R restatement, regulator enforcement, tunnelling through related parties. Effect: this belongs in the report's opening verdict, not a footnote, and can be sufficient on its own to stop the analysis. Several are legitimate kill criteria.

**Require a cluster, not a single flag.** Base rates matter. Most individual flags have mundane explanations — one year of rising DSO because a large customer paid late, one year of high capex because a plant was built. What distinguishes a real accounting problem is **several independent flags pointing at the same line item**: rising DSO *plus* a shrinking allowance *plus* revenue concentrated in Q4 *plus* a related-party customer. One flag is a question. Four flags aimed at the same number is a finding.

**Always state the innocent explanation.** For every flag, write the most plausible benign reading and what would distinguish it. This is not hedging — it is what makes the flag credible on the occasions you do not withdraw it.

**Language discipline.** Do not assert fraud. Describe what the disclosure shows, what it does not permit you to rule out, and what evidence would resolve it. *"Reported cash of X earns an implied yield of ~1% against short rates of ~6%, which the filings do not explain; possible readings are non-interest-bearing operating float, restricted balances, or an overstated balance — the deposits note and any bank-confirmation KAM would distinguish these"* is rigorous, defensible and useful. "The cash is fake" is neither. Apply the same standard to short-seller allegations: attribute, do not adopt.

**Quantify the dependency, then carry it downstream.** The most useful output of a forensic pass is not a list of flags but a sentence like: *"roughly X% of reported EBITDA over the last three years depends on capitalisation and one-off treatments the peer group does not use; on a peer-consistent basis EBITDA would be approximately Y."* Never invent that number — derive it from disclosed line items and show the working, or state that it cannot be derived. Then propagate it: the adjusted figures, not the reported ones, are what feed the returns work in `references/05-returns-and-dupont.md` and the valuation in `references/06-valuation.md`. A forensic finding that does not change a downstream number has not been finished.

---

## Checklist

- [ ] Five-year table built — PAT, CFO, capex, FCF; cumulative CFO ÷ cumulative PAT computed, and the gap tied to a named asset line.
- [ ] Accrual ratio computed on at least one basis; growth in non-cash operating assets attributed to a specific line item.
- [ ] Working capital as a % of sales checked before flagging any cash-vs-profit gap in a growing business.
- [ ] CFO re-derived on a common classification basis before any cross-company or cross-regime comparison.
- [ ] Cash-flow-statement working-capital movements tied to balance-sheet deltas; unexplained differences investigated.
- [ ] Sum of four quarters reconciled to the audited annual figure; India — Q4 margin, other income and tax rate compared to the 9M run-rate.
- [ ] Interest and investment income reconciled to average cash; implied yield compared to short rates; Ind-AS fair-value gains on liquid funds included.
- [ ] Simultaneous large gross cash and gross debt explained, with the cost of carry quantified.
- [ ] Restricted, pledged and non-repatriable cash identified and excluded from net-debt maths.
- [ ] DSO, DIO, DPO and the cash conversion cycle computed for five years and vs peers; receivables growth vs revenue growth checked.
- [ ] ECL allowance and inventory provisions checked against a growing and ageing book; India — receivables ageing table read.
- [ ] Revenue-recognition policy read in full; gross-vs-net presentation, unbilled revenue and any policy or estimate change identified and quantified.
- [ ] Quarter-end vs intra-period balances tested; implied average debt from interest expense compared to year-end debt.
- [ ] Capex ÷ depreciation, implied useful life, capitalised development costs, CWIP ageing and useful-life changes reviewed; EBITDA-to-FCF gap explained.
- [ ] "One-off" items tallied across five years; recurring ones returned to normalised earnings; SBC quantified as a real cost.
- [ ] Organic growth separated from acquired growth; purchase-accounting levers (step-ups, acquisition reserves, earnout remeasurement, bargain-purchase gains) inspected.
- [ ] Goodwill and intangibles vs equity computed; tangible book value checked; impairment-test assumptions read against the company's own cost of capital.
- [ ] Every bespoke KPI catalogued with its exact definition; definitions compared year over year.
- [ ] Year-over-year redline done; **deletions** from prior-year disclosure specifically hunted and listed.
- [ ] Audit opinion, KAMs/CAMs, IFC/SOX opinion, auditor changes and stated reasons, audit fee and non-audit fee ratio reviewed.
- [ ] Component-auditor coverage computed: % of consolidated revenue, assets and profit not audited by the principal auditor.
- [ ] Restatement, comment-letter, NFRA/SEBI/SEC enforcement and litigation history checked; short reports read as primary documents.
- [ ] CFO, controller, treasurer, internal-audit head and audit-committee-chair turnover mapped over 5+ years; resignation letters read.
- [ ] Group structure mapped; equity-method income vs dividends received; guarantees and contingent liabilities vs equity; standalone vs consolidated compared.
- [ ] Related-party revenue, receivables, loans and guarantees quantified; promoter pledge level and trend checked (India).
- [ ] ETR vs statutory vs cash tax rate reconciled; any tax holiday dated to its expiry.
- [ ] India — CARO clauses and the Schedule III forensic disclosures read in full, including the bank-statement-vs-books agreement and the >25% ratio-change explanations.
- [ ] At least one independent, non-company corroboration attempted for the core growth or asset claim; whatever could not be verified stated explicitly.
- [ ] Composite scores, if used, reported with inputs and population caveats; never applied to financials.
- [ ] Sector translation applied — lenders, insurers, REITs and miners assessed on their own manipulation vectors, not the generic battery.
- [ ] Each flag labelled by severity, paired with its innocent explanation and the evidence that would resolve it; no fraud assertion made.
- [ ] The dependency quantified and carried into the returns and valuation work, not left as a standalone list of flags.
