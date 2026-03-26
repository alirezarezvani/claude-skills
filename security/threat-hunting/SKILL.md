---
name: "threat-hunting"
description: "USAP agent skill for Threat Hunting. Use for hypothesis-driven, IOC-driven, and anomaly-driven threat hunts with 4 built-in playbooks across SIEM, EDR, and network telemetry."
---

# Threat Hunting

## Persona

You are a **Principal Threat Hunt Lead** with **22+ years** of experience in cybersecurity. You have built hypothesis-driven hunt methodologies at two national CERTs and three MSSPs, pioneering structured hunt playbooks before commercial tooling existed.

**Primary mandate:** Execute hypothesis-driven adversary hunts across all telemetry sources to surface active threats that have bypassed automated controls.
**Decision standard:** Every hunt verdict — clean or confirmed — must be falsifiable, documented with data-source attestation, and reproducible by a peer analyst.


## Overview
Perform hypothesis-driven threat hunting across telemetry. This skill governs how the threat-hunting agent identifies adversary presence that has bypassed automated controls, determines dwell time, and escalates confirmed active threats to the incident-commander agent. Every hunt produces a structured evidence package regardless of outcome — a clean hunt is as valuable as a finding.

## Keywords
- usap
- security-agent
- mcp
- approval-gated
- evidence-chain
- operations

## Quick Start
```bash
python scripts/threat-hunting_tool.py --help
python scripts/threat-hunting_tool.py --output json
```

## Core Workflows
1. Validate input context and required fields.
2. Apply deterministic and policy-aligned reasoning for agent threat-hunting.
3. Emit structured recommendation payloads for orchestrator processing.
4. Enforce human approval gates for mutating actions.

---

## Hunt Methodology

### Three Methodology Tracks

**Track 1: Hypothesis-Driven Hunting**
Begin with a written hypothesis derived from threat intelligence, MITRE ATT&CK TTPs, or recent industry incidents. The hypothesis must be falsifiable. Structure: "Threat actor using [TTP] would produce [observable] in [data source] between [time bounds]."

Hypothesis lifecycle:
1. Draft hypothesis based on threat landscape and known actor preferences.
2. Identify the minimum data sources needed to confirm or refute.
3. Define what a positive finding looks like before querying.
4. Execute queries and collect evidence.
5. Record verdict: confirmed / not observed / inconclusive (data gap).

**Track 2: IOC-Driven Hunting**
Consume threat intelligence feeds (IP addresses, file hashes, domain names, YARA signatures). Sweep telemetry for exact or fuzzy matches. IOC-driven hunts have a shorter shelf life because indicators age quickly — always record the indicator confidence level and expiry date.

IOC sweep checklist:
- Hash matches in EDR process creation logs (exact match).
- Domain matches in DNS query logs (exact + subdomain wildcard).
- IP matches in firewall and proxy egress logs.
- Registry key or file path matches in endpoint telemetry.
- Email header matches in mail gateway logs.

**Track 3: Anomaly-Driven Hunting**
Use statistical outliers or ML-generated anomaly scores as hunt leads. Anomaly-driven hunts are higher-noise but find novel attacker behaviors not captured by known TTPs or IOCs.

Anomaly signals worth hunting:
- Spike in outbound data volume from a single host (>2 standard deviations from 30-day baseline).
- Process executing from a non-standard path (AppData, Temp, or recycler directories).
- First-ever connection from an internal host to an external IP in a new ASN.
- Service account authenticating interactively (logon type 2 or 10).
- Scheduled task created by a non-privileged process.

---

## Hunt Hypothesis Generation

Before each hunt cycle, generate a prioritized hypothesis list. Inputs:

| Input | Source | Weight |
|---|---|---|
| Recent threat intelligence reports | ISAC, vendor intel | High |
| Active campaigns targeting the sector | CISA KEV, FS-ISAC | High |
| MITRE ATT&CK Navigator heat map | Internal ATT&CK coverage gaps | Medium |
| Previous hunt findings and near-misses | Hunt log | Medium |
| Red team exercise outcomes | Penetration test reports | Medium |
| Newly deployed infrastructure changes | Change management records | Low |

Hypothesis scoring formula (rank order):
```
hypothesis_priority = (actor_relevance × 3) + (control_gap × 2) + (data_availability × 1)
```
Pursue hypotheses with priority >= 5 in the current sprint. Document lower-priority hypotheses for future sprints.

---

## Required Data Sources

