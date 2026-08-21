# Master report — Open-PR stream audit (25 PRs)

**Audited:** 2026-08-21 · **Branch:** `claude/pr-audit-planning-mhy82k` ·
**Scope:** every open pull request against `dev` (25 PRs, #788 → #967), each read
diff-by-diff and judged against the repo's own acceptance bar (CLAUDE.md +
CONTRIBUTING/CONVENTIONS contract, plugin.json schema rules, stdlib-only script
discipline, counter governance, skill-package pattern).

**Method:** five parallel deep-dive audits, one per PR group. Every material
claim was re-executed, not read: PR heads fetched locally
(`git fetch origin pull/N/head`), test-merged against `origin/dev` (`6972e65`),
gate scripts run (`derive_counters.py --check`, `check_plugin_json.py --all`,
`check_dual_publish.py`, skill validator + security auditor), scripts
smoke-tested (`--help`/`--sample`/`--example`), YAML parsed, external claims
verified against primary sources (AWS pricing blog, upstream GitHub repos,
issue #954's verbatim CLI error output). Baseline on `dev` is green: counters
pass, 90/90 manifests pass.

Detail files: [fix-series-governance.md](fix-series-governance.md) (#936–#940) ·
[fix-series-small.md](fix-series-small.md) (#966, #964, #932, #929, #895) ·
[new-skills.md](new-skills.md) (#967, #944, #926, #965, #942, #943) ·
[closures.md](closures.md) (#959, #913, #788, #955, #956, #957) ·
[maintainer-drafts.md](maintainer-drafts.md) (#961, #948, #946).

---

## 1. Verdict table (25 PRs)

| PR | Title (short) | Author | Verdict | One-line rationale |
|---|---|---|---|---|
| #936 | repair 14 unloadable YAML frontmatter blocks + gate G10 | benrfairless | **MERGE** | All 14 repairs verified byte-identical text; gate reproduces 0 errors on dev+series |
| #937 | recalibrate skill-tester validator + advisory gate G7 | benrfairless | **MERGE** | Old required-frontmatter schema was fictional (verified); advisory flip is safe by construction |
| #938 | remove retired model IDs / stale pricing, flip G7 blocking | benrfairless | **MERGE** | Clears a defect the repo's own July audit logged; blocking flip proven safe on current dev (0 findings / 2,703 files) |
| #939 | agent `skills:` → `plugin:skill`, fix name collisions, resync mirrors | benrfairless | **MERGE-WITH-CHANGES** | Mechanically correct (109 refs, 0 unresolvable re-verified) but needs the preloading policy decision, a rebase + mirror resync, and the comma-separated `skills:` encoding confirmed |
| #940 | gate 3 drifted counter sites, rewrite ClawHub §5 | benrfairless | **MERGE-WITH-CHANGES** | Right design, stale payload (fails its own gate on today's dev with 12 mismatches) and its §5 rewrite collides head-on with #966 — see §3 |
| #966 | strip `source`/`attribution` from 39 plugin.json → sidecars | dylanpulver | **MERGE** | Fixes live install failure (issue #954 — 37/88 at filing, 39/90 as of this audit); every removed value preserved byte-equal in `authoring-notes.json`; policy amended in-PR |
| #964 | cap 4 marketplace descriptions at 1024 chars | automotua | **MERGE** | Exactly the 4 over-cap entries, meaning preserved; take the offered CI guard (commercial-skills sits at 1021/1024) |
| #932 | correct stale DynamoDB on-demand pricing | LeeroyHannigan | **MERGE** | Verified against the live AWS Nov-2024 50%-cut announcement; one line, exactly right |
| #929 | harden gws_recipe_runner subprocess + `--yes` gate | warnes | **MERGE** | `shell=True` removed, zero shell-metacharacter templates (all 48 scanned), refusal path executed and correct |
| #895 | add LinkedIn Skills to Related Projects | sergebulaev | **MERGE-WITH-CHANGES** | Real, active MIT repo (now 578★); matches toprank precedent; refresh the stale "10 skills / 303 stars" row first |
| #967 | boost-asio-pro (async C++ networking) | alexprivalov | **MERGE** | Best-written external skill in the stream; genuinely expert (strand semantics, version floors); security-clean |
| #944 | stock-analysis (sector-relative fundamentals) | AlenSarangSatheesh | **MERGE-WITH-CHANGES** | Highest-value contribution: 24.7k lines, 26 sector playbooks, 5 real stdlib engines all verified running; needs desc ≤1024, two section headings, one FP disposition |
| #965 | dsh-deepread (evidence-first reading) | xiehuan123 | **MERGE-WITH-CHANGES** | Solid disciplined content; rename off the personal `dsh-` prefix, add citations, register as plugin |
| #942 | embedded-iot-mentor | mh-mansouri | **MERGE-WITH-CHANGES** | Real practitioner judgment, genuine gap, auto-joins domain plugin; clear the 100-line validator floor via a references file |
| #943 | swedish-mentor | mh-mansouri | **MERGE-WITH-CHANGES** (borderline) | Thinnest of the batch; needs references + plugin.json to match productivity siblings or it lands undistributable |
| #926 | business-name-fit (cross-cultural naming) | mh-mansouri | **MERGE-WITH-CHANGES** | Genuinely expert, honest, correctly attributed port; one-word trigger fix + 2 more cited sources |
| #961 | agent-launcher domain plugin (draft) | maintainer | **FINISH-PLAN** | Construction done, integration not: rebase, re-derive counters, top up references, first CI run |
| #948 | human-gate plugin (draft) | maintainer | **FINISH-PLAN → merge** | Content complete after 7 bot-review rounds, CI green; only rebase + counter re-derive + sidecar move (see §3) remain |
| #946 | agent-memory L0–L3 spec (draft) | maintainer | **REWORK** (not superseded) | Advisory-vs-runtime distinction means memory-engineering does NOT supersede it — but §2 never mentions memory-engineering and must; settle the DESIGN-only-folder precedent |
| #959 | remon-awad persona | awadremon-ops | **CLOSE** | Self-named vanity persona; house personas are role archetypes; duplicates agent-harness by its own admission |
| #913 | Ontoly Software Graph skill | 0xsarwagya | **CLOSE** | Undisclosed promotion of author's own day-old 1-star tool; directs agents to execute an unvetted external CLI; duplicates 4 existing skills |
| #788 | collab-proof retrospective skill | dong7812 | **CLOSE (superseded)** | Already re-landed on dev byte-identical (`753adb4`) with an improved plugin.json; remaining hunk would delete youtube-full and revert counters |
| #955 | REAPER Gemini/Cursor prompts | sveinnhelgihalldorsson-ops | **CLOSE** | Off-mission per-tool prompt docs inside the machine-generated `.gemini/` sync tree |
| #956 | Ableton Gemini/Cursor prompts | sveinnhelgihalldorsson-ops | **CLOSE** | Same; ships an artifact its own sibling audit rates 6 WRONG / 8 RISKY |
| #957 | Ableton test reports | sveinnhelgihalldorsson-ops | **CLOSE** | Personal QA transcripts with local Windows paths; self-contradictory verdicts; depends on #956 |

**Totals:** 8 MERGE · 8 MERGE-WITH-CHANGES · 6 CLOSE · 3 maintainer-draft plans.

---

## 2. The three biggest findings

1. **~43% of the marketplace is uninstallable in Claude Code today, and two open
   PRs "fix" it in opposite directions.** Issue #954 documents the verbatim
   failure (`Validation errors: : Unrecognized key: "source"`). #966 resolves it
   by *removing* the extension keys from all 39 manifests (provenance preserved
   byte-equal in `.claude-plugin/authoring-notes.json` sidecars — independently
   verified, zero attribution loss) and making any extra key a hard CI FAIL.
   #940's CLAUDE.md §5 rewrite goes the other way: it asserts extension fields
   "need no special dispensation." Both cannot be policy. **Recommendation:
   adopt #966's direction** — it is evidence-backed by a reproduced installer
   error, ships the enforcement to keep the bug fixed, and updates CLAUDE.md in
   the same change; #940 must drop/rework its §5 paragraphs at rebase time
   (§3, decision D1).

2. **The benrfairless series (#936–#940) is a stacked branch chain
   (936 ⊂ 937 ⊂ 938 ⊂ 939 ⊂ 940) and its quality is real.** Every mechanical
   claim survived independent re-execution (14/14 YAML repairs byte-identical,
   G7 0-findings on dev+series, 109 agent-skill refs 0-unresolvable, dual-publish
   0-drifted). Merging any later PR lands all earlier ones — do not cherry-merge.
   #936–#938 are mergeable today; #939 needs one policy decision (D2) and a
   rebase; #940 must go last with regenerated numbers because its own gate
   freezes the counters it writes.

3. **The external new-skill pipeline works — when the contribution is real.**
   Six of eight external skill PRs are keepers (one, #944, is arguably the
   deepest single domain skill ever contributed to the repo), and the three
   rejects are exactly the categories a curated library must refuse: vanity
   personas (#959), undisclosed self-promotion steering agents to run an
   unvetted third-party binary (#913), and personal working-notes dumps in
   generated directories (#955–#957). None of the 25 PRs has ever had a CI run —
   fork workflows are gated on maintainer approval, so every green claim above
   is from this audit's local reproduction. **Approve workflow runs before
   merging anything.**

---

## 3. Decisions the maintainer must make (blocking, in order)

| # | Decision | Affects | Recommendation |
|---|---|---|---|
| **D1** | Extension-key policy: strip-to-sidecar + strict validator (#966) vs "extras tolerated" (#940 §5) | #966, #940, #948, #961, and every future plugin | **Adopt #966.** It fixes a reproduced install failure and enforces the fix. #940 reworks §5 at rebase; #948/#961 move their `source`/`attribution` blocks into `authoring-notes.json` sidecars before undrafting (their current manifests would hard-fail #966's validator) |
| **D2** | Agent `skills:` field: keep `plugin:skill` preloading (~2.5k tokens per agent spawn) or delete the field (author offers both variants) | #939 | Keep preloading — the fixed form makes 81 agents' skill refs actually resolve; token cost is bounded and visible. Record the decision on the PR |
| **D3** | DESIGN-only folders under domain roots: sanctioned pattern or not | #946 | Not sanctioned: move the spec to `audit/agent-memory-design-2026-08/` (public-record pattern, counter-free) or park in gitignored `documentation/` until the §9.2 extraction trial justifies building |
| **D4** | Release-version framing: do #966+#964 ship as a patch (v2.11.3 "installability") and the new-skill batch as v2.12.0? | changelog, marketplace `metadata.version` | Yes — see merge order below; #940 (rebased) is the natural counter-true-up vehicle for the release that closes the batch |

---

## 4. Global merge order

Zero git-level conflicts exist between the independent PRs (verified pairwise);
the constraints are the stack (#936→#940), the D1 policy fork, and the
marketplace-tail collision between #948 and #961.

**Phase 0 — hygiene (now).** Approve GitHub Actions runs on all fork PRs so the
gates execute on GitHub runners, not only in this audit's local reproduction.

**Phase 1 — governance floor.** Merge **#936 → #937 → #938** (stacked; all
test-merge clean on today's dev; all verified). This lands gates G10 + G7 that
protect everything after.

**Phase 2 — installability (D1).** Merge **#966**, then **#964**. Post-merge,
run `claude plugin install roast@claude-code-skills` as the real-world check.
Follow-up (small PR): update the 3 living docs that still tell authors to put
attribution in plugin.json (paths in [fix-series-small.md](fix-series-small.md)).

**Phase 3 — surgical fixes.** Merge **#932**, **#929**; refresh #895's row
(11 skills / current stars) then merge **#895**.

**Phase 4 — new skills** (each after its listed required changes; per-PR change
lists in [new-skills.md](new-skills.md)): **#967 → #944 → #926 → #965 → #942 →
#943**. Ordered by readiness; #943 last and only if the author packages it.
Counters intentionally drift during this phase — do **not** hand-patch per merge.

**Phase 5 — the big rename + counter close-out.** After D2: rebase **#939**
(re-run all four mirror syncs; convert dev's new `cs-book-to-skill.md`; confirm
or re-encode the 9 comma-separated `skills:` values as YAML lists), merge.
Then rebase **#940** as the **final write**: regenerate every number from
`derive_counters.py`, add `agents`/`commands` patterns to `CLAIM_PATTERNS`,
rework §5 per D1, merge. `derive_counters.py --check` exits 0 → the release is
consistent by construction.

**Phase 6 — maintainer drafts.** **#948** first (rebase, counters, sidecar move
per D1, undraft, merge — content is done). Then **#961** (rebase after #948 to
take the marketplace tail, re-derive counters, top up references, first CI run).
**#946** per D3.

**Closures (any time, independent):** #959, #913, #788, #955, #956, #957 —
ready-to-post close comments in [closures.md](closures.md). All six are polite
and specific; #788's credits the contributor whose work already shipped.

---

## 5. Improvement streams (post-merge, non-blocking)

Recurring weaknesses this stream exposed, each worth one follow-up PR:

1. **CI never runs on fork PRs.** Every gate the repo has was moot for all 25
   PRs. Add a `pull_request_target`-safe path or a documented
   approve-runs-on-first-triage routine so external PRs get at least G1/G3/G10.
2. **Description-length regression guard.** #964 fixes 4 over-cap descriptions
   but `commercial-skills` sits at 1021/1024. Fold a ≤1024 check into
   `check_plugin_json.py` (the author offered it).
3. **Counter-drift-by-design for external PRs.** CONTRIBUTING correctly tells
   contributors not to touch counters; the repo should have a standing
   "true-up" routine (Phase 5's rebased #940 is this stream's instance).
4. **Reference-source floor is unevenly applied.** Four of the six accepted
   skills need citation top-ups; the write-a-skill checklist runner should be in
   the fork-PR CI path (see 1) so this is flagged at submission.
5. **Security-auditor false positives.** #944's one CRITICAL is a verified FP on
   finance vocabulary (`holdco-assetmgr.md:58`); the auditor needs an
   allowlist-with-reason mechanism like `check_model_freshness_allowlist.txt`.
6. **Doc drift after #966.** Three living docs still teach the old attribution
   location (exact lines in [fix-series-small.md](fix-series-small.md)).
7. **Related-Projects rows rot by design** (hardcoded star counts). Either drop
   star counts from the table or accept staleness as policy.

---

## 6. Verification — how this audit's claims are re-checked

Every per-PR section in the detail files ends with an executable verification
block. The stream-level invariants, runnable at any phase boundary:

```bash
python3 scripts/derive_counters.py --check      # counters consistent (must pass at Phase 5 close)
python3 scripts/check_plugin_json.py --all      # all manifests valid under the current policy
python3 scripts/check_dual_publish.py           # 12 pairs, 0 drifted
python3 scripts/check_frontmatter.py --all      # post-#936: 0 errors
python3 scripts/check_model_freshness.py --all  # post-#938: 0 findings, exit 0
python3 scripts/smoke_scripts.py                # all skill scripts --help clean
```

Real-world close-out after Phase 2: `claude plugin marketplace add
alirezarezvani/claude-skills && claude plugin install roast@claude-code-skills`
(the exact command that fails today per issue #954).
