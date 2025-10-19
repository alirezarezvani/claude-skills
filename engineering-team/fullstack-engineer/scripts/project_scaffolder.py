#!/usr/bin/env python3
"""
Project Scaffolder - Quickly scaffold fullstack projects with best practices
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List
import argparse

class ProjectScaffolder:
    def __init__(self, project_name: str, project_type: str):
        self.project_name = project_name
        self.project_type = project_type
        self.root_path = Path.cwd() / project_name
        
    def create_nextjs_graphql_project(self):
        """Create a Next.js + GraphQL + PostgreSQL project"""
        print(f"🚀 Creating Next.js + GraphQL project: {self.project_name}")
        
        # Create project structure
        dirs = [
            "frontend/src/components",
            "frontend/src/pages/api",
            "frontend/src/lib",
            "frontend/src/hooks",
            "frontend/src/styles",
            "frontend/src/types",
            "frontend/src/utils",
            "frontend/public",
            "backend/src/resolvers",
            "backend/src/schema",
            "backend/src/models",
            "backend/src/services",
            "backend/src/middleware",
            "backend/src/utils",
            "backend/src/types",
            "database/migrations",
            "database/seeds",
            "docker",
            "tests/unit",
            "tests/integration",
            "tests/e2e",
            ".github/workflows"
        ]
        
        for dir_path in dirs:
            (self.root_path / dir_path).mkdir(parents=True, exist_ok=True)
        
        # Create configuration files
        self._create_package_json()
        self._create_docker_compose()
        self._create_env_example()
        self._create_typescript_config()
        self._create_eslint_config()
        self._create_prettier_config()
        self._create_github_workflows()
        self._create_readme()
        
        print("✅ Project structure created successfully!")
        
    def _create_package_json(self):
        """Create package.json files for frontend and backend"""
        
        # Frontend package.json
        frontend_package = {
            "name": f"{self.project_name}-frontend",
            "version": "1.0.0",
            "private": True,
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint",
                "test": "jest --watch",
                "test:ci": "jest --ci --coverage",
                "type-check": "tsc --noEmit",
                "format": "prettier --write ."
            },
            "dependencies": {
                "next": "^14.0.0",
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "@apollo/client": "^3.8.0",
                "graphql": "^16.8.0",
                "axios": "^1.6.0",
                "@tanstack/react-query": "^5.0.0",
                "zustand": "^4.4.0",
                "zod": "^3.22.0"
            },
            "devDependencies": {
                "@types/node": "^20.0.0",
                "@types/react": "^18.2.0",
                "@types/react-dom": "^18.2.0",
                "typescript": "^5.3.0",
                "eslint": "^8.50.0",
                "eslint-config-next": "^14.0.0",
                "prettier": "^3.1.0",
                "jest": "^29.7.0",
                "@testing-library/react": "^14.1.0",
                "@testing-library/jest-dom": "^6.1.0",
                "cypress": "^13.6.0"
            }
        }
        
        # Backend package.json
        backend_package = {
            "name": f"{self.project_name}-backend",
            "version": "1.0.0",
            "private": True,
            "scripts": {
                "dev": "nodemon --exec ts-node src/index.ts",
                "build": "tsc",
                "start": "node dist/index.js",
                "test": "jest --watch",
                "test:ci": "jest --ci --coverage",
                "lint": "eslint src --ext .ts",
                "format": "prettier --write src",
                "migrate": "knex migrate:latest",
                "seed": "knex seed:run"
            },
            "dependencies": {
                "apollo-server-express": "^3.13.0",
                "express": "^4.18.0",
                "graphql": "^16.8.0",
                "pg": "^8.11.0",
                "knex": "^3.1.0",
                "bcryptjs": "^2.4.3",
                "jsonwebtoken": "^9.0.0",
                "dotenv": "^16.3.0",
                "cors": "^2.8.5",
                "helmet": "^7.1.0",
                "winston": "^3.11.0",
                "joi": "^17.11.0"
            },
            "devDependencies": {
                "@types/node": "^20.0.0",
                "@types/express": "^4.17.0",
                "@types/bcryptjs": "^2.4.0",
                "@types/jsonwebtoken": "^9.0.0",
                "typescript": "^5.3.0",
                "ts-node": "^10.9.0",
                "nodemon": "^3.0.0",
                "eslint": "^8.50.0",
                "@typescript-eslint/parser": "^6.10.0",
                "@typescript-eslint/eslint-plugin": "^6.10.0",
                "prettier": "^3.1.0",
                "jest": "^29.7.0",
                "@types/jest": "^29.5.0",
                "supertest": "^6.3.0"
            }
        }
        
        # Write package.json files
        with open(self.root_path / "frontend" / "package.json", "w") as f:
            json.dump(frontend_package, f, indent=2)
        
        with open(self.root_path / "backend" / "package.json", "w") as f:
            json.dump(backend_package, f, indent=2)
    
    def _create_docker_compose(self):
        """Create docker-compose.yml for local development"""
        docker_compose = """version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${DB_USER:-developer}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-password}
      POSTGRES_DB: ${DB_NAME:-projectdb}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-developer}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build: 
      context: ./backend
      dockerfile: ../docker/backend.Dockerfile
    ports:
      - "4000:4000"
    environment:
      NODE_ENV: development
      DATABASE_URL: postgresql://${DB_USER:-developer}:${DB_PASSWORD:-password}@postgres:5432/${DB_NAME:-projectdb}
      REDIS_URL: redis://redis:6379
      JWT_SECRET: ${JWT_SECRET:-your-secret-key}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./backend:/app
      - /app/node_modules
    command: npm run dev

  frontend:
    build:
      context: ./frontend
      dockerfile: ../docker/frontend.Dockerfile
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://backend:4000/graphql
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules
      - /app/.next
    command: npm run dev

