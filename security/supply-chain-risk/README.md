# supply-chain-risk

**Level:** L3 (SOC) | **Category:** Risk | **Intent:** `read_only` (SBOM analysis, auditing) + `mutating/policy_change` (package blocking)

Principal supply chain security engineer that evaluates software and hardware supply chain dependencies, detects malicious package injection across 5 attack categories, and assesses build pipeline integrity against the SLSA framework (Levels 0-4). Generates SBOM analysis for direct and transitive dependencies with CVE, CISA KEV, license risk, and abandonment scoring. Blocking compromised packages in registry policy requires human approval.

---

## When to trigger

- Dependency file change in source control (package.json, requirements.txt, go.mod, pom.xml)
- New CVE disclosed affecting a known dependency
- Suspicious package version bump: new maintainer, unexplained binary additions, obfuscated code
- CI/CD pipeline security event (compromised token, unauthorized runner, unexpected artifact)
- `sast-dast-coordinator` SCA scan reports a high-risk transitive dependency

---

## Attack categories detected

| Category | Indicators |
|---|---|
| Dependency confusion | Internal package name available on public registry; public version higher than internal |
| Typosquatting | Package name differs from popular package by 1-2 characters or transposition |
| Malicious maintainer takeover | Account ownership transfer; new maintainer with no history |
| Build pipeline compromise | Unauthorized changes to CI/CD scripts; compromised signing keys |
| Hardware supply chain | Unexpected firmware, modified hardware components (for IoT/OT scope) |

---

## Key outputs

| Field | Type | Description |
|---|---|---|
| `sbom_summary` | object | Total components, CVE count, CISA KEV count, abandoned packages, license violations |
| `high_risk_packages` | array | Package, version, risk type, severity, CVE ID, recommended action |
| `build_integrity_score` | int (0-100) | SLSA level assessment and checklist results |
| `blocking_required` | bool | Whether registry block is recommended (triggers mutating/policy_change) |
| `license_risk_matrix` | array | License type, copyleft risk, commercial risk per dependency |

---

## Intent classification

```
SBOM analysis, dependency auditing, CVE correlation, license review, SLSA assessment
  -> read_only

Blocking compromised packages in registry policy
  -> mutating/policy_change (approver: security_director)
```

---

## Works with

**Upstream:** `devsecops-pipeline` (build events), `sast-dast-coordinator` (SCA scan results)

**Downstream:** `vulnerability-management` (CVEs in dependencies), `findings-tracker`, `third-party-vendor-risk` (vendor package assessment), `build-integrity` (build pipeline security)

---

## Standalone use

```bash
cat supply-chain-risk/SKILL.md
# Paste into system prompt, then send a dependency event:

{
  "event_type": "supply_chain_attack",
  "severity": "high",
  "raw_payload": {
    "package_name": "event-stream",
    "ecosystem": "npm",
    "version": "3.3.6",
    "maintainer_changed_days_ago": 5,
    "new_dependency_added": "flatmap-stream",
    "flatmap_stream_downloads_last_week": 2000000,
    "suspicious_indicators": ["new_maintainer", "obfuscated_code", "unexpected_dependency"]
  }
}
```

---

## Runtime Contract

- ../../agents/supply-chain-risk.yaml
