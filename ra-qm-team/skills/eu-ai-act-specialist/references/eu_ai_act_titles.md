# EU AI Act (Regulation (EU) 2024/1689) — Titles I–XII Walkthrough

This reference answers exactly one decision: **what does each Title of the Act actually require, and which Articles do I cite in compliance artifacts?**

Pair with `scripts/ai_system_risk_classifier.py` to map a system to obligations.

## Structure of the Regulation

The Act has 13 Titles + 13 Annexes. Adopted as Regulation (EU) 2024/1689 (the "AI Act"); published in OJEU L on 12 July 2024; entered into force 1 August 2024 (Article 113).

## Title I — General Provisions (Articles 1–4)

| Article | Topic | Key requirement |
|---|---|---|
| **1** | Subject matter | Establishes harmonised rules for AI systems placed on EU market, used or put into service |
| **2** | Scope | Applies to providers, deployers, importers, distributors, authorized representatives. Extraterritorial: applies to non-EU providers placing systems on EU market. Excludes military / national security / pure scientific research |
| **3** | Definitions | "AI system" (Article 3(1)): a machine-based system designed to operate with varying levels of autonomy that may exhibit adaptiveness after deployment; infers from input how to generate outputs (predictions, content, recommendations, decisions). Per Commission Feb 2025 Guidelines, excludes simple rule-based systems with no adaptiveness |
| **4** | AI literacy | **Applies from 2 Feb 2025; replaced by Regulation (EU) 2026/1744.** Providers and deployers "shall take measures to support" the AI literacy of their staff; the text no longer requires any specific level of literacy (Art 4(1) as replaced). The Commission publishes practical examples (Art 4(2)) and the Board adopts recommendations (Art 4(3)) 🟢 |
| **4a** | Special categories of personal data for bias detection | **New, added by 2026/1744; replaces Art 10(5), which is deleted.** Providers of high-risk systems may exceptionally process special-category data for bias detection and correction under Art 10(2)(f)-(g), subject to conditions (a)-(f) (Art 4a(1)). Providers and deployers of other AI systems and models, and deployers of high-risk systems, may do so where strictly necessary under the same conditions (Art 4a(2)); this creates no obligation to run bias detection 🟢. GDPR Art 9(2) still needs its own legal basis 🔴 (our reading; check with your DPO) |

## Title II — Prohibited AI Practices (Article 5)

**In force from 2 Feb 2025.** Penalty: up to EUR 35M or 7% worldwide annual turnover (Article 99).

8 prohibited categories per Article 5(1):

- **(a)** Subliminal techniques beyond awareness causing harm
- **(b)** Exploitation of vulnerabilities (age, disability, socioeconomic situation)
- **(c)** Social scoring by public authorities causing detrimental treatment
- **(d)** Predictive policing based solely on profiling natural persons (with narrow law-enforcement exceptions per Article 5(2))
- **(e)** Untargeted scraping of facial images for facial recognition databases
- **(f)** Emotion recognition in workplace and educational institutions
- **(g)** Biometric categorisation by sensitive attributes (race, religion, political opinions, sexual orientation, etc.)
- **(h)** Real-time remote biometric identification in publicly accessible spaces for law-enforcement purposes (with narrow Article 5(2)(d)–(h) exceptions)

**Added by Regulation (EU) 2026/1744 (apply from 2 Dec 2026 🟡: date per ActuIA, HAQQ and euai-act; the Art 113 text was not read verbatim):**

- **(ba)** AI systems that generate or manipulate realistic images, video, audio or similar material of an identifiable person's intimate parts or sexually explicit activity without freely given, specific, informed, unambiguous and explicit consent 🟢
- **(bb)** AI systems that generate or manipulate child sexual abuse material within Directive 2011/93/EU, Art 2(c) and (e), except where a national "without right" defence applies 🟢
- **Scope (Art 5(1a)):** a provider is caught where that generation is the intended purpose, or a reasonably foreseeable and reproducible outcome without adequate safeguards; a deployer only where it uses the system for that purpose 🟢. A general-purpose image or video generator therefore needs documented safeguards, not just terms of use 🔴 (our reading; a market surveillance authority may set the "adequate safeguards" bar higher)

## Title III — High-Risk AI Systems (Articles 6–49)

The densest part of the regulation. **Annex III stand-alone high-risk obligations apply from 2 Dec 2027; Annex I sectoral (product-embedded) from 2 Aug 2028**, per Regulation (EU) 2026/1744 (the AI Omnibus, in force 27 Jul 2026), which deferred the original 2 Aug 2026 / 2027 dates. Article 50 transparency obligations were not deferred and apply from 2 Aug 2026.

### Chapter 1 — Classification (Articles 6–7)

