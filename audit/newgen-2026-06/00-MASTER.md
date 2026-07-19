# Master Audit Report — New-Generation Model Optimization

**Audited:** 2026-06-10 · **Branch:** `claude/skills-plugins-audit-vrttx1` · **Scope:** every canonical skill, plugin, agent, slash command, script, and registry surface (sync copies under `.codex/ .gemini/ .hermes/ .vibe/` excluded as derived artifacts).

**Method:** two automated sweep layers (the repo's own `audit_skills.py` checklist + a custom new-gen sweep for triggers, verification loops, placeholders, stale models, dead links, duplicate content) followed by 10 parallel domain deep-dives that read every SKILL.md, spot-checked references and scripts, and **executed** empirical claims where the skills make them. Rubric: [RUBRIC.md](RUBRIC.md).

---

## 1. Repo-wide scorecard

**324 unique skills** audited (346 SKILL.md files minus dual-published copies and meta/index files counted once):

| Verdict | Count | % | Meaning |
|---|---|---|---|
| **KEEP** | 190 | 59% | Ships as-is; verification criteria recorded per skill in domain reports |
| **OPTIMIZE** | 102 | 31% | Targeted edits (wiring, triggers, freshness) — content core is sound |
| **REWRITE** | 16 | 5% | Structure salvageable, content is not |
| **CUT-OR-MERGE** | 16 | 5% | Does not earn its context window |

Per domain (links go to the detailed reports with **per-skill custom verification criteria**):

| Domain report | Skills | KEEP | OPT | REW | CUT | Health |
|---|---|---|---|---|---|---|
| [productivity + markdown-html](productivity-markdown-html.md) | 11 | 9 | 2 | 0 | 0 | ★ best — 24/27 live checks pass |
| [research + research-ops](research.md) | 13 | 5 | 7 | 1 | 0 | research-ops all-KEEP; research/ needs wiring |
| [bizops + commercial + finance + growth](bizops-commercial-finance.md) | 24 | 14 | 8 | 0 | 2 | v2.8.0 verified; finance/ legacy |
| [c-level-advisor](c-level-advisor.md) | 61 | 40 | 20 | 0 | 1 | strong content, broken wiring |
| [engineering](engineering.md) | 63 | 44 | 8 | 7 | 4 | two generations coexist |
| [engineering-team](engineering-team.md) | 51 | 35 | 13 | 2 | 1 | code-corruption + stale-era issues |
| [compliance (ra-qm + compliance-os)](compliance.md) | 26 | 13 | 11 | 1 | 1 | P0 regulatory staleness |
| [marketing](marketing.md) | 49 | 20 | 24 | 1 | 4 | orphan scripts + path schism |
| [product-team + project-management](product-pm.md) | 26 | 10 | 9 | 4 | 3 | fabricated MCP wiring |
| [cross-cutting infra](cross-cutting.md) | — | — | — | — | — | registries, CI, root agents/commands |

**Other artifact classes:** 92 agents (17 of 32 root agents lack trigger descriptions; 7 of 13 c-level personas cite phantom reference files; 2 missing frontmatter) · 99 commands (9 root commands are cut/merge candidates; 28 of 39 root commands invoke phantom script paths) · 77 plugin manifests (all schema-valid; **11 not registered in marketplace.json**) · 593 scripts (583 pass `--help`; 1 real crash; 9 by-design).

---

## 2. P0 — Correctness defects (fix before anything else)

These cause a model following the skill to produce **wrong or dangerous output today**:

| # | Defect | Where | Evidence |
|---|---|---|---|
| P0-1 | **Repealed regulation taught as current law.** QSR (21 CFR 820 subsections) presented as in force; QMSR (effective 2026-02-02) never mentioned. Reference + `qsr_compliance_checker.py --section 820.30` built on removed section numbers. | `ra-qm-team/skills/fda-consultant-specialist` | [compliance.md](compliance.md) |
| P0-2 | **ALARP table violates EU MDR.** Risk-acceptability framework includes "cost-benefit of further reduction," which MDR Annex I + EN ISO 14971:2019/A11 prohibit. A notified body would flag this exact table. | `ra-qm-team/skills/risk-management-specialist` | [compliance.md](compliance.md) |
| P0-3 | **EU AI Act Article 5 mis-taught.** Default sample classifies *retail* emotion recognition as prohibited; Art. 5(1)(f) covers workplace/education only. | `ra-qm-team/skills/eu-ai-act-specialist` | [compliance.md](compliance.md) |
| P0-4 | **Silent zero-output finance tools.** All 4 scripts read the wrong JSON shape vs their own bundled sample: zero ratios, $0.00 forecasts, error message then `exit 0`. Invisible to `--help` smoke tests. | `finance/financial-analyst` | [bizops-commercial-finance.md](bizops-commercial-finance.md) |
| P0-5 | **Contradictory discount-margin math.** SKILL.md states the correct fixed-COGS formula; `deal_scorer.py` + reference use a different one (script docstring writes the correct formula, then discards it). Margin dimension (weight 0.30) understates discount damage. | `commercial/deal-desk` | [bizops-commercial-finance.md](bizops-commercial-finance.md) |
| P0-6 | **Corrupted code examples from a past bulk YAML-quoting sweep.** E.g. `z.string().min(1).max(100)` → `"zstringmin1max100"`. 4 confirmed sites; models copying these emit broken code. | `engineering-team` senior-qa:123/244, senior-backend:253, senior-frontend:425 | [engineering-team.md](engineering-team.md) |
| P0-7 | **Fabricated MCP tool names.** 3 Atlassian skills + project-management/CLAUDE.md document four different invented naming conventions; none match the bundled Remote MCP's real tools (`createJiraIssue`, `searchJiraIssuesUsingJql`, …). Every documented tool call fails. | `project-management/` (jira-expert, confluence-expert, atlassian-templates) | [product-pm.md](product-pm.md) |
| P0-8 | **Fabricated install coordinates.** Whole skill teaches a `gws` CLI from `npm i -g @anthropic/gws` / `github.com/googleworkspace/cli` — both almost certainly nonexistent; 43 recipes + 5 wrappers unusable. | `engineering-team/skills/google-workspace-cli` | [engineering-team.md](engineering-team.md) |
| P0-9 | **Skill instructs invoking agents that don't exist in this repo** (documents a different ecosystem: `planner`, `/build-fix`, …). | `engineering/skills/command-guide` | [engineering.md](engineering.md) |
| P0-10 | **Stale orchestrator text bypasses shipped converters.** "v2.10.0 foundation" wording tells the model to hand-render HTML instead of routing to md-document/md-review/md-slides, which shipped. Behavioral, not cosmetic. | `markdown-html/` orchestrator (+ domain CLAUDE.md, README) | [productivity-markdown-html.md](productivity-markdown-html.md) |
| P0-11 | **Script crash:** no argparse; `--help` (or any flag) treated as input filename → FileNotFoundError. Skill's only tool. | `marketing-skill/skills/webinar-marketing/scripts/webinar_funnel_scorer.py` | [marketing.md](marketing.md) |

---

## 3. P1 — Systemic wiring failures (one fix clears many skills)

1. **Phantom-path epidemic (the single biggest repo-wide defect).** A directory reorg added a `skills/` path segment; references never followed. **28 of 39 root commands** invoke scripts at `<domain>/<skill>/scripts/…` that live at `<domain>/skills/<skill>/scripts/…`; same stale shorthand in agents' `skills:` frontmatter, `orchestration/ORCHESTRATION.md` (points at skills that exist only as .zip archives), product/PM routers, c-level persona agents (~16 phantom reference filenames across 7 agents), email agents (`engineering/email/...` → `productivity/email/`), and **5 research skills whose final verification step calls `scripts/office/validate.py` — a file that exists nowhere**. → Build a path-existence linter (see §5) and fix in one sweep.
2. **Orphan-script epidemic.** 40+ working, `--help`-passing scripts are never named in their own SKILL.md (24 in marketing, 8 in product/PM, 6+ in engineering, reflect's all-3, ms365, incident-commander). The model loading these skills cannot use their best assets. → A3 wiring pass: exact CLI + consume-the-output step per script.
3. **Counter drift is structural.** Seven surfaces disagree (README 338 skills / CLAUDE.md header 338 / CLAUDE.md v2.10.3 block 343 / marketplace.json description 64 plugins while containing 66 / actual: **346-347 skills, 66 registered + 11 unregistered plugins, 555 tools, 700 references, 17 domains**). agents/CLAUDE.md says 16 agents; folder has 32. → Derive all counters from the tree via script; never hand-edit again.
4. **11 shippable plugins not in marketplace.json** — compliance-os (advertised in the marketplace's own description yet uninstallable), snowflake-development, behuman, claude-coach, grill-with-docs, llm-cost-optimizer, prompt-governance, business-investment-advisor, video-content-strategist, 2× ra-qm compliance-team.
5. **Marketing context-file path schism.** 19 skills read `.claude/product-marketing-context.md`, 16 read `marketing-context.md`, the creator skill writes `.agents/marketing-context.md`. The domain's "read context first" pattern silently no-ops for half its consumers.
6. **c-level role-registry drift.** Routing tables (agent-protocol, chief-of-staff, board-meeting, founder-mode, brief, c-level-agents frontmatter) stopped at 9 roles; domain has 14. CCO/CDO/CAIO/VPE questions silently misroute. Plus three competing decision-memory architectures and two onboarding interviews writing different schemas to the same file.
7. **Dual-publishing without a guard.** 11 byte-identical skill pairs (engineering ×4, c-level ×5, ra-qm ×2). Zero drift today — but no sync script and no CI check; drift is a matter of time.
8. **Trigger-description gap.** 79 skills and 77 of 92 agents lack "use when" phrasing — weak auto-invocation for new-gen models. Root cause for agents: `templates/agent-template.md` mandates a sub-150-char description with no trigger requirement. 8 v2.8.0 descriptions exceed the 1024-char spec limit (knowledge-ops 1,314 — this, not content, is why it "scored worst").
9. **Meta-tooling violates its own rubric.** `audit_skills.py --help` runs the full 30s audit; `generate-docs.py --help` **rewrites docs/ as a side effect** (verified live — this explains the dirty docs/ files found at session start); hermes/vibe/gemini sync scripts, convert.sh, and generate-docs don't know `markdown-html/` exists; CI's blocking `compileall` skips 8 post-v2.7 domains.
10. **35 stale .zip archives** in the public tree (engineering-team 18, compliance 12, marketing 5) plus 4 internal planning docs in the marketing plugin root.

---

## 4. What's already excellent (the template to copy)

- **research-ops/** — every hard rule verified in execution: ESTIMATE banners, dual-method TAM with triangulation-failure flag, anecdote-vs-insight recurrence gate, named-owner routing on every output. All-KEEP.
- **markdown-html/ + productivity/** — 24/27 empirical checks passed live: exit-code refusal gates, WCAG-AA validation, redaction linter (16 patterns, not the claimed 17 — fix the count), idempotent injection, kill-gate behavior in andreessen.
- **v2.8.0 bizops/commercial orchestrators** — `context: fork` signal-table routing with 2-signal thresholds and no-silent-chain gates verified real, not prose.
- **v2.2 security suite, playwright-pro, self-improving-agent, slo-architect, chaos-engineering, karpathy-coder, Pocock ports** — exit-code contracts, forcing questions, kill criteria, exact CLIs.
- **compliance-os layer** — Article-cited verdicts, explicit NOT-boundaries, outside-counsel routing; **no skill in the repo auto-decides compliance verdicts**.

The repo's quality story is generational, not random: everything built v2.4+ with forcing questions, refusal gates, and wired tools is KEEP-grade; v2.0–v2.1-era skills are capability brochures. The optimization play is to **retrofit the new-gen pattern onto the old generation, not to invent anything new**.

---

## 5. Recommended verification harness (CI gates to add)

Each gate below is the generalized guardrail derived from a defect class this audit found. Suggested home: `scripts/` + `ci-quality-gate.yml`.

| Gate | Catches | Spec |
|---|---|---|
| **G1 path-existence linter** | P1-1 phantom paths | Extract every `scripts/…`, `references/…`, `skills:` and relative-path mention from SKILL.md/agents/commands; assert the file exists. Fails today on ~40 surfaces; burn down, then make blocking. |
| **G2 semantic `--sample` smoke** | P0-4 silent zero-output | For every script with `--sample`/bundled sample data: run it, assert exit 0 **and** output passes a per-skill assertion (non-zero metric count, required JSON keys, banner strings). Per-skill assertions are already written: see "Verify (definition of done)" blocks in every domain report. |
| **G3 counter derivation** | P1-3 drift | `scripts/derive_counters.py` counts skills/plugins/tools/refs/agents/commands from the tree and rewrites the counter blocks in README/CLAUDE.md/marketplace.json. CI fails if claimed ≠ derived. |
| **G4 dual-publish drift guard** | P1-7 | `diff -rq` the 11 known pairs; fail on first divergence. |
| **G5 marketplace registration check** | P1-4 | Every `*/.claude-plugin/plugin.json` has a marketplace.json entry (or an explicit `unlisted` allowlist). |
| **G6 description linter upgrade** | P1-8 | Extend `skill_description_validator.py`: hard-fail >1024 chars, warn missing trigger phrasing, apply to agents too; fix `templates/agent-template.md` so new agents start compliant. |
| **G7 model-name freshness** | stale GPT-4/claude-3 era refs | Regex deny-list for retired model identifiers outside historical-context sentences (2 SKILL.md + 2 scripts today). |
| **G8 argparse contract** | P0-11 | Every `scripts/*.py` must exit 0 on `--help` within 5s unless listed in a by-design exceptions file (hooks, fixed evaluators). |
| **G9 meta-tool hygiene** | P1-9 | `generate-docs.py --help` must be side-effect-free; sync scripts/convert.sh/compileall enumerate domains from the tree, not a hardcoded list. |

---

## 6. Suggested execution order (follow-up PRs)

1. **PR-1 (P0 batch, ~1 day):** fix the 11 P0 defects. Highest stakes first: FDA/QMSR, ALARP, AI-Act sample, financial-analyst JSON shape, deal-desk formula, corrupted code literals, Atlassian tool-name appendix, webinar argparse, markdown-html orchestrator status text, retire command-guide + google-workspace-cli (or re-verify the CLI exists).
2. **PR-2 (path sweep):** G1 linter + one mechanical fix-all for the `skills/` segment; fix c-level agent KB filenames, research `office/validate.py` (write it or drop the step), email agent paths.
3. **PR-3 (registries):** G3 counter derivation + marketplace registration of the 11 plugins + c-level role-registry update (6 files) + marketing context-file unification.
4. **PR-4 (wiring):** orphan-script A3 pass per domain report lists; trigger-description batch (79 skills, 77 agents) using each report's per-skill suggested descriptions.
5. **PR-5 (CI):** land gates G2, G4–G9; remove 35 .zip archives; fix meta-tooling.
6. **PR-6+ (content):** the 16 REWRITE skills, then OPTIMIZE queue per domain, using the per-skill "Verify (definition of done)" blocks as acceptance criteria.

---

## 7. Where the per-skill verification criteria live

The user-requested **customized verification loops and validation criteria for every skill, plugin, agent, and command** are in the domain reports: every OPTIMIZE/REWRITE/CUT entry carries a "Verify (definition of done)" block of 2–4 executable checks, and every KEEP skill has a one-line verification contract in its report's "KEEP-verdict verification criteria" section. Those blocks are the input for gate G2.
