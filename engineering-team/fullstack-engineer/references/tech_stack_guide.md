# Tech Stack Guide

## Frontend Stack

### React & Next.js
```typescript
// Next.js 14 App Router Structure
app/
├── (auth)/
│   ├── login/
│   │   └── page.tsx
│   └── register/
│       └── page.tsx
├── (dashboard)/
│   ├── layout.tsx
│   └── [workspace]/
│       └── page.tsx
├── api/
│   └── [...route]/
│       └── route.ts
└── layout.tsx

// Server Components by default
export default async function Page() {
  const data = await fetchData(); // Direct data fetching
  return <ClientComponent initialData={data} />;
}

// Client Components when needed
'use client';
import { useState } from 'react';

export function InteractiveComponent() {
  const [state, setState] = useState();
  return <div>Interactive content</div>;
}
```

### State Management with Zustand
```typescript
// stores/user.store.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

interface UserState {
  user: User | null;
  preferences: UserPreferences;
  setUser: (user: User) => void;
  updatePreferences: (prefs: Partial<UserPreferences>) => void;
  logout: () => void;
}

export const useUserStore = create<UserState>()(
  devtools(
    persist(
      immer((set) => ({
        user: null,
        preferences: defaultPreferences,
        
        setUser: (user) =>
          set((state) => {
            state.user = user;
          }),
        
        updatePreferences: (prefs) =>
          set((state) => {
            Object.assign(state.preferences, prefs);
          }),
        
        logout: () =>
          set((state) => {
            state.user = null;
            state.preferences = defaultPreferences;
          }),
      })),
      {
        name: 'user-storage',
        partialize: (state) => ({ preferences: state.preferences }),
      }
    )
  )
);
```

### React Native Setup
```typescript
// React Native with Expo
npx create-expo-app MyApp --template

// Navigation with React Navigation
npm install @react-navigation/native @react-navigation/stack

// App.tsx
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Details" component={DetailsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

// Cross-platform components
import { Platform, StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  container: {
    ...Platform.select({
      ios: { paddingTop: 20 },
      android: { paddingTop: 0 },
    }),
  },
});
```

## Backend Stack

### Node.js with Express
```typescript
// server.ts
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import { errorHandler } from './middleware/error';
import { rateLimiter } from './middleware/rate-limit';

const app = express();

// Middleware
app.use(helmet());
app.use(cors());
app.use(compression());
app.use(express.json());
app.use(rateLimiter);

// Routes
app.use('/api/v1', routes);

// Error handling
app.use(errorHandler);

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

### GraphQL with Apollo Server
```typescript
// schema.graphql
type Query {
  users(filter: UserFilter, pagination: PaginationInput): UserConnection!
  user(id: ID!): User
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!
}

type Subscription {
  userUpdated(userId: ID!): User!
}

// server setup
import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import { makeExecutableSchema } from '@graphql-tools/schema';
import { WebSocketServer } from 'ws';
import { useServer } from 'graphql-ws/lib/use/ws';

const schema = makeExecutableSchema({ typeDefs, resolvers });

const apolloServer = new ApolloServer({
  schema,
  plugins: [
    ApolloServerPluginDrainHttpServer({ httpServer }),
  ],
});

await apolloServer.start();

app.use(
  '/graphql',
  expressMiddleware(apolloServer, {
    context: async ({ req }) => ({
      user: await getUserFromToken(req.headers.authorization),
      dataSources: { db, redis },
    }),
  })
);

// Subscriptions with WebSocket
const wsServer = new WebSocketServer({
  server: httpServer,
  path: '/graphql',
});

useServer({ schema }, wsServer);
```

### Go Microservices
```go
// main.go
package main

import (
    "log"
    "net/http"
    
    "github.com/gorilla/mux"
    "github.com/rs/cors"
)

func main() {
    router := mux.NewRouter()
    
    // Routes
    router.HandleFunc("/health", HealthCheck).Methods("GET")
    router.HandleFunc("/api/users", GetUsers).Methods("GET")
    router.HandleFunc("/api/users", CreateUser).Methods("POST")
    router.HandleFunc("/api/users/{id}", GetUser).Methods("GET")
    router.HandleFunc("/api/users/{id}", UpdateUser).Methods("PUT")
    router.HandleFunc("/api/users/{id}", DeleteUser).Methods("DELETE")
    
    // Middleware
    handler := cors.Default().Handler(router)
    
    log.Fatal(http.ListenAndServe(":8080", handler))
}

