# Quality Scoring Rubric

**Version**: 1.0.0  
**Last Updated**: 2026-02-16  
**Authority**: Claude Skills Engineering Team  

## Overview

This document defines the comprehensive quality scoring methodology used to assess skills within the claude-skills ecosystem. The scoring system evaluates four key dimensions, each weighted equally at 25%, to provide an objective and consistent measure of skill quality.

## Scoring Framework

### Overall Scoring Scale
- **A+ (95-100)**: Exceptional quality, exceeds all standards
- **A (90-94)**: Excellent quality, meets highest standards consistently  
- **A- (85-89)**: Very good quality, minor areas for improvement
- **B+ (80-84)**: Good quality, meets most standards well
- **B (75-79)**: Satisfactory quality, meets standards adequately
- **B- (70-74)**: Below average, several areas need improvement
- **C+ (65-69)**: Poor quality, significant improvements needed
- **C (60-64)**: Minimal acceptable quality, major improvements required
- **C- (55-59)**: Unacceptable quality, extensive rework needed
- **D (50-54)**: Very poor quality, fundamental issues present
- **F (0-49)**: Failing quality, does not meet basic standards

### Dimension Weights
Each dimension contributes equally to the overall score:
- **Documentation Quality**: 25%
- **Code Quality**: 25%
- **Completeness**: 25%
- **Usability**: 25%

## Documentation Quality (25% Weight)

### Scoring Components

#### SKILL.md Quality (40% of Documentation Score)
**Component Breakdown:**
- **Length and Depth (25%)**: Line count and content substance
- **Frontmatter Quality (25%)**: Completeness and accuracy of YAML metadata
- **Section Coverage (25%)**: Required and recommended section presence
- **Content Depth (25%)**: Technical detail and comprehensiveness

**Scoring Criteria:**

| Score Range | Length | Frontmatter | Sections | Depth |
|-------------|--------|-------------|----------|-------|
| 90-100 | 400+ lines | All fields complete + extras | All required + 4+ recommended | Rich technical detail, examples |
| 80-89 | 300-399 lines | All required fields complete | All required + 2-3 recommended | Good technical coverage |
| 70-79 | 200-299 lines | Most required fields | All required + 1 recommended | Adequate technical content |
| 60-69 | 150-199 lines | Some required fields | Most required sections | Basic technical information |
| 50-59 | 100-149 lines | Minimal frontmatter | Some required sections | Limited technical detail |
| Below 50 | <100 lines | Missing/invalid frontmatter | Few/no required sections | Insufficient content |

#### README.md Quality (25% of Documentation Score)
**Scoring Criteria:**
- **Excellent (90-100)**: 1000+ chars, comprehensive usage guide, examples, troubleshooting
- **Good (75-89)**: 500-999 chars, clear usage instructions, basic examples
- **Satisfactory (60-74)**: 200-499 chars, minimal usage information
- **Poor (40-59)**: <200 chars or confusing content
- **Failing (0-39)**: Missing or completely inadequate

#### Reference Documentation (20% of Documentation Score)
**Scoring Criteria:**
- **Excellent (90-100)**: Multiple comprehensive reference docs (2000+ chars total)
- **Good (75-89)**: 2-3 reference files with substantial content
- **Satisfactory (60-74)**: 1-2 reference files with adequate content
- **Poor (40-59)**: Minimal reference content or poor quality
- **Failing (0-39)**: No reference documentation

#### Examples and Usage Clarity (15% of Documentation Score)
**Scoring Criteria:**
- **Excellent (90-100)**: 5+ diverse examples, clear usage patterns
- **Good (75-89)**: 3-4 examples covering different scenarios
- **Satisfactory (60-74)**: 2-3 basic examples
- **Poor (40-59)**: 1-2 minimal examples
- **Failing (0-39)**: No examples or unclear usage

## Code Quality (25% Weight)

### Scoring Components

#### Script Complexity and Architecture (25% of Code Score)
**Evaluation Criteria:**
- Lines of code per script relative to tier requirements
- Function and class organization
- Code modularity and reusability
- Algorithm sophistication

**Scoring Matrix:**

| Tier | Excellent (90-100) | Good (75-89) | Satisfactory (60-74) | Poor (Below 60) |
|------|-------------------|--------------|---------------------|-----------------|
| BASIC | 200-300 LOC, well-structured | 150-199 LOC, organized | 100-149 LOC, basic | <100 LOC, minimal |
| STANDARD | 400-500 LOC, modular | 350-399 LOC, structured | 300-349 LOC, adequate | <300 LOC, basic |
| POWERFUL | 600-800 LOC, sophisticated | 550-599 LOC, advanced | 500-549 LOC, solid | <500 LOC, simple |

#### Error Handling Quality (25% of Code Score)
**Scoring Criteria:**
- **Excellent (90-100)**: Comprehensive exception handling, specific error types, recovery mechanisms
- **Good (75-89)**: Good exception handling, meaningful error messages, logging
- **Satisfactory (60-74)**: Basic try/except blocks, simple error messages
- **Poor (40-59)**: Minimal error handling, generic exceptions
- **Failing (0-39)**: No error handling or inappropriate handling

