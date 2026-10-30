# Rev 2 vs Rev 3, and Levels 1 and 3

The community request behind this skill asked for Level 2 "grounded in NIST SP
800-171 Rev 2 with the option to comply with Rev 3 in the future". This is how
to hold both without scoring against the wrong one.

Confidence key: 🟢 read in the primary source · 🟡 secondary source or recalled, not re-read for this skill · 🔴 our judgment.

## Score against Rev 2

- 32 CFR Part 170 assesses Level 2 against **NIST SP 800-171 Rev 2**: 110 requirements in 14 families, scored per 170.24. 🟢 [170.24]
- On 2 May 2024 DoD issued class deviation 2024-O0013 so that DFARS 252.204-7012 keeps pointing at Rev 2 rather than "the version in effect at the time of solicitation". 🟡 [Dev]
- NIST published Rev 3 in May 2024: 97 requirements in 17 families, with organization-defined parameters (ODPs) that DoD sets. 🟡 [R3]

So `sprs_score.py` scores only Rev 2 identifiers (`AC.L2-3.1.1` style) and refuses
anything else. Do not mix Rev 3 identifiers into the assessment file. 🔴

## Getting ready for Rev 3 without paying twice

Our recommendation, not a rule: 🔴

1. Implement and evidence to Rev 2; that is what is assessed and what the score reflects.
2. Keep the evidence per *capability* (MFA, logging, configuration baseline), not per requirement number, so it re-maps when the numbering changes.
3. Where Rev 3 adds or tightens (supply chain risk management, the new planning family, ODP-set frequencies), note the gap in the SSP's roadmap section, not in the POA&M: a POA&M item for a Rev 3 requirement is not a Rev 2 gap and confuses the assessor.
4. Watch for a DFARS change or a new class deviation; that, not the NIST publication, is the trigger.

## Level 1 and Level 3 in one paragraph each

- **Level 1 (Self):** the 15 safeguarding requirements of FAR 52.204-21, annual self-assessment and annual affirmation, all MET, **no POA&M**. 🟢 [CIO] This skill does not score Level 1; its practices are a subset of Level 2, so a clean Level 2 file covers them. 🔴
- **Level 3 (DIBCAC):** requires a Final Level 2 (C3PAO) status first, then 24 selected NIST SP 800-172 requirements assessed by DCMA DIBCAC, each worth 1 point. 🟢 [170.24][CIO]

## Sources

- [170.24] 32 CFR 170.24, CMMC Scoring Methodology. https://www.law.cornell.edu/cfr/text/32/170.24
- [CIO] DoD CIO, *About CMMC*. https://dodcio.defense.gov/cmmc/about
- [Dev] Crowell & Moring, "Miss Me With Rev 3, Says DoD" (on Class Deviation 2024-O0013, 2 May 2024). https://www.crowell.com/en/insights/client-alerts/miss-me-with-rev-3-says-dod-dod-issues-class-deviation-linking-dfars-7012-to-nist-sp-800-171-rev-2
- [R2] NIST SP 800-171 Rev. 2, *Protecting CUI in Nonfederal Systems and Organizations*. https://csrc.nist.gov/pubs/sp/800/171/r2/upd1/final
- [R2A] NIST SP 800-171A, *Assessing Security Requirements for CUI* (June 2018). https://csrc.nist.gov/pubs/sp/800/171/a/final
- [R3] NIST SP 800-171 Rev. 3 (May 2024). https://csrc.nist.gov/pubs/sp/800/171/r3/final
- [172] NIST SP 800-172, *Enhanced Security Requirements for Protecting CUI*. https://csrc.nist.gov/pubs/sp/800/172/final
