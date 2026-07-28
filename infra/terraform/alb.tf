resource "aws_lb" "backend" {
  count = var.enable_alb ? 1 : 0

  name               = var.alb_name
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.public_subnet_ids

  tags = local.common_tags
}

resource "aws_lb_listener" "http" {
  count = var.enable_alb ? 1 : 0

  load_balancer_arn = aws_lb.backend[0].arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backend.arn
  }

  tags = local.common_tags
}