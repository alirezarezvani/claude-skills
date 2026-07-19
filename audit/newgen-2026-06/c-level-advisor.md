# Domain audit: c-level-advisor/ — new-gen model optimization
Audited: 2026-06-10 · Unique skills: 61 (of 66 SKILL.md files incl. dual-published) · Agents: 14 (13 cs-* in c-level-agents/agents/ + devils-advocate; cs-ceo/cs-cto live outside the folder in /agents/c-level/) · Plugins: 8

## Scorecard

| Skill | Verdict | Top issue |
|---|---|---|
| **skills/ (main bundle, 33)** | | |
| agent-protocol | OPTIMIZE | Valid-roles list frozen at 9 roles; 5 newer roles (GC/CDO/CAIO/CCO/VPE) can't be invoked per protocol |
| board-deck-builder | OPTIMIZE | Phantom `/board-deck` command in Quick Start |
| board-meeting | OPTIMIZE | Role tables omit 5 newer roles; `/cs:board` vs `/cs:boardroom` naming clash |
| c-level-skills | CUT-OR-MERGE | Bundle README posing as a skill; contradicts cs-onboard and board-meeting on protocol details |
| ceo-advisor | KEEP | ~30 lines of shared boilerplate (Communication/Context Integration) duplicated across all role skills |
| cfo-advisor | KEEP | — |
| change-management | KEEP | — |
| chief-ai-officer-advisor | KEEP | A6 watch: hardcoded 2026 API/GPU pricing will rot |
| chief-customer-officer-advisor | KEEP | — |
| chief-data-officer-advisor | KEEP | — |
| chief-of-staff | OPTIMIZE | "28 skills" stale (33); routing matrix omits 5 roles; 3rd divergent decision-log path |
| chro-advisor | KEEP | — |
| ciso-advisor | KEEP | — |
| cmo-advisor | KEEP | — |
| company-os | KEEP | — |
| competitive-intel | OPTIMIZE | 5 phantom `/ci:*` commands in Quick Start |
| context-engine | KEEP | — |
| coo-advisor | KEEP | — |
| cpo-advisor | KEEP | — |
| cro-advisor | KEEP | — |
| cs-onboard | OPTIMIZE | Conflicts with c-level-agents `/cs:onboard` (7-dimension vs 12-question interview, same output file) |
| cto-advisor | KEEP | — |
| culture-architect | KEEP | — |
| decision-logger | KEEP | Memory path conflict with `/cs:decide` (flagged there) |
| founder-coach | KEEP | — |
| general-counsel-advisor | KEEP | — |
| internal-narrative | KEEP | — |
| intl-expansion | OPTIMIZE | Thin; no tool; no verification loop |
| ma-playbook | OPTIMIZE | Thinnest skill in domain; valuation numbers unsourced; no tool |
| org-health-diagnostic | KEEP | — |
| scenario-war-room | KEEP | Phantom `/war-room` invocation (minor) |
| strategic-alignment | KEEP | — |
| vpe-advisor | KEEP (dual-published) | Workflow CLI paths inconsistent with Quick Start paths |
| **executive-mentor/skills/ (6)** | | |
| executive-mentor | KEEP | — |
| challenge | KEEP | — |
| board-prep | KEEP | — |
| hard-call | OPTIMIZE | Placeholder description (A1 fail) |
| postmortem | OPTIMIZE | Placeholder description (A1 fail) |
| stress-test | OPTIMIZE | Placeholder description (A1 fail) |
| **c-level-agents/skills/ (22)** | | |
| c-level-agents (overview) | OPTIMIZE | Frontmatter says 8 agents / 17 commands; reality is 13 / 21 |
| founder-mode | OPTIMIZE | Routing table omits CDO/CAIO/CCO/VPE — auto-router can't reach 4 of 13 advisors |
| office-hours | KEEP | — |
| onboard | OPTIMIZE | Second, divergent founder interview writing the same `~/.claude/company-context.md` |
| brief | OPTIMIZE | Affected-roles checklist omits 5 newer advisors |
| boardroom | KEEP | — |
| decide | OPTIMIZE | Writes `~/.claude/decisions/` while decision-logger skill specifies `memory/board-meetings/` |
| execute | KEEP | — |
| post-mortem | KEEP | — |
| freeze | KEEP | `/cs:unfreeze` has no skill file (handled in-file; minor) |
| cross-eval | KEEP | — |
| cfo-review | KEEP | — |
| cmo-review | KEEP | — |
| cpo-review | KEEP | — |
| cro-review | KEEP | — |
| cto-review | KEEP | — |
| ciso-review | KEEP | — |
| gc-review | KEEP | — |
| cdo-review | OPTIMIZE | Routes to phantom `/cs:chro-review` |
| caio-review | OPTIMIZE | Routes to phantom `/cs:chro-review` |
| cco-review | OPTIMIZE | Routes to phantom `/cs:chro-review` |
| vpe-review | OPTIMIZE | Routes to phantom `/cs:chro-review` |
| **Dual-published standalone copies** | (counted above) | chief-ai-officer-advisor, chief-customer-officer-advisor, chief-data-officer-advisor, general-counsel-advisor, vpe-advisor |

