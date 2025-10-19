# Fullstack Architecture Patterns

## System Architecture Patterns

### 1. Monolithic Architecture
```
┌─────────────────────────────────┐
│         Frontend (Next.js)       │
├─────────────────────────────────┤
│      Backend API (Node.js)       │
├─────────────────────────────────┤
│      Database (PostgreSQL)       │
└─────────────────────────────────┘
```

**When to Use:**
- Small to medium projects
- Rapid prototyping
- Single team ownership
- Simple deployment requirements

**Implementation:**
```typescript
// Single repository structure
project/
├── src/
│   ├── client/     # Frontend code
│   ├── server/     # Backend code
│   ├── shared/     # Shared types/utils
│   └── database/   # Migrations/models
└── package.json    # Single package.json
```

### 2. Microservices Architecture
```
┌──────────┐ ┌──────────┐ ┌──────────┐
│   Web    │ │  Mobile  │ │   Admin  │
│ Frontend │ │    App   │ │  Portal  │
└────┬─────┘ └────┬─────┘ └────┬─────┘
     │            │            │
┌────┴────────────┴────────────┴─────┐
│          API Gateway                │
├─────────┬──────────┬────────────┬──┤
│  Auth   │ Product  │   Order    │  │
│ Service │ Service  │  Service   │  │
├─────────┼──────────┼────────────┤  │
│  User   │ Product  │   Order    │  │
│   DB    │    DB    │     DB     │  │
└─────────┴──────────┴────────────┘  │
```

**When to Use:**
- Large scale applications
- Multiple teams
- Independent scaling needs
- Complex business domains

**Implementation:**
```yaml
# docker-compose.yml for local development
version: '3.8'
services:
  api-gateway:
    build: ./gateway
    ports: ["4000:4000"]
  
  auth-service:
    build: ./services/auth
    environment:
      - DB_HOST=auth-db
  
  product-service:
    build: ./services/product
    environment:
      - DB_HOST=product-db
  
  order-service:
    build: ./services/order
    environment:
      - DB_HOST=order-db
```

### 3. Serverless Architecture
```
┌────────────────────┐
│   CloudFront CDN   │
├────────────────────┤
│  S3 Static Site    │
├────────────────────┤
│  API Gateway       │
├──────┬──────┬──────┤
│Lambda│Lambda│Lambda│
├──────┴──────┴──────┤
│    DynamoDB        │
└────────────────────┘
```

**When to Use:**
- Variable/unpredictable traffic
- Cost optimization
- Minimal ops overhead
- Event-driven workflows

**Implementation:**
```typescript
// serverless.yml
service: my-app
provider:
  name: aws
  runtime: nodejs18.x

functions:
  getUsers:
    handler: handlers/users.get
    events:
      - http:
          path: users
          method: get
  
  createUser:
    handler: handlers/users.create
    events:
      - http:
          path: users
          method: post
```

### 4. Event-Driven Architecture
```
┌─────────────┐     Events      ┌─────────────┐
│  Producer   │────────────────▶│ Event Bus   │
└─────────────┘                  └──────┬──────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                   ▼                   ▼
            ┌─────────────┐     ┌─────────────┐    ┌─────────────┐
            │ Consumer A  │     │ Consumer B  │    │ Consumer C  │
            └─────────────┘     └─────────────┘    └─────────────┘
```

**Implementation:**
```typescript
// Event Bus with Redis Pub/Sub
import { createClient } from 'redis';

class EventBus {
  private publisher;
  private subscriber;
  
  constructor() {
    this.publisher = createClient();
    this.subscriber = createClient();
  }
  
  async publish(event: string, data: any) {
    await this.publisher.publish(event, JSON.stringify(data));
  }
  
  async subscribe(event: string, handler: (data: any) => void) {
    await this.subscriber.subscribe(event);
    this.subscriber.on('message', (channel, message) => {
      if (channel === event) {
        handler(JSON.parse(message));
      }
    });
  }
}

// Usage
const eventBus = new EventBus();

// Publisher
await eventBus.publish('user.created', { 
  id: '123', 
  email: 'user@example.com' 
});

// Subscriber
eventBus.subscribe('user.created', async (data) => {
  // Send welcome email
  // Update analytics
  // Sync with CRM
});
```

