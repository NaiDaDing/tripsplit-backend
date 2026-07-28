output "ecr_repository_url" {
  description = "ECR repository URL for the backend image."
  value       = aws_ecr_repository.backend.repository_url
}

output "ecr_repository_arn" {
  description = "ECR repository ARN."
  value       = aws_ecr_repository.backend.arn
}

output "ecs_log_group_name" {
  description = "CloudWatch log group used by ECS backend tasks."
  value       = aws_cloudwatch_log_group.backend.name
}

output "alb_security_group_id" {
  description = "Security group ID for the TripSplit ALB."
  value       = aws_security_group.alb.id
}

output "backend_security_group_id" {
  description = "Security group ID for the TripSplit backend ECS tasks."
  value       = aws_security_group.backend.id
}