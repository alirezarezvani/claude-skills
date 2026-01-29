#!/usr/bin/env python3
"""
Terraform Scaffolder - Generate production-ready Terraform module templates.

Table of Contents:
    TerraformScaffolder - Main class for Terraform scaffolding
        __init__         - Initialize with output path and options
        scaffold()       - Generate complete Terraform project structure
        _create_structure() - Create directory layout
        _generate_main_tf() - Generate main.tf with provider config
        _generate_variables_tf() - Generate variables.tf
        _generate_outputs_tf() - Generate outputs.tf
        _generate_versions_tf() - Generate versions.tf with constraints
        _generate_vpc_module() - Generate VPC module
        _generate_ecs_module() - Generate ECS Fargate module
        _generate_rds_module() - Generate RDS PostgreSQL module
        _generate_environments() - Generate environment tfvars
        _generate_backend_config() - Generate S3 backend configuration
    main() - CLI entry point

Usage:
    python terraform_scaffolder.py /path/to/output --project myapp
    python terraform_scaffolder.py /path/to/output --project myapp --modules vpc,ecs,rds
    python terraform_scaffolder.py /path/to/output --project myapp --environments dev,staging,prod
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class TerraformScaffolder:
    """Generate production-ready Terraform module templates."""

    def __init__(
        self,
        output_path: str,
        project_name: str = "myproject",
        modules: Optional[List[str]] = None,
        environments: Optional[List[str]] = None,
        aws_region: str = "us-east-1",
        verbose: bool = False
    ):
        """
        Initialize the Terraform scaffolder.

        Args:
            output_path: Directory where Terraform files will be created
            project_name: Name of the project (used for resource naming)
            modules: List of modules to generate (vpc, ecs, rds)
            environments: List of environments (dev, staging, prod)
            aws_region: Default AWS region
            verbose: Enable verbose output
        """
        self.output_path = Path(output_path)
        self.project_name = project_name
        self.modules = modules or ["vpc", "ecs", "rds"]
        self.environments = environments or ["dev", "staging", "prod"]
        self.aws_region = aws_region
        self.verbose = verbose
        self.created_files = []

    def scaffold(self) -> Dict:
        """
        Generate complete Terraform project structure.

        Returns:
            Dict with status, created files, and project info
        """
        print(f"Scaffolding Terraform project: {self.project_name}")
        print(f"Output directory: {self.output_path}")
        print(f"Modules: {', '.join(self.modules)}")
        print(f"Environments: {', '.join(self.environments)}")
        print()

        try:
            self._create_structure()
            self._generate_main_tf()
            self._generate_variables_tf()
            self._generate_outputs_tf()
            self._generate_versions_tf()
            self._generate_backend_config()

            # Generate selected modules
            if "vpc" in self.modules:
                self._generate_vpc_module()
            if "ecs" in self.modules:
                self._generate_ecs_module()
            if "rds" in self.modules:
                self._generate_rds_module()

            # Generate environment configurations
            self._generate_environments()

            # Generate .gitignore
            self._generate_gitignore()

            print(f"\nCreated {len(self.created_files)} files:")
            for f in self.created_files:
                print(f"  - {f}")

            return {
                "status": "success",
                "project_name": self.project_name,
                "output_path": str(self.output_path),
                "modules": self.modules,
                "environments": self.environments,
                "files_created": self.created_files
            }

        except Exception as e:
            print(f"Error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    def _create_structure(self):
        """Create directory layout for Terraform project."""
        dirs = [
            self.output_path,
            self.output_path / "modules",
            self.output_path / "environments",
        ]

        for module in self.modules:
            dirs.append(self.output_path / "modules" / module)

        for env in self.environments:
            dirs.append(self.output_path / "environments" / env)

        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
            if self.verbose:
                print(f"Created directory: {d}")

    def _write_file(self, path: Path, content: str):
        """Write content to file and track it."""
        path.write_text(content)
        rel_path = str(path.relative_to(self.output_path))
        self.created_files.append(rel_path)
        if self.verbose:
            print(f"Created file: {rel_path}")

    def _generate_main_tf(self):
        """Generate main.tf with provider configuration and module calls."""
        module_calls = []

        if "vpc" in self.modules:
            module_calls.append('''
module "vpc" {
  source = "./modules/vpc"

  project_name    = var.project_name
  environment     = var.environment
  vpc_cidr        = var.vpc_cidr
  azs             = var.availability_zones
  private_subnets = var.private_subnet_cidrs
  public_subnets  = var.public_subnet_cidrs

  tags = local.common_tags
}''')

        if "ecs" in self.modules:
            module_calls.append('''
module "ecs" {
  source = "./modules/ecs"

  project_name       = var.project_name
  environment        = var.environment
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  public_subnet_ids  = module.vpc.public_subnet_ids

  container_image    = var.container_image
  container_port     = var.container_port
  cpu                = var.ecs_cpu
  memory             = var.ecs_memory
  desired_count      = var.ecs_desired_count

  tags = local.common_tags

  depends_on = [module.vpc]
}''')

        if "rds" in self.modules:
            module_calls.append('''
module "rds" {
  source = "./modules/rds"

  project_name       = var.project_name
  environment        = var.environment
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids

  db_name            = var.db_name
  db_username        = var.db_username
  instance_class     = var.db_instance_class
  allocated_storage  = var.db_allocated_storage
  engine_version     = var.db_engine_version

  allowed_security_groups = [module.ecs.ecs_security_group_id]

  tags = local.common_tags

  depends_on = [module.vpc]
}''')

        content = f'''# {self.project_name} - Main Terraform Configuration
# Generated by Terraform Scaffolder on {datetime.now().strftime("%Y-%m-%d")}

# -----------------------------------------------------------------------------
# Provider Configuration
# -----------------------------------------------------------------------------

provider "aws" {{
  region = var.aws_region

  default_tags {{
    tags = {{
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
    }}
  }}
}}

# -----------------------------------------------------------------------------
# Local Values
# -----------------------------------------------------------------------------

locals {{
  common_tags = {{
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }}
}}

# -----------------------------------------------------------------------------
# Data Sources
# -----------------------------------------------------------------------------

data "aws_caller_identity" "current" {{}}

data "aws_region" "current" {{}}

# -----------------------------------------------------------------------------
# Module Calls
# -----------------------------------------------------------------------------
{''.join(module_calls)}
'''
        self._write_file(self.output_path / "main.tf", content)

    def _generate_variables_tf(self):
        """Generate variables.tf with all required variables."""
        content = f'''# {self.project_name} - Variables
# Generated by Terraform Scaffolder

# -----------------------------------------------------------------------------
# General Variables
# -----------------------------------------------------------------------------

variable "project_name" {{
  description = "Name of the project"
  type        = string
  default     = "{self.project_name}"
}}

variable "environment" {{
  description = "Environment name (dev, staging, prod)"
  type        = string
}}

variable "aws_region" {{
  description = "AWS region"
  type        = string
  default     = "{self.aws_region}"
}}

# -----------------------------------------------------------------------------
# VPC Variables
# -----------------------------------------------------------------------------

variable "vpc_cidr" {{
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}}

variable "availability_zones" {{
  description = "List of availability zones"
  type        = list(string)
  default     = ["{self.aws_region}a", "{self.aws_region}b", "{self.aws_region}c"]
}}

variable "private_subnet_cidrs" {{
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}}

variable "public_subnet_cidrs" {{
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
}}

# -----------------------------------------------------------------------------
# ECS Variables
# -----------------------------------------------------------------------------

variable "container_image" {{
  description = "Docker image for the ECS task"
  type        = string
}}

variable "container_port" {{
  description = "Port the container listens on"
  type        = number
  default     = 8080
}}

variable "ecs_cpu" {{
  description = "CPU units for the ECS task"
  type        = number
  default     = 256
}}

variable "ecs_memory" {{
  description = "Memory (MB) for the ECS task"
  type        = number
  default     = 512
}}

variable "ecs_desired_count" {{
  description = "Desired number of ECS tasks"
  type        = number
  default     = 2
}}

# -----------------------------------------------------------------------------
# RDS Variables
# -----------------------------------------------------------------------------

variable "db_name" {{
  description = "Name of the database"
  type        = string
  default     = "{self.project_name.replace('-', '_')}_db"
}}

variable "db_username" {{
  description = "Database master username"
  type        = string
  default     = "admin"
  sensitive   = true
}}

variable "db_instance_class" {{
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}}

variable "db_allocated_storage" {{
  description = "Allocated storage in GB"
  type        = number
  default     = 20
}}

variable "db_engine_version" {{
  description = "PostgreSQL engine version"
  type        = string
  default     = "15.4"
}}
'''
        self._write_file(self.output_path / "variables.tf", content)

    def _generate_outputs_tf(self):
        """Generate outputs.tf with useful output values."""
        outputs = []

        if "vpc" in self.modules:
            outputs.append('''
# VPC Outputs
output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

output "private_subnet_ids" {
  description = "IDs of private subnets"
  value       = module.vpc.private_subnet_ids
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = module.vpc.public_subnet_ids
}''')

        if "ecs" in self.modules:
            outputs.append('''
# ECS Outputs
output "ecs_cluster_id" {
  description = "ID of the ECS cluster"
  value       = module.ecs.cluster_id
}

output "ecs_service_name" {
  description = "Name of the ECS service"
  value       = module.ecs.service_name
}

output "alb_dns_name" {
  description = "DNS name of the load balancer"
  value       = module.ecs.alb_dns_name
}''')

        if "rds" in self.modules:
            outputs.append('''
# RDS Outputs
output "rds_endpoint" {
  description = "RDS instance endpoint"
  value       = module.rds.endpoint
}

output "rds_port" {
  description = "RDS instance port"
  value       = module.rds.port
}''')

        content = f'''# {self.project_name} - Outputs
# Generated by Terraform Scaffolder
{''.join(outputs)}
'''
        self._write_file(self.output_path / "outputs.tf", content)

    def _generate_versions_tf(self):
        """Generate versions.tf with provider version constraints."""
        content = f'''# {self.project_name} - Terraform Version Constraints
# Generated by Terraform Scaffolder

terraform {{
  required_version = ">= 1.5.0"

  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }}
  }}
}}
'''
        self._write_file(self.output_path / "versions.tf", content)

    def _generate_backend_config(self):
        """Generate backend configuration for S3 state storage."""
        content = f'''# {self.project_name} - Backend Configuration
# Generated by Terraform Scaffolder
#
# Uncomment and configure for remote state storage:

# terraform {{
#   backend "s3" {{
#     bucket         = "{self.project_name}-terraform-state"
#     key            = "state/terraform.tfstate"
#     region         = "{self.aws_region}"
#     encrypt        = true
#     dynamodb_table = "{self.project_name}-terraform-locks"
#   }}
# }}
'''
        self._write_file(self.output_path / "backend.tf", content)

    def _generate_vpc_module(self):
        """Generate VPC module with public and private subnets."""
        module_path = self.output_path / "modules" / "vpc"

        # main.tf
        main_content = '''# VPC Module - Main Configuration

# -----------------------------------------------------------------------------
# VPC
# -----------------------------------------------------------------------------

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-vpc"
  })
}

# -----------------------------------------------------------------------------
# Internet Gateway
# -----------------------------------------------------------------------------

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-igw"
  })
}

# -----------------------------------------------------------------------------
# Public Subnets
# -----------------------------------------------------------------------------

resource "aws_subnet" "public" {
  count = length(var.public_subnets)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnets[count.index]
  availability_zone       = var.azs[count.index]
  map_public_ip_on_launch = true

  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-public-${var.azs[count.index]}"
    Tier = "public"
  })
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-public-rt"
  })
}

resource "aws_route_table_association" "public" {
  count = length(aws_subnet.public)

  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# -----------------------------------------------------------------------------
# NAT Gateway (for private subnet internet access)
# -----------------------------------------------------------------------------

resource "aws_eip" "nat" {
  count  = length(var.azs)
  domain = "vpc"

  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-nat-eip-${count.index + 1}"
  })

  depends_on = [aws_internet_gateway.main]
}

resource "aws_nat_gateway" "main" {
  count = length(var.azs)

  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-nat-${count.index + 1}"
  })

  depends_on = [aws_internet_gateway.main]
}

# -----------------------------------------------------------------------------
# Private Subnets
# -----------------------------------------------------------------------------

resource "aws_subnet" "private" {
  count = length(var.private_subnets)

  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnets[count.index]
  availability_zone = var.azs[count.index]

  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-private-${var.azs[count.index]}"
    Tier = "private"
  })
}

resource "aws_route_table" "private" {
  count = length(var.private_subnets)

  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[count.index].id
  }

  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-private-rt-${count.index + 1}"
  })
}

resource "aws_route_table_association" "private" {
  count = length(aws_subnet.private)

  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}
'''
        self._write_file(module_path / "main.tf", main_content)

        # variables.tf
        variables_content = '''# VPC Module - Variables

variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "azs" {
  description = "Availability zones"
  type        = list(string)
}

variable "private_subnets" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
}

variable "public_subnets" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
'''
        self._write_file(module_path / "variables.tf", variables_content)

        # outputs.tf
        outputs_content = '''# VPC Module - Outputs

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "private_subnet_ids" {
  description = "IDs of private subnets"
  value       = aws_subnet.private[*].id
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = aws_subnet.public[*].id
}

output "nat_gateway_ips" {
  description = "Public IPs of NAT gateways"
  value       = aws_eip.nat[*].public_ip
}

output "internet_gateway_id" {
  description = "ID of the internet gateway"
  value       = aws_internet_gateway.main.id
}
'''
        self._write_file(module_path / "outputs.tf", outputs_content)

    def _generate_ecs_module(self):
        """Generate ECS Fargate module with ALB."""
        module_path = self.output_path / "modules" / "ecs"

        # main.tf
        main_content = '''# ECS Module - Main Configuration

# -----------------------------------------------------------------------------
# ECS Cluster
# -----------------------------------------------------------------------------

resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-${var.environment}"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = var.tags
}

# -----------------------------------------------------------------------------
# Application Load Balancer
# -----------------------------------------------------------------------------

resource "aws_security_group" "alb" {
  name        = "${var.project_name}-${var.environment}-alb-sg"
  description = "Security group for ALB"
  vpc_id      = var.vpc_id

  ingress {
    description = "HTTP from internet"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS from internet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-alb-sg"
  })
}

resource "aws_lb" "main" {
  name               = "${var.project_name}-${var.environment}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.public_subnet_ids

  enable_deletion_protection = var.environment == "prod" ? true : false

  tags = var.tags
}

resource "aws_lb_target_group" "app" {
  name        = "${var.project_name}-${var.environment}-tg"
  port        = var.container_port
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200-399"
    path                = "/health"
    port                = "traffic-port"
    timeout             = 5
    unhealthy_threshold = 3
  }

  tags = var.tags
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

# -----------------------------------------------------------------------------
# ECS Task Security Group
# -----------------------------------------------------------------------------

resource "aws_security_group" "ecs_tasks" {
  name        = "${var.project_name}-${var.environment}-ecs-sg"
  description = "Security group for ECS tasks"
  vpc_id      = var.vpc_id

  ingress {
    description     = "Traffic from ALB"
    from_port       = var.container_port
    to_port         = var.container_port
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-ecs-sg"
  })
}

# -----------------------------------------------------------------------------
# IAM Roles
# -----------------------------------------------------------------------------

resource "aws_iam_role" "ecs_execution" {
  name = "${var.project_name}-${var.environment}-ecs-execution"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "ecs_execution" {
  role       = aws_iam_role.ecs_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role" "ecs_task" {
  name = "${var.project_name}-${var.environment}-ecs-task"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })

  tags = var.tags
}

# -----------------------------------------------------------------------------
# CloudWatch Log Group
# -----------------------------------------------------------------------------

resource "aws_cloudwatch_log_group" "app" {
  name              = "/ecs/${var.project_name}-${var.environment}"
  retention_in_days = 30

  tags = var.tags
}

# -----------------------------------------------------------------------------
# ECS Task Definition
# -----------------------------------------------------------------------------

resource "aws_ecs_task_definition" "app" {
  family                   = "${var.project_name}-${var.environment}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.cpu
  memory                   = var.memory
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([{
    name  = "app"
    image = var.container_image

    portMappings = [{
      containerPort = var.container_port
      hostPort      = var.container_port
      protocol      = "tcp"
    }]

    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.app.name
        "awslogs-region"        = data.aws_region.current.name
        "awslogs-stream-prefix" = "ecs"
      }
    }

    environment = [
      { name = "PORT", value = tostring(var.container_port) },
      { name = "ENVIRONMENT", value = var.environment }
    ]

    essential = true
  }])

  tags = var.tags
}

data "aws_region" "current" {}

# -----------------------------------------------------------------------------
# ECS Service
# -----------------------------------------------------------------------------

resource "aws_ecs_service" "app" {
  name            = "${var.project_name}-${var.environment}"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.ecs_tasks.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "app"
    container_port   = var.container_port
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  tags = var.tags

  lifecycle {
    ignore_changes = [desired_count]
  }
}
'''
        self._write_file(module_path / "main.tf", main_content)

        # variables.tf
        variables_content = '''# ECS Module - Variables

variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "vpc_id" {
  description = "ID of the VPC"
  type        = string
}

variable "private_subnet_ids" {
  description = "IDs of private subnets"
  type        = list(string)
}

variable "public_subnet_ids" {
  description = "IDs of public subnets"
  type        = list(string)
}

variable "container_image" {
  description = "Docker image for the ECS task"
  type        = string
}

variable "container_port" {
  description = "Port the container listens on"
  type        = number
  default     = 8080
}

variable "cpu" {
  description = "CPU units for the ECS task"
  type        = number
  default     = 256
}

variable "memory" {
  description = "Memory (MB) for the ECS task"
  type        = number
  default     = 512
}

variable "desired_count" {
  description = "Desired number of ECS tasks"
  type        = number
  default     = 2
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
'''
        self._write_file(module_path / "variables.tf", variables_content)

        # outputs.tf
        outputs_content = '''# ECS Module - Outputs

output "cluster_id" {
  description = "ID of the ECS cluster"
  value       = aws_ecs_cluster.main.id
}

output "cluster_name" {
  description = "Name of the ECS cluster"
  value       = aws_ecs_cluster.main.name
}

output "service_name" {
  description = "Name of the ECS service"
  value       = aws_ecs_service.app.name
}

output "alb_dns_name" {
  description = "DNS name of the load balancer"
  value       = aws_lb.main.dns_name
}

output "alb_arn" {
  description = "ARN of the load balancer"
  value       = aws_lb.main.arn
}

output "target_group_arn" {
  description = "ARN of the target group"
  value       = aws_lb_target_group.app.arn
}

output "ecs_security_group_id" {
  description = "ID of the ECS tasks security group"
  value       = aws_security_group.ecs_tasks.id
}
'''
        self._write_file(module_path / "outputs.tf", outputs_content)

    def _generate_rds_module(self):
        """Generate RDS PostgreSQL module."""
        module_path = self.output_path / "modules" / "rds"

        # main.tf
        main_content = '''# RDS Module - Main Configuration

# -----------------------------------------------------------------------------
# DB Subnet Group
# -----------------------------------------------------------------------------

resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-${var.environment}"
  subnet_ids = var.private_subnet_ids

  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-db-subnet-group"
  })
}

# -----------------------------------------------------------------------------
# Security Group
# -----------------------------------------------------------------------------

resource "aws_security_group" "rds" {
  name        = "${var.project_name}-${var.environment}-rds-sg"
  description = "Security group for RDS"
  vpc_id      = var.vpc_id

  ingress {
    description     = "PostgreSQL from allowed security groups"
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

  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-rds-sg"
  })
}

# -----------------------------------------------------------------------------
# RDS Parameter Group
# -----------------------------------------------------------------------------

resource "aws_db_parameter_group" "main" {
  name   = "${var.project_name}-${var.environment}-pg15"
  family = "postgres15"

  parameter {
    name  = "log_statement"
    value = "all"
  }

  parameter {
    name  = "log_min_duration_statement"
    value = "1000"
  }

  tags = var.tags
}

# -----------------------------------------------------------------------------
# Random Password for DB
# -----------------------------------------------------------------------------

resource "random_password" "db_password" {
  length  = 32
  special = false
}

# -----------------------------------------------------------------------------
# Secrets Manager for DB Credentials
# -----------------------------------------------------------------------------

resource "aws_secretsmanager_secret" "db_credentials" {
  name = "${var.project_name}-${var.environment}-db-credentials"

  tags = var.tags
}

resource "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = aws_secretsmanager_secret.db_credentials.id
  secret_string = jsonencode({
    username = var.db_username
    password = random_password.db_password.result
    host     = aws_db_instance.main.address
    port     = aws_db_instance.main.port
    database = var.db_name
  })
}

# -----------------------------------------------------------------------------
# RDS Instance
# -----------------------------------------------------------------------------

resource "aws_db_instance" "main" {
  identifier = "${var.project_name}-${var.environment}"

  engine         = "postgres"
  engine_version = var.engine_version
  instance_class = var.instance_class

  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.allocated_storage * 2
  storage_type          = "gp3"
  storage_encrypted     = true

  db_name  = var.db_name
  username = var.db_username
  password = random_password.db_password.result

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  parameter_group_name   = aws_db_parameter_group.main.name

  multi_az               = var.environment == "prod" ? true : false
  publicly_accessible    = false
  deletion_protection    = var.environment == "prod" ? true : false
  skip_final_snapshot    = var.environment != "prod"
  final_snapshot_identifier = var.environment == "prod" ? "${var.project_name}-${var.environment}-final" : null

  backup_retention_period = var.environment == "prod" ? 30 : 7
  backup_window           = "03:00-04:00"
  maintenance_window      = "Mon:04:00-Mon:05:00"

  performance_insights_enabled          = true
  performance_insights_retention_period = 7

  tags = var.tags
}
'''
        self._write_file(module_path / "main.tf", main_content)

        # variables.tf
        variables_content = '''# RDS Module - Variables

variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "vpc_id" {
  description = "ID of the VPC"
  type        = string
}

variable "private_subnet_ids" {
  description = "IDs of private subnets"
  type        = list(string)
}

variable "db_name" {
  description = "Name of the database"
  type        = string
}

variable "db_username" {
  description = "Database master username"
  type        = string
  sensitive   = true
}

variable "instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "allocated_storage" {
  description = "Allocated storage in GB"
  type        = number
  default     = 20
}

variable "engine_version" {
  description = "PostgreSQL engine version"
  type        = string
  default     = "15.4"
}

variable "allowed_security_groups" {
  description = "Security groups allowed to connect to RDS"
  type        = list(string)
  default     = []
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
'''
        self._write_file(module_path / "variables.tf", variables_content)

        # outputs.tf
        outputs_content = '''# RDS Module - Outputs

output "endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.main.address
}

output "port" {
  description = "RDS instance port"
  value       = aws_db_instance.main.port
}

output "db_name" {
  description = "Database name"
  value       = aws_db_instance.main.db_name
}

output "credentials_secret_arn" {
  description = "ARN of the Secrets Manager secret with DB credentials"
  value       = aws_secretsmanager_secret.db_credentials.arn
}

output "security_group_id" {
  description = "ID of the RDS security group"
  value       = aws_security_group.rds.id
}
'''
        self._write_file(module_path / "outputs.tf", outputs_content)

    def _generate_environments(self):
        """Generate environment-specific tfvars files."""
        env_configs = {
            "dev": {
                "vpc_cidr": "10.0.0.0/16",
                "ecs_cpu": 256,
                "ecs_memory": 512,
                "ecs_desired_count": 1,
                "db_instance_class": "db.t3.micro",
                "db_allocated_storage": 20
            },
            "staging": {
                "vpc_cidr": "10.1.0.0/16",
                "ecs_cpu": 512,
                "ecs_memory": 1024,
                "ecs_desired_count": 2,
                "db_instance_class": "db.t3.small",
                "db_allocated_storage": 50
            },
            "prod": {
                "vpc_cidr": "10.2.0.0/16",
                "ecs_cpu": 1024,
                "ecs_memory": 2048,
                "ecs_desired_count": 3,
                "db_instance_class": "db.r6g.large",
                "db_allocated_storage": 100
            }
        }

        for env in self.environments:
            config = env_configs.get(env, env_configs["dev"])

            content = f'''# {self.project_name} - {env.upper()} Environment Configuration
# Generated by Terraform Scaffolder

environment = "{env}"

# VPC Configuration
vpc_cidr = "{config['vpc_cidr']}"

# ECS Configuration
container_image   = "your-registry/{self.project_name}:latest"
container_port    = 8080
ecs_cpu           = {config['ecs_cpu']}
ecs_memory        = {config['ecs_memory']}
ecs_desired_count = {config['ecs_desired_count']}

# RDS Configuration
db_instance_class    = "{config['db_instance_class']}"
db_allocated_storage = {config['db_allocated_storage']}
'''
            env_path = self.output_path / "environments" / env
            self._write_file(env_path / "terraform.tfvars", content)

            # Create backend config for each environment
            backend_content = f'''# Backend configuration for {env}
# Run: terraform init -backend-config=environments/{env}/backend.tfvars

bucket         = "{self.project_name}-terraform-state"
key            = "{env}/terraform.tfstate"
region         = "{self.aws_region}"
encrypt        = true
dynamodb_table = "{self.project_name}-terraform-locks"
'''
            self._write_file(env_path / "backend.tfvars", backend_content)

    def _generate_gitignore(self):
        """Generate .gitignore for Terraform project."""
        content = '''# Terraform
*.tfstate
*.tfstate.*
.terraform/
.terraform.lock.hcl
*.tfplan

# Crash log files
crash.log
crash.*.log

# Sensitive variable files
*.tfvars
!environments/*/terraform.tfvars
*.auto.tfvars

# Override files
override.tf
override.tf.json
*_override.tf
*_override.tf.json

# CLI configuration files
.terraformrc
terraform.rc

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
'''
        self._write_file(self.output_path / ".gitignore", content)


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Generate production-ready Terraform module templates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ./terraform --project myapp
  %(prog)s ./terraform --project myapp --modules vpc,ecs
  %(prog)s ./terraform --project myapp --environments dev,prod --region eu-west-1
        """
    )

    parser.add_argument(
        "output_path",
        help="Directory where Terraform files will be created"
    )
    parser.add_argument(
        "--project", "-p",
        default="myproject",
        help="Project name (default: myproject)"
    )
    parser.add_argument(
        "--modules", "-m",
        default="vpc,ecs,rds",
        help="Comma-separated list of modules to generate (default: vpc,ecs,rds)"
    )
    parser.add_argument(
        "--environments", "-e",
        default="dev,staging,prod",
        help="Comma-separated list of environments (default: dev,staging,prod)"
    )
    parser.add_argument(
        "--region", "-r",
        default="us-east-1",
        help="AWS region (default: us-east-1)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    modules = [m.strip() for m in args.modules.split(",")]
    environments = [e.strip() for e in args.environments.split(",")]

    scaffolder = TerraformScaffolder(
        output_path=args.output_path,
        project_name=args.project,
        modules=modules,
        environments=environments,
        aws_region=args.region,
        verbose=args.verbose
    )

    result = scaffolder.scaffold()

    if args.json:
        print(json.dumps(result, indent=2))
    elif result["status"] == "success":
        print(f"\nTerraform project scaffolded successfully!")
        print(f"\nNext steps:")
        print(f"  cd {args.output_path}")
        print(f"  terraform init")
        print(f"  terraform plan -var-file=environments/dev/terraform.tfvars")


if __name__ == "__main__":
    main()
