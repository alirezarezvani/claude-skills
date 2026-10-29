---
title: "Access Lifecycle — Agent Skill for Compliance"
description: "Use when preparing or running a user access review, checking that leavers lost their access, finding orphaned or ownerless service accounts. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Access Lifecycle

<div class="page-meta" markdown>
<span class="meta-badge">:material-shield-check-outline: Regulatory & Quality</span>
<span class="meta-badge">:material-identifier: `access-lifecycle`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/ra-qm-team/skills/access-lifecycle/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install ra-qm-skills</code>
</div>


> **Portability:** 3 stdlib scripts, no network, no IdP or HR connection. Export CSV, run, keep the output as evidence.
> **Not audit advice.** Periods and thresholds are your policy; the scripts make you state them.

Access reviews fail audits in four ordinary ways: the review ran on an incomplete
export, someone approved their own access, a revoke was decided and never
carried out, and leavers kept working accounts nobody looked at. Each script
catches one class of these before the auditor does.

## Workflow

```bash
# 1 - Diff: who has access that the HR roster says they should not?
python scripts/access_diff.py --roster hr_roster.csv --accounts accounts.csv \
  --inactive-days 90 --privileged-review-days 90 --as-of 2026-10-31
# 2 - Campaign: did the review cover everything, and did the revokes happen?
python scripts/access_review_campaign.py --decisions campaign.csv --population accounts.csv \
  --remediation-days 10 --close-date 2026-10-20
# 3 - Map: which controls do the exceptions break, and what evidence do you keep?
python scripts/control_evidence_mapper.py --diff diff.json --campaign campaign.json --framework soc2,iso27001
```

**Step 1** joins each account to the roster on employee ID, then email. A
terminated person with an enabled account is a blocker; one who logged in after
their exit date is a worse one. Accounts that match nobody are orphans; service
accounts need a named owner. Inactivity and privileged-review age use your periods.

**Step 2** checks the campaign against the export it was built from. An enabled
account missing from the campaign means the review did not cover the population,
whatever the sign-off sheet says. It also catches undecided lines, self-review,
revokes not removed inside your window, late decisions, and a reviewer who kept
every line of a large batch at machine speed.

**Step 3** turns findings into a per-control table: FAIL, EXCEPTIONS,
NO_EXCEPTIONS, PARTLY_TESTED, NOT_TESTED or NOT_COVERED, each with what an
auditor tests and the evidence to keep. There is no PASS.

## The gates block on (exit 4)

1. A leaver with an enabled account, or any login after the exit date.
2. A privileged orphan account, or a privileged service account with no owner.
3. An enabled account the campaign never reviewed.
4. An undecided line, a self-review, or a decision with no reviewer named.
5. A revoke or modify with no removal recorded past your remediation window.

## Hard rules

- **Periods are policy.** `--inactive-days` and `--remediation-days` have no default. PCI DSS 8.2.6 says 90 days; your policy may differ.
- **Prove removals by re-export.** A closed ticket is not evidence the access is gone.
- **The export is evidence too.** Keep the query, the pull time and the row count (PCAOB AS 1105.10).
- **A rubber-stamp flag is a signal, not proof.** Ask the reviewer what they checked; do not call it fraud.
- **No PASS from a script.** Operating effectiveness is the auditor's conclusion.

## Scripts

| Script | Role | Exit codes |
|---|---|---|
| `scripts/access_diff.py` | Roster vs account export: leavers, orphans, ownerless service accounts, movers, privileged review age, inactivity | 0 clean · 2 findings · 3 bad input · 4 blocked |
| `scripts/access_review_campaign.py` | Population coverage, undecided, self-review, unremoved revokes, late decisions, rubber-stamp signal | 0 · 2 · 3 · 4 incomplete |
| `scripts/control_evidence_mapper.py` | Findings → per-control status for ISO 27001, SOC 2, NIST 800-53, PCI DSS, HIPAA, SOX IPE | 0 · 2 exceptions · 3 · 4 fail |

All support `--help`, `--sample` and `--output json`.

## References and assets

- [`references/joiner_mover_leaver_standards.md`](https://github.com/alirezarezvani/claude-skills/tree/main/ra-qm-team/skills/access-lifecycle/references/joiner_mover_leaver_standards.md) — what each framework requires for provisioning, change and removal (7 sources)
- [`references/access_review_campaigns.md`](https://github.com/alirezarezvani/claude-skills/tree/main/ra-qm-team/skills/access-lifecycle/references/access_review_campaigns.md) — population, reviewers, cadence, remediation, what auditors reject (6 sources)
- [`references/control_crosswalk.md`](https://github.com/alirezarezvani/claude-skills/tree/main/ra-qm-team/skills/access-lifecycle/references/control_crosswalk.md) — finding codes to controls across six frameworks, with the caveats (7 sources)
- [`assets/hr_roster.example.csv`](https://github.com/alirezarezvani/claude-skills/tree/main/ra-qm-team/skills/access-lifecycle/assets/hr_roster.example.csv), [`assets/accounts.example.csv`](https://github.com/alirezarezvani/claude-skills/tree/main/ra-qm-team/skills/access-lifecycle/assets/accounts.example.csv), [`assets/campaign.example.csv`](https://github.com/alirezarezvani/claude-skills/tree/main/ra-qm-team/skills/access-lifecycle/assets/campaign.example.csv) — input formats
- [`assets/access_review_signoff.md`](https://github.com/alirezarezvani/claude-skills/tree/main/ra-qm-team/skills/access-lifecycle/assets/access_review_signoff.md) — campaign sign-off with the evidence fields a reviewer fills in
