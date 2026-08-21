# PR audit detail — the benrfairless governance series (#936–#940)

**Audited:** 2026-08-21 — PR states below (CI, mergeability, commit counts) are a snapshot from that date; re-run each verification block before acting on a verdict.

Back to [00-MASTER.md](00-MASTER.md). All five: base `dev` ✓, conventional
commits ✓, zero reviews/comments, **zero CI runs** (fork PRs; workflows never
approved). **Stacked series on one base** — verified via
`git merge-base --is-ancestor`: 936 ⊂ 937 ⊂ 938 ⊂ 939 ⊂ 940. Merging a later PR
lands all earlier commits; out-of-order merging is impossible.

Context drift under the series: since base `2800f833`, dev merged #941
(book-to-skill) and #947 (memory-engineering) plus a codex-symlink sync — the
cause of #939/#940's `dirty` state and #940's stale counter payload.

---

## #936 — repair 14 unloadable YAML frontmatter blocks + gate G10 — **MERGE**

**What it does.** 16 files, +271/−12. Fixes 12 files whose unquoted
`description:` containing `": "` makes `yaml.safe_load` fail ("mapping values
are not allowed here") and 2 agents with no frontmatter at all
(`c-level-advisor/executive-mentor/agents/devils-advocate.md`,
`engineering/autoresearch-agent/agents/experiment-runner.md`). Adds
`scripts/check_frontmatter.py` (242 lines) as blocking gate G10 in
`ci-quality-gate.yml`.

**Evidence.** All 14 files re-tested at base (12 parse-fail, 2 missing) and at
head (14 parse, non-empty description). "Byte-identical text" verified
programmatically for all 11 pure-quoting fixes. Gate output reproduced exactly:
`Scanned 593 files; 0 errors, 17 warnings`, exit 0 — and re-run against
**dev + series** (601 files): still 0 errors. Test-merges clean into current dev.

**Risk noted, accepted.** `check_frontmatter.py` imports PyYAML (not stdlib);
mitigated by graceful exit-2 on ImportError and CI installing `yamllint`
(vendors PyYAML). The stdlib-only rule binds *skill* scripts; `scripts/` build
tooling already assumes CI deps.

**Plan.** Merge first, unchanged. **Improvement stream:** none needed.

**Verification.**
```bash
git fetch origin pull/936/head:pr936 && git checkout pr936
python3 scripts/check_frontmatter.py --all            # 593 files, 0 errors, 17 warnings, exit 0
python3 scripts/check_frontmatter.py --all --strict   # exit 1 (warnings escalate)
python3 scripts/check_paths.py --all && python3 scripts/check_plugin_json.py --all
# regression probe: break one quote in compliance-os/agents/cs-aims-iso42001.md → G10 exit 1 with line/col
```

---

## #937 — recalibrate skill-tester validator + advisory gate G7 — **MERGE**

**What it does.** Incremental: 5 files, +339/−47. Replaces the fictional
required-frontmatter list (`Name/Tier/Category/Dependencies/Author/Version`)
with the real schema (`name`, `description`); required-sections list becomes a
scored recommendation (≥2 of 12 headings); hand-maintained stdlib set replaced
by `sys.stdlib_module_names` + `__future__`. Rewrites the sample fixture to
carry real frontmatter. Adds `scripts/check_model_freshness.py` + allowlist as
**advisory** G7 (`continue-on-error: true`) flagging retired model IDs.

**Evidence.** Base validator on `c-level-advisor/skills/cfo-advisor` → 11 bogus
errors; PR validator → 0 errors, exactly the claimed 86.4→95.5 shift. G7 exits 1
on the pr937 tree (advisory, tolerated). One immaterial nit: PR body says "34
references"; script reports 33.

**Interaction.** `skill-quality-review.yml` calls this validator — expect score
shifts there (the point of the PR). #938 modifies the G7 script it creates.

**Plan.** Merge second, unchanged. **Improvement stream:** none.

**Verification.**
```bash
git checkout pr937
python3 engineering/skills/skill-tester/scripts/skill_validator.py c-level-advisor/skills/cfo-advisor  # 0 errors
python3 scripts/check_model_freshness.py --all; echo $?   # exit 1 advisory, 33 findings / 13 executable
python3 scripts/check_frontmatter.py --all && python3 scripts/smoke_scripts.py
```

---

## #938 — remove retired model IDs and stale pricing, flip G7 blocking — **MERGE**

**What it does.** Incremental: 19 files, +111/−94. Deletes dead 2024 cost
benchmarks from agent-designer's `agent_evaluator.py` (verified: no remaining
reader); makes senior-ml-engineer model-agnostic (price tables → tier-ratio
guidance; `calculate_cost()`/`count_tokens()` parameterized); pins
genuinely-needed IDs to current ones (`claude-opus-5`, `Claude Sonnet 5` in both
dual-publish CAIO copies); fixes a never-runnable CLI example in
`TEAM_STRUCTURE_GUIDE.md:344` (verified against the target script's real
argparse surface); flips G7 blocking and hardens it (`o-mini`-before-`o`
alternation-order bug, self-file exclusion, 3 reasoned allowlist entries).

