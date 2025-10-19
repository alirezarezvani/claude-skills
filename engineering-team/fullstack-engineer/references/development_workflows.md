# Development Workflows & Best Practices

## Git Workflow

### 1. GitFlow Model
```
main (production)
    ├── hotfix/critical-bug
    └── release/v1.2.0
          └── develop
                ├── feature/user-auth
                ├── feature/payment-integration
                └── bugfix/login-error
```

#### Branch Naming Conventions
- `feature/` - New features
- `bugfix/` - Bug fixes in development
- `hotfix/` - Critical production fixes
- `release/` - Release preparation
- `chore/` - Maintenance tasks
- `docs/` - Documentation updates

#### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `perf`: Performance improvement
- `test`: Testing
- `chore`: Maintenance
- `ci`: CI/CD changes

**Examples:**
```bash
git commit -m "feat(auth): add JWT authentication

- Implement login endpoint
- Add JWT token generation
- Add refresh token mechanism

Closes #123"
```

### 2. Pull Request Workflow

#### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests added/updated
- [ ] All tests passing

## Screenshots (if applicable)
[Add screenshots]

## Related Issues
Closes #issue_number
```

#### Code Review Checklist
- **Functionality**: Does it work as expected?
- **Design**: Is the code well-designed?
- **Complexity**: Could it be simpler?
- **Tests**: Are there adequate tests?
- **Naming**: Are names clear and consistent?
- **Comments**: Are comments necessary and helpful?
- **Style**: Does it follow style guides?
- **Documentation**: Is documentation updated?
- **Performance**: Any performance concerns?
- **Security**: Any security issues?

### 3. Branching Strategies

#### Feature Branch Workflow
```bash
# Create feature branch
git checkout -b feature/user-profile

# Work on feature
git add .
git commit -m "feat: add user profile page"

# Keep branch updated
git checkout develop
git pull origin develop
git checkout feature/user-profile
git rebase develop

# Push and create PR
git push origin feature/user-profile
```

#### Release Process
```bash
# Create release branch
git checkout -b release/v1.2.0 develop

# Bump version
npm version minor

# Final testing and fixes
git commit -m "fix: resolve release issues"

# Merge to main
git checkout main
git merge --no-ff release/v1.2.0
git tag -a v1.2.0 -m "Release version 1.2.0"

# Merge back to develop
git checkout develop
git merge --no-ff release/v1.2.0

# Clean up
git branch -d release/v1.2.0
git push origin main develop --tags
```

## Development Environment Setup

### 1. VS Code Configuration

#### Essential Extensions
```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-typescript-next",
    "bradlc.vscode-tailwindcss",
    "prisma.prisma",
    "graphql.vscode-graphql",
    "eamodio.gitlens",
    "github.copilot",
    "ms-azuretools.vscode-docker",
    "mikestead.dotenv",
    "usernamehw.errorlens",
    "yoavbls.pretty-ts-errors"
  ]
}
```

#### Settings.json
```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true,
    "source.organizeImports": true
  },
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "typescript.updateImportsOnFileMove.enabled": "always",
  "typescript.preferences.includePackageJsonAutoImports": "on",
  "files.exclude": {
    "**/.git": true,
    "**/.DS_Store": true,
    "**/node_modules": true,
    "**/dist": true,
    "**/.next": true
  },
  "search.exclude": {
    "**/node_modules": true,
    "**/dist": true,
    "**/.next": true,
    "**/coverage": true
  }
}
```

### 2. Pre-commit Hooks

#### Husky + Lint-staged Setup
```bash
npm install -D husky lint-staged

npx husky install
npx husky add .husky/pre-commit "npx lint-staged"
```

#### .lintstagedrc.json
```json
{
  "*.{ts,tsx,js,jsx}": [
    "eslint --fix",
    "prettier --write"
  ],
  "*.{json,md,yml,yaml}": [
    "prettier --write"
  ],
  "*.test.{ts,tsx}": [
    "jest --bail --findRelatedTests"
  ]
}
```

### 3. Environment Management

#### .env Structure
```bash
# .env.local (development)
NODE_ENV=development
DATABASE_URL=postgresql://dev:dev@localhost:5432/devdb
REDIS_URL=redis://localhost:6379
API_URL=http://localhost:4000
NEXT_PUBLIC_API_URL=http://localhost:4000

# .env.test (testing)
NODE_ENV=test
DATABASE_URL=postgresql://test:test@localhost:5432/testdb
REDIS_URL=redis://localhost:6380
API_URL=http://localhost:4001

# .env.production (production)
NODE_ENV=production
DATABASE_URL=${SECRET_DATABASE_URL}
REDIS_URL=${SECRET_REDIS_URL}
API_URL=https://api.example.com
```

#### Environment Validation
```typescript
// env.config.ts
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']),
  DATABASE_URL: z.string().url(),
  REDIS_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  PORT: z.string().transform(Number).default('4000'),
});

