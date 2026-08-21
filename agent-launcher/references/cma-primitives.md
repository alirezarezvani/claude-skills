# Claude Managed Agents — Core Primitives & Limits

Reference for every tool and skill in this plugin. Semantics are drawn from the
public Claude Managed Agents (CMA) documentation
(https://platform.claude.com/docs/en/managed-agents/overview). Payload shapes the
plugin emits target this contract; always confirm against the live docs before a
production launch, since the API evolves.

## The four core primitives

| Primitive | ID prefix | What it is |
|---|---|---|
| **Agent** | `agent_…` | Reusable, **versioned** config: model, system prompt, tools, MCP servers, skills, optional multiagent roster. Each config-changing update mints a **new version**; immutable once created. |
| **Environment** | `env_…` | Execution context (Anthropic `cloud` sandbox or `self_hosted`). **Unversioned**; pre-installs + caches packages across sessions. |
| **Session** | `sesn_…` | One agent instance: isolated container, conversation history, sandbox state. Two-step: **create** (provisions sandbox, starts `idle`) → **send event** to start work. |
| **Event** | — | Bidirectional `{domain}.{action}` messages (`user.message`, `agent.tool_use`, `session.status_idle`). Streamed over SSE; each carries `processed_at`. |

## Agent configuration

- **Required:** `name`, `model` (Claude 4.5-family or later).
- **Optional:** `system`, `tools`, `mcp_servers`, `skills`, `multiagent`,
  `description`, `metadata`.
- **Versioning:** array fields (`tools`, `mcp_servers`, `skills`) are
  full-replacement — omit to preserve, `[]`/`null` to clear. `metadata` merges
  per-key. Sessions pin a version `{"type":"agent","id":"…","version":N}` or
  default to latest by string ID.

## Environment configuration

- `config.type`: `cloud` (Anthropic-managed) or `self_hosted`.
- Package managers run alphabetically: `apt`, `cargo`, `gem`, `go`, `npm`, `pip`;
  pinning supported (`pandas==2.2.0`, `express@4.18.0`).
- Networking: `unrestricted` (default, full outbound minus safety blocklist) or
  `limited` (only `allowed_hosts` bare hostnames / `*.wildcard`, plus MCP +
  package-manager toggles).

## Session lifecycle

- Statuses: `idle` (awaiting input) → `running` → `rescheduling` (transient) or
  `terminated` (unrecoverable).
- Checkpoints kept **30 days** after last activity; resume by sending a
  `user.message` (resets the timer).
- Resources at creation: `memory_store`, `file`, `repository`. File/repo
  updatable mid-session; memory stores attach **only at creation**.
- Token tracking: cumulative `input_tokens`, `output_tokens`,
  `cache_creation_input_tokens`, `cache_read_input_tokens` (5-min cache TTL).

## Tools & permissions

- **Prebuilt agent toolset:** `{"type":"agent_toolset_20260401"}` — `bash`,
  `read`, `write`, `edit`, `glob`, `grep`, `web_fetch`, `web_search`.
- **Custom tools:** client-executed `{"type":"custom",…}` with `input_schema`.
  Flow: `agent.custom_tool_use` → session idles `requires_action` → return
  `user.custom_tool_result`.
- **Permission policies:** `always_allow` (auto) / `always_ask` (pause for
  `user.tool_confirmation`). Convention: **agent toolset → `always_allow`, MCP
  toolset → `always_ask`** so new MCP tools can't run unapproved.

## Outcomes — the self-grading loop (Phase 3 grade→iterate)

- Send `user.define_outcome` with `description` (task), **required** `rubric`
  (markdown criteria), optional `max_iterations` (default 3, **max 20**).
- Grader is auto-provisioned in a **separate context window** (isolated from the
  agent's choices); returns pass/fail explanation fed back for the next iteration.
- Results: `satisfied`, `needs_revision`, `max_iterations_reached`, `failed`,
  `interrupted`. One outcome per session, but chainable after a terminal event.

## Memory stores (cross-session persistence)

- Workspace-scoped text collections surviving across sessions.
- Limits: **≤100 kB (~25k tokens) per store; ≤2,000 memories per store; ≤8 stores
  per session.**
- Attach at session creation: `{type:"memory_store", memory_store_id, access,
  instructions}`; access `read_write` (default) or `read_only`.
- Mounted at `/mnt/memory/`; writes sync back and mint immutable `memver_…`
  versions (30-day retention, no restore — re-write instead).
- ⚠️ `read_write` + untrusted input = prompt-injection can poison future sessions.

## Vaults & credentials

- Register third-party creds once, reference by `vault_ids` at session creation.
- Categories: `mcp_oauth` (Anthropic auto-refresh), `static_bearer`,
  `environment_variable` (substituted at egress; not visible to the agent).
- Limits: unique key per vault, keys immutable (archive+recreate), **≤20
  creds/vault.**

## Multi-agent sessions

- One **coordinator** delegates to a roster, each agent in its own context-isolated
  session **thread**; all threads share sandbox, filesystem, vault creds.
- Declare `multiagent:{type:"coordinator", agents:[…]}`.
- Limits: **depth 1 only; ≤20 unique agents; ≤25 concurrent threads.**

## Scheduled deployments — native cron (Phase 4 recurring loop)

- A **deployment** (`depl_…`) kicks off sessions on a recurring schedule.
- Create: `POST /v1/deployments` with `name`, `agent` (id or pinned version),
  `environment_id`, **`initial_events`** (must include `user.message`; can carry
  `user.define_outcome`), `schedule:{type:"cron", expression, timezone}`.
- Schedule: standard **5-field POSIX cron** (minute granularity); `timezone` =
  IANA id; **wall-clock DST** (literal local time; spring-forward nonexistent
  times skipped, fall-back times fire twice).
- Each firing → a session, tracked as a **deployment run** (`drun_…`).
- Lifecycle: pause / unpause / archive / manual `run` (immediate test).
- Limit: **1,000 deployments/org.**

## Rate limits & structural constraints

- API: 300 req/min (create), 600 req/min (read) per org.
- Outcome `max_iterations`: default 3, max 20.
- Skills: **20 per session.**
- Memory: 100 kB / memory, 2,000 / store, 8 stores / session.
- Multiagent: 20 roster, 25 threads, depth 1.
- Vault credentials: 20 per vault.
- Checkpoints: 30-day retention.

## Not eligible / notable

- Not eligible for Zero Data Retention or HIPAA BAA (stateful by design).
- `system.message` mid-session: Opus-4.8-only.
- No spend cap inside CMA — limits are workspace-level.
- MCP tunnels for private servers: limited research preview.

## Sources

1. Claude Managed Agents — Overview. https://platform.claude.com/docs/en/managed-agents/overview
2. anthropics/launch-your-agent — `cma-primitives.md`. https://github.com/anthropics/launch-your-agent
3. anthropics/launch-your-agent — `interview-to-config.md`.
4. Anthropic API reference — messages, tool use, streaming (SSE) conventions.
5. Anthropic engineering — "Building effective agents" (workflow vs autonomous loop framing).
6. Anthropic docs — Agent Skills authoring guide (SKILL.md contract the CMA skill primitive maps onto). https://code.claude.com/docs/en/skills
7. Model Context Protocol — specification (the connector/tool surface CMAs attach to). https://modelcontextprotocol.io/specification