## Frontend Architecture Patterns

### 1. Component-Based Architecture
```typescript
// Atomic Design Pattern
components/
├── atoms/          # Basic building blocks
│   ├── Button/
│   ├── Input/
│   └── Label/
├── molecules/      # Simple groups
│   ├── FormField/
│   ├── SearchBar/
│   └── Card/
├── organisms/      # Complex components
│   ├── Header/
│   ├── UserForm/
│   └── ProductGrid/
├── templates/      # Page templates
│   ├── DashboardLayout/
│   └── AuthLayout/
└── pages/          # Actual pages
    ├── Dashboard/
    └── Login/
```

### 2. State Management Patterns

#### Zustand (Recommended for React)
```typescript
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface UserState {
  user: User | null;
  isLoading: boolean;
  error: string | null;
  login: (credentials: LoginDto) => Promise<void>;
  logout: () => void;
}

export const useUserStore = create<UserState>()(
  devtools(
    persist(
      (set, get) => ({
        user: null,
        isLoading: false,
        error: null,
        
        login: async (credentials) => {
          set({ isLoading: true, error: null });
          try {
            const user = await api.login(credentials);
            set({ user, isLoading: false });
          } catch (error) {
            set({ error: error.message, isLoading: false });
          }
        },
        
        logout: () => {
          set({ user: null });
        },
      }),
      { name: 'user-storage' }
    )
  )
);
```

#### Context + Reducer Pattern
```typescript
interface State {
  user: User | null;
  theme: 'light' | 'dark';
}

type Action = 
  | { type: 'SET_USER'; payload: User }
  | { type: 'TOGGLE_THEME' };

const AppContext = createContext<{
  state: State;
  dispatch: Dispatch<Action>;
}>({} as any);

function appReducer(state: State, action: Action): State {
  switch (action.type) {
    case 'SET_USER':
      return { ...state, user: action.payload };
    case 'TOGGLE_THEME':
      return { ...state, theme: state.theme === 'light' ? 'dark' : 'light' };
    default:
      return state;
  }
}

export function AppProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(appReducer, initialState);
  
  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
}
```

### 3. Data Fetching Patterns

#### TanStack Query (React Query)
```typescript
// hooks/useUser.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export function useUser(userId: string) {
  return useQuery({
    queryKey: ['user', userId],
    queryFn: () => api.getUser(userId),
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 10 * 60 * 1000, // 10 minutes
  });
}

export function useUpdateUser() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: UpdateUserDto) => api.updateUser(data),
    onSuccess: (data, variables) => {
      // Invalidate and refetch
      queryClient.invalidateQueries(['user', variables.id]);
      // Or update cache directly
      queryClient.setQueryData(['user', variables.id], data);
    },
  });
}
```

#### GraphQL with Apollo Client
```typescript
// apollo-client.ts
import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';

const httpLink = createHttpLink({
  uri: process.env.NEXT_PUBLIC_GRAPHQL_URL,
});

const authLink = setContext((_, { headers }) => {
  const token = localStorage.getItem('token');
  return {
    headers: {
      ...headers,
      authorization: token ? `Bearer ${token}` : "",
    }
  };
});

export const apolloClient = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache(),
});

// Usage in component
import { useQuery, gql } from '@apollo/client';

const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      name
      email
      posts {
        id
        title
      }
    }
  }
`;

function UserProfile({ userId }: { userId: string }) {
  const { loading, error, data } = useQuery(GET_USER, {
    variables: { id: userId },
  });
  
  if (loading) return <Spinner />;
  if (error) return <Error message={error.message} />;
  
  return <Profile user={data.user} />;
}
```

## Backend Architecture Patterns

### 1. Clean Architecture (Hexagonal)
```
┌─────────────────────────────────────────┐
│              Presentation               │
│         (Controllers, GraphQL)          │
├─────────────────────────────────────────┤
│             Application                 │
│          (Use Cases, DTOs)              │
├─────────────────────────────────────────┤
│               Domain                    │
│        (Entities, Business Logic)       │
├─────────────────────────────────────────┤
│            Infrastructure               │
│      (Database, External Services)      │
└─────────────────────────────────────────┘
```

**Implementation:**
```typescript
// Domain Layer - Pure business logic
export class User {
  constructor(
    private id: string,
    private email: string,
    private passwordHash: string
  ) {}
  
