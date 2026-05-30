# C-Level Advisory Skills — Claude Code Guidance

A complete virtual board of directors: 28 skills covering 10 executive roles, orchestration, cross-cutting capabilities, and culture & collaboration frameworks — plus the new **c-level-agents** plugin layer that surfaces 8 cs-* persona agents and 17 `/cs:*` slash commands on top of the skills.

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

### C-Suite Roles (15)

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
| **General Counsel** | `general-counsel-advisor/` | Risk-Based | contract_risk_scanner, term_sheet_analyzer |
| **Chief Data Officer** | `chief-data-officer-advisor/` | Decision-Driven | ai_training_data_audit, data_product_strategy_picker, data_asset_valuator |
| **Chief AI Officer** | `chief-ai-officer-advisor/` | Eval-Demanding | model_buildvsbuy_calculator, ai_risk_classifier, ai_cost_economics |
| **Chief Customer Officer** | `chief-customer-officer-advisor/` | Retention-Obsessed | retention_decomposition_analyzer, customer_segmentation_designer, cs_coverage_calculator |
| **VP of Engineering** ⭐ NEW v2.5.5 | `vpe-advisor/` | Throughput-First | delivery_throughput_analyzer, eng_hiring_funnel_calculator, eng_team_structure_designer |
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

## c-level-agents Plugin (v1.0.0 — new in v2.5.0)

A separate plugin at `c-level-agents/` that wraps the 10 C-roles with persona agents and slash commands. Founder-mode entry layer.

### 13 cs-* Agents (in `c-level-agents/agents/`)

| Agent | Voice | Wraps Skill |
|---|---|---|
| cs-cfo-advisor | Numerate skeptic | cfo-advisor |
| cs-cmo-advisor | Narrative-first | cmo-advisor |
| cs-cro-advisor | Pipeline-paranoid | cro-advisor |
| cs-cpo-advisor | JTBD-driven | cpo-advisor |
| cs-coo-advisor | Execution OS | coo-advisor |
| cs-chro-advisor | People-systems | chro-advisor |
| cs-ciso-advisor | Risk-paranoid | ciso-advisor |
| cs-chief-of-staff | Router & synthesist | chief-of-staff |
| cs-general-counsel-advisor | Risk-paranoid (legal) | general-counsel-advisor |
| cs-cdo-advisor | Decision-driven (data) | chief-data-officer-advisor |
| cs-caio-advisor | Eval-demanding (AI) | chief-ai-officer-advisor |
| cs-cco-advisor | Retention-obsessed (customer) | chief-customer-officer-advisor |
| cs-vpe-advisor ⭐ NEW v2.5.5 | Throughput-first (engineering ops) | vpe-advisor |

Existing `cs-ceo-advisor` and `cs-cto-advisor` live in `/agents/c-level/` and integrate with the same protocol.

### 17 /cs:* Slash Commands (in `c-level-agents/skills/`)

**Forcing-question office hours (8):** `/cs:office-hours`, `/cs:cfo-review`, `/cs:cmo-review`, `/cs:cpo-review`, `/cs:cro-review`, `/cs:cto-review`, `/cs:ciso-review`, `/cs:gc-review`

**Strategic sprint pipeline (5):** `/cs:brief` → `/cs:boardroom` → `/cs:decide` → `/cs:execute` → `/cs:post-mortem`

**Meta + safety (4):** `/cs:founder-mode` (auto-router), `/cs:onboard` (founder interview), `/cs:cross-eval` (multi-model consensus), `/cs:freeze` (cooldown lock)

See [c-level-agents/README.md](c-level-agents/README.md) for the full plugin guide and [c-level-agents/references/persona-voices.md](c-level-agents/references/persona-voices.md) for voice specs.

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

**Last Updated:** 2026-05-13
**Skills Deployed:** 33 skills (15 roles incl. General Counsel, CDO, CAIO, CCO, and VPE + 5 mentor commands + 6 orchestration + 6 cross-cutting + 6 culture) + 21 /cs:* sub-skills in c-level-agents plugin
**Agents:** 15 cs-* (cs-ceo, cs-cto in /agents/c-level/; 13 in c-level-agents/agents/ including new cs-vpe-advisor)
**Python Tools:** 39 (stdlib-only) — +3 with vpe-advisor (delivery_throughput_analyzer, eng_hiring_funnel_calculator, eng_team_structure_designer)
**Reference Docs:** 73 (71 in skills + 2 in c-level-agents/references)
