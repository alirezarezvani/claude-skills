# NIS2 significant incident runbook

Fill the standing part once; copy the per-incident part for each incident.
Deadlines: Directive (EU) 2022/2555 Art 23(4); Germany BSIG §32.

## Standing set-up

| Item | Value |
|---|---|
| Category (essential / important) and Member State of jurisdiction (Art 26) | |
| CSIRT or authority and reporting channel (Germany: BSI portal) | |
| Registration done? date and reference (Art 27; BSIG §33) | |
| Digital provider under 2024/2690? (DNS, TLD, cloud, DC, CDN, MSP, MSSP, marketplace, search, social, trust) | |
| Also under DORA, CRA or GDPR? (run `eu_cyber_regime_router.py`) | |
| Who decides significance (name, deputy) | |
| Who submits (name, deputy) | |
| Who informs recipients of the service (Art 23(1)) | |

## Per incident

| Step | Time (with offset) | Who | Note |
|---|---|---|---|
| Detected | | | |
| Aware (significant incident with reasonable certainty) | | | starts all clocks |
| Significance decided | | | criteria met (Art 23(3) or 2024/2690 Art 3) |
| Early warning sent | | | due aware + 24 h; malicious? cross-border? |
| Recipients informed | | | without undue delay |
| Notification sent | | | due aware + 72 h (24 h trust services) |
| Intermediate report (if requested) | | | |
| Final or progress report sent | | | due notification + 1 month |
| Handling concluded | | | final due 1 month after, if a progress report was sent |

Then run:

```bash
python scripts/nis2_incident_clock.py --incidents incidents.csv
```
