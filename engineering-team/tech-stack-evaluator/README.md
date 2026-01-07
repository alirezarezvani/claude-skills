# Technology Stack Evaluator - Comprehensive Tech Decision Support

**Version**: 1.0.0
**Author**: Claude Skills Factory
**Category**: Engineering & Architecture
**Last Updated**: 2025-11-05

---

## Overview

The **Technology Stack Evaluator** skill provides comprehensive, data-driven evaluation and comparison of technologies, frameworks, cloud providers, and complete technology stacks. It helps engineering teams make informed decisions about technology adoption, migration, and architecture choices.

### Key Features

- **8 Comprehensive Evaluation Capabilities**: Technology comparison, stack evaluation, maturity analysis, TCO calculation, security assessment, migration path analysis, cloud provider comparison, and decision reporting

- **Flexible Input Formats**: Automatic detection and parsing of text, YAML, JSON, and URLs

- **Context-Aware Output**: Adapts to Claude Desktop (rich markdown) or CLI (terminal-friendly)

- **Modular Analysis**: Choose which sections to run (quick comparison vs comprehensive report)

- **Token-Efficient**: Executive summaries (200-300 tokens) with progressive disclosure for details

- **Intelligent Recommendations**: Data-driven with confidence scores and clear decision factors

---

## What This Skill Does

### 1. Technology Comparison
Compare frameworks, languages, and tools head-to-head:
- React vs Vue vs Svelte vs Angular
- PostgreSQL vs MongoDB vs MySQL
- Node.js vs Python vs Go for APIs
- AWS vs Azure vs GCP

**Outputs**: Weighted decision matrix, pros/cons, confidence scores

### 2. Stack Evaluation
Assess complete technology stacks for specific use cases:
- Real-time collaboration platforms
- API-heavy SaaS applications
- Data-intensive applications
- Enterprise systems

**Outputs**: Stack health assessment, compatibility analysis, recommendations

### 3. Maturity & Ecosystem Analysis
Evaluate technology health and long-term viability:
- **GitHub Metrics**: Stars, forks, contributors, commit frequency
- **npm Metrics**: Downloads, version stability, dependencies
- **Community Health**: Stack Overflow, job market, tutorials
- **Viability Assessment**: Corporate backing, sustainability, risk scoring

**Outputs**: Health score (0-100), viability level, risk factors, strengths

### 4. Total Cost of Ownership (TCO)
Calculate comprehensive 3-5 year costs:
- **Initial**: Licensing, training, migration, setup
- **Operational**: Hosting, support, maintenance (yearly projections)
- **Scaling**: Per-user costs, infrastructure scaling
- **Hidden**: Technical debt, vendor lock-in, downtime, turnover
- **Productivity**: Time-to-market impact, ROI

**Outputs**: Total TCO, yearly breakdown, cost drivers, optimization opportunities

### 5. Security & Compliance
Analyze security posture and compliance readiness:
- **Vulnerability Analysis**: CVE counts by severity (Critical/High/Medium/Low)
- **Security Scoring**: 0-100 with letter grade
- **Compliance Assessment**: GDPR, SOC2, HIPAA, PCI-DSS readiness
- **Patch Responsiveness**: Average time to patch critical vulnerabilities

**Outputs**: Security score, compliance gaps, recommendations

### 6. Migration Path Analysis
Assess migration complexity and planning:
- **Complexity Scoring**: 1-10 across 6 factors (code volume, architecture, data, APIs, dependencies, testing)
- **Effort Estimation**: Person-months, timeline, phase breakdown
- **Risk Assessment**: Technical, business, and team risks with mitigations
- **Migration Strategy**: Direct, phased, or strangler pattern

**Outputs**: Migration plan, timeline, risks, success criteria

### 7. Cloud Provider Comparison
Compare AWS vs Azure vs GCP for specific workloads:
- Weighted decision criteria
- Workload-specific optimizations
- Cost comparisons
- Feature parity analysis

**Outputs**: Provider recommendation, cost comparison, feature matrix

### 8. Decision Reports
Generate comprehensive decision documentation:
- Executive summaries (200-300 tokens)
- Detailed analysis (800-1500 tokens)
- Decision matrices with confidence levels
- Exportable markdown reports

**Outputs**: Multi-format reports adapted to context

---

## File Structure

```
tech-stack-evaluator/
├── SKILL.md                          # Main skill definition (YAML + documentation)
├── README.md                         # This file - comprehensive guide
├── HOW_TO_USE.md                     # Usage examples and patterns
│
├── stack_comparator.py               # Comparison engine with weighted scoring
├── tco_calculator.py                 # Total Cost of Ownership calculations
├── ecosystem_analyzer.py             # Ecosystem health and viability assessment
├── security_assessor.py              # Security and compliance analysis
├── migration_analyzer.py             # Migration path and complexity analysis
├── format_detector.py                # Automatic input format detection
├── report_generator.py               # Context-aware report generation
│
├── sample_input_text.json            # Conversational input example
├── sample_input_structured.json      # JSON structured input example
├── sample_input_tco.json             # TCO analysis input example
└── expected_output_comparison.json   # Sample output structure
```