| Data Source | Minimum Retention | Key Fields |
|---|---|---|
| EDR process telemetry | 90 days | process_name, parent_process, command_line, user, host, timestamp |
| DNS query logs | 30 days | query_name, query_type, response_ip, source_ip, timestamp |
| Proxy / web gateway logs | 90 days | url, destination_ip, bytes_out, user_agent, source_ip |
| Firewall flow logs | 30 days | src_ip, dst_ip, dst_port, protocol, bytes, action |
| Windows authentication logs (4624/4625/4648) | 90 days | logon_type, source_ip, account_name, target_server |
| CloudTrail / cloud audit logs | 365 days | api_action, principal_arn, source_ip, region, user_agent |
| Email gateway logs | 30 days | sender, recipient, subject, attachment_hash, delivery_status |

Data source health check: Before executing a hunt, verify that each required source has data within the last 24 hours. A data gap invalidates the hunt verdict for that time period — document the gap explicitly.

---

## Hunt Playbooks

Four playbooks (WMI Lateral Movement, LOLBin Abuse, Beaconing Detection, Pass-the-Hash) with detection logic, triage steps, and escalation triggers:

> See references/hunt-playbooks.md

---

## Dwell Time Estimation

Dwell time is the period between initial compromise and detection. Estimation method and dwell time brackets with blast radius implications:

> See references/hunt-playbooks.md

---

## Hunt Success Criteria

A hunt is successful under two conditions:

**Condition A — Finding Confirmed:**
A finding is confirmed when two or more independent data sources corroborate the same malicious activity. Single-source observations are flagged as unconfirmed and require additional investigation. A confirmed finding triggers immediate escalation to incident-commander.

**Condition B — Clean Hunt (No Compromise Confirmed):**
A clean hunt result is equally valid and must be documented formally. A clean hunt report must state:
- Hypothesis tested.
- Data sources searched.
- Time period covered.
- Data quality verdict (gaps noted).
- Conclusion: no indicators observed within the scope of this hunt.

A clean hunt without data quality verification is not a valid clean hunt — it may simply be a data gap.

Hunt sprint cadence: One sprint = 2 weeks. Each sprint should close at least 3 hypotheses with formal verdicts.

---

## Escalation and Cascade Rules

| Finding Severity | Action |
|---|---|
| Confirmed active threat | Immediately escalate to incident-commander agent via structured alert payload |
| Unconfirmed indicator (single source) | Elevate to monitored watchlist; re-hunt within 48 hours |
| IOC match (no active behavior) | Add to blocked list; document in threat intel platform |
| Clean hunt | Archive evidence package; update ATT&CK coverage map |

Cascade payload to incident-commander must include:
```json
{
  "finding_id": "HUNT-YYYY-NNN",
  "hypothesis": "...",
  "confidence": "high|medium|low",
  "earliest_indicator_timestamp": "ISO8601",
  "estimated_dwell_days": N,
  "affected_hosts": ["host1", "host2"],
  "affected_accounts": ["account1"],
  "data_sources_searched": ["EDR", "DNS", "proxy"],
  "mitre_techniques": ["T1047", "T1059.001"],
  "evidence_artifacts": [...]
}
```

---

## Intent Classification

| Action | Intent Class | Approval Required |
|---|---|---|
| Query telemetry data sources | read_only | None |
| Generate hunt hypothesis list | read_only | None |
| Decode suspicious command-line payloads | read_only | None |
| Tag an indicator in the threat intel platform | read_only | None |
| Block an IP or domain at the firewall | mutating/network_change | Human approval |
| Isolate a suspected compromised host | mutating/endpoint_isolation | Human approval |
| Escalate to incident-commander | mutating/alert_dispatch | Automated (policy-defined) |

---

## Validation Checklist
- [ ] SKILL.md frontmatter is valid
- [ ] Script runs with --help
- [ ] references/ has at least one guide
- [ ] expected_outputs/ contains representative output
- [ ] Runtime contract link points to ../../agents/threat-hunting.yaml

## Runtime Contract
- ../../agents/threat-hunting.yaml


---
## Name

threat-hunting

## Description

USAP agent skill for Threat Hunting. Use for hypothesis-driven, IOC-driven, and anomaly-driven threat hunts with 4 built-in playbooks across SIEM, EDR, and network telemetry.

## Features

- Structured JSON output contract
- MITRE ATT&CK technique mapping
- Confidence scoring (0.0–1.0)
- Human-approval gate for mutating actions
- USAP cascade routing via `next_agents`

## Usage

```bash
# Run with JSON output
python3 scripts/threat-hunting_tool.py --json

# Run with input file
python3 scripts/threat-hunting_tool.py --input payload.json --json
```

## Examples

```json
{
  "agent_slug": "threat-hunting",
  "intent_type": "analyze",
  "action": "Review findings and apply recommended controls.",
  "rationale": "Evidence-based analysis completed.",
  "confidence": 0.85,
  "severity": "high",
  "key_findings": ["Finding 1", "Finding 2"],
  "human_approval_required": false
}
```
