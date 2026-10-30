# UI finish sign-off

Fill this in from the script runs before a screen is called done. Paste
verdict lines, not summaries. A BLOCKED line means the screen is not done.

**Screen / flow:**
**Build or commit:**
**URL and viewports captured:** 320 × ___ and ___ × ___
**Brief or design file:**
**Reviewer (a person, not the agent):**

## 1. Finish lint (`finish_lint.py`)

- Verdict line:
- Blockers fixed:
- Suppressions added, each with its reason:
- Template traits and generic risk:
- If generic risk is MEDIUM or HIGH, does the brief ask for this look? (yes, quote it / no, and what was changed)

## 2. State matrix (`state_matrix_checker.py`)

- Verdict line and coverage %:
- States marked NA and why:
- Product-specific states added with `--require`:

## 3. Rendered audit (`rendered_audit.py`), once per viewport and per key state

| Snapshot | Viewport | State | Verdict | Blockers | Waivers |
|---|---|---|---|---|---|
| | 320 | populated | | | |
| | desktop | populated | | | |
| | 320 | empty | | | |
| | desktop | error | | | |

- Focus data came from a real keyboard pass (`capture_snapshot.mjs`): yes / no
- CONTRAST_UNVERIFIED items checked by hand, with the lowest ratio found:

## 4. Not covered by the scripts (check by hand)

- [ ] Screen reader pass on the main flow (labels make sense, errors are announced)
- [ ] Copy read aloud once: every button says what happens, every error says what to do
- [ ] Real data: longest real name, largest real list, slowest real network
- [ ] Source accessibility scan with `a11y-audit` (alt text, labels, ARIA, headings)

## Decision

- [ ] Ship: no blockers, every waiver has a WCAG exception or a ticket
- [ ] Ship with follow-ups (list ticket ids):
- [ ] Not done: blockers remain

Signed: ______________________  Date: ____________