**Evidence.** G7 on pr938: `2653 files; 0 retired-identifier references`,
exit 0 — and on **dev + pr938** (2,703 files, incl. post-base merges): still 0.
The blocking flip cannot redden CI. `check_dual_publish.py`: 12 pairs, 0
drifted. Clears the "senior-ml-engineer stale 2024 pricing" defect logged
STILL-OPEN in `audit/engineering-agentic-2026-07/`.

**Nit (optional).** `AnthropicProvider(model="claude-opus-5")` keeps a
hardcoded default the same diff removed for OpenAI; self-policing via G7.

**Plan.** Merge third, unchanged. **Improvement stream:** make the Anthropic
model a required param for symmetry (one-liner, any future PR).

**Verification.**
```bash
git checkout pr938
python3 scripts/check_model_freshness.py --all; echo $?   # exit 0, 0 findings
python3 engineering/skills/agent-designer/agent_evaluator.py --help
python3 scripts/check_dual_publish.py                     # 12 pairs, 0 drifted
python3 engineering-team/skills/senior-prompt-engineer/scripts/prompt_optimizer.py --help
```

---

## #939 — resolve `skills:` preloading + namespace collisions — **MERGE-WITH-CHANGES**

**What it does.** Incremental: ~558 files, +2,859/−353, 3 commits.
(a) Rewrites every agent `skills:` value to `plugin:skill` form
(e.g. `skills: c-level-skills:cfo-advisor`); drops two phantom entries; removes
`context: fork` from 11 agents (skill-only field); renames the colliding
`handoff` plugins → `handoff-engineering`/`handoff-productivity`.
(b) Renames colliding bare-verb skills: agenthub `init/run/status` →
`hub-init/hub-run/hub-status`; autoresearch `run/status` → `ar-run/ar-status`;
playwright-pro `init` → `pw-init`, skill `playwright-pro` → `pw`.
(c) Regenerates all four mirrors (`.codex`/`.gemini`/`.hermes`/`.vibe`, 468
files), pruning dead symlinks.

**Evidence.** Independently re-validated: full `plugin:skill` pair set built
from every plugin.json + SKILL.md; **109 agent skill references, 0
unresolvable**; duplicate-plugin-name check clean; G10 warnings 17→6 as claimed;
broken symlinks 3→0; `check_plugin_json.py`/`check_paths.py` exit 0 (directory
`"skills": ["./skills"]` form means the dir renames need no manifest edits).

**Blockers before merge:**
1. **Decision D2** (master §3): preloading ON (~2.5k tokens/agent-spawn) vs
   deleting the field. Author explicitly offers both. Recommend: keep preloading;
   record on the PR.
2. **Rebase + mirror resync.** One real conflict
   (`.hermes/skills/claude-skills/skills-index.json`) — resolve by re-running the
   four sync scripts, never by hand-merge.
3. **Cover the new dev agent.** `engineering/book-to-skill/agents/cs-book-to-skill.md`
   (landed after the PR) still carries the old path form — convert to
   `book-to-skill:book-to-skill` or the PR re-lands the bug it fixes.
4. **Confirm the comma-separated encoding.** 9 agents got multi-skill values
   flattened to one comma-joined string (e.g. `agents/personas/content-strategist.md`,
   8 refs on one line). If the sub-agent spec wants a YAML list, these resolve to
   nothing — re-encode as YAML lists (safe either way).
5. **Release note** for renamed invocations (`pw`, `hub-*`, `ar-*`, `handoff-*`).

**Improvement stream:** resolve the documented `/hub:` vs `/agenthub:` doc
mismatch (flagged in-PR, deferred).

