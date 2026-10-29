---
name: "mcp-oauth-triage"
description: "Diagnose why an MCP connector that used to authenticate now fails: classify the fault as envelope, expiry, rotation clobber, binding, or poisoned cache before changing any code. Use when a token exchange succeeds but tool calls 401, when a connector silently degrades after a refresh, when multi-account setups return another account's data, or when re-authenticating fixes the problem only until the next refresh."
---

# MCP OAuth Triage

**Tier:** POWERFUL · **Category:** Engineering · **Domain:** AI / Auth / Connectors

## Overview

An OAuth-backed MCP connector rarely fails at the exchange. It fails somewhere between storing what the
exchange returned and reading it back on the next call, so the visible symptom is a wall of 401s while
every dashboard says the connection is healthy.

The cost of guessing is high because five common faults share one symptom and need opposite fixes.
Rotating a client secret does nothing when the real fault is a writer and a reader disagreeing about
which key holds the token. Re-authenticating cures a poisoned auth cache for a day and hides the actual
defect. This skill exists to stop that guessing: collect three artifacts, run one classifier, fix the
class you actually have.

Use it **before** touching code, and again **before** declaring the fix done.

## When to Use

- A connector that authenticated yesterday returns 401 or 403 today with no configuration change.
- The token endpoint returns 200, but the first tool call after a refresh fails.
- Re-authenticating fixes the symptom, and the failure returns within one token lifetime.
- A multi-account install returns data belonging to the wrong account.
- A "needs auth" state persists after a successful login.
- A refresh loop hammers the token endpoint (429s, rotation churn) while the connector stays down.

Do not use this skill for first-time setup that never worked. That is a scopes, redirect URI, or client
registration problem, and it belongs with `mcp-server-builder`. This skill assumes a working state
existed and was lost.

## Features

One classifier covers five fault classes. Each row names the discriminator that separates it from its
neighbours, because the fixes are destructive to each other.

| Detector | Fires on | Confirmed by |
|---|---|---|
| Envelope check | token stored one level below where the reader looks | reader key list vs record key list |
| Expiry check | fractional TTL, zero sentinel, seconds/milliseconds confusion | failure gap equals token lifetime |
| Rotation check | more than one exchange per credential per window | stored refresh token vs last exchange result |
| Binding check | audience, issuer, or account-key mismatch | claims vs the surface's protected-resource metadata |
| Cache check | auth marker that survives a successful login | clearing the marker alone restores service |

The classifier also reports what it could not check, so a clean exit is read as "not proven broken"
rather than "proven working".

## Usage

```bash
# Classify from a record and a log
python3 scripts/oauth_triage.py --token-file ./token.json --log ./connector.jsonl

# Machine-readable verdict for a ticket or CI
python3 scripts/oauth_triage.py --token-file ./token.json --log ./connector.jsonl --json

# Redact a record before it goes into a ticket or a chat
python3 scripts/oauth_triage.py --token-file ./token.json --redact

# Assert the reader's expectations explicitly
python3 scripts/oauth_triage.py --token-file ./token.json --expect-flat --expect-absolute-expiry
```

| Exit | Meaning |
|---|---|
| 0 | No defect signals found in the supplied artifacts |
| 1 | Suspect findings only, worth a second probe |
| 2 | A defect class is confirmed by the artifacts |

Exit 0 is not a health check. If the symptom is live and the classifier is clean, the artifacts are
wrong, and Step 1 of the workflow is where to go back to.

## Workflow

### Step 1: Collect three artifacts

| Artifact | What it is | Why |
|---|---|---|
| Token record | the stored JSON the connector reads back, exactly as written | reveals envelope, field types, sentinels |
| Connector log | ordered events with timestamps: exchange, store, load, call, error | reveals order, races, which side failed |
| Timing | how long after a successful call the failure appears | separates expiry semantics from binding faults |

Redact secrets. The classifier needs key names, value types, and timestamps, never the token value.

### Step 2: Run the classifier

```bash
python3 scripts/oauth_triage.py --token-file ./token.json --log ./connector.jsonl --json
```

### Step 3: Match the class to its fix

Each class has one cheap confirmation and one fix. Apply the confirmation before the fix, because the
fixes are destructive to each other: rotating credentials while the real fault is a shape mismatch
produces a second, harder incident.

