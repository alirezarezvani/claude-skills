---
name: "spec-driven-workflow"
description: "Use when the user asks to write specs before code, define acceptance criteria, plan features before implementation, generate tests from specifications, or follow spec-first development practices."
---

# Spec-Driven Workflow — POWERFUL

## Overview

Spec-driven workflow enforces a single, non-negotiable rule: **write the specification BEFORE you write any code.** Not alongside. Not after. Before.

This is not documentation. This is a contract. A spec defines what the system MUST do, what it SHOULD do, and what it explicitly WILL NOT do. Every line of code you write traces back to a requirement in the spec. Every test traces back to an acceptance criterion. If it is not in the spec, it does not get built.

### Why Spec-First Matters

1. **Eliminates rework.** 60-80% of defects originate from requirements, not implementation. Catching ambiguity in a spec costs minutes; catching it in production costs days.
2. **Forces clarity.** If you cannot write what the system should do in plain language, you do not understand the problem well enough to write code.
3. **Enables parallelism.** Once a spec is approved, frontend, backend, QA, and documentation can all start simultaneously.
4. **Creates accountability.** The spec is the definition of done. No arguments about whether a feature is "complete" — either it satisfies the acceptance criteria or it does not.
5. **Feeds TDD directly.** Acceptance criteria in Given/When/Then format translate 1:1 into test cases. The spec IS the test plan.

### The Iron Law

```
NO CODE WITHOUT AN APPROVED SPEC.
NO EXCEPTIONS. NO "QUICK PROTOTYPES." NO "I'LL DOCUMENT IT LATER."
```

If the spec is not written, reviewed, and approved, implementation does not begin. Period.

---

## The Spec Format

Every spec follows this structure. No sections are optional — if a section does not apply, write "N/A — [reason]" so reviewers know it was considered, not forgotten.

### 1. Title and Context

```markdown
# Spec: [Feature Name]

**Author:** [name]
**Date:** [ISO 8601]
**Status:** Draft | In Review | Approved | Superseded
**Reviewers:** [list]
**Related specs:** [links]

## Context

[Why does this feature exist? What problem does it solve? What is the business
motivation? Include links to user research, support tickets, or metrics that
justify this work. 2-4 paragraphs maximum.]
```

### 2. Functional Requirements (RFC 2119)

Use RFC 2119 keywords precisely:

| Keyword | Meaning |
|---------|---------|
| **MUST** | Absolute requirement. Failing this means the implementation is non-conformant. |
| **MUST NOT** | Absolute prohibition. Doing this means the implementation is broken. |
| **SHOULD** | Recommended. May be omitted with documented justification. |
| **SHOULD NOT** | Discouraged. May be included with documented justification. |
| **MAY** | Optional. Purely at the implementer's discretion. |

```markdown
## Functional Requirements

- FR-1: The system MUST authenticate users via OAuth 2.0 PKCE flow.
- FR-2: The system MUST reject tokens older than 24 hours.
- FR-3: The system SHOULD support refresh token rotation.
- FR-4: The system MAY cache user profiles for up to 5 minutes.
- FR-5: The system MUST NOT store plaintext passwords under any circumstance.
```

Number every requirement. Use `FR-` prefix. Each requirement is a single, testable statement.

### 3. Non-Functional Requirements

```markdown
## Non-Functional Requirements

### Performance
- NFR-P1: Login flow MUST complete in < 500ms (p95) under normal load.
- NFR-P2: Token validation MUST complete in < 50ms (p99).

### Security
- NFR-S1: All tokens MUST be transmitted over TLS 1.2+.
- NFR-S2: The system MUST rate-limit login attempts to 5/minute per IP.

### Accessibility
- NFR-A1: Login form MUST meet WCAG 2.1 AA standards.
- NFR-A2: Error messages MUST be announced to screen readers.

### Scalability
- NFR-SC1: The system SHOULD handle 10,000 concurrent sessions.

### Reliability
- NFR-R1: The authentication service MUST maintain 99.9% uptime.
```

### 4. Acceptance Criteria (Given/When/Then)

Every functional requirement maps to one or more acceptance criteria. Use Gherkin syntax:

