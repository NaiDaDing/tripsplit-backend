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

resource "aws_security_group" "alb" {
  name        = "tripsplit-alb-sg"
  description = "Allow HTTP access to TripSplit ALB"
  vpc_id      = var.vpc_id

  tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
  }

  lifecycle {
    ignore_changes = [ingress, egress]
  }
}

resource "aws_security_group" "backend" {
  name        = "tripsplit-backend-sg"
  description = "Allow HTTP access to TripSplit backend task"
  vpc_id      = var.vpc_id

  tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
  }

  lifecycle {
    ignore_changes = [ingress, egress]
  }
}