**Totals: KEEP 40 · OPTIMIZE 20 · REWRITE 0 · CUT-OR-MERGE 1**

## Domain-level findings

### 1. Dual-publication map (5 pairs, zero drift today — but no guard)

Each of these exists twice, byte-identical (verified with `diff -rq` across SKILL.md + all references + all scripts):

| Bundle copy (`c-level-advisor/skills/<x>/`) | Standalone copy (`c-level-advisor/<x>/skills/<x>/`) | Drifted? |
|---|---|---|
| chief-ai-officer-advisor | chief-ai-officer-advisor | No |
| chief-customer-officer-advisor | chief-customer-officer-advisor | No |
| chief-data-officer-advisor | chief-data-officer-advisor | No |
| general-counsel-advisor | general-counsel-advisor | No |
| vpe-advisor | vpe-advisor | No |

The duplication is intentional (standalone-installable plugin AND bundled in c-level-skills) but there is **no sync script, no CI check, and no comment in either copy declaring the other copy exists**. Any future edit to one side silently forks the skill. **Recommendation:** add a `scripts/check_dual_published.py` (or extend ci-quality-gate) that diffs the 5 pairs and fails on divergence; alternatively replace standalone copies with a build step. This is the single highest-leverage guard for the domain. Drift status: GREEN today, unprotected.

### 2. Role-registry drift — the domain's 9-role core never learned about its 5 newest roles

The domain grew from 9 C-roles to 14 (GC v2.5.1, CDO v2.5.2, CAIO v2.5.3, CCO v2.5.4, VPE v2.5.5), but the orchestration core was never updated:

- `agent-protocol/SKILL.md` — "Valid roles: ceo, cfo, cro, cmo, cpo, cto, chro, coo, ciso". Per the protocol's own hard rules, `[INVOKE:gc|...]` etc. is undefined.
- `chief-of-staff/SKILL.md` — routing matrix and "routes to 28 skills total" (now 33) omit the 5 roles entirely.
- `board-meeting/SKILL.md` — Phase 1 role-activation table and Phase 2 ordering list only the original 9.
- `c-level-agents/skills/founder-mode/SKILL.md` — keyword routing table has no rows for data/AI/customer/VPE topics; "retention dropped" routes to CRO, never CCO.
- `c-level-agents/skills/brief/SKILL.md` — affected-roles checklist stops at cs-chief-of-staff.
- `c-level-agents/skills/c-level-agents/SKILL.md` frontmatter — "8 cs-* agents… 17 /cs:* commands" vs actual 13 / 21.
Fix once, in all six files, in one PR.

### 3. Three competing decision-memory architectures

- `decision-logger` skill: `memory/board-meetings/decisions.md` (Layer 2) + `YYYY-MM-DD-raw.md` (Layer 1)
- `chief-of-staff` skill: `~/.claude/decision-log.md`
- `/cs:decide`: `~/.claude/decisions/approved/` + `~/.claude/decisions/raw/`

All three claim to be "the" two-layer memory. An agent following decision-logger will never find decisions written by `/cs:decide`. Pick one canonical layout (the `~/.claude/decisions/` form is most portable) and update the other two.

### 4. Two competing founder-onboarding interviews

`cs-onboard` (7 dimensions, ~45 min, conversational probes) and `c-level-agents/onboard` (12 structured questions) both write `~/.claude/company-context.md` with **different schemas**; `c-level-skills/SKILL.md` describes a third, 7-question variant that writes to "the project root". The context-engine "Required Context Fields" match only the cs-onboard schema. Reconcile to one interview + one schema.

