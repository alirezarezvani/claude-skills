# Tool Integration

| Tool | Integration Purpose | Data Flow Direction |
|---|---|---|
| Cobalt Strike (reference) | C2 architecture and beacon configuration planning | Read — technique reference only |
| Metasploit (reference) | Exploitation technique planning | Read — technique reference only |
| BloodHound (via attack-path-analysis) | AD lateral movement path data | Receive from attack-path-analysis |
| Mimikatz (reference) | Credential access technique planning | Read — technique reference only |
| MITRE ATT&CK Navigator | Technique mapping and coverage tracking | Read — technique ID validation |
| Findings Tracker | Real-time finding submission | Write — push findings as discovered |
| Orchestrator approval gate | Human approval token for execution phases | Read — wait for approval token |
