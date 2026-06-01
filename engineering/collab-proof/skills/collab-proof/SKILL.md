# collab-proof

Surfaces AI collaboration evidence the developer didn't consciously record.
Vela 3-layer pipeline × ADHD 4-frame reasoning — prompt-native, zero dependencies.

---

## Layer 01 — Signal detection

Run `git log --oneline -10` and `git diff --stat HEAD~3..HEAD` first.

Classify signal level using this rubric (pick the highest that matches):

**HIGH** → full artifacts (DECISIONS.md + session-history + WORKLOG + HTML)
- New file created, OR
- 4+ files modified, OR
- Explicit option comparison in conversation ("vs", "instead of", "chose X over Y"), OR
- Design discussion lasted 15+ exchanges, OR
- **Bug with root cause diagnosis** — conversation contains WHY the bug happened
  (not just "fixed X" but "the bug was caused by Y because Z")

**BUG_FIXING special rule** — override file count:
Even if only 1 file changed, classify as HIGH if the conversation contains:
- Root cause explanation ("the bug was...", "this happened because...", "the issue is...")
- Diagnosis process ("I checked...", "turned out...", "the problem was...")
- Fix rationale ("chose this approach because...", "instead of X, used Y because...")
File count doesn't matter for bugs — a well-diagnosed single-file fix is more valuable
than a 10-file feature with no discussion.

**MEDIUM** → WORKLOG only
- 1–3 files modified with no root cause discussion, OR
- Minor feature added, no tradeoffs discussed

**LOW** → silence, tell user "Routine session — nothing recorded."
- No code changes, only planning/discussion, OR
- Single trivial change with no context ("change this text", "fix typo", "rename variable")

Show the user: `Signal: HIGH / MEDIUM / LOW — [one-line reason]`

---

## Layer 02 — WorkIntentClassifier

Run all four frames simultaneously against conversation context + git diff.
Score each frame 0.0–1.0 using the rubric below. Then apply pruning and classification rules.

### Frame scoring rubric

**Frame A — Technical** (code churn complexity)
- `1.0` New module/file created, complex logic added (state machine, Lua script, novel algorithm)
- `0.5` Existing function logic modified, simple API endpoint added
- `0.1` Typo fix, comment change, plain text edit

**Frame B — Uncertainty** (developer doubt signals)
- `1.0` Code written then fully rolled back, explicit doubt expressed, `git revert`
- `0.5` Advice sought from Claude mid-implementation, 2+ revision requests on same area
- `0.0` Uninterrupted directive execution — developer knew exactly what to build

**Frame C — Fork** (decision branch presence)
- `1.0` Two or more alternatives explicitly compared in conversation (A vs B)
- `0.5` No explicit comparison but tradeoff mentioned (performance vs readability)
- `0.0` Single standard approach applied, no alternatives considered

