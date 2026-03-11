---
title: "C-Level Advisory Ecosystem"
description: "C-Level Advisory Ecosystem - Claude Code skill from the C-Level Advisory domain."
---

# C-Level Advisory Ecosystem

<div class="page-meta" markdown>
<span class="meta-badge">:material-account-tie: C-Level Advisory</span>
<span class="meta-badge">:material-identifier: `c-level-advisor`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/c-level-advisor/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install c-level-skills</code>
</div>


A complete virtual board of directors for founders and executives.

## Quick Start

```
1. Run /cs:setup → creates company-context.md (all agents read this)
   ✓ Verify company-context.md was created and contains your company name,
     stage, and core metrics before proceeding.
2. Ask any strategic question → Chief of Staff routes to the right role
3. For big decisions → /cs:board triggers a multi-role board meeting
   ✓ Confirm at least 3 roles have weighed in before accepting a conclusion.
```

### Commands

#### `/cs:setup` — Onboarding Questionnaire

Walks through the following prompts and writes `company-context.md` to the project root. Run once per company or when context changes significantly.

```
Q1. What is your company name and one-line description?
Q2. What stage are you at? (Idea / Pre-seed / Seed / Series A / Series B+)
Q3. What is your current ARR (or MRR) and runway in months?
Q4. What is your team size and structure?
Q5. What industry and customer segment do you serve?
Q6. What are your top 3 priorities for the next 90 days?
Q7. What is your biggest current risk or blocker?
```

After collecting answers, the agent writes structured output:

```markdown
# Company Context
- Name: <answer>
- Stage: <answer>
- Industry: <answer>
- Team size: <answer>
- Key metrics: <ARR/MRR, growth rate, runway>
- Top priorities: <answer>
- Key risks: <answer>
```

#### `/cs:board` — Full Board Meeting

Convenes all relevant executive roles in three phases:

```
Phase 1 — Framing:   Chief of Staff states the decision and success criteria.
Phase 2 — Isolation: Each role produces independent analysis (no cross-talk).
Phase 3 — Debate:    Roles surface conflicts, stress-test assumptions, align on
                     a recommendation. Dissenting views are preserved in the log.
```

Use for high-stakes or cross-functional decisions. Confirm at least 3 roles have weighed in before accepting a conclusion.

### Chief of Staff Routing Matrix

When a question arrives without a role prefix, the Chief of Staff maps it to the appropriate executive using these primary signals:

| Topic Signal | Primary Role | Supporting Roles |
|---|---|---|
| Fundraising, valuation, burn | CFO | CEO, CRO |
| Architecture, build vs. buy, tech debt | CTO | CPO, CISO |
| Hiring, culture, performance | CHRO | CEO, Executive Mentor |
| GTM, demand gen, positioning | CMO | CRO, CPO |
| Revenue, pipeline, sales motion | CRO | CMO, CFO |
| Security, compliance, risk | CISO | CTO, CFO |
| Product roadmap, prioritisation | CPO | CTO, CMO |
| Ops, process, scaling | COO | CFO, CHRO |
| Vision, strategy, investor relations | CEO | Executive Mentor |
| Career, founder psychology, leadership | Executive Mentor | CEO, CHRO |
| Multi-domain / unclear | Chief of Staff convenes board | All relevant roles |

### Invoking a Specific Role Directly

To bypass Chief of Staff routing and address one executive directly, prefix your question with the role name:

```
CFO: What is our optimal burn rate heading into a Series A?
CTO: Should we rebuild our auth layer in-house or buy a solution?
CHRO: How do we design a performance review process for a 15-person team?
```

The Chief of Staff still logs the exchange; only routing is skipped.

### Example: Strategic Question

**Input:** "Should we raise a Series A now or extend runway and grow ARR first?"

**Output format:**
- **Bottom Line:** Extend runway 6 months; raise at $2M ARR for better terms.
- **What:** Current $800K ARR is below the threshold most Series A investors benchmark.
- **Why:** Raising now increases dilution risk; 6-month extension is achievable with current burn.
- **How to Act:** Cut 2 low-ROI channels, hit $2M ARR, then run a 6-week fundraise sprint.
- **Your Decision:** Proceed with extension / Raise now anyway (choose one).

### Example: company-context.md (after /cs:setup)

```markdown
# Company Context
- Name: Acme Inc.
- Stage: Seed ($800K ARR)
- Industry: B2B SaaS
- Team size: 12
- Key metrics: 15% MoM growth, 18-month runway
- Top priorities: Series A readiness, enterprise GTM
```

## What's Included

### 10 C-Suite Roles
CEO, CTO, COO, CPO, CMO, CFO, CRO, CISO, CHRO, Executive Mentor

### 6 Orchestration Skills
Founder Onboard, Chief of Staff (router), Board Meeting, Decision Logger, Agent Protocol, Context Engine

### 6 Cross-Cutting Capabilities
Board Deck Builder, Scenario War Room, Competitive Intel, Org Health Diagnostic, M&A Playbook, International Expansion

### 6 Culture & Collaboration
Culture Architect, Company OS, Founder Coach, Strategic Alignment, Change Management, Internal Narrative

## Key Features

- **Internal Quality Loop:** Self-verify → peer-verify → critic pre-screen → present
- **Two-Layer Memory:** Raw transcripts + approved decisions only (prevents hallucinated consensus)
- **Board Meeting Isolation:** Phase 2 independent analysis before cross-examination
- **Proactive Triggers:** Context-driven early warnings without being asked
- **Structured Output:** Bottom Line → What → Why → How to Act → Your Decision
- **25 Python Tools:** All stdlib-only, CLI-first, JSON output, zero dependencies

## See Also

- `CLAUDE.md` — full architecture diagram and integration guide
- `agent-protocol/SKILL.md` — communication standard and quality loop details
- `chief-of-staff/SKILL.md` — routing matrix for all 28 skills
