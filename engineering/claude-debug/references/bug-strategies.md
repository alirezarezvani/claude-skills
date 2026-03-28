# Bug-Type Strategies — Detailed Reference

Detailed techniques for each bug type, used during Phase 2 (ISOLATE).

## Crash / Panic

**Technique: Stack trace backward analysis**

1. Read the stack trace from bottom to top
2. Find the first frame that is YOUR code (skip library/framework frames)
3. Identify the value that caused the crash (the `None`, the bad index, the null ref)
4. Trace that value backward through assignments and function calls
5. The bug is where the bad value was PRODUCED, not where it was CONSUMED

**Example: Rust unwrap panic**

```
thread 'main' panicked at 'called `Option::unwrap()` on a `None` value'
  --> src/service.rs:45:18
```

- Frame: `service.rs:45` — `user.email.unwrap()`
- Bad value: `user.email` is `None`
- Trace backward: `user` comes from `repo.find_user(id)` at line 42
- Check `find_user`: it returns a user with `email: None` when the DB column is NULL
- Root cause: `find_user` should return `Option<User>` or the query should filter `WHERE email IS NOT NULL`

## Wrong Output

**Technique: Binary search at pipeline midpoints**

For a pipeline with stages A -> B -> C -> D -> E:

1. Log the value at stage C (midpoint)
2. Is the value correct at C?
   - Yes: bug is in D or E. Log at D (midpoint of D-E).
   - No: bug is in A, B, or C. Log at B (midpoint of A-C).
3. Repeat until you find the exact stage where the value goes wrong
4. Three iterations for a 10-stage pipeline

**Key insight:** do not trace forward from the beginning. Binary search is O(log n) while linear tracing is O(n).

## Intermittent / Flaky

**Technique: Passing vs failing run diff**

1. Run the test 10 times, capturing full logs each time
2. Select one passing run log and one failing run log
3. Diff the two logs line by line
4. The first point where event ordering diverges is the race condition
5. Identify: what shared state is being accessed? What ordering assumption is violated?

**Common causes:**
- Missing mutex/lock around shared state
- Event ordering assumption (A always happens before B)
- Time-dependent behavior (timeouts, sleeps, system clock)
- Resource contention (file handles, ports, connections)

## Regression

**Technique: git bisect**

```bash
git bisect start
git bisect bad HEAD
git bisect good <last-known-good-commit>
# Run the test at each bisect point
git bisect run <test-command>
```

Once the offending commit is found:
1. Read the full diff of that commit
2. Identify the unintended side effect
3. Fix the side effect while preserving the commit's original intent

## Performance / Timeout

**Technique: Stage boundary timing**

1. Add timestamps at the entry and exit of each major stage
2. Run the slow operation
3. Calculate elapsed time per stage
4. The stage taking 95%+ of the time is where to focus
5. Drill into that stage: is it CPU-bound (tight loop, bad algorithm) or IO-bound (blocking call, deadlock)?

**Common causes:**
- O(n^2) algorithm that worked at small scale
- Unbounded retry loops
- Missing index on database query
- Deadlock between concurrent operations
- Synchronous IO in a hot path

## Test Failure

**Technique: Assertion backward trace**

1. Read the assertion: `expected X, got Y`
2. Where does `Y` (the actual value) come from?
3. Trace `Y` backward through the call chain
4. At each step ask: is this intermediate value correct?
5. The first incorrect intermediate value is closest to the root cause

**Key question:** Is the code wrong or is the test wrong? Check if the test's expected value matches the current specification. Specifications change; tests do not always keep up.
