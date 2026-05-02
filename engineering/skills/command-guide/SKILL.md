---
name: "command-guide"
description: >
  Claude Code Command Selection Guide - Automatically recommend and select the right
  commands, agents, and skills in Claude Code.
  Use when: (1) user is unsure which command or tool to use, (2) needs to decide which
  agent/skill best fits the current task, (3) querying usage scenarios for /plan, /tdd,
  /compact, /loop and other commands, (4) understanding when to invoke planner,
  code-reviewer, build-error-resolver and other agents, (5) needs command cheat sheet
  or decision flowchart.
  Triggers: "which command to use", "which agent", "command selection", "how to use /plan",
  "when to use /compact", "agent selection guide", "command cheat sheet", "skill recommendation".
---

# Claude Code Command Selection Guide

This skill helps you choose the most appropriate command, agent, or skill for different scenarios.

## Quick Decision Flowchart

```mermaid
graph TD
    A[User Request] --> B{Request Type?}
    B -->|New Feature| C[/plan]
    B -->|Bug Fix| D[/tdd or build-error-resolver]
    B -->|Code Review| E[/code-review or code-reviewer agent]
    B -->|Testing| F[/e2e or tdd-guide agent]
    B -->|Context Too Long| G[/compact]
    B -->|Documentation| H[/docs or docs-lookup agent]
    B -->|Looping Task| I[/loop]
    B -->|Security Review| J[security-reviewer agent]

    C --> K[planner agent]
    D --> L{Build Failed?}
    L -->|Yes| M[build-error-resolver]
    L -->|No| N[tdd-guide]
    E --> O[code-reviewer]
    F --> P[e2e-runner]
```

## 1. Built-in Slash Commands

### Session Management Commands

| Command | Use Case | Example |
|---------|----------|---------|
| `/compact` | Context too long (>150K tokens), slow response, task phase transition | `/compact` or auto-trigger |
| `/clear` | Start fresh conversation, clear history | `/clear` |
| `/loop` | Periodic task execution, automated looping work | `/loop 5m check build status` |
| `/help` | View help, learn commands | `/help` |
| `/fast` | Need faster response (Opus 4.6 only) | `/fast` |
| `/model` | Switch model | `/model sonnet` |

### Development Workflow Commands

| Command | Use Case | Activation Timing |
|---------|----------|-------------------|
| `/plan` | Start new feature, architecture refactor, complex tasks | **Enter Plan Mode** |
| `/tdd` | Write tests, TDD development workflow | When test guidance needed |
| `/e2e` | E2E testing, critical user flow verification | When browser testing needed |
| `/code-review` | Code quality review | After writing code |
| `/build-fix` | Build failure, type errors | When build fails |
| `/learn` | Extract patterns from session, learning | Before session ends |
| `/skill-create` | Create new skill from git history | When repeating patterns found |

### Documentation & Query Commands

| Command | Use Case | Example |
|---------|----------|---------|
| `/docs` | Update project documentation | `/docs` |
| `/update-codemaps` | Update code maps | `/update-codemaps` |
| `/remember` | Save memory to memory system | `/remember user prefers concise output` |
| `/tasks` | View task list | `/tasks` |

---

## 2. Agents Selection

### Development Workflow Agents

| Agent | Trigger Condition | Purpose |
|-------|-------------------|---------|
| `planner` | Complex feature request, architectural decision | Create implementation plan |
| `architect` | System design, tech stack selection | Architecture analysis and decisions |
| `tdd-guide` | New feature, bug fix | TDD workflow guidance |
| `code-reviewer` | **Invoke immediately after writing code** | Code quality review |
| `security-reviewer` | Handling auth, API, sensitive data | Security vulnerability detection |

### Problem Solving Agents

| Agent | Trigger Condition | Purpose |
|-------|-------------------|---------|
| `build-error-resolver` | **Invoke immediately when build fails** | Fix build/type errors |
| `e2e-runner` | Critical user flows, before PR | E2E test execution |
| `refactor-cleaner` | Code maintenance, dead code cleanup | Dead code detection and cleanup |
| `doc-updater` | Update docs, codemaps | Documentation sync |

### Research & Exploration Agents

| Agent | Trigger Condition | Purpose |
|-------|-------------------|---------|
| `Explore` | Codebase exploration, file finding | Quick codebase exploration |
| `general-purpose` | Complex multi-step tasks | General task handling |
| `docs-lookup` | Query library/framework docs | Get latest API documentation |

---

## 3. Skills Selection

### Workflow Skills

| Skill | Trigger Timing | Purpose |
|-------|----------------|---------|
| `tdd-workflow` | Developing new feature/fixing bug | Complete TDD workflow guidance |
| `verification-loop` | After feature completion, before PR | Comprehensive verification (build/test/lint/security) |
| `strategic-compact` | Long session, context pressure | Guide when to manually `/compact` |

### Architecture & Pattern Skills

| Skill | Trigger Timing | Purpose |
|-------|----------------|---------|
| `frontend-patterns` | Frontend development | React/Next.js/Vue best practices |
| `backend-patterns` | Backend development | API/service architecture patterns |
| `api-design` | API design | RESTful/API design standards |
| `mcp-server-patterns` | MCP server development | MCP configuration and patterns |

### Testing Skills

| Skill | Trigger Timing | Purpose |
|-------|----------------|---------|
| `e2e-testing` | E2E testing needs | Playwright test generation |
| `security-review` | Security review needs | OWASP Top 10 detection |

### Research Skills

