# How to Use This Skill

Hey Claude—I just added the "aws-solution-architect" skill. Can you design a scalable serverless architecture for my startup?

## Example Invocations

**Example 1: Serverless Web Application**
```
Hey Claude—I just added the "aws-solution-architect" skill. Can you design a serverless architecture for a SaaS platform with 10k users, including API, database, and authentication?
```

**Example 2: Microservices Architecture**
```
Hey Claude—I just added the "aws-solution-architect" skill. Can you design an event-driven microservices architecture using Lambda, EventBridge, and DynamoDB for an e-commerce platform?
```

**Example 3: Cost Optimization**
```
Hey Claude—I just added the "aws-solution-architect" skill. Can you analyze my current AWS setup and recommend ways to reduce costs by 30%? I'm currently spending $2000/month.
```

**Example 4: Infrastructure as Code**
```
Hey Claude—I just added the "aws-solution-architect" skill. Can you generate a CloudFormation template for a three-tier web application with auto-scaling and RDS?
```

**Example 5: Mobile Backend**
```
Hey Claude—I just added the "aws-solution-architect" skill. Can you design a scalable mobile backend using AppSync GraphQL, Cognito, and DynamoDB?
```

**Example 6: Data Pipeline**
```
Hey Claude—I just added the "aws-solution-architect" skill. Can you design a real-time data processing pipeline using Kinesis for analytics on IoT sensor data?
```

## What to Provide

Depending on your needs, provide:

### For Architecture Design:
- **Application type**: Web app, mobile backend, data pipeline, microservices, SaaS
- **Expected scale**: Number of users, requests per second, data volume
- **Budget**: Monthly AWS spend limit or constraints
- **Team context**: Team size, AWS experience level
- **Requirements**: Authentication, real-time features, compliance needs (GDPR, HIPAA)
- **Geographic scope**: Single region, multi-region, global

### For Cost Optimization:
- **Current monthly spend**: Total AWS bill
- **Resource inventory**: List of EC2, RDS, S3, etc. resources
- **Utilization metrics**: CPU, memory, storage usage
- **Budget target**: Desired monthly spend or savings percentage

### For Infrastructure as Code:
- **Template type**: CloudFormation, CDK (TypeScript/Python), or Terraform
- **Services needed**: Compute, database, storage, networking
- **Environment**: dev, staging, production configurations

## What You'll Get

Based on your request, you'll receive:

### Architecture Designs:
- **Pattern recommendation** with service selection
- **Architecture diagram** description (visual representation)
- **Service configuration** details
- **Cost estimates** with monthly breakdown
- **Pros/cons** analysis
- **Scaling characteristics** and limitations

### Infrastructure as Code:
- **CloudFormation templates** (YAML) - production-ready
- **AWS CDK stacks** (TypeScript) - modern, type-safe
- **Terraform configurations** (HCL) - multi-cloud compatible
- **Deployment instructions** and prerequisites
- **Security best practices** built-in

### Cost Optimization:
- **Current spend analysis** by service
- **Specific recommendations** with savings potential
- **Priority actions** (high/medium/low)
- **Implementation checklist** with timelines
- **Long-term optimization** strategies

### Best Practices:
- **Security hardening** checklist
- **Scalability patterns** and anti-patterns
- **Monitoring setup** recommendations
- **Disaster recovery** procedures
- **Compliance guidance** (GDPR, HIPAA, SOC 2)

## Common Use Cases

### 1. MVP/Startup Launch
**Ask for:** "Serverless architecture for MVP with minimal costs"

**You'll get:**
- Amplify or Lambda + API Gateway + DynamoDB stack
- Cognito authentication setup
- S3 + CloudFront for frontend
- Cost estimate: $20-100/month
- Fast deployment (1-3 days)

### 2. Scaling Existing Application
**Ask for:** "Migrate from single server to scalable AWS architecture"

**You'll get:**
- Migration strategy (phased approach)
- Modern three-tier or containerized architecture
- Load balancing and auto-scaling configuration
- Database migration plan (DMS)
- Zero-downtime deployment strategy

### 3. Cost Reduction
**Ask for:** "Analyze and optimize my $5000/month AWS bill"

**You'll get:**
- Service-by-service cost breakdown
- Right-sizing recommendations
- Savings Plans/Reserved Instance opportunities
- Storage lifecycle optimizations
- Estimated savings: 20-40%

### 4. Compliance Requirements
**Ask for:** "HIPAA-compliant architecture for healthcare application"

