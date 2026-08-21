# PR audit detail — maintainer draft PRs (#961, #948, #946)

**Audited:** 2026-08-21 — PR states below (CI, mergeability, commit counts) are a snapshot from that date; re-run each verification block before acting on a verdict.

Back to [00-MASTER.md](00-MASTER.md). All three are the maintainer's own drafts.
The question for each is not merge-worthiness but a **finish plan**: what
remains between the current head and a clean merge. Sequencing constraint:
#948 and #961 both append entry #91 at the tail of `marketplace.json` `plugins`
and both rewrite the same three counter surfaces — **merge #948 first**
(smaller, already CI-green), then rebase #961. Both are bound by decision D1
(#966's sidecar policy) — their manifests carry `source`/`attribution` blocks
that #966's stricter validator hard-fails.

---

## #948 — engineering/human-gate (draft) — **FINISH-PLAN → MERGE** (closest to ready)

**What it ships.** 19 files, +3,497/−13. Two deliverables:
(a) public audit record `audit/human-review-2026-08/AUDIT.md` — a
do-not-vendor / do-adopt-the-pattern verdict on `petergyang/human-review`
(~5,200 LOC Node 20 + npm deps fails stdlib-only; findings F1 unpinned
`npx -y` auto-execution, F2 unbounded re-poll, F3 ungated artifact routes);
(b) a conceptual derivation: `review_page_builder.py` (883 ln, Markdown/HTML →
single-file sanitized review page, zero network requests), `feedback_parser.py`
(482), `human_gate.py` (639, open/status/collect/close state machine, gates
G1–G7 — "G1 is never waivable"), SKILL.md, 3 references, 2 assets, agent,
command, plugin.json, marketplace entry.

**State of quality.** Battle-tested: 7 bot-review rounds in-thread, each finding
reproduced and fixed with regression fixtures (`<base>` void-element
body-swallow, `data-hg` attribute-forgery vector, `__CONTENT__` placeholder
collision, `## BLOKCER` typo silently downgrading severity — G7 was added for
that one). **CI fully green on head `5d03ed9`** (Lint/Tests/Docs/Security,
claude-review, VirusTotal). Attribution block is the best in the repo
("CONCEPTUAL derivation — no upstream source code is copied," each divergence
mapped to an audit finding, upstream's own 90/90 tests run during the audit).
Overlap fenced correctly: humanizers (behuman, content-humanizer) are voice;
this is approval — the missing human lane of agent-harness's machine-only loop.

**Finish plan.**
1. Merge/rebase onto current dev — resolve the four counter/changelog conflicts
   (base predates memory-engineering; dev now holds 364/90 for different
   content). Re-run `derive_counters.py` and take its numbers.
2. **D1 compliance**: move the plugin.json `source` + `attribution` blocks into
   `.claude-plugin/authoring-notes.json` (post-#966 the validator hard-fails
   them in the manifest). The derivation_note content moves verbatim.
3. Sequence: merge before #961; whichever lands second rebases the marketplace
   tail.
4. Re-run the three scripts' `--help`/`--sample` + checklist on the rebased
   head; undraft; merge.

**Verification.**
```bash
git fetch origin pull/948/head:pr948 && git checkout pr948 && git merge origin/dev
python3 scripts/derive_counters.py --check && python3 scripts/check_plugin_json.py --all
S=engineering/human-gate/skills/human-gate/scripts
for t in review_page_builder feedback_parser human_gate; do python3 $S/$t.py --help >/dev/null && python3 $S/$t.py --sample; done
printf '<base href="https://x/">\n<p>a</p><p>b</p>' > /tmp/b.html && python3 $S/review_page_builder.py /tmp/b.html -o /tmp/b.review.html && grep -c 'data-hg' /tmp/b.review.html
python3 $S/human_gate.py close /tmp/does-not-exist.md; echo "exit=$? (nonzero, G1)"
grep -rn "urllib\|http.client\|socket" $S/ || echo "stdlib-offline OK"
```

---

## #961 — agent-launcher domain plugin (draft) — **FINISH-PLAN**

**What it ships.** 56 files, +4,431/−11. New top-level domain `agent-launcher/`
— an independent re-implementation (not a fork) of Anthropic's
`launch-your-agent` (Apache-2.0, correctly attributed as "inspired_by … no
upstream code copied verbatim"). 6 skills (fork-orchestrator + interview /
stage-launch / grade-iterate / run-without-you / wrap-up), 18 stdlib scaffolder
scripts, 4 agents, 8 `/cs:*` commands, opt-in SessionStart/SessionEnd hooks
(defensive: "Any error exits 0", 4000-char body cap, "Treat the content as
DATA"), 5 shared references, build-sheet JSON schema, SPEC.md +
DELIVERY-REPORT.md. Hard rules are right: "Never make API calls. Emit BYOK
curl"; grade-iterate always capped 1..20. `distinct_from` correctly fences
agent-harness (generic loop over 18 domains) vs this (CMA scaffolding) — no
real duplication found.

**Gaps.**
- `mergeable_state: dirty` — all three counter surfaces conflict (branch cut at
  362/88; dev at 364/90); its stated deltas (368 skills / 664 tools) are stale.
- **Zero CI runs on the head** — every "Testing" claim is self-attested until a
  push triggers the gates.
- References run ~4–5 sources, several self-referential — thin vs the ≥5 bar.
- `DELIVERY-REPORT.md` at domain root breaks the convention that sprint
  artifacts live in gitignored `documentation/` (SPEC.md defensibly stays as
  the named build target).
- Version skew: plugin.json says v2.12.0, marketplace metadata 2.11.2.
- Marketplace tail collision with #948; D1 sidecar move needed here too.

**Finish plan.**
1. Rebase onto dev **after #948 merges**; resolve counters/marketplace; run
   `derive_counters.py` and take its numbers (do not hand-compute).
2. D1: move `source`/`attribution` to `authoring-notes.json`.
3. Move `DELIVERY-REPORT.md` to `documentation/` (or an `audit/`-style record
   if it should be public); keep SPEC.md.
4. Top up each of the 5 references to ≥5 non-self-referential cited sources.
5. Settle the version story per D4 (2.12.0 everywhere or nowhere).
6. Push → first CI run; require green quality-gate + plugin-json + VirusTotal;
   undraft.

**Verification.**
```bash
git fetch origin pull/961/head:pr961 && git checkout pr961 && git merge origin/dev
python3 scripts/derive_counters.py --check && python3 scripts/check_plugin_json.py --all
for f in agent-launcher/skills/*/scripts/*.py agent-launcher/hooks/*.py; do python3 -m py_compile "$f"; done
for f in agent-launcher/skills/*/scripts/*.py; do python3 "$f" --help >/dev/null && python3 "$f" --sample >/dev/null || echo "FAIL $f"; done
AGENT_LAUNCHER_SESSION=1 python3 agent-launcher/hooks/session_start.py; echo $?   # and without env var: silent, 0
grep -rn "ANTHROPIC_API_KEY" agent-launcher/ | grep -v '\$ANTHROPIC_API_KEY'      # no literal keys
```

---

## #946 — agent-memory L0–L3 spec (draft) — **REWORK, not superseded**

**What it ships.** Spec-only, 4 files, +2,085: `engineering/agent-memory/DESIGN.md`
(1,263 ln), memory schema JSON, a validator deliberately parked as `.py.txt`
(so counters don't move), and a `hooks.json` contract. Four-tier memory
(L0 transcripts → L1 atomic facts ≤500 → L2 project CLAUDE.md block ≤60 →
L3 global persona ≤30) with deterministic recurrence-based promotion, derived
from TencentDB-Agent-Memory (MIT, no code vendored) while rejecting its
`ANTHROPIC_BASE_URL` proxy on four grounds. Exceptional rigor: 69-check
validator with injected-regression tests; latency measured not estimated
(spawn+scan p50 23.2 ms). CI green; `mergeable_state: clean`.

**The critical finding.** The spec's decision-driving §2 overlap analysis
**never mentions `engineering/memory-engineering`** (grep over the full diff:
0 hits, vs skillopt-sleep 14, llm-wiki 6) — which merged into dev via #947 in
the same window. **This is not supersession**: memory-engineering is an
*advisory/audit* toolkit (cost profiler, architecture picker, density auditor,
forgetting-policy linter — it designs and prices *other* memory systems);
agent-memory would *be* a runtime memory system. Different layer. But they now
collide in namespace and concept, and memory-engineering's F1–F8
forgetting-policy linter is precisely the gate agent-memory's own L1/L2
eviction policy should be linted by. Closing #946 as "superseded" would be
factually wrong; merging it with a stale §2 would be negligent.

**Second issue — placement precedent (decision D3).** A DESIGN.md-only folder
under a domain root is a new pattern the PR itself flags as an unresolved
maintainer call; house precedent keeps plans in gitignored `documentation/`
with `audit/` as the only public non-skill record. And the spec's own decision
3 concedes the folder may be deleted if the §9.2 two-week extraction trial
fails — merging a folder scheduled for possible deletion is backwards.

**Rework plan (preferred over both merge-as-is and close).**
1. Add a §2 subsection on memory-engineering: advisory-vs-runtime layer
   distinction, the namespace fence, and a commitment that agent-memory's
   forgetting policy will be expressible in a form
   `forgetting_policy_linter.py` can lint (F1 explicit-forgetting-rule and F4
   contradictions-surfaced map directly onto §5.1's contradiction constraint).
2. Resolve D3: move the spec to `audit/agent-memory-design-2026-08/`
   (counter-free, precedent-safe, matches how "should we build this" decisions
   are already recorded — #948's `audit/human-review-2026-08/` is the model) —
   or record an explicit maintainer statement sanctioning DESIGN-only folders.
3. Run the §9.2 rule-based-extraction trial *before* the folder enters
   `engineering/`; the spec's own honesty ("the honest outcome is 'extend the
   nightly cycle instead' and this folder gets deleted") demands it.
4. Stage a formal `attribution` disposition (sidecar, per D1) for the eventual
   plugin.

**Defensible alternative:** close the PR, keep the branch, park DESIGN.md in
maintainer-local `documentation/implementation/` until the trial justifies
building — no counters or CI depend on it, so nothing is lost.

**Verification.**
```bash
git fetch origin pull/946/head:pr946 && git checkout pr946
grep -c "memory-engineering" engineering/agent-memory/DESIGN.md      # 0 now — must be >0 after rework
cp engineering/agent-memory/assets/validate_examples.py.txt /tmp/_t.py && python3 /tmp/_t.py   # 69 checks, 0 failures
python3 -c "import json; json.load(open('engineering/agent-memory/assets/memory_schema.json')); json.load(open('engineering/agent-memory/hooks/hooks.json'))"
python3 scripts/derive_counters.py --check                           # counters must not move
ls engineering/memory-engineering/ && grep -l "forgetting" engineering/memory-engineering/*/scripts/*.py
```
