# Domain audit: marketing-skill/ + marketing/ — new-gen model optimization
Audited: 2026-06-10 · Skills: 49 (47 in marketing-skill/skills + video-content-strategist + marketing/landing) · Agents: 6 · Commands: 4 · Plugins: 5

## Scorecard

| Skill | Verdict | Top issue |
|---|---|---|
| ab-test-setup | OPTIMIZE | Orphan script `sample_size_calculator.py` never named in SKILL.md |
| ad-creative | OPTIMIZE | Stale Meta ">20% image text = reduced distribution" rule (retired 2021) presented as current |
| aeo | KEEP | — |
| ai-seo | CUT-OR-MERGE | Near-total overlap with `aeo` (same goal, no tooling); two skills own one lane |
| analytics-tracking | OPTIMIZE | GA4 "Conversions" terminology (renamed Key events, Mar 2024); script wiring vague |
| app-store-optimization | KEEP | — |
| brand-guidelines | CUT-OR-MERGE | 93-line generic checklist a frontier model already knows; hardcoded Anthropic identity |
| campaign-analytics | KEEP | — |
| churn-prevention | KEEP | — |
| cold-email | KEEP | — |
| competitor-alternatives | OPTIMIZE | Orphan script `comparison_matrix_builder.py` |
| content-creator | CUT-OR-MERGE | Deprecated redirect still shipping 4 refs + 1 asset + agent + zip |
| content-humanizer | OPTIMIZE | 2/6 on repo checklist (worst in domain); AI-tell list itself aging ("delve" era) |
| content-production | OPTIMIZE | 3 of 4 scripts orphaned in SKILL.md |
| content-strategy | OPTIMIZE | Hollow core ("→ see references"); orphan `topic_cluster_mapper.py` |
| copy-editing | OPTIMIZE | Both scripts (`ai_content_detector`, `readability_scorer`) orphaned |
| copywriting | OPTIMIZE | Orphan `headline_scorer.py` |
| email-sequence | OPTIMIZE | Phantom `../../tools/REGISTRY.md` + 5 integration guide links; none exist |
| form-cro | OPTIMIZE | Hollow core; orphan `form_field_analyzer.py` |
| free-tool-strategy | KEEP | — |
| launch-strategy | OPTIMIZE | 74-line shell; orphan `launch_readiness_scorer.py` |
| marketing-context | OPTIMIZE | Writes `.agents/marketing-context.md` while siblings read 2 other paths |
| marketing-demand-acquisition | OPTIMIZE | `updated: 2025-01`, "q1-2025" examples; persona-narrow (Series A+ EU/US) |
| marketing-ideas | KEEP | — |
| marketing-ops | OPTIMIZE | Router missing 11 of 47 skills (incl. aeo, webinar, ASO, x-twitter) |
| marketing-psychology | KEEP | — |
| marketing-skills | CUT-OR-MERGE | Index-as-skill: stale counts (42/7/27 vs actual 47/8/58+), all example paths broken |
| marketing-strategy-pmm | KEEP | — |
| onboarding-cro | OPTIMIZE | Orphan `activation_funnel_analyzer.py` |
| page-cro | OPTIMIZE | Orphan `conversion_audit.py` |
| paid-ads | OPTIMIZE | Phantom tools/REGISTRY.md; 2 orphan scripts; "2024Q1/Mar24" naming examples |
| paywall-upgrade-cro | KEEP | — |
| popup-cro | OPTIMIZE | Hollow core ("→ see references"); zero tooling |
| pricing-strategy | KEEP | — |
| programmatic-seo | OPTIMIZE | Orphan `url_pattern_generator.py` |
| prompt-engineer-toolkit | REWRITE | All 3 references are stubs (328 B / 675 B / 1.5 KB); body ≠ marketing description |
| referral-program | KEEP | — |
| schema-markup | KEEP | — |
| seo-audit | OPTIMIZE | Hollow core; both scripts orphaned |
| signup-flow-cro | OPTIMIZE | Orphan `funnel_drop_analyzer.py` |
| site-architecture | KEEP | — |
| social-content | KEEP | — |
| social-media-analyzer | KEEP | — |
| social-media-manager | OPTIMIZE | Orphan `social_calendar_generator.py` |
| webinar-marketing | OPTIMIZE | `webinar_funnel_scorer.py` has no argparse — `--help` crashes (only D1 fail in domain) |
| x-twitter-growth | KEEP | — |
| youtube-full | KEEP | — |
| video-content-strategist | KEEP | — |
| landing (marketing/) | KEEP | — |

