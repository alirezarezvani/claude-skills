# Quality Standards

## Core Quality Principles

### **1. Quality-First Completion**
- **Zero Defect Handoff:** No work considered complete with known quality issues
- **Comprehensive Validation:** All acceptance criteria verified through testing
- **Path Resolution:** All relative paths validated and working
- **Tool Execution:** All Python tools tested and executing correctly

### **2. Testing Standards**
- **Python Tools:** All automation tools must execute without errors
- **Agent Workflows:** Agent markdown files validated for completeness
- **Integration Testing:** Agent-to-skill integration verified
- **Documentation Quality:** All documentation clear, accurate, and actionable

### **3. Code Quality**
- **Python Standards:** PEP 8 compliance for all Python scripts
- **No Hardcoded Secrets:** Use environment variables or configuration files
- **Error Handling:** Proper exception handling in all tools
- **Type Hints:** Use type annotations for Python functions

## Universal Completion Criteria (ALL TASKS)

```yaml
functional_requirements:
  - [ ] All acceptance criteria satisfied with documented verification
  - [ ] Feature functionality validated in target environments
  - [ ] Edge cases identified and handled appropriately
  - [ ] Error scenarios tested with proper error handling
  - [ ] Integration points tested and validated

quality_standards:
  - [ ] Code review completed with documented feedback
  - [ ] Automated tests passing where applicable
  - [ ] Manual testing completed for user-facing functionality
  - [ ] Documentation updated with changes
  - [ ] No broken links or missing references

documentation_requirements:
  - [ ] Technical documentation updated with implementation details
  - [ ] User documentation updated with new functionality guidance
  - [ ] Change documentation prepared with impact analysis
  - [ ] Handoff documentation prepared with clear next steps
```

## Agent-Specific Quality Gates

### **Agent Implementation Standards**

```yaml
agent_quality_validation:
  yaml_frontmatter:
    - [ ] Valid YAML syntax (no parsing errors)
    - [ ] All required fields present (name, description, skills, domain, model, tools)
    - [ ] cs-* prefix used for agent naming
    - [ ] Domain correctly categorized

  skill_integration:
    - [ ] Relative paths resolve correctly (../../ pattern)
    - [ ] Skill location documented and accessible
    - [ ] Python tools referenced with correct paths
    - [ ] Knowledge bases referenced with correct paths
    - [ ] Templates referenced with correct paths

  workflow_documentation:
    - [ ] Minimum 3 workflows documented
    - [ ] Each workflow has clear step-by-step instructions
    - [ ] Integration examples provided
    - [ ] Success metrics defined
    - [ ] Related agents cross-referenced

  testing_requirements:
    - [ ] Python tool execution tested from agent context
    - [ ] Relative path resolution verified
    - [ ] Knowledge base files accessible
    - [ ] All examples in documentation work
    - [ ] No broken markdown links
```

## Python Tool Quality Standards

### **Python Script Requirements**

```python
# All Python tools must follow these standards

"""
Module: tool_name.py
Description: [Clear description of what this tool does]
Usage: python tool_name.py [arguments]
"""

from typing import Optional, List, Dict
import sys
import json

def main(arg1: str, arg2: Optional[str] = None) -> int:
    """
    Main function description.

    Args:
        arg1: Description of argument 1
        arg2: Description of optional argument 2

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        # Tool implementation
        result = process_data(arg1, arg2)

        # Output results
        if json_output:
            print(json.dumps(result, indent=2))
        else:
            print(format_human_readable(result))

        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

### **Python Quality Checklist**

```yaml
python_tool_quality:
  code_standards:
    - [ ] PEP 8 compliant (use pylint or flake8)
    - [ ] Type hints for all functions
    - [ ] Docstrings for all public functions
    - [ ] Clear error messages
    - [ ] Proper exception handling

  functionality:
    - [ ] Handles missing arguments gracefully
    - [ ] Provides helpful usage information (--help)
    - [ ] Supports both JSON and human-readable output
    - [ ] Returns appropriate exit codes
    - [ ] No hardcoded file paths (use relative or arguments)

  dependencies:
    - [ ] Uses standard library when possible
    - [ ] External dependencies documented in skill README
    - [ ] Requirements.txt provided if external packages needed
    - [ ] Version constraints specified for dependencies
