---
name: ableton-live11-research-automation
description: >-
  Researches and designs local-first Ableton Live 11 automation using saved Live
  artifacts, Max for Live, AbletonMCP, MIDI Remote Scripts, and the Live Object
  Model. Use for Live 11 Set analysis, .als parsing, M4L, LOM, Session or
  Arrangement automation, stock devices, or Ableton MCP workflows.
---

# Ableton Live 11 Research & Automation

Local-first guidance for Ableton Live 11. Flag Live 12-only APIs and never assume
they work in Live 11.

## Quick Start

1. Record exact Live `11.x.y`, edition, OS, installed devices/Packs, and Max for
   Live availability. Live 11 uses Max 8; do not propose Max 9.
2. Choose **OFFLINE**, **LIVE**, or **HYBRID**.
3. Discover runtime MCP tools or verify exact-version LOM/framework behavior.
4. Inspect first; for writes use plan → confirm → one bounded write → read back.
5. Report evidence, confidence, version gates, and a minimal next experiment.

## Scope fences

Use for:

- Read-only analysis of `.als`, `Backup/`, and explicitly selected local assets
- Live 11 LOM automation through MCP, M4L, or a Remote Script
- Session/Arrangement workflows and installed stock-device chains
- Local RAG over Live 11, Max 8, LOM, and personal production notes

Do not use for:

- Live 12-first features. Refuse `create_audio_clip` on Live 11; its underlying
  LOM operation requires Live 12.0.5+.
- REAPER, `.RPP`, or ReaScript; route to the REAPER skill/tools.
- Cloud ingestion of sets, samples, notes, or telemetry without explicit opt-in.

## Hard rules

1. **Privacy:** keep artifacts and indexes local by default. Omit or empty MCP
   `user_prompt`/telemetry fields. Before sending user text, inspect the installed
   bridge's telemetry destination and obtain opt-in for off-machine transmission.
2. **Saved artifacts:** Live 11 `.als` files are observed to be gzip-compressed
   XML, not a supported interchange format. Never claim its schema is stable.
3. **No direct `.als` writes:** parse copies read-only. Do not edit/recompress XML
   to change a Set. Apply supported changes through Live, then use Save/Save As.
4. **No invention:** verify LOM paths, `Live.*` calls, M4L objects, and MCP schemas
   against exact-version docs/runtime; otherwise label them `UNVERIFIED`.
5. **Live mutation:** inspect → snapshot relevant pre-state → plan → obtain user
   confirmation for audible/destructive action → one bounded write → read back.
   Stop on mismatch. Stopping transport is not rollback or proof of undo safety.
6. **Callbacks:** no blocking I/O, network waits, large parsing, or long loops in
   Remote Script scheduler callbacks, deferred M4L API callbacks, observers, or
   DSP/signal-rate code.
7. **Claims:** a saved Set shows structure/settings, not actual launch history,
   runtime behavior, or authoritative plug-in availability.

## Route

| Situation | Route |
|---|---|
| Live 11 open and Ableton MCP available | **LIVE MCP** |
| Live open, no MCP | **LIVE BRIDGE** — M4L or exact-version Remote Script |
| Live closed or cross-project analysis | **OFFLINE** — saved local artifacts |
| Mine saved patterns, then apply them | **HYBRID** — offline report then live writes |

If ambiguous, ask: “Is Live 11 open with MCP, or are we analyzing saved files
offline?” Do not silently choose a write-capable route.

## Workflow

### 1. Gate the environment

Capture:

- Exact Live `11.x.y`, edition (Intro/Standard/Suite), and OS
- Installed Packs/devices; use browser/runtime discovery before promising a device
- Max for Live license/edit capability; Live 11-compatible work uses Max 8 docs
- Read-only vs write request and whether Live is currently open

Device availability varies by edition and point release. Treat Operator, Wavetable,
Simpler, Drum Rack, and other names as examples until discovered.

### 2. Inspect sources

- Set/project: copied `*.als`, `Backup/*.als`, `Samples/`, `Presets/`, and
  `Ableton Project Info/`
- Optional artifacts: `.asd`, `.amxd`, `.adv`, `.alc`, User Library files,
  exported MIDI/audio, manuals, and user-selected notes
- Live state: discover MCP schemas, then use read tools before write tools

Offline Live-state inspection is limited to saved artifacts. `.als` is the primary
Set artifact, supplemented only by explicitly selected local project/library files.

### 3. Verify the contract

- Current state: runtime reads and the user's local artifacts
- LOM/M4L contracts and threading: exact Live 11 / legacy Max 8 documentation
- Remote Script behavior: installed exact-build scripts/framework source
- MCP capability: runtime schema and, for privacy claims, installed server source
- XML shape: copied fixture observations, never a public API claim

### 4. Execute the selected route

#### OFFLINE — safe `.als` inspection

Use a copied fixture. Validate gzip, impose compressed and expanded byte limits,
stream with `xml.etree.ElementTree.iterparse`, cap depth/element count, clear
processed elements, and catch gzip/XML errors. Use `defusedxml` for untrusted Sets.
Never use unbounded `gzip.open(...).read()` followed by `ET.fromstring(...)`.