Verdict counts: **KEEP 20 · OPTIMIZE 24 · REWRITE 1 · CUT-OR-MERGE 4**

## Domain-level findings

1. **24 orphan scripts (systemic A3 failure).** Scripts exist and pass `--help` (583/593 repo sweep) but are never named in their own SKILL.md, so a model loading the skill never knows they exist: ab-test-setup, cold-email, competitor-alternatives, content-production (×3), content-strategy, copy-editing (×2), copywriting, email-sequence, form-cro, launch-strategy, marketing-context, marketing-ops, onboarding-cro, page-cro, paid-ads (×2), programmatic-seo, seo-audit (×2), signup-flow-cro, social-media-manager. One repo-wide wiring PR fixes ~half the OPTIMIZE verdicts.
2. **Context-file path schism (foundational pattern silently no-ops).** 19 skills check `.claude/product-marketing-context.md`, 16 check `marketing-context.md`, and the `marketing-context` skill that *creates* the file writes `.agents/marketing-context.md`. Whatever path the user's file is at, half the domain won't find it. Pick one canonical path.
3. **Count drift in 4 places.** marketing-skills SKILL.md: "42 skills / 7 pods / 27 tools"; marketplace.json: "44 skills / 7 pods"; plugin.json + CLAUDE.md: "45 skills / 8 pods"; actual: 47 skill dirs (incl. 1 deprecated redirect and 1 index). All example invocation paths in marketing-skills/SKILL.md omit the `skills/` segment and are broken.
4. **Duplicate AI-search lane.** `aeo` (v2.7.3 port, 3 working scripts, calibrated industry thresholds) and `ai-seo` (older, prose-only) both own "get cited by ChatGPT/Perplexity." The router routes AI-search queries to `ai-seo` and doesn't know `aeo` exists. Merge ai-seo's bot-access/robots.txt + content-pattern material into aeo references.
5. **Router drift.** marketing-ops claims to be the central router but its matrix omits 11 skills: aeo, app-store-optimization, brand-guidelines, marketing-demand-acquisition, marketing-strategy-pmm, prompt-engineer-toolkit, social-media-analyzer, webinar-marketing, x-twitter-growth, youtube-full (+ the marketing-skills index).
6. **Plugin hygiene.** marketing-skill/ root ships 5 .zip archives (~120 KB) and 4 internal planning docs (MARKETING-AUDIT-REPORT.md, -EXECUTION-PLAN.md, -EXPANSION-PLAN.md, marketing_skills_roadmap.md — 1,194 lines) inside the public plugin folder.
7. **Phantom references.** email-sequence and paid-ads link `../../tools/REGISTRY.md` and 5 `../../tools/integrations/*.md` guides; no `tools/` directory exists anywhere in marketing-skill/.
8. **Freshness is better than feared, with 3 specific stales:** Meta's 20%-image-text rule (retired 2021) in ad-creative SKILL + reference; GA4 "Conversions" (renamed "Key events" March 2024) in analytics-tracking; 2024/2025 dating in paid-ads naming examples and marketing-demand-acquisition metadata. x-twitter-growth explicitly labels its algorithm table "2025-2026" — the right pattern.
9. **New-gen model lens: the domain splits cleanly.** Skills that pair calibrated thresholds with deterministic scorers (aeo, campaign-analytics, ASO, churn-prevention, webinar funnel math, landing's validator gate) earn their context. ~8 skills are persona-prompt shells ("Core Principles → see references") whose body adds nothing a frontier model lacks — the value is locked in references the SKILL.md barely indexes.
10. **video-content-strategist plugin not registered.** It has `.claude-plugin/plugin.json` but no entry in root marketplace.json (E3).

## Per-skill findings

### ab-test-setup — OPTIMIZE
Issues: (1) `scripts/sample_size_calculator.py` orphaned — SKILL.md points users to external web calculators instead of its own tool; (2) sample-size quick table good but unverified against the script's output.
Verify: `python3 scripts/sample_size_calculator.py --help` exits 0; SKILL.md contains the literal string `sample_size_calculator.py` with an invocation; script output for baseline 5%/MDE 20% matches the table's ~7k/variant.

### ad-creative — OPTIMIZE
Issues: (1) "Image text <20%" Meta rule stated in SKILL.md spec table and references/platform-specs.md as causing "reduced distribution" — Meta retired the enforcement in 2021; (2) `ad_copy_validator.py` wired but invocation lacks args/format.
Verify: `grep -c "20%" references/platform-specs.md` returns 0 (or the claim is rewritten as historical); `python3 scripts/ad_copy_validator.py --help` exits 0; SKILL.md shows an exact CLI line with input format.

### ai-seo — CUT-OR-MERGE
Issues: (1) duplicates `aeo`'s mission with zero tooling (0 scripts vs aeo's 3); (2) router sends AI-search traffic here, starving aeo; (3) unique value (robots.txt bot matrix, 6 content patterns, GSC AI Overviews monitoring) belongs in aeo/references.
Verify: after merge, `marketing-ops/SKILL.md` routes "AI search/AEO/GEO" triggers to `aeo`; aeo references contain the bot-access table; `ai-seo/` directory removed or reduced to a redirect stub ≤ 30 lines.

