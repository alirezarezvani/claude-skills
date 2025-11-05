# Engineering Team Skills - Claude Code Guidance

This guide covers the 14 production-ready engineering skills and their Python automation tools.

## Engineering Skills Overview

**Core Engineering (9 skills):**
- senior-architect, senior-frontend, senior-backend, senior-fullstack
- senior-qa, senior-devops, senior-secops
- code-reviewer, senior-security

**AI/ML/Data (5 skills):**
- senior-data-scientist, senior-data-engineer, senior-ml-engineer
- senior-prompt-engineer, senior-computer-vision

**Total Tools:** 30+ Python automation tools

## Core Engineering Tools

### 1. Project Scaffolder (`senior-fullstack/scripts/project_scaffolder.py`)

**Purpose:** Production-ready project scaffolding for modern stacks

**Supported Stacks:**
- Next.js + GraphQL + PostgreSQL
- React + REST + MongoDB
- Vue + GraphQL + MySQL
- Express + TypeScript + PostgreSQL

**Features:**
- Docker Compose configuration
- CI/CD pipeline (GitHub Actions)
- Testing infrastructure (Jest, Cypress)
- TypeScript + ESLint + Prettier
- Database migrations

**Usage:**
```bash
# Create new project
python senior-fullstack/scripts/project_scaffolder.py my-project --type nextjs-graphql

# Start services
cd my-project && docker-compose up -d
```

### 2. Code Quality Analyzer (`senior-fullstack/scripts/code_quality_analyzer.py`)

**Purpose:** Comprehensive code quality analysis and metrics

**Features:**
- Security vulnerability scanning
- Performance issue detection
- Test coverage assessment
- Documentation quality
- Dependency analysis
- Actionable recommendations

**Usage:**
```bash
# Analyze project
python senior-fullstack/scripts/code_quality_analyzer.py /path/to/project

# JSON output
python senior-fullstack/scripts/code_quality_analyzer.py /path/to/project --json
```

**Output:**
```
Code Quality Report:
- Overall Score: 85/100
- Security: 90/100 (2 medium issues)
- Performance: 80/100 (3 optimization opportunities)
- Test Coverage: 75% (target: 80%)
- Documentation: 88/100

Recommendations:
1. Update lodash to 4.17.21 (CVE-2020-8203)
2. Optimize database queries in UserService
3. Add integration tests for payment flow
```

### 3. Fullstack Scaffolder (`senior-fullstack/scripts/fullstack_scaffolder.py`)

**Purpose:** Rapid fullstack application generation

**Usage:**
```bash
python senior-fullstack/scripts/fullstack_scaffolder.py my-app --stack nextjs-graphql
```

## AI/ML/Data Tools

### Data Science Tools

**Experiment Designer** (`senior-data-scientist/scripts/experiment_designer.py`)
- A/B test design
- Statistical power analysis
- Sample size calculation

**Feature Engineering Pipeline** (`senior-data-scientist/scripts/feature_engineering_pipeline.py`)
- Automated feature generation
- Correlation analysis
- Feature selection

**Statistical Analyzer** (`senior-data-scientist/scripts/statistical_analyzer.py`)
- Hypothesis testing
- Causal inference
- Regression analysis

### Data Engineering Tools

**Pipeline Orchestrator** (`senior-data-engineer/scripts/pipeline_orchestrator.py`)
- Airflow DAG generation
- Spark job templates
- Data quality checks

**Data Quality Validator** (`senior-data-engineer/scripts/data_quality_validator.py`)
- Schema validation
- Null check enforcement
- Anomaly detection

**ETL Generator** (`senior-data-engineer/scripts/etl_generator.py`)
- Extract-Transform-Load workflows
- CDC (Change Data Capture) patterns
- Incremental loading

### ML Engineering Tools

**Model Deployment Pipeline** (`senior-ml-engineer/scripts/model_deployment_pipeline.py`)
- Containerized model serving
- REST API generation
- Load balancing config

