# ===========================
# ALB TARGET GROUP
# ===========================
resource "aws_lb_target_group" "ui" {
  name        = local.ui_name
  port        = local.ui_container_port
  protocol    = local.ui_container_protocol
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    healthy_threshold   = 3
    interval            = 120
    matcher             = "202,200,307,404,302"
    path                = "/"
    port                = local.ui_container_port
    protocol            = local.ui_container_protocol
    unhealthy_threshold = 5
  }
}

#=========================
# ALB LISTENER RULE
#=========================
resource "aws_lb_listener_rule" "ui" {
  listener_arn = aws_lb_listener.https.arn
  priority     = 500

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.ui.arn
  }

  condition {
    path_pattern {
      values = ["/", "/*", "*"]
    }
  }
}
