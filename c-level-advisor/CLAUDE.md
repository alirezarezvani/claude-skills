# C-Level Advisory Skills — Claude Code Guidance

A complete virtual board of directors: 28 skills covering 10 executive roles, orchestration, cross-cutting capabilities, and culture & collaboration frameworks.

## Architecture

```
/cs:setup (Founder Interview) → company-context.md
                │
        Chief of Staff (Router)
                │
    ┌───────────┼───────────┐
    10 Roles    6 Cross-Cut  6 Culture
    │           │            │
    └───────────┼────────────┘
                │
        Executive Mentor (Critic)
                │
        Decision Logger (Two-Layer Memory)
```

## Skills Overview

### C-Suite Roles (10)

| Role | Folder | Reasoning Technique | Scripts |
|------|--------|-------------------|---------|
| **CEO** | `ceo-advisor/` | Tree of Thought | strategy_analyzer, financial_scenario_analyzer |
| **CTO** | `cto-advisor/` | ReAct | tech_debt_analyzer, team_scaling_calculator |
| **COO** | `coo-advisor/` | Step by Step | ops_efficiency_analyzer, okr_tracker |
| **CPO** | `cpo-advisor/` | First Principles | pmf_scorer, portfolio_analyzer |
| **CMO** | `cmo-advisor/` | Recursion of Thought | marketing_budget_modeler, growth_model_simulator |
| **CFO** | `cfo-advisor/` | Chain of Thought | burn_rate_calculator, unit_economics_analyzer, fundraising_model |
| **CRO** | `cro-advisor/` | Chain of Thought | revenue_forecast_model, churn_analyzer |
| **CISO** | `ciso-advisor/` | Risk-Based | risk_quantifier, compliance_tracker |
| **CHRO** | `chro-advisor/` | Empathy + Data | hiring_plan_modeler, comp_benchmarker |
| **Executive Mentor** | `executive-mentor/` | Adversarial | decision_matrix_scorer, stakeholder_mapper |

### Orchestration (6)

| Skill | Folder | Purpose |
|-------|--------|---------|
| **C-Suite Onboard** | `cs-onboard/` | Founder interview → company-context.md |
| **Chief of Staff** | `chief-of-staff/` | Routes questions, triggers board meetings |
| **Board Meeting** | `board-meeting/` | 6-phase multi-agent deliberation |
| **Decision Logger** | `decision-logger/` | Two-layer memory (raw + approved) |
| **Agent Protocol** | `agent-protocol/` | Inter-agent invocation, loop prevention, quality loop |
| **Context Engine** | `context-engine/` | Company context loading + anonymization |

### Cross-Cutting Capabilities (6)

| Skill | Folder | Purpose |
|-------|--------|---------|
| **Board Deck Builder** | `board-deck-builder/` | Assembles board/investor updates |
| **Scenario War Room** | `scenario-war-room/` | Multi-variable what-if modeling |
| **Competitive Intel** | `competitive-intel/` | Systematic competitor tracking |
| **Org Health Diagnostic** | `org-health-diagnostic/` | Cross-functional health scoring |
| **M&A Playbook** | `ma-playbook/` | Acquiring or being acquired |
| **International Expansion** | `intl-expansion/` | Market entry strategy |

### Culture & Collaboration (6)

| Skill | Folder | Purpose |
|-------|--------|---------|
| **Culture Architect** | `culture-architect/` | Build and operationalize culture |
| **Company OS** | `company-os/` | EOS/Scaling Up operating system |
| **Founder Coach** | `founder-coach/` | Founder development and growth |
| **Strategic Alignment** | `strategic-alignment/` | Strategy cascade, silo detection |
| **Change Management** | `change-management/` | ADKAR-based change rollout |
| **Internal Narrative** | `internal-narrative/` | One story across all audiences |

## Executive Mentor Slash Commands

The only skill with a `plugin.json` (namespace: `em`) because it has slash commands. Other skills are invoked by name through the Chief of Staff router or directly by the user. This is intentional — only add `plugin.json` when a skill has dedicated slash commands that need a namespace.

| Command | Purpose |
|---------|---------|
| `/em:challenge` | Pre-mortem analysis of any plan |
| `/em:board-prep` | Board meeting preparation |
| `/em:hard-call` | Framework for hard decisions |
| `/em:stress-test` | Stress-test any assumption |
| `/em:postmortem` | Honest retrospective |

## Key Design Decisions

- **Two-layer memory:** Raw transcripts (reference) + approved decisions only (feeds future meetings). Prevents hallucinated consensus.
- **Phase 2 isolation:** During board meetings, agents think independently before cross-examination.
- **Internal Quality Loop:** Self-verify → peer-verify → critic pre-screen → present. No unverified output reaches the founder.
- **Proactive triggers:** Every role has context-driven early warnings that surface issues without being asked.
- **User Communication Standard:** Bottom Line → What → Why → How to Act → Your Decision. Results only, no process narration.

## Python Tools (25 total)

All scripts are stdlib-only, CLI-first, with JSON output and embedded sample data.

```bash
# Examples
python cfo-advisor/scripts/burn_rate_calculator.py
python cro-advisor/scripts/churn_analyzer.py
python cpo-advisor/scripts/pmf_scorer.py
python org-health-diagnostic/scripts/health_scorer.py
python strategic-alignment/scripts/alignment_checker.py
python decision-logger/scripts/decision_tracker.py
```

## Integration with Other Domains

| C-Level Role | Layers Above |
|-------------|-------------|
| CMO | marketing-skill/ (content, demand gen, ASO execution) |
| CFO | finance/financial-analyst (spreadsheets, DCF) |
| CRO | business-growth/ (revenue ops, sales engineering) |
| CISO | ra-qm-team/ (ISO 27001 checklists, ISMS audits) |
| CPO | product-team/ (PM toolkit, user stories, sprint planning) |

---

**Last Updated:** 2026-03-05
**Skills Deployed:** 28 skills (10 roles + 5 mentor commands + 6 orchestration + 6 cross-cutting + 6 culture)
**Python Tools:** 25 (stdlib-only)
**Reference Docs:** 52
