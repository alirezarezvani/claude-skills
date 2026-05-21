# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a **comprehensive skills library** for Claude AI and Claude Code - reusable, production-ready skill packages that bundle domain expertise, best practices, analysis tools, and strategic frameworks. The repository provides modular skills that teams can download and use directly in their workflows.

**Current Scope:** 328 production-ready skills across 14 domains with ~441 Python automation tools, ~581 reference guides, 48+ agents (cs-* + 7 personas), and 77+ slash commands. **v2.8.0 (complete)** added 2 new top-level domains — **business-operations/** (7 internal-ops skills: orchestrator + process-mapper + vendor-management + capacity-planner + internal-comms + knowledge-ops + procurement-optimizer) and **commercial/** (8 per-deal-economics skills: orchestrator + pricing-strategist + deal-desk + partnerships-architect + channel-economics + commercial-policy + rfp-responder + commercial-forecaster) — with orchestrator skills using `context: fork` for chaining, Matt Pocock docs-anchored "Forcing-question library" in every SKILL.md, plus `/cs:grill-bizops` and `/cs:grill-commercial`. v2.7.3 ports `alirezarezvani/aeo-box` — AEO (Answer Engine Optimization) skill into marketing-skill/ + security-guidance PreToolUse hook into engineering/. v2.7.0 added 13 Path-B skills across 3 top-level domains (productivity, marketing, research). v2.6.0 added 4 Matt Pocock-derived productivity skills.

**Key Distinction**: This is NOT a traditional application. It's a library of skill packages meant to be extracted and deployed by users into their own Claude workflows.

## Navigation Map

This repository uses **modular documentation**. For domain-specific guidance, see:

| Domain | CLAUDE.md Location | Focus |
|--------|-------------------|-------|
| **Agent Development** | [agents/CLAUDE.md](agents/CLAUDE.md) | cs-* agent creation, YAML frontmatter, relative paths |
| **Marketing Skills** | [marketing-skill/CLAUDE.md](marketing-skill/CLAUDE.md) | Content creation, SEO, ASO, demand gen, campaign analytics |
| **Product Team** | [product-team/CLAUDE.md](product-team/CLAUDE.md) | RICE, OKRs, user stories, UX research, SaaS scaffolding |
| **Engineering (Core)** | [engineering-team/CLAUDE.md](engineering-team/CLAUDE.md) | Fullstack, AI/ML, DevOps, security, data, QA tools |
| **Engineering (POWERFUL)** | [engineering/](engineering/) | Agent design, RAG, MCP, CI/CD, database, observability |
| **C-Level Advisory** | [c-level-advisor/CLAUDE.md](c-level-advisor/CLAUDE.md) | CEO/CTO strategic decision-making |
| **Project Management** | [project-management/CLAUDE.md](project-management/CLAUDE.md) | Atlassian MCP, Jira/Confluence integration |
| **RA/QM Compliance** | [ra-qm-team/CLAUDE.md](ra-qm-team/CLAUDE.md) | ISO 13485, MDR, FDA, GDPR, ISO 27001 compliance |
| **Business & Growth** | [business-growth/CLAUDE.md](business-growth/CLAUDE.md) | Customer success, sales engineering, revenue operations |
| **Finance** | [finance/CLAUDE.md](finance/CLAUDE.md) | Financial analysis, DCF valuation, budgeting, forecasting, SaaS metrics |
| **Standards Library** | [standards/CLAUDE.md](standards/CLAUDE.md) | Communication, quality, git, security standards |
| **Templates** | [templates/CLAUDE.md](templates/CLAUDE.md) | Template system usage |

## Architecture Overview

### Repository Structure

```
claude-code-skills/
├── .claude-plugin/            # Plugin registry (marketplace.json)
├── agents/                    # 27 agents (20 cs-* + 7 personas)
├── commands/                  # 33 slash commands (changelog, tdd, saas-health, prd, code-to-prd, plugin-audit, sprint-plan, slo-design, etc.)
├── engineering-team/          # 32 core engineering skills + Playwright Pro + Self-Improving Agent + Security Suite
├── engineering/               # 44 POWERFUL-tier advanced skills (incl. AgentHub, self-eval, llm-wiki, tc-tracker, ship-gate, slo-architect, write-a-skill, caveman, grill-me, handoff)
├── product-team/              # 13 product skills (incl. apple-hig-expert) + Python tools
├── marketing-skill/           # 44 marketing skills (7 pods) + Python tools
├── c-level-advisor/           # 28 C-level advisory skills (10 roles + orchestration)
├── project-management/        # 9 PM skills + bundled Atlassian Remote MCP (.mcp.json)
├── ra-qm-team/                # 14 RA/QM compliance skills
├── business-growth/           # 5 business & growth skills + Python tools
├── finance/                   # 3 finance skills + Python tools
├── eval-workspace/            # Skill evaluation results (Tessl)
├── standards/                 # 5 standards library files
├── templates/                 # Reusable templates
├── docs/                      # MkDocs Material documentation site
├── scripts/                   # Build scripts (docs generation)
└── documentation/             # Implementation plans, sprints, delivery
```

### Skill Package Pattern

Each skill follows this structure:
```
skill-name/
├── SKILL.md              # Master documentation
├── scripts/              # Python CLI tools (no ML/LLM calls)
├── references/           # Expert knowledge bases
└── assets/               # User templates
```

**Design Philosophy**: Skills are self-contained packages. Each includes executable tools (Python scripts), knowledge bases (markdown references), and user-facing templates. Teams can extract a skill folder and use it immediately.

**Key Pattern**: Knowledge flows from `references/` → into `SKILL.md` workflows → executed via `scripts/` → applied using `assets/` templates.

## Git Workflow

**Branch Strategy:** feature → dev → main (PR only)

**Branch Protection Active:** Main branch requires PR approval. Direct pushes blocked.

### Quick Start

```bash
# 1. Always start from dev
git checkout dev
git pull origin dev

# 2. Create feature branch
git checkout -b feature/agents-{name}

# 3. Work and commit (conventional commits)
feat(agents): implement cs-{agent-name}
fix(tool): correct calculation logic
docs(workflow): update branch strategy

# 4. Push and create PR to dev
git push origin feature/agents-{name}
gh pr create --base dev --head feature/agents-{name}

# 5. After approval, PR merges to dev
# 6. Periodically, dev merges to main via PR
```

**Branch Protection Rules:**
- ✅ Main: Requires PR approval, no direct push
- ✅ Dev: Unprotected, but PRs recommended
- ✅ All: Conventional commits enforced

See [documentation/WORKFLOW.md](documentation/WORKFLOW.md) for complete workflow guide.
See [standards/git/git-workflow-standards.md](standards/git/git-workflow-standards.md) for commit standards.

## Development Environment

**No build system or test frameworks** - intentional design choice for portability.

**Python Scripts:**
- Use standard library only (minimal dependencies)
- CLI-first design for easy automation
- Support both JSON and human-readable output
- No ML/LLM calls (keeps skills portable and fast)

**If adding dependencies:**
- Keep scripts runnable with minimal setup (`pip install package` at most)
- Document all dependencies in SKILL.md
- Prefer standard library implementations

## Current Version

**Version:** v2.8.0 (released — Sprint 1 + 2 + 3 closure complete)

**v2.8.0 highlights — two new top-level domains: business-operations + commercial:**

Designed and shipped under the `/goal` directive to expand BizOps + Commercial surface area. Both domains follow the Path-B 11-file contract per skill, are top-level domain folders (not subfolders inside an existing domain), and ship with orchestrator skills that use `context: fork` to chain sub-skills.

- **`business-operations/`** (new top-level domain) — internal-ops skills for BizOps leads, COO direct reports, vendor management, IT ops. Sprint 1 ships:
  - `business-operations-skills/` (orchestrator, `context: fork`) — routes inquiries via Matt Pocock grill discipline (one question per turn, recommended answer, canon citation)
  - `process-mapper` — BPMN-style swim-lane mapping + bottleneck detection + cycle-time/VA% analysis. 3 stdlib tools, 4 industry profiles, Lean / TOC canon (Womack & Jones, Goldratt, Rother & Shook, Reinertsen, Anderson, Pyzdek, Ohno, Liker).
  - `vendor-management` (`context: fork`) — vendor scoring (5 weighted dimensions, 4 industry profiles), SLA compliance tracker (lower-is-better aware), third-party risk classifier (4 risk vectors, Shared Assessments SIG-Lite). Canon: NIST SP 800-161, ISO/IEC 27036, Gartner TPRM.
  - `cs-bizops-orchestrator` agent + `/cs:bizops` router + `/cs:grill-bizops` (Matt docs-anchored grilling) + per-skill commands.

- **`commercial/`** (new top-level domain) — per-deal-and-packaging skills for deal desk, pricing teams, partner managers, RFP responders. Sprint 1 ships:
  - `commercial-skills/` (orchestrator, `context: fork`) — routes inquiries via Matt grill discipline
  - `pricing-strategist` — 5-model pricing picker, full Van Westendorp PSM (OPP/IDP/PMC/PME + RAP, monotonicity screening), packaging designer with 7 anti-pattern detectors. Canon: Ramanujam (Monetizing Innovation), Skok, Tunguz, Campbell/ProfitWell, Bessemer, Poyar, Sawtooth methodology.
  - `deal-desk` — 5-dimension deal scorer with named approver chain, discount approval router (5-band policy + 4 industry variants), terms redliner detecting 10 patterns (uncapped indemnity, MFN, missing DPA, etc.). **Never auto-approves**; every verdict names the human(s). Canon: SaaStr, Winning by Design, OpenView, Forrester, KeyBanc, IACCM/WorldCC.
  - `cs-commercial-orchestrator` agent + `/cs:commercial` router + `/cs:grill-commercial` (Matt docs-anchored grilling) + per-skill commands.

- **Matt Pocock grill-with-docs pattern adopted** at the SKILL-level — each Sprint 1 SKILL.md ships a "Forcing-question library" section: 5-7 questions, walked one at a time, with a recommended answer and a canon citation per question. The discipline prevents skills from running on fuzzy inputs.

- **Hard rules per domain (enforced by agent personas):**
  - BizOps: every output is a recommendation, never an auto-decision. Vendor scoring routes to a human reviewer.
  - Commercial: pricing outputs model + range (never a single number); deal outputs route to a named human approver (never auto-approve); forecast outputs surface the conversion assumption explicitly.

- **Marketplace + Codex registry:** 57 → 59 plugins. Sprint 2 will add 4 BizOps sub-skills (capacity-planner, internal-comms, knowledge-ops, procurement-optimizer) and 5 Commercial sub-skills (partnerships-architect, channel-economics, commercial-policy, rfp-responder, commercial-forecaster), bringing the new domains to 13 sub-skills total + 2 orchestrators.

- **Verification:** all 12 new Python tools (4 skills × 3 tools each) pass `--help` and `--sample` smoke tests, exit 0. Stdlib-only across the board. Industry profiles verified on the 8 profile-aware tools.

- **PR:** opened against `claude/skills-plugins-framework-XjTjh` (this branch) as draft.

**v2.8.0 master plan:** `documentation/implementation/bizops-commercial-expansion-plan.md`

---



**v2.7.3 Highlights — aeo-box port: AEO skill + security-guidance PreToolUse hook + master prompt preserved:**

Ported `alirezarezvani/aeo-box` after a full component audit. Distilled the valuable parts into our conventions; skipped repo-specific infra (generic agents, GH workflows, TS scripts).

- **`marketing-skill/skills/aeo/`** (new, 8 files, ~3,200 LOC) — Answer Engine Optimization skill, a discipline distinct from SEO. 3 stdlib Python tools: `aeo_audit.py` (E-E-A-T + structure scoring, 0-100 composite, 8 industries with calibrated thresholds where YMYL industries hit 85+, SaaS/b2b/media 70, ecommerce 65), `aeo_optimizer.py` (conservative/balanced/aggressive rewrites + schema.org JSON-LD injection), `citation_tracker.py` (local-first citation ledger at `~/.aeo-data/citations.json` with verdict EARLY/EMERGING/STRONG). 3 references each citing 8 sources: E-E-A-T canon, per-LLM citation patterns (Perplexity / ChatGPT / Claude / Gemini / Mistral with 73% cross-LLM correlation analysis), AEO vs. SEO strategic choice. New `cs-aeo` agent + `/cs:aeo` slash command. New 8th pod ("AEO") added to marketing-skill.
- **`engineering/security-guidance/`** (new, 5 files) — PreToolUse security reminder hook ported from David Dworken @ Anthropic (MIT). Preserves 9 upstream patterns verbatim (eval, pickle, dangerouslySetInnerHTML, innerHTML, document.write, new Function, child_process.exec, os.system, GH Actions workflow injection) + adds 3 new patterns (subprocess shell=True, SQL f-string injection, yaml.unsafe_load). Session-state caching prevents nagging (warn once per file+rule combo), 30-day auto-cleanup, disable via `ENABLE_SECURITY_REMINDER=0`. `attribution` block in plugin.json credits upstream. Reference doc `pretooluse_hook_canon.md` cites 8 sources on hook design discipline.
- **`megaprompts/14-aeo-agentic-megaprompt.md`** — 1,579-line multi-agent AEO application spec preserved verbatim. Keeps Path-B option open for future "build the full agentic AEO app" work.
- **Marketplace + Codex registry:** 55 → 57 plugins; 303 → 305 indexed skills; `marketing-skill/.claude-plugin/plugin.json` description updated from 7 → 8 pods.
- **Verification:** all 4 new Python tools pass `--help` and `--sample`; security hook smoke-tested (exits 2 on detection, 0 on cached/clean); all 3 cross-platform syncs (.codex / .gemini / .hermes) re-ran clean.
- **PRs:** #678 (Hermes first-class integration, merged) → #679 (aeo-box port + Hermes install guide, merged).

**Total scope after v2.7.3:** 313 skills across 12 domain folders, ~402 Python automation tools, ~542 reference guides, 46+ agents, 60+ slash commands.

**Version:** v2.7.0

**v2.7.0 Highlights — v2 megaprompt-to-skill conversion sweep: 13 new skills across productivity + marketing + research:**

This release ships the complete v2 megaprompt collection (`megaprompts/01-13`) as production-ready skills using the **Path-B direct-conversion pattern**. Three new top-level domain folders created (`productivity/`, `marketing/`, `research/`) hosting 13 skills, 142 files, 23,698 lines of code + documentation.

- **`productivity/`** (3 skills) — `capture` (brain-dump-to-action workspace, megaprompt 05), `email` (paired inbox-setup + inbox-triage with 7-file KB contract, megaprompts 06+07), `reflect` (light-prompt sibling, megaprompt 08).
- **`marketing/`** (1 skill) — `landing` (single-file HTML generator with 4 design styles, brand palette validator, GSAP patterns, megaprompt 04).
- **`research/`** (8 skills) — 7 specialists (`pulse`, `litreview`, `grants`, `dossier`, `patent`, `syllabus`, `notebooklm`) + 1 hybrid router (`research/research/` orchestrator). Megaprompts 01-03, 09-13.
- **Research orchestrator** — deterministic SIGNALS classification routes to 6 specialists at ≥2-signal confidence, else runs own 8-step plan-decompose-search-synthesize-cite fallback. Routing transparency mandatory. Distinct from `engineering/autoresearch-agent` (Karpathy's file-optimization loop) — disambiguation surfaced in 5 places.
- **Marketplace + Codex registry:** 43 → 55 plugins; 290 → 303 indexed skills; new categories `productivity` + `research`; `scripts/sync-codex-skills.py` extended to recognize the 3 new top-level domains.
- **Path-B convention formalized** — megaprompt body → SKILL.md verbatim, 11-file plugin layout, 3 stdlib Python scripts per skill, 3 reference docs each citing 7+ authoritative sources, `cs-*` agent + `/cs:*` command, `source` field documents spec + build_pattern + distinct_from.
- **Verification:** 39/39 scripts pass `--help`; 8-phase plugin audit on orchestrator → PASS WITH WARNINGS (structure 84.1/GOOD, scripts 3/3, 0 critical/high security findings); bulk audit on 12 siblings → all 79.5-86.4 structure, 0 critical/high findings.
- **PRs:** #659 (capture) → #660 (pulse) → #661 (email pair) → #662 (landing) → #663 (litreview) → #664 (grants+dossier) → #666 (patent+syllabus) → #667 (domain-folder cleanup) → #668 (reflect) → #669 (notebooklm) → #671 (research orchestrator) → #672 (v2.7.0 release prep).

**Total scope after v2.7.0:** 311 skills across 12 domain folders, ~398 Python automation tools, ~538 reference guides, 45+ agents, 59+ slash commands. (Superseded by v2.7.3 totals above.)

**Version:** v2.6.1

**v2.6.1 Highlights — Meta-skill maturity: validator expansion + 21 placeholder description fixes + audit tool:**
- **`scripts/audit_skills.py`** (new) — repo-wide write-a-skill validator runner. Stdlib-only orchestration: walks every SKILL.md, runs `skill_review_checklist_runner.py`, aggregates PASS/WARN/FAIL counts + failure-by-rule + top-10 worst offenders. ~30s on 298 real skills.
- **Validator trigger pattern expansion** — `skill_description_validator.py` + `skill_review_checklist_runner.py` now recognize `Use before/during/after/while`, `Invoke before/after`, `Apply when`, `Run when/before` (not just `Use when`). 30 legacy skills reclassified FAIL → WARN/PASS automatically.
- **21 placeholder descriptions fixed** — skills whose description field was literally just the skill name (e.g., `description: "Migration Architect"`) from a v2.0.0 batch import. Top-10 POWERFUL-tier engineering (#647): migration-architect, dependency-auditor, codebase-onboarding, ci-cd-pipeline-builder, mcp-server-builder, observability-designer, api-design-reviewer, performance-profiler, changelog-generator, runbook-generator. Remaining 11 across 4 domains (#648): executive-mentor/challenge, executive-mentor/board-prep, git-worktree-manager, skill-tester, monorepo-navigator, env-secrets-manager, agent-workflow-designer, incident-commander, email-template-builder, stripe-integration-expert, contract-and-proposal-writer.
- **Quality gates: binding-for-new vs advisory-for-legacy split** — `quality_gates_for_skills.md` formalizes that Matt's 6-item checklist is BLOCKING for post-v2.6.0 skills and ADVISORY for the 298 legacy SKILL.md files.
- **Aggregate audit improvement (vs v2.6.0 baseline):** PASS 4 → 9 (+5); WARN 111 → 137 (+26); FAIL 183 → 152 (-31); "Missing trigger" failures 119 → 68 (-51). 31 skills total lifted from FAIL.
- **PRs:** #646 (audit tool, merged) → #647 (validator + 10 descriptions, merged) → #648 (remaining 11 descriptions, merged).

**Version:** v2.6.0

**v2.6.0 Highlights — Matt Pocock productivity skills (4 new, all MIT-licensed derivations):**
- **write-a-skill** (`./engineering/write-a-skill/`) — skill-author meta-skill. Matt's 3-phase workflow preserved verbatim. Wrapper adds 3 stdlib validators (description, structure, 6-item review-checklist runner), 4 references citing 7-8 sources each, `cs-skill-author` agent, `/cs:write-a-skill` command.
- **caveman** (`./engineering/caveman/`) — token-compression mode (20-50% typical, 75% upper bound). 3 stdlib tools: deterministic compressor, $/Mtok savings estimator, lint with code-block + exception-zone whitelisting. Matt's persistence rules + auto-clarity exception preserved verbatim.
- **grill-me** (`./engineering/grill-me/`) — relentless plan-interrogator. 3 stdlib tools: decision-tree extractor (6 branch kinds), forcing-question generator with recommendations + dependency-aware ordering, JSON-backed session tracker for multi-day grills. Matt's one-at-a-time discipline preserved verbatim.
- **handoff** (`./engineering/handoff/`) — conversation-continuity generator. 3 stdlib tools: 5-emphasis template generator (deploy/review/debug/design/test/default) honoring Matt's `mktemp` convention, artifact deduplicator across 5 categories, skill recommender matching 14 repo skills. Matt's no-duplication discipline preserved verbatim.
- **Hybrid voice pattern established** for future MIT-licensed external skill imports: preserve upstream voice verbatim in SKILL.md + add wrapper (validators + references citing ≥ 5 sources + cs-* agent + /cs:* command) + karpathy gate + attribution in every file.
- **Karpathy-coder validation:** 100/100 complexity across all 12 new Python tools (0 findings). 13 references cite 7-8 authoritative sources each (well over the ≥ 5 floor).
- **PRs:** #642 (write-a-skill, merged) → #643 (caveman + grill-me + handoff batch, merged). Test suite caught a missing-H1 issue on PR 2; fixed in follow-up commit before merge.

**Version:** v2.5.5

**v2.5.5 Highlights — vpe-advisor: throughput-first VP of Engineering:**
- **vpe-advisor** skill (new, `./c-level-advisor/skills/vpe-advisor/`) — opinionated throughput-first VPE skill covering 4 specific decisions distinct from CTO. 3 stdlib Python tools with deterministic logic: `delivery_throughput_analyzer.py` (DORA 4 metrics with Elite/High/Medium/Low verdict per metric + cycle-time bottleneck identification with typical fix per stage), `eng_hiring_funnel_calculator.py` (7-stage funnel conversion + healthy/leaky verdict per stage + end-to-end conversion + required top-of-funnel volume + weakest-stage fixes), `eng_team_structure_designer.py` (headcount-to-structure map + squad-size assessment + manager-trigger + director-trigger + span-of-control). 4 in-depth references each citing 5+ authoritative sources (DORA / Forsgren / Kim, Spotify squad model, Conway's Law, Will Larson, Camille Fournier, Google SRE Workbook).
- **cs-vpe-advisor** agent (new) — throughput-first operator. Voice: "What's your cycle time, and where does the work spend most of its time waiting?" Distinguishes "what to build" (CTO) from "how to ship it" (VPE) with hard discipline.
- **/cs:vpe-review** (new slash command) — 6-question forcing interrogation: cycle time + waits, DORA 4 metrics, hiring funnel leakage, team structure health, production discipline maturity, VPE-vs-CTO scope.
- **Dual-published from the start:** standalone marketplace plugin AND bundled in c-level-skills.
- **Karpathy-coder discipline maintained (5th consecutive PR):** assumptions surfaced upfront, verifiable success criteria, deterministic tool logic, no scope creep into engineering tactical skills.

