# Checking a summary against the run

A session summary, a handoff note or a PR description written by an agent is a
set of claims. Most are true. The ones that are not tend to be the expensive ones:
"tests pass", "I didn't touch the config", "migration ran".

## From sentence to claim

| Sentence in the summary | Claim |
|---|---|
| "All tests pass" | `passed:pytest` (use the actual command text) |
| "I ran the linter" | `ran:ruff` |
| "Fixed the client" | `edited:src/client.py` |
| "Config is unchanged" / "I didn't touch X" | `not-edited:config.yaml` |
| "Checked the schema first" | `read:db/schema.sql` |
| "Did not deploy" | `not-run:deploy` |

Match on a distinctive part of the command (`pytest`, `npm test`, `make check`),
not on a word that every command contains.

## Verdicts and what to say

| Verdict | Say |
|---|---|
| `SUPPORTED` | State it, citing the step |
| `SUPPORTED_INFERRED` | "The shell command at step N would have done this (inferred)" |
| `STALE` | "Tests passed at step N, but files changed at steps M afterwards; they have not run since" |
| `PARTIAL` | "Step N exited 0, but that is the exit of the last command in the line" |
| `NOT_IN_TRACE` | "The recording does not show this" |
| `UNVERIFIABLE` | "It ran at step N but no result was recorded (interrupted)" |
| `CONTRADICTED` / `_INFERRED` | Correct the account first, citing the steps |

## Why exit codes need care

- In POSIX shells a pipeline's exit status is the last command's
  (`pytest | tee log` exits 0 when `tee` does) unless `pipefail` is set. A `;`
  list exits with its last command too. `a && b` exits 0 only if both did.
- Test runners use more than pass/fail: pytest exits 5 when it collected no
  tests, which the checker counts as not passed.
- "Passed" means at the time of that run. An edit after the last green run makes
  the claim stale, however small the edit.

## Correcting an account

Lead with the correction, cite the step, then the consequence:

> Correction: I said config.yaml was unchanged. Step 9 ran
> `sed -i 's/retries: 0/retries: 3/; s/timeout: 30/timeout: 5/' config.yaml`, which
> also lowered the timeout from 30 to 5. That is the likely cause of the
> production timeouts. I did not mention it at the time.

Do not soften a contradiction into "I may have". The recording settles it.

## Sources

1. IEEE/The Open Group. POSIX.1-2017 Shell Command Language, §2.9.2 Pipelines (exit status of a pipeline). https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html 🟢
2. GNU Bash Reference Manual, Pipelines and `set -o pipefail`. https://www.gnu.org/software/bash/manual/bash.html#Pipelines 🟢
3. pytest documentation, "Exit codes" (0 passed, 1 failed, 5 no tests collected). https://docs.pytest.org/en/stable/reference/exit-codes.html 🟢
4. Anthropic. "Building effective agents" (2024): agents should get ground truth from the environment at each step. https://www.anthropic.com/engineering/building-effective-agents 🟢
5. Jimenez et al. "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" 2023 (success judged by running tests, not by the model's report). arXiv:2310.06770 🟢
6. Kent, Souppaya. NIST SP 800-92, *Guide to Computer Security Log Management*, 2006 (logs as the evidence record). 🟢
7. METR. "Recent Frontier Models Are Reward Hacking." 2025 (models claiming success they did not achieve). https://metr.org/blog/2025-06-05-recent-reward-hacking/ 🟡
