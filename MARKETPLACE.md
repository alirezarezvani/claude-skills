# Claude Skills Marketplace

> Production-ready skill packages for Claude AI - 42 expert skills across marketing, engineering, product, compliance, and leadership domains.

This repository is a Claude Code plugin marketplace containing 10 granular plugin collections, each focused on specific professional domains and use cases.

## Quick Start

### Add the Marketplace

```bash
# Add via GitHub (recommended)
/plugin marketplace add alirezarezvani/claude-skills

# Or add via git URL
/plugin marketplace add https://github.com/alirezarezvani/claude-skills.git

# Or add local development version
/plugin marketplace add /path/to/claude-skills
```

### Browse Available Plugins

```bash
# Open interactive plugin browser
/plugin

# List all installed marketplaces
/plugin marketplace list
```

### Install Plugins

```bash
# Install specific plugin from marketplace
/plugin install marketing-skills@nginity-claude-skills
/plugin install core-engineering@nginity-claude-skills

# Browse and install interactively
/plugin
```

## Available Plugin Collections

### 1. Marketing Skills (3 skills)
**Install:** `/plugin install marketing-skills@nginity-claude-skills`

Complete marketing toolkit with content creation, demand generation, and product marketing strategy.

**Included Skills:**
- **content-creator**: SEO-optimized content with brand voice analysis
- **marketing-demand-acquisition**: Lead generation and acquisition strategies
- **marketing-strategy-pmm**: Product marketing and go-to-market planning

**Use Cases:**
- Creating blog posts and social media content
- SEO optimization and keyword research
- Brand voice consistency analysis
- Content calendar planning
- Demand generation campaigns

**Python Tools:** `brand_voice_analyzer.py`, `seo_optimizer.py`

---

### 2. Executive Advisory (2 skills)
**Install:** `/plugin install executive-advisory@nginity-claude-skills`

Strategic leadership advisory for C-level executives with decision frameworks and technical guidance.

**Included Skills:**
- **ceo-advisor**: Strategic planning and business decision frameworks
- **cto-advisor**: Technical leadership and engineering strategy

**Use Cases:**
- Strategic planning and OKR setting
- Technical architecture decisions
- Team scaling and organization design
- Investment and resource allocation
- Executive decision-making frameworks

---

### 3. Product Management (3 skills)
**Install:** `/plugin install product-management@nginity-claude-skills`

Complete product management toolkit with RICE prioritization, agile delivery, and product strategy.

**Included Skills:**
- **product-manager-toolkit**: RICE prioritization, customer interviews, roadmapping
- **agile-product-owner**: User story generation, sprint planning, backlog management
- **product-strategist**: OKR cascade, strategy frameworks, market analysis

**Use Cases:**
- Feature prioritization with RICE framework
- User story and acceptance criteria creation
- Sprint planning and capacity management
- Product roadmap development
- Customer interview analysis
- OKR cascade and alignment

**Python Tools:** `rice_prioritizer.py`, `customer_interview_analyzer.py`, `user_story_generator.py`, `okr_cascade_generator.py`

---

### 4. UX Design Skills (2 skills)
**Install:** `/plugin install ux-design-skills@nginity-claude-skills`

UX research, UI design systems, persona generation, and design token automation.

**Included Skills:**
- **ux-researcher-designer**: User research, persona generation, usability testing
- **ui-design-system**: Design tokens, component libraries, style guides

**Use Cases:**
- User persona creation and validation
- Design system development
- Automated design token generation
- Usability testing planning
- Component library documentation

**Python Tools:** `persona_generator.py`, `design_token_generator.py`

---

### 5. Project Management (6 skills)
**Install:** `/plugin install project-management@nginity-claude-skills`

Complete project management suite covering PM, Scrum, Jira, Confluence, and Atlassian administration.

**Included Skills:**
- **senior-pm**: Project planning, risk management, stakeholder communication
- **scrum-master**: Sprint facilitation, agile ceremonies, team coaching
- **jira-expert**: Jira administration, workflow optimization, reporting
- **confluence-expert**: Documentation strategy, knowledge management
- **atlassian-admin**: Atlassian suite administration and integration
- **atlassian-templates**: Ready-to-use Jira and Confluence templates

**Use Cases:**
- Sprint planning and retrospectives
- Jira workflow configuration
- Confluence documentation structure
- Team capacity planning
- Agile transformation
- Project reporting and dashboards

---

### 6. Core Engineering (9 skills)
**Install:** `/plugin install core-engineering@nginity-claude-skills`

Complete engineering team skills from architecture to fullstack, QA, DevOps, and security.

**Included Skills:**
- **senior-architect**: System design, architecture patterns, technical decision-making
- **senior-frontend**: React, Next.js, TypeScript, modern frontend development
- **senior-backend**: Node.js, APIs, databases, microservices
- **senior-fullstack**: Complete stack development, project scaffolding
- **senior-qa**: Test automation, quality assurance, testing strategies
- **senior-devops**: CI/CD, Docker, Kubernetes, infrastructure automation
- **senior-secops**: Security operations, vulnerability management
- **code-reviewer**: Code review best practices, quality standards
- **senior-security**: Application security, penetration testing, security architecture

**Use Cases:**
- System architecture design
- Full-stack application development
- CI/CD pipeline setup
- Code quality analysis
- Security audits and vulnerability scanning
- Infrastructure as code
- Test automation frameworks

**Python Tools:** `project_scaffolder.py`, `code_quality_analyzer.py`, `fullstack_scaffolder.py`

---

### 7. AI/ML/Data Engineering (5 skills)
**Install:** `/plugin install ai-ml-data-engineering@nginity-claude-skills`

AI/ML and data engineering skills including data science, ML engineering, and computer vision.

