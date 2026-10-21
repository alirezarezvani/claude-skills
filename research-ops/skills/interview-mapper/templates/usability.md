# Lens: Usability / think-aloud (task performance observation)

**When:** a session where the user performs specific tasks in a product/interface out loud ("think aloud"), rather than narrating past experience. Difference from JTBD/CustDev: the unit is not motivation/problem but a SPECIFIC in-the-moment action at a specific interface step.
**Coding unit:** a pair "task step → observation" with a direct quote (spoken aloud) + what happened on screen, if captured in the transcript.
**Collection discipline:** record BEHAVIOR (where they clicked, where they stalled, what they re-read) separately from the user's verbalized interpretation — they may diverge.

## Layer 1 — operational (facts + quote + line)
- **U1 Task and expected path** — what task was given; what path was considered "correct" before the session.
- **U2 First action** — where the user went/clicked first (does it match the expected path).
- **U3 Stall points** — specific steps where the user stopped, re-read, clicked the wrong thing, asked "where is…".
- **U4 Verbalized model** — how the user explains out loud what they think will happen when they act (mental model).
- **U5 Errors and recovery** — what went wrong, whether they noticed it themselves, how they recovered from the error (or didn't).
- **U6 Successful completion** — whether they completed the task; with help/a hint or on their own; how many attempts.
- **U7 Spontaneous reactions** — emotional comments said aloud (irritation/relief/surprise) at the moment of action.

## Layer 2 — analytical (conclusion + quote; CAPS) — to council
- **A1 Problem type** — FINDABILITY (couldn't find the element) / CLARITY (found it, didn't understand it) / TRUST (understood it, not confident) / SYSTEM ERROR. For each stall point (U3).
- **A2 Barrier severity** — BLOCKING (didn't complete the task) / SLOWING (completed, but with difficulty) / COSMETIC. *(unstable)*
- **A3 Expectation-vs-interface gap** — where the mental model (U4) diverged from the system's actual behavior.
- **A4 Isolated case vs systemic problem** — specific to this user or looks like an architectural interface issue. *(unstable — requires data from ≥3 sessions)*
- **A5 Fix priority** — what to fix first (impact on task completion × frequency of stalling).
- **A6 Key insight** — 1 sentence: at step [X] the user [stalled/succeeded], because [mental model gap/interface issue], severity — [Y].

## Forcing questions (asked by the MODERATOR before/during the session, not the respondent)
What are you trying to do right now? What did you expect to see after that click? What's unclear here — say it out loud. If this hint weren't here, what would you do? Rate on a scale — how confident are you that you did it right?
