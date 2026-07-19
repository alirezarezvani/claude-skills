# Domain audit: productivity/ + markdown-html/ — new-gen model optimization
Audited: 2026-06-10 · Skills: 11 · Agents: 7 · Commands: 14 · Plugins: 6 · Hooks: 2

## Scorecard
| Skill | Verdict | Top issue |
|---|---|---|
| markdown-html-orchestrator | OPTIMIZE | Stale v2.10.0 "foundation status" text instructs the model NOT to use the (now-shipped) converters |
| design-system | KEEP | Validator script exits 0 even on FAIL verdict (refusal lives in onboard.py — documented, but easy to misread) |
| md-document | KEEP | <100-line "hard rule" is prose/command-enforced, not script-enforced (parser accepted a 70-line file) |
| md-review | KEEP | — |
| md-slides | KEEP | Boundary-less 1-slide file exits 6 (no-boundary), not 5 (poster) — doc nuance |
| capture | KEEP | dump_classifier CLI shape (positional arg) not documented in SKILL.md tooling table |
| inbox-setup | KEEP | — (its agent has a phantom skills path; see Agents) |
| inbox-triage | KEEP | — (same agent issue) |
| reflect | OPTIMIZE | 3 scripts are unwired — no CLI invocations in SKILL.md, no step consumes their output |
| handoff | KEEP | "17 regex patterns" claim is actually 16; tools table lacks exact CLI invocations |
| andreessen | KEEP | — |

Verdicts: 9 KEEP · 2 OPTIMIZE · 0 REWRITE · 0 CUT-OR-MERGE

## Empirical verification results

All runs used `MARKDOWN_HTML_NO_CONFIG=1` or an isolated `HOME` to avoid touching real config. Scratch: /tmp/audit-pmh.

| # | Check | Expected | Actual | Result |
|---|---|---|---|---|
| 1 | md-document pipeline (parser → renderer → injector) on 515-line repo CLAUDE.md | valid single-file HTML | 88 KB HTML, parses clean, 16 sections, all 4 JS features injected (+5,081 B) | PASS |
| 2 | Output single-file discipline | only Google Fonts + Prism externals | external hosts: `fonts.googleapis.com`, `cdn.jsdelivr.net` (+ content links) | PASS |
| 3 | interactivity_injector idempotency | re-inject is no-op | "no-op: marker … already present", exit 0 | PASS |
| 4 | md-document <100-line refusal at script level | refuse per SKILL.md hard rule #1 | parser/renderer accepted a 70-line file (gate lives in orchestrator `route_explainer.py` + command prose `wc -l`) | PARTIAL — claim overstates script behavior |
| 5 | slide_splitter 1-slide deck → exit 5 | exit 5 | exit 5 (with `--boundary h1` single-H1, and 3-HR degenerate deck) | PASS |
| 6 | slide_splitter no-boundary → exit 6 | exit 6 | exit 6 on 120-line prose file (also on plain 1-slide file — exit 6 fires before exit 5 when no boundaries detected) | PASS |
| 7 | md-slides happy path (5 slides, 3 with notes) | working deck | 10.8 KB single-file HTML, 5 `<section class="slide">`, keydown handlers, 1 `@media print`, 60% notes coverage reported | PASS |
| 8 | md-review diff_parser on real ```diff block | hunks JSON | 1 file / 1 hunk parsed; extractor found 2 annotations (1 BLOCKER, 1 NIT) | PASS |
| 9 | review_html_renderer without `--reviewer` → exit 3 | exit 3 | exit 3, "A code review must name a human reviewer" | PASS |
| 10 | review_html_renderer with 0 hunks → exit 4 | exit 4 | exit 4, "route to md-document instead" | PASS |
| 11 | LGTM approval capture | approvals counted | standalone `LGTM` line → 1 approval (regex requires standalone line; "LGTM otherwise." is not counted — by design) | PASS |
| 12 | brand_palette_validator refuses AA-failing palette | FAIL verdict | `--text #CCCCCC --bg #FFFFFF` → FAIL 1.61:1; but script exit 0 (verdict-only); save refusal is onboard.py | PASS (with caveat) |
| 13 | onboard.py exit 4 on AA-fail save | exit 4 | exit 4, "refusing to save: WCAG AA contrast failed" | PASS |
| 14 | onboard.py exit 3 on empty/unwritable output dir | exit 3 | exit 3 on empty path (unwritable case untestable as root — `os.access` always true; code path present at line 226) | PASS |
| 15 | orchestrator <100-line refusal | REFUSE | exit 3, Shihipar citation, design-system status surfaced | PASS |
| 16 | orchestrator silent-route on review doc | ROUTE_SILENTLY → md-review | score 13 vs runner-up 1, routed silently | PASS |
| 17 | orchestrator ambiguity → ASK_USER | one question | CLAUDE.md scored slides 18 / document 15 → ASK_USER with recommended answer (correct: CLAUDE.md is full of `---` HRs) | PASS |
| 18 | handoff redaction_linter on fake AWS key (strict) | exit 1, block | exit 1, `[high] aws_access_key`, fix suggestion + whitelist tip | PASS |
| 19 | redaction_linter whitelist `<!-- handoff:allow secret -->` | exit 0 | exit 0, "OK: no findings" | PASS |
| 20 | "17 patterns" claim | 17 Pattern() defs | **16** Pattern() defs (aws×2, github, openai, anthropic, slack, google, stripe, private-key, jwt, env-assign, db-conn, bearer, email, phone, url-token) | FAIL (off-by-one in docs) |
| 21 | handoff hooks | stdin-safe, env-disable | SessionStart: exit 0 disabled + exit 0 no-handoff; SessionEnd prints reminder, exit 0; hooks.json wires both via `${CLAUDE_PLUGIN_ROOT}` | PASS |
| 22 | andreessen market_first_evaluator --sample | verdict + weights | BUILD-POUR-FUEL, market weighted 0.55 (contribution 4.4) | PASS |
| 23 | andreessen kill gate: market 3.0, team/product 10 | KILL despite 6.15 composite | KILL-OR-REPICK-MARKET + explicit "trap" note that team/product cannot override sub-4 market | PASS |
| 24 | anti_todo_card 6th must-do | reject | exit 2, "the cap IS the discipline" | PASS |
| 25 | operating prompt operationalized | posture table | references/operating_prompt.md: verbatim prompt + 6-row instruction→behavior mapping + binding confidence-level discipline + "what this is NOT" | PASS |
| 26 | inbox-triage draft_safety_validator | exit 1 on send-shaped call | `--sample-fail` exit 1 / `--sample-pass` exit 0 | PASS |
| 27 | all 22 productivity scripts `--help` | exit 0 | 22/22 exit 0 | PASS |

