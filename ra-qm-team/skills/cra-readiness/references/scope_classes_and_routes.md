# Scope, classes and conformity routes

What `cra_scope_classifier.py` decides, and the article behind each decision.

Confidence: 🟢 regulation text · 🟡 Commission guidance or implementing act · 🔴 our reading, check with counsel or a notified body

## 1. Is it in scope?

A **product with digital elements** is software or hardware plus its remote data
processing solutions, including components placed on the market separately 🟢
(Art 3(1)). It is in scope if its intended purpose or reasonably foreseeable use
includes a direct or indirect logical or physical data connection to a device or
network 🟢 (Art 2(1)), and it is made available in the course of a commercial
activity, paid or free 🟢 (Art 3(22)).

**Excluded** 🟢: medical devices (Reg 2017/745) and IVDs (Reg 2017/746) (Art 2(2));
vehicles under Reg 2019/2144 (Art 2(2)); products certified under Reg 2018/1139,
civil aviation (Art 2(3)); marine equipment, Dir 2014/90/EU (Art 2(4)); identical
spare parts (Art 2(6)); products developed or modified exclusively for national
security or defence, or designed to process classified information (Art 2(7)).

🔴 **Medical device makers:** the MDR device is out, but your portfolio is not.
A companion app, gateway, cloud console or wellness wearable that is *not* itself
a medical device is in scope, and Annex III class I item 19 explicitly captures
health-monitoring wearables that the MDR/IVDR do not cover. The excluded device
still owes MDR Annex I §17.2/§17.4 cybersecurity (MDCG 2019-16).

**Remote data processing** is part of the product when it is done at a distance,
the product could not perform one of its functions without it, and the
manufacturer designed it or had it designed 🟢 (Art 3(2)) 🟡 (guidance: three
cumulative conditions; a third-party SaaS integrated into the product is
generally a third-party component under Art 13(5)). Pure SaaS is outside the CRA
and inside NIS2.

**Open source** 🟡: FOSS not monetised by its publisher is not placed on the
market. Charging for it or for binaries, making personal-data processing a
condition of use for non-security purposes, or reserving releases or security
updates to payers brings it in. Separate optional paid services and voluntary
donations do not. A legal person that sustainably supports FOSS intended for
commercial use is an **open-source software steward** 🟢 (Art 3(14)): a documented
cybersecurity policy (Art 24(1)-(2)), limited Article 14 duties (Art 24(3)), no
fines (Art 64(10)(b)).

## 2. Who is the manufacturer?

| Role | Duties | Source |
|---|---|---|
| Manufacturer (own name or trademark, paid, monetised or free) | Arts 13, 14, conformity, CE | 🟢 Art 3(13), 13 |
| Importer or distributor placing it under **its own name or trademark**, or substantially modifying it | becomes the manufacturer | 🟢 Art 21 |
| Anyone else who substantially modifies and makes available | manufacturer for the affected part (or whole, if overall security is affected) | 🟢 Art 22 |
| Importer | verify CE, DoC, documentation, contact details before placing | 🟢 Art 19 |
| Distributor | verify CE and upstream compliance before making available | 🟢 Art 20 |

**Substantial modification**: a post-market change that affects compliance with
Annex I Part I or changes the assessed intended purpose 🟢 (Art 3(30)). 🟡 The
guidance asks whether the change adds threat vectors or attack scenarios or
alters their likelihood or impact; security updates that only reduce risk are
generally not substantial, but one that adds a new dependency (e.g. moves local
crypto to a manufacturer cloud) can be.

## 3. Which class?

Classification follows the product's **core functionality** 🟢 (Art 7(1)).
Integrating an important product (say, a VPN client) does not by itself make the
host product important 🟢 (Art 7(1), last sentence). Technical descriptions of
every category are in Commission Implementing Regulation (EU) 2025/2392
(adopted 28 Nov 2025) 🟡.

- **Important class I** (Annex III, 19 categories): identity and privileged access management incl. readers; browsers; password managers; anti-malware; VPN; network management; SIEM; boot managers; PKI; network interfaces; operating systems; internet routers, modems, switches; microprocessors, microcontrollers, ASICs and FPGAs with security functions; smart-home assistants; smart-home security products (locks, cameras, baby monitors, alarms); connected toys with social or location features; health-monitoring or children's wearables outside MDR/IVDR 🟢
- **Important class II** (Annex III, 4): hypervisors and container runtimes; firewalls and IDS/IPS; tamper-resistant microprocessors and microcontrollers 🟢
- **Critical** (Annex IV, 3): hardware devices with security boxes; smart meter gateways and other advanced-security devices incl. secure cryptoprocessing; smartcards and secure elements 🟢
- **Default**: everything else in scope

The Commission can amend Annex III by delegated act, with at least 12 months'
transition for new or upgraded categories 🟢 (Art 7(3)).

## 4. Which conformity route? (Art 32)

| Class | Open routes | Note |
|---|---|---|
| Default | A (internal control), B+C, H, EUCC | 🟢 Art 32(1) |
| Important I | B+C, H, EUCC; **A only if** harmonised standards, common specifications or an EUCC scheme at 'substantial' are applied **in full** | 🟢 Art 32(2) |
| Important II | B+C, H, or EUCC at 'substantial' — never A | 🟢 Art 32(3) |
| Critical | EUCC where a delegated act under Art 8(1) requires it; otherwise as class II | 🟢 Art 32(4) |
| FOSS in Annex III | any Art 32(1) route if the technical documentation is public | 🟢 Art 32(5) |

🔴 **The trap for class I:** as of September 2026 no CRA harmonised standard had
been cited in the Official Journal (standardisation request M/606, C(2025) 618;
EN 40000 series in drafting, deadlines slipping). Until one is cited, module A
is closed for class I and the plan needs a notified body. Check the OJ list
before you commit to A. Notified-body capacity is the schedule risk: the
notification regime only started on 11 June 2026.

## 5. Support period (Art 13(8))

At least **five years**, unless the product is expected to be in use for less, in
which case the support period equals the expected use time 🟢. Five years is a
floor, not a default 🟡: it must reflect how long users actually keep the product.
State the end date (at least month and year) at purchase 🟢 (Art 13(19)); keep each
security update available for 10 years or the rest of the support period,
whichever is longer 🟢 (Art 13(9)); record the basis in Annex VII point 4 🟢.

## Sources

1. Regulation (EU) 2024/2847, Arts 2, 3, 7, 8, 13, 19-22, 24, 32, 64, 69; Annexes III, IV, VIII — https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng
2. Commission Implementing Regulation (EU) 2025/2392 on the technical description of important and critical product categories (28 Nov 2025)
3. European Commission, guidance on the application of the CRA, Annex to C(2026) 5252, 27 July 2026
4. Commission standardisation request C(2025) 618 (M/606), 3 Feb 2025; status per cyberresilienceact.eu tracker, Sept 2026
5. Regulation (EU) 2017/745 (MDR), Annex I §17.2 and §17.4; MDCG 2019-16 rev.1, Guidance on cybersecurity for medical devices
6. Commission Notice, *The 'Blue Guide' on the implementation of EU product rules 2022* (2022/C 247/01) — placing on the market applies per individual unit
