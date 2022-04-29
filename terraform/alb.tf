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

  egress {
    description = "Allow outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    "Name" = "${var.app}-${var.env}-alb-sg"
  }
}

resource "aws_lb" "alb" {
  name               = "${var.app}-${var.env}-public"
  idle_timeout       = 600
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.public_subnet_ids
}

# ===================================
# Listener
# ===================================
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.alb.arn
  port              = 443
  protocol          = "HTTPS"
  certificate_arn   = module.acm.acm_certificate_arn

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
  load_balancer_arn = aws_lb.alb.arn
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