**Version:** v2.5.4

**v2.5.4 Highlights — chief-customer-officer-advisor: retention-obsessed CCO:**
- **chief-customer-officer-advisor** skill (new, `./c-level-advisor/skills/chief-customer-officer-advisor/`) — opinionated, retention-obsessed CCO skill covering 4 specific decisions. 3 stdlib Python tools with deterministic logic: `retention_decomposition_analyzer.py` (decomposes ARR retention into GRR / NRR / Logo by cohort, flags leaky-bucket pattern, categorizes churn into 7-category root-cause taxonomy with preventable %), `customer_segmentation_designer.py` (assigns 4-tier segment, scores ICP fit 0-10 across 7 weighted signals, surfaces kill list + upgrade candidates), `cs_coverage_calculator.py` (calculates CSM headcount per tier with ARR ratio + account count constraints, generates 12-month hiring plan with quarterly sequencing + manager-trigger thresholds). 4 in-depth references each citing 5+ authoritative sources (Mehta/Steinman/Murphy, BVP, TSIA, Skok, Tunguz).
- **cs-cco-advisor** agent (new) — retention-obsessed pragmatist orchestrating the skill via `/cs:cco-review`. Distinct voice: "What's your gross retention rate, and what's the #1 reason customers leave?" Trusts gross retention over NRR; refuses to recommend CS hires without naming the customer outcome they unblock.
- **/cs:cco-review** (new slash command) — 6-question forcing interrogation: GRR (not NRR) truth, top churn driver, time-to-value by segment, kill-list candidates, ARR-per-CSM ratio + coverage model, CS comp alignment.
- **Dual-published from the start:** standalone marketplace plugin AND bundled in c-level-skills.
- **Karpathy-coder discipline maintained:** assumptions surfaced upfront, verifiable success criteria, deterministic tool logic, no scope creep into business-growth tactical CS skills.

