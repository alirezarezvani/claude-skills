# AppSec Code Review Workflow

## Pre-Review

1. Identify the scope: which files changed, what endpoints affected
2. Review associated threat model or design doc if available
3. Check if any high-risk areas (auth, payment, PII handling) are changed

## Phase 1: OWASP Top 10 Scan

For each changed file:
1. Check A01: Are authorization checks present on all state-changing operations?
2. Check A02: Are cryptographic functions using approved algorithms (AES-256, SHA-256+)?
3. Check A03: Are all database queries parameterized? Any template injection risk?
4. Check A05: No debug flags, default credentials, or exposed admin endpoints?
5. Check A07: Session tokens generated securely? Passwords hashed with bcrypt/argon2?

## Phase 2: Dependency Review

1. List all added/changed dependencies
2. Check each against CVE databases for known vulnerabilities
3. Flag any dependencies with CVSS >= 7.0

## Phase 3: Logic Flaw Review

1. Review business logic for trust boundary violations
2. Check for IDOR: can user A access user B's data by changing an ID?
3. Review rate limiting on sensitive endpoints

## Phase 4: Finding Documentation

1. Document each finding with: file, line number, CWE, severity, remediation
2. Map to OWASP Top 10 category
3. Draft developer-friendly remediation message
4. Apply gate decision logic

## Phase 5: Report

Produce structured JSON output with all findings, gate decision, and escalation recommendations.
