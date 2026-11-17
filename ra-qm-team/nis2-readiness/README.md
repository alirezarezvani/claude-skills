# nis2-readiness

> NIS2 is entity law, not product law. Germany's NIS2UmsuCG has applied since
> **6 December 2025**: register with the BSI within three months, report
> significant incidents within **24 hours**.

Four deterministic scripts for companies in the 18 NIS2 sectors:

| Script | Question it answers |
|---|---|
| `nis2_scope_classifier.py` | Is each entity essential, important or out, which Member State supervises it, and must it register? |
| `nis2_incident_clock.py` | Is an incident significant, and is the early warning, notification or final report due, overdue or late? |
| `art21_gap_check.py` | What blocks the Article 21 baseline, measure by measure, with the 2024/2690 Annex section for digital providers? |
| `eu_cyber_regime_router.py` | For one company and one event, which of NIS2, DORA, CRA and GDPR apply, and which clocks run in parallel? |

No network, nothing submitted. Every rule cites Directive (EU) 2022/2555,
Implementing Regulation (EU) 2024/2690 or the BSIG 2025 section it implements.

**Not legal advice.** Member State transpositions differ, and the national
authority decides on designation and significance.

## Install

```bash
/plugin marketplace add alirezarezvani/claude-skills
/plugin install nis2-readiness@claude-code-skills
```

## Use

```bash
/cs-nis2-report incidents.csv                       # a live incident
/cs-eu-cyber-scope profile.json                     # one event, several laws
/cs-nis2-readiness entities.csv incidents.csv assessment.csv   # full pass
```

Or run the scripts directly. Each has `--help`, `--sample` and `--output json`:

```bash
cd skills/nis2-readiness
python scripts/nis2_scope_classifier.py --sample
python scripts/nis2_incident_clock.py --sample
python scripts/art21_gap_check.py --sample
python scripts/eu_cyber_regime_router.py --sample
```

## What it refuses

- An entity with no headcount or financials: size decides the category.
- An Article 21 assessment that skips any of the 30 ids, or marks a mandatory measure not applicable.
- An incident with no awareness time: the clock then runs from detection.

## Financial entities

DORA replaces NIS2 Articles 21 and 23 for them. Install `dora-readiness`.

## License

MIT. See the repository LICENSE.