// Repository pattern
type UserRepository interface {
    FindAll() ([]User, error)
    FindByID(id string) (*User, error)
    Create(user *User) error
    Update(user *User) error
    Delete(id string) error
}

type postgresUserRepository struct {
    db *sql.DB
}

func (r *postgresUserRepository) FindByID(id string) (*User, error) {
    var user User
    err := r.db.QueryRow(
        "SELECT id, email, name FROM users WHERE id = $1",
        id,
    ).Scan(&user.ID, &user.Email, &user.Name)
    
    if err != nil {
        return nil, err
    }
    
    return &user, nil
}
```

### Python Services
```python
# FastAPI service
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import uvicorn

app = FastAPI(title="User Service", version="1.0.0")

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/users", response_model=List[UserSchema])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.post("/users", response_model=UserSchema)
async def create_user(
    user: CreateUserSchema,
    db: Session = Depends(get_db)
):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Background tasks with Celery
from celery import Celery

celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379',
    backend='redis://localhost:6379'
)

@celery_app.task
def process_user_data(user_id: str):
    # Long-running task
    user = fetch_user(user_id)
    analyze_user_behavior(user)
    send_notification(user)
    return {"status": "completed"}
```

## Database Stack

### PostgreSQL with Knex.js
```typescript
// knexfile.ts
import type { Knex } from 'knex';

const config: { [key: string]: Knex.Config } = {
  development: {
    client: 'postgresql',
    connection: {
      database: 'dev_db',
      user: 'developer',
      password: 'password'
    },
    pool: {
      min: 2,
      max: 10
    },
    migrations: {
      directory: './database/migrations',
      tableName: 'knex_migrations'
    },
    seeds: {
      directory: './database/seeds'
    }
  },
  
  production: {
    client: 'postgresql',
    connection: process.env.DATABASE_URL,
    pool: {
      min: 2,
      max: 20
    },
    migrations: {
      directory: './database/migrations'
    }
  }
};

export default config;

// Migration example
export async function up(knex: Knex): Promise<void> {
  await knex.schema.createTable('users', (table) => {
    table.uuid('id').primary().defaultTo(knex.raw('gen_random_uuid()'));
    table.string('email').unique().notNullable();
    table.string('password_hash').notNullable();
    table.jsonb('metadata').defaultTo('{}');
    table.timestamps(true, true);
    
    table.index(['email']);
    table.index(['created_at']);
  });
  
  // Add RLS policies
  await knex.raw(`
    ALTER TABLE users ENABLE ROW LEVEL SECURITY;
    
    CREATE POLICY users_select_policy ON users
      FOR SELECT
      TO authenticated
      USING (id = current_user_id() OR is_admin());
  `);
}
```

### Prisma ORM Alternative
```typescript
// schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String?
  password  String
  role      Role     @default(USER)
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  @@index([email])
  @@index([createdAt])
}

model Post {
  id        String   @id @default(uuid())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
  tags      Tag[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  @@index([authorId])
  @@index([published, createdAt])
}

enum Role {
  USER
  ADMIN
}

// Usage
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// With transactions
const result = await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({
    data: {
      email: 'user@example.com',
      password: hashedPassword,
      profile: {
        create: {
          bio: 'Hello world',
        },
      },
    },
  });
  
  await tx.post.create({
    data: {
      title: 'First post',
      authorId: user.id,
    },
  });
  
  return user;
});
```

### NeonDB / Supabase Configuration
```typescript
// NeonDB setup
import { neon } from '@neondatabase/serverless';

const sql = neon(process.env.DATABASE_URL!);

// Serverless function usage
export async function handler(event: any) {
  const users = await sql`SELECT * FROM users WHERE active = true`;
  return {
    statusCode: 200,
    body: JSON.stringify(users),
  };
}

// Supabase setup
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_ANON_KEY!
);

// Real-time subscriptions
const subscription = supabase
  .channel('room1')
  .on('postgres_changes', {
    event: 'INSERT',
    schema: 'public',
    table: 'messages',
  }, (payload) => {
    console.log('New message:', payload.new);
  })
  .subscribe();

// Row Level Security
const { data, error } = await supabase
  .from('posts')
  .select('*')
  .eq('published', true); // Only returns posts user has access to
```

## Infrastructure Stack

### Docker Configuration
```dockerfile
# Multi-stage build for Node.js
FROM node:18-alpine AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install --frozen-lockfile

FROM node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["node", "server.js"]
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 3000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
  type: LoadBalancer
