# NIS2 scope, entity category and registration

Who NIS2 catches, as which category, under which Member State, and what the
German transposition adds. From Directive (EU) 2022/2555 unless marked otherwise.

Confidence: 🟢 legal text · 🟡 authority guidance (official, non-binding) · 🔴 our reading, check with counsel

## The three questions, in order

1. **Sector.** Is the entity in an Annex I (11 sectors of high criticality) or Annex II (7 other critical sectors) sector and sub-sector? 🟢 Art 2(1)
2. **Size.** Is it at least medium-sized under Recommendation 2003/361 (50+ staff, or turnover above EUR 10m and balance sheet above EUR 10m), counting partner and linked enterprises? 🟢 Art 2(1); Rec 2003/361 Annex Arts 2-6
3. **Size-independent cases.** Public e-comms providers, trust service providers, TLD registries, DNS providers, domain registration services, sole providers of an essential service, entities whose disruption would have significant impact, critical entities under the CER Directive, and public administration are in scope whatever their size. 🟢 Art 2(2)-(4)

A small entity in an Annex sector is out of scope unless one of the size-independent cases applies. Member States may still designate it. 🟢 Art 2(2)(b)-(e)

## Essential or important (Art 3)

| Essential (Art 3(1)) | Basis |
|---|---|
| Annex I entities that exceed the medium-sized ceilings (250+ staff, or turnover above EUR 50m and balance sheet above EUR 43m) | 🟢 Art 3(1)(a) |
| Qualified trust service providers, TLD registries and DNS service providers, any size | 🟢 Art 3(1)(b) |
| Public e-comms providers that are medium-sized | 🟢 Art 3(1)(c) |
| Central government public administration | 🟢 Art 3(1)(d) |
| Entities a Member State identifies as essential | 🟢 Art 3(1)(e) |
| CER critical entities | 🟢 Art 3(1)(f) |
| Former NIS1 operators of essential services, if the Member State so decides | 🟢 Art 3(1)(g) |

Everything else in scope is **important** 🟢 Art 3(2). The difference is supervision (ex ante for essential, ex post for important, Arts 32-33) and the fine ceiling (below). The Article 21 measures and Article 23 reporting apply to both. 🟢 Arts 21, 23

## Jurisdiction and registration

- An entity falls under the Member State where it is established. DNS, TLD, domain registration, cloud, data centre, CDN, MSP, MSSP, marketplaces, search and social networks fall under the Member State of their **main establishment** in the EU. 🟢 Art 26(1)-(2)
- Member States had to list essential and important entities by 17 April 2025; entities supply name, address, contacts, sector, Member States served and IP ranges, and report changes within two weeks. 🟢 Art 3(3)-(4)
- The digital providers in Art 26(1)(b) register with ENISA's registry via their national authority. 🟢 Art 27

## Germany: NIS2UmsuCG (BSIG 2025)

- In force **6 December 2025** (BGBl. 2025 I Nr. 301). 🟢
- Categories: *besonders wichtige Einrichtungen* (250+ staff, or turnover above EUR 50m **and** balance sheet above EUR 43m, in Annex 1 sectors) and *wichtige Einrichtungen* (50+ staff, or turnover above EUR 10m and balance sheet above EUR 10m, in Annex 1 or 2). 🟢 BSIG §28
- **Register with the BSI within three months** of falling in scope; the BSI portal opened on 6 January 2026. 🟢 BSIG §33 · 🟡 BSI announcement
- Reporting: 24 h early warning, 72 h notification, final report after one month. 🟢 BSIG §32
- Management must approve and oversee the measures and attend training. 🟢 BSIG §38

## Fines (Art 34)

| Category | Ceiling (whichever is higher) |
|---|---|
| Essential | at least EUR 10m or 2% of worldwide annual turnover | 🟢 Art 34(4) |
| Important | at least EUR 7m or 1.4% of worldwide annual turnover | 🟢 Art 34(5) |

Germany mirrors these (BSIG §65). 🟢 Management bodies can be held liable and, for essential entities, temporarily barred. 🟢 Art 32(5)

## Where the scripts draw a line

- `nis2_scope_classifier.py` refuses to classify without employees or financials (exit 4): guessing size is the most common scoping error. 🔴
- Financial entities under DORA get a `DORA_LEX_SPECIALIS` finding: DORA's ICT risk and reporting rules replace Articles 21 and 23. 🟢 NIS2 Art 4; DORA Art 1(2)
- Member State options (designation, NIS1 operators) come back as `MS_OPTION`, not a verdict. 🔴

## Sources

1. Directive (EU) 2022/2555 (NIS2), OJ L 333, 27.12.2022 — https://eur-lex.europa.eu/eli/dir/2022/2555/oj
2. Commission Recommendation 2003/361/EC on SME definition — https://eur-lex.europa.eu/eli/reco/2003/361/oj
3. Commission Implementing Regulation (EU) 2024/2690 — https://eur-lex.europa.eu/eli/reg_impl/2024/2690/oj
4. Regulation (EU) 2022/2554 (DORA), Art 1(2) — https://eur-lex.europa.eu/eli/reg/2022/2554/oj
5. NIS2UmsuCG, BGBl. 2025 I Nr. 301 (BSIG §§28, 32, 33, 38, 65)
6. BSI, NIS-2 registration and reporting information — https://www.bsi.bund.de/
7. European Commission, NIS2 Directive policy page and FAQs 🟡 — https://digital-strategy.ec.europa.eu/en/policies/nis2-directive
