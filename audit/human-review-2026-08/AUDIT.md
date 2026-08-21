# Audit — `petergyang/human-review`

**Upstream:** https://github.com/petergyang/human-review
**Version audited:** npm `human-review@0.6.0` (clone at audit time, `main`)
**License:** MIT © 2026 Peter Yang
**Auditor:** claude-skills maintainers · **Date:** 2026-08-09
**Purpose:** decide whether/how to bring this capability into the claude-skills ecosystem.

---

## 0. Bottom line

🔴 **Do not vendor verbatim.** 🟢 **Do adopt the idea.**

The upstream is a well-engineered, genuinely careful piece of software — 90/90 tests pass,
and its security model is better than most local-server tools (DNS-rebinding defense,
constant-time token compare, realpath-checked traversal guard, deliberately inert Markdown
renderer). The problem is not quality. It is **fit**: it is a 5,164-LOC Node application with
an npm runtime dependency, and this repository's stated hard rule is stdlib-Python-only,
no build systems, no dependencies. Vendoring it would make it the first Node runtime *and*
the first npm dependency in the tree.

The transferable asset is the **pattern**, not the package: *human feedback as a batched,
structured, machine-parseable artifact — and an agent loop that blocks on it.*

---

## 1. Identity — it is not a "humanizer"

Worth stating plainly, because the name invites the confusion:

`human-review` is a **human-in-the-loop visual review harness**. It opens an HTML/Markdown
file or a localhost page in the browser, lets a person edit text directly and leave anchored
comments, and ships the whole batch back to the agent as JSON.

It is **not** an AI-slop remover. This repo already has two of those, and neither overlaps:

| Existing skill | What it does | Overlap with human-review |
|---|---|---|
| `engineering/behuman` | Self-mirror loop so the *model* writes less robotically | None |
| `marketing-skill/skills/content-humanizer` | Rewrites AI-sounding copy into brand voice | None |

Correct neighbourhood for this capability is the **agent-loop / review-gate** family:
`engineering/agent-harness`, `markdown-html/md-review`, `engineering/grill-me`.

---

## 2. What it actually is

- npm package, `type: module`, Node ≥ 20. One runtime dependency (`marked@^18.0.7`), one dev
  dependency (`jsdom`). Two GitHub Actions workflows (test, publish).
- 5,164 LOC across 19 files in `src/`. Largest: `sdk.js` (1,464), `server.js` (926),
  `chrome-client.js` (836), `chrome.css` (456).
- Four CLI verbs: open (default), `poll`, `status`, `setup`.
- Architecture: CLI → spawns a **detached local HTTP server** on 127.0.0.1 → opens the browser
  at `/s/<session>` → server serves the reviewed artifact in a sandboxed iframe with an
  injected editing SDK → user edits/comments → **Send** → agent's blocking `poll` returns a
  JSON batch → agent applies to source → `poll --ack` clears and waits again.

### The loop, as SKILL.md teaches it
1. Agent writes/updates the file.
2. `npx -y human-review path/to/file.html`
3. `npx -y human-review poll path/to/file.html --timeout 600` — **blocks**; agent is told not
   to end its turn.
4. Apply the batch; `poll --ack --timeout 600`; repeat until the user says stop.

---

## 3. Verification performed

| Check | Result |
|---|---|
| `npm ci` | clean |
| `npm test` (`node --test`) | 🟢 **90/90 pass**, 0 fail, 4.14 s |
| Source read of auth/traversal/render paths | see §4 |

Test suite includes dedicated `security.test.js`, `feedback-safety.test.js`,
`frame-policy.test.js`, and a case named *"resolveAsset refuses a symlink that points outside
the directory."* Claims in the README are backed by tests, not just prose.

---

## 4. Security audit

### 4.1 Controls that are genuinely good (verified in source)