```

### Terraform Infrastructure
```hcl
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "terraform-state-bucket"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "${var.project_name}-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["${var.aws_region}a", "${var.aws_region}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
  
  enable_nat_gateway = true
  enable_vpn_gateway = false
  
  tags = var.common_tags
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-cluster"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# RDS Database
resource "aws_db_instance" "postgres" {
  identifier = "${var.project_name}-db"
  
  engine         = "postgres"
  engine_version = "15.3"
  instance_class = "db.t3.micro"
  
  allocated_storage     = 20
  max_allocated_storage = 100
  storage_encrypted     = true
  
  db_name  = var.db_name
  username = var.db_username
  password = random_password.db_password.result
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.postgres.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  skip_final_snapshot = false
  final_snapshot_identifier = "${var.project_name}-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}"
  
  tags = var.common_tags
}

# ElastiCache Redis
resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "${var.project_name}-redis"
  engine              = "redis"
  node_type           = "cache.t3.micro"
  num_cache_nodes     = 1
  parameter_group_name = "default.redis7"
  port                = 6379
  
  subnet_group_name = aws_elasticache_subnet_group.redis.name
  security_group_ids = [aws_security_group.redis.id]
  
  tags = var.common_tags
}

# Load Balancer
resource "aws_lb" "main" {
  name               = "${var.project_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets           = module.vpc.public_subnets
  
  enable_deletion_protection = true
  enable_http2              = true
  
  tags = var.common_tags
}
```

### CI/CD with CircleCI
```yaml
# .circleci/config.yml
version: 2.1

orbs:
  node: circleci/node@5.0
  docker: circleci/docker@2.1
  aws-ecr: circleci/aws-ecr@8.1

jobs:
  test:
    docker:
      - image: cimg/node:18.0
      - image: cimg/postgres:15.0
        environment:
          POSTGRES_USER: test
          POSTGRES_DB: test_db
    steps:
      - checkout
      - node/install-packages:
          pkg-manager: pnpm
      - run:
          name: Run tests
          command: |
            pnpm test:ci
            pnpm test:e2e
      - store_test_results:
          path: test-results
      - store_artifacts:
          path: coverage

  build-and-push:
    executor: docker/docker
    steps:
      - checkout
      - setup_remote_docker:
          docker_layer_caching: true
      - aws-ecr/build-and-push-image:
          repo: "${AWS_ECR_REPO}"
          tag: "${CIRCLE_SHA1}"

  deploy:
    docker:
      - image: cimg/base:stable
    steps:
      - checkout
      - run:
          name: Deploy to ECS
          command: |
            aws ecs update-service \
              --cluster production \
              --service app-service \
              --force-new-deployment

workflows:
  version: 2
  build-test-deploy:
    jobs:
      - test
      - build-and-push:
          requires:
            - test
          filters:
            branches:
              only: main
      - deploy:
          requires:
            - build-and-push
          filters:
            branches:
              only: main
```

## Mobile Development

### React Native Architecture
```typescript
// Project structure
src/
├── components/
│   ├── common/
│   └── screens/
├── navigation/
│   ├── AppNavigator.tsx
│   └── AuthNavigator.tsx
├── services/
│   ├── api/
│   └── storage/
├── stores/
├── utils/
└── types/

// Cross-platform API service
class ApiService {
  private baseURL = Platform.select({
    ios: 'http://localhost:4000',
    android: 'http://10.0.2.2:4000',
  });
  
  async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const token = await AsyncStorage.getItem('token');
    
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        Authorization: token ? `Bearer ${token}` : '',
        ...options?.headers,
      },
    });
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }
    
    return response.json();
  }
}

// Platform-specific components
const StatusBar = Platform.select({
  ios: () => <IosStatusBar />,
  android: () => <AndroidStatusBar />,
})!;
```

### Swift (iOS Native)
```swift
// SwiftUI View
import SwiftUI
import Combine

struct UserListView: View {
    @StateObject private var viewModel = UserListViewModel()
    
    var body: some View {
        NavigationView {
            List(viewModel.users) { user in
                NavigationLink(destination: UserDetailView(user: user)) {
                    UserRow(user: user)
                }
            }
            .navigationTitle("Users")
            .onAppear {
                viewModel.fetchUsers()
            }
        }
    }
}

// ViewModel with Combine
class UserListViewModel: ObservableObject {
    @Published var users: [User] = []
    @Published var isLoading = false
    @Published var error: Error?
    