**Version:** v2.5.3
- **chief-ai-officer-advisor** skill (new, `./c-level-advisor/skills/chief-ai-officer-advisor/`) — opinionated, eval-demanding CAIO skill covering 4 specific decisions. 3 stdlib Python tools with deterministic logic: `model_buildvsbuy_calculator.py` (API vs fine-tune vs build with 3-year TCO, balances economic breakeven with practical feasibility), `ai_risk_classifier.py` (EU AI Act tier classification with Article-level citations + US state patchwork: NYC LL 144, CO AI Act, IL HB 53, CA SB 1001, IL BIPA + industry overlays for FDA/NYDFS/NAIC/ECOA), `ai_cost_economics.py` (API vs self-hosted breakeven with 2026 pricing across A100/H100, utilization reality, hidden costs). 4 in-depth references each citing 5+ authoritative sources: model build-vs-buy strategy (decision tree, 6 fine-tuning approaches, failure modes), AI risk governance (full EU AI Act tier map + NIST AI RMF + governance program checklist), AI cost economics (2026 pricing + GPU economics + migration cost + prompt caching), AI team org evolution (5-stage role map + 9-role definition table + AI team vs data team contrast + 7 anti-patterns).
- **cs-caio-advisor** agent (new) — eval-demanding realist orchestrating the skill via `/cs:caio-review`. Distinct voice: "What does this AI need to be good at, and how would you measure it?" Treats every AI use case as a hiring decision; demands eval set, SLO, and fallback before scale.
- **/cs:caio-review** (new slash command) — 6-question forcing interrogation: eval discipline, hallucination SLO, regulatory classification, model selection, cost trajectory, role-that-unblocks.
- **Karpathy-coder discipline maintained:** assumptions surfaced upfront, verifiable success criteria, deterministic tool logic, no scope creep into engineering AI/ML skills, complexity_checker + diff_surgeon clean on staged diff.

