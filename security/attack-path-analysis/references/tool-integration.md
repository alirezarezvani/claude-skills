# Tool Integration

| Tool | Integration Purpose | Data Flow Direction |
|---|---|---|
| BloodHound | AD path enumeration and graph data | Read — ingest BloodHound JSON export |
| Neo4j (BloodHound backend) | Graph query for path analysis | Read — Cypher queries for path traversal |
| Azure AD / Entra ID API | Cloud identity path data | Read — service principal and role data |
| AWS IAM Access Analyzer | IAM policy path enumeration | Read — policy reachability findings |
| MITRE ATT&CK Navigator | Technique ID validation per edge | Read — technique reference |
| Findings Tracker | Submit critical path findings | Write — path records as findings |
| red-team-planner | Receive campaign scope and return path analysis | Bidirectional — receive scope, return paths |
