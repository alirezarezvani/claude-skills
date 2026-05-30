---
title: "/cs-commercial-policy — Slash Command for AI Coding Agents"
description: "Discount matrix designer + T&C library + exception policy. New ground — designs the policy that deal-desk applies per deal. Direct invocation of the. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-commercial-policy

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/commercial/commands/cs-commercial-policy.md">Source</a></span>
</div>


Run the `commercial-policy` skill on this input:

**$ARGUMENTS**

## Three-tool workflow

1. **`discount_matrix_builder.py`** — Data-backed discount bands (by ARR band × term length × payment terms × strategic value). Outputs the matrix + the approver tier per cell. Industry tuning `--profile {saas,enterprise-software,api,marketplace,services}`.

2. **`exception_router.py`** — Exception flow: when a deal asks for terms outside the matrix, who approves and what compensating commitments are required (multi-year + prepay + named expansion path).

3. **`policy_linter.py`** — Consistency check across the matrix: no contradictions (e.g., "Manager approves up to 25%" but "VP approves up to 20%"), no gaps (deal band with no defined approver), no obvious gaming surface (cliff at 99 ARR vs 100 ARR).

## Hard rule

**No discount band without data backing.** Pull win-rate and NRR by current band before recommending changes.

## Distinct from

- Sibling `commercial/skills/deal-desk` — **applies** the policy to individual deals. Commercial-policy **designs** the policy.
- Sibling `commercial/skills/pricing-strategist` — sets the **pricing model + tier list price**. Commercial-policy governs **discounts off list**.
- `c-level-advisor/cro-advisor` — strategic
- `c-level-advisor/cfo-advisor` — financial guardrails (margin floor); commercial-policy operationalizes those
