variable "aws_region" {
  description = "AWS region for TripSplit infrastructure."
  type        = string
  default     = "ap-northeast-1"
}

variable "aws_profile" {
  description = "Local AWS CLI profile used by Terraform."
  type        = string
  default     = "tripsplit"
}

variable "project_name" {
  description = "Project name used for AWS resource naming."
  type        = string
  default     = "tripsplit"
}

variable "ecr_repository_name" {
  description = "ECR repository name for the backend Docker image."
  type        = string
  default     = "tripsplit-backend"
}

variable "ecs_log_group_name" {
  description = "CloudWatch log group name for ECS backend task logs."
  type        = string
  default     = "/ecs/tripsplit-backend"
}

variable "vpc_id" {
  description = "VPC ID for TripSplit AWS networking resources."
  type        = string
  default     = "vpc-0ab2969739373e6eb"
}