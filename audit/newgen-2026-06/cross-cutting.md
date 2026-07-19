# Cross-cutting audit: root agents, commands, standards, templates, marketplace, CI — new-gen model optimization
Audited: 2026-06-10

Scope: root `agents/` (32), root `commands/` (39), `standards/`, `templates/`, `orchestration/`, `custom-gpt/`, `assets/`, `.claude-plugin/marketplace.json`, `scripts/`, `.github/workflows/`, root README.md + CLAUDE.md. Rubric dimensions B/C/D/E.

---

## Counter-drift reconciliation table

Measured today (canonical tree, excluding `.codex/.gemini/.hermes/.vibe` sync copies and `docs/`):

| Metric | **Actual (measured)** | README.md | CLAUDE.md header (L9) | CLAUDE.md v2.10.3 block | CLAUDE.md footer (L515) | marketplace.json metadata | agents/CLAUDE.md |
|---|---|---|---|---|---|---|---|
| Skills (SKILL.md) | **346** (`audit_skills.py` count) / 347 (`find`) | 338 | 338 | 343 | 338 | 343 | "42 production skills" AND "177 existing skills" (same page) |
| Marketplace plugins | **66 entries** in marketplace.json; **77 plugin.json manifests** on disk (78 incl. `.codex-plugin` sync artifact) | — | 62 | 64 | 62 | **claims 64 — its own `plugins` array has 66** | — |
| Python tools (in-skill `scripts/*.py`) | **555** | 533 | 533 | 548 | — | 548 | — |
| Reference docs (`references/*.md`) | **700** | 676 | 676 | 691 | — | 691 | — |
| Agents (repo-wide / root) | **92 / 32** | 51+ | 51+ ("32 standalone") | — | — | 51+ | "16 Agents Currently Available" (table actually lists 19; folder has 32) |
| Slash commands (repo-wide / root) | **99 / 39** | 87+ | 87+ | 90+ | — | 90+ | — |
| Domains | **17** top-level skill domains | 16 | 16 | 17 | 16 | 17 | — |
| Version | — | — | — | v2.10.3 | **v2.9.0** | v2.10.3 | — |

Key drift facts:

1. **marketplace.json is internally inconsistent**: `metadata.description` and `description` both say "64 marketplace plugins" while the `plugins` array contains **66** entries (v2.10.x additions `universal-scraping-architect` and `youtube-full` were appended without bumping the counter).
2. **11 plugin.json manifests exist on disk but are NOT registered in marketplace.json** (invisible to marketplace installs):
   `compliance-os/`, `engineering-team/snowflake-development/`, `engineering/behuman/`, `engineering/claude-coach/`, `engineering/grill-with-docs/`, `engineering/llm-cost-optimizer/`, `engineering/prompt-governance/`, `finance/business-investment-advisor/`, `marketing-skill/video-content-strategist/`, `ra-qm-team/compliance-team-eu-ai-act/`, `ra-qm-team/compliance-team-iso42001/`. (Plus `.codex-plugin/plugin.json`, a sync artifact.) Notably, `compliance-os` is *named as a domain* in the marketplace description yet has no marketplace entry.
3. **CLAUDE.md disagrees with itself in three places** (header 338/62/16, v2.10.3 block 343/64/17, footer v2.9.0/338/62/16). README still carries the pre-v2.10 numbers everywhere, including the shields badge (`Skills-338`).
4. Even the freshest claimed numbers (343/64/548/691) trail reality (346/66-77/555/700) — the counters were last trued up at v2.10.3 and have drifted again.

---

## Root agents

32 agents (25 `cs-*` + 7 personas). **17 of 32 (53%) lack trigger phrasing** ("Use when…" / "Spawn when…" / "Invoke via…") in `description` — B1 fail. All but 2 agents carry the identical generic `tools: [Read, Write, Bash, Grep, Glob]` list (B1 "minimal tools" not practiced). The personas use a non-standard frontmatter schema (`name` with spaces, `color`, `emoji`, `vibe` fields — not Claude Code agent fields).