#### Class A: Envelope mismatch

The exchange returns a nested payload and the reader expects flat keys, or the reverse. The token
exists, the reader cannot see it, and every health check that reads the file directly reports success.

Fix: normalise on write and keep one reader. Do not add fallbacks that probe two shapes, because they
turn a loud failure into a silent one that survives the next refactor.

#### Class B: Expiry semantics

A TTL is stored in a form the reader misinterprets: fractional `expires_in`, an `expires_at` of `0`
read as "no expiry" when it means "expired at the epoch", or a relative duration read as an absolute
timestamp.

Fix: store one absolute expiry as an integer, compute it once from the provider response, and treat
zero and missing as expired. Never treat a falsy expiry as permanent.

#### Class C: Rotation clobber

Two refresh paths run concurrently. The provider rotates the refresh token and invalidates the old one.
The losing path writes its dead token over the winner's, and the next refresh fails permanently.

Fix: one refresher per credential, guarded by a lock, with the store write inside the same critical
section as the exchange. Every other caller waits on that result instead of exchanging again.

#### Class D: Binding fault

The token is valid, unexpired, correctly stored, and one surface still rejects it: audience or resource
mismatch, issuer mismatch between environments, wrong tenant, or a multi-account install keyed by a
human-readable identifier two accounts share.

Fix: request the audience the surface actually advertises, and key stored credentials on a stable
account identifier rather than an email address or display name.

#### Class E: Poisoned negative cache

A failed handshake writes a machine-wide or organization-wide "needs authentication" marker. The marker
outlives the failure, so a later successful login does not clear it and the connector stays disabled
while every credential is valid.

Fix: scope the marker to the credential it describes, and clear it on a successful exchange. A negative
cache must never outlive the condition that produced it.

### Step 4: Verify with one full round trip

A fix is not verified by a successful login. It is verified by surviving a refresh. Report three facts:
the call succeeded before refresh, it succeeded after refresh, and it succeeded after a second refresh.
Two of three is not a fix.

## Examples

**Example: rotation clobber, the cheapest possible detection.** A connector works, then fails once a
day at roughly the same hour, and re-authenticating fixes it until the next day.

```bash
$ python3 scripts/oauth_triage.py --token-file ./token.json --log ./connector.jsonl
primary_class: rotation_clobber
confidence:    high
  - [high] rotation_clobber: 2 exchange(s) within 60s of the previous one; concurrent refreshers rotate each other's token
  - [high] rotation_clobber: stored refresh_token does not match the most recent exchange result (19 vs 18 chars)
  - [medium] rotation_clobber: 1 store event(s) carry no refresh_token payload, so a clobbering writer cannot be distinguished from a correct one
next_probe:    Count concurrent refreshers; add a single-flight lock around exchange plus store, then re-check the stored refresh token.
exit_code:     2
```

The record was not corrupt and the credentials were not stale. Two components noticed the same expiry
at the same moment, one of them lost the rotation race, and its write decided which token survived.

**Example: envelope mismatch that survived a dependency upgrade.** A connector worked for months and
broke on a library upgrade that changed the serialiser. The stored file still held a valid token; the
only change was a wrapper key.

```bash
$ python3 scripts/oauth_triage.py --token-file ./token.json --expect-flat
primary_class: envelope_mismatch
confidence:    high
  - [high] envelope_mismatch: token sits under nested key 'tokens'; a flat reader sees no access_token
exit_code:     2
```

**Example: a clean record.** Exit 0 means the artifacts support no defect. It does not mean the
connector is healthy, and the correct next move is to collect a log or a failing call, not to close the
ticket.

## Architecture

The classifier is deliberately three stages, and each stage is testable in isolation.

```
record + log  ->  detectors (5)  ->  findings (class, severity, evidence)
                                           |
                                           v
                                  verdict (primary class, confidence)
                                           |
                                           v
                                  next_probe (one action) + exit code
```

- **Detectors are independent.** Each one reads the artifacts and emits findings. No detector can
  suppress another, so a clean result from one never hides a fault in another.
- **Severity drives the verdict.** The primary class is the highest-severity class present. Confidence
  rises only when the top class reaches high severity; everything else is reported as medium so a weak
  signal cannot be presented as a conclusion.
