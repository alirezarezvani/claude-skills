# PR audit detail — accepted external new-skill PRs (#967, #944, #926, #965, #942, #943)

**Audited:** 2026-08-21 — PR states below (CI, mergeability, commit counts) are a snapshot from that date; re-run each verification block before acting on a verdict.

Back to [00-MASTER.md](00-MASTER.md). Shared context: all six target `dev` ✓,
all purely additive (no conflicts), none has ever had a CI run, none touches
counters/marketplace/generated indexes — which is exactly what CONTRIBUTING
asks of external contributors. The public contributor contract
(CONTRIBUTING/CONVENTIONS) makes `scripts/` and `references/` optional; the
stricter internal CLAUDE.md bar (scripts + refs ≥5 sources + agent + command)
is applied below as improvement-stream items, not blockers — precedent exists
on dev for doc-only skills (`engineering/minimalist/`, `engineering/strict-api/`).

Security: `skill_security_auditor.py --strict` run on every PR — all clean
(0 CRITICAL / 0 HIGH) except one **verified false positive** on #944 (below).

Cross-cutting maintainer actions after merges: run `derive_counters.py` (all
six drift headline counters — Phase 5's rebased #940 is the true-up vehicle),
re-run the four sync scripts, and make the plugin/marketplace call for
#967/#965/#943 (#944 and #942 auto-join their domain plugins via
`"skills": ["./skills"]`).

---

## #967 — engineering/boost-asio-pro (async C++ networking) — **MERGE**

**What it ships.** Docs-only, 6 files, +882: SKILL.md (145) + 5 references
(coroutines 412, pre-cpp20 164, build 89, ssl 39, classic-boost 33). Core
thesis: establish Boost version × C++ standard **first** (coroutines ≥1.77 /
callbacks ≥1.74 / stackful spawn ≥1.80 / classic `io_service` 1.62–1.65), then
write in that style.

