# Infrastructure as Code Guide

Reference for Terraform patterns, AWS/GCP modules, and IaC best practices.

---

## Table of Contents

- [Terraform Fundamentals](#terraform-fundamentals)
- [Module Patterns](#module-patterns)
- [AWS Infrastructure](#aws-infrastructure)
- [Kubernetes Resources](#kubernetes-resources)
- [State Management](#state-management)
- [Security Patterns](#security-patterns)

---

## Terraform Fundamentals

### Project Structure

```
infrastructure/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   │   └── ...
│   └── production/
│       └── ...
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── ecs/
│   │   └── ...
│   ├── rds/
│   │   └── ...
│   └── s3/
│       └── ...
└── shared/
    ├── backend.tf
    └── providers.tf
```

### Provider Configuration

```hcl
# providers.tf
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      Project     = var.project_name
      ManagedBy   = "terraform"
    }
  }
}
```

### Backend Configuration

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "env/${var.environment}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

---

## Module Patterns

### VPC Module

```hcl
# modules/vpc/main.tf
variable "name" {
  type        = string
  description = "VPC name"
}

variable "cidr" {
  type        = string
  default     = "10.0.0.0/16"
  description = "VPC CIDR block"
}

variable "azs" {
  type        = list(string)
  description = "Availability zones"
}

variable "private_subnets" {
  type        = list(string)
  description = "Private subnet CIDR blocks"
}

variable "public_subnets" {
  type        = list(string)
  description = "Public subnet CIDR blocks"
}

variable "enable_nat_gateway" {
  type        = bool
  default     = true
  description = "Enable NAT Gateway for private subnets"
}

resource "aws_vpc" "main" {
  cidr_block           = var.cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = var.name
  }
}

resource "aws_subnet" "private" {
  count             = length(var.private_subnets)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnets[count.index]
  availability_zone = var.azs[count.index]

  tags = {
    Name = "${var.name}-private-${var.azs[count.index]}"
    Type = "private"
  }
}

resource "aws_subnet" "public" {
  count                   = length(var.public_subnets)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnets[count.index]
  availability_zone       = var.azs[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.name}-public-${var.azs[count.index]}"
    Type = "public"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.name}-igw"
  }
}

resource "aws_eip" "nat" {
  count  = var.enable_nat_gateway ? 1 : 0
  domain = "vpc"

  tags = {
    Name = "${var.name}-nat-eip"
  }
}

resource "aws_nat_gateway" "main" {
  count         = var.enable_nat_gateway ? 1 : 0
  allocation_id = aws_eip.nat[0].id
  subnet_id     = aws_subnet.public[0].id

  tags = {
    Name = "${var.name}-nat"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.name}-public-rt"
  }
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  dynamic "route" {
    for_each = var.enable_nat_gateway ? [1] : []
    content {
      cidr_block     = "0.0.0.0/0"
      nat_gateway_id = aws_nat_gateway.main[0].id
    }
  }

  tags = {
    Name = "${var.name}-private-rt"
  }
}

resource "aws_route_table_association" "public" {
  count          = length(var.public_subnets)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count          = length(var.private_subnets)
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}

output "vpc_id" {
  value = aws_vpc.main.id
}

output "private_subnet_ids" {
  value = aws_subnet.private[*].id
}

output "public_subnet_ids" {
  value = aws_subnet.public[*].id
}
```

### ECS Service Module

```hcl
# modules/ecs/main.tf
variable "name" {
  type        = string
  description = "Service name"
}

variable "cluster_id" {
  type        = string
  description = "ECS cluster ID"
}

variable "image" {
  type        = string
  description = "Container image"
}

variable "cpu" {
  type        = number
  default     = 256
  description = "Task CPU units"
}

variable "memory" {
  type        = number
  default     = 512
  description = "Task memory (MB)"
}

variable "desired_count" {
  type        = number
  default     = 2
  description = "Desired task count"
}

variable "subnet_ids" {
  type        = list(string)
  description = "Subnet IDs for tasks"
}

variable "security_group_ids" {
  type        = list(string)
  description = "Security group IDs"
}

variable "target_group_arn" {
  type        = string
  description = "ALB target group ARN"
}

variable "container_port" {
  type        = number
  default     = 3000
  description = "Container port"
}

variable "environment_variables" {
  type        = map(string)
  default     = {}
  description = "Environment variables"
}

variable "secrets" {
  type        = map(string)
  default     = {}
  description = "Secrets from Parameter Store/Secrets Manager"
}

resource "aws_ecs_task_definition" "main" {
  family                   = var.name
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.cpu
  memory                   = var.memory
  execution_role_arn       = aws_iam_role.execution.arn
  task_role_arn            = aws_iam_role.task.arn

  container_definitions = jsonencode([
    {
      name  = var.name
      image = var.image

      portMappings = [
        {
          containerPort = var.container_port
          protocol      = "tcp"
        }
      ]

      environment = [
        for key, value in var.environment_variables : {
          name  = key
          value = value
        }
      ]

      secrets = [
        for key, arn in var.secrets : {
          name      = key
          valueFrom = arn
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.main.name
          awslogs-region        = data.aws_region.current.name
          awslogs-stream-prefix = "ecs"
        }
      }

      healthCheck = {
        command     = ["CMD-SHELL", "curl -f http://localhost:${var.container_port}/health || exit 1"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 60
      }
    }
  ])
}

resource "aws_ecs_service" "main" {
  name            = var.name
  cluster         = var.cluster_id
  task_definition = aws_ecs_task_definition.main.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.subnet_ids
    security_groups  = var.security_group_ids
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = var.target_group_arn
    container_name   = var.name
    container_port   = var.container_port
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  deployment_configuration {
    minimum_healthy_percent = 50
    maximum_percent         = 200
  }

  lifecycle {
    ignore_changes = [desired_count]
  }
}

resource "aws_cloudwatch_log_group" "main" {
  name              = "/ecs/${var.name}"
  retention_in_days = 30
}

resource "aws_appautoscaling_target" "main" {
  max_capacity       = 10
  min_capacity       = var.desired_count
  resource_id        = "service/${var.cluster_id}/${aws_ecs_service.main.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "cpu" {
  name               = "${var.name}-cpu-autoscaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.main.resource_id
  scalable_dimension = aws_appautoscaling_target.main.scalable_dimension
  service_namespace  = aws_appautoscaling_target.main.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value       = 70.0
    scale_in_cooldown  = 300
    scale_out_cooldown = 60
  }
}

data "aws_region" "current" {}
```

### RDS Module

```hcl
# modules/rds/main.tf
variable "name" {
  type        = string
  description = "Database identifier"
}

variable "engine_version" {
  type        = string
  default     = "15.4"
  description = "PostgreSQL version"
}

variable "instance_class" {
  type        = string
  default     = "db.t3.micro"
  description = "Instance class"
}

variable "allocated_storage" {
  type        = number
  default     = 20
  description = "Storage in GB"
}

variable "database_name" {
  type        = string
  description = "Initial database name"
}

variable "master_username" {
  type        = string
  default     = "postgres"
  description = "Master username"
}

variable "vpc_id" {
  type        = string
  description = "VPC ID"
}

variable "subnet_ids" {
  type        = list(string)
  description = "Subnet IDs for DB subnet group"
}

variable "allowed_security_groups" {
  type        = list(string)
  description = "Security groups allowed to access DB"
}

resource "random_password" "master" {
  length  = 32
  special = false
}

resource "aws_secretsmanager_secret" "db_credentials" {
  name = "${var.name}-db-credentials"
}

resource "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = aws_secretsmanager_secret.db_credentials.id
  secret_string = jsonencode({
    username = var.master_username
    password = random_password.master.result
    host     = aws_db_instance.main.address
    port     = aws_db_instance.main.port
    dbname   = var.database_name
  })
}

resource "aws_db_subnet_group" "main" {
  name       = var.name
  subnet_ids = var.subnet_ids

  tags = {
    Name = var.name
  }
}

resource "aws_security_group" "db" {
  name        = "${var.name}-db"
  description = "Security group for RDS"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = var.allowed_security_groups
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.name}-db"
  }
}

resource "aws_db_instance" "main" {
  identifier = var.name

  engine         = "postgres"
  engine_version = var.engine_version
  instance_class = var.instance_class

  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.allocated_storage * 5
  storage_encrypted     = true

  db_name  = var.database_name
  username = var.master_username
  password = random_password.master.result

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db.id]

  backup_retention_period = 7
  backup_window           = "03:00-04:00"
  maintenance_window      = "Mon:04:00-Mon:05:00"

  deletion_protection = true
  skip_final_snapshot = false

  performance_insights_enabled = true

  tags = {
    Name = var.name
  }
}

output "endpoint" {
  value = aws_db_instance.main.endpoint
}

output "secret_arn" {
  value = aws_secretsmanager_secret.db_credentials.arn
}
```

---

## AWS Infrastructure

### Complete Environment

```hcl
# environments/production/main.tf
module "vpc" {
  source = "../../modules/vpc"

  name = "${var.project_name}-${var.environment}"
  cidr = "10.0.0.0/16"
  azs  = ["us-east-1a", "us-east-1b", "us-east-1c"]

  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
}

module "alb" {
  source = "../../modules/alb"

  name               = "${var.project_name}-${var.environment}"
  vpc_id             = module.vpc.vpc_id
  subnet_ids         = module.vpc.public_subnet_ids
  certificate_arn    = var.certificate_arn
  health_check_path  = "/health"
}

module "ecs_cluster" {
  source = "../../modules/ecs-cluster"

  name = "${var.project_name}-${var.environment}"
}

module "api" {
  source = "../../modules/ecs"

  name       = "api"
  cluster_id = module.ecs_cluster.id
  image      = "${var.ecr_repository}:${var.image_tag}"

  cpu    = 512
  memory = 1024
  desired_count = 3

  subnet_ids         = module.vpc.private_subnet_ids
  security_group_ids = [module.api_sg.id]
  target_group_arn   = module.alb.target_group_arn

  environment_variables = {
    NODE_ENV = "production"
    PORT     = "3000"
  }

  secrets = {
    DATABASE_URL = module.rds.secret_arn
    JWT_SECRET   = var.jwt_secret_arn
  }
}

module "rds" {
  source = "../../modules/rds"

  name          = "${var.project_name}-${var.environment}"
  database_name = "app"

  instance_class    = "db.t3.small"
  allocated_storage = 50

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids

  allowed_security_groups = [module.api_sg.id]
}
```

---

## Kubernetes Resources

### Deployment Pattern

```hcl
# modules/k8s-deployment/main.tf
resource "kubernetes_deployment" "main" {
  metadata {
    name      = var.name
    namespace = var.namespace
    labels = {
      app = var.name
    }
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        app = var.name
      }
    }

    template {
      metadata {
        labels = {
          app = var.name
        }
      }

      spec {
        container {
          name  = var.name
          image = var.image

          port {
            container_port = var.port
          }

          resources {
            limits = {
              cpu    = var.cpu_limit
              memory = var.memory_limit
            }
            requests = {
              cpu    = var.cpu_request
              memory = var.memory_request
            }
          }

          liveness_probe {
            http_get {
              path = "/health"
              port = var.port
            }
            initial_delay_seconds = 30
            period_seconds        = 10
          }

          readiness_probe {
            http_get {
              path = "/ready"
              port = var.port
            }
            initial_delay_seconds = 5
            period_seconds        = 5
          }

          dynamic "env" {
            for_each = var.environment_variables
            content {
              name  = env.key
              value = env.value
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "main" {
  metadata {
    name      = var.name
    namespace = var.namespace
  }

  spec {
    selector = {
      app = var.name
    }

    port {
      port        = 80
      target_port = var.port
    }

    type = "ClusterIP"
  }
}

resource "kubernetes_horizontal_pod_autoscaler" "main" {
  metadata {
    name      = var.name
    namespace = var.namespace
  }

  spec {
    scale_target_ref {
      api_version = "apps/v1"
      kind        = "Deployment"
      name        = kubernetes_deployment.main.metadata[0].name
    }

    min_replicas = var.min_replicas
    max_replicas = var.max_replicas

    metric {
      type = "Resource"
      resource {
        name = "cpu"
        target {
          type                = "Utilization"
          average_utilization = 70
        }
      }
    }
  }
}
```

---

## State Management

### Remote State Setup

```hcl
# Create state bucket (run once)
resource "aws_s3_bucket" "terraform_state" {
  bucket = "company-terraform-state"

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
```

---

## Security Patterns

### Least Privilege IAM

```hcl
# ECS task execution role
resource "aws_iam_role" "ecs_execution" {
  name = "${var.name}-ecs-execution"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_execution" {
  role       = aws_iam_role.ecs_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Allow reading specific secrets
resource "aws_iam_role_policy" "secrets_access" {
  name = "secrets-access"
  role = aws_iam_role.ecs_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = var.secret_arns
      }
    ]
  })
}
```

---

*See also: `deployment_strategies.md` for release patterns*