- **Evidence is text.** Every finding carries a sentence a reviewer can check against the artifact
  without re-running the tool. A finding you cannot restate in words is not evidence.
- **No network calls.** The tool never contacts a provider, so it is safe to run inside an incident, on
  a laptop, or against artifacts exported from production.

## Installation

```bash
# As part of the engineering plugin bundle
claude /plugin install engineering-advanced-skills

# Or copy into any agent's skills tree
cp -r engineering/skills/mcp-oauth-triage ~/.claude/skills/
```

Python 3.8 or newer, standard library only, no credentials required.

## Output Format

The classifier emits either a line-oriented report or JSON.

```json
{
  "primary_class": "rotation_clobber",
  "confidence": "high",
  "findings": [
    {"class": "rotation_clobber", "severity": "high", "evidence": "3 exchanges within 60s; stored refresh token is older than last exchange"}
  ],
  "next_probe": "Count concurrent refresh callers; add a single-flight lock around the exchange and store.",
  "exit_code": 2
}
```

When reporting to a team, lead with the class and the single next probe. Mechanism, history, and the
classes you ruled out belong in an appendix most readers will never open.

## Troubleshooting

| Symptom | First thing to check | Likely class |
|---|---|---|
| Login succeeds, first call 401 | reader key list vs record keys | A or B |
| Fails at a fixed interval after a refresh | failure gap vs token lifetime | B |
| Fails once a day, re-auth fixes it | exchange count per window | C |
| One surface fails, another accepts the token | `aud` and `iss` vs surface metadata | D |
| Login appears to work, behaviour never changes | auth marker outside the credential | E |
| Data from another account | credential key: email vs stable id | D |
| 429s on the token endpoint | concurrent refreshers | C caused by retry loop |

## Anti-Patterns

| Anti-pattern | Why it hurts |
|---|---|
| Rotating the client secret first | destroys the evidence for class C and D and forces re-registration during an incident |
| Re-authenticating and closing the ticket | cures class E temporarily and hides A, B, and C completely |
| Adding a fallback that accepts two record shapes | converts a loud failure into a silent one that outlives the fix |
| Treating a falsy expiry as "never expires" | produces tokens that never refresh and fail on the provider side |
| Retrying the refresh in a loop on failure | turns a rotation fault into a provider-side rate limit and a locked credential |
| Probing a second surface to "see if it works there" | class D needs a claim comparison, not more failing calls |
| Declaring success after a successful login | the failure mode is refresh, so a login proves nothing |
| Storing credentials keyed by email address | two accounts, one key, wrong tenant's data |

## Verification Checklist

Before calling a connector fixed, all of the following must be true:

- The classifier exits 0 against the post-fix record.
- The record holds one absolute integer expiry, or the reader explicitly accepts relative TTLs.
- Exactly one refresher exists per credential, and a concurrency probe shows no parallel exchange.
- The stored refresh token matches the one returned by the most recent successful exchange.
- A call through the previously failing surface succeeds before a refresh and again after it.
- The negative cache, if one exists, is scoped to the credential and cleared on success.

## Maintaining This Skill

The detector matrix is a shipped artifact, not a suggestion:

```bash
python3 scripts/run_fixtures.py --verbose   # expect 6/6
```

A new detector without a fixture in `assets/fixtures/` and an expected verdict in
`expected_outputs/verdicts.json` is untested code. Add all three in one commit.

## Related Skills

- **mcp-server-builder** for first-time server design: tool contracts, transport choice, and the
  initial OAuth wiring this skill assumes already worked once.
- **chaos-engineering** for rehearsing refresh failure deliberately, so the single-flight guard is
  tested before a provider outage tests it for you.
- **coding-agent-rollout** for the governance question of which credentials an agent may hold at all.

## References

- [references/failure-classes.md](references/failure-classes.md) for the full decision table,
  per-class log signatures, and worked examples.
- [references/verification-recipes.md](references/verification-recipes.md) for the round-trip
  verification commands and the minimum evidence pack for a fix report.
- [assets/fixtures/](assets/fixtures/) for the fixture matrix used by `scripts/run_fixtures.py`.
