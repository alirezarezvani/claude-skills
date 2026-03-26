# MITRE ATT&CK Mapping — Identity and Access Risk

## Purpose

Maps each IAM anomaly type detected by USAP to specific MITRE ATT&CK techniques,
sub-techniques, and real-world threat actor usage. Use when composing key_findings
and rationale to provide SOC-ready threat context.

---

## ATT&CK Technique Reference

### T1078 — Valid Accounts
**Parent technique**: Adversaries use existing valid credentials to gain or maintain access.

#### T1078.004 — Cloud Accounts
**Relevance to USAP**: All AWS IAM-related anomalies

| USAP Anomaly | ATT&CK Sub-context | Real-World Threat Actors |
|---|---|---|
| `privilege_escalation` via IAM PassRole | Creating new cloud infrastructure with privileged role | APT10, Scattered Spider |
| `root_account_usage` | Attacker achieved root via key material or MFA bypass | Multiple financially-motivated actors |
| `dormant_reactivation` | Old compromised account reactivated to avoid detection | APT33, Lapsus$ |
| `cross_account_anomaly` | Lateral movement between AWS accounts | APT29 (Cozy Bear), SolarWinds attackers |

**Detection indicators**:
- `sts:GetCallerIdentity` from unexpected IP = attacker confirming access
- New IAM user created outside of Terraform/IaC = backdoor creation
- API calls from Tor exit nodes or known VPN ranges

---

### T1078.002 — Domain Accounts (adapted: Service Accounts)
**Relevance**: Service account used interactively or from unexpected contexts

| USAP Anomaly | Indicator |
|---|---|
| `service_account_interactive` | Service account (named `svc-*`, `automation-*`) logging in via console |
| `service_account_interactive` | User-agent = browser/Postman instead of expected SDK/CLI |

---

### T1484 — Domain Policy Modification
**USAP context**: IAM policy changes that escalate privileges

#### T1484.001 — Group Policy Modification (adapted: IAM Policy Modification)

| Attack Path | CloudTrail Events | MITRE Detail |
|---|---|---|
| Attach admin policy to self | `iam:AttachUserPolicy` with `AdministratorAccess` | Direct privilege escalation |
| Create new policy version with `*` | `iam:CreatePolicyVersion` then `iam:SetDefaultPolicyVersion` | Policy backdoor |
| Modify role trust policy | `iam:UpdateAssumeRolePolicy` | Enables external account assumption |

---

### T1098 — Account Manipulation
**USAP context**: Creating persistent access

#### T1098.001 — Additional Cloud Credentials

| CloudTrail Evidence | Attack Meaning |
|---|---|
| `iam:CreateAccessKey` for different user | Harvesting long-term credentials from other users |
| `iam:CreateAccessKey` for own user in unusual context | Creating additional credential for persistence |
| `iam:CreateLoginProfile` for user without prior console access | Enabling console access as persistence |
| `ec2:ImportKeyPair` | Adding attacker SSH key to EC2 |

**Threat actor TTPs**:
- Scattered Spider: creates IAM users named like legitimate service accounts
- APT29: creates access keys that appear to be for automation, not human users

---

### T1550 — Use Alternate Authentication Material

#### T1550.001 — Application Access Token

| USAP Anomaly | Detail |
|---|---|
| `lateral_movement` via AssumeRole | Using STS temporary credentials to move between roles/accounts |
| Cross-account AssumeRole anomaly | Pivoting between AWS accounts using assumed role credentials |

**Multi-hop AssumeRole chain** (classic APT technique):
```
Compromised Account → AssumeRole → Account B role → AssumeRole → Account C admin role
```
Each hop uses temporary credentials (15 minutes to 1 hour validity).
CloudTrail in Account C may not show the original compromised identity.
Always trace the full chain back to the originating credentials.

---

### T1110 — Brute Force

#### T1110.004 — Credential Stuffing

| USAP Anomaly | CloudTrail Signal |
|---|---|
| `credential_stuffing` | `ConsoleLogin` events with `responseElements.ConsoleLogin = Failure` |
| Multiple source IPs | EventSource varies, multiple `errorCode: Failed authentication` |
| Geographic spread | UserAgent consistent but IPs from multiple countries |

**Credential stuffing vs password spraying distinction**:
- Stuffing: many username:password pairs (leaked database)
- Spraying: one password against many usernames (avoid lockout)
- USAP detects both via volume + timing analysis

---

### T1556 — Modify Authentication Process

#### T1556.006 — Multi-Factor Authentication

