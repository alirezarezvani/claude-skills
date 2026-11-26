# DORA register of information and ICT third-party contracts

> Rules last verified 2026-11-26 (2025/532, CTPP list and pending amendments added; in-force rules unchanged since 2026-11-17) against the EUR-Lex texts cited below. Re-check before relying on a deadline or threshold.

Confidence: 🟢 legal text · 🟡 ESA guidance or Q&A · 🔴 our reading, typical evidence only

## The register (Art 28(3))

Every financial entity keeps, at entity and at consolidated level, a register
of all contractual arrangements on the use of ICT services from ICT
third-party service providers, distinguishing those that support critical or
important functions. It reports new arrangements on critical functions and
makes the full register available to the competent authority on request. 🟢
Templates: Implementing Regulation (EU) 2024/2956; providers are identified by
LEI (EUID for some). 🟢 · First collection by the ESAs ran in spring 2025. 🟡

## Before signing (Art 28(4)-(5))

Assess whether the arrangement covers a critical or important function, check
supervisory conditions, identify and assess risks incl. concentration, do due
diligence on the provider, identify conflicts of interest. Contract only with
providers meeting appropriate information-security standards. 🟢

## What every contract must contain (Art 30(2))

| | Term |
|---|---|
| (a) | clear description of all functions and services, incl. whether subcontracting of critical functions is allowed and on what conditions |
| (b) | locations of service and data processing, and notice of changes |
| (c) | availability, authenticity, integrity and confidentiality of data, incl. personal data |
| (d) | access, recovery and return of data on insolvency, resolution, discontinuation or termination |
| (e) | service level descriptions and updates |
| (f) | assistance in ICT incidents at no or ex-ante cost |
| (g) | cooperation with competent and resolution authorities |
| (h) | termination rights and minimum notice periods |
| (i) | participation in security awareness and resilience training |
🟢 Art 30(2)

## More for critical or important functions (Art 30(3))

| | Term |
|---|---|
| (a) | full service levels with precise quantitative and qualitative targets |
| (b) | notice periods and reporting obligations to the entity |
| (c) | provider business contingency plans and security measures |
| (d) | participation and cooperation in the entity's TLPT |
| (e) | unrestricted rights of access, inspection and audit |
| (f) | exit strategies, in particular a mandatory adequate transition period |
🟢 Art 30(3)

Also: a documented exit strategy for each such service, realistic, feasible and
adequately tested, with transition plans. 🟢 Art 28(8). The policy on contracts
for critical functions follows Delegated Regulation (EU) 2024/1773. 🟢

## Subcontracting critical or important functions (Art 30(2)(a), 30(5))

Delegated Regulation (EU) 2025/532 sets what you must assess and write into the
contract when an ICT provider may subcontract services that support a critical
or important function. Adopted by the Commission in March 2025 and published
in the OJ in July 2025 🟡 (Norton Rose Fulbright, A&O Shearman and Jones Day,
July 2025). Before allowing subcontracting: a risk assessment covering the
provider's own due diligence and oversight of its subcontractors, concentration
and the location of subcontractors 🟡. In the contract: which services may be
subcontracted and on what conditions, the provider's duty to monitor its
subcontractors, advance notice of material changes, and your right to object
and to terminate if a material change goes ahead or subcontracting happens
without authorisation 🟡. The Commission removed the ESAs' draft article that
would have made financial entities monitor the whole chain themselves 🟡; the
duty to know the chain stays, through the provider and the register's
subcontractor rows (2024/2956). Read the regulation itself before you redraft
a clause: this summary is from law-firm briefings. `register_of_information_check.py`
does not test these terms. 🔴

## Concentration and third countries (Art 29)

Assess whether a contract makes you dependent on a provider that is not easily
substitutable, or creates multiple arrangements with the same or closely
connected providers. With third-country providers and subcontracting chains,
weigh insolvency law, data recovery and supervisory access. 🟢 Art 29(1)-(2)

## How the checker reads "present"

A term counts as present when your CSV lists its letter. It does not read the
contract: a lawyer or contract manager confirms each letter against the clause.
That is the evidence an auditor asks for. 🔴

## Sources

1. Regulation (EU) 2022/2554, Arts 28-30 — https://eur-lex.europa.eu/eli/reg/2022/2554/oj
2. Commission Implementing Regulation (EU) 2024/2956 (register templates) — https://eur-lex.europa.eu/eli/reg_impl/2024/2956/oj
3. Commission Delegated Regulation (EU) 2024/1773 (contractual policy) — https://eur-lex.europa.eu/eli/reg_del/2024/1773/oj
4. EBA, register of information reporting pages 🟡 — https://www.eba.europa.eu/
5. EIOPA, DORA pages 🟡 — https://www.eiopa.europa.eu/digital-operational-resilience-act-dora_en
6. ESMA, DORA pages 🟡 — https://www.esma.europa.eu/
7. Commission Delegated Regulation (EU) 2025/532 (subcontracting ICT services supporting critical or important functions) — https://eur-lex.europa.eu/eli/reg_del/2025/532/oj; summaries by Norton Rose Fulbright and Jones Day (July 2025) 🟡
