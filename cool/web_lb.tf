# Web Target Group
resource "aws_lb_target_group" "web" {
  name        = "${var.app}-${var.env}-web"
  port        = local.web_container_port
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = local.vpc_id

  health_check {
    healthy_threshold   = 3
    interval            = 60
    matcher             = "202,200,307,404,302"
    path                = "/"
    port                = local.web_container_port
    protocol            = "HTTP"
    unhealthy_threshold = 3
  }
}
