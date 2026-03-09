

Using the **performance-profiler** skill to give you a systematic plan.

---

## Systematic Profiling Plan for GET /api/users

Your symptoms (200ms → 3s at 500 concurrent users) point to either database saturation, connection pool exhaustion, or N+1 queries. Here's the exact sequence to find out.

### Phase 1: Establish Baseline

```bash
# Install tools
npm install -g clinic autocannon k6

# Baseline load test — record P50/P95/P99 before touching anything
k6 run --vus 500 --duration 60s -e BASE_URL=http://localhost:3000 - <<'EOF'
import http from 'k6/http'
import { check } from 'k6'

export const options = {
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
  },
}

export default function() {
  const res = http.get(`${__ENV.BASE_URL}/api/users`)
  check(res, { 'status 200': (r) => r.status === 200 })
}
EOF
```

Record the output: P50, P95, P99, RPS, error rate.

### Phase 2: Find the Bottleneck Layer

Run these three checks in parallel — each eliminates a different layer:

**2a. Database — is the query itself slow?**

```sql
-- Enable pg_stat_statements if not already
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Find the slow queries
SELECT
  round(mean_exec_time::numeric, 2) AS mean_ms,
  calls,
  round(total_exec_time::numeric, 2) AS total_ms,
  left(query, 100) AS query
FROM pg_stat_statements
WHERE calls > 10
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Then EXPLAIN the /api/users query specifically
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM users WHERE deleted_at IS NULL ORDER BY created_at DESC LIMIT 20;
```

Look for: `Seq Scan` on large tables (needs index), high `actual time`.

**2b. N+1 detection — is Node making too many queries per request?**

Add temporary query counting:

```javascript
// Add to your DB client temporarily
let queryCount = 0;
pool.on('query', () => queryCount++);

app.use((req, res, next) => {
  queryCount = 0;
  res.on('finish', () => {
    if (queryCount > 3) {
      console.warn(`⚠️ ${req.method} ${req.url}: ${queryCount} queries`);
    }
  });
  next();
});
```

If you see 20+ queries for one GET /api/users, you have an N+1.

**2c. Connection pool — is it exhausted under load?**

```javascript
// Log pool stats every 5s
setInterval(() => {
  console.log({
    total: pool.totalCount,
    idle: pool.idleCount,
    waiting: pool.waitingCount,  // > 0 means pool exhaustion
  });
}, 5000);
```

If `waitingCount` climbs under load, increase `max` in your pool config (default is often just 10).

### Phase 3: CPU Flamegraph

```bash
# Run under clinic flame while applying load
autocannon -c 500 -d 30 http://localhost:3000/api/users &
clinic flame -- node dist/server.js
```

This opens a flamegraph in your browser. Look for wide bars — those are where CPU time is spent. Common culprits: JSON serialization of massive result sets, synchronous operations blocking the event loop.

### Phase 4: Event Loop Blocking

```bash
npm install blocked-at
```

```javascript
import blocked from 'blocked-at';
blocked((time, stack) => {
  console.warn(`Event loop blocked for ${time}ms`, stack[0]);
}, { threshold: 50 });
```

### Phase 5: Fix and Re-measure

Based on what Phase 2-4 reveals, the fix is usually one of:

| Root Cause | Fix |
|---|---|
| Seq Scan | `CREATE INDEX idx_users_created ON users(created_at DESC) WHERE deleted_at IS NULL` |
| N+1 queries | Replace loop with JOIN or batch query |
| Pool exhaustion | Increase `max` to 50-100, add `connectionTimeoutMillis` |
| No pagination | Add `LIMIT`/`OFFSET` or cursor pagination |
| SELECT * | Select only needed columns |
| No caching | Add `Cache-Control` headers or Redis for hot data |

After fixing, re-run the exact same k6 baseline test and fill in the before/after table:

```markdown
| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| P50    | ?ms    | ?ms   | ?%    |
| P95    | ?ms    | ?ms   | ?%    |
| P99    | ?ms    | ?ms   | ?%    |
| RPS    | ?      | ?     | ?%    |
```

### Most Likely Culprit

Given the pattern (fine at low load, degrades at 500 concurrent), my top suspects in order:

1. **Connection pool exhaustion** — default pool of 10 connections serving 500 users
2. **N+1 queries** — amplifies the pool problem (20 queries/request × 500 users = 10,000 queries competing for 10 connections)
3. **Missing index** — Seq Scan gets worse as table grows

Start with Phase 2a-2c. You'll likely find your answer there without needing the flamegraph.
