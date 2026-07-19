# Domain audit: product-team/ — deep audit + agentic readiness

Audited: 2026-07-03 · 17 skills (13 under `skills/` incl. the router, 4 standalone
plugins) · 19 Python tools (all 19 pass `--help`, functional smoke tests on
sample_size_calculator and hig_checker reproduce correct math) · 5 agents + 1 persona ·
8 slash commands · 5 plugins (all `check_plugin_json.py`-clean).
Rubric: [RUBRIC.md](RUBRIC.md). Method: full SKILL.md reads, script smoke tests,
agent/command cross-referencing, counter verification.

## Summary

**Headline finding (now fixed in this PR): no orchestrator, no loop layer.** Before this
PR the domain had zero `context: fork`, zero forcing-question libraries, no `/cs:*`
router/grill commands, and its "router" (`product-skills`, 61 lines) shipped no tools —
the domain predated every v2.8+ convention. Three skills (spec-to-repo, code-to-prd,
research-summarizer) independently invented verification loops; nothing unified them.

**Agentic-readiness distribution (17 skills, post-PR):** HARNESS-READY **2**
(product-skills upgraded 1→12; spec-to-repo) · LOOP-CAPABLE **4** (product-manager-toolkit,
apple-hig-expert, code-to-prd, research-summarizer) · TOOL-ONLY **11** · PROSE-ONLY **0**.
Weakest dimensions domain-wide: **AR5 loop discipline** (only spec-to-repo has any
retry/stop language) and **AR1 goal intake** (14 of 17 accept any input silently).

## Per-skill table

Scores AR1·AR2·AR3·AR4·AR5·AR6 (post-PR where this PR changed the skill).

