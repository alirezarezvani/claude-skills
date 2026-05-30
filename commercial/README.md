# commercial

**Per-deal-and-packaging Commercial skills: pricing, deal desk, partnerships, channel economics, policy, RFP, forecast.**

v2.8.0 — 8 skills (orchestrator + 7 sub-skills), 21 stdlib Python tools, 28 references citing 7+ authoritative sources each.

## Skills

| Skill | Job-to-be-done |
|---|---|
| [`commercial-skills`](skills/commercial-skills/) | Orchestrator — routes via `context: fork` + Matt Pocock grill discipline |
| [`pricing-strategist`](skills/pricing-strategist/) | "What pricing model fits us, and what's the WTP range?" — model picker + Van Westendorp + packaging |
| [`deal-desk`](skills/deal-desk/) | "Should we approve this discount, and what's the redline?" — score + route + redline |
| [`partnerships-architect`](skills/partnerships-architect/) | "What tier is this partner, and what should the revshare be?" — 5-tier + joint GTM + revshare |
| [`channel-economics`](skills/channel-economics/) | "Is partner-led actually profitable after full-load cost-to-serve?" — mix + CTS + ROI |
| [`commercial-policy`](skills/commercial-policy/) | "What does our discount matrix and exception flow look like?" — matrix + exception + linter |
| [`rfp-responder`](skills/rfp-responder/) | "Should we bid this RFP, and with what win-themes + proof points?" — Shipley method + winrate predictor |
| [`commercial-forecaster`](skills/commercial-forecaster/) | "What's our quarter commit, and what assumption is it resting on?" — 4Q-weighted + cohort + confidence |

## Commands

- `/cs:commercial <inquiry>` — top-level router
- `/cs:grill-commercial <plan>` — Matt Pocock-style grilling against SaaS pricing canon
- `/cs:pricing-strategy`, `/cs:deal-review`, `/cs:partner-tier`, `/cs:channel-econ`, `/cs:commercial-policy`, `/cs:rfp-respond`, `/cs:commercial-forecast` — direct per-skill invocation

## Agent

- `cs-commercial-orchestrator` — margin-protective Commercial lead

## Distinct from

- `business-growth/sales-engineer` — technical sale (demos, POCs)
- `business-growth/revenue-operations` — process (lead routing, SDR motion)
- `business-growth/contract-and-proposal-writer` — free-form authoring; rfp-responder is structured response
- `c-level-advisor/cro-advisor` — strategic CRO ("when do we hire VP Sales?"), not tactical per-deal/per-policy
- `c-level-advisor/cfo-advisor` — strategic financial planning; commercial-forecaster is tactical quarterly pipeline
- `finance/financial-analysis` — close + report (backward); commercial-forecaster is forward

## License

MIT