  validatePassword(password: string): boolean {
    return bcrypt.compareSync(password, this.passwordHash);
  }
  
  changeEmail(newEmail: string): void {
    if (!this.isValidEmail(newEmail)) {
      throw new Error('Invalid email');
    }
    this.email = newEmail;
  }
  
  private isValidEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
}

// Application Layer - Use cases
export class AuthenticateUserUseCase {
  constructor(
    private userRepository: IUserRepository,
    private tokenService: ITokenService
  ) {}
  
  async execute(email: string, password: string): Promise<AuthResult> {
    const user = await this.userRepository.findByEmail(email);
    if (!user || !user.validatePassword(password)) {
      throw new UnauthorizedError('Invalid credentials');
    }
    
    const token = this.tokenService.generate(user);
    return { user, token };
  }
}

// Infrastructure Layer - Concrete implementations
export class PostgresUserRepository implements IUserRepository {
  async findByEmail(email: string): Promise<User | null> {
    const result = await db.query(
      'SELECT * FROM users WHERE email = $1',
      [email]
    );
    
    if (result.rows.length === 0) return null;
    
    return new User(
      result.rows[0].id,
      result.rows[0].email,
      result.rows[0].password_hash
    );
  }
}

// Presentation Layer - HTTP/GraphQL
export class AuthController {
  constructor(private authenticateUser: AuthenticateUserUseCase) {}
  
  async login(req: Request, res: Response) {
    try {
      const { email, password } = req.body;
      const result = await this.authenticateUser.execute(email, password);
      res.json({ token: result.token });
    } catch (error) {
      res.status(401).json({ error: error.message });
    }
  }
}
```

### 2. Repository Pattern
```typescript
// Generic Repository Interface
interface IRepository<T> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  create(entity: T): Promise<T>;
  update(id: string, entity: Partial<T>): Promise<T>;
  delete(id: string): Promise<void>;
}

// Specific Repository Interface
interface IUserRepository extends IRepository<User> {
  findByEmail(email: string): Promise<User | null>;
  findByRole(role: UserRole): Promise<User[]>;
}

// Implementation
class UserRepository implements IUserRepository {
  constructor(private db: Knex) {}
  
  async findById(id: string): Promise<User | null> {
    const data = await this.db('users').where({ id }).first();
    return data ? this.mapToEntity(data) : null;
  }
  
  async findByEmail(email: string): Promise<User | null> {
    const data = await this.db('users').where({ email }).first();
    return data ? this.mapToEntity(data) : null;
  }
  
  async create(user: User): Promise<User> {
    const [id] = await this.db('users').insert(this.mapToDb(user)).returning('id');
    return { ...user, id };
  }
  
  private mapToEntity(data: any): User {
    return new User(data);
  }
  
  private mapToDb(user: User): any {
    return {
      email: user.email,
      password_hash: user.passwordHash,
      created_at: user.createdAt,
    };
  }
}
```

### 3. Service Layer Pattern
```typescript
// Business logic separated from controllers
export class UserService {
  constructor(
    private userRepo: IUserRepository,
    private emailService: IEmailService,
    private cacheService: ICacheService
  ) {}
  
  async register(dto: RegisterUserDto): Promise<User> {
    // Validate
    await this.validateRegistration(dto);
    
    // Create user
    const passwordHash = await bcrypt.hash(dto.password, 10);
    const user = await this.userRepo.create({
      ...dto,
      passwordHash,
      isVerified: false,
    });
    
    // Send verification email
    await this.emailService.sendVerificationEmail(user);
    
    // Cache user
    await this.cacheService.set(`user:${user.id}`, user, 3600);
    
    return user;
  }
  
