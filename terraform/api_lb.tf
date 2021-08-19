# ===========================
# ALB TARGET GROUPS
# ===========================
resource "aws_lb_target_group" "api" {
  name        = local.api_name
  port        = local.api_container_port
  protocol    = local.api_container_protocol
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    healthy_threshold   = 3
    interval            = 60
    matcher             = "200"
    path                = "/"
    port                = local.api_container_port
    protocol            = local.api_container_protocol
    unhealthy_threshold = 3
  }
}

resource "aws_lb_target_group" "landing" {
  name        = local.api_name
  port        = local.landing_container_port
  protocol    = local.landing_container_protocol
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    healthy_threshold   = 3
    interval            = 60
    matcher             = "404"
    path                = "/"
    port                = local.landing_container_port
    protocol            = local.landing_container_protocol
    unhealthy_threshold = 3
  }
}

#=========================
# ALB LISTENER RULE
#=========================
resource "aws_lb_listener_rule" "api" {
  listener_arn = aws_lb_listener.https.arn
  priority     = 100

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api.arn
  }

  condition {
    path_pattern {
      values = ["/api/*", "/api/", "/api"]
    }
  }
}
