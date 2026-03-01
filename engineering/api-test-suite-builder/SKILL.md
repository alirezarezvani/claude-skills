# API Test Suite Builder

**Tier:** POWERFUL
**Category:** Engineering
**Domain:** Testing / API Quality

---

## Overview

Scans API route definitions across frameworks (Next.js App Router, Express, FastAPI, Django REST) and
auto-generates comprehensive test suites covering auth, input validation, error codes, pagination, file
uploads, and rate limiting. Outputs ready-to-run test files for Vitest+Supertest (Node) or Pytest+httpx
(Python).

---

## Core Capabilities

- **Route detection** — scan source files to extract all API endpoints
- **Auth coverage** — valid/invalid/expired tokens, missing auth header
- **Input validation** — missing fields, wrong types, boundary values, injection attempts
- **Error code matrix** — 400/401/403/404/422/500 for each route
- **Pagination** — first/last/empty/oversized pages
- **File uploads** — valid, oversized, wrong MIME type, empty
- **Rate limiting** — burst detection, per-user vs global limits

---

## When to Use

- New API added — generate test scaffold before writing implementation (TDD)
- Legacy API with no tests — scan and generate baseline coverage
- API contract review — verify existing tests match current route definitions
- Pre-release regression check — ensure all routes have at least smoke tests
- Security audit prep — generate adversarial input tests

---

## Route Detection

### Next.js App Router
```bash
# Find all route handlers
find ./app/api -name "route.ts" -o -name "route.js" | sort

# Extract HTTP methods from each route file
grep -rn "export async function\|export function" app/api/**/route.ts | \
  grep -oE "(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)" | sort -u

# Full route map
find ./app/api -name "route.ts" | while read f; do
  route=$(echo $f | sed 's|./app||' | sed 's|/route.ts||')
  methods=$(grep -oE "export (async )?function (GET|POST|PUT|PATCH|DELETE)" "$f" | \
    grep -oE "(GET|POST|PUT|PATCH|DELETE)")
  echo "$methods $route"
done
```

### Express
```bash
# Find all router files
find ./src -name "*.ts" -o -name "*.js" | xargs grep -l "router\.\(get\|post\|put\|delete\|patch\)" 2>/dev/null

# Extract routes with line numbers
grep -rn "router\.\(get\|post\|put\|delete\|patch\)\|app\.\(get\|post\|put\|delete\|patch\)" \
  src/ --include="*.ts" | grep -oE "(get|post|put|delete|patch)\(['\"][^'\"]*['\"]"

# Generate route map
grep -rn "router\.\|app\." src/ --include="*.ts" | \
  grep -oE "\.(get|post|put|delete|patch)\(['\"][^'\"]+['\"]" | \
  sed "s/\.\(.*\)('\(.*\)'/\U\1 \2/"
```

### FastAPI
```bash
# Find all route decorators
grep -rn "@app\.\|@router\." . --include="*.py" | \
  grep -E "@(app|router)\.(get|post|put|delete|patch)"

# Extract with path and function name
grep -rn "@\(app\|router\)\.\(get\|post\|put\|delete\|patch\)" . --include="*.py" | \
  grep -oE "@(app|router)\.(get|post|put|delete|patch)\(['\"][^'\"]*['\"]"
```

### Django REST Framework
```bash
# urlpatterns extraction
grep -rn "path\|re_path\|url(" . --include="*.py" | grep "urlpatterns" -A 50 | \
  grep -E "path\(['\"]" | grep -oE "['\"][^'\"]+['\"]" | head -40

# ViewSet router registration
grep -rn "router\.register\|DefaultRouter\|SimpleRouter" . --include="*.py"
```

---

## Test Generation Patterns

### Auth Test Matrix

For every authenticated endpoint, generate:

| Test Case | Expected Status |
|-----------|----------------|
| No Authorization header | 401 |
| Invalid token format | 401 |
| Valid token, wrong user role | 403 |
| Expired JWT token | 401 |
| Valid token, correct role | 2xx |
| Token from deleted user | 401 |

### Input Validation Matrix

For every POST/PUT/PATCH endpoint with a request body:

| Test Case | Expected Status |
|-----------|----------------|
| Empty body `{}` | 400 or 422 |
| Missing required fields (one at a time) | 400 or 422 |
| Wrong type (string where int expected) | 400 or 422 |
| Boundary: value at min-1 | 400 or 422 |
| Boundary: value at min | 2xx |
| Boundary: value at max | 2xx |
| Boundary: value at max+1 | 400 or 422 |
| SQL injection in string field | 400 or 200 (sanitized) |
| XSS payload in string field | 400 or 200 (sanitized) |
| Null values for required fields | 400 or 422 |

---

## Example Test Files

### Example 1 — Node.js: Vitest + Supertest (Next.js API Route)

```typescript
// tests/api/users.test.ts
import { describe, it, expect, beforeAll, afterAll } from 'vitest'
import request from 'supertest'
import { createServer } from '@/test/helpers/server'
import { generateJWT, generateExpiredJWT } from '@/test/helpers/auth'
import { createTestUser, cleanupTestUsers } from '@/test/helpers/db'

const app = createServer()

describe('GET /api/users/:id', () => {
  let validToken: string
  let adminToken: string
  let testUserId: string

  beforeAll(async () => {
    const user = await createTestUser({ role: 'user' })
    const admin = await createTestUser({ role: 'admin' })
    testUserId = user.id
    validToken = generateJWT(user)
    adminToken = generateJWT(admin)
  })

  afterAll(async () => {
    await cleanupTestUsers()
  })

  // --- Auth tests ---
  it('returns 401 with no auth header', async () => {
    const res = await request(app).get(`/api/users/${testUserId}`)
    expect(res.status).toBe(401)
    expect(res.body).toHaveProperty('error')
  })

  it('returns 401 with malformed token', async () => {
    const res = await request(app)
      .get(`/api/users/${testUserId}`)
      .set('Authorization', 'Bearer not-a-real-jwt')
    expect(res.status).toBe(401)
  })

  it('returns 401 with expired token', async () => {
    const expiredToken = generateExpiredJWT({ id: testUserId })
    const res = await request(app)
      .get(`/api/users/${testUserId}`)
      .set('Authorization', `Bearer ${expiredToken}`)
    expect(res.status).toBe(401)
    expect(res.body.error).toMatch(/expired/i)
  })

  it('returns 403 when accessing another user\'s profile without admin', async () => {
    const otherUser = await createTestUser({ role: 'user' })
    const otherToken = generateJWT(otherUser)
    const res = await request(app)
      .get(`/api/users/${testUserId}`)
      .set('Authorization', `Bearer ${otherToken}`)
    expect(res.status).toBe(403)
    await cleanupTestUsers([otherUser.id])
  })

  it('returns 200 with valid token for own profile', async () => {
    const res = await request(app)
      .get(`/api/users/${testUserId}`)
      .set('Authorization', `Bearer ${validToken}`)
    expect(res.status).toBe(200)
    expect(res.body).toMatchObject({ id: testUserId })
    expect(res.body).not.toHaveProperty('password')
    expect(res.body).not.toHaveProperty('hashedPassword')
  })

  it('returns 404 for non-existent user', async () => {
    const res = await request(app)
      .get('/api/users/00000000-0000-0000-0000-000000000000')
      .set('Authorization', `Bearer ${adminToken}`)
    expect(res.status).toBe(404)
  })

  // --- Input validation ---
  it('returns 400 for invalid UUID format', async () => {
    const res = await request(app)
      .get('/api/users/not-a-uuid')
      .set('Authorization', `Bearer ${adminToken}`)
    expect(res.status).toBe(400)
  })
})

describe('POST /api/users', () => {
  let adminToken: string

  beforeAll(async () => {
    const admin = await createTestUser({ role: 'admin' })
    adminToken = generateJWT(admin)
  })

  afterAll(cleanupTestUsers)

  // --- Input validation ---
  it('returns 422 when body is empty', async () => {
    const res = await request(app)
      .post('/api/users')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({})
    expect(res.status).toBe(422)
    expect(res.body.errors).toBeDefined()
  })

  it('returns 422 when email is missing', async () => {
    const res = await request(app)
      .post('/api/users')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({ name: 'Test User', role: 'user' })
    expect(res.status).toBe(422)
    expect(res.body.errors).toContainEqual(
      expect.objectContaining({ field: 'email' })
    )
  })

  it('returns 422 for invalid email format', async () => {
    const res = await request(app)
      .post('/api/users')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({ email: 'not-an-email', name: 'Test', role: 'user' })
    expect(res.status).toBe(422)
  })

  it('returns 422 for SQL injection attempt in email field', async () => {
    const res = await request(app)
      .post('/api/users')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({ email: "' OR '1'='1", name: 'Hacker', role: 'user' })
    expect(res.status).toBe(422)
  })

  it('returns 409 when email already exists', async () => {
    const existing = await createTestUser({ role: 'user' })
    const res = await request(app)
      .post('/api/users')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({ email: existing.email, name: 'Duplicate', role: 'user' })
    expect(res.status).toBe(409)
  })

  it('creates user successfully with valid data', async () => {
    const res = await request(app)
      .post('/api/users')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({ email: 'newuser@example.com', name: 'New User', role: 'user' })
    expect(res.status).toBe(201)
    expect(res.body).toHaveProperty('id')
    expect(res.body.email).toBe('newuser@example.com')
    expect(res.body).not.toHaveProperty('password')
  })
})

describe('GET /api/users (pagination)', () => {
  let adminToken: string

  beforeAll(async () => {
    const admin = await createTestUser({ role: 'admin' })
    adminToken = generateJWT(admin)
    // Create 15 test users for pagination
    await Promise.all(Array.from({ length: 15 }, (_, i) =>
      createTestUser({ email: `pagtest${i}@example.com` })
    ))
  })

  afterAll(cleanupTestUsers)

  it('returns first page with default limit', async () => {
    const res = await request(app)
      .get('/api/users')
      .set('Authorization', `Bearer ${adminToken}`)
    expect(res.status).toBe(200)
    expect(res.body.data).toBeInstanceOf(Array)
    expect(res.body).toHaveProperty('total')
    expect(res.body).toHaveProperty('page')
    expect(res.body).toHaveProperty('pageSize')
  })

  it('returns empty array for page beyond total', async () => {
    const res = await request(app)
      .get('/api/users?page=9999')
      .set('Authorization', `Bearer ${adminToken}`)
    expect(res.status).toBe(200)
    expect(res.body.data).toHaveLength(0)
  })

  it('returns 400 for negative page number', async () => {
    const res = await request(app)
      .get('/api/users?page=-1')
      .set('Authorization', `Bearer ${adminToken}`)
    expect(res.status).toBe(400)
  })

  it('caps pageSize at maximum allowed value', async () => {
    const res = await request(app)
      .get('/api/users?pageSize=9999')
      .set('Authorization', `Bearer ${adminToken}`)
    expect(res.status).toBe(200)
    expect(res.body.data.length).toBeLessThanOrEqual(100)
  })
})
```

