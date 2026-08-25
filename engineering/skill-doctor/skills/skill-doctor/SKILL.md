---
name: skill-doctor
description: Use when the user wants their agent setup graded from real conversation history, asks which installed skills are actually working, or wants evidence-backed skill edits — scores recent local Claude Code / Codex sessions against efficiency and code-quality rubrics, then drafts skill changes gated by a deterministic aggregator and renders one local shareable report.
argument-hint: "[optional: --repo PATH, --days N, or a question about the setup]"
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "Rebuild of warpdotdev/common-skills skill-doctor (MIT): harvest → LLM-judges-with-rubrics → deterministic aggregation gate → self-contained HTML report"
  distinct_from: "skillopt-sleep (nightly automated replay loop with adopt gate; this is one interactive graded pass); write-a-skill (authors a skill from expertise; this improves skills from observed session evidence); self-eval (grades this session's own work; this grades a window of past sessions)"
---

# skill-doctor — grade the agent setup from real sessions

> **Privacy is the contract.** Everything runs locally. Transcripts are condensed,
> secret-redacted, chmod-0600, and never uploaded — the only shareable artifact is
> the report the user chooses to share.

Run from the repo being graded. Every artifact goes to one fresh scratch dir, never
into the repo:

```bash
RUN="$(mktemp -d "${TMPDIR:-/tmp}/skill-doctor-XXXXXXXX")"
python scripts/collect_sessions.py --out "$RUN"          # 1 — harvest + redact
```

**1 — Collect.** Scans Claude Code project-history JSONL and Codex rollouts,
discovers repo skills (`.claude/skills`, `.agents/skills`, `.codex/skills`, plugin
layouts), detects skill usage (`Skill` invocations, slash commands, SKILL.md paths), samples
newest-first, and writes redacted transcripts. Read `$RUN/inventory.json`: if
`sessions_sampled` is 0, tell the user there is nothing recent to score (suggest
`--days 90` or `--repo`) and stop. `skills_found` 0 is fine — the report becomes a
case for creating skills.

**2 — Score.** `python scripts/score_aggregator.py --inventory "$RUN/inventory.json"
--emit-template > "$RUN/session_scores.json"`. Read each transcript in
`$RUN/transcripts/` and judge it against **both** rubrics — `scorers/efficiency.md`
and `scorers/code-quality.md`. Fill the template with a **label from the rubric's
table** and a 1–3 sentence reason citing transcript specifics. Never invent numeric
scores — the aggregator derives them from labels. Use `insufficient_evidence` when
a transcript shows no judgeable diff. Also write 1–5 `top_findings`: the most
impactful cross-session patterns, concrete and specific.

**3 — Draft edits.** Follow `references/skill_edit_governance.md` (the filing bar:
would a competent agent with the current instructions still fail this way?). For
each suggestion that clears it, write the full improved SKILL.md to
`$RUN/proposed/<skill>/SKILL.md`, produce `diff -u <current> <proposed>`, and record
it in `$RUN/suggestions.json` citing the sampled session id(s) that motivated it.
Zero suggestions is a valid success — say why per finding. Never modify the user's
real skill files in this step.

**4 — Aggregate (the gate).** `python scripts/score_aggregator.py --inventory
"$RUN/inventory.json" --scores "$RUN/session_scores.json" --suggestions
"$RUN/suggestions.json"`. It validates labels against the rubric tables, refuses
scores for unsampled sessions, requires substantive reasons, rejects suggestions
that cite no scored session, computes `overall = 0.5·efficiency +
0.35·code_quality + 0.15·skill_coverage`, and writes `report.json`. **Exit 4 is a
stop**: fix what it names and re-run; never hand-edit report.json around it.

**5 — Render + tell.** `python scripts/render_report.py --report "$RUN/report.json"`
→ one self-contained `report.html` (no JS, no CDN, dark-mode + print-to-PDF). Then
tell the user the grade and the top findings in text, link
`file://$RUN/report.html`, and ask whether to apply the proposed diffs to their
real skills — apply only on an explicit yes, skill by skill.

## Hard rules

1. **Never upload transcripts, session files, or any excerpt.** Local only.
2. **Labels only, from the rubric tables.** The aggregator owns all arithmetic.
3. **Every suggestion traces to a scored session** — or it is dropped. Generic best practice is not evidence.
4. **Zero suggestions is a success**, not a failure to report around.
5. **Exit 4 from the aggregator is a stop**, not an error to swallow or bypass.
6. **Never touch the user's real skill files** without an explicit per-skill yes; proposed edits live under `$RUN/proposed/`.
7. **A proposed skill edit follows write-a-skill discipline** — trigger phrase in the description, smallest change that expresses the rule, replace over append.

## Scripts

| Script | Role | Exit codes |
|---|---|---|
| `scripts/collect_sessions.py` | Harvest Claude Code + Codex sessions, redact secrets, sample, inventory | 0 · 3 bad input |
| `scripts/score_aggregator.py` | Validate labels/reasons/suggestions, compute grade, emit report.json | 0 · 2 warnings · 3 bad input · 4 validation failure |
| `scripts/render_report.py` | report.json → single self-contained report.html | 0 · 3 bad input |

All support `--help`, `--output json`, and `--sample` (no real history needed).

## References and assets

- [`scorers/efficiency.md`](scorers/efficiency.md) · [`scorers/code-quality.md`](scorers/code-quality.md) — the two rubrics, preserved verbatim from upstream
- [`references/transcript_scoring_canon.md`](references/transcript_scoring_canon.md) — why rubric-anchored LLM judging works and where it fails (7 sources)
- [`references/session_mining_privacy.md`](references/session_mining_privacy.md) — the local-only contract, redaction pattern canon (7 sources)
- [`references/skill_edit_governance.md`](references/skill_edit_governance.md) — the filing bar for proposing skill edits (7 sources)
- [`assets/session_scores.example.json`](assets/session_scores.example.json) · [`assets/suggestions.example.json`](assets/suggestions.example.json) · [`assets/report.example.json`](assets/report.example.json) — the three handoff shapes
