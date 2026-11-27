# Article 14 reporting: what is live since 11 September 2026

Reporting is the only CRA duty already in force for most manufacturers, and it
reaches products shipped years before the CRA existed. Everything here is from
Regulation (EU) 2024/2847 unless marked otherwise.

Confidence: 🟢 regulation text · 🟡 Commission guidance or ENISA (non-binding, official) · 🔴 our reading, check with counsel

## Dates

| Date | What applies | Source |
|---|---|---|
| 10 Dec 2024 | Regulation in force | 🟢 Art 71(1); OJ L 2024/2847 of 20.11.2024 |
| 11 Jun 2026 | Notified bodies regime (Chapter IV, Arts 35-51) | 🟢 Art 71(2) |
| **11 Sep 2026** | **Article 14 reporting** | 🟢 Art 71(2) |
| 11 Dec 2027 | Everything else, incl. Annex I, conformity, CE marking, Art 24 stewards | 🟢 Art 71(2) |
| 11 Jun 2028 | End of validity for certificates issued under other cybersecurity acts | 🟢 Art 69(1) |

ENISA launched the Single Reporting Platform (SRP) on 11 September 2026 at
`portal.cra-srp.enisa.europa.eu` as an "initial operating capability", with more
functions to follow 🟢 (ENISA press release of that date). Reports written in
July 2026 that the SRP would not be live are superseded. At launch it
had no API, an English-only interface and no voluntary-report flow 🔴 (third-party
onboarding reports; verify on the portal).

## What must be reported

| Event | Trigger | Recipient | Source |
|---|---|---|---|
| Actively exploited vulnerability | "reliable evidence that a malicious actor has exploited" it in a system without permission | CSIRT designated as coordinator + ENISA, simultaneously, via the SRP | 🟢 Art 3(42), Art 14(1) |
| Severe incident having an impact on the security of the product | affects or could affect protection of sensitive or important data or functions, or led or could lead to malicious code in the product or the user's network | same | 🟢 Art 14(3), 14(5) |

