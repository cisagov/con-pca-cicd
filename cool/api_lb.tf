# Api Target Group
resource "aws_lb_target_group" "api" {
  name        = "${var.app}-${var.env}-api"
  port        = local.api_container_port
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = local.vpc_id

  health_check {
    healthy_threshold   = 3
    interval            = 60
    matcher             = "200"
    path                = "/"
    port                = local.api_container_port
    protocol            = "HTTP"
    unhealthy_threshold = 3
  }
}

# Api Listener Rule
resource "aws_lb_listener_rule" "api" {
  listener_arn = aws_lb_listener.internal_https.arn
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

# Landing Page Target Group
resource "aws_lb_target_group" "landing" {
  name        = "${var.app}-${var.env}-landing"
  port        = local.landing_container_port
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = local.vpc_id

  health_check {
    healthy_threshold   = 3
    interval            = 60
    matcher             = "200,404"
    path                = "/"
    port                = local.landing_container_port
    unhealthy_threshold = 3
  }
}
