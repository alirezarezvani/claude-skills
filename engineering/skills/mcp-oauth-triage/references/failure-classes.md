# Failure Classes: Decision Table and Log Signatures

Companion to `SKILL.md`. Use this file when the classifier returns a class you need to argue for, or
when it returns `none` against a live symptom and you have to decide which artifact is missing.

## The single question that separates the five classes

Ask: **did the token exchange succeed?**

| Answer | Then ask | Class |
|---|---|---|
| Exchange failed | Was the failure transient (5xx, timeout) or permanent (400, invalid_grant)? | Transient is not a class, retry with backoff. Permanent is class D or a registration fault |
| Exchange succeeded | Does the stored record carry the token the exchange returned? | No: class A. Yes: next row |
| Stored correctly | Does the epoch the record claims match the provider's view? | No: class B. Yes: next row |
| Expiry agrees | Did a second refresher write between the exchange and the store? | Yes: class C. No: next row |
| No clobber | Does the failing surface accept this token from another client? | Yes: class D. No: next row |
| Surface rejects it there too | Does an auth marker survive a successful login? | Yes: class E |

Transient failures are deliberately not a class. They matter only because a retry loop around a
transient failure creates class C, which is permanent. That is the most common way a provider blip
becomes a multi-day outage.

## Class A: Envelope mismatch

**Log signature**

```
exchange  200  {"tokens": {"access_token": "..."}}
store     200  wrote keys: ["tokens"]
load      200  keys present: false
call      401  missing access_token
```

The store and the reader disagree about depth. The token exists, the reader cannot see it, and every
health check that reads the file directly reports success.

**Second variant:** the writer stores flat keys and a newer reader was written against a nested schema.
Same symptom, opposite direction, and the fix belongs in the reader, not the writer.

**Third variant worth knowing:** the writer serialises a dataclass whose fields are snake_case while
the reader deserialises a model with camelCase aliases and no fallback. The record looks correct to a
human and empty to the parser.

**Worked example.** A connector worked for three months and broke on a dependency upgrade that changed
the serialiser. The stored file still contained a valid token. The only change was a wrapper key. The
correct response was to normalise the write path and delete the old reader in the same commit, not to
teach the reader both shapes.

## Class B: Expiry semantics

**Log signature**

```
exchange  200  expires_in: 3599.999
store     200  expires_at: 1793113293.123
load      200  expires_at: 1793113293   (truncated)
call      401  at t+3599.5
```

Or, for the sentinel variant:

```
store     200  expires_at: 0
load      200  treating expires_at 0 as no expiry
call      401  immediately after the next provider-side rotation
```

The dangerous variant is the falsy sentinel, because `if not expires_at: skip refresh` reads as
defensive code and is wrong. Zero means "expired at the epoch", never "unknown" and never "forever".

**Clock variant.** Two hosts, one skewed forward by minutes, sharing a credential store. The skewed host
writes an expiry in its own future, the honest host reads it as already past and refreshes constantly,
which then triggers class C.

**Confirmation arithmetic.** First failure timestamp minus issuance timestamp, compared with the token
lifetime the provider advertises. If those agree to within clock skew, the class is B. If the failure
arrives much earlier, keep looking.

## Class C: Rotation clobber

**Log signature**

```
exchange  200  refresh_token -> A
exchange  200  refresh_token -> B      (same credential, 40ms later)
store     200  refresh_token: A        (losing writer)
refresh   400  invalid_grant
refresh   400  invalid_grant
```

Providers that rotate refresh tokens invalidate the previous value on every exchange. Two callers, one
store, and the loser's write decides which token survives. The result is a credential that is dead on
both sides while each component believes it did the right thing.

**Where it comes from.** Startup warm-up plus the first real request; wake-from-sleep plus a scheduled
refresh; a retry decorator around the exchange without idempotence; a tool-call fan-out where several
handlers notice the same expiry at once.

**The mitigation that works.** One refresher per credential, a lock held across both the exchange and
the store write, and every other caller waiting on that result. A refresh that completes without
writing, or a write that happens outside the lock, reintroduces the class.

**The mitigation that does not work.** Comparing token strings before writing. It closes the window only
if the compare and the write are atomic, which they usually are not.

## Class D: Binding fault

**Log signature**

```
exchange  200  aud: https://api.other.example.com
call      401  {"error": "invalid_token", "error_description": "audience mismatch"}
```

Binding faults fail one surface while another accepts the same token. That is the discriminator: a
storage or expiry fault is indifferent to which endpoint you call.

**Sub-classes**

| Sub-class | Discriminator | Fix |
|---|---|---|
| Audience mismatch | token `aud` does not cover the failing surface's protected-resource metadata | request the advertised resource |
| Issuer mismatch | token `iss` names a different environment or tenant | point the client at the issuer that matches the surface |
| Scope under-grant | 403 with `insufficient_scope` while other calls succeed | request the scope the failing tool needs, at consent time |
| Account collision | data belongs to another account, no error at all | key credentials on a stable account id, never on email or display name |

Account collision is the one that produces no error and therefore no incident. It only surfaces when
someone notices a record that should not be there.

## Class E: Poisoned negative cache

**Log signature**

```
helper    502  preflight failed
store     200  needs_auth: true
login     200  user completed consent
call      401  connector disabled: needs auth
call      401  connector disabled: needs auth
```

A negative result was cached at a scope broader than the thing that failed. Fixing the cause does not
clear the effect, so re-authenticating appears to work and changes nothing visible.

**Where the marker usually lives.** A user-level settings file, a workspace-level cache, an
organization policy record, a keychain item separate from the credential, or a row in a database that
outlives the process.

**Confirmation that costs nothing.** Clear only the marker, leave credentials untouched, retry. Recovery
proves the class without a single new login. If clearing the marker restores service and the next
transient failure re-poisons it, the class is confirmed twice over.

## Reporting a verdict

Lead with three lines and stop:

1. Class, with confidence.
2. The one artifact or probe that confirmed it.
3. The single next action.

Mechanism, history, and the alternative classes you ruled out belong in an appendix that most readers
will never open. A report that opens with a narrative of the investigation invites a second round of
questions; a report that opens with a class invites a fix.
