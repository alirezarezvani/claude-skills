# Discount Economics

The math of what a discount actually costs. Most sales discounts are described as a list-price reduction; the real impact is on **gross margin** and **LTV**, both of which compound across the customer base over time.

## The fundamental formula

A discount of D% on a product with gross margin G% reduces net margin by:

    margin_loss_points = D * (G / 100)
    net_margin = G - margin_loss_points

### Worked examples

| List discount | Gross margin | Margin loss | Net margin |
|---|---|---|---|
| 10% | 80% | 8 pts | 72% |
| 20% | 80% | 16 pts | 64% |
| **30%** | **80%** | **24 pts** | **56%** |
| 30% | 60% | 18 pts | 42% |
| 40% | 80% | 32 pts | 48% |
| 50% | 80% | 40 pts | 40% |

**A 30% discount on an 80%-gross-margin product wipes 24 points of margin** — that's a 30% margin loss in *relative* terms (24/80 = 30%), but the conventional shorthand "30% discount = 30% margin hit" understates the absolute hit on a low-margin product.

### Why the conventional shorthand is wrong

People often say "a 30% discount loses 30% of margin." That's only true for a 100%-margin product. For an 80%-margin SaaS, the discount cuts the **revenue** by 30% but the **margin** by 30% × (80/100) = 24 points, or 30% in relative terms. The dollar impact compounds across the contract term.

## LTV impact

Discount also compounds across multi-year contracts. A 24-month deal at 30% discount loses:

    lifetime_margin_loss = (D / 100) * G/100 * list_price * (term_months / 12)

For a $200K-ARR deal at 30% discount, 80% gross margin, 24-month term:

    = 0.30 * 0.80 * 200,000 * 2 = $96,000 of gross margin given up

That's $96K of fully-loaded P&L impact for one deal. Across 50 deals/quarter at the same discount, the company is giving up $19.2M/year in gross margin.

## Discount creep

The most-cited dataset (Pacific Crest / KeyBanc SaaS Survey) shows median discount rises ~1.5 pts/year unless the deal desk actively defends pricing. Causes:

1. AE comp on bookings, not margin → AEs discount to close.
2. Multi-year deals trade discount for term length but term length doesn't recover the margin loss if churn risk is non-zero.
3. Competitive deals get matched discounts that then propagate to non-competitive deals via MFN clauses.
4. Renewal discounts (CS giving discount to retain) anchor the next renewal lower.

## When a discount is justified

The deal desk should approve a discount when **at least one** of these is true and quantified:

1. **Strategic logo** — the customer is a reference account that materially shortens future sales cycles. Logo value ≥ discount $.
2. **Expansion lock-in** — the discount is paired with a *multi-year + expansion commitment* that recovers margin over the contract term.
3. **Competitive displacement** — the discount displaces an incumbent and the lifetime ARR > displacement cost.
4. **Cash-acceleration** — payment up-front in exchange for discount, where the cash NPV recovers the margin loss.

The deal scorer's `strategic` dimension flags logo / reference / expansion / renewal explicitly. If none of those are set, a discount above the policy band is presumptively unjustified.

## NRR + discount correlation

OpenView's *State of the SaaS Industry* shows companies with high NRR (≥ 120%) discount less on initial deals than companies with low NRR (≤ 100%). The mechanism: high-NRR companies have a strong expansion motion that they don't need to buy with up-front discount; low-NRR companies discount up-front to compensate for weak expansion.

This is why deal-desk should treat "discount to close" as a leading indicator of NRR weakness, not a one-deal problem.

## Sources

1. **David Skok — For Entrepreneurs** — *SaaS Metrics 2.0* and *The SaaS Business Model*. Canonical treatment of LTV/CAC + the impact of discount on payback period. https://www.forentrepreneurs.com/
2. **Bessemer Venture Partners — State of the Cloud** — Annual report with discount benchmarks by ACV band ($1K, $10K, $100K, $1M+) and stage. https://www.bvp.com/
3. **Tomasz Tunguz — Redpoint** — Multi-year studies on discount-to-close patterns, including the finding that median enterprise SaaS discount sits at 18-22% across the industry. https://tomtunguz.com/
4. **OpenView Venture Partners** — *State of the SaaS Industry* + Expansion Economics research. Documents the NRR-vs-discount correlation. https://openviewpartners.com/
5. **Pacific Crest SaaS Survey** (now KeyBanc Capital Markets) — Annual primary-research survey of B2B SaaS companies. Most-cited dataset for discount benchmarks. https://www.key.com/businesses-institutions/industry-expertise/saas-survey.html
6. **KeyBanc Capital Markets SaaS Survey** — Continuation of Pacific Crest. Annual benchmark for net dollar retention, gross margin, and discount-by-segment.
7. **Insight Partners Revenue Operations Research** — Their PitchBook + portfolio data on discount discipline at growth-stage SaaS. https://www.insightpartners.com/

## Patterns to surface in any margin review

- Pre-discount gross margin and post-discount net margin in **absolute points**, not just percent.
- Lifetime margin given up over the contract term, in dollars.
- Whether the strategic flags justify the discount (logo / reference / expansion / renewal).
- Whether the customer is paying up-front in exchange for the discount (cash NPV).
- Comparison to the company's median deal-discount (drift signal).