```markdown
## Acceptance Criteria

### AC-1: Successful login (FR-1)
Given a user with valid credentials
When they submit the login form with correct email and password
Then they receive a valid access token
And they are redirected to the dashboard
And the login event is logged with timestamp and IP

### AC-2: Expired token rejection (FR-2)
Given a user with an access token issued 25 hours ago
When they make an API request with that token
Then they receive a 401 Unauthorized response
And the response body contains error code "TOKEN_EXPIRED"
And they are NOT redirected (API clients handle their own flow)

### AC-3: Rate limiting (NFR-S2)
Given an IP address that has made 5 failed login attempts in the last minute
When a 6th login attempt arrives from that IP
Then the request is rejected with 429 Too Many Requests
And the response includes a Retry-After header
```

### 5. Edge Cases and Error Scenarios

```markdown
## Edge Cases

- EC-1: User submits login form with empty email → Show validation error, do not hit API.
- EC-2: OAuth provider is down → Show "Service temporarily unavailable", retry after 30s.
- EC-3: User has account but no password (social-only) → Redirect to social login.
- EC-4: Concurrent login from two devices → Both sessions are valid (no single-session enforcement).
- EC-5: Token expires mid-request → Complete the current request, return warning header.
```

### 6. API Contracts

Define request/response shapes using TypeScript-style notation:

```markdown
## API Contracts

### POST /api/auth/login
Request:
```typescript
interface LoginRequest {
  email: string;       // MUST be valid email format
  password: string;    // MUST be 8-128 characters
  rememberMe?: boolean; // Default: false
}
```

Success Response (200):
```typescript
interface LoginResponse {
  accessToken: string;   // JWT, expires in 24h
  refreshToken: string;  // Opaque, expires in 30d
  expiresIn: number;     // Seconds until access token expires
  user: {
    id: string;
    email: string;
    displayName: string;
  };
}
```

Error Response (401):
```typescript
interface AuthError {
  error: "INVALID_CREDENTIALS" | "TOKEN_EXPIRED" | "ACCOUNT_LOCKED";
  message: string;
  retryAfter?: number; // Seconds, present for rate-limited responses
}
```
```

### 7. Data Models

```markdown
## Data Models

### User
| Field | Type | Constraints |
|-------|------|-------------|
| id | UUID | Primary key, auto-generated |
| email | string | Unique, max 255 chars, valid email format |
| passwordHash | string | bcrypt, never exposed via API |
| createdAt | timestamp | UTC, immutable |
| lastLoginAt | timestamp | UTC, updated on each login |
| loginAttempts | integer | Reset to 0 on successful login |
| lockedUntil | timestamp | Null if not locked |
```

### 8. Out of Scope

Explicit exclusions prevent scope creep:

```markdown
## Out of Scope

- OS-1: Multi-factor authentication (separate spec: SPEC-042)
- OS-2: Social login providers beyond Google and GitHub
- OS-3: Admin impersonation of user accounts
- OS-4: Password complexity rules beyond minimum length (deferred to v2)
- OS-5: Session management UI (users cannot see/revoke active sessions yet)
```

If someone asks for an out-of-scope item during implementation, point them to this section. Do not build it.

---

## Bounded Autonomy Rules

These rules define when an agent (human or AI) MUST stop and ask for guidance vs. when they can proceed independently.

### STOP and Ask When:

1. **Scope creep detected.** The implementation requires something not in the spec. Even if it seems obviously needed, STOP. The spec might have excluded it deliberately.

2. **Ambiguity exceeds 30%.** If you cannot determine the correct behavior from the spec for more than 30% of a given requirement, the spec is incomplete. Do not guess.

3. **Breaking changes required.** The implementation would change an existing API contract, database schema, or public interface. Always escalate.

4. **Security implications.** Any change that touches authentication, authorization, encryption, or PII handling requires explicit approval.

5. **Performance characteristics unknown.** If a requirement says "MUST complete in < 500ms" but you have no way to measure or guarantee that, escalate before implementing a guess.

6. **Cross-team dependencies.** If the spec requires coordination with another team or service, confirm the dependency before building against it.

### Continue Autonomously When:

1. **Spec is clear and unambiguous** for the current task.
2. **All acceptance criteria have passing tests** and you are refactoring internals.
3. **Changes are non-breaking** — no public API, schema, or behavior changes.
4. **Implementation is a direct translation** of a well-defined acceptance criterion.
5. **Error handling follows established patterns** already documented in the codebase.

