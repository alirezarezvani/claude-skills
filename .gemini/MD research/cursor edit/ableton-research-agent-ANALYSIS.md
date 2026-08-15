# Ableton Live 11 Research-Agent Verification

## Gaps in original prompt

- The prompt names useful domains but does not define an evidence hierarchy, a Live 11 compatibility gate, or a boundary between offline Set inspection and live control.
- It treats `.als` XML as broadly available project truth without warning that the schema is undocumented/version-sensitive, referenced media and devices may live outside the Set, and third-party plug-in state is generally opaque.
- It does not distinguish a **Live Set** (`.als`) from its containing **Live Project** folder, nor Session clips from Arrangement clips.
- It conflates several control surfaces: Max for Live's documented Live Object Model (LOM), Live's Python 3 MIDI Remote Script environment, and an MCP server's particular wrapper tools. A method exposed by one is not automatically exposed by the others.
- It asks for script blueprints without requiring capability discovery, read-before-write behavior, undo/backup planning, post-action verification, or protection against playback/audio-thread disruption.
- Stock-device coverage lacks edition and point-release qualifiers. Live 11 Intro, Standard, and Suite differ, and Drift is a Live 11.3 addition.
- “Audio and MIDI ingestion” needs privacy and provenance rules: default to metadata/indexes and user-selected roots; never assume external samples, plug-ins, Packs, or User Library content are embedded in an `.als`.

## Corrections / verified facts

- A **Live Set** is Live's document; it normally resides in a **Live Project** folder with related media. A Set has two clip environments sharing the same tracks: **Session View** (non-linear clip launching) and **Arrangement View** (linear timeline). Session tracks are columns, scenes are rows, and a scene launches the row. On one track, a playing Session clip overrides Arrangement playback until the user returns that track to Arrangement.
- Clips are MIDI or audio containers. A Session clip occupies a `ClipSlot`; Arrangement clips sit at timeline positions. Do not use “scene” for an Arrangement section.
- `.als` is gzip-compressed XML. Offline, a read-only parser can usually inventory tempo/time signature, tracks/returns, names, Session slots/scenes, Arrangement clips, MIDI notes, device chains/names, automation and file references, subject to Live-version schema drift.
- The XML is not a supported public interchange schema. Preserve the original, enforce decompression/size/XML limits, reject malformed input, and avoid in-place XML rewriting. If writing is ever allowed, write a new file, validate IDs/references, recompress as gzip, and open-test a disposable copy in the matching Live version.
- An `.als` often stores **references**, not all dependencies. Samples and M4L files may be external unless **Collect All and Save** was used; third-party plug-ins are not collected. `.asd` sample-analysis files are proprietary binary, not XML. Plug-in state in `.als` is commonly an opaque vendor blob: inventory or hash it, but do not claim generic parameter decoding.
- Offline parsing cannot report authoritative runtime state such as current meters, audible output, loaded/missing-device behavior, browser contents, transient playback state, or the result of executing devices. Those require Live (and often the original assets/plug-ins) running.
- Live 11 stock device families are **Instruments**, **MIDI Effects**, and **Audio Effects**, plus device Racks. Signal order on a MIDI track is MIDI effects → instrument → audio effects. High-level examples: instruments/samplers (Simpler, Sampler, Impulse), synthesis/physical modeling (Operator, Wavetable, Analog, Collision, Electric, Tension; Drift only in 11.3+), MIDI processing (Arpeggiator, Chord, Note Length, Pitch, Random, Scale, Velocity), and audio processing spanning EQ/dynamics, filter/modulation, delay/reverb, distortion/color, spectral processing, and utility/routing. Availability must be checked against edition and exact 11.x version.
- Max for Live devices use `.amxd`. Live 11 bundles **Max 8**; Max 9 is not compatible with Live 11. M4L devices can be instruments, MIDI effects, or audio effects and, unlike native devices, can be opened/customized in Max when the license/edition permits.
- Freezing an M4L device packages dependencies (for example subpatchers, media, JavaScript, images, externals) into the saved device for distribution. It is not Live's **Freeze Track** audio-render/CPU feature. Treat frozen devices as packaged artifacts; unfreeze/edit/save in Max rather than editing package internals.
- Relevant Live 11 LOM surfaces include Application/Application.View, Song (`live_set`), Song.View, Track, Scene, ClipSlot, Clip, Device/MaxDevice, DeviceParameter, MixerDevice, CuePoint, and control surfaces. M4L accesses documented members through `live.path`, `live.object`, `live.observer`, `live.remote~`, or the Max `LiveAPI` JavaScript object. Roots include `live_app`, `live_set`, `control_surfaces N`, and `this_device`.
- The LOM is a documented **subset**, not all of Live. Normal Live API messages run on Live's main thread and are deferred; `live.remote~` is the specialized path for real-time control of remotely mappable parameters. Never place blocking file/network/research work on Live's main or audio-sensitive path.
- Live 11 MIDI Remote Scripts run on **Python 3**. They are control-surface integrations running inside Live, not a general promise that arbitrary Python APIs are stable or supported. Never invent methods from private framework code or from a different Live build.
- A typical AbletonMCP bridge has two parts: an MCP server and a Python Remote Script enabled in Live, communicating locally (commonly via a localhost socket). Therefore its real-time tools require Live running, the script enabled, and a compatible Set/version; MCP connectivity alone does not prove Live-side readiness.
- The installed `user-AbletonMCP` surface groups into: inspection (`get_session_info`, `get_track_info`, `get_arrangement_clips`); track/clip authoring (`create_midi_track`, `create_clip`, `add_notes_to_clip`, naming); Session/transport (`fire_clip`, `stop_clip`, `start_playback`, `stop_playback`, `set_tempo`); browser/device loading (`get_browser_tree`, `get_browser_items_at_path`, `load_instrument_or_effect`, `load_drum_kit`); and Arrangement operations (`switch_to_arrangement_view`, `set_arrangement_time`, `duplicate_to_arrangement`, Arrangement clip naming).
- Critical compatibility finding: this installed bridge documents `create_audio_clip` as requiring **Live 12.0.5+** (`ClipSlot.create_audio_clip`). It must be unavailable/refused in a Live 11 agent. By contrast, this bridge marks `duplicate_to_arrangement` as Live 11/12. Tool presence is not proof of Live 11 support.

