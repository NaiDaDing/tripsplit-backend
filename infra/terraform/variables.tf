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

variable "backend_container_port" {
  description = "Port exposed by the TripSplit backend container."
  type        = number
  default     = 8000
}

variable "backend_health_check_path" {
  description = "Health check path for the TripSplit backend target group."
  type        = string
  default     = "/healthz"
}

variable "ecs_cluster_name" {
  description = "Name of the TripSplit ECS cluster."
  type        = string
  default     = "tripsplit-cluster"
}

variable "ecs_service_name" {
  description = "Name of the TripSplit ECS service."
  type        = string
  default     = "tripsplit-backend-service-qzrpnmt5"
}

variable "public_subnet_ids" {
  description = "Public subnet IDs used by the ECS service."
  type        = list(string)
  default = [
    "subnet-02a3b0fc1884863f6",
    "subnet-0bc74c9d98a2fbefe",
    "subnet-0ea3d53c06a8c00e7",
  ]
}