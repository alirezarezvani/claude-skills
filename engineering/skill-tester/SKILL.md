# Skill Tester

---

**Name**: skill-tester
**Tier**: POWERFUL
**Category**: Engineering Quality Assurance
**Dependencies**: None (Python Standard Library Only)
**Author**: Claude Skills Engineering Team
**Version**: 1.0.0
**Last Updated**: 2026-02-16

---

## Description

The Skill Tester is a comprehensive meta-skill designed to validate, test, and score the quality of skills within the claude-skills ecosystem. This powerful quality assurance tool ensures that all skills meet the rigorous standards required for BASIC, STANDARD, and POWERFUL tier classifications through automated validation, testing, and scoring mechanisms.

As the gatekeeping system for skill quality, this meta-skill provides three core capabilities:
1. **Structure Validation** - Ensures skills conform to required directory structures, file formats, and documentation standards
2. **Script Testing** - Validates Python scripts for syntax, imports, functionality, and output format compliance  
3. **Quality Scoring** - Provides comprehensive quality assessment across multiple dimensions with letter grades and improvement recommendations

This skill is essential for maintaining ecosystem consistency, enabling automated CI/CD integration, and supporting both manual and automated quality assurance workflows. It serves as the foundation for pre-commit hooks, pull request validation, and continuous integration processes that maintain the high-quality standards of the claude-skills repository.

## Core Features

### Comprehensive Skill Validation
- **Structure Compliance**: Validates directory structure, required files (SKILL.md, README.md, scripts/, references/, assets/, expected_outputs/)
- **Documentation Standards**: Checks SKILL.md frontmatter, section completeness, minimum line counts per tier
- **File Format Validation**: Ensures proper Markdown formatting, YAML frontmatter syntax, and file naming conventions

### Advanced Script Testing
- **Syntax Validation**: Compiles Python scripts to detect syntax errors before execution
- **Import Analysis**: Enforces standard library only policy, identifies external dependencies
- **Runtime Testing**: Executes scripts with sample data, validates argparse implementation, tests --help functionality
- **Output Format Compliance**: Verifies dual output support (JSON + human-readable), proper error handling

### Multi-Dimensional Quality Scoring
- **Documentation Quality (25%)**: SKILL.md depth and completeness, README clarity, reference documentation quality
- **Code Quality (25%)**: Script complexity, error handling robustness, output format consistency, maintainability
- **Completeness (25%)**: Required directory presence, sample data adequacy, expected output verification
- **Usability (25%)**: Example clarity, argparse help text quality, installation simplicity, user experience

### Tier Classification System
Automatically classifies skills based on complexity and functionality:

#### BASIC Tier Requirements
- Minimum 100 lines in SKILL.md
- At least 1 Python script (100-300 LOC)
- Basic argparse implementation
- Simple input/output handling
- Essential documentation coverage

#### STANDARD Tier Requirements  
- Minimum 200 lines in SKILL.md
- 1-2 Python scripts (300-500 LOC each)
- Advanced argparse with subcommands
- JSON + text output formats
- Comprehensive examples and references
- Error handling and edge case management

#### POWERFUL Tier Requirements
- Minimum 300 lines in SKILL.md
- 2-3 Python scripts (500-800 LOC each)
- Complex argparse with multiple modes
- Sophisticated output formatting and validation
- Extensive documentation and reference materials
- Advanced error handling and recovery mechanisms
- CI/CD integration capabilities

## Architecture & Design

### Modular Design Philosophy
The skill-tester follows a modular architecture where each component serves a specific validation purpose:

- **skill_validator.py**: Core structural and documentation validation engine
- **script_tester.py**: Runtime testing and execution validation framework  
- **quality_scorer.py**: Multi-dimensional quality assessment and scoring system

### Standards Enforcement
All validation is performed against well-defined standards documented in the references/ directory:
- **Skill Structure Specification**: Defines mandatory and optional components
- **Tier Requirements Matrix**: Detailed requirements for each skill tier
- **Quality Scoring Rubric**: Comprehensive scoring methodology and weightings

### Integration Capabilities
Designed for seamless integration into existing development workflows:
- **Pre-commit Hooks**: Prevents substandard skills from being committed
- **CI/CD Pipelines**: Automated quality gates in pull request workflows
- **Manual Validation**: Interactive command-line tools for development-time validation
- **Batch Processing**: Bulk validation and scoring of existing skill repositories

## Implementation Details

### skill_validator.py Core Functions
```python
# Primary validation workflow
validate_skill_structure() -> ValidationReport
check_skill_md_compliance() -> DocumentationReport  
validate_python_scripts() -> ScriptReport
generate_compliance_score() -> float
```

Key validation checks include:
- SKILL.md frontmatter parsing and validation
- Required section presence (Description, Features, Usage, etc.)
- Minimum line count enforcement per tier
- Python script argparse implementation verification
- Standard library import enforcement
- Directory structure compliance
- README.md quality assessment