Extract only observed fields, such as tracks, devices, Session layout, scene names,
launch settings, tempo/time signature, Arrangement clips, and groove references.
Do not infer a performed scene sequence without logs; repeated-set tendencies are
heuristics and must be labeled as such.

References may break when a Set is separated from its project/dependencies. Prefer
Collect All and Save, then move the whole Project.

#### LIVE MCP — runtime-discovered tools

Call `GetMcpTools` for `user-AbletonMCP` (or the environment's list-tools
equivalent), inspect full schemas, then call only discovered tools. Start with
session/track reads. Omit telemetry text unless its destination is audited and the
user opted in.

The following table is **illustrative only**, based on one observed server snapshot;
runtime discovery is authoritative and forks may differ:

| Category | Illustrative tools |
|---|---|
| Read | `get_session_info`, `get_track_info`, `get_arrangement_clips` |
| Tracks/clips | `create_midi_track`, `create_clip`, `add_notes_to_clip`, `set_clip_name` |
| Transport | `set_tempo`, `start_playback`, `stop_playback`, `fire_clip`, `stop_clip` |
| Browser | `get_browser_tree`, `get_browser_items_at_path`, `load_instrument_or_effect` |
| Arrangement | `switch_to_arrangement_view`, `duplicate_to_arrangement`, `set_arrangement_clip_name` |
| Refused on Live 11 | `create_audio_clip` — Live 12.0.5+ only |

Tool presence does not prove Live 11 compatibility. Verify each schema's version
notes. Preserve Session clip-slot indexes vs ordered Arrangement clip indexes.

#### LIVE BRIDGE — Remote Script or M4L

**Remote Scripts**

- Third-party scripts are a supported extension mechanism, but `_Framework`,
  `ableton.v2`, and related Python surfaces are private, undocumented, and
  exact-build-sensitive—not a stable official SDK.
- Pin exact Live 11.x and framework generation; inspect installed scripts/source.
- Install third-party scripts under `<User Library>/Remote Scripts/`; do not edit
  the application bundle.
- If verified for that build, the application entry is
  `Live.Application.get_application().get_document()`. Within a `ControlSurface`,
  prefer the exact `song`/`song()` accessor exposed by the selected framework.
- Keep scheduler/update callbacks short and non-blocking; marshal external work
  back through the framework's verified scheduling mechanism.

**Max for Live**

- Use Live 11-compatible Max 8 docs. Verify M4L authoring capability first.
- Ordinary Live API traffic is deferred on Live's main thread; it is not an
  audio-thread API. `live.observer` notifications must not directly mutate the Set;
  schedule follow-up API work with `deferlow` where required.
- `live.remote~` is the distinct signal-rate parameter-control mechanism. Do not
  use LOM/OSC for sample-accurate or note-on timing.
- Handle dynamic IDs, `id 0`, path changes, and observer teardown.
- OSC/Node latency is implementation-dependent; benchmark round-trip latency and
  state timing guarantees rather than claiming it is inherently high or low.

Common documented paths include `song.tracks`,
`song.tracks[i].clip_slots[j]`, `clip_slot.clip`, `track.devices`, and
`device.parameters`. Verify names and mutability in the Live 11 LOM before use.

### 5. Verify and report

For every live write, read back the smallest affected state. For offline batches,
test one copied Set, record observed tags, then expand. Include version/edition,
route, evidence, confidence, privacy status, and unresolved `UNVERIFIED` claims.

## Worked example

**Input:** “Live 11 is closed. Analyze a copy of `Song.als` and list devices.”

**Actions:**

1. Route **OFFLINE**, read-only; record exact Live version if known.
2. Check compressed size; stream-decompress under an expanded-byte cap.
3. `iterparse` a copied fixture, cap depth/elements, and collect observed device
   nodes with track context.
4. Do not infer launch history; do not modify/recompress the Set.

**Output sketch:**

```markdown
# Device inventory
## Scope
Live 11 | OFFLINE | copied Song.als | read-only
## Findings
- Track "Bass": Operator — medium confidence; observed XML tag, availability unverified
## Verify
Parsed under limits; 1 Set; tags are observations, not a supported schema
## Next
Confirm edition/installed devices before generating a live chain
```

## Output contract

Return:

1. Scope: exact Live version/edition/OS, route, read/write
2. Findings: claims with confidence and source
3. Approach: primary path and fallback
4. Actions/templates: minimal and version-gated
5. Verification: pre-state/read-back or copied-fixture result
6. Risks: privacy, schema drift, callbacks, edition, destructive effects
7. Next: smallest safe experiment or explicit user action

## Anti-patterns

- Directly editing/recompressing `.als` XML
- Unbounded gzip expansion or whole-document XML parsing
- Inventing `track.plugins`, LOM methods, MCP tools, or framework accessors
- Calling private Remote Script frameworks an official stable API
- Treating M4L Live API callbacks as audio-thread execution
- Mutating the Set directly from a `live.observer` notification
- Recommending `create_audio_clip` on Live 11
- Claiming saved Session layout proves launch history
- Sending MCP telemetry text or private artifacts off-machine by default
- Treating transport stop as rollback
- REAPER/ReaScript advice inside this skill