    private var cancellables = Set<AnyCancellable>()
    private let apiService = APIService()
    
    func fetchUsers() {
        isLoading = true
        
        apiService.getUsers()
            .receive(on: DispatchQueue.main)
            .sink(
                receiveCompletion: { completion in
                    self.isLoading = false
                    if case .failure(let error) = completion {
                        self.error = error
                    }
                },
                receiveValue: { users in
                    self.users = users
                }
            )
            .store(in: &cancellables)
    }
}

// Network Layer
class APIService {
    private let session = URLSession.shared
    private let baseURL = "https://api.example.com"
    
    func getUsers() -> AnyPublisher<[User], Error> {
        guard let url = URL(string: "\(baseURL)/users") else {
            return Fail(error: APIError.invalidURL)
                .eraseToAnyPublisher()
        }
        
        return session.dataTaskPublisher(for: url)
            .map(\.data)
            .decode(type: [User].self, decoder: JSONDecoder())
            .eraseToAnyPublisher()
    }
}
```

### Kotlin (Android Native)
```kotlin
// Jetpack Compose UI
@Composable
fun UserListScreen(
    viewModel: UserListViewModel = hiltViewModel()
) {
    val users by viewModel.users.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp)
    ) {
        items(users) { user ->
            UserCard(
                user = user,
                onClick = { viewModel.onUserClick(user) }
            )
        }
    }
    
    if (isLoading) {
        Box(
            modifier = Modifier.fillMaxSize(),
            contentAlignment = Alignment.Center
        ) {
            CircularProgressIndicator()
        }
    }
}

// ViewModel with Hilt
@HiltViewModel
class UserListViewModel @Inject constructor(
    private val userRepository: UserRepository
) : ViewModel() {
    
    private val _users = MutableStateFlow<List<User>>(emptyList())
    val users: StateFlow<List<User>> = _users.asStateFlow()
    
    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()
    
    init {
        fetchUsers()
    }
    
    private fun fetchUsers() {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val result = userRepository.getUsers()
                _users.value = result
            } catch (e: Exception) {
                // Handle error
            } finally {
                _isLoading.value = false
            }
        }
    }
}

// Repository with Retrofit
@Singleton
class UserRepository @Inject constructor(
    private val api: ApiService,
    private val userDao: UserDao
) {
    suspend fun getUsers(): List<User> {
        return try {
            val users = api.getUsers()
            userDao.insertAll(users)
            users
        } catch (e: Exception) {
            userDao.getAllUsers()
        }
    }
}

// Retrofit API Service
interface ApiService {
    @GET("users")
    suspend fun getUsers(): List<User>
    
    @POST("users")
    suspend fun createUser(@Body user: User): User
    
    @PUT("users/{id}")
    suspend fun updateUser(
        @Path("id") id: String,
        @Body user: User
    ): User
}
```

### Flutter Cross-Platform
```dart
// main.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

void main() {
  runApp(
    ProviderScope(
      child: MyApp(),
    ),
  );
}

// User List Screen
class UserListScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final usersAsync = ref.watch(usersProvider);
    
    return Scaffold(
      appBar: AppBar(title: Text('Users')),
      body: usersAsync.when(
        data: (users) => ListView.builder(
          itemCount: users.length,
          itemBuilder: (context, index) {
            final user = users[index];
            return ListTile(
              title: Text(user.name),
              subtitle: Text(user.email),
              onTap: () => Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => UserDetailScreen(user: user),
                ),
              ),
            );
          },
        ),
        loading: () => Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Error: $err')),
      ),
    );
  }
}

// State Management with Riverpod
final usersProvider = FutureProvider<List<User>>((ref) async {
  final repository = ref.read(userRepositoryProvider);
  return repository.getUsers();
});

final userRepositoryProvider = Provider<UserRepository>((ref) {
  final dio = ref.read(dioProvider);
  return UserRepository(dio);
});

// Repository
class UserRepository {
  final Dio _dio;
  
  UserRepository(this._dio);
  
  Future<List<User>> getUsers() async {
    try {
      final response = await _dio.get('/users');
      return (response.data as List)
          .map((json) => User.fromJson(json))
          .toList();
    } on DioError catch (e) {
      throw _handleError(e);
    }
  }
}

// Model with Freezed
@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    required String email,
    String? avatar,
    DateTime? createdAt,
  }) = _User;
  
  factory User.fromJson(Map<String, dynamic> json) =>
      _$UserFromJson(json);
}
```
