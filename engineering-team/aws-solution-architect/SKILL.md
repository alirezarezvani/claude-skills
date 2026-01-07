---
name: aws-solution-architect
description: Expert AWS solution architecture for startups focusing on serverless, scalable, and cost-effective cloud infrastructure with modern DevOps practices and infrastructure-as-code
---

# AWS Solution Architect for Startups

This skill provides comprehensive AWS architecture design expertise for startup companies, emphasizing serverless technologies, scalability, cost optimization, and modern cloud-native patterns.

## Capabilities

- **Serverless Architecture Design**: Lambda, API Gateway, DynamoDB, EventBridge, Step Functions, AppSync
- **Infrastructure as Code**: CloudFormation, CDK (Cloud Development Kit), Terraform templates
- **Scalable Application Architecture**: Auto-scaling, load balancing, multi-region deployment
- **Data & Storage Solutions**: S3, RDS Aurora Serverless, DynamoDB, ElastiCache, Neptune
- **Event-Driven Architecture**: EventBridge, SNS, SQS, Kinesis, Lambda triggers
- **API Design**: API Gateway (REST & WebSocket), AppSync (GraphQL), rate limiting, authentication
- **Authentication & Authorization**: Cognito, IAM, fine-grained access control, federated identity
- **CI/CD Pipelines**: CodePipeline, CodeBuild, CodeDeploy, GitHub Actions integration
- **Monitoring & Observability**: CloudWatch, X-Ray, CloudTrail, alarms, dashboards
- **Cost Optimization**: Reserved instances, Savings Plans, right-sizing, budget alerts
- **Security Best Practices**: VPC design, security groups, WAF, Secrets Manager, encryption
- **Microservices Patterns**: Service mesh, API composition, saga patterns, CQRS
- **Container Orchestration**: ECS Fargate, EKS (Kubernetes), App Runner
- **Content Delivery**: CloudFront, edge locations, origin shield, caching strategies
- **Database Migration**: DMS, schema conversion, zero-downtime migrations

## Input Requirements

Architecture design requires:
- **Application type**: Web app, mobile backend, data pipeline, microservices, SaaS platform
- **Traffic expectations**: Users/day, requests/second, geographic distribution
- **Data requirements**: Storage needs, database type, backup/retention policies
- **Budget constraints**: Monthly spend limits, cost optimization priorities
- **Team size & expertise**: Developer count, AWS experience level, DevOps maturity
- **Compliance needs**: GDPR, HIPAA, SOC 2, PCI-DSS, data residency
- **Availability requirements**: SLA targets, uptime goals, disaster recovery RPO/RTO

Formats accepted:
- Text description of application requirements
- JSON with structured architecture specifications
- Existing architecture diagrams or documentation
- Current AWS resource inventory (for optimization)

## Output Formats

Results include:
- **Architecture diagrams**: Visual representations using draw.io or Lucidchart format
- **CloudFormation/CDK templates**: Infrastructure as Code (IaC) ready to deploy
- **Terraform configurations**: Multi-cloud compatible infrastructure definitions
- **Cost estimates**: Detailed monthly cost breakdown with optimization suggestions
- **Security assessment**: Best practices checklist, compliance validation
- **Deployment guides**: Step-by-step implementation instructions
- **Runbooks**: Operational procedures, troubleshooting guides, disaster recovery plans
- **Migration strategies**: Phased migration plans, rollback procedures

## How to Use

"Design a serverless API backend for a mobile app with 100k users using Lambda and DynamoDB"
"Create a cost-optimized architecture for a SaaS platform with multi-tenancy"
"Generate CloudFormation template for a three-tier web application with auto-scaling"
"Design event-driven microservices architecture using EventBridge and Step Functions"
"Optimize my current AWS setup to reduce costs by 30%"

## Scripts

- `architecture_designer.py`: Generates architecture patterns and service recommendations
- `serverless_stack.py`: Creates serverless application stacks (Lambda, API Gateway, DynamoDB)
- `cost_optimizer.py`: Analyzes AWS costs and provides optimization recommendations
- `iac_generator.py`: Generates CloudFormation, CDK, or Terraform templates
- `security_auditor.py`: AWS security best practices validation and compliance checks

## Architecture Patterns

### 1. Serverless Web Application
**Use Case**: SaaS platforms, mobile backends, low-traffic websites

**Stack**:
- **Frontend**: S3 + CloudFront (static hosting)
- **API**: API Gateway + Lambda
- **Database**: DynamoDB or Aurora Serverless
- **Auth**: Cognito
- **CI/CD**: Amplify or CodePipeline

**Benefits**: Zero server management, pay-per-use, auto-scaling, low operational overhead

**Cost**: $50-500/month for small to medium traffic

### 2. Event-Driven Microservices
**Use Case**: Complex business workflows, asynchronous processing, decoupled systems

**Stack**:
- **Events**: EventBridge (event bus)
- **Processing**: Lambda functions or ECS Fargate
- **Queue**: SQS (dead letter queues for failures)
- **State Management**: Step Functions
- **Storage**: DynamoDB, S3

**Benefits**: Loose coupling, independent scaling, failure isolation, easy testing

