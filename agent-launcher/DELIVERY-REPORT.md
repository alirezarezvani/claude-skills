# agent-launcher — delivery report (implemented vs spec)

**Goal:** implement `SPEC.md` fully — a plugin re-implementation of Anthropic's
`launch-your-agent` (Apache-2.0; independent, not a fork) for building Claude
Managed Agents, where every session starts with a goal that compiles into a loop
or a workflow.

**Method:** built the plugin, self-tested every tool + the full 4-phase pipeline,
then ran an independent 10-agent verification **workflow** (`verify-agent-launcher`)
that re-checked each spec part against disk (read-only; re-ran the tools itself) and
synthesized a verdict.

## Verification verdict: **PASS** — 9/9 parts, 0 differences from spec

| # | Spec part | Verdict | Evidence (independent re-check) |
|---|---|---|---|
| 1 | 6 skills | ✅ PASS | Exactly the 6 folders; each SKILL.md name = folder, valid frontmatter (v2.12.0); orchestrator has `context: fork`; all carry a Forcing-question library |
| 2 | 18 stdlib tools | ✅ PASS | All 18 filenames present; every `--help`/`--sample` exits 0; **zero** network imports (`requests`/`urllib`/`socket`/`anthropic`/`openai`/`httpx`/subprocess); no key echoed |
| 3 | 4 agents | ✅ PASS | orchestrator + interviewer + grader + deployer; valid frontmatter; distinct voice each; router / grade-loop / scheduling roles correct |
| 4 | 8 commands | ✅ PASS | launch, goal, interview, stage-launch, grade, run-without-you, wrap-up, grill — all with `description`; `/cs:goal` covers set/status/advance; grill = one-question-at-a-time |
| 5 | Opt-in hooks | ✅ PASS | hooks.json valid (SessionStart+End); **no flag → silent, exit 0**; `AGENT_LAUNCHER_SESSION=1` + goal → emits `<agent_launcher_goal>`, exit 0; both wrapped so any error still exits 0 |
| 6 | References + assets | ✅ PASS | 5 references (each sourced); schema valid JSON; example-build-sheet conforms to schema required fields |
| 7 | Manifest + registration + counters | ✅ PASS | plugin.json valid (6 `./`-prefixed skills, source + attribution blocks); marketplace lists it; `check_plugin_json.py --all` OK; `derive_counters.py --check` passes |
| 8 | Hard rules | ✅ PASS | No key printed/embedded; `payload_validator.py` FAILs on an embedded key; `loop_compiler.py` clamps max_iterations 99→20 and 0→1; `primitives_validator.py` FAILs on 21 skills/9 stores/99 iters; `cron_validator.py` rejects bad cron (exit 1) |
| 9 | Goal → loop/workflow model | ✅ PASS | goal.json phase progression works; router exit 0/3/4 (route/ask/refuse); loop_compiler emits single-pass, **bounded grade-iterate**, and **cron-loop** (with nestable outcome) — both loop types real |

**Synthesis (verbatim):** "No differences from spec were found in any part."
**Recommended follow-ups from the workflow:** none.

## Design decisions (as chosen up front)

| Decision | Choice implemented |
|---|---|
| Placement | New top-level `agent-launcher/` domain plugin (`research-ops`/`markdown-html` shape) |
| Session goal | **Both** — opt-in `AGENT_LAUNCHER_SESSION=1` SessionStart hook **and** `/cs:goal` command surface |
| Live vs scaffold | **Deterministic BYOK scaffolders** — stdlib-only, no API calls; live launches emitted as curl the user runs |
| Loop model | **Both** — bounded grade→iterate loop **and** recurring cron deployment loop (a cron loop can nest an outcome so each firing self-grades) |

## What was built

- **6 skills** (orchestrator `context: fork` + interview + stage-launch +
  grade-iterate + run-without-you + wrap-up)
- **18 stdlib tools** (3/skill), all `--help`/`--sample` clean
- **4 agents**, **8 `/cs:*` commands**, **opt-in SessionStart/SessionEnd hooks**
- **5 shared references** (CMA primitives, interview→config, examples bank,
  loops-and-workflows, session-goal model)
- **4 assets** (build-sheet JSON schema, overview HTML template, NEXT-DIRECTIONS
  template, example build sheet)
- Registered in `marketplace.json`; headline counters trued up
  (skills 362→368, domains 18→19, tools 644→664, refs 741→746, agents 102→106,
  commands 116→124, plugins 88→89) — `derive_counters.py --check` green.

## Things that differed from the original plan

**None.** Every deliverable in `SPEC.md` shipped as specified, and the independent
verification workflow found zero deviations. One implementation detail worth noting
(not a deviation): the tools emit **BYOK curl** for all live CMA calls rather than
calling the API, which is the deliberate consequence of the "deterministic
scaffolders" decision and the repo's no-network-in-scripts / no-paid-dependency
rules.

## How it was verified (reproducible)

```bash
# every tool
for f in agent-launcher/skills/*/scripts/*.py; do python3 "$f" --help; python3 "$f" --sample; done
# full 4-phase pipeline produced: goal.json, build-sheet.json, payloads/, launch.sh,
#   outcome.json, deployment.json, eval.json, NEXT-DIRECTIONS.md, agent-overview.html
# gates
python3 scripts/check_plugin_json.py --all      # agent-launcher OK
python3 scripts/derive_counters.py --check       # passes
bash -n my-agent/launch.sh                        # syntax OK
```

_Verification workflow: `verify-agent-launcher` (10 agents, 0 errors, ~212s)._