**Frame D — AI contribution** (Claude's actual impact)
- `1.0` Claude identified a bug/edge case the developer hadn't noticed and proposed the fix
- `0.6` Claude generated structural boilerplate/skeleton that significantly accelerated execution
- `0.2` Claude reformatted or transcribed developer-directed code without independent contribution

---

### Pruning rule

Prune any frame scoring < 0.4.

**Exception — High-Speed Execution Guard:**
If `Frame A >= 0.8` AND `Frame D >= 0.6`, do NOT prune and do NOT silence the session,
even if Frame B = 0.0 and Frame C = 0.0.
Classify immediately as `FEATURE_BUILDING` with `HIGH` signal.

---

### Intent classification

| Surviving frames | Dominant intent |
|---|---|
| A high + D mid-high (B, C low) | `FEATURE_BUILDING` |
| B high + A/D high | `BUG_FIXING` or `STUCK` |
| C high + A high | `REFACTORING` or `EXPLORING` |
| All frames < 0.4 | `FLOW_STATE` or LOW |

### Internal output format (show to user before Layer 03)

```json
{
  "frames": {
    "technical": 0.0,
    "uncertainty": 0.0,
    "fork": 0.0,
    "ai_contribution": 0.0
  },
  "pruned": ["list of pruned frame names"],
  "intent": "FEATURE_BUILDING",
  "signal": "HIGH",
  "calibration_note": "one sentence explaining any exception rule applied"
}
```

---

## Layer 03 — Output

### If HIGH signal

**Append to `DECISIONS.md`** — one entry per real fork (Frame C must confirm alternatives existed):

```markdown
## [YYYY-MM-DD] <title>

**Context**: [Frame A — what forced this choice]
**Decision**: what was chosen
**Alternatives considered**: [Frame C — road not taken]
**Reasoning**: why — prefix "inferred:" if reconstructed from context
**AI contribution**:
  - Identified: [Frame D — something developer missed]
  - Suggested: [Frame D — approach or alternative]
  - Developer-driven: [what the developer decided independently]
**Intent class**: [from Layer 02]
**Signal score**: HIGH
**Outcome**: implemented | pending | reversed
```

If no real fork existed → write nothing. Never fabricate decisions.

**BUG_FIXING intent: use this format instead:**

```markdown
## [YYYY-MM-DD] <bug title>

**Root cause**: what actually caused the bug — the WHY, not just the what
**Symptom**: what the developer observed
**Fix**: what was changed
**Why this fix**: rationale — inferred if not stated explicitly
**Alternative fixes considered**: other approaches discussed (if any)
**AI contribution**:
  - Identified: [Frame D — did Claude spot the root cause?]
  - Suggested: [Frame D — fix approach or diagnostic step]
  - Developer-driven: [what the developer diagnosed/decided independently]
**Intent class**: BUG_FIXING
**Signal score**: HIGH
**Outcome**: fixed | workaround | deferred
```

**Create `session-history/YYYY-MM-DD-HHMM.md`**:

```markdown
# Session [YYYY-MM-DD HH:MM]

**Intent**: [class] (runner-up: [class if any])
**Signal**: HIGH
**Frames active**: A ([score]) / B ([score]) / C ([score]) / D ([score])

## What shipped
[grounded in git log]

## What was figured out
[Frame B + C — the reasoning, tradeoffs, debugging — what developers forget]

## Decisions made this session
[refs to DECISIONS.md entries]

## Where it got hard
[Frame B findings — uncertainty, reverts, EXPLORING/STUCK signals]

## AI contribution summary
[Frame D synthesis — one honest paragraph, calibrated]

## Next steps inferred
[what's obviously incomplete]
```

**Append to `WORKLOG.md`**:
```
YYYY-MM-DD HH:MM | [intent] | HIGH | <verb phrase> — <why it mattered>
```

**Generate `session-history/YYYY-MM-DD-HHMM-proof.html`** directly:

Write a self-contained HTML file. No CDN. No external resources. Must open at `file://`.

Required structure:
```
Header
  project name · date · intent badge (color-coded by class) · signal score bar (0–1 gradient)

Cognitive frames section
  4 cards: Frame A / B / C / D — each with score and one-line finding
  Pruned frames shown at reduced opacity

Decisions section
  One card per DECISIONS.md entry:
  Context | Decision | Alternatives | Reasoning
  AI contribution block: Identified (purple) / Suggested (amber) / Developer-driven (green)
  Outcome badge

Session narrative section
  What shipped · What was figured out · Where it got hard · Next steps

AI contribution summary
  Frame D synthesis paragraph

Footer
  Last git commit hash (run: git log --oneline -1)
  "Generated by collab-proof · [timestamp]"
```

Inline all CSS. Use dark background (#0d1117), card background (#161b22), border (#30363d).
Write the complete HTML to the file — do not ask the user for confirmation.

**Anchor proof to git** (run after HTML is written):
```bash
PROOF=$(ls -t session-history/*-proof.html 2>/dev/null | head -1)
if [ -n "$PROOF" ]; then
  HASH=$(python3 -c "import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$PROOF")
  git notes append -m "collab-proof sha256: $HASH file: $(basename $PROOF)" HEAD 2>/dev/null || \
  git notes add   -m "collab-proof sha256: $HASH file: $(basename $PROOF)" HEAD 2>/dev/null || true
fi
```

---

### If MEDIUM signal

Append one line to `WORKLOG.md` only:
```
YYYY-MM-DD HH:MM | [intent] | MEDIUM | <verb phrase>
```

---

### If LOW signal

Tell user: "Signal: LOW — Routine session, nothing recorded."

---

## Honesty rules

- Never invent decisions not in the conversation or implied by the diff
- "inferred:" prefix when reasoning is reconstructed
- Frame D must be calibrated — neither overclaim nor dismiss
- If all frames score < 0.4 → write nothing
