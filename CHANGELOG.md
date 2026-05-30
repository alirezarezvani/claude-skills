# Changelog

All notable changes to the Claude Skills Library will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] — code-reviewer: C-specific smell detector + fixtures

### Added — language-specific smell pack for C (this PR)

Closes Phase 2 / Tier 1 of the post-#769 audit: brings C onto the same footing as C# and Java for deterministic detection. Until now, `code_quality_checker.py` only had `check_<name>_specific_smells` for C# and Java; C / C++ / Rust / Ruby / PHP / Dart all fell through to generic checks.

- **`check_c_specific_smells()`** in `scripts/code_quality_checker.py` (~110 lines). Detects:
  - **Banned functions** — `gets`, `strcpy`, `strcat`, `sprintf`, `vsprintf` (all no-bounds; CWE-242 and CWE-120 family).
  - **Format-string vulnerability** — `printf(var)` / `syslog(var)` with a bare identifier as the format argument (CWE-134). Skips literal-string first args.
  - **Unbounded `scanf`** — `%s` specifier without a width (CWE-120). Suppressed when a width is present (`%31s`, etc.).
  - **`malloc`/`calloc`/`realloc` without NULL check** — result variable not checked within 5 lines (CWE-690 NULL pointer dereference). Recognises `if (p == NULL)`, `if (NULL == p)`, `if (!p)`, `if (p != NULL)`.
  - **`free()` without zeroing** — pointer not set to `NULL` on the next real line (CWE-416 use-after-free guardrail). Low severity since some style guides skip it.
  - **`system()` with non-literal argument** — command-injection surface (CWE-78). Suppressed when the argument is a string literal or `NULL`.
- Wired into `analyze_file()` after the C# and Java dispatchers.
- **`assets/sample_c_smells.c`** + **`assets/sample_c_clean.c`** — labelled fixtures; every smell is annotated inline with the CWE it maps to. Smells fixture has 10 C-specific detector hits (some rules fire more than once); clean fixture has 0 hits and scores 100/A.
- **`expected_outputs/sample_c_smells_quality.json`** + **`expected_outputs/sample_c_clean_quality.json`** — regression-detection harness following the C# / Java pattern.
- Documentation refreshed: `README.md` adds C to the "Language-specific smell packs" line and the bundled-fixtures table; `SKILL.md` and `docs/skills/engineering-team/code-reviewer.md` update the "Adding a New Language" guide and "Regression Fixtures" section to reference C# + Java + C.