  private async validateRegistration(dto: RegisterUserDto): Promise<void> {
    const existing = await this.userRepo.findByEmail(dto.email);
    if (existing) {
      throw new ConflictError('Email already registered');
    }
    
    if (dto.password.length < 8) {
      throw new ValidationError('Password too short');
    }
  }
}
```

## Database Patterns

### 1. Database Migration Pattern
```typescript
// migrations/20240101_create_users_table.ts
export async function up(knex: Knex): Promise<void> {
  await knex.schema.createTable('users', (table) => {
    table.uuid('id').primary().defaultTo(knex.raw('gen_random_uuid()'));
    table.string('email').unique().notNullable();
    table.string('password_hash').notNullable();
    table.jsonb('profile');
    table.timestamp('created_at').defaultTo(knex.fn.now());
    table.timestamp('updated_at').defaultTo(knex.fn.now());
    
    table.index('email');
    table.index('created_at');
  });
}

export async function down(knex: Knex): Promise<void> {
  await knex.schema.dropTable('users');
}
```

### 2. Query Builder Pattern
```typescript
class UserQueryBuilder {
  private query: Knex.QueryBuilder;
  
  constructor(private db: Knex) {
    this.query = this.db('users');
  }
  
  withPosts(): this {
    this.query.leftJoin('posts', 'users.id', 'posts.user_id')
              .select('posts.*');
    return this;
  }
  
  whereActive(): this {
    this.query.where('users.is_active', true);
    return this;
  }
  
  createdAfter(date: Date): this {
    this.query.where('users.created_at', '>', date);
    return this;
  }
  
  paginate(page: number, limit: number): this {
    this.query.limit(limit).offset((page - 1) * limit);
    return this;
  }
  
  async execute(): Promise<User[]> {
    const results = await this.query;
    return results.map(r => new User(r));
  }
}

// Usage
const users = await new UserQueryBuilder(db)
  .withPosts()
  .whereActive()
  .createdAfter(new Date('2024-01-01'))
  .paginate(1, 20)
  .execute();
```

### 3. Unit of Work Pattern
```typescript
class UnitOfWork {
  private operations: Array<() => Promise<any>> = [];
  
  constructor(private db: Knex) {}
  
  registerCreate<T>(repo: IRepository<T>, entity: T): void {
    this.operations.push(() => repo.create(entity));
  }
  
  registerUpdate<T>(repo: IRepository<T>, id: string, data: Partial<T>): void {
    this.operations.push(() => repo.update(id, data));
  }
  
  registerDelete<T>(repo: IRepository<T>, id: string): void {
    this.operations.push(() => repo.delete(id));
  }
  
  async commit(): Promise<void> {
    const trx = await this.db.transaction();
    
    try {
      for (const operation of this.operations) {
        await operation();
      }
      await trx.commit();
      this.operations = [];
    } catch (error) {
      await trx.rollback();
      throw error;
    }
  }
  
  rollback(): void {
    this.operations = [];
  }
}

// Usage
const uow = new UnitOfWork(db);

uow.registerCreate(userRepo, newUser);
uow.registerUpdate(profileRepo, userId, { bio: 'Updated bio' });
uow.registerDelete(postRepo, postId);

await uow.commit(); // All operations in single transaction
```

## Security Patterns

### 1. Authentication & Authorization
```typescript
// JWT Authentication Middleware
export const authenticate = async (
  req: Request, 
  res: Response, 
  next: NextFunction
) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];
    
    if (!token) {
      throw new UnauthorizedError('No token provided');
    }
    
    const payload = jwt.verify(token, process.env.JWT_SECRET!) as JwtPayload;
    
    // Check if token is blacklisted
    const isBlacklisted = await redis.get(`blacklist:${token}`);
    if (isBlacklisted) {
      throw new UnauthorizedError('Token revoked');
    }
    
    // Attach user to request
    req.user = await userService.findById(payload.sub);
    
    if (!req.user) {
      throw new UnauthorizedError('User not found');
    }
    
    next();
  } catch (error) {
    res.status(401).json({ error: 'Authentication failed' });
  }
};

// Role-based Authorization
export const authorize = (...roles: UserRole[]) => {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Not authenticated' });
    }
    
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    
    next();
  };
};

