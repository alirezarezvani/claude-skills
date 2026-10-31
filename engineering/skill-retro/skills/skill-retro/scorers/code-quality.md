---
name: Code Quality
description: "Whether the code, tests, and comments the agent produced are well-designed and consistent with the target repo's conventions."
labels:
  - value: "approve"
    description: "The agent produced well-designed, correct code that is consistent with repo conventions, adequately tested, and clean of smells; a senior reviewer would approve it outright, with at most trivial nits."
    score: 1
  - value: "block"
    description: "The agent produced code with at least one defect a reviewer would insist on fixing before merge: a correctness or concurrency bug, a missed edge case, an inconsistent pattern, weak or missing tests, or mixed-in artifacts that do not belong."
    score: 0.2
  - value: "insufficient_evidence"
    description: "The transcript shows no code diff, or too little of one to judge."
    score: 0.5
---
**Rubric**

This scorer applies to conversations where the agent produced code changes. Evaluate the actual code artifact — the edits themselves, not the process used to produce them. Judge it the way a careful senior reviewer would review the same pull request, using the target repo's own established conventions as the standard. The verdict is binary: `approve` means that reviewer would merge the change as-is, with at most trivial nits; if they would insist on a fix before merging — one real defect is enough — the verdict is `block`. If the condensed transcript doesn't show enough of the change to judge, the verdict is `insufficient_evidence` and the session is excluded from aggregation. The bullets below are common quality dimensions, not an exhaustive checklist — judge any other way the artifact falls short of what a careful senior engineer would ship.

Assess:

- **Design.** The shape of the change fits the codebase; it isn't premature abstraction, scope creep, or a change that belongs somewhere else (a library, a config value, a separate service).
- **Correctness.** The change does what it claims, including edge cases (nil/empty inputs, boundaries) and concurrency safety (races, unsafe shared state, spawned work that outlives request-scoped values).
- **Complexity.** No function, type, or expression is doing more than it needs to; no speculative genericity or indirection added for a need that doesn't exist yet.
- **Repo conventions.** Follows the same idioms as similar code in the same package or module — error handling, type placement, naming schemes, and any other established pattern visible in the surrounding code. An unexplained deviation from a clear local pattern is a defect even if the new code works.
- **Code smells.** Magic numbers or strings without a named constant, copy-paste that should be a shared function, commented-out code, vague or stale TODOs, workarounds that patch a symptom instead of the root cause, silently swallowed errors, deep nesting that early returns would flatten.
- **Tests.** Present for the change, and actually verify the behavior they claim to (a broken implementation would fail them) rather than asserting trivia or mocking away the logic under test; cover the error and edge paths, not just the happy path; not so tightly coupled to internals that unrelated changes would break them.
- **Naming.** Every new identifier communicates what it represents, at a length that's unambiguous without being noisy.
- **Comments.** Explain why, not what; a doc comment on an exported symbol describes its purpose and constraints without narrating its implementation; no comment describes an edit, a refactor, or a prior state of the code rather than its current behavior.
- **Diff hygiene.** The change contains only the edits that are intended to be committed — no temporary or transient text, scratch scripts, debug prints, or other verification scaffolding left alongside it.
- **Documentation.** READMEs, guides, or API docs are updated in the same change when the change affects how the software is built, tested, or used.
- **Corrections.** A defect the user pointed out mid-conversation counts against the artifact regardless of whether it was ultimately fixed; needing an external correction at all is a negative signal, not just a defect left unresolved.

Out of scope: how directly the agent worked (scored under Efficiency), and whether it followed instructions or skills. Judge the artifact on its own merits.

**Reason**

One to three sentences citing the specific file, pattern, or defect that drove the grade — quote or closely paraphrase the line or convention at issue. Name what would have caught it: a lint rule, a repo convention the agent should have searched for, a test case, or a skill. For `insufficient_evidence`, say what you couldn't see — for example, no diff was produced, or the diff wasn't in the transcript.