### Python Modules (7 files)

1. **`stack_comparator.py`** (355 lines)
   - Weighted scoring algorithm
   - Feature matrices
   - Pros/cons generation
   - Recommendation engine with confidence calculation

2. **`tco_calculator.py`** (403 lines)
   - Initial costs (licensing, training, migration)
   - Operational costs with growth projections
   - Scaling cost analysis
   - Hidden costs (technical debt, vendor lock-in, downtime)
   - Productivity impact and ROI

3. **`ecosystem_analyzer.py`** (419 lines)
   - GitHub health scoring (stars, forks, commits, issues)
   - npm health scoring (downloads, versions, dependencies)
   - Community health (Stack Overflow, jobs, tutorials)
   - Corporate backing assessment
   - Viability risk analysis

4. **`security_assessor.py`** (406 lines)
   - Vulnerability scoring (CVE analysis)
   - Patch responsiveness assessment
   - Security features evaluation
   - Compliance readiness (GDPR, SOC2, HIPAA, PCI-DSS)
   - Risk level determination

5. **`migration_analyzer.py`** (485 lines)
   - Complexity scoring (6 factors: code, architecture, data, APIs, dependencies, testing)
   - Effort estimation (person-months, timeline)
   - Risk assessment (technical, business, team)
   - Migration strategy recommendation (direct, phased, strangler)
   - Success criteria definition

6. **`format_detector.py`** (334 lines)
   - Automatic format detection (JSON, YAML, URLs, text)
   - Multi-format parsing
   - Technology name extraction
   - Use case inference
   - Priority detection

7. **`report_generator.py`** (372 lines)
   - Context detection (Desktop vs CLI)
   - Executive summary generation (200-300 tokens)
   - Full report generation with modular sections
   - Rich markdown (Desktop) vs ASCII tables (CLI)
   - Export to file functionality

**Total**: ~2,774 lines of Python code

---

## Installation

### Claude Code (Project-Level)
```bash
# Navigate to your project
cd /path/to/your/project

# Create skills directory if it doesn't exist
mkdir -p .claude/skills

# Copy the skill folder
cp -r /path/to/tech-stack-evaluator .claude/skills/
```

### Claude Code (User-Level, All Projects)
```bash
# Create user-level skills directory
mkdir -p ~/.claude/skills

# Copy the skill folder
cp -r /path/to/tech-stack-evaluator ~/.claude/skills/
```

### Claude Desktop
1. Locate the skill ZIP file: `tech-stack-evaluator.zip`
2. Drag and drop the ZIP into Claude Desktop
3. The skill will be automatically loaded

### Claude Apps (Browser)
Use the `skill-creator` skill to import the ZIP file, or manually copy files to your project's `.claude/skills/` directory.

### API Usage
```bash
# Upload skill via API
curl -X POST https://api.anthropic.com/v1/skills \
  -H "Authorization: Bearer $ANTHROPIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d @tech-stack-evaluator.zip
```

---

## Quick Start

### 1. Simple Comparison (Text Input)
```
"Compare React vs Vue for a SaaS dashboard"
```

**Output**: Executive summary with recommendation, pros/cons, confidence score

### 2. TCO Analysis (Structured Input)
```json
{
  "tco_analysis": {
    "technology": "AWS",
    "team_size": 8,
    "timeline_years": 5,
    "operational_costs": {
      "monthly_hosting": 3000
    }
  }
}
```

**Output**: 5-year TCO breakdown with cost optimization suggestions

### 3. Migration Assessment
```
"Assess migration from Angular.js to React. Codebase: 50,000 lines, 200 components, 6-person team."
```

**Output**: Complexity score, effort estimate, timeline, risk assessment, migration plan

### 4. Security & Compliance
```
"Analyze security of Express.js + MongoDB stack. Need SOC2 compliance."
```

**Output**: Security score, vulnerability analysis, compliance gaps, recommendations

---

## Usage Examples

See **[HOW_TO_USE.md](HOW_TO_USE.md)** for comprehensive examples including:
- 6 real-world scenarios
- All input format examples
- Advanced usage patterns
- Tips for best results
- Common questions and troubleshooting

---

## Metrics and Calculations

### Scoring Algorithms

**Technology Comparison (0-100 scale)**:
- 8 weighted criteria (performance, scalability, developer experience, ecosystem, learning curve, documentation, community, enterprise readiness)
- User-defined weights (defaults provided)
- Use-case specific adjustments (e.g., real-time workloads get performance bonus)
- Confidence calculation based on score gap

