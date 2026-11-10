# cra-readiness

> The Cyber Resilience Act has two clocks. Article 14 reporting has applied
> since **11 September 2026** to every in-scope product on the EU market, old
> ones included. Everything else, CE marking included, applies from
> **11 December 2027**.

Four deterministic scripts for manufacturers, importers and open-source
stewards of software, firmware and connected devices sold in the EU:

| Script | Question it answers |
|---|---|
| `cra_scope_classifier.py` | Which products are in scope, which class (default, important I/II, critical), which conformity routes are open, is the support period long enough, which CSIRT gets our reports? |
| `art14_report_clock.py` | Is an early warning, notification or final report due, overdue or late right now? |
| `annex_i_gap_check.py` | Can we sign the EU declaration of conformity, or what blocks it? |
| `sbom_check.py` | Does our SBOM meet the Annex I Part II(1) floor? |

No network, no SRP connection, nothing submitted. Every rule cites the article
of Regulation (EU) 2024/2847 it implements, checked against the Official Journal
text, Implementing Regulation (EU) 2025/2392 and the Commission's July 2026
guidance (C(2026) 5252).

**Not legal advice and not a conformity assessment.** The manufacturer signs the
declaration; on routes B+C and H a notified body decides. Borderline product
categories can be read differently by a notified body or market surveillance
authority.

## Install

```bash
/plugin marketplace add alirezarezvani/claude-skills
/plugin install cra-readiness@claude-code-skills
```

## Use

```bash
/cs-cra-report events.csv                                   # a live vulnerability or incident
/cs-cra-readiness inventory.csv events.csv assessment.csv sbom.json   # full pass
```

Or run the scripts directly. Each has `--help`, `--sample` and `--output json`:

```bash
cd skills/cra-readiness
python scripts/cra_scope_classifier.py --sample
python scripts/art14_report_clock.py --sample
python scripts/annex_i_gap_check.py --sample
python scripts/sbom_check.py --sample
```

## What it refuses

- A class I product planned on module A while no harmonised standard is applied in full (Art 32(2)).
- A support period under five years for a product used for five or more (Art 13(8)).
- An assessment that skips any of the 39 Annex I/II/VII ids, or marks vulnerability handling not applicable.
- An event with no awareness time: the clock then runs from detection.

## Medical device makers

MDR and IVDR devices are excluded (Art 2(2)), but companion apps, gateways and
wellness wearables that are not themselves medical devices are not. The scope
classifier says which is which.

## License

MIT. See the repository LICENSE.
