---
name: "ai-decision-authority"
description: "Routes marketing and GTM decisions into three AI governance zones (AI-Primary, Collaborative, Human-Primary) by stakes and reversibility. Use when deciding which AI outputs need human review, whether an agent may act autonomously on a task, why AI adoption is collapsing under review requirements, or when auditing a list of workflows for safe autonomy. Triggers on 'should a human review this', 'can the agent just do this', 'AI governance policy', 'human in the loop'."
---

# AI Decision Authority

## Overview

Decide which AI outputs a human must approve, and which an agent can own outright.

Most AI governance in marketing fails in one of two directions. Review everything, and adoption collapses because using the tool is slower than doing the work by hand. Review nothing, and compliance exceptions accumulate quietly until one does not stay quiet, at which point legal arrives and you get the first failure anyway.

Both failures come from applying one rule to every decision. Generating forty subject lines for a test is not the same decision as approving a regulatory disclosure. This skill sorts them by stakes rather than by seniority, so governance sits where the consequences are.

Use it for a single decision, or to audit thirty workflows at once.

## Workflow

Ask three questions in this order. Order matters, because reversibility dominates.

**1. Can it be corrected if it is wrong?**
If this output is wrong, can it be quietly fixed, or has the damage already left the building? A content variant can be swapped in an hour. A regulatory filing cannot.

**2. Who sees it, and what follows?**
Internal only, or does it cross a legal, executive, or external boundary? Exposure is what pulls a decision up out of Zone 1.

**3. How often does it happen?**
A hundred times a week, or once a quarter? High-frequency standardised decisions are where a per-output human gate kills adoption. Low-frequency, high-consequence decisions absorb human ownership without becoming a bottleneck.

Then assign a zone and apply its rule.

### Zone 1: AI-Primary

Reversible, high-volume, internal only. Correctable at negligible cost.

Examples: first-pass copy drafts, internal research summaries, data categorisation, competitive analysis, test variants, segmentation queries, performance summaries.

**Rule:** the agent acts. Keep a log. Audit a periodic sample, never every output. No per-output gate.

Expect roughly 70% of decision volume here. If your Zone 1 is small, you have miscategorised and adoption will suffer.

### Zone 2: Collaborative

Reaches an external audience. Wrong output carries reputational or compliance cost. Human review adds real judgment rather than a rubber stamp.

Examples: customer-facing messaging, press releases, partner commitments, pricing communications, campaign briefs, external first drafts.

**Rule:** the agent drafts. A human approves before anything goes external. The agent does not hold the send permission.

### Zone 3: Human-Primary

Irreversible, novel, or legally exposed. A named person's career is attached to the outcome.

Examples: regulatory disclosures, M&A communications, executive positioning, legal filings, board materials, crisis response, pricing announcements.

**Rule:** the agent researches and drafts ranked options with transparent reasoning. A named human decides and executes.

Keep this zone small. A large Zone 3 is the review-everything failure wearing a different hat.

### Govern at the boundary, not the workflow

Most workflows span zones. "Agent drafts the weekly newsletter and schedules it" is Zone 1 drafting plus Zone 2 sending.

Govern the boundary. Let the drafting run free and gate the send. Governing the whole workflow at its highest zone is where most of the available adoption is lost.

## Output format

For one decision:

```
Decision: <restate it>
Reversibility: <answer>
Exposure: <answer>
Frequency: <answer>
-> Zone <n>: <name>
Rule: <the governance rule>
If misclassified: <what breaks one zone down / one zone up>
```

For a list, produce a table: Decision | Zone | Rule | Why.

Always name the misclassification cost. It is the part that changes behaviour.

## Anti-Patterns

**Do not gate every output.** The most common failure. It looks responsible and it collapses adoption, because practitioners route around any system slower than doing the work manually. Check usage numbers, not policy documents.

**Do not sort by seniority.** Zones are set by stakes and reversibility. A director's internal summary is Zone 1. A junior's regulatory claim is Zone 3.

**Do not let Zone 3 sprawl.** If more than a handful of decision types land there, they have been miscategorised out of fear rather than analysis.

**Do not govern a whole workflow at its highest zone.** Split it and gate the boundary.

**Do not treat 70% as a target.** It is an observation from one deployment, not a benchmark to hit. Your distribution depends on your function.

**Do not give an agent the send, publish, or file permission** because its drafts have been good. Draft quality and send authority are separate grants.

**Do not skip the misclassification cost.** A zone assignment without the consequence of getting it wrong is an opinion, not governance.

## Cross-References

- `marketing-ops/` : operationalise the zones as actual workflow permissions
- `marketing-strategy-pmm/` : positioning and messaging decisions, mostly Zone 2
- `launch-strategy/` : launch narratives and disclosures, mixed Zone 2 and 3
- `brand-guidelines/` : the standard Zone 2 review checks a draft against
- `content-production/` : high-volume Zone 1 work, the clearest autonomy candidate

## Provenance

Based on the Augmented Marketing Decision Architecture, developed in an enterprise product marketing function and observed across 16 product launches at Tableau (Salesforce) prior to 2025. Observational deployment, not a controlled study. The 70% figure and the zone definitions come from that context and may not transfer to yours.

Framework by Kuber Sharma. Specification: kubersharma.com/frameworks/amda
