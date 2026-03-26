# Immediate Triage: 0-2 Hours

The first two hours are the highest-leverage window for limiting blast radius. Execute all triage steps in parallel where possible.

## Step 1: Scope Assessment (0-30 minutes)

Identify every asset in the environment that runs the affected product and version:

1. Query CMDB for software by vendor, product, and version.
2. Query cloud asset inventory (AWS SSM Inventory, Azure Arc, GCP Asset Inventory).
3. Query EDR for running process version strings.
4. Query network scanners for externally reachable instances of the affected service.

Output: Asset inventory table with columns — hostname, IP, environment (prod/dev/test), internet-facing (Y/N), data classification of hosted data, business owner.

## Step 2: Exposure Scoring (30-60 minutes)

For each affected asset, compute an exposure score:

```
exposure_score = (internet_facing × 3) + (data_sensitivity × 2) + (patch_complexity × 1)
```

Prioritization tiers:

| Score | Tier | Action |
|---|---|---|
| >= 8 | Critical | Immediate compensating control; consider service isolation |
| 5-7 | High | Compensating control within 4 hours |
| 2-4 | Medium | Compensating control within 24 hours |
| < 2 | Low | Monitor; patch in next maintenance window |

## Step 3: Active Exploitation Evidence Check (60-120 minutes)

Search available telemetry for indicators of active exploitation targeting the organization:

- Review WAF logs for payloads matching the vulnerability's attack pattern.
- Review EDR for exploitation behaviors (process injection, reverse shell, unexpected child process of the affected service).
- Review SIEM for alerts correlated to the affected systems in the past 14 days.
- Query threat intelligence platform for targeting of the organization's IP ranges or domain.

If active exploitation is confirmed against the organization: immediately transition to the incident-commander agent. The zero-day-response agent remains active to coordinate compensating controls in parallel with incident response.
