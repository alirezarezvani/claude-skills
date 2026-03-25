---
title: "Security Penetration Testing — Agent Skill & Codex Plugin"
description: "Use when the user asks to perform security audits, penetration testing, vulnerability scanning, OWASP Top 10 checks, or offensive security. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Security Penetration Testing

<div class="page-meta" markdown>
<span class="meta-badge">:material-code-braces: Engineering - Core</span>
<span class="meta-badge">:material-identifier: `security-pen-testing`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/security-pen-testing/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install engineering-skills</code>
</div>


Hands-on offensive security testing skill for finding vulnerabilities before attackers do. This is NOT compliance checking (see senior-secops) or security policy writing (see senior-security) — this is about systematic vulnerability discovery through authorized testing.

---

## Table of Contents

- [Overview](#overview)
- [OWASP Top 10 Systematic Audit](#owasp-top-10-systematic-audit)
- [Static Analysis](#static-analysis)
- [Dependency Vulnerability Scanning](#dependency-vulnerability-scanning)
- [Secret Scanning](#secret-scanning)
- [API Security Testing](#api-security-testing)
- [Web Vulnerability Testing](#web-vulnerability-testing)
- [Infrastructure Security](#infrastructure-security)
- [Pen Test Report Generation](#pen-test-report-generation)
- [Responsible Disclosure Workflow](#responsible-disclosure-workflow)
- [Workflows](#workflows)
- [Anti-Patterns](#anti-patterns)
- [Cross-References](#cross-references)

---

## Overview

### What This Skill Does

This skill provides the methodology, checklists, and automation for **offensive security testing** — actively probing systems to discover exploitable vulnerabilities. It covers web applications, APIs, infrastructure, and supply chain security.

### Distinction from Other Security Skills

| Skill | Focus | Approach |
|-------|-------|----------|
| **security-pen-testing** (this) | Finding vulnerabilities | Offensive — simulate attacker techniques |
| senior-secops | Security operations | Defensive — monitoring, incident response, SIEM |
| senior-security | Security policy | Governance — policies, frameworks, risk registers |
| skill-security-auditor | CI/CD gates | Automated — pre-merge security checks |

### Prerequisites

All testing described here assumes **written authorization** from the system owner. Unauthorized testing is illegal under the CFAA and equivalent laws worldwide. Always obtain a signed scope-of-work or rules-of-engagement document before starting.

---

## OWASP Top 10 Systematic Audit

Use the vulnerability scanner tool for automated checklist generation:

```bash
# Generate OWASP checklist for a web application
python scripts/vulnerability_scanner.py --target web --scope full

# Quick API-focused scan
python scripts/vulnerability_scanner.py --target api --scope quick --json
```

### A01:2021 — Broken Access Control

**Test Procedures:**
1. Attempt horizontal privilege escalation: access another user's resources by changing IDs
2. Test vertical escalation: access admin endpoints with regular user tokens
3. Verify CORS configuration — check `Access-Control-Allow-Origin` for wildcards
4. Test forced browsing to admin pages (`/admin`, `/api/admin`, `/debug`)
5. Modify JWT claims (`role`, `is_admin`) and replay tokens

**What to Look For:**
- Missing authorization checks on API endpoints
- Predictable resource IDs (sequential integers vs. UUIDs)
- Client-side only access controls (hidden UI elements without server checks)
- CORS misconfigurations allowing arbitrary origins

### A02:2021 — Cryptographic Failures

**Test Procedures:**
1. Check TLS version — reject anything below TLS 1.2
2. Verify password hashing: bcrypt/scrypt/argon2 with adequate cost factor
3. Look for sensitive data in URLs (tokens in query params get logged)
4. Check for hardcoded encryption keys in source code
5. Test for weak random number generation (Math.random() for tokens)

**What to Look For:**
- MD5/SHA1 used for password hashing
- Secrets in environment variables without encryption at rest
- Missing `Strict-Transport-Security` header
- Self-signed certificates in production

### A03:2021 — Injection

**Test Procedures:**
1. SQL injection: test all input fields with `' OR 1=1--` and time-based payloads
2. NoSQL injection: test with `{"$gt": ""}` and `{"$ne": null}` in JSON bodies
3. Command injection: test inputs with `; whoami` and backtick substitution
4. LDAP injection: test with `*)(uid=*))(|(uid=*`
5. Template injection: test with `{{7*7}}` and `${7*7}`

**What to Look For:**
- String concatenation in SQL queries
- User input passed to `eval()`, `exec()`, `os.system()`
- Unparameterized ORM queries
- Template engines rendering user input without sandboxing

### A04:2021 — Insecure Design

**Test Procedures:**
1. Review business logic flows for abuse scenarios (e.g., negative quantities in carts)
2. Check rate limiting on sensitive operations (login, password reset, OTP)
3. Test multi-step flows for state manipulation (skip payment step)
4. Verify security questions aren't guessable

**What to Look For:**
- Missing rate limits on authentication endpoints
- Business logic that trusts client-side calculations
- Lack of account lockout after failed attempts
- Missing CAPTCHA on public-facing forms

### A05:2021 — Security Misconfiguration

**Test Procedures:**
1. Check for default credentials on admin panels
2. Verify unnecessary HTTP methods are disabled (TRACE, DELETE on public endpoints)
3. Check error handling — stack traces should never leak to users
4. Review HTTP security headers (CSP, X-Frame-Options, X-Content-Type-Options)
5. Check directory listing is disabled

**What to Look For:**
- Debug mode enabled in production
- Default admin:admin credentials
- Verbose error messages with stack traces
- Missing security headers

### A06:2021 — Vulnerable and Outdated Components

**Test Procedures:**
1. Run dependency audit against known CVE databases
2. Check for end-of-life frameworks and libraries
3. Verify transitive dependency versions
4. Check for known vulnerable versions (e.g., Log4j 2.0-2.14.1)

```bash
# Audit a package manifest
python scripts/dependency_auditor.py --file package.json --severity high
python scripts/dependency_auditor.py --file requirements.txt --json
```

### A07:2021 — Identification and Authentication Failures

**Test Procedures:**
1. Test brute force protection on login endpoints
2. Check password policy enforcement (minimum length, complexity)
3. Verify session invalidation on logout and password change
4. Test "remember me" token security (HttpOnly, Secure, SameSite flags)
5. Check multi-factor authentication bypass paths

**What to Look For:**
- Sessions that persist after logout
- Missing `HttpOnly` and `Secure` flags on session cookies
- Password reset tokens that don't expire
- Username enumeration via different error messages

### A08:2021 — Software and Data Integrity Failures

**Test Procedures:**
1. Check for unsigned updates or deployment artifacts
2. Verify CI/CD pipeline integrity (signed commits, protected branches)
3. Test deserialization endpoints with crafted payloads
4. Check for SRI (Subresource Integrity) on CDN-loaded scripts

**What to Look For:**
- Unsafe deserialization of user input (pickle, Java serialization)
- Missing integrity checks on downloaded artifacts
- CI/CD pipelines running untrusted code
- CDN scripts without SRI hashes

### A09:2021 — Security Logging and Monitoring Failures

**Test Procedures:**
1. Verify authentication events are logged (success and failure)
2. Check that logs don't contain sensitive data (passwords, tokens, PII)
3. Test alerting thresholds (do 50 failed logins trigger an alert?)
4. Verify log integrity — can an attacker tamper with logs?

**What to Look For:**
- Missing audit trail for admin actions
- Passwords or tokens appearing in logs
- No alerting on suspicious patterns
- Logs stored without integrity protection

### A10:2021 — Server-Side Request Forgery (SSRF)

**Test Procedures:**
1. Test URL input fields with internal addresses (`http://169.254.169.254/` for cloud metadata)
2. Check for open redirect chains that reach internal services
3. Test with DNS rebinding payloads
4. Verify allowlist validation on outbound requests

**What to Look For:**
- User-controlled URLs passed to `fetch()`, `requests.get()`, `curl`
- Missing allowlist on outbound HTTP requests
- Ability to reach cloud metadata endpoints (AWS, GCP, Azure)
- PDF generators or screenshot services that fetch arbitrary URLs

---

## Static Analysis

### CodeQL Custom Rules

Write custom CodeQL queries for project-specific vulnerability patterns:

```ql
/**
 * Detect SQL injection via string concatenation
 */
import python
import semmle.python.dataflow.new.DataFlow

from Call call, StringFormatting fmt
where
  call.getFunc().getName() = "execute" and
  fmt = call.getArg(0) and
  exists(DataFlow::Node source |
    source.asExpr() instanceof Name and
    DataFlow::localFlow(source, DataFlow::exprNode(fmt.getAnOperand()))
  )
select call, "Potential SQL injection: user input flows into execute()"
```

### Semgrep Custom Rules

Create project-specific Semgrep rules:

```yaml
rules:
  - id: hardcoded-jwt-secret
    pattern: |
      jwt.encode($PAYLOAD, "...", ...)
    message: "JWT signed with hardcoded secret"
    severity: ERROR
    languages: [python]

  - id: unsafe-yaml-load
    pattern: yaml.load($DATA)
    fix: yaml.safe_load($DATA)
    message: "Use yaml.safe_load() to prevent arbitrary code execution"
    severity: WARNING
    languages: [python]

  - id: express-no-helmet
    pattern: |
      const app = express();
      ...
      app.listen(...)
    pattern-not: |
      const app = express();
      ...
      app.use(helmet(...));
      ...
      app.listen(...)
    message: "Express app missing helmet middleware for security headers"
    severity: WARNING
    languages: [javascript, typescript]
```

### ESLint Security Plugins

Recommended configuration:

```json
{
  "plugins": ["security", "no-unsanitized"],
  "extends": ["plugin:security/recommended"],
  "rules": {
    "security/detect-object-injection": "error",
    "security/detect-non-literal-regexp": "warn",
    "security/detect-unsafe-regex": "error",
    "security/detect-buffer-noassert": "error",
    "security/detect-eval-with-expression": "error",
    "no-unsanitized/method": "error",
    "no-unsanitized/property": "error"
  }
}
```

---

## Dependency Vulnerability Scanning

### Ecosystem-Specific Commands

```bash
# Node.js
npm audit --json | jq '.vulnerabilities | to_entries[] | select(.value.severity == "critical")'

# Python
pip audit --format json --desc
safety check --json

# Go
govulncheck ./...

# Ruby
bundle audit check --update
```

### CVE Triage Workflow

1. **Collect**: Run ecosystem audit tools, aggregate findings
2. **Deduplicate**: Group by CVE ID across direct and transitive deps
3. **Score**: Use CVSS base score + environmental adjustments
4. **Prioritize**: Critical + exploitable + reachable = fix immediately
5. **Remediate**: Upgrade, patch, or mitigate with compensating controls
6. **Verify**: Rerun audit to confirm fix, update lock files

```bash
# Use the dependency auditor for automated triage
python scripts/dependency_auditor.py --file package.json --severity critical --json
```

### Known Vulnerable Patterns

| Package | Vulnerable Versions | CVE | Impact |
|---------|-------------------|-----|--------|
| log4j-core | 2.0 - 2.14.1 | CVE-2021-44228 | RCE via JNDI injection |
| lodash | < 4.17.21 | CVE-2021-23337 | Prototype pollution |
| axios | < 1.6.0 | CVE-2023-45857 | CSRF token exposure |
| pillow | < 9.3.0 | CVE-2022-45198 | DoS via crafted image |
| express | < 4.19.2 | CVE-2024-29041 | Open redirect |

---

## Secret Scanning

### TruffleHog Patterns

```bash
# Scan git history for secrets
trufflehog git file://. --only-verified --json

# Scan filesystem (no git history)
trufflehog filesystem . --json
```

### Gitleaks Configuration

```toml
# .gitleaks.toml
title = "Custom Gitleaks Config"

[[rules]]
id = "aws-access-key"
description = "AWS Access Key ID"
regex = '''AKIA[0-9A-Z]{16}'''
tags = ["aws", "credentials"]

[[rules]]
id = "generic-api-key"
description = "Generic API Key"
regex = '''(?i)(api[_-]?key|apikey)\s*[:=]\s*['\"][a-zA-Z0-9]{20,}['\"]'''
tags = ["api", "key"]

[[rules]]
id = "private-key"
description = "Private Key Header"
regex = '''-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----'''
tags = ["private-key"]

[allowlist]
paths = ['''\.test\.''', '''_test\.go''', '''mock''', '''fixture''']
```

### Pre-commit Hook Integration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

  - repo: https://github.com/trufflesecurity/trufflehog
    rev: v3.63.0
    hooks:
      - id: trufflehog
        args: ["git", "file://.", "--since-commit", "HEAD", "--only-verified"]
```

### CI Integration (GitHub Actions)

```yaml
name: Secret Scan
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: trufflesecurity/trufflehog@main
        with:
          extra_args: --only-verified
```

---

## API Security Testing

### Authentication Bypass

**JWT Manipulation:**
1. Decode token at jwt.io — inspect claims without verification
2. Change `alg` to `none` and remove signature: `eyJ...payload.`
3. Change `alg` from RS256 to HS256 and sign with the public key
4. Modify claims (`role: "admin"`, `exp: 9999999999`) and re-sign with weak secrets
5. Test key confusion: HMAC signed with RSA public key bytes

**Session Fixation:**
1. Obtain a session token before authentication
2. Authenticate — check if the session ID changes
3. If the same session ID persists, the app is vulnerable to session fixation

### Authorization Flaws

**IDOR (Insecure Direct Object Reference):**
```
GET /api/users/123/profile → 200 (your profile)
GET /api/users/124/profile → 200 (someone else's profile — IDOR!)
GET /api/users/124/profile → 403 (properly protected)
```

Test pattern: Change numeric IDs, UUIDs, slugs in every endpoint. Use Burp Intruder or a simple script to iterate.

**BOLA (Broken Object Level Authorization):**
Same as IDOR but specifically in REST APIs. Test every CRUD operation:
- Can user A read user B's resource?
- Can user A update user B's resource?
- Can user A delete user B's resource?

**BFLA (Broken Function Level Authorization):**
```
# Regular user tries admin endpoints
POST /api/admin/users          → Should be 403
DELETE /api/admin/users/123     → Should be 403
PUT /api/settings/global        → Should be 403
```

### Rate Limiting Validation

Test rate limits on critical endpoints:
```bash
# Rapid-fire login attempts
for i in $(seq 1 100); do
  curl -s -o /dev/null -w "%{http_code}" \
    -X POST https://target.com/api/login \
    -d '{"email":"test@test.com","password":"wrong"}';
done
# Expect: 429 after threshold (typically 5-10 attempts)
```

### Mass Assignment Detection

```bash
# Try adding admin fields to a regular update request
PUT /api/users/profile
{
  "name": "Normal User",
  "email": "user@test.com",
  "role": "admin",          # mass assignment attempt
  "is_verified": true,      # mass assignment attempt
  "subscription": "enterprise"  # mass assignment attempt
}
```

### GraphQL-Specific Testing

**Introspection Query:**
```graphql
{
  __schema {
    types { name fields { name type { name } } }
  }
}
```
Introspection should be **disabled in production**.

**Query Depth Attack:**
```graphql
{
  user(id: 1) {
    friends {
      friends {
        friends {
          friends { # Keep nesting until server crashes
            name
          }
        }
      }
    }
  }
}
```

**Batching Attack:**
```json
[
  {"query": "mutation { login(user:\"admin\", pass:\"password1\") { token } }"},
  {"query": "mutation { login(user:\"admin\", pass:\"password2\") { token } }"},
  {"query": "mutation { login(user:\"admin\", pass:\"password3\") { token } }"}
]
```
Batch mutations can bypass rate limiting if counted as a single request.

---

## Web Vulnerability Testing

### XSS (Cross-Site Scripting)

**Reflected XSS Test Payloads** (non-destructive):
```
<script>alert(document.domain)</script>
"><img src=x onerror=alert(document.domain)>
javascript:alert(document.domain)
<svg onload=alert(document.domain)>
'-alert(document.domain)-'
</script><script>alert(document.domain)</script>
```

**Stored XSS**: Submit payloads in persistent fields (comments, profiles, messages), then check if they render for other users.

**DOM-Based XSS**: Look for `innerHTML`, `document.write()`, `eval()` operating on `location.hash`, `location.search`, or `document.referrer`.

### CSRF Token Validation

1. Capture a legitimate request with CSRF token
2. Replay the request without the token — should fail (403)
3. Replay with a token from a different session — should fail
4. Check if token changes per request or is static per session
5. Verify `SameSite` cookie attribute is set to `Strict` or `Lax`

### SQL Injection

**Detection Payloads** (safe, non-destructive):
```
' OR '1'='1
' OR '1'='1' --
" OR "1"="1
1 OR 1=1
' UNION SELECT NULL--
' AND SLEEP(5)--     (time-based blind)
' AND 1=1--          (boolean-based blind)
```

**Union-Based Enumeration** (authorized testing only):
```sql
' UNION SELECT 1,2,3--                    -- Find column count
' UNION SELECT table_name,2,3 FROM information_schema.tables--
' UNION SELECT column_name,2,3 FROM information_schema.columns WHERE table_name='users'--
```

**Time-Based Blind:**
```sql
' AND IF(1=1, SLEEP(5), 0)--     -- MySQL
' AND pg_sleep(5)--               -- PostgreSQL
' WAITFOR DELAY '0:0:5'--        -- MSSQL
```

### SSRF Detection

**Payloads for SSRF testing:**
```
http://127.0.0.1
http://localhost
http://169.254.169.254/latest/meta-data/   (AWS metadata)
http://metadata.google.internal/            (GCP metadata)
http://169.254.169.254/metadata/instance    (Azure metadata)
http://[::1]                                (IPv6 localhost)
http://0x7f000001                           (hex encoding)
http://2130706433                           (decimal encoding)
```

### Path Traversal

```
GET /api/files?name=../../../etc/passwd
GET /api/files?name=....//....//....//etc/passwd
GET /api/files?name=%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd
GET /api/files?name=..%252f..%252f..%252fetc%252fpasswd  (double encoding)
```

---

## Infrastructure Security

### Misconfigured Cloud Storage

**S3 Bucket Checks:**
```bash
# Check for public read access
aws s3 ls s3://target-bucket --no-sign-request

# Check bucket policy
aws s3api get-bucket-policy --bucket target-bucket

# Check ACL
aws s3api get-bucket-acl --bucket target-bucket
```

**Common Bucket Name Patterns:**
```
{company}-backup, {company}-dev, {company}-staging
{company}-assets, {company}-uploads, {company}-logs
```

### HTTP Security Headers

Required headers and expected values:

| Header | Expected Value |
|--------|---------------|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains; preload` |
| `Content-Security-Policy` | Restrictive policy, no `unsafe-inline` or `unsafe-eval` |
| `X-Content-Type-Options` | `nosniff` |
| `X-Frame-Options` | `DENY` or `SAMEORIGIN` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | Restrict camera, microphone, geolocation |
| `X-XSS-Protection` | `0` (deprecated, CSP is preferred) |

### TLS Configuration

```bash
# Check TLS version and cipher suites
nmap --script ssl-enum-ciphers -p 443 target.com

# Quick check with testssl.sh
./testssl.sh target.com

# Check certificate expiry
echo | openssl s_client -connect target.com:443 2>/dev/null | openssl x509 -noout -dates
```

**Reject:** TLS 1.0, TLS 1.1, RC4, DES, 3DES, MD5 in cipher suites, CBC mode ciphers (BEAST), export-grade ciphers.

### Open Port Scanning

```bash
# Quick top-1000 ports
nmap -sV target.com

# Full port scan
nmap -p- -sV target.com

# Common dangerous open ports
# 21 (FTP), 23 (Telnet), 445 (SMB), 3389 (RDP), 6379 (Redis), 27017 (MongoDB)
```

---

## Pen Test Report Generation

Generate professional reports from structured findings:

```bash
# Generate markdown report from findings JSON
python scripts/pentest_report_generator.py --findings findings.json --format md --output report.md

# Generate JSON report
python scripts/pentest_report_generator.py --findings findings.json --format json --output report.json
```

### Findings JSON Format

```json
[
  {
    "title": "SQL Injection in Login Endpoint",
    "severity": "critical",
    "cvss_score": 9.8,
    "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
    "category": "A03:2021 - Injection",
    "description": "The /api/login endpoint is vulnerable to SQL injection via the email parameter.",
    "evidence": "Request: POST /api/login {\"email\": \"' OR 1=1--\", \"password\": \"x\"}\nResponse: 200 OK with admin session token",
    "impact": "Full database access, authentication bypass, potential remote code execution",
    "remediation": "Use parameterized queries. Replace string concatenation with prepared statements.",
    "references": ["https://cwe.mitre.org/data/definitions/89.html"]
  }
]
```

### Report Structure

1. **Executive Summary**: Business impact, overall risk level, top 3 findings
2. **Scope**: What was tested, what was excluded, testing dates
3. **Methodology**: Tools used, testing approach (black/gray/white box)
4. **Findings Table**: Sorted by severity with CVSS scores
5. **Detailed Findings**: Each with description, evidence, impact, remediation
6. **Remediation Priority Matrix**: Effort vs. impact for each fix
7. **Appendix**: Raw tool output, full payload lists

---

## Responsible Disclosure Workflow

Responsible disclosure is **mandatory** for any vulnerability found during authorized testing or independent research. See `references/responsible_disclosure.md` for full templates.

### Timeline

| Day | Action |
|-----|--------|
| 0 | Discovery — document finding with evidence |
| 1 | Report to vendor via security contact or bug bounty program |
| 7 | Follow up if no acknowledgment received |
| 30 | Request status update and remediation timeline |
| 60 | Second follow-up — offer technical assistance |
| 90 | Public disclosure (with or without fix, per industry standard) |

### Key Principles

1. **Never exploit beyond proof of concept** — demonstrate impact without causing damage
2. **Encrypt all communications** — PGP/GPG for email, secure channels for details
3. **Do not access, modify, or exfiltrate real user data** — use your own test accounts
4. **Document everything** — timestamps, screenshots, request/response pairs
5. **Respect the vendor's timeline** — extend deadline if they're actively working on a fix

---

## Workflows

### Workflow 1: Quick Security Check (15 Minutes)

For pre-merge reviews or quick health checks:

```bash
# 1. Generate OWASP checklist
python scripts/vulnerability_scanner.py --target web --scope quick

# 2. Scan dependencies
python scripts/dependency_auditor.py --file package.json --severity high

# 3. Check for secrets in recent commits
# (Use gitleaks or trufflehog as described in Secret Scanning section)

# 4. Review HTTP security headers
curl -sI https://target.com | grep -iE "(strict-transport|content-security|x-frame|x-content-type)"
```

**Decision**: If any critical or high findings, block the merge.

### Workflow 2: Full Penetration Test (Multi-Day Assessment)

**Day 1 — Reconnaissance:**
1. Map the attack surface: endpoints, authentication flows, third-party integrations
2. Run automated OWASP checklist (full scope)
3. Run dependency audit across all manifests
4. Run secret scan on full git history

**Day 2 — Manual Testing:**
1. Test authentication and authorization (IDOR, BOLA, BFLA)
2. Test injection points (SQLi, XSS, SSRF, command injection)
3. Test business logic flaws
4. Test API-specific vulnerabilities (GraphQL, rate limiting, mass assignment)

**Day 3 — Infrastructure and Reporting:**
1. Check cloud storage permissions
2. Verify TLS configuration and security headers
3. Port scan for unnecessary services
4. Compile findings into structured JSON
5. Generate pen test report

```bash
# Generate final report
python scripts/pentest_report_generator.py --findings findings.json --format md --output pentest-report.md
```

### Workflow 3: CI/CD Security Gate

Automated security checks that run on every pull request:

```yaml
# .github/workflows/security-gate.yml
name: Security Gate
on: [pull_request]
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      # Secret scanning
      - name: Scan for secrets
        uses: trufflesecurity/trufflehog@main
        with:
          extra_args: --only-verified

      # Dependency audit
      - name: Audit dependencies
        run: |
          npm audit --audit-level=high
          pip audit --desc

      # SAST
      - name: Static analysis
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/secrets
            p/owasp-top-ten

      # Security headers check (staging only)
      - name: Check security headers
        if: github.base_ref == 'staging'
        run: |
          curl -sI $STAGING_URL | python scripts/vulnerability_scanner.py --target web --scope quick
```

**Gate Policy**: Block merge on critical/high findings. Warn on medium. Log low/info.

---

## Anti-Patterns

1. **Testing in production without authorization** — Always get written permission and use staging/test environments when possible
2. **Ignoring low-severity findings** — Low findings compound; a chain of lows can become a critical exploit path
3. **Skipping responsible disclosure** — Every vulnerability found must be reported through proper channels
4. **Relying solely on automated tools** — Tools miss business logic flaws, chained exploits, and novel attack vectors
5. **Testing without a defined scope** — Scope creep leads to legal liability; document what is and isn't in scope
6. **Reporting without remediation guidance** — Every finding must include actionable remediation steps
7. **Storing evidence insecurely** — Pen test evidence (screenshots, payloads, tokens) is sensitive; encrypt and restrict access
8. **One-time testing** — Security testing must be continuous; integrate into CI/CD and schedule periodic assessments

---

## Cross-References

| Skill | Relationship |
|-------|-------------|
| [senior-secops](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/senior-secops/SKILL.md) | Defensive security operations — monitoring, incident response, SIEM configuration |
| [senior-security](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/senior-security/SKILL.md) | Security policy and governance — frameworks, risk registers, compliance |
| [dependency-auditor](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/dependency-auditor/SKILL.md) | Deep supply chain security — SBOMs, license compliance, transitive risk |
| [code-reviewer](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/code-reviewer/SKILL.md) | Code review practices — includes security review checklist |