**Ecosystem Health (0-100 scale)**:
- GitHub: Stars, forks, contributors, commit frequency
- npm: Weekly downloads, version stability, dependencies count
- Community: Stack Overflow questions, job postings, tutorials, forums
- Corporate backing: Funding, company type
- Maintenance: Issue response time, resolution rate, release frequency

**Security Score (0-100 scale, A-F grade)**:
- Vulnerability count and severity (CVE database)
- Patch responsiveness (days to patch critical/high)
- Security features (encryption, auth, logging, etc.)
- Track record (years since major incident, certifications, audits)

**Migration Complexity (1-10 scale)**:
- Code volume (lines of code, files, components)
- Architecture changes (minimal to complete rewrite)
- Data migration (database size, schema changes)
- API compatibility (breaking changes)
- Dependency changes (percentage to replace)
- Testing requirements (coverage, test count)

### Financial Calculations

**TCO Components**:
- Initial: Licensing + Training (hours × rate × team size) + Migration + Setup + Tooling
- Operational (yearly): Licensing + Hosting (with growth) + Support + Maintenance (dev hours)
- Scaling: User projections × cost per user, Infrastructure scaling
- Hidden: Technical debt (15-20% of dev time) + Vendor lock-in risk + Security incidents + Downtime + Turnover

**ROI Calculation**:
- Productivity value = (Additional features per year) × (Feature value)
- Net TCO = Total TCO - Productivity value
- Break-even analysis

### Compliance Assessment

**Standards Supported**: GDPR, SOC2, HIPAA, PCI-DSS

**Readiness Levels**:
- **Ready (90-100%)**: Compliant, minor verification needed
- **Mostly Ready (70-89%)**: Minor gaps, additional configuration
- **Partial (50-69%)**: Significant work required
- **Not Ready (<50%)**: Major gaps, extensive implementation

**Required Features per Standard**:
- **GDPR**: Data privacy, consent management, data portability, right to deletion, audit logging
- **SOC2**: Access controls, encryption (at rest + transit), audit logging, backup/recovery
- **HIPAA**: PHI protection, encryption, access controls, audit logging
- **PCI-DSS**: Payment data encryption, access controls, network security, vulnerability management

---

## Best Practices

### For Accurate Evaluations
1. **Define Clear Use Case**: "Real-time collaboration platform" > "web app"
2. **Provide Complete Context**: Team size, skills, constraints, timeline
3. **Set Realistic Priorities**: Use weighted criteria (total = 100%)
4. **Consider Team Skills**: Factor in learning curve and existing expertise
5. **Think Long-Term**: Evaluate 3-5 year outlook

### For TCO Analysis
1. **Include All Costs**: Don't forget training, migration, technical debt
2. **Realistic Scaling**: Base on actual growth metrics
3. **Developer Productivity**: Time-to-market is a critical cost factor
4. **Hidden Costs**: Vendor lock-in, exit costs, technical debt
5. **Document Assumptions**: Make TCO assumptions explicit

### For Migration Decisions
1. **Risk Assessment First**: Identify showstoppers early
2. **Incremental Migration**: Avoid big-bang rewrites
3. **Prototype Critical Paths**: Test complex scenarios
4. **Rollback Plans**: Always have fallback strategy
5. **Baseline Metrics**: Measure current performance before migration

### For Security Evaluation
1. **Recent Vulnerabilities**: Focus on last 12 months
2. **Patch Response Time**: Fast patching > zero vulnerabilities
3. **Validate Claims**: Vendor claims ≠ actual compliance
4. **Supply Chain**: Evaluate security of all dependencies
5. **Test Features**: Don't assume features work as documented

---

## Limitations

### Data Accuracy
- **Ecosystem metrics**: Point-in-time snapshots (GitHub/npm data changes rapidly)
- **TCO calculations**: Estimates based on assumptions and market rates
- **Benchmark data**: May not reflect your specific configuration
- **Vulnerability data**: Depends on public CVE database completeness

### Scope Boundaries
- **Industry-specific requirements**: Some specialized needs not covered by standard analysis
- **Emerging technologies**: Very new tech (<1 year) may lack sufficient data
- **Custom/proprietary solutions**: Cannot evaluate closed-source tools without data
- **Organizational factors**: Cannot account for politics, vendor relationships, legacy commitments

### When NOT to Use
- **Trivial decisions**: Nearly-identical tools (use team preference)
- **Mandated solutions**: Technology choice already decided
- **Insufficient context**: Unknown requirements or priorities
- **Real-time production**: Use for planning, not emergencies
- **Non-technical decisions**: Business strategy, hiring, org issues

---

## Confidence Levels

All recommendations include confidence scores (0-100%):