**Verification (post-rebase).**
```bash
git checkout pr939
for d in .codex .gemini .vibe .hermes; do find $d -xtype l | wc -l; done   # all 0
python3 scripts/check_frontmatter.py --all        # 0 errors, 6 warnings
python3 scripts/check_paths.py --all && python3 scripts/check_plugin_json.py --all
python3 scripts/check_dual_publish.py && python3 scripts/derive_counters.py --check
# resolver check: rebuild plugin:skill pairs from all plugin.json + SKILL.md names,
# split every agent skills: value on commas, assert 0 unresolvable (script in audit tooling)
```

---

## #940 — gate the drifted counter sites, rewrite ClawHub §5 — **MERGE-WITH-CHANGES (merge LAST)**

**What it does.** Incremental: 5 files, +40/−18. Extends
`derive_counters.py::run_check` from 1 gated JSON site to 4 (adds marketplace
`description`, `mkdocs.yml site_description`, `.codex-plugin/plugin.json`
description); rewrites the three drifted texts with uniform gated phrasing;
bumps `.codex-plugin/plugin.json` from v2.2.0-era numbers (nine releases
behind — verified). Rewrites CLAUDE.md ClawHub §5: drops "No other extras" and
the `./`-prefix regression history, asserts unrecognized top-level fields are
tolerated.

**Evidence & defects.**
- The three drift sites and before-values are real; the gate design is right.
- **Fails its own gate on today's dev**: simulated merge + `--check` → 12
  mismatches ("claims skills=362, derived 364 … tools 644 vs 667 … plugins 88 vs
  90") across all three newly gated sites. Numbers must be regenerated at rebase.
- **Ungated claims inside gated sites**: `CLAIM_PATTERNS` has no
  `agents`/`commands` patterns, yet the PR writes "102 agents, 116 slash
  commands" (both already stale: 104/120) into sites the gate scans but cannot
  see.
- **Policy collision with #966 (decision D1)**: the §5 rewrite says extension
  fields "need no special dispensation" while `check_plugin_json.py` (untouched
  here; made *stricter* by #966) hard-errors on any extra key. An author
  following the new prose would be rejected by the repo's own blocking CI.
- A governance change ("No other extras" was a stated non-negotiable) is
  smuggled under `fix(docs)` — needs an explicit maintainer ACK either way.

**Required changes.**
1. Rebase onto post-Phase-4 dev; regenerate all descriptions from
   `derive_counters.py` output; `--check` must exit 0.
2. Add `agents` + `commands` patterns to `CLAIM_PATTERNS` (or drop those two
   figures from gated strings).
3. Rework §5 per D1 (recommended: keep #966's strict policy; state that
   `authoring-notes.json` is the sidecar home for provenance; keep one line
   recording the historical `./`-prefix regression — the deleted text was the
   only in-repo record of it).

**Why last:** its own gate freezes the counters it writes, so it must be the
final write of the release — the natural true-up vehicle after the new-skill
batch (D4).

**Verification (post-rebase).**
```bash
git checkout pr940
python3 scripts/derive_counters.py            # ground truth
python3 scripts/derive_counters.py --check    # MUST exit 0 across all gated sites
# perturbation probe: change "364"→"363" in mkdocs.yml site_description → --check FAILS; revert
python3 -c "import json; json.load(open('.codex-plugin/plugin.json')); json.load(open('.claude-plugin/marketplace.json'))"
```

---

## Overlap map (why the order is fixed)

| File | 936 | 937 | 938 | 939 | 940 |
|---|---|---|---|---|---|
| `ci-quality-gate.yml` | +G10 | +G7 advisory | G7→blocking | — | — |
| `check_model_freshness.py` + allowlist | — | creates | hardens | — | — |
| `check_frontmatter.py` | creates | — | — | (warning count depends on 939) | — |
| agent `.md` files | quotes descriptions | — | — | rewrites `skills:` in same files | — |
| mirrors (4 dirs) | — | — | — | regenerates (sole dev conflict) | inherited |
| counters/CLAUDE.md/marketplace/mkdocs/codex-plugin | — | — | — | — | sole owner |

If #939's preloading question stalls: #940's 5-file payload touches nothing
#939 owns except the inherited mirror commit — it can be rebased off the stack
directly onto #938 and re-submitted. Worth offering the author.