| Agent | Verdict | Issue |
|---|---|---|
| engineering/cs-backend-engineer | KEEP | Exemplary: trigger + invocation path + `context: fork` + differentiated forcing questions |
| engineering/cs-frontend-engineer | KEEP | Same pattern; good |
| engineering/cs-fullstack-engineer | KEEP | Same pattern; good |
| engineering/cs-karpathy-reviewer | KEEP | Good trigger; near-duplicate of `engineering/karpathy-coder/agents/karpathy-reviewer.md` (differs, but two sources of truth) |
| engineering/cs-wiki-ingestor / -librarian / -linter (3) | KEEP | Good triggers; near-duplicates of `engineering/llm-wiki/agents/wiki-*.md` — pick one canonical home |
| engineering/cs-senior-engineer | OPTIMIZE | Trigger OK but scope ("architecture, code review, DevOps, API design") overlaps cs-engineering-lead + the 3 role engineers — B2 differentiation weak |
| engineering-team/cs-engineering-lead | OPTIMIZE | Trigger OK; differentiate from cs-senior-engineer or merge |
| engineering-team/cs-workspace-admin | KEEP | Specific, trigger present |
| marketing/cs-aeo | KEEP | Model trigger + voice + refusal rule |
| marketing/cs-webinar-marketer | KEEP | Model trigger + voice |
| marketing/cs-content-creator | OPTIMIZE | No trigger phrasing; description is a topic list |
| marketing/cs-demand-gen-specialist | OPTIMIZE | No trigger phrasing |
| c-level/cs-ceo-advisor | OPTIMIZE | No trigger; 360-line body is content-rich but description is a noun phrase |
| c-level/cs-cto-advisor | OPTIMIZE | No trigger |
| product/cs-product-manager | OPTIMIZE | No trigger; claims 8 skills incl. those owned by sibling agents (strategist, ux-researcher) — B2 overlap |
| product/cs-product-strategist | OPTIMIZE | No trigger; skill overlap with cs-product-manager |
| product/cs-agile-product-owner | OPTIMIZE | No trigger |
| product/cs-ux-researcher | OPTIMIZE | No trigger |
| product/cs-product-analyst | REWRITE | No trigger AND 31-line near-placeholder body (B3) — thinnest agent in the folder |
| project-management/cs-project-manager | OPTIMIZE | No trigger; 515-line body |
| business-growth/cs-growth-strategist | KEEP | "Spawn when…" present |
| finance/cs-financial-analyst | KEEP | "Spawn when…" present |
| ra-qm-team/cs-quality-regulatory | KEEP | "Spawn when…" present |
| personas/solo-founder | OPTIMIZE | No trigger; no `skills:` mapping; non-standard frontmatter |
| personas/startup-cto | OPTIMIZE | No trigger; overlaps cs-cto-advisor (B2 pair) |
| personas/growth-marketer | OPTIMIZE | No trigger; no `skills:`; overlaps cs-demand-gen-specialist |
| personas/content-strategist | OPTIMIZE | No trigger; overlaps cs-content-creator |
| personas/product-manager | OPTIMIZE | No trigger; overlaps cs-product-manager |
| personas/finance-lead | OPTIMIZE | No trigger; skills list (`ceo-advisor`, `cost-estimator`) is bare-name shorthand that doesn't resolve to paths; overlaps cs-financial-analyst |
| personas/devops-engineer | OPTIMIZE | No trigger; references `ms365-tenant-manager` / `aws-solution-architect` which exist only as **.zip archives** in engineering-team/ |

Cross-cutting agent issues:
- **`skills:` frontmatter shorthand is one directory level stale repo-wide**: e.g. `product-team/product-manager-toolkit` — actual path is `product-team/skills/product-manager-toolkit`. Every domain-prefixed `skills:` value resolves only via the `skills/` insertion.
- `templates/agent-template.md` is the root cause of the missing-trigger pattern: it mandates "One-line description… under 150 characters" with **no trigger-phrase requirement**, contradicting agents/CLAUDE.md's own current guidance and rubric B1.

---

## Root commands

39 commands. **34 of 39 never reference `$ARGUMENTS`** despite advertising `Usage: /cmd <args>` in descriptions (C2 weak; only focused-fix, tc, and the 4 cs-*-review/grill commands handle it). Only the 4 newest commands use `argument-hint`.

