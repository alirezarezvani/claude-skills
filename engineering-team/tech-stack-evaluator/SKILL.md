---
name: tech-stack-evaluator
description: Comprehensive technology stack evaluation and comparison tool with TCO analysis, security assessment, and intelligent recommendations for engineering teams
---

# Technology Stack Evaluator

A comprehensive evaluation framework for comparing technologies, frameworks, cloud providers, and complete technology stacks. Provides data-driven recommendations with TCO analysis, security assessment, ecosystem health scoring, and migration path analysis.

## Capabilities

This skill provides eight comprehensive evaluation capabilities:

- **Technology Comparison**: Head-to-head comparisons of frameworks, languages, and tools (React vs Vue, PostgreSQL vs MongoDB, Node.js vs Python)
- **Stack Evaluation**: Assess complete technology stacks for specific use cases (real-time collaboration, API-heavy SaaS, data-intensive platforms)
- **Maturity & Ecosystem Analysis**: Evaluate community health, maintenance status, long-term viability, and ecosystem strength
- **Total Cost of Ownership (TCO)**: Calculate comprehensive costs including licensing, hosting, developer productivity, and scaling
- **Security & Compliance**: Analyze vulnerabilities, compliance readiness (GDPR, SOC2, HIPAA), and security posture
- **Migration Path Analysis**: Assess migration complexity, risks, timelines, and strategies from legacy to modern stacks
- **Cloud Provider Comparison**: Compare AWS vs Azure vs GCP for specific workloads with cost and feature analysis
- **Decision Reports**: Generate comprehensive decision matrices with pros/cons, confidence scores, and actionable recommendations

## Input Requirements

### Flexible Input Formats (Automatic Detection)

The skill automatically detects and processes multiple input formats:

**Text/Conversational**:
```
"Compare React vs Vue for building a SaaS dashboard"
"Evaluate technology stack for real-time collaboration platform"
"Should we migrate from MongoDB to PostgreSQL?"
```

**Structured (YAML)**:
```yaml
comparison:
  technologies:
    - name: "React"
    - name: "Vue"
  use_case: "SaaS dashboard"
  priorities:
    - "Developer productivity"
    - "Ecosystem maturity"
    - "Performance"
```

**Structured (JSON)**:
```json
{
  "comparison": {
    "technologies": ["React", "Vue"],
    "use_case": "SaaS dashboard",
    "priorities": ["Developer productivity", "Ecosystem maturity"]
  }
}
```

**URLs for Ecosystem Analysis**:
- GitHub repository URLs (for health scoring)
- npm package URLs (for download statistics)
- Technology documentation URLs (for feature extraction)

### Analysis Scope Selection

Users can select which analyses to run:
- **Quick Comparison**: Basic scoring and comparison (200-300 tokens)
- **Standard Analysis**: Scoring + TCO + Security (500-800 tokens)
- **Comprehensive Report**: All analyses including migration paths (1200-1500 tokens)
- **Custom**: User selects specific sections (modular)

## Output Formats

### Context-Aware Output

The skill automatically adapts output based on environment:

**Claude Desktop (Rich Markdown)**:
- Formatted tables with color indicators
- Expandable sections for detailed analysis
- Visual decision matrices
- Charts and graphs (when appropriate)

**CLI/Terminal (Terminal-Friendly)**:
- Plain text tables with ASCII borders
- Compact formatting
- Clear section headers
- Copy-paste friendly code blocks

### Progressive Disclosure Structure

**Executive Summary (200-300 tokens)**:
- Recommendation summary
- Top 3 pros and cons
- Confidence level (High/Medium/Low)
- Key decision factors

**Detailed Breakdown (on-demand)**:
- Complete scoring matrices
- Detailed TCO calculations
- Full security analysis
- Migration complexity assessment
- All supporting data and calculations

### Report Sections (User-Selectable)

Users choose which sections to include:

1. **Scoring & Comparison Matrix**
   - Weighted decision scores
   - Head-to-head comparison tables
   - Strengths and weaknesses

2. **Financial Analysis**
   - TCO breakdown (5-year projection)
   - ROI analysis
   - Cost per user/request metrics
   - Hidden cost identification

3. **Ecosystem Health**
   - Community size and activity
   - GitHub stars, npm downloads
   - Release frequency and maintenance
   - Issue response times
   - Viability assessment

4. **Security & Compliance**
   - Vulnerability count (CVE database)
   - Security patch frequency
   - Compliance readiness (GDPR, SOC2, HIPAA)
   - Security scoring

5. **Migration Analysis** (when applicable)
   - Migration complexity scoring
   - Code change estimates
   - Data migration requirements
   - Downtime assessment
   - Risk mitigation strategies

6. **Performance Benchmarks**
   - Throughput/latency comparisons
   - Resource usage analysis
   - Scalability characteristics

## How to Use

### Basic Invocations

**Quick Comparison**:
```
"Compare React vs Vue for our SaaS dashboard project"
"PostgreSQL vs MongoDB for our application"
```