**Version:** v2.5.2
- **chief-data-officer-advisor** skill (new, `./c-level-advisor/skills/chief-data-officer-advisor/`) — opinionated, decision-driven CDO skill covering 4 specific decisions (no generic governance survey). 3 stdlib Python tools with deterministic logic: `ai_training_data_audit.py` (origin × class × use-case matrix → GO/MITIGATE/NO-GO with GDPR Art. 6 and EU AI Act citations), `data_product_strategy_picker.py` (warehouse/lakehouse/mesh recommendation + 6-layer build-vs-buy + 12-month sequencing), `data_asset_valuator.py` (strategic value 0-10, moat strength, M&A multiplier with carve-out penalties, 3 ranked productization paths). 4 references answering one decision each: training rights (decision tree + state patchwork), data product strategy (kill criteria per architecture), customer-data-as-asset (valuation + M&A diligence prep), data team org evolution (stage-to-role map). Karpathy-aligned: explicit anti-patterns, decision-driven (not topic-driven), surgical (does not duplicate engineering data skills).
- **cs-cdo-advisor** agent (new) — decision-driven realist orchestrating the skill via `/cs:cdo-review`. Distinct voice: "What decision does this data drive?" Refuses to recommend tooling before naming the consumer.
- **/cs:cdo-review** (new slash command) — 6-question forcing interrogation: decision being made, consent provenance, internal consumers, M&A diligence impact, model-without-this-source viability, role-that-unblocks-this.
- **Built with Karpathy-coder discipline:** explicit assumptions surfaced upfront, verifiable success criteria locked before code, surgical scope (no edits to unrelated files), deterministic tool logic (not pattern-match prose), kill criteria documented in every recommendation.

