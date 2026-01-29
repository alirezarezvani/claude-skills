# Deployment Strategies Guide

Reference for blue-green, canary, rolling deployments, and rollback procedures.

---

## Table of Contents

- [Strategy Comparison](#strategy-comparison)
- [Blue-Green Deployment](#blue-green-deployment)
- [Canary Deployment](#canary-deployment)
- [Rolling Deployment](#rolling-deployment)
- [Rollback Procedures](#rollback-procedures)
- [Health Checks](#health-checks)

---

## Strategy Comparison

### Decision Matrix

```
┌─────────────────────────────────────────────────────────────┐
│                  DEPLOYMENT STRATEGY SELECTION              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  RISK vs COST TRADEOFF                                      │
│                                                             │
│  Cost ↑                                                     │
│       │     Blue-Green                                      │
│       │        ●                                            │
│       │                                                     │
│       │              Canary                                 │
│       │                 ●                                   │
│       │                                                     │
│       │                       Rolling                       │
│       │                          ●                          │
│       │                                                     │
│       └────────────────────────────────────────→ Risk ↑     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Strategy Overview

| Strategy | Downtime | Rollback Speed | Cost | Risk | Best For |
|----------|----------|----------------|------|------|----------|
| Blue-Green | Zero | Instant | High (2x) | Low | Critical systems |
| Canary | Zero | Fast | Medium | Medium | User-facing services |
| Rolling | Zero | Slow | Low | Medium | Stateless services |
| Recreate | Yes | N/A | Low | High | Dev/test only |

### Selection Guide

**Choose Blue-Green when:**
- Zero downtime is mandatory
- Instant rollback is required
- Infrastructure cost is acceptable
- Database schema changes are minimal

**Choose Canary when:**
- You need to test with real traffic
- Gradual rollout is acceptable
- You have good monitoring/observability
- User segmentation is possible

**Choose Rolling when:**
- Cost optimization is priority
- Service is stateless
- Some deployment risk is acceptable
- You have health checks in place

---

## Blue-Green Deployment

### Architecture

```
                    Load Balancer
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
       ┌──────────────┐     ┌──────────────┐
       │    BLUE      │     │    GREEN     │
       │   (Active)   │     │   (Idle)     │
       │              │     │              │
       │  v1.0.0      │     │  v1.1.0      │
       │  3 replicas  │     │  3 replicas  │
       └──────────────┘     └──────────────┘
              │                     │
              └─────────┬───────────┘
                        ▼
                   Database
                  (shared)
```

### Kubernetes Implementation

```yaml
# blue-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
  labels:
    app: myapp
    version: blue
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
        image: myapp:v1.0.0
        ports:
        - containerPort: 8080
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 10

---
# green-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-green
  labels:
    app: myapp
    version: green
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
        image: myapp:v1.1.0
        ports:
        - containerPort: 8080
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5

---
# service.yaml (switch between blue/green)
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    version: blue  # Change to 'green' to switch
  ports:
  - port: 80
    targetPort: 8080
```

### AWS ALB Blue-Green

```hcl
# Terraform for ALB blue-green
resource "aws_lb_target_group" "blue" {
  name     = "${var.name}-blue"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    path                = "/health"
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 10
  }
}

resource "aws_lb_target_group" "green" {
  name     = "${var.name}-green"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    path                = "/health"
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 10
  }
}

resource "aws_lb_listener_rule" "main" {
  listener_arn = var.listener_arn
  priority     = 100

  action {
    type             = "forward"
    target_group_arn = var.active_color == "blue" ? aws_lb_target_group.blue.arn : aws_lb_target_group.green.arn
  }

  condition {
    path_pattern {
      values = ["/*"]
    }
  }
}
```

### Switch Procedure

```bash
#!/bin/bash
# blue-green-switch.sh

CURRENT_COLOR=$(kubectl get svc myapp -o jsonpath='{.spec.selector.version}')

if [ "$CURRENT_COLOR" == "blue" ]; then
  NEW_COLOR="green"
else
  NEW_COLOR="blue"
fi

echo "Switching from $CURRENT_COLOR to $NEW_COLOR"

# Verify new deployment is healthy
kubectl rollout status deployment/app-$NEW_COLOR --timeout=300s

# Switch traffic
kubectl patch svc myapp -p "{\"spec\":{\"selector\":{\"version\":\"$NEW_COLOR\"}}}"

echo "Traffic now routing to $NEW_COLOR"
```

---

## Canary Deployment

### Traffic Split Architecture

```
                    Load Balancer
                         │
              ┌──────────┴──────────┐
              │ 90%            10%  │
              ▼                     ▼
       ┌──────────────┐     ┌──────────────┐
       │   STABLE     │     │   CANARY     │
       │              │     │              │
       │  v1.0.0      │     │  v1.1.0      │
       │  9 replicas  │     │  1 replica   │
       └──────────────┘     └──────────────┘
```

### Kubernetes with Istio

```yaml
# VirtualService for canary traffic split
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
  - myapp
  http:
  - match:
    - headers:
        canary:
          exact: "true"
    route:
    - destination:
        host: myapp
        subset: canary
  - route:
    - destination:
        host: myapp
        subset: stable
      weight: 90
    - destination:
        host: myapp
        subset: canary
      weight: 10

---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myapp
spec:
  host: myapp
  subsets:
  - name: stable
    labels:
      version: stable
  - name: canary
    labels:
      version: canary
```

### AWS ALB Weighted Routing

```hcl
resource "aws_lb_listener_rule" "canary" {
  listener_arn = var.listener_arn
  priority     = 100

  action {
    type = "forward"

    forward {
      target_group {
        arn    = aws_lb_target_group.stable.arn
        weight = 90
      }

      target_group {
        arn    = aws_lb_target_group.canary.arn
        weight = 10
      }

      stickiness {
        enabled  = true
        duration = 3600
      }
    }
  }

  condition {
    path_pattern {
      values = ["/*"]
    }
  }
}
```

### Canary Analysis Script

```python
#!/usr/bin/env python3
"""
Canary analysis - compare metrics between stable and canary
"""

import requests
import time

PROMETHEUS_URL = "http://prometheus:9090"
CANARY_THRESHOLD = {
    "error_rate": 0.01,      # Max 1% error rate
    "latency_p99": 500,      # Max 500ms p99 latency
    "success_rate": 0.99     # Min 99% success rate
}

def query_prometheus(query: str) -> float:
    response = requests.get(
        f"{PROMETHEUS_URL}/api/v1/query",
        params={"query": query}
    )
    result = response.json()
    if result["data"]["result"]:
        return float(result["data"]["result"][0]["value"][1])
    return 0.0

def analyze_canary() -> dict:
    """Compare canary vs stable metrics"""

    # Error rate comparison
    stable_errors = query_prometheus(
        'sum(rate(http_requests_total{version="stable",status=~"5.."}[5m])) / '
        'sum(rate(http_requests_total{version="stable"}[5m]))'
    )
    canary_errors = query_prometheus(
        'sum(rate(http_requests_total{version="canary",status=~"5.."}[5m])) / '
        'sum(rate(http_requests_total{version="canary"}[5m]))'
    )

    # Latency comparison
    stable_latency = query_prometheus(
        'histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{version="stable"}[5m])) by (le)) * 1000'
    )
    canary_latency = query_prometheus(
        'histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{version="canary"}[5m])) by (le)) * 1000'
    )

    analysis = {
        "pass": True,
        "metrics": {
            "stable_error_rate": stable_errors,
            "canary_error_rate": canary_errors,
            "stable_latency_p99": stable_latency,
            "canary_latency_p99": canary_latency
        },
        "checks": []
    }

    # Check error rate
    if canary_errors > CANARY_THRESHOLD["error_rate"]:
        analysis["pass"] = False
        analysis["checks"].append(f"FAIL: Canary error rate {canary_errors:.2%} > threshold {CANARY_THRESHOLD['error_rate']:.2%}")
    else:
        analysis["checks"].append(f"PASS: Canary error rate {canary_errors:.2%}")

    # Check latency
    if canary_latency > CANARY_THRESHOLD["latency_p99"]:
        analysis["pass"] = False
        analysis["checks"].append(f"FAIL: Canary p99 latency {canary_latency:.0f}ms > threshold {CANARY_THRESHOLD['latency_p99']}ms")
    else:
        analysis["checks"].append(f"PASS: Canary p99 latency {canary_latency:.0f}ms")

    return analysis

if __name__ == "__main__":
    result = analyze_canary()
    for check in result["checks"]:
        print(check)

    if result["pass"]:
        print("\n✅ Canary analysis PASSED - safe to promote")
        exit(0)
    else:
        print("\n❌ Canary analysis FAILED - rollback recommended")
        exit(1)
```

### Progressive Rollout

```bash
#!/bin/bash
# progressive-canary.sh

STAGES=(10 25 50 75 100)
ANALYSIS_INTERVAL=300  # 5 minutes between stages

for weight in "${STAGES[@]}"; do
    echo "Setting canary weight to ${weight}%"

    # Update traffic split
    kubectl patch virtualservice myapp --type=merge -p "{
        \"spec\": {
            \"http\": [{
                \"route\": [
                    {\"destination\": {\"host\": \"myapp\", \"subset\": \"stable\"}, \"weight\": $((100 - weight))},
                    {\"destination\": {\"host\": \"myapp\", \"subset\": \"canary\"}, \"weight\": $weight}
                ]
            }]
        }
    }"

    echo "Waiting ${ANALYSIS_INTERVAL}s for metrics..."
    sleep $ANALYSIS_INTERVAL

    # Run analysis
    if ! python3 canary_analysis.py; then
        echo "❌ Canary failed at ${weight}% - rolling back"
        kubectl patch virtualservice myapp --type=merge -p '{
            "spec": {"http": [{"route": [{"destination": {"host": "myapp", "subset": "stable"}, "weight": 100}]}]}
        }'
        exit 1
    fi

    echo "✅ Stage ${weight}% passed"