**MLOps Setup Tool** (`senior-ml-engineer/scripts/mlops_setup_tool.py`)
- MLflow configuration
- Model versioning
- Drift monitoring

**LLM Integration Builder** (`senior-ml-engineer/scripts/llm_integration_builder.py`)
- OpenAI API integration
- Prompt templates
- Response parsing

### Prompt Engineering Tools

**Prompt Optimizer** (`senior-prompt-engineer/scripts/prompt_optimizer.py`)
- Prompt A/B testing
- Token optimization
- Few-shot example generation

**RAG System Builder** (`senior-prompt-engineer/scripts/rag_system_builder.py`)
- Vector database setup
- Embedding generation
- Retrieval strategies

**Agent Orchestrator** (`senior-prompt-engineer/scripts/agent_orchestrator.py`)
- Multi-agent workflows
- Tool calling patterns
- State management

### Computer Vision Tools

**Vision Model Trainer** (`senior-computer-vision/scripts/vision_model_trainer.py`)
- Object detection (YOLO, Faster R-CNN)
- Semantic segmentation
- Transfer learning

**Inference Optimizer** (`senior-computer-vision/scripts/inference_optimizer.py`)
- Model quantization
- TensorRT optimization
- ONNX export

**Video Processor** (`senior-computer-vision/scripts/video_processor.py`)
- Frame extraction
- Object tracking
- Scene detection

## Tech Stack Patterns

### Frontend (React/Next.js)
- TypeScript strict mode
- Component-driven architecture
- Atomic design patterns
- State management (Zustand/Jotai)
- Testing (Jest + React Testing Library)

### Backend (Node.js/Express)
- Clean architecture
- Dependency injection
- Repository pattern
- Domain-driven design
- Testing (Jest + Supertest)

### Fullstack Integration
- GraphQL for API layer
- REST for external services
- WebSocket for real-time
- Redis for caching
- PostgreSQL for persistence

## Development Workflows

### Workflow 1: New Project Setup

```bash
# 1. Scaffold project
python senior-fullstack/scripts/project_scaffolder.py my-app --type nextjs-graphql

# 2. Start services
cd my-app && docker-compose up -d

# 3. Run migrations
npm run migrate

# 4. Start development
npm run dev
```

### Workflow 2: Code Quality Check

```bash
# 1. Analyze codebase
python senior-fullstack/scripts/code_quality_analyzer.py ./

# 2. Fix security issues
npm audit fix

# 3. Run tests
npm test

# 4. Build production
npm run build
```

### Workflow 3: ML Model Deployment

```bash
# 1. Setup MLOps infrastructure
python senior-ml-engineer/scripts/mlops_setup_tool.py

# 2. Deploy model
python senior-ml-engineer/scripts/model_deployment_pipeline.py model.pkl

# 3. Monitor performance
# Check MLflow dashboard
```

## Quality Standards

**All engineering tools must:**
- Support modern tech stacks (Next.js, React, Vue, Express)
- Generate production-ready code
- Include testing infrastructure
- Provide Docker configurations
- Support CI/CD integration

## Integration Patterns

### GitHub Actions CI/CD

All scaffolders generate GitHub Actions workflows:
```yaml
.github/workflows/
├── test.yml          # Run tests on PR
├── build.yml         # Build and lint
└── deploy.yml        # Deploy to production
```

### Docker Compose

Multi-service development environment:
```yaml
services:
  - app (Next.js)
  - api (GraphQL)
  - db (PostgreSQL)
  - redis (Cache)
```

## Additional Resources

- **Quick Start:** `START_HERE.md`
- **Team Structure:** `TEAM_STRUCTURE_GUIDE.md`
- **Engineering Roadmap:** `engineering_skills_roadmap.md` (if exists)
- **Main Documentation:** `../CLAUDE.md`

---

**Last Updated:** November 5, 2025
**Skills Deployed:** 14/14 engineering skills production-ready
**Total Tools:** 30+ Python automation tools across core + AI/ML/Data