### 5. Phantom slash commands

Referenced but existing nowhere in `commands/` nor as plugin command/skill files: `/board-deck`, `/war-room`, `/health`, `/health:dimension`, `/ci:landscape|battlecard|winloss|update|map`, `/cs:chro-review`, `/cs:coo-review` (routed-to from 4+ review skills), `/cs:board` + `/cs:decisions` + `/cs:review` + `/cs:setup` + `/cs:update` (pre-date the c-level-agents `/cs:*` namespace and now collide with it). Either create thin command files or rewrite the Quick Starts as natural-language triggers.

### 6. Agent reference-file hallucinations (see Agents section)

7 of 13 cs-* agents cite knowledge-base filenames that do not exist on disk — apparently written from memory of what the references *should* be called. New-gen models will attempt to Read these paths and fail.

### 7. Shared boilerplate tax

Every role-advisor SKILL.md carries the identical ~25-line Communication / Context Integration / Internal Quality Loop block that `agent-protocol/SKILL.md` already owns. Across ~15 skills that's ~375 lines of duplicated context. A one-line pointer ("Output passes the Internal Quality Loop — see agent-protocol/SKILL.md") would reclaim it. Also: `Keywords` sections (10–40 terms each) are dead weight for new-gen trigger matching since the frontmatter description already carries triggers.

### 8. Repo hygiene

- `ceo-advisor.zip` (32K) and `cto-advisor.zip` (28K) are stray build artifacts at the domain root — delete.
- `c_level_leadership_skills_overview.md` at domain root duplicates CLAUDE.md content.
- `c-level-advisor/CLAUDE.md` says "Skills Deployed: 33 … + 21 /cs:* sub-skills" but also "28 skills" in the architecture intro of chief-of-staff; CLAUDE.md itself says "13 cs-* persona agents" correctly but root repo CLAUDE.md says "51+ agents (cs-* + 7 personas)" — counts drift in 3 places.

## Per-skill findings

### c-level-skills (skills/c-level-skills/)
- **Verdict: CUT-OR-MERGE**
- Issues: (1) It's the bundle's README wearing a SKILL.md frontmatter — `name: "c-level-advisor"` doesn't even match its folder. (2) Describes `/cs:setup` as a 7-question form writing company-context.md "to the project root", contradicting cs-onboard (7 dimensions, `~/.claude/`) and c-level-agents/onboard (12 questions). (3) Describes `/cs:board` as 3 phases; board-meeting skill defines 6. (4) Stale counts (28 skills, 25 tools). (5) As a trigger surface it competes with chief-of-staff for the same routing job.
- Verify: `grep -c "Phase" skills/c-level-skills/SKILL.md` no longer describes a board protocol that disagrees with `board-meeting/SKILL.md`; content merged into README.md or CLAUDE.md; `find c-level-advisor/skills -name SKILL.md | wc -l` drops by 1 (or file becomes a pure router stub < 40 lines).

### agent-protocol
- **Verdict: OPTIMIZE**
- Issues: (1) Valid-roles list omits gc/cdo/caio/cco/vpe. (2) Peer-verification table has no rows for legal/data/AI/customer claims. (3) At 418 lines it carries the Communication Standard that 15 sibling skills then duplicate — the duplication should collapse toward this file.
- Verify: `grep -E "gc|cdo|caio|cco|vpe" skills/agent-protocol/SKILL.md` returns the invocation registry rows; the 5 newer role SKILL.mds still render the `[INVOKE:role|...]` examples without contradiction; sibling role skills reference (not restate) the quality loop.

### chief-of-staff
- **Verdict: OPTIMIZE**
- Issues: (1) "routes to 28 skills total" — 33 exist. (2) Routing matrix has no rows for legal, data strategy, AI strategy, customer/retention, eng-delivery topics. (3) Decision log path `~/.claude/decision-log.md` is a third memory location (see domain finding 3). (4) References `references/routing-matrix.md` — confirm it covers all 14 roles too.
- Verify: routing matrix includes GC/CDO/CAIO/CCO/VPE rows; `grep "28 skills" SKILL.md` → no hits; decision-log path identical to decision-logger's canonical path.