### Escalation Protocol

When you must stop, provide:

```markdown
## Escalation: [Brief Title]

**Blocked on:** [requirement ID, e.g., FR-3]
**Question:** [Specific, answerable question — not "what should I do?"]
**Options considered:**
  A. [Option] — Pros: [...] Cons: [...]
  B. [Option] — Pros: [...] Cons: [...]
**My recommendation:** [A or B, with reasoning]
**Impact of waiting:** [What is blocked until this is resolved?]
```

Never escalate without a recommendation. Never present an open-ended question. Always give options.

See `references/bounded_autonomy_rules.md` for the complete decision matrix.

---

## Workflow — 6 Phases

### Phase 1: Gather Requirements

**Goal:** Understand what needs to be built and why.

1. **Interview the user.** Ask:
   - What problem does this solve?
   - Who are the users?
   - What does success look like?
   - What explicitly should NOT be built?
2. **Read existing code.** Understand the current system before proposing changes.
3. **Identify constraints.** Performance budgets, security requirements, backward compatibility.
4. **List unknowns.** Every unknown is a risk. Surface them now, not during implementation.

**Exit criteria:** You can explain the feature to someone unfamiliar with the project in 2 minutes.

### Phase 2: Write Spec

**Goal:** Produce a complete spec document following The Spec Format above.

1. Fill every section of the template. No section left blank.
2. Number all requirements (FR-*, NFR-*, AC-*, EC-*, OS-*).
3. Use RFC 2119 keywords precisely.
4. Write acceptance criteria in Given/When/Then format.
5. Define API contracts with TypeScript-style types.
6. List explicit exclusions in Out of Scope.

**Exit criteria:** The spec can be handed to a developer who was not in the requirements meeting, and they can implement the feature without asking clarifying questions.

### Phase 3: Validate Spec

**Goal:** Verify the spec is complete, consistent, and implementable.

Run `spec_validator.py` against the spec file:

```bash
python spec_validator.py --file spec.md --strict
```

Manual validation checklist:
- [ ] Every functional requirement has at least one acceptance criterion
- [ ] Every acceptance criterion is testable (no subjective language)
- [ ] API contracts cover all endpoints mentioned in requirements
- [ ] Data models cover all entities mentioned in requirements
- [ ] Edge cases cover failure modes for every external dependency
- [ ] Out of scope is explicit about what was considered and rejected
- [ ] Non-functional requirements have measurable thresholds

**Exit criteria:** Spec scores 80+ on validator, and all manual checklist items pass.

### Phase 4: Generate Tests

**Goal:** Extract test cases from acceptance criteria before writing implementation code.

Run `test_extractor.py` against the approved spec:

```bash
python test_extractor.py --file spec.md --framework pytest --output tests/
```

1. Each acceptance criterion becomes one or more test cases.
2. Each edge case becomes a test case.
3. Tests are stubs — they define the assertion but not the implementation.
4. All tests MUST fail initially (red phase of TDD).

**Exit criteria:** You have a test file where every test fails with "not implemented" or equivalent.

### Phase 5: Implement

**Goal:** Write code that makes failing tests pass, one acceptance criterion at a time.

1. Pick one acceptance criterion (start with the simplest).
2. Make its test(s) pass with minimal code.
3. Run the full test suite — no regressions.
4. Commit.
5. Pick the next acceptance criterion. Repeat.

**Rules:**
- Do NOT implement anything not in the spec.
- Do NOT optimize before all acceptance criteria pass.
- Do NOT refactor before all acceptance criteria pass.
- If you discover a missing requirement, STOP and update the spec first.

**Exit criteria:** All tests pass. All acceptance criteria satisfied.

### Phase 6: Self-Review

**Goal:** Verify implementation matches spec before marking done.

Run through the Self-Review Checklist below. If any item fails, fix it before declaring the task complete.

---

## Self-Review Checklist

Before marking any implementation as done, verify ALL of the following:

