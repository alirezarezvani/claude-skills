---
name: "cs-grants"
description: "/cs:grants <research-idea> — NIH funding intelligence. 6-Q grill-me intake (idea + career stage + prelim + environment + posture + institutes) → 5-facet Consensus positioning + RePORTER POST institute mapping + NOSI fetches → 9-section .docx with mandatory program officer recommendation."
---

# /cs:grants — NIH Funding Intelligence

**Command:** `/cs:grants <research-idea>`

The `cs-grants` persona produces a strategic NIH funding overview as an editable `.docx` for clinical researchers.

## When to Run

- Scoping NIH funding for a new research idea
- Preparing for an R01 / R21 / K-award submission
- Identifying institute targets + study sections
- Generating draft Significance/Innovation language

## NIH-Only Scope

Non-NIH funders (PCORI, DOD CDMRP, VA, foundations) are **out of scope** — surfaced and flagged at intake. Use a different skill or manual search for those.

## Forcing Intake (6 Questions, One at a Time)

| Q | Asks | Notes |
|---|---|---|
| Q1 | Research idea (2-3 sentences) | refuses vague; "AI for healthcare" gets pushed back |
| Q2 | Career stage: pre-doc / postdoc / early career / independent / senior | forcing choice |
| Q3 | Preliminary data: none / pilot / strong / validated | forcing choice |
| Q4 | Environment: R01-eligible / mid-tier / resource-constrained / industry-collab | forcing choice |
| Q5 | Submission posture: new / resubmission / exploring | forcing choice |
| Q6 | Known institute targets, or "no preference — find the right ones" | accept either |

Stop condition: after Q6, commit and start Phase 2A. Never re-open intake.

## What You Get

After all 6 Qs + Phase 2A (Consensus) + Phase 2B (RePORTER) + NOSI discovery + Phase 3 DOCX:

```
grants_<topic-slug>_<YYYY-MM-DD>.docx

9 sections:
1. Executive Summary (career stage, environment, 3-4 key findings)
2. Research Positioning (3-5 gap quotes + draft Significance/Innovation)
3. Target Institutes (ranking table + interpretation)
4. Grant Opportunities (NOSI callout if any + top-3 FOAs)
5. Funded Overlap (top-5 projects + differentiation)
6. Study Sections (ranking + best-match)
7. Strategic Recommendations & Next Steps (3-4 recs + program officer + timeline)
8. References (numbered, hyperlinked to Consensus)
9. Audit Log (Consensus + RePORTER + NOSI tables + counts + plan tier)
```

## Critical Tool Constraints

- **Consensus**: 1 q/sec sequential. Plan-tier detected from "Found N, showing top M" patterns.
- **RePORTER**: **POST-only**. Use `bash_tool` + `curl`. NEVER `web_fetch` (GET-only — will fail silently).
- **NOSI fetch**: `web_fetch` for `NOT-*` URLs. If fetch fails, log `[NOSI {number} — fetch failed]` and continue.

## Discipline (Research-Pack Convention)

- **One intake Q per turn.** Never bundle.
- **Sequential Consensus.** 1 q/sec.
- **RePORTER POST.** `bash_tool` + `curl`. Not `web_fetch`.
- **Source discipline.** Cite only session results.
- **Three-count tracking.** Sent / shown / cited (Consensus) + projects / cited (RePORTER).
- **Plan-tier detect at first Consensus call.** Surface in audit.
- **Dynamic FY window.** Compute at runtime; never hardcode years.
- **Scope-aware mechanisms.** Career stage + scope + prelim, not stage alone.
- **Mandatory program officer rec.** Single most valuable advice.

## Mechanism Reference (Embedded)

| Mechanism | Career stage | Scope | Prelim needed | Budget (typical) |
|---|---|---|---|---|
| F31, F32 | Trainee | Solo training | None–pilot | $40-50k/yr × 2-3 yr |
| T32 | Inst. training grants | Pre-doc/postdoc | Institutional | Varies |
| R03 | Independent | Small/pilot | None–pilot | $50k/yr × 2 yr |
| R21 | Independent | Pilot/exploratory | None–pilot | $275k DC × 2 yr |
| K-series | Early career | Career dev. | Pilot | $100-180k × 5 yr |
| K99/R00 | Postdoc → ind. | Transition | Strong | $90k + $250k × 3 yr |
| R01 | Independent | Hypothesis-driven | Strong | $250-499k × 4-5 yr |
| R35 | Senior PI | Program | Validated | $750k × 5-8 yr |
| U01 | Multi-site | Cooperative | Strong–validated | Varies; usually >$500k |
| P01/P30 | Senior | Program | Validated | Multi-PI; >$1M/yr |

## Submission Timeline (Embedded)

| Mechanism | Standard receipt dates |
|---|---|
| R01, R21, R03 | Feb 5, Jun 5, Oct 5 |
| K awards (K01, K08, K23, K99) | Feb 12, Jun 12, Oct 12 |
| R34, R61/R33 | Feb 16, Jun 16, Oct 16 |
| F31, F32 | Apr 8, Aug 8, Dec 8 |

## Trigger Phrases

- "grants for [topic]"
- "find grants for my research idea"
- "what grants match my research"
- "help me find NIH funding"
- "grant opportunities for my research"
- "NIH funding for [topic]"

## Anti-Patterns Rejected

- Parallelizing Consensus calls
- Using `web_fetch` for RePORTER (POST-only)
- Hardcoded fiscal year values
- Mechanism recommendations on career stage alone
- Silently filling thin facets with training knowledge
- Skipping audit log
- Skipping program officer recommendation
- Conflating "found" / "shown" / "cited"
- Fabricating NOSI details when fetch fails

## Related

- Agent: [`cs-grants`](../agents/cs-grants.md)
- Skill: [`grants`](../skills/grants/SKILL.md)
- Source spec: [`megaprompts/08-grants-megaprompt.md`](../../../megaprompts/08-grants-megaprompt.md)
- Sibling: `/cs:litreview` (academic literature, no RePORTER)

---

**Version:** 1.0.0
**Source:** Path-B direct conversion of `megaprompts/08-grants-megaprompt.md`
