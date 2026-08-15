# Ableton Cursor Skill — create-skill Compliance Report

**Evaluated:** 2026-08-14  
**Target skill:** `ableton-research-agent-CURSOR-SKILL.md`  
**Resolved path:** `C:\claude-skills\.gemini\MD research\cursor edit\ableton-research-agent-CURSOR-SKILL.md`  
*(User-specified path `...\MD research\ableton-research-agent-CURSOR-SKILL.md` not found; file lives under `cursor edit\`.)*  
**Reference:** `C:\Users\RoG\.cursor\skills-cursor\create-skill\SKILL.md`  
**Secondary reference:** `skill-tester` (claude-skills repo meta-skill — applied only where relevant to Cursor personal skills)  
**Proposed install path:** `~/.cursor/skills/ableton-live11-research-automation/SKILL.md`

---

## Executive summary

| Metric | Result |
|--------|--------|
| **Overall grade** | **B+** |
| **Line count** | 210 / 500 max |
| **Install-ready** | Yes (with minor packaging notes) |
| **Agent usability** | Strong — clear gates, path routing, verification discipline |
| **Critical blockers (P0)** | 0 |

The skill is well above minimum Cursor create-skill quality. Frontmatter, scope boundaries, workflow, and anti-patterns are solid. Main gaps: no concrete worked example, no progressive-disclosure split for MCP/LOM reference material, and a hardcoded MCP tool table that can drift from live schemas.

---

## 1. YAML frontmatter

| Criterion | Pass/Fail | Evidence |
|-----------|-----------|----------|
| `name` present | **PASS** | `name: ableton-live11-research-automation` |
| `name` ≤ 64 chars | **PASS** | 33 characters |
| `name` charset (lowercase, hyphens, numbers) | **PASS** | No uppercase, underscores, or spaces |
| `description` non-empty | **PASS** | 4-line block under `description: >-` |
| `description` ≤ 1024 chars | **PASS** | ~348 characters (estimated) |
| **WHAT** (capabilities) | **PASS** | *"Researches and designs local-first Ableton Live 11 automation: stock devices, Max for Live, AbletonMCP, MIDI Remote Scripts, LOM, and .als (gzipped XML) analysis."* |
| **WHEN** (triggers) | **PASS** | *"Use when the user asks about Ableton Live 11, Live Set parsing, M4L, MIDI Remote Scripts, Ableton MCP, Session/Arrangement automation, or stock Live devices."* |
| Third-person voice | **PASS** | *"Researches and designs"* — not "I can help" |
| Trigger term density | **PASS** | `.als`, M4L, LOM, MCP, Session/Arrangement, stock devices |
| `disable-model-invocation` | **PASS** (implicit) | Field omitted → appropriate for auto-discovery when user mentions Ableton (create-skill: omit only when ambient auto-invoke is desired) |

**Frontmatter snippet:**

```yaml
---
name: ableton-live11-research-automation
description: >-
  Researches and designs local-first Ableton Live 11 automation: stock devices,
  Max for Live, AbletonMCP, MIDI Remote Scripts, LOM, and .als (gzipped XML)
  analysis. Use when the user asks about Ableton Live 11, Live Set parsing, M4L,
  MIDI Remote Scripts, Ableton MCP, Session/Arrangement automation, or stock
  Live devices.
---
```

---

## 2. Structure & authoring principles

| Criterion | Pass/Fail | Evidence |
|-----------|-----------|----------|
| Clear **when to use** | **PASS** | § "When to use" (6 bullet scenarios, L15–22) |
| Clear **when not to use** | **PASS** | § "When not to use" — Live 12-first, REAPER, generic DAW, cloud-default (L24–29) |
| Step-by-step **workflow** | **PASS** | Checklist L56–63 + Steps 1–6 (L65–125) |
| **Progressive disclosure** | **PARTIAL** | Single 210-line file; no `reference.md` / `examples.md`. Acceptable today; will strain if MCP/LOM tables grow |
| **Token efficiency** | **PASS** | Assumes agent competence; tables over prose; one minimal Python snippet |
| **Under 500 lines** | **PASS** | 210 lines |
| **Degrees of freedom** | **PASS** | Hard rules (L31–38) + path-selection matrix (L40–50) = medium freedom; deliverable template (L166–191) = medium-low for outputs |
| Consistent terminology | **PASS** | OFFLINE / LIVE / HYBRID used throughout; LOM vs MCP vs M4L not conflated |
| No Windows-style paths | **PASS** | Uses forward slashes and generic paths (`Backup/`, `Samples/`) |
| No vague skill name | **PASS** | Specific domain + version scope |
| File references one level deep | **PASS** | No broken internal links; external docs only |
| Time-sensitive info handled well | **PASS** | Live 11 vs 12 gated explicitly (*"create_audio_clip is Live 12.0.5+ only"*) — version gates, not calendar expiry |
| **Examples (concrete)** | **FAIL** | Deliverable *template* present (L166–191) but no worked input→output example |
| **Quick Start** section | **PARTIAL** | Title + version scope (L11–13) serve as orientation; no dedicated one-screen Quick Start per create-skill example |
| Feedback / verification loop | **PASS** | Step 3 Verify (L78–82), evidence priority (L203–209), anti-patterns (L193–201) |
| Conditional workflow | **PASS** | Path selection table routes OFFLINE vs LIVE MCP vs HYBRID (L40–50) |

---

## 3. Installability as `~/.cursor/skills/ableton-live11-research-automation/SKILL.md`

| Criterion | Pass/Fail | Evidence |
|-----------|-----------|----------|
| Directory name matches `name` field | **PASS** | `ableton-live11-research-automation/` ↔ frontmatter `name` |
| Valid SKILL.md-only layout | **PASS** | Instruction skill; no required scripts for Cursor install |
| Not in reserved `skills-cursor/` path | **PASS** | Target is `~/.cursor/skills/` (personal) |
| Self-contained (no missing local refs) | **PASS** | No `[reference.md](reference.md)` links to absent files |
| Environment assumptions documented | **PASS** | `user-AbletonMCP`, Live 11 running, local `.als` — explicit |
| Portable across projects | **PASS** | Personal skill scope; no repo-relative paths |

**Install steps (validated structurally, not executed):**

```text
mkdir -p ~/.cursor/skills/ableton-live11-research-automation
cp "cursor edit/ableton-research-agent-CURSOR-SKILL.md" \
   ~/.cursor/skills/ableton-live11-research-automation/SKILL.md
```

Optional follow-on (not required for install):

```text
ableton-live11-research-automation/
├── SKILL.md
├── reference-mcp-lom.md   # recommended split (see P2 fixes)
└── examples.md            # recommended (see P1 fixes)
```

---

## 4. Agent usability (practical invocation test)

Simulated agent scenarios against skill text:

| Scenario | Expected behavior per skill | Usability |
|----------|----------------------------|-----------|
| User: "Parse my `.als` for device usage" | Route OFFLINE; gzip→XML; read-only default | **Clear** — Path table + Step 2 + code snippet |
| User: "Fire clip 1 on track 2" (Live open) | LIVE MCP path; GetMcpTools first | **Clear** — L44, L129, hard rule #4 |
| User: "Use create_audio_clip on Live 11" | Refuse / version gate | **Clear** — L26, L139, anti-pattern L197 |
| User: "REAPER RPP automation" | Decline; redirect | **Clear** — L27 |
| User: "What's the LOM path for parameters?" | Cite docs; no invention | **Clear** — L159–164, evidence priority |
| User: vague "help with my DAW" | When-not-to-use should trigger ask/clarify | **Adequate** — could add explicit "ask one question" forcing |

**Strengths for agents:**

- Hard rules (#1–6) are actionable and testable
- Path-selection matrix removes guesswork between offline and live
- MCP discovery mandated before tool calls (*"Discover MCP tools before inventing control sequences"*, L50)
- Deliverable template standardizes output shape

**Weaknesses for agents:**

- No single end-to-end example tying workflow steps → deliverable
- MCP tool table (L127–139) may be treated as canonical over live `GetMcpTools` output
- RAG section (L110–114) mentions librosa/madmom but doesn't set default vs optional clearly enough

---

## 5. skill-tester cross-check (advisory)

`skill-tester` targets **claude-skills repo packages** (scripts/, references/, assets/). Most checks are **N/A** for a Cursor personal instruction skill.

| skill-tester dimension | Applicability | Notes |
|------------------------|---------------|-------|
| Repo directory layout | N/A | Cursor skills don't require scripts/ or references/ |
| Python script testing | N/A | One inline snippet only; not a bundled script |
| Tier line counts (100–300 lines) | N/A | create-skill caps at 500; this skill at 210 is ideal |
| Documentation depth | **PASS** | Would score well on usability/documentation if ported |
| Security (no secret exfil) | **PASS** | Privacy hard rule #1, local-first RAG |

---

## 6. Scoring summary

| Category | Score | Weight | Weighted |
|----------|-------|--------|----------|
| Frontmatter & discovery | 95% | 25% | 23.75 |
| Structure & workflow | 88% | 30% | 26.40 |
| Token efficiency & disclosure | 82% | 20% | 16.40 |
| Installability | 95% | 15% | 14.25 |
| Agent usability | 85% | 10% | 8.50 |
| **Total** | | | **89.3 → B+** |

Letter grade mapping: A (90+), B (80–89), C (70–79), D (60–69), F (&lt;60).

---

## 7. Fix recommendations

### P0 — Blockers (must fix before publish)

*None.*

### P1 — High priority (materially improves agent outcomes)

| # | Fix | Rationale |
|---|-----|-----------|
| 1 | **Add one worked example** under `## Examples`: user request → scope choice → key findings table → minimal template snippet. | create-skill Examples pattern; closes the only structural FAIL. |
| 2 | **Add `## Quick Start`** (3–5 bullets) immediately after the title block: confirm Live 11 → pick OFFLINE/LIVE/HYBRID → verify MCP/LOM → ship deliverable. | Faster orientation than reading full workflow on first invoke. |
| 3 | **Demote MCP tool table to illustrative** — prepend: *"Illustrative only; always prefer live output from `GetMcpTools` on `user-AbletonMCP`."* | Prevents stale tool names from overriding live schemas. |

### P2 — Nice to have (maintainability & polish)

| # | Fix | Rationale |
|---|-----|-----------|
| 4 | Split LOM paths + MCP categories into `reference-mcp-lom.md`; link from SKILL.md. | Progressive disclosure before file grows past ~300 lines. |
| 5 | Add `examples.md` with a second scenario (HYBRID habit mining). | Supports complex path without bloating SKILL.md. |
| 6 | Clarify RAG defaults: stdlib/index-only baseline; librosa/madmom explicitly optional. | Reduces agent over-engineering on first RAG task. |
| 7 | Add forcing question when scope ambiguous: *"Is Live 11 open with MCP, or offline `.als` only?"* | Matches create-skill conditional workflow pattern. |
| 8 | Move source file to stable path or document `cursor edit/` as canonical during draft. | Avoids install/copy confusion (this review hit path mismatch). |

---

## 8. create-skill checklist (final)

### Core quality

- [x] Description specific with key terms
- [x] Description includes WHAT and WHEN
- [x] Third person
- [x] Under 500 lines (210)
- [x] Consistent terminology
- [ ] Concrete examples (template only — **gap**)

### Structure

- [x] Workflows have clear steps
- [x] No bad time-sensitive patterns
- [~] Progressive disclosure (acceptable now; split recommended later)
- [x] No Windows-style paths

### Install

- [x] Name matches directory
- [x] Self-contained SKILL.md
- [x] Suitable for `~/.cursor/skills/ableton-live11-research-automation/SKILL.md`

---

## 9. Verdict

**Grade: B+** — Production-ready for personal install with P1 polish recommended before treating as a reference-quality Cursor skill.

**Top 5 issues (no critical blockers):**

1. **No concrete worked example** — only a deliverable template (P1)
2. **Hardcoded MCP tool table** may override live `GetMcpTools` discovery (P1)
3. **Missing Quick Start** section for first-invoke orientation (P1)
4. **No progressive-disclosure files** for growing MCP/LOM reference (P2)
5. **Source path ambiguity** — skill file under `cursor edit/` vs expected parent path (P2)

---

*Report generated by create-skill compliance review. Re-run after P1 fixes to target A (90+).*