- [ ] **Every acceptance criterion has a passing test.** No exceptions. If AC-3 exists, a test for AC-3 exists and passes.
- [ ] **Every edge case has a test.** EC-1 through EC-N all have corresponding test cases.
- [ ] **No scope creep.** The implementation does not include features not in the spec. If you added something, either update the spec or remove it.
- [ ] **API contracts match implementation.** Request/response shapes in code match the spec exactly. Field names, types, status codes — all of it.
- [ ] **Error scenarios tested.** Every error response defined in the spec has a test that triggers it.
- [ ] **Non-functional requirements verified.** If the spec says < 500ms, you have evidence (benchmark, load test, profiling) that it meets the threshold.
- [ ] **Data model matches.** Database schema matches the spec. No extra columns, no missing constraints.
- [ ] **Out-of-scope items not built.** Double-check that nothing from the Out of Scope section leaked into the implementation.

---

## Integration with TDD Guide

Spec-driven workflow and TDD are complementary, not competing:

```
Spec-Driven Workflow          TDD (Red-Green-Refactor)
─────────────────────         ──────────────────────────
Phase 1: Gather Requirements
Phase 2: Write Spec
Phase 3: Validate Spec
Phase 4: Generate Tests  ──→  RED: Tests exist and fail
Phase 5: Implement       ──→  GREEN: Minimal code to pass
Phase 6: Self-Review     ──→  REFACTOR: Clean up internals
```

**The handoff:** Spec-driven workflow produces the test stubs (Phase 4). TDD takes over from there. The spec tells you WHAT to test. TDD tells you HOW to implement.

Use `engineering-team/tdd-guide` for:
- Red-green-refactor cycle discipline
- Coverage analysis and gap detection
- Framework-specific test patterns (Jest, Pytest, JUnit)

Use `engineering/spec-driven-workflow` for:
- Defining what to build before building it
- Acceptance criteria authoring
- Completeness validation
- Scope control

---

## Examples

### Full Spec: User Password Reset

```markdown
# Spec: Password Reset Flow

**Author:** Engineering Team
**Date:** 2026-03-25
**Status:** Approved

## Context

Users who forget their passwords currently have no self-service recovery option.
Support receives ~200 password reset requests per week, costing approximately
8 hours of support time. This feature eliminates that burden entirely.

## Functional Requirements

- FR-1: The system MUST allow users to request a password reset via email.
- FR-2: The system MUST send a reset link that expires after 1 hour.
- FR-3: The system MUST invalidate all previous reset links when a new one is requested.
- FR-4: The system MUST enforce minimum password length of 8 characters on reset.
- FR-5: The system MUST NOT reveal whether an email exists in the system.
- FR-6: The system SHOULD log all reset attempts for audit purposes.

## Acceptance Criteria

### AC-1: Request reset (FR-1, FR-5)
Given a user on the password reset page
When they enter any email address and submit
Then they see "If an account exists, a reset link has been sent"
And the response is identical whether the email exists or not

### AC-2: Valid reset link (FR-2)
Given a user who received a reset email 30 minutes ago
When they click the reset link
Then they see the password reset form

### AC-3: Expired reset link (FR-2)
Given a user who received a reset email 2 hours ago
When they click the reset link
Then they see "This link has expired. Please request a new one."

### AC-4: Previous links invalidated (FR-3)
Given a user who requested two reset emails
When they click the link from the first email
Then they see "This link is no longer valid."

## Edge Cases

- EC-1: User submits reset for non-existent email → Same success message (FR-5).
- EC-2: User clicks reset link twice → Second click shows "already used" if password was changed.
- EC-3: Email delivery fails → Log error, do not retry automatically.
- EC-4: User requests reset while already logged in → Allow it, do not force logout.

## Out of Scope

- OS-1: Security questions as alternative reset method.
- OS-2: SMS-based password reset.
- OS-3: Admin-initiated password reset (separate spec).
```

### Extracted Test Cases (from above spec)