**Error Handling Checklist:**
- [ ] Try/except blocks for risky operations
- [ ] Specific exception types (not just Exception)
- [ ] Meaningful error messages for users
- [ ] Proper error logging or reporting
- [ ] Graceful degradation where possible
- [ ] Input validation and sanitization

#### Code Structure and Organization (25% of Code Score)
**Evaluation Elements:**
- Function decomposition and single responsibility
- Class design and inheritance patterns
- Import organization and dependency management
- Documentation and comments quality
- Consistent naming conventions
- PEP 8 compliance

**Scoring Guidelines:**
- **Excellent (90-100)**: Exemplary structure, comprehensive docstrings, perfect style
- **Good (75-89)**: Well-organized, good documentation, minor style issues
- **Satisfactory (60-74)**: Adequate structure, basic documentation, some style issues
- **Poor (40-59)**: Poor organization, minimal documentation, style problems
- **Failing (0-39)**: No clear structure, no documentation, major style violations

#### Output Format Support (25% of Code Score)
**Required Capabilities:**
- JSON output format support
- Human-readable output format
- Proper data serialization
- Consistent output structure
- Error output handling

**Scoring Criteria:**
- **Excellent (90-100)**: Dual format + custom formats, perfect serialization
- **Good (75-89)**: Dual format support, good serialization
- **Satisfactory (60-74)**: Single format well-implemented
- **Poor (40-59)**: Basic output, formatting issues
- **Failing (0-39)**: Poor or no structured output

## Completeness (25% Weight)

### Scoring Components

#### Directory Structure Compliance (25% of Completeness Score)
**Required Directories by Tier:**
- **BASIC**: scripts/ (required), assets/ + references/ (recommended)
- **STANDARD**: scripts/ + assets/ + references/ (required), expected_outputs/ (recommended)
- **POWERFUL**: scripts/ + assets/ + references/ + expected_outputs/ (all required)

**Scoring Calculation:**
```
Structure Score = (Required Present / Required Total) * 0.6 + 
                  (Recommended Present / Recommended Total) * 0.4
```

#### Asset Availability and Quality (25% of Completeness Score)
**Scoring Criteria:**
- **Excellent (90-100)**: 5+ diverse assets, multiple file types, realistic data
- **Good (75-89)**: 3-4 assets, some diversity, good quality
- **Satisfactory (60-74)**: 2-3 assets, basic variety
- **Poor (40-59)**: 1-2 minimal assets
- **Failing (0-39)**: No assets or unusable assets

**Asset Quality Factors:**
- File diversity (JSON, CSV, YAML, etc.)
- Data realism and complexity
- Coverage of use cases
- File size appropriateness
- Documentation of asset purpose

#### Expected Output Coverage (25% of Completeness Score)
**Evaluation Criteria:**
- Correspondence with asset files
- Coverage of success and error scenarios
- Output format variety
- Reproducibility and accuracy

**Scoring Matrix:**
- **Excellent (90-100)**: Complete output coverage, all scenarios, verified accuracy
- **Good (75-89)**: Good coverage, most scenarios, mostly accurate
- **Satisfactory (60-74)**: Basic coverage, main scenarios
- **Poor (40-59)**: Minimal coverage, some inaccuracies
- **Failing (0-39)**: No expected outputs or completely inaccurate

#### Test Coverage and Validation (25% of Completeness Score)
**Assessment Areas:**
- Sample data processing capability
- Output verification mechanisms  
- Edge case handling
- Error condition testing
- Integration test scenarios

**Scoring Guidelines:**
- **Excellent (90-100)**: Comprehensive test coverage, automated validation
- **Good (75-89)**: Good test coverage, manual validation possible
- **Satisfactory (60-74)**: Basic testing capability
- **Poor (40-59)**: Minimal testing support
- **Failing (0-39)**: No testing or validation capability

## Usability (25% Weight)

### Scoring Components

#### Installation and Setup Simplicity (25% of Usability Score)
**Evaluation Factors:**
- Dependency requirements (Python stdlib preferred)
- Setup complexity
- Environment requirements
- Installation documentation clarity

**Scoring Criteria:**
- **Excellent (90-100)**: Zero external dependencies, single-file execution
- **Good (75-89)**: Minimal dependencies, simple setup
- **Satisfactory (60-74)**: Some dependencies, documented setup
- **Poor (40-59)**: Complex dependencies, unclear setup
- **Failing (0-39)**: Unable to install or excessive complexity

#### Usage Clarity and Help Quality (25% of Usability Score)
**Assessment Elements:**
- Command-line help comprehensiveness
- Usage example clarity
- Parameter documentation quality
- Error message helpfulness

**Help Quality Checklist:**
- [ ] Comprehensive --help output
- [ ] Clear parameter descriptions
- [ ] Usage examples included
- [ ] Error messages are actionable
- [ ] Progress indicators where appropriate