### analytics-tracking — OPTIMIZE
Issues: (1) "GA4 → Admin → Conversions" + "Max 30 conversion events" uses pre-2024 terminology (now Key events); (2) `tracking_plan_generator.py` only mentioned in passing in the artifacts table — no CLI invocation or output contract.
Verify: SKILL.md says "Key events"; SKILL.md contains `python3 scripts/tracking_plan_generator.py` with args; `python3 scripts/tracking_plan_generator.py --json` emits parseable JSON.

### brand-guidelines — CUT-OR-MERGE
Issues: (1) 93 lines of generic audit checklist any frontier model reproduces unprompted (A5 fail); (2) "Anthropic Brand Identity" section hardcodes one company's identity into a generic skill; (3) no scripts, 1 reference; (4) overlaps marketing-context §10-11 (Brand Voice + Style Guide).
Verify: brand dimensions folded into marketing-context template (§10/§11 expanded); references/brand-identity-and-framework.md content preserved or moved; routing matrix no longer lists it OR skill rewritten with a deterministic brand-audit scorer.

### competitor-alternatives — OPTIMIZE
Issues: (1) `comparison_matrix_builder.py` orphaned; (2) otherwise strong 4-format framework.
Verify: SKILL.md names `comparison_matrix_builder.py` with exact CLI + consuming step; script `--help` exits 0.

### content-creator — CUT-OR-MERGE
Issues: (1) deprecated redirect skill still ships 4 references + 1 asset that the redirect never uses (A7); (2) `cs-content-creator` agent and `personas/content-strategist` still target it; (3) `content-creator.zip` lingers in plugin root; (4) routing duplicate of one row in marketing-ops.
Verify: references/ + assets/ removed (≤ 1 file redirect remains) or skill deleted with router rows updated; `grep -r "content-creator" agents/` returns no skill-target hits; zip deleted.

### content-humanizer — OPTIMIZE
Issues: (1) 2/6 on repo's own checklist (261 lines, time-sensitive content flags); (2) the AI-tell vocabulary ("delve", "landscape", em-dash) is itself a 2023-24 snapshot — new-gen models have different tells, list needs dating + refresh cadence; (3) "HubSpot published... in 2023" dated example; (4) `humanizer_scorer.py` wired only in artifacts table, no CLI contract.
Verify: `skill_review_checklist_runner.py content-humanizer` ≥ 4/6; SKILL.md shows `python3 scripts/humanizer_scorer.py <file>` with score interpretation thresholds; references/ai-tells-checklist.md carries a "last validated" date.

