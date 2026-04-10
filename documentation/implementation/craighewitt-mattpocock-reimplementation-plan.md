# CraigHewitt + MattPocock Skills — Reimplementation Plan

**Status:** Deferred (captured 2026-04-10, not yet executed)
**Source:** User-installed skill collections at `~/.claude/skills-sources/thecraighewitt-skills/` and `~/.claude/skills-sources/mattpocock-skills/`
**Goal:** Build better, more practical versions of selected skills from both collections inside claude-code-skills, reflecting real user workflows.

---

## Source collections surveyed

### TheCraigHewitt Skills (49 skills)
- **Layout:** `sales/` (21), `ceo/` (10), `youtube/` (15), `coding/` (2), `general/` (1)
- **Depth:** Avg ~420 lines per skill. Deep playbooks, opinionated frameworks (SPIN, MEDDIC, Gap Selling, retention curves).
- **Strengths:** Battle-tested methodologies from a working SaaS founder + YouTube creator. Context-aware via persistent `BUSINESS_CONTEXT.md`.
- **Gaps:** Mostly prompt-only. No scripts, no templates, no reference docs, no measurement, no skill chaining beyond naming.

### MattPocock Skills (19 skills)
- **Layout:** Flat directory. Themes: Planning & Design, Development, Tooling & Setup, Writing & Knowledge.
- **Depth:** Avg ~90 lines per skill (TDD has 6 supporting reference files).
- **Strengths:** Composable engineering pipeline (`grill-me` → `write-a-prd` → `prd-to-issues`). Some real shell scripts (`git-guardrails-claude-code`, `setup-pre-commit`). Tracer-bullet TDD methodology.
- **Gaps:** Light on examples, assumes prior knowledge ("deep modules", "tracer bullets"), narrow to software engineering.

---

## Overlap analysis vs existing claude-code-skills repo

| Domain | Existing skill | New material overlaps? | Net-new |
|---|---|---|---|
| Sales | `marketing-skill/cold-email`, `marketing-skill/email-sequence`, `business-growth/sales-engineer`, `business-growth/revenue-operations` | Partial | discovery-call, demo-script, objection-handling, negotiation, pipeline-review, forecast, win-loss-analysis, proposal-pricing, outbound-sequence, cold-call, lead-research, prospect-research, direct-mail, referral-intro, event-networking |
| CEO | `c-level-advisor/ceo-advisor`, `c-level-advisor/founder-coach`, `c-level-advisor/decision-logger` | Partial | weekly-review, quarterly-review, financial-review, one-on-ones, hiring, delegation, strategic-sparring, meeting-prep, content-repurpose |
| YouTube/Creator | ❌ none | ✅ entirely net-new | All 15 skills (idea-generation, hook-writing, title-craft, thumbnail-design, script-structure, retention-editing, description-seo, end-screen-cta, channel-strategy, channel-audit, content-calendar, video-analysis, audience-research, collab-outreach) |
| Engineering process | `engineering-team/senior-qa`, `engineering-team/code-reviewer` | ❌ no TDD/PRD/grill equivalents | write-a-prd, grill-me, tdd-vertical-slice, design-an-interface, improve-codebase-architecture, triage-issue, git-guardrails, setup-pre-commit, ubiquitous-language, edit-article, qa |

---

## Proposed build — 4 pods, ~30 skills

Each pod targets a high-value area and is built to claude-code-skills standards: `SKILL.md` + `scripts/` (Python CLI tools) + `references/` (knowledge bases) + `assets/` (templates + example galleries). All new skills include YAML frontmatter, measurable outputs, and integration hooks with existing skills.

### Pod 1 — `creator-team/` (NEW DOMAIN, ~10 skills) — highest priority
**Why:** Entirely net-new territory. No YouTube/creator skills in our repo today. Obvious gap for solo creators, YouTubers, content businesses.

**Skills to build:**
1. `creator-context` — persistent context file (channel, audience, niche, tone, goals) that other creator skills read
2. `idea-generation` — content ideation w/ scoring matrix, competitive gap analysis, keyword tool integration
3. `hook-writing` — first-30-seconds hook generator with retention curve benchmarks
4. `title-craft` — SEO + browse-optimized title generator with A/B scoring tool
5. `thumbnail-design` — composition rules, psychology brief, Canva/Figma brief generator
6. `script-structure` — long-form script skeleton with retention beat markers
7. `retention-editing` — edit decision list (EDL) generator, pacing analyzer
8. `channel-audit` — YouTube API analytics pull + diagnosis
9. `content-calendar` — batch planning + pillar allocation
10. `audience-research` — survey builder, comment-mining tool, persona synthesizer

**Python tools to add:** `youtube_analytics_pull.py`, `retention_analyzer.py`, `title_scorer.py`, `thumbnail_brief.py`, `idea_scorer.py`, `hook_rater.py`
**References:** retention curve theory, thumbnail psychology, YouTube algorithm primer, brand voice guide
**Templates:** channel brief, video brief, script outline, thumbnail brief, calendar spreadsheet

### Pod 2 — `business-growth/sales-motion/` (EXTEND, ~10 skills)
**Why:** We have strategic `sales-engineer` but no tactical motion playbooks. Tactical motion skills are what sales reps actually run daily.