**Stack Evaluation**:
```
"Evaluate technology stack for real-time collaboration platform:
Node.js, WebSockets, Redis, PostgreSQL"
```

**TCO Analysis**:
```
"Calculate total cost of ownership for AWS vs Azure for our workload:
- 50 EC2/VM instances
- 10TB storage
- High bandwidth requirements"
```

**Security Assessment**:
```
"Analyze security posture of our current stack:
Express.js, MongoDB, JWT authentication.
Need SOC2 compliance."
```

**Migration Path**:
```
"Assess migration from Angular.js (1.x) to React.
Application has 50,000 lines of code, 200 components."
```

### Advanced Invocations

**Custom Analysis Sections**:
```
"Compare Next.js vs Nuxt.js.
Include: Ecosystem health, TCO, and performance benchmarks.
Skip: Migration analysis, compliance."
```

**Weighted Decision Criteria**:
```
"Compare cloud providers for ML workloads.
Priorities (weighted):
- GPU availability (40%)
- Cost (30%)
- Ecosystem (20%)
- Support (10%)"
```

**Multi-Technology Comparison**:
```
"Compare: React, Vue, Svelte, Angular for enterprise SaaS.
Use case: Large team (20+ developers), complex state management.
Generate comprehensive decision matrix."
```

## Scripts

### Core Modules

- **`stack_comparator.py`**: Main comparison engine with weighted scoring algorithms
- **`tco_calculator.py`**: Total Cost of Ownership calculations (licensing, hosting, developer productivity, scaling)
- **`ecosystem_analyzer.py`**: Community health scoring, GitHub/npm metrics, viability assessment
- **`security_assessor.py`**: Vulnerability analysis, compliance readiness, security scoring
- **`migration_analyzer.py`**: Migration complexity scoring, risk assessment, effort estimation
- **`format_detector.py`**: Automatic input format detection (text, YAML, JSON, URLs)
- **`report_generator.py`**: Context-aware report generation with progressive disclosure

### Utility Modules

- **`data_fetcher.py`**: Fetch real-time data from GitHub, npm, CVE databases
- **`benchmark_processor.py`**: Process and normalize performance benchmark data
- **`confidence_scorer.py`**: Calculate confidence levels for recommendations

## Metrics and Calculations

### 1. Scoring & Comparison Metrics

**Technology Comparison Matrix**:
- Feature completeness (0-100 scale)
- Learning curve assessment (Easy/Medium/Hard)
- Developer experience scoring
- Documentation quality (0-10 scale)
- Weighted total scores

**Decision Scoring Algorithm**:
- User-defined weights for criteria
- Normalized scoring (0-100)
- Confidence intervals
- Sensitivity analysis

### 2. Financial Calculations

**TCO Components**:
- **Initial Costs**: Licensing, training, migration
- **Operational Costs**: Hosting, support, maintenance (monthly/yearly)
- **Scaling Costs**: Per-user costs, infrastructure scaling projections
- **Developer Productivity**: Time-to-market impact, development speed multipliers
- **Hidden Costs**: Technical debt, vendor lock-in risks

**ROI Calculations**:
- Cost savings projections (3-year, 5-year)
- Productivity gains (developer hours saved)
- Break-even analysis
- Risk-adjusted returns

**Cost Per Metric**:
- Cost per user (monthly/yearly)
- Cost per API request
- Cost per GB stored/transferred
- Cost per compute hour

### 3. Maturity & Ecosystem Metrics

**Health Scoring (0-100 scale)**:
- **GitHub Metrics**: Stars, forks, contributors, commit frequency
- **npm Metrics**: Weekly downloads, version stability, dependency count
- **Release Cadence**: Regular releases, semantic versioning adherence
- **Issue Management**: Response time, resolution rate, open vs closed issues

**Community Metrics**:
- Active maintainers count
- Contributor growth rate
- Stack Overflow question volume
- Job market demand (job postings analysis)

**Viability Assessment**:
- Corporate backing strength
- Community sustainability
- Alternative availability
- Long-term risk scoring

### 4. Security & Compliance Metrics

**Security Scoring**:
- **CVE Count**: Known vulnerabilities (last 12 months, last 3 years)
- **Severity Distribution**: Critical/High/Medium/Low vulnerability counts
- **Patch Frequency**: Average time to patch (days)
- **Security Track Record**: Historical security posture

**Compliance Readiness**:
- **GDPR**: Data privacy features, consent management, data portability
- **SOC2**: Access controls, encryption, audit logging
- **HIPAA**: PHI handling, encryption standards, access controls
- **PCI-DSS**: Payment data security (if applicable)

**Compliance Scoring (per standard)**:
- Ready: 90-100% compliant
- Mostly Ready: 70-89% (minor gaps)
- Partial: 50-69% (significant work needed)
- Not Ready: <50% (major gaps)

### 5. Migration Analysis Metrics