### content-production — OPTIMIZE
Issues: (1) `brand_voice_analyzer.py`, `content_quality_gates.py`, `seo_optimizer.py` all orphaned — only `content_scorer.py` is named; (2) marketing-skills index advertises these very scripts while the owning skill doesn't.
Verify: all 4 scripts named in SKILL.md with exact CLI; `python3 scripts/content_scorer.py --json` emits JSON with a 0-100 score; Mode 3 consumes brand_voice_analyzer + content_quality_gates outputs by name.

### content-strategy — OPTIMIZE
Issues: (1) core knowledge deferred ("Searchable vs Shareable → see references") leaving a 127-line shell; (2) `topic_cluster_mapper.py` orphaned.
Verify: SKILL.md names `topic_cluster_mapper.py` with invocation; the searchable-vs-shareable decision rule (not just pointer) appears inline; script `--help` exits 0.

### copy-editing — OPTIMIZE
Issues: (1) both scripts (`ai_content_detector.py`, `readability_scorer.py`) orphaned; (2) Seven Sweeps framework is genuinely good — wiring is the only gap.
Verify: each sweep that has a matching script names it (Sweep on AI patterns → ai_content_detector; clarity → readability_scorer); both `--help` exit 0; outputs consumed in the sweep workflow text.

### copywriting — OPTIMIZE
Issues: (1) `headline_scorer.py` orphaned; (2) headline formula section never points at its own scorer.
Verify: SKILL.md "Above the Fold" section invokes `python3 scripts/headline_scorer.py "<headline>"`; script exits 0 with a numeric score.

### email-sequence — OPTIMIZE
Issues: (1) phantom `../../tools/REGISTRY.md` + 5 `tools/integrations/*.md` links — directory doesn't exist; (2) `sequence_analyzer.py` orphaned; (3) core principles deferred to one reference, 135-line shell.
Verify: `grep -c "tools/REGISTRY" SKILL.md` returns 0; `sequence_analyzer.py` named with CLI; all relative links in SKILL.md resolve (`find` check).

### form-cro — OPTIMIZE
Issues: (1) `form_field_analyzer.py` orphaned; (2) hollow core ("Core Principles → see references").
Verify: script named with CLI and consumed in the audit output format; field-count/friction thresholds inline in SKILL.md (not only in playbook).

### launch-strategy — OPTIMIZE
Issues: (1) 74 lines — everything substantive deferred to one reference; (2) `launch_readiness_scorer.py` orphaned; (3) thinnest non-deprecated skill in domain.
Verify: SKILL.md ≥ inline ORB definition + phase model summary; `launch_readiness_scorer.py` named with CLI; `--help` exits 0.

### marketing-context — OPTIMIZE
Issues: (1) writes `.agents/marketing-context.md` while 19 sibling skills read `.claude/product-marketing-context.md` and 16 read `marketing-context.md` — the foundation file is invisible to half its consumers; (2) `context_validator.py` orphaned.
Verify: one canonical path declared and used by this skill's output instruction; `grep -rl "product-marketing-context" skills/*/SKILL.md` and `grep -rl "marketing-context.md"` agree with that path; `python3 scripts/context_validator.py --json` emits completeness score 0-100 and is named in SKILL.md.

### marketing-demand-acquisition — OPTIMIZE
Issues: (1) `metadata.updated: 2025-01`, "q1-2025-linkedin-enterprise" examples; (2) description hard-scopes to "Series A+ scaling internationally EU/US/Canada hybrid PLG/Sales-Led" — over-narrow trigger for a general demand-gen skill; (3) HubSpot-specific workflows presented as the default stack.
Verify: dates refreshed or genericized; description triggers cover demand-gen broadly with the persona as a default profile not a gate; campaign workflow validation step still names the UTM-in-CRM check.

### marketing-ops — OPTIMIZE
Issues: (1) routing matrix omits 11 skills (aeo, ASO, webinar-marketing, x-twitter-growth, social-media-analyzer, marketing-strategy-pmm, marketing-demand-acquisition, brand-guidelines, prompt-engineer-toolkit, youtube-full, video-content-strategist); (2) AI-search row routes to ai-seo only; (3) `campaign_tracker.py` orphaned.
Verify: `for d in skills/*/; do grep -q "$(basename $d)" marketing-ops/SKILL.md || echo MISS; done` prints nothing (minus deliberate exclusions); aeo present in SEO pod rows; `campaign_tracker.py` named with CLI.

