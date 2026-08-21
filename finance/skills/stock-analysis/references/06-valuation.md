# Valuation and margin of safety

Use this when: business quality, earnings quality, balance sheet and returns are already established, and you need to decide what the business is worth, what the market is already paying for, and how much room for error the price leaves.

Valuation is the last stage, never the first screen. A multiple is a compression of everything you have already established — growth, durability, capital intensity, return on incremental capital, accounting honesty — into a single number, and it is unreadable until those are known. The governing principle applies with full force: a P/E of 12 means nothing until you know the sector, the cycle position, and the company's own ten-year band. For banks, insurers, REITs, miners, shipping and holding companies the standard multiples are undefined, inverted, or actively misleading, and **the sector playbook overrides every default in this file**.

## Contents

1. [Order of operations](#order-of-operations)
2. [The multiple set](#the-multiple-set)
3. [Where each multiple breaks](#where-each-multiple-breaks)
4. [Building the enterprise value bridge](#building-the-enterprise-value-bridge)
5. [Deriving the discount rate](#deriving-the-discount-rate)
6. [Building the DCF](#building-the-dcf)
7. [Reverse DCF — the central discipline](#reverse-dcf--the-central-discipline)
8. [Earnings yield versus bond yield](#earnings-yield-versus-bond-yield)
9. [Valuation versus its own history](#valuation-versus-its-own-history)
10. [Valuation versus peers](#valuation-versus-peers)
11. [SOTP, private market value and replacement cost](#sotp-private-market-value-and-replacement-cost)
12. [Margin of safety](#margin-of-safety)
13. [Quality trap versus value trap](#quality-trap-versus-value-trap)
14. [Scenarios, expected value and IRR decomposition](#scenarios-expected-value-and-irr-decomposition)
15. [Catalyst, edge and what is already discounted](#catalyst-edge-and-what-is-already-discounted)
16. [Sector overrides](#sector-overrides)
17. [India (Ind-AS/NSE-BSE) vs US/global conventions](#india-ind-asnse-bse-vs-usglobal-conventions)
18. [Errors that ruin this section of the report](#errors-that-ruin-this-section-of-the-report)
19. [Checklist](#checklist)

---

## Order of operations

Run valuation in this sequence. Out of order, it becomes a rationalisation of the quoted price — the most common failure mode in this entire skill.

1. **Check the sector playbook first.** If it prescribes a method (P/ABV against ROE for banks, P/EV for life insurers, AFFO yield and cap-rate spread for REITs, mid-cycle EV/EBITDA and P/NAV for miners, EV/EBITDAR for airlines), use it and suppress the generic multiples it declares inapplicable.
2. **Normalise the denominator before touching the numerator.** Strip one-offs, normalise tax, decide whether earnings sit at a cyclical peak or trough, and state whether the figure is reported (Ind-AS/GAAP/IFRS) or adjusted, and why.
3. **Build the EV bridge once**, properly, and reuse it in every enterprise multiple.
4. **Run the reverse DCF before building your own forecast.** Find out what the price already assumes while you are still neutral. Once you have written a forecast you will unconsciously defend it.
5. **Then triangulate:** multiples versus own history, versus peers, a forward DCF with sensitivity, and at least one asset- or transaction-based cross-check.
6. **Convert to a scenario table** with explicit probabilities, a probability-weighted value, and an IRR decomposition. Report a range, never a point.
7. **Apply the margin of safety** against the conservative case, sized to the uncertainty of the estimate — not to how much you like the story.

---

## The multiple set

Ranges are **indicative only**. They move with market, sector, cycle, interest-rate regime and accounting period, and an Indian multiple is not directly comparable to a US one because the currency, the risk-free rate and the nominal growth rate all differ. **The company's own 5–10 year band and its true peer set override every number in this column.**

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| **Trailing P/E** | Price ÷ trailing-12m diluted EPS, after minority interest. | Depends entirely on ROIC and growth; 12–20x is unremarkable for a mature business in either market. | The most quoted and most distorted multiple. Only interpretable next to the normalised version. |
| **Forward P/E** | Price ÷ next-12m consensus or your own EPS. | Should sit below trailing P/E if earnings are growing. | Prices the year ahead, but inherits consensus optimism. Check estimate dispersion and revision direction. |
| **Normalised / mid-cycle P/E** | Price ÷ EPS at mid-cycle margins and a full tax rate, modelled across a complete cycle. | Compare to the company's own normalised history, not an absolute band. | The only P/E that survives a cyclical business. Prevents anchoring to peak or trough earnings. |
| **CAPE / Shiller P/E** | Price ÷ 10-yr average inflation-adjusted EPS. | Use versus its own history and the index's. | Cycle-proof at index level; at single-stock level it penalises genuine structural growth — use for mature cyclicals only. |
| **GAAP-vs-adjusted EPS gap** | (Adjusted EPS − reported EPS) ÷ reported EPS. | <10% and not widening. | A widening gap is an earnings-quality finding dressed up as a valuation input. |
| **Earnings yield (E/P)** | Inverse of P/E; better, FCF ÷ market cap. | Above the local 10-yr sovereign yield by a sensible premium. | Makes the equity directly comparable to bonds and to the company's own cost of debt. |
| **P/B** | Price ÷ book value per share. | Only meaningful with ROE alongside; justified P/B ≈ (ROE − g) ÷ (COE − g). | Anchors financials and asset-heavy businesses. Near-meaningless for asset-light compounders. |
| **P/TBV (P/ABV)** | Price ÷ (equity − goodwill − intangibles); for lenders also net of net NPAs (adjusted book). | With ROTCE/RoE above cost of equity, a premium is earned. | Strips acquisition accounting and, for banks, the reserves the market disbelieves. |
| **EV/EBITDA** | EV (from the bridge) ÷ EBITDA. | 6–12x common for mature industrials; capital intensity drives the band. | Capital-structure and tax neutral; the language of M&A. Blind to capex. |
| **EV/EBIT** | EV ÷ EBIT after real depreciation. | Roughly 10–16x for a decent mature business. | Harder to game than EBITDA because depreciation proxies the cost of keeping the asset base alive. Prefer it for anything capital-intensive. |
| **EV/(EBITDA − capex)** | EV ÷ (EBITDA − total capex), and ÷ (EBITDA − maintenance capex). | Compare against EV/EBITDA; a wide gap is the whole story. | Exposes the business whose EBITDA is consumed by the plant that produced it. |
| **EV/Sales** | EV ÷ revenue. Decompose: EV/Sales ÷ steady-state EBIT margin = implied EV/EBIT. | Only via the implied-margin decomposition. | The fallback when earnings are negative or unrepresentative — and worthless unless you state the margin it implies. |
| **P/S** | Market cap ÷ revenue. | As above; equity-level, so valid only for near-unlevered companies. | Sales are the hardest line to manipulate, so P/S survives trough margins. It does not survive a structurally low-margin business. |
| **PEG** | P/E ÷ expected EPS CAGR (%). | <1 classically cheap; treat 0.8–1.5 as a wide neutral band. | Links price to growth. Ignores growth's capital intensity and durability — always pair with incremental ROIC. |
| **EV/EBIT-to-growth** | EV/EBIT ÷ EBIT CAGR. | Use versus peers, not absolutely. | The capital-structure-neutral version of PEG; avoids PEG's leverage distortion. |
| **FCF yield** | FCF ÷ market cap, FCF = CFO − total capex, with SBC treated as a cost. | 4–8% for a mature business; a genuine high-reinvestment compounder can legitimately show 1–2%. | The truest "what an owner earns" measure and the hardest to manipulate. |
| **FCF/EV** | Unlevered FCF ÷ EV. | Compare directly to WACC. | Removes leverage distortion, making the yield comparable across capital structures. Below WACC, the business is not covering its capital cost. |
| **Owner-earnings yield** | (Net income + D&A − maintenance capex − working-capital needs − SBC) ÷ market cap. | Within a few points of FCF yield across 3–5 years. | Separates reported profit from distributable profit. The gap is the finding. |
| **FCF conversion** | FCF ÷ net income, cumulative over 3–5 years. | 70%+ for a mature business. | A valuation input, because it decides whether the E in P/E is spendable. |
| **Dividend yield** | DPS ÷ price. | Sector- and market-dependent; Indian large caps typically yield less than US peers. | A component of return and a discipline on capital allocation — and a trap when the market is pre-pricing a cut. |
| **Payout ratio** | DPS ÷ EPS, and dividends ÷ FCF. | Below ~70% of FCF for a sustainable dividend. | The FCF version is the one that matters; the EPS version misses the capex. |
| **Total shareholder yield** | Dividend yield + net buyback yield (net of SBC issuance) + net debt-paydown yield. | 4%+ for a mature cash generator. | Captures the whole return of capital, including the buyback that merely offsets dilution and therefore returns nothing. |
| **Multiple percentile vs own history** | Current multiple's percentile / z-score in its own 5–10 yr distribution. | Below the 50th percentile with unchanged fundamentals is the interesting case. | Own history is the cleanest comparable: same model, same accounting, same disclosure. |
| **Implied ERP (yield gap)** | Earnings or FCF yield − local 10-yr sovereign yield. | Judge against that same spread's own history, never against another country's. | Places the multiple inside the prevailing rate regime instead of in a vacuum. |
| **EV per physical unit** | EV ÷ tonne, bed, key, subscriber, MW, sq ft, MHz, dwt. | Versus greenfield replacement cost and recent transactions. | The cross-check that depends on no accounting at all. |
| **Price / intrinsic value** | Price ÷ conservatively estimated fair value. | ≤0.70 for average businesses; ≤0.80 for highly predictable ones. | The margin of safety, stated as a number rather than a feeling. |

---

## Where each multiple breaks

Every multiple has a situation in which it reliably lies. Establish which one you are in before quoting it.

| Multiple | Fails when | What it does to you | Use instead |
|---|---|---|---|
| **P/E** | Earnings sit at a cyclical peak, contain one-offs, or are negative. | Prints its lowest reading at the top of a commodity cycle — P/E is *inverted* for cyclicals. A miner or commodity chemical maker at 5x is usually a sell; at 30x, often a buy. | Mid-cycle normalised EPS; P/B against mid-cycle ROE; EV per tonne. |
| **P/E** | Capital structure differs across the peer set. | Leverage flatters EPS and compresses P/E, so the most fragile company screens cheapest. | EV/EBIT. |
| **P/E** | EPS growth is buyback-driven. | Mistakes share-count shrinkage for business growth. | Net income growth and FCF per share, with the buyback price checked against your own value range. |
| **P/B** | The business is asset-light, equity is negative after buybacks, or book carries goodwill from overpriced deals. | Meaningless or undefined; a serial acquirer looks "cheap on book" precisely because it overpaid. | P/TBV with ROTCE; for asset-light names ignore book entirely and use FCF yield. |
| **P/B (financials)** | Asset marks are stale or reserves inadequate. | A bank below book is cheap only if the book is real. The market usually prices a credit event before the auditor recognises it. | P/ABV net of net NPAs, stressed-book scenarios. `sectors/banks.md` |
| **EV/EBITDA** | Capital intensity is high, EV omits leases/pensions/minorities, or "adjusted EBITDA" carries recurring add-backs. | Understates the true purchase price and overstates the cash. SBC and annual "restructuring" added back is the classic. | EV/EBIT, EV/(EBITDA − capex), and a rebuilt EV bridge. |
| **EV/anything (banks, NBFCs, insurers)** | Debt is raw material, not financing. | Enterprise value has no meaning; net debt is not a claim to add back. | P/B, P/ABV, RoE vs COE, P/EV. Suppress every EV multiple. |
| **EV/Sales, P/S** | The implied steady-state margin is never stated. | Any price can be justified by assuming a margin the industry has never achieved. | Always decompose: EV/Sales ÷ target margin = implied EV/EBIT, then ask whether that margin is attainable. |
| **PEG** | Growth is a one-year spike, or the company is a no-growth cash cow. | Rewards a peak-growth year; penalises a genuinely cheap steady compounder. | FCF yield + growth; EV/EBIT-to-growth alongside incremental ROIC. |
| **FCF yield** | The year contains a working-capital release, an asset sale, or deferred capex. | A single year of "free cash" that is really underinvestment or stretched payables. | 3–5 year average FCF; split maintenance from growth capex; check payable days. |
| **Dividend yield** | The yield rose because the price fell. | The classic yield trap; the market pre-prices the cut months before the board announces it. | Payout as % of FCF, coverage, and balance-sheet capacity to sustain it. |
| **P/E on REITs, InvITs** | Depreciation is charged on appreciating property. | Earnings are structurally understated; P/E is nonsense. | AFFO yield, NOI cap-rate spread, NAV. `sectors/realestate-reit.md` |
| **Any multiple straddling FY20 (India) / 2019 (IFRS, US)** | Ind AS 116 / IFRS 16 / ASC 842 capitalised leases; India's s.115BAA cut the tax rate. | EBITDA, EPS and EV all stepped up for non-operating reasons. The 10-year multiple band is broken at that seam. | Restate the pre-transition years before plotting any historical multiple range. |

---

## Building the enterprise value bridge

Most "cheap on EV/EBITDA" findings are arithmetic errors in EV. Build the bridge explicitly, present it as a table in the report, and reuse the same bridge everywhere.

```
  Fully diluted market cap
+ Total debt (short-term + long-term + current maturities)
+ Capitalised lease liability
+ Preference shares / CCPS at redemption or conversion value
+ Non-controlling (minority) interest
+ Net underfunded pension / OPEB / gratuity, net of deferred tax
+ Contingent consideration, earn-outs, put options over NCI
+ Other debt-like items
− Surplus cash and equivalents
− Marketable securities and liquid investments
− Market or fair value of non-consolidated stakes (associates, JVs, listed holdings)
= Enterprise value
```

**Fully diluted share count.** Treasury-stock method for options and RSUs; if-converted for convertibles (either add the converted shares *or* add the bond to debt and interest back to earnings — never both, never neither); warrants; unvested and unexercised ESOP pools from the share-capital note. *India:* compulsorily convertible preference shares and debentures are common in recently listed new-age and PE-funded companies — convert them. *US:* SBC-driven dilution in technology can run 2–4% a year, so a count lifted from the 10-K cover understates the claim on the business.

**Cash: surplus, not total.** Only cash the business could actually distribute is deductible. Carve out (a) operating cash, roughly 2–5% of sales, (b) cash trapped where repatriation triggers tax, (c) regulatory, margin, escrow and customer-float balances (exchanges, brokers, payment companies — see `sectors/exchanges-payments.md`), (d) cash earmarked for an announced acquisition or declared dividend. *India:* surplus treasury usually sits in "current investments" as liquid mutual funds rather than in "cash and cash equivalents" — read both lines. If you deduct the investments, remove their yield from EBIT as well, or you double-count the treasury.

**Leases.** Post-IFRS 16 / Ind AS 116 / ASC 842 the liability is on the balance sheet: add it. For pre-transition years, capitalise at the present value of committed rentals, or 8x annual rent as a rough proxy, so the historical EV series is continuous. Retail, QSR, aviation, hospitality and logistics are where omitting this changes the conclusion, not the decimal.

**Minorities and associates are two halves of one discipline.** If consolidated EBITDA includes 100% of a 60%-owned subsidiary, add the minority interest to EV — ideally at market value or at the multiple you are applying, not at book. Conversely, associates and JVs are equity-accounted, contributing profit but no EBITDA: deduct their value from EV *and* strip the share of associate profit out of your earnings figure. Doing one without the other is the most common silent error in Indian conglomerate and holdco analysis.

**Pensions and gratuity.** Add the defined-benefit obligation net of plan assets, tax-effected. Material in older US and European industrials; in India the gratuity and leave-encashment provisions are usually smaller but must still be read in the employee-benefits note. A pension deficit approaching the market cap makes the equity a residual claim on an insurance liability, not on the operating business.

**Other debt-like items to hunt for:** reverse factoring and supply-chain finance hidden in trade payables, receivables securitised with recourse, asset-retirement and mine-closure obligations, litigation and tax provisions with a probable outflow, deferred acquisition consideration, promoter and related-party loans, perpetual instruments (AT1 for banks), and take-or-pay or capacity commitments in the contingent-liabilities note.

**The pairing rule.** An equity claim belongs in a numerator only with an equity metric; an enterprise claim only with an enterprise metric. P/EBITDA and EV/net-income are meaningless. If minority interest sits in EV, the earnings figure must be pre-minority.

---

## Deriving the discount rate

Never take a WACC from a screener. Derive it, state every input, and date it — a discount rate is a statement about a specific market on a specific day.

```
Ke   = Rf + β × ERP + CRP  (+ any size / illiquidity premium)
WACC = Ke × E/(D+E) + Kd × (1 − t) × D/(D+E)
```

- **Risk-free rate.** Use the long government bond yield *in the currency of the cash flows*, roughly duration-matched. India: the 10-yr G-Sec. US: the 10-yr Treasury. For a sovereign carrying real default risk, subtract the country's default spread from its local bond yield to get a true risk-free rate, then add the country risk premium back explicitly at the equity level — otherwise the same risk is counted twice.
- **Equity risk premium.** Use a consistently sourced mature-market ERP; 4.5–5.5% is the usual working range. Prefer an implied (forward-looking) ERP over a long historical average when rates have moved sharply, and use the *same* ERP for every company in a comparison.
- **Country risk premium.** For emerging markets, CRP ≈ sovereign default spread (from rating or CDS) × the ratio of equity to bond volatility, typically 1.0–1.5x. For India this has historically added roughly 2–3 percentage points. Apply CRP by **revenue exposure, not listing venue**: an Indian-listed IT exporter earning 80% of revenue in the US carries far less India risk than a domestic cement maker listed alongside it.
- **Beta.** Prefer a bottom-up beta — unlever peer betas, average, relever at the target capital structure: `βL = βU × (1 + (1 − t) × D/E)`. Regression betas for Indian mid- and small-caps are dominated by illiquidity and index composition and are close to noise; if you must use one, apply the Blume adjustment (`0.67 × raw + 0.33 × 1.0`) and disclose the window and index. A sub-1.0 beta on a highly operationally leveraged cyclical is a data artefact, not a finding.
- **Cost of debt.** Use the yield to maturity on traded bonds, or build it synthetically: risk-free + a default spread implied by interest coverage or credit rating. Do **not** use the historical average interest cost from the P&L — it reflects debt raised in a different rate regime and understates the marginal cost of new borrowing. Tax-effect at the marginal, not the effective, rate, and only to the extent interest is actually deductible.
- **Weights at market value**, using the target or sustainable capital structure rather than a temporarily distressed or temporarily cash-rich one.
- **Size and illiquidity premia** are contested. Adding 200bps to WACC to express "this is a risky small-cap" is crude and buries the judgement inside a compounding exponent. Prefer conservative cash flows plus a wider margin of safety.

**The currency-consistency rule.** Discount nominal INR cash flows at a nominal INR rate; nominal USD cash flows at a nominal USD rate; real cash flows at a real rate. Never mix. An INR WACC is structurally several points above a USD WACC purely because of the inflation differential — and therefore an INR terminal growth rate of 4% is *deeply* conservative where a USD 4% would be aggressive. To value a cross-border business, either (a) model in the functional currency and translate the resulting value at spot, or (b) translate the cash flows year by year at forward rates built from the inflation differential, `FX_t = FX_0 × ((1+i_local)/(1+i_foreign))^t`, and discount at the foreign rate. Both are correct; half of each is not. Where the company's revenue and its debt sit in different currencies, that mismatch is a risk to model in the scenarios, not a rate to average.

**Do not double-count risk.** If the bear scenario already models the asset being expropriated, do not also add a political-risk premium to WACC. Risk belongs either in the cash flows or in the rate — choose one and say which.

---

## Building the DCF

```
FCFF = EBIT × (1 − cash tax rate) + D&A − capex − ΔNWC   →  discount at WACC  →  EV
FCFE = FCFF − interest × (1 − t) + net borrowing          →  discount at Ke    →  equity value
```

- **Set the forecast horizon equal to the competitive advantage period**, typically 5–10 years, and only as long as you can name a mechanism that keeps ROIC above WACC. Beyond it, fade incremental ROIC toward the cost of capital. A model in which excess returns never fade has assumed its own conclusion.
- **Terminal value, done properly:** `TV = NOPAT_{n+1} × (1 − g/ROIC_terminal) ÷ (WACC − g)`. The `g/ROIC` term is the reinvestment that growth must be paid for; a terminal value growing at 5% forever with no reinvestment is free money and is wrong. Cap `g` at long-run **nominal** GDP in the same currency.
- **Cross-check the terminal value against an exit multiple** and report the implied exit EV/EBIT. If perpetuity growth implies an exit multiple above today's or above the historical median, the model is smuggling in a re-rating.
- **Report the terminal-value share of present value.** Above 75–80% means the DCF is a terminal-value assertion with a spreadsheet attached. Say so rather than hiding it.
- **Treat SBC as a cash cost** (or model the resulting dilution). Adding it back and calling the result FCF overstates owner returns by exactly the amount transferred to employees.
- **Use mid-year discounting** where cash flows arrive evenly; it typically lifts value 3–5% and is the honest convention.
- **Bridge EV back to equity value** with the same bridge in reverse — EV − debt − leases − minorities − pension deficit + surplus cash + non-consolidated stakes — then divide by the *diluted* count.
- **Sensitivity is not optional.** Produce a two-way table of WACC (±150bps in 50bp steps) against terminal growth (±100bps), and a second on steady-state EBIT margin. Report the spread of outcomes, not the centre cell. If a 50bp WACC change moves value 30%, the DCF is a weak instrument for this company and the multiple and asset cross-checks must carry more weight — say that explicitly.
- **Reconcile to reality.** Compute implied terminal-year revenue, market share, reinvestment rate and ROIC, and check them against history, addressable-market size and base rates. A model that quietly has the company taking 60% of its market has an unstated assumption.

---

## Reverse DCF — the central discipline

Run this **before** your own forecast. Invert the model: hold the current price fixed and solve for the operating performance required to justify it.

Solve for and report as a table:

- **Implied revenue CAGR** over the forecast horizon
- **Implied steady-state EBIT (or FCF) margin**
- **Implied competitive-advantage period** — how many years of above-WACC returns are baked in
- **Implied terminal ROIC**
- **Breakeven growth** — the rate at which the stock returns exactly the cost of capital

Then decompose the price a second way: `PVGO = market cap − (normalised NOPAT ÷ WACC)`. That splits the price into the value of current operations continued forever and the value of growth not yet delivered. If 70% of the price is PVGO, you are not buying a business, you are buying a forecast — and the report should say exactly that.

**Judge the implied numbers against base rates, not against the story.** Very few companies of any size sustain 20%+ revenue growth for a decade; excess ROIC typically fades over 5–15 years; 1,000bps of sustained margin expansion is rare outside a genuine platform shift. If the implied expectations already exceed management's own guidance, the market has done the extrapolating for you. Inversely, when a stable, cash-generative business is priced for permanent decline — implied growth below zero, implied ROIC collapsing straight to WACC — that is the cheap case worth investigating, and the reverse DCF is how you *find* it rather than assert it.

This reframes the exercise from "what is it worth" (unfalsifiable) to "what must be true, and is that likely" (testable). It is also the strongest available defence against anchoring, which is precisely why it comes before your own model rather than after it.

---

## Earnings yield versus bond yield

Equities compete with bonds for capital, and the multiple that can be justified is a function of the rate regime.

- Compute the **earnings yield (E/P)** and, better, the **FCF yield**, and set them against the local 10-yr sovereign yield. The difference is the implied equity risk premium for this stock.
- Place that spread in **its own historical distribution**. There is no universal minimum; a 200bp gap can be generous in one market and thin in another.
- **Never compare yield gaps across currencies naively.** India's higher nominal bond yield accompanies higher nominal earnings growth, so an Indian equity showing a narrower yield gap than a US equity is not thereby expensive. Compare each market's gap to its own history. This is the Fed-model critique in miniature: setting a nominal bond yield against a real earnings yield systematically flatters equities when inflation is high, so use the yield gap as a regime check, never as a fair-value model.
- **Cross-check against the company's own credit.** If its investment-grade bonds yield more than its FCF yield, the debt is the better claim on the same cash flows and the equity needs the growth to justify itself.
- **Compare earnings yield to after-tax cost of debt.** This is the arithmetic that decides whether a debt-funded buyback creates value or merely swaps balance-sheet risk for EPS.
- **Note the direction of travel.** A valuation that only works under permanently low rates is a rate bet; label it as one. A multiple set in a 1% rate world does not survive a 5% one, however good the business.

---

## Valuation versus its own history

Its own past is usually the cleanest comparable a company has: same business model, same accounting, same disclosure culture.

- Plot **each** multiple — P/E, EV/EBIT, EV/EBITDA, P/S, P/FCF, dividend yield — against its own 5- and 10-year range. Report the **median** (not the mean) and the **current percentile or z-score**.
- Exclude periods where the multiple is undefined or absurd (loss years for P/E, transition years for lease accounting), and say which years you excluded.
- **Then answer the only question that matters: why?** A stock at the top of its band is a buy if the business genuinely re-rated — moat widened, mix shifted to higher-ROIC revenue, capital intensity fell, cyclicality reduced — and a sell if nothing changed but sentiment. Name the structural change or concede there is none. "It has always been expensive" is not an argument; it is the absence of one.
- **Decompose the last 5–10 years of shareholder return** into earnings growth + multiple change + dividend + buyback. If most of the historical return came from multiple expansion, that fuel is not available twice and forward return expectations must fall.
- **Neutralise the market.** Divide the stock's multiple by the index's (Nifty 50 / Sensex / S&P 500) to build a relative multiple series. A stock expensive against its own absolute history but cheap against its relative history is telling you the whole market re-rated, not the company.
- **Watch the accounting seams.** Lease capitalisation (FY20 India, 2019 IFRS/US), India's s.115BAA tax election, GST transition, demergers and large acquisitions all break the series. Restate or annotate; never average across a break.
- **A de-rating is not automatically an opportunity.** Test whether the multiple fell because the moat is eroding — falling incremental ROIC, rising customer churn, a new entrant — in which case the market is right and the low multiple is the new correct one.

---

## Valuation versus peers

- **Build the peer set on economics, not industry codes.** True comparables share business model, capital intensity, growth profile, customer concentration and end-market. List who is in the set and why, and demonstrate the set was not chosen to flatter the conclusion.
- **Normalise before comparing:** accounting standard (Ind-AS vs IFRS vs US GAAP), R&D capitalisation, lease treatment, SBC treatment, tax regime, consolidated vs standalone basis, and fiscal-year end.
- **Adjust for the drivers of a justified premium** — ROIC, growth, margin stability, leverage, governance. A premium must be *earned*. The disciplined version: regress peer EV/EBIT (or P/B) against ROIC and growth across 10–20 names and read the residual. The outlier versus the fitted line is the finding; the fit itself tells you how much multiple dispersion fundamentals explain at all.
- **Check the sector against itself.** Cheap relative to an expensive sector is not cheap. Plot the peer-group median multiple against its own history before drawing any conclusion from a relative discount.
- **Interrogate the discount.** Most discounts are deserved: weaker returns, worse governance, promoter overhang, lower liquidity, a structurally shrinking end market. State which applies and what would remove it.
- *India:* niche sectors often have two or three listed peers, all similarly mispriced. Use global comparables, but adjust explicitly for the cost-of-capital and nominal-growth differential — an Indian company legitimately trades at a different multiple from a US peer with identical economics because both the discount rate and nominal growth differ. Unlisted transaction multiples, QIP pricing and preferential-allotment prices are additional local evidence of what informed buyers pay.

---

## SOTP, private market value and replacement cost

Multiples and DCFs both start from the same accounting. These three cross-checks do not — which is why at least one belongs in every deep dive.

**Sum of the parts.** Value each segment on its own appropriate method — a multiple where a clean peer set exists, a DCF where it does not — then:

- Capitalise **unallocated corporate costs** as a negative-value stub at the same multiple, rather than ignoring them.
- Deduct **net debt, minorities and pension** at the consolidated level using the bridge above.
- Deduct **tax on disposal** wherever the thesis relies on selling an asset carried at historic cost.
- Apply a **holdco/conglomerate discount** and state whether it is structural (poor capital allocation, no intent to unlock) or temporary (a demerger is announced and dated). In India these discounts are structurally wide — 40–70% is common — and have persisted for decades. Assuming one closes is a thesis, not an adjustment.
- Report the **implied stub**: if market cap minus the value of listed stakes is near zero or negative, the operating business is being given away — genuinely interesting when the stakes are liquid and monetisable, a trap when they are not.
- Hunt for **understated assets**: land and property at historic cost, cross-holdings in listed entities, unconsolidated JVs, brands never capitalised, carry-forward tax losses (check usability — s.79 in India on ownership change, s.382 in the US), and a loss-making incubating unit whose losses mask a profitable core.

**Private market value.** What would an informed industrial or PE buyer pay for the whole thing? Anchor on precedent transaction EV/EBITDA in the same sector and geography, including a control premium of typically 20–35%. This behaves like a floor only when the asset is genuinely acquirable — check whether it is. A 60%+ promoter holding, a golden share, a sectoral FDI cap or a regulatory-approval requirement can make a company unbuyable, and the PMV then unrealisable.

**Replacement cost and Tobin's q.** `q = EV ÷ replacement cost of productive assets`. This is the supply-side test and the most useful valuation tool in capacity-driven industries. When q is well below 1, nobody builds new capacity, supply tightens and returns eventually recover; when q is far above 1, new supply is coming and current returns will fade — which is why a commodity producer at a low P/E and a high q is a sell, not a bargain. Use the physical denominators the industry itself uses: EV/tonne (cement, steel), EV/key (hotels), EV/bed (hospitals), EV/MW (power, data centres), EV/subscriber and EV/MHz (telecom), EV/acre or per saleable sq ft (real estate), EV/dwt or broker vessel values (shipping). Compare against current greenfield build cost and recent asset transactions. In deeply distressed situations, run **liquidation value** and net current asset value as the true floor, haircutting receivables and inventory realistically.

---

## Margin of safety

The margin of safety is risk control, not rhetoric. It exists because the estimate is wrong — the only questions are by how much and in which direction.

- **Scale the required discount to the uncertainty of the estimate**, not to enthusiasm for the idea. Indicative: 15–25% for a wide-moat, predictable, low-leverage compounder; 30–40% for an average business with a normal cycle; 50%+ for cyclicals, turnarounds, leveraged balance sheets, single-product companies, opaque governance or heavy promoter pledging. Graham's classic ~one-third is a midpoint, not a universal constant.
- **Take the discount off the conservative case, not the base case.** A 30% discount to an optimistic fair value is not a margin of safety; it is an optimistic fair value with a rounding error.
- **Do not stack conservatism.** Conservative cash flows + an inflated WACC + a large price discount is three haircuts compounded, and produces a value so low nothing ever qualifies. Decide where the conservatism lives and state it.
- **Lead with the downside.** Answer "what do I lose if I am wrong" before "what do I make if I am right". Quantify the bear case as a percentage decline and a probability of *permanent* impairment, not as a mood.
- **A margin of safety does not protect against a decaying asset.** Where intrinsic value is itself falling — melting-ice-cube economics, structurally impaired end market — the discount narrows on its own while you hold. Time is a cost there, not an ally.
- **Test against the sector's own floor.** Where the playbook prescribes one (NAV for shipping, replacement cost for cement, adjusted book for banks), measure the margin of safety against that floor as well as against your DCF.
- **Needing the bull case to justify entry is a disqualification**, not a close call.

---

## Quality trap versus value trap

Separate **business quality** (ROIC−WACC spread, moat durability, reinvestment runway, margin stability — established in `references/05-returns-and-dupont.md`) from **price paid** (the multiple), and place the stock on both axes.

| | Cheap multiple | Expensive multiple |
|---|---|---|
| **High, durable ROIC** | The rare case. Requires an identifiable reason the market is wrong. | **Quality trap** — a fine business whose return is consumed by multiple compression. |
| **Low ROIC, or ROIC fading to WACC** | **Value trap** — the discount is a fact about the business, not an opportunity. | Avoid outright. |

The arithmetic underneath: over a long holding period an owner's return converges toward the business's return on capital, not toward the entry multiple. A business compounding capital at 18% delivers something close to 18% to a patient owner even from a full price; a business earning 6% delivers close to 6% however cheaply it was bought, because the cheap multiple is a one-time gain while the low return repeats every year. **Entry price decides the first few years; ROIC decides the rest.**

So ask explicitly: **does time work for me or against me here?** In a high-ROIC reinvestor, waiting creates value. In a low-return business the only lever is the multiple closing, which requires a catalyst and a clock. Two failure modes follow, and both should be named in the report when present: paying a premium multiple for a business whose *incremental* ROIC is quietly sliding toward WACC (the quality trap — visible in ROIIC long before it shows in average ROIC), and anchoring to a low multiple on a structurally declining business while mistaking cheapness for safety (the value trap).

---

## Scenarios, expected value and IRR decomposition

Never report a single number. Build the table and let it carry the conclusion.

| Scenario | Probability | Key assumptions (revenue CAGR, steady-state margin, exit multiple) | Value per share | Return vs price | IRR over holding period |
|---|---|---|---|---|---|
| Bull | e.g. 20% | | | | |
| Base | e.g. 50% | | | | |
| Bear | e.g. 25% | | | | |
| Severe / permanent impairment | e.g. 5% | | | | |

- **Each scenario must be internally coherent**, not the base case ±10%. If the bull case assumes 20% volume growth, it must also carry the operating leverage *and* the capex and working capital that growth consumes. Flexing one variable at a time understates true dispersion.
- **Probabilities must be stated and sum to 1**, and should be sanity-checked against base rates — how often turnarounds of this type actually work, how often a company of this size sustains this growth. Bottom-up models produce inside-view optimism by construction; the reference class is the correction.
- **Compute the probability-weighted value and the upside/downside ratio.** A working standard is at least 3:1 upside to downside before an idea is interesting. A symmetric 60-up/40-down bet is a fundamentally different proposition from a capped-downside one at the same base case, and only the asymmetry table reveals it.
- **Decompose expected IRR into its sources:**

```
Expected annual return ≈ FCF or dividend yield
                       + growth in earnings / FCF per share
                       ± change in the multiple (re-rating or de-rating)
                       ± change in share count
                       ± FX translation into the holder's base currency
```

  State each term. If more than half the expected return depends on multiple expansion, the thesis is a re-rating bet and must be labelled as such — re-rating requires other people to change their minds, which the analysis does not control. A return built from FCF yield plus per-share growth with a flat or conservatively contracting multiple is far more robust at the same headline upside.
- **Time is part of the arithmetic.** A 40% gap to fair value is a 35% IRR if it closes in a year and about 7% if it takes five. State the assumed holding period and always express upside in annualised terms.
- **Test against a real alternative.** The hurdle is not zero — it is the expected return on the index or a risk-free instrument over the same horizon, after transaction costs (brokerage, STT and stamp duty in India; spread and impact cost in illiquid small caps) and after tax on the realised gain. A 12% gross expected return netting to 8% against an index expected to do the same is not an opportunity. Present this as analysis of the investment's merits — not as personalised advice, and not as a position size.

---

## Catalyst, edge and what is already discounted

A valuation gap is a hypothesis about other people's future opinions. Close the loop before concluding.

- **Why does the mispricing exist, and who is on the other side?** Name the mechanism: a forced seller, index exclusion, a broken-IPO or lock-up overhang, coverage neglect below a market-cap threshold, a temporary earnings dislocation being extrapolated. If there is no answer, the most likely explanation is that the price is right and the model is not.
- **What is the edge?** Informational (rare), analytical (you modelled the fade rate correctly), or behavioural/time-horizon (you can hold through three bad quarters). Behavioural edge is the only durable one for most analysis, and it requires the catalyst timeline to be long, not absent.
- **Enumerate catalysts with expected timing:** earnings inflection, margin recovery, a capex cycle ending and FCF appearing, capital-return initiation, deleveraging past a covenant threshold, demerger or spin-off, management change, index inclusion, a regulatory decision, promoter stake increase or open offer. Distinguish a self-correcting mispricing (FCF accumulates and does the work) from one that requires an event to occur.
- **Know what is already discounted.** Check consensus estimate levels and dispersion, the direction and breadth of recent revisions, and where your forecast sits versus the street. Returns come from surprises against expectations, not from absolute results. Cross-reference with the reverse DCF: consensus estimates and price-implied expectations are frequently different, and the gap between them is itself information.
- **Steel-man the bear case.** Read the best-argued short thesis available and state which parts you accept. A valuation section with no articulated bear case has not been stress-tested, and a pre-mortem — "it is two years later and this is down 50%; what happened?" — usually surfaces the assumption you never examined.

---

## Sector overrides

**The sector playbook overrides everything above.** Applying a generic P/E across sectors is the valuation equivalent of ranking companies on operating margin.

| Sector | Default method breaks because | Use instead |
|---|---|---|
| **Banks, NBFCs, HFCs** | Debt is raw material; EV and EV/EBITDA are undefined. | P/B and P/ABV against ROE, justified P/B = (ROE − g)/(COE − g), RoRWA, stressed-book scenarios. `sectors/banks.md`, `sectors/nbfc.md` |
| **Life insurers** | Accounting profit is an artefact of new-business strain. | P/EV, VNB multiple, appraisal value. General insurers: combined ratio with P/B. `sectors/insurance.md` |
| **REITs, InvITs, developers** | Depreciation on appreciating assets destroys the earnings base. | AFFO yield, NOI cap-rate spread, NAV; developers on land-bank NAV plus pre-sales. `sectors/realestate-reit.md` |
| **Miners, steel, oil & gas, commodity chemicals** | P/E is inverted across the cycle — lowest at the peak. | Mid-cycle EV/EBITDA, P/NAV at a stated commodity deck, EV per tonne or boe of reserve, cost-curve position. `sectors/metals-mining.md`, `sectors/oil-gas.md`, `sectors/chemicals-cement.md` |
| **Airlines, hotels** | Leases and operating leverage dominate; earnings swing through zero. | EV/EBITDAR, EV per seat-km or per key, fleet replacement cost. `sectors/aviation-hotels.md` |
| **Shipping** | Asset values move faster than earnings. | P/NAV on broker vessel valuations, EV per dwt, mid-cycle charter rates. `sectors/shipping-logistics.md` |
| **Regulated utilities** | Returns are capped by the regulator. | Multiple of regulated asset base, allowed vs achieved RoE, dividend discount model. `sectors/utilities-power.md` |
| **Holdcos, conglomerates, asset managers** | Consolidated multiples blend unlike businesses. | SOTP with an explicit, justified holdco discount; AUM-based multiples for managers. `sectors/holdco-assetmgr.md` |
| **Loss-making growth / new-age** | There is no E for the P/E. | EV/Sales decomposed to an implied steady-state margin, EV/gross profit, cohort unit economics, reverse DCF on the implied margin. |
| **IT services, SaaS** | The growth-versus-margin trade-off is a choice, not a fact. | EV/FCF, EV/Sales against Rule-of-40, retention-adjusted economics. `sectors/it-saas.md` |
| **Pharma** | Value sits in a pipeline with binary outcomes. | Base-business EV/EBITDA plus probability-adjusted rNPV per asset. `sectors/pharma-healthcare.md` |

---

## India (Ind-AS/NSE-BSE) vs US/global conventions

**India-specific**

- **Units.** Market cap and EV in ₹ crore (1 crore = 10 million; 1 lakh = 100,000). State the unit in every table; mixing crore and million is the most common presentation error in India-focused output.
- **Standalone vs consolidated.** Screeners routinely serve standalone P/E and ROCE for companies whose economics are consolidated. Every valuation input must be consolidated — and the EV bridge must then carry the minority interest consolidation creates.
- **Accounting seams that break the multiple history.** Ind AS 116 lease capitalisation (FY20) lifted EBITDA and EV; the s.115BAA election to a ~25.17% effective tax rate (FY20 onward) lifted EPS. Neither is operating. Restate pre-FY20 years before plotting a ten-year multiple band.
- **Surplus treasury sits in "current investments"** (liquid mutual funds), not in cash. Deduct it in the bridge *and* remove its yield from EBIT.
- **CCPS, CCDs, warrants and ESOP pools** in recently listed companies materially change the diluted count. The share-capital and ESOP notes in the annual report are the source; the exchange filing cover page is not.
- **Promoter holding, pledge and open-offer mechanics.** SEBI's takeover code triggers a mandatory open offer past the 25% threshold with a formula-based price floor; delisting runs through reverse book-building. These create observable floors and ceilings in control situations. High promoter holding with a thin free float can sustain a multiple well above fundamentals — and can collapse it when pledged shares are invoked.
- **Holdco discounts are structurally wide and durable** (40–70% is common). Never model one closing without a named, dated catalyst.
- **Buybacks:** since the October 2024 change, buyback proceeds are taxed in shareholders' hands as deemed dividend, materially altering the buyback-versus-dividend calculus for Indian companies. Verify the current-year treatment before comparing shareholder yield across the India/US boundary.
- **Frictions a gross return ignores:** STT on both legs, exchange charges, stamp duty, GST on brokerage, and LTCG on listed equity above an annual exemption with a higher STCG rate. Verify current-year rates — they have changed repeatedly.
- **Concalls and investor presentations** frequently disclose segment EBIT, capacity, utilisation, order book and per-unit realisations absent from the filing, and these are essential for SOTP and EV-per-unit work. Cite the quarter.
- **CARO 2020** disclosures on related-party loans and unrecorded transactions are a direct cross-check on whether the "surplus cash" you deducted in the bridge is genuinely available to shareholders.

**US/global**

- **10-K, 10-Q, DEF 14A via EDGAR.** Segment data under ASC 280 for SOTP; the Reg G non-GAAP reconciliation sizes the adjusted-versus-GAAP gap for you.
- **SBC is large and must be treated as a cost.** US technology "adjusted EBITDA" and "adjusted FCF" that add SBC back overstate owner returns directly and materially.
- **Leases under ASC 842 (2019)** create the same series break as Ind AS 116, but US GAAP retains the operating/finance distinction in the P&L, so EBITDA is *not* affected identically to IFRS. Check before comparing EBITDA multiples across the standards boundary.
- **Convertibles with capped calls** need careful dilution treatment; the if-converted count in the 10-K may not reflect the hedge.
- **The 2017 US tax change** creates a discontinuity in historical P/E and EV/EBIT series.
- **Negative book equity** is normal in mature US firms after decades of buybacks; P/B is undefined and should be suppressed rather than printed.
- **A 1% excise on net buybacks** (from 2023) slightly reduces buyback yield.
- **NOL usability** is capped after an ownership change (s.382), so a headline NOL balance is worth less than face value in an SOTP.
- **ADRs** carry withholding tax and depositary fees, and the ADR price embeds an FX view — value the underlying in local currency and translate separately.

---

## Errors that ruin this section of the report

- **Anchoring:** building the DCF after looking at the price, then tuning WACC or terminal growth until it agrees. Run the reverse DCF first.
- **A broken EV bridge:** leases, minorities, pensions or the option overhang omitted; or gross cash deducted when most of it is operating, trapped or customer float.
- **Mixing claims:** an equity numerator against an enterprise denominator, or consolidated EBITDA against a parent-only EV.
- **Currency mismatch:** discounting INR cash flows at a USD WACC, or calling a 3% terminal growth rate conservative in a 5–6% inflation currency.
- **A single point value** with no sensitivity table and no scenario range.
- **Terminal value carrying 85% of the answer**, unreported.
- **Comparing multiples across the FY20/2019 accounting seam** and calling the step-change a trend.
- **Peer sets chosen to flatter**, or a "discount to peers" in a sector that is itself at a record multiple.
- **Using a low P/E on a peak-cycle commodity earner as evidence of cheapness** — the single most expensive error in this file.
- **Adding back SBC** to reach the FCF that supports the valuation.
- **Assuming a holdco or conglomerate discount closes** with no catalyst and no timeline.
- **Printing a multiple the sector playbook declares undefined** (EV/EBITDA for a bank, P/E for a REIT) with a caveat instead of suppressing it. A caveated number is still a number the reader anchors on.
- **Reporting fair value to two decimals** when the inputs are three judgement calls. Give a range and state what drives its width.
- **Presenting the output as advice.** Give the valuation range, the assumptions, the bear case and the falsifiers; do not issue a buy instruction or a position size.

---

## Checklist

- [ ] Consult the sector playbook first; use its prescribed method and suppress every multiple it declares undefined or inverted.
- [ ] Normalise earnings for one-offs, cycle position and tax before computing any multiple; state reported vs adjusted and why.
- [ ] Build the full EV bridge — diluted count, debt, leases, preferreds/CCPS, minorities, pension deficit, earn-outs, less *surplus* cash and non-consolidated stakes — and show it as a table.
- [ ] Verify every multiple pairs an equity claim with equity value and an enterprise claim with EV.
- [ ] Derive WACC explicitly: risk-free in the cash-flow currency, ERP, country risk premium by revenue exposure, bottom-up relevered beta, marginal cost of debt, market-value weights. Date it.
- [ ] Apply the currency-consistency rule; never discount local-currency cash flows at a foreign rate.
- [ ] Run the reverse DCF **before** your own forecast; report implied growth, margin, CAP, ROIC, breakeven growth and the PVGO share of price.
- [ ] Test the implied expectations against base rates and against management's own guidance.
- [ ] Build the DCF with an explicit fade toward WACC, a reinvestment-consistent terminal value, and g ≤ nominal GDP in the same currency.
- [ ] Report terminal value as a % of total, plus the implied exit multiple versus today's and the historical median.
- [ ] Produce two-way sensitivity tables on WACC × terminal growth and on steady-state margin; report the range, not the centre cell.
- [ ] Treat SBC as a cost, not an add-back, in every cash-flow measure.
- [ ] Compute FCF yield, owner-earnings yield and total shareholder yield; confirm buybacks are FCF-funded, net of SBC, and executed below your value range.
- [ ] Compare earnings/FCF yield to the local 10-yr sovereign and to the company's own after-tax cost of debt; place the spread in its own history.
- [ ] Plot every multiple against its own 5–10 year median and percentile; explain deviations structurally or concede mean reversion.
- [ ] Decompose historical shareholder return into earnings growth, multiple change and yield.
- [ ] Build a defensible peer set, normalise accounting, regress multiples against ROIC and growth, and interpret the residual rather than the raw discount.
- [ ] Check the peer group's own multiple against its history to rule out whole-sector mispricing.
- [ ] Run at least one non-accounting cross-check: SOTP, private market value with a control premium, or replacement cost / EV per physical unit and Tobin's q.
- [ ] For SOTP, net corporate costs, disposal taxes and a justified holdco discount; report the implied stub.
- [ ] Map the stock on quality (ROIC−WACC) versus price and name it: compounder, cigar-butt, quality trap or value trap.
- [ ] State the margin of safety as a % against the *conservative* case, sized to estimate uncertainty, without stacking conservatism three times.
- [ ] Build a 3–4 scenario table with stated probabilities, coherent per-scenario assumptions, a probability-weighted value and an upside/downside ratio.
- [ ] Decompose expected IRR into yield + growth + re-rating + share count + FX; flag if re-rating is more than half of it.
- [ ] State the assumed holding period, annualise the upside, and net it against transaction costs, taxes and the index alternative.
- [ ] Name the catalyst and its timing, why the mispricing exists, and what is already in consensus estimates.
- [ ] State explicit falsifiers: the price, multiple or operating outcome that would prove the valuation wrong.
- [ ] Label all indicative ranges as indicative; let peer and own-history comparison carry the conclusion.
- [ ] Present a range with assumptions and a bear case — research, not a recommendation and not a position size.
