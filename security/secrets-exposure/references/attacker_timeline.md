# Attacker Timeline Reference — Secrets Exposure

## Purpose

This reference gives concrete attacker behavior timelines for each secret type.
Use these when composing rationale and urgency justification in findings.
The timelines are based on real-world incident data and threat intelligence reports.

---

## AWS Access Key (full_account blast radius)

**Source**: GitGuardian research, AWS security incident reports, Palo Alto Unit42

| Time | Attacker Action | API Call / TTP | MITRE |
|---|---|---|---|
| T+0s | Key appears in commit or paste site | — | — |
| T+60s | Automated bot detects key | GitHub API polling, GitLab webhooks | T1530 |
| T+2m | Attacker validates key | `sts:GetCallerIdentity` | T1552.005 |
| T+3m | Enumerates account identity | `iam:GetUser`, `iam:GetAccountSummary` | T1087.004 |
| T+5m | Maps accessible services | `s3:ListAllMyBuckets`, `ec2:DescribeInstances`, `iam:ListUsers` | T1619 |
| T+8m | Identifies high-value targets | `iam:ListPolicies`, `iam:ListAttachedRolePolicies` | T1087.004 |
| T+10m | Creates backdoor user | `iam:CreateUser`, `iam:CreateAccessKey`, `iam:AttachUserPolicy` | T1098.001 |
| T+15m | Starts data exfiltration | `s3:GetObject` (all buckets), `secretsmanager:GetSecretValue` | T1530 |
| T+20m | Checks for CloudTrail | `cloudtrail:DescribeTrails`, `cloudtrail:GetTrailStatus` | T1526 |
| T+25m | Disables logging | `cloudtrail:StopLogging` or `cloudtrail:DeleteTrail` | T1562.008 |
| T+30m | Deploys crypto miner | `ec2:RunInstances` (GPU instances, high cost) | T1496 |
| T+45m | Completes bulk data export | `s3:GetObject` via sync tools | T1530 |
| T+2h | Account may be useless to legitimate owner | Billing spike, resource deletion | T1485 |
| T+24h | Incident discovered (average detection time) | SIEM alert, billing notification | — |

**Response requirement**: Rotation and revocation must be approved and executed before T+10m to prevent backdoor creation.

---

## GitHub PAT — Classic (service_scoped blast radius)

**Source**: GitHub security advisories, supply chain attack postmortems

| Time | Attacker Action | Method | MITRE |
|---|---|---|---|
| T+0s | Token appears in public repo | git push, code review | — |
| T+1m | Attacker validates token | `GET /user` via GitHub API | T1552.001 |
| T+2m | Enumerates accessible repos | `GET /user/repos`, `/orgs/{org}/repos` | T1213.003 |
| T+5m | Clones all accessible private repos | git clone (all) | T1213.003 |
| T+8m | Searches clones for secondary secrets | grep -r "password\|key\|secret" | T1552.001 |
| T+10m | Reads GitHub Actions secrets references | Looks for `${{ secrets.* }}` patterns | T1552.001 |
| T+15m | Creates persistent access | Deploy key creation, webhook registration | T1098 |
| T+20m | Pushes malicious commit if write access | Supply chain compromise attempt | T1195.001 |
| T+30m | With `admin:org` scope: adds team member | Ghost account persistence | T1136.003 |

**Response requirement**: Revoke token within 5 minutes to prevent repo clone completion.

---

## Stripe Live Key (full_account blast radius)

**Source**: PCI DSS breach reports, Stripe fraud intelligence

| Time | Attacker Action | Method | MITRE |
|---|---|---|---|
| T+0s | Key exposed | — | — |
| T+2m | Attacker creates test charge | Stripe API: `POST /charges` ($1 test) | T1552.001 |
| T+5m | Confirms key is live production | Stripe response confirms mode | T1526 |
| T+8m | Enumerates customer data | `GET /customers` (all), `GET /payment_methods` | T1213 |
| T+10m | Begins data harvest | `GET /charges` with pagination | T1213 |
| T+15m | May attempt refund fraud | Create fake refunds to attacker card | T1657 |
| T+20m | Transfers to attacker's Stripe account | Stripe Connect transfer abuse | T1657 |
| T+1h | PCI DSS 4-hour notification clock starts | Upon discovery | Regulatory |

**Response requirement**: Revoke within 5 minutes. Notify Stripe security team immediately.

---

## Database Connection String (service_scoped)

**Source**: Verizon DBIR, internal incident data

| Time | Attacker Action | Method | MITRE |
|---|---|---|---|
| T+0s | Connection string exposed | — | — |
| T+1m | Attacker tests connection | `psql $DATABASE_URL` or equivalent | T1078 |
| T+3m | Enumerates schema | `\dt *.*` or `SHOW TABLES` | T1213 |
| T+5m | Identifies high-value tables | Look for: users, payments, tokens, pii | T1213 |
| T+8m | Begins data export | `SELECT * FROM users` or pg_dump | T1530 |
| T+15m | Full database exported | pg_dump -Fc or mysqldump | T1530 |
| T+20m | May attempt data destruction (ransomware) | DROP TABLE or ransom note in DB | T1485 |

**Response requirement**: Rotate connection string AND consider the database possibly compromised — audit for unauthorized access, check if port is publicly accessible.

---

## Private Key / PEM Key (full_account blast radius — context dependent)

| Time | Attacker Action | Method |
|---|---|---|
| T+0s | Key exposed | — |
| T+5m | Attacker identifies what the key grants | Check associated certificate or SSH authorized_keys |
| T+10m | If SSH: attempts login to all known hosts | ssh-keyscan, attempts |
| T+15m | If TLS: can MITM encrypted traffic | SSL stripping, rogue endpoint |
| T+20m | If code signing: can sign malicious code | Supply chain attack |

---

## SSH Private Key

| Time | Attacker Action |
|---|---|
| T+0s | Key exposed |
| T+5m | Attacker scans associated public key fingerprint across Shodan/Censys |
| T+10m | Attempts SSH to known IPs associated with the org |
| T+15m | If access gained: lateral movement begins |
| T+20m | Creates additional authorized_keys for persistence |

---

## JWT Signing Secret

| Time | Attacker Action |
|---|---|
| T+0s | Secret exposed |
| T+2m | Attacker crafts forged JWT with `sub: admin` or arbitrary user claims |
| T+5m | Forged JWT accepted by all service endpoints |
| T+immediate | Full authentication bypass — no login required |
| T+10m | Mass account takeover possible at scale |

**Note**: JWT secret exposure = IMMEDIATE CRITICAL. No time window — attacker has instant auth bypass on exposure. This is the highest urgency credential type.

---

## Generic API Key

| Time | Notes |
|---|---|
| T+0s | Key exposed |
| T+5m | Attacker identifies service from context clues |
| T+10m | Tests key against most likely API endpoints |
| T+15m | On success: begins service-specific exploitation |

---

## Industry Benchmark: Mean Time to Abuse

Based on GitGuardian 2024 research:
- **AWS keys in public GitHub repos**: 97% abused within 4 minutes of first commit
- **Generic API keys**: ~25% abused within 24 hours
- **Database URLs in public repos**: ~50% attempted within 1 hour
- **JWT secrets**: Real-time abuse possible (no scanning delay needed)

**Design implication for USAP**: The approval workflow must complete faster than the abuse timeline for the detected secret type. For AWS keys, this means the entire detect → approve → rotate cycle must be under 10 minutes.
