---
name: testing-best-practices
description: "Use when users ask about testing strategies, unit tests, integration tests, test coverage, test-driven development (TDD), mocking, test patterns, or improving code testability. Triggers: 'how to test', 'write tests for', 'improve test coverage', 'testing strategy', 'mock this', 'test this function'."
license: MIT
metadata:
  version: 1.0.0
  author: xingzihai
  category: engineering
  updated: 2026-03-25
---

# Testing Best Practices

**Tier:** POWERFUL
**Category:** Engineering Quality
**Domain:** Software Testing / Quality Assurance

---

## Overview

You are an expert in software testing. Your goal is to help teams write tests that actually catch bugs, provide confidence for refactoring, and document system behavior — not tests that just increase coverage metrics.

Good tests are an investment. Bad tests are a liability. This skill helps you write the former.

---

## Before Starting

**Check for context first:**
If `project-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. Current State
- What testing framework(s) are you using? (Jest, pytest, Go testing, etc.)
- What's your current test coverage percentage?
- What types of tests exist? (unit, integration, e2e)

### 2. Goals
- What problem are you trying to solve? (better coverage, faster tests, more reliable tests)
- What's the critical path that needs testing?
- Are there flaky tests causing issues?

### 3. Testing Constraints
- What's the test execution time budget?
- Are there any CI/CD pipeline constraints?
- What mocking libraries are available?

---

## How This Skill Works

### Mode 1: Build Test Suite from Scratch
When starting with minimal or no tests — establish foundations.

### Mode 2: Improve Existing Tests
When tests exist but have issues (flaky, slow, low coverage). Analyze → identify gaps → recommend fixes.

### Mode 3: Test-Driven Development (TDD)
When writing tests before implementation. Design the interface through tests first.

---

## Testing Pyramid

The testing pyramid is your guide to test distribution:

```
        /\
       /  \    E2E Tests (10%)
      /----\   - Slow, expensive, realistic
     /      \  
    /--------\ Integration Tests (20%)
   /          \ - Medium speed, test interactions
  /            \
 /--------------\ Unit Tests (70%)
/                \ - Fast, isolated, numerous
```

| Test Type | Speed | Scope | When to Use |
|-----------|-------|-------|-------------|
| **Unit** | ms | Single function/class | Business logic, edge cases |
| **Integration** | seconds | Multiple components | API calls, DB interactions, services |
| **E2E** | minutes | Full system | Critical user journeys, smoke tests |

**Rules:**
- 70% unit, 20% integration, 10% E2E
- If integration tests are slow, add more unit tests
- If unit tests are complex, you're testing too much at once

---

## Core Principles

### 1. Tests Should Fail for One Reason

Each test should verify one specific behavior. If a test fails, you should immediately know what's broken.

```python
# Bad: Testing multiple things
def test_user_creation():
    user = create_user("test@example.com")
    assert user.email == "test@example.com"
    assert user.is_active == True
    assert user.role == "user"
    assert send_welcome_email.called

# Good: One assertion per test concept
def test_user_creation_sets_email():
    user = create_user("test@example.com")
    assert user.email == "test@example.com"

def test_new_users_are_active_by_default():
    user = create_user("test@example.com")
    assert user.is_active == True
```

### 2. Tests Should Be Independent

No test should depend on another test's outcome. Each test sets up its own world.

```javascript
// Bad: Shared state
let user;
beforeAll(() => { user = createUser(); });

test('user has email', () => {
  expect(user.email).toBeDefined();
});

// Good: Isolated state
beforeEach(() => {
  user = createUser(); // Fresh for each test
});
```

### 3. Tests Should Be Deterministic

Same input, same output — every time. No randomness, no time dependencies, no network calls.

```python
# Bad: Time-dependent
def test_expiration():
    token = create_token()
    time.sleep(2)  # Flaky!
    assert token.is_expired()

# Good: Control time
def test_expiration(freezer):
    freezer.move_to("2024-01-01 12:00:00")
    token = create_token()
    freezer.move_to("2024-01-01 12:01:00")
    assert token.is_expired()
```

### 4. Test Behavior, Not Implementation

Tests should verify WHAT the code does, not HOW it does it. Implementation changes shouldn't break tests.

```python
# Bad: Testing implementation
def test_sort_uses_quicksort():
    sorter = Sorter()
    assert sorter._algorithm == "quicksort"

# Good: Testing behavior
def test_sort_returns_ordered_list():
    result = sort([3, 1, 2])
    assert result == [1, 2, 3]
```

---

## Test Naming Convention

Test names should read like documentation. When they fail, the name tells you what's broken.

**Pattern:** `test_<method>_<scenario>_<expected_result>`

```python
# Good examples
test_create_user_with_valid_email_returns_user_object()
test_create_user_with_invalid_email_raises_validation_error()
test_create_user_with_duplicate_email_raises_conflict_error()
test_delete_user_when_not_found_raises_not_found_error()
test_calculate_discount_with_vip_member_applies_20_percent()
```

**JavaScript/Jest style:**
```javascript
describe('UserService', () => {
  describe('createUser', () => {
    it('should return user object when email is valid', () => {})
    it('should raise ValidationError when email is invalid', () => {})
    it('should raise ConflictError when email already exists', () => {})
  })
})
```

---

## Mocking Strategies

### What to Mock

| Mock It | Don't Mock It |
|---------|---------------|
| External APIs | Internal business logic |
| Database (in unit tests) | Value objects |
| File system | Pure functions |
| Time | Data transformations |
| Network calls | In-memory data structures |

### Mocking Patterns

```python
# Python (unittest.mock)
from unittest.mock import Mock, patch, MagicMock

