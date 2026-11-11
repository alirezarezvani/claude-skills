# Classification: IEC 62304 safety class, FDA documentation level, 524B cyber device

Three classifications sit on the same software and are routinely confused. They
use different inputs, so the same product can land in different places.

| Question | Framework | Input that decides it | Assessed |
|---|---|---|---|
| Which lifecycle activities are required? | IEC 62304:2006+A1:2015, 4.3 | worst-case harm the software can contribute to | **after** risk control measures external to the software system |
| How much software documentation goes into a US submission? | FDA, *Content of Premarket Submissions for Device Software Functions* (June 2023) | probable risk of death or serious injury from a failure or flaw | **before** risk control measures |
| Do the statutory cybersecurity requirements apply? | FD&C Act 524B (21 U.S.C. 360n-2) | software + internet connectivity + characteristics vulnerable to threats | not risk-based at all |

Confidence legend: 🟢 checked against the primary text · 🟡 two or more independent
secondary sources agree, primary is paywalled · 🔴 not verified, do not rely on it.

## 1. IEC 62304 software safety class (clause 4.3)

🟡 **Definitions.** Class A: no injury or damage to health is possible. Class B:
non-serious injury is possible. Class C: death or serious injury is possible.

🟡 **The Amendment 1 (2015) decision path (Figure 3).**

1. Can the software system contribute to a hazardous situation? No → **A**.
2. Yes → does it result in unacceptable risk once **risk control measures
   external to the software system** are considered? No → **A**.
3. Yes → what injury is possible? Non-serious → **B**; serious injury or death → **C**.

Until classification is done the software is treated as class C. Severity, not
probability of harm, decides the class.

🟡 **What counts as external.** External means outside the software system, not
outside the product: a hardware pressure-relief valve, a hardware watchdog, an
independent second system, a trained user's check. A monitor inside the same
software system does not lower its class. External measures must themselves be
verified, a human check typically by usability evaluation (IEC 62366-1).
`software_safety_classifier.py` refuses to use an unverified external control.

🟡 **Items and segregation.** A software system takes the class of its highest
item. Items inherit the system's class unless the architecture justifies a lower
one (weak or no coupling; strongest when the items run on separate hardware).
For class C the segregation necessary for risk control is clause 5.3.5. Without
documented segregation every item carries the highest class.

**Common misreadings found in published guides (and corrected here):**

- "Classify before any risk controls." That was the reading of the 2006 text;
  A1 explicitly lets external risk controls lower the class. One vendor guide
  checked for this skill (Greenlight Guru, 2026) still says classification is
  done before risk controls. The FDA documentation level, by contrast, really is
  assessed before risk controls; that is a different question.
- "Class A needs no testing." Since A1, software system testing (5.7) is
  required for class A.

## 2. FDA documentation level (Basic / Enhanced)

🟢 The June 2023 final guidance replaced the 2005 Major/Moderate/Minor "level of
concern". **Enhanced** documentation applies where a failure or flaw of any
device software function could present a hazardous situation with a probable
risk of death or serious injury to a patient, user or others in the environment
of use, **assessed prior to the implementation of risk control measures**. FDA
generally recommends Enhanced for Class III devices and device constituents of
combination products (a sponsor may justify otherwise). Basic applies everywhere
else. The level applies to the device as a whole.

🟢 What changes between the levels (FDA webinar deck, 20 July 2023):

| Element | Basic | Enhanced |
|---|---|---|
| Software Design Specification | keep in the DHF; FDA may request | submit, with traceability to the SRS |
| Development, configuration management, maintenance | IEC 62304 declaration of conformity **or** a process summary | the same **plus** the complete configuration management and maintenance plans |
| Testing | unit/integration/system summary; system test protocol and report | the same **plus** unit and integration test protocols and reports |

All other elements (level rationale, software description, risk management file,
SRS, architecture diagram, version history, unresolved anomalies) are the same
for both.

**Consequence the classifier flags (ENHANCED_GAP):** a team that is IEC 62304
class B because a hardware interlock is external can still owe Enhanced
documentation, because FDA ignores that interlock when picking the level.

🟢 FDA recognises IEC 62304 Ed. 1.1 2015-06 (and ANSI/AAMI IEC 62304:2006/A1:2016)
as consensus standard **13-79**, complete recognition, entered 14 January 2019.

## 3. FD&C Act 524B "cyber device"

🟢 Section 524B (21 U.S.C. 360n-2), in force 90 days after 29 December 2022
(i.e. 29 March 2023). A **cyber device** (c) includes software validated,
installed or authorised by the sponsor as or in a device, **has the ability to
connect to the internet**, and contains technological characteristics that
could be vulnerable to cybersecurity threats. A sponsor submitting a 510(k),
De Novo, PMA, PDP or HDE for one must (b):