```python
# Generated by test_extractor.py --framework pytest

class TestPasswordReset:
    def test_ac1_request_reset_existing_email(self):
        """AC-1: Request reset with existing email shows generic message."""
        # Given a user on the password reset page
        # When they enter a registered email and submit
        # Then they see "If an account exists, a reset link has been sent"
        raise NotImplementedError("Implement this test")

    def test_ac1_request_reset_nonexistent_email(self):
        """AC-1: Request reset with unknown email shows same generic message."""
        # Given a user on the password reset page
        # When they enter an unregistered email and submit
        # Then they see identical response to existing email case
        raise NotImplementedError("Implement this test")

    def test_ac2_valid_reset_link(self):
        """AC-2: Reset link works within expiry window."""
        raise NotImplementedError("Implement this test")

    def test_ac3_expired_reset_link(self):
        """AC-3: Reset link rejected after 1 hour."""
        raise NotImplementedError("Implement this test")

    def test_ac4_previous_links_invalidated(self):
        """AC-4: Old reset links stop working when new one is requested."""
        raise NotImplementedError("Implement this test")

    def test_ec1_nonexistent_email_same_response(self):
        """EC-1: Non-existent email produces identical response."""
        raise NotImplementedError("Implement this test")

    def test_ec2_reset_link_used_twice(self):
        """EC-2: Already-used reset link shows appropriate message."""
        raise NotImplementedError("Implement this test")
```

---

## Anti-Patterns

### 1. Coding Before Spec Approval

**Symptom:** "I'll start coding while the spec is being reviewed."
**Problem:** The review will surface changes. Now you have code that implements a rejected design.
**Rule:** Implementation does not begin until spec status is "Approved."

### 2. Vague Acceptance Criteria

**Symptom:** "The system should work well" or "The UI should be responsive."
**Problem:** Untestable. What does "well" mean? What does "responsive" mean?
**Rule:** Every acceptance criterion must be verifiable by a machine. If you cannot write a test for it, rewrite the criterion.

### 3. Missing Edge Cases

**Symptom:** Happy path is specified, error paths are not.
**Problem:** Developers invent error handling on the fly, leading to inconsistent behavior.
**Rule:** For every external dependency (API, database, file system, user input), specify at least one failure scenario.

### 4. Spec as Post-Hoc Documentation

**Symptom:** "Let me write the spec now that the feature is done."
**Problem:** This is documentation, not specification. It describes what was built, not what should have been built. It cannot catch design errors because the design is already frozen.
**Rule:** If the spec was written after the code, it is not a spec. Relabel it as documentation.

### 5. Gold-Plating Beyond Spec

**Symptom:** "While I was in there, I also added..."
**Problem:** Untested code. Unreviewed design. Potential for subtle bugs in the "bonus" feature.
**Rule:** If it is not in the spec, it does not get built. File a new spec for additional features.

### 6. Acceptance Criteria Without Requirement Traceability

**Symptom:** AC-7 exists but does not reference any FR-* or NFR-*.
**Problem:** Orphaned criteria mean either a requirement is missing or the criterion is unnecessary.
**Rule:** Every AC-* MUST reference at least one FR-* or NFR-*.

### 7. Skipping Validation

**Symptom:** "The spec looks fine, let's just start."
**Problem:** Missing sections discovered during implementation cause blocking delays.
**Rule:** Always run `spec_validator.py --strict` before starting implementation. Fix all warnings.

---

## Cross-References

- **`engineering-team/tdd-guide`** — Red-green-refactor cycle, test generation, coverage analysis. Use after Phase 4 of this workflow.
- **`engineering/focused-fix`** — Deep-dive feature repair. When a spec-driven implementation has systemic issues, use focused-fix for diagnosis.
- **`engineering/rag-architect`** — If the feature involves retrieval or knowledge systems, use rag-architect for the technical design within the spec.
- **`references/spec_format_guide.md`** — Complete template with section-by-section explanations.
- **`references/bounded_autonomy_rules.md`** — Full decision matrix for when to stop vs. continue.
- **`references/acceptance_criteria_patterns.md`** — Pattern library for writing Given/When/Then criteria.

---

## Tools

| Script | Purpose | Key Flags |
|--------|---------|-----------|
| `spec_generator.py` | Generate spec template from feature name/description | `--name`, `--description`, `--format`, `--json` |
| `spec_validator.py` | Validate spec completeness (0-100 score) | `--file`, `--strict`, `--json` |
| `test_extractor.py` | Extract test stubs from acceptance criteria | `--file`, `--framework`, `--output`, `--json` |

```bash
# Generate a spec template
python spec_generator.py --name "User Authentication" --description "OAuth 2.0 login flow"

# Validate a spec
python spec_validator.py --file specs/auth.md --strict

# Extract test cases
python test_extractor.py --file specs/auth.md --framework pytest --output tests/test_auth.py
```