volumes:
  postgres_data:
  redis_data:
"""
        with open(self.root_path / "docker-compose.yml", "w") as f:
            f.write(docker_compose)
        
        # Create Dockerfiles
        backend_dockerfile = """FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

RUN npm run build

EXPOSE 4000

CMD ["npm", "start"]
"""
        
        frontend_dockerfile = """FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
"""
        
        with open(self.root_path / "docker" / "backend.Dockerfile", "w") as f:
            f.write(backend_dockerfile)
        
        with open(self.root_path / "docker" / "frontend.Dockerfile", "w") as f:
            f.write(frontend_dockerfile)
    
    def _create_env_example(self):
        """Create .env.example file"""
        env_content = """# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=developer
DB_PASSWORD=password
DB_NAME=projectdb
DATABASE_URL=postgresql://developer:password@localhost:5432/projectdb

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET=your-secret-key-change-this-in-production
JWT_EXPIRY=7d

# API
API_PORT=4000
NEXT_PUBLIC_API_URL=http://localhost:4000/graphql

# Frontend
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Environment
NODE_ENV=development

# Monitoring (optional)
SENTRY_DSN=
NEW_RELIC_LICENSE_KEY=

# AWS (optional)
AWS_REGION=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
S3_BUCKET_NAME=
"""
        with open(self.root_path / ".env.example", "w") as f:
            f.write(env_content)
    
    def _create_typescript_config(self):
        """Create TypeScript configuration files"""
        
        # Frontend tsconfig.json
        frontend_tsconfig = {
            "compilerOptions": {
                "target": "ES2022",
                "lib": ["dom", "dom.iterable", "esnext"],
                "allowJs": True,
                "skipLibCheck": True,
                "strict": True,
                "forceConsistentCasingInFileNames": True,
                "noEmit": True,
                "esModuleInterop": True,
                "module": "esnext",
                "moduleResolution": "node",
                "resolveJsonModule": True,
                "isolatedModules": True,
                "jsx": "preserve",
                "incremental": True,
                "paths": {
                    "@/*": ["./src/*"],
                    "@components/*": ["./src/components/*"],
                    "@hooks/*": ["./src/hooks/*"],
                    "@lib/*": ["./src/lib/*"],
                    "@types/*": ["./src/types/*"],
                    "@utils/*": ["./src/utils/*"]
                }
            },
            "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
            "exclude": ["node_modules"]
        }
        
        # Backend tsconfig.json
        backend_tsconfig = {
            "compilerOptions": {
                "target": "ES2022",
                "module": "commonjs",
                "lib": ["ES2022"],
                "outDir": "./dist",
                "rootDir": "./src",
                "strict": True,
                "esModuleInterop": True,
                "skipLibCheck": True,
                "forceConsistentCasingInFileNames": True,
                "resolveJsonModule": True,
                "declaration": True,
                "declarationMap": True,
                "sourceMap": True,
                "noUnusedLocals": True,
                "noUnusedParameters": True,
                "noImplicitReturns": True,
                "noFallthroughCasesInSwitch": True,
                "paths": {
                    "@/*": ["./src/*"],
                    "@models/*": ["./src/models/*"],
                    "@services/*": ["./src/services/*"],
                    "@resolvers/*": ["./src/resolvers/*"],
                    "@middleware/*": ["./src/middleware/*"],
                    "@utils/*": ["./src/utils/*"],
                    "@types/*": ["./src/types/*"]
                }
            },
            "include": ["src/**/*"],
            "exclude": ["node_modules", "dist", "**/*.test.ts"]
        }
        
        with open(self.root_path / "frontend" / "tsconfig.json", "w") as f:
            json.dump(frontend_tsconfig, f, indent=2)
        
        with open(self.root_path / "backend" / "tsconfig.json", "w") as f:
            json.dump(backend_tsconfig, f, indent=2)
    
    def _create_eslint_config(self):
        """Create ESLint configuration"""
        eslintrc = {
            "extends": [
                "eslint:recommended",
                "plugin:@typescript-eslint/recommended",
                "plugin:react/recommended",
                "plugin:react-hooks/recommended",
                "next/core-web-vitals",
                "prettier"
            ],
            "parser": "@typescript-eslint/parser",
            "plugins": ["@typescript-eslint", "react", "react-hooks"],
            "rules": {
                "@typescript-eslint/no-unused-vars": ["error", {"argsIgnorePattern": "^_"}],
                "@typescript-eslint/no-explicit-any": "error",
                "react/react-in-jsx-scope": "off",
                "react/prop-types": "off",
                "no-console": ["warn", {"allow": ["warn", "error"]}]
            }
        }
        
        with open(self.root_path / ".eslintrc.json", "w") as f:
            json.dump(eslintrc, f, indent=2)
    
    def _create_prettier_config(self):
        """Create Prettier configuration"""
        prettierrc = {
            "semi": True,
            "singleQuote": True,
            "tabWidth": 2,
            "trailingComma": "es5",
            "printWidth": 100,
            "bracketSpacing": True,
            "arrowParens": "always",
            "endOfLine": "lf"
        }
        
        with open(self.root_path / ".prettierrc", "w") as f:
            json.dump(prettierrc, f, indent=2)
        
        # .prettierignore
        prettierignore = """node_modules
