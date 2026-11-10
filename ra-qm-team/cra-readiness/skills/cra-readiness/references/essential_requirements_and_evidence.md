# Essential requirements and the evidence an assessor asks for

Maps every id in `annex_i_gap_check.py` to its source and to the evidence that
usually closes it. The evidence column is practice, not law 🔴; the requirement
column is 🟢 Regulation (EU) 2024/2847.

## Annex I Part I — properties of the product

Applied "on the basis of the cybersecurity risk assessment referred to in
Article 13(2) and where applicable" 🟢. A requirement you mark not applicable needs
a justification in the technical documentation 🟢 (Art 13(4)).

| Id | Requirement | Typical evidence |
|---|---|---|
| P1-1 | Cybersecurity level appropriate to the risks | Risk assessment (Art 13(2)-(3)), threat model |
| P1-2a | No known exploitable vulnerabilities at release | Release-gate scan against the SBOM, triage log for every open CVE |
| P1-2b | Secure by default, reset to original state | Default-config review, first-boot credential handling, factory-reset test |
| P1-2c | Security updates, automatic by default with opt-out and postponement | Update architecture doc, opt-out UI, notification test |
| P1-2d | Protection from unauthorised access; report possible unauthorised access | AuthN/AuthZ design, brute-force tests, access-failure logging |
| P1-2e | Confidentiality, state-of-the-art encryption at rest and in transit | Crypto inventory, TLS config scan, key management |
| P1-2f | Integrity of data, commands, programs, configuration; report corruption | Secure boot / code signing, config integrity checks |
| P1-2g | Data minimisation | Data inventory per function (shared with the GDPR record) |
| P1-2h | Availability of essential functions, DoS resilience | Load/DoS tests, degraded-mode behaviour |
| P1-2i | Minimise impact on other devices' and networks' availability | Rate limits, retry/backoff design |
| P1-2j | Limit attack surface incl. external interfaces | Port/service inventory, debug interfaces disabled |
| P1-2k | Exploitation mitigation | Compiler hardening, ASLR/DEP/stack protection, sandboxing |
| P1-2l | Record and monitor internal activity, user opt-out | Security event log spec |
| P1-2m | Secure, easy permanent data removal; secure transfer | Wipe procedure, verification test |

## Annex I Part II — vulnerability handling

No "where applicable": every in-scope product, for the whole support period 🟢.

| Id | Requirement | Typical evidence |
|---|---|---|
| P2-1 | Identify components; machine-readable SBOM, at least top-level dependencies | SBOM per release + `sbom_check.py` PASS |
| P2-2 | Remediate without delay; security updates separate where feasible | Patch SLA by severity, release notes split |
| P2-3 | Regular security testing and review | Pen-test reports, SAST/DAST in CI |
| P2-4 | Publicly disclose fixed vulnerabilities after the update | Published advisories (CSAF recommended 🔴) |
| P2-5 | Coordinated vulnerability disclosure policy, enforced | Published CVD policy (ISO/IEC 29147 and 30111 shape it 🔴) |
| P2-6 | Contact address for vulnerability reports | security.txt (RFC 9116), PSIRT mailbox |
| P2-7 | Secure update distribution | Signed updates, delivery channel threat model |
| P2-8 | Updates without delay, free of charge, with advisories | Update policy, advisory template |

## Annex VII — technical documentation (keep 10 years, Art 13(13))

| Id | Content |
|---|---|
| TD-1 | General description: purpose, software versions, hardware photos, Annex II info |
| TD-2 | Design, development, production; vulnerability handling incl. SBOM, CVD policy, contact, update distribution |
| TD-3 | Cybersecurity risk assessment |
| TD-4 | Basis for the support period (Art 13(8)) |
| TD-5 | Standards, common specifications or schemes applied, or the solutions used instead |
| TD-6 | Test reports against Annex I Parts I and II |
| TD-7 | Copy of the EU declaration of conformity |
| TD-8 | SBOM on reasoned request of a market surveillance authority |

## Annex II — user information (keep 10 years or the support period, Art 13(18))

UI-1 manufacturer contact · UI-2 vulnerability single point of contact and CVD
policy location · UI-3 product identification · UI-4 intended purpose and
security properties · UI-5 foreseeable risk circumstances · UI-6 DoC address ·
UI-7 type of support and **end date of the support period** · UI-8 instructions
(secure commissioning, effect of changes, installing updates, secure
decommissioning, turning off automatic updates, integrator information) · UI-9
SBOM location if shared.

## Retention periods 🟢

| What | How long | Article |
|---|---|---|
| Each security update | 10 years after issue, or rest of support period if longer | 13(9) |
| Technical documentation and DoC | 10 years after placing on the market, or support period if longer | 13(13) |
| Annex II user information | same | 13(18) |

## Standards

No CRA harmonised standard was cited in the OJ as of September 2026 🔴 (check
the current list). Until then, use the drafts and established standards as
evidence of "solutions adopted" (TD-5): EN 18031-1/-2/-3 (RED delegated act,
radio equipment), IEC 62443-4-1/-4-2 (industrial), ETSI EN 303 645 (consumer IoT),
ISO/IEC 29147 and 30111 (disclosure and handling). Mapping them is evidence, not
a presumption of conformity 🟢 (presumption only from cited harmonised standards,
Art 27(1)).

## Sources

1. Regulation (EU) 2024/2847, Art 13, Art 27, Art 28, Art 31; Annexes I, II, VII — https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng
2. European Commission, guidance on the application of the CRA, Annex to C(2026) 5252, 27 July 2026
3. ISO/IEC 29147:2018 Vulnerability disclosure; ISO/IEC 30111:2019 Vulnerability handling processes
4. RFC 9116, *A File Format to Aid in Security Vulnerability Disclosure* (security.txt), 2022
5. OASIS CSAF 2.0 (Common Security Advisory Framework), 2022
6. BSI TR-03183-2, *Cyber Resilience Requirements for Manufacturers and Products, Part 2: Software Bill of Materials*
7. NTIA, *The Minimum Elements For a Software Bill of Materials*, July 2021
8. ETSI EN 303 645 (consumer IoT); IEC 62443-4-1 and 4-2; EN 18031 series
