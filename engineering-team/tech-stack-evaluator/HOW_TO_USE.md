# How to Use the Technology Stack Evaluator Skill

The Technology Stack Evaluator skill provides comprehensive evaluation and comparison of technologies, frameworks, and complete technology stacks for engineering teams.

## Quick Start Examples

### Example 1: Simple Technology Comparison

**Conversational (Easiest)**:
```
Hey Claude—I just added the "tech-stack-evaluator" skill. Can you compare React vs Vue for building a SaaS dashboard?
```

**What you'll get**:
- Executive summary with recommendation
- Comparison matrix with scores
- Top 3 pros and cons for each
- Confidence level
- Key decision factors

---

### Example 2: Complete Stack Evaluation

```
Hey Claude—I just added the "tech-stack-evaluator" skill. Can you evaluate this technology stack for a real-time collaboration platform:
- Frontend: Next.js
- Backend: Node.js + Express
- Database: PostgreSQL
- Real-time: WebSockets
- Hosting: AWS

Include TCO analysis and ecosystem health assessment.
```

**What you'll get**:
- Complete stack evaluation
- TCO breakdown (5-year projection)
- Ecosystem health scores
- Security assessment
- Detailed recommendations

---

### Example 3: Migration Analysis

```
Hey Claude—I just added the "tech-stack-evaluator" skill. We're considering migrating from Angular.js (1.x) to React. Our codebase:
- 75,000 lines of code
- 300 components
- 8-person development team
- Must minimize downtime

Can you assess migration complexity, effort, risks, and timeline?
```

**What you'll get**:
- Migration complexity score (1-10)
- Effort estimate (person-months and timeline)
- Risk assessment (technical, business, team)
- Phased migration plan
- Success criteria

---

### Example 4: TCO Analysis

```
Hey Claude—I just added the "tech-stack-evaluator" skill. Calculate total cost of ownership for AWS vs Azure for our workload:
- 50 EC2/VM instances (growing 25% annually)
- 20TB database storage
- Team: 12 developers
- 5-year projection

Include hidden costs like technical debt and vendor lock-in.
```

**What you'll get**:
- 5-year TCO breakdown
- Initial vs operational costs
- Scaling cost projections
- Cost per user metrics
- Hidden costs (technical debt, vendor lock-in, downtime)
- Cost optimization opportunities

---

### Example 5: Security & Compliance Assessment

```
Hey Claude—I just added the "tech-stack-evaluator" skill. Assess the security posture of our current stack:
- Express.js (Node.js)
- MongoDB
- JWT authentication
- Hosted on AWS

We need SOC2 and GDPR compliance. What are the gaps?
```

**What you'll get**:
- Security score (0-100) with grade
- Vulnerability analysis (CVE counts by severity)
- Compliance readiness for SOC2 and GDPR
- Missing security features
- Recommendations to improve security

---

### Example 6: Cloud Provider Comparison

```
Hey Claude—I just added the "tech-stack-evaluator" skill. Compare AWS vs Azure vs GCP for machine learning workloads:
- Priorities: GPU availability (40%), Cost (30%), ML ecosystem (20%), Support (10%)
- Need: High GPU availability for model training
- Team: 5 ML engineers, experienced with Python

Generate weighted decision matrix.
```

**What you'll get**:
- Weighted comparison matrix
- Scores across all criteria
- Best performer by category
- Overall recommendation with confidence
- Pros/cons for each provider

---

## Input Formats Supported

### 1. Conversational Text (Easiest)
Just describe what you want in natural language:
```
"Compare PostgreSQL vs MongoDB for a SaaS application"
"Evaluate security of our Express.js + JWT stack"
"Calculate TCO for migrating to microservices"
```

### 2. Structured JSON
For precise control over evaluation parameters:
```json
{
  "comparison": {
    "technologies": ["React", "Vue", "Svelte"],
    "use_case": "Enterprise dashboard",
    "weights": {
      "performance": 25,
      "developer_experience": 30,
      "ecosystem": 25,
      "learning_curve": 20
    }
  }
}
```

### 3. YAML (Alternative Structured Format)
```yaml
comparison:
  technologies:
    - React
    - Vue
  use_case: SaaS dashboard
  priorities:
    - Developer productivity
    - Ecosystem maturity
```

### 4. URLs for Ecosystem Analysis
```
"Analyze ecosystem health for these technologies:
- https://github.com/facebook/react
- https://github.com/vuejs/vue
- https://www.npmjs.com/package/react"
```

The skill automatically detects the format and parses accordingly!

---

## Report Sections Available

