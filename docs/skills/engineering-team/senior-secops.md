---
title: "Senior SecOps Engineer"
description: "Senior SecOps Engineer - Claude Code skill from the Engineering - Core domain."
---

# Senior SecOps Engineer

<div class="page-meta" markdown>
<span class="meta-badge">:material-code-braces: Engineering - Core</span>
<span class="meta-badge">:material-identifier: `senior-secops`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/senior-secops/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install engineering-skills</code>
</div>


Complete toolkit for Security Operations including vulnerability management, compliance verification, secure coding practices, and security automation.

---

## Table of Contents

- [Core Capabilities](#core-capabilities)
- [Workflows](#workflows)
- [Tool Reference](#tool-reference)
- [Security Standards](#security-standards)
- [Compliance Frameworks](#compliance-frameworks)
- [Best Practices](#best-practices)

---

## Core Capabilities

### 1. Security Scanner

Scan source code for security vulnerabilities including hardcoded secrets, SQL injection, XSS, command injection, and path traversal.

```bash
# Scan project for security issues
python scripts/security_scanner.py /path/to/project

# Filter by severity
python scripts/security_scanner.py /path/to/project --severity high

# JSON output for CI/CD
python scripts/security_scanner.py /path/to/project --json --output report.json
```

**Detects:**
- Hardcoded secrets (API keys, passwords, AWS credentials, GitHub tokens, private keys)
- SQL injection patterns (string concatenation, f-strings, template literals)
- XSS vulnerabilities (innerHTML assignment, unsafe DOM manipulation, React unsafe patterns)
- Command injection (shell=True, exec, eval with user input)
- Path traversal (file operations with user input)

### 2. Vulnerability Assessor

Scan dependencies for known CVEs across npm, Python, and Go ecosystems.

```bash
# Assess project dependencies
python scripts/vulnerability_assessor.py /path/to/project

# Critical/high only
python scripts/vulnerability_assessor.py /path/to/project --severity high

# Export vulnerability report
python scripts/vulnerability_assessor.py /path/to/project --json --output vulns.json
```

**Scans:**
- `package.json` and `package-lock.json` (npm)
- `requirements.txt` and `pyproject.toml` (Python)
- `go.mod` (Go)

**Output:**
- CVE IDs with CVSS scores
- Affected package versions
- Fixed versions for remediation
- Overall risk score (0-100)

### 3. Compliance Checker

Verify security compliance against SOC 2, PCI-DSS, HIPAA, and GDPR frameworks.

```bash
# Check all frameworks
python scripts/compliance_checker.py /path/to/project

# Specific framework
python scripts/compliance_checker.py /path/to/project --framework soc2
python scripts/compliance_checker.py /path/to/project --framework pci-dss
python scripts/compliance_checker.py /path/to/project --framework hipaa
python scripts/compliance_checker.py /path/to/project --framework gdpr

# Export compliance report
python scripts/compliance_checker.py /path/to/project --json --output compliance.json
```

**Verifies:**
- Access control implementation
- Encryption at rest and in transit
- Audit logging
- Authentication strength (MFA, password hashing)
- Security documentation
- CI/CD security controls

---

## Workflows

### Workflow 1: Security Audit

Complete security assessment of a codebase.

```bash
# Step 1: Scan for code vulnerabilities
python scripts/security_scanner.py . --severity medium
# STOP if exit code 2 — resolve critical findings before continuing
```

```bash
# Step 2: Check dependency vulnerabilities
python scripts/vulnerability_assessor.py . --severity high
# STOP if exit code 2 — patch critical CVEs before continuing
```

```bash
# Step 3: Verify compliance controls
python scripts/compliance_checker.py . --framework all
# STOP if exit code 2 — address critical gaps before proceeding
```

```bash
# Step 4: Generate combined reports
python scripts/security_scanner.py . --json --output security.json
python scripts/vulnerability_assessor.py . --json --output vulns.json
python scripts/compliance_checker.py . --json --output compliance.json
```

### Workflow 2: CI/CD Security Gate

Integrate security checks into deployment pipeline.

```yaml
# .github/workflows/security.yml
name: "security-scan"

on:
  pull_request:
    branches: [main, develop]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: "set-up-python"
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: "security-scanner"
        run: python scripts/security_scanner.py . --severity high

      - name: "vulnerability-assessment"
        run: python scripts/vulnerability_assessor.py . --severity critical

      - name: "compliance-check"
        run: python scripts/compliance_checker.py . --framework soc2
```

Each step fails the pipeline on its respective exit code — no deployment proceeds past a critical finding.

### Workflow 3: CVE Triage

Respond to a new CVE affecting your application.

```
1. ASSESS (0-2 hours)
   - Identify affected systems using vulnerability_assessor.py
   - Check if CVE is being actively exploited
   - Determine CVSS environmental score for your context
   - STOP if CVSS 9.0+ on internet-facing system — escalate immediately

2. PRIORITIZE
   - Critical (CVSS 9.0+, internet-facing): 24 hours
   - High (CVSS 7.0-8.9): 7 days
   - Medium (CVSS 4.0-6.9): 30 days
   - Low (CVSS < 4.0): 90 days

3. REMEDIATE
   - Update affected dependency to fixed version
   - Run security_scanner.py to verify fix (must return exit code 0)
   - STOP if scanner still flags the CVE — do not deploy
   - Test for regressions
   - Deploy with enhanced monitoring

4. VERIFY
   - Re-run vulnerability_assessor.py
   - Confirm CVE no longer reported
   - Document remediation actions
```

### Workflow 4: Incident Response

Security incident handling procedure.

```
PHASE 1: DETECT & IDENTIFY (0-15 min)
- Alert received and acknowledged
- Initial severity assessment (SEV-1 to SEV-4)
- Incident commander assigned
- Communication channel established

PHASE 2: CONTAIN (15-60 min)
- Affected systems identified
- Network isolation if needed
- Credentials rotated if compromised
- Preserve evidence (logs, memory dumps)

PHASE 3: ERADICATE (1-4 hours)
- Root cause identified
- Malware/backdoors removed
- Vulnerabilities patched (run security_scanner.py; must return exit code 0)
- Systems hardened

PHASE 4: RECOVER (4-24 hours)
- Systems restored from clean backup
- Services brought back online
- Enhanced monitoring enabled
- User access restored

PHASE 5: POST-INCIDENT (24-72 hours)
- Incident timeline documented
- Root cause analysis complete
- Lessons learned documented
- Preventive measures implemented
- Stakeholder report delivered
```

---

## Tool Reference

### security_scanner.py

| Option | Description |
|--------|-------------|
| `target` | Directory or file to scan |
| `--severity, -s` | Minimum severity: critical, high, medium, low |
| `--verbose, -v` | Show files as they're scanned |
| `--json` | Output results as JSON |
| `--output, -o` | Write results to file |

**Exit Codes:** `0` = no critical/high findings · `1` = high severity findings · `2` = critical severity findings

### vulnerability_assessor.py

| Option | Description |
|--------|-------------|
| `target` | Directory containing dependency files |
| `--severity, -s` | Minimum severity: critical, high, medium, low |
| `--verbose, -v` | Show files as they're scanned |
| `--json` | Output results as JSON |
| `--output, -o` | Write results to file |

**Exit Codes:** `0` = no critical/high vulnerabilities · `1` = high severity vulnerabilities · `2` = critical severity vulnerabilities

### compliance_checker.py

| Option | Description |
|--------|-------------|
| `target` | Directory to check |
| `--framework, -f` | Framework: soc2, pci-dss, hipaa, gdpr, all |
| `--verbose, -v` | Show checks as they run |
| `--json` | Output results as JSON |
| `--output, -o` | Write results to file |

**Exit Codes:** `0` = compliant (90%+ score) · `1` = non-compliant (50-69% score) · `2` = critical gaps (<50% score)

---

## Security Standards

See `references/security_standards.md` for OWASP Top 10 full guidance, secure coding standards, authentication requirements, and API security controls.

### Secure Coding Checklist

```markdown
## Input Validation
- [ ] Validate all input on server side
- [ ] Use allowlists over denylists
- [ ] Sanitize for specific context (HTML, SQL, shell)

## Output Encoding
- [ ] HTML encode for browser output
- [ ] URL encode for URLs
- [ ] JavaScript encode for script contexts

## Authentication
- [ ] Use bcrypt/argon2 for passwords
- [ ] Implement MFA for sensitive operations
- [ ] Enforce strong password policy

## Session Management
- [ ] Generate secure random session IDs
- [ ] Set HttpOnly, Secure, SameSite flags
- [ ] Implement session timeout (15 min idle)

## Error Handling
- [ ] Log errors with context (no secrets)
- [ ] Return generic messages to users
- [ ] Never expose stack traces in production

## Secrets Management
- [ ] Use environment variables or secrets manager
- [ ] Never commit secrets to version control
- [ ] Rotate credentials regularly
```

---

## Compliance Frameworks

See `references/compliance_requirements.md` for full control mappings. Run `compliance_checker.py` to verify the controls below:

### SOC 2 Type II
- **CC6** Logical Access: authentication, authorization, MFA
- **CC7** System Operations: monitoring, logging, incident response
- **CC8** Change Management: CI/CD, code review, deployment controls

### PCI-DSS v4.0
- **Req 3/4**: Encryption at rest and in transit (TLS 1.2+)
- **Req 6**: Secure development (input validation, secure coding)
- **Req 8**: Strong authentication (MFA, password policy)
- **Req 10/11**: Audit logging, SAST/DAST/penetration testing

### HIPAA Security Rule
- Unique user IDs and audit trails for PHI access (164.312(a)(1), 164.312(b))
- MFA for person/entity authentication (164.312(d))
- Transmission encryption via TLS (164.312(e)(1))

### GDPR
- **Art 25/32**: Privacy by design, encryption, pseudonymization
- **Art 33**: Breach notification within 72 hours
- **Art 17/20**: Right to erasure and data portability

---

## Best Practices

### Secrets Management

```python
# BAD: Hardcoded secret
API_KEY = "sk-1234567890abcdef"

# GOOD: Environment variable
import os
API_KEY = os.environ.get("API_KEY")

# BETTER: Secrets manager
from your_vault_client import get_secret
API_KEY = get_secret("api/key")
```

### SQL Injection Prevention

```python
# BAD: String concatenation
query = f"SELECT * FROM users WHERE id = {user_id}"

# GOOD: Parameterized query
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### XSS Prevention

```javascript
// BAD: Direct innerHTML assignment is vulnerable
// GOOD: Use textContent (auto-escaped)
element.textContent = userInput;

// GOOD: Use sanitization library for HTML
import DOMPurify from 'dompurify';
const safeHTML = DOMPurify.sanitize(userInput);
```

### Authentication

```javascript
// Password hashing
const bcrypt = require('bcrypt');
const SALT_ROUNDS = 12;

// Hash password
const hash = await bcrypt.hash(password, SALT_ROUNDS);

// Verify password
const match = await bcrypt.compare(password, hash);
```

### Security Headers

```javascript
// Express.js security headers
const helmet = require('helmet');
app.use(helmet());

// Or manually set headers:
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  res.setHeader('Content-Security-Policy', "default-src 'self'");
  next();
});
```

---

## Reference Documentation

| Document | Description |
|----------|-------------|
| `references/security_standards.md` | OWASP Top 10, secure coding, authentication, API security |
| `references/vulnerability_management_guide.md` | CVE triage, CVSS scoring, remediation workflows |
| `references/compliance_requirements.md` | SOC 2, PCI-DSS, HIPAA, GDPR full control mappings |
