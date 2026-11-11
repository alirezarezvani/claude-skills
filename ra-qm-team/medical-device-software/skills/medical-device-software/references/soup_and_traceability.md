# SOUP, SBOM and traceability: where software files fail review

Notified bodies and FDA reviewers open the same three things first: the safety
classification rationale, the trace matrix, and the SOUP list. This reference
covers the last two. Confidence legend as in
`classification_and_documentation_levels.md`.

## SOUP under IEC 62304

🟡 SOUP (software of unknown provenance) is a software item that is already
developed and generally available and was not developed for the medical device,
or was previously developed without adequate records of its development
process. Open-source libraries, operating systems, runtimes, commercial SDKs and
your own pre-62304 code all qualify.

| Obligation | Clause | Classes | Register column checked |
|---|---|---|---|
| Identify each SOUP item: title, manufacturer, unique designator | 8.1.2 | A, B, C | `name`, `supplier`, `version` (exact, never "latest") |
| Functional and performance requirements the item must meet for its use | 5.3.3 | B, C | `functional_requirements` |
| System hardware and software the item needs to work | 5.3.4 | B, C | `hw_sw_requirements` |
| Evaluate the published anomaly list for anomalies that could cause a hazardous situation | 7.1.3 | B, C | `anomaly_list_source`, `anomaly_review_date` |
| Include SOUP in software risk analysis and in change impact analysis | 7.1, 7.4 | B, C | (risk file) |

🟢 BSI (notified body, March 2025) reminds manufacturers that patches often sit in
SOUP (operating system, libraries) and that known anomalies must be documented.

**What "evaluated" has to show.** A date alone is weak. Keep, per release, the
list version or URL you read, the anomalies relevant to the functions you use,
and the decision for each (not reachable, mitigated by X, accepted with rationale).
The review-age window in `soup_register_check.py` (default 180 days) is policy,
not a clause: pick one in your SOP and justify it against your release cadence.

## SOUP is also your cybersecurity inventory

| Need | Source | Register column |
|---|---|---|
| SBOM including commercial, open-source and off-the-shelf components | 🟢 FD&C Act 524B(b)(3) | `purl`, SBOM cross-check |
| Plan to monitor and address postmarket vulnerabilities | 🟢 524B(b)(1) | `vuln_monitoring` |
| Third-party items managed, risk-transfer category declared | 🟡 IEC 81001-5-1 4.1.5, 4.3 (+ISH1:2025) | `support_category` |
| End-of-support known and planned | FDA 2025 guidance (support and end-of-support information); 81001-5-1 6.x | `end_of_support`, `eos_plan` |

Keep **one** register and generate the SBOM from the build, then diff the two:
`soup_register_check.py --sbom` reports components that are in the build but
were never assessed (NOT_IN_REGISTER) and register entries that no longer ship
(NOT_IN_SBOM). Two hand-maintained lists drift within a release.

An item past its end of support is effectively "required" software in
81001-5-1 terms (no upstream updates) whatever the register says; the check
flags it (CATEGORY_STALE) and blocks it outright when no plan is recorded.

## Traceability

🟡 What IEC 62304 asks to be traceable (A1): system requirements to software
requirements (5.2.1), software requirements to software system tests (5.7.1,
every class), and for class B and C, hazardous situations and software causes
to the risk control measures implemented in software and to their verification
(7.3.1, 7.3.3). At release, verification must be complete (5.8.1) and known
residual anomalies documented (5.8.2), and for B and C evaluated for safety
(5.8.3).

🟢 What reviewers do with it (BSI, March 2025): ask for trace matrices from
software requirements to test cases, expect risk mitigations to trace to
requirements and requirements to V&V tests, and **read raw data**: datasheets for
manual tests, execution logs for automated ones, acceptance criteria stated in
plain language.

`trace_matrix_check.py` enforces the link structure and the release state:

- every requirement has a parent system requirement and at least one test;
- with `--release`, no test may be failed or unrun without an anomaly id;
- for class B/C, every risk control traces to a hazard and has a passing test.

It cannot tell whether a linked test actually exercises the requirement. That
is the reviewer's job, and the most common way a green matrix still fails audit.

## FDA submission view

🟢 Both documentation levels require the SRS, architecture diagram, risk
management file, version history and the list of unresolved anomalies; Enhanced
adds the SDS with traceability to the SRS and the unit and integration test
protocols and reports (FDA webinar deck, July 2023). Unresolved anomalies in
the submission come straight from the RESIDUAL_ANOMALY rows.

## Sources

1. IEC 62304 Ed. 1.1 preview (definitions and clause list) — https://webstore.ansi.org/preview-pages/IEC/preview_iec62304%7Bed1.1%7Den.pdf
2. Al Cohen, "IEC 62304 Items by Class" (5.3.3, 5.3.4, 7.1.3 class markers) — https://alcohen.com/iec-62304-checklist/
3. SimQ, IEC 62304 class summary (SOUP identification in every class; requirements and anomaly evaluation from B) — https://simq.de/en/iec-62304-software-safety-classes/
4. BSI notified-body webinar, 27 March 2025 — https://bsigroup.com/siteassets/pdf/en/insights-and-media/media/webinars/bsi-md-software-under-mdr-perspectives-notified-body-270325-en-gb.pdf
5. 21 U.S.C. 360n-2 (FD&C Act 524B) — https://www.law.cornell.edu/uscode/text/21/360n-2
6. IEC 81001-5-1:2021/ISH1:2025 preview — https://www.en-standard.eu/publicdoc/iec_previews/1151833.pdf
7. FDA CDRH webinar deck, device software functions guidance, 20 July 2023 — https://fda.gov/media/170328/download
8. FDA, Cybersecurity in Medical Devices (27 June 2025) — https://www.hhs.gov/guidance/sites/default/files/hhs-guidance-documents/FDA/GUI00001825-final-PremarketCybersecurity-2025.pdf