dist
.next
coverage
*.log
.env
.env.local
"""
        with open(self.root_path / ".prettierignore", "w") as f:
            f.write(prettierignore)
    
    def _create_github_workflows(self):
        """Create GitHub Actions workflows"""
        ci_workflow = """name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  NODE_VERSION: '18'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: |
          cd frontend && npm ci
          cd ../backend && npm ci
      
      - name: Run ESLint
        run: |
          cd frontend && npm run lint
          cd ../backend && npm run lint
      
      - name: Run Type Check
        run: |
          cd frontend && npm run type-check
          cd ../backend && npx tsc --noEmit

  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: |
          cd frontend && npm ci
          cd ../backend && npm ci
      
      - name: Run backend tests
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379
          JWT_SECRET: test-secret
        run: |
          cd backend
          npm run test:ci
      
      - name: Run frontend tests
        run: |
          cd frontend
          npm run test:ci
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./frontend/coverage/lcov.info,./backend/coverage/lcov.info

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run security audit
        run: |
          cd frontend && npm audit --audit-level=moderate
          cd ../backend && npm audit --audit-level=moderate
      
      - name: Run Snyk security scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

  build:
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Build frontend
        run: |
          cd frontend
          npm ci
          npm run build
      
      - name: Build backend
        run: |
          cd backend
          npm ci
          npm run build
      
      - name: Build Docker images
        run: |
          docker build -f docker/frontend.Dockerfile -t frontend:latest ./frontend
          docker build -f docker/backend.Dockerfile -t backend:latest ./backend
"""
        with open(self.root_path / ".github" / "workflows" / "ci.yml", "w") as f:
            f.write(ci_workflow)
    
    def _create_readme(self):
        """Create comprehensive README.md"""
        readme = f"""# {self.project_name}

## 🚀 Tech Stack

### Frontend
- **Framework**: Next.js 14 with TypeScript
- **State Management**: Zustand
- **Data Fetching**: Apollo Client (GraphQL) & TanStack Query
- **Styling**: Tailwind CSS / CSS Modules
- **Testing**: Jest, React Testing Library, Cypress

### Backend
- **Runtime**: Node.js with TypeScript
- **Framework**: Express + Apollo Server
- **Database**: PostgreSQL with Knex.js
- **Caching**: Redis
- **Authentication**: JWT
- **Testing**: Jest, Supertest

### DevOps
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Monitoring**: Sentry, New Relic (optional)
- **Cloud**: AWS/GCP/Azure ready

## 📦 Project Structure