# Mock a function
with patch('module.external_api_call') as mock_api:
    mock_api.return_value = {"status": "success"}
    result = my_function()

# Verify it was called
mock_api.assert_called_once_with(expected_params)

# JavaScript (Jest)
jest.mock('./api');
api.fetchUser.mockResolvedValue({ id: 1, name: 'Test' });

// Verify
expect(api.fetchUser).toHaveBeenCalledWith(expectedId);
```

### Mocking Anti-Patterns

```python
# Bad: Over-mocking (testing mocks, not code)
def test_process_order():
    with patch('module.get_order') as mock_get, \
         patch('module.validate') as mock_val, \
         patch('module.save') as mock_save, \
         patch('module.notify') as mock_notify:
        # This test verifies nothing about real behavior
        process_order(1)
        mock_save.assert_called()  # Just verifying mocks work
```

---

## Test Coverage Guidelines

### What Coverage Means

| Coverage % | Meaning |
|------------|---------|
| < 50% | Critical gaps, high risk |
| 50-70% | Basic coverage, missing edge cases |
| 70-85% | Good coverage, well-tested codebase |
| 85-95% | Excellent, diminishing returns |
| > 95% | May indicate over-testing, brittle tests |

### Coverage Targets by Code Type

| Code Type | Target Coverage |
|-----------|-----------------|
| Business logic | 90%+ |
| API endpoints | 85%+ |
| UI components | 70%+ |
| Utilities/helpers | 95%+ |
| Configuration | 50% |
| Generated code | Skip |

### Coverage Commands

```bash
# Python (pytest)
pytest --cov=src --cov-report=html --cov-report=term

# JavaScript (Jest)
jest --coverage --coverageThreshold='{"global":{"branches":80,"functions":80,"lines":80}}'

# Go
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

---

## Edge Cases to Test

Always test these scenarios:

### Input Validation
- Empty/null/undefined values
- Maximum length strings
- Negative numbers when positive expected
- Zero values
- Unicode and special characters

### Boundary Conditions
- Off-by-one errors
- Integer overflow
- Empty collections
- Single item collections

### Error Paths
- Network timeouts
- Invalid responses
- Permission denied
- Resource not found
- Rate limiting

### Concurrency (where applicable)
- Race conditions
- Deadlocks
- Resource contention

---

## Testing Checklist

```markdown
## Test Quality Checklist

### Structure
- [ ] Test name describes the scenario and expected outcome
- [ ] Test is independent (no shared mutable state)
- [ ] Test has clear arrange/act/assert sections
- [ ] Test is in the right layer (unit/integration/e2e)

### Coverage
- [ ] Happy path is tested
- [ ] Edge cases are tested (empty, null, max, min)
- [ ] Error paths are tested
- [ ] No unreachable code in the tested module

### Reliability
- [ ] No hardcoded waits or sleeps
- [ ] No time-dependent logic without time control
- [ ] No network calls in unit tests
- [ ] No file system dependencies without mocking

### Maintainability
- [ ] Test code is as clean as production code
- [ ] No magic numbers without explanation
- [ ] Helper functions for common setup
- [ ] No copy-pasted test logic
```

---

## Proactive Triggers

Surface these without being asked:

- **Test file has no corresponding source file** → orphan test, may indicate deleted code
- **Test file is 10x larger than source file** → over-testing, consider refactoring
- **All tests in a file have identical setup** → extract to beforeEach/beforeAll
- **Tests using `time.sleep()` or `wait()` → flaky test risk, use time mocking
- **Coverage below 50% on business logic** → critical testing gap
- **Tests with 50+ lines of setup** → test is doing too much, split it

---

## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| "Write tests for this function" | Complete test file with unit tests for happy path, edge cases, and error handling |
| "Improve test coverage" | Coverage analysis with prioritized test recommendations and code snippets |
| "Fix flaky tests" | Root cause analysis and refactored test code with proper mocking/time control |
| "Design test strategy" | Testing pyramid plan with coverage targets and framework recommendations |
| "Review my tests" | Test quality scorecard (0-100) with specific improvement suggestions |

---

## Common Pitfalls

### 1. Testing for Coverage, Not Confidence
**Problem**: Writing tests that pass but don't verify behavior.
**Solution**: Each test should fail if the behavior it tests is broken.

### 2. Over-Mocking
**Problem**: Tests verify mocks, not actual behavior.
**Solution**: Mock at boundaries (APIs, DB), not internal logic.

### 3. Giant Test Functions
**Problem**: One test doing 10 assertions, hard to debug when it fails.
**Solution**: One concept per test, use describe blocks for grouping.

### 4. Ignoring Test Speed
**Problem**: Tests take 10+ minutes, so developers skip running them.
**Solution**: Parallelize, move slow tests to integration suite, mock external calls.

### 5. Flaky Tests from Shared State
**Problem**: Tests pass sometimes, fail other times.
**Solution**: Reset state in beforeEach/afterEach, never share mutable state.

---

## Communication

All output follows the structured communication standard:
- **Bottom line first** — recommendation before explanation
- **What + Why + How** — every finding has all three
- **Confidence tagging** — 🟢 verified / 🟡 medium / 🔴 assumed

---

## Related Skills

- **pr-review-expert**: For reviewing pull requests including test changes. Use when reviewing PRs with test modifications.
- **tech-debt-tracker**: For tracking test-related technical debt. Use when planning test improvement initiatives.
- **ci-cd-pipeline-builder**: For setting up test automation in CI/CD. Use when integrating tests into pipelines.
- **codebase-onboarding**: For understanding existing test patterns in a new codebase. Use when joining a new project.
- **skill-tester**: For testing Claude skills themselves. NOT for general code testing.