---
title: "/cs-rfp-respond — Slash Command for AI Coding Agents"
description: "Structured RFP/RFI/RFQ response with win-theme injection and proof-point matrix. NOT free-form proposal authoring (that's. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-rfp-respond

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/commercial/commands/cs-rfp-respond.md">Source</a></span>
</div>


Run the `rfp-responder` skill on this input:

**$ARGUMENTS**

## Three-tool workflow

1. **`rfp_parser.py`** — Extracts sections + requirements + scoring criteria from RFP text. Tags each requirement: MANDATORY / WEIGHTED / NICE-TO-HAVE. Surfaces scoring weight if disclosed.

2. **`response_drafter.py`** — Proof-point matrix per requirement (case studies, certs, customer quotes, technical attestations). Refuses to invent claims — requires either a verifiable source or an explicit "GAP" label. Win-theme injection per Shipley methodology.

3. **`winrate_predictor.py`** — Shipley-derived winrate estimate from: incumbent advantage, requirement-fit %, relationship strength with buyer, decision-criteria alignment, late-entry penalty.

## Hard rule

**Every proof point must have a verifiable source.** No invented claims. GAP labels surface explicitly so leadership decides whether to address or no-bid.

## Distinct from

- `business-growth/contract-and-proposal-writer` — **free-form** proposal authoring (your-narrative-driven). RFP-responder handles **structured** response where the buyer dictates the format and the questions.
- `c-level-advisor/general-counsel-advisor` — contract redline. RFP-responder is the response **before** the contract.
- `marketing-skill/*` — external marketing assets (web, ads, content). RFP-responder is a sales-enablement artifact tied to one buyer.
