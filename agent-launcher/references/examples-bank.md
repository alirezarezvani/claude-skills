# Examples bank — CMA agents worth launching

Concrete v0 scopes the interview can anchor on. Each shows the one job, the loop
shape, and the first deferral. Use these to open the interview warmly, then build
from the founder's own words — never substitute an example for what they stated.

## 1. Support-inbox triage (recurring loop)
- **Job:** every morning, read overnight support emails and label each
  urgent / question / bug / spam with a one-line reason.
- **Primitives:** cloud env (unrestricted) · agent toolset · Gmail MCP
  (`always_ask`) · `read_only` memory of past labels · outcome rubric on label
  accuracy · cron `0 9 * * *`.
- **Loop:** recurring deployment, each firing self-grades (nested outcome).
- **v0 mock:** custom `label_email` tool returns a mock result; **v1** wires the
  real Gmail MCP when the OAuth vault cred lands.

## 2. Nightly repo dependency auditor (recurring loop)
- **Job:** scan the repo for outdated / vulnerable dependencies and write a
  `report.md`.
- **Primitives:** cloud env with `npm` + `pip` · `repository` resource · agent
  toolset · outcome rubric ("names every advisory with a fix") · cron `0 2 * * *`.
- **Loop:** recurring deployment.
- **v1:** open a PR with the bumps (needs GitHub MCP).

## 3. Weekly competitor pulse (recurring loop)
- **Job:** each Monday, fetch three competitor changelogs and summarize what
  changed for our roadmap.
- **Primitives:** `limited` networking (`allowed_hosts` = the three domains) ·
  `web_fetch` · `read_write` memory of prior weeks · outcome rubric · cron
  `0 8 * * 1`.
- **Loop:** recurring deployment; memory makes week 10 sharper than week 1.

## 4. One-shot data cleaner (single-pass → grade loop)
- **Job:** normalize a messy CSV to a target schema and validate every row.
- **Primitives:** cloud env with `pandas==2.2.0` · `file` resource · agent
  toolset · outcome rubric on schema conformance · `max_iterations: 5`.
- **Loop:** grade→iterate until `satisfied`; no schedule (runs on request).

## 5. Draft-only sales-email responder (grade loop, human-in-loop)
- **Job:** draft (never send) a reply to an inbound sales email in our voice.
- **Primitives:** agent toolset · `read_only` memory of our voice guide · outcome
  rubric on tone + accuracy · custom `save_draft` tool (`always_ask`).
- **Loop:** grade→iterate; sending stays a human step (v1 = wire real send behind
  `always_ask`).

## Pattern notes

- **Mock connectors in v0.** Every example that needs a real integration ships a
  schema-true custom-tool mock first; the real MCP server is the first v1 deferral.
- **Memory is opt-in.** Only examples that benefit from cross-run learning attach a
  store; the rest skip it to reduce surface.
- **Every recurring loop nests an outcome** so each firing self-grades.

## Sources

1. anthropics/launch-your-agent — `examples-bank.md`.
2. Claude Managed Agents — Overview (use-case framing).
3. Anthropic — "Building effective agents" (agent use-case taxonomy).
4. Anthropic customer stories — internal-worker / product-feature agent patterns.
5. This repo — engineering/dependency-auditor, marketing pulse, research/pulse (analogous jobs).
6. Anthropic engineering — "How we built our multi-agent research system" (2025): orchestrator/worker decomposition patterns the example agents mirror.
7. Anthropic engineering — "Writing effective tools for agents": tool-surface design criteria applied when picking each example's connectors.
