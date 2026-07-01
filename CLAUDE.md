# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a **comprehensive skills library** for Claude AI and Claude Code - reusable, production-ready skill packages that bundle domain expertise, best practices, analysis tools, and strategic frameworks. The repository provides modular skills that teams can download and use directly in their workflows.

**Current Scope:** 350 production-ready skills across 18 domains with 589 Python automation tools, 717 reference guides, 95 agents (cs-* + 7 personas), and 101 slash commands, distributed as 80 marketplace plugins. Headline counters are derived from the tree by `scripts/derive_counters.py` (run with `--check` to verify the docs still match). **v2.9.0 (complete)** added the **research-ops/** top-level domain — enterprise Research Operations (orchestrator + clinical-research + research-finance + market-research + product-research), the managed counterpart to the academic research/ domain, with `context: fork` orchestration and a Matt Pocock "Forcing-question library" in every SKILL.md plus `/cs:grill-research-ops`. **v2.8.0 (complete)** added 2 new top-level domains — **business-operations/** (7 internal-ops skills: orchestrator + process-mapper + vendor-management + capacity-planner + internal-comms + knowledge-ops + procurement-optimizer) and **commercial/** (8 per-deal-economics skills: orchestrator + pricing-strategist + deal-desk + partnerships-architect + channel-economics + commercial-policy + rfp-responder + commercial-forecaster) — with orchestrator skills using `context: fork` for chaining, Matt Pocock docs-anchored "Forcing-question library" in every SKILL.md, plus `/cs:grill-bizops` and `/cs:grill-commercial`. **v2.8.2** adds a productivity-shaped `handoff` skill (sibling to engineering/handoff) inspired by Matt Pocock — first-run setup with configurable save location, redaction linter, SessionStart + SessionEnd hooks, fidelity self-check, `--refresh` flag. **v2.8.1** upgraded the engineering role-skills (senior-fullstack / senior-frontend / senior-backend) with karpathy-coder + Matt Pocock decision engines + per-role forcing questions. v2.7.3 ports `alirezarezvani/aeo-box` — AEO (Answer Engine Optimization) skill into marketing-skill/ + security-guidance PreToolUse hook into engineering/. v2.7.0 added 13 Path-B skills across 3 top-level domains (productivity, marketing, research). v2.6.0 added 4 Matt Pocock-derived productivity skills.

**Key Distinction**: This is NOT a traditional application. It's a library of skill packages meant to be extracted and deployed by users into their own Claude workflows.

## Maintainer-Local Folders (gitignored)

The following exist on the maintainer's disk but are excluded from the public GitHub tree so cloners only see production skill packages:

- `documentation/` — sprint plans, strategy, implementation roadmaps
- `eval-workspace/` — Tessl evaluation outputs
- `megaprompts/` — pre-skill draft specs (Path-B source material)
- `tests/` — pytest suite (run locally; not in CI)
- `.autoresearch/` — autoresearch agent workspace
- `AUDIT_REPORT.md` — internal audit snapshots

**Distinct from the above:** the top-level `audit/` directory (e.g.
`audit/newgen-2026-06/`) is an **intentional, public** audit record — rubric +
per-domain reports with per-skill verification criteria that follow-up PRs use
as acceptance gates. It is excluded from headline counters by
`scripts/derive_counters.py`, but it is committed and visible to cloners.
`AUDIT_REPORT.md` (gitignored, above) is the older internal-snapshot format.

In-repo references to paths under these folders (e.g. `documentation/implementation/...`) resolve locally for the maintainer but appear as dead links on GitHub. This is intentional.

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
| **Research Operations** | [research-ops/CLAUDE.md](research-ops/CLAUDE.md) | Clinical study design, R&D finance, market research, product research (enterprise counterpart to academic research/) |
| **Markdown → HTML** | [markdown-html/CLAUDE.md](markdown-html/CLAUDE.md) | Markdown-to-interactive-HTML converter (orchestrator + design-system foundation; md-document/review/slides v2.10.1). Inspired by Shihipar's "Claude Code HTML output" essay |
| **Standards Library** | [standards/CLAUDE.md](standards/CLAUDE.md) | Communication, quality, git, security standards |
| **Templates** | [templates/CLAUDE.md](templates/CLAUDE.md) | Template system usage |

## Architecture Overview

### Repository Structure

```
claude-code-skills/
├── .claude-plugin/            # Plugin registry (marketplace.json)
├── agents/                    # 32 standalone agents (cs-* + 7 personas); 51+ cs-* agents repo-wide
├── commands/                  # slash commands (changelog, tdd, saas-health, prd, code-to-prd, plugin-audit, sprint-plan, slo-design, etc.); 87+ repo-wide
├── engineering-team/          # 51 core engineering skills + Playwright Pro + Self-Improving Agent + Security Suite
├── engineering/               # 78 POWERFUL-tier advanced skills (incl. AgentHub, autoresearch-agent, self-eval, llm-wiki, tc-tracker, ship-gate, slo-architect, write-a-skill, caveman, grill-me, handoff)
├── product-team/              # 17 product skills (incl. apple-hig-expert) + Python tools
├── marketing-skill/           # 46 marketing skills (8 pods) + Python tools
├── c-level-advisor/           # 66 C-level advisory skills (full C-suite + founder-mode agents + orchestration)
├── project-management/        # 9 PM skills + bundled Atlassian Remote MCP (.mcp.json)
├── ra-qm-team/                # 18 RA/QM compliance skills
├── compliance-os/             # 9 compliance-OS skills
├── business-growth/           # 5 business & growth skills + Python tools
├── business-operations/       # 7 internal-ops skills (orchestrator + 6 sub-skills)
├── commercial/                # 8 per-deal-economics skills (orchestrator + 7 sub-skills)
├── finance/                   # 4 finance skills + Python tools
├── research/                  # 8 academic research skills (orchestrator + 7 specialists)
├── research-ops/              # 5 research-ops skills (orchestrator + clinical-research + research-finance + market-research + product-research)
├── markdown-html/             # 2 markdown-to-HTML skills v2.10.0 foundation (orchestrator + design-system); md-document/review/slides land in v2.10.1
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

> **⛔ HARD RULE — PR TARGET IS ALWAYS `dev`, NEVER `main`.**
> Every PR (human or AI-created) must use `--base dev`. Nothing merges into `main`
> directly — `main` only receives periodic `dev → main` promotion PRs opened by the
> maintainer. If you find a PR targeting `main`, retarget it to `dev` before review.
> AI agents (Claude Code included): set the base branch explicitly when creating PRs;
> never rely on the repository default branch.

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

**Version:** v2.10.3 (md-slides — slide-deck converter; completes the markdown-html/ domain)

**v2.10.3 highlights — md-slides (markdown deck → single-file HTML presentation):**

Completes the `markdown-html/` domain at 5 skills. The Tier-3 use case from Shihipar's essay ("Slide Decks"): a markdown deck (slides separated by `---` HR boundaries or `# ` H1 headings, with optional `<!-- notes: ... -->` presenter notes blocks) becomes a single-file HTML presentation that runs in any browser with keyboard nav, presenter mode, and print-to-PDF.

- **`md-slides` skill** — three stdlib tools pipeline together (slide_splitter → presenter_notes_parser → deck_html_renderer):
  - **`slide_splitter.py`** — splits markdown on `---` HR or `# ` H1 boundaries (or `--boundary auto`: HR wins ≥ 3, else H1 ≥ 5). Extracts the first heading per slide as the title. Hard rule: refuses 1-slide decks (exit 5 — it's a poster) and no-boundary input (exit 6 — route to md-document). Soft-warns slides > 40 source lines (signal-to-noise; renders anyway).
  - **`presenter_notes_parser.py`** — extracts `<!-- notes: ... -->` blocks (also `speaker-notes:` and `presenter:` aliases) from each slide, attaches as a separate `notes` field, strips from the body so the slide renders cleanly. Tracks `notes_coverage_pct` for the optional `--strict-notes` gate (refuses < 50% coverage).
  - **`deck_html_renderer.py`** — single-file HTML deck. All slides as `<section class="slide">` elements, one visible at a time (CSS-controlled). Vanilla JS keyboard handlers: `→`/`Space`/`PgDn` advance; `←`/`PgUp` previous; `Home`/`End` first/last; `P` toggles presenter mode; `Esc` exits presenter. URL-hash deep linking (`#3` jumps to slide 3, browser back/forward walks slides). Progress bar at top (3px); slide counter bottom-right. Presenter mode = split view: current slide (60% width) + panel (40% width with clock + speaker notes + next-slide preview). `@media print { section { display: block; page-break-after: always; } }` → `Cmd+P` produces PDF with one slide per page. `prefers-reduced-motion` honored. Reuses `md-document/scripts/markdown_parser.py` for slide-body content rendering. Prism.js is **opt-in via `--syntax`** (off by default — most decks don't need it; keeps the file tiny).
- **3 reference docs** each citing 5-7 sources: `presentation_ux.md` (Atkinson *Beyond Bullet Points* + Reynolds *Presentation Zen* + Tufte *Cognitive Style of PowerPoint* + NN/g + Weinschenk + Marp/reveal.js/Big convergence + Tom MacWright), `keyboard_nav_patterns.md` (reveal.js / Big / Spectacle keymap + WCAG 2.1.1 + 2.4.3 + MDN KeyboardEvent + NN/g), `single_file_deck_conventions.md` (Big + Marp + Pandoc + reveal.js standalone + WCAG 2.3.3 + `@media print`).
- **1 template asset** documenting the canonical single-file deck shape.
- **`/cs:md-slides` slash command** with 6 pre-flight gates + pipeline + output digest.
- **Empirical footprint**: 5-slide sample deck (3 with presenter notes) → 12.2 KB single-file HTML with keyboard nav + presenter mode + print-to-PDF. By comparison, equivalent Google Slides / Keynote / reveal.js multi-file exports are 200 KB+ of CSS/JS chrome.
- **Plugin manifest:** `markdown-html-skills` plugin.json `skills` array now lists 5 paths (orchestrator + design-system + md-document + md-review + md-slides). Marketplace counters updated (trued up 2026-06-10 via `scripts/derive_counters.py`): 77 plugins, 17 domains, **345 skills**, **580 Python tools**, **702 references**, **99 slash commands**.
- **Domain status: COMPLETE.** All 5 planned skills shipped across 4 PRs (#780 foundation, #793 md-document, #795 md-review, this PR md-slides). The markdown-html/ domain operationalizes Shihipar's central claim — markdown collapses past 100 lines; HTML restores density, clarity, shareability, and lightweight interaction — across all three layout families (long-form documents, code reviews, slide decks).

---

**Version:** v2.10.2 (md-review — code-review converter for the markdown-html/ domain)

**v2.10.2 highlights — md-review (code-review markdown → 2-col HTML):**

Adds the fourth skill to `markdown-html/`. The Tier-2 use case from Shihipar's essay ("Code Review and PR Writeups"): a markdown PR writeup with ```diff blocks and `> [!BLOCKER]/[!MAJOR]/[!MINOR]/[!NIT]` severity callouts becomes a single-file 2-column HTML review with a top jump-nav, diff on the left, severity-tagged annotation cards on the right, and a mandatory named reviewer footer.

- **`md-review` skill** — three stdlib tools pipeline together (diff_parser → annotation_extractor → review_html_renderer):
  - **`diff_parser.py`** — scans markdown for ```diff fenced blocks, parses each as a unified diff (`--- a/file`, `+++ b/file`, `@@ -10,7 +10,8 @@`, ` ` / `+` / `-` body lines), assigns per-line numbers on both old (`lo`) and new (`ln`) sides, preserves the per-hunk @@ header context. Supports `--infer-diff` for unfenced/language-less blocks. Stdlib regex + state machine.
  - **`annotation_extractor.py`** — extracts severity callouts (GFM `> [!BLOCKER]` style) and inline markers (`nit:`, `blocker:`, etc.). Default convention BLOCKER/MAJOR/MINOR/NIT per Google's *Code Review Developer Guide*; overridable via `--severity-convention "critical,important,suggestion,nit"`. Attaches each annotation to the nearest preceding diff block by source-line index; unanchored annotations go to a "general comments" section. Also captures `LGTM`/`👍`/`approved` markers separately as approvals.
  - **`review_html_renderer.py`** — emits single-file 2-col HTML. Top jump-nav lists every annotation with severity badge + 80-char preview + jump link + counts in heading ("3 BLOCKER · 2 MAJOR · 1 NIT"). Each hunk-row is a CSS grid with diff on the left (per-line numbers, +/− marks, addition/deletion bg tints from `--md-success` / `--md-warn` via `color-mix`) and annotation cards on the right (severity badges that ship color + icon + aria-label + text per WCAG 1.4.1; BLOCKER danger color computed by hue-rotating the design-system accent 120° toward red). Approval bar surfaces when LGTM markers present and no findings. Collapses to stacked on viewports < 900px. Mandatory `--reviewer` (refuses with exit 3 otherwise — research-ops named-owner discipline). Refuses with exit 4 if no hunks present (wrong skill → route to md-document). No Prism CDN (diff coloring conflicts with syntax highlighting).
- **3 reference docs** each citing 5-7 sources: `diff_rendering_canon.md` (POSIX diff + GitHub/GitLab + difftastic + *SWE at Google* ch. 9), `severity_coding.md` (WCAG 1.4.1 + Google review taxonomy + Don Norman *Design of Everyday Things* + NN/g color UX), `pr_annotation_ux.md` (convergent 2-col UX from GitHub/GitLab/Reviewable/CodeStream + *SWE at Google* + NN/g F-shape).
- **1 template asset** documenting the canonical 2-col review HTML shape.
- **`/cs:md-review` slash command** ships the 4 pre-flight gates (under-100-lines, no-onboarding, missing-reviewer, no-hunks) + pipeline + output digest.
- **Empirical footprint**: 2-hunk sample review with 2 annotations → 11.3 KB single-file HTML.
- **Plugin manifest:** `markdown-html-skills` plugin.json `skills` array now lists 4 paths. Marketplace counters updated: 64 plugins, 17 domains, **342 skills** (was 341 after v2.10.1).

**Coming in v2.10.3:** `md-slides` — slide splitter + presenter-notes parser + arrow-key/space-bar nav + `@media print` for PDF export. Reuses `md-document`'s renderer scaffolding + `design-system/scripts/config_loader.py`.

---

**Version:** v2.10.1 (md-document — long-form converter for the markdown-html/ domain)

**v2.10.1 highlights — md-document (long-form markdown → single-file HTML):**

Adds the third skill to `markdown-html/` (foundation shipped in v2.10.0). The 90%-case converter: any markdown spec, plan, RFC, report, or explainer becomes a single-file, lightly-interactive HTML document with the user's onboarded brand.

- **`md-document` skill** — three stdlib tools pipeline together (markdown_parser.py → html_renderer.py → interactivity_injector.py):
  - **`markdown_parser.py`** — CommonMark subset → section AST (headings 1-6 with slug anchors, paragraphs with inline bold/italic/code/links/images, fenced code with language tag, GFM tables with per-column alignment, GFM callouts NOTE/TIP/IMPORTANT/WARNING/CAUTION, blockquotes, ordered + unordered lists, horizontal rules). Stdlib regex + state machine, no `markdown` dependency.
  - **`html_renderer.py`** — section AST + design-system config → single-file HTML. Inlines the 12 derived CSS custom properties from `~/.config/markdown-html/design-system.json`, applies the user's `design_style` (editorial/technical/minimal/playful) via body-class CSS overrides, renders Google Fonts CDN link + Prism.js theme link per `code_theme`, emits sticky-sidebar / collapsible-top / inline / none TOC per `toc.behavior`. Smoke-tested: changing design_style actually changes max-width, line-height, callout shape, and code font-size — customization is in-use, not decorative.
  - **`interactivity_injector.py`** — vanilla-JS payload injected before `</body>`: search filter on H2 sections (Esc clears), code-copy buttons (navigator.clipboard with execCommand fallback), smooth-scroll on TOC links, scrollspy via IntersectionObserver (sets `aria-current="location"` on the matching TOC entry). Idempotent (marker check). Feature subset selectable via `--features search,copycode,smoothscroll,scrollspy`.
- **3 reference docs**, each citing 5-7 sources: `information_density_patterns.md` (Shihipar + Tufte + Wattenberger + Appleton + Ciechanowski + Bret Victor + Jakob Nielsen), `toc_and_nav_ux.md` (NN/g + WCAG 2.2 + ARIA APG + Vitepress/Docusaurus/mdBook convergence + GOV.UK design system + MDN IntersectionObserver), `single_file_html_discipline.md` (Shihipar + Tom MacWright's Big + Google Fonts API + Prism.js + Anil Dash's *The Web We Lost*).
- **1 template asset** (`md_document_template.html`) documenting the canonical output shape for renderer reference.
- **`/cs:md-document` slash command** ships the pre-flight gates + 3-tool pipeline + output digest.
- **Empirical footprint**: ~150-line markdown → 11 KB HTML / 15 KB with JS; ~470-line markdown → 17 KB / 23 KB with JS. By comparison, equivalent Notion/Confluence/GitBook exports are 200 KB+ of CSS chrome.
- **Plugin manifest:** `markdown-html-skills` plugin.json `skills` array now lists 3 paths (orchestrator + design-system + md-document). Marketplace + root CLAUDE.md counters updated: 64 plugins, 17 domains, **341 skills** (was 338 before v2.10.0). Cleans up stale 338/63 counters left by v2.10.0 PR #780.

**Coming in v2.10.2:** `md-review` (2-col diff + severity-tagged margin annotations + jump-nav) and `md-slides` (arrow-key nav + presenter mode + print-to-PDF). Both will reuse `md-document`'s renderer scaffolding and `design-system/scripts/config_loader.py`.

---

**Version:** v2.10.0 (foundation released — `markdown-html/` domain: markdown-to-interactive-HTML converter)

**v2.10.0 foundation highlights — markdown-html/ domain (new top-level domain):**

New `markdown-html/` top-level domain — operationalizes Thariq Shihipar's central claim from his Medium essay *Claude Code HTML output: Why Markdown Lost and How to Switch* (2026): **markdown collapses past ~100 lines for agent-generated artifacts; HTML restores information density, visual clarity, shareability, and lightweight interaction.** Foundation PR (v2.10.0) ships 2 of 5 planned skills; converters land in v2.10.1.

- **`markdown-html-orchestrator`** (`context: fork`) — deterministic doctype classifier scores filename hints (2 points each) + content signals (1 point each) across three lanes (DOCUMENT / REVIEW / SLIDES). Silent-routes when winner ≥ 3 AND (runner-up = 0 OR winner ≥ 2× runner-up); below threshold asks one question with a recommended answer. Three pre-flight refusals: input < 100 lines (Shihipar threshold), design-system not onboarded, output dir unwritable. 3 stdlib tools: `doctype_classifier.py`, `route_explainer.py` (the "never silently chain" enforcer; also gates on design-system status), `output_path_resolver.py` (kebab slug + collision suffix). Canon: Shihipar; Tufte; Bret Victor; Maggie Appleton; Bartosz Ciechanowski; Amelia Wattenberger.
- **`design-system`** — one-time onboarding wizard (10 questions: `default_output_dir`, brand primary/accent HEX, heading + body Google Fonts from 12 safe defaults, design style `editorial/technical/minimal/playful`, syntax theme `light/dark/auto`, TOC behavior `sticky-sidebar/collapsible-top/inline/none`, optional company name + logo URL). WCAG-AA-validated 12-token CSS custom-property palette derived in HSL space — primary's luminance branch decides whether bg = primary (dark-mode docs) or bg = near-neutral light (vibrant primary as accent); link contrast iteratively walked to 4.5:1. 3 stdlib tools: `onboard.py` (interactive + `--defaults/--set/--show/--reset/--scope`), `config_loader.py` (project > global > defaults, deep merge, `MARKDOWN_HTML_NO_CONFIG=1` bypass), `brand_palette_validator.py` (WCAG 2.2 §1.4.3/§1.4.11 + HSL derivation, 12 tokens: `--md-bg/surface/border/text/text-muted/accent/accent-soft/code-bg/link/link-hover/success/warn`). Refuses to save if body-text or link contrast fails AA 4.5:1, or if output dir is unwritable. Canon: WCAG 2.2; Ellen Lupton *Thinking with Type*; Adobe Spectrum; Sara Soueidan accessible color tokens; Material Design 3.
- **`cs-markdown-html-orchestrator` agent + 3 slash commands:** `/cs:markdown-html <path>.md` (router), `/cs:grill-markdown-html <path>.md` (Matt-Pocock 5-question grill, one per turn with recommended answer + canon citation), `/cs:design-system` (surfaces onboarding). Forcing-question library in every SKILL.md.
- **Hard rules:** refuse < 100 lines (Shihipar); refuse without onboarding; refuse unwritable save dir; single-file HTML only (Google Fonts + Prism.js CDN are the only permitted externals; no JS framework runtimes); never silently chain converters; customization must change behavior (not decoration).
- **Coming in v2.10.1:** `md-document` (sticky TOC + collapsibles + search + code-copy + scrollspy), `md-review` (2-col diff + severity-tagged margin annotations + jump-nav), `md-slides` (arrow-key nav + presenter mode + print-to-PDF). All three import `design-system/scripts/config_loader.py` for shared tokens.
- **6 stdlib-only Python tools** (3 per skill, all pass `--help` + `--sample`), **6 reference docs** each citing 5-7 authoritative sources, **1 JSON schema asset** for the customization config. Distinct from Anthropic's official Playground plugin (interactive prompt-tuning controls with sliders/knobs/prompt-copy-back) and from `marketing/landing/` (landing-page generator from scratch).
- **Marketplace + Codex registry:** 63 → 64 plugins; 16 → 17 domains; new `documentation` category.

---

**Version:** v2.9.0 (research-ops/ domain: enterprise Research Operations)

**v2.9.0 highlights — research-ops/ domain (new top-level domain):**

New `research-ops/` top-level domain — the enterprise / cross-functional counterpart to the academic `research/` domain (which finds literature, grants, patents). Single domain plugin (commercial/ + business-operations/ pattern): orchestrator (`context: fork`) + 4 managed sub-skills.

- **`clinical-research`** — prospective clinical STUDY design (not regulatory submission, which stays in `ra-qm-team`). 3 stdlib tools: `sample_size_estimator.py` (closed-form power/n for means/proportions/survival with a built-in z-table, dropout inflation, "ESTIMATE — confirm with a biostatistician" banner), `endpoint_selector.py` (5-dimension scoring → PRIMARY/KEY-SECONDARY/EXPLORATORY, penalizes unvalidated surrogates), `phase_gate_scorer.py` (feasibility 0-100 → GO/GO-WITH-CONDITIONS/REDESIGN/NO-GO + named owner chain). Canon: ICH E8/E9/E9(R1), CONSORT, SPIRIT, FDA Multiple Endpoints, Cohen, Schoenfeld.
- **`research-finance`** — internal R&D PROGRAM/portfolio finance (not corporate close `finance/`, not grant discovery `research/grants`). 3 tools: `program_budget_planner.py` (multi-period budget + F&A/MTDC split + assumptions block), `burn_runway_tracker.py` (trailing burn, runway, milestone-vs-cash), `capex_vs_opex_router.py` (IAS 38 / ASC 730 routing → CAPITALIZE-CANDIDATE/EXPENSE/FINANCE-OWNER-REVIEW, never auto-decides). Canon: IAS 38, ASC 730/985-20, 2 CFR 200, Cooper stage-gate, rNPV.
- **`market-research`** — upstream sizing/survey/segmentation methodology (not campaign analytics `marketing-skill`). 3 tools: `market_sizer.py` (TAM/SAM/SOM both top-down AND bottoms-up + triangulation flag, never a single number), `sample_size_planner.py` (survey n + FPC + per-segment minima), `segmentation_scorer.py` (Kotler 5-criteria + substantiality/accessibility gate). Canon: Cochran, Dillman, Groves, Kotler, Bessemer/a16z sizing.
- **`product-research`** — product/user research method + insight-repository discipline (not persona/journey/live-A-B `product-team`). 3 tools: `study_designer.py` (goal×stage → method + plan skeleton), `saturation_planner.py` (Nielsen-5 / Guest-12 with explicit confidence), `insight_synthesizer.py` (clusters coded observations, flags single-source anecdotes — never promotes them). Canon: Portigal, JTBD, Rohrer (NN/g), Nielsen, Guest et al., ResearchOps/Polaris.
- **Hard rules:** clinical outputs are estimates + named clinical owner (never fact); finance surfaces assumptions and routes treatment to a named finance owner (never auto-decides); market sizes show method + assumptions (never a single number); product insights require recurrence across independent participants. `cs-research-ops-orchestrator` agent + `/cs:research-ops` router + `/cs:grill-research-ops` (Matt docs-anchored grilling) + 4 per-skill commands.
- **Onboarding + customization + autoresearch (per sub-skill, isolated):** each sub-skill ships `onboard.py` (its own question set), `config_loader.py` (a customization config consumed by every tool, project>global>defaults precedence, `RESEARCH_OPS_NO_CONFIG=1` bypass), and `ar_evaluator.py` — an opt-in, locked-ground-truth bridge to `engineering/autoresearch-agent` (loop edits the skill's input file; metrics: clinical `feasibility_composite`↑, finance `runway_months`↑, market `tam_divergence`↓, product `validated_insights`↑). 24 stdlib tools total (12 analysis + 12 onboarding/customization/autoresearch; all pass `--help`/`--sample`), 12 reference docs (5-7 sources each). Marketplace 61 → 62 plugins; domains 15 → 16.

**v2.8.3** shipped the Mistral Vibe cross-platform sync (`scripts/sync-vibe-skills.py`, `~/.vibe/skills/claude-skills/`) — bringing first-class tool support to 13 coding agents.

**v2.8.4 highlights — productivity/andreessen skill, Marc Andreessen-mode:**

New `productivity/andreessen/` plugin — the Andreessen-lens counterpart to a founder-operating-system plugin. A blunt, market-first operator that pressure-tests ventures/ideas/features/career-bets through Andreessen's documented frameworks (market > team > product; product/market fit is the only milestone; bias to build) and runs his 3x5-card + Anti-Todo daily routine.

- **Runs on a fixed anti-sycophancy operating prompt** (user-supplied, preserved verbatim in `references/operating_prompt.md`): leads with the strongest counterargument, never validates premises, no disclaimers, no morals lectures, explicit confidence levels (high/moderate/low/unknown), never apologizes for disagreeing, no capitulation without new evidence. The user's second emphasis block is operationalized as a posture-mapping table so each instruction changes behavior rather than sitting as decoration.
- **3 stdlib deterministic tools:** `market_first_evaluator.py` (market weighted 0.55, sub-4 market is a hard kill gate → BUILD-POUR-FUEL / MARKET-FIRST-DERISK / KILL-OR-REPICK-MARKET), `pmf_signal_scorer.py` (felt-signals + the Sean Ellis 40% gate, labeled as Ellis's not Andreessen's → BEFORE/APPROACHING/AFTER-PMF), `anti_todo_card.py` (3x5 card with enforced 3-5 cap + Anti-Todo log).
- **4 references** (each citing 5-7 sources with explicit confidence levels on every Andreessen attribution, incl. the documented reversal of "don't keep a schedule"), **5 assets** (worked examples + fillable worksheet + blank card), `cs-andreessen` agent, `/cs:andreessen` + `/cs:pmf-check` commands.
- **8-phase plugin audit:** PASS WITH WARNINGS → structure 91.3/EXCELLENT, quality 65.7 (after asset/example additions), scripts 3/3, security PASS (0 critical, 0 high). Marketplace 60 → 61 plugins; productivity domain 5 → 6 skills.

---

**v2.8.2 highlights — productivity/handoff skill, Matt Pocock-inspired:**

Single-skill point release after v2.8.1. New `productivity/handoff/` skill is a sibling to the existing `engineering/handoff/`. Both preserve Matt Pocock's seven-sentence body verbatim; the productivity variant adds the wrappers the engineering port deliberately skipped:

- **First-run setup** (`scripts/setup.py`) — 5-question Q&A. No pre-selected default for save location: user explicitly picks OS temp / home folder / per-project `.handoff/` / custom path on first run. Prompt-once-then-default model: declining setup drops a sentinel so the prompt never re-appears.
- **Redaction linter** (`scripts/redaction_linter.py`) — 17 stdlib regex patterns (AWS / GitHub / OpenAI / Anthropic / Slack / Stripe / JWT / private-key blocks / env-style secret assignments / DB connection strings / bearer tokens / URL token params / email / phone). Strict-by-default with inline `<!-- handoff:allow secret -->` whitelist marker. Operationalizes Matt's redaction sentence.
- **SessionStart auto-load + SessionEnd reminder hooks** — paired routine-integration. SessionStart surfaces latest handoff as `<handoff_from_previous_session>` data; SessionEnd reminds if no handoff in the last 30 minutes. Disable per-session via `HANDOFF_SESSIONSTART=0` / `HANDOFF_SESSIONEND=0`.
- **Mandatory checklist** (`references/handoff_prompt.md`) + **self-check script** (`scripts/handoff_self_check.py`) — 7-step checklist enforced by 6-check script (all 5 sections present, Goal non-empty, State references artifacts, Decisions present when git is dirty, 3-5 Skills with `— why`, Artifacts are paths only). Strict mode exits 1 on high-severity findings.
- **mtime-guarded cleanup** — auto-cleanup never deletes a handoff the user edited as a working surface.
- **`--refresh` flag** — reuses the most recent handoff in the configured location instead of creating a new file; keeps save location uncluttered.

Ships 7 stdlib-only Python tools, 5 reference docs (each citing 5-6 sources), `cs-handoff-author` agent, `/cs:handoff` + `/cs:handoff-setup` commands. Plugin audit (8 phases): structure 86.0/100, quality 63.0/100, security PASS (0 critical, 0 high). 2 PRs merged: #724 (v1.0) + #728 (v1.1).

**v2.8.2 master plan:** in-conversation design + 8-phase audit applied twice (after each PR).

---

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

   No other extras. The `skills` value depends on the plugin layout. Per the live Claude Code plugin spec ([plugins-reference](https://code.claude.com/docs/en/plugins-reference)), **all paths must be relative to the plugin root and start with `./`**. CC 2.1.144+ returns `Validation errors: skills: Invalid input` on a bare string without the prefix.

   **Canonical forms (CC 2.1.144+):**
   - Single-skill plugin (SKILL.md at root): `"skills": ["./"]` (array form required).
   - Plugin with `skills/` subdir: `"skills": "./skills"` or `"skills": ["./skills"]`.
   - Multi-skill domain plugin (skills are subfolders at root): `"skills": ["./sub1", "./sub2", ...]` (explicit list).

   **Legacy form (still tolerated by the validator):** `"skills": "skills"` (bare subdir name, no `./`). Older versions of CC accepted this; current CC rejects it. The repo has been fully migrated to the canonical form — the validator keeps WARN-level tolerance for the legacy literal as a safety net against accidental regressions in copied templates. Do **not** use this form in new manifests.

   **Historical regressions (now reversed upstream):** The `./` prefix was briefly forbidden between CC v2.1.107 and v2.1.144 (issues #539, #686). That window is closed; the `./` prefix is required again. Do **not** reintroduce the bare-string form for new manifests.

   **Enforcement:** `scripts/check_plugin_json.py --all` runs in `ci-quality-gate.yml` on every PR. It hard-fails on any non-`./`-prefixed string that isn't the legacy `"skills"` literal, on empty strings/arrays, and on non-string array entries. When CC tightens its path validator again in the future, update both the validator (`_check_skills_string` / `_check_skills_array`) and this section together — they must move in lockstep.
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

**Last Updated:** June 10, 2026
**Version:** v2.10.3
**Status:** 345 skills deployed across 17 domains, 78 marketplace plugins, docs site live (counters derived via `scripts/derive_counters.py`)