| # | Control | Evidence |
|---|---|---|
| S1 | Binds loopback only | `server.listen(port, "127.0.0.1")` — `server.js:914` |
| S2 | DNS-rebinding defense — `Host` must be `127.0.0.1:<port>` or `localhost:<port>`, else refused | `server.js:448-450` |
| S3 | Per-run 128-bit token on every `/api/*` route; **header-only** (deliberately not a query param, so it cannot leak into logs or shell history); constant-time compare with length pre-check | `server.js:106`, `461-466` |
| S4 | State dir `~/.human-review` created `mode 0o700` | `paths.js` `ensureStateDir()` |
| S5 | Path traversal blocked by **both** lexical containment and `realpathSync` containment — a symlink cannot escape the reviewed file's directory | `state.js:277-306` |
| S6 | URL targets restricted to `localhost` / `127.0.0.1` / `[::1]`; embedded credentials rejected | `paths.js` `localUrl()` |
| S7 | Iframe sandbox: file/Markdown reviews get an **opaque origin** (no `allow-same-origin`), so a reviewed file cannot read sibling files through the artifact route; only real localhost apps keep their origin | `frame-policy.js` |
| S8 | Markdown renderer is **deliberately inert** — raw HTML inside Markdown is escaped to text; link/image hrefs are scheme-allowlisted (`http`/`https`/`mailto`; `data:image/*;base64` for images only) | `markdown.js` |
| S9 | 24 MB body cap; pasted-image filenames are **generated**, never user-supplied; upload MIME allowlisted to png/jpeg/gif/webp | `server.js:36`, `660-688` |
| S10 | Detached server **self-terminates after 45 min idle** | `server.js:39`, `892` |

This is a more disciplined threat model than the average "it's just localhost" tool.

### 4.2 Findings

| # | Sev | Finding |
|---|---|---|
| **F1** | 🔴 **HIGH** | **Unpinned remote code execution by design.** SKILL.md instructs the agent to run `npx -y human-review …` on *every* invocation. `-y` auto-approves the install and the spec is unpinned, so each run may resolve and execute a **newly published** version of the package. The user never approves that upgrade. For a library whose hard rule is zero-dependency, this is the blocking issue. *Mitigation for any adoption: pin an exact version, vendor the code, or require a preinstalled binary and refuse to auto-fetch.* |
| **F2** | 🟠 **MED** | **Unbounded agent poll loop; no headless guard.** SKILL.md says "Do not end your turn while it is waiting" and, on `{"status":"timeout"}`, "run the same poll command again to keep waiting." There is no environment check and no maximum retry count. On a headless/CI/remote agent — no browser, no human at the keyboard — this becomes an indefinite loop burning wall-clock and context. This is precisely the **AR5 loop-discipline gap** this repo's own `audit/engineering-agentic-2026-07/` named as its repo-wide weakness. |
| **F3** | 🟠 **MED** | **Not every route is token-gated.** Only `/api/*` requires the token (`server.js:461`). `/artifact/<key>` and `/s/<id>` do not. Any other local process — or a browser page that learns the port and the 16-hex page key — can read the reviewed file's rendered content and its sibling assets. Keys are 64-bit and the `Host` check (S2) blocks the remote-rebinding path, so this is a local-trust-model gap rather than a remote hole, but it should not be silent. |
| **F4** | 🟠 **MED** | **`setup --global` mutates three global agent configs.** It writes `SKILL.md` into `~/.claude/skills/`, `~/.codex/skills/`, and `~/.agents/skills/`, and appends a block to the project's `AGENTS.md`. Installing a skill by asking an agent to run a CLI that rewrites user-global config is a larger footprint than the README's one-line install implies. (Note: this repo `.gitignore`s `AGENTS.md`, so such an append would be invisible to `git status` here.) |
| **F5** | 🟡 **LOW** | **Silent writes to the user's HTML.** README: *"For HTML files, direct edits and resizes save automatically."* Confirmed at the `action === "save"` route (`server.js:690+`). The reviewed file is overwritten with serialized browser HTML with no explicit confirmation step. Upstream correctly refuses this for Markdown and localhost targets, but for HTML it is a real, undeclared write path. |
| **F6** | 🟡 **LOW** | **One third-party parser in the trust path.** `marked` parses user Markdown. Well-maintained, and upstream mitigates hard via the inert renderer (S8), but it is still a dependency this repo currently has zero of. |
| **F7** | ⚪ **INFO** | **Lingering listener, self-limiting.** The server is spawned `detached` + `unref()`'d and outlives the CLI, with `{port, pid, token}` persisted in `~/.human-review/server.json`. There is no `stop`/`shutdown` verb in the CLI help. Mitigated by S10's 45-minute idle exit — noting it only because "no way to stop it" is the natural first read of the code. |

