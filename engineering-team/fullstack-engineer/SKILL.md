---
name: fullstack-engineer
description: Comprehensive fullstack development skill for building modern web applications with React, Next.js, Node.js, GraphQL, and PostgreSQL. Includes project scaffolding, code quality analysis, architecture patterns, and complete tech stack guidance. Use when building new projects, analyzing code quality, implementing design patterns, or setting up development workflows.
---

# Fullstack Engineer

Complete toolkit for fullstack development with modern web technologies and best practices.

## Quick Start

### New Project Setup
```bash
# Scaffold a new fullstack project
python scripts/project_scaffolder.py my-project --type nextjs-graphql

# Navigate to project
cd my-project

# Start with Docker
docker-compose up -d

# Or install manually
cd frontend && npm install
cd ../backend && npm install
```

### Code Quality Check
```bash
# Analyze existing project
python scripts/code_quality_analyzer.py /path/to/project

# Get JSON report
python scripts/code_quality_analyzer.py /path/to/project --json
```

## Core Capabilities

### 1. Project Scaffolding

The `project_scaffolder.py` creates production-ready project structures:

- **Next.js + GraphQL + PostgreSQL** stack
- Docker Compose configuration
- CI/CD pipeline with GitHub Actions
- Testing setup (Jest, Cypress)
- TypeScript configuration
- ESLint + Prettier
- Environment management

**Usage:**
```bash
python scripts/project_scaffolder.py <project-name> --type nextjs-graphql
```

### 2. Code Quality Analysis

The `code_quality_analyzer.py` provides comprehensive analysis:

- Code metrics (LOC, complexity, languages)
- Security vulnerability scanning
- Performance issue detection
- Test coverage assessment
- Documentation quality
- Dependency analysis

**Usage:**
```bash
python scripts/code_quality_analyzer.py <project-path>
```

### 3. Architecture Patterns

Reference comprehensive patterns in `references/architecture_patterns.md`:

- **System Architecture**: Monolithic, Microservices, Serverless
- **Frontend Patterns**: Component architecture, State management
- **Backend Patterns**: Clean architecture, Repository pattern
- **Database Patterns**: Migrations, Query builders
- **Security Patterns**: Authentication, Authorization
- **Testing Patterns**: Unit, Integration, E2E

### 4. Development Workflows

Complete workflow guide in `references/development_workflows.md`:

- Git workflow (GitFlow, PR process)
- Development environment setup
- Testing strategies
- CI/CD pipelines
- Monitoring & observability
- Security best practices
- Documentation standards

### 5. Tech Stack Guide

Detailed implementation guide in `references/tech_stack_guide.md`:

- **Frontend**: React, Next.js, React Native, Flutter
- **Backend**: Node.js, Express, GraphQL, Go, Python
- **Database**: PostgreSQL, Prisma, Knex.js
- **Infrastructure**: Docker, Kubernetes, Terraform
- **Mobile**: Swift, Kotlin, React Native

## Project Structure Templates

### Monolithic Structure
```
project/
├── src/
│   ├── client/          # Frontend code
│   ├── server/          # Backend code
│   ├── shared/          # Shared types
│   └── database/        # DB schemas
├── tests/
├── docker/
└── .github/workflows/
```

### Microservices Structure
```
project/
├── services/
│   ├── auth/
│   ├── users/
│   ├── products/
│   └── gateway/
├── shared/
├── infrastructure/
└── docker-compose.yml
```

## Development Workflow

### 1. Starting New Project

```bash
# Create project
python scripts/project_scaffolder.py awesome-app --type nextjs-graphql

# Setup environment
cd awesome-app
cp .env.example .env
# Edit .env with your values

# Start development
docker-compose up -d

# Access services
# Frontend: http://localhost:3000
# GraphQL: http://localhost:4000/graphql
# Database: localhost:5432
```

### 2. Code Quality Checks

Before committing code:

```bash
# Run quality analyzer
python scripts/code_quality_analyzer.py .

# Fix issues based on report
# - Security vulnerabilities (Critical)
# - Performance issues (High)
# - Complexity issues (Medium)
# - Documentation gaps (Low)
```

### 3. Architecture Decision

