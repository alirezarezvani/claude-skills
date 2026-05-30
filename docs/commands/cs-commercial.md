---
title: "/cs-commercial — Slash Command for AI Coding Agents"
description: "Top-level Commercial router. Routes the inquiry to one of seven Commercial sub-skills (pricing, deal, partner, channel, policy, RFP, forecast) and. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-commercial

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/commercial/commands/cs-commercial.md">Source</a></span>
</div>


Use the `cs-commercial-orchestrator` agent + `commercial-skills` orchestrator skill to handle this inquiry:

**$ARGUMENTS**

## Routing protocol

1. Classify the inquiry against the seven Commercial lanes:
   - **PRICING** — pricing model, packaging, WTP, value pricing → `pricing-strategist`
   - **DEAL** — deal review, discount approval, redline, margin → `deal-desk`
   - **PARTNERSHIP** — partner tier, joint GTM, revshare → `partnerships-architect`
   - **CHANNEL_ECON** — channel mix, cost-to-serve, direct vs partner → `channel-economics`
   - **POLICY** — discount matrix, commercial policy, exception framework → `commercial-policy`
   - **RFP** — RFP/RFI/RFQ/security questionnaire → `rfp-responder`
   - **FORECAST** — bookings, ARR, NRR forward projection → `commercial-forecaster`

2. Top lane score ≥ 2 → invoke that sub-skill in forked context.

3. Single-signal or tie → one clarifying question.

4. After sub-skill runs, return ≤ 200-word digest.

## Output expectations

- What was analyzed
- Top 3 findings with severity
- Top 3 next actions with **named human approver** where applicable
- Artifact path
- Suggested chain

## Hard rules

- Pricing outputs: **model + range**, never a specific number.
- Deal outputs: **score + named approver routing**, never auto-approval.
- Forecast outputs: surface the **conversion assumption** explicitly.

## Anti-patterns

- ❌ Running all 7 sub-skills "to be thorough" — pick one, digest, chain
- ❌ Letting precedent set policy — flag policy-breaking deals for review