**You'll get:**
- Compliant service selection (BAA-eligible only)
- Encryption configuration (at rest and in transit)
- Audit logging setup (CloudTrail, Config)
- Network isolation (VPC private subnets)
- Access control (IAM policies)

### 5. Global Deployment
**Ask for:** "Multi-region architecture for global users"

**You'll get:**
- Route 53 geolocation routing
- DynamoDB Global Tables or Aurora Global
- CloudFront edge caching
- Disaster recovery and failover
- Cross-region cost considerations

## Prerequisites

### For Using Generated Templates:

**AWS Account**:
- Active AWS account with appropriate permissions
- IAM user or role with admin access (for initial setup)
- Billing alerts enabled

**Tools Required**:
```bash
# AWS CLI
brew install awscli  # macOS
aws configure

# For CloudFormation
# (AWS CLI includes CloudFormation)

# For AWS CDK
npm install -g aws-cdk
cdk --version

# For Terraform
brew install terraform  # macOS
terraform --version
```

**Knowledge**:
- Basic AWS concepts (VPC, IAM, EC2, S3)
- Command line proficiency
- Git for version control

## Deployment Steps

### CloudFormation:
```bash
# Validate template
aws cloudformation validate-template --template-body file://template.yaml

# Deploy stack
aws cloudformation create-stack \
  --stack-name my-app-stack \
  --template-body file://template.yaml \
  --parameters ParameterKey=Environment,ParameterValue=dev \
  --capabilities CAPABILITY_IAM

# Monitor deployment
aws cloudformation describe-stacks --stack-name my-app-stack
```

### AWS CDK:
```bash
# Initialize project
cdk init app --language=typescript

# Install dependencies
npm install

# Deploy stack
cdk deploy

# View outputs
cdk outputs
```

### Terraform:
```bash
# Initialize
terraform init

# Plan deployment
terraform plan

# Apply changes
terraform apply

# View outputs
terraform output
```

## Best Practices Tips

### 1. Start Small, Scale Gradually
- Begin with serverless to minimize costs
- Add managed services as you grow
- Avoid over-engineering for hypothetical scale

### 2. Enable Monitoring from Day One
- Set up CloudWatch dashboards
- Configure alarms for critical metrics
- Enable AWS Cost Explorer
- Create budget alerts

### 3. Infrastructure as Code Always
- Version control all infrastructure
- Use separate accounts for dev/staging/prod
- Implement CI/CD for infrastructure changes
- Document architecture decisions

### 4. Security First
- Enable MFA on root and admin accounts
- Use IAM roles, never long-term credentials
- Encrypt everything (S3, RDS, EBS)
- Regular security audits (AWS Security Hub)

### 5. Cost Management
- Tag all resources for cost allocation
- Review bills weekly
- Delete unused resources promptly
- Use Savings Plans for predictable workloads

## Troubleshooting

### Common Issues:

**"Access Denied" errors:**
- Check IAM permissions for your user/role
- Ensure service-linked roles exist
- Verify resource policies (S3, KMS)

**High costs unexpectedly:**
- Check for undeleted resources (EC2, RDS snapshots)
- Review NAT Gateway data transfer
- Check CloudWatch Logs retention
- Look for unauthorized usage

**Deployment failures:**
- Validate templates before deploying
- Check service quotas (limits)
- Verify VPC/subnet configuration
- Review CloudFormation/Terraform error messages

**Performance issues:**
- Enable CloudWatch metrics and X-Ray
- Check database connection pooling
- Review Lambda cold starts (use provisioned concurrency)
- Optimize database queries and indexes

## Additional Resources

- **AWS Well-Architected Framework**: https://aws.amazon.com/architecture/well-architected/
- **AWS Architecture Center**: https://aws.amazon.com/architecture/
- **Serverless Land**: https://serverlessland.com/
- **AWS Pricing Calculator**: https://calculator.aws/
- **AWS Free Tier**: https://aws.amazon.com/free/
- **AWS Startups**: https://aws.amazon.com/startups/

## Tips for Best Results

1. **Be specific** about scale and budget constraints
2. **Mention team experience** level with AWS
3. **State compliance requirements** upfront (GDPR, HIPAA, etc.)
4. **Describe current setup** if migrating from existing infrastructure
5. **Ask for alternatives** if you need options to compare
6. **Request explanations** for WHY certain services are recommended
7. **Specify IaC preference** (CloudFormation, CDK, or Terraform)

## Support

For AWS-specific questions:
- AWS Support Plans (Developer, Business, Enterprise)
- AWS re:Post community forum
- AWS Documentation: https://docs.aws.amazon.com/
- AWS Training: https://aws.amazon.com/training/