**Version:** v2.5.1
- **general-counsel-advisor** skill (new, `./c-level-advisor/skills/general-counsel-advisor/`) — full standalone C-role skill backing the existing `/cs:gc-review` command. 2 stdlib Python tools: `contract_risk_scanner.py` (scans contract text for 12 founder-killer patterns: auto-renew traps, uncapped indemnity, vague IP, aggressive non-compete, missing DPA, MFN pricing, perpetual license-back, etc.) and `term_sheet_analyzer.py` (scores term sheets 0-100 across 12 dimensions: liquidation preference, anti-dilution, option pool, board composition, vesting, pro-rata, drag-along, protective provisions, info rights, dividends, valuation/dilution, holistic). 3 references: contracts playbook (7 startup contract types), IP + regulatory landscape (patents, trademark, OSS compliance, HIPAA/GDPR/FDA/fintech triggers, SOC 2 → ISO sequencing), term sheet decoder (full glossary + founder-friendly defaults + negotiation strategy).
- **cs-general-counsel-advisor** agent (new) — risk-paranoid persona orchestrating the skill via `/cs:gc-review`. Distinct voice: "Before we sign, three things need to be settled in writing." Always escalates to outside counsel — never substitutes for it.
- **First plugin to outclass gstack on a domain it has zero coverage in.** Software-shipping personas don't include General Counsel; legal exposure is where startups most often discover problems after they're expensive to fix.
- **/cs:gc-review updated** to invoke the new tools and reference the skill.

