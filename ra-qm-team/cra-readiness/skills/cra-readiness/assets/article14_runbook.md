# Article 14 reporting runbook

Fill this in once per organisation, then keep one copy of section 3 per event.
Field names follow Article 14 of Regulation (EU) 2024/2847; check the live
Single Reporting Platform (SRP) form before your first report.

## 1. Standing set-up (do before anything happens)

| Item | Value | Owner |
|---|---|---|
| CSIRT designated as coordinator (Art 14(7)) and the basis (main establishment / authorised rep / importer / distributor / most users) | | |
| SRP accounts: who can submit, who is the backup, 24/7 coverage | | |
| Who decides "aware" (initial assessment owner) and how it is logged | | |
| Product list with the Member States each is made available in | from `cra_scope_classifier.py` | |
| User-notification channel per product (advisory page, CSAF feed, email) (Art 14(8)) | | |
| Micro or small enterprise? (Art 64(10)(a) affects fines, not the duty) | | |

## 2. Triage: is it reportable?

1. Actively exploited vulnerability? Reliable evidence that a malicious actor exploited it in a system without permission (Art 3(42)). Good-faith research and a component flaw not exploited in your product do not count.
2. Severe incident? Affects or could affect protection of sensitive or important data or functions, or led or could lead to malicious code in the product or user networks (Art 14(5)). Example: compromise of your update signing or release pipeline.
3. Record **detected at** and **aware at** (initial assessment reached reasonable certainty, Commission guidance C(2026) 5252). The SRP does not record awareness; this log is your evidence.

## 3. Per-event record

| Field | Value |
|---|---|
| Event id / kind (vulnerability or incident) | |
| Product(s), versions | |
| Detected at (with UTC offset) | |
| Aware at (with UTC offset), decided by | |
| **Early warning due** (aware + 24 h) / sent at | |
| Member States where made available | |
| Incidents: unlawful or malicious act suspected? | |
| **Notification due** (aware + 72 h) / sent at | |
| Nature of exploit or incident, initial assessment | |
| Corrective and mitigating measures taken; measures users can take | |
| Sensitivity of the information | |
| Corrective measure available at | |
| **Final report due** (vuln: fix + 14 days; incident: notification + 1 month) / sent at | |
| Severity and impact; malicious actor (vuln) or root cause (incident) | |
| Security update details | |
| Users informed at, channel, machine-readable? | |

Run `python scripts/art14_report_clock.py --events <log.csv>` after every update to the log.

## 4. After closure

- Publish the fixed-vulnerability advisory (Annex I Part II(4)).
- Feed root cause into the risk assessment (Art 13(3), (7)).
- If the component is third-party, report the flaw and share the fix with its maintainer (Art 13(6)).