**Systemic C3 defect — phantom script paths: 28 of 39 commands contain ≥1 path that does not exist.** Root commands consistently reference `<domain>/<skill>/scripts/x.py`, but skills were reorganized into `<domain>/skills/<skill>/scripts/x.py` (and single-skill plugins into `<plugin>/skills/<name>/scripts/`). Every "Scripts" section pointing at e.g. `engineering/changelog-generator/...`, `finance/financial-analyst/...`, `product-team/product-manager-toolkit/...` is a dead path; the scripts exist one level deeper. A model following these commands hits file-not-found on first invocation.

| Command | Verdict | Issue |
|---|---|---|
| plugin-audit | KEEP | Real 8-phase orchestration; 4 stale paths to fix |
| seo-auditor | KEEP | Real pipeline; 8 stale paths |
| tc | KEEP | State machine + $ARGUMENTS dispatch; 6 stale paths |
| cs-aeo, cs-webinar | KEEP | Tool-wired workflows |
| cs-backend-review, cs-frontend-review, cs-fullstack-review, cs-engineer-grill | KEEP | argument-hint + agent fork + gates — the model pattern for the rest |
| a11y-audit | KEEP | Uses `{skill_path}` placeholder (resilient); fix Skill Reference path |
| code-to-prd | KEEP | `{skill_path}` placeholder pattern; 3 stale refs |
| chaos-experiment, slo-design, operator-audit, flag-cleanup | KEEP | Interactive wizards/gates; no stale paths detected |
| google-workspace | OPTIMIZE | Good content; 6 stale script paths |
| changelog, pipeline, okr, rice, persona, retro, user-story, saas-health, tech-debt, competitive-matrix, financial-health, project-health, sprint-health | OPTIMIZE | Script-wired (passes C3 in spirit) but **all script paths are phantoms** (missing `skills/` segment) |
| focused-fix | OPTIMIZE | Strong 5-phase protocol + $ARGUMENTS; "Related Skills" points to `engineering/focused-fix` (actual: `engineering/skills/focused-fix`) and to external `superpowers:systematic-debugging` (not in this repo). **Known-issue verified FALSE POSITIVE: the "TODO/FIXME" string is instructional content in the Phase 3 diagnostic checklist, not a real marker** — no actual TODO/FIXME/placeholder markers in commands/ or agents/ |
| karpathy-check | CUT-OR-MERGE (dedupe) | **Byte-identical** to `engineering/karpathy-coder/commands/karpathy-check.md`; also references bare `scripts/complexity_checker.py` which only resolves inside the plugin |
| wiki-ingest, wiki-init, wiki-lint, wiki-query, wiki-log (5) | CUT-OR-MERGE (dedupe) | **Byte-identical** to `engineering/llm-wiki/commands/wiki-*.md` — root copies are second sources of truth that will drift |
| prd | CUT-OR-MERGE | Bare-prompt restatement: 25 lines = output bullet list + skill pointer. A frontier model produces this without the command |
| sprint-plan | CUT-OR-MERGE | Same: 25 lines, no script, no gate, no $ARGUMENTS |
| tdd | CUT-OR-MERGE | References 4 scripts explicitly labeled "(library module)" — not CLI-invocable, so the command orchestrates nothing a bare prompt couldn't |

**Cut-or-merge candidates: 9** (6 byte-identical duplicates + prd + sprint-plan + tdd).

---

## standards/ + templates/ + orchestration/ + custom-gpt/ + assets/

