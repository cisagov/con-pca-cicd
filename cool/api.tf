locals {
  api_container_port          = 80
  api_container_protocol      = "HTTP"
  api_load_balancer_port      = 8043
  api_load_balancer_http_port = 8000
  api_name                    = "${var.app}-${var.env}-api"
}

# ===========================
# SECURITY GROUP
# ===========================
resource "aws_security_group" "api" {
  name        = "${local.api_name}-alb"
  description = "Allow traffic for api from alb"
  vpc_id      = aws_vpc.vpc.id

  ingress {
    description     = "Allow container port from ALB"
    from_port       = local.api_container_port
    to_port         = local.api_container_port
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
    self            = true
  }

  egress {
    description = "Allow outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    "Name" = "${local.api_name}-alb"
  }
}