You can request specific sections or get the full report:

### Available Sections:
1. **Executive Summary** (200-300 tokens) - Recommendation + top pros/cons
2. **Comparison Matrix** - Weighted scoring across all criteria
3. **TCO Analysis** - Complete cost breakdown (initial + operational + hidden)
4. **Ecosystem Health** - Community size, maintenance, viability
5. **Security Assessment** - Vulnerabilities, compliance readiness
6. **Migration Analysis** - Complexity, effort, risks, timeline
7. **Performance Benchmarks** - Throughput, latency, resource usage

### Request Specific Sections:
```
"Compare Next.js vs Nuxt.js. Include only: ecosystem health and performance benchmarks. Skip TCO and migration analysis."
```

---

## What to Provide

### For Technology Comparison:
- Technologies to compare (2-5 recommended)
- Use case or application type (optional but helpful)
- Priorities/weights (optional, uses sensible defaults)

### For TCO Analysis:
- Technology/platform name
- Team size
- Current costs (hosting, licensing, support)
- Growth projections (user growth, scaling needs)
- Developer productivity factors (optional)

### For Migration Assessment:
- Source technology (current stack)
- Target technology (desired stack)
- Codebase statistics (lines of code, number of components)
- Team information (size, experience level)
- Constraints (downtime tolerance, timeline)

### For Security Assessment:
- Technology stack components
- Security features currently implemented
- Compliance requirements (GDPR, SOC2, HIPAA, PCI-DSS)
- Known vulnerabilities (if any)

### For Ecosystem Analysis:
- Technology name or GitHub/npm URL
- Specific metrics of interest (optional)

---

## Output Formats

The skill adapts output based on your environment:

### Claude Desktop (Rich Markdown)
- Formatted tables with visual indicators
- Expandable sections
- Color-coded scores (via markdown formatting)
- Decision matrices

### CLI/Terminal (Terminal-Friendly)
- ASCII tables
- Compact formatting
- Plain text output
- Copy-paste friendly

The skill automatically detects your environment!

---

## Advanced Usage

### Custom Weighted Criteria:
```
"Compare React vs Vue vs Svelte.
Priorities (weighted):
- Developer experience: 35%
- Performance: 30%
- Ecosystem: 20%
- Learning curve: 15%"
```

### Multiple Analysis Types:
```
"Evaluate Next.js for our enterprise SaaS platform.
Include: TCO (5-year), ecosystem health, security assessment, and performance vs Nuxt.js."
```

### Progressive Disclosure:
```
"Compare AWS vs Azure. Start with executive summary only."

(After reviewing summary)
"Show me the detailed TCO breakdown for AWS."
```

---

## Tips for Best Results

1. **Be Specific About Use Case**: "Real-time collaboration platform" is better than "web app"

2. **Provide Context**: Team size, experience level, constraints help generate better recommendations

3. **Set Clear Priorities**: If cost is more important than performance, say so with weights

4. **Request Incremental Analysis**: Start with executive summary, then drill into specific sections

5. **Include Constraints**: Zero-downtime requirement, budget limits, timeline pressure

6. **Validate Assumptions**: Review the TCO assumptions and adjust if needed

---

## Common Questions

**Q: How current is the data?**
A: The skill uses current data sources when available (GitHub, npm, CVE databases). Ecosystem metrics are point-in-time snapshots.

**Q: Can I compare more than 2 technologies?**
A: Yes! You can compare 2-5 technologies. More than 5 becomes less actionable.

**Q: What if I don't know the exact data for TCO analysis?**
A: The skill uses industry-standard defaults. Just provide what you know (team size, rough costs) and it will fill in reasonable estimates.

**Q: Can I export reports?**
A: Yes! The skill can generate markdown reports that you can save or export.

**Q: How do confidence scores work?**
A: Confidence (0-100%) is based on:
- Score gap between options (larger gap = higher confidence)
- Data completeness
- Clarity of requirements

**Q: What if technologies are very close in scores?**
A: The skill will report low confidence and highlight that it's a close call, helping you understand there's no clear winner.

---

## Need Help?

If results aren't what you expected:
1. **Clarify your use case** - Be more specific about requirements
2. **Adjust priorities** - Set custom weights for what matters most
3. **Provide more context** - Team skills, constraints, business goals
4. **Request specific sections** - Focus on what's most relevant

Example clarification:
```
"The comparison seemed to favor React, but we're a small team (3 devs) with no React experience. Can you re-evaluate with learning curve weighted at 40%?"
```

The skill will adjust the analysis based on your refined requirements!
