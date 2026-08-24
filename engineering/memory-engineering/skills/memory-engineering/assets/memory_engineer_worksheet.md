# Memory Engineer Worksheet — the seven forcing questions

Walk these **one at a time**, in order. Each has a recommended answer and a
citation. Do not batch them; the answer to one changes the framing of the next.

Fill this in before writing any memory code. If a question cannot be answered,
that is the finding — stop and go get the answer.

---

**System under review:** ________________________________________
**Date:** ____________  **Owner (a named human):** ____________________

---

## 1. What does one constructed record cost, and how many queries will it serve?

*Why it matters:* Construction energy exceeds total query energy across 300
queries for LLM-mediated memory. The invisible half of the bill is usually the
bigger half.

*Recommended answer:* Under roughly 10 queries per record, build **lazily on
second access** rather than eagerly at the end of every session.

*Citation:* Stanford rec. 4 — `memory_cost_canon.md` §6
*Check with:* `memory_cost_profiler.py`

**Your answer:**

```
cost per record: ______     queries per record: ______
decision: ____________________________________________
```

---

## 2. Which of build cost, query speed, and accuracy are you giving up?

*Why it matters:* No paradigm family wins all three. Refusing to name the
sacrifice does not avoid it — it just means it gets discovered in production.

*Recommended answer:* Name it explicitly and write it down here, so the next
person does not re-litigate it.

*Citation:* Stanford taxonomy — `memory_cost_canon.md` §3
*Check with:* `memory_architecture_picker.py`

**Your answer:**

```
family chosen: ________________________________________
cost accepted: ________________________________________
what would kill this choice: __________________________
```

---

## 3. Is this record a fact, a skill, or an event?

*Why it matters:* Agents do not need to replay what happened; they need the
facts and skills extracted from it. Storing events is what makes retrieval
drown.

*Recommended answer:* Keep facts and skills. Extract from events, then drop the
events.

*Citation:* PlugMem — `what_to_keep.md` §1
*Check with:* `memory_density_auditor.py`

**Your answer:**

```
current FACT/SKILL/LOG/PROSE split: ___________________
extraction happens at:  [ ] write time  [ ] read time  [ ] not at all
```

---

## 4. When two stored memories disagree, what happens?

*Why it matters:* Two memories that disagree may both have been true in
different contexts. Anything automatic destroys the evidence that a conflict
existed — and the conflict is usually the interesting part.

*Recommended answer:* Surface both versions with sources and timestamps to a
human. `newest_wins` and `auto_merge` are not policies, they are defaults
nobody chose.

*Citation:* `forgetting_policy_design.md` §3 — linter check **F4 (blocking)**

**Your answer:**

```
contradiction policy: _________________________________
who resolves it: ______________________________________
```

---

## 5. Who can write to this store, and can you delete one record without a migration?

*Why it matters:* A wrong memory does not fail once — it persists into every
future session that reads it. And anything that influences what the agent reads
can influence what it permanently believes.

*Recommended answer:* Separate read scope from write scope; shared stores
read-only. Keep a hard-delete path you can invoke without a migration.

*Citation:* Anthropic — `memory_control_and_governance.md` §3, §5
*Linter checks:* F5, F6, F7

**Your answer:**

```
read scope: ___________________________________________
write scope: __________________________________________
delete one record without a migration?  [ ] yes  [ ] no
untrusted-content ingestion holds write scope?  [ ] yes  [ ] no
```

---

## 6. What leaves the store, and on what rule?

*Why it matters:* None of the evaluated memory systems prunes or forgets by
default. If you did not build it, you do not have it — and retrofitting it onto
a full store is a migration nobody ever does.

*Recommended answer:* Choose now, while the store is small: a TTL, a capacity
bound **with a stated eviction order**, or relevance decay.

*Citation:* Stanford — `forgetting_policy_design.md` §1, §2 — linter check
**F1 (blocking)**

**Your answer:**

```
mechanism: [ ] TTL ____d  [ ] capacity ______  [ ] decay  [ ] NONE (blocked)
eviction order (if capacity): _________________________
```

---

## 7. Are you tracking footprint growth *slope*, or only current size?

*Why it matters:* At 1M tokens, footprint already varies up to 9× across
systems. Growth slope, not starting size, is what bankrupts a long-lived agent —
and agentic systems compound as the store itself grows.

*Recommended answer:* Track the slope and alert on it.

*Citation:* Stanford rec. 9 — `memory_cost_canon.md` §4 — linter check F8

**Your answer:**

```
slope tracked?  [ ] yes  [ ] no (baseline only)
alert threshold: ______________________________________
```

---

## Sign-off

- [ ] `memory_cost_profiler.py` run; cost per correct answer recorded
- [ ] `memory_architecture_picker.py` run; the accepted cost is named above
- [ ] `memory_density_auditor.py` run; FACT/SKILL/LOG/PROSE split recorded
- [ ] `forgetting_policy_linter.py` exits 0 or 2 — **never 4**
- [ ] Every scheduled pass was run by hand first and changed a decision

**Named owner:** ______________________  **Date:** ____________
