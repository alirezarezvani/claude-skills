---
name: Efficiency
description: "Whether the agent worked directly toward its result, or wasted effort on redundant steps, avoidable rework, or unnecessary back-and-forth."
labels:
  - value: "highly_efficient"
    description: "The agent took a direct path: nothing re-read or re-run, independent steps batched, no work redone."
    score: 1
  - value: "mostly_efficient"
    description: "The agent slipped once or twice: a duplicated read, an early retry, or a small correction — with no knock-on cost."
    score: 0.8
  - value: "mostly_inefficient"
    description: "The agent wasted effort repeatedly, or caused a round of rework an earlier check would have prevented."
    score: 0.4
  - value: "highly_inefficient"
    description: "The agent's waste dominated the run: the same defect reworked across cycles, repeated user correction, or extended flailing / looping."
    score: 0.2
---
**Rubric**

You are scoring one condensed transcript of a local coding-agent conversation. Evaluate the full cost of reaching the result: the steps the agent took, rework it caused, and human attention it consumed. Score against what a competent engineer with the same tools would have needed, not against what was achievable with only what the agent happened to have. A mistake that looks unavoidable in context still counts if better tooling, a skill, or a check would have prevented it — name that cause in the reason. The bullets below are common sources of waste, not an exhaustive checklist — judge any other way the run cost more than it should have.

Assess:

- **Rework from mistakes.** Work redone because the agent got it wrong the first time: a test or build failure a local check would have caught, edits to the wrong file, a misread requirement later reverted.
- **Cost to the human.** Repeated correction or steering from the user is the most expensive waste. A question asked up front is cheap; the same question asked after building the wrong thing is not.
- **Information gathering.** Re-reading, re-running, or re-searching for something already found; reading a large file end to end when a targeted search would answer it.
- **Routine-step overhead.** A roundabout way of doing something that's a standard, repeated part of this agent's job — more steps, more calls, or a broader operation than the step needs — when a more direct path was available. Weight this beyond its one-run cost: the same avoidable overhead recurs on every future conversation until a skill or rule fixes the pattern.
- **Batching.** Independent reads, searches, or workstreams run serially across turns instead of together.
- **Flailing.** Retrying a failing approach unchanged, or guessing when reading the code or docs would have settled it. An abandoned path only counts against the agent when the information to avoid it was already available.
- **Verification timing.** Checks run once, early enough to catch a defect before declaring done, not deferred until after or re-run redundantly.

**Reason**

One to three sentences naming the dominant source of waste with a rough count (three fix-test cycles, four redundant reads, two repeated user corrections), and the likely fixable cause — a missing or weak skill, an ambiguous instruction, a late check. When a skill exists that should have prevented the waste, name the skill.
