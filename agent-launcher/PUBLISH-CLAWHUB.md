# ClawHub publish plan — agent-launcher (6 skills)

Prepared 2026-08-24. Live publish requires the maintainer's ClawHub credentials +
drip timer, which do not exist in remote sessions — run this from the maintainer
machine.

## What to publish

Six skills from `agent-launcher/skills/`, version **2.11.2** (matches
`plugin.json` per the repo's "version follows repo versioning" rule — bump all
together at the next release cut):

| Order | Skill folder | Preferred slug | Fallback (only if slug taken) |
|---|---|---|---|
| 1 | `agent-launcher-orchestrator` | `agent-launcher-orchestrator` | `cs-agent-launcher-orchestrator` |
| 2 | `stage-launch` | `stage-launch` | `cs-stage-launch` |
| 3 | `grade-iterate` | `grade-iterate` | `cs-grade-iterate` |
| 4 | `run-without-you` | `run-without-you` | `cs-run-without-you` |
| 5 | `interview` | *likely taken* → `cs-interview` | `cs-agent-interview` |
| 6 | `wrap-up` | *likely taken* → `cs-wrap-up` | `cs-agent-wrap-up` |

`interview` and `wrap-up` are generic slugs — expect conflicts (upstream
`anthropics/launch-your-agent` itself ships a `wrap-up` skill). Per the repo
rule, the `cs-` prefix applies **only on the ClawHub registry**; never rename the
repo folders.

## Constraints (from root CLAUDE.md)

- **Rate limit: 5 new skills/hour** → publish 1–5 in the first batch, 6 after the
  window (or let `clawhub-drip.timer` pace all 6).
- **No paid dependencies:** satisfied — all 18 tools are stdlib-only; live CMA
  calls are BYOK curl the user runs.
- Version must match the repo release version.

## Pre-publish checklist

- [ ] `python3 scripts/derive_counters.py --check` green
- [ ] All 6 SKILL.md frontmatter `version:` fields match `plugin.json`
- [ ] `for f in agent-launcher/skills/*/scripts/*.py; do python3 "$f" --help >/dev/null; done` exits clean
- [ ] Attribution intact: `plugin.json` `attribution` block names
      `anthropics/launch-your-agent` (Apache-2.0)
- [ ] Strip the repo-only `source`/`attribution` extension fields at publish time
      if the stripping pipeline is active