**Cost**: $100-1000/month depending on event volume

### 3. Modern Three-Tier Application
**Use Case**: Traditional web apps with dynamic content, e-commerce, CMS

**Stack**:
- **Load Balancer**: ALB (Application Load Balancer)
- **Compute**: ECS Fargate or EC2 Auto Scaling
- **Database**: RDS Aurora (MySQL/PostgreSQL)
- **Cache**: ElastiCache (Redis)
- **CDN**: CloudFront
- **Storage**: S3

**Benefits**: Proven pattern, easy to understand, flexible scaling

**Cost**: $300-2000/month depending on traffic and instance sizes

### 4. Real-Time Data Processing
**Use Case**: Analytics, IoT data ingestion, log processing, streaming

**Stack**:
- **Ingestion**: Kinesis Data Streams or Firehose
- **Processing**: Lambda or Kinesis Analytics
- **Storage**: S3 (data lake) + Athena (queries)
- **Visualization**: QuickSight
- **Alerting**: CloudWatch + SNS

**Benefits**: Handle millions of events, real-time insights, cost-effective storage

**Cost**: $200-1500/month depending on data volume

### 5. GraphQL API Backend
**Use Case**: Mobile apps, single-page applications, flexible data queries

**Stack**:
- **API**: AppSync (managed GraphQL)
- **Resolvers**: Lambda or direct DynamoDB integration
- **Database**: DynamoDB
- **Real-time**: AppSync subscriptions (WebSocket)
- **Auth**: Cognito or API keys

**Benefits**: Single endpoint, reduce over/under-fetching, real-time subscriptions

**Cost**: $50-400/month for moderate usage

### 6. Multi-Region High Availability
**Use Case**: Global applications, disaster recovery, compliance requirements

**Stack**:
- **DNS**: Route 53 (geolocation routing)
- **CDN**: CloudFront with multiple origins
- **Compute**: Multi-region Lambda or ECS
- **Database**: DynamoDB Global Tables or Aurora Global Database
- **Replication**: S3 cross-region replication

**Benefits**: Low latency globally, disaster recovery, data sovereignty

**Cost**: 1.5-2x single region costs

## Best Practices

### Serverless Design Principles
1. **Stateless functions** - Store state in DynamoDB, S3, or ElastiCache
2. **Idempotency** - Handle retries gracefully, use unique request IDs
3. **Cold start optimization** - Use provisioned concurrency for critical paths, optimize package size
4. **Timeout management** - Set appropriate timeouts, use Step Functions for long processes
5. **Error handling** - Implement retry logic, dead letter queues, exponential backoff

### Cost Optimization
1. **Right-sizing** - Start small, monitor metrics, scale based on actual usage
2. **Reserved capacity** - Use Savings Plans or Reserved Instances for predictable workloads
3. **S3 lifecycle policies** - Transition to cheaper storage tiers (IA, Glacier)
4. **Lambda memory optimization** - Test different memory settings for cost/performance balance
5. **CloudWatch log retention** - Set appropriate retention periods (7-30 days for most)
6. **NAT Gateway alternatives** - Use VPC endpoints, consider single NAT in dev environments

### Security Hardening
1. **Principle of least privilege** - IAM roles with minimal permissions
2. **Encryption everywhere** - At rest (KMS) and in transit (TLS/SSL)
3. **Network isolation** - Private subnets, security groups, NACLs
4. **Secrets management** - Use Secrets Manager or Parameter Store, never hardcode
5. **API protection** - WAF rules, rate limiting, API keys, OAuth2
6. **Audit logging** - CloudTrail for API calls, VPC Flow Logs for network traffic

### Scalability Design
1. **Horizontal over vertical** - Scale out with more small instances vs. larger instances
2. **Database sharding** - Partition data by tenant, geography, or time
3. **Read replicas** - Offload read traffic from primary database
4. **Caching layers** - CloudFront (edge), ElastiCache (application), DAX (DynamoDB)
5. **Async processing** - Use queues (SQS) for non-critical operations
6. **Auto-scaling policies** - Target tracking (CPU, requests) vs. step scaling

### DevOps & Reliability
1. **Infrastructure as Code** - Version control, peer review, automated testing
2. **Blue/Green deployments** - Zero-downtime releases, instant rollback
3. **Canary releases** - Test new versions with small traffic percentage
4. **Health checks** - Application-level health endpoints, graceful degradation
5. **Chaos engineering** - Test failure scenarios, validate recovery procedures
6. **Monitoring & alerting** - Set up CloudWatch alarms for critical metrics

## Service Selection Guide

### Compute
- **Lambda**: Event-driven, short-duration tasks (<15 min), variable traffic
- **Fargate**: Containerized apps, long-running processes, predictable traffic
- **EC2**: Custom configurations, GPU/FPGA needs, Windows apps
- **App Runner**: Simple container deployment from source code

### Database
- **DynamoDB**: Key-value, document store, serverless, single-digit ms latency
- **Aurora Serverless**: Relational DB, variable workloads, auto-scaling
- **Aurora Standard**: High-performance relational, predictable traffic
- **RDS**: Traditional databases (MySQL, PostgreSQL, MariaDB, SQL Server)
- **DocumentDB**: MongoDB-compatible, document store
- **Neptune**: Graph database for connected data
- **Timestream**: Time-series data, IoT metrics

