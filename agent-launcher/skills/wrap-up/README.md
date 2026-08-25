# wrap-up (close-out)

Recap every CMA primitive the founder owns, regenerate the single-file overview
page, and suggest the next 1–2 upgrades. The last stop before `phase=done`.

## Usage

```bash
python3 scripts/primitives_inventory.py --sheet ./my-agent/build-sheet.json --goal ./my-agent/goal.json
python3 scripts/overview_page.py --sheet ./my-agent/build-sheet.json --out-dir ./my-agent --status live
python3 scripts/upgrade_suggester.py --sheet ./my-agent/build-sheet.json --top 2
```

## Tools

| Tool | Purpose |
|---|---|
| `primitives_inventory.py` | table of everything owned (agent/env/session/memory/outcome/deployment) |
| `overview_page.py` | regenerate self-contained `agent-overview.html` (template in [`../../assets/`](../../assets/)) |
| `upgrade_suggester.py` | rank next moves from deferrals + standing hardening steps |