**Complexity Scoring (1-10 scale)**:
- **Code Changes**: Estimated lines of code affected
- **Architecture Impact**: Breaking changes, API compatibility
- **Data Migration**: Schema changes, data transformation complexity
- **Downtime Requirements**: Zero-downtime possible vs planned outage

**Effort Estimation**:
- Development hours (by component)
- Testing hours
- Training hours
- Total person-months

**Risk Assessment**:
- **Technical Risks**: API incompatibilities, performance regressions
- **Business Risks**: Downtime impact, feature parity gaps
- **Team Risks**: Learning curve, skill gaps
- **Mitigation Strategies**: Risk-specific recommendations

**Migration Phases**:
- Phase 1: Planning and prototyping (timeline, effort)
- Phase 2: Core migration (timeline, effort)
- Phase 3: Testing and validation (timeline, effort)
- Phase 4: Deployment and monitoring (timeline, effort)

### 6. Performance Benchmark Metrics

**Throughput/Latency**:
- Requests per second (RPS)
- Average response time (ms)
- P95/P99 latency percentiles
- Concurrent user capacity

**Resource Usage**:
- Memory consumption (MB/GB)
- CPU utilization (%)
- Storage requirements
- Network bandwidth

**Scalability Characteristics**:
- Horizontal scaling efficiency
- Vertical scaling limits
- Cost per performance unit
- Scaling inflection points

## Best Practices

### For Accurate Evaluations

1. **Define Clear Use Case**: Specify exact requirements, constraints, and priorities
2. **Provide Complete Context**: Team size, existing stack, timeline, budget constraints
3. **Set Realistic Priorities**: Use weighted criteria (total = 100%) for multi-factor decisions
4. **Consider Team Skills**: Factor in learning curve and existing expertise
5. **Think Long-Term**: Evaluate 3-5 year outlook, not just immediate needs

### For TCO Analysis

1. **Include All Cost Components**: Don't forget training, migration, technical debt
2. **Use Realistic Scaling Projections**: Base on actual growth metrics, not wishful thinking
3. **Account for Developer Productivity**: Time-to-market and development speed are critical costs
4. **Consider Hidden Costs**: Vendor lock-in, exit costs, technical debt accumulation
5. **Validate Assumptions**: Document all TCO assumptions for review

### For Migration Decisions

1. **Start with Risk Assessment**: Identify showstoppers early
2. **Plan Incremental Migration**: Avoid big-bang rewrites when possible
3. **Prototype Critical Paths**: Test complex migration scenarios before committing
4. **Build Rollback Plans**: Always have a fallback strategy
5. **Measure Baseline Performance**: Establish current metrics before migration

### For Security Evaluation

1. **Check Recent Vulnerabilities**: Focus on last 12 months for current security posture
2. **Review Patch Response Time**: Fast patching is more important than zero vulnerabilities
3. **Validate Compliance Claims**: Vendor claims ≠ actual compliance readiness
4. **Consider Supply Chain**: Evaluate security of all dependencies
5. **Test Security Features**: Don't assume features work as documented

## Limitations

### Data Accuracy

- **Ecosystem metrics** are point-in-time snapshots (GitHub stars, npm downloads change rapidly)
- **TCO calculations** are estimates based on provided assumptions and market rates
- **Benchmark data** may not reflect your specific use case or configuration
- **Security vulnerability counts** depend on public CVE database completeness

### Scope Boundaries

- **Industry-Specific Requirements**: Some specialized industries may have unique constraints not covered by standard analysis
- **Emerging Technologies**: Very new technologies (<1 year old) may lack sufficient data for accurate assessment
- **Custom/Proprietary Solutions**: Cannot evaluate closed-source or internal tools without data
- **Political/Organizational Factors**: Cannot account for company politics, vendor relationships, or legacy commitments

### Contextual Limitations

- **Team Skill Assessment**: Cannot directly evaluate your team's specific skills and learning capacity
- **Existing Architecture**: Recommendations assume greenfield unless migration context provided
- **Budget Constraints**: TCO analysis provides costs but cannot make budget decisions for you
- **Timeline Pressure**: Cannot account for business deadlines and time-to-market urgency

### When NOT to Use This Skill

- **Trivial Decisions**: Choosing between nearly-identical tools (use team preference)
- **Mandated Solutions**: When technology choice is already decided by management/policy
- **Insufficient Context**: When you don't know your requirements, priorities, or constraints
- **Real-Time Production Decisions**: Use for planning, not emergency production issues
- **Non-Technical Decisions**: Business strategy, hiring, organizational issues

## Confidence Levels

The skill provides confidence scores with all recommendations:

- **High Confidence (80-100%)**: Strong data, clear winner, low risk
- **Medium Confidence (50-79%)**: Good data, trade-offs present, moderate risk
- **Low Confidence (<50%)**: Limited data, close call, high uncertainty
- **Insufficient Data**: Cannot make recommendation without more information

Confidence is based on:
- Data completeness and recency
- Consensus across multiple metrics
- Clarity of use case requirements
- Industry maturity and standards
