# IPO mode — analysing a company that is not yet listed

Use this when: the company has **not started trading yet** — an open or upcoming IPO, a filed DRHP, an announced price band, an SME-platform issue, or "should I apply to X's IPO". If the company already trades and listed within roughly the last two years, this is the wrong file: use `references/13-situations.md` §8 instead, which handles the post-listing overlay.

An IPO is not a cheaper version of a listed-company analysis. Two of this skill's load-bearing mechanisms are simply unavailable, and one question changes shape entirely:

- **There is no own-history benchmark.** You have restated prospectus financials prepared by the issuer for the purpose of selling, not audited public reporting under scrutiny. Half the skill's comparison logic — "how does this company compare to its own five-year record?" — cannot run.
- **There is no market price to test.** The price is *set* by the issuer and bookrunners, not discovered. So the valuation question is not "is the market wrong?" but **"is this band justified against listed peers, and what does it assume?"**
- **The information asymmetry is at its maximum and runs entirely against you.** IPOs are sold, not bought. They are timed by informed sellers into favourable markets, with disclosure the seller controls and coverage largely originating from the bookrunners.

Everything below follows from those three facts.

## Contents

- [Stage I0 — Establish the offer](#stage-i0--establish-the-offer)
- [Stage I1 — Get the right document](#stage-i1--get-the-right-document)
- [Stage I2 — Who is selling, and why now](#stage-i2--who-is-selling-and-why-now)
- [Stage I3 — Interrogate the restated financials](#stage-i3--interrogate-the-restated-financials)
- [Stage I4 — Sector playbook and listed-peer benchmarking](#stage-i4--sector-playbook-and-listed-peer-benchmarking)
- [Stage I5 — Value the band, not the company](#stage-i5--value-the-band-not-the-company)
- [Stage I6 — Structure, supply and mechanics](#stage-i6--structure-supply-and-mechanics)
- [Stage I7 — Verdict and what to watch](#stage-i7--verdict-and-what-to-watch)
- [Scoring adjustments](#scoring-adjustments)
- [Checklist](#checklist)

## Stage I0 — Establish the offer

Before any analysis, pin down what is actually being sold:

| Item | Why it matters |
|---|---|
| Issuer, exchange, **main board vs SME platform** | SME issues (NSE Emerge, BSE SME) carry materially lighter disclosure, thinner post-listing scrutiny, larger lot sizes and far worse liquidity. Say so prominently if it is one |
| Total issue size, and the **fresh issue vs offer-for-sale split** | Fresh issue money enters the company; OFS money goes to exiting shareholders. **A 100% OFS raises nothing for the business** |
| Price band (floor and cap), face value, lot size | All valuation work must be run at **both** ends of the band |
| Implied market cap at floor and at cap | The number most retail coverage never states plainly |
| Post-issue promoter holding and total dilution | How much of the company is actually being sold |
| Issue dates, anchor allotment date, listing date | Anchor book pricing is a data point available before you decide |
| Registrar and bookrunners | Track record matters; so does whether coverage is BRLM-affiliated |
| Reservation/discount for employees, shareholders, retail | Changes effective price for some applicants |

## Stage I1 — Get the right document

- **DRHP** (draft) — filed with SEBI, **contains no price band**. Fine for business and financial analysis; useless for valuation.
- **RHP** (red herring) — filed after SEBI observations, **contains the price band and the "Basis for Offer Price" section**. This is the document you need to assess valuation.
- **SEBI observation letter, addenda and corrigenda** — changes between DRHP and RHP tell you what the regulator pushed back on.
- **US equivalent:** Form S-1 and its amendments (S-1/A); the final prospectus (424B4) carries the priced terms.

Sources: SEBI's website, the exchange sites (NSE/BSE), the BRLM sites, and the registrar. For US issues, EDGAR. If you only have news coverage of the IPO and not the RHP itself, say so — coverage routinely misreports the OFS split and the implied multiple.

**Two RHP sections do a great deal of work and are frequently skipped:**

1. **"Basis for Offer Price"** — the issuer's own justification, including its stated P/E, EV/EBITDA and RoNW at the band, and its chosen peer set. Read the peer set critically: issuers pick flattering comparables. Rebuild it yourself using `references/10-peer-set.md`.
2. **KPI disclosure** — since 2022 SEBI requires issuers to disclose the KPIs they shared with pre-IPO investors, with peer comparison, certified and approved by the audit committee. This is a direct, mandated window into the metrics management itself considers definitive, and into what earlier investors were shown.

Also read the **Risk Factors** section in full. It is drafted by lawyers to protect the issuer, which makes it the most candid disclosure in the document — the material risks are genuinely listed there, just buried in volume.

## Stage I2 — Who is selling, and why now

This is the analytical heart of an IPO, and it has no equivalent in listed-company work.

- **Identify every selling shareholder and the size of each stake being sold.** Promoter, founder, PE/VC, strategic investor, employees.
- **Cost basis and the last private round.** If a PE holder entered at ₹X two years ago and is exiting at 8×, that is their view of fair value — expressed with real money and better information than you have.
- **Is the promoter selling, and how much?** Founders trimming a small stake for liquidity is normal. Founders exiting a large proportion at the top of a cycle is a signal, and should be weighed against whatever growth story the RHP tells.
- **Use-of-proceeds specificity.** "Funding a named plant with a named capacity and a stated commissioning date" is a real plan. "General corporate purposes", "repayment of borrowings availed from promoters" and large unallocated portions are much weaker, and the proportion going to each should be stated.
- **Why this window?** IPOs cluster at cyclical and sentiment peaks in the issuer's sector. Ask explicitly whether the sector is at a favourable point in its cycle, and consult the relevant sector playbook on where the cycle is.

## Stage I3 — Interrogate the restated financials

You typically get three to five years of restated financials. Treat them as a document prepared to support a sale.

**The margin-ramp test.** A beautiful three-year improvement into the IPO year is a **warning, not a strength**. Pre-IPO financial dressing is common and frequently reverts within four to eight quarters of listing. Plot revenue growth, margins and working capital by year and ask what changed and whether the change is structural or presentational.

**Specific things to hunt:**

| What | Why |
|---|---|
| Related-party clean-ups executed shortly before filing | Transactions that existed for years and vanish just before the DRHP indicate what the structure actually looked like |
| One-off or lumpy revenue concentrated in the final year | Inflates the base the multiple is applied to |
| Working-capital squeeze into the IPO year | Stretched payables, channel stuffing, receivables factoring — flatters cash flow at exactly the moment it is being examined |
| Restructuring, carve-outs, subsidiary transfers in the period | Restated financials for a business that did not exist in that form; comparability across years may be fictional |
| Change of auditor during the restated period | See `references/07-forensic-red-flags.md` §8 |
| Promoter remuneration and any pre-IPO bonus/ESOP grants | Post-listing cost base may differ from the historical one |
| Contingent liabilities and litigation | Disclosed in the RHP at length; quantify against equity |

Run the **forensic triage** from `references/18-forensic-mode.md` Stage F1 on the restated numbers — cash conversion, receivables vs sales, capex vs depreciation, audit opinion. The cluster rule and the no-assertion-of-fraud discipline apply exactly as they do elsewhere.

## Stage I4 — Sector playbook and listed-peer benchmarking

Route to the sector playbook as normal — the sector determines which metrics apply, and that is unchanged by listing status. A pre-IPO bank is still assessed on NIM, GNPA and CAR; a pre-IPO REIT on AFFO and occupancy.

Because own-history benchmarking is unavailable, **the listed peer set carries the entire comparative load.** Build it explicitly per `references/10-peer-set.md`, and state it. Where the issuer has no genuine listed comparable — increasingly common for platform and new-economy issues — say so plainly rather than forcing a bad peer. The honest output there is a wider valuation range and lower confidence, not a fabricated precision.

## Stage I5 — Value the band, not the company

Run every valuation at **both the floor and the cap**, and present them side by side. The cap is what you will most likely pay in an oversubscribed issue.

1. **Compute the implied multiples at the band** — P/E, EV/EBITDA, P/B, P/S on post-issue share count. Post-issue count, not pre-issue: fresh issue dilutes.
2. **Compare against the listed peer set** on the sector's correct multiple, not a generic P/E.
3. **Check the issuer's own "Basis for Offer Price" arithmetic** and its peer selection. Where you disagree, show both.
4. **Reverse-engineer the assumption.** What growth and margin does the cap of the band require to deliver an acceptable return? This is the most useful single output of the whole exercise — it converts "is it expensive?" into a testable claim about the business.
5. **Anchor book as a reference point.** Anchors are allotted at the cap and their identities are disclosed. Long-only institutions and sovereign funds are a different signal from a book dominated by short-horizon money — though note anchors are allocation-driven and their participation is not diligence you can rely on.
6. **Last private round valuation** as a sanity check. An IPO priced below the last round is a real signal; so is one priced at a large premium to a round done months earlier.

Be explicit that a first-day price is not a valuation. **Grey-market premium (GMP) carries zero information about business value** and should never appear in the valuation section; if the user raises it, say what it actually is — an unregulated, unofficial, often manipulated indicator of short-term demand.

## Stage I6 — Structure, supply and mechanics

- **Lock-in expiry calendar** — build the actual dates. **India (SEBI ICDR):** anchor investors, 50% of allotment for 30 days and the remainder for 90 days; minimum promoter contribution for 18 months; other pre-issue capital typically 6 months. **US:** typically 180-day underwriter lock-up with earlier release triggers. Each expiry is a scheduled, foreseeable supply event.
- **Post-issue free float** — small float creates volatility and can create index-inclusion demand unrelated to value.
- **Allocation structure** — QIB / NII / retail split, and any reservation. Note that issuers without the profitability track record route face a different mandated split, which is itself informative.
- **Subscription data**, if the issue is open — informative about demand, not about value.
- **Post-issue capital structure** — ESOP pool, outstanding convertibles, further dilution already contemplated.

## Stage I7 — Verdict and what to watch

Run `references/20-challenge-pass.md` first. The IPO-specific challenges worth forcing: is the peer set the one *you* built or the one the issuer supplied? Have you valued at the **cap** and on **post-issue** share count? Is the margin ramp being treated as a strength when it should be a warning? Is any part of the verdict resting on subscription figures or GMP, which carry no information about value? And have you separated "good business" from "good price at this band" — an IPO can be both a fine company and an expensive issue.

Deliver an assessment of **business quality** and **whether the band is defensible against listed peers**, with the assumptions the price requires. Do not tell the user whether to apply — that is a personalised investment decision. Presenting the analysis, the range, the risks and the specific things that would change the conclusion is both more useful and the correct boundary.

Distinguish two questions the user may be conflating, because they have different answers and different evidence:

1. **Is this a business I want to own for years?** — answered by the analysis above.
2. **Will it pop on listing?** — a question about short-term demand and allocation dynamics, not fundamentals. The skill does not predict listing pops, and should say so.

**What to watch post-listing** — give the user a concrete list: the first two to four quarters of *public* reporting to test whether prospectus-year margins hold; the first major lock-up expiry; whether use-of-proceeds is deployed as stated; and any divergence between reported KPIs and the ones disclosed in the RHP.

## Scoring adjustments

`scripts/score.py` works pre-listing with three adjustments — state that you made them:

- **Mark own-history metrics as unavailable.** `multiple_vs_own_10y_median_pct` and any `own_history` basis cannot be computed. Omit them; the scorer renormalises weights across available metrics and reports the reduced coverage. Do not substitute a guess.
- **Score valuation at the cap of the band**, using post-issue share count, and note that the floor would score better. Use `peer_values` for the listed peer set so the valuation category is scored on peer percentile rather than absolute bands.
- **Expect and report lower coverage.** A pre-IPO scorecard legitimately has weaker coverage than a listed one. If coverage falls below the threshold, report the category scores without a headline composite rather than presenting a confident number built on gaps.

Gates apply unchanged, with one addition worth checking explicitly: a **100% offer-for-sale with vague use-of-proceeds and a heavy promoter exit** is a governance concern that belongs in the verdict, not averaged into a category.

## Checklist

- [ ] Main board vs SME platform identified and its disclosure implications stated.
- [ ] RHP obtained (not just news coverage); DRHP-only noted as a valuation limitation.
- [ ] Fresh issue vs OFS split quantified; 100% OFS flagged explicitly.
- [ ] Every selling shareholder, their stake sold, and cost basis / last round valuation identified.
- [ ] Use-of-proceeds assessed for specificity; unallocated and promoter-loan-repayment portions quantified.
- [ ] "Basis for Offer Price" section read; issuer's peer set rebuilt independently.
- [ ] Mandated KPI disclosure and peer comparison read.
- [ ] Risk Factors section read in full.
- [ ] Margin ramp into the IPO year tested and explained as structural or presentational.
- [ ] Related-party clean-ups, restructurings and final-year one-offs hunted in the restated period.
- [ ] Forensic Stage F1 triage run on the restated financials.
- [ ] Sector playbook applied; listed peer set built explicitly and stated.
- [ ] Implied multiples computed at **both** floor and cap on **post-issue** share count.
- [ ] Reverse-engineered growth/margin assumption at the cap stated.
- [ ] Anchor book composition and last private round used as reference points.
- [ ] Full lock-in expiry calendar built with dates.
- [ ] GMP explicitly excluded from valuation and explained if raised.
- [ ] Scoring adjustments made and disclosed; coverage reported.
- [ ] "Own for years" vs "will it pop" separated; no listing-pop prediction offered.
- [ ] Post-listing watch list delivered.
- [ ] No apply/don't-apply instruction; analysis and range presented instead.
