# DORA major ICT incident runbook

Fill the standing part once; copy the per-incident part for each incident.
Keep it with the incident record. Deadlines: Delegated Regulation (EU) 2025/301 Art 5.

## Standing set-up

| Item | Value |
|---|---|
| Competent authority and submission channel | |
| Entity kind for Art 5(5) (credit institution / CCP / trading venue / NIS2-identified / other) | |
| Copy to NIS2 CSIRT required by our Member State? (DORA Art 19(1)) | |
| Bank holidays file for `--holidays` | |
| Who classifies (name, deputy) | |
| Who submits (name, deputy) | |
| Who informs clients (DORA Art 19(3)) | |
| Register of critical or important functions (DORA Art 3(22)) | |

## Per incident

| Step | Time (with offset) | Who | Note |
|---|---|---|---|
| Detected | | | |
| Aware | | | starts the 24 h ceiling |
| Classified major | | | starts the 4 h clock; attach the criteria met |
| Initial notification sent | | | due min(classified + 4 h, aware + 24 h) |
| Clients informed | | | if financial interests affected |
| Intermediate report sent | | | due initial + 72 h |
| Regular activities recovered | | | send an updated intermediate report |
| Final report sent | | | due last intermediate + 1 month |
| Authority told of a delay (Art 5(3)) | | | before the deadline, with reasons |

Then run:

```bash
python scripts/dora_incident_classifier.py --incidents incidents.csv --entity <kind> --holidays 2026-12-25,2026-12-26
```