1. submit a plan to monitor, identify and address postmarket vulnerabilities and
   exploits, including coordinated vulnerability disclosure;
2. design, develop and maintain processes giving reasonable assurance the device
   and related systems are cybersecure, with updates and patches on a reasonably
   justified regular cycle for known unacceptable vulnerabilities and as soon as
   possible out of cycle for critical ones;
3. provide a software bill of materials, including commercial, open-source and
   off-the-shelf components;
4. comply with other requirements FDA sets by regulation.

FDA may exempt devices or categories by Federal Register notice (d).

🟢 FDA's guidance *Cybersecurity in Medical Devices: Quality System Considerations
and Content of Premarket Submissions* was updated and announced on 27 June 2025,
adding a section on 524B cyber devices; it supersedes the September 2023 final.
🟢 Its Section VII.B reads "ability to connect to the internet" to include
connection "whether intentionally or unintentionally, through any means", with
an illustrative list: network, server or cloud connections; radio-frequency
(Wi-Fi, cellular, Bluetooth, BLE); magnetic inductive communications; and
hardware connectors capable of connecting to the internet (USB, ethernet,
serial port). A USB service port is enough. Set `internet_capable=yes` unless
you can show none of these exists.

## 4. EU context

- 🟡 MDR Annex I 17.2: software developed and manufactured according to the state
  of the art, taking into account development life cycle, risk management
  including information security, verification and validation. 17.4: minimum
  requirements on hardware, IT network characteristics and IT security measures.
  EN 62304:2006+A1:2015 is what notified bodies audit as the state of the art
  (BSI, notified-body webinar, 27 March 2025).
- 🔴 **Harmonisation.** As of November 2026 this skill could not confirm that
  EN 62304 or EN IEC 81001-5-1 is cited in the Official Journal under the MDR
  (checked: the Commission's harmonised-standards page listing Decision
  2021/1182 and its amendments up to 2026/1231; amendments 2025/2078 and 2026/193
  do not include either). Read the Commission's consolidated list before claiming
  presumption of conformity; plan as if neither gives it.
- MDR device class (Rule 11, MDCG 2019-11) is a separate question:
  `mdr-745-specialist` owns it.
- Medical devices are excluded from the EU Cyber Resilience Act (Art 2(2));
  non-device companion apps and gateways are not. `cra-readiness` owns that line.

## 5. IEC 62304 Edition 2

🟡 Edition 2 is still in drafting. Changes in the 2025 committee draft include
two process rigour levels replacing classes A/B/C, explicit AI/ML lifecycle
content, a scope widened to health software, and cybersecurity referred to
IEC 81001-5-1. Secondary reports (QuickBird Medical, 10 September 2026) give an
IEC forecast publication date of 26 October 2028, slipped from April 2027. Plan
on Edition 1.1 (2006+A1:2015); do not build a QMS on a committee draft.

## Sources

1. IEC 62304:2006+AMD1:2015 (Ed. 1.1) table of contents and clause 1.4, ANSI webstore preview — https://webstore.ansi.org/preview-pages/IEC/preview_iec62304%7Bed1.1%7Den.pdf
2. Johner Institute, "Software safety classes IEC 62304" — https://blog.johner-institute.com/iec-62304-medical-software/safety-class-iec-62304/
3. SimQ, "IEC 62304 Software Safety Classes A, B and C" — https://simq.de/en/iec-62304-software-safety-classes/
4. FDA CDRH webinar deck, "Content of Premarket Submissions for Device Software Functions, Final Guidance", 20 July 2023 — https://fda.gov/media/170328/download
5. 21 U.S.C. 360n-2 (FD&C Act 524B) — https://www.law.cornell.edu/uscode/text/21/360n-2
6. Federal Register 90 FR (27 June 2025), notice of availability of the updated premarket cybersecurity guidance — https://www.govinfo.gov/content/pkg/FR-2025-06-27/html/2025-11669.htm; guidance text (issued 27 June 2025, Section VII.B) — https://www.hhs.gov/guidance/sites/default/files/hhs-guidance-documents/FDA/GUI00001825-final-PremarketCybersecurity-2025.pdf
7. FDA Recognized Consensus Standards database, IEC 62304 (13-79) — https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/results.cfm?title=62304
8. European Commission, harmonised standards for medical devices — https://single-market-economy.ec.europa.eu/single-market/goods/european-standards/harmonised-standards/medical-devices_en
9. BSI, "Software under MDR: perspectives of a notified body", 27 March 2025 — https://bsigroup.com/siteassets/pdf/en/insights-and-media/media/webinars/bsi-md-software-under-mdr-perspectives-notified-body-270325-en-gb.pdf
10. QuickBird Medical, "IEC 62304 Edition 2 has been delayed", 10 September 2026 — https://quickbirdmedical.com/en/news/iec-62304-edition-2-august-2026/