**standards/** — NOT orphaned: referenced by `.github/workflows/skill-quality-review.yml`, `skill-security-audit.yml`, `commands/plugin-audit.md`, root CLAUDE.md, `.claude/commands/update-docs.md`. No stale model names or dead dates. Caveat: `communication-standards.md` is only **38 lines** (vs 319–545 for siblings) — underweight for a "standards" file. The other 4 are substantive.

**templates/** — Stale meta-documentation:
- `templates/CLAUDE.md` says `agent-template.md` exists "**(when created)**" — it has existed for a long time; also promises `command-template.md` and workflow templates "(when created)" that were **never created** (phantom inventory).
- `templates/agent-template.md` (318 lines) actively teaches the B1 anti-pattern: "description… under 150 characters", no trigger-phrase requirement, generic 5-tool list. This template is why 17/32 root agents fail B1. Verdict: REWRITE the frontmatter section.

**orchestration/ORCHESTRATION.md** (262 lines) — Referenced from README + agents/CLAUDE.md + mkdocs (not orphaned). Concept is sound, but its load examples are stale: `engineering/aws-solution-architect/SKILL.md` and `engineering/mcp-server-builder/SKILL.md` — `aws-solution-architect` exists only as `engineering-team/aws-solution-architect.zip` (an archive!) and mcp-server-builder lives at `engineering/skills/mcp-server-builder/`. Verdict: OPTIMIZE (fix example paths).

**custom-gpt/README.md** (128 lines) — Referenced from README + mkdocs; 6 ChatGPT GPT links. Not orphaned; external links unverifiable from here. Verdict: KEEP.

**assets/icon.png** — **Orphan.** Zero references from marketplace.json, any plugin.json, README, or mkdocs (grep across .json/.md/.yml). Either wire it into marketplace metadata or remove.

**engineering-team/*.zip** (12 archives: senior-fullstack.zip, aws-solution-architect.zip, etc.) — observed while tracing paths; zipped skill archives sitting in the published tree, referenced by personas/orchestration as if unzipped. Flagging for the engineering-team domain auditor.

---

## scripts/ (build & sync)

| Script | --help | Finding |
|---|---|---|
| check_plugin_json.py | PASS (argparse) | `--all` validates all 77 manifests, 0 WARN/FAIL today. Solid (D1–D3) |
| sync-codex-skills.py | PASS | Knows all 17 domains incl. markdown-html |
| sync-gemini-skills.py | PASS | **Missing `markdown-html` domain** — 5 skills never sync to Gemini |
| sync-hermes-skills.py | PASS | **Missing `markdown-html`** — never syncs to Hermes |
| sync-vibe-skills.py | PASS | **Missing `markdown-html`** — never syncs to Vibe |
| sync_skill_bundles.py | PASS (argparse) | OK |
| extract_release_notes.py | PASS (argparse) | OK |
| **audit_skills.py** | **FAIL** | No argparse; `--help` is ignored and the **full 346-skill audit runs** (~30s). D1 violation in the repo's own meta-audit tool |
| **generate-docs.py** | **FAIL — destructive** | No argparse; `--help` silently **regenerates the entire docs/ tree** (verified: modified 5 + created 4 files during this audit; reverted). A help invocation must never write. Also lacks markdown-html coverage (no docs pages exist for the 5 markdown-html skills) |
| convert.sh / install.sh / openclaw-install.sh / review-new-skills.sh / *-install.sh | header-documented | No hardcoded `/Users/...` or maintainer-specific paths found anywhere in scripts/ (good). `convert.sh` also has no markdown-html awareness |

---

## CI workflows

12 workflows. What actually gates PRs:

- **ci-quality-gate.yml** — runs on every PR. **CONFIRMED: `python scripts/check_plugin_json.py --all` runs as a blocking step**, exactly as CLAUDE.md claims (labeled "guards #539 + #686"). yamllint + workflow schema check (schema check is `|| true` — advisory). **Gap: the blocking `compileall` step covers only 9 pre-v2.7 folders** (`marketing-skill product-team c-level-advisor engineering-team ra-qm-team engineering business-growth finance project-management scripts`) — **8 newer domains are never syntax-checked in CI**: `productivity/`, `marketing/`, `research/`, `research-ops/`, `business-operations/`, `commercial/`, `markdown-html/`, `compliance-os/`. Safety scan and link check are `|| true` (advisory).
- **skill-quality-review.yml / skill-security-audit.yml** — PR-triggered, reference standards/; Tessl review depends on external secrets.
- **enforce-pr-target.yml** — pull_request_target gate (branch strategy enforcement). Runs.
- **claude.yml / claude-code-review.yml / pr-issue-auto-close.yml / virustotal-scan.yml** — event-driven; not quality gates per se.
- **release.yml** (push→main), **static.yml** (Pages), **sync-codex-skills.yml** (push), **smart-sync.yml** (issues; excluded from schema validation due to `projects_v2_item`).

Net: the only **blocking** code-quality gates are compileall (with the 8-domain hole) and check_plugin_json. Everything else is advisory or external-dependent. Note: `tests/` pytest suite is maintainer-local (gitignored) — no test gate runs in CI by design, but CLAUDE.md's claim "run locally; not in CI" is accurate.

---

## README/CLAUDE.md accuracy

- README header, badge, and FAQ all say **338 skills / 533 tools / 676 references / 51+ agents / 87+ commands / 16 domains** — all five numbers are stale (actual: 346 / 555 / 700 / 92 / 99 / 17). The shields badge hardcodes `Skills-338`.
- README relative links: all resolve in-tree (CHANGELOG.md, CONTRIBUTING.md, personas, orchestration). **No 404-for-cloners links found beyond the documented gitignored-folder exception.** CLAUDE.md's `documentation/...` links are covered by the Maintainer-Local Folders note (intentional).
- CLAUDE.md is **self-contradictory**: header (L9) 338/62/16, v2.10.3 block 343/64/17, footer "Last Updated May 27, 2026 / Version v2.9.0 / 338 skills…16 domains / 62 plugins". Three different repo states in one file.
- agents/CLAUDE.md is the worst offender: "42 production skills" and "177 existing skills" in adjacent paragraphs, "16 Agents Currently Available" heading over a 19-row table, while the folder holds 32 agent files.
- README claim "All 533 Python CLI tools… verified to run with `--help`" — falsified twice in scripts/ alone (audit_skills.py, generate-docs.py), and the count is 555.

---

## Top recommendations

1. **Single-source the counters.** Add a `scripts/update_counters.py` (or extend audit_skills.py) that computes skills/plugins/tools/references/agents/commands from the tree and rewrites README badge, CLAUDE.md header+footer, and marketplace.json metadata in one pass; wire it as a blocking CI check ("counters match tree"). Today 7 locations disagree, including marketplace.json with itself (says 64, contains 66).
2. **Fix the phantom-path epidemic in root commands (28/39 affected).** Mechanical fix: insert the missing `skills/` segment (`<domain>/skills/<skill>/scripts/…`); add a CI grep that fails on any in-repo path reference in commands/ + agents/ that doesn't exist. Same fix applies to agents' `skills:` shorthand, orchestration/ORCHESTRATION.md examples, and templates.
3. **Reconcile marketplace.json with disk**: register or explicitly de-list the 11 unregistered plugin.json manifests (compliance-os is even advertised in the marketplace description but uninstallable from it); bump the self-described plugin count to the real entry count.
4. **De-duplicate the 6 byte-identical root commands** (karpathy-check + 5 wiki-*) — keep the plugin copies as canonical; cut `prd`, `sprint-plan`, `tdd` or merge them into their skills (bare-prompt-replaceable).
5. **Repair the meta-tooling**: give audit_skills.py and generate-docs.py argparse (`--help` must be side-effect-free — generate-docs.py currently rewrites docs/ on `--help`); add `markdown-html` to sync-hermes/vibe/gemini + convert.sh + generate-docs; extend ci-quality-gate compileall to the 8 uncovered domains.
6. **Fix the template that breeds B1 failures**: add a mandatory trigger-phrase line ("Use when… / Spawn when…") to templates/agent-template.md, then backfill the 17 root agents missing triggers (the 4 v2.8.1 engineering agents are the pattern to copy); update templates/CLAUDE.md's "(when created)" phantom inventory.

### Custom verification criteria (cross-cutting contract)

- `python3 scripts/check_plugin_json.py --all` exits 0 with 77+ manifests OK (keep green).
- `python3 -c "import json; m=json.load(open('.claude-plugin/marketplace.json')); n=len(m['plugins']); assert str(n) in m['metadata']['description'], (n, 'not in metadata')"` exits 0 after counter fix.
- For every `*.py` path matched by `` grep -rhoE '`[a-z-]+(/[a-zA-Z0-9_.-]+)+\.py`' commands/*.md ``: the file exists relative to repo root (0 misses; today: 28 commands fail).
- `python3 scripts/audit_skills.py --help` and `python3 scripts/generate-docs.py --help` exit 0 in <2s with **zero filesystem writes** (`git status --porcelain` empty after).
- `grep -RLE "Use when|Spawn when|Invoke via|Use PROACTIVELY" $(find agents -name 'cs-*.md')` returns empty after trigger backfill.
