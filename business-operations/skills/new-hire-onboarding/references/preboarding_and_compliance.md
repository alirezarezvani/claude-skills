# Preboarding and compliance

The first day is decided in the two weeks before it. A hire who arrives with no
laptop, no account or no completed right-to-work check loses the day, and in
the UK the employer may lose much more. `preboarding_gate.py` turns this page
into dated tasks.

## Lead times (defaults in the script)

| Category | Default lead (business days before start) | Why |
|---|---|---|
| contract | 10 | A signed offer or contract before anything is ordered in the hire's name |
| equipment | 3 on site, 7 remote | Courier, customs and a spare day for a failed delivery |
| payroll | 5 | Tax and bank details in before the first pay run cutoff |
| accounts | 2 | Email, SSO and the role's day-one systems, tested by someone other than IT |
| day_one_agenda | 2 | Sent to the hire so they know where to be and who they meet |
| right_to_work | 1 (UK minimum) | See below |

These are defaults, not rules: set `lead_days` per task from your own vendors.
Weekends are skipped; public holidays are not, so add a day around them.

## Right to work

**United States, Form I-9.** The employee completes Section 1 no later than
the first day of employment; the employer completes Section 2 within 3
business days of the first day (a Monday start means Thursday). The script
prints both dates. Confidence: high (USCIS I-9 Central and Handbook M-274).

**United Kingdom.** "You must check that a job applicant is allowed to work for
you in the UK before you employ them" (GOV.UK). A civil penalty of up to
£60,000 per illegal worker applies where no correct check was done, and
knowingly employing an illegal worker is a criminal offence (up to 5 years).
The script makes the check blocking one business day before the start.
Confidence: high (GOV.UK, read 2026-11-26).

**Germany (not built into the script).** Right to work matters only for
non-EU nationals, but every hire triggers the Nachweisgesetz: § 2 (1) requires
the names of the parties, pay and working hours by the first day of work; the
start date, duration, place of work, job description, probation, on-call and
overtime rules by the seventh calendar day; everything else within one month.
Text form (for example email) is allowed when the document can be stored and
printed and the employer asks for a receipt. Confidence: high on the text
(gesetze-im-internet.de, read 2026-11-26); have counsel confirm how it applies.

**Anywhere else:** the script requires a `right_to_work` task but has no
deadline. Ask HR or counsel; never guess.

## The four Cs

Bauer (SHRM Foundation, 2010) splits onboarding into Compliance (rules and
paperwork), Clarification (what the job is and how success is judged), Culture
and Connection. Most organisations stop at Compliance. The preboarding gate
covers Compliance and the first step of Connection (a named manager and buddy);
`plan_builder.py` covers Clarification.

## Sources

1. USCIS, I-9 Central, "Completing Section 2, Employer Review and Attestation". https://www.uscis.gov/i-9-central/completing-form-i-9/completing-section-2-employer-review-and-attestation
2. USCIS, Handbook for Employers M-274, 4.0 "Completing Section 2". https://www.uscis.gov/i-9-central/form-i-9-resources/handbook-for-employers-m-274/40-completing-section-2-employer-review-and-verification
3. GOV.UK, "Check a job applicant's right to work". https://www.gov.uk/check-job-applicant-right-to-work
4. GOV.UK, "Penalties for employing illegal workers". https://www.gov.uk/penalties-for-employing-illegal-workers
5. Nachweisgesetz § 2. https://www.gesetze-im-internet.de/nachwg/__2.html
6. Bauer, T. N. (2010). *Onboarding New Employees: Maximizing Success*. SHRM Foundation Effective Practice Guidelines.
