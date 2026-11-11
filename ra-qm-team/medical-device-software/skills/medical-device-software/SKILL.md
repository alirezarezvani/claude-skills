---
name: medical-device-software
description: Use for any question about the software inside a medical device, SaMD or regulated health app - which IEC 62304 safety class (A/B/C) it is and how much process and documentation that class needs, what to record about open-source or third-party libraries (SOUP, SBOM), trace matrix and release testing, IEC 81001-5-1 security, or the FDA documentation level and 524B cyber-device duties. Checks the user's files with four scripts that cite the clause.
argument-hint: "[software inventory CSV | lifecycle assessment CSV | SOUP register CSV + SBOM | trace matrix CSV]"
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "Four deterministic stdlib scripts with blocking exit codes (IEC 62304 4.3 classifier with FDA documentation level and 524B cyber-device check, class-scoped lifecycle gap check with IEC 81001-5-1, SOUP register and SBOM cross-check, trace matrix release gate); clause claims labelled primary-verified, secondary-agreed or unverified"
  distinct_from: "mdr-745-specialist (MDR device class, technical documentation); fda-consultant-specialist (submission pathway); risk-management-specialist (ISO 14971 file); cra-readiness (CRA, which excludes medical devices); regulatory-affairs-head (strategy)"
---

# Medical Device Software

> **Portability:** 4 stdlib scripts, no network. Fill CSVs, run, keep the output with the software file.
> **Not a conformity assessment.** IEC 62304 is paywalled: clause markers here come from two agreeing secondary sources (🟡) and your licensed copy prevails. A notified body or FDA reviewer can read a borderline call differently.

Software files fail review in the same places: a class claimed lower than the
harm allows, an "external" risk control that lives in the same software system,
a SOUP list with "latest" as the version and no anomaly review, a trace matrix
with risk controls nobody tested, and security treated as an afterthought.
Three classifications get confused, and they use different inputs:

| Question | Decided by | Assessed |
|---|---|---|
| IEC 62304 class A/B/C (which activities) | worst-case harm, clause 4.3 + A1 Fig. 3 | **after** risk controls external to the software system |
| FDA Basic / Enhanced (what you submit) | probable risk of death or serious injury | **before** any risk controls |
| FD&C Act 524B cyber device | software + any internet-capable path (USB counts) | not risk-based |

## Workflow

```bash
# 1 - Classify: system and item classes, FDA level, cyber device?
python scripts/software_safety_classifier.py --inventory assets/software_inventory.example.csv
# 2 - Gap check: is every activity the class requires done, with evidence?
python scripts/lifecycle_gap_check.py --class B --security --assessment assets/lifecycle_assessment.example.csv
# 3 - SOUP: identified, specified, anomaly lists reviewed, in the SBOM?
python scripts/soup_register_check.py --register assets/soup_register.example.csv --sbom assets/sbom.example.cdx.json --cyber-device
# 4 - Release: every requirement tested, every risk control verified?
python scripts/trace_matrix_check.py --matrix assets/trace_matrix.example.csv --class C --release
```

Class first: steps 2 to 4 take the class from step 1. `--template` prints an
empty input; `lifecycle_gap_check.py --list --class X` prints the required ids.

## The gates block on (exit 4)

1. A claimed class below what the harm allows, or an item below its system without a segregation rationale — 62304 4.3.
2. An external risk control used to lower the class that is not itself verified — 62304 4.3 (A1).
3. A required activity NOT MET, or NA where the clause is not conditional — the class table (A1 Table A.1).
4. A SOUP item with no exact version (8.1.2), no stated requirements (5.3.3/5.3.4) or no anomaly-list review (7.1.3) for class B/C, or past end of support with no plan.
5. A class B/C risk control with no hazard or no passing test (7.3.1, 7.3.3); with `--release`, any untested requirement or open failed result without an anomaly record (5.7, 5.8).
6. A cyber device with no vulnerability monitoring on a SOUP item — 524B(b)(1).

## Hard rules

- **Unassessed is not MET.** The gap check refuses a file that skips a required id.
- **Unclassified is class C.** Unknown inputs never round down.
- **Severity decides the class, not probability.** Only verified external controls lower it.
- **Class A still tests.** Software system testing (5.7) applies to every class since A1.
- **Mark the confidence.** 🟢 primary text checked · 🟡 secondary sources agree · 🔴 not verified. EN 62304 and EN IEC 81001-5-1 are not confirmed as cited in the OJ under the MDR; never claim presumption of conformity without checking the current list.
- **Never sign or submit.** The scripts prepare evidence; the manufacturer's named people approve the class, the release and the submission.

## Scripts

| Script | Role | Exit codes |
|---|---|---|
| `scripts/software_safety_classifier.py` | 62304 4.3 class per system and item, segregation, FDA documentation level, 524B cyber device | 0 classified · 2 findings · 3 bad input · 4 blocked |
| `scripts/lifecycle_gap_check.py` | 62304 activities by class (+4.4 legacy), 81001-5-1 activities with `--security` | 0 ready · 2 gaps · 3 · 4 blocked |
| `scripts/soup_register_check.py` | 8.1.2, 5.3.3/5.3.4, 7.1.3, end of support, 81001-5-1 risk-transfer category, SBOM cross-check (CycloneDX/SPDX) | 0 pass · 2 · 3 · 4 blocked |
| `scripts/trace_matrix_check.py` | system → software requirement → test → result, risk control → hazard, release state | 0 pass · 2 · 3 · 4 blocked |

All support `--help`, `--sample`, `--template` and `--output json`.

## References and assets

- [`references/classification_and_documentation_levels.md`](references/classification_and_documentation_levels.md) — 62304 class decision path, external controls, segregation, FDA Basic/Enhanced, 524B, EU status, Edition 2 (10 sources)
- [`references/lifecycle_requirements_by_class.md`](references/lifecycle_requirements_by_class.md) — every clause by class, legacy software, regulatory standing (7 sources)
- [`references/secure_lifecycle_81001_5_1.md`](references/secure_lifecycle_81001_5_1.md) — 81001-5-1 clause map, ISH1:2025 risk transfer, mapping to 524B and MDCG 2019-16 (7 sources)
- [`references/soup_and_traceability.md`](references/soup_and_traceability.md) — SOUP evidence by class, SBOM, what reviewers check in a trace matrix (8 sources)
- `assets/*.example.csv`, `assets/sbom.example.cdx.json` — input formats, generated from each script's `--sample`
