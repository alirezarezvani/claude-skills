# NIS2 Article 23: significant incidents and the three reports

> Rules last verified 2026-11-17 against the EUR-Lex texts cited below. Re-check before relying on a deadline or threshold.

Confidence: 🟢 legal text · 🟡 authority guidance · 🔴 our reading, check with counsel

## What is significant (Art 23(3))

An incident is significant if it has caused or can cause **severe operational
disruption of the services or financial loss** for the entity, or has affected
or can affect **other natural or legal persons by causing considerable
material or non-material damage**. 🟢 Art 23(3)

For DNS, TLD, cloud, data centre, CDN, MSP, MSSP, marketplaces, search, social
networks and trust services, Implementing Regulation 2024/2690 makes this
concrete. An incident is significant if any of these holds 🟢 2024/2690 Art 3(1):

- financial loss above EUR 500 000 or 5% of annual turnover, whichever is lower;
- exfiltration of trade secrets;
- death, or considerable damage to a person's health;
- successful, suspectedly malicious and unauthorised access that may cause severe disruption;
- a sector-specific threshold in Arts 5-14 (e.g. a cloud service fully unavailable for more than 30 minutes).

Recurring incidents (twice in six months, same apparent root cause) that are
significant together count as one 🟢 2024/2690 Art 4. Scheduled maintenance is
not an incident for this purpose 🟢 2024/2690 Art 3(2).

## The reports

| Report | Deadline | Content | Source |
|---|---|---|---|
| Early warning | within 24 h of becoming aware | suspected unlawful or malicious cause? cross-border impact? | 🟢 Art 23(4)(a) |
| Incident notification | within 72 h of becoming aware (24 h for trust service providers on trust-service incidents) | update, initial assessment of severity and impact, indicators of compromise | 🟢 Art 23(4)(b) |
| Intermediate report | on request of the CSIRT or authority | status updates | 🟢 Art 23(4)(c) |
| Final report | one month after the notification | detailed description, severity and impact, type of threat or root cause, mitigation applied and ongoing, cross-border impact | 🟢 Art 23(4)(d) |
| Progress report | instead of the final, if the incident is ongoing at one month; final then due one month after handling ends | | 🟢 Art 23(4)(e) |

Recipients are informed of significant incidents likely to affect their
services "without undue delay", and of measures they can take for significant
cyber threats. 🟢 Art 23(1)-(2)

"Becoming aware" is not the first alert: it is when the entity has reasonable
certainty a significant incident occurred 🔴 (our reading; check your
authority's guidance). The scripts therefore ask for both
detection and awareness times and fall back to detection when awareness is
missing. 🔴

## Overlaps for one event

| Law | Trigger | First deadline | Recipient |
|---|---|---|---|
| NIS2 | significant incident | 24 h after awareness | CSIRT or competent authority |
| DORA (financial entities, replaces NIS2 Art 23) | major ICT incident | 4 h after classification, at most 24 h after awareness | financial competent authority (copy to CSIRT if the Member State requires, DORA Art 19(1)) |
| CRA (manufacturer of the affected product) | actively exploited vulnerability or severe incident affecting the product | 24 h after awareness | coordinator CSIRT + ENISA via the SRP |
| GDPR | personal-data breach likely to result in a risk | 72 h after awareness | data protection authority (Art 33); data subjects if high risk (Art 34) |

`eu_cyber_regime_router.py` lays these clocks side by side for one entity and
one event. Who reports is set by each law; one event can create four reports. 🟢

## Penalties for missing a report

Failing Art 23 is a breach sanctioned under Art 34 (see the scope reference for
ceilings). Germany: BSIG §65. 🟢

## Sources

1. Directive (EU) 2022/2555, Arts 23, 34 — https://eur-lex.europa.eu/eli/dir/2022/2555/oj
2. Implementing Regulation (EU) 2024/2690, Arts 3-14 — https://eur-lex.europa.eu/eli/reg_impl/2024/2690/oj
3. Regulation (EU) 2022/2554 (DORA), Art 19 — https://eur-lex.europa.eu/eli/reg/2022/2554/oj
4. Regulation (EU) 2024/2847 (CRA), Art 14 — https://eur-lex.europa.eu/eli/reg/2024/2847/oj
5. Regulation (EU) 2016/679 (GDPR), Arts 33-34 — https://eur-lex.europa.eu/eli/reg/2016/679/oj
6. NIS2UmsuCG, BGBl. 2025 I Nr. 301 (BSIG §32)
7. ENISA, NIS2 technical implementation guidance for 2024/2690 (2025) 🟡 — https://www.enisa.europa.eu/
