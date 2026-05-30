# Commercial — Domain Guide

This file provides domain-specific guidance for skills in `commercial/`.

## Purpose

The Commercial domain ships skills that help **deal-desk operators, pricing teams, partner managers, RFP responders, and commercial forecasters** make per-deal and packaging decisions. This is **not strategy** (`c-level-advisor/cro-advisor`), **not sales execution** (`business-growth/sales-engineer`), and **not financial close** (`finance/financial-analysis`).

## Skills (v2.8.0 complete)

| Skill | Purpose | `context: fork`? |
|---|---|---|
| `commercial-skills` | Domain orchestrator — routes to 7 sub-skills | YES |
| `pricing-strategist` | Pricing model picker + Van Westendorp WTP + packaging | NO |
| `deal-desk` | Per-deal scorer + discount approval routing + redline | NO |
| `partnerships-architect` | 5-tier classifier + joint GTM + revshare modeler | NO |
| `channel-economics` | Cost-to-serve + ROI + channel mix optimizer | NO |
| `commercial-policy` | Data-backed discount matrix + exception flow + policy linter | NO |
| `rfp-responder` | Shipley-method structured RFP/RFI/RFQ response | YES |
| `commercial-forecaster` | 4Q-weighted bookings + cohort NRR/GRR + funnel-confidence | NO |

## Hard rules (domain-specific)

1. **Pricing outputs: model + range, never a specific number.** The human picks the number.
2. **Deal outputs: score + named human approver. Never auto-approve.** Even at 0% discount.
3. **Forecast outputs: surface the conversion assumption explicitly.** Pipeline math without disclosed assumptions is theatre.
4. **RFP responses: never invent claims for GAP requirements.** Surface the gap; leadership decides bid/no-bid.
5. **Partnership tiers: insist on independent-demand evidence for STRATEGIC.** Forrester: channel-led deals from your own pipeline cost more than direct.
6. **Channel ROI requires retention differential.** CAC alone is meaningless without channel-level retention.
7. **Stdlib-only Python.** Deterministic logic, no LLM calls in scripts.
8. **Industry tuning** via `--profile {saas,api,enterprise-software,marketplace,services,hardware}` on every scoring tool.
9. **Matt Pocock grill discipline** — `/cs:grill-commercial` interrogates plan against SaaS pricing canon before any sub-skill runs.

## Build pattern

Path-B 11-file contract per skill. SKILL.md includes a "Forcing-question library" section that grills the user with cited canon (Skok, Tunguz, Bessemer, Ramanujam, ProfitWell, Winning by Design, Shipley, APMP).

## Agent + command pattern

- `cs-commercial-orchestrator` — margin-protective Commercial lead. Voice: "What's the margin at full discount, AND what does next quarter's pipeline look like at the same terms?"
- `/cs:commercial <inquiry>` — top-level router
- `/cs:grill-commercial <plan>` — Matt-style grilling first
- `/cs:pricing-strategy`, `/cs:deal-review`, `/cs:partner-tier`, `/cs:channel-econ`, `/cs:commercial-policy`, `/cs:rfp-respond`, `/cs:commercial-forecast` — direct per-skill invocation

## Anti-patterns (domain-level)

- ❌ Skills that overlap `business-growth/contract-and-proposal-writer` (prose authoring) — Commercial is **decision logic + structured response**
- ❌ Skills that overlap `c-level-advisor/cro-advisor` — that's strategic CRO judgment
- ❌ Skills that recommend a specific price — recommend model + range
- ❌ Skills that auto-approve deals — score + route to named human
- ❌ Forecasting tools that hide conversion assumptions
- ❌ RFP responder that invents claims — surface GAPs, leadership decides
- ❌ Partnership classifier that grants STRATEGIC tier without independent-demand evidence

## References

- Master plan: `documentation/implementation/bizops-commercial-expansion-plan.md`
- Matt Pocock derivation: `engineering/grill-with-docs`
- Strategic complement: `c-level-advisor/cro-advisor`
- Sales execution complement: `business-growth/sales-engineer`
