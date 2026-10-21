# Question Bank (LP perspective)

The questions an LP should put to a GP before committing capital — each paired
with what a **good answer** sounds like and, more importantly, what a **bad
answer** sounds like. The bad-answer signals are this file's reason to exist:
plenty of tools tell you what to ask; the differentiator is naming the specific
evasion so an LP can recognize it in real time.

## How to read this file

- **Priority is must-ask or nice-to-ask.** A **must-ask** is one where a bad
  answer is, on its own, a reason to pass or to hard-condition the commitment.
  A **nice-to-ask** sharpens the picture but rarely decides the outcome alone.
  Apply judgment: a nice-to-ask escalates to must-ask when the matching flag
  from `03` has already fired.
- **The bad-answer signal is the product.** A vague "they were evasive" is not
  useful. Each bad-answer cell names the *specific* dodge for that question —
  the redirect, the substituted metric, the silence — so the evasion is
  identifiable, not just felt.
- **Cross-references point into `03-red-flag-library.md`.** Most questions are
  the full-length version of a flag's one-line "Response"; the flag ID is cited. Ask the question
  *because* the flag fired; treat a bad answer as the flag confirmed.
- **Conditional questions are marked.** Some questions only apply to a deal type
  or a cycle position (HML/credit debt funds, post-2020 office). They are
  labeled so the skill asks them only when relevant.
- **No invented thresholds.** Numeric triggers (pref <6%, promote >30%,
  exit-dependent IRR >60%) come from `02`/`03` or a committed analyst rule;
  otherwise the question defers to the deal's own underwriting.

## Contents