Tally: **24 PASS · 1 PARTIAL · 1 FAIL** (plus 1 caveat). The domains' empirical claims are overwhelmingly real.

## Domain-level findings

1. **Staleness cascade in markdown-html/ (the one real defect).** The domain shipped complete at v2.10.3, but three files still describe the v2.10.0 foundation: `markdown-html/CLAUDE.md` (skills table marks md-document/review/slides "v2.10.1"), `markdown-html/README.md` ("Status — v2.10.0 (foundation)", converters "v2.10.1 (next PR)"), and the orchestrator SKILL.md ("Until v2.10.1, the orchestrator's job stops at step 4 — … lets Claude do the rendering inline"). A new-gen model following the orchestrator SKILL.md today is **instructed to bypass the shipped converters** and hand-render. This is an A6 failure with behavioral consequence, not cosmetic.
2. **Refusal gates split between scripts and prose — mostly fine, but SKILL.md wording overclaims twice.** md-document's "Hard rule 1: Refuses input < 100 lines" and design-system's validator both read as script-level gates; in reality the 100-line gate lives in the orchestrator's `route_explainer.py` and in the converter commands' `wc -l` instruction, and the palette refusal lives in `onboard.py` (validator exits 0 on FAIL verdict). Direct script invocation skips both. Acceptable for a model that follows the commands, but the prose should say where each gate is enforced.
3. **A3 weakness across productivity/: tool tables without exact CLI invocations.** reflect, handoff, and capture (dump_classifier) list scripts in a table but never show how to call them — I had to discover arg shapes by trial (`redaction_linter.py FILE` positional, not `--file`; `bias_pattern_detector.py --conversation`). markdown-html/ does this right (every SKILL.md has copy-pasteable invocations); productivity/ should match.
4. **Counter/spec drift.** Redaction patterns 16 vs claimed 17 (root CLAUDE.md v2.8.2 notes). reflect's spec is `megaprompts/02-reflect-megaprompt.md` per SKILL.md + plugin.json, but root CLAUDE.md v2.7.0 notes call reflect "megaprompt 08". Minor, but counters are this repo's brand — keep them true.
5. **Trigger quality is uniformly strong (A1).** Every skill in scope has concrete trigger phrases, third-person descriptions, refusal conditions in the description itself, and "distinct from" disambiguation. This is the best trigger discipline of any domain pattern observed; no action needed.
6. **Context economy is good but markdown-html SKILL.md bodies duplicate the domain CLAUDE.md hard rules ~3×** (domain CLAUDE.md, SKILL.md "Hard rules", command "Pre-flight gates"). Tolerable since skills ship standalone, but the duplication is what made the staleness cascade possible — single-source the version/status table.

