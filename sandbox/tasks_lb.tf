# ===========================
# ALB TARGET GROUPS
# ===========================
resource "aws_lb_target_group" "tasks" {
  name        = local.tasks_name
  port        = local.tasks_container_port
  protocol    = local.tasks_container_protocol
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    healthy_threshold   = 3
    interval            = 60
    matcher             = "200,404"
    path                = "/"
    port                = local.tasks_container_port
    protocol            = local.tasks_container_protocol
    unhealthy_threshold = 3
  }
}


#=========================
# ALB LISTENER RULE
#=========================
resource "aws_lb_listener_rule" "tasks" {
  listener_arn = aws_lb_listener.https.arn
  priority     = 300

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tasks.arn
  }

  condition {
    path_pattern {
      values = ["/tasks/*", "/tasks/", "/tasks"]
    }
  }
}
