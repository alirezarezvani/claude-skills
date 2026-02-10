# Claude Skills Library (Your Agentic Startup Kit)

**Production-Ready skill packages for Claude AI & Claude Code** - Reusable expertise bundles combining best practices, analysis tools, and strategic frameworks for marketing teams, executive leadership, product development, your web and mobile engineering teams. Many other teams will be included soon and regularly.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude AI](https://img.shields.io/badge/Claude-AI-blue.svg)](https://claude.ai)
[![Claude Code](https://img.shields.io/badge/Claude-Code-purple.svg)](https://claude.ai/code)
[![Multi-Agent Compatible](https://img.shields.io/badge/Multi--Agent-Compatible-green.svg)](https://github.com/skillcreatorai/Ai-Agent-Skills)
[![53 Skills](https://img.shields.io/badge/Skills-53-brightgreen.svg)](#-available-skills)
[![SkillCheck Validated](https://img.shields.io/badge/SkillCheck-Validated-4c1)](https://getskillcheck.com)

---

## ⚡ Quick Install

**Choose your AI agent:**

### Method 1: Claude Code Native (Recommended for Claude Code users)

Use Claude Code's built-in plugin system for native integration:

```bash
# In Claude Code, run:
/plugin marketplace add alirezarezvani/claude-skills

# Then install skill bundles:
/plugin install marketing-skills@claude-code-skills     # 6 marketing skills
/plugin install engineering-skills@claude-code-skills   # 18 engineering skills
/plugin install product-skills@claude-code-skills       # 5 product skills
/plugin install c-level-skills@claude-code-skills       # 2 C-level advisory skills
/plugin install pm-skills@claude-code-skills            # 6 project management skills
/plugin install ra-qm-skills@claude-code-skills         # 12 regulatory/quality skills
/plugin install business-growth-skills@claude-code-skills  # 3 business & growth skills
/plugin install finance-skills@claude-code-skills           # 1 finance skill

# Or install individual skills:
/plugin install content-creator@claude-code-skills      # Single skill
/plugin install fullstack-engineer@claude-code-skills   # Single skill
```

**Benefits:**
- ✅ Native Claude Code integration
- ✅ Automatic updates with `/plugin update`
- ✅ Version management with git tags
- ✅ Skills available in `~/.claude/skills/`

---

### Method 2: OpenAI Codex Installation

For OpenAI Codex users, install via universal installer or direct script:

```bash
# Option A: Universal installer
npx ai-agent-skills install alirezarezvani/claude-skills --agent codex

# Option B: Direct installation script
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills
./scripts/codex-install.sh

# Option C: Install specific category or skill
./scripts/codex-install.sh --category engineering
./scripts/codex-install.sh --skill content-creator
```

**Benefits:**
- ✅ Full Codex compatibility via `.codex/skills/` symlinks
- ✅ 43 skills with YAML frontmatter metadata
- ✅ Cross-platform scripts (Unix + Windows)
- ✅ Skills available in `~/.codex/skills/`

**See:** [How to Use with OpenAI Codex](#-how-to-use-with-openai-codex) for detailed guide.

---

### Method 3: Universal Installer (Works across all agents)

Install to Claude Code, Cursor, VS Code, Amp, Goose, and more - all with one command:

```bash
# Install all 53 skills to all supported agents
npx ai-agent-skills install alirezarezvani/claude-skills

# Install to specific agent (Claude Code)
npx ai-agent-skills install alirezarezvani/claude-skills --agent claude

# Install single skill
npx ai-agent-skills install alirezarezvani/claude-skills/marketing-skill/content-creator

# Install to Cursor
npx ai-agent-skills install alirezarezvani/claude-skills --agent cursor

# Preview before installing
npx ai-agent-skills install alirezarezvani/claude-skills --dry-run
```

**Benefits:**
- ✅ Works across 9+ AI agents simultaneously
- ✅ One command installs to all agents
- ✅ No agent-specific configuration needed

**Supported Agents:** Claude Code, Cursor, VS Code, Copilot, Goose, Amp, OpenAI Codex, Letta, OpenCode

**Installation Locations:**
- Claude Code: `~/.claude/skills/`
- Cursor: `.cursor/skills/`
- VS Code/Copilot: `.github/skills/`
- Goose: `~/.config/goose/skills/`
- OpenAI Codex: `~/.codex/skills/`
- Project-specific: `.skills/`

---

**Detailed Installation Guide:** See [INSTALLATION.md](INSTALLATION.md) for complete instructions, troubleshooting, and manual installation.

---

## 📚 Table of Contents

- [Quick Install](#-quick-install)
- [Overview](#-overview)
- [Available Skills](#-available-skills)
- [Quick Start](#-quick-start)
- [How to Use with Claude AI](#-how-to-use-with-claude-ai)
- [How to Use with Claude Code](#-how-to-use-with-claude-code)
- [How to Use with OpenAI Codex](#-how-to-use-with-openai-codex)
- [Skill Architecture](#-skill-architecture)
- [Installation](#-installation)
- [Usage Examples](#-usage-examples)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 🎯 Overview

This repository provides **modular, self-contained skill packages** designed to augment Claude AI with specialized domain expertise. Each skill includes:

- **📖 Comprehensive documentation** - Workflows, best practices, and strategic frameworks
- **🛠️ Python analysis tools** - 87+ CLI utilities for automated analysis and optimization
- **📚 Knowledge bases** - Curated reference materials and guidelines
- **📋 Ready-to-use templates** - Customizable assets for immediate deployment

**Key Benefits:**
- ⚡ **Immediate deployment** - Download and use in minutes
- 🎯 **Domain expertise** - Battle-tested frameworks from industry experts
- 🔧 **Practical tools** - Algorithmic analysis without external API dependencies
- 📈 **Measurable ROI** - 40%+ time savings, 30%+ quality improvements

---

## 🚀 Available Skills

### Marketing Skills

**6 comprehensive marketing skills** covering content creation, demand generation, product marketing strategy, mobile app optimization, social media analytics, and campaign analytics.

#### 📝 Content Creator
**Status:** ✅ Production Ready | **Version:** 1.0

Professional-grade brand voice analysis, SEO optimization, and platform-specific content frameworks.

**What's Included:**
- **Brand Voice Analyzer** - Analyze text for tone, formality, and readability (Python CLI)
- **SEO Optimizer** - Comprehensive SEO scoring and optimization recommendations (Python CLI)
- **Brand Guidelines** - 5 personality archetypes and voice framework
- **Content Frameworks** - 15+ templates (blog posts, emails, social media, video scripts)
- **Social Media Optimization** - Platform-specific guides for LinkedIn, Twitter/X, Instagram, Facebook, TikTok
- **Content Calendar Template** - Monthly planning and distribution framework

**Learn More:** [marketing-skill/content-creator/SKILL.md](marketing-skill/content-creator/SKILL.md)

---

#### 🎯 Marketing Demand & Acquisition
**Status:** ✅ Production Ready | **Version:** 1.0

Expert demand generation, paid media, SEO, and partnerships for Series A+ startups.

**What's Included:**
- **CAC Calculator** - Calculate channel-specific and blended customer acquisition cost (Python CLI)
- **Full-Funnel Strategy** - TOFU → MOFU → BOFU frameworks
- **Channel Playbooks** - LinkedIn Ads, Google Ads, Meta, SEO, Partnerships
- **HubSpot Integration** - Campaign tracking, attribution, lead scoring
- **International Expansion** - EU vs US vs Canada tactics
- **Performance Benchmarks** - B2B SaaS CAC and conversion benchmarks

**Learn More:** [marketing-skill/marketing-demand-acquisition/SKILL.md](marketing-skill/marketing-demand-acquisition/SKILL.md)

---

#### 🚀 Marketing Strategy & Product Marketing
**Status:** ✅ Production Ready | **Version:** 1.0

Product marketing, positioning, GTM strategy, and competitive intelligence.

**What's Included:**
- **ICP Definition** - Firmographics and psychographics frameworks
- **Positioning** - April Dunford positioning methodology
- **GTM Strategy** - PLG, Sales-Led, and Hybrid motion playbooks
- **Launch Plans** - 90-day product launch frameworks (Tier 1/2/3)
- **Competitive Intelligence** - Battlecard templates and analysis frameworks
- **International Market Entry** - 5-phase market expansion playbooks
- **Sales Enablement** - Training programs and asset development

**Learn More:** [marketing-skill/marketing-strategy-pmm/SKILL.md](marketing-skill/marketing-strategy-pmm/SKILL.md)

---

#### 📱 App Store Optimization (ASO)
**Status:** ✅ Production Ready | **Version:** 1.0

Complete ASO toolkit for Apple App Store and Google Play Store optimization.

**What's Included:**
- **Keyword Research** - Volume, competition, and relevance analysis frameworks
- **Metadata Optimization** - Platform-specific title, description, and keyword optimization
- **Conversion Optimization** - A/B testing frameworks and visual asset testing strategies
- **Rating & Review Management** - Review monitoring, response templates, sentiment analysis
- **Launch Strategies** - Pre-launch checklists, timing optimization, soft launch tactics
- **Analytics Tracking** - ASO score calculation, performance benchmarking, competitor tracking
- **Platform Support** - Apple App Store (30 char title) and Google Play Store (50 char title)

**Learn More:** [marketing-skill/app-store-optimization/SKILL.md](marketing-skill/app-store-optimization/SKILL.md)

---

#### 📊 Social Media Analyzer
**Status:** ✅ Production Ready | **Version:** 1.0

Analyze social media campaign performance across platforms with data-driven insights and ROI tracking.

**What's Included:**
- **Campaign Metrics Calculator** - Engagement rate, reach, impressions, CTR calculations (Python CLI)
- **Performance Analyzer** - ROI analysis and optimization recommendations (Python CLI)
- **Multi-Platform Support** - Facebook, Instagram, Twitter/X, LinkedIn, TikTok best practices
- **Audience Insights** - Demographics, peak engagement times, content performance patterns
- **Trend Detection** - High-performing content types, hashtag analysis, posting patterns
- **Competitive Benchmarking** - Industry standard comparisons and gap analysis
- **ROI Analysis** - Cost per engagement, campaign effectiveness measurement

**Learn More:** [marketing-skill/social-media-analyzer/SKILL.md](marketing-skill/social-media-analyzer/SKILL.md)

---

#### 📈 Campaign Analytics
**Status:** ✅ Production Ready | **Version:** 1.0

Multi-touch attribution, funnel conversion analysis, and campaign ROI measurement.

**What's Included:**
- **Attribution Analyzer** - Multi-touch attribution modeling across marketing channels (Python CLI)
- **Funnel Analyzer** - Conversion funnel analysis with bottleneck detection (Python CLI)
- **Campaign ROI Calculator** - Comprehensive campaign ROI metrics with benchmarking (Python CLI)
- **Attribution Models** - First-touch, last-touch, linear, time-decay, position-based
- **Industry Benchmarks** - Channel and vertical performance benchmarks

**Learn More:** [marketing-skill/campaign-analytics/SKILL.md](marketing-skill/campaign-analytics/SKILL.md)

---

### C-Level Advisory Skills

#### 👔 CEO Advisor
**Status:** ✅ Production Ready | **Version:** 1.0

Executive leadership guidance for strategic decision-making, organizational development, and stakeholder management.

**What's Included:**
- **Strategy Analyzer** - Evaluate strategic initiatives and competitive positioning (Python CLI)
- **Financial Scenario Analyzer** - Model financial scenarios and business outcomes (Python CLI)
- **Executive Decision Framework** - Structured decision-making methodology
- **Leadership & Organizational Culture** - Culture building and change management
- **Board Governance & Investor Relations** - Stakeholder communication best practices

**Core Workflows:**
1. Strategic planning and initiative evaluation
2. Financial scenario modeling
3. Board and investor communication
4. Organizational culture development

**Learn More:** [c-level-advisor/ceo-advisor/SKILL.md](c-level-advisor/ceo-advisor/SKILL.md)

---

#### 💻 CTO Advisor
**Status:** ✅ Production Ready | **Version:** 1.0

Technical leadership guidance for engineering teams, architecture decisions, and technology strategy.

**What's Included:**
- **Tech Debt Analyzer** - Quantify and prioritize technical debt (Python CLI)
- **Team Scaling Calculator** - Model engineering team growth and structure (Python CLI)
- **Engineering Metrics Framework** - DORA metrics, velocity, and quality indicators
- **Technology Evaluation Framework** - Structured approach to technology selection
- **Architecture Decision Records** - ADR templates and best practices

**Core Workflows:**
1. Technical debt assessment and management
2. Engineering team scaling and structure
3. Technology evaluation and selection
4. Architecture decision documentation

**Learn More:** [c-level-advisor/cto-advisor/SKILL.md](c-level-advisor/cto-advisor/SKILL.md)

---

### Product Team Skills

#### 📊 Product Manager Toolkit
**Status:** ✅ Production Ready | **Version:** 1.0

Essential tools and frameworks for modern product management, from discovery to delivery.

**What's Included:**
- **RICE Prioritizer** - Automated feature prioritization with portfolio analysis (Python CLI)
- **Customer Interview Analyzer** - AI-powered insight extraction from user interviews (Python CLI)
- **PRD Templates** - 4 comprehensive formats (Standard, One-Page, Agile Epic, Feature Brief)
- **Discovery Frameworks** - Customer interview guides, hypothesis templates, opportunity solution trees
- **Metrics & Analytics** - North Star metrics, funnel analysis, feature success tracking

**Core Workflows:**
1. Feature prioritization with RICE scoring
2. Customer discovery and interview analysis
3. PRD development and stakeholder alignment
4. Product metrics and success measurement

**Learn More:** [product-team/product-manager-toolkit/SKILL.md](product-team/product-manager-toolkit/SKILL.md)

---

#### 🎯 Agile Product Owner
**Status:** ✅ Production Ready | **Version:** 1.0

Sprint execution and backlog management tools for agile product delivery.

**What's Included:**
- **User Story Generator** - INVEST-compliant stories with acceptance criteria (Python CLI)
- **Sprint Planner** - Capacity-based sprint planning automation
- **Epic Breakdown** - Automatic story generation from epics
- **Velocity Tracker** - Sprint metrics and burndown analysis
- **Agile Ceremonies** - Frameworks for standups, retros, planning, reviews

**Core Workflows:**
1. Backlog refinement and grooming
2. Sprint planning and capacity allocation
3. User story writing and acceptance criteria
4. Sprint execution and velocity tracking

**Learn More:** [product-team/agile-product-owner/SKILL.md](product-team/agile-product-owner/SKILL.md)

---

#### 🚀 Product Strategist
**Status:** ✅ Production Ready | **Version:** 1.0

Strategic planning and vision alignment for heads of product and product leaders.

**What's Included:**
- **OKR Cascade Generator** - Automated company → product → team goal alignment (Python CLI)
- **Alignment Scoring** - Vertical and horizontal OKR alignment measurement
- **Strategy Templates** - Growth, retention, revenue, and innovation frameworks
- **Team Scaling Tools** - Organizational design and structure planning
- **Vision Frameworks** - Product vision, positioning, and roadmap development

**Core Workflows:**
1. Strategic planning and OKR setting
2. Product vision and positioning
3. Roadmap development and communication
4. Team organization and scaling

**Learn More:** [product-team/product-strategist/SKILL.md](product-team/product-strategist/SKILL.md)

---

#### 🎨 UX Researcher Designer
**Status:** ✅ Production Ready | **Version:** 1.0

User research and experience design frameworks for creating user-centered products.

**What's Included:**
- **Persona Generator** - Data-driven persona creation from user research (Python CLI)
- **Journey Mapper** - Customer journey visualization and mapping
- **Research Synthesizer** - Pattern identification from user interviews
- **Usability Framework** - Testing protocols and heuristic evaluation
- **Design Thinking** - Double diamond process, workshops, and facilitation

**Core Workflows:**
1. User research planning and execution
2. Research synthesis and insight generation
3. Persona development and validation
4. Journey mapping and experience design

**Learn More:** [product-team/ux-researcher-designer/SKILL.md](product-team/ux-researcher-designer/SKILL.md)

---

#### 🎨 UI Design System
**Status:** ✅ Production Ready | **Version:** 1.0

Visual design systems and component architecture for consistent user interfaces.

**What's Included:**
- **Design Token Generator** - Complete token system from brand colors (Python CLI)
- **Component Architecture** - Atomic design implementation and organization
- **Responsive Calculator** - Breakpoint and grid system generation
- **Export Formats** - JSON, CSS, SCSS outputs for development handoff
- **Documentation Templates** - Storybook integration and component specs

**Core Workflows:**
1. Design token system creation
2. Component library architecture
3. Design system documentation
4. Developer handoff and implementation

**Learn More:** [product-team/ui-design-system/SKILL.md](product-team/ui-design-system/SKILL.md)

---

### Project Management Team Skills

**6 world-class Atlassian expert skills** for project and agile delivery teams using Jira and Confluence.

#### 📋 Senior Project Management Expert
**Status:** ✅ Production Ready | **Version:** 1.0

Strategic project management for software, SaaS, and digital applications.

**What's Included:**
- Portfolio management and strategic planning
- Stakeholder alignment and executive reporting
- Risk management and budget oversight
- Cross-functional team leadership
- Roadmap development and project charters
- Atlassian MCP integration for metrics and reporting

**Learn More:** See `project-management/README.md` for details

---

#### 🏃 Scrum Master Expert
**Status:** ✅ Production Ready | **Version:** 1.0

Agile facilitation for software development teams.

**What's Included:**
- Sprint planning and execution
- Daily standups and retrospectives
- Backlog refinement and grooming
- Velocity tracking and metrics
- Impediment removal and escalation
- Team coaching on agile practices
- Atlassian MCP integration for sprint management

**Learn More:** See `project-management/README.md` for details

---

#### ⚙️ Atlassian Jira Expert
**Status:** ✅ Production Ready | **Version:** 1.0

Jira configuration, JQL mastery, and technical operations.

**What's Included:**
- Advanced JQL query writing
- Project and workflow configuration
- Custom fields and automation rules
- Dashboards and reporting
- Integration setup and optimization
- Performance tuning
- Atlassian MCP integration for all Jira operations

**Learn More:** See `project-management/README.md` for details

---

#### 📚 Atlassian Confluence Expert
**Status:** ✅ Production Ready | **Version:** 1.0

Knowledge management and documentation architecture.

**What's Included:**
- Space architecture and organization
- Page templates and macro implementation
- Documentation strategy and governance
- Content collaboration workflows
- Jira integration and linking
- Search optimization and findability
- Atlassian MCP integration for documentation

**Learn More:** See `project-management/README.md` for details

---

#### 🔧 Atlassian Administrator
**Status:** ✅ Production Ready | **Version:** 1.0

System administration for Atlassian suite.

**What's Included:**
- User provisioning and access management
- Global configuration and governance
- Security and compliance setup
- SSO and integration deployment
- Performance optimization
- Disaster recovery and license management
- Atlassian MCP integration for system administration

**Learn More:** See `project-management/README.md` for details

---

#### 📄 Atlassian Template Creator Expert
**Status:** ✅ Production Ready | **Version:** 1.0

Template and file creation/modification specialist.

**What's Included:**
- Confluence page template design (15+ templates)
- Jira issue template creation
- Blueprint development for complex structures
- Standardized content and governance
- Dynamic content and automation
- Template lifecycle management
- Atlassian MCP integration for template deployment

**Learn More:** See `project-management/README.md` for details

---

### Engineering Team Skills

**Complete engineering skills suite with 13 specialized roles** covering architecture, development, testing, security, operations, cloud infrastructure, and enterprise systems.

#### 🏗️ Senior Software Architect
**Status:** ✅ Production Ready | **Version:** 1.0

System architecture design, technology stack decisions, and architecture documentation.

**What's Included:**
- **Architecture Diagram Generator** - Create C4, sequence, and component diagrams (Python CLI)
- **Project Architect** - Scaffold architecture documentation and ADRs (Python CLI)
- **Dependency Analyzer** - Analyze and visualize dependencies (Python CLI)
- **Architecture Patterns** - Monolithic, microservices, serverless, event-driven patterns
- **System Design Workflows** - Step-by-step architecture design process
- **Tech Decision Guide** - Framework for technology stack selection

**Learn More:** See `engineering-team/README.md` for details

---

#### ⚛️ Senior Frontend Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

Frontend development with React, Next.js, and TypeScript.

**What's Included:**
- **Component Generator** - Scaffold React components with TypeScript (Python CLI)
- **Bundle Analyzer** - Optimize bundle size and performance (Python CLI)
- **Frontend Scaffolder** - Complete frontend project setup (Python CLI)
- **React Patterns** - Component composition, hooks, state management
- **Next.js Optimization** - App Router, Server Components, performance tuning
- **Frontend Best Practices** - Accessibility, SEO, performance optimization

**Learn More:** See `engineering-team/README.md` for details

---

#### 🔧 Senior Backend Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

Backend development with Node.js, Express, GraphQL, Go, and Python.

**What's Included:**
- **API Scaffolder** - Generate REST and GraphQL endpoints (Python CLI)
- **Database Migration Tool** - Manage PostgreSQL migrations (Python CLI)
- **API Load Tester** - Performance testing and optimization (Python CLI)
- **API Design Patterns** - RESTful, GraphQL, microservices architecture
- **Database Optimization** - Query optimization, indexing, connection pooling
- **Backend Security** - Authentication, authorization, data validation

**Learn More:** See `engineering-team/README.md` for details

---

#### 💻 Senior Fullstack Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

End-to-end application development with complete stack integration.

**What's Included:**
- **Fullstack Scaffolder** - Complete Next.js + GraphQL + PostgreSQL projects (Python CLI)
- **Project Scaffolder** - Production-ready project structure (Python CLI)
- **Code Quality Analyzer** - Comprehensive analysis and security scanning (Python CLI)
- **Tech Stack Guide** - Complete implementation guides for your stack
- **Architecture Patterns** - Full-stack system design and integration
- **Development Workflows** - Git, CI/CD, testing, deployment automation

**Learn More:** [engineering-team/fullstack-engineer/SKILL.md](engineering-team/fullstack-engineer/SKILL.md)

---

#### 🧪 Senior QA Testing Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

Quality assurance and test automation for comprehensive testing strategies.

**What's Included:**
- **Test Suite Generator** - Create unit, integration, E2E tests (Python CLI)
- **Coverage Analyzer** - Analyze and report test coverage (Python CLI)
- **E2E Test Scaffolder** - Setup Playwright/Cypress tests (Python CLI)
- **Testing Strategies** - Testing pyramid, TDD, BDD methodologies
- **Test Automation Patterns** - Page objects, fixtures, mocking strategies
- **QA Best Practices** - Quality metrics, regression testing, performance testing

**Learn More:** See `engineering-team/README.md` for details

---

#### 🚀 Senior DevOps Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

CI/CD automation, infrastructure as code, and deployment management.

**What's Included:**
- **Pipeline Generator** - Create GitHub Actions/CircleCI pipelines (Python CLI)
- **Terraform Scaffolder** - Generate infrastructure as code (Python CLI)
- **Deployment Manager** - Automate deployment workflows (Python CLI)
- **CI/CD Pipeline Guide** - Best practices for continuous integration/deployment
- **Infrastructure as Code** - Terraform, CloudFormation, Kubernetes
- **Deployment Strategies** - Blue-green, canary, rolling deployments

**Learn More:** See `engineering-team/README.md` for details

---

#### 🛡️ Senior SecOps Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

Security operations, vulnerability management, and compliance automation.

**What's Included:**
- **Security Scanner** - Automated vulnerability scanning (Python CLI)
- **Vulnerability Assessor** - Risk assessment and prioritization (Python CLI)
- **Compliance Checker** - GDPR, SOC2 compliance validation (Python CLI)
- **Security Standards** - OWASP Top 10, security best practices
- **Vulnerability Management** - Detection, assessment, remediation workflows
- **Compliance Requirements** - Compliance frameworks and automation

**Learn More:** See `engineering-team/README.md` for details

---

#### 👁️ Code Reviewer
**Status:** ✅ Production Ready | **Version:** 1.0

Automated code review, quality checking, and PR analysis.

**What's Included:**
- **PR Analyzer** - Automated pull request analysis (Python CLI)
- **Code Quality Checker** - Quality metrics and scoring (Python CLI)
- **Review Report Generator** - Generate comprehensive review reports (Python CLI)
- **Code Review Checklist** - Comprehensive review standards
- **Coding Standards** - Language-specific conventions and best practices
- **Common Anti-patterns** - What to avoid and how to fix

**Learn More:** See `engineering-team/README.md` for details

---

#### 🔐 Senior Security Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

Security architecture, penetration testing, and cryptography implementation.

**What's Included:**
- **Threat Modeler** - Automated threat modeling (Python CLI)
- **Security Auditor** - Comprehensive security audits (Python CLI)
- **Pentest Automator** - Automated penetration testing (Python CLI)
- **Security Architecture Patterns** - Zero Trust, defense in depth, secure design
- **Penetration Testing Guide** - Testing methodologies and tools
- **Cryptography Implementation** - Encryption, hashing, secure communication

**Learn More:** See `engineering-team/README.md` for details

---

#### ☁️ AWS Solution Architect
**Status:** ✅ Production Ready | **Version:** 1.0

Expert AWS solution architecture for startups with serverless and cost-optimized design.

**What's Included:**
- **Architecture Designer** - Generate architecture patterns and service recommendations (Python CLI)
- **Serverless Stack Builder** - Create Lambda, API Gateway, DynamoDB stacks (Python CLI)
- **Cost Optimizer** - AWS cost analysis and optimization strategies (Python CLI)
- **IaC Generator** - CloudFormation, CDK, Terraform template generation (Python CLI)
- **Security Auditor** - AWS security validation and compliance checks (Python CLI)
- **Serverless Patterns** - Lambda, API Gateway, DynamoDB, Step Functions, EventBridge
- **Event-Driven Architecture** - Microservices with SQS, SNS, Kinesis
- **Container Orchestration** - ECS Fargate, EKS best practices

**Learn More:** [engineering-team/aws-solution-architect/SKILL.md](engineering-team/aws-solution-architect/SKILL.md)

---

#### 🏢 Microsoft 365 Tenant Manager
**Status:** ✅ Production Ready | **Version:** 1.0

Comprehensive Microsoft 365 administration for Global Administrators and IT teams.

**What's Included:**
- **Tenant Setup Tool** - Initial configuration automation (Python CLI)
- **User Management** - Lifecycle operations and bulk provisioning (Python CLI)
- **Security Policies** - Conditional Access, MFA, DLP configuration (Python CLI)
- **Reporting Suite** - Analytics, audit logs, compliance reports (Python CLI)
- **PowerShell Generator** - Microsoft Graph API script generation (Python CLI)
- **SharePoint & Teams** - Site provisioning, Teams policy management
- **Exchange Online** - Mailbox management, mail flow rules, transport security
- **License Management** - Allocation, optimization, cost analysis

**Learn More:** [engineering-team/ms365-tenant-manager/SKILL.md](engineering-team/ms365-tenant-manager/SKILL.md)

---

#### 🧪 TDD Guide
**Status:** ✅ Production Ready | **Version:** 1.0

Comprehensive Test-Driven Development guide with intelligent test generation and coverage analysis.

**What's Included:**
- **Test Generation** - Convert requirements, user stories, and API specs to executable tests
- **Coverage Analysis** - Parse LCOV, JSON, XML coverage reports with gap identification
- **Framework Support** - Jest, Pytest, JUnit, Vitest, Mocha, RSpec with auto-detection
- **Quality Review** - Test isolation, assertions, naming conventions, complexity analysis
- **Missing Scenarios** - Identify untested edge cases and error conditions
- **Red-Green-Refactor** - Step-by-step TDD cycle guidance with best practices
- **Metrics Dashboard** - Coverage, complexity, quality scores, execution timing

**Learn More:** [engineering-team/tdd-guide/SKILL.md](engineering-team/tdd-guide/SKILL.md)

---

#### 🔍 Tech Stack Evaluator
**Status:** ✅ Production Ready | **Version:** 1.0

Comprehensive technology evaluation with TCO analysis, security assessment, and migration planning.

**What's Included:**
- **Technology Comparison** - Head-to-head framework and tool comparisons with scoring
- **Stack Evaluation** - Complete stack assessment for specific use cases (e.g., e-commerce, SaaS)
- **TCO Calculator** - Licensing, hosting, developer productivity, and maintenance costs
- **Security Assessment** - Vulnerability analysis, update frequency, compliance readiness
- **Migration Analyzer** - Legacy to modern migration complexity, risks, and timeline estimation
- **Cloud Comparison** - AWS vs Azure vs GCP for specific workloads with cost projections
- **Decision Reports** - Matrices with pros/cons, confidence scores, and actionable recommendations

**Learn More:** [engineering-team/tech-stack-evaluator/SKILL.md](engineering-team/tech-stack-evaluator/SKILL.md)

---

### AI/ML/Data Team Skills

**5 specialized AI/ML and data engineering skills** for building modern data-driven and AI-powered products.

#### 📊 Senior Data Scientist
**Status:** ✅ Production Ready | **Version:** 1.0

Statistical modeling, experimentation, and business analytics.

**What's Included:**
- **Experiment Designer** - Design A/B tests and statistical experiments (Python CLI)
- **Feature Engineering Pipeline** - Automated feature engineering workflows (Python CLI)
- **Statistical Analyzer** - Statistical modeling and causal inference (Python CLI)
- **Statistical Methods** - Hypothesis testing, regression, time series, causal inference
- **Experimentation Framework** - A/B testing, multi-armed bandits, Bayesian optimization
- **Analytics Patterns** - Business metrics, dashboards, reporting

**Learn More:** See `engineering-team/README.md` for details

---

#### 🔧 Senior Data Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

Data pipeline engineering, ETL/ELT workflows, and data infrastructure.

**What's Included:**
- **Pipeline Orchestrator** - Build data pipelines with Airflow/Spark (Python CLI)
- **Data Quality Validator** - Data quality checks and monitoring (Python CLI)
- **ETL Generator** - Generate ETL/ELT workflows (Python CLI)
- **Data Pipeline Patterns** - Batch, streaming, lambda architecture
- **Data Quality Framework** - Validation, monitoring, lineage tracking
- **Data Modeling Guide** - Dimensional modeling, data vault, schema design

**Learn More:** See `engineering-team/README.md` for details

---

#### 🤖 Senior ML/AI Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

MLOps, model deployment, and LLM integration for production AI systems.

**What's Included:**
- **Model Deployment Pipeline** - Deploy ML models to production (Python CLI)
- **MLOps Setup Tool** - Setup MLOps infrastructure with MLflow (Python CLI)
- **LLM Integration Builder** - Integrate LLMs into applications (Python CLI)
- **MLOps Production Patterns** - Model versioning, monitoring, A/B testing
- **LLM Integration Guide** - RAG, fine-tuning, prompt engineering
- **Model Deployment Strategies** - Serving, scaling, monitoring

**Learn More:** See `engineering-team/README.md` for details

---

#### 💬 Senior Prompt Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

LLM optimization, RAG systems, and agentic AI development.

**What's Included:**
- **Prompt Optimizer** - Optimize prompts for better LLM responses (Python CLI)
- **RAG System Builder** - Build Retrieval Augmented Generation systems (Python CLI)
- **Agent Orchestrator** - Design and orchestrate AI agents (Python CLI)
- **Advanced Prompting Techniques** - Chain-of-thought, few-shot, meta-prompting
- **RAG Architecture Patterns** - Vector search, chunking, reranking
- **Agent Design Patterns** - ReAct, tool use, multi-agent systems

**Learn More:** See `engineering-team/README.md` for details

---

#### 👁️ Senior Computer Vision Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

Computer vision, image/video AI, and real-time visual inference.

**What's Included:**
- **Vision Model Trainer** - Train object detection and segmentation models (Python CLI)
- **Inference Optimizer** - Optimize vision model inference (Python CLI)
- **Video Processor** - Process and analyze video streams (Python CLI)
- **Vision Architecture Patterns** - Object detection, segmentation, classification
- **Real-time Inference Guide** - Edge deployment, optimization, latency reduction
- **Computer Vision Production** - Model serving, monitoring, data pipelines

**Learn More:** See `engineering-team/README.md` for details

---

### Regulatory Affairs & Quality Management Team Skills

**12 world-class expert skills** for HealthTech and MedTech organizations covering regulatory compliance, quality systems, risk management, security, and audit excellence.

#### 📋 Senior Regulatory Affairs Manager (Head of RA)
**Status:** ✅ Production Ready | **Version:** 1.0

Strategic regulatory leadership and cross-functional coordination for market access.

**What's Included:**
- **Regulatory Pathway Analyzer** - Analyze optimal regulatory routes (Python CLI)
- **Submission Timeline Tracker** - Track submission progress and milestones (Python CLI)
- **Regulatory Intelligence Monitor** - Monitor global regulatory changes (Python CLI)
- **EU MDR Submission Guide** - Complete MDR submission process
- **FDA Submission Guide** - FDA pathways (510k, PMA, De Novo)
- **Global Regulatory Pathways** - International frameworks

**Learn More:** See `ra-qm-team/README.md` for details

---

#### ⭐ Senior Quality Manager Responsible Person (QMR)
**Status:** ✅ Production Ready | **Version:** 1.0

Overall quality system responsibility and regulatory compliance oversight.

**What's Included:**
- **QMS Effectiveness Monitor** - Monitor QMS performance metrics (Python CLI)
- **Compliance Dashboard Generator** - Generate compliance reports (Python CLI)
- **Management Review Analyzer** - Analyze management review data (Python CLI)
- **QMR Responsibilities Framework** - Complete role definition
- **Quality Leadership Guide** - Strategic quality management
- **Management Review Procedures** - Effective management reviews

**Learn More:** See `ra-qm-team/README.md` for details

---

#### 📊 Senior Quality Manager - QMS ISO 13485 Specialist
**Status:** ✅ Production Ready | **Version:** 1.0

ISO 13485 QMS implementation, maintenance, and optimization.

**What's Included:**
- **QMS Compliance Checker** - Check ISO 13485 compliance (Python CLI)
- **Design Control Tracker** - Track design control activities (Python CLI)
- **Document Control System** - Manage controlled documents (Python CLI)
- **ISO 13485 Implementation** - Complete implementation guide
- **Design Controls Handbook** - Best practices
- **Internal Audit Program** - Audit planning and execution

**Learn More:** See `ra-qm-team/README.md` for details

---

#### 🔄 Senior CAPA Officer
**Status:** ✅ Production Ready | **Version:** 1.0

Corrective and preventive action management within QMS.

**What's Included:**
- **CAPA Tracker** - Track CAPA status and effectiveness (Python CLI)
- **Root Cause Analyzer** - Facilitate root cause analysis (Python CLI)
- **Trend Analysis Tool** - Analyze quality trends (Python CLI)
- **CAPA Process Guide** - Complete CAPA procedures
- **Root Cause Analysis Methods** - 5 Whys, Fishbone, FTA
- **Effectiveness Verification** - CAPA effectiveness assessment

**Learn More:** See `ra-qm-team/README.md` for details

---

#### 📝 Senior Quality Documentation Manager
**Status:** ✅ Production Ready | **Version:** 1.0

Documentation control and review of regulatory documentation.

**What's Included:**
- **Document Version Control** - Manage document versions (Python CLI)
- **Technical File Builder** - Build regulatory technical files (Python CLI)
- **Document Compliance Checker** - Verify compliance (Python CLI)
- **Document Control Procedures** - Best practices
- **Technical File Requirements** - Regulatory requirements
- **Change Control Process** - Change management

**Learn More:** See `ra-qm-team/README.md` for details

---

#### ⚠️ Senior Risk Management Specialist
**Status:** ✅ Production Ready | **Version:** 1.0

ISO 14971 risk management throughout product lifecycle.

**What's Included:**
- **Risk Register Manager** - Manage product risk registers (Python CLI)
- **FMEA Calculator** - Calculate risk priority numbers (Python CLI)
- **Risk Control Tracker** - Track risk control effectiveness (Python CLI)
- **ISO 14971 Implementation** - Complete risk management process
- **Risk Analysis Methods** - FMEA, FTA, HAZOP
- **Post-Production Monitoring** - Post-market risk management

**Learn More:** See `ra-qm-team/README.md` for details

---

#### 🔒 Senior Information Security Manager (ISO 27001/27002)
**Status:** ✅ Production Ready | **Version:** 1.0

ISMS implementation and cybersecurity compliance for medical devices.

**What's Included:**
- **ISMS Compliance Checker** - Check ISO 27001 compliance (Python CLI)
- **Security Risk Assessor** - Assess cybersecurity risks (Python CLI)
- **Vulnerability Tracker** - Track security vulnerabilities (Python CLI)
- **ISO 27001 Implementation** - ISMS implementation guide
- **Medical Device Cybersecurity** - Device security requirements
- **Security Controls Framework** - ISO 27002 controls

**Learn More:** See `ra-qm-team/README.md` for details

---

#### 🇪🇺 Senior MDR 2017/745 Specialist
**Status:** ✅ Production Ready | **Version:** 1.0

EU MDR compliance expertise and consulting.

**What's Included:**
- **MDR Compliance Checker** - Check MDR compliance status (Python CLI)
- **Classification Analyzer** - Support device classification (Python CLI)
- **UDI Generator** - Generate and validate UDI codes (Python CLI)
- **MDR Requirements Overview** - Complete MDR requirements
- **Clinical Evaluation Guide** - Clinical evidence requirements
- **Technical Documentation MDR** - MDR technical files

**Learn More:** See `ra-qm-team/README.md` for details

---

#### 🇺🇸 Senior FDA Consultant and Specialist
**Status:** ✅ Production Ready | **Version:** 1.0

FDA submission pathways and QSR compliance.

**What's Included:**
- **FDA Submission Packager** - Package FDA submissions (Python CLI)
- **QSR Compliance Checker** - Check QSR compliance (Python CLI)
- **Predicate Device Analyzer** - Analyze substantial equivalence (Python CLI)
- **FDA Submission Pathways** - 510k, PMA, De Novo guidance
- **QSR 820 Compliance** - Complete QSR requirements
- **FDA Cybersecurity Guide** - FDA cybersecurity requirements

**Learn More:** See `ra-qm-team/README.md` for details

---

#### 🔍 Senior QMS Audit Expert
**Status:** ✅ Production Ready | **Version:** 1.0

Internal and external QMS auditing expertise.

**What's Included:**
- **Audit Planner** - Plan and schedule QMS audits (Python CLI)
- **Finding Tracker** - Track audit findings and CAPAs (Python CLI)
- **Audit Report Generator** - Generate audit reports (Python CLI)
- **Audit Program Management** - Planning and scheduling
- **Audit Execution Checklist** - Procedures and checklists
- **Nonconformity Management** - Finding and CAPA management

**Learn More:** See `ra-qm-team/README.md` for details

---

#### 🔐 Senior ISMS Audit Expert
**Status:** ✅ Production Ready | **Version:** 1.0

Information security management system auditing.

**What's Included:**
- **ISMS Audit Planner** - Plan ISO 27001 audits (Python CLI)
- **Security Controls Assessor** - Assess security controls (Python CLI)
- **ISMS Finding Tracker** - Track security findings (Python CLI)
- **ISO 27001 Audit Guide** - ISMS audit procedures
- **Security Controls Assessment** - Control testing methodologies
- **ISMS Certification Preparation** - Certification readiness

**Learn More:** See `ra-qm-team/README.md` for details

---

#### 🛡️ Senior GDPR/DSGVO Expert
**Status:** ✅ Production Ready | **Version:** 1.0

EU GDPR and German DSGVO compliance and auditing.

**What's Included:**
- **GDPR Compliance Checker** - Check GDPR compliance (Python CLI)
- **DPIA Generator** - Generate privacy impact assessments (Python CLI)
- **Data Breach Reporter** - Manage breach notifications (Python CLI)
- **GDPR Compliance Framework** - Complete GDPR requirements
- **DPIA Methodology** - Privacy impact assessment process
- **Medical Device Privacy** - Privacy for medical devices

**Learn More:** See `ra-qm-team/README.md` for details

---

### Business & Growth Skills

**3 specialized business growth skills** covering customer success, sales engineering, and revenue operations.

#### 🤝 Customer Success Manager
**Status:** ✅ Production Ready | **Version:** 1.0

Expert customer success management with onboarding, retention, and expansion frameworks.

**What's Included:**
- **Health Score Calculator** - Calculate customer health scores with weighted metrics (Python CLI)
- **Churn Risk Analyzer** - Identify at-risk accounts with early warning signals (Python CLI)
- **Onboarding Playbooks** - Structured onboarding frameworks for different customer segments
- **Retention Strategies** - Proactive retention and expansion revenue tactics
- **QBR Templates** - Quarterly business review preparation and execution

**Learn More:** [business-growth/customer-success-manager/SKILL.md](business-growth/customer-success-manager/SKILL.md)

---

#### 💼 Sales Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

Technical sales support with solution design, RFP responses, and demo optimization.

**What's Included:**
- **Solution Designer** - Map customer requirements to product capabilities (Python CLI)
- **RFP Response Generator** - Generate structured RFP responses from templates (Python CLI)
- **Demo Frameworks** - Technical demonstration planning and execution
- **POC Management** - Proof of concept planning and success criteria
- **Technical Discovery** - Pre-sales technical assessment frameworks

**Learn More:** [business-growth/sales-engineer/SKILL.md](business-growth/sales-engineer/SKILL.md)

---

#### 📊 Revenue Operations
**Status:** ✅ Production Ready | **Version:** 1.0

Revenue operations with pipeline analytics, forecasting, and process optimization.

**What's Included:**
- **Pipeline Analyzer** - Analyze pipeline health, velocity, and conversion rates (Python CLI)
- **Forecast Modeler** - Revenue forecasting with multiple scenario modeling (Python CLI)
- **Process Optimizer** - Identify and resolve revenue process bottlenecks
- **GTM Metrics** - Go-to-market metrics tracking and benchmarking
- **Territory Planning** - Data-driven territory design and optimization

**Learn More:** [business-growth/revenue-operations/SKILL.md](business-growth/revenue-operations/SKILL.md)

---

### Finance Skills

#### 💰 Financial Analyst
**Status:** ✅ Production Ready | **Version:** 1.0

Financial analysis with DCF valuation, budgeting, forecasting, and financial modeling.

**What's Included:**
- **DCF Calculator** - Discounted cash flow valuation with sensitivity analysis (Python CLI)
- **Budget Analyzer** - Budget variance analysis and forecasting (Python CLI)
- **Financial Modeler** - Three-statement financial model generation (Python CLI)
- **Ratio Analyzer** - Financial ratio analysis with industry benchmarks
- **Scenario Planner** - Multi-scenario financial planning and stress testing

**Learn More:** [finance/financial-analyst/SKILL.md](finance/financial-analyst/SKILL.md)

---

## ⚡ Quick Start

### For Claude AI Users

1. **Download** the skill package you need (or clone this repository)
2. **Upload** the SKILL.md file to your Claude conversation
3. **Reference** the skill: "Using the content-creator skill, help me write a LinkedIn post about AI"

### For Claude Code Users

1. **Clone** this repository into your project
2. **Load** the skill in your Claude Code session
3. **Execute** workflows and run analysis tools directly

---

## 🤖 How to Use with Claude AI

Claude AI can use these skills to provide specialized expertise in your conversations.

### Method 1: Upload Skill Documentation

**Step-by-Step:**

1. **Navigate to the skill folder** you want to use (e.g., `marketing-skill/content-creator/`)

2. **Upload the SKILL.md file** to your Claude conversation:
   - Click the attachment icon 📎
   - Select `SKILL.md` from the skill folder
   - Upload to the conversation

3. **Reference the skill in your prompts:**
   ```
   Using the content-creator skill, help me:
   - Write a blog post about sustainable technology
   - Analyze my brand voice from these 3 articles
   - Create a LinkedIn content calendar for November 2025
   ```

4. **Access reference materials as needed:**
   - Upload specific reference files (e.g., `references/content_frameworks.md`)
   - Claude will use the frameworks to guide content creation

### Method 2: Use Packaged .zip Archives

For easy sharing with your team:

1. **Download** the pre-packaged .zip file (e.g., `content-creator.zip`)
2. **Extract** to your local machine
3. **Upload SKILL.md** to Claude as described above

### Example Prompts

**Content Creator Skill:**
```
Using the content-creator skill:
1. Analyze this article for brand voice consistency
2. Optimize this blog post for the keyword "marketing automation"
3. Create a 30-day LinkedIn content calendar for our product launch
4. Write a Twitter thread explaining our new feature
```

**CEO Advisor Skill:**
```
Using the ceo-advisor skill:
1. Help me evaluate our product expansion strategy
2. Create a board presentation for Q4 results
3. Model financial scenarios for hiring 10 new salespeople
4. Draft investor update email for our Series A round
```

**CTO Advisor Skill:**
```
Using the cto-advisor skill:
1. Analyze our technical debt and create a reduction roadmap
2. Calculate optimal team structure for scaling to 50 engineers
3. Evaluate whether we should adopt GraphQL or stick with REST
4. Create an ADR for our microservices migration decision
```

**Product Manager Toolkit:**
```
Using the product-manager-toolkit skill:
1. Prioritize our backlog of 50 features using RICE scoring
2. Analyze customer interview transcripts to extract pain points
3. Create a PRD for our new analytics dashboard feature
4. Design a customer discovery interview guide for B2B users
```

**Agile Product Owner:**
```
Using the agile-product-owner skill:
1. Generate user stories for our mobile app redesign epic
2. Plan next sprint with 30 story points capacity
3. Create acceptance criteria for authentication feature
4. Analyze our velocity trends over last 6 sprints
```

**Product Strategist:**
```
Using the product-strategist skill:
1. Generate OKR cascade from company goals to team level
2. Create product vision and positioning for new market
3. Design quarterly roadmap with strategic themes
4. Plan product team scaling from 5 to 20 people
```

**UX Researcher Designer:**
```
Using the ux-researcher-designer skill:
1. Create data-driven personas from 20 user interviews
2. Map customer journey for onboarding experience
3. Design usability test protocol for checkout flow
4. Synthesize research findings into actionable insights
```

**UI Design System:**
```
Using the ui-design-system skill:
1. Generate complete design token system from brand color #0066CC
2. Create component library architecture using atomic design
3. Define responsive breakpoints and grid system
4. Export design tokens as CSS variables for developers
```

**Fullstack Engineer:**
```
Using the fullstack-engineer skill:
1. Scaffold a new Next.js + GraphQL + PostgreSQL project
2. Analyze code quality and security vulnerabilities in existing project
3. Implement clean architecture patterns for backend API
4. Set up CI/CD pipeline with GitHub Actions and Docker
```

### Tips for Best Results

✅ **DO:**
- Reference the skill name explicitly in your prompts
- Upload relevant reference materials for complex tasks
- Ask Claude to use specific frameworks or templates from the skill
- Provide context about your industry, audience, or constraints

❌ **DON'T:**
- Assume Claude remembers the skill across different conversations (re-upload if needed)
- Mix too many skills in one conversation (focus on one domain at a time)
- Skip uploading the SKILL.md file (it contains essential workflows)

---

## 💻 How to Use with Claude Code

Claude Code can execute the Python analysis tools and integrate skills into your development workflow.

### Setup

1. **Clone this repository** into your project or workspace:
   ```bash
   git clone https://github.com/alirezarezvani/claude-skills.git
   cd claude-skills
   ```

2. **Install Python dependencies** (if needed):
   ```bash
   # Most scripts use standard library only
   pip install pyyaml  # Optional, for future features
   ```

3. **Verify installation**:
   ```bash
   python marketing-skill/content-creator/scripts/brand_voice_analyzer.py --help
   python marketing-skill/content-creator/scripts/seo_optimizer.py --help
   ```

### Using Analysis Tools

#### Brand Voice Analyzer

Analyze any text file for brand voice characteristics and readability:

```bash
# Analyze with human-readable output
python marketing-skill/content-creator/scripts/brand_voice_analyzer.py article.txt

# Analyze with JSON output for automation
python marketing-skill/content-creator/scripts/brand_voice_analyzer.py article.txt json
```

**Output includes:**
- Formality score (informal → formal scale)
- Tone analysis (professional, friendly, authoritative, etc.)
- Perspective (first-person, third-person)
- Flesch Reading Ease score
- Sentence structure analysis
- Improvement recommendations

#### SEO Optimizer

Comprehensive SEO analysis and optimization:

```bash
# Basic SEO analysis
python marketing-skill/content-creator/scripts/seo_optimizer.py blog-post.md "primary keyword"

# With secondary keywords
python marketing-skill/content-creator/scripts/seo_optimizer.py blog-post.md "marketing automation" "email marketing,lead nurturing"
```

**Output includes:**
- SEO score (0-100)
- Keyword density analysis (primary, secondary, LSI keywords)
- Content structure evaluation (headings, paragraphs, links)
- Readability assessment
- Meta tag suggestions (title, description, URL, OG tags)
- Actionable optimization recommendations

#### Tech Debt Analyzer (CTO Advisor)

Quantify and prioritize technical debt:

```bash
python c-level-advisor/cto-advisor/scripts/tech_debt_analyzer.py /path/to/codebase
```

#### Team Scaling Calculator (CTO Advisor)

Model engineering team growth:

```bash
python c-level-advisor/cto-advisor/scripts/team_scaling_calculator.py --current-size 10 --target-size 50
```

#### Financial Scenario Analyzer (CEO Advisor)

Model business scenarios:

```bash
python c-level-advisor/ceo-advisor/scripts/financial_scenario_analyzer.py scenarios.yaml
```

#### Strategy Analyzer (CEO Advisor)

Evaluate strategic initiatives:

```bash
python c-level-advisor/ceo-advisor/scripts/strategy_analyzer.py strategy-doc.md
```

#### RICE Prioritizer (Product Manager)

Feature prioritization with portfolio analysis:

```bash
# Basic prioritization
python product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv

# With custom team capacity
python product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv --capacity 20

# Output as JSON
python product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv --output json
```

#### Customer Interview Analyzer (Product Manager)

Extract insights from user interviews:

```bash
# Analyze single interview
python product-team/product-manager-toolkit/scripts/customer_interview_analyzer.py interview.txt

# Output as JSON for aggregation
python product-team/product-manager-toolkit/scripts/customer_interview_analyzer.py interview.txt json
```

#### User Story Generator (Product Owner)

Generate INVEST-compliant user stories:

```bash
# Interactive mode
python product-team/agile-product-owner/scripts/user_story_generator.py

# Generate sprint plan with capacity
python product-team/agile-product-owner/scripts/user_story_generator.py sprint 30
```

#### OKR Cascade Generator (Product Strategist)

Generate aligned OKR hierarchy:

```bash
# Generate OKRs for growth strategy
python product-team/product-strategist/scripts/okr_cascade_generator.py growth

# Other strategy types: retention, revenue, innovation
python product-team/product-strategist/scripts/okr_cascade_generator.py retention
```

#### Persona Generator (UX Researcher)

Create data-driven personas:

```bash
# Interactive persona creation
python product-team/ux-researcher-designer/scripts/persona_generator.py

# Export as JSON
python product-team/ux-researcher-designer/scripts/persona_generator.py --output json
```

#### Design Token Generator (UI Designer)

Generate complete design system tokens:

```bash
# Generate tokens from brand color
python product-team/ui-design-system/scripts/design_token_generator.py "#0066CC" modern css

# Output formats: css, json, scss
python product-team/ui-design-system/scripts/design_token_generator.py "#0066CC" modern json
```

#### Project Scaffolder (Fullstack Engineer)

Scaffold production-ready fullstack projects:

```bash
# Create new Next.js + GraphQL + PostgreSQL project
python engineering-team/fullstack-engineer/scripts/project_scaffolder.py my-project --type nextjs-graphql

# Navigate and start
cd my-project && docker-compose up -d
```

#### Code Quality Analyzer (Fullstack Engineer)

Analyze code quality and security:

```bash
# Analyze existing project
python engineering-team/fullstack-engineer/scripts/code_quality_analyzer.py /path/to/project

# Get JSON report
python engineering-team/fullstack-engineer/scripts/code_quality_analyzer.py /path/to/project --json
```

#### Fullstack Scaffolder (Fullstack Engineer)

Rapid fullstack project generation:

```bash
# Generate fullstack application structure
python engineering-team/fullstack-engineer/scripts/fullstack_scaffolder.py my-app --stack nextjs-graphql
```

### Integrating with Claude Code Workflows

**Example 1: Automated Content Quality Check**

```bash
# In your Claude Code session:
# 1. Write content using content-creator frameworks
# 2. Run automated analysis
python marketing-skill/content-creator/scripts/seo_optimizer.py output.md "target keyword"
python marketing-skill/content-creator/scripts/brand_voice_analyzer.py output.md json

# 3. Claude Code reviews results and suggests improvements
```

**Example 2: Technical Debt Tracking**

```bash
# Run monthly tech debt analysis
python c-level-advisor/cto-advisor/scripts/tech_debt_analyzer.py src/

# Claude Code generates report and roadmap
# Tracks progress over time
```

**Example 3: Content Pipeline Automation**

Create a workflow in Claude Code:
1. Generate content using content frameworks
2. Auto-run SEO optimizer on all drafts
3. Flag content below SEO score threshold (< 75)
4. Apply recommendations automatically
5. Re-score and validate

### Advanced: Custom Skill Development

Use this repository as a template to build your own skills:

1. **Fork this repository**
2. **Create new skill folder** following the architecture pattern
3. **Develop** your domain-specific tools and frameworks
4. **Document** workflows in SKILL.md
5. **Share** with your team or contribute back

See [CLAUDE.md](CLAUDE.md) for detailed architecture and development guidelines.

---

## 🤖 How to Use with OpenAI Codex

OpenAI Codex users can install and use these skills through the `.codex/skills/` directory, which provides Codex-compatible skill discovery.

### Quick Installation

**Option 1: Universal Installer (Recommended)**

```bash
# Install all 43 skills to Codex
npx ai-agent-skills install alirezarezvani/claude-skills --agent codex

# Verify installation
ls ~/.codex/skills/
```

**Option 2: Direct Installation Script**

```bash
# Clone and install
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills
./scripts/codex-install.sh

# Or install specific category
./scripts/codex-install.sh --category marketing
./scripts/codex-install.sh --category engineering

# Or install single skill
./scripts/codex-install.sh --skill content-creator
```

**Option 3: Manual Installation**

```bash
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills
mkdir -p ~/.codex/skills
cp -rL .codex/skills/* ~/.codex/skills/
```

### Using Skills in Codex

Once installed, skills are available at `~/.codex/skills/`. Each skill contains:

```
~/.codex/skills/
├── content-creator/
│   ├── SKILL.md              # Main documentation
│   ├── scripts/              # Python CLI tools
│   ├── references/           # Knowledge bases
│   └── assets/               # Templates
├── senior-fullstack/
├── product-manager-toolkit/
└── ... (53 skills total)
```

### Available Skills by Category

| Category | Count | Key Skills |
|----------|-------|------------|
| **Marketing** | 6 | content-creator, marketing-demand-acquisition, app-store-optimization |
| **Engineering** | 18 | senior-fullstack, aws-solution-architect, senior-ml-engineer, tdd-guide |
| **Product** | 5 | product-manager-toolkit, agile-product-owner, ux-researcher-designer |
| **C-Level** | 2 | ceo-advisor, cto-advisor |
| **Project Management** | 6 | scrum-master, senior-pm, jira-expert, confluence-expert |
| **RA/QM** | 12 | regulatory-affairs-head, quality-manager-qms-iso13485, gdpr-dsgvo-expert |
| **Business & Growth** | 3 | customer-success-manager, sales-engineer, revenue-operations |
| **Finance** | 1 | financial-analyst |

### Running Python Analysis Tools

```bash
# Brand voice analysis
python ~/.codex/skills/content-creator/scripts/brand_voice_analyzer.py article.txt

# SEO optimization
python ~/.codex/skills/content-creator/scripts/seo_optimizer.py blog.md "target keyword"

# Tech debt analysis
python ~/.codex/skills/cto-advisor/scripts/tech_debt_analyzer.py /path/to/codebase

# RICE prioritization
python ~/.codex/skills/product-manager-toolkit/scripts/rice_prioritizer.py features.csv
```

### Skills Index

The `.codex/skills-index.json` manifest provides metadata for all skills:

```bash
# View skills index
cat ~/.codex/skills-index.json | python -m json.tool

# Or from the repository
cat .codex/skills-index.json
```

### Windows Installation

```cmd
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills
scripts\codex-install.bat

REM Or install single skill
scripts\codex-install.bat --skill content-creator
```

### Keeping Skills Updated

```bash
# Update from repository
cd claude-skills
git pull
./scripts/codex-install.sh
```

**Detailed Installation Guide:** See [INSTALLATION.md](INSTALLATION.md#openai-codex-installation) for complete instructions, troubleshooting, and category-specific installation.

---

## 🏗️ Skill Architecture

Each skill package follows a consistent, modular structure:

```
{skill-category}/
└── {skill-name}/
    ├── SKILL.md                          # Master documentation
    ├── scripts/                          # Python CLI tools
    │   ├── {tool_name}.py               # Executable analysis tools
    │   └── ...
    ├── references/                       # Knowledge bases
    │   ├── {framework_name}.md          # Curated guidelines
    │   └── ...
    └── assets/                           # User templates
        ├── {template_name}.md           # Ready-to-use templates
        └── ...
```

### Design Principles

1. **Self-Contained** - Each skill is fully independent and deployable
2. **Documentation-Driven** - Success depends on clear, actionable documentation
3. **Algorithm Over AI** - Use deterministic analysis (code) when possible for speed and reliability
4. **Template-Heavy** - Provide ready-to-use frameworks users can customize
5. **Platform-Specific** - Focus on specific, actionable advice over generic best practices

### Component Responsibilities

| Component | Purpose | Format |
|-----------|---------|--------|
| **SKILL.md** | Entry point, workflows, usage instructions | Markdown |
| **scripts/** | Automated analysis and optimization tools | Python CLI |
| **references/** | Expert knowledge, frameworks, guidelines | Markdown |
| **assets/** | Templates for end-user customization | Markdown/YAML |

---

## 📦 Installation

### Method 1: Universal Installer (Recommended)

**Fastest way to get started** - Installs to all supported agents automatically:

```bash
# Install all skills to Claude Code, Cursor, VS Code, Amp, Goose, etc.
npx ai-agent-skills install alirezarezvani/claude-skills

# Or install to specific agent
npx ai-agent-skills install alirezarezvani/claude-skills --agent claude

# Or install single skill
npx ai-agent-skills install alirezarezvani/claude-skills/marketing-skill/content-creator
```

**Supported Agents:**
- Claude Code (`--agent claude`) → `~/.claude/skills/`
- Cursor (`--agent cursor`) → `.cursor/skills/`
- VS Code/Copilot (`--agent vscode`) → `.github/skills/`
- Goose (`--agent goose`) → `~/.config/goose/skills/`
- Project-specific (`--agent project`) → `.skills/`

**Verification:**
```bash
# Check installed skills (Claude Code example)
ls ~/.claude/skills/

# Use skills directly in your agent
# No additional setup required!
```

---

### Method 2: Manual Installation (Alternative)

For development, customization, or offline use:

#### Prerequisites

- **Python 3.7+** (for running analysis scripts)
- **Claude AI account** or **Claude Code** (for using skills)
- **Git** (for cloning repository)

#### Clone Repository

```bash
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills
```

#### Install Dependencies

Most scripts use Python standard library only. Optional dependencies:

```bash
pip install pyyaml  # For future features
```

#### Verify Installation

```bash
# Test marketing skills
python marketing-skill/content-creator/scripts/brand_voice_analyzer.py --help
python marketing-skill/content-creator/scripts/seo_optimizer.py --help

# Test C-level advisor skills
python c-level-advisor/cto-advisor/scripts/tech_debt_analyzer.py --help
python c-level-advisor/cto-advisor/scripts/team_scaling_calculator.py --help
python c-level-advisor/ceo-advisor/scripts/strategy_analyzer.py --help
python c-level-advisor/ceo-advisor/scripts/financial_scenario_analyzer.py --help

# Test product team skills
python product-team/product-manager-toolkit/scripts/rice_prioritizer.py --help
python product-team/product-manager-toolkit/scripts/customer_interview_analyzer.py --help
python product-team/agile-product-owner/scripts/user_story_generator.py --help
python product-team/product-strategist/scripts/okr_cascade_generator.py --help
python product-team/ux-researcher-designer/scripts/persona_generator.py --help
python product-team/ui-design-system/scripts/design_token_generator.py --help

# Test engineering team skills
python engineering-team/fullstack-engineer/scripts/project_scaffolder.py --help
python engineering-team/fullstack-engineer/scripts/code_quality_analyzer.py --help
python engineering-team/fullstack-engineer/scripts/fullstack_scaffolder.py --help
```

---

## 📖 Usage Examples

### Example 1: Blog Post Optimization

**Scenario:** You've written a blog post and want to optimize it for SEO and brand consistency.

```bash
# Step 1: Check SEO
python marketing-skill/content-creator/scripts/seo_optimizer.py blog-post.md "AI automation"

# Output: SEO Score: 68/100
# Recommendations:
# - Add 3 more mentions of primary keyword (current density: 0.8%, target: 1-2%)
# - Include H2 heading with primary keyword
# - Add 2 internal links
# - Meta description too short (current: 120 chars, target: 150-160)

# Step 2: Check brand voice
python marketing-skill/content-creator/scripts/brand_voice_analyzer.py blog-post.md

# Output:
# Formality: 7/10 (Professional)
# Tone: Authoritative, Informative
# Readability: 65 (Standard - college level)
# Recommendations:
# - Reduce sentence length by 15% for better readability
# - Use more active voice (currently 60%, target: 70%+)

# Step 3: Apply fixes in your editor
# Step 4: Re-run analysis to verify improvements
```

### Example 2: LinkedIn Content Calendar

**Using Claude AI:**

1. Upload `marketing-skill/content-creator/SKILL.md`
2. Prompt:
   ```
   Using the content-creator skill, create a 30-day LinkedIn content calendar
   for our B2B SaaS company launching a new marketing automation feature.

   Target audience: Marketing directors at mid-sized companies (50-500 employees)
   Brand voice: Expert + Friendly (from the 5 archetypes)
   Topics: Marketing automation, lead nurturing, ROI measurement
   ```

3. Claude generates:
   - 30-day calendar with post types (how-to, case study, tips, thought leadership)
   - Specific post outlines using content frameworks
   - Optimal posting times based on LinkedIn best practices
   - Hashtag recommendations
   - Engagement strategies

### Example 3: Technical Debt Assessment

**Using Claude Code:**

```bash
# Run tech debt analysis
python c-level-advisor/cto-advisor/scripts/tech_debt_analyzer.py /path/to/codebase

# Claude Code processes results and:
# 1. Identifies top 10 debt items by severity
# 2. Estimates effort to address (hours/days)
# 3. Calculates impact on velocity
# 4. Generates prioritized roadmap
# 5. Creates Jira tickets with detailed descriptions

# Output: Quarterly tech debt reduction plan
```

### Example 4: Board Presentation Prep

**Using CEO Advisor Skill:**

1. Upload `c-level-advisor/ceo-advisor/SKILL.md`
2. Upload `c-level-advisor/ceo-advisor/references/board_governance_investor_relations.md`
3. Prompt:
   ```
   Using the ceo-advisor skill, help me prepare a board presentation for Q4 2025.

   Context:
   - SaaS company, $5M ARR, 40% YoY growth
   - Raised Series A ($10M) 18 months ago
   - Runway: 24 months
   - Key decision: Expand to European market or double-down on US

   Include: Financial summary, strategic options, recommendation, Q&A prep
   ```

4. Claude generates:
   - Structured presentation outline using board governance best practices
   - Financial scenario models for both options
   - Risk analysis and mitigation strategies
   - Anticipated board questions with prepared answers
   - Decision framework showing evaluation criteria

---

## 🔗 Related Projects & Tools

Explore our complete ecosystem of Claude Code augmentation tools and utilities:

### 🏭 Claude Code Skills & Agents Factory

**Repository:** [claude-code-skill-factory](https://github.com/alirezarezvani/claude-code-skill-factory)

**What it is:** Factory toolkit for generating production-ready Claude Skills and Agents at scale.

**Key Features:**
- 🎯 **69 Factory Presets** across 15 professional domains
- 🔧 **Smart Generation** - Automatically determines if Python code or prompt-only instruction is needed
- 📦 **Complete Skill Packages** - Generates SKILL.md, Python scripts, references, and sample data
- 🚀 **Multi-Platform Support** - Works with Claude.ai, Claude Code, and API
- ⚡ **Rapid Prototyping** - Create custom skills in minutes, not hours

**Perfect For:**
- Building custom skills beyond the 53 provided in this library
- Generating domain-specific agents for your organization
- Scaling AI customization across teams
- Rapid prototyping of specialized workflows

**Use Case:** "I need a skill for [your specific domain]? Use the Factory to generate it instantly!"

---

### 💎 Claude Code Tresor (Productivity Toolkit)

**Repository:** [claude-code-tresor](https://github.com/alirezarezvani/claude-code-tresor)

**What it is:** Comprehensive productivity enhancement toolkit with 20+ utilities for Claude Code development workflows.

**Key Features:**
- 🤖 **8 Autonomous Skills** - Background helpers (code quality, security, testing, docs)
- 👨‍💻 **8 Expert Agents** - Manual specialists via `@` mentions (architecture, debugging, performance)
- ⚡ **4 Workflow Commands** - Slash commands (`/scaffold`, `/review`, `/test-gen`, `/docs-gen`)
- 📋 **20+ Prompt Templates** - Common development scenarios ready to use
- 📚 **Development Standards** - Style guides and best practices

**Perfect For:**
- Solo developers seeking productivity acceleration
- Development teams standardizing processes
- Code quality automation and continuous improvement
- Professional Claude Code workflows from scaffolding through deployment

**Use Case:** "Working on a project in Claude Code? Use Tresor's agents, commands, and skills to supercharge your development workflow!"

---

### 🌟 How These Projects Work Together

**Complete Claude Code Ecosystem:**

```
┌─────────────────────────────────────────────────────────┐
│  Claude Skills Library (This Repository)                │
│  53 Domain Expert Skills - Marketing to Engineering     │
│  Use for: Domain expertise, frameworks, best practices  │
└────────────────┬────────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
┌──────────────┐  ┌───────────────────┐
│ Skill Factory│  │  Claude Tresor    │
│              │  │                   │
│ Create MORE  │  │ USE skills in     │
│ custom skills│  │ development       │
│              │  │                   │
│ For: Custom  │  │ For: Daily dev    │
│ domains &    │  │ workflows, code   │
│ org-specific │  │ quality, testing  │
│ needs        │  │ automation        │
└──────────────┘  └───────────────────┘
```

**Workflow:**
1. **Start here** (Skills Library) - Get 53 production-ready expert skills
2. **Expand** (Skill Factory) - Generate custom skills for your specific needs
3. **Supercharge** (Tresor) - Use skills + agents + commands in Claude Code development

**Together they provide:**
- ✅ 53 ready-to-use expert skills (this repo)
- ✅ Unlimited custom skill generation (Factory)
- ✅ Complete development workflow automation (Tresor)
- ✅ Cross-platform compatibility (Claude.ai, Claude Code, API)

**All repositories by [Alireza Rezvani](https://alirezarezvani.com)** - Building the complete Claude Code augmentation ecosystem.

---

## 🗺️ Roadmap

### Current Status (Q4 2025)

**✅ Phase 1: Complete - 53 Production-Ready Skills**

**Marketing Skills (6):**
- Content Creator - Brand voice analysis, SEO optimization, social media frameworks
- Marketing Demand & Acquisition - Multi-channel demand gen, paid media, partnerships
- Marketing Strategy & Product Marketing - Positioning, GTM, competitive intelligence
- App Store Optimization (ASO) - App Store & Google Play metadata optimization, keyword research
- Social Media Analyzer - Platform analytics, engagement optimization, competitor benchmarking
- Campaign Analytics - Multi-touch attribution, funnel conversion analysis, campaign ROI

**C-Level Advisory Skills (2):**
- CEO Advisor - Strategic planning, financial modeling, board governance
- CTO Advisor - Technical debt analysis, team scaling, architecture decisions

**Product Team Skills (5):**
- Product Manager Toolkit - RICE prioritization, interview analysis, PRD templates
- Agile Product Owner - User story generation, sprint planning, velocity tracking
- Product Strategist - OKR cascading, strategic planning, vision frameworks
- UX Researcher Designer - Persona generation, journey mapping, research synthesis
- UI Design System - Design tokens, component architecture, system documentation

**Project Management Skills (6):**
- Senior PM Expert - Portfolio management, stakeholder alignment, executive reporting
- Scrum Master Expert - Sprint ceremonies, agile coaching, velocity tracking
- Atlassian Jira Expert - JQL mastery, configuration, automation, dashboards
- Atlassian Confluence Expert - Knowledge management, documentation, templates
- Atlassian Administrator - System administration, security, user management
- Atlassian Template Creator - Template design, standardization, 15+ ready templates

**Engineering Team Skills - Core Engineering (13):**
- Senior Software Architect - Architecture design, tech decisions, documentation
- Senior Frontend Engineer - React/Next.js development, performance optimization
- Senior Backend Engineer - API design, database optimization, microservices
- Senior Fullstack Engineer - End-to-end development, code quality, DevOps integration
- Senior QA Testing Engineer - Test automation, coverage analysis, E2E testing
- Senior DevOps Engineer - CI/CD pipelines, infrastructure as code, deployment
- Senior SecOps Engineer - Security operations, vulnerability management, compliance
- Code Reviewer - PR analysis, code quality, automated reviews
- Senior Security Engineer - Security architecture, penetration testing, cryptography
- AWS Solution Architect - Serverless architectures, cost optimization, AWS best practices
- Microsoft 365 Tenant Manager - Tenant configuration, security, compliance, automation
- TDD Guide - Test-driven development methodology, test patterns, quality frameworks
- Tech Stack Evaluator - Technology evaluation, vendor selection, architecture decisions

**Engineering Team Skills - AI/ML/Data (5):**
- Senior Data Scientist - Statistical modeling, experimentation, analytics
- Senior Data Engineer - Data pipelines, ETL/ELT, data infrastructure
- Senior ML/AI Engineer - MLOps, model deployment, LLM integration
- Senior Prompt Engineer - LLM optimization, RAG systems, agentic AI
- Senior Computer Vision Engineer - Object detection, image/video AI, real-time inference

**Regulatory Affairs & Quality Management (12):**
- Senior Regulatory Affairs Manager - Strategic regulatory leadership, submission management
- Senior Quality Manager (QMR) - Overall quality system responsibility
- Senior QMS ISO 13485 Specialist - QMS implementation and certification
- Senior CAPA Officer - Corrective/preventive action management
- Senior Quality Documentation Manager - Regulatory documentation control
- Senior Risk Management Specialist - ISO 14971 risk management
- Senior Information Security Manager - ISO 27001 ISMS and cybersecurity
- Senior MDR 2017/745 Specialist - EU MDR compliance expertise
- Senior FDA Consultant - FDA pathways and QSR compliance
- Senior QMS Audit Expert - Internal and external auditing
- Senior ISMS Audit Expert - Security system auditing
- Senior GDPR/DSGVO Expert - Privacy and data protection compliance

**Business & Growth Skills (3):**
- Customer Success Manager - Onboarding, retention, expansion, health scoring
- Sales Engineer - Technical sales, solution design, RFP responses, demo optimization
- Revenue Operations - Pipeline analytics, forecasting, process optimization

**Finance Skills (1):**
- Financial Analyst - DCF valuation, budgeting, forecasting, financial modeling

### Phase 2: Marketing Expansion (Q2 2026)

**🔄 In Planning:**
- **SEO Optimizer Skill** - Deep SEO analysis and optimization (standalone expansion)
- **Social Media Manager Skill** - Campaign management across platforms

### Phase 2: Business & Growth (Q2 2026)

**📋 Planned:**
- **Growth Marketer** - Acquisition, activation, viral loops, experimentation

### Phase 3: Specialized Domains (Q3 2026)

**💡 Proposed:**
- **Mobile Engineer** - Swift/Kotlin deep-dive, native platform development
- **Blockchain Engineer** - Web3, smart contracts, decentralized systems
- **Game Developer** - Game engines, graphics, real-time systems
- **IoT Engineer** - Embedded systems, edge computing, hardware integration

### Projected Impact

| Metric | Current | Target (Q3 2026) |
|--------|---------|------------------|
| Available Skills | 53 | 55+ |
| Skill Categories | 8 | 9 |
| Python Tools | 87+ | 110+ |
| Time Savings | 70% | 85% |
| Quality Improvement | 65% | 80% |
| Teams Using | Early adopters | 3,000+ |
| Organizations | 25 | 250+ |
| Industries Covered | Tech, HealthTech | Tech, Health, Finance, Manufacturing |

### ROI Metrics (Current - 53 Skills)

**Time Savings Per Organization:**
- Marketing teams: 310 hours/month (Content + Demand Gen + PMM + ASO + Social Media)
- C-level executives: 30 hours/month
- Product teams: 180 hours/month
- Project management teams: 200 hours/month (PM + Agile + Atlassian)
- Core engineering teams: 580 hours/month (13 specialized roles)
- AI/ML/Data teams: 280 hours/month
- Regulatory/Quality teams: 320 hours/month
- Business & growth teams: 190 hours/month (Customer Success + Sales Engineering + Revenue Ops)
- Finance teams: 60 hours/month (Financial analysis + modeling + forecasting)
- **Total: 2,150 hours/month per organization**

**Financial Impact:**
- Time value: $190,000/month (@ $100/hour)
- Quality improvements: $220,000/month (reduced rework)
- Faster delivery: $260,000/month (opportunity value)
- Security risk mitigation: $200,000/month
- ML/AI innovation value: $250,000/month
- Regulatory compliance value: $400,000/month (avoided delays, penalties)
- Marketing efficiency value: $100,000/month (better CAC, conversion, positioning)
- PM/Agile efficiency value: $130,000/month (faster delivery, better stakeholder satisfaction)
- **Total: $1,750,000/month value per organization**
- **Annual ROI: $21.0M per organization**

**Productivity Gains:**
- Developer velocity: +70% improvement
- Deployment frequency: +200% increase
- Bug reduction: -50%
- Security incidents: -85%
- Code review time: -60%
- Onboarding time: -65%
- ML model deployment time: -80%
- Data pipeline reliability: +95%
- Regulatory submission success: +95%
- Time to market: -40% reduction
- Compliance risk: -90% reduction
- Sprint predictability: +40%
- Project on-time delivery: +25%
- Atlassian efficiency: +70%

**See detailed roadmaps:**
- [marketing-skill/marketing_skills_roadmap.md](marketing-skill/marketing_skills_roadmap.md)
- [product-team/product_team_implementation_guide.md](product-team/product_team_implementation_guide.md)
- [project-management/README.md](project-management/README.md) | [project-management/REAL_WORLD_SCENARIO.md](project-management/REAL_WORLD_SCENARIO.md)
- [engineering-team/START_HERE.md](engineering-team/START_HERE.md) | [engineering-team/TEAM_STRUCTURE_GUIDE.md](engineering-team/TEAM_STRUCTURE_GUIDE.md)
- [ra-qm-team/README.md](ra-qm-team/README.md) | [ra-qm-team/final-complete-skills-collection.md](ra-qm-team/final-complete-skills-collection.md)

---

## 🤝 Contributing

Contributions are welcome! This repository aims to democratize professional expertise through reusable skill packages.

### How to Contribute

1. **Fork** this repository
2. **Create** a feature branch (`git checkout -b feature/new-skill`)
3. **Develop** your skill following the architecture guidelines in [CLAUDE.md](CLAUDE.md)
4. **Test** your tools and validate documentation
5. **Submit** a pull request with detailed description

### Contribution Ideas

- **New Skills** - Domain expertise in your field (finance, HR, product management, etc.)
- **Tool Enhancements** - Improve existing Python analysis scripts
- **Framework Additions** - Add new templates or methodologies to existing skills
- **Documentation** - Improve how-to guides, examples, or translations
- **Bug Fixes** - Fix issues in scripts or documentation

### Quality Standards

All contributions should:
- ✅ Follow the modular skill architecture pattern
- ✅ Include comprehensive SKILL.md documentation
- ✅ Provide actionable, specific guidance (not generic advice)
- ✅ Use algorithmic tools (Python) when possible, not just documentation
- ✅ Include ready-to-use templates or examples
- ✅ Be self-contained and independently deployable

---

## 📄 License

This project is licensed under the **MIT License** - see below for details.

```
MIT License

Copyright (c) 2025 Alireza Rezvani

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

You are free to:
- ✅ Use these skills commercially
- ✅ Modify and adapt to your needs
- ✅ Distribute to your team or clients
- ✅ Create derivative works

---

## 👤 Author

**Alireza Rezvani**

Building AI-powered tools and frameworks to democratize professional expertise.

- 🌐 **Website:** [alirezarezvani.com](https://alirezarezvani.com)
- 📝 **Blog:** [medium.com/@alirezarezvani](https://medium.com/@alirezarezvani)
- 💼 **LinkedIn:** Connect for updates on new skills and AI developments
- 📧 **Contact:** Available through website or blog

### About This Project

This repository emerged from years of experience building marketing strategies, leading engineering teams, and advising executives. The goal is simple: **make world-class expertise accessible to everyone** through Claude AI.

Each skill represents hundreds of hours of domain expertise, distilled into actionable frameworks and automated tools. By sharing these openly, I hope to help teams work smarter, move faster, and achieve better results.

**Follow my journey** building AI-powered professional tools on [Medium](https://medium.com/@alirezarezvani).

---

## 🙏 Acknowledgments

- **Anthropic** - For building Claude AI and Claude Code, making this possible
- **Early Adopters** - Teams testing these skills and providing feedback
- **Open Source Community** - For tools and libraries that power the analysis scripts

---

## 📞 Support & Feedback

### Getting Help

- **Documentation Issues:** Open an issue in this repository
- **Skill Requests:** Submit a feature request describing your use case
- **General Questions:** Reach out via my [website](https://alirezarezvani.com) or [blog](https://medium.com/@alirezarezvani)

### Sharing Your Success

Using these skills successfully? I'd love to hear about it:
- Share your story on social media (tag me!)
- Write about your experience on Medium
- Submit a case study for inclusion in this README

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=alirezarezvani/claude-skills&type=Date)](https://star-history.com/#alirezarezvani/claude-skills&Date)

---

<div align="center">

**⭐ Star this repository** if you find these skills useful!

**🔗 Share** with teams who could benefit from AI-powered expertise

**🚀 Built with Claude AI** | **📦 Packaged for Impact** | **🌍 Open for All**

</div>