- **Article 6(1)** + Annex I: AI systems that are safety components of products covered by sectoral law (machinery, toys, medical devices, etc.) are high-risk
- **Article 6(2)** + Annex III: AI systems in 8 categories (biometrics, critical infrastructure, education, employment, essential services, law enforcement, migration, justice) are high-risk
- **Article 6(3)**: carve-out — a system in Annex III is NOT high-risk if it performs a narrow procedural task, improves a previously completed human activity, detects decision-making patterns without replacing human assessment, or performs a preparatory task. **Profiling overrides the carve-out** (Article 6(3) last sentence)

See `high_risk_systems_annex_iii.md` for the detailed Annex III walkthrough.

### Chapter 2 — Requirements for High-Risk Systems (Articles 8–17)

| Article | Requirement |
|---|---|
| **8** | Compliance with all Section 2 requirements |
| **9** | Risk management system across full lifecycle |
| **10** | Data governance: training/validation/test datasets quality + bias examination. Art 10(5) deleted by 2026/1744; special-category processing for bias now sits in Art 4a |
| **11** | Technical documentation per Annex IV |
| **12** | Automatic event logging |
| **13** | Transparency + instructions for use to deployers |
| **14** | Human oversight design |
| **15** | Accuracy, robustness, cybersecurity |
| **16** | General provider obligations + named contact person |
| **17** | Quality management system (provider) |

### Chapter 3 — Obligations of Actors (Articles 22–27)

| Article | Topic | Applies to |
|---|---|---|
| **22** | Authorized representative | Non-EU providers must appoint one |
| **23** | Importer obligations | Verify provider conformity assessment before import |
| **24** | Distributor obligations | Verify CE marking before making available |
| **25** | Responsibilities along the value chain | Substantial modification turns deployer into provider |
| **26** | Deployer obligations | Use per instructions; human oversight; input data; logs; transparency |
| **27** | Fundamental Rights Impact Assessment (FRIA) | Public-sector deployers + essential-services deployers of high-risk |

### Chapter 4 — Notified Bodies (Articles 28–39)

Procedures for designating + monitoring notified bodies (involved in Module H conformity assessment per Annex VII).

### Chapter 5 — Standards, Conformity Assessment, Certificates, Registration (Articles 40–49)

| Article | Topic |
|---|---|
| **40** | Harmonised standards — presumption of conformity |
| **41** | Common specifications (where standards lacking) |
| **43** | Conformity assessment procedure (Module A internal control vs Module H notified body) |
| **47** | EU declaration of conformity (provider signs; 10-year retention) |
| **48** | CE marking |
| **49** | Registration in EU database (Article 71) for Annex III systems |

## Title IV — Transparency Obligations (Article 50)

**Applies from 2 Aug 2026** (Art 113; not deferred by 2026/1744). Generative systems placed on the market before 2 Aug 2026 have until **2 Dec 2026** for Art 50(2) only (new Art 111(4) 🟡; recital 38 of 2026/1744 confirms a four-month transitional period 🟢). Art 50(1) and 50(4) get no grace 🟡.

| Article 50 paragraph | Requirement |
|---|---|
| **50(1)** | Disclose AI interaction (chatbots): natural persons must be informed |
| **50(2)** | Mark synthetic content (machine-readable) as AI-generated |
| **50(3)** | Disclose emotion recognition / biometric categorisation to subjects (outside Article 5 prohibition) |
| **50(4)** | Disclose deepfakes (image/audio/video) — exception for art, satire, security |

## Title V — General-Purpose AI Models (Articles 51–55)

**In force from 2 Aug 2025.** See `gpai_obligations.md` for the detailed walkthrough.

| Article | Topic |
|---|---|
| **51** | Classification of GPAI with systemic risk (training compute ≥ 10²⁵ FLOPs) |
| **52** | Procedure for adding/removing systemic-risk designation |
| **53** | Obligations for ALL GPAI providers (technical docs, transparency to downstream, copyright policy, training data summary) |
| **54** | Authorized representative for non-EU GPAI providers |
| **55** | Additional obligations for systemic-risk GPAI (model evaluations, adversarial testing, incident reporting, cybersecurity) |

## Title VI — Measures in Support of Innovation (Articles 57–63)

| Article | Topic |
|---|---|
| **57** | AI regulatory sandboxes: at least one national sandbox operational by **2 Aug 2027** (Art 57(1) as amended by 2026/1744; was 2 Aug 2026). The AI Office may run a Union-level sandbox with priority access for SMEs and small mid-caps (new Art 57(3a)) 🟢 |
| **58** | Modalities for sandboxes |
| **59** | Further processing of personal data for AI development in sandboxes |
| **60** | Real-world testing of high-risk systems outside sandboxes |
| **62** | SME / start-up specific measures |

## Title VII — Governance (Articles 64–70)