---

## 5. Convention fit with `claude-skills`

| Repo rule (CLAUDE.md) | Upstream | Fit |
|---|---|---|
| Python scripts, **standard library only** | Node 20, ESM, npm dep | ❌ |
| **No build systems or test frameworks** | `package.json`, `node --test`, 2 CI workflows | ❌ |
| Skill layout: `SKILL.md` + `scripts/` + `references/` + `assets/` | `src/*.js` + one `SKILL.md` | ❌ |
| No LLM calls in scripts | none | ✅ |
| Self-contained, no cross-skill dependencies | self-contained | ✅ |
| MIT + attributable upstream | MIT © Peter Yang | ✅ |
| `plugin.json` schema | absent (npm package, not a CC plugin) | ⚠️ must be authored |

**Why the vendoring precedent does not transfer.** `loop-library/` and
`engineering/skillopt-sleep/` were vendorable *because they were stdlib-Python-only with zero
third-party deps* — that is stated outright in skillopt-sleep's attribution note as the reason
the heavier `skillopt` training package was deliberately left behind. `human-review` fails the
same test that filtered `skillopt` out.

---

## 6. Gap analysis — what it would actually add

No skill in the tree does batched human-in-the-loop review. The nearest three all miss it:

- **`markdown-html/md-review`** — renders a code review *to* HTML. One-way. No feedback channel.
- **`engineering/grill-me`** — interrogates a plan through chat prose. No artifact surface.
- **`engineering/agent-harness`** — has a real loop controller (`loop_controller.py`) with
  `init/next/record/verify/close`, but AR4 verification is **machine-only**. There is no
  human-verification lane, and `close` cannot represent "a person looked at this and approved it."

That last one is the actual insertion point. The novel, portable idea is:

> **Structured human feedback as a first-class, machine-parseable verification artifact —
> not chat prose — with a loop that blocks on it and a gate that refuses to close without it.**

That idea is fully expressible in stdlib Python. The 5k LOC of contenteditable/anchoring/
block-drag machinery is what makes upstream *pleasant*; it is not what makes it *valuable*.

---

## 7. Recommendation

Adopt the pattern; do not adopt the package. Three viable shapes, in the build decision doc.

Whatever ships must carry, at minimum:

1. **No unpinned network execution** (fixes F1) — nothing auto-fetched at run time.
2. **A headless guard and a hard iteration cap** on any wait loop (fixes F2), with a named
   terminal state on exhaustion, matching `agent-harness` loop discipline.
3. **Token-gate every route**, not just `/api/*` (fixes F3), if a local server is used at all.
4. **No writes to user-global config** as an install side effect (fixes F4).
5. **No silent overwrite of a source file** — explicit confirm or write-to-copy (fixes F5).
6. **Attribution block** in `plugin.json` naming upstream, its author, and its MIT license,
   per the `caveman`/`grill-me`/`skillopt-sleep` precedent.

---

## 8. Attribution

Upstream is MIT-licensed. Any derived work in this repo must preserve
`Copyright (c) 2026 Peter Yang`, link the source repository, and state in `plugin.json`'s
`attribution` block what was taken (pattern vs. code) and what was changed. Nothing in this
audit's recommended path copies upstream source, so the derivation is *conceptual* — the
attribution should say exactly that rather than implying a code vendor.
