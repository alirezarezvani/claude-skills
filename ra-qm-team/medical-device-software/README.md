# medical-device-software

> IEC 62304 decides which lifecycle activities your device software needs.
> FDA decides how much of that you submit, on a different input. FD&C Act 524B
> decides whether you owe a cybersecurity plan and an SBOM, on yet another.
> This plugin keeps the three apart and checks the evidence behind each.

Four deterministic scripts for manufacturers of medical device software and SaMD:

| Script | Question it answers |
|---|---|
| `software_safety_classifier.py` | What IEC 62304 class is each software system and item (4.3, A1 external controls, segregation)? Basic or Enhanced FDA documentation? Is it a 524B cyber device? |
| `lifecycle_gap_check.py` | Is every activity the class requires done, with evidence? With `--security`, the IEC 81001-5-1 activities too; with `--legacy`, clause 4.4. |
| `soup_register_check.py` | Is every SOUP item identified (8.1.2), specified (5.3.3/5.3.4), anomaly-reviewed (7.1.3), supported, and in the SBOM? |
| `trace_matrix_check.py` | Is every requirement traced and tested, every risk control linked to a hazard and verified, and the release free of open failures? |

No network, nothing submitted. Python standard library only.

## How sure the rules are

IEC 62304 and IEC 81001-5-1 are paywalled. Each claim in the references is labelled:

- 🟢 checked against the primary text (FDA guidance, 21 U.S.C. 360n-2, FDA recognised-standards database, MDCG 2019-16, IEC public samples and the ISH1:2025 preview, BSI notified-body material);
- 🟡 two or more independent secondary sources agree (the IEC 62304 class-by-clause table);
- 🔴 not verified, do not rely on it (whether EN 62304 or EN IEC 81001-5-1 is cited in the Official Journal under the MDR).

Your licensed copy of the standard prevails over this plugin.

**Not a conformity assessment and not regulatory advice.** A notified body or FDA reviewer may read a borderline class or an NA justification differently.

## Install

```bash
/plugin marketplace add alirezarezvani/claude-skills
/plugin install medical-device-software@claude-code-skills
```

## Use

```bash
/cs-medical-device-software inventory.csv assessment.csv soup.csv sbom.json trace.csv   # full pass
/cs-soup-review soup.csv sbom.json                                                       # SOUP and SBOM only
```

Or run the scripts directly. Each has `--help`, `--sample`, `--template` and `--output json`:

```bash
cd skills/medical-device-software
python scripts/software_safety_classifier.py --sample
python scripts/lifecycle_gap_check.py --sample
python scripts/soup_register_check.py --sample
python scripts/trace_matrix_check.py --sample
```

Every `--sample` deliberately contains blockers and exits 4.

## What it refuses

- A claimed class below what the harm allows, or an item below its system with no segregation rationale.
- An unverified external risk control used to lower the class.
- A lifecycle assessment that skips a required activity, or marks a non-conditional one NA.
- SOUP with no exact version, or a class B/C SOUP item with no anomaly-list review.
- A class B/C risk control with no passing test; with `--release`, any open failed or unrun test.

## Related skills

`mdr-745-specialist` (MDR class and technical documentation), `fda-consultant-specialist` (submission pathway), `risk-management-specialist` (ISO 14971), `cra-readiness` (non-device apps and gateways under the EU CRA).

## License

MIT. See the repository LICENSE.