---

### Example 2 — Node.js: File Upload Tests

```typescript
// tests/api/uploads.test.ts
import { describe, it, expect } from 'vitest'
import request from 'supertest'
import path from 'path'
import fs from 'fs'
import { createServer } from '@/test/helpers/server'
import { generateJWT } from '@/test/helpers/auth'
import { createTestUser } from '@/test/helpers/db'

const app = createServer()

describe('POST /api/upload', () => {
  let validToken: string

  beforeAll(async () => {
    const user = await createTestUser({ role: 'user' })
    validToken = generateJWT(user)
  })

  it('returns 401 without authentication', async () => {
    const res = await request(app)
      .post('/api/upload')
      .attach('file', Buffer.from('test'), 'test.pdf')
    expect(res.status).toBe(401)
  })

  it('returns 400 when no file attached', async () => {
    const res = await request(app)
      .post('/api/upload')
      .set('Authorization', `Bearer ${validToken}`)
    expect(res.status).toBe(400)
    expect(res.body.error).toMatch(/file/i)
  })

  it('returns 400 for unsupported file type (exe)', async () => {
    const res = await request(app)
      .post('/api/upload')
      .set('Authorization', `Bearer ${validToken}`)
      .attach('file', Buffer.from('MZ fake exe'), { filename: 'virus.exe', contentType: 'application/octet-stream' })
    expect(res.status).toBe(400)
    expect(res.body.error).toMatch(/type|format|allowed/i)
  })

  it('returns 413 for oversized file (>10MB)', async () => {
    const largeBuf = Buffer.alloc(11 * 1024 * 1024) // 11MB
    const res = await request(app)
      .post('/api/upload')
      .set('Authorization', `Bearer ${validToken}`)
      .attach('file', largeBuf, { filename: 'large.pdf', contentType: 'application/pdf' })
    expect(res.status).toBe(413)
  })

  it('returns 400 for empty file (0 bytes)', async () => {
    const res = await request(app)
      .post('/api/upload')
      .set('Authorization', `Bearer ${validToken}`)
      .attach('file', Buffer.alloc(0), { filename: 'empty.pdf', contentType: 'application/pdf' })
    expect(res.status).toBe(400)
  })

  it('rejects MIME type spoofing (pdf extension but exe content)', async () => {
    // Real malicious file: exe magic bytes but pdf extension
    const fakeExe = Buffer.from('4D5A9000', 'hex') // MZ header
    const res = await request(app)
      .post('/api/upload')
      .set('Authorization', `Bearer ${validToken}`)
      .attach('file', fakeExe, { filename: 'document.pdf', contentType: 'application/pdf' })
    // Should detect magic bytes mismatch
    expect([400, 415]).toContain(res.status)
  })

  it('accepts valid PDF file', async () => {
    const pdfHeader = Buffer.from('%PDF-1.4 test content')
    const res = await request(app)
      .post('/api/upload')
      .set('Authorization', `Bearer ${validToken}`)
      .attach('file', pdfHeader, { filename: 'valid.pdf', contentType: 'application/pdf' })
    expect(res.status).toBe(200)
    expect(res.body).toHaveProperty('url')
    expect(res.body).toHaveProperty('id')
  })
})
```