done

echo "🎉 Canary promotion complete"
```

---

## Rolling Deployment

### Kubernetes Rolling Update

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%        # Can have 25% more pods during update
      maxUnavailable: 25%  # Can have 25% fewer pods during update
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
        image: myapp:v1.1.0
        ports:
        - containerPort: 8080
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
          successThreshold: 1
          failureThreshold: 3
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 10
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### ECS Rolling Update

```hcl
resource "aws_ecs_service" "main" {
  name            = var.name
  cluster         = var.cluster_id
  task_definition = aws_ecs_task_definition.main.arn
  desired_count   = 4

  deployment_configuration {
    minimum_healthy_percent = 50   # Keep at least 50% healthy
    maximum_percent         = 200  # Can scale to 200% during deploy
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true  # Auto-rollback on failure
  }

  # Ensure new tasks are healthy before stopping old ones
  health_check_grace_period_seconds = 60
}
```

---

## Rollback Procedures

### Kubernetes Rollback

```bash
# View rollout history
kubectl rollout history deployment/myapp

# Rollback to previous version
kubectl rollout undo deployment/myapp

# Rollback to specific revision
kubectl rollout undo deployment/myapp --to-revision=3

# Check rollback status
kubectl rollout status deployment/myapp
```

### Automated Rollback Script

```bash
#!/bin/bash
# auto-rollback.sh