## Live 11 specificity checklist

- [ ] State and verify exact Live version (11.x.y), edition (Intro/Standard/Suite), OS, and Max version before advice or action.
- [ ] Prefer `/en/live-manual/11/` and Live 11 release notes; reject unqualified current LOM pages that explicitly target Live 12.x.
- [ ] Exclude Live 12-only features/APIs: Meld, Roar, Granulator III, native MIDI Transformations/Generators, Sound Similarity Search, and `ClipSlot.create_audio_clip`.
- [ ] Mark Drift as 11.3+, AUv3 support as 11.2+ on macOS, and Remote Scripts as Python 3.
- [ ] Confirm device/Pack availability by edition and browser discovery; never promise Suite devices in Intro/Standard.
- [ ] Separate offline `.als` evidence from live LOM/MCP observations in every answer.
- [ ] Discover actual MCP tools and parameters at runtime; do not infer a method from another fork, README, Live 12 docs, or private Remote Script internals.
- [ ] Snapshot/inspect before mutation, ask before destructive or audible transport actions, use bounded operations, and verify state after each write.
- [ ] Never claim rendered audio quality, plug-in parameter truth, or missing-asset resolution from XML alone.

## Stock / M4L / AbletonMCP pillars

- **Stock Live 11:** explain signal-flow categories and practical device-selection workflows; query the Live browser where possible; cite edition and 11.x availability; distinguish native devices, Racks, official M4L devices, Packs, and third-party plug-ins. Keep device lists illustrative unless generated from the user's installation.
- **Max for Live:** cover `.amxd`, editable vs frozen/package behavior, dependency handling, Max 8 compatibility, LOM navigation/query/set/call/observe/parameter-control operations, observer lifecycle, main-thread deferral, and safe local collectors that batch/throttle output away from audio-sensitive execution.
- **AbletonMCP:** treat the installed schema as the capability contract. Begin with connection/session inspection, then use narrow categories: introspection, browser discovery/loading, MIDI track/clip construction, Session audition/transport, and Arrangement duplication/navigation. Require Live-side readiness and post-call reads; refuse unsupported Live 12-only wrappers.