---

### Example 3 — Python: Pytest + httpx (FastAPI)

```python
# tests/api/test_items.py
import pytest
import httpx
from datetime import datetime, timedelta
import jwt

BASE_URL = "http://localhost:8000"
JWT_SECRET = "test-secret"  # use test config, never production secret


def make_token(user_id: str, role: str = "user", expired: bool = False) -> str:
    exp = datetime.utcnow() + (timedelta(hours=-1) if expired else timedelta(hours=1))
    return jwt.encode(
        {"sub": user_id, "role": role, "exp": exp},
        JWT_SECRET,
        algorithm="HS256",
    )


@pytest.fixture
def client():
    with httpx.Client(base_url=BASE_URL) as c:
        yield c


@pytest.fixture
def valid_token():
    return make_token("user-123", role="user")


@pytest.fixture
def admin_token():
    return make_token("admin-456", role="admin")


@pytest.fixture
def expired_token():
    return make_token("user-123", expired=True)


class TestGetItem:
    def test_returns_401_without_auth(self, client):
        res = client.get("/api/items/1")
        assert res.status_code == 401

    def test_returns_401_with_invalid_token(self, client):
        res = client.get("/api/items/1", headers={"Authorization": "Bearer garbage"})
        assert res.status_code == 401

    def test_returns_401_with_expired_token(self, client, expired_token):
        res = client.get("/api/items/1", headers={"Authorization": f"Bearer {expired_token}"})
        assert res.status_code == 401
        assert "expired" in res.json().get("detail", "").lower()

    def test_returns_404_for_nonexistent_item(self, client, valid_token):
        res = client.get(
            "/api/items/99999999",
            headers={"Authorization": f"Bearer {valid_token}"},
        )
        assert res.status_code == 404

    def test_returns_400_for_invalid_id_format(self, client, valid_token):
        res = client.get(
            "/api/items/not-a-number",
            headers={"Authorization": f"Bearer {valid_token}"},
        )
        assert res.status_code in (400, 422)

    def test_returns_200_with_valid_auth(self, client, valid_token, test_item):
        res = client.get(
            f"/api/items/{test_item['id']}",
            headers={"Authorization": f"Bearer {valid_token}"},
        )
        assert res.status_code == 200
        data = res.json()
        assert data["id"] == test_item["id"]
        assert "password" not in data


class TestCreateItem:
    def test_returns_422_with_empty_body(self, client, admin_token):
        res = client.post(
            "/api/items",
            json={},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert res.status_code == 422
        errors = res.json()["detail"]
        assert len(errors) > 0

    def test_returns_422_with_missing_required_field(self, client, admin_token):
        res = client.post(
            "/api/items",
            json={"description": "no name field"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert res.status_code == 422
        fields = [e["loc"][-1] for e in res.json()["detail"]]
        assert "name" in fields

    def test_returns_422_with_wrong_type(self, client, admin_token):
        res = client.post(
            "/api/items",
            json={"name": "test", "price": "not-a-number"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert res.status_code == 422

    @pytest.mark.parametrize("price", [-1, -0.01])
    def test_returns_422_for_negative_price(self, client, admin_token, price):
        res = client.post(
            "/api/items",
            json={"name": "test", "price": price},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert res.status_code == 422

    def test_returns_422_for_price_exceeding_max(self, client, admin_token):
        res = client.post(
            "/api/items",
            json={"name": "test", "price": 1_000_001},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert res.status_code == 422

    def test_creates_item_successfully(self, client, admin_token):
        res = client.post(
            "/api/items",
            json={"name": "New Widget", "price": 9.99, "category": "tools"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert res.status_code == 201
        data = res.json()
        assert "id" in data
        assert data["name"] == "New Widget"

    def test_returns_403_for_non_admin(self, client, valid_token):
        res = client.post(
            "/api/items",
            json={"name": "test", "price": 1.0},
            headers={"Authorization": f"Bearer {valid_token}"},
        )
        assert res.status_code == 403


class TestPagination:
    def test_returns_paginated_response(self, client, valid_token):
        res = client.get(
            "/api/items?page=1&size=10",
            headers={"Authorization": f"Bearer {valid_token}"},
        )
        assert res.status_code == 200
        data = res.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert len(data["items"]) <= 10

    def test_empty_result_for_out_of_range_page(self, client, valid_token):
        res = client.get(
            "/api/items?page=99999",
            headers={"Authorization": f"Bearer {valid_token}"},
        )
        assert res.status_code == 200
        assert res.json()["items"] == []

    def test_returns_422_for_page_zero(self, client, valid_token):
        res = client.get(
            "/api/items?page=0",
            headers={"Authorization": f"Bearer {valid_token}"},
        )
        assert res.status_code == 422

    def test_caps_page_size_at_maximum(self, client, valid_token):
        res = client.get(
            "/api/items?size=9999",
            headers={"Authorization": f"Bearer {valid_token}"},
        )
        assert res.status_code == 200
        assert len(res.json()["items"]) <= 100  # max page size


class TestRateLimiting:
    def test_rate_limit_after_burst(self, client, valid_token):
        responses = []
        for _ in range(60):  # exceed typical 50/min limit
            res = client.get(
                "/api/items",
                headers={"Authorization": f"Bearer {valid_token}"},
            )
            responses.append(res.status_code)
            if res.status_code == 429:
                break
        assert 429 in responses, "Rate limit was not triggered"

    def test_rate_limit_response_has_retry_after(self, client, valid_token):
        for _ in range(60):
            res = client.get("/api/items", headers={"Authorization": f"Bearer {valid_token}"})
            if res.status_code == 429:
                assert "Retry-After" in res.headers or "retry_after" in res.json()
                break
```

