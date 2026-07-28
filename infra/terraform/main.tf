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

resource "aws_lb_target_group" "backend" {
  name        = "tripsplit-backend-tg"
  port        = var.backend_container_port
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    enabled             = true
    path                = var.backend_health_check_path
    matcher             = "200"
    protocol            = "HTTP"
    port                = "traffic-port"
    healthy_threshold   = 5
    unhealthy_threshold = 2
    interval            = 30
    timeout             = 5
  }

  tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
  }
}

resource "aws_ecs_cluster" "main" {
  name = var.ecs_cluster_name

  tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
  }
}

resource "aws_ecs_service" "backend" {
  name            = var.ecs_service_name
  cluster         = aws_ecs_cluster.main.id
  task_definition = "tripsplit-backend"
  desired_count   = 0
  launch_type     = "FARGATE"

  enable_ecs_managed_tags = true

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  network_configuration {
    subnets          = var.public_subnet_ids
    security_groups  = [aws_security_group.backend.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.backend.arn
    container_name   = "tripsplit-backend"
    container_port   = var.backend_container_port
  }

  lifecycle {
    ignore_changes = [
      desired_count,
      task_definition,
      load_balancer,
    ]
  }

  tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
  }
}