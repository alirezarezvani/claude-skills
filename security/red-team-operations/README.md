# red-team-operations

**Level:** L3 (SOC/Red Team) | **Category:** Red Team | **Intent:** `read_only` (planning) + `mutating/remediation_action` (execution directives — require approval tokens)

Adversary simulation agent that translates approved campaign plans from `red-team-planner` into discrete operational steps across all seven Cyber Kill Chain phases. Manages OPSEC planning, C2 infrastructure design (with kill switch procedures), lateral movement path selection ranked by detection risk, exfiltration staging with volume caps, and pre-operation IOC management. Applies the strictest authorization controls in the system — every execution directive requires a valid human approval token and a MITRE ATT&CK technique ID.

**Authorization required:** A campaign plan from `red-team-planner` with `campaign_id`, `authorization_ref`, defined scope boundary, and completed RoE checklist. Any missing validation item returns a HALT notice.

---

## When to trigger

- Receives a validated campaign plan from `red-team-planner` with all required authorization fields
- Phase entry conditions are confirmed and human approval tokens are granted for that phase
- Never self-initiates — always campaign-driven

---

## Cyber Kill Chain phases covered

| Phase | Key decisions |
|---|---|
| Reconnaissance | OSINT methodology, passive vs. active split, infrastructure enumeration |
| Weaponization | Payload selection within OPSEC constraints |
| Delivery | Initial access technique ranked by detection risk |
| Exploitation | Hand-off to `safe-exploitation` agent with technique_ids and abort_conditions |
| Installation | Persistence mechanism selection (lowest artifact footprint) |
| C2 | Channel, protocol, beacon interval (60s floor + jitter), redirector topology, kill switch |
| Actions on Objectives | Lateral movement path (lowest-detection-risk-first), exfil staging with volume caps and rate limits |

---

## Key outputs

| Field | Type | Description |
|---|---|---|
| `phase_plan` | array | Per-phase: entry conditions, success criteria, abort conditions, handoff target |
| `opsec_plan` | object | Infrastructure requirements, tool selection, beacon intervals, IOC minimization |
| `c2_architecture` | object | Primary/backup channels, kill switch procedure |
| `lateral_movement_techniques` | array | MITRE ID, detection risk level (lowest first), prerequisites, expected artifacts |
| `exfil_staging` | object | Staging location, volume caps, transfer rate limits, encryption |
| `pre_op_ioc_list` | array | Network/host/behavioral indicators with detection tool mapping + cleanup checklist |

---

## OPSEC constraints enforced

- Minimum beacon interval: 60 seconds + jitter
- All C2 infrastructure: separate from production environments
- No in-scope system modification without explicit approval token
- Exfiltration volume capped per campaign plan
- Kill switch procedure documented before any phase begins

---

## Works with

**Upstream:** `red-team-planner` (campaign plan), `attack-path-analysis` (lateral movement path data)

**Downstream:**
- `safe-exploitation` — exploitation phase hand-off (receives targets, technique IDs, RoE ref, abort conditions)
- `attack-path-analysis` — lateral movement refinement (sends current position, target assets, available credentials)
- `findings-tracker` — real-time finding submission as findings are generated

---

## Standalone use (read-only planning mode)

```bash
cat red-team-operations/SKILL.md
# Paste into system prompt for operational planning:

{
  "event_type": "red_team_execution",
  "severity": "info",
  "raw_payload": {
    "campaign_id": "RT-2026-Q1-001",
    "authorization_ref": "PENTEST-AUTH-2026-001",
    "scope": "acme-corp.com and all subdomains",
    "out_of_scope": ["payments.acme-corp.com", "hr.acme-corp.com"],
    "roe_checklist_complete": true,
    "phase_requested": "c2_design",
    "objectives": ["demonstrate_lateral_movement", "reach_domain_controller"],
    "detection_tools_in_scope": ["CrowdStrike", "Splunk_SIEM"]
  }
}
```

---

## Runtime Contract

- ../../agents/red-team-operations.yaml
