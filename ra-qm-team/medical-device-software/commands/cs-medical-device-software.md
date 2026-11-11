---
disable-model-invocation: true
description: Full IEC 62304 / IEC 81001-5-1 pass on medical device software - classify, check lifecycle activities for the class, check SOUP and SBOM, gate the trace matrix for release.
argument-hint: "inventory.csv [assessment.csv] [soup.csv] [sbom.json] [trace.csv]"
---

# /cs-medical-device-software

Answer one question about `$ARGUMENTS`: **what class is this software, what does that class require, and what stands between it and release or submission?**

Ask first for anything missing: the worst harm each item can contribute to, any risk control outside the software and how it was verified, whether the device can connect to the internet by any path (USB included), and the markets (EU, US). Never assume an activity is done because nobody mentioned it.

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/medical-device-software/scripts/software_safety_classifier.py --inventory <inventory.csv>
python ${CLAUDE_PLUGIN_ROOT}/skills/medical-device-software/scripts/lifecycle_gap_check.py --class <A|B|C> --security --assessment <assessment.csv>
python ${CLAUDE_PLUGIN_ROOT}/skills/medical-device-software/scripts/soup_register_check.py --register <soup.csv> --sbom <sbom.json> --cyber-device
python ${CLAUDE_PLUGIN_ROOT}/skills/medical-device-software/scripts/trace_matrix_check.py --matrix <trace.csv> --class <A|B|C> --release
```

Each script prints an empty input with `--template`. Drop `--security` and `--cyber-device` only when the device has no connectivity at all.

## Report

1. Class per system and item, FDA documentation level, cyber device yes/no, each with the deciding input.
2. Blockers with the clause, then gaps, with owners.
3. Confidence: which calls rest on secondary sources (🟡) and should be checked against the licensed standard.
4. What was not checked: whether evidence is adequate, whether tests exercise the requirement (reviewer), legal questions (counsel).

Never approve a class, a release or a submission. Name who does.