### script_tester.py Testing Framework
```python
# Core testing functions
syntax_validation() -> SyntaxReport
import_validation() -> ImportReport
runtime_testing() -> RuntimeReport
output_format_validation() -> OutputReport
```

Testing capabilities encompass:
- Python AST-based syntax validation
- Import statement analysis and external dependency detection
- Controlled script execution with timeout protection
- Argparse --help functionality verification
- Sample data processing and output validation
- Expected output comparison and difference reporting

### quality_scorer.py Scoring System
```python
# Multi-dimensional scoring
score_documentation() -> float  # 25% weight
score_code_quality() -> float   # 25% weight
score_completeness() -> float   # 25% weight
score_usability() -> float      # 25% weight
calculate_overall_grade() -> str # A-F grade
```

Scoring dimensions include:
- **Documentation**: Completeness, clarity, examples, reference quality
- **Code Quality**: Complexity, maintainability, error handling, output consistency
- **Completeness**: Required files, sample data, expected outputs, test coverage  
- **Usability**: Help text quality, example clarity, installation simplicity

## Usage Scenarios

### Development Workflow Integration
```bash
# Pre-commit hook validation
skill_validator.py path/to/skill --tier POWERFUL --json

# Comprehensive skill testing
script_tester.py path/to/skill --timeout 30 --sample-data

# Quality assessment and scoring
quality_scorer.py path/to/skill --detailed --recommendations
```

### CI/CD Pipeline Integration
```yaml
# GitHub Actions workflow example
- name: Validate Skill Quality
  run: |
    python skill_validator.py engineering/${{ matrix.skill }} --json | tee validation.json
    python script_tester.py engineering/${{ matrix.skill }} | tee testing.json
    python quality_scorer.py engineering/${{ matrix.skill }} --json | tee scoring.json
```

### Batch Repository Analysis
```bash
# Validate all skills in repository
find engineering/ -type d -maxdepth 1 | xargs -I {} skill_validator.py {}

# Generate repository quality report
quality_scorer.py engineering/ --batch --output-format json > repo_quality.json
```

## Output Formats & Reporting

### Dual Output Support
All tools provide both human-readable and machine-parseable output:

#### Human-Readable Format
```
=== SKILL VALIDATION REPORT ===
Skill: engineering/example-skill
Tier: STANDARD
Overall Score: 85/100 (B)

Structure Validation: ✓ PASS
├─ SKILL.md: ✓ EXISTS (247 lines)
├─ README.md: ✓ EXISTS  
├─ scripts/: ✓ EXISTS (2 files)
└─ references/: ⚠ MISSING (recommended)

Documentation Quality: 22/25 (88%)
Code Quality: 20/25 (80%)
Completeness: 18/25 (72%)
Usability: 21/25 (84%)

Recommendations:
• Add references/ directory with documentation
• Improve error handling in main.py
• Include more comprehensive examples
```

#### JSON Format
```json
{
  "skill_path": "engineering/example-skill",
  "timestamp": "2026-02-16T16:41:00Z",
  "validation_results": {
    "structure_compliance": {
      "score": 0.95,
      "checks": {
        "skill_md_exists": true,
        "readme_exists": true,
        "scripts_directory": true,
        "references_directory": false
      }
    },
    "overall_score": 85,
    "letter_grade": "B",
    "tier_recommendation": "STANDARD",
    "improvement_suggestions": [
      "Add references/ directory",
      "Improve error handling",
      "Include comprehensive examples"
    ]
  }
}
```

## Quality Assurance Standards

### Code Quality Requirements
- **Standard Library Only**: No external dependencies (pip packages)
- **Error Handling**: Comprehensive exception handling with meaningful error messages
- **Output Consistency**: Standardized JSON schema and human-readable formatting
- **Performance**: Efficient validation algorithms with reasonable execution time
- **Maintainability**: Clear code structure, comprehensive docstrings, type hints where appropriate

### Testing Standards  
- **Self-Testing**: The skill-tester validates itself (meta-validation)
- **Sample Data Coverage**: Comprehensive test cases covering edge cases and error conditions
- **Expected Output Verification**: All sample runs produce verifiable, reproducible outputs
- **Timeout Protection**: Safe execution of potentially problematic scripts with timeout limits

### Documentation Standards
- **Comprehensive Coverage**: All functions, classes, and modules documented
- **Usage Examples**: Clear, practical examples for all use cases
- **Integration Guides**: Step-by-step CI/CD and workflow integration instructions
- **Reference Materials**: Complete specification documents for standards and requirements

## Integration Examples

### Pre-Commit Hook Setup
```bash
#!/bin/bash
# .git/hooks/pre-commit
echo "Running skill validation..."
python engineering/skill-tester/scripts/skill_validator.py engineering/new-skill --tier STANDARD
if [ $? -ne 0 ]; then
    echo "Skill validation failed. Commit blocked."
    exit 1
fi
echo "Validation passed. Proceeding with commit."
```

