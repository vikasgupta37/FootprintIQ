variable "aws_region" {
  type        = string
  description = "AWS region for resources"
  default     = "us-east-1"
}

variable "environment" {
  type        = string
  description = "Target deployment environment (e.g. staging, production)"
  default     = "production"
}

variable "vpc_cidr" {
  type        = string
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

variable "backend_cpu" {
  type        = string
  description = "CPU units for backend service (1024 = 1 vCPU)"
  default     = "1024"
}

variable "backend_memory" {
  type        = string
  description = "Memory for backend service in MB"
  default     = "2048"
}

variable "frontend_cpu" {
  type        = string
  description = "CPU units for frontend service"
  default     = "512"
}

variable "frontend_memory" {
  type        = string
  description = "Memory for frontend service in MB"
  default     = "1024"
}

variable "db_instance_class" {
  type        = string
  description = "RDS instance class"
  default     = "db.t3.medium"
}

variable "redis_node_type" {
  type        = string
  description = "ElastiCache Redis node type"
  default     = "cache.t3.medium"
}
