---
name: "senior-secops"
description: "Find and fix application security problems: security reviews, CVE remediation, hardening, secrets and auth, SOC 2, PCI-DSS, HIPAA and GDPR checks. Use whenever the user asks if their app is secure, needs to patch a vulnerable dependency or prepares for an audit."
---

# Senior SecOps Engineer

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

Steps and scoring rules are in `references/vulnerability_management_guide.md` (section Workflow 3: CVE Triage). Use `vulnerability_assessor.py` to score each CVE.

### Workflow 4: Incident Response

The incident response steps are in `references/vulnerability_management_guide.md` (section Workflow 4: Incident Response).

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

The secure coding checklist (input validation, output encoding, authentication, session, error handling, secrets) is in `references/security_standards.md` (section Secure Coding Checklist).

---

## Compliance Frameworks

See `references/compliance_requirements.md` for full control mappings. Run `compliance_checker.py` to verify the controls below:

SOC 2, PCI-DSS, HIPAA and GDPR control mappings are in `references/compliance_requirements.md`.

---

## Best Practices

Secure coding examples (secrets, SQL injection, XSS, authentication, security headers) are in `references/security_standards.md` (section Best Practices).

---

## OWASP Top 10 Quick-Check

Categories follow the [OWASP Top 10:2025](https://owasp.org/Top10/2025/). Rapid 15-minute assessment — run through each category and note pass/fail. For deep-dive testing, hand off to the **security-pen-testing** skill.

| # | Category | One-Line Check |
|---|----------|----------------|
| A01 | Broken Access Control | Verify role checks on every endpoint; test horizontal privilege escalation; block SSRF to internal and metadata endpoints (169.254.169.254) |
| A02 | Security Misconfiguration | Check default credentials removed; error pages generic |
| A03 | Software Supply Chain Failures | Run `vulnerability_assessor.py` (zero critical/high CVEs); lockfiles committed; CI actions pinned |
| A04 | Cryptographic Failures | Confirm TLS 1.2+ everywhere; no secrets in logs or source |
| A05 | Injection | Run parameterized query audit; check ORM raw-query usage |
| A06 | Insecure Design | Review threat model exists for critical flows |
| A07 | Authentication Failures | Verify MFA on admin; brute-force protection active |
| A08 | Software or Data Integrity Failures | Confirm CI/CD pipeline signs artifacts; no unsigned deps |
| A09 | Security Logging and Alerting Failures | Validate audit logs capture auth events; alerts configured |
| A10 | Mishandling of Exceptional Conditions | Security checks fail closed on errors and timeouts; no stack traces in responses |

> **Deep dive needed?** Hand off to `security-pen-testing` for full OWASP Testing Guide coverage.

---

## Secret Scanning Tools

Scanner choice for each stage (pre-commit, CI, repository history) is in `references/vulnerability_management_guide.md` (section Secret Scanning Tools).

---

## Supply Chain Security

Supply chain controls (lockfiles, pinned CI actions, signed artifacts) are in `references/vulnerability_management_guide.md` (section Supply Chain Security).

---

## Reference Documentation

| Document | Description |
|----------|-------------|
| `references/security_standards.md` | OWASP Top 10, secure coding, authentication, API security |
| `references/vulnerability_management_guide.md` | CVE triage, CVSS scoring, remediation workflows |
| `references/compliance_requirements.md` | SOC 2, PCI-DSS, HIPAA, GDPR full control mappings |
