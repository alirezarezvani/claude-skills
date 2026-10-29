# Level 2 scoring, POA&M and status

What `sprs_score.py` and `poam_closeout.py` implement, with the paragraph each
rule comes from.

Confidence key: 🟢 read in the primary source · 🟡 secondary source or recalled, not re-read for this skill · 🔴 our judgment.

## Where CMMC sits in a contract

- The program rule is 32 CFR Part 170; the contract clause rule is 48 CFR (DFARS) parts 204, 212, 217 and 252, published 10 September 2025 and enforceable from **10 November 2025**. 🟡 [DFARS-FR]
- Rollout runs in four phases, each starting one year after the last (32 CFR 170.3(e)). 🟢 [170.3]
  - **Phase 1 (from 10 Nov 2025):** Level 1 (Self) or Level 2 (Self) as a condition of award. DoD may ask for Level 2 (C3PAO) instead.
  - **Phase 2 (from 10 Nov 2026):** adds Level 2 (C3PAO) as a condition of award; may be deferred to an option period.
  - **Phase 3 (from 10 Nov 2027):** Level 2 (C3PAO) for all applicable solicitations and options; Level 3 (DIBCAC) planned.
  - **Phase 4 (from 10 Nov 2028):** everything, including options on older contracts.
- The dates are derived from the 10 November 2025 start and the one-year steps. 🔴 Check the solicitation: it names the level and assessment type.

## The score (32 CFR 170.24(c)(2))

- Start at 110, one per NIST SP 800-171 Rev 2 requirement. Subtract for each NOT MET requirement. 🟢 [170.24]
- **5 points:** requirements whose absence could lead to significant exploitation of the network or exfiltration of CUI (42 fixed, plus 3.5.3 and 3.13.11 at full deduction). 🟢 [170.24]
- **3 points:** a specific, confined effect on the network and its data (14). 🟢 [170.24]
- **1 point:** the rest, with limited or indirect effect (51). 🟢 [170.24]
- **Partial credit, two requirements only:** IA.L2-3.5.3 costs 3 when MFA covers remote and privileged users only, 5 when it is not implemented; SC.L2-3.13.11 costs 3 when CUI is encrypted without FIPS-validated cryptography, 5 when it is not encrypted. 🟢 [170.24]
- **CA.L2-3.12.4 (the SSP) has no point value.** Without a current SSP the assessment cannot be completed. 🟢 [170.24] So the lowest possible score is 110 − 313 = **−203**, which matches the SPRS range. 🟡 [DoDAM]
- A requirement is MET only when all of its assessment objectives in NIST SP 800-171A are satisfied; Level 2 has 320 of them. A self-assessment that marks requirements MET without checking each objective overstates the score. 🟡 [171A]
- NOT APPLICABLE counts as MET. An enduring exception or a temporary deficiency on an operational plan of action, written into the SSP with its mitigations, is also assessed as MET. 🟢 [170.24] The assessor still has to accept the reason, so `sprs_score.py` flags an NA with no justification. 🔴
- The Basic self-assessment score that DFARS 252.204-7019/-7020 asks contractors to post in SPRS uses the same DoD Assessment Methodology weights. 🟡 [DoDAM]

## POA&M rules (32 CFR 170.21)

- A Level 2 POA&M is allowed only if **score ÷ 110 ≥ 0.8**, which is 88 or more. 🟢 [170.21]
- Only requirements worth **1 point** may be on it, with one exception: SC.L2-3.13.11 when encryption is used but not FIPS-validated (3 points). 🟢 [170.21]
- **Never on a POA&M:** AC.L2-3.1.20 (external connections), AC.L2-3.1.22 (public posting), CA.L2-3.12.4 (SSP), PE.L2-3.10.3 (escort visitors), PE.L2-3.10.4 (physical access logs), PE.L2-3.10.5 (physical access devices). 🟢 [170.21] Five of the six are also Level 1 practices, and Level 1 allows no POA&M at all; the sixth is the SSP. That link is our reading of why. 🔴
- A POA&M does not substitute for implementation, and every NOT MET requirement must have one. 🟢 [170.24]
- **Closeout within 180 days** of the Conditional CMMC Status Date. It covers only the requirements on the POA&M. The OSA performs it for Level 2 (Self); a C3PAO performs it for Level 2 (C3PAO). If it is not closed in time, the Conditional status **expires**. 🟢 [170.21]

What this means in practice: of the 51 one-point requirements, 5 are excluded, so
46 can ever be deferred, and only 22 of them fit under the 88 floor. Every 5- and 3-point gap (except non-FIPS encryption) must be fixed before
the assessment. 🔴

## Status, validity and affirmations

- A CMMC Status is valid for **three years**; a Final status keeps the three years from the Conditional status date. 🟢 [CIO]
- Affirmations are entered in SPRS by the **Affirming Official**, a senior person in the OSA responsible for compliance. They are due on reaching Conditional status, on reaching Final status, after a POA&M closeout, and **annually** after the Final status date. 🟢 [170.22]
- An assessment lapses if the annual affirmation is not made. 🟢 [CIO] An affirmation is a representation to the government, so a false one carries False Claims Act exposure. 🟡 [DOJ-CCI]

## Sources

- [170.3] 32 CFR 170.3, Applicability (phases in (e)). https://www.law.cornell.edu/cfr/text/32/170.3
- [170.21] 32 CFR 170.21, Plan of Action and Milestones requirements. https://www.law.cornell.edu/cfr/text/32/170.21
- [170.22] 32 CFR 170.22, Affirmation. https://www.law.cornell.edu/cfr/text/32/170.22
- [170.24] 32 CFR 170.24, CMMC Scoring Methodology. https://www.law.cornell.edu/cfr/text/32/170.24
- [DFARS-FR] DoD, *DFARS: Assessing Contractor Implementation of Cybersecurity Requirements*, final rule, Federal Register doc. 2025-17359 (10 Sep 2025). Summary used: https://www.grfcpa.com/resource/dfars-publishes-final-rule-on-cmmc-effective-november-10/
- [CIO] DoD CIO, *About CMMC*. https://dodcio.defense.gov/cmmc/about
- [DoDAM] DoD, *NIST SP 800-171 DoD Assessment Methodology*, Version 1.2.1 (24 June 2020).
- [171A] NIST SP 800-171A, *Assessing Security Requirements for CUI* (June 2018). https://csrc.nist.gov/pubs/sp/800/171/a/final
- [DOJ-CCI] U.S. Department of Justice, Civil Cyber-Fraud Initiative (announced 6 October 2021). https://www.justice.gov/opa/pr/deputy-attorney-general-lisa-o-monaco-announces-new-civil-cyber-fraud-initiative
