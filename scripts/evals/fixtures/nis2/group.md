# Nordheim group (all entities established in Germany only)

| Entity | Activity | Employees | Turnover | Balance sheet | Notes |
|---|---|---|---|---|---|
| Stadtwerke Nordheim GmbH | Drinking water supply and distribution | 180 | EUR 42m | EUR 60m | independent from the other two entities for size purposes |
| Nordheim Cloud GmbH | Cloud computing (IaaS) for local businesses | 40 | EUR 8m | EUR 5m | independent |
| Nordheim DNS Services GmbH | Authoritative and recursive DNS for 900 domains | 12 | EUR 2m | EUR 1m | independent |

None of the entities has registered with the BSI yet.

## Incident

Ransomware encrypted the Stadtwerke billing system and the SCADA historian.
Our SOC detected unusual encryption activity on 2026-11-16 at 22:10 CET.
At 2026-11-17 06:30 CET the incident team confirmed it was a ransomware attack
that stopped billing and degraded remote monitoring of two pumping stations.
The billing system holds names, addresses and bank details of 38,000 customers.
Water supply itself has not been interrupted so far.
