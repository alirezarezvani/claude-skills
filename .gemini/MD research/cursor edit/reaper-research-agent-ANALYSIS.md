# REAPER Research Agent — Analysis Note

Brief verification of the original prompt and why the optimized Gemini + Cursor skill files differ.

## Gaps in the original

| Gap | Issue |
|-----|--------|
| “regex/AST tree-parsing” | Misframes RPP: it is a **nested chunk** format, not a classic AST. Regex-only is brittle on large/nested projects. |
| “headless or direct ReaScript … vs reapy” | Underspecified. **reapy needs a running REAPER** (distant API) for most live ops; true headless live control is limited. Offline work should use RPP parsers / CLI render paths. |
| Config surface | Mentions `reaper-kb.ini` only; misses `reaper.ini`, FX chains, SWS, ReaPack, ExtState, Actions. |
| No evidence discipline | No cite/verify rules → high risk of invented API names. |
| No dual-path (offline vs live) | Mixing file mining and live control without a decision table. |
| No MCP awareness | Cursor environments may have `user-reaper`; original never routes to live tools. |
| Weak deliverable schema | Constraints listed, but no turn-level output format or anti-hallucination checklist. |
| Sibling drift | Ableton + cross-DAW prompts exist; REAPER prompt didn’t fence scope against Ableton LOM conflation. |

## Corrections verified

1. **RPP = nested chunks** (`<REAPER_PROJECT`, `<TRACK`, …). Prefer `rpp` / `rppxml` / `reaproj` / ReaTeam state-chunk docs over naive regex.
2. **reapy** wraps ReaScript and, for external Python, talks to a **running** REAPER; not a drop-in headless DAW API.
3. **Config corpus** for habit mining: `reaper-kb.ini`, `reaper.ini`, Actions/custom actions, ExtState, FX chains, SWS/ReaPack.
4. **Local-first privacy** kept as a hard default in both optimized files.
5. **Cursor path:** prefer `user-reaper` MCP when REAPER is open; else offline RPP parse.

## Why each edit improves results

- **Explicit role + success criteria** → Gemini stays on research/design, not fluff.
- **Workflow (scope→sources→verify→design→templates→risks)** → consistent, checkable turns.
- **Corrected pillars** → fewer dead-end “AST/headless” designs.
- **Evidence priority + UNVERIFIED labels** → reduces API hallucination.
- **Output schema + checklist** → paste-ready deliverables every turn.
- **Cursor skill: short + trigger-rich description** → discoverable; token-efficient body.
- **MCP vs offline table** → agents pick the right tool instead of parsing files when live control is available.

## Files produced

- `reaper-research-agent-GEMINI.md` — Gem / system prompt  
- `reaper-research-agent-CURSOR-SKILL.md` — copy to `~/.cursor/skills/reaper-research-automation/SKILL.md`  
- This analysis note