export const env = envSchema.parse(process.env);
```

## Testing Strategy

### 1. Test Pyramid

```
        /\        E2E Tests (10%)
       /  \       - Critical user journeys
      /    \      - Cross-browser testing
     /      \     
    /        \    Integration Tests (30%)
   /          \   - API endpoints
  /            \  - Database operations
 /              \ - Service interactions
/________________\
                  Unit Tests (60%)
                  - Business logic
                  - Utilities
                  - Components
```

### 2. Testing Best Practices

#### AAA Pattern (Arrange, Act, Assert)
```typescript
describe('UserService', () => {
  it('should create a user successfully', async () => {
    // Arrange
    const userData = {
      email: 'test@example.com',
      password: 'SecurePass123!',
    };
    const mockRepo = createMockRepository();
    const service = new UserService(mockRepo);
    
    // Act
    const user = await service.createUser(userData);
    
    // Assert
    expect(user).toBeDefined();
    expect(user.email).toBe(userData.email);
    expect(mockRepo.save).toHaveBeenCalledWith(
      expect.objectContaining({ email: userData.email })
    );
  });
});
```

#### Test Data Builders
```typescript
class UserBuilder {
  private user: Partial<User> = {
    id: '123',
    email: 'test@example.com',
    name: 'Test User',
    role: 'user',
  };
  
  withEmail(email: string): this {
    this.user.email = email;
    return this;
  }
  
  withRole(role: UserRole): this {
    this.user.role = role;
    return this;
  }
  
  withVerified(verified = true): this {
    this.user.isVerified = verified;
    return this;
  }
  
  build(): User {
    return this.user as User;
  }
}

// Usage
const adminUser = new UserBuilder()
  .withRole('admin')
  .withVerified()
  .build();
```

### 3. Test Coverage Goals

- **Overall**: 80%+
- **Critical paths**: 95%+
- **Utilities**: 100%
- **UI Components**: 70%+
- **E2E**: Critical flows only

## Code Quality Standards

### 1. TypeScript Configuration

#### Strict tsconfig.json
```json
{
  "compilerOptions": {
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "resolveJsonModule": true
  }
}
```

### 2. Code Organization

#### Folder Structure
```
src/
├── components/          # Reusable UI components
│   ├── common/
│   ├── forms/
│   └── layouts/
├── features/           # Feature-based modules
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── types/
│   └── users/
├── hooks/             # Shared React hooks
├── lib/               # Third-party configurations
├── services/          # API and business logic
├── stores/            # State management
├── types/             # TypeScript definitions
├── utils/             # Utility functions
└── config/            # App configuration
```

#### Import Order
```typescript
// 1. External imports
import React from 'react';
import { useQuery } from '@tanstack/react-query';

// 2. Internal aliases
import { Button } from '@/components/common';
import { useAuth } from '@/hooks';

// 3. Relative imports
import { UserCard } from './UserCard';
import styles from './UserList.module.css';

// 4. Type imports
import type { User } from '@/types';
```

### 3. Performance Guidelines

#### React Optimization
```typescript
// Memoization
const ExpensiveComponent = React.memo(({ data }) => {
  return <div>{/* Render logic */}</div>;
}, (prevProps, nextProps) => {
  // Custom comparison
  return prevProps.data.id === nextProps.data.id;
});

// useMemo for expensive calculations
const processedData = useMemo(() => {
  return heavyDataProcessing(rawData);
}, [rawData]);

// useCallback for stable references
const handleSubmit = useCallback((values: FormValues) => {
  submitForm(values);
}, [submitForm]);

// Code splitting
const AdminPanel = lazy(() => import('./AdminPanel'));

// Virtual scrolling for large lists
import { FixedSizeList } from 'react-window';

function LargeList({ items }) {
  return (
    <FixedSizeList
      height={600}
      itemCount={items.length}
      itemSize={50}
      width="100%"
    >
      {({ index, style }) => (
        <div style={style}>
          {items[index].name}
        </div>
      )}
    </FixedSizeList>
  );
}
```

#### Database Optimization
```typescript
// Query optimization
// Bad - Multiple queries
const users = await db('users').select('*');
for (const user of users) {
  user.posts = await db('posts').where('user_id', user.id);
}

// Good - Single query with join
const users = await db('users')
  .leftJoin('posts', 'users.id', 'posts.user_id')
  .select('users.*', db.raw('json_agg(posts.*) as posts'))
  .groupBy('users.id');