---

## Generating Tests from Route Scan

When given a codebase, follow this process:

1. **Scan routes** using the detection commands above
2. **Read each route handler** to understand:
   - Expected request body schema
   - Auth requirements (middleware, decorators)
   - Return types and status codes
   - Business rules (ownership, role checks)
3. **Generate test file** per route group using the patterns above
4. **Name tests descriptively**: `"returns 401 when token is expired"` not `"auth test 3"`
5. **Use factories/fixtures** for test data — never hardcode IDs
6. **Assert response shape**, not just status code

---

## Common Pitfalls

- **Testing only happy paths** — 80% of bugs live in error paths; test those first
- **Hardcoded test data IDs** — use factories/fixtures; IDs change between environments
- **Shared state between tests** — always clean up in afterEach/afterAll
- **Testing implementation, not behavior** — test what the API returns, not how it does it
- **Missing boundary tests** — off-by-one errors are extremely common in pagination and limits
- **Not testing token expiry** — expired tokens behave differently from invalid ones
- **Ignoring Content-Type** — test that API rejects wrong content types (xml when json expected)

---

## Best Practices

1. One describe block per endpoint — keeps failures isolated and readable
2. Seed minimal data — don't load the entire DB; create only what the test needs
3. Use `beforeAll` for shared setup, `afterAll` for cleanup — not `beforeEach` for expensive ops
4. Assert specific error messages/fields, not just status codes
5. Test that sensitive fields (password, secret) are never in responses
6. For auth tests, always test the "missing header" case separately from "invalid token"
7. Add rate limit tests last — they can interfere with other test suites if run in parallel