DEPLOYMENT="myapp"
NAMESPACE="production"
ERROR_THRESHOLD=5
CHECK_INTERVAL=10
CHECK_COUNT=0
ERROR_COUNT=0

echo "Monitoring deployment $DEPLOYMENT for errors..."

while [ $CHECK_COUNT -lt 30 ]; do
    # Check pod status
    UNHEALTHY=$(kubectl get pods -n $NAMESPACE -l app=$DEPLOYMENT \
        --field-selector=status.phase!=Running \
        --no-headers 2>/dev/null | wc -l)

    # Check for crash loops
    CRASHLOOP=$(kubectl get pods -n $NAMESPACE -l app=$DEPLOYMENT \
        -o jsonpath='{.items[*].status.containerStatuses[*].restartCount}' | \
        awk '{for(i=1;i<=NF;i++) if($i>3) print $i}' | wc -l)

    if [ $UNHEALTHY -gt 0 ] || [ $CRASHLOOP -gt 0 ]; then
        ((ERROR_COUNT++))
        echo "⚠️ Error detected: unhealthy=$UNHEALTHY, crashloop=$CRASHLOOP"

        if [ $ERROR_COUNT -ge $ERROR_THRESHOLD ]; then
            echo "❌ Error threshold reached. Initiating rollback..."
            kubectl rollout undo deployment/$DEPLOYMENT -n $NAMESPACE
            kubectl rollout status deployment/$DEPLOYMENT -n $NAMESPACE --timeout=300s

            # Send alert
            curl -X POST "$SLACK_WEBHOOK" -d "{
                \"text\": \"🔄 Auto-rollback triggered for $DEPLOYMENT in $NAMESPACE\"
            }"

            exit 1
        fi
    else
        ERROR_COUNT=0
    fi

    ((CHECK_COUNT++))
    sleep $CHECK_INTERVAL