```

## Documentation Quality Standards

### **Markdown Documentation Requirements**

```yaml
documentation_quality:
  structure:
    - [ ] Clear hierarchy with proper headings
    - [ ] Table of contents for long documents
    - [ ] Consistent formatting throughout
    - [ ] Code blocks use appropriate syntax highlighting
    - [ ] Lists properly formatted

  content:
    - [ ] All links work (no 404s)
    - [ ] All code examples tested and working
    - [ ] All file paths are correct
    - [ ] Screenshots/diagrams up to date
    - [ ] No outdated information

  accessibility:
    - [ ] Alt text for images
    - [ ] Descriptive link text (not "click here")
    - [ ] Proper heading hierarchy (no skipping levels)
    - [ ] Code examples include explanatory text

  maintenance:
    - [ ] Date updated timestamp
    - [ ] Version information if applicable
    - [ ] Changelog for significant updates
```

## Quality Validation Commands

### **Automated Quality Checks**

```bash
# Markdown linting
yamllint agents/**/*.md standards/**/*.md documentation/**/*.md

# Python syntax validation
python -m compileall marketing-skill product-team c-level-advisor engineering-team ra-qm-team

# Check for broken links (manual check required)
# Verify all ../../ relative paths resolve

# Test Python tools
for script in $(find . -name "*.py" -path "*/scripts/*"); do
    echo "Testing: $script"
    python "$script" --help || echo "❌ Failed: $script"
done
```

### **Manual Validation Checklist**

```yaml
pre_commit_validation:
  agent_files:
    - [ ] YAML frontmatter valid
    - [ ] All workflows documented
    - [ ] Integration examples present
    - [ ] No broken links
    - [ ] Relative paths verified

  python_tools:
    - [ ] Scripts execute without errors
    - [ ] --help flag works
    - [ ] Error handling tested
    - [ ] Output formats correct

  documentation:
    - [ ] README updated if needed
    - [ ] CLAUDE.md reflects changes
    - [ ] All examples tested
    - [ ] Changelog updated

pre_push_validation:
    - [ ] All quality checks pass
    - [ ] No secrets in code
    - [ ] Commit messages follow convention
    - [ ] Branch protection requirements met
```

## Quality Metrics for Agents & Skills

### **Success Criteria**

```yaml
agent_effectiveness:
  workflow_clarity:
    target: "Users can follow workflows without assistance"
    measurement: "Documentation completeness and clarity"

  tool_reliability:
    target: "100% of Python tools execute successfully"
    measurement: "Script execution success rate"

  path_resolution:
    target: "100% of relative paths resolve correctly"
    measurement: "Path validation tests passing"

  integration_quality:
    target: "Agents seamlessly invoke skills"
    measurement: "Agent-skill integration tests passing"

documentation_quality:
  completeness:
    target: "All required sections present"
    measurement: "Documentation structure checklist"

  accuracy:
    target: "Zero broken links or outdated information"
    measurement: "Link validation and content review"

  usability:
    target: "Users can implement workflows in <30 minutes"
    measurement: "Time-to-implementation tracking"
```

## Quality Improvement Process

### **Continuous Quality Enhancement**

- **Pre-commit:** Validate syntax, check paths, test tools locally
- **Pull Request:** Peer review, automated testing, quality gate checks
- **Post-merge:** Monitor for issues, collect user feedback
- **Monthly:** Review quality metrics, update standards as needed
- **Quarterly:** Assess skill/agent effectiveness, plan improvements

### **Quality Issue Resolution**

```yaml
issue_priority:
  P0_critical:
    - Broken Python tools (execution failures)
    - Invalid relative paths (404 errors)
    - Security vulnerabilities
    - Data loss or corruption
    response_time: "<1 hour"

  P1_high:
    - Broken workflows in agents
    - Documentation inaccuracies
    - Missing required sections
    - Performance issues
    response_time: "<24 hours"

  P2_medium:
    - Enhancement requests
    - Documentation improvements
    - Code refactoring
    - Optimization opportunities
    response_time: "<1 week"

  P3_low:
    - Nice-to-have features
    - Minor documentation updates
    - Style improvements
    response_time: "<1 month"
```

---

**Focus**: Python tool quality, agent workflow clarity, skill integration testing
**Updated**: November 2025
**Review**: Monthly quality assessment
**Compliance**: PEP 8, Markdown standards, relative path conventions