### marketing-skills — CUT-OR-MERGE
Issues: (1) it's a README/index in SKILL.md clothing — no workflow, no trigger utility; (2) stale counts (42 skills/7 pods/27 tools vs actual 47/8/58+); (3) every example path broken (omits `skills/` segment: `marketing-skill/content-production/scripts/...`); (4) references 6 scripts that live in other skills (phantom `scripts/*.py` paths); (5) duplicates marketing-ops (router) and README.md (index).
Verify: file demoted to README.md (or deleted) and removed from skill counts; if kept as SKILL.md, all paths resolve (`grep -oE "marketing-skill[^ )]*" | xargs -I{} test -e {}`) and counts match `ls skills/ | wc -l`.

### onboarding-cro — OPTIMIZE
Issues: (1) `activation_funnel_analyzer.py` orphaned; (2) no references dir — all knowledge inline (acceptable) but no verification loop.
Verify: script named with CLI; `--help` exits 0; output (drop-off by step) consumed in the audit output format section.

### page-cro — OPTIMIZE
Issues: (1) `conversion_audit.py` orphaned; (2) framework is solid but ends with no machine-checkable gate (A4).
Verify: SKILL.md invokes `python3 scripts/conversion_audit.py` and the audit report format references its score; `--help` exits 0.

### paid-ads — OPTIMIZE
Issues: (1) phantom `../../tools/REGISTRY.md` reference; (2) `ad_health_scorer.py` + `roas_calculator.py` both orphaned; (3) naming-convention examples dated "2024Q1"/"Mar24"; (4) 5 refs exist but only 1 linked from SKILL.md.
Verify: zero phantom links; both scripts named with CLI; `python3 scripts/roas_calculator.py --help` exits 0; example campaign names use current-year placeholders or `{YYYY}` tokens.

### popup-cro — OPTIMIZE
Issues: (1) hollow core ("Core Principles → see references/popup-cro-playbook.md"); (2) zero tooling; (3) experiment lists are the kind of generic ideation a frontier model produces unaided (A5 risk).
Verify: trigger-timing and frequency-cap thresholds (the calibrated part of the playbook) surfaced inline; SKILL.md ≤ 250 lines with decision rules, not idea lists.

### programmatic-seo — OPTIMIZE
Issues: (1) `url_pattern_generator.py` orphaned; (2) otherwise strong (data-defensibility hierarchy, penalty avoidance).
Verify: script named with CLI in the page-generation workflow; `--help` exits 0.

### prompt-engineer-toolkit — REWRITE
Issues: (1) references are stubs: evaluation-rubric.md 328 B, technique-guide.md 675 B, prompt-templates.md 1.5 KB — no citations, no marketing templates despite the description promising "prompt templates for marketing use cases (ad copy, email campaigns, social media)" (A1/A7 fail); (2) body is generic LLM-feature governance, not marketing — arguably belongs in engineering/; (3) scripts (`prompt_tester.py`, `prompt_versioner.py`) are real and wired — keep them.
Verify: each reference ≥ 3 KB with ≥ 5 cited sources OR skill relocated to engineering/ with description rewritten to match the body; prompt-templates.md contains ≥ 5 concrete marketing prompt templates if it stays in marketing; both scripts still pass `--help`.

### seo-audit — OPTIMIZE
Issues: (1) both scripts (`seo_checker.py`, `seo_health_scorer.py`) orphaned; (2) audit framework wholly deferred ("→ See references/seo-audit-reference.md"); (3) 4 references are good (CWV thresholds, E-E-A-T) but SKILL.md gives the model no decision rules inline.
Verify: both scripts named with CLI and consumed in the report structure; CWV pass/fail thresholds (LCP/INP/CLS numbers) inline in SKILL.md; `--help` exits 0 on both.