done

echo "✅ Deployment stable after ${CHECK_COUNT} checks"
```

### ECS Rollback

```bash
#!/bin/bash
# ecs-rollback.sh

CLUSTER="production"
SERVICE="myapp"

# Get previous task definition
CURRENT_TASK=$(aws ecs describe-services \
    --cluster $CLUSTER \
    --services $SERVICE \
    --query 'services[0].taskDefinition' \
    --output text)

CURRENT_REVISION=$(echo $CURRENT_TASK | grep -oP ':\K\d+$')
PREVIOUS_REVISION=$((CURRENT_REVISION - 1))

TASK_FAMILY=$(echo $CURRENT_TASK | sed 's/:[0-9]*$//')
PREVIOUS_TASK="${TASK_FAMILY}:${PREVIOUS_REVISION}"

echo "Rolling back from revision $CURRENT_REVISION to $PREVIOUS_REVISION"

# Update service with previous task definition
aws ecs update-service \
    --cluster $CLUSTER \
    --service $SERVICE \
    --task-definition $PREVIOUS_TASK

# Wait for rollback to complete
aws ecs wait services-stable \
    --cluster $CLUSTER \
    --services $SERVICE

echo "✅ Rollback complete"
```

---

## Health Checks

### Kubernetes Probes

```yaml
containers:
- name: app
  image: myapp:latest

  # Readiness: Is the container ready to serve traffic?
  readinessProbe:
    httpGet:
      path: /ready
      port: 8080
    initialDelaySeconds: 5
    periodSeconds: 5
    successThreshold: 1
    failureThreshold: 3

  # Liveness: Is the container alive?
  livenessProbe:
    httpGet:
      path: /health
      port: 8080
    initialDelaySeconds: 15
    periodSeconds: 10
    timeoutSeconds: 5
    failureThreshold: 3

  # Startup: Has the container started? (for slow-starting apps)
  startupProbe:
    httpGet:
      path: /health
      port: 8080
    initialDelaySeconds: 10
    periodSeconds: 10
    failureThreshold: 30  # 30 * 10 = 5 minutes to start
```

### Health Check Endpoint

```javascript
// Express.js health check endpoints
app.get('/health', (req, res) => {
  // Basic liveness check
  res.status(200).json({ status: 'healthy' });
});

app.get('/ready', async (req, res) => {
  try {
    // Check database connection
    await db.query('SELECT 1');

    // Check cache connection
    await redis.ping();

    // Check external dependencies
    const externalHealthy = await checkExternalServices();

    if (externalHealthy) {
      res.status(200).json({
        status: 'ready',
        checks: {
          database: 'healthy',
          cache: 'healthy',
          external: 'healthy'
        }
      });
    } else {
      res.status(503).json({
        status: 'not ready',
        checks: {
          database: 'healthy',
          cache: 'healthy',
          external: 'unhealthy'
        }
      });
    }
  } catch (error) {
    res.status(503).json({
      status: 'not ready',
      error: error.message
    });
  }
});
```

### ALB Health Check

```hcl
resource "aws_lb_target_group" "main" {
  name     = var.name
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    enabled             = true
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 10
    matcher             = "200-299"
  }

  # Wait for draining before removing instances
  deregistration_delay = 30

  stickiness {
    type            = "lb_cookie"
    cookie_duration = 3600
    enabled         = true
  }
}
```

---

## Quick Reference

### Deployment Commands

| Action | Kubernetes | ECS |
|--------|------------|-----|
| Deploy | `kubectl apply -f deployment.yaml` | `aws ecs update-service` |
| Rollback | `kubectl rollout undo deployment/app` | Update to previous task def |
| Status | `kubectl rollout status deployment/app` | `aws ecs wait services-stable` |
| History | `kubectl rollout history deployment/app` | List task definitions |
| Scale | `kubectl scale deployment/app --replicas=5` | Update desired count |

### Health Check Timing

| Probe | Initial Delay | Period | Timeout | Failures |
|-------|---------------|--------|---------|----------|
| Readiness | 5s | 5s | 3s | 3 |
| Liveness | 15s | 10s | 5s | 3 |
| Startup | 10s | 10s | 5s | 30 |

---

*See also: `cicd_pipeline_guide.md` for CI/CD integration*
