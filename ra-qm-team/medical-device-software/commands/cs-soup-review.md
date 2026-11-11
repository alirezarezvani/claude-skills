---
disable-model-invocation: true
description: Review a medical device SOUP register against IEC 62304 (8.1.2, 5.3.3, 5.3.4, 7.1.3) and IEC 81001-5-1, and cross-check it with the SBOM for FD&C Act 524B.
argument-hint: "soup_register.csv [sbom.json] [--class A|B|C]"
---

# /cs-soup-review

Answer one question about `$ARGUMENTS`: **is every third-party and legacy component identified, specified, reviewed for known anomalies and in the SBOM?**

Ask for the software safety class if it is not given (it decides whether 5.3.3, 5.3.4 and 7.1.3 apply) and whether the device is a 524B cyber device.

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/medical-device-software/scripts/soup_register_check.py --register <soup.csv> --sbom <sbom.json> --cyber-device
```

Use `--template` to start a register. `--max-review-days` and `--eos-warn-days` are policy settings; ask for the values in the user's SOP.

## Report

1. Blockers per item with the clause: no exact version, no requirements, anomaly list not reviewed, past end of support with no plan, no vulnerability monitoring.
2. SBOM drift: in the build but never assessed, assessed but no longer shipped.
3. Items whose 81001-5-1 risk-transfer category (maintained, supported, required) is missing or out of date.
4. What was not checked: whether the anomaly review reached the right decision.