**Why it clears the bar.** The strongest doc-only submission in the stream —
specific, hard-won, verified-accurate knowledge: the strand-write-interleaving
trap ("Two `async_write`s in flight on the same strand still interleave bytes
on the wire") with the correct write-queue pattern in both styles; a
version-floor table that bites in practice ("Debian bookworm ships Boost 1.74 —
the `#include` fails outright"); `async_accept(make_strand(...))` return-type
subtlety; `operation_aborted`-as-keep-waiting timer semantics. Ends "It
compiles. Build it." — the repo's verification-first ethos. Zero overlap on dev
(no C++ networking skill anywhere). Frontmatter/trigger/desc all pass; the only
validator error is the waivable missing-`scripts/` (doc-only, justified in the
PR body). Security PASS.

**Plan.** Merge first in Phase 4, as-is. **Improvement stream:** (1) in-tree
attribution note for the author's linked MIT examples repo (PR body offers it);
(2) add a short Sources block per reference (official Boost/Asio docs + release
notes clear ≥5 easily); (3) maintainer plugin/marketplace decision + counter
true-up.

**Verification.**
```bash
git fetch origin pull/967/head:pr967 && git checkout pr967
python3 engineering/skills/skill-tester/scripts/skill_validator.py engineering/boost-asio-pro          # only the waivable no-scripts error
python3 engineering/skills/skill-security-auditor/scripts/skill_security_auditor.py engineering/boost-asio-pro --strict  # PASS 0C/0H
```

---

## #944 — finance/skills/stock-analysis — **MERGE-WITH-CHANGES**

**What it ships.** The deepest domain skill in the stream: 61 files, +24,758.
SKILL.md (304, 10-stage workflow + sector router + output contract), 21 core
references (159–629 lines each: data sourcing, earnings quality, forensic red
flags, valuation, epistemics, IPO/forensic modes, …), **26 sector playbooks**
(banks, NBFC, insurance, IT/SaaS, pharma, REITs, holdco, semiconductors, …),
**5 stdlib CLI engines** (`ratios.py` 2,690 ln, `score.py` 2,072,
`verify_data.py` 1,663, `lint_report.py` 1,121, `valuation.py` 893) +
1,608-line `benchmarks.json`, declarative `evals/` + worked `examples/`.
India-first (SEBI LODR, Ind-AS, CARO 2020) and global (EDGAR, IFRS/US-GAAP).

**Why it clears the bar.** Practitioner-grade throughout: "For banks, insurers,
REITs and miners the standard ratios are not merely less useful, they are
undefined or inverted"; holdco look-through P/E, double leverage ">1.3x a red
flag… invisible in consolidated D/E", India NAV discounts 40–75%; "You cannot
compute a quarterly CCC [in India]… State that limitation rather than
interpolating silently." "Never invent a number" is enforced structurally.
Scripts verified by execution: all 5 pass `--help`; `--example`/`--json` modes
exit 0; `lint_report.py` on the bundled example → OVERALL PASS; imports are
argparse/json/math/re/statistics/dataclasses only — zero
subprocess/eval/urllib/socket/file-writes, no `random`/`now()` → fully
deterministic. Distinct lane from `financial-analyst` (FP&A/DCF) and
`business-investment-advisor` (capex ROI). Auto-joins the finance plugin
(`"skills": ["./skills"]`). "Not investment advice" boundary present in both
description and body.

**Required changes (pre-merge).**
1. **Trim `description:` to ≤1024 chars** (currently 1,463 — the one hard
   checklist violation). Keep the trigger set (analyse/value a stock;
   OPM/ROCE/NIM/GNPA; forensic "is the profit real"; IPO/DRHP); cut the quoted
   example enumeration.
2. Add `## Anti-Patterns` and `## Cross-References` headings (content largely
   exists; cross-refs must name `finance/financial-analyst` and
   `finance/business-investment-advisor` with the lane boundary).
3. Disposition the auditor's one CRITICAL [PROMPT-EXFIL] at
   `references/sectors/holdco-assetmgr.md:58` — **verified false positive**
   (finance-vocabulary pattern match on the LTV/double-leverage table, nothing
   about credentials). Needs an auditor allowlist entry or maintainer waiver
   note so strict CI can pass (see master §5.5).

**Improvement stream (post-merge).** `source`-style provenance for the upstream
MIT repo (in `authoring-notes.json` per D1); split `ratios.py`/`score.py` per
the validator's karpathy-style size nit; decide whether `evals/`+`examples/`
dirs become a blessed pattern (they are genuinely good).

**Verification.**
```bash
git fetch origin pull/944/head:pr944 && git checkout pr944
cd finance/skills/stock-analysis/scripts
for s in ratios score valuation verify_data lint_report; do python3 $s.py --help; done
python3 ratios.py --example --json && python3 score.py --example --json && python3 valuation.py --example && python3 verify_data.py --example
python3 lint_report.py ../examples/standard-analysis-example.md      # OVERALL PASS
grep -rnE 'subprocess|eval\(|urllib|requests|socket' *.py            # no hits
# description-length gate (must be ≤1024 post-fix):
python3 - <<'EOF'
import re; t=open('finance/skills/stock-analysis/SKILL.md').read()
print(len(re.search(r'description:\s*(.*)',t.split('---')[1]).group(1)))
EOF
```

---

## #926 — marketing-skill/skills/business-name-fit — **MERGE-WITH-CHANGES**

**What it ships.** 3 files, +323: SKILL.md (120) + 2 references (naming-research
95, worked-examples 108). Correctly attributed port of
`Elham-Farajnejad/business-name-fit`. Cross-cultural business-name
suggestion/vetting: meaning, look-alike, pronunciation, spelling, WIPO
distinctiveness, sound symbolism, closing with a trademark/domain/native-speaker
verification handoff.

**Why it clears the bar.** Genuinely expert and epistemically honest: "a founder
can build a business on such a name and still never own it"; the cross-cultural
inversion ("a word plainly descriptive at home may be arbitrary and strong
abroad, and the reverse"); Scenario C rejects both the on-the-nose name and the
distinctiveness winner (Simorgh) for search pollution; "these associations come
mainly from English-language research and do not transfer automatically" is
repeated as an Anti-Pattern. No naming skill exists among 46 marketing skills;
`brand-guidelines` is correctly sequenced as post-name work. Auto-registers via
the marketing plugin's directory glob. Contributor iterated 4 commits including
a self-caught fix — engaged.

**Required changes (pre-merge).**
1. Description: "Use **whenever**" → "Use **when**" (one word; makes the repo
   validator's trigger regex pass).
2. Add 2 cited sources to reach the ≥5 floor (currently 3: WIPO 900.1E, Kohli &
   LaBahn 1997, Pogacar et al. 2015 — candidates: USPTO TMEP §1209,
   Usunier & Shaner 2002, Interbrand/Lexicon methodology).
3. Optional: swap `❌/⚠️` table tokens for `FAIL/CAUTION` text.

**Verification.**
```bash
git fetch origin pull/926/head:pr926 && git checkout pr926
python3 engineering/write-a-skill/skills/write-a-skill/scripts/skill_description_validator.py marketing-skill/skills/business-name-fit/SKILL.md
python3 engineering/write-a-skill/skills/write-a-skill/scripts/skill_review_checklist_runner.py marketing-skill/skills/business-name-fit/
python3 scripts/check_plugin_json.py --all
```

---

## #965 — research/dsh-deepread → deepread — **MERGE-WITH-CHANGES**

**What it ships.** 3 files, +272: SKILL.md (156) + 2 references (feynman 60,
knowledge-map 56). Evidence-first reading of **supplied** documents: 5 modes
(quick/deep/map/feynman/book), claim/reason/evidence/assumption/counterargument
decomposition, 4-level confidence labels, evidence ledger. Bilingual triggers
(`精读`, `费曼读书法`).

**Why it clears the bar.** Disciplined, not slop: "A topic label is not a
claim. Bad: 'This chapter is about habits.' Good: 'The author argues that
changing environmental cues is more reliable than relying on willpower'";
"Do not convert confidence into fake numerical precision"; book mode requires
"a final thesis map that could not be obtained by reading only the introduction
and conclusion"; prompt-injection defense in both body and Anti-Patterns. Real
lane: `research/deep-research` is discovery, `product-team/research-summarizer`
is briefs — the boundary is drawn explicitly with cross-refs.

**Required changes (pre-merge).**
1. **Rename `research/dsh-deepread` → `research/deepread`** (folder + `name:` +
   the two "DSH" H1 strings) — personal branding prefix has no meaning here;
   renaming after sync/marketplace registration is costly, so do it now.
2. Add ≥5 cited sources across the references (Adler & Van Doren, Toulmin,
   Karpicke/Roediger retrieval practice, Ahrens, Feynman-technique canon).
3. Path-qualify the `research-summarizer` cross-reference
   (`product-team/research-summarizer`).
4. Registration: add `.claude-plugin/plugin.json` (`"skills": ["./"]`) +
   marketplace entry to match every `research/` sibling, and a SIGNALS routing
   row in the `research/research` orchestrator (maintainer or follow-up).

**Verification.**
```bash
git fetch origin pull/965/head:pr965 && git checkout pr965
python3 engineering/skills/skill-tester/scripts/skill_validator.py research/deepread
python3 engineering/skills/skill-security-auditor/scripts/skill_security_auditor.py research/deepread --strict   # PASS 0C/0H
grep -rn 'research-summarizer' research/deepread/    # path-qualified
```

---

## #942 — engineering-team/skills/embedded-iot-mentor — **MERGE-WITH-CHANGES (light)**

**What it ships.** 1 file, +129 (SKILL.md). MCU/board/toolchain selection
(ESP32/Pico W/STM32/nRF52 decision table), firmware-reuse-first doctrine
(ESPHome/Tasmota/Meshtastic/WLED before writing code), data-destination table,
cost/time snapshots, breadboard-MVP-by-default phasing.

**Why it clears the bar.** Real practitioner judgment: "Writing firmware is a
cost the user pays, not a deliverable they receive"; the soil-NPK-probe
conductivity example; "'on my phone' is not 'from anywhere' — away from home
means a VPN, a tunnel, or a hosted service, never a port forward"; two-axis
experience probe; per-section output caps with drop conditions. Zero
embedded/firmware coverage on dev; correct domain (practitioner
engineering-team); **auto-joins the domain plugin** via `"skills": ["./skills"]`
— unlike its sibling #943, it is distributable on merge. Security PASS; no
vendor lock-in.

**Required change (pre-merge).** Clear the validator's 100-content-line floor
(currently 92): extract the MCU + toolchain + data-destination tables into
`references/hardware-selection.md` with ≥5 cited sources
(Espressif/ST/Nordic/RPi docs, ESPHome/PlatformIO) — kills two findings at once.

**Improvement stream.** One stdlib script (`bom_cost_estimator.py` or a power-
budget estimator) + `/cs:` command to reach the Path-B house shape.

**Verification.**
```bash
git fetch origin pull/942/head:pr942 && git checkout pr942
python3 engineering/skills/skill-tester/scripts/skill_validator.py engineering-team/skills/embedded-iot-mentor
python3 -c "import json; print(json.load(open('engineering-team/.claude-plugin/plugin.json'))['skills'])"   # ['./skills'] → auto-included
```

---

## #943 — productivity/swedish-mentor — **MERGE-WITH-CHANGES (borderline REWORK)**

**What it ships.** 1 file, +81 (SKILL.md). CEFR-leveled Swedish-learning
mentor: 2-question placement probe (don't take "I'm intermediate" at face
value), curated real channel/podcast recommendations with level tags, learning
path across the four skills. Prompt-injection guard and a "Never invent a URL"
rule present.

**Why it is borderline.** Thinnest of the batch: a well-groomed system prompt
more than a skill package — no references at all (the only one of the six), a
small resource list that will go stale with nothing to maintain it, generic
CEFR table, and a formulaic mandated opener ("Start every reply with a warm
agency line"). It also would land as the **only unregistered skill in
`productivity/`** — all 10 siblings are their own plugins — i.e. present in the
tree but undistributable. Validator: 61 content lines < 100 floor + no scripts.
Placement debatable (language learning ≠ productivity) but no better domain
exists and there is zero overlap.

**Required changes (pre-merge — all three, or defer the PR).**
1. Move the resource catalog + CEFR guide into
   `references/swedish-resources.md` with real URLs and ≥5 cited sources
   (Skolverket/SFI, Council of Europe CEFR, UR Play, Sveriges Radio) — fixes
   the length floor and the staleness problem simultaneously.
2. Add `.claude-plugin/plugin.json` (`"skills": ["./"]`) to match the domain,
   or the maintainer explicitly accepts tree-only status.
3. Soften the mandated opener into guidance.

**Verification.**
```bash
git fetch origin pull/943/head:pr943 && git checkout pr943
python3 engineering/skills/skill-tester/scripts/skill_validator.py productivity/swedish-mentor   # 0 errors post-fix
python3 scripts/check_plugin_json.py --all      # after plugin.json added
```