### GitHub Actions Workflow
```yaml
name: Skill Quality Gate
on:
  pull_request:
    paths: ['engineering/**']

jobs:
  validate-skills:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Validate Changed Skills
        run: |
          changed_skills=$(git diff --name-only ${{ github.event.before }} | grep -E '^engineering/[^/]+/' | cut -d'/' -f1-2 | sort -u)
          for skill in $changed_skills; do
            echo "Validating $skill..."
            python engineering/skill-tester/scripts/skill_validator.py $skill --json
            python engineering/skill-tester/scripts/script_tester.py $skill
            python engineering/skill-tester/scripts/quality_scorer.py $skill --minimum-score 75
          done
```

### Continuous Quality Monitoring
```bash
#!/bin/bash
# Daily quality report generation
echo "Generating daily skill quality report..."
timestamp=$(date +"%Y-%m-%d")
python engineering/skill-tester/scripts/quality_scorer.py engineering/ \
  --batch --json > "reports/quality_report_${timestamp}.json"

echo "Quality trends analysis..."
python engineering/skill-tester/scripts/trend_analyzer.py reports/ \
  --days 30 > "reports/quality_trends_${timestamp}.md"
```

## Performance & Scalability

### Execution Performance
- **Fast Validation**: Structure validation completes in <1 second per skill
- **Efficient Testing**: Script testing with timeout protection (configurable, default 30s)
- **Batch Processing**: Optimized for repository-wide analysis with parallel processing support
- **Memory Efficiency**: Minimal memory footprint for large-scale repository analysis

### Scalability Considerations
- **Repository Size**: Designed to handle repositories with 100+ skills
- **Concurrent Execution**: Thread-safe implementation supports parallel validation
- **Resource Management**: Automatic cleanup of temporary files and subprocess resources
- **Configuration Flexibility**: Configurable timeouts, memory limits, and validation strictness

## Security & Safety

### Safe Execution Environment
- **Sandboxed Testing**: Scripts execute in controlled environment with timeout protection
- **Resource Limits**: Memory and CPU usage monitoring to prevent resource exhaustion
- **Input Validation**: All inputs sanitized and validated before processing
- **No Network Access**: Offline operation ensures no external dependencies or network calls

### Security Best Practices
- **No Code Injection**: Static analysis only, no dynamic code generation
- **Path Traversal Protection**: Secure file system access with path validation
- **Minimal Privileges**: Operates with minimal required file system permissions
- **Audit Logging**: Comprehensive logging for security monitoring and troubleshooting

## Troubleshooting & Support

### Common Issues & Solutions

#### Validation Failures
- **Missing Files**: Check directory structure against tier requirements
- **Import Errors**: Ensure only standard library imports are used
- **Documentation Issues**: Verify SKILL.md frontmatter and section completeness

#### Script Testing Problems  
- **Timeout Errors**: Increase timeout limit or optimize script performance
- **Execution Failures**: Check script syntax and import statement validity
- **Output Format Issues**: Ensure proper JSON formatting and dual output support

#### Quality Scoring Discrepancies
- **Low Scores**: Review scoring rubric and improvement recommendations
- **Tier Misclassification**: Verify skill complexity against tier requirements
- **Inconsistent Results**: Check for recent changes in quality standards or scoring weights

### Debugging Support
- **Verbose Mode**: Detailed logging and execution tracing available
- **Dry Run Mode**: Validation without execution for debugging purposes
- **Debug Output**: Comprehensive error reporting with file locations and suggestions

## Future Enhancements

### Planned Features
- **Machine Learning Quality Prediction**: AI-powered quality assessment using historical data
- **Performance Benchmarking**: Execution time and resource usage tracking across skills
- **Dependency Analysis**: Automated detection and validation of skill interdependencies
- **Quality Trend Analysis**: Historical quality tracking and regression detection

### Integration Roadmap
- **IDE Plugins**: Real-time validation in popular development environments
- **Web Dashboard**: Centralized quality monitoring and reporting interface
- **API Endpoints**: RESTful API for external integration and automation
- **Notification Systems**: Automated alerts for quality degradation or validation failures

## Conclusion

The Skill Tester represents a critical infrastructure component for maintaining the high-quality standards of the claude-skills ecosystem. By providing comprehensive validation, testing, and scoring capabilities, it ensures that all skills meet or exceed the rigorous requirements for their respective tiers.

This meta-skill not only serves as a quality gate but also as a development tool that guides skill authors toward best practices and helps maintain consistency across the entire repository. Through its integration capabilities and comprehensive reporting, it enables both manual and automated quality assurance workflows that scale with the growing claude-skills ecosystem.

The combination of structural validation, runtime testing, and multi-dimensional quality scoring provides unparalleled visibility into skill quality while maintaining the flexibility needed for diverse skill types and complexity levels. As the claude-skills repository continues to grow, the Skill Tester will remain the cornerstone of quality assurance and ecosystem integrity.