// Indexing strategy
await knex.schema.createTable('users', (table) => {
  table.uuid('id').primary();
  table.string('email').unique();
  table.timestamp('created_at');
  
  // Indexes for common queries
  table.index(['email', 'created_at']);
  table.index('created_at');
});

// Connection pooling
const db = knex({
  client: 'pg',
  connection: DATABASE_URL,
  pool: {
    min: 2,
    max: 10,
    acquireTimeoutMillis: 30000,
    createTimeoutMillis: 30000,
    destroyTimeoutMillis: 5000,
    idleTimeoutMillis: 30000,
    reapIntervalMillis: 1000,
  },
});
```

## CI/CD Pipeline

### 1. GitHub Actions Workflow

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  NODE_VERSION: '18'
  PNPM_VERSION: '8'

jobs:
  # Quality checks
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup pnpm
        uses: pnpm/action-setup@v2
        with:
          version: ${{ env.PNPM_VERSION }}
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'
      
      - name: Install dependencies
        run: pnpm install --frozen-lockfile
      
      - name: Lint
        run: pnpm lint
      
      - name: Type check
        run: pnpm type-check
      
      - name: Format check
        run: pnpm format:check

  # Testing
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup environment
        uses: ./.github/actions/setup
      
      - name: Run unit tests
        run: pnpm test:unit
      
      - name: Run integration tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
        run: |
          pnpm db:migrate
          pnpm test:integration
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  # Build
  build:
    needs: [quality, test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup environment
        uses: ./.github/actions/setup
      
      - name: Build application
        run: pnpm build
      
      - name: Build Docker image
        run: docker build -t app:${{ github.sha }} .
      
      - name: Push to registry
        if: github.ref == 'refs/heads/main'
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push app:${{ github.sha }}

  # Deploy
  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ${{ secrets.PROD_USER }}
          key: ${{ secrets.PROD_SSH_KEY }}
          script: |
            docker pull app:${{ github.sha }}
            docker stop app || true
            docker rm app || true
            docker run -d --name app -p 80:3000 app:${{ github.sha }}
```

### 2. Deployment Checklist

#### Pre-deployment
- [ ] All tests passing
- [ ] Code review approved
- [ ] Database migrations ready
- [ ] Environment variables updated
- [ ] Feature flags configured
- [ ] Monitoring alerts set up
- [ ] Rollback plan prepared

#### Deployment
- [ ] Deploy to staging
- [ ] Run smoke tests
- [ ] Check monitoring dashboards
- [ ] Deploy to production (canary/blue-green)
- [ ] Verify health checks
- [ ] Monitor error rates

#### Post-deployment
- [ ] Verify key metrics
- [ ] Check user feedback
- [ ] Document any issues
- [ ] Update status page
- [ ] Team retrospective

## Monitoring & Observability

### 1. Logging Strategy

```typescript
// Winston logger configuration
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'api' },
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
  ],
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.combine(
      winston.format.colorize(),
      winston.format.simple()
    ),
  }));
}

// Request logging middleware
app.use((req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    
    logger.info('Request processed', {
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration,
      userId: req.user?.id,
      ip: req.ip,
      userAgent: req.get('user-agent'),
    });
  });
  
  next();
});
```

### 2. Error Tracking

```typescript
// Sentry integration
import * as Sentry from '@sentry/node';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  integrations: [
    new Sentry.Integrations.Http({ tracing: true }),
    new Sentry.Integrations.Express({ app }),
  ],
  tracesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,
  beforeSend(event, hint) {
    // Filter sensitive data
    if (event.request?.cookies) {
      delete event.request.cookies;
    }
    return event;
  },
});

// Error boundary for React
class ErrorBoundary extends React.Component {
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    Sentry.withScope((scope) => {
      scope.setExtras(errorInfo);
      Sentry.captureException(error);
    });
  }
  
  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}
```

### 3. Performance Monitoring

```typescript
// Custom metrics with Prometheus
import { register, Counter, Histogram, Gauge } from 'prom-client';

const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status'],
});

const activeConnections = new Gauge({
  name: 'active_connections',
  help: 'Number of active connections',
});

const requestCounter = new Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status'],
});

// Metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});
```

## Security Best Practices

### 1. Authentication & Authorization

