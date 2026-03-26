# Tool Integration

| Tool | Integration Purpose | Data Flow Direction |
|---|---|---|
| MITRE ATT&CK Navigator | Technique selection and heatmap generation | Read — import technique IDs |
| PTES Framework Reference | Phase-by-phase planning structure | Read — structural template |
| BloodHound (via attack-path-analysis) | AD path enumeration feeding campaign design | Receive from attack-path-analysis |
| Scope management system | Authorization boundary enforcement | Read — validate IP/domain scope |
| Ticketing integration (via findings-tracker) | Campaign findings tracking | Write — push campaign ID to tracker |
| Orchestrator approval gate | Human approval for cascade directives | Read — wait for approval token |