| USAP Anomaly | Indicator |
|---|---|
| `mfa_bypass` | `ConsoleLogin` with `additionalEventData.MFAUsed = No` for MFA-required user |
| `mfa_bypass` | STS `AssumeRoleWithSAML` or `AssumeRoleWithWebIdentity` bypassing native MFA |

**MFA bypass techniques**:
1. SIM swap → take over MFA phone number
2. Phishing OTP in real-time (AiTM — Adversary in the Middle)
3. Session cookie theft (bypasses MFA entirely)
4. Social engineering IT helpdesk to disable MFA

---

### T1562 — Impair Defenses

#### T1562.008 — Disable or Modify Cloud Logs

**This is the highest-urgency indicator. Always escalate to SEV1.**

| CloudTrail Event | Attack Meaning |
|---|---|
| `cloudtrail:StopLogging` | Attacker disabling your primary audit log |
| `cloudtrail:DeleteTrail` | Permanent log destruction |
| `guardduty:DeleteDetector` | Disabling anomaly detection |
| `guardduty:DisableOrganizationAdminAccount` | Disabling GuardDuty org-wide |
| `config:StopConfigurationRecorder` | Disabling configuration compliance tracking |
| `securityhub:DisableSecurityHub` | Disabling central security findings |

**Response**: Any of these events = your investigation evidence is being destroyed. Preserve existing logs immediately. Treat the full timeframe before this event as potentially unlogged.

---

### T1530 — Data from Cloud Storage

| USAP Anomaly | Signal |
|---|---|
| `data_enumeration_burst` | `s3:ListAllMyBuckets` followed by `s3:GetObject` at scale |
| High-volume S3 downloads | Egress spike + many GetObject calls |

**AWS Macie integration**: For confirmed or suspected S3 exfiltration, note that
AWS Macie S3 inventory findings can supplement USAP evidence.

---

### T1619 — Cloud Storage Object Discovery

| Behavior | API Calls |
|---|---|
| Identifying S3 buckets | `s3:ListAllMyBuckets`, `s3:GetBucketLocation` |
| Identifying data sensitivity | `s3:GetBucketTagging`, `s3:GetBucketAcl` |
| Enumerating other services | `rds:DescribeDBInstances`, `dynamodb:ListTables` |

---

## Threat Actor Profiles (IAM Focus)

### Scattered Spider (UNC3944)
- **Primary TTP**: Social engineering IT helpdesk to reset MFA
- **Cloud focus**: Azure AD, Okta, then pivoting to AWS
- **USAP indicators**: `mfa_bypass` + cloud access + new device enrollment
- **Response priority**: Immediately verify with helpdesk if MFA was recently reset

### APT29 (Cozy Bear)
- **Primary TTP**: Supply chain compromise → credential theft → long-term persistent access
- **Cloud focus**: Microsoft 365 OAuth tokens, then AWS cross-account
- **USAP indicators**: `lateral_movement` across accounts, `dormant_reactivation`, OAuth token anomalies
- **Response priority**: Full blast radius assessment; assume months of access

### Lapsus$
- **Primary TTP**: Insider recruitment or SIM swap → MFA bypass → cloud admin
- **Cloud focus**: Dev environments, source code, CI/CD pipelines
- **USAP indicators**: `privilege_escalation` in dev account, code repo access after credential stuffing

### Financially Motivated Actors (generic cloud crypto miners)
- **Primary TTP**: Exposed access key → EC2 mass launch
- **USAP indicators**: `privilege_escalation` or known key + `ec2:RunInstances` calls
- **Response**: Immediate key revocation + EC2 scan for unauthorized instances

---

## MITRE ATT&CK Navigator Tags (IAM)

For USAP finding `key_findings`, use these standardized tags:

```
T1078.004   Valid Accounts: Cloud Accounts
T1078.002   Valid Accounts: Domain Accounts (service accounts)
T1484.001   Domain Policy Modification: Group Policy Modification
T1098.001   Account Manipulation: Additional Cloud Credentials
T1550.001   Use Alternate Authentication Material: Application Access Token
T1110.004   Brute Force: Credential Stuffing
T1556.006   Modify Authentication Process: Multi-Factor Authentication
T1562.008   Impair Defenses: Disable or Modify Cloud Logs
T1530       Data from Cloud Storage
T1619       Cloud Storage Object Discovery
T1087.004   Account Discovery: Cloud Account
T1136.003   Create Account: Cloud Account
T1496       Resource Hijacking
T1485       Data Destruction
```