Not reportable: a vulnerability found by good-faith testing, or a component
flaw with no evidence of exploitation in your product 🟢 (Art 3(42); recital 67)
🟡 (guidance: a third-party component flaw is reportable only if exploited in the
manufacturer's product). Handle those under Annex I Part II and, for components,
tell the maintainer (Art 13(6)). Voluntary reporting covers near misses and
non-exploited vulnerabilities 🟢 (Art 15).

## The three clocks

| Report | Vulnerability (Art 14(2)) | Severe incident (Art 14(4)) |
|---|---|---|
| Early warning | 24 h from awareness; Member States where the product is available | 24 h; plus whether unlawful or malicious acts are suspected |
| Notification | 72 h from awareness; product, nature of the exploit, corrective and user measures, sensitivity | 72 h; nature, initial assessment, measures, sensitivity |
| Final report | **14 days after a corrective or mitigating measure is available**; description, severity, impact, malicious actor info, update details | **one month after the incident notification**; detailed description, severity, impact, threat type or root cause, mitigation |

Users: after awareness, inform impacted users, and where appropriate all users,
of the event and the measures they can take, in a structured machine-readable
format where appropriate. If you don't, the CSIRT may 🟢 (Art 14(8)).

**When does "aware" start?** 🟡 The Commission guidance (Annex to C(2026) 5252,
27 July 2026) treats a manufacturer as aware once a prompt initial assessment
gives a reasonable degree of certainty. The SRP does not record that moment, so
your triage log is the evidence. 🔴 A market surveillance authority could argue
from first detection if the triage was slow or undocumented; `art14_report_clock.py`
runs from detection when no awareness time is logged for that reason.

## Where reports go (Art 14(7))

The SRP endpoint of the CSIRT coordinator in the Member State of your **main
establishment** in the Union. Without one: the Member State of the authorised
representative, then the importer, then the distributor, then the one with most
users 🟢. Later reports may go to the same CSIRT as the first 🟢. 🔴 The SRP's
"Assigned Representative" account role is not the Art 18 authorised representative.

## Legacy products

Products placed on the market before 11 December 2027 owe nothing else under
the CRA unless substantially modified, **but Article 14 applies to them** 🟢
(Art 69(2)-(3)). 🟡 Per the guidance the duty is not retroactive: exploitation
known before 11 September 2026 is not reportable, and it continues after the
support period ends. 🔴 That last point surprises teams with end-of-life fleets.
Keep a contact route and triage for every product still in the field.

## Penalties and the SME carve-out

Breaching Art 13 or 14: up to EUR 15 000 000 or 2.5 % of worldwide annual
turnover, whichever is higher 🟢 (Art 64(2)). Micro and small enterprises cannot
be fined for missing the **24-hour early warning** (Art 14(2)(a), 14(4)(a)), and
open-source stewards cannot be fined at all 🟢 (Art 64(10)). The early warning is
still owed; only the fine is excluded.

## Pending changes to watch

- The **Digital Omnibus** (COM(2025) 837, 19 Nov 2025) would create one incident
  reporting entry point across GDPR, NIS2, DORA and CER. The Council's mandate
  (Coreper, 21 Oct 2026) replaces the EU-level point with a national entry point
  per Member State and adds a NIS2 clause treating a CRA severe-incident
  notification as meeting NIS2 Art 23(4) information requirements 🟡
  (regreportingdesk.com, diesec.com). It is not adopted: Parliament's committee
  vote is expected in early 2027. It does not change CRA Art 14 deadlines.
- The Art 14(10) implementing act on notification format and procedure had not
  been adopted as of 26 Nov 2026 🟡 (no adoption found in the trackers below).
  Use the SRP's own forms until it is.

## Delayed dissemination: Delegated Regulation (EU) 2026/881

Adopted 11 Dec 2025 under Art 14(9), published OJ L 20.4.2026, in force on the
twentieth day after publication (10 May 2026) 🟢 (Art 6). It governs when the
CSIRT that first receives your notification may hold it back from other CSIRTs
and market surveillance authorities. It does not change your 24h/72h/14-day
clock. The CSIRT decides, at its discretion, for no longer than strictly
necessary; there is no fixed maximum 🟢 (Art 3, recital 1). Grounds 🟢:

- Art 3(a): you expect a mitigation within 72 hours. If none arrives, the CSIRT
  must disseminate. Put the expected fix date in the early warning: it is the
  fact that opens this ground.
- Art 3(b)-(c): the details would let someone build an exploit, or partial
  sharing is enough for other CSIRTs to act; full release once a mitigation exists.
- Art 3(d): a coordinated disclosure through a trusted intermediary, released
  when delay is no longer needed and the parties consent.
- Art 4: a specific receiving CSIRT has had a confidentiality incident or lacks
  capability. Art 5: the SRP itself has had a confidentiality incident, until
  ENISA reports it restored.

🔴 You cannot ask for a delay as of right; a manufacturer that wants one should
say why in the notification and keep the CSIRT's answer with the report.

## Sources

1. Regulation (EU) 2024/2847, OJ L 2024/2847, 20.11.2024 — https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng (Arts 3, 14, 15, 16, 64, 69, 71)
2. European Commission, *Commission guidance on the application of the CRA*, Annex to C(2026) 5252, 27 July 2026 — https://digital-strategy.ec.europa.eu/en/library/commission-publishes-new-guidance-support-timely-cyber-resilience-act-implementation
3. ENISA, *The CRA Single Reporting Platform is launched*, 11 September 2026 — https://www.enisa.europa.eu/news/the-cra-single-reporting-platform-is-launched
4. ENISA, SRP FAQ — https://www.enisa.europa.eu/topics/product-security/vulnerability-services/eu-incident-response-and-cyber-crisis-management/single-reporting-platform-srp/frequently-asked-questions
5. Directive (EU) 2022/2555 (NIS2), Arts 6 and 12 — definitions of incident and near miss, CSIRT coordinators
6. European Commission, Digital Omnibus proposal COM(2025) 837, 19 November 2025; Council mandate 21 October 2026 (Council doc 14756/26), as summarised by regreportingdesk.com (Nov 2026) and diesec.com (27 Oct 2026)
7. cyberresilienceact.eu, *CRA reporting: 24h, 72h & 14-day deadlines* — SRP field limits and launch constraints (independent, verify)
8. Commission Delegated Regulation (EU) 2026/881 of 11 December 2025 (Art 14(9)), OJ L 20.4.2026 — https://eur-lex.europa.eu/eli/reg_del/2026/881/oj (read via the OJ PDF copy at ibf-solutions.com)
