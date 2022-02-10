#=================================================
#  APPLICATION LOAD BALANCER
#=================================================
resource "aws_security_group" "alb" {
  name        = "${var.app}-${var.env}-alb-sg"
  description = "Allowed ports into alb"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    "Name" = "${var.app}-${var.env}-alb-sg"
  }
}

module "alb" {
  source             = "cloudposse/alb/aws"
  version            = "0.35.3"
  namespace          = var.app
  stage              = var.env
  name               = "alb"
  http_enabled       = false
  idle_timeout       = var.idle_timeout
  internal           = false
  vpc_id             = var.vpc_id
  security_group_ids = [aws_security_group.alb.id]
  subnet_ids         = var.public_subnet_ids
  target_group_name  = "${var.app}-${var.env}-tg"
}

# ===================================
# Listener
# ===================================
resource "aws_lb_listener" "https" {
  load_balancer_arn = module.alb.alb_arn
  port              = 443
  protocol          = "HTTPS"
  certificate_arn   = module.acm.this_acm_certificate_arn

  default_action {
    type = "fixed-response"
    fixed_response {
      content_type = "text/plain"
      message_body = "${var.app}-${var.env} fixed response"
      status_code  = 200
    }
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = module.alb.alb_arn
  port              = 80
  protocol          = "HTTP"
  default_action {
    type = "fixed-response"
    fixed_response {
      content_type = "text/plain"
      message_body = "${var.app}-${var.env} fixed response"
      status_code  = 200
    }
  }
}
