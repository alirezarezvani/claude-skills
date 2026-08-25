---
name: stock-analysis
description: Produce a rigorous, sector-relative, multi-factor fundamental analysis of a publicly listed company — Indian (NSE/BSE) or US/global. Use when the user asks to analyse, research, evaluate, or value a stock, ticker, or listed company; asks whether a business is fundamentally strong, cheap, or expensive; compares companies or benchmarks one against its sector; or mentions OPM, ROCE, ROE, ROIC, P/E, EV/EBITDA, free cash flow, NIM, GNPA, CASA, promoter holding or pledging. Use it for accounting-quality and forensic questions — "is the profit real", "why is profit rising but cash isn't", auditor qualifications, related-party concerns — which route to the forensic-only mode, and for IPOs and not-yet-listed companies — "should I apply to this IPO", DRHP/RHP or S-1 questions, price band, grey market premium — which route to the IPO mode. Use it even when the request sounds casual ("is Infosys any good?"). Do not use it for personalised investment advice, portfolio allocation, or trading signals.
---

# Stock Analysis

Produce an evidence-backed fundamental analysis of one company, benchmarked against the right peers, and delivered as a written report plus a sector-relative scorecard.

## The principle that governs everything here

**A financial metric carries no meaning until you know the sector it came from and the company's own history.**

If X earns a 20% operating margin and Y earns 30%, that tells you nothing about which is the better business. Y may be in software (where 30% is mediocre) and X in distribution (where 20% is exceptional). Y's 30% may need three times the capital to produce, so X earns a far higher return on the money invested. Y's margin may be eroding while X's compounds.

Two consequences shape this whole skill:

1. **Never rank companies on a single metric.** Every judgement combines profitability, returns on capital, cash conversion, balance sheet, growth durability, governance, and price.
2. **Compare like with like.** Benchmark against sector peers or against the company's own multi-year record — never a raw cross-industry number. For banks, insurers, REITs and miners the standard ratios are not merely less useful, they are *undefined or inverted*; those sectors need their own metric set entirely.

Read `references/05-returns-and-dupont.md` for why return on capital, not margin, is the metric that actually determines compounding.

## Non-negotiables

### Never invent a number

This is the failure mode that destroys the value of the whole analysis. A fabricated revenue figure or a hallucinated ROCE produces a confident, well-formatted, *useless* report — and the user may act on it.

- Every figure carries a **source and a period** ("FY25 annual report, consolidated, p.112" / "10-K FY2024, Item 8" / "Q3 FY26 quarterly results filing, BSE").
- If a number cannot be sourced, write `not available` and say what would be needed. An analysis with acknowledged gaps is far more valuable than one with invented precision.
- Cross-check headline figures (revenue, net profit, debt, cash) against a second source when possible — at least one of the two must be a primary document.
- **Every financial figure in the analysis must trace to a primary document** — annual report, 10-K/10-Q, quarterly results filing, concall transcript, investor presentation, DRHP/RHP, exchange filing, or rating rationale. Aggregator websites (screener.in, Yahoo Finance, Tikr, etc.) are navigation aids for locating documents and optional labelled cross-checks — they are never a source of record. The one exception is current share price and market cap, which are inherently sourced from exchange or finance websites and must carry an as-of date.
- State **consolidated vs standalone** explicitly — for any company with subsidiaries these differ materially, and mixing them silently invalidates every ratio.
- State **currency and units**. Indian filings use crore/lakh; US filings use millions/billions. Getting this wrong by 10x is a common and embarrassing error.
- Flag stale data. A price or multiple without an as-of date is not usable.

Detailed sourcing routes and a verification protocol: `references/01-data-sourcing.md`.

### Official records are the source — and they hold far more than the financial statements

Two failure modes hide behind a report that looks well-sourced. Guard against both.

**First: the source of record is the company's own filings — nothing else is.** Rank sources by how many hands the number has passed through, and cite only the primary one:

1. **Primary filings** — annual report / 10-K, exchange filings (NSE/BSE, SEC EDGAR), quarterly results, the offer document (DRHP/RHP/S-1), audited statements.
2. **Company-published secondary** — concall transcripts, investor presentations, earnings releases.
3. **Regulator / third-party primary** — SEBI/MCA/ROC records, credit-rating rationales, exchange shareholding and pledge data.