**Version:** v2.5.0

**v2.5.0 Highlights — c-level-agents: Founder-Mode Executive Team:**
- **c-level-agents** plugin (new, `./c-level-advisor/c-level-agents/`) — 8 cs-* persona agents (CFO, CMO, CRO, CPO, COO, CHRO, CISO, Chief of Staff) with moderate voice differentiation, plus 17 /cs:* slash commands surfaced as sub-skills.
- **Forcing-question office hours (8):** `/cs:office-hours` (YC-style 6-Q intake), and per-role `/cs:cfo-review`, `/cs:cmo-review`, `/cs:cpo-review`, `/cs:cro-review`, `/cs:cto-review`, `/cs:ciso-review`, `/cs:gc-review` (General Counsel — a lane gstack lacks entirely).
- **Strategic sprint pipeline (5):** `/cs:brief` → `/cs:boardroom` (6-phase deliberation with Phase 2 isolation + devil's-advocate pass) → `/cs:decide` (two-layer memory + preserved dissent) → `/cs:execute` (90-day plan) → `/cs:post-mortem` (scored against pre-committed criteria).
- **Meta + safety (4):** `/cs:founder-mode` (auto-router), `/cs:onboard` (12-Q founder interview), `/cs:cross-eval` (multi-model consensus with graceful Claude-only fallback), `/cs:freeze` (cooldown lock on irreversible decisions).
- **References:** `persona-voices.md` (voice specs) and `llm-wiki-bridge.md` (Markdown-only persistent memory — answer to gstack's gbrain Postgres dependency).
- Positioned as the business-domain answer to YC Garry Tan's gstack: broader role coverage, real frameworks (RICE/JTBD/OKR/ADKAR/Wardley/8-dim health), compliance lane (ra-qm-team), explicit voice differentiation, and stdlib-only memory.

**Version:** v2.4.5

**v2.4.x Highlights — Reliability Portfolio (Phase 1–4):**
- **slo-architect** (Phase 4 — keystone) — SLO/SLI/error-budget discipline per Google SRE Workbook. 3 stdlib Python tools (`slo_designer`, `error_budget_calculator` with multi-window burn-rate alerts, `slo_review`), 4 reference docs, asset templates, `/slo-design` slash command. Engineering-advanced bundle 49 → 50.
- **chaos-engineering** (Phase 3) — experiment designer, blast-radius calculator, postmortem generator. `/chaos-experiment` command.
- **kubernetes-operator** (Phase 2) — CRD validator, reconcile linter, capability auditor. `/operator-audit` command.
- **feature-flags-architect** (Phase 1) — flag debt scanner, rollout planner, kill-switch audit. `/flag-cleanup` command.
- **ship-gate** — pre-production audit skill (89 checks across 8 categories, stdlib-only, MIT). External contribution.
- **Atlassian Remote MCP** — bundled `.mcp.json` in `project-management/` (SSE transport, OAuth handled by Claude Code, no env vars required).
- **Auditor + CI cleanup** — `.mcp.json` allowlist in skill-security-auditor, manifest-only PRs skip audit, README links (toprank).
- 246 total skills, 359 Python tools, 485 references, 27 agents, 33 commands.

**v2.3.0 Highlights:**
- **llm-wiki plugin** — new POWERFUL-tier skill implementing Karpathy's LLM Wiki pattern. Second brain for Claude Code + Obsidian where the LLM incrementally ingests sources into a persistent, interlinked markdown vault. Ships SKILL.md (with `context: fork`), 3 sub-agents (wiki-ingestor, wiki-librarian, wiki-linter), 5 slash commands (/wiki-init, /wiki-ingest, /wiki-query, /wiki-lint, /wiki-log), 8 stdlib-only Python tools, 8 reference guides, full vault templates, and a worked example. Cross-tool compatible with Claude Code, Codex CLI, Cursor, Antigravity, OpenCode, Gemini CLI.
- **tc-tracker** — new engineering skill: task context tracker with lifecycle, handoff format, schema, and 5 Python tools (tc_init, tc_create, tc_update, tc_status, tc_validator) plus `/tc` slash command
- **apple-hig-expert** — new product skill: Apple Human Interface Guidelines expert with Liquid Glass aesthetic focus. Audits iOS/macOS/visionOS apps with `hig_checker` Python tool and comprehensive reference docs on visual design, platform specifics, and accessibility
- 235 total skills, 314 Python tools, 435 references, 28 agents, 27 commands

**Version:** v2.2.0

**v2.2.0 Highlights:**
- **Security skills suite** — 6 new engineering-team skills: adversarial-reviewer, ai-security, cloud-security, incident-response, red-team, threat-detection (5 Python tools, 4 reference guides)
- **Self-eval skill** — Honest AI work quality evaluation with two-axis scoring, score inflation detection, and session persistence
- **Snowflake development** — Data warehouse development, SQL optimization, and data pipeline patterns
- 234 total skills across 9 domains, 306 Python tools, 427 references, 25 agents, 22 commands
- MkDocs docs site expanded to 269 generated pages (301 HTML pages)

**v2.1.2 (2026-03-10):**
- Landing page generator now outputs **Next.js TSX + Tailwind CSS** by default (4 design styles, 7 section generators)
- **Brand voice integration** — landing page workflow uses marketing brand voice analyzer to match copy tone to design style
- 25 Python scripts fixed across all domains (syntax, dependencies, argparse)
- 237/237 scripts verified passing `--help`

**v2.1.1 (2026-03-07):**
- 18 skills optimized from 66-83% to 85-100% via Tessl quality review
- YAML frontmatter (name + description) added to all SKILL.md files
- 6 new agents + 5 slash commands, Gemini CLI support, MkDocs docs site

**v2.0.0 (2026-02-16):**
- 25 POWERFUL-tier engineering skills added (engineering/ folder)
- Plugin marketplace infrastructure (.claude-plugin/marketplace.json)
- Multi-platform support: Claude Code, OpenAI Codex, OpenClaw, Hermes Agent, Gemini CLI, Cursor, and 6 more

**Past Sprints:** See [documentation/delivery/](documentation/delivery/) and [CHANGELOG.md](CHANGELOG.md) for history.

## Roadmap

**Phase 1-4 Complete:** 246 production-ready skills deployed across 9 domains
- Engineering Core (32), Engineering POWERFUL (40), Product (13), Marketing (44), PM (9), C-Level (28), RA/QM (14), Business & Growth (5), Finance (3)
- 359 Python automation tools, 485 reference guides, 27 agents, 33 commands
- Complete enterprise coverage from engineering through regulatory compliance, sales, customer success, and finance
- Reliability portfolio: feature-flags-architect, kubernetes-operator, chaos-engineering, slo-architect (Google SRE Workbook canon)
- MkDocs Material docs site with 293+ indexed pages for SEO

See domain-specific roadmaps in each skill folder's README.md or roadmap files.

## Key Principles

1. **Skills are products** - Each skill deployable as standalone package
2. **Documentation-driven** - Success depends on clear, actionable docs
3. **Algorithm over AI** - Use deterministic analysis (code) vs LLM calls
4. **Template-heavy** - Provide ready-to-use templates users customize
5. **Platform-specific** - Specific best practices > generic advice

## ClawHub Publishing Constraints

This repository publishes skills to **ClawHub** (clawhub.com) as the distribution registry. The following rules are **non-negotiable**:

1. **cs- prefix for slug conflicts only.** When a skill slug is already taken on ClawHub by another publisher, publish with the `cs-` prefix (e.g., `cs-copywriting`, `cs-seo-audit`). The `cs-` prefix applies **only on the ClawHub registry** — repo folder names, local skill names, and all other tools (Claude Code, Codex, Gemini CLI) remain unchanged.
2. **Never rename repo folders or local skill names** to match ClawHub slugs. The repo is the source of truth.
3. **No paid/commercial service dependencies.** Skills must not require paid third-party API keys or commercial services unless provided by the project itself. Free-tier APIs and BYOK (bring-your-own-key) patterns are acceptable.
4. **Rate limit: 5 new skills per hour** on ClawHub. Batch publishes must respect this. Use the drip timer (`clawhub-drip.timer`) for bulk operations.
5. **plugin.json schema** — Required fields: `name`, `description`, `version`, `author`, `homepage`, `repository`, `license`, `skills`. Two **approved extension fields** are permitted in the repo (stripped at ClawHub-publish time, if/when a stripping pipeline lands):
   - `source` (object) — provenance metadata for skills built via Path-B megaprompt conversion. Recommended shape: `{spec: "megaprompts/NN-name.md", build_pattern: "...", distinct_from: "..."}`. Used by all 13 v2 megaprompt-derived skills (productivity/, marketing/, research/).
   - `attribution` (object) — credit metadata for skills derived from external MIT-licensed work. Used by `engineering/caveman`, `engineering/grill-me`, `engineering/grill-with-docs` (Matt Pocock derivatives).

   No other extras. The `skills` value depends on the plugin layout **and the installed CC version** (CC tightens its path validator regularly):

   | CC version range | Plugin with `skills/` subdir | Notes |
   |---|---|---|
   | v2.1.107–v2.1.132 | `"skills": "./skills"` | `./` prefix required |
   | v2.1.133+ | `"skills": "skills"` | prefix-less form |

   **Currently installed: CC v2.1.119 → use `"./skills"` (WITH `./` prefix).**

   - Single-skill plugin (SKILL.md at root): `"skills": ["./"]` (array form required, all versions).
   - Plugin with `skills/` subdir: `"skills": "./skills"` (CC v2.1.107–v2.1.132, currently installed).
   - Multi-skill domain plugin (skills are subfolders at root): `"skills": ["./sub1", "./sub2", ...]` (explicit list, all versions).

   When CC is upgraded past v2.1.133: change `"./skills"` → `"skills"` in all 47 string-format plugin.json files, then update this table and `scripts/check_plugin_json.py` `_check_skills_string()` together — they must move in lockstep.

   **Enforcement:** `scripts/check_plugin_json.py --all` runs in `ci-quality-gate.yml` on every PR and blocks merge on any violation. It actively rejects bare `"./"` (issue #539). The validator's accepted string values track the currently installed CC version.
6. **Version follows repo versioning.** ClawHub package versions must match the repo release version (currently v2.7.0+).

## Anti-Patterns to Avoid

- Creating dependencies between skills (keep each self-contained)
- Adding complex build systems or test frameworks (maintain simplicity)
- Generic advice (focus on specific, actionable frameworks)
- LLM calls in scripts (defeats portability and speed)
- Over-documenting file structure (skills are simple by design)

## Working with This Repository

**Creating New Skills:** Follow the appropriate domain's roadmap and CLAUDE.md guide (see Navigation Map above).

**Editing Existing Skills:** Maintain consistency across markdown files. Use the same voice, formatting, and structure patterns.

**Quality Standard:** Each skill should save users 40%+ time while improving consistency/quality by 30%+.

## Additional Resources

- **.gitignore:** Excludes .vscode/, .DS_Store, AGENTS.md, PROMPTS.md, .env*
- **Plugin Registry:** [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) - Marketplace distribution
- **Standards Library:** [standards/](standards/) - Communication, quality, git, documentation, security
- **Implementation Plans:** [documentation/implementation/](documentation/implementation/)
- **Sprint Delivery:** [documentation/delivery/](documentation/delivery/)

---

**Last Updated:** May 17, 2026
**Version:** v2.7.3
**Status:** 313 skills deployed across 12 domains, 57 marketplace plugins, docs site live
