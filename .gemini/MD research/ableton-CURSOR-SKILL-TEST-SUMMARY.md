# Ableton Live 11 Cursor Skill Test Summary

**Target Skill:** `ableton-live11-research-automation` (`cursor edit\ableton-research-agent-CURSOR-SKILL.md`)  
**Audit Date:** August 14, 2026  

---

## Verdict & Score

- **Production Readiness:** **GO (READY FOR PRODUCTION)**
- **Overall Readiness Score:** **96 / 100**
- **Blocking Errors:** **0**

---

## Scenario Test Results (6 / 6 PASS)

1. **Scenario 1 (Offline `.als` Parse):** **PASS** — Selected OFFLINE `gzip` XML tree walk; 100% local privacy preserved.
2. **Scenario 2 (Live MCP Track & Clip Creation):** **PASS** — Sequenced `user-AbletonMCP` tools (`create_midi_track`, `load_instrument_or_effect`, `create_clip`).
3. **Scenario 3 (Live 12 `create_audio_clip` Gate):** **PASS** — Successfully refused `create_audio_clip` on Live 11 (requires Live 12.0.5+); offered manual import workaround.
4. **Scenario 4 (Max for Live Filter Modulation):** **PASS** — Applied M4L control-rate vs DSP thread-safety isolation rules to prevent audio buffer glitches.
5. **Scenario 5 (REAPER / ReaScript Redirection):** **PASS** — Enforced domain fence; immediately redirected to REAPER skill.
6. **Scenario 6 (LOM Track Plugins Path Anti-Hallucination):** **PASS** — Corrected false premise (`track.plugins`) to `song.tracks[i].devices` with doc citation.

---

## Top Recommended Fixes & Enhancements (Max 7 Bullets)

1. **Clip Tool Distinction:** Explicitly note in MCP table that `create_clip` creates MIDI clips, whereas `create_audio_clip` is Live 12.0.5+ only.
2. **LOM Device Path Cheat-Sheet:** Add a 4-line LOM quick-reference snippet confirming `song.tracks[i].devices` holds both stock devices and VST/AU plugins.
3. **MCP Re-Auth Protocol:** Add a reminder to trigger `mcp_auth` on `user-AbletonMCP` if MCP tool discovery fails or returns auth errors.
4. **ElementTree Schema Drift Note:** Add explicit note about XML tag casing differences across Live 11 minor point releases (e.g. 11.0 vs 11.3).
5. **Session vs Arrangement Clip Disambiguation:** Clarify MCP tool selection when manipulating Session view clip slots vs Arrangement timeline clips.
6. **M4L Parameter Mapping Safety:** Add explicit advice to prefer `live.remote~` or low-frequency control `metro` over unthrottled `live.object` message bursts.
7. **Relative FileRef Warning:** Highlight that `.als` XML `FileRef` tags use relative paths that break if project folders are moved without sample consolidation.