## Per-skill findings

### markdown-html-orchestrator — OPTIMIZE
- **Verdict:** OPTIMIZE (targeted edits; routing logic and scripts are excellent and fully verified)
- **Issues:**
  1. SKILL.md "Foundation status (v2.10.0)" paragraph + Step 5 ("Until v2.10.1 … lets Claude do the rendering inline") + Output-artifacts table ("v2.10.1" status column) instruct the model to bypass shipped converters. Delete the transitional text.
  2. Frontmatter `version: 2.10.0` while plugin is 2.10.3.
  3. `markdown-html/CLAUDE.md` skills table and `README.md` status section carry the same stale v2.10.0 framing (fix together).
  4. Pipeline snippets use `skills/markdown-html-orchestrator/...` relative paths while Step-1 uses repo-rooted `markdown-html/skills/...` — pick one convention.
- **Verify:**
  - `grep -c "v2.10.1" markdown-html/skills/markdown-html-orchestrator/SKILL.md` returns 0
  - `grep -c "foundation" markdown-html/README.md markdown-html/CLAUDE.md` returns 0 stale-status hits (status table lists all 5 skills "✓ live")
  - `printf '# s\n' > /tmp/s.md && python3 markdown-html/skills/markdown-html-orchestrator/scripts/doctype_classifier.py --input /tmp/s.md --output json | python3 .../route_explainer.py; test $? -eq 3` (refusal stays green)
  - review-shaped ≥100-line input still yields `ROUTE_SILENTLY -> md-review`

### reflect — OPTIMIZE
- **Verdict:** OPTIMIZE (the prompt body is strong; the script layer is dead weight as wired)
- **Issues:**
  1. A3: no CLI invocations anywhere in SKILL.md for the 3 scripts; no workflow step consumes their output. For an in-conversation reflection skill the model cannot trivially produce a transcript file, so `bias_pattern_detector.py --conversation FILE` and `conversation_depth_analyzer.py` have no realistic input path described.
  2. A4: `directional_recommendation_validator.py` is the natural verification loop (assert output ends Continue/Pivot/Pause) but is never invoked in the workflow. Wire it: "pipe your draft reflection through the validator before sending; exit 0 required."
  3. Either wire all 3 scripts with exact invocations + an input-capture step, or cut detector/analyzer and keep only the validator (A7).
- **Verify:**
  - SKILL.md "Tooling" section contains ≥1 fenced `python3 …` invocation per retained script
  - `printf 'analysis...\nContinue. Because X and Y are verified.\n' | python3 productivity/reflect/skills/reflect/scripts/directional_recommendation_validator.py -` (or documented file form) exits 0; output missing a closing recommendation exits non-zero
  - `python3 .../bias_pattern_detector.py --sample --output json` exits 0 with keys `biases_detected`, `biases_clear`, `details` (if retained)

## KEEP-verdict verification criteria

- **design-system:** `HOME=$(mktemp -d) python3 markdown-html/skills/design-system/scripts/onboard.py --defaults` exits 0; `--set brand.text='#CCCCCC' --set brand.bg='#FFFFFF'` exits 4; `--set default_output_dir=` exits 3; `config_loader.py --status` reports `setup_completed: true` after defaults.
- **md-document:** full 3-script pipeline on a ≥100-line file exits 0×3 and produces HTML whose only external hosts are `fonts.googleapis.com` + `cdn.jsdelivr.net`; second injector run prints `no-op` and exits 0. (Optimization PRs must also fix Hard-rule-1 wording to name where the 100-line gate is enforced.)
- **md-review:** renderer without `--reviewer` exits 3; with 0-hunk input exits 4; with valid input exits 0 and output contains the reviewer name + per-severity counts; standalone `LGTM` line yields `approvals: 1`.
- **md-slides:** `slide_splitter.py` exits 5 on a boundary-detected 1-slide deck, 6 on boundary-less input, 0 on a 5-slide HR deck; rendered deck contains 5 `class="slide"` sections, `addEventListener`, and `@media print`.
- **capture:** `dump_classifier.py <file>` and `--sample` exit 0; `workspace_inventory.py --root . --keywords "a,b"` exits 0 (documented invocation stays true); `complexity_estimator.py --sample small` recommends compressed format.
- **inbox-setup:** `kb_validator.py --sample` exits 0 with verdict PASS and 7-file contract checks; SKILL.md section count stays 8 with S4 skip-logic intact.
- **inbox-triage:** `draft_safety_validator.py --sample-fail` exits 1, `--sample-pass` exits 0; SKILL.md states DRAFTS-ONLY in ≥3 places; `search_window_calculator.py --help` exits 0.
- **handoff:** `redaction_linter.py <file-with-AKIA-key>` exits 1 strict / 0 with `<!-- handoff:allow secret -->`; `echo '{}' | HANDOFF_SESSIONSTART=0 python3 hooks/session_start.py` exits 0; `handoff_self_check.py --sample` exits 0; fix the "17 patterns" claim to 16 (or add the 17th) wherever it appears.
- **andreessen:** `market_first_evaluator.py --size 3 --growth 3 --timing 3 --pull 3 --team 10 --product 10` verdict is KILL-OR-REPICK-MARKET; `anti_todo_card.py --new --must-do a b c d e f` exits 2; `references/operating_prompt.md` retains the verbatim prompt + 6-row posture table.