**Scoring Matrix:**
- **Excellent (90-100)**: Exemplary help, multiple examples, perfect error messages
- **Good (75-89)**: Good help quality, clear examples, helpful errors
- **Satisfactory (60-74)**: Adequate help, basic examples
- **Poor (40-59)**: Minimal help, confusing interface
- **Failing (0-39)**: No help or completely unclear interface

#### Documentation Accessibility (25% of Usability Score)
**Evaluation Criteria:**
- README quick start effectiveness
- SKILL.md navigation and structure
- Reference material organization
- Learning curve considerations

**Accessibility Factors:**
- Information hierarchy clarity
- Cross-reference quality
- Beginner-friendly explanations
- Advanced user shortcuts
- Troubleshooting guidance

#### Practical Example Quality (25% of Usability Score)
**Assessment Areas:**
- Example realism and relevance
- Complexity progression (simple to advanced)
- Output demonstration
- Common use case coverage
- Integration scenarios

**Scoring Guidelines:**
- **Excellent (90-100)**: 5+ examples, perfect progression, real-world scenarios
- **Good (75-89)**: 3-4 examples, good variety, practical scenarios
- **Satisfactory (60-74)**: 2-3 examples, adequate coverage
- **Poor (40-59)**: 1-2 examples, limited practical value
- **Failing (0-39)**: No examples or completely impractical

## Scoring Calculations

### Dimension Score Calculation
Each dimension score is calculated as a weighted average of its components:

```python
def calculate_dimension_score(components):
    total_weighted_score = 0
    total_weight = 0
    
    for component_name, component_data in components.items():
        score = component_data['score']
        weight = component_data['weight']
        total_weighted_score += score * weight
        total_weight += weight
    
    return total_weighted_score / total_weight if total_weight > 0 else 0
```

### Overall Score Calculation
The overall score combines all dimensions with equal weighting:

```python
def calculate_overall_score(dimensions):
    return sum(dimension.score * 0.25 for dimension in dimensions.values())
```

### Letter Grade Assignment
```python
def assign_letter_grade(overall_score):
    if overall_score >= 95: return "A+"
    elif overall_score >= 90: return "A"
    elif overall_score >= 85: return "A-"
    elif overall_score >= 80: return "B+"
    elif overall_score >= 75: return "B"
    elif overall_score >= 70: return "B-"
    elif overall_score >= 65: return "C+"
    elif overall_score >= 60: return "C"
    elif overall_score >= 55: return "C-"
    elif overall_score >= 50: return "D"
    else: return "F"
```

## Quality Improvement Recommendations

### Score-Based Recommendations

#### For Scores Below 60 (C- or Lower)
**Priority Actions:**
1. Address fundamental structural issues
2. Implement basic error handling
3. Add essential documentation sections
4. Create minimal viable examples
5. Fix critical functionality issues

#### For Scores 60-74 (C+ to B-)
**Improvement Areas:**
1. Expand documentation comprehensiveness
2. Enhance error handling sophistication
3. Add more diverse examples and use cases
4. Improve code organization and structure
5. Increase test coverage and validation

#### For Scores 75-84 (B to B+)
**Enhancement Opportunities:**
1. Refine documentation for expert-level quality
2. Implement advanced error recovery mechanisms
3. Add comprehensive reference materials
4. Optimize code architecture and performance
5. Develop extensive example library

#### For Scores 85+ (A- or Higher)
**Excellence Maintenance:**
1. Regular quality audits and updates
2. Community feedback integration
3. Best practice evolution tracking
4. Mentoring lower-quality skills
5. Innovation and cutting-edge feature adoption

### Dimension-Specific Improvement Strategies

#### Low Documentation Scores
- Expand SKILL.md with technical details
- Add comprehensive API reference
- Include architecture diagrams and explanations
- Develop troubleshooting guides
- Create contributor documentation

#### Low Code Quality Scores
- Refactor for better modularity
- Implement comprehensive error handling
- Add extensive code documentation
- Apply advanced design patterns
- Optimize performance and efficiency

#### Low Completeness Scores
- Add missing directories and files
- Develop comprehensive sample datasets
- Create expected output libraries
- Implement automated testing
- Add integration examples

#### Low Usability Scores
- Simplify installation process
- Improve command-line interface design
- Enhance help text and documentation
- Create beginner-friendly tutorials
- Add interactive examples

## Quality Assurance Process

### Automated Scoring
The quality scorer runs automated assessments based on this rubric:
1. File system analysis for structure compliance
2. Content analysis for documentation quality
3. Code analysis for quality metrics
4. Asset inventory and quality assessment

### Manual Review Process
Human reviewers validate automated scores and provide qualitative insights:
1. Content quality assessment beyond automated metrics
2. Usability testing with real-world scenarios
3. Technical accuracy verification
4. Community value assessment

### Continuous Improvement
The scoring rubric evolves based on:
- Community feedback and usage patterns
- Industry best practice changes
- Tool capability enhancements
- Quality trend analysis

This quality scoring rubric ensures consistent, objective, and comprehensive assessment of all skills within the claude-skills ecosystem while providing clear guidance for quality improvement.