```
{self.project_name}/
├── frontend/                # Next.js application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/         # Next.js pages
│   │   ├── hooks/         # Custom React hooks
│   │   ├── lib/           # Libraries and configs
│   │   ├── styles/        # Global styles
│   │   ├── types/         # TypeScript types
│   │   └── utils/         # Utility functions
│   └── public/            # Static assets
├── backend/               # Node.js GraphQL API
│   └── src/
│       ├── resolvers/     # GraphQL resolvers
│       ├── schema/        # GraphQL schema
│       ├── models/        # Database models
│       ├── services/      # Business logic
│       ├── middleware/    # Express middleware
│       └── utils/         # Utilities
├── database/              # Database files
│   ├── migrations/        # Database migrations
│   └── seeds/            # Seed data
├── tests/                # Test files
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── e2e/            # End-to-end tests
├── docker/              # Docker configurations
└── .github/            # GitHub Actions workflows
```

## 🛠️ Getting Started

### Prerequisites
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15+ (or use Docker)
- Redis 7+ (or use Docker)

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd {self.project_name}
```

2. Copy environment variables
```bash
cp .env.example .env
# Edit .env with your values
```

3. Start services with Docker Compose
```bash
docker-compose up -d
```

4. Install dependencies
```bash
# Frontend
cd frontend && npm install

# Backend
cd ../backend && npm install
```

5. Run database migrations
```bash
cd backend
npm run migrate
npm run seed  # Optional: seed data
```

6. Start development servers
```bash
# Terminal 1 - Backend
cd backend && npm run dev

# Terminal 2 - Frontend
cd frontend && npm run dev
```

Visit:
- Frontend: http://localhost:3000
- GraphQL Playground: http://localhost:4000/graphql
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## 📝 Development

### Commands

#### Frontend
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run test         # Run tests
npm run lint         # Lint code
npm run type-check   # TypeScript check
```

#### Backend
```bash
npm run dev          # Start development server
npm run build        # Build TypeScript
npm run start        # Start production server
npm run test         # Run tests
npm run lint         # Lint code
npm run migrate      # Run migrations
npm run seed         # Run seeders
```

### Code Style
- ESLint for linting
- Prettier for formatting
- Husky for pre-commit hooks
- Conventional Commits

### Testing Strategy
- Unit Tests: Jest
- Integration Tests: Supertest
- E2E Tests: Cypress
- Coverage Goal: 80%+

## 🚀 Deployment

### Using Docker
```bash
# Build images
docker build -f docker/frontend.Dockerfile -t {self.project_name}-frontend:latest ./frontend
docker build -f docker/backend.Dockerfile -t {self.project_name}-backend:latest ./backend

# Run containers
docker-compose -f docker-compose.production.yml up -d
```

### Environment Variables
See `.env.example` for all required environment variables.

## 📊 Monitoring

- **Error Tracking**: Sentry
- **APM**: New Relic / DataDog
- **Logs**: Winston + CloudWatch
- **Metrics**: Prometheus + Grafana

## 🔒 Security

- JWT authentication
- Input validation with Joi/Zod
- SQL injection prevention (Knex.js)
- XSS protection (React)
- CORS configuration
- Rate limiting
- Security headers (Helmet)

## 📚 Documentation

- API Documentation: `/graphql` (GraphQL Playground)
- Component Storybook: `npm run storybook`
- Database Schema: `/database/schema.md`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.
"""
        with open(self.root_path / "README.md", "w") as f:
            f.write(readme)
    
    def scaffold(self):
        """Main scaffolding method"""
        if self.project_type == "nextjs-graphql":
            self.create_nextjs_graphql_project()
        elif self.project_type == "react-native":
            self.create_react_native_project()
        elif self.project_type == "microservices":
            self.create_microservices_project()
        else:
            print(f"Project type '{self.project_type}' not supported")
            return False
        
        return True
    
    def create_react_native_project(self):
        """Create React Native project structure"""
        # Implementation for React Native
        print("React Native scaffolding - to be implemented")
    
    def create_microservices_project(self):
        """Create Microservices architecture"""
        # Implementation for Microservices
        print("Microservices scaffolding - to be implemented")

def main():
    parser = argparse.ArgumentParser(description='Scaffold a fullstack project')
    parser.add_argument('project_name', help='Name of the project')
    parser.add_argument('--type', 
                       choices=['nextjs-graphql', 'react-native', 'microservices'],
                       default='nextjs-graphql',
                       help='Type of project to scaffold')
    
    args = parser.parse_args()
    
    scaffolder = ProjectScaffolder(args.project_name, args.type)
    if scaffolder.scaffold():
        print(f"\n✨ Project '{args.project_name}' created successfully!")
        print(f"📁 Location: {scaffolder.root_path}")
        print("\n🎯 Next steps:")
        print("  1. cd " + args.project_name)
        print("  2. docker-compose up -d")
        print("  3. cd frontend && npm install")
        print("  4. cd ../backend && npm install")
        print("  5. npm run dev (in both directories)")

if __name__ == '__main__':
    main()
