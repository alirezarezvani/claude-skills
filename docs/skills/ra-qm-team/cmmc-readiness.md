---
title: "CMMC Readiness — Agent Skill for Compliance"
description: "Use when a defense contractor or subcontractor is preparing for a CMMC 2.0 Level 2 self-assessment or C3PAO assessment, calculating or checking an. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# CMMC Readiness

<div class="page-meta" markdown>
<span class="meta-badge">:material-shield-check-outline: Regulatory & Quality</span>
<span class="meta-badge">:material-identifier: `cmmc-readiness`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/ra-qm-team/skills/cmmc-readiness/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install ra-qm-skills</code>
</div>


> **Portability:** 3 stdlib scripts, no network, no SPRS connection. Fill CSVs, run, keep the output with the SSP.
> **Not an assessment and not legal advice.** A C3PAO or DIBCAC assessor decides MET; the Affirming Official affirms in SPRS.

Level 2 assessments fail in predictable ways: a 5-point gap someone planned to
put on a POA&M, an SSP that misses half the assets, a cloud drive holding CUI
without FedRAMP, and a Conditional status that quietly expires on day 181. Each
script catches one of these before the assessor does.

## Workflow

```bash
# 1 - Scope: what is in the assessment, and what must the SSP say about it?
python scripts/scope_classifier.py --inventory assets/inventory.example.csv
# 2 - Score: what is the SPRS score, and can we reach Conditional or Final status?
python scripts/sprs_score.py --assessment assets/assessment.example.csv --output json > score.json
# 3 - Closeout: is the POA&M complete, deferrable, and on time?
python scripts/poam_closeout.py --score score.json --poam assets/poam.example.csv \
  --conditional-date 2026-06-15 --as-of 2026-11-01
```

**Step 1** sorts every asset into the 32 CFR 170.19 categories (CUI, Security
Protection, Contractor Risk Managed, Specialized, Out-of-Scope) and blocks on
in-scope assets missing from the inventory or SSP, and on any cloud provider
holding CUI without FedRAMP Moderate or an equivalent body of evidence.

**Step 2** scores all 110 requirements (5, 3 or 1 point; partial credit only for
MFA and FIPS encryption; the SSP unscored but mandatory). It lists what must be
fixed before any assessment and what may go on a POA&M, and says how many points
short of 88 you would still be after fixing the blockers.

**Step 3** checks the POA&M against the score: every deferred gap has an item,
nothing ineligible is on it, every open item has an owner and a date before the
180-day deadline. It also prints the status calendar: closeout deadline, expiry,
and annual affirmation dates.

## The gates block on (exit 4)

1. CA.L2-3.12.4 not met: no current SSP means no assessment can finish.
2. A NOT MET requirement worth more than 1 point (except SC.L2-3.13.11 encrypted but not FIPS-validated).
3. A NOT MET AC.L2-3.1.20, AC.L2-3.1.22, PE.L2-3.10.3, 3.10.4 or 3.10.5: never deferrable.
4. A score under 88 after everything deferrable is deferred.
5. POA&M items still open after the 180-day closeout deadline, or an annual affirmation missed.
6. An in-scope asset missing from the SSP or inventory, or a CSP holding CUI without FedRAMP.

## Hard rules

- **Unassessed is not MET.** The score script refuses a file that does not list all 110 requirements.
- **Score against Rev 2.** 32 CFR 170 and DFARS class deviation 2024-O0013 keep Level 2 on NIST SP 800-171 Rev 2; plan Rev 3 in the SSP roadmap, not the POA&M.
- **NA needs a reason the assessor will accept.** An NA without one is reported.
- **A POA&M is not implementation.** Deferral buys 180 days, not a waiver.
- **Never affirm for anyone.** Name the Affirming Official; the scripts only prepare the evidence.

## Scripts

| Script | Role | Exit codes |
|---|---|---|
| `scripts/sprs_score.py` | 110-requirement score, Conditional/Final eligibility, fix-first list | 0 final · 2 conditional · 3 bad input · 4 not eligible |
| `scripts/poam_closeout.py` | POA&M vs score, deferral eligibility, owners, 180-day deadline, affirmation calendar | 0 ready · 2 open · 3 · 4 blocked/expired |
| `scripts/scope_classifier.py` | Asset inventory → 170.19 categories, SSP/inventory/diagram gaps, ESP and FedRAMP checks | 0 · 2 findings · 3 · 4 blocked |

All support `--help`, `--sample` and `--output json`.

## References and assets

- [`references/level2_scoring_and_status.md`](https://github.com/alirezarezvani/claude-skills/tree/main/ra-qm-team/skills/cmmc-readiness/references/level2_scoring_and_status.md) — phases, weights, POA&M rules, status, affirmations (8 sources)
- [`references/scoping_and_providers.md`](https://github.com/alirezarezvani/claude-skills/tree/main/ra-qm-team/skills/cmmc-readiness/references/scoping_and_providers.md) — asset categories, enclaves, ESPs and FedRAMP equivalency (6 sources)
- [`references/rev2_rev3_and_levels.md`](https://github.com/alirezarezvani/claude-skills/tree/main/ra-qm-team/skills/cmmc-readiness/references/rev2_rev3_and_levels.md) — why you score Rev 2, preparing for Rev 3, Levels 1 and 3 (7 sources)
- [`assets/assessment.example.csv`](https://github.com/alirezarezvani/claude-skills/tree/main/ra-qm-team/skills/cmmc-readiness/assets/assessment.example.csv), [`assets/poam.example.csv`](https://github.com/alirezarezvani/claude-skills/tree/main/ra-qm-team/skills/cmmc-readiness/assets/poam.example.csv), [`assets/inventory.example.csv`](https://github.com/alirezarezvani/claude-skills/tree/main/ra-qm-team/skills/cmmc-readiness/assets/inventory.example.csv) — input formats
- [`assets/assessment_readiness_signoff.md`](https://github.com/alirezarezvani/claude-skills/tree/main/ra-qm-team/skills/cmmc-readiness/assets/assessment_readiness_signoff.md) — readiness sign-off before booking the assessment
