# Secrets at commit time, and what to do when one got out

A secret is cheapest to stop before the commit exists. After a push it is in
every clone, fork and CI cache, and deleting it in a later commit removes it from
nothing but the tip.

## What secret_gate.py checks

Only lines the commit **adds**, plus the names of staged files:

| Code | What | Why it blocks |
|---|---|---|
| `SECRET` | provider-shaped tokens: AWS access key ids, GitHub/GitLab tokens, Slack tokens and webhooks, Stripe live keys, Google API keys, Anthropic/OpenAI keys, npm/PyPI tokens, private key blocks, JWTs, passwords in URLs | These shapes are rarely anything else |
| `GENERIC_SECRET` | `api_key`/`secret`/`token`/`password` assigned a literal of 16+ characters with Shannon entropy ≥ 3.5 bits/char | Catches in-house keys; placeholders such as `changeme`, `<token>`, `${VAR}` and environment reads are skipped |
| `SENSITIVE_FILE` | `.env` (but not `.env.example`), `*.pem`, `*.key`, keystores, SSH keys, `credentials.json`, `.netrc`, `*.tfstate` | Terraform state stores secrets in plain text |
| `CONFLICT_MARKER` | `<<<<<<<` / `>>>>>>>` | A broken file, not a secret, but just as certainly unwanted |

It warns on debugger leftovers and large files. Matches are printed redacted, and
the allowlist stores a hash, so neither the output nor the allowlist leaks the value.

**Measured (October 2026).** On 174,018 lines added to this repository over four
months, the gate raised 7 blocking findings: all were deliberate fake keys in
fixtures or examples, which a path waiver covers. On a 13-file set of synthetic
secrets in YAML, JSON, .env, Dockerfile, shell, Terraform, Go, Python and JS, it
caught 11 on the first run and 12 after unquoted config values were added; the
miss is a low-entropy password (`Winter2024!`), which no pattern gate catches
reliably.

**Limits, stated plainly.** It is pattern matching: it misses secrets with no
known shape and low-entropy passwords, and it cannot tell a live key from a
revoked one. It is a gate at the point of commit, not an audit of history. For a
deeper scan of history, an open-source scanner such as gitleaks (MIT) or Yelp's
detect-secrets (which OWASP names) does more.

## Waiving a false positive

Add a line to `.commit-craft-allow` at the repo root, with a reason of at least
10 characters. An entry without one is ignored.

```
3f9a0c1e5b7d2a44  documented example key from the vendor's public test docs
path:tests/fixtures/certs/*  throwaway certs generated for TLS tests, never deployed
```

Never waive to get a commit through. If the value is real, the waiver puts it in history.

## When a secret has already been committed

Order matters:

1. **Revoke or rotate it first.** OWASP: "Keys that were exposed should undergo immediate revocation", then a replacement is issued. GitHub's guide on removing sensitive data says the same, and that once the secret is revoked or rotated, rewriting history "may not be warranted".
2. **Only then consider rewriting history** with `git filter-repo` (GitHub recommends it; `--sensitive-data-removal` needs 2.47+). A rewrite of a shared branch changes every later commit id and needs everyone to re-clone, so it is a team decision.
3. **Check where else it went:** CI logs, build artifacts, forks, chat pastes.
4. **Add the gate** (`assets/hooks/pre-commit`) so the next one stops at the keyboard.

Not yet pushed? `git reset --soft HEAD~1` (or an interactive rebase on local
commits), remove the value, and commit again. Rotate anyway if it was ever in a
shared place such as a CI run or a screen share.

## Sources

1. OWASP, *Secrets Management Cheat Sheet* (8.1 detection before commit; 9.2 revocation and rotation). https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
2. GitHub Docs, *Removing sensitive data from a repository*. https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
3. MITRE, *CWE-798: Use of Hard-coded Credentials*. https://cwe.mitre.org/data/definitions/798.html
4. Git, `githooks` (pre-commit, commit-msg, pre-push). https://git-scm.com/docs/githooks
5. git-filter-repo (MIT). https://github.com/newren/git-filter-repo
6. gitleaks (MIT). https://github.com/gitleaks/gitleaks
7. Yelp, detect-secrets (Apache-2.0). https://github.com/Yelp/detect-secrets
