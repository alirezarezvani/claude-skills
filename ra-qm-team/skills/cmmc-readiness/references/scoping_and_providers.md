# Scoping and external providers

What `scope_classifier.py` implements. Scope is the biggest cost lever in a
Level 2 assessment: every in-scope asset is assessed or documented, and a
provider that holds CUI brings its own evidence burden.

Confidence key: 🟢 read in the primary source · 🟡 secondary source or recalled, not re-read for this skill · 🔴 our judgment.

## Asset categories (32 CFR 170.19(c)(1), Table 3)

| Category | What it is | OSA must | Assessor does |
|---|---|---|---|
| CUI Asset | Processes, stores or transmits CUI | Inventory, SSP, scope diagram | Assesses all Level 2 requirements |
| Security Protection Asset | Provides security functions to the scope | Same | Assesses the requirements relevant to the capability |
| Contractor Risk Managed Asset | **Can**, but is not intended to, handle CUI because of policies, procedures and practices; need not be separated | Same | Reviews the SSP; may run a limited check that "shall not materially increase the assessment duration nor the assessment cost" |
| Specialized Asset | Can handle CUI but cannot be fully secured: IoT, IIoT, OT, GFE, restricted information systems, test equipment | Same, plus show they are managed under risk-based policy | Reviews the SSP; not assessed against other requirements |
| Out-of-Scope Asset | Cannot handle CUI and protects nothing in scope, or is physically or logically separated | Be ready to justify it | Nothing |

🟢 [170.19] A VDI client configured to pass only keyboard, video and mouse data is
out of scope. 🟢 [170.19] An asset that fits any in-scope category cannot be called
out of scope. 🟢 [170.19]

`scope_classifier.py` applies the categories in this order: specialized type
first, then VDI, then CUI, then security function, then the CRMA test. The order
is ours; the rule describes the categories, not a sequence. 🔴

## Where scoping usually goes wrong

- **A CRMA without the policy.** The category exists only "because of policy, procedures and practices in place". If you cannot point to them, expect the assessor to treat the asset as a CUI asset. 🟢 [170.19] The script asks for `policy_ref`. 🔴
- **An asset in the diagram but not the SSP**, or the reverse. Table 3 asks for all three: inventory, SSP and diagram. The SSP gap also hits CA.L2-3.12.4, which blocks the whole assessment. 🟢 [170.19][170.24]
- **The enclave that leaks.** An enclave narrows scope only if the separation is real. Shared admin accounts, shared identity, or file sync between enclave and corporate network bring the corporate side back in. 🔴 The DoD CMMC Scoping Guide gives the same warning in its examples. 🟡 [ScopeGuide]

## External Service Providers (170.19(c)(2), Table 4)

| Provider holds | Cloud provider (CSP) | Not a CSP |
|---|---|---|
| CUI (with or without SPD) | Must meet the FedRAMP requirements of DFARS 252.204-7012 | Its services are in your scope and assessed with you |
| Security Protection Data only | Assessed as a Security Protection Asset | Assessed as a Security Protection Asset |
| Neither | Not an ESP under CMMC | Not an ESP under CMMC |

🟢 [170.19] The OSA documents each ESP in its SSP, and the ESP's service
description and customer responsibility matrix must match. 🟢 [170.19]

**FedRAMP for a CSP holding CUI.** DFARS 252.204-7012(b)(2)(ii)(D) requires the
CSP to meet security requirements equivalent to the FedRAMP Moderate baseline. 🟡 [7012]
DoD CIO's December 2023 memo on FedRAMP Moderate equivalency says a non-authorized
offering is equivalent only if a FedRAMP-recognized 3PAO assessed it, all controls
in the Moderate baseline are met with no open POA&M items from that assessment, and
the contractor holds the body of evidence (SSP, SAP, SAR, POA&M). The contractor
answers for that evidence. 🟡 [Equiv]

`scope_classifier.py` blocks on a CSP holding CUI with FedRAMP `none` or `unknown`,
and warns on `equivalent` so you go and collect the evidence. 🔴

## Sources

- [170.19] 32 CFR 170.19, CMMC scoping. https://www.law.cornell.edu/cfr/text/32/170.19
- [170.24] 32 CFR 170.24, CMMC Scoring Methodology (SSP rule). https://www.law.cornell.edu/cfr/text/32/170.24
- [7012] DFARS 252.204-7012, Safeguarding Covered Defense Information and Cyber Incident Reporting. https://www.acquisition.gov/dfars/252.204-7012-safeguarding-covered-defense-information-and-cyber-incident-reporting.
- [Equiv] DoD CIO, *FedRAMP Moderate Equivalency for Cloud Service Provider's (CSP) Cloud Service Offerings* (December 2023). Summary used: https://cloudsecurityalliance.org/articles/fedramp-moderate-equivalency-for-cloud-service-providers-explained
- [ScopeGuide] DoD CIO, *CMMC Scoping Guide – Level 2*. https://dodcio.defense.gov/cmmc/Resources-Documentation/
- [800-171] NIST SP 800-171 Rev. 2, §1.1 (scope of the requirements). https://csrc.nist.gov/pubs/sp/800/171/r2/upd1/final
