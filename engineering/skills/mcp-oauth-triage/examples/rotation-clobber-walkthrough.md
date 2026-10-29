# Example: triaging a connector that fails once a day

A worked walkthrough of the most common real shape. Everything below is reproducible from the shipped
fixtures in `assets/fixtures/`.

## The report

A team reports: "Our MCP connector disconnects every morning. Restarting fixes it. Reconnecting the
account fixes it too. It comes back the next day."

Three descriptions of the same event, and all three point at different fixes. Restarting clears an
in-memory path. Reconnecting replaces credentials. Neither addresses the cause.

## Artifact 1: the record

```bash
python3 scripts/oauth_triage.py --token-file assets/fixtures/rotation_record.json --redact
```

```json
{
  "access_token": "<redacted:str>",
  "expires_at": 1793116893,
  "refresh_token": "<redacted:str>"
}
```

The shape is correct. One flat record, one absolute integer expiry, a refresh token present. Nothing
here explains a daily failure, which is the first useful fact: the fault is not in storage shape, so
classes A and B are unlikely.

## Artifact 2: the log

```bash
python3 scripts/oauth_triage.py --token-file assets/fixtures/rotation_record.json \
  --log assets/fixtures/rotation_events.jsonl
```

```
primary_class: rotation_clobber
confidence:    high
  - [high] rotation_clobber: 2 exchange(s) within 60s of the previous one; concurrent refreshers rotate each other's token
  - [high] rotation_clobber: stored refresh_token does not match the most recent exchange result (19 vs 18 chars)
  - [medium] rotation_clobber: 1 store event(s) carry no refresh_token payload, so a clobbering writer cannot be distinguished from a correct one
next_probe:    Count concurrent refreshers; add a single-flight lock around exchange plus store, then re-check the stored refresh token.
exit_code:     2
```

Two exchanges inside one minute for a single credential (three in total, so two consecutive pairs fall
inside the window), and the stored refresh token predates the last exchange. The third finding is the
tell that matters most in practice: the store write carried no refresh token, so the writer that lost
the race had no way to record that it lost. That is the signature: a component refreshed, another component refreshed concurrently,
the provider invalidated the first token on the second exchange, and a late writer put a dead token back
in the store.

The "daily" periodicity is not a schedule. It is the token lifetime: every refresh window, whichever
process wakes first wins the race, and the loser's write is the one that persists.

## Artifact 3: why restarting appeared to work

A restart drops the in-memory credential and forces one refresh path to start alone, so the first
exchange after a restart cannot race. The connector then works until the next window where two paths
overlap. That is why the fix looked real and lasted exactly one token lifetime.

## The fix

```python
# One refresher per credential. The store write lives inside the same lock.
def refresh(credential_id, store, exchange, lock_factory):
    with lock_factory(credential_id):
        current = store.read(credential_id)
        if not is_expired(current):
            return current
        fresh = exchange(current["refresh_token"])
        store.write(credential_id, fresh)     # inside the lock, not after it
        return fresh
```

Three properties matter, and dropping any one of them reintroduces the class:

1. The expiry check happens **inside** the lock, so a caller that arrives second sees the fresh token
   instead of exchanging again.
2. The store write happens **inside** the lock. A write after release is the clobber.
3. The lock is keyed on the credential, not the process, so two processes cannot each hold "the" lock.

## Verification

```bash
# Post-fix record and log should classify clean
python3 scripts/oauth_triage.py --token-file new_token.json --log new_connector.jsonl

# And the fixture matrix should still be green if you touched the detector
python3 scripts/run_fixtures.py --verbose
```

Then run the three-call round trip from `references/verification-recipes.md`: succeed before a refresh,
succeed after one refresh, succeed after a second. A connector that survives two refreshes has survived
the window that produced the original symptom.

## What the same report would have looked like as a different class

| If the log had shown | The class would be | The fix would be |
|---|---|---|
| one exchange, then a 401 on the first call | B, expiry semantics | store an absolute integer expiry |
| one exchange, then a 401 on a different surface only | D, binding fault | request the advertised audience |
| no exchanges at all, and a persistent auth marker | E, poisoned cache | clear and scope the marker |
| a stored record with a nested wrapper key | A, envelope mismatch | normalise on write, delete the second reader |

One symptom, five fixes. That is the reason the classifier runs before the change, not after.
