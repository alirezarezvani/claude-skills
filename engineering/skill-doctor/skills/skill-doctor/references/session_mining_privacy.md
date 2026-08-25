# Session mining privacy — the local-only contract and the redaction canon

Session transcripts are the most sensitive artifact an agent setup produces: they
contain pasted secrets, internal paths, customer data fragments, and the user's
own words. skill-doctor reads them, so it carries the strictest handling rules in
this plugin. This reference explains each rule and where its pattern set comes from.

## 1. The contract

1. **Read-only sources.** Session history (`~/.claude/projects/**.jsonl`,
   `~/.codex/sessions/**`) is never modified, moved, or re-written — only parsed.
2. **Local-only outputs.** Condensed transcripts, inventory, scores, and the
   report are written to one scratch directory on the user's machine. Nothing is
   uploaded by any script; the SKILL.md forbids the agent from doing so either.
   The only shareable artifact is the report the user chooses to share.
3. **Redact before write.** Every transcript line passes `redact_secrets()`
   before touching disk. There is deliberately no `--no-redact` flag: an
   unredacted condensed transcript is a copy of the secret in a second location,
   which is exactly what secret-hygiene guidance says never to create (source 3).
4. **Restrictive permissions.** Output directories are `chmod 0700`, files
   `0600` — the process-umask default is world-readable on many systems. This
   follows the hardening applied to `engineering/skillopt-sleep/` in this repo
   after its adversarial review rounds (source 6).
5. **Data minimization.** Transcripts are condensed (message and tool-output
   budgets, head/tail truncation of long sessions) — collect what scoring needs,
   not everything available. This is GDPR Art. 5(1)(c)'s principle applied to a
   local tool: minimum data, single purpose, short-lived scratch storage (source 2).

## 2. The redaction pattern set

The patterns in `collect_sessions.py` are a curated subset of the detector sets
used by the mainstream secret scanners — gitleaks' default ruleset (source 4),
TruffleHog's detector corpus (source 5), and GitHub secret scanning's published
provider patterns (source 7):

| Label | Shape | Canonical source |
|---|---|---|
| `private-key` | `-----BEGIN … PRIVATE KEY-----` block | gitleaks `private-key` |
| `aws-access-key` | `AKIA`/`ASIA` + 16 chars | AWS credential format; gitleaks |
| `github-token` | `ghp_`/`gho_`/`ghu_`/`ghs_`/`ghr_`, `github_pat_` | GitHub token formats (source 7) |
| `anthropic-key` / `openai-key` | `sk-ant-…` / `sk-…` | vendor formats; ordered so the more specific wins |
| `slack-token` | `xox[baprs]-…` | Slack token format |
| `stripe-key` | `sk_live_` / `rk_live_` | Stripe key format |
| `jwt` | three base64url segments starting `eyJ` | RFC 7519 structure |
| `bearer-token` | `Bearer <long-token>` | RFC 6750 header |
| `connection-string` | `scheme://user:pass@host` | OWASP secrets guidance (source 3) |
| `url-credential` | `?token=`/`&api_key=`… | GitHub/Azure SAS-style URL secrets |
| `env-secret` | `*_API_KEY=`, `*_SECRET:` … value | env-assignment heuristic (keeps the variable name, redacts the value) |

Replacement is `[REDACTED:<label>]`, and the per-label counts land in
`inventory.json` — so the report can honestly say how much was scrubbed, and a
sudden spike in redactions is itself a finding about the user's workflow.

**Known limits.** Pattern-based scanning misses high-entropy secrets with no
recognizable shape and free-text PII (names, emails in prose). That is why
redaction is a second line, not the first: the first is that transcripts are
condensed, stay on the machine, and live in a temp directory the OS reclaims.

## 3. Why the harness vendors' own guidance matters

Claude Code stores full session transcripts locally per project (source 1); the
data is the user's, on the user's disk, and a grading tool inherits that trust
boundary. Mining it is legitimate exactly as long as the results stay inside the
boundary — the same read-only-harvest posture the SkillOpt sleep engine takes with
the identical data source (source 6).

## Sources

1. Anthropic — Claude Code data usage & session-history documentation (code.claude.com/docs; transcripts under `~/.claude/projects/`).
2. GDPR, Art. 5(1)(c) — data minimisation: adequate, relevant, limited to what is necessary for the purpose.
3. OWASP Secrets Management Cheat Sheet — cheatsheetseries.owasp.org: never duplicate secrets into logs or derived artifacts.
4. gitleaks — github.com/gitleaks/gitleaks default ruleset (`gitleaks.toml`): the reference regex corpus for token shapes.
5. TruffleHog v3 — github.com/trufflesecurity/trufflehog detector corpus: provider-specific secret formats.
6. This repo — `engineering/skillopt-sleep/README.md` "Deviations from upstream": `redact_secrets()` coverage of every persisted artifact plus the 0700/0600 chmod pass; `productivity/handoff` ships the sibling 17-pattern redaction linter.
7. GitHub Docs — *Secret scanning patterns*: published token formats for GitHub and partner providers (`ghp_`, `github_pat_`, and the partner list).