### signup-flow-cro — OPTIMIZE
Issues: (1) `funnel_drop_analyzer.py` orphaned.
Verify: script named with CLI; `--help` exits 0; output consumed in audit format.

### social-media-manager — OPTIMIZE
Issues: (1) `social_calendar_generator.py` orphaned; (2) overlaps social-content's platform tables (duplicate cadence specs that can drift independently).
Verify: script named with CLI; cadence table either deduplicated with social-content or marked as the canonical copy; `--help` exits 0.

### webinar-marketing — OPTIMIZE
Issues: (1) **confirmed known issue:** `scripts/webinar_funnel_scorer.py` has no argparse — `python3 ... --help` raises FileNotFoundError treating `--help` as a JSON filename (only D1 failure in marketing scope; it is the skill's only script, no affected siblings); (2) SKILL.md itself is among the best in the domain (backward funnel math, benchmark-tagged outputs) — fix is surgical.
Verify: `python3 scripts/webinar_funnel_scorer.py --help` exits 0 and prints usage; no-arg run still executes embedded sample and prints `WEBINAR FUNNEL SCORE: \d+/100` plus a JSON block; `echo '{}' | python3 scripts/webinar_funnel_scorer.py -` doesn't crash.

## KEEP-verdict verification criteria

- **aeo** — all 3 scripts pass `--help`; `aeo_audit.py --input <md> --output json` emits composite 0-100 + 4 dimension keys; industry table thresholds (healthcare/finance/legal ≥ 85) unchanged.
- **app-store-optimization** — all 8 scripts pass `--help`; `metadata_optimizer.py --platform ios --title "<31 chars>"` flags the over-limit title; char-limit table matches Apple 30/30/100 + Play 50/80.
- **campaign-analytics** — 3 scripts run on `assets/sample_campaign_data.json` with `--format json` exit 0; attribution output includes all 5 models; funnel analyzer names a bottleneck stage.
- **churn-prevention** — `churn_impact_calculator.py` runs no-arg with sample, exits 0; benchmark table retains save-rate ≥ 10-15% / recovery 25-35% calibration.
- **cold-email** — 3 references resolve; deliverability section still names SPF/DKIM/DMARC + warmup ramp; orphan `email_sequence_analyzer.py` gets wired (carryover from A3 sweep).
- **free-tool-strategy** — `tool_idea_scorer`-class script passes `--help` and is named in Mode 1; 6-factor evaluation framework present.
- **marketing-ideas** — references/ideas-by-category.md contains all 139 numbered ideas; SKILL.md stage-mapping numbers (#79, #81...) resolve to entries in the reference.
- **marketing-psychology** — references/mental-models-catalog.md contains ≥ 70 models; the 6-category count table matches the catalog's actual counts.
- **marketing-strategy-pmm** — 4 references resolve; April Dunford positioning workflow + ICP validation checklist intact; no scripts claimed (none promised).
- **paywall-upgrade-cro** — self-contained; description's distinct-from-pricing-page boundary preserved; router row intact.
- **pricing-strategy** — `pricing_modeler.py` passes `--help` and stays named in SKILL.md; three-axes model + Van Westendorp trigger words remain in description.
- **referral-program** — incentive-structure script passes `--help` and is named; LTV-ceiling logic for incentive sizing intact.
- **schema-markup** — `schema_validator.py` named in Mode 1 step 1 and passes `--help`; schema selection table covers FAQ/HowTo/Article/Product/Organization/Person.
- **site-architecture** — `sitemap_analyzer.py` named in Mode 1 and passes `--help`; subfolder-over-subdomain rule intact.
- **social-content** — references/platforms.md + post-templates.md resolve; cadence table consistent with social-media-manager's (post-dedup).
- **social-media-analyzer** — both scripts pass `--help`; engagement-rate formula (engagements/reach×100) and validation gates (ER < 100%) intact.
- **x-twitter-growth** — all 5 scripts pass `--help` and stay named; algorithm-signal table keeps an explicit date label ("2025-2026" or refreshed); cadence-by-account-size table intact.
- **youtube-full** — BYOK note + OSS fallback table intact; fix 3 cross-reference paths (`marketing-skill/skills/video-content-strategist` → actual location); endpoint table matches credit-cost table.
- **video-content-strategist** — niche/positioning framework + 90-day plan intact; plugin gets registered in marketplace.json (currently missing).
- **landing (marketing/)** — 3 scripts pass `--help`; `html_validator.py --file <out>.html` checks all 8 listed gates; GSAP CDN pins resolve; SKILL.md keeps gsap.set()-before-timeline FOUC rule.

## Agents

| Agent | Verdict | Notes |
|---|---|---|
| agents/marketing/cs-aeo.md | KEEP | B1-B3 pass; differentiated voice (refuses fake authority, AEO≠SEO routing); trigger phrasing present. |
| agents/marketing/cs-webinar-marketer.md | KEEP | Differentiated (refuses vanity metrics; fixes the broken stage); trigger phrasing present. |
| marketing/landing/agents/cs-landing.md | KEEP | Forcing-intake persona with concrete refusals; wired to skill + scripts. |
| agents/marketing/cs-content-creator.md | CUT-OR-MERGE | Targets the **deprecated** content-creator skill via a wrong path (`marketing-skill/content-creator`); no trigger phrasing (B1 fail); 3 paragraphs of swappable boilerplate (B2/B3 fail). Retarget to content-production or delete. |
| agents/marketing/cs-demand-gen-specialist.md | REWRITE | No trigger phrasing; wrong skill path (`marketing-skill/marketing-demand-acquisition`, missing `skills/`); body is the same boilerplate template as cs-content-creator — swappable (B2 fail). |
| agents/personas/content-strategist.md | OPTIMIZE | Skills list includes deprecated `content-creator`; otherwise differentiated persona frontmatter. |

## Commands

| Command | Verdict | Notes |
|---|---|---|
| commands/cs-aeo.md | KEEP | C1-C3 pass; orchestrates 3 scripts with modes; explicit when-NOT-to-run; distinct from /cs:seo-audit documented. |
| commands/cs-webinar.md | KEEP | C1-C3 pass; plan/rescue/evergreen modes; gates on funnel-math feasibility. |
| marketing/landing/commands/cs-landing.md | KEEP | C1-C3 pass; 4-question forcing intake + validator gate; routes away to landing-page-generator when conversion-optimized output needed. |
| commands/seo-auditor.md | KEEP | Repo-docs SEO utility (not marketing-skill plugin surface); 7-phase pipeline with report-only flag; does real orchestration. |

Gap: no `/cs:*` commands exist for the other 45 marketing skills — the domain relies on skill triggers alone. Acceptable, but the marketing-skills index promises slash-command-grade entry points it doesn't have.

## Plugin manifests

| Manifest | Verdict | Notes |
|---|---|---|
| marketing-skill/.claude-plugin/plugin.json | OPTIMIZE | Schema valid (`"skills": ["./skills"]` ✓). E2 fail: description says "45 skills across 8 pods" — actual 47 skill dirs (incl. deprecated redirect + index); marketplace.json entry says 44/7; marketing-skills SKILL.md says 42/7. Three counts, four places. |
| marketing-skill/skills/aeo/.claude-plugin/plugin.json | KEEP | Schema valid; `source` extension block documented; description matches contents. |
| marketing-skill/skills/youtube-full/.claude-plugin/plugin.json | KEEP | Schema valid; attribution block present; BYOK disclosed (ClawHub rule 3 satisfied — free tier + OSS fallbacks documented). |
| marketing-skill/video-content-strategist/.claude-plugin/plugin.json | OPTIMIZE | Schema valid but **not registered in root marketplace.json** (E3 fail) — plugin is undiscoverable. |
| marketing/landing/.claude-plugin/plugin.json | OPTIMIZE | Schema valid; `source` block present. E2 drift: marketplace.json description for `landing` describes the *other* landing skill ("4 design styles, brand palette validation" = product-team TSX generator language), not this GSAP/HTML one. |

Hygiene: marketing-skill/ plugin root ships 5 .zip archives and 4 internal planning markdown docs (1,194 lines) that don't belong in a distributed plugin.