Verification: all 6 fixtures (C# / Java / C × smells / clean) match their committed `expected_outputs/*.json` byte-for-byte. C smells fixture scores 4/100 (F); C clean fixture scores 100/100 (A).

**Not yet (separate PRs):** `check_<name>_specific_smells` for C++, Rust, Python, Kotlin, PHP, Ruby, Dart, Go, Swift, TypeScript, JavaScript (audit-ranked sequence). C++ and Rust are next — security delta is highest there (smart-pointer ownership, `unsafe` block discipline).

---

## [Unreleased] — code-reviewer: 6 new languages + analyzer wiring + doc sync

### Added — language coverage 7 → 13 (PR #769)

Six new language-rule files in `engineering-team/skills/code-reviewer/languages/`. Each follows the established 8-section contract (PR Analyzer Signals / Code Quality Checks / Security / Async / Resource Management / Exception Handling / Performance / Idioms). Contributor: @mitnick2012.

- **`c.md`** — memory safety, banned functions (`gets`, `strcpy`, `sprintf` without bounds), pointer ownership, buffer-bounds discipline, undefined-behavior patterns.
- **`cpp.md`** — smart-pointer ownership transfer, RAII discipline, `reinterpret_cast` audit, missing virtual destructors, C++17/20 idioms.
- **`rust.md`** — `unsafe` block justification, `.unwrap()` in production paths, Tokio runtime pitfalls, `thiserror` vs `anyhow` separation, clippy compliance.
- **`ruby.md`** — Rails-aware: N+1 with `includes`, `strong_parameters`, `YAML.safe_load` vs `YAML.load`, `Marshal.load`, Ruby 3.x idioms.
- **`php.md`** — SQL injection, `unserialize`, `eval`, file inclusion, CSRF, XSS, PHP 8.x idioms (`match`, enums, `readonly`).
- **`dart.md`** — Dart + Flutter unified: widget `dispose()` lifecycle, `BuildContext` across async gaps, `const` widget optimization, state-management patterns.

`SKILL.md` dispatch table and `--language` valid-values comment updated accordingly. No existing language files were modified.

### Fixed — deterministic analyzer wiring (PR #772)

Post-merge audit of PR #769 surfaced a gap: `SKILL.md`'s dispatch table and the `--language` help text both advertised coverage for the 6 new languages, but `scripts/code_quality_checker.py` was never updated — files in those languages were silently skipped by the deterministic analyzer.

Three structures in `code_quality_checker.py` extended (+94 / -1, stdlib-only):

- **`LANGUAGE_EXTENSIONS`** — 6 new dict entries matching `SKILL.md` exactly. `c` declared before `cpp` so plain `.h` resolves to C per the dispatch-table contract.
- **`find_functions` patterns** — language-aware function regexes. C/C++ require a trailing `{` (filters prototypes and call sites) plus negative-lookahead on control-flow keywords. Rust uses the unambiguous `fn` keyword. Ruby handles `def`, `def self.x`, predicate (`?`) / bang (`!`) suffixes, parenthesised-or-bare params. PHP requires the `function` keyword. Dart matches typed-return-then-name with optional `async` / `async*` / `sync*` markers.
- **`find_classes` patterns + nested `method_patterns`** — type-def regexes: `struct` / `typedef struct` for C; `class` / `struct` for C++; `struct` / `enum` / `trait` / `union` for Rust; `class` / `module` for Ruby; `class` / `interface` / `trait` / `enum` for PHP; `class` / `mixin` / `enum` / `extension` with all 5 Dart 3 class modifiers (`abstract` / `sealed` / `final` / `base` / `interface`).

Verification: `python3 scripts/code_quality_checker.py --help` now lists all 14 languages as `--language` choices. Smoke-tested with a minimal sample per new language; each correctly detects functions and classes. All 4 bundled regression fixtures (`csharp`/`java` × `smells`/`clean`) still match their committed `expected_outputs/*.json` byte-for-byte.

**Not yet:** language-specific `check_<name>_specific_smells` detectors for the 6 new languages (only C# and Java have these today). Audit ranked C / C++ / Rust as the next-highest-leverage additions.

### Changed — documentation sync (this PR)

- **`engineering-team/skills/code-reviewer/README.md`** — language list (line 3) and the "Review rules" guide-per-language reference (line 90) updated 7 → 13 languages.
- **`docs/skills/engineering-team/code-reviewer.md`** — MkDocs page synced: frontmatter description, file-tree, dispatch table (6 new rows), and `--language` valid-values comment.
- **Cross-platform sync indexes** — `.gemini/skills-index.json` and `.vibe/skills/claude-skills/skills-index.json` regenerated via `scripts/sync-gemini-skills.py` / `scripts/sync-vibe-skills.py`; `.hermes/skills/claude-skills/skills-index.json` hand-patched (full regen would have bundled 33 unrelated new-skill entries — left for a separate mirror-refresh PR). `.codex/skills-index.json` was already current. All 3 updated mirrors now show the canonical 13-language description from `SKILL.md` frontmatter.

---

## [Unreleased] — Mistral Vibe cross-platform installation (closes #705)

### Added

- **`scripts/sync-vibe-skills.py`** — installs claude-code-skills into [Mistral Vibe](https://github.com/mistralai/mistral-vibe) (Apache-2.0 CLI coding agent). Fork of `sync-hermes-skills.py` with target `~/.vibe/skills/claude-skills/<domain>/<skill>/`, namespaced to avoid collisions with Vibe built-ins. Same flags: `--verbose`, `--domain`, `--dry-run`, `--copy`, `--json`, `--target`.
- **`scripts/vibe-install.sh`** — bash one-liner wrapper for parity with `gemini-install.sh` and `codex-install.sh`. Surfaces Vibe-specific post-install usage tips (`/skills`, `/<slug>`).
- **`.vibe/skills/claude-skills/`** — pre-generated tree committed to the repo: 306 skill symlinks across 14 domains plus a `skills-index.json` manifest. Lets users inspect the install surface without running the script. Mirrors the existing `.hermes/skills/claude-skills/` precedent.
- **`INSTALLATION.md`** — new "Mistral Vibe Installation" section (setup, direct Python invocation, verify, uninstall, Python CLI tools), plus TOC entry and a row in the cross-tool compatibility table.
- **`README.md`** — Mistral Vibe added to the "Works with" line, footnote describing the BYO-sync tier (mirrors the Hermes footnote), row in the Multi-Tool Support table, and FAQ updated from 12 → 13 supported tools.
- **`docs/index.md`, `docs/getting-started.md`, `docs/integrations.md`** — Mistral Vibe install tab added to all three pages, full ~130-line integration section parallel to Hermes section in `integrations.md`, description meta tags updated 12 → 13 AI coding tools.
- **`.claude-plugin/marketplace.json`, `mkdocs.yml`** — platform compatibility taglines updated; all 13 tools named explicitly in `mkdocs.yml`.

### Why

Mistral Vibe (released Jan 2026, v2.0) uses the [Agent Skills spec](https://docs.mistral.ai/mistral-vibe/agents-skills) — exactly the same `SKILL.md` + YAML frontmatter contract this repo already ships. Zero format conversion needed; the integration slots cleanly into the existing 5-target cross-platform sync pattern (`.claude` / `.codex` / `.gemini` / `.hermes` / `.vibe`). Issue [#705](https://github.com/alirezarezvani/claude-skills/issues/705) requested this from @saifjarboui.

---

## [2.8.2] - 2026-05-23 — productivity/handoff skill, Matt Pocock-inspired

Single-skill point release on top of v2.8.1. New `productivity/handoff/` skill is a sibling to the existing `engineering/handoff/` (shipped in v2.6.0). Both preserve Matt Pocock's seven-sentence body verbatim; the productivity variant adds the wrappers the engineering port deliberately skipped.

### Added — `productivity/handoff/` skill (PR #724)

Single-skill plugin. Stdlib-only across the board. 23 files total.

- **`SKILL.md`** — Matt Pocock's seven-sentence body preserved verbatim, surrounded by invocation triggers, output-path discipline, 5-section template (Goal / State / Decisions / Skills / Artifacts), redaction checklist, anti-patterns block in Matt's register, examples, usage table.
- **`scripts/setup.py`** — first-run Q&A. 5 core questions (save location, retention, redaction strictness, git context, recommender scope) plus 2 optional (filename style, project override). **No pre-selected default for Q1**: user explicitly picks OS temp / home folder / per-project `.handoff/` / custom on first run. Prompt-once-then-default model: declining setup drops a sentinel so the prompt never re-appears. `/cs:handoff-setup` re-runs anytime.
- **`scripts/handoff_template_generator.py`** — writes the 5-section scaffold at the configured path. Auto-includes git context (branch, last commit, dirty-file count) when in a repo + enabled in config.
- **`scripts/redaction_linter.py`** — 17 stdlib regex patterns: AWS access keys, AWS secret assignments, GitHub tokens, OpenAI keys, Anthropic keys, Slack tokens, Google API keys, Stripe keys, private-key blocks, JWT, env-style secret assignments, DB connection strings with creds, bearer tokens, URL token params, email, phone, private CIDR. Strict-by-default with inline `<!-- handoff:allow secret -->` whitelist marker. Operationalizes Matt's redaction sentence (which the engineering port left as prose-only).
- **`scripts/skill_recommender.py`** — scans repo SKILL.md files, scores against goal text, returns top 3-5 matches with one-line *why*. Hard cap at 5 — refuses to list more.
- **`scripts/cleanup.py`** — mtime-guarded retention cleanup. **Never deletes a handoff the user edited as a working surface** (data-loss prevention).
- **`scripts/config_loader.py`** — shared helper. Project config → global config → built-in defaults precedence.
- **`hooks/session_start.py`** + **`hooks/hooks.json`** — `SessionStart` hook surfaces latest handoff (within retention window) as `<handoff_from_previous_session>` data. Treated as data, not instructions. Disable via `HANDOFF_SESSIONSTART=0`.
- **`references/handoff_prompt.md`** — mandatory 7-step checklist for the agent. Forces topic-by-topic classification (State / Decision / drop) instead of free-handing prose.
- **`references/handoff_structure.md`** — 5-section template with worked example.
- **`references/deduplication_discipline.md`** — Matt's no-duplication rule made concrete via do-this-not-that pairs.
- **`references/redaction_checklist.md`** — what regex catches + manual-review steps for what regex can't.
- **`references/configuration.md`** — field-by-field config reference.
- **`agents/cs-handoff-author.md`** + **`commands/cs-handoff.md`** + **`commands/cs-handoff-setup.md`**.

### Added — v1.1 improvements (PR #728)

Three follow-up improvements judged most impactful in v1.1 design review.

- **`hooks/session_end.py`** — pairs with SessionStart. When a session ends with no handoff in the last 30 minutes, prints a one-line reminder. Cannot prompt interactively or block session end (Claude Code hook constraint) — surfaces text via stdout. Disable via `HANDOFF_SESSIONEND=0`. `hooks/hooks.json` updated to wire both hooks.
- **`scripts/handoff_self_check.py`** — operationalizes `handoff_prompt.md`. 6 checks: all 5 sections present, Goal non-empty, State bullets reference an artifact (commit hash / PR / file path), Open Decisions present when git is dirty / has recent commits, Skills 3-5 with `— why` explanation, Artifacts are paths/URLs only. Strict mode exits 1 only on high-severity findings (medium issues warn without blocking). Closes the fidelity gap (W3 from the design weakness list).
- **`--refresh` flag** on `handoff_template_generator.py` — reuses the most recent handoff instead of creating a new file. Falls through to create-if-missing when none exists. Keeps the save location uncluttered.
- `/cs:handoff` command flow updated to insert self-check between scaffold-fill and redaction linter.

### Coexists with — `engineering/handoff/`

| Aspect | `productivity/handoff/` (v2.8.2) | `engineering/handoff/` (v2.6.0) |
|---|---|---|
| Primary audience | End-of-day / cross-machine session handoff | Code/PR handoff |
| First-run setup | Yes (5 questions, configurable save location) | No (fixed `mktemp`) |
| Redaction enforcement | Yes (linter + whitelist + strict/warn/off) | No |
| SessionStart auto-load | Yes (hook + retention-aware) | No |
| SessionEnd reminder | Yes (when no recent handoff) | No |
| Mandatory checklist | Yes (handoff_prompt.md, 7 steps) | No |
| Self-check fidelity script | Yes | No |
| Retention cleanup | Yes (mtime-guarded) | No |

Both stay. Cross-referenced in their READMEs.

### Inspired by

[Matt Pocock's handoff skill](https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff) (MIT). Matt's seven-sentence body of `SKILL.md` is preserved verbatim. The wrapper around it (first-run setup, redaction enforcement, hooks, self-check, --refresh, retention) is original work in this repo.

### Audit results

Plugin audit ran twice (after each PR) — final state:

- Phase 2 (structure): **86.0/100 (GOOD)** — above 75 threshold
- Phase 3 (quality): **63.0/100 (C)** — above 60 floor (sibling `capture` scores 46.4 on the same scorer)
- Phase 4 (scripts): **PASS** — 7 scripts, 3 PASS + 4 PARTIAL (sibling `config_loader` import flagged as external — false positive)
- Phase 5 (security): **PASS** — 0 critical, 0 high
- Phase 6 (marketplace): **PASS** — plugin.json valid, marketplace entry at 2.8.2
- Phase 7 (ecosystem): **PASS** — Codex + Gemini indexed, 0 broken internal links
- Phase 8 (code review): **PASS** — all 7 scripts and 2 hooks work end-to-end

### Documentation sync (PR #729)

- `CLAUDE.md` Current Scope: 328 → 329 skills, v2.8.2 Highlights section added, footer bumped.
- `mkdocs.yml` nav: `productivity/handoff` entry added under Productivity.
- `docs/skills/productivity/handoff.md` generated.
- `README.md` badges: Skills 313 → 329, Agents 46+ → 49+, Commands 60+ → 79+. Productivity table row updated to 5 skills (incl. handoff).
- `docs/index.md` + `docs/getting-started.md`: counts and version references updated.
- 0 remaining stale `v2.7.5` references (an earlier version-number typo that this release also corrects).

### Stats

- 328 → 329 skills (productivity: +1)
- 14 domains unchanged
- Plugins in marketplace: 59 → 60
- New artifacts: 23 files in productivity/handoff/

### PRs

- #724 (v1.0 — 5 must-haves)
- #728 (v1.1 — SessionEnd + self-check + --refresh)
- #729 (docs sync)

---

## [2.8.1] - 2026-05-20 — Engineering role-skill upgrade: karpathy-coder + Matt Pocock applied to fullstack / frontend / backend

### Audited and upgraded

The three role-based engineering skills — `senior-fullstack`, `senior-frontend`, `senior-backend` — were audited against the karpathy-coder + Matt Pocock canon already shipping in this repo (`engineering/karpathy-coder`, `engineering/grill-me`, `engineering/grill-with-docs`, v2.8.0 BizOps/Commercial pattern). Three findings drove the upgrade:

1. **Generic role descriptions, not opinionated workflows.** Existing SKILL.md files described capabilities; they did not enforce assumptions, success criteria, or kill criteria.
2. **No customization surface.** A 4-person SaaS startup and a 200-person enterprise read the same recommendations.
3. **No invocation contract.** Other agents/skills could not orchestrate fullstack / frontend / backend lenses via a typed surface.

### Added — per-skill artifacts (21 new files: 7 × 3 skills)

For each of `senior-fullstack`, `senior-frontend`, `senior-backend`:

- `scripts/<role>_decision_engine.py` — stdlib-only deterministic profile picker. Refuses to recommend without the four core assumptions (Karpathy #1). Surfaces kill criteria. Names the human approver chain (never auto-approves).
- `profiles/*.json` × 4 — customization profiles, JSON-loadable, swappable. Users copy one to `<your-org>.json` to override defaults.
- `references/forcing_questions.md` — 7 Matt Pocock forcing questions per skill, one per turn, each with recommended answer + canon citation + kill criterion. 21 forcing questions total across the three roles.
- `references/composition_map.md` — explicit routing table to POWERFUL-tier specialists (api-design-reviewer, database-designer, slo-architect, performance-profiler, a11y-audit, epic-design, apple-hig-expert, etc.).

### Added — 3 orchestrator agents (cs-* with `context: fork`)

- `agents/engineering/cs-fullstack-engineer.md` — walks 7 fullstack questions → decision engine → forks specialists.
- `agents/engineering/cs-frontend-engineer.md` — frontend equivalent.
- `agents/engineering/cs-backend-engineer.md` — backend equivalent.

All three are invokable by other agents via `Agent({subagent_type:"cs-<role>-engineer", prompt:"..."})` — the "invokable by other agents" promise.

### Added — 4 slash commands

- `/cs:fullstack-review <prompt>` — full grill + decision engine + composition routing.
- `/cs:frontend-review <prompt>` — frontend equivalent.
- `/cs:backend-review <prompt>` — backend equivalent.
- `/cs:engineer-grill <plan> [--lane fullstack|frontend|backend|all]` — cross-role 21-question forcing-question runner.

### Augmented — 3 existing SKILL.md files (additive edits only)

Each augmented SKILL.md now has 4 new sections appended:

1. **Assumptions and Verifiable Success Criteria** (Karpathy #1 + #4) — names the four core assumptions + three machine-checkable success criteria.
2. **Customization profiles** — table of the 4 profiles + how to add an org-specific one.
3. **Composition map** — table of which POWERFUL specialist to fork into per sub-concern.
4. **Forcing-question library (Matt Pocock grill)** — summary of the 7 questions + the discipline.
5. **Invocation from other agents and skills** — explicit contract: 3 surfaces.

### Principles enforced

- **Karpathy #1 (Think Before Coding):** every decision engine refuses to run without the four core assumption inputs.
- **Karpathy #2 (Simplicity First):** profiles never auto-recommend microservices unless team size + platform team + bounded-context independence all pass (Newman's MonolithFirst).
- **Karpathy #3 (Surgical Changes):** the upgrade did NOT rewrite existing SKILL.md content. New sections appended; existing tools / references / scaffolding untouched.
- **Karpathy #4 (Goal-Driven Execution):** every recommendation prints verifiable success criteria (latency floor, CWV target, SLO).
- **Matt Pocock grill discipline:** all 21 forcing questions ship with recommended answer + canon citation + kill criterion + one-per-turn rule.

### Verification

- 12/12 profile JSON files parse cleanly (`json.load`).
- 3/3 new Python decision engines pass `--help` and `--sample`, exit code 0.
- 3/3 new cs-* agents have valid YAML frontmatter with required keys (`name`, `description`, `skills`, `domain`, `model`, `tools`, `context: fork`).
- 3/3 agent → skill relative paths resolve from `agents/engineering/`.
- 3/3 slash commands reference their correct cs-* agent.
- Existing SKILL.md content unchanged (additive edits only — Karpathy #3, surgical scope).

### Customization story

Adding org-specific defaults requires zero code changes:

```bash
cp engineering-team/skills/senior-fullstack/profiles/saas-startup.json \
   engineering-team/skills/senior-fullstack/profiles/my-org.json
# Edit constraints + stack_recommendations + named_approver_chain
# Decision engine auto-discovers the new profile via Path.glob('*.json')
```

This is the "world-class customizable plugin" promise: profiles are the customization surface, not code.

### Versions bumped

- `engineering-team/.claude-plugin/plugin.json`: `2.2.3` → `2.8.1`
- `.claude-plugin/marketplace.json`: `engineering-skills` plugin → `2.8.1`

---

## [2.8.0] - 2026-05-19 — business-operations + commercial domains, plugin.json regression fix, auto-release pipeline

### Added

#### `business-operations/` — new top-level domain (Sprint 1 + 2 complete)

Internal-ops skills for BizOps leads, COO direct reports, vendor management, IT ops. Both Sprints ship the orchestrator + 6 sub-skills using `context: fork` to chain without polluting parent context.

- `business-operations-skills` (orchestrator) — routes inquiries to the right sub-skill and returns a digest
- `process-mapper` — BPMN modeling + bottleneck detection + cycle-time analysis (Lean + TOC canon: Womack & Jones, Goldratt, Rother & Shook, Reinertsen, Anderson, Pyzdek, Ohno, Liker)
- `vendor-management` (`context: fork`) — SLA tracking + risk scoring + supplier scorecards (NIST SP 800-161, ISO/IEC 27036, Shared Assessments SIG-Lite)
- `capacity-planner` (Sprint 2) — Erlang-C queueing math for ops teams; NOT engineering capacity (vpe-advisor's lane). Implements full Erlang-C in stdlib Python (~30 lines, log-space to avoid factorial overflow). Canon: Erlang 1909, Little 1961, Hopp & Spearman, Reinertsen, Kingman, ITIL.
- `internal-comms` (Sprint 2) — ADKAR (Prosci) + Kotter 8-step change-comms with magnitude validation (rejects celebratory framing on disruptive, layoff-keywords without disruptive magnitude). 5 tone profiles. Canon: Hiatt, Kotter, Bridges, Schein, Heath brothers, Lencioni.
- `knowledge-ops` (Sprint 2, `context: fork`) — Company SOPs + runbooks + KB hygiene with 5W2H validation. 6 industry profiles. 5 regulatory overlays (SOC2/HIPAA/ISO13485/GDPR/SOX). Canon: Ishikawa (5W2H), Liker (Toyota), Gawande (Checklist Manifesto), ISO 9001, ITIL v4, FDA 21 CFR Part 211, Google SRE Workbook.
- `procurement-optimizer` (Sprint 2) — UNSPSC-aligned spend categorization + supplier consolidation. HARD REFUSAL for tier-1 single-source consolidation without break-glass plan. Canon: A.T. Kearney, Spend Matters, Hackett, BCG, Productiv, Zylo, Vendr.
- Distinct from `business-growth/` (external sales), `c-level-advisor/coo-advisor` (strategic), `engineering/slo-architect` (system reliability), `engineering/llm-wiki` (personal PKM)

#### `commercial/` — new top-level domain (Sprint 1 + 2 complete)

Per-deal-and-packaging economics skills for pricing, deal desk, partnerships, RFP, forecasting. Both Sprints ship the orchestrator + 7 sub-skills.

- `commercial-skills` (orchestrator) — routes commercial inquiries via `context: fork`
- `pricing-strategist` — Van Westendorp WTP analysis (full PSM: OPP/IDP/PMC/PME + RAP, monotonicity screening, N<30 warning) + 5-model picker + 7 packaging anti-pattern detectors. Canon: Ramanujam (*Monetizing Innovation*), Skok, Tunguz, Campbell/ProfitWell, Bessemer, Poyar, Sawtooth.
- `deal-desk` — 5-dim deal scorer + discount approval routing (5-band policy + 4 industry variants) + 10-pattern terms redliner. **Never auto-approves** — every verdict names the human(s). Canon: SaaStr, Winning by Design, OpenView, Forrester, KeyBanc, IACCM/WorldCC.
- `partnerships-architect` (Sprint 2) — 5-tier classifier (REFERRAL/RESELLER/OEM/SI/STRATEGIC with hard floors per tier) + joint GTM + revshare modeler. Canon: Chintagunta, Hessling, Forrester, Moore, Tzuo, MPN, AWS APN.
- `channel-economics` (Sprint 2) — Fully-loaded CTS + 3-lens ROI (Cash / LTV / Marginal) + channel mix optimizer with sensitivity. Canon: Skok, Tunguz, Ramanujam, Kaplan & Cooper, Horngren, McKinsey, BCG.
- `commercial-policy` (Sprint 2) — Data-backed discount matrix (4-dim: ARR × term × payment × strategic) + exception flow with compensating commitments + 10-rule linter (L01-L10 BLOCKER/MAJOR/MINOR). Canon: OpenView, Skok, Tunguz, BVP, KeyBanc, SaaStr, Winning by Design.
- `rfp-responder` (Sprint 2, `context: fork`) — Shipley-method structured RFP/RFI/RFQ response. Parser with NICE>MANDATORY>WEIGHTED precedence + response drafter (HARD RULE: never invent claims for GAP) + winrate predictor with BID/PARTNER-BID/NO-BID verdict. Canon: Shipley Proposal Guide v6, APMP BoK, Sant, FAR, GSA.
- `commercial-forecaster` (Sprint 2) — 4Q-weighted bookings + cohort NRR/GRR + funnel-confidence with MANDATORY assumption disclosure. 3-tier commit/best-case/pipe-only with sandbag/hockey-stick detection. Canon: Skok, Tunguz, OpenView, BVP, Chen, Balfour, Ramanujam.
- Distinct from `business-growth/sales-engineer` (technical sale), `business-growth/contract-and-proposal-writer` (free-form authoring; RFP-responder handles buyer-dictated structured response), `c-level-advisor/cro-advisor` (strategic), `finance/financial-analysis` (close+report, not forward)

#### Matt Pocock grill-with-docs discipline (per user direction)

Every v2.8.0 SKILL.md ships a **"Forcing-question library"** section: 5–7 cited canon-anchored questions, walked one at a time by the orchestrator (or `/cs:grill-bizops` / `/cs:grill-commercial`), each with a **recommended answer** + a **canon citation** + **depth-first decision-tree walking**. Discipline derived verbatim from `engineering/grill-me` + `engineering/grill-with-docs` (Matt Pocock, MIT).

- `/cs:grill-bizops` — Matt Pocock docs-anchored grilling for BizOps workflows
- `/cs:grill-commercial` — same for commercial decisions (pricing, deals, partnerships)
- Plus 15 per-skill slash commands: `/cs:bizops`, `/cs:process-map`, `/cs:vendor-review`, `/cs:capacity-plan`, `/cs:internal-comms`, `/cs:knowledge-ops`, `/cs:procurement`, `/cs:commercial`, `/cs:pricing-strategy`, `/cs:deal-review`, `/cs:partner-tier`, `/cs:channel-econ`, `/cs:commercial-policy`, `/cs:rfp-respond`, `/cs:commercial-forecast`

#### Hard rules per skill (enforced by agent personas + scripts)

- **Pricing**: outputs are model + range, **never a single number** — the human picks the number
- **Deal-desk**: every verdict (incl. APPROVE) names the human approver — **never auto-approves**
- **Forecaster**: every output names the conversion assumption + data window + weighting choice explicitly
- **RFP**: GAP requirements are surfaced for leadership decision — **never invents claims**
- **Partnership**: STRATEGIC tier requires named-account independent-demand evidence
- **Procurement**: tier-1 single-source consolidation **refused without** documented break-glass plan
- **Vendor**: scoring outputs route to a named human reviewer — **never auto-replaces**

#### Sprint 3 — closure (this commit)

Final housekeeping to take v2.8.0 from "Sprint 2 complete" to "release-ready":

- **Cross-platform sync** — `scripts/sync-codex-skills.py`, `scripts/sync-gemini-skills.py`, and `scripts/sync-hermes-skills.py` extended to recognize `business-operations/` and `commercial/` top-level domains. Codex symlinks regenerated for 15 new skills; Gemini index expanded by 30 entries.
- **Docs generation** — `scripts/generate-docs.py` extended with Pass 2 command discovery walking `<domain>/commands/<cmd>.md` (v2.8.0 pattern) AND `<domain>/<skill>/commands/<cmd>.md` (v2.7.0 pattern). Now generates 311 skill pages + 75 agent pages + 69 command pages (was 311 + 73 + 34) across **14 domains**. The previously-missing v2.7.0 commands (capture, pulse, landing, etc.) plus all v2.8.0 commands now have rendered MkDocs pages.
- **MkDocs nav** — `mkdocs.yml` updated with new "Business Operations" and "Commercial" sections (14 sub-skill entries), 2 new orchestrator agents, and 17 new slash commands.
- **Plugin manifest validation** — both `business-operations/.claude-plugin/plugin.json` and `commercial/.claude-plugin/plugin.json` pass `scripts/check_plugin_json.py --all` cleanly (recognized `source` extension field per PR #690).
- **Per-skill audit** — `scripts/audit_skills.py` ran across 329 skills total; all 13 v2.8.0 sub-skills audited with checklist scores 2-5/6 (dominant failure: rule #2 "SKILL.md under 100 lines" — known tension with our deliberate "Forcing-question library" depth; documented as ADVISORY for skills that deliberately expose extended grill discipline).

#### Release automation

- **`.github/workflows/release.yml`** — On every push to `main`, parses CHANGELOG.md and auto-creates a git tag + GitHub Release for the latest version listed. Idempotent (skips if tag already exists). Release notes are extracted from the matching CHANGELOG section.
- **`scripts/extract_release_notes.py`** — Stdlib-only CHANGELOG parser. Extracts the latest version, date, subtitle, and body. Used by the release workflow but also runnable standalone for previewing release notes.

### Fixed

#### Plugin manifest `/doctor` warning — issue #686 (reported by @esoneill)

Claude Code 2.1.133+ rejects `"skills": "./skills"` with a "Path escapes plugin directory" warning, even though `./skills` resolves to a valid subdirectory inside the plugin root. This blocked skill registration for the 9 main marketplace plugins plus 38 sibling sub-plugins.

- **PR #689** — replaced `"skills": "./skills"` with `"skills": "skills"` across all 47 affected `plugin.json` files. Updated `CLAUDE.md` ClawHub publishing constraints to document the new convention.
- **PR #690 (regression prevention)** — `scripts/check_plugin_json.py` now actively rejects any `"skills"` string starting with `"./"` (catches both `"./skills"` and `"./skills/sub"` regressions). Wired into `ci-quality-gate.yml` as a blocking step on every PR. Also recognized `source` and `attribution` as approved extension fields (per CLAUDE.md), and dropped the over-strict `"./"` rejection inside arrays (`["./"]` is the documented single-skill-at-root form). Validator's previous error message was actually recommending `"./skills"` verbatim — a leftover from #539, the *first* round of this same upstream rule tightening — which has been corrected.

This is the second round of the same Claude Code path-validator tightening (round 1 was #539, fixing `"./"` → `"./skills"` at CC v2.1.107). The new validator + CI gate prevents a future round 3 from silently shipping again.

### Maintenance

- **inspect-assets.py** (#684, contributor: @TemaDeveloper) — `--help` now works without Pillow installed
- Codex symlink syncs (automated)

### Stats (final v2.8.0)

- **313 → 328 skills** (+15: business-operations 7 + commercial 8)
- **12 → 14 top-level domains**
- **60 → 77 slash commands** (+17 new `/cs:*` commands)
- **402 → 441 stdlib Python tools** (+39: 13 sub-skills × 3 tools each)
- **542 → 581 reference documents** (+39, each citing ≥7 authoritative sources)
- **46 → 48 cs-* agents** (+2: cs-bizops-orchestrator, cs-commercial-orchestrator)
- **57 → 59 marketplace plugins** (+2: business-operations-skills, commercial-skills)
- **34 → 69 documented slash commands in MkDocs** (+35: previously-orphaned v2.7.0 + all v2.8.0)
- **73 → 75 documented agents in MkDocs** (+2)
- All 39 Python tools pass `--help` and `--sample` smoke tests (exit 0)
- All 39 reference docs cite ≥7 authoritative sources
- 0 external imports (stdlib-only across the board)
- 0 LLM calls in tool scripts (deterministic, repeatable)

## [2.7.3] - 2026-05-17 — aeo-box port: AEO skill + security-guidance PreToolUse hook

### Added

**Ported `alirezarezvani/aeo-box` after a full component audit.** Two new skills, one preserved megaprompt, and a Hermes Agent install/configure walkthrough.

#### `marketing-skill/skills/aeo/` — Answer Engine Optimization

A discipline distinct from SEO. AEO optimizes content for **citation** in LLM-generated responses (ChatGPT, Perplexity, Claude, Gemini, Mistral); SEO optimizes for search rankings. New 8th pod in marketing-skill.

- `aeo_audit.py` — E-E-A-T + structure scoring, 0-100 composite with letter grade. 8 industries with calibrated thresholds (YMYL industries 85+, SaaS/b2b/media 70, ecommerce 65).
- `aeo_optimizer.py` — Content rewriting in 3 modes (conservative/balanced/aggressive). Auto-injects schema.org Article + FAQPage JSON-LD.
- `citation_tracker.py` — Local-first citation ledger at `~/.aeo-data/citations.json`. Stats: count, LLM coverage, velocity, top queries, verdict (EARLY / EMERGING / STRONG).
- 3 references each citing 8 sources: E-E-A-T canon (Google QRG adapted for LLM citation), per-LLM citation patterns (with 73% cross-LLM correlation analysis), AEO-vs-SEO strategic choice.
- `cs-aeo` agent (pragmatic content strategist; refuses fake authority signals) + `/cs:aeo` slash command.

#### `engineering/security-guidance/` — PreToolUse security hook

Ported from David Dworken (@dworken) at Anthropic (MIT). PreToolUse hook that catches 12 security anti-patterns in Edit/Write/MultiEdit operations **before** they're written:

| Pattern | Upstream | Added in this port |
|---|:-:|:-:|
| `child_process.exec` / `execSync` | ✓ | |
| `new Function` | ✓ | |
| `eval(` | ✓ | |
| `dangerouslySetInnerHTML` | ✓ | |
| `document.write` | ✓ | |
| `.innerHTML =` | ✓ | |
| `pickle` | ✓ | |
| `os.system` | ✓ | |
| GitHub Actions workflow injection | ✓ | |
| `subprocess shell=True` | | ✓ |
| SQL via f-string or `.format` | | ✓ |
| `yaml.unsafe_load` | | ✓ |

Session-state caching prevents nagging (warn once per file+rule combo); 30-day auto-cleanup; disable per-session with `ENABLE_SECURITY_REMINDER=0`. Full `attribution` block in plugin.json credits the upstream.

#### `megaprompts/14-aeo-agentic-megaprompt.md`

1,579-line multi-agent AEO application spec preserved verbatim. Keeps Path-B option open for future "build the full agentic AEO app" work.

#### `docs/integrations.md` — Hermes Agent install/configure walkthrough

Earlier user-flagged docs gap: nowhere did the repo tell users HOW to install Hermes Agent itself (only how to install our skills INTO Hermes). Added macOS/Linux/Windows install paths, complete first-run walkthrough, sample `~/.hermes/config.yaml`, and a 6 Q&A troubleshooting section.

### Changed

- **Marketplace**: 55 → 57 plugins. Top-level + metadata descriptions updated to v2.7.3 / 313 skills.
- **Domain plugin.json**: `marketing-skill/.claude-plugin/plugin.json` description updated from "44 skills across 7 pods" → "45 skills across 8 pods" (adds AEO pod). Version bumped 2.2.3 → 2.7.3.
- **CLAUDE.md**: root + marketing-skill CLAUDE.md refreshed to 313/402/542 counts.
- **README.md**: badges (313 / 46+ / 60+), Skills Overview table row counts, FAQ counts.
- **docs/index.md + getting-started.md + mkdocs.yml**: title, meta description, hero subtitle, grid cards, nav entries.
- **MkDocs**: 401 → 403 generated pages (296 skill + 73 agent + 34 command).

### Layout fix (during /plugin-audit Phase 7)

- Moved `marketing-skill/agents/cs-aeo.md` → `agents/marketing/cs-aeo.md` (repo convention: agents live at root `agents/<domain>/`).
- Moved `marketing-skill/commands/cs-aeo.md` → `commands/cs-aeo.md` (repo convention: commands live at root `commands/`).
- Cleaned empty `marketing-skill/agents/` and `marketing-skill/commands/` directories.
- Without this fix, `scripts/generate-docs.py` wouldn't have generated docs/agents/cs-aeo.md or docs/commands/cs-aeo.md.

### Cross-platform sync

- `.codex/skills-index.json`: 303 → 305 skills.
- `.gemini/skills-index.json`: 353 → 355 items.
- `.hermes/skills/claude-skills/skills-index.json`: 305 skills across 12 domains.

### Honest assessments from /plugin-audit (both skills)

**aeo**: PASS WITH WARNINGS — structure 86.4/GOOD, quality 52.4/D (validator expects legacy frontmatter fields v2.7 skills don't use), 3/3 scripts PASS, 2 HIGH security findings (NET-EXFIL from `urllib.request` — same known false-positive as sister `seo-audit` skill; URL fetch is core functionality for content-audit-by-URL tools).

**security-guidance**: PASS WITH WARNINGS — structural mismatch (validators assume `scripts/` layout, hook plugins use `hooks/` per Claude Code spec), 6 CRITICAL + 4 HIGH security findings are all recursive false-positives (the auditor detects the hook's own pattern-strings like `"exec("`, `"eval("`, `"yaml.load("` as actual calls — verified zero real exec/eval calls). Live smoke test: `eval(input())` in Write tool → exit 2 + warning. **Real defects: 0.**

### PRs

#678 (Hermes first-class integration) → #679 (aeo-box port + Hermes install guide) → this PR (v2.7.3 release: docs sync + layout fix + CHANGELOG + audit).

### Verification

- All 4 new Python tools pass `--help` and `--sample`.
- Security hook smoke-tested: exit 2 on detection, exit 0 on cached/clean.
- All 3 cross-platform syncs ran clean.
- MkDocs build: exit 0, 450 HTML pages generated.

---

## [2.7.0] - 2026-05-16 — v2 megaprompt-to-skill conversion sweep: 13 new skills (productivity + marketing + research)

### Added — 13 Path-B Skills From `megaprompts/`

This release ships the complete v2 megaprompt collection (`megaprompts/01-13`) as production-ready skills using the **Path-B direct-conversion pattern**: each megaprompt's body becomes the SKILL.md verbatim, wrapped in the standard 11-file plugin layout (`.claude-plugin/plugin.json`, README, agent, command, SKILL.md, 3 references citing 7+ sources each, 3 stdlib Python scripts).

Three new top-level domain folders were created to host the 13 skills:

| Domain | Skills | Build pattern |
|---|---|---|
| `productivity/` | `capture`, `email` (paired: inbox-setup + inbox-triage), `reflect` | Personal-productivity slices — single-action intake, KB-file contract between pair |
| `marketing/` | `landing` | Single-file HTML landing-page generator with 4 design styles |
| `research/` | `pulse`, `litreview`, `grants`, `dossier`, `patent`, `syllabus`, `notebooklm`, `research` (orchestrator) | 7 research-pack siblings + 1 hybrid router |

**13 skills, 142 files, 23,698 lines of code + documentation.** All scripts stdlib-only. All references cite 7+ authoritative sources.

#### Productivity slice (3 skills)

- **`productivity/capture/`** (PR #659) — Brain-dump-to-action workspace. Classify→cluster→connect→clarify intake. Path-B from megaprompt 05.
- **`productivity/email/`** (PR #661) — Email-workflow skill pair. `inbox-setup` builds taxonomy/KB; `inbox-triage` classifies + drafts (drafts-only, never auto-send). 7-file KB contract between them. Path-B from megaprompts 06+07.
- **`productivity/reflect/`** (PR #668) — Light-prompt reflection sibling of capture. Path-B from megaprompt 08.

#### Marketing slice (1 skill)

- **`marketing/landing/`** (PR #662) — Single-file HTML landing-page generator. 4 design styles, brand palette validator, GSAP animation patterns, kebab-slug URL hygiene. Path-B from megaprompt 04.

#### Research pack (8 skills — 7 specialists + 1 orchestrator)

- **`research/pulse/`** (PR #660) — Multi-source recency research (Reddit/HN/X/web sentiment + trending). Research-pack convention. Path-B from megaprompt 01.
- **`research/litreview/`** (PR #663) — Academic literature orientation. PICO/SPIDER frameworks, systematic review structure, 8-section DOCX guide. Path-B from megaprompt 09.
- **`research/grants/`** (PR #664) — NIH grant-funding intelligence. RePORTER/NOSI/study-section navigation, R01/R21/K-award strategy. Path-B from megaprompt 11.
- **`research/dossier/`** (PR #664) — Decision-grade entity research. Due-diligence/background-check/competitor-prep with tier-weighted verdict + citation tracker. Path-B from megaprompt 02.
- **`research/patent/`** (PR #666) — Patent prior-art + IP landscape. FTO/novelty/family-resolver via 3-pass Jaccard heuristic. Path-B from megaprompt 12.
- **`research/syllabus/`** (PR #666) — Course supplementary-reading skill. Topic-grouper + bundled Node.js DOCX generator. Path-B from megaprompt 10.
- **`research/notebooklm/`** (PR #669) — Google NotebookLM browser-automation. 4 actions (read/extract, add-source, Studio outputs, create notebook). Screenshot-first + find-before-click + fire-and-notify discipline. Path-B from megaprompt 03.
- **`research/research/`** (PR #671) — **Research orchestrator (hybrid router + fallback).** Deterministic SIGNALS classification routes to the 6 specialists above at ≥2-signal confidence, else runs own 8-step plan-decompose-search-synthesize-cite fallback. Routing transparency mandatory. Distinct from `engineering/autoresearch-agent` (Karpathy's file-optimization loop). Path-B from megaprompt 13.

### Added — Marketplace + Codex Registry

- **`.claude-plugin/marketplace.json`**: 43 → 55 plugins. 12 new entries (email-pair holds 2 skills) across 3 categories. New categories added: `productivity`, `research`.
- **`.codex/skills-index.json`**: 290 → 303 entries. 13 new skills indexed with category metadata.
- **`.codex/skills/` symlinks**: 11 new symlinks created (capture + pulse already existed from prior auto-sync).
- **`scripts/sync-codex-skills.py`**: Added `productivity/`, `marketing/`, `research/` to `SKILL_DOMAINS` so future auto-sync runs pick up the new top-level domains.

### Path-B Convention (Documented)

This release formalizes the **Path-B direct-conversion** pattern for future megaprompt-derived skills:

- Megaprompt body → SKILL.md preserving content verbatim
- 11-file standard plugin layout (12 files for skills with bundled JS DOCX generators like syllabus)
- 3 stdlib Python scripts per skill (no external deps)
- 3 reference docs per skill, each citing 7+ authoritative sources
- `cs-*` agent + `/cs:*` command per plugin
- `source` field in `plugin.json` documents `spec` (megaprompt path) + `build_pattern` + `distinct_from` (where disambiguation needed)

### Verification

- **39/39 scripts pass `--help`** across all 13 skills
- **8-phase plugin audit** on `research/research`: PASS WITH WARNINGS (structure 84.1/GOOD, scripts 3/3, security 0 findings)
- **Spot-check audit** on pulse / litreview / notebooklm: all 86.4/GOOD, 3/3 scripts, security PASS
- **Bulk audit** on remaining 9 skills: all 79.5-86.4 structure, 0 critical/high security findings (1 false positive in syllabus on a user-facing `npm install docx` error-message string literal)
- **Cross-skill consistency**: 7/7 research-pack siblings carry the `Agent Integrity Rules` block (1 q/sec rate limit, three-count tracking, retry-once-after-3s, source discipline)
- **Orchestrator disambiguation**: `distinct_from autoresearch-agent` callouts present in plugin.json + README + SKILL.md + agent + command (5 places)

### PRs

#659 (capture), #660 (pulse), #661 (email pair), #662 (landing), #663 (litreview), #664 (grants+dossier), #666 (patent+syllabus), #667 (domain-folder cleanup), #668 (reflect), #669 (notebooklm), #671 (research orchestrator), #672 (v2.7.0 release prep — this commit).

## [2.6.1] - 2026-05-14 — Meta-skill maturity: validator expansion + 21 placeholder descriptions + audit tool

### Added — Tooling

- **`scripts/audit_skills.py`** (`./scripts/audit_skills.py`) — repo-wide write-a-skill validator runner. Stdlib-only orchestration that walks every SKILL.md in the repo, runs `skill_review_checklist_runner.py` against each, and aggregates results (PASS/WARN/FAIL counts, failure-by-rule breakdown, top-10 worst offenders). Excludes auto-generated tool bundles (`.gemini/`, `.codex/`, `.cursor/`, `.cline/`) and template fixtures. ~30s to run across 298 real skills. Merged via #646.

### Fixed — Validator False Positives

The v2.6.0 validators recognized only `Use when`, `Use for`, `Invoke when`, `Trigger when` as valid trigger phrases. But legacy skills had semantically-valid natural-English triggers like `Use before annual GDPR review` (gdpr-audit-prep). Expanded trigger patterns to include:

- `Use before/during/after/while ...`
- `Invoke before/after ...`
- `Apply when ...`
- `Run when/before ...`

**Impact: 30 legacy skills reclassified from FAIL → WARN/PASS automatically.** Karpathy `complexity_checker`: 100/100 PASS on both modified validators (`skill_description_validator.py` + `skill_review_checklist_runner.py`). Merged via #647.

### Fixed — 21 Placeholder Descriptions

The v2.6.0 audit revealed 21 skills (~7% of repo) whose description field was literally just the skill name (e.g., `description: "Migration Architect"`). These were real bugs from a v2.0.0 batch import. All 21 fixed in this release.

**Top-10 POWERFUL-tier engineering skills (merged via #647):**
- `migration-architect` — zero-downtime migration planning + rollback strategy
- `dependency-auditor` — vulnerabilities + license + safe-upgrade audit
- `codebase-onboarding` — codebase analysis + onboarding doc generation
- `ci-cd-pipeline-builder` — pragmatic CI/CD from project stack signals
- `mcp-server-builder` — MCP servers from OpenAPI contracts (Python + TS)
- `observability-designer` — metrics + logs + traces + SLI/SLO design
- `api-design-reviewer` — REST design review + breaking-change detection
- `performance-profiler` — Node/Python/Go profiling + flamegraphs + load tests
- `changelog-generator` — Conventional Commits → release notes automation
- `runbook-generator` — operational runbooks from service name + templates

**Remaining 11 across 4 domains (merged via #648):**
- `executive-mentor/skills/challenge` — pre-mortem plan analysis
- `executive-mentor/skills/board-prep` — adversarial board prep
- `git-worktree-manager` — parallel feature work with Git worktrees
- `skill-tester` — meta-skill QA (structure + script + quality scoring)
- `monorepo-navigator` — Turborepo / Nx / pnpm / Lerna navigation
- `env-secrets-manager` — env-var hygiene + secrets rotation
- `agent-workflow-designer` — production-grade multi-agent workflows
- `incident-commander` — incident response framework
- `email-template-builder` — React Email + provider integration
- `stripe-integration-expert` — subscriptions + webhooks + billing
- `contract-and-proposal-writer` — jurisdiction-aware business documents

Each new description: ≤1024 chars, third person, action verb in first sentence, "Use when ..." trigger in second sentence per Matt Pocock's rule.

### Changed — Quality Gates Reference

Updated `engineering/write-a-skill/skills/write-a-skill/references/quality_gates_for_skills.md` to formalize the **binding-for-new vs advisory-for-legacy split**. The 6-item checklist remains BLOCKING for post-v2.6.0 skills and ADVISORY for the 298 legacy SKILL.md files.

Why: forcing the gate as blocking would either delay every PR or require disabling the gate. The pragmatic split lets the repo grow the PASS count over time without force-marching 298 retrofits.

### Aggregate Audit Improvement

Against the 298 real-skill cohort (excludes auto-generated bundles):

| Metric | v2.6.0 baseline | v2.6.1 (now) | Δ |
|---|---|---|---|
| ✅ PASS (6/6) | 4 (1%) | **9 (3%)** | **+5** |
| 🟡 WARN (5/6) | 111 (37%) | **137 (46%)** | **+26** |
| 🔴 FAIL (≤4/6) | 183 (61%) | **152 (51%)** | **-31** |
| "Missing trigger" failures | 119 (39%) | **68 (23%)** | **-51** |

**31 skills total lifted from FAIL → WARN/PASS in v2.6.1.**

### PRs in v2.6.1

- #646 — `scripts/audit_skills.py` repo-wide audit harness
- #647 — validator trigger expansion + 10 placeholder description fixes + legacy advisory
- #648 — closes out remaining 11 placeholder description fixes

### What's Next (Not in This Release)

- **v2.6.2 candidate:** 27% terminology drift (agent/bot, skill/tool mixing). Larger scope; requires careful prose edits.
- **v2.7 candidate:** large-scale audit against the 100-line ceiling. 88% of legacy skills exceed it. Decide which top-20 high-traffic skills to refactor with `references/<topic>.md` splits.

## [2.6.0] - 2026-05-13 — Matt Pocock productivity skills: write-a-skill + caveman + grill-me + handoff

### Added — Engineering / Productivity (4 new skills, all MIT-licensed derivations)

- **write-a-skill** skill (`./engineering/write-a-skill/`) — skill-author meta-skill derived from [Matt Pocock's write-a-skill](https://github.com/mattpocock/skills/tree/main/skills/productivity/write-a-skill) (MIT). Matt's SKILL.md content + 3-phase workflow (Gather → Draft → Review) preserved verbatim per his MIT license.
  - **3 stdlib Python validation tools**: `skill_description_validator.py` (5-check verdict: present, ≤1024 chars, third person, "Use when" trigger, action verb in first sentence), `skill_structure_validator.py` (6-check verdict: SKILL.md present + ≤100 lines, references when split needed, one-level-deep, no circular refs, scripts/ folder note), `skill_review_checklist_runner.py` (combined 6-item runner per Matt's checklist).
  - **4 references** (7-8 sources each): progressive disclosure principles (Matt, Anthropic, Don Norman, Pirolli & Card, Maeda, DocOps, Pareto), description design patterns (Matt, Anthropic, Garrett, Nielsen Norman, Karpathy, SEO), quality gates (Matt, Humble & Farley, Kim et al., Hyrum's Law), companion tooling.
  - **cs-skill-author** persona agent (forcing-question interrogator).
  - **`/cs:write-a-skill`** slash command (6-question forcing interrogation mirroring Matt's review checklist).

- **caveman** skill (`./engineering/caveman/`) — token-compression mode derived from [Matt Pocock's caveman](https://github.com/mattpocock/skills/tree/main/skills/productivity/caveman) (MIT). Matt's persistence rules + auto-clarity exception preserved verbatim.
  - **3 stdlib Python tools**: `caveman_compressor.py` (deterministic application of Matt's rules — drop articles/filler/pleasantries/hedging, abbreviate technical terms, causality arrows; 20-50% typical reduction, 75% upper bound), `token_savings_estimator.py` (chars/token heuristic for prose vs technical text + $/Mtok cost extrapolation), `caveman_lint.py` (detects banned vocab with code-block + exception-zone whitelisting).
  - **3 references** (7-8 sources each): compression principles (Matt, Strunk & White, Plain Language Movement, Pinker, Williams, Anthropic, tokenizer heuristics), when caveman backfires (Matt, NN/g, FAA cockpit-warning research, Krug, Schneier, Larson), companion tooling.
  - **cs-caveman-mode** persona agent (persistence-enforced operator).
  - **`/cs:caveman`** slash command.

- **grill-me** skill (`./engineering/grill-me/`) — relentless plan-interrogator derived from [Matt Pocock's grill-me](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me) (MIT). Matt's one-at-a-time interview discipline preserved verbatim.
  - **3 stdlib Python tools**: `decision_tree_extractor.py` (6 branch kinds: intent / choice / open / tradeoff / dependency / question), `question_generator.py` (forcing questions with recommended answers + dependency-aware ordering), `grill_session_tracker.py` (JSON-backed state in `~/.grill_sessions/` for multi-day grills).
  - **3 references** (7-8 sources each): forcing-question patterns (Matt, Socratic Method, YC office-hours, 5 Whys, Cockburn, Popper, Galef, Larson), when to stop grilling (Matt, Galef, Kahneman, Bezos Type 1/2 decisions, YC Founder School, Cynefin), companion tooling.
  - **cs-grill-master** persona agent (one-question-at-a-time enforcer with codebase-exploration-first discipline).
  - **`/cs:grill-me`** slash command.

- **handoff** skill (`./engineering/handoff/`) — conversation-continuity generator derived from [Matt Pocock's handoff](https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff) (MIT). Matt's no-duplication discipline + `mktemp` convention preserved verbatim.
  - **3 stdlib Python tools**: `handoff_template_generator.py` (5-section scaffold tailored to 5 next-session emphases: deploy/review/debug/design/test/default; honors Matt's `mktemp -t handoff-XXXXXX.md`), `artifact_deduplicator.py` (detects PRD/ADR/issue/commit/long-code-block duplication with reference suggestions), `skill_recommender.py` (matches handoff content to 14 skills in this repo, ranked by signal strength).
  - **4 references** (7-8 sources each): handoff structure (Matt, DRY, runbook patterns, Atlassian, GitHub PR conventions, Anthropic, Kim et al.), deduplication discipline (Matt, Hunt & Thomas, Fowler, DocOps, Karpathy LLM Wiki, git-as-source-of-truth, Stripe API versioning), next-session skill matching (Matt, Anthropic, TF-IDF/BM25, recommender systems, Karpathy, Hyrum's Law), companion tooling.
  - **cs-handoff-author** persona agent (no-duplication-tolerated).
  - **`/cs:handoff <next-session-focus>`** slash command with argument-hint per Matt's convention.

### Attribution

All four skills derive from [Matt Pocock's MIT-licensed skills repo](https://github.com/mattpocock/skills) — *"Skills for Real Engineers. Straight from my .claude directory"*. Matt's SKILL.md content reproduced verbatim under MIT. Attribution in every file: README.md + plugin.json `attribution` block + SKILL.md frontmatter metadata + agent + command + reference footers.

### The Pattern (Hybrid Voice Approach)

This release establishes the pattern for deriving MIT-licensed external skills into this repo:

1. **Preserve upstream voice verbatim** in SKILL.md
2. **Add wrapper layer**: stdlib Python validation tools + 3-4 references (each citing ≥ 5 authoritative sources) + cs-* persona agent + /cs:* slash command
3. **Karpathy-coder gate** before merge (complexity_checker + assumption_linter)
4. **Attribution discipline** in plugin.json + README + every file footer

### Verified

- **12 Python tools** total: 100/100 complexity across all (0 findings) — karpathy `complexity_checker` PASS
- **13 references** total: 7-8 authoritative sources each (well over the ≥ 5 floor)
- **All 4 SKILL.md** PASS write-a-skill's own 6-item review checklist (the meta-skill dogfooded)
- **SKILL.md sizes**: 144 (write-a-skill, wrapper preserves Matt's full content), 69 (caveman), 58 (grill-me), 41 (handoff) — three of four under Matt's 100-line ceiling; write-a-skill documented exception (verbatim preservation overhead)
- **pytest**: 1,921 tests passing
- **CI**: PR 2 caught the missing H1 issue via `test_skill_integrity.py` (test suite worked as designed); fixed in a follow-up commit before merge

### Documented Trade-offs

- **assumption_linter false positives** on `caveman_compressor.py`, `caveman_lint.py`, `artifact_deduplicator.py`, `handoff_template_generator.py`, `skill_recommender.py`: the linter flags banned-vocabulary strings (just, simply, fix, refactor, of course) that appear inside the tools' DATA dictionaries — these strings exist precisely to be detected. Documented as expected; no code change.
- **caveman compression ratio**: Matt's stated "~75%" is the upper bound on extremely verbose responses with multiple pleasantries + filler + hedging. Realistic compression on typical mid-conversation text is 20-50%. Documented in `compression_principles.md`.

### PRs

- PR #642 — write-a-skill alone (merged 2026-05-13)
- PR #643 — caveman + grill-me + handoff batch (merged 2026-05-13)

## [2.5.7] - 2026-05-13 — Docs site refresh: nav additions, dual-publish dedup, 301 redirects

### Added

- **5 new C-role docs pages** added to `mkdocs.yml` nav (C-Level Advisory section): General Counsel Advisor, Chief Data Officer Advisor, Chief AI Officer Advisor, Chief Customer Officer Advisor, VP Engineering Advisor.
- **13 new cs-* agent docs pages** added to `mkdocs.yml` nav (Agents section): cs-cfo / cs-cmo / cs-cro / cs-cpo / cs-coo / cs-chro / cs-ciso / cs-chief-of-staff / cs-general-counsel / cs-cdo / cs-caio / cs-cco / cs-vpe.
- **`mkdocs-redirects` plugin** added to `mkdocs.yml` plugins list. Provides client-side redirects (meta-refresh + JS fallback) — Google's SERP indexing treats meta-refresh with delay=0 as 301-equivalent.

### Fixed

- **`scripts/generate-docs.py` dedup bug:** the auto-generator created BOTH `<name>.md` (bundled) AND `<name>-<name>.md` (standalone wrapper) for dual-published skills, producing duplicate-content pages. The dedup now detects the dual-publish pattern (`<domain>/<name>/skills/<same-name>/SKILL.md` paired with `<domain>/skills/<name>/SKILL.md`) and skips the standalone mirror in favor of the bundled (canonical) version.
- **4 pre-existing engineering dual-publish duplicate pages deleted** with 301-equivalent redirects:
  - `skills/engineering/chaos-engineering-chaos-engineering.md` → `skills/engineering/chaos-engineering.md`
  - `skills/engineering/feature-flags-architect-feature-flags-architect.md` → `skills/engineering/feature-flags-architect.md`
  - `skills/engineering/kubernetes-operator-kubernetes-operator.md` → `skills/engineering/kubernetes-operator.md`
  - `skills/engineering/slo-architect-slo-architect.md` → `skills/engineering/slo-architect.md`
  - All 4 old URLs redirect to the canonical page; existing Google SERP indexes preserved.

### Changed

- **`mkdocs.yml` `site_description`** — updated from "246 skills, 20 cs-* agents" (6 versions stale) to current "268 skills, 33 cs-* agents (incl. founder-mode C-suite), 21 /cs:* slash commands."
- **`README.md`** — header counts updated: 246 → 268 skills; 20 → 33 agents; 33 → 54 commands; 359 → 373 Python tools. Subtitle expanded with founder-mode lineup callout.
- **`.github/workflows/static.yml`** — install step updated from `pip install mkdocs-material` to `pip install mkdocs-material mkdocs-redirects` to support the new plugin.

### Verified

- `mkdocs build` succeeds (357 HTML pages generated)
- Redirect HTML correctly emitted with `<meta http-equiv="refresh" content="0; url=...">` + JavaScript fallback that preserves URL anchors
- karpathy `diff_surgeon`: clean on staged diff
- 71 pre-existing skill pages preserved (no SEO equity loss)

### Pre-existing (not addressed in this PR)

13 INFO-level link warnings exist from before this session (broken anchors and relative-link-without-index hints). These are pre-existing in the docs and not introduced or worsened by this PR. Tracked as a separate cleanup if desired.

## [2.5.6] - 2026-05-13 — Cleanup: missing voice specs + broken agent paths

### Fixed

- **3 missing voice specs added to `c-level-advisor/c-level-agents/references/persona-voices.md`:**
  - `cs-ceo-advisor` — The Strategic Translator (tree-of-thought reasoning; refuses to debate tactics until the strategic question is named)
  - `cs-cto-advisor` — The Architecture-First Pragmatist (ReAct reasoning; treats every architecture decision as a 3-year commitment)
  - `cs-general-counsel-advisor` — The Risk-Paranoid Lawyer (Not Your Lawyer) — carry-over from v2.5.1
  - All three agents existed but their voice specs were never added to the persona reference (cs-ceo / cs-cto pre-date the c-level-agents plugin; cs-gc was an oversight in v2.5.1).
- **Broken paths fixed in 2 pre-existing agent files** (`agents/c-level/cs-ceo-advisor.md` and `agents/c-level/cs-cto-advisor.md`):
  - All 57 references to `../../c-level-advisor/ceo-advisor/` and `../../c-level-advisor/cto-advisor/` updated to `../../c-level-advisor/skills/ceo-advisor/` and `../../c-level-advisor/skills/cto-advisor/` respectively (correct path; the bundled skills live under `skills/`)
  - YAML `skills:` field also corrected (was `c-level-advisor/ceo-advisor`, now `c-level-advisor/skills/ceo-advisor`)
- **karpathy-coder/diff_surgeon:** clean on staged diff

### Why

Both gaps were carry-over items noted across multiple PRs in this session (v2.5.1 → v2.5.5) per karpathy principle #3 (surgical scope — no unrelated cleanups inside scoped feature PRs). This dedicated cleanup PR addresses them in one focused change without touching any feature work.

### Changed

- `c-level-advisor/c-level-agents/references/persona-voices.md` — 13 → 13 voice specs cataloged (all cs-* agents in the persona-voices list now match the agents that exist)
- `agents/c-level/cs-ceo-advisor.md` — 32 path corrections
- `agents/c-level/cs-cto-advisor.md` — 25 path corrections

No skill/agent/command count changes; no manifest version bumps (this is a pure-fix PR).

## [2.5.5] - 2026-05-13 — vpe-advisor: throughput-first VP of Engineering

### Added — C-Level Advisory

- **vpe-advisor** skill (`./c-level-advisor/skills/vpe-advisor/`) — opinionated throughput-first VP of Engineering skill. Fifth decision-driven C-role skill in the founder-mode lineup (after GC, CDO, CAIO, CCO). Covers four specific decisions distinct from CTO:
  1. **Are we delivering at the right throughput?** (DORA 4 metrics + bottleneck identification)
  2. **How do we scale the eng hiring funnel?** (7-stage funnel + pipeline gap + weakest-stage fix)
  3. **What's our eng team structure — when to add a tech-lead manager?** (squad/tribe + manager-trigger + span-of-control)
  4. **What's our production discipline?** (on-call, deployment cadence, postmortem culture, SLO discipline — reference-only)
- **Critical distinction enforced:** VPE is NOT a CTO skill. CTO owns *what to build* (architecture, scaling cliffs, build-vs-buy). VPE owns *how to ship it* (delivery operations, hiring execution, team structure, production discipline). At early stage these are often the same person; at scale they're distinct roles.
- **3 stdlib Python tools with deterministic logic:**
  - **`delivery_throughput_analyzer.py`** — Returns DORA 4 metrics (Deployment Frequency, Lead Time for Changes, MTTR, Change Failure Rate) with Elite/High/Medium/Low verdict per metric and overall. Cycle-time bottleneck identification (top wait stage as % of cycle) with typical fixes per bottleneck (review queue, CI flakiness, deploy gates, scheduled releases). Embedded sample (30-day Platform Squad, 28 deploys) → overall High; bottleneck = first_review_to_approval at 45.8% of cycle.
  - **`eng_hiring_funnel_calculator.py`** — Stage-by-stage conversion rates for 7-stage funnel (Applied → Sourcer → Recruiter → Hiring Mgr → Tech → Onsite → Offer → Accept) with healthy/leaky verdict per stage. End-to-end conversion rate, required top-of-funnel volume for hiring target, weakest-stage identification with fixes (sourcing channel diversification, calibration, interview design, comp/close discipline). Embedded sample (Q2 2026, 4-engineer hiring target) → 0.62% end-to-end, gap of 160 candidates, weakest = offer_extended_to_offer_accepted at 60%.
  - **`eng_team_structure_designer.py`** — Recommended structure (informal pods / formal squads / squads+tribes / multi-tribe) based on headcount. Squad sizing assessment (5-9 IC healthy range). Manager-trigger (first EM at 5-7 ICs; EM-overstretched > 10 ICs; EM-underutilized < 4 ICs). Director-trigger (3+ EMs reporting directly to VPE/CTO). Embedded sample (25-engineer team, 22 ICs / 3 EMs / 1 CTO) → 4-squad structure, no EM trigger (3 EMs for 22 ICs = healthy 7.3 per EM), director trigger FIRES (3 EMs report directly to CTO).
- **4 in-depth references each citing 5+ authoritative sources:**
  - `delivery_throughput.md` — Full DORA framework with thresholds + 4 common bottlenecks + what to fix first (lead time → failure rate → frequency → MTTR) + 4 anti-patterns. Cites Accelerate (Forsgren/Humble/Kim), Google State of DevOps annual report, The Phoenix Project, Reinertsen Flow, Newman Microservices, Humble Continuous Delivery, Atlassian/GitHub/GitLab benchmarks.
  - `engineering_hiring_funnel.md` — 7-stage funnel + healthy conversion benchmarks + leakage diagnosis per stage + pipeline volume math + sourcing channel diversification + technical interview design + cost-per-hire. Cites LinkedIn Talent Insights, Atlassian Recruiting Ops, Levels.fyi + Pave, Lou Adler "Hire With Your Head", Adler/Bock "Work Rules!", CMU/Booth interview validity research, SHRM surveys.
  - `eng_team_structure.md` — Conway's Law + headcount-to-structure map + span-of-control benchmarks + EM vs tech lead distinction + manager/director/VPE triggers + squad sizing + chapter discipline. Cites Kniberg "Scaling Agile @ Spotify", Kniberg 2020 retrospective, Will Larson "Elegant Puzzle", Camille Fournier "Manager's Path", Conway 1968, Schwartz "A Seat at the Table", Lencioni "Five Dysfunctions", Stripe/Shopify/GitHub/Netflix engineering blogs.
  - `production_discipline.md` — On-call rotation design (≥ 6 people; burnout signals) + incident response (4-tier severity, IC role, blameless postmortems) + deployment cadence (continuous vs scheduled; progressive delivery) + SLO discipline integration + 5-level maturity model. Cites Google SRE (Beyer/Jones/Petoff/Murphy), SRE Workbook, John Allspaw postmortem writings, PagerDuty Incident Response docs, Charity Majors observability, Nora Jones chaos engineering, Mikey Dickerson reliability hierarchy.
- **cs-vpe-advisor** agent (`./c-level-advisor/c-level-agents/agents/cs-vpe-advisor.md`) — throughput-first operator. Voice: "What's your cycle time, and where does the work spend most of its time waiting?" Trusts DORA metrics over vibe. Refuses to recommend hires without naming the throughput or quality bottleneck they unblock.
- **`/cs:vpe-review`** slash command (`./c-level-advisor/c-level-agents/skills/vpe-review/SKILL.md`) — 6-question forcing interrogation: cycle time + waits, DORA verdict, hiring funnel leakage, team structure health, production discipline maturity, VPE-vs-CTO scope decision.
- **cs-vpe-advisor voice spec** added to `persona-voices.md`.
- **Dual-published from the start:** standalone plugin at `c-level-advisor/vpe-advisor/` with mirrored content (per #624 pattern). `sync_skill_bundles.py` keeps both copies aligned.

### Why This Matters

The single most-asked staffing question at Series B is: "Do we need a VPE separately from the CTO?" This skill makes the decision mechanical:

- If CTO is spending > 50% on management vs strategy, VPE is needed
- If CTO is a co-founder more comfortable with strategy than execution, VPE complements
- At small scale (< 20 eng), one person can do both — but the operating decisions still need to be made

Existing skills don't quite own these decisions: cs-cto-advisor is about architecture; cs-engineering-lead is day-to-day incident coordination; cs-chro-advisor owns hiring SYSTEMS company-wide but not eng-specific funnel execution. VPE fills the gap with deterministic frameworks for delivery operations.

### Built with Karpathy-Coder Discipline (5th Consecutive PR)

Maintained the discipline established in v2.5.2:

- **Principle 1:** assumptions surfaced upfront, including the critical CTO-vs-VPE distinction. Locked direction before code.
- **Principle 2:** rejected generic "engineering operations survey" framing. Each tool/reference covers ONE decision. No overlap with engineering tactical skills (`engineering/slo-architect/`, `engineering/feature-flags-architect/`, etc.).
- **Principle 3:** touched only files in the locked plan. No "while I'm here" cleanup. No edits to other c-level skills.
- **Principle 4:** all 3 Python tools smoke-tested with embedded samples before commit. Verifiable outputs (DORA overall High; hiring gap +160 candidates; 25-eng team → 4 squads, director trigger fired).

### Changed

- **Total skills:** 267 → 268 (+1 vpe-advisor)
- **cs-* agents:** 32 → 33 (+1 cs-vpe-advisor in c-level-agents plugin)
- **/cs:* slash commands:** 20 → 21 (+1 /cs:vpe-review)
- **Python tools:** 370 → 373 (+3 in vpe-advisor/scripts/)
- **References:** 502 → 506 (+4 in vpe-advisor/references/)
- **Marketplace plugins:** 38 → 39 (+1 standalone vpe-advisor entry)
- **c-level-skills** plugin: v2.5.4 → v2.5.5 (description expanded; 32 → 33 skills, 12 → 13 cs-* agents)
- **c-level-agents** plugin: v1.4.0 → v1.5.0 (description expanded with VPE; new agent + command; +`vp-engineering`, `vpe`, `dora`, `delivery-throughput`, `engineering-hiring`, `eng-team-structure`, `production-discipline` keywords)

### Known follow-ups (NOT in this PR per surgical scope)

- `cs-general-counsel-advisor` voice spec still missing from `persona-voices.md` (carried from v2.5.1; multi-PR carry-over)
- Phase 2 final remainder (1 role): CCO-comms (Chief Communications Officer) — naming conflict with CCO (Chief Customer Officer); needs disambiguation before adding

### Disclaimer

DORA benchmarks come from cross-industry research; specific thresholds shift with stage and complexity. Hiring funnel benchmarks vary by role level + geography. This skill provides operating-baseline guidance; pair with cs-cto-advisor (architecture), cs-chro-advisor (hiring systems), and engineering tactical skills for execution.

## [2.5.4] - 2026-05-13 — chief-customer-officer-advisor: retention-obsessed CCO

### Added — C-Level Advisory

- **chief-customer-officer-advisor** skill (`./c-level-advisor/skills/chief-customer-officer-advisor/`) — opinionated, retention-obsessed CCO skill. Fourth decision-driven C-role skill in the founder-mode lineup. Covers four specific decisions (not generic CS survey):
  1. **What's our retention architecture — and is gross retention vs NRR honest?** (decomposition + 7-category churn taxonomy)
  2. **How do we segment customers for differential investment?** (4-tier framework + ICP fit scoring + kill list)
  3. **What's the CS team's coverage model — and when do we go pooled vs named?** (ratio math + manager trigger)
  4. **What CS role do we hire next?** (stage-to-role map; CSM ≠ Support ≠ AM ≠ IM)
- **3 stdlib Python tools with deterministic logic:**
  - **`retention_decomposition_analyzer.py`** — Decomposes ARR retention by cohort into GRR (truth) / NRR (vanity if alone) / Logo Retention separately. Flags leaky-bucket pattern (NRR > 100% AND GRR < 85%). Categorizes churn across 7-category root-cause taxonomy (product_fit / competitor_loss / no_value_realized / pricing / champion_left / company_event / tactical_failure) and computes preventable % (CS-controllable). Embedded sample: 2 cohorts, Q1 GRR 91.7% CONCERNING (NRR too low at 106.7%), Q2 GRR 84.7% CRITICAL (declining trend), top driver = product_fit at 54.5% preventable.
  - **`customer_segmentation_designer.py`** — Assigns 4-tier segment (Strategic / Enterprise / Mid-market / SMB-long-tail) by ARR. Scores ICP fit 0-10 from 7 weighted signals (industry, size, workflow, exec sponsor, advocacy, expansion potential, competitor concentration). Surfaces kill list (support cost > 50% of ARR AND ICP fit < 5) with the 3 paths (non-renewal / downgrade-to-tech-touch / raise-price). Surfaces upgrade candidates (high fit + expansion potential).
  - **`cs_coverage_calculator.py`** — Calculates required CSM headcount per tier with two constraints (ARR ratio AND account count, whichever is binding). Surfaces manager-trigger thresholds (5+ ICs in tier OR 8+ across function). Generates 12-month hiring plan with quarterly sequencing. Includes fully-loaded cost projection.
- **4 in-depth references each citing 5+ authoritative sources:**
  - `retention_decomposition.md` — GRR vs NRR honest math + leaky-bucket pattern + 7-category churn taxonomy + leading-indicator playbook + cohort discipline. Cites Mehta/Steinman/Murphy "Customer Success", Lincoln Murphy, David Skok (forEntrepreneurs), BVP State of the Cloud, ChartMogul/ProfitWell benchmarks, Reichheld "The Loyalty Effect", Tomasz Tunguz.
  - `customer_segmentation_strategy.md` — 4-tier framework + ICP fit weighting (7 signals) + tier transition triggers + kill list criteria + the 3 paths. Cites Lincoln Murphy, Bain "Loyalty Effect", Tunguz, Skok, ChartMogul/ProfitWell, Adamson/Dixon/Toman "Challenger Customer".
  - `cs_coverage_model.md` — Tech-touch / pooled / named / named+exec models + ARR-per-CSM ratios by stage and segment + manager-trigger + CS comp design + ramp curves. Cites Gainsight, TSIA, Mehta/Pickens "Customer Success Economy", ChurnZero, Skok, Lincoln Murphy, Pacific Crest/KeyBanc SaaS survey.
  - `cs_team_org_evolution.md` — 5-stage role map + 6-role definition table (CSM ≠ Support ≠ AM ≠ IM ≠ CS Ops ≠ Customer Marketing) + AM-vs-CSM split decision + 7 anti-patterns. Cites Mehta/Steinman/Murphy, Mehta/Pickens, BVP, TSIA, Gainsight, ChurnZero, Lincoln Murphy.
- **cs-cco-advisor** agent (`./c-level-advisor/c-level-agents/agents/cs-cco-advisor.md`) — retention-obsessed pragmatist. Voice: "What's your gross retention rate, and what's the #1 reason customers leave?" Trusts gross retention over NRR. Refuses to recommend CS hires without naming the customer outcome they unblock.
- **`/cs:cco-review`** slash command (`./c-level-advisor/c-level-agents/skills/cco-review/SKILL.md`) — 6-question forcing interrogation: GRR (not NRR), top churn driver, time-to-value, kill-list candidates, ARR-per-CSM ratio + coverage model, CS comp alignment.
- **cs-cco-advisor voice spec** added to `persona-voices.md`.
- **Dual-published from the start:** standalone plugin at `c-level-advisor/chief-customer-officer-advisor/` with mirrored content (per the same pattern as #624 for GC/CDO/CAIO). `sync_skill_bundles.py` keeps both copies aligned.

### Why This Matters

By 2026, every B2B SaaS founder is being asked a board-level question: "What's your NRR?" The truth is that NRR alone is the vanity metric — it can hide a leaky bucket where 85% gross retention is masked by expansion from the survivors. This skill enforces the discipline of decomposition before reporting, and surfaces three decisions the other C-roles can't quite own:

- **CRO** owns the revenue math (NRR, expansion comp, ramp); **CCO** owns customer *experience* and the 7-category churn root cause analysis. Clean split.
- **CPO** owns product roadmap; **CCO** surfaces product gaps via churn data. CPO decides; CCO feeds.
- **CHRO** owns CS team comp; **CCO** designs the coverage model + ratios. CHRO executes; CCO designs.

The differential-investment framework (kill list + upgrade candidates) is the strategically distinct CCO contribution. Most founders avoid the kill-list conversation; this skill makes it mechanical.

### Built with Karpathy-Coder Discipline (fourth consecutive PR)

Maintained the discipline established in v2.5.2:

- **Principle 1:** assumptions surfaced upfront, including the CRO vs CCO split assumption (revenue math vs customer experience). Locked direction before code.
- **Principle 2:** rejected generic "customer success survey" framing. Each tool/reference covers ONE decision. No overlap with `business-growth/customer-success-management/`.
- **Principle 3:** touched only files in the locked plan. No "while I'm here" cleanup of unrelated files. No edits to other c-level skills.
- **Principle 4:** all 3 Python tools smoke-tested with embedded samples before commit. Verifiable outputs (Q1 GRR 91.7% CONCERNING / Q2 GRR 84.7% CRITICAL; 5 customers tiered with 1 kill + 2 upgrade candidates; 4 → 12 CSMs / $2.25M annual cost at 40% growth).

### Changed

- **Total skills:** 266 → 267 (+1 chief-customer-officer-advisor)
- **cs-* agents:** 31 → 32 (+1 cs-cco-advisor in c-level-agents plugin)
- **/cs:* slash commands:** 19 → 20 (+1 /cs:cco-review)
- **Python tools:** 367 → 370 (+3 in chief-customer-officer-advisor/scripts/)
- **References:** 498 → 502 (+4 in chief-customer-officer-advisor/references/)
- **Marketplace plugins:** 37 → 38 (+1 standalone chief-customer-officer-advisor entry)
- **c-level-skills** plugin: v2.5.3 → v2.5.4 (description expanded; 31 → 32 skills, 11 → 12 cs-* agents)
- **c-level-agents** plugin: v1.3.0 → v1.4.0 (description expanded with CCO; new agent + command; +`chief-customer-officer`, `cco`, `retention-decomposition`, `customer-segmentation`, `cs-coverage` keywords)

### Known follow-ups (NOT in this PR per surgical scope)

- The `cs-general-counsel-advisor` voice spec is still missing from `persona-voices.md` (carried from v2.5.1). Will be addressed in a separate small PR.
- Phase 2 remainder (2 more C-roles: VPE engineering execution, CCO-comms) deferred to v2.5.5+.

### Disclaimer

Retention benchmarks vary significantly by ACV, segment, and industry. This skill provides B2B SaaS-baseline guidance; consumer SaaS, marketplaces, and hardware have materially different retention math.

## [2.5.3] - 2026-05-12 — chief-ai-officer-advisor: AI strategy with citations

### Added — C-Level Advisory

- **chief-ai-officer-advisor** skill (`./c-level-advisor/skills/chief-ai-officer-advisor/`) — opinionated, eval-demanding CAIO skill covering 4 specific decisions. The third decision-driven C-role skill in the founder-mode lineup, after general-counsel-advisor (v2.5.1) and chief-data-officer-advisor (v2.5.2).
- **4 specific decisions covered** (not a generic AI strategy survey):
  1. **Should we use an API, fine-tune, or build our own?** (model build-vs-buy with 3-year TCO)
  2. **Is this AI use case high-risk under regulation, and how do we govern it?** (EU AI Act + NIST AI RMF + US state patchwork)
  3. **When do we switch from API to self-hosted, and at what cost?** (token economics with breakeven analysis)
  4. **What AI role do we hire next?** (stage-to-role map; AI engineer ≠ ML engineer ≠ research scientist)
- **3 stdlib Python tools with deterministic logic**:
  - **`model_buildvsbuy_calculator.py`** — Returns API / FINE_TUNE / BUILD recommendation, 3-year TCO across 6 path variants (API frontier-premium/economy/open-hosted, fine-tune, self-hosted 70B-class, build-from-scratch), and breakeven analysis. Balances economic crossover with practical feasibility (data availability, ML team capacity, compliance constraints). Embedded sample (B2B customer support, 4M queries/mo) → API recommendation despite economic breakeven crossed, due to no fine-tune data + 1-engineer ML team.
  - **`ai_risk_classifier.py`** — Returns EU AI Act tier (PROHIBITED / HIGH / LIMITED / MINIMAL) with Article-level citations, US state triggers (NYC LL 144, CO AI Act, IL HB 53, CA SB 1001, IL BIPA), industry overlays (FDA AI/ML, ECOA, NAIC AI bulletin), required-controls list, and conformity-assessment flag. Embedded sample (AI hiring screening in EU+NY+CO+IL+CA) → HIGH risk, conformity required, 3 US state triggers, 14 controls. 7 EU AI Act articles cited (5, 6, 9-15, 43, 49, 72).
  - **`ai_cost_economics.py`** — Returns monthly costs at 6 paths (3 API tiers + self-hosted at low/mid/high GPU rates), breakeven monthly tokens, sensitivity to GPU pricing. Embedded sample (5M tokens/day, 750M/mo) → API at $1,500/mo beats self-hosted at $13,450/mo by 9x; breakeven at 6.7B tokens/mo for 70B-class on A100s. Reveals key insight that self-hosted floor (24/7 warm GPUs + ops) makes API economics dominate at typical B2B SaaS scale.
- **4 in-depth references each citing 5+ authoritative sources**:
  - `model_buildvsbuy_strategy.md` — 3 paths with failure modes, 6 fine-tuning approaches (few-shot, prompt eng, RAG, LoRA, full FT, RLHF/DPO, continued pre-training) ranked by cost and use case, decision tree, eval-first discipline. Cites Anthropic/OpenAI/Google/Meta model cards, LoRA paper (Hu et al.), RLHF paper (Ouyang et al.), DPO paper (Rafailov et al.), Foundation Models report (Stanford CRFM), Foundation Models and Fair Use (Henderson et al.).
  - `ai_risk_governance.md` — Full EU AI Act tier map (prohibited Article 5, high-risk Article 6 + Annex III, limited-risk Article 50, minimal-risk) with all 8 high-risk domains + 11 obligation Articles. NIST AI RMF 1.0 (4 functions, 7 trustworthy characteristics). US state patchwork (NYC LL 144, CO AI Act, IL HB 53, CA SB 1001, CA AB 2013, CA AB 1008, IL BIPA, WA MHMD, TX biometric). Industry overlays (FDA, CFPB, Fed SR 11-7, NYDFS Reg 23, ECOA, NAIC). 10-item governance program checklist. When-to-hire-AI-counsel criteria.
  - `ai_cost_economics.md` — 2026 API pricing across 4 tiers, GPU rental (A100/H100/H200/B200), throughput estimates, GPU count by model size, cost-per-million-tokens calculations, utilization reality (interactive 20-40%, batch 60-80%), 6 hidden costs of self-hosted, 6 hidden costs of API, migration cost (3-6 months, 2-3 engineers), prompt caching as economics lever. Cites vLLM paper, DistServe (NSDI 2024), HELM benchmark, Artificial Analysis, Llama 3.1 paper.
  - `ai_team_org_evolution.md` — 5-stage role map (pre-seed → late-stage), 9-role definition table distinguishing AI engineer / ML engineer / research scientist / data scientist / AI safety / AI PM / Head of AI / CAIO. AI team vs data team contrast (8 dimensions). 7 specific anti-patterns. Hiring sequencing rule. Cites Huyen "Designing ML Systems" + "AI Engineering", State of AI Report, Karpathy's AI engineer archetype discussions.
- **cs-caio-advisor** agent (`./c-level-advisor/c-level-agents/agents/cs-caio-advisor.md`) — eval-demanding realist orchestrating the skill. Voice: "What does this AI need to be good at, and how would you measure it?" Treats every AI use case as a hiring decision; pushes back on AI hype; demands fallback behavior before scale.
- **`/cs:caio-review`** slash command (`./c-level-advisor/c-level-agents/skills/caio-review/SKILL.md`) — 6-question forcing interrogation: eval discipline, hallucination SLO, regulatory tier, model selection, cost trajectory, role-that-unblocks-this.
- **cs-caio-advisor voice spec** added to `persona-voices.md`.

### Why This Matters

By 2026, every founder is making AI decisions that didn't exist 18 months ago — and gstack, general legal counsel, CTOs, and CISOs each only cover part of the picture. The CAIO concerns that this skill uniquely owns:

1. **Model build-vs-buy is not a single answer.** 80% of B2B SaaS should use frontier APIs; 15% should fine-tune; <1% should pre-train. The decision depends on data availability + team capacity + economics + compliance, not on technology preference.
2. **EU AI Act conformity is consequential and slow.** A high-risk AI use case requires 3-12 months of conformity work + EU database registration + 10 Articles of obligations. Discovering this 2 weeks before EU launch is a category of pain this skill prevents.
3. **API vs self-hosted breakeven is much higher than founders expect.** For 70B-class on rented A100s, breakeven is typically 1-10 billion tokens per month — not the 100M-500M most founders intuit. Self-hosting "to save money" usually wastes engineering capacity.
4. **AI team confusion costs 12 months of productivity.** Hiring a research scientist as first AI hire is the single most common AI hiring mistake, and it's expensive to undo.

### Built with Karpathy-Coder Discipline

Maintained the discipline established in v2.5.2:

- **Principle 1 (Think before coding):** assumptions surfaced upfront before file writes. Locked 4 decisions, 3 tools, 4 references, success criteria. User confirmed direction.
- **Principle 2 (Simplicity first):** rejected "generic AI strategy survey" framing. Each tool covers ONE decision. Each reference answers ONE decision. No overlap with engineering/rag-architect, engineering/agent-designer, engineering/llm-cost-optimizer.
- **Principle 3 (Surgical changes):** touched only files in the locked plan. No "while I'm here" cleanup.
- **Principle 4 (Goal-driven execution):** all 3 tools smoke-tested with embedded samples before commit. Verifiable success criteria met.

### Changed

- **Total skills:** 265 → 266 (+1 chief-ai-officer-advisor)
- **cs-* agents:** 30 → 31 (+1 cs-caio-advisor in c-level-agents plugin)
- **/cs:* slash commands:** 18 → 19 (+1 /cs:caio-review)
- **Python tools:** 364 → 367 (+3 in chief-ai-officer-advisor/scripts/)
- **References:** 494 → 498 (+4 in chief-ai-officer-advisor/references/)
- **c-level-skills** plugin: v2.5.2 → v2.5.3 (description expanded; 30 → 31 skills, 10 → 11 cs-* agents)
- **c-level-agents** plugin: v1.2.0 → v1.3.0 (description expanded with CAIO; new agent + command; +`chief-ai-officer`, `caio`, `ai-strategy`, `model-buildvsbuy`, `eu-ai-act`, `ai-cost-economics` keywords)

### Known follow-ups (NOT included this PR per surgical scope)

- The `cs-general-counsel-advisor` voice spec is still missing from `persona-voices.md` (carried from v2.5.1). Will be addressed in a separate small PR.
- Phase 2 remainder (3 more C-roles: CCO customer, VPE engineering execution, CCO comms) deferred to v2.5.4+.

### Disclaimer

The `chief-ai-officer-advisor` skill surfaces strategic AI decisions but is **not legal advice** for AI regulation, **not a replacement for outside AI counsel** for EU AI Act conformity assessments, and **not a tactical AI/ML engineering skill**. For tactical AI engineering, see `engineering/rag-architect/`, `engineering/agent-designer/`, `engineering/prompt-governance/`, `engineering/self-eval/`, `engineering/llm-cost-optimizer/`.

## [2.5.2] - 2026-05-12 — chief-data-officer-advisor: data strategy without surveys

### Added — C-Level Advisory

- **chief-data-officer-advisor** skill (`./c-level-advisor/skills/chief-data-officer-advisor/`) — opinionated, decision-driven CDO skill. Refuses to be a generic data-governance survey; instead answers four specific decisions:
  1. **Can we train our model on this data?** (AI training data rights matrix)
  2. **Warehouse, lakehouse, or mesh — and what do we build vs buy?** (data product strategy)
  3. **What is our customer data worth?** (B2B customer-data-as-asset valuation + M&A multiplier)
  4. **What data role do we hire next?** (data team org evolution)
- **3 stdlib Python tools with deterministic logic** (not pattern-match prose):
  - **`ai_training_data_audit.py`** — Audits data sources on 3 dimensions (origin × data class × use case). Returns GO/MITIGATE/NO-GO per source with risk, remediation, and GDPR Art. 6 + EU AI Act + US state citations. Embedded sample tests 7 sources spanning all 3 verdicts. Implements 6+ rule branches (scraped always NO-GO, regulated requires framework-specific consent, PII for fine-tuning requires explicit opt-in, etc.).
  - **`data_product_strategy_picker.py`** — Picks warehouse/lakehouse/mesh from a company profile (stage, consumers, data volume, ML models, culture). Returns architecture + 6-layer build-vs-buy decisions (storage, ELT, modeling, BI, feature store, ML platform) + 12-month sequencing roadmap. Deterministic: same profile → same recommendation. Embedded sample (Series A B2B SaaS, 8 consumers, 4.5TB, 1 ML model) → LAKEHOUSE recommendation.
  - **`data_asset_valuator.py`** — Computes strategic value 0-10 from 4 components (exclusivity, freshness, cohort breadth, history depth), derives moat strength (NONE/WEAK/MEDIUM/STRONG), applies M&A multiplier (1.0x–1.7x ARR depending on moat) with penalties for MSA carve-out rate and failed anonymization audit. Ranks 3 productization paths (benchmark report / embedding endpoint / direct license) by risk + viability. Embedded sample (B2B sales engagement corpus, 380 customers, 47 carve-outs) → 8.2/10 STRONG moat, 1.33-1.61x multiplier, recommends benchmark report as starting path.
- **4 references answering one decision each** (not topic surveys):
  - `ai_training_data_rights.md` — Decision: can we train on this source? Three-dimension matrix + GDPR Art. 6 lawful basis decision tree + EU AI Act high-risk triggers + US state patchwork (CCPA/CPRA, NYC LL 144, IL BIPA, WA MHMD).
  - `data_product_strategy.md` — Decision: which architecture and what do we build? Stage-driven kill criteria per architecture + 6-layer build-vs-buy decision tree + sequencing pattern + anti-patterns.
  - `customer_data_as_asset.md` — Decision: what's our data worth and can we productize it? 5-component valuation framework + M&A multiplier with carve-out impact + 3 productization paths with prerequisites + 10-item M&A diligence prep checklist + quarterly contractual constraint audit pattern.
  - `data_team_org_evolution.md` — Decision: what role next, when to centralize vs embed? 5-stage map (seed → late-stage) with specific role definitions + centralize-vs-embed-vs-federated triggers + 6 anti-patterns ("hiring data scientist as first data hire" etc.).
- **cs-cdo-advisor** agent (`./c-level-advisor/c-level-agents/agents/cs-cdo-advisor.md`) — decision-driven realist orchestrating the skill. Voice: "What decision does this data drive?" Refuses to recommend tooling before naming the consumer. Treats AI training data as both contractual liability and strategic asset.
- **`/cs:cdo-review`** slash command (`./c-level-advisor/c-level-agents/skills/cdo-review/SKILL.md`) — 6-question forcing interrogation pattern matching the /cs:cfo-review / /cs:gc-review etc. shape.
- **cs-cdo-advisor voice spec** added to `persona-voices.md`.

### Why This Matters

By 2026 every B2B SaaS founder is asking three questions the existing C-level skills can't fully answer:
1. **"Can we train our model on customer data?"** — overlaps cs-ciso (security), cs-general-counsel (contracts), and engineering (tactics), but none of them owns the strategic data picture.
2. **"What's the right data architecture — and when?"** — engineering's database-designer and observability-designer cover tactics, but the warehouse-vs-lakehouse-vs-mesh decision is stage-driven, not technology-driven.
3. **"What's our data actually worth in M&A?"** — this comes up at every Series B+ and has no home in existing skills.

This skill fills that gap with **deterministic decision logic** (not survey prose), explicit kill criteria, and a hard rule against duplicating engineering data skills.

### Built with Karpathy-Coder Discipline

This PR was the first in this repo built under explicit karpathy-coder guidance:
- **Principle 1 (Think before coding):** assumptions surfaced upfront, verifiable success criteria locked before any file was written.
- **Principle 2 (Simplicity first):** rejected "generic governance survey" framing; each tool/reference covers ONE decision; refused to add scope ("data product strategy picker" doesn't try to also do data quality, RAG, or schema design).
- **Principle 3 (Surgical changes):** touched only the files in the locked plan. Caught one scope-creep attempt (adding cs-general-counsel-advisor voice spec while editing persona-voices.md) and reverted it — that gap belongs in a separate PR.
- **Principle 4 (Goal-driven execution):** all 3 Python tools smoke-tested with embedded samples before commit (audit: 7 sources → 2 NO-GO / 2 MITIGATE / 3 GO; strategy picker: Series A → LAKEHOUSE; valuator: 8.2/10 STRONG moat).

### Changed

- **Total skills:** 264 → 265 (+1 chief-data-officer-advisor)
- **cs-* agents:** 29 → 30 (+1 cs-cdo-advisor in c-level-agents plugin)
- **/cs:* slash commands:** 17 → 18 (+1 /cs:cdo-review)
- **Python tools:** 361 → 364 (+3 in chief-data-officer-advisor/scripts/)
- **References:** 490 → 494 (+4 in chief-data-officer-advisor/references/)
- **c-level-skills** plugin: v2.5.1 → v2.5.2 (description expanded; 29 → 30 skills, 9 → 10 cs-* agents)
- **c-level-agents** plugin: v1.1.0 → v1.2.0 (description expanded with CDO; new agent; +`chief-data-officer`, `cdo`, `ai-training-data`, `data-product-strategy`, `data-as-asset` keywords)

### Known follow-ups (NOT included this PR per surgical scope)

- The `cs-general-counsel-advisor` voice spec is missing from `persona-voices.md` (introduced in v2.5.1 but not added to the voice reference). Will be addressed in a separate small PR alongside other voice cleanup.
- Phase 2 remainder (4 more C-roles: CAIO AI, CCO customer, VPE engineering execution, CCO comms) deferred to v2.5.3+.

### Disclaimer

The `chief-data-officer-advisor` skill surfaces strategic decisions but is **not legal advice** for AI training, **not a replacement for outside counsel** for productization/licensing decisions, and **not a tactical data engineering skill**. For tactical data engineering, see the engineering/ domain (`database-designer`, `observability-designer`, `data-quality-auditor`, `sql-database-assistant`, `rag-architect`, `llm-cost-optimizer`).

## [2.5.1] - 2026-05-12 — general-counsel-advisor: the gstack-can't-touch lane

### Added — C-Level Advisory

- **general-counsel-advisor** skill (`./c-level-advisor/skills/general-counsel-advisor/`) — full standalone C-role skill backing the `/cs:gc-review` command (which previously had no underlying skill). 2 stdlib Python tools, 3 reference docs.
  - **`contract_risk_scanner.py`** — Scans contract text for 12 founder-killer clause patterns: auto-renewal with long notice (>30 day), customer-indemnity-carved-out-from-cap, one-sided indemnity, vague IP ownership, aggressive non-compete (>1 year), one-sided choice-of-law/venue, one-sided force majeure, missing DPA when personal data flows, MFN pricing, one-sided audit rights, broad non-solicit, perpetual license-back. Outputs ranked findings (CRITICAL/HIGH/MEDIUM) with excerpt, why-it-matters, and suggested redline. Stdlib-only, JSON or text output. Embedded sample MSA detects 7 risks across all 3 severity levels.
  - **`term_sheet_analyzer.py`** — Scores a term sheet 0-100 across 12 dimensions: liquidation preference (1x non-participating vs participating vs multi-preference), anti-dilution (broad-based weighted average vs narrow vs full ratchet), option pool (pre-money vs post-money + size), board composition (founder vs investor vs independent seats), vesting + acceleration (single vs double trigger), pro-rata, drag-along (founder consent / price floor), protective provisions (NVCA standard vs aggressive), information rights, dividends (none / non-cumulative / cumulative), valuation/dilution sanity, holistic posture. Outputs FOUNDER_FRIENDLY / NEGOTIATE / HOSTILE grade plus per-clause flags. Stdlib-only, JSON-input + JSON-or-text output.
  - **`references/contracts_playbook.md`** — 7 standard startup contracts (MSA, customer SaaS, NDA, DPA, employment, contractor, equity), top redlines per type, quick triage heuristics.
  - **`references/ip_and_regulatory.md`** — Full IP strategy (patents, copyright, trademark, trade secrets, invention assignment, OSS license compliance for permissive/weak-copyleft/strong-copyleft including AGPL) plus regulatory trigger matrix (HIPAA, PCI DSS, BSA/AML, FDA 510(k), MDR, GDPR, CCPA, COPPA, securities, ITAR, EU AI Act, telehealth, insurance) with SOC 2 → ISO 27001 → ISO 42001 sequencing and when-to-hire-a-GC criteria.
  - **`references/term_sheet_decoder.md`** — Full term sheet glossary, founder-friendly defaults cheat sheet, the three clauses that matter most (liquidation preference, option pool pre/post-money, anti-dilution), and negotiation strategy.
- **cs-general-counsel-advisor** agent (`./c-level-advisor/c-level-agents/agents/cs-general-counsel-advisor.md`) — risk-paranoid persona orchestrating the skill via `/cs:gc-review`. Distinct voice: "Before we sign, three things need to be settled in writing." Hard rule: never gives definitive legal advice; always escalates to qualified outside counsel.
- **`/cs:gc-review`** updated to invoke the new tools and reference the skill (the command previously pointed at a planned skill with a CHANGELOG note).

### Why This Matters

YC Garry Tan's `gstack` has zero coverage for General Counsel — its "executives" are all software-shipping personas (CEO = scope-cutter, Eng Mgr = test matrix). But legal exposure is where startups most often discover a problem after it's expensive to fix: a missed DPA exposes the company to GDPR fines, vague IP clauses kill acquisition deals years later, full-ratchet anti-dilution silently transfers 5-15% of founder equity at the next down round. This is the first plugin in the founder-mode lineup to outclass gstack on a domain it doesn't even attempt.

### Changed

- **Total skills:** 263 → 264 (+1 general-counsel-advisor)
- **cs-* agents:** 28 → 29 (+1 cs-general-counsel-advisor in c-level-agents plugin)
- **Python tools:** 359 → 361 (+2 in general-counsel-advisor/scripts/)
- **References:** 487 → 490 (+3 in general-counsel-advisor/references/)
- **c-level-skills** plugin: v2.5.0 → v2.5.1 (description expanded; 28 → 29 skills, 8 → 9 cs-* agents)
- **c-level-agents** plugin: v1.0.0 → v1.1.0 (description expanded with General Counsel; new agent added; +`contract-review`, `term-sheet`, `ip-strategy` keywords)

### Disclaimer

The `general-counsel-advisor` skill and `cs-general-counsel-advisor` agent are **not legal advice**. Every output surfaces questions to bring to qualified counsel; both Python tools and all 3 references repeatedly remind users to engage licensed attorneys for binding decisions. The skill is positioned as a triage layer — useful for catching the obvious traps before $500/hour counsel time, never as a substitute.

## [2.5.0] - 2026-05-12 — c-level-agents: Founder-Mode Executive Team

### Added — C-Level Advisory

- **c-level-agents** plugin (`./c-level-advisor/c-level-agents/`) — surfaces the existing 28 c-level skills through a founder-mode interface of cs-* persona agents and `/cs:*` slash commands. New marketplace entry registered separately (category: leadership).
- **8 new cs-* persona agents** with distinct cognitive voices, completing agent coverage for every C-role:
  - `cs-cfo-advisor` (numerate skeptic) wraps cfo-advisor
  - `cs-cmo-advisor` (narrative-first) wraps cmo-advisor
  - `cs-cro-advisor` (pipeline-paranoid) wraps cro-advisor
  - `cs-cpo-advisor` (JTBD-driven) wraps cpo-advisor
  - `cs-coo-advisor` (execution OS) wraps coo-advisor
  - `cs-chro-advisor` (people-systems) wraps chro-advisor
  - `cs-ciso-advisor` (risk-paranoid) wraps ciso-advisor
  - `cs-chief-of-staff` (router & synthesist) wraps chief-of-staff
- **17 /cs:* slash commands** delivered as sub-skills under `c-level-agents/skills/`:
  - **Forcing-question office hours (8):** `/cs:office-hours` (YC-style 6-question intake), `/cs:cfo-review`, `/cs:cmo-review`, `/cs:cpo-review`, `/cs:cro-review`, `/cs:cto-review`, `/cs:ciso-review`, `/cs:gc-review` (General Counsel — a lane gstack has zero of)
  - **Strategic sprint pipeline (5):** `/cs:brief` → `/cs:boardroom` (6-phase deliberation with Phase 2 isolation + devil's advocate pass) → `/cs:decide` (two-layer memory log with preserved dissent) → `/cs:execute` (90-day plan with weekly milestones + DRIs) → `/cs:post-mortem` (scored against pre-committed criteria and revisited dissent)
  - **Meta + safety (4):** `/cs:founder-mode` (auto-router — the killer command), `/cs:onboard` (12-question founder interview → `~/.claude/company-context.md`), `/cs:cross-eval` (multi-model consensus with graceful degradation to Claude-only adversarial mode when Codex/Gemini absent), `/cs:freeze` (cooldown lock on irreversible decisions with `/cs:unfreeze` audit trail)
- **References:** `c-level-agents/references/persona-voices.md` (voice specs per role — moderate aggression: bookend opening + closing, neutral analysis body) and `c-level-agents/references/llm-wiki-bridge.md` (Markdown-only persistent memory via `llm-wiki` — the answer to gstack's gbrain Postgres+pgvector dependency).
- **c-level-skills marketplace entry** description expanded and version bumped to v2.5.0 to reflect the bundled plugin layer.

### Why This Matters

Garry Tan's `gstack` (~66K stars) demonstrated the power of slash-command-first, forcing-question agent gearing — but its "executives" are all software-shipping personas (CEO = scope-cutter, Eng Mgr = test matrix). This release brings the same pattern to **real business decisions**: CFO with unit economics, CMO with positioning, General Counsel with contract risk, CISO with threat modeling, and a 6-phase boardroom that surpasses gstack's sequential review chain with Phase 2 isolation + adversarial pass. Combined with this repo's pre-existing compliance (ra-qm-team), finance, marketing, business-growth, and product domains, this is the business-domain answer to founder-mode — broader role coverage, real frameworks, Markdown-only memory, and explicit voice differentiation.

### Changed

- **Total skills:** 246 → 263 (+17 from c-level-agents sub-skills)
- **cs-* agents:** 20 → 28 (+8 new c-level personas inside the plugin)
- **Slash commands:** 33 → 50 (+17 /cs:* commands as sub-skills)
- **Marketplace plugins:** 33 → 34 (+1 c-level-agents entry)
- **c-level-skills** plugin: v2.2.3 → v2.5.0

## [2.4.5] - 2026-05-11 — Reliability Portfolio + Count-Truth Reconciliation

### Added — Engineering POWERFUL

- **slo-architect** — End-to-end SLO/SLI/error-budget discipline per Google SRE Workbook. Generates structured SLO definitions and refuses to render if required fields (owner, error-budget policy, SLI numerator/denominator) are missing (`slo_designer.py`). Computes error budget and the canonical multi-window burn-rate alert thresholds — fast (1h/5m, page), slow (6h/30m, page), ticket (3d/6h) — with PromQL-shaped output ready to paste (`error_budget_calculator.py`). Reviews existing SLO docs for the 7 common bugs: target too high (≥99.99%), target too low (≤99%), window too short (<7d), window too long (>90d), no SLI definition, no error budget policy, CPU-as-SLI (`slo_review.py`). 4 references on SLO principles, SLI design (5 types), error budget math, and composition with the rest of the portfolio. Asset templates for SLO YAML and error budget policy. New `/slo-design` slash command. Karpathy complexity 95/100. Composes explicitly with feature-flags-architect (rollout abort uses SLO burn-rate), chaos-engineering (blast-radius bounded by SLO error budget), kubernetes-operator (Capability Level 4 requires SLOs).
- **ship-gate** — Pre-production audit skill from external contributor @rx4u (originally PR #527, re-applied to post-restructure dev layout). Scans codebases across 8 categories — security, database, deployment, code quality, AI/LLM, dependencies, frontend, observability — with 89 automated and manual checks. Intercepts deploy-intent phrases ("push to production", "ship it", "go live") and blocks until critical issues resolve. Stack-agnostic (Node/Next/React/Vue/Svelte/Astro/Express/Python/Django/Flask/etc.). Stdlib-only Python scanner (`ship_gate_scanner.py`, ~1230 LOC) with JSON output, ANSI color, interactive manual prompts, and exit codes (0=CLEAR, 1=CRITICAL, 2=HIGH).
- **feature-flags-architect** — End-to-end feature-flag discipline. Detects stale flags as debt (`flag_debt_scanner.py`), generates phased rollout plans across ring/linear/log/cohort strategies (`rollout_planner.py`), and audits every flag for documented kill switch (`kill_switch_audit.py`). 4 references on flag taxonomy, provider comparison (LaunchDarkly / GrowthBook / Statsig / Unleash / Flipt / DIY), rollout strategies, and lifecycle. Ships standalone plugin AND in the engineering-advanced-skills bundle. New `/flag-cleanup` slash command.
- **kubernetes-operator** — End-to-end Kubernetes Operator discipline. Validates CRDs against operator-pattern best practices (`crd_validator.py`), lints Go reconcile functions for anti-patterns like `time.Sleep`, spec mutation, missing requeue, finalizer imbalance (`reconcile_lint.py`), and scores operators against OperatorHub Capability Levels 1-5 (`operator_capability_audit.py`). 4 references on operator pattern, CRD design, reconcile loop patterns, and framework comparison (controller-runtime / kubebuilder / operator-sdk / metacontroller / KOPF). Asset templates for production CRD YAML and Go controller skeleton (both pass linters). New `/operator-audit` slash command. NOT a generic k8s skill — specifically the Operator pattern. Self-tested: linters caught 4 real bugs in their own asset templates during build.
- **chaos-engineering** — End-to-end chaos engineering discipline. Generates structured experiment plans with hypothesis + steady-state + blast-radius + abort-criteria (`experiment_designer.py`), computes blast radius with GREEN/YELLOW/RED risk score against monthly error budget (`blast_radius_calculator.py`), and produces blameless postmortems with blame-language detection (`experiment_postmortem.py`). 4 references on the 4 founding principles + 5th abort-criteria principle, hypothesis/steady-state/abort design, the 7-attack taxonomy (latency / error / resource / network-partition / dependency / time / infrastructure), and tooling landscape (Chaos Toolkit / Chaos Mesh / Litmus / Gremlin / AWS FIS / DIY). Templates for plans and postmortems. New `/chaos-experiment` slash command. Composes explicitly with feature-flags-architect (kill switches as abort triggers) and kubernetes-operator (operators are common chaos targets). Karpathy complexity 95/100 — best score in the new portfolio.

### Added — Repo infrastructure

- **scripts/sync_skill_bundles.py** — mirror standalone plugin payloads into their domain-bundled location; `--check` exits 1 on drift, `--sync` rewrites the mirror. Locks in the dual-publish invariant for every new skill.
- **scripts/check_plugin_json.py** — strict ClawHub schema validator (exactly 8 fields, semver, `author{name,url}`, `skills` as string or array — bare `"./"` rejected per Claude Code v2.1.107+). Verified against all 31 existing plugin.json files.

### Changed

- **Total skills:** 235 (v2.3.0 claim) → 246 (file-system truth via `find . -name SKILL.md` minus 4 distribution duplicates). +5 new skills this cycle (slo-architect, ship-gate, feature-flags-architect, kubernetes-operator, chaos-engineering); +6 discovered during #608/#609 reconciliation.
- **Python tools:** 314 → 359 (`find . -path '*/scripts/*.py' | wc -l`)
- **References:** 435 → 485 (`find . -path '*/references/*.md' | wc -l`)
- **Agents:** 28 → 27 (file-system truth: 20 `cs-*` + 7 personas. Previous "30" miscounted README/TEMPLATE as agents)
- **Slash commands:** 27 → 33 (`find commands -name '*.md' | wc -l`)
- **Marketplace plugins:** 30 → 33 (registered in `.claude-plugin/marketplace.json`)
- **engineering-advanced-skills** plugin: v2.3.3 → v2.4.2
- **marketplace.json**: `feature-flags-architect`, `kubernetes-operator`, and `chaos-engineering` registered as standalone plugins

### Fixed

- `tests/test_skill_integrity.py::TestScriptDirectories::test_scripts_dirs_have_python_files` — was rejecting valid skills shipping `.mjs`/`.js`/`.ts`/`.sh` scripts (e.g., `full-page-screenshot`). Now accepts any executable script extension while keeping the "scripts/ dir is non-empty" intent.
- **#608, #609 — Count claims aligned to ground-truth.** Every metric in `CLAUDE.md`, `README.md`, `docs/`, `mkdocs.yml`, and `.claude-plugin/marketplace.json` now reproduces from a deterministic `find` or `python3 -c "import json"` command. Stale claims of "188 skills", "30 agents", "3 personas", "235 skills" (current-state) were replaced with file-system truth. Per-domain marketplace breakdown also reconciled: engineering-advanced 40→67 unique, engineering-core 32→51, marketing 44→45, c-level 28→34, product 13→17, finance 3→4. Domains ra-qm-team (14), project-management (9), business-growth (5) unchanged.
- **skill-security-auditor** — self-skip false positives via `noqa` directive (the auditor was flagging its own scanner code).

## [2.2.0] - 2026-03-31

### Added — Security Skills Suite & Self-Eval

**6 New Security Skills (engineering-team):**
- **adversarial-reviewer** — Adversarial code review with 3 hostile personas (Saboteur, New Hire, Security Auditor) to break self-review monoculture
- **ai-security** — ATLAS-mapped prompt injection detection, model inversion & data poisoning risk scoring (`ai_threat_scanner.py`)
- **cloud-security** — IAM privilege escalation paths, S3 public access checks, security group detection across AWS/Azure/GCP (`cloud_posture_check.py`)
- **incident-response** — SEV1-SEV4 triage, 14-type incident taxonomy, NIST SP 800-61 forensics (`incident_triage.py`)
- **red-team** — MITRE ATT&CK kill-chain planning, effort scoring, choke point identification (`engagement_planner.py`)
- **threat-detection** — Hypothesis-driven threat hunting, IOC sweep generation, z-score anomaly detection (`threat_signal_analyzer.py`)

**1 New Engineering Skill (engineering/):**
- **self-eval** — Honest AI work quality evaluation with two-axis scoring (substance + execution), score inflation detection, devil's advocate reasoning, and session persistence

**1 New Engineering Skill (engineering-team/):**
- **snowflake-development** — Snowflake data warehouse development, SQL optimization, and data pipeline patterns

### Changed
- **Total skills:** 205 → 223 across 9 domains
- **Python tools:** 268 → 298 CLI scripts (all stdlib-only, verified)
- **Reference guides:** 384 → 416
- **Agents:** 16 → 23
- **Commands:** 19 → 22
- **Engineering Core:** 30 → 36 skills
- **Engineering POWERFUL:** 35 → 36 skills
- **MkDocs docs site:** 269 generated pages, 301 HTML pages
- All domain plugin.json files updated to v2.2.0
- Marketplace description updated with new skill counts
- Codex CLI and Gemini CLI indexes re-synced

### Documentation
- Root CLAUDE.md, README.md, docs/index.md, docs/getting-started.md updated with new counts
- engineering-team/CLAUDE.md updated with security skills section
- mkdocs.yml site_description updated
- New skill docs pages auto-generated for all 8 new skills

### Backward Compatibility
- All existing SKILL.md files, scripts, and references unchanged
- No skill removals or renames
- Plugin source paths unchanged — existing installations will not break
- All new skills are additive only

---

## [2.1.2] - 2026-03-10

### Changed — Product Team Quality & Cross-Domain Integration

**Landing Page Generator — TSX + Brand Voice Integration:**
- Landing page scaffolder now defaults to **Next.js/React TSX output** with Tailwind CSS (HTML preserved via `--format html`)
- 4 Tailwind design styles: `dark-saas`, `clean-minimal`, `bold-startup`, `enterprise` with complete class mappings
- 7 section generators: nav, hero, features, testimonials, pricing, CTA, footer
- Brand voice integration: generation workflow now includes brand voice analysis (step 2) using `marketing-skill/content-production/scripts/brand_voice_analyzer.py` to map voice profile to design style + copy framework
- Added Related Skills cross-references to SKILL.md

**Documentation Updates:**
- `product-team/CLAUDE.md` — Added Workflow 4 (Brand-Aligned Landing Page), updated scaffolder section with TSX docs, added Cross-Domain Integration section
- `product-team/README.md` — Fixed ghost script references (removed 7 scripts that never existed), corrected skill/tool/agent/command counts
- `product-team/.codex/instructions.md` — Added brand voice cross-domain workflow and TSX default note

### Fixed
- **competitive-teardown/SKILL.md** — Fixed 6 broken file references (`DATA_COLLECTION.md` → `references/data-collection-guide.md`, `TEMPLATES.md` → `references/analysis-templates.md`)
- **saas-scaffolder/scripts/project_bootstrapper.py** — Fixed f-string backslash syntax incompatible with Python <3.12
- **237 Python scripts verified** — All pass `--help` without errors (previous session fixed 25 scripts across all domains)

### Added
- `landing-page-generator/SKILL.md` — Brand voice analysis as prerequisite step in generation workflow
- Codex and Gemini skill indexes re-synced with updated SKILL.md content

### Backward Compatibility
- `--format html` still works for landing page scaffolder (TSX is new default)
- All existing script CLIs and arguments unchanged
- No skill removals or renames
- Plugin source paths unchanged — existing installations will not break

---

## [2.1.1] - 2026-03-07

### Changed — Tessl Quality Optimization (#287)
18 skills optimized from 66-83% to 85-100% via `tessl skill review --optimize`:

| Skill | Before | After |
|-------|--------|-------|
| `project-management/confluence-expert` | 66% | 94% |
| `project-management/jira-expert` | 77% | 97% |
| `product-team/product-strategist` | 76% | 85%+ |
| `marketing-skill/campaign-analytics` | 70% | 85%+ |
| `business-growth/customer-success-manager` | 70% | 85%+ |
| `business-growth/revenue-operations` | 70% | 85%+ |
| `finance/financial-analyst` | 70% | 85%+ |
| `engineering-team/senior-secops` | 75% | 94% |
| `marketing-skill/prompt-engineer-toolkit` | 79% | 90% |
| `ra-qm-team/quality-manager-qms-iso13485` | 76% | 85%+ |
| `engineering-team/senior-security` | 80% | 93% |
| `engineering-team/playwright-pro` | 82% | 100% |
| `engineering-team/senior-backend` | 83% | 100% |
| `engineering-team/senior-qa` | 83% | 100% |
| `engineering-team/senior-ml-engineer` | 82% | 99% |
| `engineering-team/ms365-tenant-manager` | 83% | 100% |
| `engineering-team/aws-solution-architect` | 83% | 94% |
| `c-level-advisor/cto-advisor` | 82% | 99% |
| `marketing-skill/marketing-demand-acquisition` | 72% | 99% |

### Fixed
- Created missing `finance/financial-analyst/references/industry-adaptations.md` (reference was declared but file didn't exist)
- Removed dead `project-management/packaged-skills/` folder (zip files redundant)

### Added
- `SKILL_PIPELINE.md` — Mandatory 9-phase production pipeline for all skill work

### Verified
- Claude Code compliance: 18/18 pass (after fix)
- All YAML frontmatter valid
- All file references resolve
- All SKILL.md files under 500 lines

## [Unreleased]

### Added
- **skill-security-auditor** (POWERFUL tier) — Security audit and vulnerability scanner for AI agent skills. Scans for malicious code, prompt injection, data exfiltration, supply chain risks, and privilege escalation. Zero dependencies, PASS/WARN/FAIL verdicts.
- `engineering/git-worktree-manager` enhancements:
  - Added `scripts/worktree_manager.py` (worktree creation, port allocation, env sync, optional dependency install)
  - Added `scripts/worktree_cleanup.py` (stale/dirty/merged analysis with safe cleanup options)
  - Added extracted references and new skill README
- `engineering/mcp-server-builder` enhancements:
  - Added `scripts/openapi_to_mcp.py` (OpenAPI -> MCP manifest + scaffold generation)
  - Added `scripts/mcp_validator.py` (tool definition validation and strict checks)
  - Extracted templates/guides into references and added skill README
- `engineering/changelog-generator` enhancements:
  - Added `scripts/generate_changelog.py` (conventional commit parsing + Keep a Changelog rendering)
  - Added `scripts/commit_linter.py` (strict conventional commit validation)
  - Extracted CI/format/monorepo docs into references and added skill README
- `engineering/ci-cd-pipeline-builder` enhancements:
  - Added `scripts/stack_detector.py` (stack and tooling detection)
  - Added `scripts/pipeline_generator.py` (GitHub Actions / GitLab CI YAML generation)
  - Extracted platform templates into references and added skill README
- `marketing-skill/prompt-engineer-toolkit` enhancements:
  - Added `scripts/prompt_tester.py` (A/B prompt evaluation with per-case scoring)
  - Added `scripts/prompt_versioner.py` (prompt history, diff, changelog management)
  - Extracted prompt libraries/guides into references and added skill README

### Changed
- Refactored the five enhanced skills to slim, workflow-first `SKILL.md` documents aligned to Anthropic best practices.
- Updated `engineering/.claude-plugin/plugin.json` metadata:
  - Description now reflects 25 advanced engineering skills
  - Version bumped from `1.0.0` to `1.1.0`
- Updated root `README.md` with a dedicated \"Recently Enhanced Skills\" section.

### Planned
- Complete Anthropic best practices refactoring (5/42 skills remaining)
- Production Python tools for remaining RA/QM skills
- Marketing expansion: SEO Optimizer, Social Media Manager skills

---

## [2.0.0] - 2026-02-16

### ⚡ POWERFUL Tier — 25 New Skills

A new tier of advanced, deeply-engineered skills with comprehensive tooling:

- **incident-commander** — Incident response playbook with severity classifier, timeline reconstructor, and PIR generator
- **tech-debt-tracker** — Codebase debt scanner with AST parsing, debt prioritizer, and trend dashboard
- **api-design-reviewer** — REST API linter, breaking change detector, and API design scorecard
- **interview-system-designer** — Interview loop designer, question bank generator, and hiring calibrator
- **migration-architect** — Migration planner, compatibility checker, and rollback generator
- **observability-designer** — SLO designer, alert optimizer, and dashboard generator
- **dependency-auditor** — Multi-language dependency scanner, license compliance checker, and upgrade planner
- **release-manager** — Automated changelog generator, semantic version bumper, and release readiness checker
- **database-designer** — Schema analyzer with ERD generation, index optimizer, and migration generator
- **rag-architect** — RAG pipeline builder, chunking optimizer, and retrieval evaluator
- **agent-designer** — Multi-agent architect, tool schema generator, and agent performance evaluator
- **skill-tester** — Meta-skill validator, script tester, and quality scorer
- **agent-workflow-designer** — Multi-agent orchestration system designer with sequential, parallel, router, orchestrator, and evaluator patterns
- **api-test-suite-builder** — API route scanner and test suite generator across frameworks (Next.js, Express, FastAPI, Django REST)
- **changelog-generator** — Conventional commit parser, semantic version bumper, and structured changelog generator
- **ci-cd-pipeline-builder** — Stack-aware CI/CD pipeline generator for GitHub Actions, GitLab CI, and more
- **codebase-onboarding** — Codebase analyzer and onboarding documentation generator for new team members
- **database-schema-designer** — Database schema design and modeling tool with migration support
- **env-secrets-manager** — Environment and secrets management across dev/staging/prod lifecycle
- **git-worktree-manager** — Systematic Git worktree management for parallel development workflows
- **mcp-server-builder** — MCP (Model Context Protocol) server scaffolder and implementation guide
- **monorepo-navigator** — Monorepo management for Turborepo, Nx, pnpm workspaces, and Lerna
- **performance-profiler** — Systematic performance profiling for Node.js, Python, and Go applications
- **pr-review-expert** — Structured code review for GitHub PRs and GitLab MRs with systematic analysis
- **runbook-generator** — Production-grade operational runbook generator with stack detection

### 🆕 New Domains & Skills

- **business-growth** domain (3 skills):
  - `customer-success-manager` — Onboarding, retention, expansion, health scoring (2 Python tools)
  - `sales-engineer` — Technical sales, solution design, RFP responses (2 Python tools)
  - `revenue-operations` — Pipeline analytics, forecasting, process optimization (2 Python tools)
- **finance** domain (1 skill):
  - `financial-analyst` — DCF valuation, budgeting, forecasting, financial modeling (3 Python tools)
- **marketing** addition:
  - `campaign-analytics` — Multi-touch attribution, funnel conversion, campaign ROI (3 Python tools)

### 🔄 Anthropic Best Practices Refactoring (37/42 Skills)

Major rewrite of existing skills following Anthropic's agent skills specification. Each refactored skill received:
- Professional metadata (license, version, category, domain, keywords)
- Trigger phrases for better Claude activation
- Table of contents with proper section navigation
- Numbered workflows with validation checkpoints
- Progressive Disclosure Architecture (PDA)
- Concise SKILL.md (<200 lines target) with layered reference files

**Engineering skills refactored (14):**
- `senior-architect`, `senior-frontend`, `senior-backend`, `senior-fullstack`
- `senior-qa`, `senior-secops`, `senior-security`, `code-reviewer`
- `senior-data-engineer`, `senior-computer-vision`, `senior-ml-engineer`
- `senior-prompt-engineer`, `tdd-guide`, `tech-stack-evaluator`

**Product & PM skills refactored (5):**
- `product-manager-toolkit`, `product-strategist`, `agile-product-owner`
- `ux-researcher-designer`, `ui-design-system`

**RA/QM skills refactored (12):**
- `regulatory-affairs-head`, `quality-manager-qmr`, `quality-manager-qms-iso13485`
- `capa-officer`, `quality-documentation-manager`, `risk-management-specialist`
- `information-security-manager-iso27001`, `mdr-745-specialist`, `fda-consultant-specialist`
- `qms-audit-expert`, `isms-audit-expert`, `gdpr-dsgvo-expert`

**Marketing skills refactored (4):**
- `marketing-demand-acquisition`, `marketing-strategy-pmm`
- `content-creator`, `app-store-optimization`

**Other refactored (2):**
- `aws-solution-architect`, `ms365-tenant-manager`

### 🔧 Elevated Skills
- `scrum-master` and `senior-pm` elevated to POWERFUL tier — PR #190

### 🤖 Platform Support
- **OpenAI Codex support** — Full compatibility without restructuring — PR #43, #45, #47
- **Claude Code native marketplace** — `marketplace.json` and plugin support — PR #182, #185
- **Codex skills sync** — Automated symlink workflow for Codex integration

### 📊 Stats
- **86 total skills** across 9 domains (up from 42 across 6)
- **92+ Python automation tools** (up from 20+)
- **26 POWERFUL-tier skills** in `engineering/` domain (including skill-security-auditor)
- **37/42 original skills refactored** to Anthropic best practices

### Fixed
- CI workflows (`smart-sync.yml`, `pr-issue-auto-close.yml`) — PR #193
- Installation documentation (Issue #189) — PR #193
- Plugin JSON with correct counts and missing domains — PR #186
- PM skills extracted from zips into standard directories — PR #184, #185
- Marketing skill count corrected (6 total) — PR #182
- Codex skills sync workflow fixes — PR #178, #179, #180
- `social-media-analyzer` restructured with proper organization — PR #147, #151

---

## [1.1.0] - 2025-10-21 - Anthropic Best Practices Refactoring (Phase 1)

### Changed — Marketing & C-Level Skills

**Enhanced with Anthropic Agent Skills Specification:**

**Marketing Skills (3 skills):**
- Added professional metadata (license, version, category, domain)
- Added keywords sections for better discovery
- Enhanced descriptions with explicit triggers
- Added python-tools and tech-stack documentation

**C-Level Skills (2 skills):**
- Added professional metadata with frameworks
- Added keywords sections (20+ keywords per skill)
- Enhanced descriptions for better Claude activation
- Added technical and strategic terminology

### Added
- `documentation/implementation/SKILLS_REFACTORING_PLAN.md` — Complete 4-phase refactoring roadmap
- `documentation/PYTHON_TOOLS_AUDIT.md` — Comprehensive tools quality assessment

**Refactoring Progress:** 5/42 skills complete (12%)

---

## [1.0.2] - 2025-10-21

### Added
- `LICENSE` file — Official MIT License
- `CONTRIBUTING.md` — Contribution guidelines and standards
- `CODE_OF_CONDUCT.md` — Community standards (Contributor Covenant 2.0)
- `SECURITY.md` — Security policy and vulnerability reporting
- `CHANGELOG.md` — Version history tracking

### Documentation
- Complete GitHub repository setup for open source
- Professional community health files
- Clear contribution process
- Security vulnerability handling

---

## [1.0.1] - 2025-10-21

### Added
- GitHub Star History chart to README.md
- Professional repository presentation

### Changed
- README.md table of contents anchor links fixed
- Project management folder reorganized (packaged-skills/ structure)

---

## [1.0.0] - 2025-10-21

### Added — Complete Initial Release

**42 Production-Ready Skills across 6 Domains:**

#### Marketing Skills (3)
- `content-creator` — Brand voice analyzer, SEO optimizer, content frameworks
- `marketing-demand-acquisition` — Demand gen, paid media, CAC calculator
- `marketing-strategy-pmm` — Positioning, GTM, competitive intelligence

#### C-Level Advisory (2)
- `ceo-advisor` — Strategy analyzer, financial scenario modeling, board governance
- `cto-advisor` — Tech debt analyzer, team scaling calculator, engineering metrics

#### Product Team (5)
- `product-manager-toolkit` — RICE prioritizer, interview analyzer, PRD templates
- `agile-product-owner` — User story generator, sprint planning
- `product-strategist` — OKR cascade generator, strategic planning
- `ux-researcher-designer` — Persona generator, user research
- `ui-design-system` — Design token generator, component architecture

#### Project Management (6)
- `senior-pm` — Portfolio management, stakeholder alignment
- `scrum-master` — Sprint ceremonies, agile coaching
- `jira-expert` — JQL mastery, configuration, dashboards
- `confluence-expert` — Knowledge management, documentation
- `atlassian-admin` — System administration, security
- `atlassian-templates` — Template design, 15+ ready templates

#### Engineering — Core (9)
- `senior-architect` — Architecture diagrams, dependency analysis, ADRs
- `senior-frontend` — React components, bundle optimization
- `senior-backend` — API scaffolder, database migrations, load testing
- `senior-fullstack` — Project scaffolder, code quality analyzer
- `senior-qa` — Test suite generator, coverage analyzer, E2E tests
- `senior-devops` — CI/CD pipelines, Terraform, deployment automation
- `senior-secops` — Security scanner, vulnerability assessment, compliance
- `code-reviewer` — PR analyzer, code quality checker
- `senior-security` — Threat modeling, security audits, pentesting

#### Engineering — AI/ML/Data (5)
- `senior-data-scientist` — Experiment designer, feature engineering, statistical analysis
- `senior-data-engineer` — Pipeline orchestrator, data quality validator, ETL
- `senior-ml-engineer` — Model deployment, MLOps setup, RAG system builder
- `senior-prompt-engineer` — Prompt optimizer, RAG evaluator, agent orchestrator
- `senior-computer-vision` — Vision model trainer, inference optimizer, video processor

#### Regulatory Affairs & Quality Management (12)
- `regulatory-affairs-head` — Regulatory pathway analyzer, submission tracking
- `quality-manager-qmr` — QMS effectiveness monitor, compliance dashboards
- `quality-manager-qms-iso13485` — QMS compliance checker, design control tracker
- `capa-officer` — CAPA tracker, root cause analyzer, trend analysis
- `quality-documentation-manager` — Document version control, technical file builder
- `risk-management-specialist` — Risk register manager, FMEA calculator
- `information-security-manager-iso27001` — ISMS compliance, security risk assessment
- `mdr-745-specialist` — MDR compliance checker, UDI generator
- `fda-consultant-specialist` — FDA submission packager, QSR compliance
- `qms-audit-expert` — Audit planner, finding tracker
- `isms-audit-expert` — ISMS audit planner, security controls assessor
- `gdpr-dsgvo-expert` — GDPR compliance checker, DPIA generator

### Documentation
- Comprehensive README.md with all 42 skills
- Domain-specific README files (6 domains)
- CLAUDE.md development guide
- Installation and usage guides
- Real-world scenario walkthroughs

### Automation
- 20+ verified production-ready Python CLI tools
- 90+ comprehensive reference guides
- Atlassian MCP Server integration

---

## Version History Summary

| Version | Date | Skills | Domains | Key Changes |
|---------|------|--------|---------|-------------|
| 2.1.2 | 2026-03-10 | 170 | 9 | Landing page TSX output, brand voice integration, 25 script fixes |
| 2.1.1 | 2026-03-07 | 170 | 9 | 18 skills optimized via Tessl, YAML frontmatter, agents + commands |
| 2.0.0 | 2026-02-16 | 86 | 9 | 26 POWERFUL-tier skills, 37 refactored, Codex support, 3 new domains |
| 1.1.0 | 2025-10-21 | 42 | 6 | Anthropic best practices refactoring (5 skills) |
| 1.0.2 | 2025-10-21 | 42 | 6 | GitHub repository pages (LICENSE, CONTRIBUTING, etc.) |
| 1.0.1 | 2025-10-21 | 42 | 6 | Star History, link fixes |
| 1.0.0 | 2025-10-21 | 42 | 6 | Initial release — 42 skills, 6 domains |

---

## Semantic Versioning

- **Major (x.0.0):** Breaking changes, major new domains, significant architecture shifts
- **Minor (1.x.0):** New skills, significant enhancements
- **Patch (1.0.x):** Bug fixes, documentation updates, minor improvements

---

[Unreleased]: https://github.com/alirezarezvani/claude-skills/compare/v2.1.2...HEAD
[2.1.2]: https://github.com/alirezarezvani/claude-skills/compare/v2.1.1...v2.1.2
[2.1.1]: https://github.com/alirezarezvani/claude-skills/compare/v2.0.0...v2.1.1
[2.0.0]: https://github.com/alirezarezvani/claude-skills/compare/v1.0.2...v2.0.0
[1.1.0]: https://github.com/alirezarezvani/claude-skills/compare/v1.0.1...v1.1.0
[1.0.2]: https://github.com/alirezarezvani/claude-skills/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/alirezarezvani/claude-skills/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/alirezarezvani/claude-skills/releases/tag/v1.0.0