## Evidence priority for research agents

1. Runtime evidence from the user's exact Live 11 build: version/edition, MCP schema, `get_session_info`, browser discovery, and read-back after a change.
2. Ableton Live 11 manual, Live 11 release notes, and Ableton Help articles.
3. Cycling '74 **Max 8** documentation and a LOM reference explicitly matching the applicable Live 11 release.
4. Source code/version tag of the installed AbletonMCP fork and Remote Script.
5. Reproducible inspection of copied `.als` fixtures, with parser/version recorded.
6. Community reverse engineering only for undocumented file-format details; label it non-contractual and corroborate it. Never promote search snippets, a different MCP fork, or Live 12 docs over exact-version evidence.

Primary references: [Live 11 concepts](https://www.ableton.com/en/live-manual/11/live-concepts/), [Live 11 devices](https://www.ableton.com/en/live-manual/11/working-with-instruments-and-effects/), [Live 11 Max for Live](https://www.ableton.com/en/live-manual/11/max-for-live/), [Live-specific file types](https://help.ableton.com/hc/en-us/articles/209769625-Live-specific-file-types), [Remote Scripts](https://help.ableton.com/hc/en-us/articles/209072009-Installing-third-party-remote-scripts), [controlling Live with M4L](https://help.ableton.com/hc/en-us/articles/5402681764242-Controlling-Live-using-Max-for-Live), and [Max 8 Live API overview](https://docs.cycling74.com/legacy/max8/vignettes/live_api_overview).

## Recommendations for Gemini prompt + Cursor skill authors

- Add a hard opening gate: “Target Ableton Live 11; collect exact 11.x.y + edition; never silently substitute Live 12 documentation or APIs.”
- Encode three modes with explicit boundaries: **offline research/read-only Set analysis**, **live inspection**, and **live mutation**. Do not let a research request drift into controlling Live.
- Require claim labels: `OFFICIAL-L11`, `RUNTIME-VERIFIED`, `BRIDGE-SOURCE`, or `COMMUNITY/UNDOCUMENTED`.
- Add an anti-hallucination rule: only call methods/tools present in the exact runtime schema or exact-version official LOM; quote the discovered signature before generating code.
- Add a Live 12 denylist and specifically gate `create_audio_clip`; offer Live 11-safe alternatives such as user import, browser loading where supported, or creating MIDI clips and duplicating them to Arrangement.
- Make local-first mean localhost binding, user-approved roots, metadata-first indexing, no cloud upload by default, secret/path redaction, and no background crawling outside selected folders.
- For `.als`, default to read-only copies, record Set version, impose gzip/XML safety limits, preserve unknown nodes, and never promise round-trip writing without disposable-copy validation in Live 11.
- For live actions, require inspect → plan → user confirmation when destructive/audible → execute one bounded step → read back → stop on mismatch. Do not auto-start playback or load devices merely to “verify” research.
- For M4L collectors, throttle observers, release observers on teardown, batch disk/socket writes, avoid synchronous I/O in Live callbacks, and use `live.remote~` only for its documented real-time parameter-control role.
- Prefer tool-category workflows over a static exhaustive list, because AbletonMCP forks and installed versions differ. Capability discovery must override prompt assumptions.
