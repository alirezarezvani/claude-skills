---
description: Grade the agent setup from real local session history — rubric-scored, evidence-gated, rendered as one local shareable report.
argument-hint: "[optional: --repo PATH | --days N | --harness claude|codex | a question about the setup]"
---

# /cs:skill-doctor

Run the skill-doctor pass with `$ARGUMENTS` (pass any `--repo`, `--days`,
`--harness`, `--include-subagents` flags through to the collector).

Load `engineering/skill-doctor/skills/skill-doctor/SKILL.md` and follow it
exactly. Summary of the contract:

## Pre-flight

1. **Confirm the target repo** — the report is scoped to one repo's skills and
   the sessions that ran inside it. Run from that repo or pass `--repo`.
2. **State the privacy contract up front**: everything runs locally, transcripts
   are redacted before they touch disk, nothing is uploaded.
3. Create the scratch dir: `RUN="$(mktemp -d "${TMPDIR:-/tmp}/skill-doctor-XXXXXXXX")"`.

## Pipeline

```bash
python engineering/skill-doctor/skills/skill-doctor/scripts/collect_sessions.py --out "$RUN" $ARGUMENTS
python engineering/skill-doctor/skills/skill-doctor/scripts/score_aggregator.py --inventory "$RUN/inventory.json" --emit-template > "$RUN/session_scores.json"
# ... judge each transcript against scorers/, fill the template, draft suggestions ...
python engineering/skill-doctor/skills/skill-doctor/scripts/score_aggregator.py --inventory "$RUN/inventory.json" --scores "$RUN/session_scores.json" --suggestions "$RUN/suggestions.json"
python engineering/skill-doctor/skills/skill-doctor/scripts/render_report.py --report "$RUN/report.json"
```

If `sessions_sampled` is 0, stop and tell the user (suggest `--days 90`). If the
aggregator exits 4, fix what it names and re-run — never bypass it. Report every
non-zero exit code as a finding, not an error to swallow.

## Output

Tell the user, in text: the letter grade, the three top findings, how many
secrets were redacted, and the suggestion count (zero is a valid success — say
why per finding). Then link the local report:

- Your quality report: `file://$RUN/report.html` (print to PDF to share)

Finally ask: **"Want me to apply any of these proposed diffs to your real
skills?"** — and apply only on an explicit per-skill yes.