| Article | Body |
|---|---|
| **64** | European Artificial Intelligence Office (the "AI Office") |
| **65** | European AI Board |
| **66** | Member State national competent authorities |
| **67** | Advisory Forum (industry + civil society) |
| **68** | Scientific Panel of independent experts |

## Title VIII — EU Database (Article 71)

EU-wide database of stand-alone high-risk Annex III AI systems. Provider registration before placing on market.

## Title IX — Post-Market Monitoring, Information Sharing, Market Surveillance (Articles 72–84)

| Article | Topic |
|---|---|
| **72** | Provider post-market monitoring system |
| **73** | Serious-incident reporting (provider) — 15 days general; 2 days for critical infrastructure |
| **74** | Market surveillance + AI Office cooperation |
| **75** | As amended by 2026/1744: the AI Office is exclusively competent for AI systems built on a GPAI model by the same provider or undertaking (except Annex I products, Annex III points 2 and 8, and Art 74(6) systems), and for systems that are or sit inside a VLOP or VLOSE (Art 75(1)). New Arts 75a-75b give it investigation, inspection and binding-commitment powers 🟢. A company integrating a third party's model stays with the national authority 🟡 |
| **76–84** | Market surveillance powers, enforcement, mutual assistance |

## Title X — Codes of Conduct and Guidelines (Articles 95–96)

Voluntary codes of conduct extending Title III principles to non-high-risk systems. Commission may issue guidelines.

## Title XI — Delegated and Implementing Acts (Articles 97–98)

Commission powers to update Annexes (notably Annex III categories) via delegated acts.

## Title XII — Final Provisions (Articles 99–113)

| Article | Topic |
|---|---|
| **99** | Penalties: up to EUR 35M / 7% turnover (Article 5); EUR 15M / 3% (most high-risk); EUR 7.5M / 1% (incorrect info) |
| **102** | Amendments to other regulations (medical devices, etc.) |
| **113** | Entry into force + application phasing (amended by 2026/1744: Annex III high-risk 2 Dec 2027, Annex I 2 Aug 2028) |

## Annexes — At a Glance

| Annex | Topic |
|---|---|
| **I** | List of EU sectoral product legislation (machinery, toys, MDR, IVDR, etc.) — Article 6(1) trigger |
| **II** | List of Union harmonisation legislation |
| **III** | High-risk AI systems referred to in Article 6(2) — 8 categories |
| **IV** | Technical documentation referred to in Article 11 (8 items) |
| **V** | EU declaration of conformity (Article 47) |
| **VI** | Conformity assessment Module A — Internal Control |
| **VII** | Conformity assessment Module H — Full Quality Assurance |
| **VIII** | Information to be submitted upon registration in EU database (Article 71) |
| **IX** | Information for testing in real-world conditions (Article 60) |
| **X** | Union legislative acts on large-scale IT systems |
| **XI** | Technical documentation for GPAI providers (Article 53) |
| **XII** | Transparency information for downstream providers (Article 53(1)(b)) |
| **XIII** | Designation of GPAI with systemic risk (Article 51 criteria) |

## When This Reference Doesn't Help

- **Specific Annex III high-risk system classification.** See `high_risk_systems_annex_iii.md`.
- **GPAI obligations detail.** See `gpai_obligations.md`.
- **Cross-walking to ISO 42001 / NIST AI RMF.** See `cross_framework_mapping_ai_act.md`.

---

**Source authorities (non-exhaustive):**

- **Regulation (EU) 2024/1689** — the AI Act (the binding regulation; published in OJEU L on 12 July 2024)
- **Regulation (EU) 2026/1744** of 8 July 2026 (Digital Omnibus on AI), OJ L 24.7.2026, in force 27 Jul 2026 — https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ%3AL_202601744 (Art 1 amendments to Arts 4, 4a, 5, 10, 43, 57, 75 read on 26 Nov 2026; Arts 99, 111 and 113 not read verbatim)
- **ActuIA**, "AI Act: obligations in force and delays under omnibus 2026/1744", 6 Oct 2026; **HAQQ**, "EU AI Act Amendments 2026", updated 22 Oct 2026 — secondary, used for the 2 Dec 2026 and Art 111(4) dates
- **European Commission** — Guidelines on the definition of an AI system (Feb 2025)
- **European Commission** — Guidelines on prohibited AI practices (Feb 2025)
- **European Commission Q&A** — AI Act explanatory materials (continuously updated)
- **European Data Protection Board (EDPB)** — Opinion 28/2024 (Dec 2024) on personal-data processing in AI models
- **European Data Protection Supervisor (EDPS)** — AI Act commentary + GDPR-AI Act interaction
- **ENISA** — Multilayer Framework for Good Cybersecurity Practices for AI (Mar 2023)
- **IAPP** — EU AI Act Tracker (continuously updated practitioner reference)
- **CEN-CENELEC JTC 21** — harmonised standards work programme (Article 40 reference)
