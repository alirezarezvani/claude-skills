---
title: "Senior Security Engineer — Threat Modeling + Security Router — Agent Skill & Codex Plugin"
description: "Use when the user asks for STRIDE threat modeling, DREAD risk scoring, data-flow-diagram threat analysis, or a quick secret scan — or when a security. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Senior Security Engineer — Threat Modeling + Security Router

<div class="page-meta" markdown>
<span class="meta-badge">:material-code-braces: Engineering - Core</span>
<span class="meta-badge">:material-identifier: `senior-security`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/skills/senior-security/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install engineering-skills</code>
</div>


This skill does exactly one job itself — **STRIDE/DREAD threat modeling** (plus a quick secret scan) — and routes every other security request to the specialist skill that owns that lane. Do not duplicate sibling content here; route instead.

## Routing Table (read this first)

| The user wants... | Route to | Why that skill owns it |
|---|---|---|
| Vulnerability assessment, pen-test methodology, OWASP Top 10 testing | [`skills/security-pen-testing`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/skills/security-pen-testing) | Ships `vulnerability_scanner.py` + `dependency_auditor.py` with exit-code contracts |
| Incident triage, SEV classification, forensics, containment | [`skills/incident-response`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/skills/incident-response) | SEV1–SEV4 taxonomy, NIST SP 800-61 phases, `incident_triage.py` |
| Production outage command (non-security incidents) | [`skills/incident-commander`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/skills/incident-commander) | Severity classifier + timeline + postmortem tools |
| Security monitoring, CVE triage SLAs, compliance checks (SOC 2 etc.), security headers | [`skills/senior-secops`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/skills/senior-secops) | `security_scanner.py` + `compliance_checker.py`, CVE SLA table |
| Hostile/adversarial code review | [`skills/adversarial-reviewer`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/skills/adversarial-reviewer) | 3-persona review with BLOCK/CONCERNS/CLEAN verdict |
| Secure code review as part of general review | [`skills/code-reviewer`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/skills/code-reviewer) | Language dispatch + regression fixtures |
| Cloud IAM escalation paths, S3 exposure, security groups | [`skills/cloud-security`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/skills/cloud-security) | `cloud_posture_check.py` with per-check exit codes |
| Threat hunting, IOC sweeps, anomaly detection | [`skills/threat-detection`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/skills/threat-detection) | z-score anomaly + IOC staleness tooling |
| Red-team engagement planning, ATT&CK kill chains | [`skills/red-team`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/skills/red-team) | `engagement_planner.py` with authorization gate |
| LLM/AI attack surface (prompt injection, poisoning) | [`skills/ai-security`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/skills/ai-security) | ATLAS-mapped `ai_threat_scanner.py` |

If the request spans lanes (e.g., "secure this new architecture"), do the threat model here first — its output (prioritized threats + mitigations) tells you which siblings to load next. Never bulk-load multiple security skills speculatively.

## What This Skill Owns: STRIDE Threat Modeling

### Workflow

1. **Scope:** assets to protect, trust boundaries, data flows (external entities, processes, data stores, flows).
2. **Generate the threat model** per component:
   ```bash
   python3 scripts/threat_modeler.py --component "User Authentication" --assets "credentials,sessions" --json --output threats.json
   ```
   Output: per-threat STRIDE category, DREAD score (Damage, Reproducibility, Exploitability, Affected users, Discoverability — each 1–10), and suggested mitigations. Repeat per DFD element; `--interactive` walks scoping questions; `--list-threats` shows the threat database.
3. **Consume the output:** sort `threats.json` by DREAD score descending; everything ≥ 7 average needs a named mitigation owner before the design ships. Map each mitigation to the responsible sibling lane (e.g., IAM threats → `cloud-security`, injection threats → `code-reviewer`).
4. **Quick secret sweep** while you have the codebase open:
   ```bash
   python3 scripts/secret_scanner.py /path/to/project --format json --severity high
   ```
   20+ patterns (AWS keys, GitHub tokens, private keys, generic credentials). Any critical/high finding blocks merge until rotated and moved to a secret manager.
5. **Verification gate:** every DFD element has ≥ 1 STRIDE row considered, every threat with DREAD ≥ 7 has an owner + mitigation, and the secret scan exits with zero high/critical findings. Re-run both tools after mitigations land — that re-run is the done signal, not the document.

### STRIDE per Element Matrix

| DFD Element | S | T | R | I | D | E |
|-------------|---|---|---|---|---|---|
| External Entity | X | | X | | | |
| Process | X | X | X | X | X | X |
| Data Store | | X | X | X | X | |
| Data Flow | | X | | X | X | |

(S=Spoofing→authn, T=Tampering→integrity, R=Repudiation→audit logs, I=Info Disclosure→encryption/access control, D=DoS→rate limiting/redundancy, E=Elevation→least privilege.)

## References (load on demand)

| Document | Content |
|----------|---------|
| [references/threat-modeling-guide.md](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/skills/senior-security/references/threat-modeling-guide.md) | STRIDE methodology, attack trees, DREAD scoring, DFD creation |
| [references/security-architecture-patterns.md](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/skills/senior-security/references/security-architecture-patterns.md) | Zero Trust, defense-in-depth, authentication patterns, API security |
| [references/cryptography-implementation.md](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/skills/senior-security/references/cryptography-implementation.md) | AES-GCM, Ed25519, password hashing (Argon2id), key management |

The architecture and crypto references are kept because no sibling ships them; for *operating* those controls (scanning, compliance, monitoring) still route to `senior-secops`.