Third-party research notes, brokerage reports, news articles and data aggregators (screener.in, Tikr, Yahoo/Google Finance, trendlyne) are **navigation and cross-check aids only** — they exist to help you *locate* the filing and to flag an outlier worth investigating. An aggregator or news figure must never be the thing you cite; when it disagrees with the filing, the filing wins and the disagreement is itself a finding. The one standing exception is live share price and market cap, which carry an as-of date. If a figure exists only in an aggregator and cannot be traced to a filing, it is `not sourced` — say so.

**Second: a filing is not just its three financial statements.** Most of what actually decides an analysis is the **non-financial** disclosure wrapped around the numbers, and it must be read and used as a first-class input — not skimmed on the way to the P&L:

- the **business, strategy and risk-factor** sections — what is sold and to whom, the stated moat, and the risks management is legally obliged to admit;
- **MD&A** read across 3–5 years — growth decomposed into volume / price / mix, capacity, capex plans, order book, guidance, and the drift between what was promised and what was delivered;
- the **auditor's report, CARO annexure, Key Audit Matters and emphasis-of-matter** — the auditor's own map of where the numbers are fragile;
- **related-party transactions, contingent liabilities, litigation and capital commitments** — the commonest routes for value to leave a minority shareholder, and quantifiable in one sitting;
- **governance and ownership** — board and audit-committee composition and independence, promoter holding trend and pledge, remuneration versus profit, auditor tenure and any resignation, AGM voting dissent, ESOP dilution;
- **segment and operational data** — segment-level revenue, EBIT and capital employed (segment ROCE is usually the report's most surprising number), plus the sector KPIs — capacity utilisation, occupancy/ARPOB, ANDA filings, same-store growth, order-book conversion — that never appear in the income statement;
- **ESG/BRSR, secretarial audit (MR-3), and subsidiary (AOC-1) disclosures.**

`references/15-document-diligence.md` is the runbook for extracting all of this, with a time-boxed reading order. Treat it as part of the core workflow, not an optional deep-dive: an analysis built only on the income statement, balance sheet and cash flow has read perhaps a fifth of the official record and skipped the four-fifths where the moat, the governance and the landmines live.

### Analysis, not advice

Produce analysis, evidence, and a reasoned view of business quality and valuation. Do not produce personalised investment advice, position sizing for the user, or buy/sell instructions framed as recommendations for their money. State clearly that the output is research, not licensed financial advice, and that the user is responsible for their own decisions.

Presenting a bull case, a bear case, a valuation range, and what would falsify the thesis is genuinely useful and stays on the right side of this line. "You should buy 50 shares" does not.

### Show the reasoning and the uncertainty

Where an estimate is used (normalised earnings, maintenance capex, mid-cycle margins), say it is an estimate, give the assumption, and show what changes if the assumption is wrong. False precision — a target price to two decimals off a hand-waved growth rate — is worse than an honest range.

## Choose a depth mode

Match effort to what the user asked for. Announce which mode you are running so expectations are set.

| Mode | When | What it covers |
|---|---|---|
| **Screen** | "quick take", "is this worth looking at" | Stages 0–3 plus valuation sanity check. Kill criteria, headline quality metrics, obvious red flags. Short verdict. |
| **Standard** (default) | "analyse this stock" | All stages, moderate depth per stage, full scorecard and report. |
| **Deep dive** | "detailed", "thorough", "maximum depth", or a position the user intends to size | All stages at full depth, situation playbook, document-level diligence, forensic pass, scenario valuation, explicit bear case. |
| **Forensic** | "is the profit real", "are they cooking the books", "cash flow doesn't match profit", "check the accounting" | A different question entirely — *can these accounts bear weight?* Skips business quality, growth and valuation. Follow `references/18-forensic-mode.md`. |
| **IPO** | The company is **not yet trading** — an open or upcoming IPO, a filed DRHP/RHP, "should I apply to X's IPO" | No market price and no public track record, so own-history benchmarking and market-price valuation are both unavailable. Follow `references/19-ipo-mode.md`. |

## The workflow

If you are running **Forensic mode**, stop here and follow `references/18-forensic-mode.md` instead — it has its own stages (F0–F5) and its own verdict scale, because "can I trust these numbers?" is not answered by a shorter version of "is this a good investment?".

If the company is **not yet listed**, stop here and follow `references/19-ipo-mode.md` — stages I0–I7. The workflow below assumes a traded security with a price and a public reporting history, and an IPO has neither. Note the boundary: a company that has *already listed* within the last two years uses this workflow with the recent-IPO overlay in `references/13-situations.md` §8, not IPO mode.

Otherwise work through these stages in order. Later stages depend on earlier ones — classifying the sector before you compute ratios is what stops you applying the wrong metric set.

### Stage 0 — Establish identity

Pin down exactly what is being analysed before touching numbers:

- Company, exchange, ticker, ISIN. Resolve ambiguity (many names collide across exchanges).
- **Which security**: ordinary shares, dual-class/DVR line, ADR/GDR, or a holdco that owns the operating company. These trade at different prices and confer different rights.
- Reporting currency and fiscal year end (needed to align peers).
- Consolidated or standalone basis for the analysis (consolidated is almost always correct).
- Market cap, enterprise value, free float.

If any of these do not exist because the company has not begun trading, you are in IPO mode — go to `references/19-ipo-mode.md`.

### Stage 1 — Acquire data

Follow `references/01-data-sourcing.md`. This is a **document-first** workflow: obtain the raw company documents before extracting any numbers.

**Step 1a — Document acquisition.** Before touching any numbers, identify and obtain the following documents (or as many as are available):

- Latest annual report or 10-K (and ideally the prior 4 years)
- Last 4–8 quarterly results filings from the exchange
- Latest 2 concall / earnings-call transcripts
- Latest investor presentation
- Quarterly shareholding pattern filings (last 4–8 quarters)
- Latest credit rating rationale
- DRHP/RHP if listed within the last 3–4 years

Source these from the company's investor-relations page, NSE/BSE corporate filings, SEC EDGAR, or equivalent primary repositories. Aggregator websites (screener.in, Tikr, Yahoo Finance) may be used to *locate* these documents — for example, screener.in links to underlying annual reports and concall transcripts — but the aggregator page itself is not the document.

**Step 1b — Extract the financials.** From the documents obtained above, gather at minimum 5 years of income statement, balance sheet and cash flow; quarterly trend for the last 8 quarters; and the shareholding pattern. Every figure must cite the specific document and page/section it was extracted from.

**Step 1c — Extract the non-financial record too.** The financial statements are only part of what these documents contain, and often not the part that decides the analysis. From the *same official documents*, extract and carry forward — each with its document and page/section cite:

- **Business & strategy** — the business-overview and MD&A narrative: what is sold, to whom, the stated moat and strategy, capacity and utilisation, capex plans, order book / backlog.
- **Risk factors** — the management-admitted risks, diffed across years (a risk that silently disappears is a disclosure decision, not a solved problem).
- **Auditor's report, CARO, KAMs, emphasis-of-matter** — opinion type for standalone *and* consolidated, and the specific line items the auditor itself flagged as fragile.
- **Related-party transactions, contingent liabilities, litigation, capital commitments** — including year-end outstanding balances, not just the year's flows.
- **Governance & ownership** — board/audit-committee composition and independence, promoter holding trend and pledge %, remuneration versus PAT, auditor tenure/resignation, AGM voting dissent, ESOP dilution.
- **Segment & operational KPIs** — segment-level revenue / EBIT / capital employed, and the sector operating metrics that never reach the P&L.

Walk the **entire** annual report section by section — not just the financials, and not only the shortlist above. Almost every section carries something an investor should weigh (the strategy in the chairman's letter, the pay ratio in an annexure, a covenant in a borrowings note, the one live case in an otherwise-routine litigation schedule), so the rule is **consider all of it, then report selectively**: read comprehensively, extract what is material, and let the write-up stay focused — a section that is genuinely empty this year is recorded as "read — nothing material", never skipped unread. `references/15-document-diligence.md` gives both a **complete annual-report contents map** (§0) and the time-boxed reading order (§1) for when to prioritise what. This step is **mandatory in Standard and Deep-dive modes**; even in Screen mode, read at least the auditor's report/opinion, the CARO fraud/statutory-dues/default clauses, and the shareholding-and-pledge pattern before forming a view. An analysis that quotes ratios but never opened the auditor's report or the related-party note is not finished.

If a required document cannot be obtained, ask the user for it **by name** — not "can you give me more data" but "please upload the FY25 annual report PDF and the last two concall transcripts". If the user provides numbers from an aggregator instead of the document, note them as `aggregator-sourced, unverified` and flag the gap. Do not fill gaps with recalled figures; recalled financials are frequently wrong and always stale.

**Then run the recency gate before you analyse anything.** This is the most common way a well-built analysis turns out wrong: not bad arithmetic, but a conclusion drawn from data that was already superseded when it was written. Adversarial review of real reports found verdict-level failures caused by results, regulatory decisions and deal approvals that were public *days before* the analysis date and simply absent from it.

So establish explicitly, and state in the report:

- **What is the latest period the company has actually reported**, and has a quarter been published since the annual figures you are using? Search for results dated after your newest data point rather than assuming your source is current.
- **What has happened since that period end** — earnings releases, rating actions, regulatory or court decisions, M&A approvals, block deals, management changes, guidance updates.
- **Do any of these already trip the invalidation triggers you are about to write?** A trigger that has already fired is not a future risk; it is a present finding.

Record the answer as one line: *"Most recent period incorporated: Q1 FY27, published 11-Jul-2026; checked for events to 22-Jul-2026."* A reader cannot judge staleness you have not disclosed.

**Then verify the data before you compute on it.** Assemble what you gathered into an intake file and run `python scripts/verify_data.py <intake>.json` (see `references/21-data-integrity-tools.md`). It is the mechanical enforcement of the sourcing rules above: it catches figures with no source or period, cross-source disagreements (the check that stops a wrong peer number reaching the verdict), silent consolidated/standalone mixing, crore-vs-million unit traps, and periods that a newer release has already superseded. Fix every error-level finding before proceeding; a fast, clean intake is worth more than a fast analysis built on an unchecked one.

### Stage 2 — Classify sector and situation

This is the hinge of the whole analysis, because it determines which metrics even apply.

**Sector** — pick the playbook from the router below and read it before computing anything.
**Situation** — check `references/13-situations.md` for lifecycle overlays (loss-making growth, deep cyclical, turnaround, spin-off, holdco, recent IPO, PSU, serial acquirer, promoter-controlled). A deep cyclical at a trailing P/E of 5 is usually expensive, not cheap; the situation playbook is what stops that error.

### Stage 3 — Kill-criteria and red-flag screen

Run this early. Most candidates fail here, and finding out cheaply is the point.

Read `references/07-forensic-red-flags.md` and `references/08-governance.md`. Screen for: cash flow persistently below profit, receivables growing faster than sales, auditor qualifications or resignations, high or rising promoter pledging, related-party leakage, frequent "one-off" charges, restatements, opaque group structure, and unsustainable leverage. The **anomaly scan** in `references/15-document-diligence.md` §0 maps these to the exact annual-report sections and the abnormal pattern to look for in each — legal-dispute and contingent-liability sizing, related-party tunnelling, and the shareholding-and-pledge trend especially, since these three often surface in the annual report before they surface anywhere else.

If something serious surfaces, say so prominently and early in the report rather than burying it. A governance red flag can outweigh every positive on the scorecard, and the report should reflect that rather than averaging it away.

**Escalate to Forensic mode** when a Stage 3 finding is severe enough that valuation becomes pointless until it is resolved — an adverse or qualified audit opinion, cumulative cash flow far below cumulative profit, cash that cannot be evidenced, or related-party leakage. Tell the user you are switching, and why. Valuing a company whose reported earnings you do not believe is wasted work.

### Stage 4 — Core analysis

Work through `references/02-core-factors.md`, drawing on:

- `references/03-earnings-quality.md` — revenue growth decomposition, margin trends, accruals, one-offs, tax normalcy, SBC and dilution
- `references/04-balance-sheet-and-cashflow.md` — leverage, coverage, maturity wall, working capital, OCF vs profit, FCF, capex split
- `references/05-returns-and-dupont.md` — ROIC vs WACC, DuPont decomposition, incremental returns, normalisation
- `references/15-document-diligence.md` — the qualitative record extracted at Stage 1c, now *synthesised alongside the ratios*: MD&A promise-versus-delivery, related-party leakage, contingent liabilities, segment ROCE, governance and auditor signals. The numbers and the narrative are analysed together, not in separate silos.
- The **sector playbook**, which overrides or replaces generic metrics where they do not apply

Business quality and moat, growth durability and reinvestment runway sit inside `02-core-factors.md`.

### Stage 5 — Build the peer set and benchmark

Follow `references/10-peer-set.md`. A wrong peer set produces confidently wrong conclusions, so construct it explicitly and state the basis: same sector and sub-sector, comparable business model and capital intensity, similar accounting regime, aligned fiscal periods.

Benchmark every key metric two ways — **against peers** and **against the company's own 5–10 year history**. Both matter: a company can beat its peers while decaying against itself.

### Stage 6 — Value it

Follow `references/06-valuation.md`. Use the method the **sector playbook** specifies (P/B and ROE for banks, P/EV for life insurers, AFFO and cap rates for REITs, mid-cycle EV/EBITDA for miners, EV/EBITDAR for airlines). Applying a generic P/E across sectors is the valuation equivalent of the OPM mistake.

Include a reverse-DCF style check — what growth and margin does the current price already assume? — because it converts valuation from an opinion into a testable question. Run `scripts/valuation.py` for the EV bridge, trailing multiples, the reverse-DCF implied growth and the probability-weighted scenario table rather than computing them by hand — it removes arithmetic slips and flags aggressive assumptions (e.g. terminal growth above nominal GDP).

### Stage 7 — Risk, bear case, invalidation

Read `references/09-risk-and-macro.md`. Write a genuine bear case, not a strawman: the most credible argument that this is a bad investment. Then state the specific, observable events that would prove the positive thesis wrong.

### Stage 8 — Score and write

Score using `references/11-scoring-rubric.md` (run `scripts/score.py` for the arithmetic), then write the report using the template in `references/12-report-template.md`. Before writing, read the worked exemplars in `examples/` to calibrate the target quality: `examples/standard-analysis-example.md` (a full Standard-mode report that passes the linter and embeds real `valuation.py` output) and `examples/forensic-analysis-example.md` (a Forensic-mode review following the F0–F5 template). They are fictional by design — models of *how*, never sources of figures.

### Stage 9 — Challenge the draft before delivering it

You wrote the thesis, so you will not attack it as hard as someone else would. Follow `references/20-challenge-pass.md`: identify what the verdict actually rests on, attack those claims, verify the numbers trace to their sources, and test whether the conclusion survives a different peer set and a different weight preset.

Mandatory in Deep dive. Recommended in Standard. Skip in Screen, where the conclusion is explicitly provisional. **If you can spawn subagents, use them** — independence is the mechanism, and an author reviewing their own work is a weak substitute.

The point is that the verdict can move. A challenge pass that only ever adds caveats to an already-written conclusion manufactures false confidence and is worse than none.

### Stage 10 — Lint before delivering

Run `python scripts/lint_report.py <report>.md` (see `references/21-data-integrity-tools.md`). It is a mechanical last check that the report honours the non-negotiables: a recency statement and data-quality note are present, basis and units are stated, a scorecard is not shown without its gate disclosure, a bear case and disclaimer exist, and — the core check — that financial figures sit near a source rather than floating free. Treat error-level findings as blocking and fix them; a low figure-sourcing ratio means go back and cite, not ship. The linter is a floor, not a substitute for judgement.

Save the report as a markdown file named `<TICKER>-analysis-<YYYY-MM-DD>.md` unless the user asks otherwise, and summarise the key findings in chat.

## Sector router

Read the matching playbook at Stage 2. When a company spans several sectors, use the segment that drives most of the profit and note the others; conglomerates go to the holdco playbook and are valued sum-of-the-parts.

| If the company is… | Read |
|---|---|
| A bank or lender taking deposits | `references/sectors/banks.md` |
| An NBFC, housing finance or non-bank lender | `references/sectors/nbfc.md` |
| A mortgage REIT, BDC, private-credit vehicle, equipment lessor or leasing company | `references/sectors/mortgage-reit-specialty-finance.md` |
| A life, general, health or P&C insurer | `references/sectors/insurance.md` |
| An insurance broker, MGA, TPA or distribution platform — places risk but underwrites none | `references/sectors/insurance-brokers-services.md` |
| IT services, software, SaaS, internet platform | `references/sectors/it-saas.md` |
| Staffing, consulting, advertising, outsourced professional and business services | `references/sectors/people-businesses.md` |
| Pharma, CDMO, hospitals, diagnostics, medical devices | `references/sectors/pharma-healthcare.md` |
| A pre-revenue, clinical-stage drug developer with no approved product | `references/sectors/biotech-clinical.md` |
| FMCG, consumer staples, branded consumer, QSR | `references/sectors/fmcg-consumer.md` |
| Automobiles, auto components, tyres | `references/sectors/auto.md` |
| Steel, aluminium, mining, other commodity producers | `references/sectors/metals-mining.md` |
| Oil & gas — upstream, refining, marketing, gas utilities | `references/sectors/oil-gas.md` |
| Power generation, transmission, regulated utilities | `references/sectors/utilities-power.md` |
| Waste collection and disposal, landfills, recycling, water and wastewater treatment | `references/sectors/waste-environmental.md` |
| Real estate developers, REITs, InvITs | `references/sectors/realestate-reit.md` |
| Infrastructure, EPC, capital goods, defence | `references/sectors/infra-capitalgoods.md` |
| Telecom, towers, broadcasting, media, OTT | `references/sectors/telecom-media.md` |
| Airlines, hotels, travel, restaurants, OTAs | `references/sectors/aviation-hotels.md` |
| Retail chains, e-commerce, marketplaces, quick commerce | `references/sectors/retail-ecommerce.md` |
| Specialty chemicals, agrochemicals, fertilisers, cement | `references/sectors/chemicals-cement.md` |
| Holding companies, conglomerates, AMCs, alternative managers | `references/sectors/holdco-assetmgr.md` |
| Shipping, tankers, dry bulk, ports, trucking, logistics | `references/sectors/shipping-logistics.md` |
| Railroads and rail freight networks | `references/sectors/rail-freight.md` |
| Exchanges, depositories, clearing houses, rating agencies, card and payment networks | `references/sectors/exchanges-payments.md` |
| Semiconductors, fabs, equipment, capital-intensive hardware | `references/sectors/semiconductors.md` |

If none fits cleanly, use `references/02-core-factors.md` with the generic ratio set and say in the report that no specialised playbook applied — then be extra careful about which standard metrics are actually meaningful for that business model.

## Bundled scripts

Run these rather than recomputing by hand; they remove arithmetic slips and keep results consistent between analyses.

- `scripts/ratios.py` — takes a small JSON of raw financials and returns the full ratio set, DuPont decomposition, accrual and cash-conversion checks. `python scripts/ratios.py --help`
- `scripts/score.py` — sector-relative multi-factor scoring with editable benchmarks and category weights. `python scripts/score.py --help`
  - For a company with materially different businesses, pass a `segments` array and each segment is scored against its own sector's benchmarks and blended by profit — `python scripts/score.py --example-segments` prints a runnable example. The blend is a quality summary, never a substitute for sum-of-the-parts valuation.
- `scripts/valuation.py` — Stage-6 valuation calculator: EV bridge, trailing multiples, the reverse-DCF implied-growth solve, a forward 2-stage DCF, and a probability-weighted scenario table. Runs only the sections whose inputs you supply, and guards invalid assumptions (terminal growth ≥ WACC fails). `python scripts/valuation.py --template` / `--example`
- `scripts/verify_data.py` — data-intake gate. Validates gathered figures for provenance, **source tier (documents primary, aggregators navigation-only)**, cross-source agreement, basis/unit consistency and staleness before you compute on them. Run it at Stage 1. `python scripts/verify_data.py --template`
- `scripts/lint_report.py` — finished-report QA. Checks the non-negotiables and the figure-sourcing ratio before delivery. Run it at Stage 10. `python scripts/lint_report.py --help`

Both are plain Python with no third-party dependencies. Sector benchmark tables live in `scripts/benchmarks.json` and are meant to be edited — treat the shipped values as reasonable defaults, not gospel, and override them when you have better peer data for the specific market and period.

## Output contract

Deliver two things, always:

1. **The report** — follow `references/12-report-template.md`. It opens with the verdict and the key risks, because a reader who stops after the first screen should still get the substance.
2. **The scorecard** — sector-relative scores by category with the weights shown, plus the composite. Show the inputs so the reader can disagree with a specific number rather than the whole thing.

Include the data-quality note: which figures are sourced, which are estimated, which are missing, and the as-of date.

## Reference index

Read these as needed; they are written to be consulted individually rather than all at once.

| File | Use it for |
|---|---|
| `references/01-data-sourcing.md` | Where to get data for India and global markets, and how to verify it |
| `references/02-core-factors.md` | The universal multi-factor checklist: business, moat, industry, growth |
| `references/03-earnings-quality.md` | Income statement analysis and earnings quality |
| `references/04-balance-sheet-and-cashflow.md` | Solvency, liquidity, working capital, cash generation |
| `references/05-returns-and-dupont.md` | ROIC/ROCE/ROE, DuPont, incremental returns, why margin alone misleads |
| `references/06-valuation.md` | Every valuation method, EV bridge, WACC derivation, reverse DCF, scenarios |
| `references/07-forensic-red-flags.md` | Accounting manipulation and fraud detection |
| `references/08-governance.md` | Management, promoters, board, auditors, related parties |
| `references/09-risk-and-macro.md` | Company, macro, regulatory, ESG and tail risks |
| `references/10-peer-set.md` | Constructing a defensible like-for-like comparison set |
| `references/11-scoring-rubric.md` | The sector-relative multi-factor scoring method |
| `references/12-report-template.md` | The exact output structure |
| `references/13-situations.md` | Lifecycle overlays: cyclicals, turnarounds, holdcos, IPOs, PSUs |
| `references/14-accounting-comparability.md` | IFRS/GAAP/Ind-AS differences, leases, restatements, normalisation |
| `references/15-document-diligence.md` | Annual report, auditor's report, CARO, KAM, transcripts, rating rationales |
| `references/16-market-mechanics-and-tax.md` | Surveillance, corporate actions, dilution instruments, taxation |
| `references/17-process-and-epistemics.md` | Circle of competence, falsification, base rates, when to say no |
| `references/18-forensic-mode.md` | Forensic-only runbook: triage battery, verdict scale, output template |
| `references/19-ipo-mode.md` | Not-yet-listed companies: DRHP/RHP, seller motive, valuing the price band |
| `references/20-challenge-pass.md` | Adversarial review before delivery: attack the load-bearing claims |
| `references/21-data-integrity-tools.md` | The intake gate and report linter: how and when to run them |
| `references/sectors/_index.md` | Sector router with sub-sector guidance |

## Anti-Patterns

- Judging a bank, insurer, REIT, or miner on generic ratios — for these sectors the standard ratios are undefined or inverted; route through the sector playbook first.
- Inventing or interpolating a number instead of writing "not available" with the reason.
- Averaging a disqualifying red flag into a composite score instead of letting it cap or void the verdict.
- Treating aggregator or screener figures as primary evidence — they navigate; filings decide.
- Running every reference on every company — three or four factors decide most outcomes.
- Presenting output as investment advice — the deliverable is analysis, never an allocation or a trading signal.

## Cross-References

- `finance/skills/financial-analyst` — inside-out corporate FP&A, budgeting, and DCF modelling for a company you operate; this skill is the outside-in public-market view of a listed company.
- `finance/business-investment-advisor` — internal capex and project-ROI decisions; this skill values traded equity, not internal projects.
- `finance/skills/saas-metrics-coach` — operating SaaS metrics (NRR, CAC, burn) for internal steering, not listed-equity valuation.

## A note on judgement

These references are extensive, and working through all of them mechanically produces a long document rather than an insight. The point of the depth is that you can reach for the right tool, not that every tool gets used on every company.

For most companies, three or four factors genuinely decide the outcome — a moat that is widening or narrowing, returns on incremental capital, whether cash follows profit, and whether the price already assumes success. Identify those, evidence them properly, and let the rest of the checklist do its real job: making sure nothing disqualifying was missed.

If the business sits outside what can be understood with the available information, say so. Declining to analyse is a legitimate and useful answer.
