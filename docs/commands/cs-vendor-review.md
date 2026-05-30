---
title: "/cs-vendor-review — Slash Command for AI Coding Agents"
description: "Score vendors on a multi-dimensional scorecard (reliability / support / security / commercial / strategic-fit), track SLA compliance, classify. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-vendor-review

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/business-operations/commands/cs-vendor-review.md">Source</a></span>
</div>


Run the `vendor-management` skill on this input:

**$ARGUMENTS**

## Three-tool workflow

1. **`vendor_scorer.py`** — Score each vendor 0-100 across 5 weighted dimensions: reliability, support, security, commercial, strategic-fit. Industry tuning via `--profile {saas,fintech,healthcare,enterprise}`. Verdict: KEEP / REVIEW / REPLACE.

2. **`sla_compliance_tracker.py`** — Compute compliance % per vendor, breach trend (improving/stable/degrading), credit-claim eligibility.

3. **`vendor_risk_classifier.py`** — Classify risk per Shared Assessments SIG-Lite framework: Critical/High/Medium/Low across 4 vectors (data sensitivity, financial exposure, operational dependency, regulatory exposure). Industry-tunable.

## Output

- Per-vendor scorecard (markdown)
- SLA compliance breakdown with credit-claim flags
- Risk matrix with mitigation actions per vector
- Top 3 vendors to REVIEW or REPLACE

## Distinct from

- `c-level-advisor/general-counsel-advisor` — that's contract law + redline. This is **operational vendor performance**.
- `business-growth/contract-and-proposal-writer` — that's external proposal authoring. This is **inbound vendor scoring**.
- Sibling `procurement-optimizer` — that's spend categorization + supplier rationalization. This is **vendor performance + risk**.
