---
name: senior-security
description: Security engineering toolkit for threat modeling, vulnerability analysis, secure architecture, and penetration testing. Includes STRIDE analysis, OWASP guidance, cryptography patterns, and security scanning tools.
triggers:
  - security architecture
  - threat modeling
  - STRIDE analysis
  - penetration testing
  - vulnerability assessment
  - secure coding
  - OWASP
  - application security
  - cryptography implementation
  - secret scanning
  - security audit
  - zero trust
---

# Senior Security Engineer

Security engineering tools for threat modeling, vulnerability analysis, secure architecture design, and penetration testing.

---

## Table of Contents

- [Threat Modeling Workflow](#threat-modeling-workflow)
- [Security Architecture Workflow](#security-architecture-workflow)
- [Vulnerability Assessment Workflow](#vulnerability-assessment-workflow)
- [Secure Code Review Workflow](#secure-code-review-workflow)
- [Incident Response Workflow](#incident-response-workflow)
- [Security Tools Reference](#security-tools-reference)
- [Tools and References](#tools-and-references)

---

## Threat Modeling Workflow

Identify and analyze security threats using STRIDE methodology.

### Workflow: Conduct Threat Model

1. Define system scope and boundaries:
   - Identify assets to protect
   - Map trust boundaries
   - Document data flows
2. Create data flow diagram:
   - External entities (users, services)
   - Processes (application components)
   - Data stores (databases, caches)
   - Data flows (APIs, network connections)
3. Apply STRIDE to each DFD element:
   - Spoofing: Can identity be faked?
   - Tampering: Can data be modified?
   - Repudiation: Can actions be denied?
   - Information Disclosure: Can data leak?
   - Denial of Service: Can availability be affected?
   - Elevation of Privilege: Can access be escalated?
4. Score risks using DREAD:
   - Damage potential (1-10)
   - Reproducibility (1-10)
   - Exploitability (1-10)
   - Affected users (1-10)
   - Discoverability (1-10)
5. Prioritize threats by risk score
6. Define mitigations for each threat
7. Document in threat model report
8. **Validation:** All DFD elements analyzed; STRIDE applied; threats scored; mitigations mapped

### STRIDE Threat Categories

| Category | Description | Security Property | Mitigation Focus |
|----------|-------------|-------------------|------------------|
| Spoofing | Impersonating users or systems | Authentication | MFA, certificates, strong auth |
| Tampering | Modifying data or code | Integrity | Signing, checksums, validation |
| Repudiation | Denying actions | Non-repudiation | Audit logs, digital signatures |
| Information Disclosure | Exposing data | Confidentiality | Encryption, access controls |
| Denial of Service | Disrupting availability | Availability | Rate limiting, redundancy |
| Elevation of Privilege | Gaining unauthorized access | Authorization | RBAC, least privilege |

### STRIDE per Element Matrix

| DFD Element | S | T | R | I | D | E |
|-------------|---|---|---|---|---|---|
| External Entity | X | | X | | | |
| Process | X | X | X | X | X | X |
| Data Store | | X | X | X | X | |
| Data Flow | | X | | X | X | |

See: [references/threat-modeling-guide.md](references/threat-modeling-guide.md)

---

## Security Architecture Workflow

Design secure systems using defense-in-depth principles.

### Workflow: Design Secure Architecture

1. Define security requirements:
   - Compliance requirements (GDPR, HIPAA, PCI-DSS)
   - Data classification (public, internal, confidential, restricted)
   - Threat model inputs
2. Apply defense-in-depth layers:
   - Perimeter: WAF, DDoS protection, rate limiting
   - Network: Segmentation, IDS/IPS, mTLS
   - Host: Patching, EDR, hardening
   - Application: Input validation, authentication, secure coding
   - Data: Encryption at rest and in transit
3. Implement Zero Trust principles:
   - Verify explicitly (every request)
   - Least privilege access (JIT/JEA)
   - Assume breach (segment, monitor)
4. Configure authentication and authorization:
   - Identity provider selection
   - MFA requirements
   - RBAC/ABAC model
5. Design encryption strategy:
   - Key management approach
   - Algorithm selection
   - Certificate lifecycle
6. Plan security monitoring:
   - Log aggregation
   - SIEM integration
   - Alerting rules
7. Document architecture decisions
8. **Validation:** Defense-in-depth layers defined; Zero Trust applied; encryption strategy documented; monitoring planned

### Defense-in-Depth Layers

```
Layer 1: PERIMETER
  WAF, DDoS mitigation, DNS filtering, rate limiting

Layer 2: NETWORK
  Segmentation, IDS/IPS, network monitoring, VPN, mTLS

Layer 3: HOST
  Endpoint protection, OS hardening, patching, logging

Layer 4: APPLICATION
  Input validation, authentication, secure coding, SAST

Layer 5: DATA
  Encryption at rest/transit, access controls, DLP, backup
```

### Authentication Pattern Selection

| Use Case | Recommended Pattern |
|----------|---------------------|
| Web application | OAuth 2.0 + PKCE with OIDC |
| API authentication | JWT with short expiration + refresh tokens |
| Service-to-service | mTLS with certificate rotation |
| CLI/Automation | API keys with IP allowlisting |
| High security | FIDO2/WebAuthn hardware keys |

See: [references/security-architecture-patterns.md](references/security-architecture-patterns.md)

---

## Vulnerability Assessment Workflow

Identify and remediate security vulnerabilities in applications.

### Workflow: Conduct Vulnerability Assessment

1. Define assessment scope:
   - In-scope systems and applications
   - Testing methodology (black box, gray box, white box)
   - Rules of engagement
2. Gather information:
   - Technology stack inventory
   - Architecture documentation
   - Previous vulnerability reports
3. Perform automated scanning:
   - SAST (static analysis)
   - DAST (dynamic analysis)
   - Dependency scanning
   - Secret detection
4. Conduct manual testing:
   - Business logic flaws
   - Authentication bypass
   - Authorization issues
   - Injection vulnerabilities
5. Classify findings by severity:
   - Critical: Immediate exploitation risk
   - High: Significant impact, easier to exploit
   - Medium: Moderate impact or difficulty
   - Low: Minor impact
6. Develop remediation plan:
   - Prioritize by risk
   - Assign owners
   - Set deadlines
7. Verify fixes and document
8. **Validation:** Scope defined; automated and manual testing complete; findings classified; remediation tracked

### OWASP Top 10 Mapping

| Rank | Vulnerability | Testing Approach |
|------|---------------|------------------|
| A01 | Broken Access Control | Manual IDOR testing, authorization checks |
| A02 | Cryptographic Failures | Algorithm review, key management audit |
| A03 | Injection | SAST + manual payload testing |
| A04 | Insecure Design | Threat modeling, architecture review |
| A05 | Security Misconfiguration | Configuration audit, CIS benchmarks |
| A06 | Vulnerable Components | Dependency scanning, CVE monitoring |
| A07 | Authentication Failures | Password policy, session management review |
| A08 | Software/Data Integrity | CI/CD security, code signing verification |
| A09 | Logging Failures | Log review, SIEM configuration check |
| A10 | SSRF | Manual URL manipulation testing |

### Vulnerability Severity Matrix

| Impact / Exploitability | Easy | Moderate | Difficult |
|-------------------------|------|----------|-----------|
| Critical | Critical | Critical | High |
| High | Critical | High | Medium |
| Medium | High | Medium | Low |
| Low | Medium | Low | Low |

---

## Secure Code Review Workflow

Review code for security vulnerabilities before deployment.

### Workflow: Conduct Security Code Review

1. Establish review scope:
   - Changed files and functions
   - Security-sensitive areas (auth, crypto, input handling)
   - Third-party integrations
2. Run automated analysis:
   - SAST tools (Semgrep, CodeQL, Bandit)
   - Secret scanning
   - Dependency vulnerability check
3. Review authentication code:
   - Password handling (hashing, storage)
   - Session management
   - Token validation
4. Review authorization code:
   - Access control checks
   - RBAC implementation
   - Privilege boundaries
5. Review data handling:
   - Input validation
   - Output encoding
   - SQL query construction
   - File path handling
6. Review cryptographic code:
   - Algorithm selection
   - Key management
   - Random number generation
7. Document findings with severity
8. **Validation:** Automated scans passed; auth/authz reviewed; data handling checked; crypto verified; findings documented

### Security Code Review Checklist

| Category | Check | Risk |
|----------|-------|------|
| Input Validation | All user input validated and sanitized | Injection |
| Output Encoding | Context-appropriate encoding applied | XSS |
| Authentication | Passwords hashed with Argon2/bcrypt | Credential theft |
| Session | Secure cookie flags set (HttpOnly, Secure, SameSite) | Session hijacking |
| Authorization | Server-side permission checks on all endpoints | Privilege escalation |
| SQL | Parameterized queries used exclusively | SQL injection |
| File Access | Path traversal sequences rejected | Path traversal |
| Secrets | No hardcoded credentials or keys | Information disclosure |
| Dependencies | Known vulnerable packages updated | Supply chain |
| Logging | Sensitive data not logged | Information disclosure |

### Secure vs Insecure Patterns

| Pattern | Issue | Secure Alternative |
|---------|-------|-------------------|
| SQL string formatting | SQL injection | Use parameterized queries with placeholders |
| Shell command building | Command injection | Use subprocess with argument lists, no shell |
| Path concatenation | Path traversal | Validate and canonicalize paths |
| MD5/SHA1 for passwords | Weak hashing | Use Argon2id or bcrypt |
| Math.random for tokens | Predictable values | Use crypto.getRandomValues |

---

## Incident Response Workflow

Respond to and contain security incidents.

### Workflow: Handle Security Incident

1. Identify and triage:
   - Validate incident is genuine
   - Assess initial scope and severity
   - Activate incident response team
2. Contain the threat:
   - Isolate affected systems
   - Block malicious IPs/accounts
   - Disable compromised credentials
3. Eradicate root cause:
   - Remove malware/backdoors
   - Patch vulnerabilities
   - Update configurations
4. Recover operations:
   - Restore from clean backups
   - Verify system integrity
   - Monitor for recurrence
5. Conduct post-mortem:
   - Timeline reconstruction
   - Root cause analysis
   - Lessons learned
6. Implement improvements:
   - Update detection rules
   - Enhance controls
   - Update runbooks
7. Document and report
8. **Validation:** Threat contained; root cause eliminated; systems recovered; post-mortem complete; improvements implemented

### Incident Severity Levels

| Level | Description | Response Time | Escalation |
|-------|-------------|---------------|------------|
| P1 - Critical | Active breach, data exfiltration | Immediate | CISO, Legal, Executive |
| P2 - High | Confirmed compromise, contained | 1 hour | Security Lead, IT Director |
| P3 - Medium | Potential compromise, under investigation | 4 hours | Security Team |
| P4 - Low | Suspicious activity, low impact | 24 hours | On-call engineer |

### Incident Response Checklist

| Phase | Actions |
|-------|---------|
| Identification | Validate alert, assess scope, determine severity |
| Containment | Isolate systems, preserve evidence, block access |
| Eradication | Remove threat, patch vulnerabilities, reset credentials |
| Recovery | Restore services, verify integrity, increase monitoring |
| Lessons Learned | Document timeline, identify gaps, update procedures |

---

## Security Tools Reference

### Recommended Security Tools

| Category | Tools |
|----------|-------|
| SAST | Semgrep, CodeQL, Bandit (Python), ESLint security plugins |
| DAST | OWASP ZAP, Burp Suite, Nikto |
| Dependency Scanning | Snyk, Dependabot, npm audit, pip-audit |
| Secret Detection | GitLeaks, TruffleHog, detect-secrets |
| Container Security | Trivy, Clair, Anchore |
| Infrastructure | Checkov, tfsec, ScoutSuite |
| Network | Wireshark, Nmap, Masscan |
| Penetration | Metasploit, sqlmap, Burp Suite Pro |

### Cryptographic Algorithm Selection

| Use Case | Algorithm | Key Size |
|----------|-----------|----------|
| Symmetric encryption | AES-256-GCM | 256 bits |
| Password hashing | Argon2id | N/A (use defaults) |
| Message authentication | HMAC-SHA256 | 256 bits |
| Digital signatures | Ed25519 | 256 bits |
| Key exchange | X25519 | 256 bits |
| TLS | TLS 1.3 | N/A |

See: [references/cryptography-implementation.md](references/cryptography-implementation.md)

---

## Tools and References

### Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| [threat_modeler.py](scripts/threat_modeler.py) | STRIDE threat analysis with risk scoring | `python threat_modeler.py --component "Authentication"` |
| [secret_scanner.py](scripts/secret_scanner.py) | Detect hardcoded secrets and credentials | `python secret_scanner.py /path/to/project` |

**Threat Modeler Features:**
- STRIDE analysis for any system component
- DREAD risk scoring
- Mitigation recommendations
- JSON and text output formats
- Interactive mode for guided analysis

**Secret Scanner Features:**
- Detects AWS, GCP, Azure credentials
- Finds API keys and tokens (GitHub, Slack, Stripe)
- Identifies private keys and passwords
- Supports 20+ secret patterns
- CI/CD integration ready

### References

| Document | Content |
|----------|---------|
| [security-architecture-patterns.md](references/security-architecture-patterns.md) | Zero Trust, defense-in-depth, authentication patterns, API security |
| [threat-modeling-guide.md](references/threat-modeling-guide.md) | STRIDE methodology, attack trees, DREAD scoring, DFD creation |
| [cryptography-implementation.md](references/cryptography-implementation.md) | AES-GCM, RSA, Ed25519, password hashing, key management |

---

## Security Standards Reference

### Compliance Frameworks

| Framework | Focus | Applicable To |
|-----------|-------|---------------|
| OWASP ASVS | Application security | Web applications |
| CIS Benchmarks | System hardening | Servers, containers, cloud |
| NIST CSF | Risk management | Enterprise security programs |
| PCI-DSS | Payment card data | Payment processing |
| HIPAA | Healthcare data | Healthcare applications |
| SOC 2 | Service organization controls | SaaS providers |

### Security Headers Checklist

| Header | Recommended Value |
|--------|-------------------|
| Content-Security-Policy | default-src self; script-src self |
| X-Frame-Options | DENY |
| X-Content-Type-Options | nosniff |
| Strict-Transport-Security | max-age=31536000; includeSubDomains |
| Referrer-Policy | strict-origin-when-cross-origin |
| Permissions-Policy | geolocation=(), microphone=(), camera=() |

---

## Related Skills

| Skill | Integration Point |
|-------|-------------------|
| [senior-devops](../senior-devops/) | CI/CD security, infrastructure hardening |
| [senior-secops](../senior-secops/) | Security monitoring, incident response |
| [senior-backend](../senior-backend/) | Secure API development |
| [senior-architect](../senior-architect/) | Security architecture decisions |
