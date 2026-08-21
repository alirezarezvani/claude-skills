# The challenge pass — adversarial review before you finalise

Use this when: a report has been drafted and before it is delivered. Mandatory in Deep dive mode, in Forensic mode before assigning a verdict, and in IPO mode before assessing the band. Recommended in Standard mode. Skip it in Screen mode — a screen's conclusion is explicitly provisional.

The problem this solves is structural, not one of effort. **You wrote the thesis, so you will not attack it as hard as someone else would.** A bear case written by the author of the bull case is systematically weaker: it tends to select risks that are already priced, already disclosed, or comfortably distant, and to avoid the one assumption the whole verdict is standing on. `references/17-process-and-epistemics.md` §17 names this — external challenge and echo chambers — but naming a bias does not remove it. This file makes the challenge a step with its own output.

**The test of a real challenge pass is that it can change the answer.** If it can only add caveats to a conclusion that was already written, it is theatre and is worse than nothing, because it manufactures false confidence. Build it so the verdict can move, and be willing to move it.

## Contents

- [How to run it: independent vs self-review](#how-to-run-it-independent-vs-self-review)
- [Stage C0 — Find the load-bearing claims](#stage-c0--find-the-load-bearing-claims)
- [Stage C1 — Attack them](#stage-c1--attack-them)
- [Stage C2 — Verify sources and arithmetic](#stage-c2--verify-sources-and-arithmetic)
- [Stage C3 — Attack the method, not just the numbers](#stage-c3--attack-the-method-not-just-the-numbers)
- [Stage C4 — The outside view](#stage-c4--the-outside-view)
- [Stage C5 — Hunt disconfirming evidence](#stage-c5--hunt-disconfirming-evidence)
- [Stage C6 — Disposition and verdict revision](#stage-c6--disposition-and-verdict-revision)
- [Anti-theatre requirements](#anti-theatre-requirements)
- [Output: the challenge log](#output-the-challenge-log)
- [Checklist](#checklist)

## What it costs, and when that is justified

A full independent challenge pass costs roughly as much as the original analysis again — measured in practice at around 200k tokens and 15–20 minutes per report when run with independent challengers and live source verification. Budget for it deliberately rather than firing it reflexively.

That cost is easily justified before committing real money to a position, and for a forensic verdict where being wrong is expensive in both directions. It is not justified for a quick screen, for a company you have already decided against, or for a conclusion nobody will act on. When budget is tight, run Stage C0 plus C1 on the single most load-bearing claim and say that is what you did — a targeted challenge of the one assumption carrying the verdict is worth far more than a shallow sweep of all of them.

## How to run it: independent vs self-review

**If you can spawn subagents, do.** Independence is the entire mechanism, and it is not simulated well by an author reviewing their own work. Give each challenger the report and the question, and — importantly — **do not give it your reasoning**. It should reach its own view from the evidence, then disagree or not.

Four lenses, run in parallel:

| Lens | Brief |
|---|---|
| **The skeptic** | Assume the verdict is wrong. Explain how that happened. What did the analyst want to believe? |
| **The auditor** | Ignore the argument entirely. Verify that every material figure traces to its cited source and that the numbers reconcile with each other |
| **The short-seller** | Build the strongest possible case against the position, using evidence from outside the company's own disclosure |
| **The methodologist** | Attack the peer set, the sector routing, the situation classification, the normalisation choices and the scorecard weights |

**If you cannot spawn subagents**, run the four lenses sequentially as separate passes, and re-read the report *cold* between each — do not carry your drafting context into the challenge. State in the output that this was self-review, because a reader should weight it accordingly.

## Stage C0 — Find the load-bearing claims

Most of a report is scaffolding. The verdict usually rests on two to four claims, and everything else could be wrong without changing the conclusion.

Write them out explicitly. For each, answer: **if this claim is false, does the verdict change?** If the answer is no, it is not load-bearing — set it aside and stop spending challenge effort on it.

Then rank by fragility: how confident is the claim, and how much weight is it carrying? **The most dangerous claim in any report is the one carrying the most weight with the least evidence** — typically a normalised margin, a mid-cycle assumption, a maintenance-capex estimate, a terminal growth rate, or a peer set the analyst chose.

## Stage C1 — Attack them

For each load-bearing claim, run these in order:

1. **Reverse the burden.** Do not ask "is this claim supported?" Ask "**assume it is false — what would the world look like, and does the evidence actually distinguish that world from this one?**" Frequently it does not, and the claim was an assumption wearing the clothes of a finding.
2. **Find the strongest counter-evidence**, not the most convenient. If the counter-evidence you cite is one you can easily dismiss, you have not tried.
3. **Check whether the claim is evidence or inference.** Apply the F/A/E/I tagging from §9 of `17-process-and-epistemics.md`. A verdict resting on chained inferences is far weaker than one resting on facts, and the chain multiplies: three inferences at 80% confidence give you roughly 50%.
4. **Test the single-input sensitivity.** Which one input, if wrong by a plausible margin, flips the verdict? State it explicitly. If a 200bps change in an assumed margin moves the conclusion from "attractive" to "expensive", the honest output is a range and a lower confidence tier, not a verdict.
5. **Check the claim against the report's own invalidation triggers.** Reports routinely list triggers that are *already partly met* at the time of writing. If one is, the verdict must account for it rather than list it as a future risk.

## Stage C2 — Verify sources and arithmetic

Adversarial in the plainest sense: assume the analyst was sloppy and try to prove it.

- **Trace a sample of material figures to the cited source.** Not all of them — the largest, the most load-bearing, and any that look surprisingly convenient. A figure that cannot be traced is downgraded to unverified, whatever it says.
- **Check internal consistency.** Do the margins implied by the absolute numbers match the stated margins? Does the growth rate match the endpoints? Do segment figures sum to the consolidated? Inconsistency is a finding in itself — and this test has already caught real errors.
- **Check period and basis consistency.** Consolidated compared against standalone, FY against CY, TTM against full-year, one company's FY26 against another's FY25. These errors are silent and common.
- **Check units and currency.** Crore vs million vs billion; reported vs converted figures.
- **Check the peer figures as hard as the subject's.** Peer data is usually sourced more casually than the target's, yet the whole sector-relative conclusion rests on it.

## Stage C3 — Attack the method, not just the numbers

The numbers can be right and the conclusion still wrong, because the framework was mis-selected.

- **Peer set.** Was it constructed to be comparable, or to flatter? Add the two most awkward comparables that were left out and see whether the percentile ranking survives.
- **Sector routing.** Was the right playbook applied? For a multi-segment group, was the dominant-profit segment correctly identified, and were the secondary segments' distortions on the consolidated numbers actually stated?
- **Situation classification.** Was a cyclical valued on peak earnings? A recent IPO valued on prospectus-year margins? A holdco valued on a consolidated multiple?
- **Normalisation.** Were one-offs adjusted **symmetrically** — or were the ones that hurt the thesis normalised away while the ones that helped were kept?
- **Scorecard weights and benchmarks.** Re-run the score under a different weight preset and, where peer data exists, on peer percentiles rather than shipped bands. **If the verdict flips between presets, the verdict is a function of the weights, not the company — and that must be said.**
- **Coverage.** What share of the metric set was actually populated? A confident composite built on 55% coverage is a confident guess.

## Stage C4 — The outside view

Bottom-up analysis is systematically optimistic because it reasons from a specific story rather than a reference class.

- **Base rates.** What proportion of companies sustain 25% growth for five years? What proportion of turnarounds in this sector actually turn? What happened to the last several roll-ups, capacity expansions or foreign acquisitions in this industry? If the report's forecast sits far outside the reference class, it needs a stated reason why this case is different — and "strong management" is not one.
- **Management's own record.** Compare past guidance to delivery. A management team that has missed its stated targets for three years is not a credible source for year-four guidance.
- **The cycle.** Is the analysis extrapolating a cyclical peak or trough? Where does the sector playbook say the cycle is?

## Stage C5 — Hunt disconfirming evidence

Actively search for what would contradict the thesis, rather than gathering more of what supports it. Specifically:

- Short reports, forensic research and adverse media — read as **primary documents to be evaluated**, attributed and verified, never adopted wholesale.
- Regulatory actions, litigation, tax disputes and enforcement history.
- Customer, supplier, employee and channel signals that contradict the reported trend.
- The competitor's disclosure. A rival's commentary on pricing, share and demand is a check on the subject's version of the same market — and rivals have no incentive to flatter.
- The bear case as stated by people who actually hold it, in their own terms.

## Stage C6 — Disposition and verdict revision

Every challenge gets one of four dispositions, and each has a consequence:

| Disposition | Meaning | Consequence |
|---|---|---|
| **UPHELD** | The challenge succeeded; the original claim does not survive | Revise the report. Change the verdict if the claim was load-bearing |
| **WEAKENED** | The claim survives but with less force or a wider range than stated | Widen the range, lower the confidence tier, or add the caveat into the body — not a footnote |
| **REJECTED** | The challenge was considered and does not hold | Log it with the reason. This is valuable: it shows the reader what was tested |
| **UNRESOLVED** | Cannot be settled with available evidence | Name the specific evidence needed. Carry it into the report's uncertainty section. **Never resolve an unresolved challenge in the thesis's favour by default** |

Then do the thing that makes this real: **if a load-bearing claim was upheld against, change the conclusion.** Say plainly in the report that the challenge pass altered the verdict and how. A visible revision is the strongest signal of a functioning process; an unchanged verdict after every challenge pass, report after report, is evidence the process is not working.

## Anti-theatre requirements

A challenge pass that always concludes "thesis holds" is worse than none. Three requirements guard against that:

1. **State what would have changed your mind**, specifically and in advance of looking. If you cannot articulate disconfirming evidence, you are not holding a falsifiable view.
2. **If nothing was refuted, say what you looked for and failed to find** — and note explicitly that failing to refute is not the same as confirming. Absence of a found problem is weak evidence when search was shallow.
3. **Name the most likely way this analysis is wrong**, even when you cannot refute it. Every analysis has one. An author who cannot name theirs has not looked.

## Output: the challenge log

Append to the report, or deliver alongside it:

```markdown
## Challenge pass
Method: <independent challengers (N lenses) | sequential self-review>
Load-bearing claims identified: <list>

| # | Claim challenged | Attack | Disposition | Consequence |
|---|---|---|---|---|
| 1 | | | UPHELD/WEAKENED/REJECTED/UNRESOLVED | |

**Single-input sensitivity:** the verdict turns most on <input>. A change of <magnitude> flips it to <alternative>.
**Verdict change:** <none | changed from X to Y because ...>
**What would have changed my mind:** <stated>
**Most likely way this analysis is wrong:** <stated>
**Searched but not found:** <what disconfirming evidence was sought and not located>
```

## Checklist

- [ ] Load-bearing claims identified explicitly; non-load-bearing material set aside.
- [ ] Most fragile claim named — highest weight, weakest evidence.
- [ ] Burden reversed on each load-bearing claim, not merely re-checked.
- [ ] F/A/E/I applied; inference chains and their compounded confidence noted.
- [ ] Single-input sensitivity stated: which input flips the verdict, and by how much.
- [ ] Report's own invalidation triggers checked for ones already partly met.
- [ ] Sample of material figures traced to cited sources; untraceable ones downgraded.
- [ ] Internal consistency, period/basis, units and currency checked.
- [ ] Peer figures checked as hard as the subject's.
- [ ] Peer set stress-tested by adding the awkward comparables that were omitted.
- [ ] Sector routing, situation classification and normalisation symmetry challenged.
- [ ] Score re-run under a different weight preset; verdict-flip noted if it occurs.
- [ ] Base rates and management's guidance-vs-delivery record applied.
- [ ] Disconfirming evidence actively sought, including competitor disclosure and short reports.
- [ ] Every challenge assigned a disposition; unresolved ones not defaulted in the thesis's favour.
- [ ] Verdict revised where a load-bearing challenge was upheld, and the revision stated openly.
- [ ] "What would have changed my mind", "most likely way this is wrong", and "searched but not found" all present.
