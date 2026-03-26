# Hunt Playbooks

## Playbook 1: Lateral Movement via WMI

Hypothesis: Attacker has established a foothold and is moving laterally using WMI remote execution, a technique commonly used to avoid spawning cmd.exe or PowerShell directly on the target.

Data sources required: EDR process creation events, Windows Security Event Log (4688).

Detection logic:
```
process_name = "wmiprvse.exe"
AND parent_process = "svchost.exe"
AND child_process NOT IN ["scrcons.exe"]  -- expected WMI children
AND child_process IN ["cmd.exe", "powershell.exe", "wscript.exe", "cscript.exe", "mshta.exe", "rundll32.exe"]
```

Triage steps:
1. Identify the initiating account that triggered the WMI call (Security Event 4688, 4648).
2. Determine the source host that made the remote WMI request (Security Event 4624 on target, logon type 3).
3. Map source host to user — is this expected admin activity?
4. Review the full command line argument of the spawned child process.
5. Check if the same pattern appears on multiple hosts within the same time window (indicates automated lateral movement).

Escalation trigger: Pattern on 3+ hosts within 60 minutes OR command line contains encoded payload or download cradle.

---

## Playbook 2: Living-Off-the-Land Binary Abuse

Hypothesis: Attacker is using trusted Windows binaries (LOLBins) to execute malicious code and evade detection by avoiding custom malware.

Detection logic:
```
process_name IN ["powershell.exe", "pwsh.exe"]
AND (
  command_line CONTAINS "-enc" OR
  command_line CONTAINS "-EncodedCommand" OR
  command_line CONTAINS "-nop" OR
  command_line CONTAINS "-NonInteractive" OR
  command_line CONTAINS "IEX" OR
  command_line CONTAINS "DownloadString" OR
  command_line CONTAINS "WebClient"
)
AND hour(timestamp) NOT IN [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]  -- outside business hours
AND parent_process NOT IN ["explorer.exe", "wmiprvse.exe"]  -- unexpected parent
```

After-hours threshold: Executions outside 07:00-17:00 local time increase base anomaly score by 2.

Decode encoded commands: Extract the base64 payload from `-EncodedCommand` argument and decode. Record decoded payload verbatim in the hunt evidence package.

---

## Playbook 3: Beaconing Detection

Hypothesis: A compromised host is communicating with a C2 server at regular intervals, a pattern that differs from human-driven browsing behavior.

Data sources: DNS query logs, proxy egress logs, firewall flow logs.

Statistical beaconing signature:
- Jitter less than 10% of mean interval (e.g., queries every 60 seconds +/- 3 seconds).
- Consistent small payload size per request (C2 keep-alive packets are typically small).
- Destination domain registered within the last 90 days (WHOIS lookup).
- Destination domain has no Alexa/Tranco top-1M entry.
- Communication continues across overnight and weekend hours (not human-driven).

Detection approach:
```
For each (source_ip, destination_domain) pair:
  intervals = [timestamps[i+1] - timestamps[i] for all i]
  jitter_coefficient = std(intervals) / mean(intervals)
  if jitter_coefficient < 0.1 AND count(intervals) > 20:
    flag as potential beacon
```

Escalation trigger: Confirmed beacon pattern to a domain less than 90 days old with no legitimate business purpose.

---

## Playbook 4: Pass-the-Hash Detection

Hypothesis: Attacker has harvested NTLM hashes from memory and is authenticating using the hash rather than the plaintext credential — no keyboard activity required on the originating workstation.

Data sources: Windows Security Event Log (4624, 4648), EDR, physical access / endpoint activity logs.

Detection logic:
```
Event 4624 on target host:
  LogonType = 3 (network logon)
  AuthenticationPackage = "NTLM"
  Source host = workstation (not a server or DC)

AND on source host at same timestamp:
  No keyboard or mouse activity for 10+ minutes (EDR idle indicator)
  No interactive user session (Event 4624 type 2 absent)
```

Triage steps:
1. Confirm the source workstation was locked or had no active user session at the time of the NTLM auth event.
2. Check if the authenticating account has recently been used on a host where Mimikatz or LSASS dumping tools have run (cross-reference with EDR behavioral alerts).
3. Verify the target resource being accessed — is it a high-value server (DC, file share, HRMS)?

---

## Dwell Time Estimation

Dwell time is the period between initial compromise and detection. Accurate dwell time estimation informs blast radius assessment and evidence collection scope.

Estimation method:
1. Identify the earliest observed malicious artifact (file write, process, network connection).
2. Scan backwards from that timestamp in all data sources for related indicators.
3. Check CloudTrail, authentication logs, and email logs for initial access vectors.
4. Cross-reference with threat actor infrastructure registration dates (WHOIS, Shodan).

Dwell time brackets and implications:

| Dwell Time | Blast Radius Assumption | Evidence Collection Scope |
|---|---|---|
| < 24 hours | Limited — likely early stage | 7-day lookback |
| 1-7 days | Moderate — reconnaissance complete | 30-day lookback |
| 7-30 days | High — lateral movement likely | 90-day lookback + backup media |
| > 30 days | Critical — full environment compromise assumed | Full historical + offline media |

Document dwell time estimate with confidence level (high / medium / low) and the earliest observed indicator that anchors the estimate.