// Usage
router.get('/admin/users', 
  authenticate, 
  authorize(UserRole.ADMIN), 
  adminController.getUsers
);
```

### 2. Input Validation Pattern
```typescript
import { z } from 'zod';

// Define schemas
const CreateUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).regex(/^(?=.*[A-Z])(?=.*\d)/, 
    'Password must contain uppercase and number'),
  name: z.string().min(2).max(50),
  age: z.number().int().positive().max(120).optional(),
  role: z.enum(['user', 'admin']).default('user'),
});

// Validation middleware
export const validate = <T>(schema: z.ZodSchema<T>) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      req.body = await schema.parseAsync(req.body);
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({
          error: 'Validation failed',
          details: error.errors,
        });
      } else {
        next(error);
      }
    }
  };
};

// Usage
router.post('/users', 
  validate(CreateUserSchema), 
  userController.create
);
```

### 3. Rate Limiting Pattern
```typescript
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';

// Basic rate limiter
export const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP',
  standardHeaders: true,
  legacyHeaders: false,
});

// Strict rate limiter for auth endpoints
export const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  skipSuccessfulRequests: true, // Don't count successful requests
  store: new RedisStore({
    client: redis,
    prefix: 'rl:auth:',
  }),
});

// Dynamic rate limiting based on user tier
export const dynamicLimiter = async (
  req: Request, 
  res: Response, 
  next: NextFunction
) => {
  const limits = {
    free: 10,
    pro: 100,
    enterprise: 1000,
  };
  
  const userTier = req.user?.tier || 'free';
  const limit = limits[userTier];
  
  const key = `rl:${req.user?.id || req.ip}:${Date.now() / 60000 | 0}`;
  const current = await redis.incr(key);
  
  if (current === 1) {
    await redis.expire(key, 60); // 1 minute window
  }
  
  if (current > limit) {
    return res.status(429).json({ 
      error: 'Rate limit exceeded',
      retryAfter: 60,
    });
  }
  
  res.setHeader('X-RateLimit-Limit', limit.toString());
  res.setHeader('X-RateLimit-Remaining', (limit - current).toString());
  
  next();
};
```

## Testing Patterns

### 1. Unit Testing
```typescript
// user.service.test.ts
describe('UserService', () => {
  let userService: UserService;
  let mockUserRepo: jest.Mocked<IUserRepository>;
  let mockEmailService: jest.Mocked<IEmailService>;
  
  beforeEach(() => {
    mockUserRepo = {
      create: jest.fn(),
      findByEmail: jest.fn(),
      // ... other methods
    };
    
    mockEmailService = {
      sendVerificationEmail: jest.fn(),
    };
    
    userService = new UserService(mockUserRepo, mockEmailService);
  });
  
  describe('register', () => {
    it('should create a new user and send verification email', async () => {
      const dto: RegisterUserDto = {
        email: 'test@example.com',
        password: 'Password123!',
        name: 'Test User',
      };
      
      const expectedUser = {
        id: '123',
        ...dto,
        passwordHash: 'hashed',
        isVerified: false,
      };
      
      mockUserRepo.findByEmail.mockResolvedValue(null);
      mockUserRepo.create.mockResolvedValue(expectedUser);
      
      const result = await userService.register(dto);
      
      expect(mockUserRepo.findByEmail).toHaveBeenCalledWith(dto.email);
      expect(mockUserRepo.create).toHaveBeenCalledWith(
        expect.objectContaining({
          email: dto.email,
          name: dto.name,
        })
      );
      expect(mockEmailService.sendVerificationEmail).toHaveBeenCalledWith(expectedUser);
      expect(result).toEqual(expectedUser);
    });
    
    it('should throw error if email already exists', async () => {
      mockUserRepo.findByEmail.mockResolvedValue({ id: '123' } as User);
      
      await expect(
        userService.register({
          email: 'existing@example.com',
          password: 'Password123!',
          name: 'Test',
        })
      ).rejects.toThrow('Email already registered');
    });
  });
});
```

### 2. Integration Testing
```typescript
// api.integration.test.ts
import request from 'supertest';
import { app } from '../src/app';
import { db } from '../src/db';

