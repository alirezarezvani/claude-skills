# dora-readiness

> DORA has applied since **17 January 2025**. Supervisors first ask for two
> things: the register of information and major-incident reports, the first
> due **4 hours** after you classify the incident as major.

Three deterministic scripts for EU financial entities:

| Script | Question it answers |
|---|---|
| `dora_scope_check.py` | Full regime, simplified framework (Art 16), excluded, or ICT provider? NIS2 overlap, critical provider oversight? |
| `dora_incident_classifier.py` | Is an ICT incident major under RTS 2024/1772, are recurring incidents major together, and is a report due, overdue or late under RTS 2025/301? |
| `register_of_information_check.py` | Does every ICT contract carry the Article 30 terms, does every critical function have an exit plan, and where is concentration risk? |

No network, nothing submitted. Every rule cites Regulation (EU) 2022/2554 or
the delegated or implementing regulation it implements.

**Not legal advice.** The competent authority supervises; contract wording
goes to counsel. This is the Digital Operational Resilience Act, not DevOps
DORA metrics.

## Install

```bash
/plugin marketplace add alirezarezvani/claude-skills
/plugin install dora-readiness@claude-code-skills
```

## Use

```bash
/cs-dora-incident incidents.csv                              # a live ICT incident
/cs-dora-readiness entities.csv incidents.csv register.csv   # full pass
```

Or run the scripts directly. Each has `--help`, `--sample` and `--output json`:

```bash
cd skills/dora-readiness
python scripts/dora_scope_check.py --sample
python scripts/dora_incident_classifier.py --sample
python scripts/register_of_information_check.py --sample
```

## What it refuses

- An entity type DORA does not list.
- A contract for a critical or important function without the Art 30(3) terms or an exit plan.
- A contract nobody assessed for criticality.

## Non-financial entities

Install `nis2-readiness`; it also routes one event across NIS2, DORA, CRA and GDPR.

## License

MIT. See the repository LICENSE.