Use the architecture patterns reference to choose:

1. **System Architecture**
   - Small project → Monolithic
   - Large team → Microservices
   - Variable load → Serverless

2. **State Management**
   - Simple → Context API
   - Medium → Zustand
   - Complex → Redux Toolkit

3. **Database Strategy**
   - Rapid development → Prisma
   - Full control → Knex.js
   - Serverless → NeonDB

## Testing Strategy

### Test Pyramid Implementation

```
     E2E (10%)      - Critical paths only
    Integration (30%) - API, Database
   Unit Tests (60%)   - Logic, Components
```

### Running Tests

```bash
# Unit tests
npm run test:unit

# Integration tests
npm run test:integration

# E2E tests
npm run test:e2e

# All with coverage
npm run test:coverage
```

## Security Checklist

Before deployment, ensure:

- [ ] No hardcoded secrets
- [ ] Input validation implemented
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] CORS configured
- [ ] Rate limiting active
- [ ] Security headers set
- [ ] Dependencies updated

## Performance Optimization

### Frontend
- Code splitting with dynamic imports
- Image optimization (WebP, lazy loading)
- Bundle size analysis
- React component memoization
- Virtual scrolling for large lists

### Backend
- Database query optimization
- Caching strategy (Redis)
- Connection pooling
- Pagination implementation
- N+1 query prevention

### Infrastructure
- CDN configuration
- Horizontal scaling
- Load balancing
- Database indexing
- Container optimization

## Deployment Guide

### Development
```bash
docker-compose up -d
```

### Staging
```bash
docker build -t app:staging .
docker push registry/app:staging
kubectl apply -f k8s/staging/
```

### Production
```bash
# Build and tag
docker build -t app:v1.0.0 .
docker push registry/app:v1.0.0

# Deploy with zero downtime
kubectl set image deployment/app app=registry/app:v1.0.0
kubectl rollout status deployment/app
```

## Monitoring & Debugging

### Health Checks
```typescript
// Backend health endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: Date.now(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
  });
});
```

### Logging
```typescript
// Structured logging
logger.info('Request processed', {
  method: req.method,
  path: req.path,
  duration: responseTime,
  userId: req.user?.id,
});
```

### Error Tracking
- Sentry for error monitoring
- New Relic for APM
- CloudWatch for logs
- Grafana for metrics

## Best Practices Summary

### Code Organization
- Feature-based structure
- Consistent naming conventions
- Clear separation of concerns
- Reusable components

### Development Process
- Write tests first (TDD)
- Code review everything
- Document decisions
- Automate repetitive tasks

### Performance
- Measure before optimizing
- Cache aggressively
- Optimize database queries
- Use CDN for assets

### Security
- Never trust user input
- Use parameterized queries
- Implement rate limiting
- Keep dependencies updated

## Common Commands Reference

```bash
# Development
npm run dev              # Start development server
npm run build           # Build for production
npm run test            # Run tests
npm run lint            # Lint code
npm run format          # Format code

# Database
npm run db:migrate      # Run migrations
npm run db:seed         # Seed database
npm run db:reset        # Reset database

# Docker
docker-compose up       # Start services
docker-compose down     # Stop services
docker-compose logs -f  # View logs
docker-compose exec app sh  # Shell into container

# Kubernetes
kubectl get pods        # List pods
kubectl logs <pod>      # View logs
kubectl exec -it <pod> sh  # Shell into pod
kubectl rollout restart deployment/app  # Restart deployment
```

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
lsof -i :3000  # Find process
kill -9 <PID>  # Kill process
```

**Docker connection issues:**
```bash
docker-compose down -v  # Remove volumes
docker system prune -a  # Clean everything
```

**Database migration errors:**
```bash
npm run db:rollback    # Rollback migration
npm run db:migrate     # Re-run migrations
```

## Resources

- Architecture Patterns: See `references/architecture_patterns.md`
- Development Workflows: See `references/development_workflows.md`
- Tech Stack Guide: See `references/tech_stack_guide.md`
- Project Scaffolder: Use `scripts/project_scaffolder.py`
- Code Analyzer: Use `scripts/code_quality_analyzer.py`
