# skill-doctor — grade the agent setup from real sessions

A rebuild of [warpdotdev/common-skills' `skill-doctor`](https://github.com/warpdotdev/common-skills/tree/f3b58c81d1cfd5d8eabf2e32edb32db2b0573923/.agents/skills/skill-doctor)
(MIT, © Denver Technologies, Inc.) as a full plugin in this library's conventions.

The idea is upstream's, and it is a good one: the only honest benchmark for an
agent setup is **what actually happened in its recent sessions**. skill-doctor
harvests the last N days of local Claude Code / Codex conversations scoped to one
repo, has the agent judge each condensed transcript against two fixed rubrics
(efficiency and code quality), measures which installed skills actually fired,
and proposes only the skill edits the evidence justifies — rendered as one local,
shareable HTML report.

See **Deviations from upstream** below for the authoritative list of what changed.

---

## Pipeline

| Step | Who | Artifact |
|------|-----|----------|
| 1. Collect | `scripts/collect_sessions.py` | `inventory.json` + redacted `transcripts/*.md` |
| 2. Score | the agent, against `scorers/*.md` | `session_scores.json` (labels + reasons only) |
| 3. Draft | the agent, per `references/skill_edit_governance.md` | `proposed/<skill>/SKILL.md` + `suggestions.json` |
| 4. Aggregate | `scripts/score_aggregator.py` — **the gate** | validated `report.json` (all arithmetic lives here) |
| 5. Render | `scripts/render_report.py` | self-contained `report.html` |

Everything lands in one `mktemp -d` scratch dir; nothing is written into the
user's repo and nothing is uploaded anywhere. All three tools are stdlib-only and
support `--help`, `--output json`, and `--sample`.

## The gate (what makes this version stricter)

Upstream had the scoring agent compute its own averages and assemble
`report.json` by hand. Here `score_aggregator.py` owns that step and refuses:

- a score whose label is not in the rubric table (numbers are derived, never accepted);
- a score for a session that was never sampled (fabrication guard);
- a reason under 20 characters (theater guard);
- a suggestion that cites no sampled session id (evidence traceability);
- a suggestion with no drafted diff.

Exit 4 means nothing is written — the SKILL.md instructs the agent to fix what
the gate names, never to bypass it. Zero suggestions passing the filing bar is a
valid, reportable success.

## Privacy contract

- Session history is read-only input; artifacts are `chmod 0700`/`0600`.
- Every transcript line passes a 12-pattern secret redactor (keys, tokens, JWTs,
  connection strings, env-style secrets) **before** it touches disk; there is no
  off switch, and per-label redaction counts land in the inventory and report.
- The report page itself says what was and wasn't collected.

Details and sources: `skills/skill-doctor/references/session_mining_privacy.md`.

## Deviations from upstream

**This numbered list is the authoritative record.** The `attribution.derivation_note`
in `.claude-plugin/authoring-notes.json` summarizes it; if the two ever disagree, this list wins.

**Structural**

1. **Repo-native plugin layout.** Upstream is a bare skill folder
   (`SKILL.md`, `scripts/`, `scorers/`, `references/`, `assets/`). Here it is a full
   plugin: `skills/skill-doctor/{SKILL.md,scripts,scorers,references,assets}` plus
   `agents/cs-skill-doctor.md`, `commands/cs-skill-doctor.md`, a manifest plus an
   `attribution` record in `.claude-plugin/authoring-notes.json`, and this README.
2. **Preserved verbatim:** both scoring rubrics (`scorers/efficiency.md`,
   `scorers/code-quality.md`) and the skill-improvement method + filing bar (now
   §1–§2 of `references/skill_edit_governance.md`). These are the best part of
   upstream and were not touched.
3. **Warp session source dropped.** Upstream reads Warp's `warp.sqlite` stores via
   a 388-line hand-rolled protobuf decoder (`warp_decoder.py`). This library
   targets Claude Code (plus the Codex sync), and vendoring an unverifiable binary
   decoder conflicts with its keep-scripts-auditable convention. Warp users should
   run upstream. `--harness` accordingly offers `auto|all|claude|codex`.
4. **Upstream's `test_collect_sessions.py` not vendored** — this repo ships no test
   framework by design; the scripts carry `--sample` smoke fixtures instead.

**The gate (new, no upstream counterpart)**

5. **`score_aggregator.py` added.** Upstream's Step 3 asks the scoring LLM to do
   the averaging and JSON assembly itself. Per this repo's "algorithm over AI"
   principle, all arithmetic moved into code: labels map to scores via embedded
   tables mirroring the rubrics, weights (0.5/0.35/0.15) and the letter-grade
   table are applied deterministically, and `report.json` is emitted only after
   validation passes.
6. **Anti-theater checks.** Scores for unsampled sessions are rejected outright
   (upstream would silently average them in), every sampled session must be
   scored, reasons are length-checked, duplicate entries fail.
7. **Evidence traceability enforced.** Upstream's rule that suggestions "must
   trace back to observed waste" was prose; here a suggestion without a sampled
   session citation or a diff fails the gate.
8. **`--emit-template`** prints the exact scores-file skeleton for the sampled
   sessions, so the scoring agent cannot mis-shape the handoff.

**Collector hardening**

9. **Secret redaction, always on.** Upstream writes condensed transcript excerpts
   to disk unredacted. Every entry now passes `redact_secrets()` (12 ordered
   patterns: private-key blocks, AWS/GitHub/Anthropic/OpenAI/Slack/Stripe tokens,
   JWTs, bearer tokens, connection strings, URL credentials, env-style secret
   assignments) before writing; per-label counts land in `inventory.json`. There
   is deliberately no `--no-redact` flag. Follows the `skillopt-sleep` deviation
   precedent and `productivity/handoff`'s redaction linter.
10. **Artifact permissions.** Output dirs `chmod 0700`, files `0600` (upstream
    left them at the process umask). Applied to transcripts, inventory, report
    JSON and HTML.
11. **Plugin-layout skill discovery.** Skill roots now also match
    `<root>/*/skills/*/SKILL.md`, so marketplace-plugin checkouts (like this
    repo) are inventoried, not just bare `skills/<name>/` folders.
12. **Slash-command usage detection.** Claude Code `<command-name>` markers in
    user turns are mined for skill usage before the injected-content filter
    drops them (upstream only detected the `Skill` tool and path mentions), and
    namespaced invocations like `/cs:foo` match skill `foo`.
13. **Deterministic ordering.** Session sort keys are tie-broken by path/id so
    two runs over the same history sample identically; `--sample` runs the whole
    pipeline on fixed synthetic fixtures (one with a planted fake secret, so the
    redactor is exercised) without touching real history.
14. **House CLI contract.** All three tools take `--help`, `--output json`,
    `--sample`, and return typed exit codes (0 / 2 warnings / 3 bad input /
    4 validation failure) instead of upstream's mixed conventions.

**Renderer replaced**

15. **Zero JavaScript.** Upstream embeds a 1,531-line prebuilt `@pierre/diffs`
    bundle (unreadable in review — exactly what this library's no-opaque-vendored-
    artifacts stance avoids) plus ~200 lines of canvas share-image code. Diffs are
    now colored with pure CSS spans, long ones collapse behind a native
    `<details>` toggle, and sharing is print-to-PDF via `@media print`.
16. **Vendor branding removed.** The Warp pixel-mark SVG, "warp factories" stamp,
    and the `warp.dev/factories` request-access CTA (upstream hardcodes it as the
    report's default `cta_url` and its SKILL.md ends every response with the
    link) are gone. The footer states the privacy contract instead.
17. **Theme + a11y.** `prefers-color-scheme` dark palette, `lang` attribute,
    viewport meta — upstream's page is fixed light-only.
18. **Renderer validates its input.** Missing `scores`/`stats`/`top_findings`/
    `suggestions` fields refuse with exit 3 and point to the aggregator, instead
    of upstream's KeyError traceback.

**Post-review hardening (added during PR review)**

21. **Repo-scoping transparency + `--strict-repo`.** Upstream's worktree/basename
    fallback silently treats any directory named like the repo as the repo — an
    unrelated project sharing a common name (`backend`, `app`) could leak its
    sessions into the run. Each session now records how it matched
    (`repo_match: "path" | "name"`), name-only matches are counted in
    `inventory.json` (`sessions_matched_by_name_only`) and called out in the
    collector's summary, and `--strict-repo` disables the fallback entirely.
22. **Bounded session reads.** Session files are read through a
    `MAX_FILE_BYTES` cap instead of upstream's slurp-then-truncate, so a
    pathological multi-hundred-MB JSONL never lands in memory whole.

**Docs & governance**

19. **References rewritten as cited canon.** Upstream ships one reference
    (`skill-improvements.md`, preserved here) with no sources. This plugin adds
    three references citing 7 sources each: the LLM-as-judge scoring canon, the
    session-mining privacy canon, and the expanded edit-governance doc that wires
    proposals into `engineering/write-a-skill`'s 6-item checklist.
20. **Cross-links into this repo's ecosystem** — routing table in the agent
    (skillopt-sleep for the automated nightly loop, write-a-skill for authoring,
    self-eval for grading the current session, plugin-audit for static checks).

## Install

Registered in `.claude-plugin/marketplace.json` as `skill-doctor`. From this
marketplace: `/plugin install skill-doctor@claude-code-skills`.

## Attribution

Upstream: [warpdotdev/common-skills](https://github.com/warpdotdev/common-skills)
`.agents/skills/skill-doctor/` at commit `f3b58c81d1cfd5d8eabf2e32edb32db2b0573923`,
MIT, © Denver Technologies, Inc. See `LICENSE` and the `attribution` record in
`.claude-plugin/authoring-notes.json`.