| Skill | AR1-6 | Tot | Class | Top improvement |
|---|---|---|---|---|
| skills/product-skills (orchestrator) | 2·2·2·2·2·2 | 12 | HR | (upgraded this PR: was a 61-line prose router, PROSE-ONLY) |
| skills/spec-to-repo | 1·2·2·2·1·1 | 9 | HR | Wire to an agent + command (currently orphaned from both) |
| skills/product-manager-toolkit | 1·1·2·1·0·1 | 6 | LC | Make the PRD checklist a blocking gate; add WSJF/CoD lane + eval-spec PRD section |
| code-to-prd (standalone) | 1·2·2·2·0·2 | 9 | LC (AR5 gate) | One sentence: max 2 analyze-fix cycles vs golden `expected_outputs/`, then escalate |
| research-summarizer (standalone) | 1·1·2·2·0·1 | 7 | LC | Cap the Verification Loop (2 re-extraction passes) → instant HR |
| apple-hig-expert (standalone) | 1·0·2·2·0·1 | 6 | LC | Numbered workflow; move `templates/` → `assets/`; add fix-recheck cap |
| skills/experiment-designer | 1·1·2·1·0·0 | 5 | TO | Make sample-size output a blocking gate on any test recommendation; 423 words is thin |
| skills/ux-researcher-designer | 0·1·2·1·0·1 | 5 | TO | (fake `--help` + unseeded RNG fixed this PR) Validation checklists → exit gates |
| skills/ui-design-system | 0·1·2·1·0·1 | 5 | TO | Add command; disambiguate vs markdown-html/design-system |
| skills/saas-scaffolder | 0·1·2·1·0·1 | 5 | TO | Make the 33-item checklist machine-checkable (reuse spec-to-repo's validator); dedupe references pair |
| agile-product-owner (standalone) | 0·1·2·1·0·1 | 5 | TO | (fake `--help` fixed this PR) INVEST checklist → gate |
| skills/product-analytics | 0·1·2·1·0·0 | 4 | TO | NSM validator + benchmark bands (see improvement-fields F7/F8); anti-patterns table exists, gate doesn't |
| skills/landing-page-generator | 0·1·2·1·0·0 | 4 | TO | Add `distinct_from` vs marketing/landing; render-check gate on emitted TSX |
| skills/product-strategist | 0·1·2·0·0·1 | 4 | TO | Alignment score exists but nothing requires it; outcome-vs-output OKR lint |
| skills/competitive-teardown | 0·1·2·0·0·0 | 3 | TO | Data-verification discipline (it synthesizes scraped claims with no source gate) |
| skills/product-discovery | 0·1·2·0·0·0 | 3 | TO | Wire to the new discovery loop (orchestrator now provides tracker + OST linter); 1 reference, no agent/command |
| skills/roadmap-communicator | 0·0·2·1·0·0 | 3 | TO | Merge-or-disambiguate vs `/changelog` + engineering/changelog-generator; 367 words |

## Domain-level findings

1. **Orchestration gap (fixed this PR).** `product-skills` is now a `context: fork`
   orchestrator with a deterministic 16-lane router (`product_goal_router.py`, exit
   0/2/3), a recurring discovery loop with two machine gates
   (`discovery_cadence_tracker.py`, `ost_linter.py`), a forcing-question library, and
   agent-harness integration. Agent `cs-product-orchestrator` + `/cs:product`,
   `/cs:grill-product`, `/cs:product-loop` commands added.
2. **References cite no sources: 39 of 43 reference files contain zero URLs/citations.**
   Only apple-hig-expert (3/3) and research-summarizer (1/2) meet the ≥5-sources bar. The
   3 new orchestrator references cite 7 sources each; the other 39 remain open work.
3. **Two tools faked their `--help` (fixed this PR).** `user_story_generator.py` and
   `persona_generator.py` exited 0 while ignoring the flag and running demos;
   persona_generator was additionally non-deterministic (unseeded `random.choice`). Both
   now use argparse; personas are seeded (default 42).
4. **Stale/contradictory counters + broken paths (open).** product-team/README.md holds 3
   mutually inconsistent counts and 9 broken Quick Start paths (missing `skills/`
   segment); `.codex/instructions.md` has 3 broken paths; CLAUDE.md says "13 skills" then
   lists 16, claims 17 tools (actual 19). The domain plugin.json description claims
   skills the bundle doesn't contain. CLAUDE.md counters updated this PR; README overhaul
   is follow-up F10.
5. **Unmanaged overlaps (open):** landing-page-generator ↔ `marketing/landing`;
   saas-scaffolder ↔ spec-to-repo; roadmap-communicator ↔ `/changelog` +
   `engineering/changelog-generator`; ui-design-system ↔ `markdown-html/design-system`.
   Only research-summarizer ships a "Distinct From" section. The orchestrator's routing
   table now provides partial disambiguation; per-skill `distinct_from` notes remain.
6. **8 of 13 bundled skills ship 0 assets** despite the repo's template-heavy principle;
   apple-hig-expert uses a nonstandard `templates/` dir.
7. **Agent/command coverage holes (open):** 6 skills map to no cs-* agent
   (product-discovery, roadmap-communicator, spec-to-repo, code-to-prd, apple-hig-expert,
   research-summarizer); 10 have no slash command. The orchestrator router reaches all 17
   lanes, which mitigates but does not close this.

## Verification criteria (executable)

- **product-skills (orchestrator):** `python3 product-team/skills/product-skills/scripts/product_goal_router.py --sample`
  exits 0 and routes to `product-discovery`; `--text "hello"` exits 3;
  `discovery_cadence_tracker.py --input assets/sample_discovery_log.json` exits 0 with
  `health_score` 62.0 and verdict `AT-RISK`; `ost_linter.py --input assets/sample_ost.json`
  exits 2 with exactly one O2 and one O4 violation; `--sample` variants all exit 0.
- **spec-to-repo:** `validate_project.py --strict` on a scaffolded repo exits 0 before
  the workflow may report done (existing contract, holds).
- **code-to-prd:** analyzer output diffs clean against `expected_outputs/` goldens
  (existing contract, holds).
- **persona_generator (fixed):** `--help` prints argparse usage (not a demo); two `json`
  runs produce byte-identical output.
- **user_story_generator (fixed):** `--help` prints argparse usage; `sprint 30` still
  plans a 30-point sprint (backward-compatible positional).
- **Manifest truth:** `harness_manifest_builder.py --domain product-team --no-timestamp`
  produces a diff-clean `product-team.json` with `product-skills` scoring all five
  `agentic_signals` true and 3 wired, sample-supporting tools.
