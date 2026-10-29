# mcp-oauth-triage

Classify why an MCP connector that used to authenticate has stopped, before you change any code.

Five faults share one symptom (a wall of 401s while every dashboard reports the connection healthy) and
need opposite fixes. Rotating a client secret while the real fault is a serialiser that writes a wrapper
key produces a second, harder incident. Re-authenticating cures a poisoned auth cache for a day and
hides the actual defect.

## Install

```bash
claude /plugin install engineering-advanced-skills
```

Or copy the directory into your agent's skills tree:

```bash
cp -r engineering/skills/mcp-oauth-triage ~/.claude/skills/
```

Works with Claude Code, Codex CLI, Gemini CLI, and any agent that reads `SKILL.md` under the
agentskills.io standard. Python 3.8 or newer, standard library only, no network access.

## Usage

```bash
# 1. Redact a token record before it goes into a ticket or a chat
python3 scripts/oauth_triage.py --token-file ~/.config/my-mcp/token.json --redact

# 2. Classify from a record and a connector log
python3 scripts/oauth_triage.py --token-file ./token.json --log ./connector.jsonl

# 3. Machine-readable verdict for CI or a ticket
python3 scripts/oauth_triage.py --token-file ./token.json --log ./connector.jsonl --json
```

Exit codes: `0` no defect signals, `1` suspect only, `2` a class is confirmed.

## The five classes

| Class | One-line discriminator | Cheap confirmation |
|---|---|---|
| Envelope mismatch | token exists in the file, reader reports it missing | compare reader keys with record keys |
| Expiry semantics | failures at a suspiciously fixed interval | failure gap equals token lifetime |
| Rotation clobber | two refreshers, one credential store | more than one exchange per window |
| Binding fault | one surface fails, another accepts the same token | token `aud`/`iss` vs surface metadata |
| Poisoned negative cache | re-auth appears to work, behaviour never changes | clear the marker only, retry |

Full decision table, log signatures, and worked examples:
[references/failure-classes.md](references/failure-classes.md).

## What it will not do

- It does not call OAuth providers. It reads artifacts you already have.
- It does not prove a connector is healthy. Exit 0 means "not proven broken".
- It does not fix anything. It names the class so the fix is not a guess.

## Example output

```
$ python3 scripts/oauth_triage.py --token-file ./token.json --log ./connector.jsonl
primary_class: rotation_clobber
confidence:    high
  - [high] rotation_clobber: 3 exchange(s) within 60s of the previous one; concurrent refreshers rotate each other's token
  - [high] rotation_clobber: stored refresh_token does not match the most recent exchange result (18 vs 22 chars)
next_probe:    Count concurrent refreshers; add a single-flight lock around exchange plus store, then re-check the stored refresh token.
exit_code:     2
```

## Verification

A login is not a verification. The failure mode is refresh. See
[references/verification-recipes.md](references/verification-recipes.md) for the three-call round trip
and the six-row evidence pack a fix report needs.

## Tests

The classifier ships with a fixture matrix covering all five classes plus a clean record. Run it before
changing any detector:

```bash
python3 scripts/run_fixtures.py --verbose
# 6/6 fixtures matched
```

Fixtures live in `assets/fixtures/`, expected verdicts in `expected_outputs/verdicts.json`. When you add
a detector, add a fixture and an expected verdict in the same commit, otherwise the matrix stops being
evidence and becomes decoration.

## Related skills

- `mcp-server-builder` for first-time OAuth wiring and tool contract design.
- `chaos-engineering` for rehearsing refresh failure before a provider rehearses it for you.
- `coding-agent-rollout` for deciding which credentials an agent may hold.

## License

MIT, matching the parent repository.