- **High (80-100%)**: Strong data, clear winner, low risk
- **Medium (50-79%)**: Good data, trade-offs present, moderate risk
- **Low (<50%)**: Limited data, close call, high uncertainty
- **Insufficient Data**: Cannot recommend without more information

**Confidence based on**:
- Data completeness and recency
- Consensus across multiple metrics
- Clarity of use case requirements
- Industry maturity and standards

---

## Output Examples

### Executive Summary (200-300 tokens)
```markdown
# Technology Evaluation: React vs Vue

## Recommendation
**React is recommended for your SaaS dashboard project**
*Confidence: 78%*

### Top Strengths
- Larger ecosystem with 2.5× more packages available
- Stronger corporate backing (Meta) ensures long-term viability
- Higher job market demand (3× more job postings)

### Key Concerns
- Steeper learning curve (score: 65 vs Vue's 80)
- More complex state management patterns
- Requires additional libraries for routing, forms

### Decision Factors
- **Ecosystem**: React (score: 95)
- **Developer Experience**: Vue (score: 88)
- **Community Support**: React (score: 92)
```

### Comparison Matrix (Desktop)
```markdown
| Category              | Weight | React | Vue   |
|-----------------------|--------|-------|-------|
| Performance           | 15%    | 85.0  | 87.0  |
| Scalability           | 15%    | 90.0  | 85.0  |
| Developer Experience  | 20%    | 80.0  | 88.0  |
| Ecosystem             | 15%    | 95.0  | 82.0  |
| Learning Curve        | 10%    | 65.0  | 80.0  |
| Documentation         | 10%    | 92.0  | 90.0  |
| Community Support     | 10%    | 92.0  | 85.0  |
| Enterprise Readiness  | 5%     | 95.0  | 80.0  |
| **WEIGHTED TOTAL**    | 100%   | 85.3  | 84.9  |
```

### TCO Summary
```markdown
## Total Cost of Ownership: AWS (5 years)

**Total TCO**: $1,247,500
**Net TCO (after productivity gains)**: $987,300
**Average Yearly**: $249,500

### Initial Investment: $125,000
- Training: $40,000 (10 devs × 40 hours × $100/hr)
- Migration: $50,000
- Setup & Tooling: $35,000

### Key Cost Drivers
- Infrastructure/hosting ($625,000 over 5 years)
- Developer maintenance time ($380,000)
- Technical debt accumulation ($87,500)

### Optimization Opportunities
- Improve scaling efficiency - costs growing 25% YoY
- Address technical debt accumulation
- Consider reserved instances for 30% hosting savings
```

---

## Version History

### v1.0.0 (2025-11-05)
- Initial release
- 8 comprehensive evaluation capabilities
- 7 Python modules (2,774 lines)
- Automatic format detection (text, YAML, JSON, URLs)
- Context-aware output (Desktop vs CLI)
- Modular reporting with progressive disclosure
- Complete documentation with 6+ usage examples

---

## Dependencies

**Python Standard Library Only** - No external dependencies required:
- `typing` - Type hints
- `json` - JSON parsing
- `re` - Regular expressions
- `datetime` - Date/time operations
- `os` - Environment detection
- `platform` - Platform information

**Why no external dependencies?**
- Ensures compatibility across all Claude environments
- No installation or version conflicts
- Faster loading and execution
- Simpler deployment

---

## Support and Feedback

### Getting Help
1. Review **[HOW_TO_USE.md](HOW_TO_USE.md)** for detailed examples
2. Check sample input files for format references
3. Start with conversational text input (easiest)
4. Request specific sections if full report is overwhelming

### Improving Results
If recommendations don't match expectations:
- **Clarify use case**: Be more specific about requirements
- **Adjust priorities**: Set custom weights for criteria
- **Provide more context**: Team skills, constraints, business goals
- **Request specific sections**: Focus on most relevant analyses

### Known Issues
- Very new technologies (<6 months) may have limited ecosystem data
- Proprietary/closed-source tools require manual data input
- Compliance assessment is guidance, not legal certification

---

## Contributing

This skill is part of the Claude Skills Factory. To contribute improvements:
1. Test changes with multiple scenarios
2. Maintain Python standard library only (no external deps)
3. Update documentation to match code changes
4. Preserve token efficiency (200-300 token summaries)
5. Validate all calculations with real-world data

---

## License

Part of Claude Skills Factory
© 2025 Claude Skills Factory
Licensed under MIT License

---

## Related Skills

- **prompt-factory**: Generate domain-specific prompts
- **aws-solution-architect**: AWS-specific architecture evaluation
- **psychology-advisor**: Decision-making psychology
- **content-researcher**: Technology trend research

---

**Ready to evaluate your tech stack?** See [HOW_TO_USE.md](HOW_TO_USE.md) for quick start examples!
