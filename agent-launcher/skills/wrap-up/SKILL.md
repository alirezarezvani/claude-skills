---
name: wrap-up
description: "Use when closing out a launched managed agent ('wrap up', 'what do I own now'). Inventories primitives with primitives_inventory.py, regenerates the overview with overview_page.py and suggests next upgrades with upgrade_suggester.py."
license: MIT
metadata:
  version: 2.11.2
  author: Alireza Rezvani
  tags: [cma, wrap-up, closeout, inventory, overview, upgrades, next-directions]
  compatible_tools: [claude-code, codex-cli, cursor, antigravity, opencode, gemini-cli]
---

# Wrap-up — close it out

The explicit close-out. Confirm what's live, regenerate the shareable overview,
and name the next 1–2 upgrades so the founder leaves with a clear roadmap. The
`./my-agent/` folder keeps working after the session ends.

## Workflow

1. **Inventory what they own.**
   ```bash
   python3 scripts/primitives_inventory.py \
     --sheet ./my-agent/build-sheet.json --goal ./my-agent/goal.json
   ```
   Tables agent / environment / session / memory / outcome / deployment and the
   phases completed.
2. **Regenerate the overview page.**
   ```bash
   python3 scripts/overview_page.py \
     --sheet ./my-agent/build-sheet.json --out-dir ./my-agent \
     --status live --loop-shape cron-loop --last-verdict satisfied
   ```
   Self-contained `agent-overview.html` (inline CSS, theme-aware, no external
   assets) — shareable as-is.
3. **Suggest the next moves.**
   ```bash
   python3 scripts/upgrade_suggester.py --sheet ./my-agent/build-sheet.json --top 2
   ```
   Ranks recorded deferrals (v1 before v2, real-integration first) plus standing
   hardening (tighten networking, pin the agent version, nest an outcome).
4. **Finalize.** Ensure `NEXT-DIRECTIONS.md` is current (Phase-4 tool), then
   `goal_state.py advance` → `phase=done`.

## Hard rules

- **Recap what's actually live** — read it from the sheet + goal state, never
  assert primitives that weren't created.
- **The overview is single-file** — no external assets, so it shares cleanly.
- **Every next move names the exact mechanism.**

## Forcing-question library (recommend + cite)

1. "Confirm what's live vs still a plan?" *Recommend:* inventory from the sheet.
   *Cite:* this SKILL. 
2. "Which single upgrade has the highest payoff?" *Recommend:* the top-ranked v1
   deferral. *Cite:* upgrade_suggester ranking.
3. "Is the overview page current?" *Recommend:* regenerate after any change.
   *Cite:* this SKILL.

## Tools

- `scripts/primitives_inventory.py` — recap every owned primitive.
- `scripts/overview_page.py` — regenerate single-file agent-overview.html.
- `scripts/upgrade_suggester.py` — next 1–2 upgrades with mechanisms.