```typescript
// Secure password hashing
import bcrypt from 'bcryptjs';

const SALT_ROUNDS = 12;

export async function hashPassword(password: string): Promise<string> {
  return bcrypt.hash(password, SALT_ROUNDS);
}

export async function verifyPassword(
  password: string, 
  hash: string
): Promise<boolean> {
  return bcrypt.compare(password, hash);
}

// JWT with refresh tokens
interface TokenPair {
  accessToken: string;
  refreshToken: string;
}

export function generateTokens(userId: string): TokenPair {
  const accessToken = jwt.sign(
    { sub: userId },
    process.env.JWT_SECRET!,
    { expiresIn: '15m' }
  );
  
  const refreshToken = jwt.sign(
    { sub: userId },
    process.env.JWT_REFRESH_SECRET!,
    { expiresIn: '7d' }
  );
  
  return { accessToken, refreshToken };
}

// Session management with Redis
async function createSession(userId: string): Promise<string> {
  const sessionId = crypto.randomUUID();
  const sessionData = {
    userId,
    createdAt: Date.now(),
    lastActivity: Date.now(),
  };
  
  await redis.setex(
    `session:${sessionId}`,
    3600, // 1 hour
    JSON.stringify(sessionData)
  );
  
  return sessionId;
}
```

### 2. Input Validation & Sanitization

```typescript
// Input validation with Zod
import { z } from 'zod';
import DOMPurify from 'isomorphic-dompurify';

const UserInputSchema = z.object({
  email: z.string().email().toLowerCase(),
  username: z.string()
    .min(3)
    .max(20)
    .regex(/^[a-zA-Z0-9_]+$/, 'Username can only contain letters, numbers, and underscores'),
  bio: z.string()
    .max(500)
    .transform(val => DOMPurify.sanitize(val)), // Sanitize HTML
  age: z.number().int().positive().max(150),
  website: z.string().url().optional(),
});

// SQL injection prevention with parameterized queries
// Never do this:
const query = `SELECT * FROM users WHERE email = '${email}'`;

// Always do this:
const user = await db('users').where({ email }).first();
// Or with raw queries:
const user = await db.raw(
  'SELECT * FROM users WHERE email = ?',
  [email]
);
```

### 3. Security Headers

```typescript
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'"],
      fontSrc: ["'self'"],
      objectSrc: ["'none'"],
      mediaSrc: ["'self'"],
      frameSrc: ["'none'"],
    },
  },
  crossOriginEmbedderPolicy: true,
  crossOriginOpenerPolicy: true,
  crossOriginResourcePolicy: { policy: "cross-origin" },
  dnsPrefetchControl: true,
  frameguard: { action: 'deny' },
  hidePoweredBy: true,
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true,
  },
  ieNoOpen: true,
  noSniff: true,
  originAgentCluster: true,
  permittedCrossDomainPolicies: false,
  referrerPolicy: { policy: "no-referrer" },
  xssFilter: true,
}));
```

## Documentation Standards

### 1. API Documentation

```typescript
/**
 * @swagger
 * /api/users:
 *   get:
 *     summary: Get all users
 *     tags: [Users]
 *     parameters:
 *       - in: query
 *         name: page
 *         schema:
 *           type: integer
 *           default: 1
 *         description: Page number
 *       - in: query
 *         name: limit
 *         schema:
 *           type: integer
 *           default: 10
 *         description: Items per page
 *     responses:
 *       200:
 *         description: List of users
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 users:
 *                   type: array
 *                   items:
 *                     $ref: '#/components/schemas/User'
 *                 meta:
 *                   $ref: '#/components/schemas/PaginationMeta'
 *       401:
 *         description: Unauthorized
 */
router.get('/users', authenticate, userController.getUsers);
```

### 2. Code Documentation

```typescript
/**
 * Processes payment for an order
 * 
 * @param orderId - The unique order identifier
 * @param paymentMethod - Payment method details
 * @returns Payment result with transaction ID
 * @throws {PaymentError} When payment processing fails
 * @throws {ValidationError} When input validation fails
 * 
 * @example
 * ```typescript
 * const result = await processPayment('order-123', {
 *   type: 'card',
 *   token: 'tok_visa',
 * });
 * console.log(result.transactionId);
 * ```
 */
export async function processPayment(
  orderId: string,
  paymentMethod: PaymentMethod
): Promise<PaymentResult> {
  // Implementation
}
```

### 3. README Template

```markdown
# Project Name

Brief description of the project.

## 🚀 Features

- Feature 1
- Feature 2
- Feature 3

## 📋 Prerequisites

- Node.js 18+
- PostgreSQL 15+
- Redis 7+

## 🔧 Installation

\`\`\`bash
# Clone repository
git clone https://github.com/username/project.git

# Install dependencies
pnpm install

# Setup environment
cp .env.example .env

# Run migrations
pnpm db:migrate

# Start development
pnpm dev
\`\`\`

## 🧪 Testing

\`\`\`bash
# Unit tests
pnpm test:unit

# Integration tests
pnpm test:integration

# E2E tests
pnpm test:e2e

# All tests with coverage
pnpm test:coverage
\`\`\`

## 📚 Documentation

- [API Documentation](./docs/api.md)
- [Architecture Guide](./docs/architecture.md)
- [Contributing Guide](./CONTRIBUTING.md)

## 📄 License

MIT
```