### Storage
- **S3 Standard**: Frequent access, low latency
- **S3 Intelligent-Tiering**: Automatic cost optimization
- **S3 IA (Infrequent Access)**: Backups, archives (30-day minimum)
- **S3 Glacier**: Long-term archives, compliance
- **EFS**: Network file system, shared storage across instances
- **EBS**: Block storage for EC2, high IOPS

### Messaging & Events
- **EventBridge**: Event bus, loosely coupled microservices
- **SNS**: Pub/sub, fan-out notifications
- **SQS**: Message queuing, decoupling, buffering
- **Kinesis**: Real-time streaming data, analytics
- **MQ**: Managed message brokers (RabbitMQ, ActiveMQ)

### API & Integration
- **API Gateway**: REST APIs, WebSocket, throttling, caching
- **AppSync**: GraphQL APIs, real-time subscriptions
- **AppFlow**: SaaS integration (Salesforce, Slack, etc.)
- **Step Functions**: Workflow orchestration, state machines

## Startup-Specific Considerations

### MVP (Minimum Viable Product) Architecture
**Goal**: Launch fast, minimal infrastructure

**Recommended**:
- Amplify (full-stack deployment)
- Lambda + API Gateway + DynamoDB
- Cognito for auth
- CloudFront + S3 for frontend

**Cost**: $20-100/month
**Setup time**: 1-3 days

### Growth Stage (Scaling to 10k-100k users)
**Goal**: Handle growth, maintain cost efficiency

**Add**:
- ElastiCache for caching
- Aurora Serverless for complex queries
- CloudWatch dashboards and alarms
- CI/CD pipeline (CodePipeline)
- Multi-AZ deployment

**Cost**: $500-2000/month
**Migration time**: 1-2 weeks

### Scale-Up (100k+ users, Series A+)
**Goal**: Reliability, observability, global reach

**Add**:
- Multi-region deployment
- DynamoDB Global Tables
- Advanced monitoring (X-Ray, third-party APM)
- WAF and Shield for DDoS protection
- Dedicated support plan
- Reserved instances/Savings Plans

**Cost**: $3000-10000/month
**Migration time**: 1-3 months

## Common Pitfalls to Avoid

### Technical Debt
- **Over-engineering early** - Don't build for 10M users when you have 100
- **Under-monitoring** - Set up basic monitoring from day one
- **Ignoring costs** - Enable Cost Explorer and billing alerts immediately
- **Single region dependency** - Plan for multi-region from start

### Security Mistakes
- **Public S3 buckets** - Use bucket policies, block public access
- **Overly permissive IAM** - Avoid "*" permissions, use specific resources
- **Hardcoded credentials** - Use IAM roles, Secrets Manager
- **Unencrypted data** - Enable encryption by default

### Performance Issues
- **No caching** - Add CloudFront, ElastiCache early
- **Inefficient queries** - Use indexes, avoid scans in DynamoDB
- **Large Lambda packages** - Use layers, minimize dependencies
- **N+1 queries** - Implement DataLoader pattern, batch operations

### Cost Surprises
- **Undeleted resources** - Tag everything, review regularly
- **Data transfer costs** - Keep traffic within same AZ/region when possible
- **NAT Gateway charges** - Use VPC endpoints for AWS services
- **CloudWatch Logs accumulation** - Set retention policies

## Compliance & Governance

### Data Residency
- Use specific regions (eu-west-1 for GDPR)
- Enable S3 bucket replication restrictions
- Configure Route 53 geolocation routing

### HIPAA Compliance
- Use BAA-eligible services only
- Enable encryption at rest and in transit
- Implement audit logging (CloudTrail)
- Configure VPC with private subnets

### SOC 2 / ISO 27001
- Enable AWS Config for compliance rules
- Use AWS Audit Manager
- Implement least privilege access
- Regular security assessments

## Limitations

- **Lambda limitations**: 15-minute execution limit, 10GB memory max, cold start latency
- **API Gateway limits**: 29-second timeout, 10MB payload size
- **DynamoDB limits**: 400KB item size, eventually consistent reads by default
- **Regional availability**: Not all services available in all regions
- **Vendor lock-in**: Some serverless services are AWS-specific (consider abstraction layers)
- **Learning curve**: Requires AWS expertise, DevOps knowledge
- **Debugging complexity**: Distributed systems harder to troubleshoot than monoliths

## Helpful Resources

- **AWS Well-Architected Framework**: https://aws.amazon.com/architecture/well-architected/
- **AWS Architecture Center**: https://aws.amazon.com/architecture/
- **Serverless Land**: https://serverlessland.com/
- **AWS Pricing Calculator**: https://calculator.aws/
- **AWS Cost Explorer**: Track and analyze spending
- **AWS Trusted Advisor**: Automated best practice checks
- **CloudFormation Templates**: https://github.com/awslabs/aws-cloudformation-templates
- **AWS CDK Examples**: https://github.com/aws-samples/aws-cdk-examples
