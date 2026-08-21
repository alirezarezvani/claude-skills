# Review-loop discipline: waiting, capping, escalating

An agent that asks for human review has to decide three things it usually gets wrong:
**how to wait, when to stop, and what "done" means.** This document is the reasoning
behind the answers baked into `human_gate.py`.

---

## 1. Never block a turn on a human

The tempting design is a blocking poll: the agent opens a review, calls
`poll --timeout 600`, and holds its turn until the human clicks Send.

`petergyang/human-review` does exactly this, and instructs the agent accordingly:

> Keep this command in the foreground. Do not end your turn while it is waiting. […]
> If it prints `{"status":"timeout"}`, no feedback has arrived yet — run the same poll
> command again to keep waiting.

For a developer sitting in front of their own terminal with the browser already open,
this is a genuinely nice experience — the loop feels continuous. It is also the single
most dangerous instruction to generalise, for four reasons:

1. **Human review latency is unbounded.** Minutes if they are at the desk; days if the
   reviewer is a compliance officer. No timeout is right for both.
2. **There is no headless guard.** On CI, over SSH, or in a remote agent session, there
   is no browser and no human. The re-poll instruction has no terminating condition —
   it loops until something external kills it.
3. **It burns context.** Each poll round-trip consumes tokens producing nothing.
4. **It inverts the cost model.** The agent is the cheap, restartable participant; the
   human is the scarce one. Making the cheap participant wait *for* the scarce one, in
   a way that consumes resources while idle, is backwards.

**The rule here: `status` never blocks; the agent opens a round, hands over the path,
and ends its turn.** State lives on disk in `.human-gate/`, so nothing is lost between
turns. The human's Send is not an event the agent must catch — it is a file that will be
there when the agent next looks.

This is the same conclusion the repository's own agentic-readiness audit reached
independently: `audit/engineering-agentic-2026-07/` names **AR5 (loop discipline)** as
the repo-wide weakness, with iteration caps and named terminal states as the fix.

---

## 2. Cap the rounds, and make exhaustion mean something

An uncapped review loop has no failure state, which sounds safe and is not. Two
pathologies:

- **Infinite polish.** Each round surfaces new NITs because reviewers reliably find
  *something*. Without a cap, "one more round" is always locally reasonable and the
  artifact never ships. Wiegers documents this directly in *Peer Reviews in Software*.
- **Silent divergence.** Rounds 3, 4, 5 contest the same point in different words. The
  loop is no longer converging; it is a disagreement wearing a process costume.

`--max-rounds` (default 5) bounds it, and exhaustion exits **5 = ESCALATE** with an
explicit instruction: stop iterating, summarise what is still contested, hand it to a
human. It does **not** exit 0.

This distinction matters more than the number. Anthropic's guidance on long-running
agents makes the general point: an agent that exhausts its budget must **escalate**, not
degrade into a pass. A budget silently treated as success is worse than no budget, because
it converts a known limit into an unnoticed one.

The convergence signal worth watching: **two consecutive rounds producing only NITs
means the artifact is done.** Say so, rather than fishing for a third.

---

## 3. Refuse to close — the verifier's discipline

The core anti-pattern is **verification theater**: an agent that reports success by
narrating success. The defence is that the thing which *decides* done must be different
from the thing which *does* the work.

`engineering/agent-harness`'s `loop_controller.py` implements this for machine checks —
it runs verification commands itself via subprocess rather than trusting an agent's
claim that they passed. `human_gate.py` applies the identical principle to the human
lane: the gate reads recorded state on disk, not the agent's assertion.

The refusals, and the specific lie each one prevents:

| Rule | Prevents the claim… |
|---|---|
| G1 no round collected | "I had it reviewed" — when no review exists |
| G2 blocking items open | "I addressed the feedback" — when the blocker is untouched |
| G3 no named reviewer | "The team signed off" — when no person did |
| G4 sidecar changed post-collect | "That's the latest review" — when it is not |
| G5 cap exhausted | "We converged" — when the loop just ran out |
| G6 undocumented waiver | "It was fine to skip" — with no record of who decided |

**G4 deserves its own note.** It catches a genuinely subtle case: the reviewer adds a
late blocker to the sidecar *after* the agent collected round N. Without a content hash
comparison, the gate would close against a stale snapshot and the new blocker would
vanish. `fingerprint()` hashes contents rather than trusting mtime, so a re-save with no
changes does not spuriously reopen the gate.

---

## 4. Waivers must be explicit, never inferred

A gate with no override gets bypassed — someone comments out the check, or stops running
it. Nygard's *Release It!* makes this point about circuit breakers generally: a safety
mechanism with no legitimate manual override will be disabled illegitimately.

So `--waive "<reason>"` exists. Its discipline:

- The reason is **required** — there is no bare `--force`.
- The reason and **every refusal it overrode** are written into gate state, so the
  waiver is auditable after the fact.
- The waiver is per-artifact, not global. It does not lower the bar for anything else.

A recorded "we shipped this unreviewed because the reviewer was on leave and the CTO
accepted the risk" is a legitimate engineering decision. An unrecorded one is an
incident waiting to be reconstructed from memory.

---

## 5. Match gate strength to reversibility

Holding every artifact to the same bar trains people to route around the gate. Scale it:

| Situation | Posture |
|---|---|
| Internal draft, a branch, notes | Open a round if asked. NITs do not block. |
| Spec, plan, RFC others will build from | Hold G2 strictly. Named reviewer required. |
| External, irreversible, regulated | Require an explicit **APPROVE** item — absence of blockers is not consent. |

The last row is the one agents get wrong most often. "No blockers were raised" and
"a person approved this" are different states, which is why `APPROVE` is a distinct kind
in the schema and why `batch.approved` is only true when an APPROVE exists *and* no
blocking item is open.

---

## 6. What good looks like

A healthy loop, end to end:

```
open      → round 1, page built, path handed over, TURN ENDS
          … human reviews on their own schedule …
status    → exit 3, feedback waiting
collect   → 1 BLOCKER, 2 NIT, 1 EDIT. Apply all. EDIT verbatim.
open      → round 2, TURN ENDS
collect   → APPROVE, 0 blocking
close     → GATE PASSED (reviewer: reza, rounds: 2)
```

Two rounds, no blocking waits, a named human, an auditable record. The agent never once
had to decide whether its own work was good enough — which is the entire point.

---

## Sources

1. Anthropic. *Building Effective Agents* — checkpointing, budgets and escalation in
   agent loop design. https://www.anthropic.com/engineering/building-effective-agents
2. Yang, J. et al. *SWE-agent: Agent-Computer Interfaces Enable Automated Software
   Engineering.* NeurIPS, 2024.
3. Wiegers, K. *Peer Reviews in Software: A Practical Guide*, ch. on review scope and
   the diminishing returns of extra rounds. Addison-Wesley, 2001.
4. Nygard, M. *Release It! Design and Deploy Production-Ready Software*, 2nd ed.
   (circuit breakers, manual overrides). Pragmatic Bookshelf, 2018.
5. Bainbridge, L. *Ironies of Automation.* Automatica 19(6), 1983.
6. Yang, P. *human-review* SKILL.md — the blocking-poll contract this design
   deliberately inverts. https://github.com/petergyang/human-review
7. This repository. `audit/engineering-agentic-2026-07/` — AR5 loop-discipline finding.
8. This repository. `engineering/agent-harness/skills/agent-harness/scripts/loop_controller.py`
   — machine-verification counterpart to this gate.
