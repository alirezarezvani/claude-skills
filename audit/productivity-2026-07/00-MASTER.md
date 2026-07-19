# Master report — Productivity domain audit + coverage expansion

**Audited:** 2026-07-17 · **Branch:** `claude/productivity-skills-audit-obucop` ·
**Scope:** the full `productivity/` domain — 6 plugins / 7 skills at audit time (capture,
inbox-setup, inbox-triage, reflect, handoff, andreessen, roast; `fable-goal` landed on
`dev` mid-audit and is noted in the coverage map) — audited on quality (Matt Pocock
6-item review checklist), scripts smoke-tested, agentic signals read from the
`engineering/agent-harness` productivity manifest, and the domain's *coverage* mapped
against the personal-productivity canon to find the missing lanes.

**Method:** (1) goal formalized through the repo's own harness
(`goal_compiler.py` against `assets/harnesses/productivity.json` → `plan.v1`, 4 tasks);
(2) every SKILL.md run through `skill_review_checklist_runner.py`; (3) all 24 bundled
scripts smoke-tested (`--help`); (4) manifest `agentic_signals` reviewed per skill;
(5) coverage gap analysis against GTD / Deep Work / meeting-science canon;
(6) three parallel build agents shipped the missing plugins (this PR).

---

## 1. Existing-skill scorecard (7 skills, pre-PR)

| Skill | Checklist verdict | Failing rules | Scripts `--help` | Weakest agentic signals |
|---|---|---|---|---|
| andreessen | WARN | under-100-lines | 3/3 pass | close_out |
| capture | WARN | under-100-lines | 3/3 pass | verification, close_out |
| inbox-setup | FAIL | under-100-lines · no code-block examples | 3/3 pass | verification |
| inbox-triage | FAIL | under-100-lines · skill/tool terminology mix | 3/3 pass | verification, close_out |
| handoff | FAIL | under-100-lines · skill/tool terminology mix | 7/7 pass | goal_intake, loop_discipline |
| reflect | FAIL | under-100-lines · no code-block examples | 3/3 pass | refusal_gate, close_out |
| roast | FAIL | under-100-lines · skill/tool terminology mix | 3/3 pass | refusal_gate, verification, close_out |

Reading: the domain's execution layer is healthy — **all 24 scripts pass smoke tests**,
every plugin ships the full Path-B contract (agent + command + 3 scripts + 3
references). The findings are documentation-hygiene (the checklist is advisory for
legacy skills, binding for new ones per `quality_gates_for_skills.md`) and the
repo-wide AR5/AR6 pattern the engineering audit already named: **verification and
close-out are the weakest signals** (5/7 skills lack `close_out`, 4/7 lack
`verification`).

## 2. Coverage gap analysis

What the domain covered pre-PR, mapped to the personal-productivity stack:

| Lane | Canon | Covered by |
|---|---|---|
| Intake / capture | Allen (GTD capture) | `capture` |
| Email | — | `inbox-setup` + `inbox-triage` |
| Retrospection | bias literature | `reflect` (per-conversation) |
| Session continuity | Pocock | `handoff` |
| Decision pressure-test | Andreessen; red-teaming | `andreessen`, `roast` |
| Daily task pick | Andreessen 3x5 card | `andreessen` |
| Goal-prompt authoring | — | `fable-goal` (landed on `dev` mid-audit) |
| **Periodic review** | **Allen — "the critical success factor"** | **nothing** |
| **Time / attention management** | **Newport — Deep Work, time-blocking** | **nothing** |
| **Meeting hygiene** | **Rogelberg; Perlow (HBR)** | **nothing** |

The three empty lanes are the three largest bodies of personal-productivity canon not
represented anywhere in the repo (project-management covers *team* ceremonies and
delivery flow, not the individual's calendar; business-operations/internal-comms covers
*org* communication design, not one person's meeting load).

## 3. What this PR ships: 3 new plugins

Each follows the full Path-B contract (plugin.json + README + cs-* agent + /cs:*
command(s) + SKILL.md + 3 stdlib scripts with `--help`/`--sample` + 3 references citing
5–7 sources + assets), and each SKILL.md passes the 6-item checklist **PASS** — the
binding gate for post-v2.6.0 skills that the legacy siblings predate.

1. **`weekly-review`** — the GTD weekly-review loop. `open_loop_scanner.py` (workspace
   scan: unchecked boxes, TODO/FIXME, stale files), `weekly_review_gate.py` (GET CLEAR /
   GET CURRENT / GET CREATIVE checklist; refuses COMPLETE while a GET CURRENT step is
   missing — exit 2), `commitment_auditor.py` (stalled / no-next-action /
   someday-candidate flags + 0–100 health score). Agent `cs-weekly-review`; command
   `/cs:weekly-review`.
2. **`deep-work`** — time-block planning + shallow-work budget. `time_block_planner.py`
   (deep blocks ≥90 min first, shallow batched, buffers; refuses >4h deep demand —
   exit 2), `shallow_work_auditor.py` (deep/shallow classification + budget verdict +
   the recent-graduate forcing question), `focus_session_logger.py` (JSON-state log:
   weekly deep hours vs target, streaks). Agent `cs-deep-work`; commands `/cs:deep-work`,
   `/cs:time-block`.
3. **`meetings`** — the meeting-cost gate + agenda + action discipline.
   `meeting_cost_calculator.py` (cost incl. optional refocus overhead; ASYNC / NOT-READY
   / MEET verdicts with exit codes), `agenda_builder.py` (refuses topics without a
   desired outcome; decision-first ordering; timebox overflow refusal),
   `action_item_extractor.py` (owner + due extraction; ORPHAN / NO-DUE flags). Agent
   `cs-meeting-discipline`; commands `/cs:meeting-prep`, `/cs:meeting-actions`.

## 4. Follow-ups for the legacy 7 (not this PR)

- F1 — add one fenced example block to `inbox-setup` and `reflect` SKILL.md (clears
  their checklist FAIL).
- F2 — terminology sweep (`tool` → `script`) in `inbox-triage`, `handoff`, `roast`
  SKILL.md.
- F3 — the AR5/AR6 sweep the engineering audit recommends repo-wide: one iteration-cap
  sentence + one close-out criterion per SKILL.md would lift most of the domain to
  LOOP-CAPABLE.

## 5. Verification record for this PR

- Checklist runner → PASS on all 3 new skills (binding gate).
- All 9 new scripts exit 0 on `--help` and `--sample`; refusal paths exercised
  (documented non-zero exits).
- `scripts/check_plugin_json.py --all` clean after marketplace registration.
- Productivity harness manifest regenerated via `harness_manifest_builder.py`.
- Cross-platform installability re-verified by running the announced sync scripts
  (Codex, Gemini CLI, Vibe, Hermes, Codebuff) and confirming the 3 new skills are
  picked up.