**Included Skills:**
- **senior-data-scientist**: Statistical analysis, experimentation, feature engineering
- **senior-data-engineer**: Data pipelines, ETL/ELT, data quality
- **senior-ml-engineer**: Model deployment, MLOps, production ML systems
- **senior-prompt-engineer**: LLM optimization, RAG systems, AI agents
- **senior-computer-vision**: Object detection, image processing, video analysis

**Use Cases:**
- A/B test design and statistical analysis
- Data pipeline orchestration
- ML model deployment and monitoring
- LLM prompt optimization
- Computer vision model training
- Feature engineering pipelines
- RAG system development

**Python Tools:** `experiment_designer.py`, `pipeline_orchestrator.py`, `model_deployment_pipeline.py`, `prompt_optimizer.py`, `vision_model_trainer.py`

---

### 8. Regulatory Affairs (4 skills)
**Install:** `/plugin install regulatory-affairs@nginity-claude-skills`

HealthTech/MedTech regulatory compliance including MDR 2017/745, FDA, and risk management.

**Included Skills:**
- **regulatory-affairs-head**: Regulatory strategy, submissions, compliance oversight
- **mdr-745-specialist**: EU MDR 2017/745 compliance and implementation
- **fda-consultant-specialist**: FDA 510(k), PMA, quality system regulations
- **risk-management-specialist**: ISO 14971 risk management process

**Use Cases:**
- Regulatory submission preparation
- MDR compliance documentation
- FDA regulatory pathway selection
- Risk management file creation
- Post-market surveillance
- Technical file compilation

---

### 9. Quality Management (5 skills)
**Install:** `/plugin install quality-management@nginity-claude-skills`

Quality management systems covering QMR, ISO 13485, CAPA, and ISO 27001.

**Included Skills:**
- **quality-manager-qmr**: Quality management representative role
- **quality-manager-qms-iso13485**: ISO 13485 QMS implementation
- **capa-officer**: Corrective and preventive action management
- **quality-documentation-manager**: Document control and management
- **information-security-manager-iso27001**: ISO 27001 ISMS implementation

**Use Cases:**
- QMS documentation and implementation
- CAPA investigation and closure
- Management review preparation
- Document control systems
- Information security management
- Internal audit execution

---

### 10. Audit & Compliance (3 skills)
**Install:** `/plugin install audit-compliance@nginity-claude-skills`

Audit and compliance expertise including QMS, ISMS, and GDPR compliance.

**Included Skills:**
- **qms-audit-expert**: Quality management system auditing
- **isms-audit-expert**: Information security management system auditing
- **gdpr-dsgvo-expert**: GDPR/DSGVO compliance and data protection

**Use Cases:**
- Internal quality audits
- External audit preparation
- GDPR compliance assessment
- Information security audits
- Non-conformance management
- Audit finding resolution

---

## Team Configuration

Configure automatic marketplace installation for team projects by adding to `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "nginity-claude-skills": {
      "source": {
        "source": "github",
        "repo": "alirezarezvani/claude-skills"
      }
    }
  },
  "enabledPlugins": [
    "marketing-skills",
    "core-engineering",
    "product-management"
  ]
}
```

When team members trust the repository folder, Claude Code automatically installs the marketplace and specified plugins.

## Skill Structure

Each skill includes:

- **SKILL.md**: Master documentation with workflows and usage examples
- **scripts/**: Python CLI tools for algorithmic analysis (2-3 per skill)
- **references/**: Expert knowledge bases with frameworks and best practices
- **assets/**: User-facing templates and checklists (where applicable)

## Python Tools

97 production-ready Python automation tools are included across all skills:

### Running Tools

```bash
# Marketing tools
python marketing-skill/content-creator/scripts/brand_voice_analyzer.py content.txt
python marketing-skill/content-creator/scripts/seo_optimizer.py article.md "keyword"

# Product tools
python product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv
python product-team/agile-product-owner/scripts/user_story_generator.py sprint 30

# Engineering tools
python engineering-team/senior-fullstack/scripts/project_scaffolder.py my-app --type nextjs-graphql
python engineering-team/senior-fullstack/scripts/code_quality_analyzer.py /path/to/project

# Data/ML tools
python engineering-team/senior-data-scientist/scripts/experiment_designer.py
python engineering-team/senior-ml-engineer/scripts/model_deployment_pipeline.py
```

## Troubleshooting

### Marketplace not loading

**Issue:** Can't add marketplace or see plugins

**Solutions:**
- Verify repository URL is accessible
- Check `.claude-plugin/marketplace.json` exists
- Ensure you have access to private repositories (if applicable)
- Try adding with full git URL instead of shorthand

### Plugin installation fails

**Issue:** Marketplace appears but plugin won't install

**Solutions:**
- Verify skill paths in marketplace.json
- Check that SKILL.md files exist in specified locations
- Try installing from local clone for debugging
- Review Claude Code logs for specific errors

### Skills not appearing in Claude

**Issue:** Plugin installed but skills aren't available

**Solutions:**
- Restart Claude Code session
- Verify plugin is listed in `/plugin list`
- Check that skills are enabled in settings
- Ensure SKILL.md has valid YAML frontmatter

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch for new skills
3. Follow existing skill structure and conventions
4. Test locally before submitting PR
5. Update marketplace.json with new skills

## License

MIT License - see LICENSE file for details.

## Support

- **Issues:** https://github.com/alirezarezvani/claude-skills/issues
- **Documentation:** See individual SKILL.md files
- **Email:** contact@nginity.io

---

**Total Skills:** 42 production-ready skills
**Total Tools:** 97 Python automation tools
**Total Plugins:** 10 granular collections
**Domains Covered:** Marketing, Engineering, Product, Compliance, Leadership