1. [Deal-specific](#deal-specific) — `Q-DS-01`–`Q-DS-03`
2. [GP / sponsor-specific](#gp--sponsor-specific) — `Q-GP-01`–`Q-GP-04`
3. [Market-specific](#market-specific) — `Q-MKT-01`–`Q-MKT-02`
4. [Fee / structure-specific](#fee--structure-specific) — `Q-FEE-01`–`Q-FEE-04`
5. [Risk-specific](#risk-specific) — `Q-RISK-01`–`Q-RISK-06`
6. [Exit-specific](#exit-specific) — `Q-EXIT-01`–`Q-EXIT-02`
7. [Distribution timing](#distribution-timing) — `Q-DIST-01`–`Q-DIST-02`
8. [LP liquidity / secondary market](#lp-liquidity--secondary-market) — `Q-LIQ-01`–`Q-LIQ-02`

25 questions across 8 categories. Cross-references span 28 distinct flag IDs
from `03-red-flag-library.md`.

---

## Deal-specific

Questions that interrogate where the return actually comes from — the core of
distinguishing an asset story from a financing story.

| ID | Question | Priority | Good-answer signals | Bad-answer signals | 03 ref |
|---|---|---|---|---|---|
| Q-DS-01 | "What share of projected LP IRR comes from in-place cash flow versus the exit, and what's the IRR at a flat exit cap?" | Must-ask | A specific split; most return from in-place cash flow; the deal still clears the pref at a flat exit cap. | Can't or won't decompose the IRR; pivots to "real estate always appreciates"; the IRR collapses below pref at a flat exit cap. | GEN-08, EQUITY-06 |
| Q-DS-02 | "Strip out leverage and cap-rate compression — what is the unlevered, in-place return?" | Must-ask | Provides an unlevered number; the operational return stands on its own before financing. | Treats the levered IRR as the only relevant figure; no unlevered view exists; "leverage is just how the deal works." | GEN-07 |
| Q-DS-03 | "What is the return under a bear case — flat rents, higher exit cap, no refinance?" | Must-ask | A real downside scenario with the three swing assumptions stressed; LP capital survives it. | A single-point pro forma with no downside; "we underwrite conservatively" with nothing to show; the bear case is still a gain. | GEN-13 |

**Notes.** Q-DS-01 and Q-DS-02 are the same question from two sides; ask both,
because a GP can answer one plausibly and still fail the other. A deal that fails
all three is a financing story (GEN-07) regardless of how the headline IRR reads.

---

## GP / sponsor-specific

Alignment, conduct, and the honesty of the track record. These apply to every
deal type, debt or equity.

| ID | Question | Priority | Good-answer signals | Bad-answer signals | 03 ref |
|---|---|---|---|---|---|
| Q-GP-01 | "How much of your own capital is in this deal, on the same terms as LPs?" | Must-ask | A meaningful dollar amount on pari-passu terms; co-invest scales with deal size across the GP's deals. | "Our sweat equity is our investment"; co-invest is a fee waiver, not cash; token amount on better terms than LPs. | GEN-01 |
| Q-GP-02 | "Can you restate your track record as net-to-LP IRR on fully-realized, exited deals only?" | Must-ask | Produces realized, net-to-LP figures; acknowledges losers; distinguishes realized from marked. | Offers only project-level or GP-level IRR; "most deals are still performing"; can't separate realized from unrealized. | GEN-05, GEN-14 |
| Q-GP-03 | "Have you or your principals faced any regulatory action, enforcement, or investor litigation?" | Must-ask | A direct yes/no; if yes, full context and resolution offered unprompted. | Deflects to "nothing material"; blames the LP/regulator; a search surfaces something they didn't disclose. | GEN-02 |
| Q-GP-04 | "How have your headcount and deal-monitoring capacity grown alongside AUM?" | Nice-to-ask | Team scaled with capital; named people own asset management; monitoring cadence described. | AUM multiplied while the team stayed flat; "we're lean and efficient" as the whole answer; no named asset manager. | GEN-04 |

**Notes.** Q-GP-02 is the single highest-yield question in the bank. A GP that
cites only unrealized marks (GEN-14) *and* only project-level IRR (GEN-05) has
given no validated LP-outcome data at all — that pairing is a RED cluster, not
two soft answers. Escalate Q-GP-04 to must-ask whenever GEN-04 has fired.

---

## Market-specific

Whether the deal's market assumptions are grounded or asserted. The second
question fires only for assets `01-asset-class-norms.md` marks *variable*.

| ID | Question | Priority | Good-answer signals | Bad-answer signals | 03 ref |
|---|---|---|---|---|---|
| Q-MKT-01 | "What submarket supply pipeline and absorption data support the rent-growth assumption?" | Must-ask | Cites submarket-level supply and absorption; rent growth tied to data, not the metro headline. | Metro-level optimism standing in for submarket data; "rents always go up here"; no supply pipeline acknowledged. | GEN-18 |
| Q-MKT-02 *(office / variable assets)* | "How does the underwriting reflect post-2020 physical occupancy and sublease overhang in this submarket?" | Must-ask *(if applicable)* | Uses physical (not leased) occupancy; acknowledges the structural reset and sublease shadow supply. | Leans on a pre-2020 baseline; quotes leased occupancy only; treats WFH as fully reversed. | GEN-19 |

**Notes.** Q-MKT-02 applies to any asset class `01` marks *variable* (office,
experiential retail, regulatory-exposed STR), not office alone. Pair Q-MKT-01
with GEN-13 (no downside case): a cycle-exposed market plus a single-point pro
forma is sharper than either flag alone.

---

## Fee / structure-specific

The fee stack, the waterfall, and the preferred return — what the LP pays and
what protects the LP before the GP earns promote. Thresholds here come from
`02-fee-stack-library.md`.

| ID | Question | Priority | Good-answer signals | Bad-answer signals | 03 ref |
|---|---|---|---|---|---|
| Q-FEE-01 | "Can you provide the complete fee schedule and the full distribution waterfall?" | Must-ask | A full written schedule and waterfall; gross-to-net drag is computable from it. | "Standard market fees"; partial list; "the PPM has it" without producing it; fees surface only after commitment. | GEN-16 |
| Q-FEE-02 | "Which service providers are GP-affiliated, what do they charge, and are those rates third-party-benchmarked?" | Must-ask | Names affiliated entities, discloses their fees, benchmarks them to market or discounts them. | "All arm's-length" without naming providers; affiliate fees undisclosed; no benchmark offered. | GEN-06 |
| Q-FEE-03 | "Is the waterfall deal-by-deal or whole-of-fund, and is there a clawback?" | Must-ask | Whole-of-fund, or deal-by-deal *with* a secured/escrowed clawback; mechanism explained plainly. | Deal-by-deal with high promote and no clawback; can't explain the catch-up; "you get paid when we get paid." | EQUITY-01, EQUITY-02 |
| Q-FEE-04 | "What preferred return do LPs receive before the GP earns promote, and is it cumulative and compounding?" | Must-ask | A pref at or above market for the asset class, cumulative, carrying forward and compounding unpaid amounts. | Pref below 6% or absent; non-cumulative; promote sits above a preferred-equity pref (turning it into common risk). | EQUITY-04, EQUITY-05, PREF-01 |

**Notes.** Q-FEE-02 catches what the fee inventory in `02` can miss: each
affiliate fee can sit in-range while the *aggregation through related parties*
is the problem. The test is disclosure and benchmarking, not the existence of an
affiliate. Q-FEE-03's deal-by-deal structure is only RED when paired with a high
promote and no clawback — ask all three parts.

---

## Risk-specific

The debt, the financials, and — for debt funds — the loan book. Where the
return story meets the things that can break it. The last three questions are
debt-fund-conditional.

| ID | Question | Priority | Good-answer signals | Bad-answer signals | 03 ref |
|---|---|---|---|---|---|
| Q-RISK-01 | "When does the debt mature relative to the projected hold, and what's the refinance or extension plan?" | Must-ask | Debt matures at or after the planned exit; extension options or a refi-independent path exist. | Maturity falls inside the hold; "we'll refinance" with no terms; no plan if the refi market is shut. | GEN-09 |
| Q-RISK-02 | "When does the rate cap expire relative to debt maturity, and what's the cost to extend it at current pricing?" | Must-ask | Cap covers the full hold or has a budgeted extension; current replacement cost is known. | Cap expires before maturity; extension cost not modeled; "rates should be lower by then." | GEN-10 |
| Q-RISK-03 | "Can you provide trailing-twelve-month actuals, the rent roll, and complete debt terms?" | Must-ask | Full T-12, current rent roll, and all debt terms provided without friction. | T-3/T-6 only; rent roll withheld; "the financials are confidential until you commit." | GEN-12, GEN-15 |
| Q-RISK-04 *(HML / bridge fund)* | "What is the average portfolio LTV on as-is value, not just ARV?" | Must-ask *(if applicable)* | Reports LTV on as-is value; a real equity cushion exists if the renovation thesis fails. | Quotes only LTV-on-ARV; can't produce as-is LTV; "our borrowers always complete." | HML-01 |
| Q-RISK-05 *(HML / credit fund)* | "What is your historical default rate and realized recovery rate, including through 2020 and 2022–23?" | Must-ask *(if applicable)* | Discloses both default and recovery with workout timelines, across stress periods. | Default rate without recovery (or vice versa); "we've never had a loss"; silence on 2022–23. | HML-03, HML-04 |
| Q-RISK-06 *(credit fund)* | "What is the fund's leverage ratio, and is the quoted LP IRR levered or unlevered?" | Must-ask *(if applicable)* | States fund-level leverage; clarifies the IRR is levered and shows the unlevered figure. | Won't disclose leverage; presents a levered IRR as if unlevered; "leverage is conservative" with no number. | CREDIT-01 |

**Notes.** Q-RISK-02 targets the specific 2022–24 failure mode behind many
multifamily-syndication capital calls — the cap's *expiry date*, not the rate
itself, is the trigger, so it's distinct from generic floating-rate exposure.
Q-RISK-05's two halves travel together: a 2% default rate with 40% recovery is
worse than 5% default with 90% recovery, so a GP disclosing only one number has
told you nothing about realized loss.

---

## Exit-specific

The terminal assumptions that drive the headline IRR — the exit cap and the
refinance the plan may depend on.

| ID | Question | Priority | Good-answer signals | Bad-answer signals | 03 ref |
|---|---|---|---|---|---|
| Q-EXIT-01 | "Why is the exit cap below the going-in cap, and what's the IRR at an exit cap equal to or above going-in?" | Must-ask | Exit cap equals or exceeds going-in (no baked-in compression), or compression is justified by a specific, defensible thesis. | Exit cap below going-in with "cap rates will compress"; the IRR breaks at a flat exit cap; no sensitivity offered. | EQUITY-06 |
| Q-EXIT-02 | "Does the business plan depend on a refinance, and what happens to distributions if the refi isn't available on the assumed terms?" | Must-ask | Capital return doesn't hinge on a refi; if it does, a credible fallback exists. | Distributions or capital return require a refi at lower rates; no fallback; "the refi market will reopen." | EQUITY-07 |

**Notes.** Q-EXIT-01 connects directly to Q-DS-01: an aggressive exit cap is the
usual mechanism behind exit-dependent IRR. If both fire, the verdict should name
the deal a financing story explicitly.

---

## Distribution timing

When LP capital actually comes back — the J-curve question that two deals with
identical headline IRRs can answer very differently. (Design-review addition,
2026-06-01.)

| ID | Question | Priority | Good-answer signals | Bad-answer signals | 03 ref |
|---|---|---|---|---|---|
| Q-DIST-01 | "What is the projected distribution schedule, and at what milestones does LP capital start returning?" | Must-ask | A specific schedule tied to operational triggers; clear on when distributions begin and what gates them. | "We'll distribute when the deal supports it" with no milestones; an IRR quoted with no distribution timing; silence. | GEN-11 |
| Q-DIST-02 | "When are capital calls expected, and what's the consequence of a missed or late call?" | Nice-to-ask | A defined call schedule; the dilution/penalty mechanics are stated and reasonable. | "Calls as needed" with no notice period; punitive dilution buried in the docs; can't describe the mechanics. | — |

**Notes.** Q-DIST-01 is why two deals with the same IRR are not equivalent: a
back-loaded deal concentrates all return risk at the exit (GEN-11). Q-DIST-02
has no `03` flag because it concerns the LP's own cash-management decision, not a
deal defect — but a punitive missed-call provision is a real LP exposure.

---

## LP liquidity / secondary market

The LP's own exit and tax mechanics — questions about the investor's position,
not the asset. (Q-LIQ-01 is a design-review addition, 2026-06-01.)

| ID | Question | Priority | Good-answer signals | Bad-answer signals | 03 ref |
|---|---|---|---|---|---|
| Q-LIQ-01 | "What are my options if I need to exit before the hold period ends?" | Must-ask | Names a secondary platform or process, a realistic liquidity timeline, and is honest that there may be none. | "A secondary market may develop"; "we'll try to accommodate"; silence — i.e. illiquid with the lock-up undisclosed. | — |
| Q-LIQ-02 | "When will K-1s be delivered each year, and have you historically delivered them before the filing deadline?" | Nice-to-ask | A committed delivery window with a track record of meeting it. | "As soon as we can"; a history of extensions forcing LPs to file late; no answer. | — |

**Notes.** This category has no `03` cross-references by design — these are
LP-decision questions, not deal-defect flags. They belong here precisely because
`03` is scoped to the deal's risks while the LP's own liquidity and tax timing
are equally part of the commit-or-pass decision (see `01-asset-class-norms.md`
on lock-up by asset class). An honest "there is no liquidity" is a *good* answer;
a vague promise of liquidity that doesn't exist is the bad one.

---

## Provenance

The shared sources in `01-asset-class-norms.md` → Provenance (ILPA
due-diligence and alignment standards; Preqin / NCREIF realized-vs-marketed
dispersion, why net-to-LP realized figures (Q-GP-02) are the only validated
track record), plus:

- **SEC enforcement patterns.** The fact patterns that make Q-GP-02 and Q-GP-03
  high-yield — undisclosed affiliate fees, unrealized marks as returns,
  misleading track-record IRRs.
- **Post-2022 distress case studies.** The rate-cap-expiry / frozen-refi
  failures of 2022–24 — the source for Q-RISK-01, Q-RISK-02, and Q-EXIT-02 as a
  connected line of questioning.

*Last reviewed: 2026-06-03. Questions and bad-answer signals derive from the
flags in `03-red-flag-library.md`; when a flag's ID or threshold changes, update
the matching question's cross-reference here. New questions append to the
relevant category and take the next ID in their `Q-<CAT>-NN` sequence so
SKILL.md references stay stable.*