describe('User API Integration', () => {
  beforeEach(async () => {
    await db.migrate.latest();
    await db.seed.run();
  });
  
  afterEach(async () => {
    await db.migrate.rollback();
  });
  
  describe('POST /api/users', () => {
    it('should create a new user', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({
          email: 'newuser@example.com',
          password: 'Password123!',
          name: 'New User',
        })
        .expect(201);
      
      expect(response.body).toMatchObject({
        id: expect.any(String),
        email: 'newuser@example.com',
        name: 'New User',
      });
      
      // Verify in database
      const user = await db('users')
        .where({ email: 'newuser@example.com' })
        .first();
      
      expect(user).toBeDefined();
      expect(user.is_verified).toBe(false);
    });
    
    it('should return 400 for invalid input', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({
          email: 'invalid-email',
          password: '123', // Too short
        })
        .expect(400);
      
      expect(response.body).toHaveProperty('error');
      expect(response.body.details).toBeInstanceOf(Array);
    });
  });
});
```

### 3. E2E Testing (Cypress)
```typescript
// cypress/e2e/user-registration.cy.ts
describe('User Registration Flow', () => {
  beforeEach(() => {
    cy.task('db:seed');
    cy.visit('/register');
  });
  
  it('should successfully register a new user', () => {
    // Fill form
    cy.get('[data-testid="email-input"]').type('newuser@example.com');
    cy.get('[data-testid="password-input"]').type('Password123!');
    cy.get('[data-testid="confirm-password-input"]').type('Password123!');
    cy.get('[data-testid="name-input"]').type('New User');
    
    // Submit
    cy.get('[data-testid="register-button"]').click();
    
    // Verify redirect
    cy.url().should('include', '/verify-email');
    cy.contains('Please check your email').should('be.visible');
    
    // Verify email was sent (using mailhog or similar)
    cy.task('mail:check', 'newuser@example.com').then((email) => {
      expect(email.subject).to.equal('Verify your email');
      expect(email.html).to.include('verification link');
    });
  });
  
  it('should show validation errors', () => {
    cy.get('[data-testid="register-button"]').click();
    
    cy.contains('Email is required').should('be.visible');
    cy.contains('Password is required').should('be.visible');
    
    // Test password requirements
    cy.get('[data-testid="password-input"]').type('weak');
    cy.contains('Password must be at least 8 characters').should('be.visible');
  });
});
```

## Performance Optimization Patterns

### 1. Caching Strategies
```typescript
// Multi-layer caching
class CacheService {
  private memoryCache = new Map<string, { data: any; expires: number }>();
  
  constructor(private redis: Redis) {}
  
  async get<T>(key: string): Promise<T | null> {
    // L1: Memory cache
    const memory = this.memoryCache.get(key);
    if (memory && memory.expires > Date.now()) {
      return memory.data;
    }
    
    // L2: Redis cache
    const cached = await this.redis.get(key);
    if (cached) {
      const data = JSON.parse(cached);
      // Populate memory cache
      this.memoryCache.set(key, {
        data,
        expires: Date.now() + 60000, // 1 minute
      });
      return data;
    }
    
    return null;
  }
  
  async set<T>(key: string, value: T, ttl: number): Promise<void> {
    // Set in both caches
    this.memoryCache.set(key, {
      data: value,
      expires: Date.now() + (ttl * 1000),
    });
    
    await this.redis.setex(key, ttl, JSON.stringify(value));
  }
  
  async invalidate(pattern: string): Promise<void> {
    // Clear memory cache
    for (const key of this.memoryCache.keys()) {
      if (key.includes(pattern)) {
        this.memoryCache.delete(key);
      }
    }
    
    // Clear Redis cache
    const keys = await this.redis.keys(`*${pattern}*`);
    if (keys.length > 0) {
      await this.redis.del(...keys);
    }
  }
}

// Cache-aside pattern
async function getUserWithCache(userId: string): Promise<User> {
  const cacheKey = `user:${userId}`;
  
  // Try cache first
  let user = await cache.get<User>(cacheKey);
  
  if (!user) {
    // Cache miss - fetch from database
    user = await userRepository.findById(userId);
    
    if (user) {
      // Cache for 1 hour
      await cache.set(cacheKey, user, 3600);
    }
  }
  
  return user;
}
```

### 2. Database Query Optimization
```typescript
// N+1 Query Prevention
// Bad - N+1 queries
async function getUsersWithPostsBad(): Promise<User[]> {
  const users = await db('users').select('*');
  
  for (const user of users) {
    user.posts = await db('posts').where({ user_id: user.id });
  }
  
  return users;
}

