---
Name: valid-test-skill
Description: "A valid test skill for testing the skill-tester. Use when testing validation, scoring, or testing workflows."
Tier: STANDARD
Category: testing
Dependencies: None
Author: Test Author
Version: 1.0.0
Last Updated: 2026-03-26
---

# Valid Test Skill

You are an expert in testing. Your goal is to validate the skill-tester tool.

## Description

This is a test skill designed to validate the skill-tester's ability to correctly identify and score well-structured skills. It follows all the required patterns from the SKILL-AUTHORING-STANDARD.md.

## Features

- Feature 1: Validates skill structure
- Feature 2: Tests Python script quality
- Feature 3: Scores skill completeness
- Feature 4: Provides improvement recommendations

## Usage

### Basic Usage

```bash
python scripts/example_tool.py --input data.txt --output result.json
```

### Advanced Usage

```bash
python scripts/example_tool.py --input data.txt --output result.json --verbose --format json
```

## Examples

### Example 1: Basic Validation

```bash
python scripts/example_tool.py --input sample.txt
```

Output:
```
Validation complete. Score: 85/100
```

### Example 2: JSON Output

```bash
python scripts/example_tool.py --input sample.txt --json
```

Output:
```json
{
  "score": 85,
  "status": "PASS",
  "recommendations": []
}
```

## Architecture

The skill follows a modular architecture:

- `scripts/` - Contains Python tools
- `references/` - Contains reference documentation
- `assets/` - Contains sample data

## Installation

No installation required. Uses Python standard library only.

## Proactive Triggers

Surface these issues without being asked:

- **Invalid skill structure** → Flag missing required directories
- **Script errors** → Flag syntax or import issues
- **Low quality score** → Flag skills below minimum threshold

## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| Validation report | Detailed scorecard with pass/fail status |
| Quality score | 0-100 score with letter grade |
| Recommendations | Prioritized improvement list |

## Communication

All output follows the structured communication standard:
- **Bottom line first** — answer before explanation
- **What + Why + How** — every finding has all three
- **Actions have owners and deadlines** — no "we should consider"
- **Confidence tagging** — 🟢 verified / 🟡 medium / 🔴 assumed

## Related Skills

- **skill-tester**: Use when validating other skills. NOT for creating new skills.
- **quality-scorer**: Use when assessing skill quality. NOT for structural validation.

## Troubleshooting

### Common Issues

1. **Script won't run**: Check Python version (3.7+ required)
2. **Import errors**: Ensure only stdlib imports are used
3. **Low score**: Review recommendations and add missing sections

## Contributing

Contributions welcome! Please follow the SKILL-AUTHORING-STANDARD.md guidelines.