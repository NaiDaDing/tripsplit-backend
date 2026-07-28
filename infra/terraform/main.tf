resource "aws_ecr_repository" "backend" {
  name                 = var.ecr_repository_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
  }
}

resource "aws_cloudwatch_log_group" "backend" {
  name              = var.ecs_log_group_name
  retention_in_days = 14

  tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
  }
}