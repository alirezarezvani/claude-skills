---
name: tdd-guide
description: Comprehensive Test Driven Development guide for engineering subagents with multi-framework support, coverage analysis, and intelligent test generation
---

# TDD Guide - Test Driven Development for Engineering Teams

A comprehensive Test Driven Development skill that provides intelligent test generation, coverage analysis, framework integration, and TDD workflow guidance across multiple languages and testing frameworks.

## Capabilities

### Test Generation
- **Generate Test Cases from Requirements**: Convert user stories, API specs, and business requirements into executable test cases
- **Create Test Stubs**: Generate test function scaffolding with proper naming, imports, and setup/teardown
- **Generate Test Fixtures**: Create realistic test data, mocks, and fixtures for various scenarios

### TDD Workflow Support
- **Guide Red-Green-Refactor**: Step-by-step guidance through TDD cycles with validation
- **Suggest Missing Scenarios**: Identify untested edge cases, error conditions, and boundary scenarios
- **Review Test Quality**: Analyze test isolation, assertions quality, naming conventions, and maintainability

### Coverage & Metrics Analysis
- **Calculate Coverage**: Parse LCOV, JSON, and XML coverage reports for line/branch/function coverage
- **Identify Untested Paths**: Find code paths, branches, and error handlers without test coverage
- **Recommend Improvements**: Prioritized recommendations (P0/P1/P2) for coverage gaps and test quality

### Framework Integration
- **Multi-Framework Support**: Jest, Pytest, JUnit, Vitest, Mocha, RSpec adapters
- **Generate Boilerplate**: Create test files with proper imports, describe blocks, and best practices
- **Configure Test Runners**: Set up test configuration, coverage tools, and CI integration

### Comprehensive Metrics
- **Test Coverage**: Line, branch, function coverage with gap analysis
- **Code Complexity**: Cyclomatic complexity, cognitive complexity, testability scoring
- **Test Quality**: Assertions per test, isolation score, naming quality, test smell detection
- **Test Data**: Boundary value analysis, edge case identification, mock data generation
- **Test Execution**: Timing analysis, slow test detection, flakiness detection
- **Missing Tests**: Uncovered edge cases, error handling gaps, missing integration scenarios

## Input Requirements

The skill supports **automatic format detection** for flexible input:

### Source Code
- **Languages**: TypeScript, JavaScript, Python, Java
- **Format**: Direct file paths or copy-pasted code blocks
- **Detection**: Automatic language/framework detection from syntax and imports

### Test Artifacts
- **Coverage Reports**: LCOV (.lcov), JSON (coverage-final.json), XML (cobertura.xml)
- **Test Results**: JUnit XML, Jest JSON, Pytest JSON, TAP format
- **Format**: File paths or raw coverage data

### Requirements (Optional)
- **User Stories**: Text descriptions of functionality
- **API Specifications**: OpenAPI/Swagger, REST endpoints, GraphQL schemas
- **Business Requirements**: Acceptance criteria, business rules

### Input Methods
- **Option A**: Provide file paths (skill will read files)
- **Option B**: Copy-paste code/data directly
- **Option C**: Mix of both (automatically detected)

## Output Formats

The skill provides **context-aware output** optimized for your environment:

### Code Files
- **Test Files**: Generated tests (Jest/Pytest/JUnit/Vitest) with proper structure
- **Fixtures**: Test data files, mock objects, factory functions
- **Mocks**: Mock implementations, stub functions, test doubles

### Reports
- **Markdown**: Rich coverage reports, recommendations, quality analysis (Claude Desktop)
- **JSON**: Machine-readable metrics, structured data for CI/CD integration
- **Terminal-Friendly**: Simplified output for Claude Code CLI

### Smart Defaults
- **Desktop/Apps**: Rich markdown with tables, code blocks, visual hierarchy
- **CLI**: Concise, terminal-friendly format with clear sections
- **CI/CD**: JSON output for automated processing

### Progressive Disclosure
- **Summary First**: High-level overview (<200 tokens)
- **Details on Demand**: Full analysis available (500-1000 tokens)
- **Prioritized**: P0 (critical) → P1 (important) → P2 (nice-to-have)

## How to Use

### Basic Usage
```
@tdd-guide

I need tests for my authentication module. Here's the code:
[paste code or provide file path]

Generate comprehensive test cases covering happy path, error cases, and edge cases.
```

### Coverage Analysis
```
@tdd-guide

Analyze test coverage for my TypeScript project. Coverage report: coverage/lcov.info

Identify gaps and provide prioritized recommendations.
```

### TDD Workflow
```
@tdd-guide

Guide me through TDD for implementing a password validation function.

Requirements:
- Min 8 characters
- At least 1 uppercase, 1 lowercase, 1 number, 1 special char
- No common passwords
```

### Multi-Framework Support
```
@tdd-guide

Convert these Jest tests to Pytest format:
[paste Jest tests]
```

## Scripts

### Core Modules

- **test_generator.py**: Intelligent test case generation from requirements and code
- **coverage_analyzer.py**: Parse and analyze coverage reports (LCOV, JSON, XML)
- **metrics_calculator.py**: Calculate comprehensive test and code quality metrics
- **framework_adapter.py**: Multi-framework adapter (Jest, Pytest, JUnit, Vitest)
- **tdd_workflow.py**: Red-green-refactor workflow guidance and validation
- **fixture_generator.py**: Generate realistic test data and fixtures
- **format_detector.py**: Automatic language and framework detection

