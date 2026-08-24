# interview (Phase 1)

Interview a founder into a validated Claude Managed Agent **build sheet** —
primitives table + v1/v2 deferrals + eval plan. No API key needed in this phase.

## Usage

```bash
python3 scripts/interview_planner.py \
  --job "Triage overnight support email" --trigger schedule \
  --inputs "gmail,memory" --actions "label" \
  --dod "one label per email, grounded reason" --recurrence daily \
  --out ./my-agent/plan.json

python3 scripts/build_sheet_builder.py --plan ./my-agent/plan.json --out-dir ./my-agent
python3 scripts/primitives_validator.py --sheet ./my-agent/build-sheet.json
```

## Tools

| Tool | Purpose |
|---|---|
| `interview_planner.py` | six intake slots → primitives skeleton + deferrals |
| `build_sheet_builder.py` | assemble/normalize `build-sheet.json` |
| `primitives_validator.py` | validate vs CMA limits (PASS/WARN/FAIL, exit 1 on FAIL) |

The build-sheet schema and a worked example live in
[`../../assets/`](../../assets/); the intake-slot mapping is documented in
[`../../references/interview-to-config.md`](../../references/interview-to-config.md).
