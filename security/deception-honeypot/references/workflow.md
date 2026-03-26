# Deception & Honeypot Workflow

## Phase 1: Environment Assessment

1. Map network topology and identify high-value target zones
2. Identify current detection coverage gaps (where attacker could move undetected)
3. Assess existing SIEM/EDR integration points for deception alert ingestion

## Phase 2: Deception Asset Selection

1. Select honeypot types based on attacker objectives and environment topology
2. Choose canary token types based on data sensitivity and access patterns
3. Define lateral movement trap placement based on likely attack paths

## Phase 3: Deployment Planning

1. Define placement for each deception asset with network diagram
2. Configure alert logic: what interaction triggers what alert
3. Define SIEM integration for deception asset events
4. Set false positive handling: any interaction with deception assets = confirmed threat

## Phase 4: Monitoring Integration

1. Create SIEM detection rules for each deception asset type
2. Define escalation runbook for each alert type
3. Test alert pipeline with controlled interaction before production deployment

## Phase 5: Ongoing Management

1. Rotate canary tokens quarterly
2. Update honeypot services to match current technology stack
3. Review deception asset interaction logs weekly
