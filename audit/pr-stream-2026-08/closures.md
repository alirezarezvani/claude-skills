# PR audit detail — recommended closures (#959, #913, #788, #955, #956, #957)

**Audited:** 2026-08-21 — PR states below (CI, mergeability, commit counts) are a snapshot from that date; re-run each verification block before acting on a verdict.

Back to [00-MASTER.md](00-MASTER.md). Six PRs should be closed, each for a
different, specific reason — none for "low effort." Draft close comments are
included; all are polite, name the concrete gap, and (where the contributor
could realistically resubmit) point at the path back in.

---

## #959 — remon-awad persona (awadremon-ops) — **CLOSE**

**What it is.** One file: `agents/personas/remon-awad.md` (+147). A
"cross-domain copilot for Remon" routing goals to existing agents, with fallback
to `engineering/agent-harness`'s `/cs:harness`.

**Why close.**
- **Person-named persona is not house style**: the 7 existing personas are role
  archetypes (content-strategist, devops-engineer, startup-cto, …). This one is
  named after the contributor and scoped to one individual ("Cross-domain
  copilot for Remon").
- **Duplicates agent-harness by its own admission**: the file itself says to
  fall back to "the repo's own generic router … against the real per-domain
  manifest," and concedes its own cached routing table will rot.
- **Not registered** (personas README table, counters untouched); brand-new
  `-ops` account, single-commit drive-by shape.
- Credit where due: all 23 referenced agent/asset paths were verified real —
  zero hallucinations. The diligence is good; the artifact is a personal
  dotfile, not a library asset.

**Draft close comment.**
> Thanks for the care here — every one of the 23 referenced paths checks out,
> which is rare. Closing anyway for two structural reasons: (1) personas in
> `agents/personas/` are role archetypes, not person-scoped configs — a persona
> named for one individual belongs in your own `~/.claude/agents/`; (2) the
> functional core duplicates `engineering/agent-harness`'s manifest-driven
> `/cs:harness` router, which the file itself names as the fallback — a
> hand-cached dispatch table in front of it is exactly the drift the manifests
> exist to prevent. If you want to contribute in this lane, extending the
> agent-harness manifests (or proposing a *role*-named dispatcher with a clear
> delta over `/cs:harness`) would be welcome.

**Verification.**
```bash
git fetch origin pull/959/head:pr-959
git show pr-959:agents/personas/remon-awad.md | head -8   # self-named frontmatter
ls agents/personas/                                       # role archetypes only
```

---

## #913 — Ontoly Software Graph skill (0xsarwagya) — **CLOSE**

**What it is.** 2 files, +128: a SKILL.md instructing agents to run
**`ontoly build .`** and prefer "Ontoly CLI or MCP capabilities" over reading
source, plus a 13-line, zero-citation checklist reference.

**Why close (in order of severity).**
1. **Supply-chain risk**: directs agents to install and execute an unvetted
   third-party CLI against user repositories. `ontoly` resolves to
   **the PR author's own repo**, created **the day before the PR** (2026-07-13
   vs 2026-07-14), 1 star / 1 fork — authorship undisclosed in the PR body.
   Its only third-party trace is the identical skill text seeded into another
   curated skill repo (cross-repo promotion pattern).
2. **Hard external dependency**: `grep -ri ontoly` outside the PR → zero hits;
   the skill is inert without the vendor tool. Violates the self-containment
   spirit of the no-paid-dependency rule even if technically "open-source."
3. **Full lane overlap**: its own Cross-References name the incumbents —
   codebase-onboarding, monorepo-navigator, dependency-auditor,
   mcp-server-builder. Strip the branding and nothing new remains.
4. 13-line reference, 0 citations vs the ≥5-source bar; keyword-stuffed trigger
   designed to catch broad queries ("architecture review") and route them to
   the vendor tool.

**Draft close comment.**
> Closing. Two blockers: (1) the skill's core instruction is to install and run
> the external `ontoly` CLI — which is your own project, created the day before
> this PR, and that authorship isn't disclosed here. This repo can't endorse
> executing an unvetted third-party binary against user codebases, and
> undisclosed self-promotion isn't something we can merge. (2) Coverage-wise,
> the skill's own Cross-References list the four existing skills that already
> own this lane. If you want to resubmit: disclose authorship, make it
> tool-agnostic ("graph-backed codebase evidence" covering the established
> field, with no auto-run of any vendor CLI without explicit user consent),
> cite ≥5 independent sources, and show the tool's maturity first.

**Verification.**
```bash
git fetch origin pull/913/head:pr-913
git show pr-913:engineering/skills/ontoly-software-graph/SKILL.md | grep "ontoly build"
grep -ri "ontoly" --include="*.md" . | grep -v pr-913     # zero in-repo provider
```

