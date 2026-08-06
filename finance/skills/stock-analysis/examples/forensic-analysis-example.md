# Forensic review — Kesar Agro Industries (NSE: KESARAGRO)

> **ILLUSTRATIVE EXAMPLE — FICTIONAL COMPANY.** Kesar Agro Industries Ltd does
> not exist. This is a worked exemplar of the skill's Forensic-mode output, run
> against the extracts in `evals/fixtures/synthetic-ar-excerpt.md`. Every figure
> is invented. It illustrates method and tone — including the discipline of
> describing what disclosure shows without asserting fraud — not a real finding.

**Verdict: D — Structural integrity risk.**
As of 2026-08-02 · Basis: Consolidated · Currency/units: INR crore
Most recent period incorporated: FY26 (ended 31-Mar-2026), audited. Pre-Q1-FY27.

---

## Document base

**Obtained:** FY26 annual report extracts — five-year highlights, Independent Auditor's Report (consolidated), CARO 2020 annexure, related-party note (38), contingent-liabilities note (39), four-quarter shareholding/pledge pattern, corporate-governance extract [all: Kesar Agro FY26 AR extract, §1–§7].

**Not obtained (and what each would test):** full notes to accounts and receivables ageing table (extent of the ₹210 cr >365-day receivable and its provisioning); MCA/ROC filings of Kesar Estates Pvt Ltd (whether the ₹180 cr advance is recoverable); prior-year annual reports in full (silent restatements); concall transcripts (management's account of the default and going-concern); rating rationale (liquidity grade). This is a **filings-extract-only** pass — but note that verdict D here rests on the auditor's own qualified opinion, which is decisive from the documents in hand.

## Summary

The accounts cannot be relied upon as presented. The auditor has issued a **qualified opinion** over an unprovided ₹180 cr interest-free advance to a promoter-controlled entity, and separately flags a **material uncertainty over going concern** [§2]. Independently, reported profit rose every year FY22–FY26 while operating cash flow was **negative and worsening** across the same period [§1], and the CARO annexure reports a term-loan default, unpaid statutory dues, evergreening, and — most concretely — that the receivables the company reported to its banks **do not agree with its books** [§3]. Several independent flags converge on the same place: profit has gone into receivables and related-party advances, not cash. The single most load-bearing unresolved item is the ₹180 cr advance, which alone exceeds three years of cumulative reported profit.

## Triage results

| # | Test | Result | Reading |
|---|---|---|---|
| 1 | Cash conversion (5y cumulative CFO/PAT) | CFO Σ(FY22–26) = −₹164 cr vs PAT Σ = +₹239 cr → **−0.69** [§1] | Profit is not becoming cash; it is reversing into cash *out*flow. Caps composite at 4.0. |
| 2 | Implied yield on cash vs short rates | Interest income ₹3 cr ÷ avg cash ~₹200 cr = **~1.5%**, vs ~11% paid on borrowings [§1] | Cash earns far below the rate paid to borrow; either restricted/encumbered or not fully there. Cost of carry is value-destructive with no stated reason. |
| 3 | Receivables vs sales | Receivables CAGR **27.9%** vs revenue CAGR **15.9%** (FY22–26); DSO 82 → 122 days [§1] | Sustained divergence; caps composite at 6.0. WC test below rules out the innocent reading. |
| 4 | Capex vs depreciation | Not determinable from the extract | Flagged as a gap; full cash flow / PPE note needed. |
| 5 | Audit opinion | **Qualified**, plus going-concern material uncertainty, plus prior auditor **resigned** mid-term [§2, §3] | Qualified opinion caps at 4.0; resignation without a clean reason caps at 4.5. Both are structural (D) signals. |
| 6 | Related party & pledge | RP advance ₹40→95→**180 cr** interest-free; below-market RP sales; promoter pledge **18%→71%** [§4, §6] | Tunnelling indicators cap at 4.5; pledge >50% caps at 4.0. |

**Innocent-explanation test (mandatory before flagging #1/#3):** could the cash gap simply be a fast-growing, working-capital-heavy agri business? No. Receivables as a % of sales *rose* from 22.5% (FY22) to 33.5% (FY26) [computed, §1]. A stable ratio on a growing base would be growth; a *rising* ratio means the growth is being funded, not earned. The innocent reading does not survive.

## Findings

**F1 — Unprovided related-party advance (₹180 cr).**
- *What the disclosure shows:* an interest-free advance to Kesar Estates Pvt Ltd (promoter-controlled), no repayment schedule, outstanding and growing three years, no provision; the auditor states profit before tax would be ₹180 cr lower if provided [§2, §4].
- *Severity:* structural integrity risk.
- *Innocent explanation:* a genuine, recoverable operational advance. But recoverability is precisely what the auditor could not evidence, and the balance grows yearly regardless of performance.
- *What would resolve it:* Kesar Estates' MCA financials and the terms/security of the advance.
- *Cluster:* joins the below-market RP sales (§4) and the ₹300 cr guarantee to the same entity (§5) — all pointing at promoter-group leakage.

**F2 — Profit-to-cash reversal, landing in receivables and RP advances.**
- *What it shows:* PAT +₹239 cr cumulatively (FY22–26) against CFO −₹164 cr; over the same window receivables rose ~₹538 cr and RP advances ~₹140 cr [§1, §4].
- *Severity:* structural.
- *Innocent explanation:* WC-intensive growth — ruled out by the rising receivables/sales ratio above.
- *What would resolve it:* the receivables ageing table and evidence of post-year-end collection.
- *Cluster:* the CARO bank-returns-vs-books disagreement (F3) points at the *same* receivables line.

**F3 — CARO: books disagree with what lenders were told; plus default and arrears.**
- *What it shows:* quarterly returns to banks overstated receivables vs the books by ~₹60 cr in three of four quarters; ₹95 cr term-loan default (120 days); ₹22 cr undisputed statutory dues unpaid >6 months; evergreening of related-party loans [§3].
- *Severity:* structural. An auditor-attested reconciliation failure between the books and the lender statements is among the most concrete red flags in any annual report.
- *Innocent explanation:* a timing/reconciliation error — but management only states it is "in the process of reconciling," and unpaid statutory dues are hard evidence of a cash squeeze (companies pay taxes last).
- *Cluster:* corroborates F2 (the receivables are questionable) and the going-concern note.

**F4 — Contingent liabilities exceed net worth; governance instability.**
- *What it shows:* contingent liabilities ₹420 cr (incl. a ₹300 cr guarantee for the promoter entity) vs net worth ₹350 cr; three CFOs in four years; mid-term auditor resignation citing information not made available; audit committee met twice; promoter is also Chairman/MD [§5, §7, §3].
- *Severity:* structural (governance).
- *What would resolve it:* it compounds rather than resolves the above — the guarantee ties the listed company's solvency to the same promoter entity that holds the unprovided advance.

## Quantified dependency

On a provisioned basis the group has not been profitable. Cumulative reported PAT for FY24–FY26 is ₹164 cr (48+55+61) [§1]; the **single ₹180 cr unprovided advance, if provided as the auditor implies, more than erases it** [§2]. That is before any provision against the ₹210 cr of >365-day receivables carried at a ₹9 cr allowance [§2], or the ~₹24 cr margin differential on ₹300 cr of related-party sales booked at 2% vs ~10% third-party [computed, §4]. Reported profit does not survive contact with the disclosed adjustments; no valuation should be built on it.

## Gates raised

- Qualified audit opinion → **cap 4.0** (checked, confirmed present).
- 5y cumulative CFO/PAT < 0.5 → **cap 4.0** (checked, −0.69).
- Related-party tunnelling indicators → **cap 4.5** (checked, present).
- Promoter pledge > 50% → **cap 4.0** (checked, 71%).
- Going-concern material uncertainty → structural (checked, present).

Multiple independent gates fire; the verdict is **D**, not a low numeric score, because valuation is moot until integrity is resolved.

## What was not verified

Filings-extract-only pass. Not verified: recoverability of the ₹180 cr advance (needs Kesar Estates' accounts); existence/encumbrance of the ₹210 cr cash (needs bank confirmations and the charge registry); the receivables ageing beyond the ₹210 cr >365-day figure; whether prior years were silently restated; management's own account (concall). None of these is needed to reach verdict D — the qualified opinion and going-concern uncertainty are decisive from the documents in hand — but each would sharpen the picture and none should be assumed clean.

---
*This is analysis of publicly disclosed information, not an allegation of wrongdoing and not licensed financial advice. Findings describe what the disclosure does and does not explain; they are not conclusions of fraud. (Fictional worked example — company and figures invented.)*