### board-meeting
- **Verdict: OPTIMIZE**
- Issues: (1) Phase 1 activation table + Phase 2 ordering cover 9 roles. (2) Invoked as `/cs:board` here but `/cs:boardroom` in c-level-agents — two names, one protocol. (3) Memory paths must match the canonical decision-memory layout chosen in domain finding 3.
- Verify: one command name used in both files (`grep -r "cs:board\b" c-level-advisor/` returns 0 or all-consistent); activation table lists 14 roles; memory paths match decision-logger.

### board-deck-builder
- **Verdict: OPTIMIZE**
- Issues: (1) `/board-deck [quarterly|monthly|fundraising]` doesn't exist as a command anywhere. (2) No CISO/GC/data sections cross-referenced to the 5 newer roles where relevant (minor). Content itself (4-act structure, bad-news framework, asks slide) is genuinely good.
- Verify: Quick Start either points at an existing command file or is rephrased as a trigger sentence; `references/deck-frameworks.md` + `templates/board-deck-template.md` exist (they do — keep green).

### competitive-intel
- **Verdict: OPTIMIZE**
- Issues: (1) Five phantom `/ci:*` commands as the entire Quick Start. (2) No script despite tabular scoring (threat matrix, feature-gap) being mechanizable — optional. Frameworks (8 tracking dimensions, win/loss interview protocol, over/under-tracking signals) are real.
- Verify: Quick Start contains no `/ci:` strings OR `commands/ci-*.md` files exist; battlecard template still referenced and present.

### cs-onboard
- **Verdict: OPTIMIZE**
- Issues: (1) Same output file as c-level-agents/onboard with a different schema (see domain finding 4). (2) `/cs:setup` + `/cs:update` names collide with the c-level-agents `/cs:` namespace without skill files behind them.
- Verify: exactly one interview skill owns `~/.claude/company-context.md`; context-engine "Required Context Fields" match the surviving schema; `grep -rl "company-context.md" c-level-advisor | xargs grep -l "project root"` → 0 hits.

### intl-expansion
- **Verdict: OPTIMIZE**
- Issues: (1) No script, no verification loop — ends at a checklist. (2) Market-selection scoring matrix is the mechanizable core; a 20-line stdlib scorer would lift this to KEEP. (3) Weakest A5 in the cross-cutting set: most rows ("research local buying behavior") a frontier model already knows.
- Verify: add `scripts/market_entry_scorer.py --sample` exits 0 emitting JSON with per-market weighted score; SKILL.md Quick Start invokes it; `references/regional-guide.md` retains region-specific regulatory facts (data residency, entity requirements) that aren't generic.

### ma-playbook
- **Verdict: OPTIMIZE**
- Issues: (1) Thinnest skill in domain (98 lines), pure checklist. (2) "2-15x ARR for SaaS" and "$1-3M per engineer" unsourced and freshness-fragile (A6). (3) No tool — a DD red-flag scanner or earnout-structure checker would be in-pattern with general-counsel-advisor. (4) Overlaps general-counsel-advisor (LOI/negotiation) and chief-data-officer-advisor (data diligence) without cross-references.
- Verify: multiples carry a source + as-of date; Adjacent Skills section cross-links gc-advisor + cdo-advisor; either a script exists passing `--help`, or the skill explicitly delegates quantitative work to cfo-advisor tools.

### executive-mentor/hard-call, postmortem, stress-test (3 skills)
- **Verdict: OPTIMIZE** (each)
- Issues: descriptions are literal placeholders (`"/em -hard-call — Framework for Decisions With No Good Options"`) — no trigger phrasing, malformed command name (`/em -hard-call` vs `/em:hard-call`). Bodies are excellent (10/10/10, Grove test, proper 5-Whys, change-register-with-verification-date); only the frontmatter fails.
- Verify: `python3 scripts/audit_skills.py` (repo validator) no longer flags these three for missing trigger; each description ≥ 1 "Use when" clause and < 1024 chars.