---

## #788 — collab-proof (dong7812) — **CLOSE (superseded — not rejected)**

**What it is.** The oldest open PR (June 1): `engineering/collab-proof/` plugin,
8 files, +699/−41. Full review history: blocking review addressed June 3; owner
asked for a rebase June 15; contributor never rebased (9+ weeks idle).

**Why close.** The content **already shipped**: dev commit `753adb4`
"feat(engineering): add collab-proof skill (clean re-land of #788)" +
`7303501` (trailing newline + attribution block). Diffed PR head vs dev:
`SKILL.md` is **byte-identical**; the only delta is plugin.json, where **dev's
version is strictly better**. What remains in the PR is actively harmful: its
stale `.claude-plugin/marketplace.json` hunk was written against v2.9.0 and
would **delete the `youtube-full` plugin entry** and revert marketplace
counters/version. There is nothing left to land; do not request a rebase.

**Draft close comment.**
> Closing as landed, not rejected: your skill was merged to dev in `753adb4`
> (a clean re-land of this PR) with your authorship preserved in the plugin
> manifest (`"author": {"name": "dong7812"}`), plus a small manifest polish in
> `7303501`. This PR's remaining delta is only a stale marketplace.json hunk
> that would now regress newer entries, so there's nothing further to merge
> here. Thanks for the contribution and for working through the June review —
> `engineering/collab-proof/` is live because of it.

**Verification.**
```bash
git log --oneline origin/dev -- engineering/collab-proof/     # 753adb4 + 7303501
git fetch origin pull/788/head:pr-788
diff <(git show pr-788:engineering/collab-proof/skills/collab-proof/SKILL.md) engineering/collab-proof/skills/collab-proof/SKILL.md   # empty
git show pr-788:.claude-plugin/marketplace.json | grep -c youtube-full    # 0 → destructive hunk
```

---

## #955 / #956 / #957 — Gemini/Cursor DAW prompt docs (sveinnhelgihalldorsson-ops) — **CLOSE as a set**

**What they are.** A coupled trio (opened the same second): #955 REAPER prompts
(4 files, +378), #956 Ableton prompts (4 files, +831), #957 QA reports *about
#956's file* (5 files, +585). All land hand-authored Gemini system prompts and
**Cursor personal skills** ("copy to `~/.cursor/skills/...`") under
`.gemini/MD research/`.

**Why close.**
1. **Off-mission**: this is a Claude skills library; multi-platform support is
   delivered by `scripts/sync-*-skills.py` from canonical SKILL.md packages —
   never hand-authored per-tool prompt docs. No house pattern fits.
2. **Wrong location**: `.gemini/` on dev contains only machine-generated
   symlinks + `skills-index.json` (verified). Hand content there pollutes a
   sync-managed tree.
3. **Personal working-notes leakage**: #957's reports embed the contributor's
   local Windows paths (`C:\Users\RoG\...`); its three reports contradict each
   other ("GO, 96/100" vs "not ready to ship unchanged"); #956 ships an
   artifact its own sibling audit rates 6 WRONG / 8 RISKY (including an
   invented `Live.Application.get_document()` API), with the claimed fixes in
   no PR.
4. Not skill packages: no SKILL.md-per-convention, no plugin, no counters;
   spaced filenames (`MD research/`) against kebab-case.

Credit: the underlying REAPER/Ableton research is competent (the RPP-chunk and
reapy corrections are real). It just isn't a contribution *to this library*.

**Draft close comment (post on #955, reference on #956/#957).**
> Closing all three together. The research quality is real — the RPP-chunk and
> reapy corrections are the kind of accuracy work we like — but these are
> Gemini/Cursor prompt documents in `.gemini/`, which is a machine-generated
> sync directory here (built by `scripts/sync-gemini-skills.py` from canonical
> SKILL.md packages; hand-added files there get orphaned by the next sync).
> The repo also can't take personal working files (the test reports embed
> `C:\Users\...` paths and internal MCP server names). If you'd like to
> contribute DAW automation properly, the path is a real skill package —
> `SKILL.md` + stdlib scripts (an RPP parser would be a great deterministic
> tool) + cited references — per `engineering/write-a-skill`. Happy to review
> that.

**Verification.**
```bash
for n in 955 956 957; do git fetch origin pull/$n/head:pr-$n; git diff --stat origin/dev...pr-$n | tail -1; done
git ls-tree origin/dev .gemini/                                   # sync-output only
git grep -l 'C:\\\\Users' pr-957 -- '.gemini/'                    # personal-path leakage
```
