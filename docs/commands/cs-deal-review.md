---
title: "/cs-deal-review — Slash Command for AI Coding Agents"
description: "Per-deal review. Score margin + risk, route discount approval to the right human, redline T&Cs against commercial policy. Never auto-approves. Direct. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-deal-review

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/commercial/commands/cs-deal-review.md">Source</a></span>
</div>


Run the `deal-desk` skill on this input:

**$ARGUMENTS**

## Three-tool workflow

1. **`deal_scorer.py`** — Score deal 0-100 across 5 dimensions: margin (gross margin after discount), risk (payment terms + redline count), strategic value (logo / reference / expansion), commercial fit (within policy band), term shape (multi-year vs annual). Industry tuning via `--profile`. Verdict: APPROVE / REVIEW / ESCALATE / DECLINE + **named human approver**.

2. **`discount_approval_router.py`** — Route discount to the right approver tier (defaults: 0-15% AE, 15-25% Manager, 25-35% Director, 35-50% VP, 50%+ CFO/CRO). Outputs approval chain with the deal's hop points highlighted + estimated approval cycle days.

3. **`terms_redliner.py`** — Detect 10+ founder/seller-killer patterns: uncapped indemnity, missing DPA when EU data involved, MFN pricing, auto-renew without notification, perpetual license-back, exclusivity without compensation. Output: ranked redline list with severity + standard counter + named legal approver.

## Output

- Deal scorecard with per-dimension breakdown + verdict
- Discount approval chain (named humans)
- Redline list with severity + counter language
- Top 3 next actions

## Hard rule

**This skill never says "approved".** It always outputs a recommendation + named human approver.

## Distinct from

- `cs-pricing-strategy` — that **sets the pricing model**. This handles **per-deal** decisions.
- `business-growth/contract-and-proposal-writer` — that's **authoring**. This is **approval gate**.
- `commercial-policy` (sibling) — that **designs the policy**. This **applies it per deal**.
- `c-level-advisor/general-counsel-advisor` — that's **legal redline at deeper level**. This is **commercial redline against policy**.
