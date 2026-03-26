# threat-hunting

**Level:** L3 (SOC) | **Category:** Detection | **Intent:** `read_only` (analysis) + `mutating/network_change` (block actions)

Performs hypothesis-driven, IOC-driven, and anomaly-driven threat hunting across endpoint, network, and cloud telemetry. Generates falsifiable hunt hypotheses, executes structured hunt playbooks, estimates attacker dwell time, and escalates confirmed active threats to incident-commander. Every hunt produces a formal evidence package — including clean hunts.

---

## When to trigger

- Scheduled hunt sprint (every 2 weeks minimum)
- Threat intelligence report describing a TTP targeting your sector
- CISA KEV entry relevant to your technology stack
- Red team exercise identified a detection gap
- Post-incident request to hunt for related activity beyond the known scope
- Anomaly score spike from behavioral-analytics or telemetry-signal-quality

---

## Key outputs

| Field | Type | Description |
|---|---|---|
| `action` | string | `escalate_to_incident_commander`, `add_to_watchlist`, `block_indicator`, `archive_clean_hunt` |
| `intent_type` | string | `read_only` (analysis) or `mutating/network_change` (blocking) |
| `confidence` | string | `high`, `medium`, `low` |
| `key_findings` | array | Hunt hypothesis verdict, techniques matched, earliest indicator timestamp |
| `mitre_techniques` | array | ATT&CK technique IDs (e.g. `T1047`, `T1059.001`) |
| `estimated_dwell_days` | int | Estimated attacker dwell time |

---

## Hunt playbooks built in

| Playbook | Hypothesis | Key signals |
|---|---|---|
| WMI Lateral Movement | Attacker using WMI remote exec to avoid PowerShell spawning | `wmiprvse.exe` spawning `cmd.exe`, logon type 3 |
| Living-Off-the-Land Binary Abuse | Attacker using trusted binaries (LOLBins) with encoded payloads | PowerShell `-enc`, `IEX`, `DownloadString`, after-hours execution |
| Beaconing Detection | Compromised host communicating with C2 at regular intervals | Jitter coefficient < 0.10, small consistent payload, new domain |
| Pass-the-Hash | Attacker using NTLM hash from a workstation with no active user session | NTLM logon type 3 + idle source workstation |

---

## Dwell time brackets

| Dwell time | Evidence scope required |
|---|---|
| < 24 hours | 7-day lookback |
| 1-7 days | 30-day lookback |
| 7-30 days | 90-day lookback + backup media |
| > 30 days | Full historical — assume full environment compromise |

---

## Works with

**Upstream:** `telemetry-signal-quality` (data source health), `threat-intelligence` (IOC feeds), `behavioral-analytics` (anomaly leads)

**Downstream:** `incident-commander` (confirmed active threats escalated with structured payload), `findings-tracker` (clean hunt archives), `detection-engineering` (detection gaps identified)

---

## Standalone use

```bash
cat threat-hunting/SKILL.md
# Paste into system prompt, then send a hunt request:

{
  "event_type": "hunt_request",
  "severity": "medium",
  "raw_payload": {
    "trigger": "CISA KEV — CVE-2024-XXXX exploitation observed in the wild",
    "sector": "financial_services",
    "data_sources_available": ["EDR", "DNS", "CloudTrail", "proxy"],
    "lookback_days": 30
  }
}
```

---

## Runtime Contract

- ../../agents/threat-hunting.yaml
