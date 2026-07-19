---
title: "Slash Commands — AI Coding Agent Commands & Codex Shortcuts"
description: "92 slash commands for Claude Code, Codex CLI, and Gemini CLI — sprint planning, tech debt analysis, PRDs, OKRs, and more."
---

<div class="domain-header" markdown>

# :material-console: Slash Commands

<p class="domain-count">92 commands for quick access to common operations</p>

</div>

<div class="grid cards" markdown>

-   :material-console:{ .lg .middle } **[`/a11y-audit`](a11y-audit.md)**

    ---

    Scan a frontend project for WCAG 2.2 accessibility issues, show fixes, and optionally check color contrast.

-   :material-console:{ .lg .middle } **[`/changelog`](changelog.md)**

    ---

    Generate Keep a Changelog entries from git history and validate commit message format.

-   :material-console:{ .lg .middle } **[`/chaos-experiment`](chaos-experiment.md)**

    ---

    Step through the design of a chaos engineering experiment using the chaos-engineering skill. Produces a plan, calcula...

-   :material-console:{ .lg .middle } **[`/code-to-prd`](code-to-prd.md)**

    ---

    Reverse-engineer a frontend codebase into a complete Product Requirements Document.

-   :material-console:{ .lg .middle } **[`/competitive-matrix`](competitive-matrix.md)**

    ---

    Build competitive matrices with weighted scoring, gap analysis, and market positioning insights.

-   :material-console:{ .lg .middle } **[`/cs-aeo`](cs-aeo.md)**

    ---

    Command: /cs:aeo action args

-   :material-console:{ .lg .middle } **[`/cs-backend-review`](cs-backend-review.md)**

    ---

    Use the cs-backend-engineer agent (uses context: fork) to handle this inquiry:

-   :material-console:{ .lg .middle } **[`/cs-engineer-grill`](cs-engineer-grill.md)**

    ---

    Walk the user through the Matt Pocock forcing-question discipline before they lock any engineering decision. This is ...

-   :material-console:{ .lg .middle } **[`/cs-frontend-review`](cs-frontend-review.md)**

    ---

    Use the cs-frontend-engineer agent (uses context: fork) to handle this inquiry:

-   :material-console:{ .lg .middle } **[`/cs-fullstack-review`](cs-fullstack-review.md)**

    ---

    Use the cs-fullstack-engineer agent (which uses context: fork to keep the parent thread clean) to handle this inquiry:

-   :material-console:{ .lg .middle } **[`/cs-webinar`](cs-webinar.md)**

    ---

    Command: /cs:webinar mode args

-   :material-console:{ .lg .middle } **[`/financial-health`](financial-health.md)**

    ---

    Analyze financial statements, build valuation models, assess budget variances, and construct forecasts.

-   :material-console:{ .lg .middle } **[`/flag-cleanup`](flag-cleanup.md)**

    ---

    Run the full feature-flag cleanup workflow:

-   :material-console:{ .lg .middle } **[`/focused-fix`](focused-fix.md)**

    ---

    Systematically repair an entire feature or module using the 5-phase protocol. Target: $ARGUMENTS (a feature path or m...

-   :material-console:{ .lg .middle } **[`/google-workspace`](google-workspace.md)**

    ---

    Google Workspace CLI administration via the gws CLI. Run setup diagnostics, security audits, browse and execute recip...

-   :material-console:{ .lg .middle } **[`/karpathy-check`](karpathy-check.md)**

    ---

    Review your staged changes (or last commit) against Karpathy's 4 coding principles.

-   :material-console:{ .lg .middle } **[`/okr`](okr.md)**

    ---

    Generate cascaded OKR frameworks from company-level strategy down to team-level key results.

-   :material-console:{ .lg .middle } **[`/operator-audit`](operator-audit.md)**

    ---

    Run the full audit on a Kubernetes Operator repository:

-   :material-console:{ .lg .middle } **[`/persona`](persona.md)**

    ---

    Generate structured user personas with demographics, goals, pain points, and behavioral patterns.

-   :material-console:{ .lg .middle } **[`/pipeline`](pipeline.md)**

    ---

    Detect project stack and generate CI/CD pipeline configurations for GitHub Actions or GitLab CI.

-   :material-console:{ .lg .middle } **[`/plugin-audit`](plugin-audit.md)**

    ---

    Full audit pipeline for any skill, plugin, agent, or command in this repository. Runs 8 validation phases, auto-fixes...

-   :material-console:{ .lg .middle } **[`/prd`](prd.md)**

    ---

    Generate a concise, evidence-gated product requirements document for $ARGUMENTS.

-   :material-console:{ .lg .middle } **[`/project-health`](project-health.md)**

    ---

    Generate portfolio health dashboards and risk matrices for project oversight.

-   :material-console:{ .lg .middle } **[`/retro`](retro.md)**

    ---

    Analyze retrospective data for recurring themes, sentiment trends, and action item effectiveness.

-   :material-console:{ .lg .middle } **[`/rice`](rice.md)**

    ---

    Prioritize features using RICE scoring (Reach, Impact, Confidence, Effort) with optional capacity constraints.

-   :material-console:{ .lg .middle } **[`/saas-health`](saas-health.md)**

    ---

    Calculate SaaS financial health metrics from raw business numbers, benchmark against industry standards, and project ...

-   :material-console:{ .lg .middle } **[`/seo-auditor`](seo-auditor.md)**

    ---

    Systematically scan, audit, and optimize documentation files for SEO. Targets README.md files and docs/ pages — fixes...

-   :material-console:{ .lg .middle } **[`/slo-design`](slo-design.md)**

    ---

    Step through SLO design using the slo-architect skill. Produces an SLO definition, computes error budget + multi-wind...

-   :material-console:{ .lg .middle } **[`/sprint-health`](sprint-health.md)**

    ---

    Score sprint health across delivery, quality, and team metrics with velocity trend analysis.

-   :material-console:{ .lg .middle } **[`/sprint-plan`](sprint-plan.md)**

    ---

    Create a sprint plan for $ARGUMENTS with explicit capacity math, a carry-over check, and a definition-of-ready gate. ...

-   :material-console:{ .lg .middle } **[`/tc`](tc.md)**

    ---

    Dispatch a TC (Technical Change) command. Arguments: $ARGUMENTS.

-   :material-console:{ .lg .middle } **[`/tdd`](tdd.md)**

    ---

    Drive a test-first workflow for $ARGUMENTS using the TDD Guide skill. The first word of $ARGUMENTS selects the mode (...

-   :material-console:{ .lg .middle } **[`/tech-debt`](tech-debt.md)**

    ---

    Scan codebases for technical debt, score severity, and generate prioritized remediation plans.

-   :material-console:{ .lg .middle } **[`/user-story`](user-story.md)**

    ---

    Generate structured user stories with acceptance criteria, story points, and sprint capacity planning.

-   :material-console:{ .lg .middle } **[`/wiki-ingest`](wiki-ingest.md)**

    ---

    Ingest a new source into the LLM Wiki. This is the most-used command.

-   :material-console:{ .lg .middle } **[`/wiki-init`](wiki-init.md)**

    ---

    Bootstrap a new LLM Wiki vault. Creates raw/, wiki/{entities,concepts,sources,comparisons,synthesis}, the index and l...

-   :material-console:{ .lg .middle } **[`/wiki-lint`](wiki-lint.md)**

    ---

    Health-check the wiki. Surfaces orphan pages, broken wikilinks, stale claims, missing frontmatter, contradictions, an...

-   :material-console:{ .lg .middle } **[`/wiki-log`](wiki-log.md)**

    ---

    Show recent entries from wiki/log.md. Every LLM operation on the wiki leaves a standardized entry:

-   :material-console:{ .lg .middle } **[`/wiki-query`](wiki-query.md)**

    ---

    Ask the wiki a question. The librarian reads index.md first, picks relevant pages across categories, synthesizes an a...

-   :material-console:{ .lg .middle } **[`/cs-caveman`](cs-caveman.md)**

    ---

    Command: /cs:caveman

-   :material-console:{ .lg .middle } **[`/cs-claude-coach`](cs-claude-coach.md)**

    ---

    Activates the claude-coach skill. From this point on, the conversation gains:

-   :material-console:{ .lg .middle } **[`/cs-grill-me`](cs-grill-me.md)**

    ---

    Command: /cs:grill-me <path-to-plan>

-   :material-console:{ .lg .middle } **[`/cs-grill-with-docs`](cs-grill-with-docs.md)**

    ---

    Command: /cs:grill-with-docs <path-to-plan>

-   :material-console:{ .lg .middle } **[`/cs-handoff`](cs-handoff.md)**

    ---

    Command: /cs:handoff <next-session-focus>

-   :material-console:{ .lg .middle } **[`/cs-scrape`](cs-scrape.md)**

    ---

    Run a gated extraction pipeline for $ARGUMENTS using skills/universal-scraping-architect/SKILL.md.

-   :material-console:{ .lg .middle } **[`/cs-workflow-build`](cs-workflow-build.md)**

    ---

    Command: /cs:workflow-build <task-description>

-   :material-console:{ .lg .middle } **[`/cs-write-a-skill`](cs-write-a-skill.md)**

    ---

    Command: /cs:write-a-skill <name-or-description>

-   :material-console:{ .lg .middle } **[`/cs-andreessen`](cs-andreessen.md)**

    ---

    Command: /cs:andreessen

-   :material-console:{ .lg .middle } **[`/cs-pmf-check`](cs-pmf-check.md)**

    ---

    Command: /cs:pmf-check

-   :material-console:{ .lg .middle } **[`/cs-capture`](cs-capture.md)**

    ---

    Command: /cs:capture <dump-text-or-path>

-   :material-console:{ .lg .middle } **[`/cs-inbox-setup`](cs-inbox-setup.md)**

    ---

    Command: /cs:inbox-setup

-   :material-console:{ .lg .middle } **[`/cs-inbox-triage`](cs-inbox-triage.md)**

    ---

    Command: /cs:inbox-triage

-   :material-console:{ .lg .middle } **[`/cs-handoff-setup`](cs-handoff-setup.md)**

    ---

    Configure the handoff skill. Walks 5 questions (plus 1-2 optional) and writes the config. Re-run any time.

-   :material-console:{ .lg .middle } **[`/cs-reflect`](cs-reflect.md)**

    ---

    Command: /cs:reflect

-   :material-console:{ .lg .middle } **[`/cs-landing`](cs-landing.md)**

    ---

    Command: /cs:landing <product-or-brief>

-   :material-console:{ .lg .middle } **[`/cs-dossier`](cs-dossier.md)**

    ---

    Command: /cs:dossier <entity>

-   :material-console:{ .lg .middle } **[`/cs-grants`](cs-grants.md)**

    ---

    Command: /cs:grants <research-idea>

-   :material-console:{ .lg .middle } **[`/cs-litreview`](cs-litreview.md)**

    ---

    Command: /cs:litreview <research question>

-   :material-console:{ .lg .middle } **[`/cs-notebooklm`](cs-notebooklm.md)**

    ---

    Command: /cs:notebooklm

-   :material-console:{ .lg .middle } **[`/cs-patent`](cs-patent.md)**

    ---

    Command: /cs:patent <invention description>

-   :material-console:{ .lg .middle } **[`/cs-pulse`](cs-pulse.md)**

    ---

    Command: /cs:pulse <topic>

-   :material-console:{ .lg .middle } **[`/cs-research`](cs-research.md)**

    ---

    Command: /cs:research <research question>

-   :material-console:{ .lg .middle } **[`/cs-syllabus`](cs-syllabus.md)**

    ---

    Command: /cs:syllabus <syllabus-file-or-paste>

-   :material-console:{ .lg .middle } **[`/cs-bizops`](cs-bizops.md)**

    ---

    Use the cs-bizops-orchestrator agent + business-operations-skills orchestrator skill to handle this inquiry:

-   :material-console:{ .lg .middle } **[`/cs-capacity-plan`](cs-capacity-plan.md)**

    ---

    Run the capacity-planner skill on this input:

-   :material-console:{ .lg .middle } **[`/cs-grill-bizops`](cs-grill-bizops.md)**

    ---

    Apply Matt Pocock's grill-with-docs discipline to this BizOps plan / problem:

-   :material-console:{ .lg .middle } **[`/cs-internal-comms`](cs-internal-comms.md)**

    ---

    Run the internal-comms skill on this input:

-   :material-console:{ .lg .middle } **[`/cs-knowledge-ops`](cs-knowledge-ops.md)**

    ---

    Run the knowledge-ops skill on this input:

-   :material-console:{ .lg .middle } **[`/cs-process-map`](cs-process-map.md)**

    ---

    Run the process-mapper skill on this input:

-   :material-console:{ .lg .middle } **[`/cs-procurement`](cs-procurement.md)**

    ---

    Run the procurement-optimizer skill on this input:

-   :material-console:{ .lg .middle } **[`/cs-vendor-review`](cs-vendor-review.md)**

    ---

    Run the vendor-management skill on this input:

-   :material-console:{ .lg .middle } **[`/cs-channel-econ`](cs-channel-econ.md)**

    ---

    Run the channel-economics skill on this input:

-   :material-console:{ .lg .middle } **[`/cs-commercial-forecast`](cs-commercial-forecast.md)**

    ---

    Run the commercial-forecaster skill on this input:

-   :material-console:{ .lg .middle } **[`/cs-commercial-policy`](cs-commercial-policy.md)**

    ---

    Run the commercial-policy skill on this input:

-   :material-console:{ .lg .middle } **[`/cs-commercial`](cs-commercial.md)**

    ---

    Use the cs-commercial-orchestrator agent + commercial-skills orchestrator skill to handle this inquiry:

-   :material-console:{ .lg .middle } **[`/cs-deal-review`](cs-deal-review.md)**

    ---

    Run the deal-desk skill on this input:

-   :material-console:{ .lg .middle } **[`/cs-grill-commercial`](cs-grill-commercial.md)**

    ---

    Apply Matt Pocock's grill-with-docs discipline to this Commercial plan / problem:

-   :material-console:{ .lg .middle } **[`/cs-partner-tier`](cs-partner-tier.md)**

    ---

    Run the partnerships-architect skill on this input:

-   :material-console:{ .lg .middle } **[`/cs-pricing-strategy`](cs-pricing-strategy.md)**

    ---

    Run the pricing-strategist skill on this input:

-   :material-console:{ .lg .middle } **[`/cs-rfp-respond`](cs-rfp-respond.md)**

    ---

    Run the rfp-responder skill on this input:

-   :material-console:{ .lg .middle } **[`/cs-clinical-research`](cs-clinical-research.md)**

    ---

    Run the clinical-research skill on this input:

-   :material-console:{ .lg .middle } **[`/cs-grill-research-ops`](cs-grill-research-ops.md)**

    ---

    Apply Matt Pocock's grill-with-docs discipline to this plan / problem:

-   :material-console:{ .lg .middle } **[`/cs-market-research`](cs-market-research.md)**

    ---

    Run the market-research skill on this input:

-   :material-console:{ .lg .middle } **[`/cs-product-research`](cs-product-research.md)**

    ---

    Run the product-research skill on this input:

-   :material-console:{ .lg .middle } **[`/cs-research-finance`](cs-research-finance.md)**

    ---

    Run the research-finance skill on this input:

-   :material-console:{ .lg .middle } **[`/cs-research-ops`](cs-research-ops.md)**

    ---

    Route this inquiry through the research-ops-skills orchestrator:

-   :material-console:{ .lg .middle } **[`/cs-design-system`](cs-design-system.md)**

    ---

    Run the design-system wizard:

-   :material-console:{ .lg .middle } **[`/cs-grill-markdown-html`](cs-grill-markdown-html.md)**

    ---

    Walk the user through 5 forcing questions before routing to the converter. One question per turn, with a recommended ...

-   :material-console:{ .lg .middle } **[`/cs-markdown-html`](cs-markdown-html.md)**

    ---

    Route this conversion through the markdown-html-orchestrator skill:

-   :material-console:{ .lg .middle } **[`/cs-md-document`](cs-md-document.md)**

    ---

    Convert the markdown at $ARGUMENTS into a single-file interactive HTML document.

-   :material-console:{ .lg .middle } **[`/cs-md-review`](cs-md-review.md)**

    ---

    Convert the review markdown at $ARGUMENTS into a single-file 2-column HTML review.

-   :material-console:{ .lg .middle } **[`/cs-md-slides`](cs-md-slides.md)**

    ---

    Convert the markdown deck at $ARGUMENTS into a single-file interactive HTML presentation.

</div>
