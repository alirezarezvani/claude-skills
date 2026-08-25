# PR audit detail — small-fix PRs (#966, #964, #932, #929, #895)

**Audited:** 2026-08-21 — PR states below (CI, mergeability, commit counts) are a snapshot from that date; re-run each verification block before acting on a verdict.

Back to [00-MASTER.md](00-MASTER.md). All five: base `dev` ✓, zero
reviews/comments/CI runs. **Pairwise file overlaps: NONE** (computed over
changed-file sets); all five test-merge clean onto dev `6972e65` — merge order
is git-unconstrained. Semantic constraint: once #966 lands, its stricter
validator hard-fails any future manifest reintroducing `source`/`attribution`
(this binds #948/#961, not these five).

---

## #966 — strip `source`/`attribution` from 39 plugin.json manifests — **MERGE**

**What it does.** 80 files, +336/−258. Removes `source` from 24 manifests and
`attribution` from 16 (39 distinct); adds a sibling
`.claude-plugin/authoring-notes.json` per manifest holding the removed value(s).
`check_plugin_json.py`: deletes `APPROVED_EXTENSIONS` — any extra key is now a
hard FAIL. CLAUDE.md ClawHub rule 5 rewritten in the same change ("Authoring
metadata now lives in a sibling file the validator never reads … `source`
remains valid in `marketplace.json` — the two schemas are not interchangeable").
`marketplace.json` correctly untouched.

**The policy question, resolved by evidence.** CLAUDE.md did bless
`source`/`attribution` as approved extension fields — *pending a ClawHub-time
stripping pipeline that never landed*. Claude Code's installer reads the raw
manifest, and issue #954 (open, 2026-08-14) documents the verbatim failure:
`✘ Failed to install plugin "roast@claude-code-skills" … Unrecognized key:
"source"` (same for `"attribution"` on grill-me). **39 of 90 plugins are
uninstallable today.** (Count reconciliation: #954 said 37 of 88 at filing,
against `aa8d778`; book-to-skill and memory-engineering landed since, each
carrying the keys — hence 39 of 90 as of this audit. Not a discrepancy.) The PR amends the documented policy in the same diff —
this is a policy update with evidence, not a violation.

**Attribution loss: none.** All 39 base-vs-head manifests compared
programmatically: every diff is a pure removal of exactly those keys, zero other
key changed; every sidecar is byte-equal (as parsed JSON) to the removed
content. Example: `engineering/caveman/.claude-plugin/authoring-notes.json`
carries the full MIT credit verbatim. MIT-derived plugins also retain
attribution in READMEs/LICENSE; the sidecar ships inside `.claude-plugin/` with
the installed plugin.

**Gates reproduced locally on the PR tree:** `check_plugin_json.py --all` → 90
OK; `derive_counters.py --check` → pass; `check_dual_publish.py` → 0 drifted;
negative test: pre-fix caveman manifest → `FAIL … extra fields:
['attribution']`, exit 1.

**Plan.** Merge in Phase 2, first of the pair. **Improvement stream (follow-up
PR):** three living docs still teach plugin.json as the attribution home and now
contradict policy —
`engineering/write-a-skill/skills/write-a-skill/references/quality_gates_for_skills.md`
(lines 61, 129), `engineering/write-a-skill/agents/cs-skill-author.md` (line
100), `engineering/security-guidance/skills/security-guidance/SKILL.md` (line
123). Point them at `authoring-notes.json`. Also: #948/#961 must move their
extension blocks to sidecars before undrafting (D1).

**Verification.**
```bash
git fetch origin pull/966/head:pr966 && git worktree add /tmp/wt966 pr966 && cd /tmp/wt966
python3 scripts/check_plugin_json.py --all            # 90 OK, 0 FAIL
python3 scripts/derive_counters.py --check && python3 scripts/check_dual_publish.py
# post-merge real-world check (the exact failing command from issue #954):
claude plugin marketplace add alirezarezvani/claude-skills && claude plugin install roast@claude-code-skills
```

---

## #964 — cap 4 marketplace descriptions at 1024 chars — **MERGE**

**What it does.** 1 file (`.claude-plugin/marketplace.json`), +4/−4. Shortens
exactly the 4 over-cap descriptions: `engineering-advanced-skills` 1132→986,
`memory-engineering` 1044→964, `research-ops-skills` 1593→957,
`markdown-html-skills` 1240→914. Unblocks GitHub Copilot CLI marketplace
loading (1024-char limit per GitHub docs).

**Evidence.** Verified on base: exactly those 4 exceed 1024, no others.
Parsed-JSON field diff over all 90 entries: only `description` differs, only in
those 4. Trims are genuinely parenthetical — all 37 skill names kept in
engineering-advanced-skills; no inventory item dropped; no mid-word cuts. One
immaterial PR-body inaccuracy: claims post-fix max is 986; actually 1021
(`commercial-skills`, untouched) — still under cap.

**Risk.** `commercial-skills` at **1021/1024** — 3 chars of headroom; the next
routine tweak re-breaks Copilot. The author offered a CI guard; it is not in
this PR.

**Plan.** Merge in Phase 2 after #966 (no overlap; release-note them together).
**Improvement stream:** accept the offered ≤1024 guard — fold into
`check_plugin_json.py` or `ci-quality-gate.yml`.

**Verification.**
```bash
git fetch origin pull/964/head:pr964
git diff origin/dev pr964 --stat        # 1 file, +4 -4
git show pr964:.claude-plugin/marketplace.json | python3 -c "
import json,sys; d=json.load(sys.stdin)
ls=sorted(((len(p['description']),p['name']) for p in d['plugins']),reverse=True)[:5]
print(ls); assert ls[0][0]<=1024"
```

---

## #932 — correct stale DynamoDB on-demand pricing — **MERGE**

**What it does.** 1 file, +1/−1:
`engineering-team/skills/aws-solution-architect/references/service_selection.md:122`
— `$1.25/M writes, $0.25/M reads` → `$0.625/M writes, $0.125/M reads`.

**Evidence.** The cited AWS Database Blog post was fetched live during audit:
"DynamoDB lowers pricing for on-demand throughput … 50% … November 1, 2024."
Post-cut us-east-1 rates match the diff exactly; both numbers precisely halved;
line context is standard (not transactional) throughput — the author's own note
that $1.25 is the correct *transactional* rate shows unusual domain care. One
harmless PR-prose overstatement (mentions figures not present in the file).

**Plan.** Merge in Phase 3, unchanged. **Improvement stream:** consider an
"as of <date> (us-east-1)" annotation convention for priced reference lines —
this class of drift will recur (same disease #938 fixed elsewhere).

**Verification.**
```bash
git fetch origin pull/932/head:pr932 && git diff origin/dev pr932   # exactly the 1-line swap
curl -sL https://aws.amazon.com/blogs/database/new-amazon-dynamodb-lowers-pricing-for-on-demand-throughput-and-global-tables/ | grep -o "50%"
```

---

## #929 — harden gws_recipe_runner subprocess execution — **MERGE**

**What it does.** 1 file, +23/−3
(`engineering-team/google-workspace-cli/.../scripts/gws_recipe_runner.py`).
Replaces `subprocess.run(cmd, shell=True)` with
`shlex.split(cmd, comments=True)` + `shell=False` (unparseable/empty handled by
skip-and-continue); adds a required `--yes` flag — `--run` without `--dry-run`
and without `--yes` now prints a refusal naming the irreversible side effects
and exits 1. Docstring/epilog updated.

**Evidence — executed, not just read.** `shell=True` count on head: 0. On the PR
head: `--help` OK; `--list --json` valid JSON (43 recipes);
`--run standup-report --dry-run` unchanged; bare `--run` → refusal + exit 1.
All 48 command templates scanned: zero use pipes/redirects/`&&`/`;`/`$()`/globs
— `shell=False` changes nothing for the current catalog; the 2 inline-comment
templates are handled by `comments=True`. The "latent footgun" framing is
honest: the fix pre-empts the injection that `cmd.format(**args)` + `shell=True`
would have created.

**Breaking change, intended:** bare `--run X` no longer executes. SKILL.md never
documents bare `--run` (checked) — no doc drift.

**Plan.** Merge in Phase 3, unchanged. **Improvement stream:** cosmetic
indentation nit on the `--yes` argument line.

**Verification.**
```bash
git fetch origin pull/929/head:pr929 && git worktree add /tmp/wt929 pr929
P=/tmp/wt929/engineering-team/google-workspace-cli/skills/google-workspace-cli/scripts/gws_recipe_runner.py
python3 $P --help && python3 $P --list --json | python3 -m json.tool >/dev/null
python3 $P --run standup-report --dry-run
python3 $P --run standup-report; test $? -eq 1     # refusal without --yes
grep -c "shell=True" $P                            # 0
```

---

## #895 — add LinkedIn Skills to Related Projects — **MERGE-WITH-CHANGES**

**What it does.** 1 file, +1/−0: one row in the README Related Projects table
linking `sergebulaev/linkedin-skills` ("10 LinkedIn skills … MIT, 303 stars").

**Evidence.** Self-promotion, yes — but matching the established `toprank`
precedent (#517/#601, disclosed in the PR). The repo is real and healthy:
verified live — public, **578★ / 90 forks**, actively pushed, genuine MIT
LICENSE, real Claude Code + Codex install docs. Genuinely on-topic. Row text is
stale, not fabricated (10→11 skills, 303→578 stars since July filing).
Docs-only; counters unaffected.

**Required change (pre-merge).** Refresh the row: "11 LinkedIn skills … MIT" —
and preferably drop the hardcoded star count entirely (toprank's "107 stars"
has the same rot disease). One-line review suggestion; author has been
convention-careful (correct base, correct table format).

**Plan.** Phase 3 after the row refresh. **Improvement stream:** decide the
Related-Projects star-count policy repo-wide (master §5.7).

**Verification.**
```bash
git fetch origin pull/895/head:pr895 && git diff origin/dev pr895   # single added row
curl -s https://api.github.com/repos/sergebulaev/linkedin-skills | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['stargazers_count'],d['license']['spdx_id'],d['pushed_at'])"
```