| Skill | Trigger Timing | Purpose |
|-------|----------------|---------|
| `deep-research` | Need deep research | Multi-round search and research |
| `exa-search` | Need web search | Web content search |
| `documentation-lookup` | Query library docs | Context7 documentation query |

---

## 4. Scenario Decision Matrix

### By Task Phase

| Phase | Recommended Tool Combination | Reason |
|-------|------------------------------|--------|
| **Requirements Analysis** | `planner` + `Explore` | Plan first, explore later |
| **Architecture Design** | `architect` + `api-design` skill | Professional architecture guidance |
| **Pre-Development** | `tdd-guide` + `tdd-workflow` skill | Test first |
| **During Development** | Direct edit + quick iteration | Stay in flow |
| **Post-Development** | `code-reviewer` + `verification-loop` | Quality gate |
| **Testing Phase** | `e2e-runner` + `e2e-testing` skill | Complete test coverage |
| **Before PR** | `security-reviewer` + `verification-loop` | Final verification |
| **Build Failure** | `build-error-resolver` | Focused fix |

### By Problem Type

| Problem | Invoke Immediately | Note |
|---------|--------------------|------|
| Build failure | `build-error-resolver` | Minimal changes, quick fix |
| Type error | `build-error-resolver` | TypeScript specialist |
| Bug fix | `tdd-guide` | Write test then fix |
| Security vulnerability | `security-reviewer` | OWASP detection |
| Poor code quality | `code-reviewer` | Immediate review |
| Missing documentation | `doc-updater` | Auto update |
| Dead code | `refactor-cleaner` | Safe cleanup |

### By Development Type

| Development Type | Skills Combination |
|------------------|--------------------|
| Frontend feature | `frontend-patterns` + `tdd-workflow` |
| Backend API | `backend-patterns` + `api-design` + `tdd-workflow` |
| MCP server | `mcp-server-patterns` + `tdd-workflow` |
| Database | `database-reviewer` agent |
| Security feature | `security-reviewer` + `security-review` skill |

---

## 5. Parallel Execution Strategy

### Parallelizable Scenarios

Recommended: Launch multiple independent tasks simultaneously

Scenario: Preparing PR after code completion
- Agent 1: code-reviewer (code quality)
- Agent 2: security-reviewer (security review)
- Agent 3: e2e-runner (E2E tests)

Scenario: Large refactor analysis
- Agent 1: architect (architecture analysis)
- Agent 2: Explore (code exploration)
- Agent 3: refactor-cleaner (dead code detection)

### Sequential Execution Required

Cannot parallelize: Dependencies exist

Scenario: Fixing build error
- Sequence: build-error-resolver -> test verification -> code-reviewer

Scenario: New feature development
- Sequence: planner -> tdd-guide (write tests) -> implementation -> code-reviewer

---

## 6. Auto-Trigger Rules

### Invoke Without User Request

| Situation | Auto Action |
|-----------|-------------|
| Code written/modified | **Immediately invoke** `code-reviewer` |
| Build fails | **Immediately invoke** `build-error-resolver` |
| Complex feature request | **Immediately invoke** `planner` |
| Handling auth/sensitive data | **Immediately invoke** `security-reviewer` |
| New feature/bug fix | **Immediately invoke** `tdd-guide` |
| Architectural decision | **Immediately invoke** `architect` |

---

## 7. Context Management Timing

| Indicator | Trigger `/compact` |
|-----------|-------------------|
| Token > 150K | Immediately compact |
| Slow response | Suggest compact |
| Task phase switch | Compact at boundary |
| Major milestone completed | Compact then continue |
| Debugging ends -> new task | Clear debug traces |

**Best Practices**:
- Compact after research, before implementation (preserve plan)
- Compact after milestone completion (clear intermediate state)
- Don't compact mid-implementation (lose variables/paths)

---

## 8. Command Cheat Sheet

```
Development Workflow:
/plan        -> Enter planning mode (complex tasks)
/tdd         -> TDD workflow
/e2e         -> E2E testing
/code-review -> Code review
/build-fix   -> Fix build

Session Management:
/compact     -> Compact context
/clear       -> Clear session
/loop        -> Looping task
/fast        -> Fast mode

Documentation & Memory:
/docs        -> Update docs
/remember    -> Save memory
/tasks       -> View tasks

Help:
/help        -> View all commands
```

---

## 9. Usage Examples

### Example 1: New Feature Development

User: Add user authentication feature

Workflow:
1. /plan -> planner agent creates plan
2. tdd-guide -> write tests
3. Implementation -> edit code
4. code-reviewer -> code review
5. security-reviewer -> security review (auth sensitive)
6. e2e-runner -> E2E tests
7. /compact -> compact after milestone completion

### Example 2: Build Failure

User: npm run build failed

Workflow:
1. build-error-resolver -> analyze error, minimal fix
2. Verify build success
3. code-reviewer -> check fix quality

### Example 3: Code Refactoring

User: Refactor authentication module

Workflow:
1. architect -> architecture analysis
2. planner -> implementation plan
3. refactor-cleaner -> dead code detection
4. tdd-guide -> ensure test coverage
5. Implementation -> refactor code
6. verification-loop -> comprehensive verification

---

**Core Principles**:
1. **Plan first, implement later** - Use `/plan` for complex tasks
2. **Test first** - Use `tdd-guide` for new features
3. **Review immediately after coding** - Use `code-reviewer` when code complete
4. **Fix build immediately when failed** - Use `build-error-resolver`
5. **Review sensitive code** - Use `security-reviewer` for auth/API
6. **Verify comprehensively before PR** - Use `verification-loop`
