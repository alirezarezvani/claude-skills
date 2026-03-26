# Output Routing and Context Discovery

## Output Routing

| Document Type | Detected Condition | Route To |
|---|---|---|
| Architecture Doc | Any finding | `risk-threat-modeling` |
| PRD / Requirements | PCI, GDPR, HIPAA, SOC2, FedRAMP keywords | `compliance-mapping` |
| PRD / Requirements | Code/pipeline references | `pipeline-security-scan` |
| PRD / Requirements | General product requirements | `appsec-code-review` |
| POA&M | Control deficiency gaps | `compliance-mapping` |
| Any | Critical gap (no auth, hardcoded creds) | `cs-security-analyst` (via alert triage) |

## Context Discovery

Before prompting for input, check for context sources in this order:

1. **`security-context.md`** — Apply environment type, regulatory scope, and approved tooling to analysis context.
2. **`metadata.context_file`** — If frontmatter specifies a context_file, read and apply relevant fields.

Announce discovered context: "Found security-context.md — applying [regulatory_scope], [environment_type]."

## Output Artifacts

| When operator asks for... | You produce... |
|---|---|
| Security review of this PRD | Structured JSON output with all critical_gaps, design_findings, missing_controls, and routing recommendations |
| What are the threat vectors? | MITRE ATT&CK technique list with document evidence references for each technique |
| What's missing for compliance? | Compliance gap table: regulation → requirement → gap → recommended control |
| Summary for the eng team | Human-readable finding list with severity, location in document, and remediation guidance |
