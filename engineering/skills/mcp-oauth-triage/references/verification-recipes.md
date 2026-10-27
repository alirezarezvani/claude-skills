# Verification Recipes

A login proves consent. It does not prove the connector survives a refresh, and refresh is where four of
the five classes live. Use these recipes to produce evidence a reviewer can check without trusting you.

## Recipe 1: Record shape

```bash
python3 scripts/oauth_triage.py --token-file ./token.json --expect-flat --expect-absolute-expiry
```

Expect exit 0. A non-zero exit names the field causing it. Run this after any change to a serialiser, a
dataclass, or a model alias.

## Recipe 2: Single refresher

The goal is to prove exactly one exchange happens per credential per expiry window.

```bash
python3 scripts/oauth_triage.py --token-file ./token.json --log ./connector.jsonl --json \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['primary_class'], d['confidence'])"
```

Then, with the connector under normal load, count exchange events in one window:

```bash
python3 - <<'PY'
import json
from collections import Counter

events = [json.loads(l) for l in open('connector.jsonl') if l.strip()]
exchanges = [e for e in events if str(e.get('event', '')).lower() in
             {'exchange', 'refresh', 'token_exchange', 'token_refresh'}]
print('exchanges:', len(exchanges))
print('distinct credentials:', len({e.get('credential') or e.get('account_id') or '?' for e in exchanges}))
PY
```

One exchange per credential per window is correct. Two or more inside the same window is class C, even
if the connector currently works, because the next rotation will decide a winner you cannot control.

## Recipe 3: Round trip across a refresh

This is the only recipe that proves a fix. Record all three results.

```bash
# 1. Call through the surface that was failing, before any refresh
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $TOKEN" "$SURFACE"

# 2. Force one refresh, then call again
#    (force by expiring the record or by invoking the connector's refresh entry point)
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $TOKEN" "$SURFACE"

# 3. Wait for the next scheduled refresh, then call a third time
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $TOKEN" "$SURFACE"
```

Two of three is not a fix. A pattern of 200, 200, 401 means the fault is downstream of the first
refresh, which usually points at class B or C rather than the original symptom.

## Recipe 4: Binding comparison

```bash
# What the token claims
python3 scripts/oauth_triage.py --token-file ./token.json --expect-aud "$SURFACE" --json

# What the surface advertises
curl -s "$SURFACE/.well-known/oauth-protected-resource" | python3 -m json.tool
```

Compare `aud` against the advertised `resource`, and `iss` against the advertised authorization server.
A mismatch on either is class D and no amount of re-authentication will change it.

## Recipe 5: Negative cache isolation

```bash
# 1. Snapshot the marker state
python3 scripts/oauth_triage.py --token-file ./token.json --json | grep -i cache

# 2. Clear only the marker, leave the credential untouched, retry
# 3. If service returns, the class is E, and the marker needs a scope
```

Do not delete the credential to test this. Deleting the credential confirms nothing and costs a login.

## Minimum evidence pack for a fix report

| Item | Command |
|---|---|
| Pre-fix verdict | `oauth_triage.py --token-file old.json --log old.jsonl --json` |
| Post-fix verdict | `oauth_triage.py --token-file new.json --log new.jsonl --json` |
| Exchange count under load | Recipe 2 |
| Round trip | Recipe 3, all three codes |
| Diff of the change | `git diff` of the writer, the reader, and the lock |
| Scope of any cache or marker touched | the exact path or key, and why that scope |

Six rows, six commands. If a row is empty, the fix is not verified, whatever the connector appears to do
in the moment.