### Utilities

- **complexity_analyzer.py**: Cyclomatic and cognitive complexity analysis
- **test_quality_scorer.py**: Test quality scoring (isolation, assertions, naming)
- **missing_test_detector.py**: Identify untested paths and missing scenarios
- **output_formatter.py**: Context-aware output formatting (Desktop vs CLI)

## Best Practices

### Test Generation
1. **Start with Requirements**: Write tests from user stories before seeing implementation
2. **Test Behavior, Not Implementation**: Focus on what code does, not how it does it
3. **One Assertion Focus**: Each test should verify one specific behavior
4. **Descriptive Names**: Test names should read like specifications

### TDD Workflow
1. **Red**: Write failing test first
2. **Green**: Write minimal code to make it pass
3. **Refactor**: Improve code while keeping tests green
4. **Repeat**: Small iterations, frequent commits

### Coverage Goals
1. **Aim for 80%+**: Line coverage baseline for most projects
2. **100% Critical Paths**: Authentication, payments, data validation must be fully covered
3. **Branch Coverage Matters**: Line coverage alone is insufficient
4. **Don't Game Metrics**: Focus on meaningful tests, not coverage numbers

### Test Quality
1. **Independent Tests**: Each test should run in isolation
2. **Fast Execution**: Keep unit tests under 100ms each
3. **Deterministic**: Tests should always produce same results
4. **Clear Failures**: Assertion messages should explain what went wrong

### Framework Selection
1. **Jest**: JavaScript/TypeScript projects (React, Node.js)
2. **Pytest**: Python projects (Django, Flask, FastAPI)
3. **JUnit**: Java projects (Spring, Android)
4. **Vitest**: Modern Vite-based projects

## Multi-Language Support

### TypeScript/JavaScript
- Frameworks: Jest, Vitest, Mocha, Jasmine
- Runners: Node.js, Karma, Playwright
- Coverage: Istanbul/nyc, c8

### Python
- Frameworks: Pytest, unittest, nose2
- Runners: pytest, tox, nox
- Coverage: coverage.py, pytest-cov

### Java
- Frameworks: JUnit 5, TestNG, Mockito
- Runners: Maven Surefire, Gradle Test
- Coverage: JaCoCo, Cobertura

## Limitations

### Scope
- **Unit Tests Focus**: Primarily optimized for unit tests (integration tests require different patterns)
- **Static Analysis Only**: Cannot execute tests or measure actual code behavior
- **Language Support**: Best support for TypeScript, JavaScript, Python, Java (other languages limited)

### Coverage Analysis
- **Report Dependency**: Requires existing coverage reports (cannot generate coverage from scratch)
- **Format Support**: LCOV, JSON, XML only (other formats need conversion)
- **Interpretation Context**: Coverage numbers need human judgment for meaningfulness

### Test Generation
- **Baseline Quality**: Generated tests provide scaffolding, require human review and refinement
- **Complex Logic**: Advanced business logic and integration scenarios need manual test design
- **Mocking Strategy**: Mock/stub strategies should align with project patterns

### Framework Integration
- **Configuration Required**: Test runners need proper setup (this skill doesn't modify package.json or pom.xml)
- **Version Compatibility**: Generated code targets recent stable versions (Jest 29+, Pytest 7+, JUnit 5+)

### When NOT to Use This Skill
- **E2E Testing**: Use dedicated E2E tools (Playwright, Cypress, Selenium)
- **Performance Testing**: Use JMeter, k6, or Locust
- **Security Testing**: Use OWASP ZAP, Burp Suite, or security-focused tools
- **Manual Testing**: Some scenarios require human exploratory testing

## Example Workflows

### Workflow 1: Generate Tests from Requirements
```
Input: User story + API specification
Process: Parse requirements → Generate test cases → Create test stubs
Output: Complete test files ready for implementation
```

### Workflow 2: Improve Coverage
```
Input: Coverage report + source code
Process: Identify gaps → Suggest tests → Generate test code
Output: Prioritized test cases for uncovered code
```

### Workflow 3: TDD New Feature
```
Input: Feature requirements
Process: Guide red-green-refactor → Validate each step → Suggest refactorings
Output: Well-tested feature with clean code
```

### Workflow 4: Framework Migration
```
Input: Tests in Framework A
Process: Parse tests → Translate patterns → Generate equivalent tests
Output: Tests in Framework B with same coverage
```

## Integration Points

### CI/CD Integration
- Parse coverage reports from CI artifacts
- Generate coverage badges and reports
- Fail builds on coverage thresholds
- Track coverage trends over time

### IDE Integration
- Generate tests for selected code
- Run coverage analysis on save
- Highlight untested code paths
- Quick-fix suggestions for test gaps

### Code Review
- Validate test coverage in PRs
- Check test quality standards
- Identify missing test scenarios
- Suggest improvements before merge

## Version Support

- **Node.js**: 16+ (Jest 29+, Vitest 0.34+)
- **Python**: 3.8+ (Pytest 7+)
- **Java**: 11+ (JUnit 5.9+)
- **TypeScript**: 4.5+

## Related Skills

This skill works well with:
- **code-review**: Validate test quality during reviews
- **refactoring-assistant**: Maintain tests during refactoring
- **ci-cd-helper**: Integrate coverage in pipelines
- **documentation-generator**: Generate test documentation
