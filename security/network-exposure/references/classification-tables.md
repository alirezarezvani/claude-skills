# Network Exposure Classification Tables

## Port and Service Risk Classification

| Port | Service | Protocol | Risk Level | Notes |
|---|---|---|---|---|
| 22 | SSH | TCP | Medium | Acceptable if key-based auth enforced; High if password auth enabled |
| 23 | Telnet | TCP | Critical | Plaintext protocol — never acceptable on internet-facing systems |
| 25 | SMTP | TCP | Medium | Acceptable for mail servers; High if open relay |
| 53 | DNS | UDP/TCP | Medium | High if recursion enabled and internet-facing (open resolver) |
| 80 | HTTP | TCP | Medium | All production traffic should redirect to 443 |
| 443 | HTTPS | TCP | Low | Acceptable — verify TLS version and cipher suite |
| 445 | SMB | TCP | Critical | Never expose to internet; High if accessible from DMZ |
| 1433 | MSSQL | TCP | Critical | Database port must never be internet-facing |
| 1521 | Oracle DB | TCP | Critical | Database port must never be internet-facing |
| 2375 | Docker API (unauth) | TCP | Critical | Unauthenticated Docker API — immediate container escape risk |
| 2376 | Docker API (TLS) | TCP | High | Verify mutual TLS; escalate if certificate validation missing |
| 3306 | MySQL | TCP | Critical | Database port must never be internet-facing |
| 3389 | RDP | TCP | High | Never expose to internet; mandate NLA and MFA |
| 4444 | Metasploit default | TCP | Critical | Active exploitation indicator if observed listening |
| 5432 | PostgreSQL | TCP | Critical | Database port must never be internet-facing |
| 5900 | VNC | TCP | Critical | Plaintext remote access — immediately escalate |
| 6379 | Redis | TCP | Critical | No native auth in default config; never internet-facing |
| 8080 | HTTP Alt | TCP | High | Often admin interfaces — verify authentication |
| 8443 | HTTPS Alt | TCP | Medium | Verify TLS and authentication |
| 9200 | Elasticsearch | TCP | Critical | Default unauthenticated — never internet-facing |
| 9300 | Elasticsearch Cluster | TCP | Critical | Cluster transport — never internet-facing |
| 27017 | MongoDB | TCP | Critical | Default unauthenticated — never internet-facing |
| 50000 | Jenkins | TCP | Critical | Code execution capability — verify authentication |

## Firewall Rule Risk Classification

| Rule Pattern | Risk | Description |
|---|---|---|
| source=any, dest=any, port=any | Critical | Full any/any rule — complete bypass of segmentation |
| source=0.0.0.0/0, dest=internal, port=3389 | Critical | RDP exposed to internet |
| source=0.0.0.0/0, dest=internal, port=22 | High | SSH exposed to internet — acceptable only with bastion |
| source=0.0.0.0/0, dest=DB_subnet, port=any | Critical | Database subnet accessible from internet |
| source=DMZ, dest=internal_all, port=any | High | DMZ can reach all internal — segmentation failure |
| source=workstation_subnet, dest=DC, port=445/389 | Medium | Workstations accessing DC directly — lateral movement enabler |
| source=any, dest=admin_network, port=any | Critical | Admin network has unrestricted inbound |
| Implicit deny missing at rule set end | High | Missing default deny — misconfiguration risk |

## Network Segmentation Model

| Zone | Description | Allowed Inbound Sources | Allowed Outbound Destinations |
|---|---|---|---|
| Internet | Public internet | N/A | N/A |
| DMZ | Internet-facing services | Internet (specific ports) | App tier (specific ports only) |
| App Tier | Application servers | DMZ, internal users | DB tier (specific ports), external APIs |
| DB Tier | Database servers | App tier only | No internet, logging only |
| Admin Network | Jump servers, management | Internal auth users only | All internal zones (with MFA) |
| Workstation | End-user devices | Corporate network | Internet (filtered), App tier |
| OT/IoT | Operational technology | Isolated — monitored only | No internet, no corporate IT |

## Lateral Movement Enabler Classification

| Indicator | Risk | Description |
|---|---|---|
| SMB (445) accessible from workstations to servers | High | Pass-the-hash and ransomware propagation vector |
| LDAP (389) accessible from all workstations to DC | Medium | Acceptable for auth; High if LDAP signing disabled |
| WinRM (5985/5986) accessible laterally | High | PowerShell remoting lateral movement |
| RPC (135) accessible between all hosts | Medium | Required for Windows; restrict to necessary endpoints |
| SSH accessible between all Linux hosts | High | Credential-based lateral movement if keys shared |
| Kerberos (88) from non-DC hosts to internet | Critical | Potential AS-REP roasting or ticket exfiltration |
| DNS (53) TCP from internal hosts to external | High | DNS tunneling vector |