**Skills to build:**
1. `sales-motion-context` — persistent ICP, stage definitions, methodology choice (MEDDIC/SPIN)
2. `discovery-call` — call framework + scorecard
3. `demo-script` — scoped demo generator with tailored value mapping
4. `objection-handling` — objection library + response bank
5. `negotiation` — concession matrix, BATNA scaffolding
6. `forecast` — weighted pipeline math, commit/upside/best-case categorizer
7. `pipeline-review` — stage hygiene checker, stalled deal detector
8. `win-loss-analysis` — pattern extractor across closed deals
9. `proposal-pricing` — pricing tiers, ROI builder
10. `outbound-sequence` — multi-channel cadence designer with personalization tokens

**Python tools:** `forecast_calculator.py`, `pipeline_hygiene_checker.py`, `deal_score.py`, `sequence_builder.py`, `win_loss_miner.py`
**References:** MEDDIC, SPIN, Gap Selling, Sandler frameworks; deal stage rubrics; objection library
**Templates:** call scorecard, discovery framework, demo script shell, proposal template, forecast spreadsheet, sequence JSON

### Pod 3 — `c-level-advisor/operating-rhythm/` (EXTEND, ~6 skills)
**Why:** We have strategic advisors but thin operating rhythm coverage. These are the recurring rituals that keep a company running.

**Skills to build:**
1. `weekly-review` — 15-min scorecard + blocker surfacing
2. `quarterly-review` — 90-min reset + OKR refresh
3. `financial-review` — P&L walkthrough + variance analysis
4. `one-on-ones` — 1:1 framework, check-in cadence
5. `hiring` — problem-based role spec, candidate rubric, comp positioning
6. `delegation` — delegation matrix, stretch assignment framework
7. `strategic-sparring` — pressure-test decisions, 30/90/180 day consequence mapping (integrates with existing `decision-logger`)

**Python tools:** `scorecard_builder.py`, `okr_tracker.py`, `delegation_matrix.py`, `hiring_rubric_scorer.py`
**References:** hiring frameworks, 1:1 playbooks, OKR design, operating cadence patterns
**Templates:** weekly scorecard, QBR deck outline, 1:1 agenda, hiring scorecard, delegation matrix

### Pod 4 — `engineering/dev-process/` (NEW POWERFUL POD, ~6 skills)
**Why:** MattPocock's methodology (deep modules, tracer bullets, vertical slices, HITL vs AFK) isn't represented in our engineering pods. These are "how you think about building" skills, not role-based.

**Skills to build:**
1. `grill-me` — relentless interview to resolve decision tree before any code
2. `write-a-prd` — interactive PRD builder → GitHub issue
3. `prd-to-issues` — break PRD into independently-grabbable GitHub issues
4. `tdd-vertical-slice` — tracer-bullet TDD (not horizontal slices)
5. `design-an-interface` — generate 3+ parallel API designs, compare on depth/simplicity
6. `triage-issue` — bug investigation → fix plan → GitHub issue
7. `git-guardrails` — PreToolUse hook installer blocking dangerous git commands

**Python tools:** `prd_to_issues.py`, `issue_filer.py`, `git_guardrails_installer.py`, `module_depth_analyzer.py`
**References:** Ousterhout deep modules primer, tracer bullet pattern, vertical slice TDD, ports & adapters
**Templates:** PRD template, GitHub issue template, refactor plan template, pre-commit hook config

---

## What makes this "better" than the originals

1. **Python automation** — every skill has at least one executable tool, not just prompts
2. **Real templates** — ready-to-fill artifacts, not "here's the structure"
3. **Measurement baked in** — benchmarks and success metrics per skill (e.g., cold-email reply rate targets, retention curve thresholds)
4. **Example galleries** — 3-5 anonymized real outputs per skill
5. **Shared context models** — per-pod context files (creator-context, sales-motion-context) that multiple skills read, so the user doesn't re-answer diagnostic questions each session
6. **Skill chaining** — explicit orchestration (e.g., `creator-workflow` meta-skill chains ideation → script → hook → thumbnail)
7. **Integration with existing skills** — `pipeline-review` reads from `revenue-operations`; `strategic-sparring` writes to `decision-logger`
8. **Cross-tool portability** — plugin.json, marketplace entry, symlink-friendly for Codex/Cursor/OpenClaw

## What NOT to port

- `coding/ralph` — autonomous PRD impl loop. Complex, Docker-sandboxed, overlaps with our `self-improving-agent`. Skip or reference.
- Duplicates where we already have strong coverage (`cold-email` — our existing version is deeper)
- Anything too opinionated to generalize (e.g., specific SaaS founder methodology that doesn't fit all audiences)

## Execution plan

- **Phase A — Pod 1 (creator-team)** as proof of concept. Highest-value, entirely net-new, measurable success.
- **Phase B — Pod 2 (sales-motion)** once Phase A is validated.
- **Phase C — Pod 3 (operating-rhythm)** extends existing c-level-advisor.
- **Phase D — Pod 4 (dev-process)** extends engineering/.

**Estimated effort:** 2-3 focused sessions per pod (~10 sessions total). Can be run as separate PRs off `dev`.

**Branch strategy:** `feature/creator-team-pod1` → PR to `dev` → repeat per pod.

**Version target:** v2.3.0 when Pod 1 ships; v2.4.0 when all 4 pods complete.

---

**Next action when resumed:** Confirm scope with user (all 4 pods vs start with Pod 1), then create `feature/creator-team-pod1` branch and begin building `creator-context` + first 3 skills.