### c-level-agents (overview skill)
- **Verdict: OPTIMIZE**
- Issues: (1) Frontmatter `agents:` lists 8 (13 exist), `commands:` lists 17 (21 exist) — a new-gen router using this metadata will never surface vpe/cdo/caio/cco surfaces. (2) References block links `../../references/persona-voices.md` and `../references/persona-voices.md` inconsistently (one resolves, one doesn't).
- Verify: frontmatter agent/command lists match `ls agents/ | wc -l` = 13 and `ls skills/ | wc -l` − 1 = 21; all relative links resolve from the file's own directory.

### founder-mode
- **Verdict: OPTIMIZE**
- Issues: (1) Routing table has no signal rows for retention/CS (CCO), data architecture/training data (CDO), model selection/AI risk (CAIO), DORA/eng hiring (VPE) — the self-described "killer command" silently misroutes 4 domains to the wrong advisor. (2) Claims routing knowledge of decisions via decision-logger — path depends on domain finding 3.
- Verify: table includes the 4 missing roles with ≥ 4 keywords each; example "`the win rate dropped`" vs "`gross retention dropped`" route to CRO vs CCO respectively.

### onboard (c-level-agents)
- **Verdict: OPTIMIZE** — see domain finding 4. Verify: one canonical schema; symlink guidance (llm-wiki bridge) unchanged.

### brief
- **Verdict: OPTIMIZE**
- Issues: affected-roles checklist (drives boardroom panel composition) omits cs-general-counsel/cdo/caio/cco/vpe — a pricing-with-data-licensing brief can't seat the right panel.
- Verify: checklist lists all 14 advisors; `grep -c "cs-" skills/brief/SKILL.md` ≥ 14.

### decide
- **Verdict: OPTIMIZE**
- Issues: writes `~/.claude/decisions/{raw,approved}/` while decision-logger (the skill it claims to invoke) specifies `memory/board-meetings/`. The "two-layer memory" exists in two incompatible places.
- Verify: `grep -r "decisions/approved\|board-meetings/decisions" c-level-advisor/ -l` shows one canonical layout across decide, decision-logger, chief-of-staff, board-meeting.

### cdo-review, caio-review, cco-review, vpe-review (4 skills)
- **Verdict: OPTIMIZE** (each, same one-line fix)
- Issues: Routing sections send follow-ups to `/cs:chro-review` (and vpe-review also implies `/cs:coo-review`) — neither exists. Everything else is exemplary: role-specific forcing questions with thresholds, exact CLI to the backing skill's tools, structured output with verdict gates.
- Verify: every `/cs:*` string in the Routing sections resolves to a file under `c-level-agents/skills/*/SKILL.md`; `grep -r "cs:chro-review\|cs:coo-review" c-level-agents/` → 0 hits (or the two commands are created).

## KEEP-verdict verification criteria

- **ceo-advisor** — metrics dashboard targets present (burn multiple < 2x, NPS > 40); `python3 skills/ceo-advisor/scripts/strategy_analyzer.py` exits 0; boilerplate block replaced by agent-protocol pointer without losing the Tree-of-Thought section.
- **cfo-advisor** — all 3 scripts exit 0 bare; SKILL.md keeps burn-multiple/Rule-of-40/NDR thresholds table; "not a financial analyst skill" disambiguation to finance/ retained.
- **cto-advisor** — tech-debt priority formula `(Severity × Blast Radius) / Cost-to-fix` intact; both scripts exit 0; ADR template with 3-year-TCO checklist retained.
- **coo-advisor** — process-maturity 5-level table + both scripts green; VPE-vs-COO scope note added when role registry is fixed (advisory).
- **cpo-advisor** — D30 retention thresholds (20% consumer / 40% B2B) + invest/maintain/kill table intact; `pmf_scorer.py` exits 0.
- **cmo-advisor** — channel-level CAC discipline + pipeline-coverage 3–4x targets intact; both scripts green.
- **cro-advisor** — Magic Number + CAC-payback formulas verbatim; NRR benchmark table intact; both scripts green.
- **ciso-advisor** — `ALE = SLE × ARO` formula + compliance sequencing (SOC2 T1 → T2 → ISO/HIPAA) intact; both scripts green.
- **chro-advisor** — calibrated rating distribution table + compa-ratio 0.95–1.05 target intact; both scripts green.
- **chief-data-officer-advisor** (dual) — `ai_training_data_audit.py` bare-run exits 0 with GO/MITIGATE/NO-GO verdicts; both copies stay byte-identical (`diff -rq` clean); GDPR Art. 6 citations present in references.
- **chief-ai-officer-advisor** (dual) — 3 scripts exit 0; EU AI Act tier table retains Article citations; pricing figures carry an as-of date (A6 guard); copies identical.
- **chief-customer-officer-advisor** (dual) — `retention_decomposition_analyzer.py` flags leaky-bucket (NRR>100 ∧ GRR<85) on sample; GRR/NRR threshold table intact; copies identical.
- **general-counsel-advisor** (dual) — `contract_risk_scanner.py` bare-run flags ≥ 1 finding on bundled sample; "Not legal advice" disclaimer in SKILL.md + both tools; copies identical.
- **vpe-advisor** (dual) — `delivery_throughput_analyzer.py` emits DORA verdict + bottleneck (verified: exits 0, "Overall DORA level: High", bottleneck stage + % of cycle); fix workflow paths `../../skills/vpe-advisor/...` → `scripts/...`; copies identical.
- **context-engine** — 90-day staleness gate + anonymization never-send list intact; aligned to surviving onboarding schema.
- **decision-logger** — `python3 scripts/decision_tracker.py --demo` exits 0; DO_NOT_RESURFACE enforcement block intact; canonical path winner of domain finding 3.
- **scenario-war-room** — max-3-variables rule + cascade map + trigger-point examples intact; `scenario_modeler.py` exits 0; `/war-room` string removed or backed by a command.
- **org-health-diagnostic** — `health_scorer.py --json` emits machine-parseable dimension scores; 8-dimension thresholds + dimension-interaction table intact.
- **strategic-alignment** — `alignment_checker.py` detects orphans/conflicts/coverage-gaps on sample JSON; 5-people articulation test intact.
- **culture-architect** — values→behavioral-anchors table + culture-health score bands (80/65/50) intact.
- **company-os** — L10 agenda + IDS + rocks 3–7 cap intact; no phantom commands introduced.
- **founder-coach** — Skill×Will matrix + delegation ladder + calendar-audit target % table intact.
- **change-management** — ADKAR per-change-type timelines + resistance-pattern table intact.
- **internal-narrative** — audience translation matrix + contradiction check + 4-hour crisis rule intact.
- **executive-mentor / challenge / board-prep** — both scripts exit 0; challenge keeps assumption-confidence×impact matrix; board-prep keeps numbers-cold list.
- **office-hours / boardroom / execute / post-mortem / freeze / cross-eval** — pipeline artifact paths (`~/.claude/briefs|boardroom|execution|postmortems|freezes`) mutually consistent; each Routing section's `/cs:*` targets resolve; boardroom keeps Phase-2 isolation + dissent column; post-mortem keeps pre-committed-criteria scoring; freeze keeps default-period table.
- **cfo/cmo/cpo/cro/cto/ciso/gc-review** — every relative `python ../../../skills/...` path resolves from the file's directory; six questions per role remain role-specific (no copy-paste across roles); verdict gates (🟢/🟡/🔴) intact.

## Agents

| Agent | B1 (frontmatter) | B2 (differentiation) | B3 (body) | Top issue |
|---|---|---|---|---|
| cs-cfo-advisor | ⚠️ no "Use when" | PASS — burn-multiple/dilution forcing Qs, bear-case rule | PASS | model: opus justified? |
| cs-cmo-advisor | ⚠️ | PASS — one-sentence-positioning gate | **FAIL refs** — cites `growth_playbooks.md`, `marketing_operations.md` (don't exist; actual: growth_frameworks.md, marketing_org.md) | phantom KB files |
| cs-cro-advisor | ⚠️ | PASS — coverage>forecast, discount-creep tell | **FAIL refs** — all 3 KB names wrong (`revenue_operations/sales_motion/retention_expansion` vs actual sales_playbook/pricing_strategy/nrr_playbook) | phantom KB files |
| cs-cpo-advisor | ⚠️ | PASS — retention-curve-before-roadmap | **FAIL refs** — all 3 wrong (`product_vision/portfolio_strategy/pmf_framework` vs product_strategy/product_org_design/pmf_playbook) | phantom KB files |
| cs-coo-advisor | ⚠️ | PASS — DRI/cadence refusal gate | **FAIL refs** — all 3 wrong (`operating_cadence/okr_execution/scaling_playbooks` vs ops_cadence/process_frameworks/scaling_playbook) | phantom KB files |
| cs-chro-advisor | ⚠️ | PASS — no-promotion-without-ladder refusal | **FAIL refs** — all 3 wrong (`hiring_systems/comp_philosophy/leveling_ladders` vs people_strategy/comp_frameworks/org_design) | phantom KB files |
| cs-ciso-advisor | ⚠️ | PASS — assume-breach, $-quantified risk | **FAIL ref** — cites `threat_modeling.md` (doesn't exist; actual security_strategy.md) | phantom KB file |
| cs-chief-of-staff | ⚠️ | PASS — pure router, distinct job | **FAIL refs** — `routing_logic.md`/`synthesis_patterns.md` vs actual routing-matrix.md/synthesis-framework.md; routing table omits 5 roles | phantom KB files + role drift |
| cs-general-counsel-advisor | PASS (has disclaimer + scope) | PASS — escalate-to-counsel hard rule | PASS — exact tool wiring, correct paths | — |
| cs-cdo-advisor | PASS | PASS — "what decision does this data drive" refusal gate | PASS | — |
| cs-caio-advisor | PASS | PASS — no-eval-no-ship gate | PASS | — |
| cs-cco-advisor | PASS | PASS — gross-over-NRR, which-customer-would-you-fire | PASS | — |
| cs-vpe-advisor | PASS | PASS — explicit 4-way differentiation (CTO/eng-lead/CHRO/COO) | PASS | — |
| devils-advocate (executive-mentor) | no frontmatter at all (prose file) | PASS — exactly-3-concerns + never-clean-approval rules; behavior-changing | PASS — worked example | add YAML frontmatter |

**B2 assessment:** the personas genuinely pass the swap test. Each agent has different refusal gates (CFO: no scale on broken unit economics; CAIO: no eval set, no ship; CCO: no CS hire without a named customer outcome; CHRO: no promotion without ladder step), different tool wiring, and different success metrics — swapping cs-cfo-advisor's prompt into cs-cmo-advisor would be noticed immediately. The voice bookending ("opening/forcing/closing") is thin but the underlying workflows differ structurally.

**The systemic agent defect is B-side tool wiring, not differentiation:** 7 of 13 agents (the v2.5.0 batch: cfo is clean; cmo, cro, cpo, coo, chro, ciso, chief-of-staff are not) cite knowledge-base filenames that don't exist on disk. The 5 newer agents (gc, cdo, caio, cco, vpe — written against real files) are clean. Fix: one PR correcting ~16 filenames; verify with a link-checker pass (`for f in agents/*.md; do grep -o '\.\./\.\./skills/[a-z-]*/references/[a-z_-]*\.md' $f | while read p; do test -f "$(dirname $f)/$p" || echo "$f → $p"; done; done` → empty).

Also: `cs-ceo-advisor` and `cs-cto-advisor` live in `/agents/c-level/` outside this folder while 11 sibling links point at them via `../../../../agents/c-level/` — fragile but currently resolving.

## Plugin manifests

8 manifests, all schema-valid, all version 2.9.0 and consistent with marketplace.json (E1/E3 PASS). E2 findings:

| Plugin | Drift |
|---|---|
| c-level-skills (root) | Description says "33 skills + 13 agents + 21 commands" — accurate. But `"skills": ["./skills"]` only ships the bundle dir; the c-level-agents layer named in the description is NOT included in this plugin's skills path (it's a separate plugin) — description overpromises the install. |
| c-level-agents | Accurate (13 agents / 21 commands) — but the bundled overview SKILL.md frontmatter still says 8/17 (see per-skill). Manifest is ahead of its own skill. |
| executive-mentor | Accurate. CLAUDE.md claims it is "the only skill with a plugin.json (namespace: em)" — false since v2.5.x; 7 other plugin.json files exist in the domain. CLAUDE.md statement is the drift, not the manifest. |
| chief-ai-officer-advisor | Accurate, rich. "2026 pricing" claim is a freshness liability shared with the skill (A6). |
| chief-customer-officer-advisor / chief-data-officer-advisor / general-counsel-advisor / vpe-advisor | Accurate; descriptions correctly state "Standalone-installable; also bundled in c-level-skills" — the only place the dual-publication is documented. Mirror this sentence into the SKILL.md of each pair so editors learn about the twin copy. |

Scripts: all 25 bundle scripts pass repo-wide smoke tests (D1); spot-runs of `delivery_throughput_analyzer.py` (DORA verdict + bottleneck %), `decision_tracker.py --demo`, and `health_scorer.py --json` confirm deterministic, sample-embedded, machine-parseable output (D2/D3 PASS).