## Agents

7 agents. One real bug, otherwise differentiated and non-boilerplate (B2/B3 pass — capture's 210-line persona, inbox pair's halting rules, and andreessen's binding voice could not be swapped unnoticed).

- **BUG — `cs-inbox-setup.md` and `cs-inbox-triage.md` declare `skills: engineering/email/skills/inbox-setup` / `...inbox-triage`. The skills live at `productivity/email/skills/...`; `engineering/email/` does not exist.** Phantom path (B1). Fix: `skills: productivity/email/skills/inbox-setup` (resp. `-triage`).
- B1 trigger phrasing: only `cs-handoff-author` uses explicit "Invoke when…" language. The other six describe the persona but not when to fire; cheap win to prepend "Use when…" to each description.
- `cs-markdown-html-orchestrator` (model: sonnet) carries the same stale assumption indirectly via the skill it wraps — no edit needed once the SKILL.md is fixed.
- Frontmatter style is inconsistent across the set (`tools: [..]` vs `tools: "..."` vs quoted lists; `model: opus`/`sonnet`/`inherit`) — harmless but worth normalizing in an optimization PR.

## Commands

14 commands. All have accurate descriptions (C1). All orchestrate tools or enforce gates a bare prompt would not (C3): the six markdown-html commands embed pre-flight refusal gates + exact pipelines; `/cs:handoff` enforces checklist→linter→save ordering; `/cs:inbox-*` enforce the one-question-per-turn and DRAFTS-ONLY disciplines; `/cs:andreessen` + `/cs:pmf-check` bind verdict tools.

- C2: markdown-html commands + handoff pair carry `argument-hint`; the 6 productivity megaprompt-era commands (andreessen, pmf-check, capture, inbox-setup, inbox-triage, reflect) embed usage in the body instead of `argument-hint` frontmatter — minor normalization.
- `/cs:grill-markdown-html` and `/cs:design-system` are genuinely distinct surfaces (grill vs route vs onboard); no merge candidates.

## Plugin manifests

6 plugins, all schema-valid (repo-wide `check_plugin_json.py --all` green), all using canonical `./`-prefixed skills arrays.

- **markdown-html-skills (2.10.3):** description counts verified — 15 tools (3×5 ✓), 15 references (3×5 ✓), 4 assets (1 schema + 3 templates ✓), 5 skill paths ✓. E2/E3 pass. Best manifest in scope.
- **Productivity five (all 2.9.0):** coherent with their marketplace.json entries (E3 pass), though frozen at 2.9.0 while the repo is at 2.10.3 — per repo policy versions should track releases; bump at next touch.
- **Name drift (low):** marketplace entry names differ from plugin.json `name` for four plugins — `capture-skill`/`capture`, `email-pair`/`email`, `reflect-skill`/`reflect`, `handoff-productivity`/`handoff`. If intentional (ClawHub slug conflicts), document it; otherwise align.
- `handoff` plugin correctly omits a `hooks` key in plugin.json while shipping `hooks/hooks.json` — Claude Code's auto-discovery convention; hooks verified working via `${CLAUDE_PLUGIN_ROOT}` commands.

## Hooks

2 hooks (handoff SessionStart + SessionEnd). Both stdlib-only, fail-open (`sys.exit(0)` on import error — "hook must never break a session"), env-disable verified (`HANDOFF_SESSIONSTART=0` / `HANDOFF_SESSIONEND=0`), 12,000-char body cap on injected handoff prevents context blowout. D4 by-design stdin exception documented in-file. PASS.