// Good - Single query with join
async function getUsersWithPostsGood(): Promise<User[]> {
  const results = await db('users')
    .leftJoin('posts', 'users.id', 'posts.user_id')
    .select(
      'users.*',
      db.raw('COALESCE(json_agg(posts.*) FILTER (WHERE posts.id IS NOT NULL), \'[]\') as posts')
    )
    .groupBy('users.id');
  
  return results.map(r => ({
    ...r,
    posts: JSON.parse(r.posts),
  }));
}

// DataLoader for batching
import DataLoader from 'dataloader';

const userLoader = new DataLoader(async (userIds: string[]) => {
  const users = await db('users').whereIn('id', userIds);
  
  // DataLoader expects results in same order as input
  const userMap = new Map(users.map(u => [u.id, u]));
  return userIds.map(id => userMap.get(id) || null);
});

// Usage in GraphQL resolver
const resolvers = {
  Post: {
    author: (post: Post) => userLoader.load(post.user_id),
  },
};
```

### 3. API Response Optimization
```typescript
// Pagination
interface PaginationParams {
  page: number;
  limit: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

interface PaginatedResponse<T> {
  data: T[];
  meta: {
    total: number;
    page: number;
    limit: number;
    totalPages: number;
    hasNext: boolean;
    hasPrev: boolean;
  };
}

async function paginate<T>(
  query: Knex.QueryBuilder,
  params: PaginationParams
): Promise<PaginatedResponse<T>> {
  const { page, limit, sortBy = 'created_at', sortOrder = 'desc' } = params;
  
  // Get total count
  const [{ count }] = await query.clone().count('* as count');
  const total = parseInt(count as string, 10);
  
  // Apply pagination
  const data = await query
    .orderBy(sortBy, sortOrder)
    .limit(limit)
    .offset((page - 1) * limit);
  
  return {
    data,
    meta: {
      total,
      page,
      limit,
      totalPages: Math.ceil(total / limit),
      hasNext: page * limit < total,
      hasPrev: page > 1,
    },
  };
}

// Field selection (GraphQL-like)
async function getUsers(fields?: string[]): Promise<User[]> {
  const query = db('users');
  
  if (fields && fields.length > 0) {
    // Only select requested fields
    query.select(fields.filter(f => allowedFields.includes(f)));
  } else {
    // Default fields (exclude sensitive data)
    query.select('id', 'name', 'email', 'created_at');
  }
  
  return query;
}

// Response compression
import compression from 'compression';

app.use(compression({
  filter: (req, res) => {
    if (req.headers['x-no-compression']) {
      return false;
    }
    return compression.filter(req, res);
  },
  threshold: 1024, // Only compress responses > 1kb
}));
```

## Deployment Patterns

### 1. Blue-Green Deployment
```yaml
# kubernetes/blue-green-deployment.yaml
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: myapp
    version: blue  # Switch between blue/green
  ports:
    - port: 80
      targetPort: 3000
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
      - name: app
        image: myapp:1.0.0
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
      - name: app
        image: myapp:2.0.0
```

### 2. Canary Deployment
```typescript
// Feature flags for canary releases
import { FeatureFlag } from './feature-flag-service';

@FeatureFlag('new-checkout-flow', 0.1) // 10% of users
async function checkout(req: Request, res: Response) {
  if (req.featureFlags?.['new-checkout-flow']) {
    return newCheckoutFlow(req, res);
  }
  return oldCheckoutFlow(req, res);
}

// Traffic splitting with nginx
```

### 3. Rolling Deployment
```yaml
# Kubernetes rolling update
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Max pods above desired replicas
      maxUnavailable: 1  # Max pods that can be unavailable
  template:
    spec:
      containers:
      - name: app
        image: myapp:2.0.0
        readinessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
```
